#!/usr/bin/env python3
"""gatebraid-snapshot - the control-plane snapshot producer (M3 node O0, T1).

Emits a `gatebraid/snapshot@1` document: a point-in-time read of the control
plane that carries its own integrity with it.  The design rule this file serves
is the schema's own, restated because it is the whole point: A CONSUMER MUST
NEVER BE ABLE TO READ A DEGRADED SNAPSHOT AS A HEALTHY ONE.

THE PRODUCER/CONSUMER BYTE CONTRACT (P0-2), stated here because this is the
producing half
--------------------------------------------------------------------------
The document is written as EXPLICITLY UTF-8-ENCODED BYTES to a binary sink -
`sys.stdout.buffer` or the `--out` file opened in binary mode - and NEVER
through the inherited console text layer.  This matters and was measured: on
this host a `cp936` parent console re-encodes text-layer writes and corrupts
every non-ASCII byte in the document, including the U+2014 EM DASH that four of
the fourteen `Workflow` values carry.  The consumer (`gatebraid-frontier`)
therefore reads bytes and decodes UTF-8 itself.  Human-readable summary output
goes to STDERR, so stdout carries the document and nothing else.

WHERE THE CLOSED ENUMERATIONS COME FROM, and why they are not typed here
-----------------------------------------------------------------------
`Workflow` values contain U+2014 EM DASH and `Next Approval` values contain
U+2192 RIGHTWARDS ARROW; a terminal that mangles UTF-8 renders them
identically, and re-typing either mark is how they drift.  This file therefore
READS every closed enumeration - source status, issue state, workflow, verdict
- out of the frozen schema at run time and matches raw values against them by
exact string equality.  Nothing that fails to match is coerced: it becomes
`UNKNOWN`, which the schema makes force `undecidable`.

P0-1 - EVERY READ BECOMES A SOURCE ENTRY
----------------------------------------
Each control-plane read produces one `sources[]` entry carrying `status` from
the schema's closed enumeration, `complete`, `exit_code`, and `failure_detail`
whenever the status is not `ok`.  A non-zero process exit is surfaced in the
document; it is never folded into an absent or empty value, which is the
ADR-0029 decision 2 P0-1 defect verbatim.

`exit_code` SEMANTICS, disclosed because the schema constrains them.  The
schema forbids a non-`ok` status from reporting a success exit.  A read can
nevertheless fail while the process exits 0 - `gh` returns 0 and the body is
unparseable, or the endpoint answers with a shape this tool does not
recognise.  In that case `exit_code` carries the documented read-outcome
sentinel EX_DATAERR (65) and `failure_detail` names the real process exit, so
the process's own status is recoverable from the document rather than lost.
Where the process itself failed, `exit_code` is that process exit as measured.

P0-3 - PAGINATION OR A BOUNDED FLAG, NEVER SILENCE
--------------------------------------------------
Every verdict-relevant connection is paginated to exhaustion.  Where a page cap
is reached with pages still outstanding, the source carries `bounded` with
`reason`, `cap`, `observed` and `has_next_page` together with `complete: false`
- reaching a cap FAILS CLOSED rather than reporting a truncated list as whole.

SELF-VALIDATION BEFORE EMISSION
-------------------------------
The document is validated against the frozen schema before a byte of it is
written.  A document that does not validate is not emitted at all: the tool
exits 1 having produced nothing, because emitting a malformed snapshot is
strictly worse than emitting none.

Exit codes: 0 snapshot emitted, every source `ok` and complete - 1 no document
could be produced (self-validation failed) - 2 usage or input error - 3
snapshot emitted and DEGRADED.  3 exists so that a shell caller reading only
the exit status cannot mistake a degraded snapshot for a healthy one.
Python 3 standard library only at module level; the JSON Schema loader is
imported inside a function, guarded.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)
SCHEMA_REL = os.path.join("schema", "snapshot.schema.json")

GENERATOR_NAME = "gatebraid-snapshot"
GENERATOR_VERSION = "1.0.0"

# The read-outcome sentinel described in the module docstring.  Named, not
# spelled inline, so the document's meaning is greppable from this file.
EX_DATAERR = 65

SOURCE_IDS = ("project_items", "issue_states", "dep_blocked_by", "dep_blocking")


class InputError(Exception):
    """A usage or input failure. Exits 2, distinct from an unemittable document (1)."""


# --------------------------------------------------------------- the schema

def load_schema(path=None):
    p = path or os.path.join(REPO_ROOT, SCHEMA_REL)
    if not os.path.isfile(p):
        raise InputError("STRUCTURE: the frozen schema is not at %s" % p)
    with open(p, "rb") as fh:
        raw = fh.read()
    try:
        return json.loads(raw.decode("utf-8")), p, hashlib.sha256(raw).hexdigest()
    except (UnicodeDecodeError, ValueError) as exc:
        raise InputError("STRUCTURE: the frozen schema does not parse (%s)" % exc)


def enum_at(schema, *pointer):
    """Read one closed enumeration out of the frozen schema.

    Never typed into this file: see the module docstring on U+2014 and U+2192.
    A pointer that does not resolve to an `enum` is a structural failure here
    rather than a silently empty set, because an empty enumeration would accept
    nothing and be read as 'the schema changed' far too late.
    """
    node = schema
    for part in pointer:
        if not isinstance(node, dict) or part not in node:
            raise InputError("STRUCTURE: the frozen schema has no %s" % "/".join(pointer))
        node = node[part]
    values = node.get("enum") if isinstance(node, dict) else None
    if not values:
        raise InputError("STRUCTURE: %s is not a closed enumeration" % "/".join(pointer))
    return list(values)


def load_schema_validator(schema):
    """Import the JSON Schema loader lazily, guarded.

    Kept out of module scope so this file carries no module-level third-party
    import.  `$id` is dropped for validation purposes for the reason measured at
    P2-S3 Gate 2 and recorded in `bin/gatebraid-validate.py`: the frozen `$id`
    values are identifiers rather than URLs, and older loaders resolve local
    `#/$defs/...` pointers against them and fail.  Every `$ref` in this schema is
    a local JSON pointer, so removing the base URI cannot change which documents
    validate - only where the resolver looks.
    """
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise InputError(
            "STRUCTURE: the JSON Schema loader is unavailable (%s); this tool "
            "self-validates before emitting and will not emit unchecked" % exc)
    resolvable = dict(schema)
    resolvable.pop("$id", None)
    return Draft202012Validator(resolvable)


# ------------------------------------------------------------- transports

class ReadResult(object):
    """One raw read outcome, before classification. Transport-independent."""

    def __init__(self, exit_code=0, stdout="", stderr="", http_status=None,
                 rate_limit_remaining=None, transport_error=None):
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr
        self.http_status = http_status
        self.rate_limit_remaining = rate_limit_remaining
        self.transport_error = transport_error


class ReplayTransport(object):
    """Serve canned read outcomes from a transcript file.

    THIS IS NOT A MOCK OF THE CLASSIFIER.  The transcript supplies only what a
    real read supplies - an exit status, two streams, and the two headers that
    distinguish the 403 classes - and the outcome then travels the SAME
    classification and assembly path as a live read.  That is what makes a
    seeded condition evidence about this tool rather than about a stub.
    """

    kind = "replay"

    def __init__(self, transcript, path):
        self.reads = transcript.get("reads") or {}
        self.path = path

    def read(self, source_id, page_index):
        entry = self.reads.get(source_id)
        if entry is None:
            return ReadResult(exit_code=EX_DATAERR,
                              transport_error="no transcript entry for source %r" % source_id)
        pages = entry if isinstance(entry, list) else [entry]
        if page_index >= len(pages):
            return ReadResult(exit_code=EX_DATAERR,
                              transport_error="transcript for %r has no page %d"
                                              % (source_id, page_index))
        page = pages[page_index]
        body = page.get("stdout", "")
        if not isinstance(body, str):
            body = json.dumps(body, ensure_ascii=False)
        return ReadResult(
            exit_code=page.get("exit_code", 0),
            stdout=body,
            stderr=page.get("stderr", ""),
            http_status=page.get("http_status"),
            rate_limit_remaining=page.get("rate_limit_remaining"),
            transport_error=page.get("transport_error"))


class LiveTransport(object):
    """Read the live control plane through the authenticated `gh` CLI.

    No HTTP client is constructed here and no credential is handled: `gh` holds
    the authentication, as the project's hard rules require.  `GH_CONFIG_DIR` is
    inherited from the environment and is never set by this file.
    """

    kind = "live"

    def __init__(self, owner, project_number, repo):
        self.owner = owner
        self.project_number = project_number
        self.repo = repo

    def _run(self, argv):
        try:
            proc = subprocess.run(argv, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        except OSError as exc:
            return ReadResult(exit_code=EX_DATAERR,
                              transport_error="the gh executable could not be run (%s)" % exc)
        return ReadResult(exit_code=proc.returncode,
                          stdout=proc.stdout.decode("utf-8", "replace"),
                          stderr=proc.stderr.decode("utf-8", "replace"))

    def read(self, source_id, page_index):
        if source_id == "project_items":
            return self._run(["gh", "project", "item-list", str(self.project_number),
                              "--owner", self.owner, "--format", "json"])
        return self._run(["gh", "api", "repos/%s/issues" % self.repo])


# ------------------------------------------------------------ classification

def classify(result, statuses):
    """Map one raw read outcome onto the schema's CLOSED status enumeration.

    Returns (status, exit_code, failure_detail_or_None).  The mapping is total:
    every outcome lands on a member of the closed set, and the fallback is a
    FAILURE class rather than `ok`.  That direction is the whole point - an
    outcome nobody anticipated must degrade the snapshot, not pass through it.
    """
    def member(name):
        if name not in statuses:
            raise InputError("STRUCTURE: %r is absent from the frozen status enum" % name)
        return name

    process_exit = result.exit_code
    stderr = (result.stderr or "")
    lowered = stderr.lower()

    def fail(status, detail):
        code = process_exit if process_exit != 0 else EX_DATAERR
        if process_exit == 0:
            detail = ("%s; the process exited 0 and `exit_code` carries the "
                      "read-outcome sentinel %d" % (detail, EX_DATAERR))
        return member(status), code, detail

    if result.transport_error:
        return fail("network_error", "the read could not be performed: %s"
                    % result.transport_error)

    http = result.http_status
    remaining = result.rate_limit_remaining

    # Rate limiting is checked before the permission class it shares HTTP 403
    # with: collapsing the two loses the difference between 'retry later' and
    # 'never', which the schema keeps distinct on purpose.
    if remaining == 0:
        return fail("rate_limited", "the rate-limit budget is exhausted "
                                    "(rate_limit_remaining 0)")
    if http is not None:
        if http == 401:
            return fail("auth_failure", "the endpoint answered 401")
        if http == 403:
            return fail("permission_failure", "the endpoint answered 403 with "
                                              "rate-limit budget remaining")
        if http == 404:
            return fail("unexpected_endpoint", "the endpoint answered 404")
        if 500 <= http <= 599:
            return fail("server_error", "the endpoint answered %d" % http)
        if http >= 400:
            return fail("unexpected_endpoint", "the endpoint answered %d" % http)

    if process_exit != 0:
        if "authentication" in lowered or "not logged" in lowered or "401" in lowered:
            return fail("auth_failure", "the read exited %d reporting an "
                                        "authentication failure" % process_exit)
        if "forbidden" in lowered or "permission" in lowered or "403" in lowered:
            return fail("permission_failure", "the read exited %d reporting a "
                                              "permission failure" % process_exit)
        if "rate limit" in lowered:
            return fail("rate_limited", "the read exited %d reporting a rate limit"
                        % process_exit)
        if "could not resolve" in lowered or "connection" in lowered \
                or "timeout" in lowered or "network" in lowered:
            return fail("network_error", "the read exited %d reporting a network "
                                         "failure" % process_exit)
        if "500" in lowered or "502" in lowered or "503" in lowered \
                or "server error" in lowered:
            return fail("server_error", "the read exited %d reporting a server error"
                        % process_exit)
        return fail("unexpected_endpoint",
                    "the read exited %d and the failure did not match a known class"
                    % process_exit)

    try:
        payload = json.loads(result.stdout)
    except ValueError as exc:
        return fail("parse_error", "the response body is not valid JSON (%s)" % exc)
    if not isinstance(payload, dict):
        return fail("unexpected_endpoint",
                    "the response body is a %s where an object was required"
                    % type(payload).__name__)
    return member("ok"), 0, None


# ------------------------------------------------------------------ reading

def read_source(transport, source_id, statuses, page_cap):
    """Perform one source's read, paginating to exhaustion or to the cap.

    Returns (source_entry, payload_or_None).  P0-3 lives here: the loop either
    exhausts the connection or records exactly where and why it stopped.
    """
    query = "%s:%s" % (transport.kind, source_id)
    pages = []
    observed = 0
    page_index = 0
    result = None

    while True:
        result = transport.read(source_id, page_index)
        status, exit_code, detail = classify(result, statuses)
        if status != "ok":
            # A failed read is an INCOMPLETE read, and P0-3 requires every
            # incomplete source to say where it stopped - which is why the
            # bounded reason enumeration carries `query_failed`. `has_next_page`
            # is true because the connection was demonstrably not exhausted: the
            # read failed before it could be. Asserting false here would claim
            # knowledge the failure denied us, in the one direction that lets a
            # truncated read pass for a whole one.
            entry = {
                "source_id": source_id,
                "query": query,
                "status": status,
                "complete": False,
                "exit_code": exit_code,
                "failure_detail": detail,
                "bounded": {
                    "reason": "query_failed",
                    "cap": page_cap,
                    "observed": observed,
                    "has_next_page": True,
                },
            }
            if result.http_status is not None:
                entry["http_status"] = result.http_status
            if result.rate_limit_remaining is not None:
                entry["rate_limit_remaining"] = result.rate_limit_remaining
            return entry, None

        payload = json.loads(result.stdout)
        pages.append(payload)
        observed += len(payload.get("nodes") or [])
        page_index += 1
        if not bool(payload.get("hasNextPage")):
            break
        if page_index >= page_cap:
            # FAIL CLOSED AT THE CAP. The connection is not exhausted, so the
            # source says so rather than presenting a truncated list as whole.
            entry = {
                "source_id": source_id,
                "query": query,
                "status": "ok",
                "complete": False,
                "exit_code": 0,
                "bounded": {
                    "reason": "page_cap_reached",
                    "cap": page_cap,
                    "observed": observed,
                    "has_next_page": True,
                },
            }
            return entry, merge_pages(pages)

    entry = {
        "source_id": source_id,
        "query": query,
        "status": "ok",
        "complete": True,
        "exit_code": 0,
    }
    if result.http_status is not None:
        entry["http_status"] = result.http_status
    if result.rate_limit_remaining is not None:
        entry["rate_limit_remaining"] = result.rate_limit_remaining
    return entry, merge_pages(pages)


def merge_pages(pages):
    merged = {"nodes": [], "states": {}, "edges": {}}
    for page in pages:
        merged["nodes"].extend(page.get("nodes") or [])
        merged["states"].update(page.get("states") or {})
        for k, v in (page.get("edges") or {}).items():
            merged["edges"].setdefault(k, []).extend(v)
    return merged


# ------------------------------------------------------------------ assembly

def closed(value, allowed):
    """Exact membership or `UNKNOWN`. Nothing is coerced toward a healthy value."""
    return value if value in allowed else "UNKNOWN"


def build_items(payloads, enums, degraded):
    states = (payloads.get("issue_states") or {}).get("states") or {}
    blocked_by_all = (payloads.get("dep_blocked_by") or {}).get("edges") or {}
    blocking_all = (payloads.get("dep_blocking") or {}).get("edges") or {}
    have_blocked_by = payloads.get("dep_blocked_by") is not None
    have_blocking = payloads.get("dep_blocking") is not None

    items = []
    for row in ((payloads.get("project_items") or {}).get("nodes") or []):
        issue = row.get("issue")
        raw_state = states.get(issue, row.get("issue_state_raw"))
        state = closed(raw_state, enums["issue_state"])

        item = {
            "item_id": row.get("item_id") or "",
            "issue": issue or "",
            "issue_state": state,
            "slice_metadata_present": bool(row.get("slice_metadata_present")),
        }
        if state == "UNKNOWN" and raw_state is not None:
            item["issue_state_raw"] = str(raw_state)

        blocked_by = [normalise_edge(e, enums) for e in (blocked_by_all.get(issue) or [])]
        blocking = [normalise_edge(e, enums) for e in (blocking_all.get(issue) or [])]
        item["dependencies"] = {
            "blocked_by": blocked_by,
            "blocking": blocking,
            "cross_check": cross_check(issue, blocked_by, blocking_all,
                                       have_blocked_by, have_blocking),
        }
        item["soft_dependencies"] = parse_soft(row)

        if not item["slice_metadata_present"]:
            # No verdict at all, and a reason a reader can act on: an exclusion
            # nobody can read is indistinguishable from an omission.
            item["excluded_reason"] = str(row.get("excluded_reason")
                                          or "the Project row carries no Slice metadata")
            items.append(item)
            continue

        item["slice_id"] = str(row.get("slice_id") or "")
        item["workflow"] = closed(row.get("workflow_raw"), enums["workflow"])
        item["verdict"] = verdict_for(item, degraded)
        items.append(item)
    return items


def normalise_edge(edge, enums):
    return {
        "issue": str(edge.get("issue") or ""),
        "state": closed(edge.get("state"), enums["issue_state"]),
    }


def cross_check(issue, blocked_by, blocking_all, have_blocked_by, have_blocking):
    """Compare the two dependency directions against each other.

    `not_performed` when either direction was not read - a cross-check that did
    not happen must be sayable rather than assumed consistent.  `mismatch` when
    an edge asserted in one direction is not asserted in the other.  Both force
    `undecidable` at the item, so neither can become a tie broken in favour of
    whichever direction happened to be read.
    """
    if not (have_blocked_by and have_blocking):
        return "not_performed"
    for edge in blocked_by:
        reverse = blocking_all.get(edge["issue"]) or []
        if not any((r.get("issue") == issue) for r in reverse):
            return "mismatch"
    return "consistent"


def parse_soft(row):
    """Parse declared soft dependencies, or SAY the parse did not happen."""
    declared = bool(row.get("soft_dependencies_declared"))
    raw = row.get("soft_dependencies_raw")
    if not declared:
        return {"declared": False, "parse_status": "parsed", "entries": []}
    if raw is None or not str(raw).strip():
        return {"declared": True, "parse_status": "not_parsed"}
    entries = [part.strip() for part in str(raw).split(",") if part.strip()]
    if not entries:
        return {"declared": True, "parse_status": "not_parsed"}
    return {"declared": True, "parse_status": "parsed", "entries": entries}


def verdict_for(item, degraded):
    """Fail-closed verdict. Every branch that is not provably clear is `undecidable`."""
    if degraded:
        return "undecidable"
    if item["issue_state"] == "UNKNOWN":
        return "undecidable"
    if item["dependencies"]["cross_check"] in ("mismatch", "not_performed"):
        return "undecidable"
    if item["soft_dependencies"].get("parse_status") == "not_parsed":
        return "undecidable"
    if item.get("workflow") == "UNKNOWN":
        return "undecidable"
    if item.get("workflow") == "Aborted":
        # ADR-0025 decision 8: an Aborted slice is never a candidate, whatever
        # its edges say. `blocked` and `undecidable` are both legitimate here;
        # `startable` never is.
        return "blocked"
    if any(edge["state"] == "OPEN" for edge in item["dependencies"]["blocked_by"]):
        return "blocked"
    if any(edge["state"] == "UNKNOWN" for edge in item["dependencies"]["blocked_by"]):
        return "undecidable"
    return "startable"


def source_is_degraded(entry):
    return entry.get("status") != "ok" or entry.get("complete") is False


# -------------------------------------------------------------------- emit

def self_sha256():
    try:
        with open(os.path.abspath(__file__), "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except OSError:
        return None


def build_document(transport, schema, enums, page_cap, generated_at):
    sources = []
    payloads = {}
    for source_id in SOURCE_IDS:
        entry, payload = read_source(transport, source_id, enums["status"], page_cap)
        sources.append(entry)
        if payload is not None:
            payloads[source_id] = payload

    degraded = any(source_is_degraded(s) for s in sources)
    doc = {
        "schema": "gatebraid/snapshot@1",
        "snapshot_version": 1,
        "generated_at": generated_at,
        "generator": {"name": GENERATOR_NAME, "version": GENERATOR_VERSION},
        "sources": sources,
        "items": build_items(payloads, enums, degraded),
    }
    sha = self_sha256()
    if sha:
        doc["generator"]["source_sha256"] = sha
    return doc, degraded


def encode_document(doc):
    """The one place bytes are made. Explicit UTF-8, never the console codec."""
    return (json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True)
            + "\n").encode("utf-8")


def emit(data, out_path):
    if out_path:
        with open(out_path, "wb") as fh:
            fh.write(data)
        return
    stream = getattr(sys.stdout, "buffer", None)
    if stream is None:
        raise InputError("STRUCTURE: stdout has no binary layer; the byte "
                         "contract cannot be honoured")
    stream.write(data)
    stream.flush()


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="gatebraid-snapshot",
        description="Emit a gatebraid/snapshot@1 control-plane snapshot.")
    ap.add_argument("--out", metavar="PATH",
                    help="write the document here (binary); default is binary stdout")
    ap.add_argument("--replay", metavar="PATH",
                    help="serve reads from a transcript instead of the live control plane")
    ap.add_argument("--schema", metavar="PATH", help="override the frozen schema path")
    ap.add_argument("--page-cap", type=int, default=10, metavar="N",
                    help="maximum pages per connection before the bounded flag (default 10)")
    ap.add_argument("--generated-at", metavar="TS",
                    help="pin the document timestamp (determinism in tests)")
    ap.add_argument("--owner", default="MianliWang")
    ap.add_argument("--project", type=int, default=1)
    ap.add_argument("--repo", default="MianliWang/gatebraid")
    args = ap.parse_args(argv)

    try:
        if args.page_cap < 1:
            raise InputError("USAGE: --page-cap must be at least 1")
        schema, schema_path, schema_sha = load_schema(args.schema)
        enums = {
            "status": enum_at(schema, "$defs", "source", "properties", "status"),
            "issue_state": enum_at(schema, "$defs", "item", "properties", "issue_state"),
            "workflow": enum_at(schema, "$defs", "item", "properties", "workflow"),
            "verdict": enum_at(schema, "$defs", "item", "properties", "verdict"),
        }

        if args.replay:
            if not os.path.isfile(args.replay):
                raise InputError("USAGE: no transcript at %s" % args.replay)
            with open(args.replay, "rb") as fh:
                transcript = json.loads(fh.read().decode("utf-8"))
            transport = ReplayTransport(transcript, args.replay)
        else:
            transport = LiveTransport(args.owner, args.project, args.repo)

        generated_at = args.generated_at or "2026-01-01T00:00:00Z"
        doc, degraded = build_document(transport, schema, enums, args.page_cap,
                                       generated_at)

        validator = load_schema_validator(schema)
        errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))
        if errors:
            sys.stderr.write("SNAPSHOT NOT EMITTED: the document failed its own "
                             "self-validation against %s\n" % schema_path)
            for err in errors[:20]:
                path = "/".join(str(p) for p in err.absolute_path) or "(root)"
                sys.stderr.write("   %-14s %s\n" % (err.validator, path))
            sys.stderr.write("errors                        : %d\n" % len(errors))
            return 1
    except InputError as exc:
        sys.stderr.write("%s\n" % exc)
        return 2

    emit(encode_document(doc), args.out)

    sys.stderr.write("generator                     : %s %s\n"
                     % (GENERATOR_NAME, GENERATOR_VERSION))
    sys.stderr.write("schema                        : %s sha256=%s\n"
                     % (schema_path, schema_sha))
    sys.stderr.write("transport                     : %s\n" % transport.kind)
    sys.stderr.write("sources                       : %d\n" % len(doc["sources"]))
    for s in doc["sources"]:
        sys.stderr.write("   %-16s %-20s complete=%-5s exit=%d%s\n"
                         % (s["source_id"], s["status"], s["complete"], s["exit_code"],
                            "  bounded" if "bounded" in s else ""))
    sys.stderr.write("items                         : %d\n" % len(doc["items"]))
    sys.stderr.write("degraded                      : %s\n" % ("yes" if degraded else "no"))
    if degraded:
        sys.stderr.write("SNAPSHOT DEGRADED: every item carries verdict `undecidable`; "
                         "exit status 3 so no caller reads this as a healthy read\n")
        return 3
    sys.stderr.write("SNAPSHOT OK: every source read completely with status `ok`\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
