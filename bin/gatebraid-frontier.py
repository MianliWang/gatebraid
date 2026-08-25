#!/usr/bin/env python3
"""gatebraid-frontier - the snapshot consumer and verdict emitter (M3 node O0, T2).

Reads a `gatebraid/snapshot@1` document, VALIDATES IT AGAINST THE FROZEN SCHEMA
BEFORE READING ANY FIELD OF IT, and only then emits verdicts.

HOW "NO VERDICT WITHOUT VALIDATION" IS ENFORCED, structurally rather than by
discipline
---------------------------------------------------------------------------
A comment saying `validate first` is worth nothing; the next edit moves a read
above it.  So the consumable form of a snapshot is a distinct type,
`ValidatedSnapshot`, whose constructor refuses to build without a token that
only `validate()` holds.  Every verdict-emitting path takes a `ValidatedSnapshot`
and there is no other way to reach one.  A future edit that tries to consume raw
parsed JSON does not produce a wrong verdict - it raises, because the object it
needs cannot be conjured.  That is the difference between a checked property and
an intended one, and this Slice's negative criterion N4 scans for exactly it.

THE CONSUMING HALF OF THE BYTE CONTRACT (P0-2)
----------------------------------------------
The document is read as BYTES and decoded as UTF-8 explicitly, never through the
inherited console text layer.  On this host a `cp936` console mangles every
non-ASCII byte, including the U+2014 EM DASH that four of the fourteen
`Workflow` values carry - and a mangled `Workflow` is not merely cosmetic, it
fails the closed-enumeration match and would silently become `UNKNOWN`.  A
decode failure is a REFUSAL, never a lossy replacement: `errors="replace"` here
would manufacture exactly the corruption the contract exists to detect.

WHY THE PRODUCER'S OWN VERDICT IS NOT TRUSTED
---------------------------------------------
The document carries a `verdict` per item and this tool RE-DERIVES it rather
than reading it.  Where the re-derivation and the declared verdict disagree, the
result is `undecidable` and the disagreement is named in the item's reasons - a
consumer that echoed the producer's verdict would inherit every producer defect
silently, which is the whole failure mode O0 exists to remove.

P0-4, clause by clause, each forcing `undecidable` rather than a default
-----------------------------------------------------------------------
  * `schema` and `snapshot_version` present and recognised, checked BEFORE
    consumption - an unrecognised document is refused, never read as current.
  * `issue_state` from the closed enumeration; `UNKNOWN` yields `undecidable`,
    never unblocked.
  * a verdict ONLY for an item whose `slice_metadata_present` is true; an item
    without it carries `excluded_reason` and gets no verdict at all.
  * both dependency directions read and cross-checked; `mismatch` or
    `not_performed` yields `undecidable`.
  * a declared soft dependency parsed, or `parse_status: not_parsed`, which
    yields `undecidable`.
  * an `Aborted` workflow is never `startable` (ADR-0025 decision 8).
  * ANY degraded source yields `undecidable` for EVERY item.

Exit codes: 0 report emitted from a healthy snapshot - 1 the snapshot was
REFUSED and no verdict was emitted - 2 usage or input error - 3 report emitted
and every verdict is `undecidable` because the snapshot was degraded.
Python 3 standard library only at module level; the JSON Schema loader is
imported inside a function, guarded.
"""

import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)
SCHEMA_REL = os.path.join("schema", "snapshot.schema.json")

CONSUMER_NAME = "gatebraid-frontier"
CONSUMER_VERSION = "1.0.0"
REPORT_ID = "gatebraid/frontier-report@1"

SNAPSHOT_SCHEMA_ID = "gatebraid/snapshot@1"
SUPPORTED_SNAPSHOT_VERSIONS = (1,)


class InputError(Exception):
    """A usage or input failure. Exits 2."""


