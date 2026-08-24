#!/usr/bin/env python3
"""gatebraid-o0-acceptance-selftest - falsify the acceptance harness itself.

ADR-0028 decision 1: a check is falsified once before it is trusted.  The
harness is the instrument that certifies the pair, so the question this file
answers is the one that matters most: WOULD THE HARNESS NOTICE?

A harness that reports CLEAN against the real tools has shown only that the
tools pass it.  It has not shown that it can fail.  This file therefore builds a
COMPLETE PARALLEL TREE in a temporary directory - the harness, the real
producer, the frozen schema and the frozen corpus, with the consumer REPLACED by
a fail-open stub that answers `startable` to everything - and requires the
harness to fail there.  The stub is the P0-1 defect in its purest form: a
consumer that always says yes.  A harness that cannot catch that consumer is
worth nothing, whatever it reports about the real one.

Two further defect shapes are seeded the same way: a consumer that emits nothing
at all (the case must be counted UNEXERCISED, never quietly skipped), and, on a
UTF-8 parent console, a `--byte-contract` run whose own premise fails (it must
refuse rather than credit the binary path with surviving a corruption that never
happened).

Nothing under the repository is written and nothing contacts the network.

Exit codes: 0 all conditions produced their required status - 1 one or more did
not - 2 the harness itself could not run.  Python 3 standard library only.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
HARNESS = os.path.join(HERE, "gatebraid-o0-acceptance.py")
SNAPSHOT = os.path.join(HERE, "gatebraid-snapshot.py")
FRONTIER = os.path.join(HERE, "gatebraid-frontier.py")
SCHEMA = os.path.join(REPO, "schema", "snapshot.schema.json")
CORPUS = os.path.join(REPO, "fixtures", "state-pipeline")

FAIL_OPEN_CONSUMER = '''#!/usr/bin/env python3
"""A deliberately FAIL-OPEN consumer: it answers `startable` to everything.

