#!/usr/bin/env python3
"""gatebraid-validate - the independent evidence validator (M3 node N3).

Re-derives verdicts for a Gatebraid evidence document from the document itself
plus the frozen schemas, and publishes a `gatebraid/coverage-report@1` saying
which properties it checked and on what basis.

WHAT THIS TOOL IS INDEPENDENT OF, and why the word matters
----------------------------------------------------------
M3-PLAN.md §2 N3 requires independence of the generator in BOTH imports and
authorship: "the authoring sessions receive the frozen schemas and the N1
corpus, never N2's implementation".  This file imports nothing from the
generator and was written without reading it.  Its inputs were
`schema/evidence-capture.schema.json`, `schema/gate-run-v2.schema.json`,
`schema/coverage-report.schema.json`, and the N1 corpus under `fixtures/`.

THE TRUST BOUNDARY, stated because a validator that hides it is worse than one
that has none
-----------------------------------------------------------------------------
This tool re-derives RECORD SEMANTICS.  It does NOT attest that the capture
event occurred as described - that a command ran, in that cwd, producing those
bytes.  Every property it accepts on the generator's word is emitted with
class `capture-trusted` and is labelled as such in the report, never credited
silently.  `replayed` is reserved for independent re-execution; this tool does
not re-execute captured commands, so that class is legitimately empty, which
`gatebraid/coverage-report@1` explicitly permits.

WHAT THE SCHEMAS CANNOT SAY, and this tool therefore must
---------------------------------------------------------
Each relation below is named by the frozen schemas themselves as inexpressible
in JSON Schema and delegated to this validator:
  * `ended_at >= started_at`                    (evidence-capture@1, ended_at)
  * a base64 payload's `sha256` and `byte_length`      (evidence-capture@1, data)
  * `sections_examined + len(unexamined) == sections_total`
                                                (coverage-report@1, completeness)
  * `replay.rederived_sha256` against the digest claimed
                                     (bytes-platform EXPECTATIONS known_limitation)
  * a report citing ITSELF as one of its two platforms          (same)
  * timestamp FIELD RANGES - the patterns are lexical only, so 2026-02-31 and a
    month of 13 both match and must be rejected here.

Exit codes: 0 accepted / all expectations met · 1 rejected or a mismatch ·
2 usage or input error.  Python 3 standard library only at module level; the
JSON Schema loader is imported inside a function, guarded, so this file adds no
module-level third-party dependency.
"""

import argparse
import base64
import binascii
import calendar
import datetime
import hashlib
import json
import os
import platform
import re
import sys

class InputError(Exception):
    """A usage or input failure. Exits 2, distinct from a rejected record (1)."""


VALIDATOR_NAME = "gatebraid-validate"
VALIDATOR_VERSION = "1.0.0"

SCHEMA_FOR = {
    "gatebraid/evidence-capture@1": "schema/evidence-capture.schema.json",
    "gatebraid/gate-run@2": "schema/gate-run-v2.schema.json",
    "gatebraid/metrics@1": "schema/metrics.schema.json",
    "gatebraid/coverage-report@1": "schema/coverage-report.schema.json",
}

TRUST_BOUNDARY = (
    "N3 independently re-derives record semantics from the captured evidence — "
    "it does not independently attest that the capture event occurred as described "
    "(that a command ran, in that cwd, with that unmodified output)."
)

RFC3339 = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})[Tt](\d{2}):(\d{2}):(\d{2})(\.\d+)?([Zz]|[+-]\d{2}:\d{2})$"
)

# A placeholder is a value shaped like a promise rather than a measurement.
# The pattern is deliberately structural: it matches angle-bracket stand-ins and
# ellipsis fillers without this file ever needing to carry an example of one.
PLACEHOLDER = re.compile(r"<[^>]{1,64}>|\.{3}|\bTBD\b|\bTODO\b")

# ---- the mention test (friction #169) ------------------------------------
# The rule above is correct about what it matches and wrong about what that
# means in a field whose job is to QUOTE foreign text. A captured command line
# may contain an ellipsis because the command did; a citation may abbreviate an
# identifier. Neither is a promise standing in for a measurement.
#
# A hit is reclassified as a MENTION only when BOTH hold:
#   (a) its locus is a command or citation field, and
#   (b) the hit matches one of two NAMED quoting forms.
# Everything else stays a finding. Locus alone is deliberately not enough: the
# same `/checks/N/command` locus carries GraphQL spreads that must be excused
# and elided command citations that must NOT be, and only the form separates
# the two populations.
#
# Mentions are recorded as a labelled property, never silently dropped.
MENTION_LOCUS = (
    re.compile(r"^/invocation/argv/\d+$"),      # a captured command's argv
    re.compile(r"^/checks/\d+/command$"),       # a gate record's command citation
    re.compile(r"^/notes$"),                    # the annotation / citation field
)