class SnapshotRefused(Exception):
    """The document is not a snapshot this tool may consume. Exits 1.

    Distinct from InputError on purpose: a refused snapshot is a MEASUREMENT
    about the document, and the caller must be able to tell it apart from its
    own mistake in invoking this tool.
    """


# The token that makes `ValidatedSnapshot` unforgeable from outside `validate`.
_VALIDATION_TOKEN = object()


class ValidatedSnapshot(object):
    """The ONLY carrier of a consumable snapshot.

    Constructed exclusively by `validate()`.  Every verdict-emitting function in
    this file takes one of these, so there is no reachable path from raw parsed
    JSON to a verdict.  See the module docstring.
    """

    def __init__(self, doc, schema_path, schema_sha256, token):
        if token is not _VALIDATION_TOKEN:
            raise SnapshotRefused(
                "a snapshot may only be consumed after validate() has accepted it")
        self._doc = doc
        self.schema_path = schema_path
        self.schema_sha256 = schema_sha256

    @property
    def sources(self):
        return self._doc["sources"]

    @property
    def items(self):
        return self._doc["items"]

    @property
    def generated_at(self):
        return self._doc["generated_at"]

    @property
    def snapshot_version(self):
        return self._doc["snapshot_version"]


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


def load_schema_validator(schema):
    """Import the JSON Schema loader lazily, guarded.

    `$id` is dropped for validation purposes for the reason recorded in
    `bin/gatebraid-validate.py`: the frozen `$id` values are identifiers rather
    than URLs and older loaders resolve local pointers against them and fail.
    Every `$ref` here is a local JSON pointer, so this changes where the resolver
    looks and not which documents validate.
    """
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise InputError(
            "STRUCTURE: the JSON Schema loader is unavailable (%s); this tool "
            "refuses to emit a verdict it could not validate first" % exc)
    resolvable = dict(schema)
    resolvable.pop("$id", None)
    return Draft202012Validator(resolvable)


# ------------------------------------------------------------- reading bytes

def read_document_bytes(path):
    """Read the document as BYTES. The consuming half of the byte contract."""
    if path == "-":
        stream = getattr(sys.stdin, "buffer", None)
        if stream is None:
            raise InputError("STRUCTURE: stdin has no binary layer; the byte "
                             "contract cannot be honoured")
        return stream.read()
    if not os.path.isfile(path):
        raise InputError("USAGE: no snapshot document at %s" % path)
    with open(path, "rb") as fh:
        return fh.read()


def decode_document(raw):
    """Decode UTF-8 STRICTLY. A decode failure is a refusal, never a repair."""
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SnapshotRefused(
            "the document is not valid UTF-8 (%s); a lossy decode here would "
            "manufacture the corruption the byte contract exists to detect" % exc)


# ---------------------------------------------------------------- validation

def validate(raw_bytes, schema, schema_path, schema_sha256):
    """Refuse or accept. The ONLY constructor of a consumable snapshot.

    Order matters and is asserted here: decode, parse, check the document's own
    identity, then validate structurally.  The identity check comes before the
    structural one so that an unrecognised `schema` value is reported as what it
    is rather than as a pile of downstream conditional failures.
    """
    text = decode_document(raw_bytes)
    try:
        doc = json.loads(text)
    except ValueError as exc:
        raise SnapshotRefused("the document is not valid JSON (%s)" % exc)
    if not isinstance(doc, dict):
        raise SnapshotRefused("the document is a %s where an object was required"
                              % type(doc).__name__)

    # P0-4's version check, before consumption and before any field is read for
    # meaning. `in` on a dict is not a read of the value.
    if "schema" not in doc:
        raise SnapshotRefused(
            "the document does not say what it is: `schema` is absent, so it "
            "cannot be consumed as if current")
    if doc["schema"] != SNAPSHOT_SCHEMA_ID:
        raise SnapshotRefused(
            "the document declares an interface this tool does not consume")
    if "snapshot_version" not in doc:
        raise SnapshotRefused("`snapshot_version` is absent")
    if doc["snapshot_version"] not in SUPPORTED_SNAPSHOT_VERSIONS:
        raise SnapshotRefused(
            "snapshot_version %r is outside this tool's supported set %r"
            % (doc["snapshot_version"], list(SUPPORTED_SNAPSHOT_VERSIONS)))

    validator = load_schema_validator(schema)
    errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))
    if errors:
        detail = "; ".join(
            "%s at %s" % (e.validator, "/".join(str(p) for p in e.absolute_path) or "(root)")
            for e in errors[:5])
        raise SnapshotRefused(
            "the document does not validate against %s (%d error locus/loci: %s)"
            % (SNAPSHOT_SCHEMA_ID, len(errors), detail))

    return ValidatedSnapshot(doc, schema_path, schema_sha256, _VALIDATION_TOKEN)