This is the defect M3 node O0 exists to remove, written down so the acceptance
harness can be measured against it. It validates nothing and reads nothing.
"""
import argparse, json, sys

ap = argparse.ArgumentParser()
ap.add_argument("snapshot")
ap.add_argument("--out")
ap.add_argument("--schema")
args = ap.parse_args()

report = {
    "report": "gatebraid/frontier-report@1",
    "snapshot_degraded": False,
    "verdicts": [{"item_id": "stub", "issue": "stub#1", "slice_id": "P9-S1",
                  "workflow": "Backlog", "verdict": "startable",
                  "declared_verdict": "startable", "reasons": ["stub"]}],
    "excluded": [],
    "summary": {"startable": 1, "blocked": 0, "undecidable": 0, "excluded": 0},
}
data = (json.dumps(report) + "\\n").encode("utf-8")
if args.out:
    open(args.out, "wb").write(data)
else:
    sys.stdout.buffer.write(data)
sys.exit(0)
'''

SILENT_CONSUMER = '''#!/usr/bin/env python3
"""A consumer that emits nothing at all. The case must be counted unexercised."""
import sys
sys.exit(0)
'''


def build_tree(tmp, consumer_source):
    """A complete parallel repository with one half swapped out."""
    root = tempfile.mkdtemp(prefix="tree-", dir=tmp)
    os.makedirs(os.path.join(root, "bin"))
    os.makedirs(os.path.join(root, "schema"))
    os.makedirs(os.path.join(root, "fixtures"))
    shutil.copy(HARNESS, os.path.join(root, "bin", "gatebraid-o0-acceptance.py"))
    shutil.copy(SNAPSHOT, os.path.join(root, "bin", "gatebraid-snapshot.py"))
    shutil.copy(SCHEMA, os.path.join(root, "schema", "snapshot.schema.json"))
    shutil.copytree(CORPUS, os.path.join(root, "fixtures", "state-pipeline"))
    with open(os.path.join(root, "bin", "gatebraid-frontier.py"), "w",
              encoding="utf-8") as fh:
        fh.write(consumer_source)
    return root


def run(argv, cwd=None):
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([sys.executable, "-B"] + argv, cwd=cwd or REPO,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


class Conditions(object):
    def __init__(self):
        self.rows = []

    def check(self, cid, name, want, got, observation, marker=None, output=""):
        ok = (got == want)
        if marker is not None:
            ok = ok and (marker in output)
        self.rows.append((cid, name, want, got, ok, observation))
        return ok


def main():
    for required in (HARNESS, SNAPSHOT, FRONTIER, SCHEMA, CORPUS):
        if not os.path.exists(required):
            print("HARNESS: required input not found at %s" % required)
            return 2

    tmp = tempfile.mkdtemp(prefix="gatebraid-o0-acceptance-selftest-")
    c = Conditions()
    try:
        # ---- the real pair passes every mode --------------------------------
        for cid, mode in (("A01", "--induced-failures"),
                          ("A02", "--dependency-directions"),
                          ("A03", "--corpus")):
            rc, out = run([HARNESS, mode])
            c.check(cid, "the real pair passes %s" % mode, 0, rc,
                    "the positive control: a harness that failed here would be "
                    "measuring its own defect", "ACCEPTANCE CLEAN", out)

        if os.name == "nt":
            rc, out = run([HARNESS, "--byte-contract"])
            c.check("A04", "the real pair passes --byte-contract", 0, rc,
                    "the cp936 premise holds on this host", "ACCEPTANCE CLEAN", out)
        else:
            rc, out = run([HARNESS, "--byte-contract"])
            c.check("A04", "--byte-contract refuses where its premise cannot hold",
                    2, rc,
                    "a run that cannot establish its premise must not report a "
                    "pass", "USAGE", out)

        # ---- THE CENTRAL CONDITION: a fail-open consumer is caught ----------
        root = build_tree(tmp, FAIL_OPEN_CONSUMER)
        stub_harness = os.path.join(root, "bin", "gatebraid-o0-acceptance.py")
        rc, out = run([stub_harness, "--induced-failures"], cwd=root)
        c.check("A05", "a fail-open consumer makes the harness FAIL", 1, rc,
                "a consumer that always says startable is the P0-1 defect itself",
                "ACCEPTANCE NOT CLEAN", out)
        c.check("A06", "and every induced case is reported failing", True,
                "cases failing                 : 12" in out,
                "all twelve, not a sample: each class is independently seeded")
        c.check("A07", "and the summary does not claim undecidable coverage", True,
                "induced classes carrying undecidable : 0 / 12" in out,
                "the summary line must move with the measurement")

        rc, out = run([stub_harness, "--dependency-directions"], cwd=root)
        c.check("A08", "a fail-open consumer fails dependency-directions too", 1, rc,
                "the cross-check clauses are where a fail-open consumer hides",
                "ACCEPTANCE NOT CLEAN", out)

        rc, out = run([stub_harness, "--corpus"], cwd=root)
        c.check("A09", "and is caught over the frozen corpus", 1, rc,
                "a consumer that refuses nothing accepts every corpus negative",
                "ACCEPTANCE NOT CLEAN", out)

        # ---- a silent consumer is UNEXERCISED, never a quiet skip -----------
        root2 = build_tree(tmp, SILENT_CONSUMER)
        silent_harness = os.path.join(root2, "bin", "gatebraid-o0-acceptance.py")
        rc, out = run([silent_harness, "--induced-failures"], cwd=root2)
        c.check("A10", "a silent consumer exits 1, never 0", 1, rc,
                "an unexercised case is a failure, not a skip",
                "ACCEPTANCE NOT CLEAN", out)
        c.check("A11", "and the cases are counted unexercised", True,
                "classes reported unexercised  : 12" in out,
                "a case nobody ran must be visible as such in the summary")

        # ---- the report file is written and says what the table said --------
        out_path = os.path.join(tmp, "report.json")
        rc, out = run([HARNESS, "--induced-failures", "--out", out_path])
        doc = json.load(open(out_path, encoding="utf-8")) if os.path.isfile(out_path) else {}
        c.check("A12", "the report file is written", True, os.path.isfile(out_path),
                "the JSON and the printed table are the same measurement")
        c.check("A13", "and records the run as clean", True,
                bool(doc.get("summary", {}).get("clean")),
                "a machine reader must reach the same verdict as the human one")
        c.check("A14", "and carries every declared case", 12,
                len(doc.get("cases") or []),
                "the file is the record, not a summary of one")

        out_path2 = os.path.join(tmp, "stub-report.json")
        rc, out = run([stub_harness, "--induced-failures", "--out", out_path2],
                      cwd=root)
        doc2 = json.load(open(out_path2, encoding="utf-8")) if os.path.isfile(out_path2) else {}
        c.check("A15", "and records a failing run as NOT clean", False,
                bool(doc2.get("summary", {}).get("clean")),
                "the file must not disagree with the exit status")

        # ---- usage discipline ------------------------------------------------
        rc, out = run([HARNESS])
        c.check("A16", "no mode selected is a usage error", 2, rc,
                "a harness with no mode must not default to the cheapest one")
        rc, out = run([HARNESS, "--induced-failures", "--corpus"])
        c.check("A17", "two modes at once is a usage error", 2, rc,
                "one mode, one summary, one exit status")

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
    print("harness under test            : %s" % HARNESS)
    print("interpreter                   : %s" % sys.executable)
    print("falsification method          : a complete parallel tree with the "
          "consumer replaced by a fail-open stub")
    print("network reads performed       : 0")
    print("conditions failed             : %d" % failed)
    if failed == 0:
        print("SELFTEST CLEAN: every seeded condition produced its required exit status")
    else:
        print("SELFTEST NOT CLEAN: see the FAIL rows above")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
