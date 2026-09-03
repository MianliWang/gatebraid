"""Verify every Gate 0 capture twice: the capture tool's own guard, and the
independent validator.

Clause 5 of the Gate 0 Opening comment requires this gate's captures to be
machine-validated with the landed bin/gatebraid-validate.py, not only its
record. Two independent checkers are run over every capture:

  layer 1  bin/gatebraid-capture.py --verify-record --rederive
           the same guard the write path uses, plus the re-derivation layer,
           so a capture whose recorded digests do not reproduce is rejected
           rather than trusted;
  layer 2  bin/gatebraid-validate.py --record
           the N3 validator, which re-derives verdicts independently of the
           tool that wrote the file.

A capture is accepted only if BOTH accept it. Disagreement between the two is
itself a failure, and is printed rather than reconciled.

Documents in this directory that are not gatebraid/evidence-capture@1 — the
snapshot and frontier documents this gate produced — are checked by layer 2
only, because layer 1's guard is defined for capture records. Which layers ran
is printed per file rather than left to be inferred.

This driver's own capture does not appear in the set it checks: the capture
tool writes that file after this process exits, so at run time it does not
exist. Stated rather than left to be noticed.
"""
import glob, json, os, subprocess, sys

CAP = "docs/evidence/gatebraid/P2-S5/captures"
PY = "C:/Python312/python.exe"
CAPTURE_TOOL = "bin/gatebraid-capture.py"
VALIDATE_TOOL = "bin/gatebraid-validate.py"


def run(argv):
    r = subprocess.run(argv, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    tail = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    return r.returncode, (tail[-1] if tail else "(no output)")


def is_capture(path):
    try:
        return json.load(open(path, encoding="utf-8")).get("schema") == \
            "gatebraid/evidence-capture@1"
    except Exception:
        return False


files = sorted(glob.glob(os.path.join(CAP, "*.json")))
ok = bad = uncovered = 0
failures = []
uncovered_docs = []

for f in files:
    base = os.path.basename(f)
    cap_doc = is_capture(f)
    if cap_doc:
        rc1, v1 = run([PY, "-B", CAPTURE_TOOL, "--verify-record", f, "--rederive"])
    else:
        rc1, v1 = 0, "(layer 1 n/a: not a capture record)"
    rc2, v2 = run([PY, "-B", VALIDATE_TOOL, "--record", f])

    layers = "guard+rederive,validate" if cap_doc else "validate"

    # Layer 2 exit 2 is, by the validator's own exit-code contract, a usage or
    # input error — not a verdict on the document. For a document that is not
    # an evidence-capture@1 record it means the validator does not route this
    # interface at all. Two distinct causes were measured here, and neither is
    # a rejection:
    #   g0-snapshot.json        declares unknown interface 'gatebraid/snapshot@1'
    #   g0-frontier-report.json declares no `schema` key at all — the frontier
    #                           document names its interface under `report`
    # Conflating "this checker does not cover this interface" with "this
    # checker rejected this document" misreports both, so the class is counted
    # and named rather than folded into either. Classification is on the exit
    # code, not on message text, so a reworded message cannot silently move a
    # document between classes. A capture record that exits 2 is NOT excused.
    if rc2 == 2 and not cap_doc:
        uncovered += 1
        status = "NOT-COVERED"
        uncovered_docs.append((base, v2))
    elif rc1 == 0 and rc2 == 0:
        ok += 1
        status = "accepted"
    else:
        bad += 1
        status = "REJECTED"
        failures.append((base, rc1, v1, rc2, v2))
    print("%-38s %-24s L1=%d L2=%d  %s" % (base, layers, rc1, rc2, status))

print()
print("documents checked        : %d" % len(files))
print("accepted by both layers  : %d" % ok)
print("rejected                 : %d" % bad)
print("interface not covered    : %d" % uncovered)
for base, v2 in uncovered_docs:
    print("   NOT-COVERED %-30s %s" % (base, v2[:90]))
for base, rc1, v1, rc2, v2 in failures:
    print("   REJECTED %s" % base)
    print("      layer1 exit=%d %s" % (rc1, v1[:80]))
    print("      layer2 exit=%d %s" % (rc2, v2[:80]))
sys.exit(1 if bad else 0)