# Form 1: a GraphQL inline-fragment spread, `... on TypeName`.
MENTION_SPREAD = re.compile(r"\.{3}\s+on\s+[A-Za-z_][A-Za-z0-9_]*")
# Form 2: an intra-token identifier abbreviation - an ellipsis BOUNDED by
# identifier characters rather than standing alone as a token. An ellipsis with
# whitespace or punctuation beside it is standing in for omitted text and stays
# a finding, which is what keeps an elided command citation reportable.
MENTION_ABBREV = re.compile(r"[A-Za-z0-9_]\.{3}[A-Za-z0-9_]")


def _is_mention_locus(locus):
    """Is this a field whose job is to quote foreign text?"""
    return any(rx.match(locus) for rx in MENTION_LOCUS)


def _is_mention(text, match):
    """Is this PLACEHOLDER hit one of the two named quoting forms?"""
    if match.group(0) != "...":
        return False            # angle-bracket stand-ins and TBD/TODO never qualify
    if MENTION_SPREAD.match(text, match.start()):
        return True
    return bool(MENTION_ABBREV.match(text, max(0, match.start() - 1)))



# ----------------------------------------------------------------- loader

def load_schema_validator(schema):
    """Import the JSON Schema loader lazily.

    Kept out of module scope on purpose: the Slice's frozen negative criterion
    N-B forbids a module-level third-party import, and a guarded import inside a
    function is the documented exception.  Returns (validator, loader_string).
    """
    try:
        import jsonschema
        from jsonschema import Draft202012Validator
    except ImportError as exc:  # pragma: no cover - environment failure
        raise InputError("STRUCTURE: the JSON Schema loader is unavailable (%s)" % exc)
    try:
        import importlib.metadata as _md
        ver = _md.version("jsonschema")
    except Exception:
        ver = getattr(jsonschema, "__version__", "unknown")
    loader = "CPython %s (%s), jsonschema %s, Draft202012Validator" % (
        platform.python_version(), sys.executable, ver)

    # DUAL-PLATFORM DEFECT, measured at this Slice's Gate 2 and fixed here.
    # The frozen schemas declare `$id` values like `gatebraid/evidence-capture@1`,
    # which are identifiers rather than URLs. jsonschema 4.10.3 (the WSL loader)
    # treats `$id` as a base URI and resolves the internal `#/$defs/...` refs
    # against it, producing `unknown url type: 'gatebraid/gatebraid/...'`;
    # jsonschema 4.23.0 (the Windows loader) tolerates it. Every `$ref` in every
    # frozen schema is a LOCAL JSON pointer - measured, all 13 of them - so
    # removing the base URI for validation purposes cannot change which documents
    # validate. It changes only where the resolver looks, and it makes the two
    # declared platforms agree. `$id` is still read from the file elsewhere, where
    # its value is the thing being compared.
    resolvable = dict(schema)
    resolvable.pop("$id", None)
    return Draft202012Validator(resolvable), loader


def error_locus(err):
    """One structural error as the corpus records loci: keyword, path, schema_path.

    `(root)` for the document root, a `property` name for a `required` failure,
    and `extra_count` - a MULTIPLICITY, never the names - for
    `additionalProperties`.  ADR-0028 §3: a checker never quotes what it forbids
    into a record, so no offending value appears here.
    """
    path = "/".join(str(p) for p in err.absolute_path)
    out = {
        "keyword": err.validator,
        "path": path if path else "(root)",
        "schema_path": "/".join(str(p) for p in err.absolute_schema_path),
    }
    if err.validator == "required" and isinstance(err.instance, dict) \
            and isinstance(err.validator_value, list):
        missing = [k for k in err.validator_value if k not in err.instance]
        if len(missing) == 1:
            out["property"] = missing[0]
    if err.validator == "additionalProperties" and isinstance(err.instance, dict) \
            and isinstance(err.schema, dict):
        out["extra_count"] = len(set(err.instance) - set(err.schema.get("properties", {})))
    return out


def structural_errors(doc, schema):
    validator, loader = load_schema_validator(schema)
    return [error_locus(e) for e in validator.iter_errors(doc)], loader


# ------------------------------------------------------- semantic re-derivation

def _pointer(*parts):
    """RFC 6901 pointer from path segments."""
    if not parts:
        return ""
    esc = [str(p).replace("~", "~0").replace("/", "~1") for p in parts]
    return "/" + "/".join(esc)