# ----------------------------------------------------------------- verdicts

def degraded_sources(snapshot):
    """Source entries that are not `ok` or not complete. Requires validation."""
    out = []
    for source in snapshot.sources:
        if source["status"] != "ok" or source["complete"] is False:
            out.append(source)
    return out


def derive_verdict(item, degraded):
    """Re-derive one item's verdict from the document's facts.

    Returns (verdict, reasons).  Every branch that is not provably clear returns
    `undecidable`; there is no default that resolves toward `startable`.  Fields
    read here are schema-required, so they are indexed rather than fetched with a
    default - a default on a verdict-relevant field is the fail-open shape this
    Slice's negative criterion N2 scans for.
    """
    reasons = []
    if degraded:
        reasons.append("a source is degraded, so no item can carry a verdict "
                       "other than undecidable")
        return "undecidable", reasons

    if item["issue_state"] == "UNKNOWN":
        reasons.append("the Issue state did not map into the closed enumeration; "
                       "an unrecognised state is undecidable, never unblocked")
        return "undecidable", reasons

    cross = item["dependencies"]["cross_check"]
    if cross == "not_performed":
        reasons.append("the two dependency directions were never cross-checked")
        return "undecidable", reasons
    if cross == "mismatch":
        reasons.append("the two dependency directions disagree")
        return "undecidable", reasons

    soft = item["soft_dependencies"]
    if soft["parse_status"] == "not_parsed":
        reasons.append("a declared soft dependency was not parsed, and an "
                       "unparsed declaration cannot leave the item startable")
        return "undecidable", reasons

    workflow = item["workflow"]
    if workflow == "UNKNOWN":
        reasons.append("the Workflow value did not map into the closed enumeration")
        return "undecidable", reasons
    if workflow == "Aborted":
        reasons.append("an Aborted slice is never a candidate (ADR-0025 "
                       "decision 8), whatever its edges say")
        return "blocked", reasons

    open_edges = [e["issue"] for e in item["dependencies"]["blocked_by"]
                  if e["state"] == "OPEN"]
    unknown_edges = [e["issue"] for e in item["dependencies"]["blocked_by"]
                     if e["state"] == "UNKNOWN"]
    if unknown_edges:
        reasons.append("a blocking edge carries an unrecognised state (%d edge(s))"
                       % len(unknown_edges))
        return "undecidable", reasons
    if open_edges:
        reasons.append("blocked by %d open dependency/dependencies" % len(open_edges))
        return "blocked", reasons

    reasons.append("every dependency is closed, both directions agree, and the "
                   "sources read completely")
    return "startable", reasons


