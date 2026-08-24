#!/usr/bin/env python3
"""gatebraid-frontier-selftest - falsify the snapshot consumer before it is trusted.

ADR-0028 decision 1: a check is falsified once before it is trusted.  This file
seeds a condition for every rule `gatebraid-frontier` claims to enforce and
asserts the EXIT STATUS each must produce, plus a required observation where the
exit status alone would not separate the outcomes.

THE SEEDS ARE DERIVED FROM THE FROZEN CORPUS, not invented here.  The base
document is `fixtures/state-pipeline/valid-canonical-snapshot.json`, and each
seed breaks exactly ONE relation in it.  Corpus material is used directly where
the corpus already carries the case - notably N4's behavioural half, which uses
`sp10-snapshot-missing-schema-key.json` as the frozen plan names it rather than
a lookalike authored beside the test.

TWO DIRECTIONS, ALWAYS.  A tool that refused everything would pass every
negative condition below, so the positive controls (F01-F04) carry equal weight:
they are the conditions a reject-everything consumer fails.  That is the GR2-07
lesson the corpus records, applied to the consuming half.

Nothing here contacts the network and nothing under the repository is written:
seeds go to a temporary directory OUTSIDE every repository
(`tempfile.mkdtemp()`), which `protocols/gate-2-contract.md` permits explicitly
and which this Slice's Gate 2 evidence names.

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
TOOL = os.path.join(HERE, "gatebraid-frontier.py")
SCHEMA = os.path.join(REPO, "schema", "snapshot.schema.json")
CORPUS = os.path.join(REPO, "fixtures", "state-pipeline")
CANONICAL = os.path.join(CORPUS, "valid-canonical-snapshot.json")
MISSING_SCHEMA_KEY = os.path.join(CORPUS, "sp10-snapshot-missing-schema-key.json")
UNKNOWN_STATE = os.path.join(CORPUS, "sp08-unknown-state-treated-unblocked.json")


def run(args):
    """Invoke the tool as a subprocess so the EXIT STATUS is the real one.

    stdout is kept as BYTES: this harness checks a byte contract, and a harness
    that decodes before comparing cannot see the defect it exists to catch.
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


class Conditions(object):
    def __init__(self):
        self.rows = []

    def check(self, cid, name, want, got, observation, marker=None, output=""):
        ok = (got == want)
        if marker is not None:
            ok = ok and (marker in output)
        self.rows.append((cid, name, want, got, ok, observation))
        return ok


def report_of(path):
    if not os.path.isfile(path):
        return {}
    return json.load(open(path, encoding="utf-8"))


def only_verdict(path):
    rep = report_of(path)
    v = rep.get("verdicts") or []
    return v[0].get("verdict") if v else "<no verdict>"