def parse_rfc3339(value):
    """Return (ok, datetime|None). Lexical form AND field ranges.

    The frozen schemas say in terms that their pattern checks lexical form only
    and that range and calendar validity are this validator's duty.
    """
    if not isinstance(value, str):
        return False, None
    m = RFC3339.match(value)
    if not m:
        return False, None
    y, mo, d, hh, mm, ss = (int(m.group(i)) for i in range(1, 7))
    if not 1 <= mo <= 12:
        return False, None
    if not 1 <= d <= calendar.monthrange(y, mo)[1]:
        return False, None
    if hh > 23 or mm > 59 or ss > 60:
        return False, None
    off = m.group(8)
    delta = datetime.timedelta(0)
    if off and off not in ("Z", "z"):
        sign = 1 if off[0] == "+" else -1
        oh, om = int(off[1:3]), int(off[4:6])
        if oh > 23 or om > 59:
            return False, None
        delta = sign * datetime.timedelta(hours=oh, minutes=om)
    # Sub-second precision is load-bearing, not decoration: two capture timestamps
    # commonly differ only in the fraction, and dropping it collapses them to the
    # same instant, which silently defeats the ended_at >= started_at duty.
    frac = m.group(7)
    micro = 0
    if frac:
        micro = int(round(float(frac) * 1_000_000))
        micro = min(micro, 999_999)
    try:
        naive = datetime.datetime(y, mo, d, hh, mm, min(ss, 59), micro)
    except ValueError:
        return False, None
    return True, naive - delta


class Finding(object):
    __slots__ = ("locus", "rule_id", "position", "extra_count")

    def __init__(self, locus, rule_id, position=None, extra_count=None):
        self.locus = locus
        self.rule_id = rule_id
        self.position = position
        self.extra_count = extra_count

    def emit(self, index):
        out = {"finding_id": "F%03d" % index, "locus": self.locus, "rule_id": self.rule_id}
        if self.position is not None:
            out["position"] = self.position
        if self.extra_count is not None:
            out["extra_count"] = self.extra_count
        return out


class Prop(object):
    __slots__ = ("property_id", "locus", "cls", "verdict", "trusted_on", "note")

    def __init__(self, property_id, locus, cls, verdict, trusted_on=None, note=None):
        self.property_id = property_id
        self.locus = locus
        self.cls = cls
        self.verdict = verdict
        self.trusted_on = trusted_on
        self.note = note

    def emit(self):
        out = {"property_id": self.property_id, "locus": self.locus,
               "class": self.cls, "verdict": self.verdict}
        if self.cls == "capture-trusted":
            out["trusted_on"] = "generator-capture"
        if self.note:
            out["note"] = self.note
        return out


def check_timestamps(doc, props, findings, fields, rule_prefix):
    """Calendar-valid timestamps, and ordering where both endpoints exist."""
    parsed = {}
    for f in fields:
        if f not in doc:
            continue
        ok, dt = parse_rfc3339(doc[f])
        parsed[f] = dt if ok else None
        props.append(Prop("%s-%s-calendar" % (rule_prefix, f), _pointer(f), "semantic",
                          "pass" if ok else "fail",
                          note="field ranges re-derived; the schema pattern is lexical only"))
        if not ok:
            findings.append(Finding(_pointer(f), "timestamp-not-calendar-valid"))
    if parsed.get("started_at") and parsed.get("ended_at"):
        ordered = parsed["ended_at"] >= parsed["started_at"]
        props.append(Prop("%s-interval-ordered" % rule_prefix, _pointer("ended_at"),
                          "semantic", "pass" if ordered else "fail",
                          note="ended_at >= started_at, named inexpressible by the schema"))
        if not ordered:
            findings.append(Finding(_pointer("ended_at"), "ended-before-started"))


def check_placeholders(doc, props, findings):
    """No placeholder survives into a field that should carry a measurement.

    A hit inside a command or citation field that matches one of the two named
    quoting forms is a MENTION rather than an elision (friction #169). Mentions
    are counted and labelled rather than dropped, so the exemption is visible in
    the record it applies to.
    """
    hits = []
    mentions = []

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, path + [k])
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + [i])
        elif isinstance(node, str):
            locus = _pointer(*path)
            excused = _is_mention_locus(locus)
            flagged = False
            for m in PLACEHOLDER.finditer(node):
                if excused and _is_mention(node, m):
                    mentions.append(locus)
                elif not flagged:
                    hits.append(locus)
                    flagged = True

    walk(doc, [])
    props.append(Prop("no-placeholder-survives", "", "semantic",
                      "pass" if not hits else "fail",
                      note="structural placeholder scan over every string value; a hit "
                           "in a command or citation field matching a named quoting "
                           "form is classified as a mention, not an elision"))
    props.append(Prop("placeholder-mentions-classified", "", "semantic", "pass",
                      note="quoting-form mentions excused at command/citation loci: %d"
                           % len(mentions)))
    for h in hits:
        findings.append(Finding(h, "placeholder-survives-its-own-check"))


