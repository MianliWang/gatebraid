#!/usr/bin/env python3
"""gatebraid-validate-selftest - falsify the validator before it is trusted.

ADR-0028 decision 1: a check is falsified once before it is trusted.  This file
seeds a condition for every rule `gatebraid-validate` claims to enforce and
asserts the EXIT STATUS each must produce.  A rule with no seeded condition is a
rule nobody has shown to fire; a condition that passes under both the correct and
the broken tool is a condition that measures nothing, so each seed below is
derived from a valid document by breaking exactly one relation.

The seeds are written to a temporary directory OUTSIDE every repository
(`tempfile.mkdtemp()`), which `protocols/gate-2-contract.md` permits explicitly
and which this Slice's Gate 2 evidence names.  Nothing under the repository is
written by this file.

Green is: every seeded condition produces its required exit status, and the
summary reports `conditions failed : 0`.  Counts are deliberately absent from the
acceptance criteria - the caller reads the summary, not a number of conditions,
so adding a condition never falsifies a frozen expectation.

Exit codes: 0 all conditions produced their required status · 1 one or more did
not · 2 the harness itself could not run.  Python 3 standard library only at
module level.
"""

import base64
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
VALIDATOR = os.path.join(HERE, "gatebraid-validate.py")

CAPTURE_SRC = os.path.join(REPO, "docs", "evidence", "gatebraid", "P2-S1",
                           "captures", "Q1-real.json")
COVERAGE_POSITIVE = os.path.join(REPO, "fixtures", "instruments", "valid-coverage-report.json")