def main():
    for required in (TOOL, SCHEMA, CANONICAL, MISSING_SCHEMA_KEY, UNKNOWN_STATE):
        if not os.path.isfile(required):
            print("HARNESS: required input not found at %s" % required)
            return 2

    base = json.load(open(CANONICAL, encoding="utf-8"))
    schema = json.load(open(SCHEMA, encoding="utf-8"))
    # Read, never typed: four Workflow values carry U+2014.
    workflows = schema["$defs"]["item"]["properties"]["workflow"]["enum"]
    em_dash_workflow = next(w for w in workflows if "—" in w)

    def seed(mutate):
        doc = copy.deepcopy(base)
        mutate(doc)
        return doc

    tmp = tempfile.mkdtemp(prefix="gatebraid-frontier-selftest-")
    c = Conditions()
    try:
        # ---- positive controls: a reject-everything consumer fails HERE -----
        out = os.path.join(tmp, "F01.json")
        rc, _, err = run([CANONICAL, "--out", out])
        c.check("F01", "the canonical corpus snapshot is consumed", 0, rc,
                "the condition a reject-everything consumer fails", "FRONTIER OK", err)
        c.check("F02", "and its verdict is re-derived as startable", "startable",
                only_verdict(out), "fail-closed is not reject-everything")

        out = os.path.join(tmp, "F03.json")
        rc, _, err = run([os.path.join(CORPUS, "valid-non-slice-item-excluded.json"),
                          "--out", out])
        rep = report_of(out)
        c.check("F03", "a non-Slice row yields no verdict at all", 0,
                len(rep.get("verdicts") or []),
                "not undecidable, not absent-and-unexplained: no verdict")
        c.check("F04", "and is excluded with a stated reason", True,
                bool((rep.get("excluded") or [{}])[0].get("excluded_reason")),
                "an exclusion nobody can read is indistinguishable from an omission")

        out = os.path.join(tmp, "F05.json")
        rc, _, err = run([os.path.join(CORPUS, "valid-aborted-item-not-startable.json"),
                          "--out", out])
        c.check("F05", "ADR-0025 d8 an Aborted item is never startable", True,
                only_verdict(out) != "startable",
                "the candidacy intersection, whatever the edges say")

        # ---- N4 behavioural half, on the fixture the frozen plan names ------
        out = os.path.join(tmp, "F06.json")
        rc, stdout_bytes, err = run([MISSING_SCHEMA_KEY, "--out", out])
        c.check("F06", "N4 a document with no schema key is REFUSED", 1, rc,
                "consumed as if current is SP-10", "SNAPSHOT REFUSED", err)
        c.check("F07", "N4 and no verdict is emitted for it", False,
                os.path.isfile(out),
                "no verdict without validation, measured rather than intended")
        c.check("F08", "N4 and nothing reaches stdout either", 0, len(stdout_bytes),
                "a report on stdout would be consumed by the next stage in a pipe")

        # ---- the validated-snapshot type cannot be forged -------------------
        probe = (
            "import sys; sys.path.insert(0, %r);\n"
            "import importlib.util as u;\n"
            "spec = u.spec_from_file_location('gf', %r); m = u.module_from_spec(spec);\n"
            "spec.loader.exec_module(m);\n"
            "try:\n"
            "    m.ValidatedSnapshot({}, 'p', 's', object())\n"
            "    print('FORGED')\n"
            "except m.SnapshotRefused:\n"
            "    print('REFUSED')\n" % (HERE, TOOL))
        pp = os.path.join(tmp, "forge.py")
        with open(pp, "w", encoding="utf-8") as fh:
            fh.write(probe)
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        proc = subprocess.run([sys.executable, "-B", pp], cwd=REPO,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        c.check("F09", "N4 a consumable snapshot cannot be forged", "REFUSED",
                proc.stdout.decode("utf-8", "replace").strip(),
                "the structural half: a verdict path needs an object only "
                "validate() can construct")

        # ---- P0-4: degradation forces undecidable ---------------------------
        out = os.path.join(tmp, "F10.json")
        rc, _, err = run([os.path.join(CORPUS, "valid-degraded-all-undecidable.json"),
                          "--out", out])
        c.check("F10", "a degraded snapshot exits 3, never 0", 3, rc,
                "the exit status is the only thing a shell caller reads",
                "FRONTIER UNDECIDABLE", err)
        c.check("F11", "and every item is undecidable", "undecidable",
                only_verdict(out), "P0-1's kill, enforced at the consuming end too")

        # ---- P0-4: an unknown Issue state ------------------------------------
        p = write_json(os.path.join(tmp, "F12-in.json"), seed(
            lambda d: (d["items"][0].update({"issue_state": "UNKNOWN",
                                             "issue_state_raw": "LOCKED",
                                             "verdict": "undecidable"}))))
        out = os.path.join(tmp, "F12.json")
        rc, _, err = run([p, "--out", out])
        c.check("F12", "P0-4 an UNKNOWN issue state is undecidable", "undecidable",
                only_verdict(out), "state != OPEN read as unblocked is the defect")

        # ---- P0-4: the cross-check ------------------------------------------
        for cid, value, why in (("F13", "not_performed", "a cross-check that never happened"),
                                ("F14", "mismatch", "the two directions disagreeing")):
            p = write_json(os.path.join(tmp, cid + "-in.json"), seed(
                lambda d, v=value: (d["items"][0]["dependencies"].update({"cross_check": v}),
                                    d["items"][0].update({"verdict": "undecidable"}))))
            out = os.path.join(tmp, cid + ".json")
            rc, _, err = run([p, "--out", out])
            c.check(cid, "P0-4 %s is undecidable" % value, "undecidable",
                    only_verdict(out), why)

        # ---- P0-4: a declared soft dependency that was not parsed ------------
        p = write_json(os.path.join(tmp, "F15-in.json"), seed(
            lambda d: (d["items"][0]["soft_dependencies"].update(
                {"declared": True, "parse_status": "not_parsed"}),
                d["items"][0].update({"verdict": "undecidable"}))))
        out = os.path.join(tmp, "F15.json")
        rc, _, err = run([p, "--out", out])
        c.check("F15", "P0-4 an unparsed soft dependency is undecidable", "undecidable",
                only_verdict(out), "silent ignore is SP-12")

        # ---- P0-4: an unrecognised Workflow ----------------------------------
        p = write_json(os.path.join(tmp, "F16-in.json"), seed(
            lambda d: d["items"][0].update({"workflow": "UNKNOWN",
                                            "verdict": "undecidable"})))
        out = os.path.join(tmp, "F16.json")
        rc, _, err = run([p, "--out", out])
        c.check("F16", "P0-4 an UNKNOWN workflow is undecidable", "undecidable",
                only_verdict(out), "an open vocabulary arrives as a string nobody checks")

        # ---- an open blocking edge blocks; an unknown-state edge does not
        #      resolve in the permissive direction --------------------------
        p = write_json(os.path.join(tmp, "F17-in.json"), seed(
            lambda d: (d["items"][0]["dependencies"]["blocked_by"].append(
                {"issue": "MianliWang/gatebraid#5", "state": "OPEN"}),
                d["items"][0]["dependencies"]["blocking"].clear(),
                d["items"][0]["dependencies"].update({"cross_check": "consistent"}),
                d["items"][0].update({"verdict": "blocked"}))))
        out = os.path.join(tmp, "F17.json")
        rc, _, err = run([p, "--out", out])
        c.check("F17", "an open blocking edge yields blocked", "blocked",
                only_verdict(out), "the ordinary negative case, still measured")

        p = write_json(os.path.join(tmp, "F18-in.json"), seed(
            lambda d: (d["items"][0]["dependencies"]["blocked_by"].append(
                {"issue": "MianliWang/gatebraid#5", "state": "UNKNOWN"}),
                d["items"][0]["dependencies"]["blocking"].clear(),
                d["items"][0].update({"verdict": "undecidable"}))))
        out = os.path.join(tmp, "F18.json")
        rc, _, err = run([p, "--out", out])
        c.check("F18", "an edge with an unknown state is undecidable", "undecidable",
                only_verdict(out), "never resolved toward not-blocking")

        # ---- the producer's own verdict is not trusted -----------------------
        p = write_json(os.path.join(tmp, "F19-in.json"), seed(
            lambda d: d["items"][0].update({"verdict": "blocked"})))
        out = os.path.join(tmp, "F19.json")
        rc, _, err = run([p, "--out", out])
        c.check("F19", "a declared verdict that disagrees is undecidable", "undecidable",
                only_verdict(out),
                "echoing the producer would inherit every producer defect silently")

        # ---- P0-4's version check, before consumption ------------------------
        p = write_json(os.path.join(tmp, "F20-in.json"), seed(
            lambda d: d.update({"schema": "gatebraid/snapshot@2"})))
        rc, _, err = run([p, "--out", os.path.join(tmp, "F20.json")])
        c.check("F20", "an unrecognised interface is refused", 1, rc,
                "never read as if current", "SNAPSHOT REFUSED", err)

        p = write_json(os.path.join(tmp, "F21-in.json"),
                       seed(lambda d: d.pop("snapshot_version")))
        rc, _, err = run([p, "--out", os.path.join(tmp, "F21.json")])
        c.check("F21", "an absent snapshot_version is refused", 1, rc,
                "P0-4 requires both present rather than inferred", "SNAPSHOT REFUSED", err)

        p = write_json(os.path.join(tmp, "F22-in.json"),
                       seed(lambda d: d.update({"snapshot_version": 99})))
        rc, _, err = run([p, "--out", os.path.join(tmp, "F22.json")])
        c.check("F22", "an unsupported snapshot_version is refused", 1, rc,
                "a future shape is not consumed by a tool that predates it",
                "SNAPSHOT REFUSED", err)

        # ---- a structurally invalid document is refused ----------------------
        rc, _, err = run([UNKNOWN_STATE, "--out", os.path.join(tmp, "F23.json")])
        c.check("F23", "a corpus negative fails schema validation and is refused", 1, rc,
                "the schema still governs; reading a document is not accepting it",
                "does not validate", err)

        # ---- P0-2: the consuming half of the byte contract -------------------
        bad = os.path.join(tmp, "F24-in.json")
        with open(bad, "wb") as fh:
            fh.write(b'{"schema": "gatebraid/snapshot@1", "x": "\xff\xfe not utf-8"}')
        rc, _, err = run([bad, "--out", os.path.join(tmp, "F24.json")])
        c.check("F24", "P0-2 a non-UTF-8 document is refused, not repaired", 1, rc,
                "errors=replace here would manufacture the very corruption "
                "the contract detects", "SNAPSHOT REFUSED", err)

        p = write_json(os.path.join(tmp, "F25-in.json"), seed(
            lambda d: d["items"][0].update({"workflow": em_dash_workflow,
                                            "verdict": "startable"})))
        rc, stdout_bytes, err = run([p])
        c.check("F25", "P0-2 the report reaches stdout as UTF-8 bytes", True,
                em_dash_workflow.encode("utf-8") in stdout_bytes,
                "a text-layer write under a cp936 console corrupts this exact mark")
        c.check("F26", "P0-2 stdout carries the report and nothing else", True,
                stdout_bytes.strip().startswith(b"{")
                and stdout_bytes.strip().endswith(b"}"),
                "the summary goes to stderr so the byte contract stays clean")

        # ---- malformed input is refused, not consumed ------------------------
        bad = os.path.join(tmp, "F27-in.json")
        with open(bad, "wb") as fh:
            fh.write(b"{not json")
        rc, _, err = run([bad, "--out", os.path.join(tmp, "F27.json")])
        c.check("F27", "a document that is not JSON is refused", 1, rc,
                "a broken input must not become a verdict", "SNAPSHOT REFUSED", err)

        # ---- usage failures stay distinct from refusals ----------------------
        rc, _, err = run([os.path.join(tmp, "absent.json")])
        c.check("F28", "an absent document is a usage error, not a refusal", 2, rc,
                "the caller must tell its own mistake from a measurement", "USAGE", err)
        rc, _, err = run([CANONICAL, "--schema", os.path.join(tmp, "no-schema.json")])
        c.check("F29", "an absent schema is a usage error, never a pass", 2, rc,
                "a tool that cannot validate must not emit a verdict", "STRUCTURE", err)

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
    print("seeds derived from            : %s" % CANONICAL)
    print("network reads performed       : 0")
    print("conditions failed             : %d" % failed)
    if failed == 0:
        print("SELFTEST CLEAN: every seeded condition produced its required exit status")
    else:
        print("SELFTEST NOT CLEAN: see the FAIL rows above")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