def check_capture(doc, props, findings):
    """gatebraid/evidence-capture@1 re-derivations."""
    check_timestamps(doc, props, findings, ("started_at", "ended_at"), "capture")

    streams = doc.get("streams") or {}
    total_lone_cr = 0
    measurable = True
    for name in ("stdout", "stderr"):
        st = streams.get(name)
        if not isinstance(st, dict):
            continue
        base = _pointer("streams", name)
        data = st.get("data", "")
        try:
            raw = base64.b64decode(data, validate=True)
            decoded = True
        except (binascii.Error, ValueError):
            raw, decoded = b"", False
            measurable = False
        props.append(Prop("stream-%s-decodes" % name, _pointer("streams", name, "data"),
                          "semantic", "pass" if decoded else "fail",
                          note="base64 payload decoded from the record's own bytes"))
        if not decoded:
            findings.append(Finding(_pointer("streams", name, "data"), "base64-does-not-decode"))
            continue

        got_len = len(raw)
        want_len = st.get("byte_length")
        ok_len = (got_len == want_len)
        props.append(Prop("stream-%s-byte-length" % name, _pointer("streams", name, "byte_length"),
                          "semantic", "pass" if ok_len else "fail",
                          note="byte_length re-derived from the decoded payload"))
        if not ok_len:
            findings.append(Finding(_pointer("streams", name, "byte_length"),
                                    "byte-length-mismatch", position=got_len))

        got_sha = hashlib.sha256(raw).hexdigest()
        ok_sha = (got_sha == st.get("sha256"))
        props.append(Prop("stream-%s-sha256" % name, _pointer("streams", name, "sha256"),
                          "semantic", "pass" if ok_sha else "fail",
                          note="sha256 re-derived over the raw bytes before base64"))
        if not ok_sha:
            findings.append(Finding(_pointer("streams", name, "sha256"), "sha256-does-not-rederive"))

        total_lone_cr += raw.count(b"\r") - raw.count(b"\r\n")

    sa = (doc.get("self_assertions") or {}).get("zero_lone_cr") or {}
    if "count" in sa and measurable:
        ok_cr = (sa["count"] == total_lone_cr)
        props.append(Prop("zero-lone-cr-count", _pointer("self_assertions", "zero_lone_cr", "count"),
                          "semantic", "pass" if ok_cr else "fail",
                          note="lone-CR count re-derived from the decoded stream bytes"))
        if not ok_cr:
            findings.append(Finding(_pointer("self_assertions", "zero_lone_cr", "count"),
                                    "lone-cr-count-mismatch", position=total_lone_cr))

    # Accepted on the generator's word, and LABELLED so.
    for field in ("exit_code", "invocation", "platform", "generator"):
        if field in doc:
            props.append(Prop("capture-%s" % field, _pointer(field), "capture-trusted", "pass",
                              note="accepted on the generator's capture; not independently attested"))


