#!/usr/bin/env python3
"""gatebraid-snapshot-selftest - falsify the snapshot producer before it is trusted.

ADR-0028 decision 1: a check is falsified once before it is trusted.  This file
seeds a condition for every rule `gatebraid-snapshot` claims to enforce and
asserts the EXIT STATUS each must produce, plus a required observation in the
output where the exit status alone would not distinguish the outcomes.

WHY THE SEEDS GO THROUGH THE REPLAY TRANSPORT AND NOT THROUGH A STUB.  The
transport supplies only what a real read supplies - an exit status, two streams,
and the two headers that separate the 403 classes.  Classification, assembly,
verdict derivation and self-validation are then the tool's own, unmodified.  A
seed therefore measures the tool rather than a mock of it.  Nothing here
contacts the network: there is no live read in this file and no HTTP client.

EACH SEED BREAKS EXACTLY ONE RELATION in a document known to be healthy, so a
condition that passes under both the correct and the broken tool - which
measures nothing - cannot survive here.  The healthy document itself is a seeded
condition (S08): a fail-closed tool that rejected everything would pass every
negative case and fail that one, which is the GR2-07 lesson the frozen corpus
records.

The seeds are written to a temporary directory OUTSIDE every repository
(`tempfile.mkdtemp()`), which `protocols/gate-2-contract.md` permits explicitly
and which this Slice's Gate 2 evidence names.  Nothing under the repository is
written by this file.

Green is: every seeded condition produces its required exit status and required
observation, and the summary reports `conditions failed : 0`.  Counts are
deliberately absent from the acceptance criteria - the caller reads the summary,
not a number of conditions, so adding a condition never falsifies a frozen
expectation.

Exit codes: 0 all conditions produced their required status - 1 one or more did
not - 2 the harness itself could not run.  Python 3 standard library only.
"""

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TOOL = os.path.join(HERE, "gatebraid-snapshot.py")
SCHEMA = os.path.join(REPO, "schema", "snapshot.schema.json")