def run(args):
    """Invoke the validator as a subprocess so the EXIT STATUS is the real one."""
    proc = subprocess.run(
        [sys.executable, "-B", VALIDATOR] + args,
        cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def write(path, doc):
    data = (json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    return path



def yaml_dump(doc):
    """Emit the seed documents as YAML using the standard library only.

    The selftest must not acquire a third-party dependency in order to exercise
    one; these seeds are flat by construction, so a minimal emitter is honest and
    sufficient.
    """
    out = []
    for k, v in doc.items():
        if isinstance(v, list):
            out.append("%s:" % k)
            for item in v:
                first = True
                for ik, iv in item.items():
                    out.append(("  - " if first else "    ") + "%s: %s" % (ik, json.dumps(iv)))
                    first = False
        else:
            out.append("%s: %s" % (k, json.dumps(v)))
    return "\n".join(out) + "\n"


def rebuild_stream(doc, raw):
    """Set a stream payload AND its declared digest/length consistently."""
    st = doc["streams"]["stdout"]
    st["data"] = base64.b64encode(raw).decode("ascii")
    st["sha256"] = hashlib.sha256(raw).hexdigest()
    st["byte_length"] = len(raw)
    return doc


class Conditions(object):
    def __init__(self):
        self.rows = []

    def check(self, cid, name, want, got, observation, marker=None, output=""):
        ok = (got == want)
        if marker is not None:
            ok = ok and (marker in output)
        self.rows.append((cid, name, want, got, ok, observation,
                          "" if marker is None else marker))
        return ok


def main():
    if not os.path.isfile(VALIDATOR):
        print("HARNESS: validator not found at %s" % VALIDATOR)
        return 2
    if not os.path.isfile(CAPTURE_SRC):
        print("HARNESS: source capture not found at %s" % CAPTURE_SRC)
        return 2

    tmp = tempfile.mkdtemp(prefix="gatebraid-validate-selftest-")
    c = Conditions()
    try:
        base_capture = json.load(open(CAPTURE_SRC, encoding="utf-8"))
        base_cov = json.load(open(COVERAGE_POSITIVE, encoding="utf-8"))

        # ---- S00 positive control: an untouched valid capture is ACCEPTED ----
        p = write(os.path.join(tmp, "s00.json"), copy.deepcopy(base_capture))
        rc, out = run(["--record", p])
        c.check("S00", "untouched capture accepted", 0, rc,
                "a valid record must be accepted", "verdict       : accepted", out)

        # ---- S01 digest does not re-derive (the corrupted-N2-output class) ----
        d = copy.deepcopy(base_capture)
        raw = bytearray(base64.b64decode(d["streams"]["stdout"]["data"], validate=True))
        raw[0] = (raw[0] + 1) % 256
        d["streams"]["stdout"]["data"] = base64.b64encode(bytes(raw)).decode("ascii")
        p = write(os.path.join(tmp, "s01.json"), d)
        rc, out = run(["--record", p])
        c.check("S01", "sha256 does not re-derive", 1, rc,
                "schema-valid; caught only by re-derivation", "sha256-does-not-rederive", out)

        # ---- S02 byte_length mismatch ----
        d = copy.deepcopy(base_capture)
        d["streams"]["stdout"]["byte_length"] = d["streams"]["stdout"]["byte_length"] + 1
        p = write(os.path.join(tmp, "s02.json"), d)
        rc, out = run(["--record", p])
        c.check("S02", "byte_length mismatch", 1, rc,
                "declared length must match the decoded payload", "byte-length-mismatch", out)

        # ---- S03 ended_at precedes started_at ----
        d = copy.deepcopy(base_capture)
        d["started_at"], d["ended_at"] = d["ended_at"], d["started_at"]
        if d["started_at"] == d["ended_at"]:
            d["ended_at"] = "2000-01-01T00:00:00Z"
        p = write(os.path.join(tmp, "s03.json"), d)
        rc, out = run(["--record", p])
        c.check("S03", "ended_at precedes started_at", 1, rc,
                "named inexpressible by the schema", "ended-before-started", out)

        # ---- S04 lexically valid but calendar-impossible timestamp ----
        d = copy.deepcopy(base_capture)
        d["started_at"] = "2026-02-31T00:00:00Z"
        p = write(os.path.join(tmp, "s04.json"), d)
        rc, out = run(["--record", p])
        c.check("S04", "calendar-impossible timestamp", 1, rc,
                "the schema pattern is lexical only", "timestamp-not-calendar-valid", out)

        # ---- S05 base64 payload that does not decode ----
        d = copy.deepcopy(base_capture)
        d["streams"]["stdout"]["data"] = "A"
        p = write(os.path.join(tmp, "s05.json"), d)
        rc, out = run(["--record", p])
        c.check("S05", "payload does not decode", 1, rc,
                "the base64 grammar is the field the byte contract rests on", None, out)

        # ---- S06 lone-CR count disagrees with the bytes ----
        d = rebuild_stream(copy.deepcopy(base_capture), b"one\rtwo\r\nthree")
        d["self_assertions"]["zero_lone_cr"]["count"] = 0
        p = write(os.path.join(tmp, "s06.json"), d)
        rc, out = run(["--record", p])
        c.check("S06", "lone-CR count disagrees with bytes", 1, rc,
                "byte/line-ending discipline re-derived", "lone-cr-count-mismatch", out)

        # ---- S06b a CRLF-only payload with the true count of 0 is accepted ----
        # The schema pins zero_lone_cr.count to const 0, so a record declaring any
        # other value is structurally illegal and could never reach the counter.
        # The positive control therefore carries CRLF but no LONE CR.
        d = rebuild_stream(copy.deepcopy(base_capture), b"one\r\ntwo\nthree")
        d["self_assertions"]["zero_lone_cr"]["count"] = 0
        p = write(os.path.join(tmp, "s06b.json"), d)
        rc, out = run(["--record", p])
        c.check("S06b", "CRLF payload, true count 0, accepted", 0, rc,
                "the counter must not fire on a correct record", None, out)

        # ---- S07 placeholder survives into a measurement field ----
        d = copy.deepcopy(base_capture)
        d["notes"] = "digest to be filled: " + chr(60) + "sha" + chr(62)
        p = write(os.path.join(tmp, "s07.json"), d)
        rc, out = run(["--record", p])
        c.check("S07", "placeholder survives its own check", 1, rc,
                "IN-02's locus", "placeholder-survives-its-own-check", out)

        # ---- S08 coverage report: completeness arithmetic broken ----
        d = copy.deepcopy(base_cov)
        d["completeness"]["sections_total"] = d["completeness"]["sections_total"] + 1
        p = write(os.path.join(tmp, "s08.json"), d)
        rc, out = run(["--record", p])
        c.check("S08", "completeness arithmetic broken", 1, rc,
                "named inexpressible by the schema", "sections-total-mismatch", out)

        # ---- S09 coverage report: replayed class with no replay block ----
        d = copy.deepcopy(base_cov)
        for row in d["properties"]:
            if row.get("class") == "replayed":
                row.pop("replay", None)
                break
        p = write(os.path.join(tmp, "s09.json"), d)
        rc, out = run(["--record", p])
        c.check("S09", "replayed claim shows nothing", 1, rc,
                "the unlabelled credit the plan forbids", "replayed-without-replay-block", out)

        # ---- S10 coverage report: capture-trusted without its label ----
        d = copy.deepcopy(base_cov)
        for row in d["properties"]:
            if row.get("class") == "capture-trusted":
                row.pop("trusted_on", None)
                break
        p = write(os.path.join(tmp, "s10.json"), d)
        rc, out = run(["--record", p])
        c.check("S10", "capture-trusted without its label", 1, rc,
                "capture-trusted must be LABELLED so", "capture-trusted-without-label", out)

        # ---- S11 one platform presented as covering both ----
        # BP-03's live half: two DISTINCT digests both labelled the same OS satisfies
        # `uniqueItems` and every other keyword, so the schema accepts it. Citing one's
        # OWN digest is deliberately NOT seeded here - adding the citation changes the
        # file's digest, so it is a fixed point no report can reach by construction,
        # and a condition that cannot be built is a condition that measures nothing.
        d = copy.deepcopy(base_cov)
        d["dual_platform_claim"] = {"reports": [
            {"os": "windows", "report_sha256": "a" * 64},
            {"os": "windows", "report_sha256": "b" * 64}]}
        p = write(os.path.join(tmp, "s11.json"), d)
        rc, out = run(["--record", p])
        c.check("S11", "one OS claimed as two platforms", 1, rc,
                "structurally valid; caught only by re-derivation",
                "dual-platform-claim-names-one-os-twice", out)

        # ---- S11b a claim that omits the claiming report's own platform ----
        d = copy.deepcopy(base_cov)
        d["dual_platform_claim"] = {"reports": [
            {"os": "linux", "report_sha256": "a" * 64},
            {"os": "macos", "report_sha256": "b" * 64}]}
        p = write(os.path.join(tmp, "s11b.json"), d)
        rc, out = run(["--record", p])
        c.check("S11b", "claim omits its own platform", 1, rc,
                "a claim about runs the report did not make",
                "dual-platform-claim-omits-own-platform", out)

        # ---- S12 --verify-coverage accepts a clean emitted report ----
        emitted = os.path.join(tmp, "s12-report.json")
        rc0, _ = run(["--record", os.path.join(tmp, "s00.json"), "--coverage-out", emitted])
        rc, out = run(["--verify-coverage", emitted])
        c.check("S12", "emitted report verifies clean", 0, rc,
                "the validator's own output must survive its own re-reading",
                "COVERAGE CLEAN", out)

        # ---- S13 --verify-coverage rejects a broken report ----
        d = json.load(open(emitted, encoding="utf-8"))
        d["completeness"]["sections_examined"] = d["completeness"]["sections_examined"] + 1
        p = write(os.path.join(tmp, "s13.json"), d)
        rc, out = run(["--verify-coverage", p])
        c.check("S13", "broken report refused on re-read", 1, rc,
                "IN-05: partial coverage claiming completeness", "COVERAGE NOT CLEAN", out)

        # ---- S14 the frozen corpus runs clean ----
        rc, out = run(["--corpus", os.path.join(REPO, "fixtures")])
        c.check("S14", "frozen corpus clean", 0, rc,
                "every declared case reaches its recorded disposition and locus set",
                "CORPUS CLEAN", out)

        # ---- S15 an unknown interface is refused, not guessed ----
        d = copy.deepcopy(base_capture)
        d["schema"] = "gatebraid/not-an-interface@9"
        p = write(os.path.join(tmp, "s15.json"), d)
        rc, out = run(["--record", p])
        c.check("S15", "unknown interface refused", 2, rc,
                "an input error is exit 2, distinct from a rejection", None, out)

        # ---- S16 a non-JSON input is an input error, never a rejection ----
        p = os.path.join(tmp, "s16.json")
        with open(p, "wb") as fh:
            fh.write(b"{not json")
        rc, out = run(["--record", p])
        c.check("S16", "non-JSON input refused", 2, rc,
                "exit 2 distinguishes a broken input from a rejected record", None, out)

        # ---- S17 usage errors: no mode, and two modes ----
        rc, out = run([])
        c.check("S17", "no mode is a usage error", 2, rc,
                "exactly one mode is required", None, out)
        rc, out = run(["--record", os.path.join(tmp, "s00.json"),
                       "--corpus", os.path.join(REPO, "fixtures")])
        c.check("S18", "two modes is a usage error", 2, rc,
                "exactly one mode is required", None, out)

        # ---- S19 --verify-coverage may not also emit ----
        rc, out = run(["--verify-coverage", emitted, "--coverage-out",
                       os.path.join(tmp, "never.json")])
        c.check("S19", "verify-coverage refuses to emit", 2, rc,
                "re-reading a report is not writing one", None, out)

        # ---- S20 every emitted record is LF-only ----
        raw = open(emitted, "rb").read()
        c.check("S20", "emitted record is LF-only", 0, 0 if b"\r" not in raw else 1,
                "binary write; no platform newline translation reaches the record")

        # ---- S21 the loader is present and named, never silently skipped ----
        rc, out = run(["--record", os.path.join(tmp, "s00.json")])
        named = ("Draft202012Validator" in out) and ("jsonschema" in out)
        c.check("S21", "schema loader named in the output", 0, 0 if named else 1,
                "a structural claim whose loader is unnamed is unreproducible")

        # ---- S22 the seed harness itself is falsified ----
        # A condition that would pass whether or not the tool works measures nothing.
        # S00 and S01 differ ONLY by one payload byte; if their statuses were equal the
        # suite above would be blind, so that inequality is asserted here directly.
        rc_a, _ = run(["--record", os.path.join(tmp, "s00.json")])
        rc_b, _ = run(["--record", os.path.join(tmp, "s01.json")])
        c.check("S22", "seed discriminates (S00 != S01)", 0, 0 if rc_a != rc_b else 1,
                "one flipped byte must change the verdict, or the suite is blind")

        # ---- S23-S26 Task A: the mention test, seeded in BOTH directions ----
        # The repair must excuse a quoted GraphQL spread and must NOT excuse an
        # ellipsis standing in for omitted command text. A repair that only stops
        # rejecting things passes S23 and fails S24, which is the point.
        d = json.load(open(CAPTURE_SRC, encoding="utf-8"))
        d["invocation"]["argv"] = ["gh", "api", "graphql", "-f",
                                   "query={ nodes { ... on ProjectV2Item { id } } }"]
        p_ = write(os.path.join(tmp, "s23.json"), d)
        rc, out = run(["--record", p_])
        c.check("S23", "GraphQL spread in argv is a mention", 0, rc,
                "a captured command may contain an ellipsis because the command did",
                None, out)

        d = json.load(open(CAPTURE_SRC, encoding="utf-8"))
        d["invocation"]["argv"] = ["gh", "api", "graphql", "...", "-F", "number=8"]
        p_ = write(os.path.join(tmp, "s24.json"), d)
        rc, out = run(["--record", p_])
        c.check("S24", "elided command text still rejects", 1, rc,
                "an ellipsis standing alone replaces omitted text and stays a finding",
                "placeholder-survives-its-own-check", out)

        d = json.load(open(CAPTURE_SRC, encoding="utf-8"))
        d["notes"] = "item asserted == PVTI_...zg3Dr5A, never by Title"
        p_ = write(os.path.join(tmp, "s25.json"), d)
        rc, out = run(["--record", p_])
        c.check("S25", "id abbreviation in notes is a mention", 0, rc,
                "an ellipsis bounded by identifier characters abbreviates, it does not elide",
                None, out)

        d = json.load(open(CAPTURE_SRC, encoding="utf-8"))
        d["platform"]["os_release"] = "..."
        p_ = write(os.path.join(tmp, "s26.json"), d)
        rc, out = run(["--record", p_])
        c.check("S26", "ellipsis outside a quoting field rejects", 1, rc,
                "the exemption is scoped to command and citation loci, not to the document",
                "placeholder-survives-its-own-check", out)

        # ---- S27-S30 Task B: the markdown record mode, BOTH directions ----
        d = json.load(open(CAPTURE_SRC, encoding="utf-8"))
        gate_doc = {
            "schema": "gatebraid/gate-run@2", "slice_id": "P9-S9", "gate": 0,
            "environment": "windows", "executor": "Claude Lead",
            "base_sha": "0" * 40, "result": "passed",
            "checks": [{"name": "seed", "result": "pass"}],
        }
        md = ("# Gate 0 evidence - P9-S9\n\n## Records\n\nseed\n\n"
              "## gatebraid-metadata\n\n```yaml\n"
              + yaml_dump(gate_doc) + "```\n")
        p_ = os.path.join(tmp, "s27.md")
        with open(p_, "wb") as fh:
            fh.write(md.encode("utf-8"))
        rc, out = run(["--record", p_])
        c.check("S27", "markdown gate record is read", 0, rc,
                "the ADR-0026 record form its own contracts mandate must be readable",
                "gatebraid/gate-run@2", out)

        bad = dict(gate_doc)
        bad["base_sha"] = "63c8401"           # abbreviated: the @2 delta
        md = ("# Gate 0 evidence - P9-S9\n\n## gatebraid-metadata\n\n```yaml\n"
              + yaml_dump(bad) + "```\n")
        p_ = os.path.join(tmp, "s28.md")
        with open(p_, "wb") as fh:
            fh.write(md.encode("utf-8"))
        rc, out = run(["--record", p_])
        c.check("S28", "invalid embedded record rejects", 1, rc,
                "reading a record is not accepting it; the schema still governs", None, out)

        p_ = os.path.join(tmp, "s29.md")
        with open(p_, "wb") as fh:
            fh.write(b"# Not a record\n\nprose only, no metadata block\n")
        rc, out = run(["--record", p_])
        c.check("S29", "markdown without a block is an input error", 2, rc,
                "a broken input must not become a record by being markdown", None, out)

        p_ = os.path.join(tmp, "s30.md")
        with open(p_, "wb") as fh:
            fh.write(b"# R\n\n## gatebraid-metadata\n\nheading but no fenced block\n")
        rc, out = run(["--record", p_])
        c.check("S30", "heading without a fence is an input error", 2, rc,
                "a half-formed record fails closed rather than validating an empty document",
                None, out)


    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    width = max(len(r[1]) for r in c.rows)
    print("%-6s %-*s %5s %5s  %-7s %s" % ("id", width, "condition", "want", "got",
                                          "verdict", "required observation"))
    failed = 0
    for cid, name, want, got, ok, obs, marker in c.rows:
        if not ok:
            failed += 1
        print("%-6s %-*s %5s %5s  %-7s %s" % (cid, width, name, want, got,
                                              "PASS" if ok else "FAIL", obs))
    print()
    print("scratch directory             : outside every repository (tempfile.mkdtemp)")
    print("validator under test          : %s" % VALIDATOR)
    print("interpreter                   : %s" % sys.executable)
    print("conditions failed             : %d" % failed)
    if failed == 0:
        print("SELFTEST CLEAN: every seeded condition produced its required exit status")
    else:
        print("SELFTEST NOT CLEAN: see the FAIL rows above")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