def check_coverage_report(doc, props, findings, self_sha256=None):
    """gatebraid/coverage-report@1 re-derivations."""
    check_timestamps(doc, props, findings, ("recorded_at",), "report")

    comp = doc.get("completeness")
    if isinstance(comp, dict):
        total = comp.get("sections_total")
        examined = comp.get("sections_examined")
        unexamined = comp.get("unexamined") or []
        if isinstance(total, int) and isinstance(examined, int):
            ok = (examined + len(unexamined) == total)
            props.append(Prop("completeness-arithmetic", _pointer("completeness"), "semantic",
                              "pass" if ok else "fail",
                              note="sections_examined + len(unexamined) == sections_total, "
                                   "named inexpressible by the schema"))
            if not ok:
                findings.append(Finding(_pointer("completeness"), "completeness-arithmetic-mismatch"))
        secs = doc.get("sections") or []
        if isinstance(secs, list) and isinstance(total, int):
            ok_total = (len(secs) == total)
            props.append(Prop("completeness-sections-total", _pointer("completeness", "sections_total"),
                              "semantic", "pass" if ok_total else "fail",
                              note="sections_total re-derived by counting the sections array"))
            if not ok_total:
                findings.append(Finding(_pointer("completeness", "sections_total"),
                                        "sections-total-mismatch", position=len(secs)))

    dpc = doc.get("dual_platform_claim")
    if isinstance(dpc, dict):
        reports = [r for r in (dpc.get("reports") or []) if isinstance(r, dict)]

        # BP-03, the half the schema cannot reach. `uniqueItems` catches the same
        # report cited twice, but two DISTINCT digests both labelled the same OS is
        # exactly "one platform's capture presented as covering both" and validates
        # structurally. Two different OS values are what a dual-platform claim means.
        oss = [r.get("os") for r in reports]
        same_os = len(oss) == 2 and oss[0] == oss[1]
        props.append(Prop("dual-platform-two-distinct-os", _pointer("dual_platform_claim", "reports"),
                          "semantic", "fail" if same_os else "pass",
                          note="a dual-platform claim naming one OS twice is one platform "
                               "presented as covering both"))
        if same_os:
            findings.append(Finding(_pointer("dual_platform_claim", "reports"),
                                    "dual-platform-claim-names-one-os-twice"))

        own = (doc.get("platform") or {}).get("os")
        omits_own = bool(reports) and own is not None and own not in oss
        props.append(Prop("dual-platform-includes-own-platform", _pointer("dual_platform_claim"),
                          "semantic", "fail" if omits_own else "pass",
                          note="the claiming report's own platform must be one of the two "
                               "it claims, or the claim is about runs it did not make"))
        if omits_own:
            findings.append(Finding(_pointer("dual_platform_claim", "reports"),
                                    "dual-platform-claim-omits-own-platform"))

        if self_sha256:
            cites_self = any(r.get("report_sha256") == self_sha256 for r in reports)
            for i, rep in enumerate(reports):
                if rep.get("report_sha256") == self_sha256:
                    findings.append(Finding(_pointer("dual_platform_claim", "reports", i),
                                            "dual-platform-claim-cites-itself"))
            props.append(Prop("dual-platform-not-self-cited", _pointer("dual_platform_claim"),
                              "semantic", "fail" if cites_self else "pass",
                              note="citing one's own digest is a fixed point a report cannot "
                                   "reach by construction; kept because a contrived one would "
                                   "otherwise pass unnoticed"))

    # The unlabelled-credit rule, re-derived rather than assumed from the schema.
    for i, p in enumerate(doc.get("properties") or []):
        if not isinstance(p, dict):
            continue
        cls = p.get("class")
        loc = _pointer("properties", i)
        if cls == "replayed" and not isinstance(p.get("replay"), dict):
            findings.append(Finding(loc, "replayed-without-replay-block"))
        if cls != "replayed" and "replay" in p:
            findings.append(Finding(loc, "replay-block-under-non-replayed-class"))
        if cls == "capture-trusted" and p.get("trusted_on") != "generator-capture":
            findings.append(Finding(loc, "capture-trusted-without-label"))
    props.append(Prop("no-unlabelled-replayable-credit", _pointer("properties"), "semantic",
                      "fail" if any(f.rule_id.startswith(("replayed-", "replay-", "capture-trusted-"))
                                    for f in findings) else "pass",
                      note="every class/evidence pairing re-derived from the report's own rows"))


def check_gate_run(doc, props, findings):
    """gatebraid/gate-run@2 re-derivations."""
    check_timestamps(doc, props, findings, ("started_at", "ended_at"), "gate")
    for i, c in enumerate(doc.get("checks") or []):
        if isinstance(c, dict) and doc.get("bootstrap_exception") is True and not c.get("output_ref"):
            findings.append(Finding(_pointer("checks", i), "bootstrap-check-without-output-ref"))
    props.append(Prop("bootstrap-checks-pinned", _pointer("checks"), "semantic",
                      "fail" if any(f.rule_id == "bootstrap-check-without-output-ref"
                                    for f in findings) else "pass",
                      note="on a bootstrap_exception record every check must pin its capture"))


SEMANTIC_FOR = {
    "gatebraid/evidence-capture@1": check_capture,
    "gatebraid/coverage-report@1": check_coverage_report,
    "gatebraid/gate-run@2": check_gate_run,
}


# ------------------------------------------------------------------ report

def build_report(path, doc, raw_bytes, schema_id, struct_errors, props, findings,
                 loader, report_id, recorded_at):
    # FULL-FILE COVERAGE (M3-PLAN.md §2 N3, the review-4 lesson): the whole
    # document, then every top-level member, each with a disposition. Every one is
    # `examined`, and that is a measurement rather than a courtesy: the structural
    # row validates the COMPLETE document against the frozen interface, so each
    # member's shape is examined; `properties` records which members additionally
    # carry a re-derived semantic relation. `not_applicable` is reserved for a
    # section this validator genuinely cannot adjudicate, and it would carry its
    # reason and drop `complete` to false by way of `unexamined`.
    sections = [{"pointer": "", "disposition": "examined"}]
    if isinstance(doc, dict):
        for key in doc:
            sections.append({"pointer": _pointer(key), "disposition": "examined"})

    unexamined = [s["pointer"] for s in sections if s["disposition"] != "examined"]
    examined = sum(1 for s in sections if s["disposition"] == "examined")
    verdict = "accepted" if (not struct_errors and not findings
                             and all(p.verdict == "pass" for p in props)) else "rejected"
    if verdict == "rejected" and not findings:
        findings = [Finding("", "structural-validation-failed")]

    report = {
        "schema": "gatebraid/coverage-report@1",
        "report_id": report_id,
        "validator": {
            "name": VALIDATOR_NAME,
            "version": VALIDATOR_VERSION,
            "source_sha256": hashlib.sha256(
                open(os.path.abspath(__file__), "rb").read()).hexdigest(),
        },
        "target": {
            "path": path.replace("\\", "/"),
            "sha256": hashlib.sha256(raw_bytes).hexdigest(),
            "schema_id": schema_id,
        },
        "platform": {
            "os": "wsl" if ("microsoft" in platform.release().lower()
                            or "WSL_DISTRO_NAME" in os.environ) else
                  ("windows" if os.name == "nt" else
                   ("macos" if sys.platform == "darwin" else "linux")),
            "os_release": platform.platform(),
            "interpreter": loader,
        },
        "recorded_at": recorded_at,
        "trust_boundary": TRUST_BOUNDARY,
        "sections": sections,
        "properties": [p.emit() for p in props],
        "completeness": {
            "sections_total": len(sections),
            "sections_examined": examined,
            "unexamined": unexamined,
            "complete": len(unexamined) == 0,
        },
        "verdict": verdict,
        "findings": [f.emit(i + 1) for i, f in enumerate(findings)],
    }
    if struct_errors:
        report["notes"] = ("structural validation produced %d error locus/loci; "
                           "loci are recorded in the run summary by keyword, path and "
                           "schema_path, never by the offending value" % len(struct_errors))
    return report