def run(args):
    """Invoke the tool as a subprocess so the EXIT STATUS is the real one.

    stdout is kept as BYTES and never decoded here: this harness checks a byte
    contract, and a harness that decodes before comparing cannot see the defect
    it exists to catch.
    """
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([sys.executable, "-B", TOOL] + args, cwd=REPO,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    return proc.returncode, proc.stdout, proc.stderr.decode("utf-8", "replace")


def write_json(path, doc):
    with open(path, "wb") as fh:
        fh.write((json.dumps(doc, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    return path


def healthy_transcript():
    """A document with every source `ok` and complete. The positive control."""
    return {
        "reads": {
            "project_items": {"stdout": {"nodes": [
                {"item_id": "PVTI_a", "issue": "MianliWang/gatebraid#14",
                 "slice_metadata_present": True, "slice_id": "P2-S4",
                 "workflow_raw": "Needs Plan Approval",
                 "soft_dependencies_declared": False},
                {"item_id": "PVTI_b", "issue": "MianliWang/gatebraid#3",
                 "slice_metadata_present": False,
                 "excluded_reason": "a Phase container row, not a Slice"},
            ], "hasNextPage": False}},
            "issue_states": {"stdout": {"states": {
                "MianliWang/gatebraid#14": "OPEN",
                "MianliWang/gatebraid#3": "OPEN"}}},
            "dep_blocked_by": {"stdout": {"edges": {}}},
            "dep_blocking": {"stdout": {"edges": {}}},
        }
    }


def seed(mutate):
    doc = copy.deepcopy(healthy_transcript())
    mutate(doc["reads"])
    return doc


class Conditions(object):
    def __init__(self):
        self.rows = []

    def check(self, cid, name, want, got, observation, marker=None, output=""):
        ok = (got == want)
        if marker is not None:
            ok = ok and (marker in output)
        self.rows.append((cid, name, want, got, ok, observation))
        return ok


def status_of(path, source_id):
    doc = json.load(open(path, encoding="utf-8"))
    for s in doc["sources"]:
        if s["source_id"] == source_id:
            return s
    return {}


def item_of(path, item_id):
    doc = json.load(open(path, encoding="utf-8"))
    for i in doc["items"]:
        if i["item_id"] == item_id:
            return i
    return {}


def main():
    if not os.path.isfile(TOOL):
        print("HARNESS: tool not found at %s" % TOOL)
        return 2
    if not os.path.isfile(SCHEMA):
        print("HARNESS: frozen schema not found at %s" % SCHEMA)
        return 2

    schema = json.load(open(SCHEMA, encoding="utf-8"))
    # The enumerations are READ, never typed: four Workflow values carry U+2014
    # and a harness that re-typed one would test its own typo.
    workflows = schema["$defs"]["item"]["properties"]["workflow"]["enum"]
    em_dash_workflow = next(w for w in workflows if "—" in w)

    tmp = tempfile.mkdtemp(prefix="gatebraid-snapshot-selftest-")
    c = Conditions()
    try:
        # ---- the positive control -------------------------------------------
        p = write_json(os.path.join(tmp, "healthy.json"), healthy_transcript())
        out = os.path.join(tmp, "healthy-out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        c.check("S01", "a healthy read emits and exits 0", 0, rc,
                "a fail-closed tool that rejected everything would fail HERE and "
                "pass every negative below", "SNAPSHOT OK", err)
        c.check("S02", "the healthy positive control is startable", "startable",
                item_of(out, "PVTI_a").get("verdict") if rc == 0 else "n/a",
                "the tool can still say yes; fail-closed is not reject-everything")

        # ---- P0-1: the seven closed failure classes, one seed each ----------
        classes = [
            ("S03", "auth_failure", "401 answered on a read",
             lambda r: r.update({"issue_states": {"http_status": 401, "exit_code": 1,
                                                  "stderr": "HTTP 401"}})),
            ("S04", "permission_failure", "403 with budget remaining",
             lambda r: r.update({"issue_states": {"http_status": 403, "exit_code": 1,
                                                  "rate_limit_remaining": 17,
                                                  "stderr": "HTTP 403"}})),
            ("S05", "rate_limited", "403 with the budget exhausted",
             lambda r: r.update({"issue_states": {"http_status": 403, "exit_code": 1,
                                                  "rate_limit_remaining": 0,
                                                  "stderr": "HTTP 403"}})),
            ("S06", "network_error", "the read could not be performed",
             lambda r: r.update({"issue_states": {"exit_code": 1,
                                                  "transport_error": "connection refused"}})),
            ("S07", "server_error", "the endpoint answered 503",
             lambda r: r.update({"issue_states": {"http_status": 503, "exit_code": 1,
                                                  "stderr": "HTTP 503"}})),
            ("S08", "parse_error", "a body that is not JSON",
             lambda r: r.update({"issue_states": {"exit_code": 0,
                                                  "stdout": "{not json"}})),
            ("S09", "unexpected_endpoint", "a shape the tool does not recognise",
             lambda r: r.update({"issue_states": {"exit_code": 0, "stdout": "[1,2,3]"}})),
        ]
        for cid, want_status, why, mutate in classes:
            p = write_json(os.path.join(tmp, cid + ".json"), seed(mutate))
            out = os.path.join(tmp, cid + "-out.json")
            rc, _, err = run(["--replay", p, "--out", out])
            got = status_of(out, "issue_states").get("status") if rc == 3 else "exit%d" % rc
            c.check(cid, "P0-1 %s (%s)" % (want_status, why), want_status, got,
                    "a class with no seeded condition is a class nobody has shown to fire")

        # ---- P0-1: a degraded read can never exit 0 -------------------------
        p = write_json(os.path.join(tmp, "S10.json"),
                       seed(lambda r: r.update({"issue_states": {"http_status": 401,
                                                                 "exit_code": 1,
                                                                 "stderr": "HTTP 401"}})))
        rc, _, err = run(["--replay", p, "--out", os.path.join(tmp, "S10-out.json")])
        c.check("S10", "a degraded snapshot exits 3, never 0", 3, rc,
                "the exit status is the only thing a shell caller reads",
                "SNAPSHOT DEGRADED", err)

        # ---- P0-1: a degraded read forces every verdict to undecidable ------
        out = os.path.join(tmp, "S10-out.json")
        c.check("S11", "degraded forces verdict undecidable", "undecidable",
                item_of(out, "PVTI_a").get("verdict"),
                "the dropped-edge-read-as-no-blocker defect, structurally refused")

        # ---- P0-1: a non-zero process exit is surfaced, never folded --------
        c.check("S12", "the non-zero process exit reaches the document", 1,
                status_of(out, "issue_states").get("exit_code"),
                "ADR-0029 decision 2 P0-1: a non-zero gh exit folded into None")

        # ---- the read-outcome sentinel, and the real exit kept recoverable --
        p = write_json(os.path.join(tmp, "S13.json"),
                       seed(lambda r: r.update({"issue_states": {"exit_code": 0,
                                                                 "stdout": "{not json"}})))
        out = os.path.join(tmp, "S13-out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        src = status_of(out, "issue_states")
        c.check("S13", "a zero-exit failed read carries the sentinel", 65,
                src.get("exit_code"),
                "the schema forbids a non-ok status reporting a success exit")
        c.check("S14", "and names the real process exit in failure_detail", True,
                "exited 0" in (src.get("failure_detail") or ""),
                "the process status stays recoverable rather than being lost")

        # ---- P0-3: the page cap fails closed --------------------------------
        p = write_json(os.path.join(tmp, "S15.json"), seed(lambda r: r.update(
            {"project_items": [{"stdout": {"nodes": [], "hasNextPage": True}},
                               {"stdout": {"nodes": [], "hasNextPage": True}}]})))
        out = os.path.join(tmp, "S15-out.json")
        rc, _, err = run(["--replay", p, "--out", out, "--page-cap", "1"])
        b = status_of(out, "project_items").get("bounded") or {}
        c.check("S15", "P0-3 the cap sets bounded and degrades", "page_cap_reached",
                b.get("reason"), "a truncated list reported as whole is the P0-3 defect")
        c.check("S16", "P0-3 the capped read is not complete", False,
                status_of(out, "project_items").get("complete"),
                "completeness asserted without pagination")
        c.check("S17", "P0-3 a capped read exits 3", 3, rc,
                "reaching a cap fails closed rather than passing")

        # ---- P0-3: a FAILED read is an incomplete read and says where -------
        c.check("S18", "a failed read carries bounded query_failed", "query_failed",
                (status_of(os.path.join(tmp, "S10-out.json"), "issue_states")
                 .get("bounded") or {}).get("reason"),
                "an incomplete read that does not say where it stopped is "
                "indistinguishable from a complete one")

        # ---- P0-4: an unrecognised state becomes UNKNOWN, not OPEN ----------
        p = write_json(os.path.join(tmp, "S19.json"), seed(lambda r: r.update(
            {"issue_states": {"stdout": {"states": {
                "MianliWang/gatebraid#14": "LOCKED",
                "MianliWang/gatebraid#3": "OPEN"}}}})))
        out = os.path.join(tmp, "S19-out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        it = item_of(out, "PVTI_a")
        c.check("S19", "P0-4 an unknown issue state maps to UNKNOWN", "UNKNOWN",
                it.get("issue_state"), "state != OPEN read as unblocked is the defect")
        c.check("S20", "P0-4 and yields undecidable, never unblocked", "undecidable",
                it.get("verdict"), "the unblocked reading is what P0-4 names")
        c.check("S21", "P0-4 the unrecognised value is kept for diagnosis", True,
                it.get("issue_state_raw") is not None,
                "diagnosable without being trusted")

        # ---- P0-4: an unrecognised workflow degrades too ---------------------
        p = write_json(os.path.join(tmp, "S22.json"), seed(lambda r: r.update(
            {"project_items": {"stdout": {"nodes": [
                {"item_id": "PVTI_a", "issue": "MianliWang/gatebraid#14",
                 "slice_metadata_present": True, "slice_id": "P2-S4",
                 "workflow_raw": "Gate 9 - Inventing",
                 "soft_dependencies_declared": False}], "hasNextPage": False}}})))
        out = os.path.join(tmp, "S22-out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        c.check("S22", "P0-4 an unrecognised workflow yields undecidable", "undecidable",
                item_of(out, "PVTI_a").get("verdict"),
                "an open vocabulary would let a new value arrive as a string nobody checks")

        # ---- P0-4: no verdict at all for a non-Slice row --------------------
        out = os.path.join(tmp, "healthy-out.json")
        nonslice = item_of(out, "PVTI_b")
        c.check("S23", "P0-4 a non-Slice row carries no verdict", True,
                "verdict" not in nonslice,
                "a verdict emitted for a non-Slice row is SP-09")
        c.check("S24", "P0-4 and states why it was excluded", True,
                bool(nonslice.get("excluded_reason")),
                "an exclusion nobody can read is indistinguishable from an omission")

        # ---- P0-4: both directions, cross-checked ---------------------------
        p = write_json(os.path.join(tmp, "S25.json"), seed(lambda r: r.update(
            {"dep_blocked_by": {"stdout": {"edges": {
                "MianliWang/gatebraid#14": [{"issue": "MianliWang/gatebraid#3",
                                             "state": "OPEN"}]}}},
             "dep_blocking": {"stdout": {"edges": {}}}})))
        out = os.path.join(tmp, "S25-out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        it = item_of(out, "PVTI_a")
        c.check("S25", "P0-4 a one-directional read is a mismatch", "mismatch",
                it.get("dependencies", {}).get("cross_check"),
                "one direction trusted without the cross-check is SP-11")
        c.check("S26", "P0-4 and a mismatch yields undecidable", "undecidable",
                it.get("verdict"),
                "not a tie broken in favour of the direction that was read")

        # ---- P0-4: a declared soft dependency is parsed, or it says so ------
        p = write_json(os.path.join(tmp, "S27.json"), seed(lambda r: r.update(
            {"project_items": {"stdout": {"nodes": [
                {"item_id": "PVTI_a", "issue": "MianliWang/gatebraid#14",
                 "slice_metadata_present": True, "slice_id": "P2-S4",
                 "workflow_raw": "Needs Plan Approval",
                 "soft_dependencies_declared": True,
                 "soft_dependencies_raw": "   "}], "hasNextPage": False}}})))
        out = os.path.join(tmp, "S27.out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        it = item_of(out, "PVTI_a")
        c.check("S27", "P0-4 an unparsed soft dependency says not_parsed", "not_parsed",
                it.get("soft_dependencies", {}).get("parse_status"),
                "silent ignore is SP-12")
        c.check("S28", "P0-4 and costs the verdict", "undecidable", it.get("verdict"),
                "an unparsed declaration cannot leave the item startable")

        # ---- ADR-0025 decision 8: Aborted is never startable ----------------
        p = write_json(os.path.join(tmp, "S29.json"), seed(lambda r: r.update(
            {"project_items": {"stdout": {"nodes": [
                {"item_id": "PVTI_a", "issue": "MianliWang/gatebraid#14",
                 "slice_metadata_present": True, "slice_id": "P2-S4",
                 "workflow_raw": "Aborted",
                 "soft_dependencies_declared": False}], "hasNextPage": False}}})))
        out = os.path.join(tmp, "S29-out.json")
        rc, _, err = run(["--replay", p, "--out", out])
        c.check("S29", "ADR-0025 d8 an Aborted item is never startable", True,
                item_of(out, "PVTI_a").get("verdict") != "startable",
                "the candidacy intersection, from measured friction #85")

        # ---- P0-2: the byte contract ----------------------------------------
        p = write_json(os.path.join(tmp, "S30.json"), seed(lambda r: r.update(
            {"project_items": {"stdout": {"nodes": [
                {"item_id": "PVTI_a", "issue": "MianliWang/gatebraid#14",
                 "slice_metadata_present": True, "slice_id": "P2-S4",
                 "workflow_raw": em_dash_workflow,
                 "soft_dependencies_declared": False}], "hasNextPage": False}}})))
        rc, stdout_bytes, err = run(["--replay", p])
        c.check("S30", "P0-2 stdout carries the document as UTF-8 bytes", True,
                em_dash_workflow.encode("utf-8") in stdout_bytes,
                "a text-layer write under a non-UTF-8 console corrupts this exact mark")
        c.check("S31", "P0-2 stdout carries the document and nothing else", True,
                stdout_bytes.strip().startswith(b"{") and stdout_bytes.strip().endswith(b"}"),
                "the summary goes to stderr so the byte contract stays clean")

        # ---- self-validation actually gates emission ------------------------
        strict = copy.deepcopy(schema)
        strict.setdefault("required", []).append("a_property_no_document_carries")
        sp = write_json(os.path.join(tmp, "strict-schema.json"), strict)
        p = write_json(os.path.join(tmp, "S33.json"), healthy_transcript())
        out = os.path.join(tmp, "S33-out.json")
        rc, stdout_bytes, err = run(["--replay", p, "--out", out, "--schema", sp])
        c.check("S32", "a document that fails self-validation is not emitted", 1, rc,
                "emitting a malformed snapshot is worse than emitting none",
                "SNAPSHOT NOT EMITTED", err)
        c.check("S33", "and nothing was written to the output path", False,
                os.path.isfile(out),
                "a partial file on disk would be read by the next consumer")

        # ---- usage failures are distinct from degraded reads ----------------
        rc, _, err = run(["--replay", os.path.join(tmp, "does-not-exist.json")])
        c.check("S34", "an absent transcript is a usage error", 2, rc,
                "input failure must not be reported as a degraded read", "USAGE", err)
        rc, _, err = run(["--replay", p, "--page-cap", "0"])
        c.check("S35", "a nonsense page cap is a usage error", 2, rc,
                "a cap of zero would make every read bounded and look like P0-3", "USAGE", err)
        rc, _, err = run(["--replay", p, "--schema", os.path.join(tmp, "no-schema.json")])
        c.check("S36", "an absent schema is a usage error, never a pass", 2, rc,
                "a tool that cannot self-validate must not emit", "STRUCTURE", err)

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    width = max(len(r[1]) for r in c.rows)
    print("%-6s %-*s %-13s %-13s %-7s %s"
          % ("id", width, "condition", "want", "got", "verdict", "required observation"))
    failed = 0
    for cid, name, want, got, ok, obs in c.rows:
        if not ok:
            failed += 1
        print("%-6s %-*s %-13s %-13s %-7s %s"
              % (cid, width, name, str(want)[:13], str(got)[:13],
                 "PASS" if ok else "FAIL", obs))
    print()
    print("scratch directory             : outside every repository (tempfile.mkdtemp)")
    print("tool under test               : %s" % TOOL)
    print("interpreter                   : %s" % sys.executable)
    print("network reads performed       : 0 (every seed served by the replay transport)")
    print("conditions failed             : %d" % failed)
    if failed == 0:
        print("SELFTEST CLEAN: every seeded condition produced its required exit status")
    else:
        print("SELFTEST NOT CLEAN: see the FAIL rows above")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