def consume(snapshot):
    """Emit verdicts. Takes a ValidatedSnapshot and nothing else.

    This signature IS the N4 guarantee: there is no way to call this with a
    document that has not been through `validate()`.
    """
    degraded = degraded_sources(snapshot)
    is_degraded = bool(degraded)

    verdicts = []
    excluded = []
    for item in snapshot.items:
        if item["slice_metadata_present"] is False:
            # No verdict at all - not `undecidable`, not absent-and-unexplained.
            excluded.append({
                "item_id": item["item_id"],
                "issue": item["issue"],
                "excluded_reason": item["excluded_reason"],
            })
            continue

        derived, reasons = derive_verdict(item, is_degraded)
        declared = item["verdict"]
        if declared != derived:
            # The producer's verdict is not trusted. A disagreement is itself a
            # degradation: something in the chain is wrong and which half is
            # wrong is not knowable from here.
            reasons.append("the document declares %r where re-derivation yields "
                           "%r; a disagreement is undecidable, not a vote"
                           % (declared, derived))
            derived = "undecidable"
        verdicts.append({
            "item_id": item["item_id"],
            "issue": item["issue"],
            "slice_id": item["slice_id"],
            "workflow": item["workflow"],
            "verdict": derived,
            "declared_verdict": declared,
            "reasons": reasons,
        })

    summary = {
        "startable": sum(1 for v in verdicts if v["verdict"] == "startable"),
        "blocked": sum(1 for v in verdicts if v["verdict"] == "blocked"),
        "undecidable": sum(1 for v in verdicts if v["verdict"] == "undecidable"),
        "excluded": len(excluded),
    }
    return {
        "report": REPORT_ID,
        "consumer": {"name": CONSUMER_NAME, "version": CONSUMER_VERSION},
        "snapshot": {
            "generated_at": snapshot.generated_at,
            "snapshot_version": snapshot.snapshot_version,
            "validated_against": snapshot.schema_path,
            "schema_sha256": snapshot.schema_sha256,
        },
        "snapshot_degraded": is_degraded,
        "degraded_sources": [
            {"source_id": s["source_id"], "status": s["status"],
             "complete": s["complete"]} for s in degraded],
        "verdicts": verdicts,
        "excluded": excluded,
        "summary": summary,
    }, is_degraded


def encode_report(report):
    return (json.dumps(report, ensure_ascii=False, indent=1, sort_keys=True)
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
        prog="gatebraid-frontier",
        description="Consume a gatebraid/snapshot@1 document and emit verdicts.")
    ap.add_argument("snapshot", help="path to the snapshot document, or - for stdin")
    ap.add_argument("--out", metavar="PATH",
                    help="write the report here (binary); default is binary stdout")
    ap.add_argument("--schema", metavar="PATH", help="override the frozen schema path")
    args = ap.parse_args(argv)

    try:
        schema, schema_path, schema_sha = load_schema(args.schema)
        raw = read_document_bytes(args.snapshot)
    except InputError as exc:
        sys.stderr.write("%s\n" % exc)
        return 2

    try:
        snapshot = validate(raw, schema, schema_path, schema_sha)
    except SnapshotRefused as exc:
        sys.stderr.write("SNAPSHOT REFUSED: %s\n" % exc)
        sys.stderr.write("verdicts emitted             : 0 "
                         "(no verdict is emitted for a document this tool "
                         "could not validate)\n")
        return 1
    except InputError as exc:
        sys.stderr.write("%s\n" % exc)
        return 2

    report, is_degraded = consume(snapshot)
    emit(encode_report(report), args.out)

    s = report["summary"]
    sys.stderr.write("consumer                      : %s %s\n"
                     % (CONSUMER_NAME, CONSUMER_VERSION))
    sys.stderr.write("validated against             : %s sha256=%s\n"
                     % (schema_path, schema_sha))
    sys.stderr.write("items excluded (no verdict)   : %d\n" % s["excluded"])
    sys.stderr.write("startable                     : %d\n" % s["startable"])
    sys.stderr.write("blocked                       : %d\n" % s["blocked"])
    sys.stderr.write("undecidable                   : %d\n" % s["undecidable"])
    if is_degraded:
        sys.stderr.write("FRONTIER UNDECIDABLE: the snapshot is degraded in %d "
                         "source(s), so every item is undecidable\n"
                         % len(report["degraded_sources"]))
        return 3
    sys.stderr.write("FRONTIER OK: the snapshot validated and every verdict was "
                     "re-derived from it\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