def now_rfc3339():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_json(path, obj):
    """Binary write, LF only, so no platform newline translation reaches the record."""
    text = json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=False) + "\n"
    data = text.encode("utf-8")
    if b"\r" in data:
        raise InputError("STRUCTURE: refusing to write a record containing CR")
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.isdir(parent):
        os.makedirs(parent)
    with open(path, "wb") as fh:
        fh.write(data)
    return data


# ------------------------------------------------------------------- modes

# The ADR-0026 gate record is markdown carrying its gatebraid/gate-run@2 block in
# a fenced yaml section. Reading only JSON left three of every Slice's four gate
# records outside this validator's reach (friction #170): the record form the
# contracts mandate was the one form it could not open.
MD_HEADING = re.compile(r"^##[ \t]+gatebraid-metadata[ \t]*$", re.M)
MD_FENCE = re.compile(r"^```[ \t]*ya?ml[ \t]*\r?\n(.*?)^```[ \t]*$", re.M | re.S)


def load_yaml_document(text, path):
    """Extract and parse the `## gatebraid-metadata` block of a markdown record.

    The YAML loader is imported HERE, inside the function and guarded, for the
    same reason `load_schema_validator` imports the JSON Schema loader here: this
    file's module level stays standard-library only, and the Slice's frozen
    negative criterion N3 forbids changing that to fix a defect.

    Returns None when the text carries no metadata heading - the caller then
    reports the original input error, so a genuinely broken input stays an input
    error rather than becoming a record.
    """
    m = MD_HEADING.search(text)
    if not m:
        return None
    fence = MD_FENCE.search(text, m.end())
    if not fence:
        raise InputError(
            "STRUCTURE: %s has a `## gatebraid-metadata` heading but no fenced yaml "
            "block under it" % path)
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - environment failure
        raise InputError("STRUCTURE: the YAML loader is unavailable (%s)" % exc)
    try:
        doc = yaml.safe_load(fence.group(1))
    except Exception as exc:
        raise InputError("STRUCTURE: %s carries an unparseable metadata block (%s)"
                         % (path, exc))
    return doc



def validate_document(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise InputError("STRUCTURE: %s is not UTF-8 (%s)" % (path, exc))
    try:
        doc = json.loads(text)
        source_form = "json"
    except ValueError as exc:
        # Not JSON. It may still be an ADR-0026 markdown record; if it is not,
        # the original input error stands and the exit status stays 2.
        doc = load_yaml_document(text, path)
        if doc is None:
            raise InputError("STRUCTURE: %s is not UTF-8 JSON (%s)" % (path, exc))
        source_form = "markdown"
    if not isinstance(doc, dict) or "schema" not in doc:
        raise InputError("STRUCTURE: %s declares no `schema` and cannot be re-derived" % path)
    schema_id = doc["schema"]
    if schema_id not in SCHEMA_FOR:
        raise InputError("STRUCTURE: %s declares unknown interface %r" % (path, schema_id))
    schema = json.load(open(SCHEMA_FOR[schema_id], encoding="utf-8"))
    errors, loader = structural_errors(doc, schema)

    props, findings = [], []
    props.append(Prop("structural-shape", "", "structural",
                      "pass" if not errors else "fail",
                      note="validated against the frozen interface with the loader named"))
    for e in errors:
        findings.append(Finding("/" + e["path"] if e["path"] != "(root)" else "",
                                "structural:" + e["keyword"],
                                extra_count=e.get("extra_count")))
    check_placeholders(doc, props, findings)
    fn = SEMANTIC_FOR.get(schema_id)
    if fn is check_coverage_report:
        fn(doc, props, findings, hashlib.sha256(raw).hexdigest())
    elif fn:
        fn(doc, props, findings)
    return doc, raw, schema_id, errors, props, findings, loader


def mode_record(args):
    doc, raw, schema_id, errors, props, findings, loader = validate_document(args.record)
    report = build_report(args.record, doc, raw, schema_id, errors, props, findings,
                          loader, args.report_id or ("cov-" + os.path.basename(args.record)),
                          now_rfc3339())
    print("target        : %s" % args.record)
    print("interface     : %s" % schema_id)
    print("loader        : %s" % loader)
    print("structural    : %d error locus/loci" % len(errors))
    for e in errors:
        print("   %-22s %-40s %s" % (e["keyword"], e["path"], e["schema_path"]))
    print("properties    : %d rows" % len(props))
    for cls in ("structural", "semantic", "replayed", "capture-trusted"):
        n = sum(1 for p in props if p.cls == cls)
        print("   %-16s %d" % (cls, n))
    print("findings      : %d" % len(report["findings"]))
    for f in report["findings"]:
        print("   %-8s %-46s %s" % (f["finding_id"], f["locus"] or "(root)", f["rule_id"]))
    print("verdict       : %s" % report["verdict"])
    if args.coverage_out:
        data = write_json(args.coverage_out, report)
        print("coverage-out  : %s  bytes=%d sha256=%s"
              % (args.coverage_out, len(data), hashlib.sha256(data).hexdigest()))
    return 0 if report["verdict"] == "accepted" else 1


def mode_corpus(args):
    root = args.corpus
    manifest = json.load(open(os.path.join(root, "CORPORA.json"), encoding="utf-8"))
    built = manifest.get("built", [])
    print("corpus root   : %s" % root)
    print("corpora built : %s" % ", ".join(built))
    loader_seen = None
    total = matched = 0
    unexpected = []
    semantic_on_positive = []
    for corp in built:
        exp_path = os.path.join(root, corp, "EXPECTATIONS.json")
        if not os.path.isfile(exp_path):
            unexpected.append((corp, "-", "corpus declared built but carries no EXPECTATIONS.json"))
            continue
        exp = json.load(open(exp_path, encoding="utf-8"))
        print()
        print("== %s (%s), %d cases" % (corp, exp.get("corpus_version", "?"), len(exp["cases"])))
        for case in exp["cases"]:
            total += 1
            fixture = os.path.join(root, corp, case["fixture"])
            doc = json.load(open(fixture, encoding="utf-8"))
            schema = json.load(open(case["schema"], encoding="utf-8"))
            errs, loader = structural_errors(doc, schema)
            loader_seen = loader_seen or loader
            got = "valid" if not errs else "invalid"
            want = case["expect"]
            observed = {json.dumps(e, sort_keys=True) for e in errs}
            recorded = {json.dumps(e, sort_keys=True) for e in case.get("expect_errors", [])}
            locus_ok = (observed == recorded)
            ok = (got == want) and locus_ok
            if ok:
                matched += 1
            else:
                why = []
                if got != want:
                    why.append("disposition %s, recorded %s" % (got, want))
                if not locus_ok:
                    why.append("locus set differs: %d observed, %d recorded"
                               % (len(observed), len(recorded)))
                unexpected.append((corp, case["id"], "; ".join(why)))
            # On a positive control the semantic layer must also be clean.
            if want == "valid":
                p2, f2 = [], []
                fn = SEMANTIC_FOR.get(doc.get("schema"))
                if fn is check_coverage_report:
                    fn(doc, p2, f2, hashlib.sha256(open(fixture, "rb").read()).hexdigest())
                elif fn:
                    fn(doc, p2, f2)
                if f2:
                    semantic_on_positive.append((corp, case["id"], len(f2)))
            print("   %-8s %-52s want=%-7s got=%-7s locus=%s %s"
                  % (case["id"], case["fixture"][:52], want, got,
                     "match" if locus_ok else "DIFFER", "" if ok else "  <== UNEXPECTED"))

    print()
    print("loader                        : %s" % (loader_seen or "n/a"))
    print("cases declared                : %d" % total)
    print("cases reaching their recorded disposition and locus set : %d" % matched)
    print("unexpected dispositions       : %d" % len(unexpected))
    for corp, cid, why in unexpected:
        print("   %-20s %-8s %s" % (corp, cid, why))
    print("positive controls with semantic findings : %d" % len(semantic_on_positive))
    for corp, cid, n in semantic_on_positive:
        print("   %-20s %-8s %d finding(s)" % (corp, cid, n))

    if args.coverage_out:
        target = None
        for corp in built:
            exp_path = os.path.join(root, corp, "EXPECTATIONS.json")
            if not os.path.isfile(exp_path):
                continue
            exp = json.load(open(exp_path, encoding="utf-8"))
            for case in exp["cases"]:
                if case["expect"] == "valid" and case["schema"].endswith("evidence-capture.schema.json"):
                    target = os.path.join(root, corp, case["fixture"])
                    break
            if target:
                break
        if not target:
            raise InputError("STRUCTURE: no evidence-capture@1 positive control to report on")
        doc, raw, schema_id, errors, props, findings, loader = validate_document(target)
        report = build_report(target, doc, raw, schema_id, errors, props, findings, loader,
                              args.report_id or "cov-corpus-positive-control", now_rfc3339())
        data = write_json(args.coverage_out, report)
        print("coverage-out                  : %s  target=%s bytes=%d sha256=%s"
              % (args.coverage_out, target, len(data), hashlib.sha256(data).hexdigest()))

    clean = (not unexpected) and (not semantic_on_positive)
    print()
    if clean:
        print("CORPUS CLEAN: every declared case reached its recorded disposition and locus set")
    else:
        print("CORPUS NOT CLEAN: see the unexpected rows above")
    print("unexpected dispositions       : %d" % len(unexpected))
    return 0 if clean else 1


def mode_verify_coverage(args):
    path = args.verify_coverage
    with open(path, "rb") as fh:
        raw = fh.read()
    doc = json.loads(raw.decode("utf-8"))
    if doc.get("schema") != "gatebraid/coverage-report@1":
        raise InputError("STRUCTURE: %s is not a gatebraid/coverage-report@1 document" % path)
    schema = json.load(open(SCHEMA_FOR["gatebraid/coverage-report@1"], encoding="utf-8"))
    errs, loader = structural_errors(doc, schema)
    props, findings = [], []
    check_coverage_report(doc, props, findings, hashlib.sha256(raw).hexdigest())
    check_placeholders(doc, props, findings)

    counts = {"structural": 0, "semantic": 0, "replayed": 0, "capture-trusted": 0}
    unlabelled = 0
    for p in doc.get("properties") or []:
        cls = p.get("class")
        if cls in counts:
            counts[cls] += 1
        if cls == "replayed" and not isinstance(p.get("replay"), dict):
            unlabelled += 1
        if cls != "replayed" and "replay" in p:
            unlabelled += 1
        if cls == "capture-trusted" and p.get("trusted_on") != "generator-capture":
            unlabelled += 1

    print("report        : %s" % path)
    print("loader        : %s" % loader)
    print("structural    : %d error locus/loci" % len(errs))
    for e in errs:
        print("   %-22s %-40s %s" % (e["keyword"], e["path"], e["schema_path"]))
    print("classification, every verified property carrying exactly one class:")
    for cls in ("structural", "semantic", "replayed", "capture-trusted"):
        print("   %-16s %d" % (cls, counts[cls]))
    print("classified rows               : %d" % sum(counts.values()))
    print("rows in the report            : %d" % len(doc.get("properties") or []))
    print("re-derivation findings        : %d" % len(findings))
    for i, f in enumerate(findings):
        print("   %-8s %-46s %s" % ("F%03d" % (i + 1), f.locus or "(root)", f.rule_id))
    print("unlabelled replayable credits : %d" % unlabelled)
    clean = (not errs and not findings and unlabelled == 0
             and sum(counts.values()) == len(doc.get("properties") or []))
    print()
    if clean:
        print("COVERAGE CLEAN: every verified property carries exactly one of the four "
              "classes and no replayable claim is credited without a label")
    else:
        print("COVERAGE NOT CLEAN: see the rows above")
    print("unlabelled replayable credits : %d" % unlabelled)
    return 0 if clean else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog=VALIDATOR_NAME,
        description="Independently re-derive verdicts for Gatebraid evidence documents.")
    ap.add_argument("--corpus", metavar="DIR",
                    help="run the N1 mutation suite over the frozen corpus")
    ap.add_argument("--record", metavar="PATH",
                    help="re-derive verdicts for one evidence document")
    ap.add_argument("--verify-coverage", metavar="PATH",
                    help="re-read an emitted coverage report and check its classification")
    ap.add_argument("--coverage-out", metavar="PATH",
                    help="write the gatebraid/coverage-report@1 document here")
    ap.add_argument("--report-id", metavar="ID", help="report_id for the emitted document")
    args = ap.parse_args(argv)

    modes = [bool(args.corpus), bool(args.record), bool(args.verify_coverage)]
    if sum(modes) != 1:
        ap.error("exactly one of --corpus, --record, --verify-coverage is required")
    if args.verify_coverage and args.coverage_out:
        ap.error("--verify-coverage re-reads a report; it does not emit one")

    if args.corpus:
        return mode_corpus(args)
    if args.record:
        return mode_record(args)
    return mode_verify_coverage(args)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except InputError as exc:
        print(exc, file=sys.stderr)
        sys.exit(2)
