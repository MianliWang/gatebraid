"""Verify every Gate 0 capture with the capture tool's own guard, layer B included.

The State Packet Approval section 4 requires this gate's captures to be
machine-validated, not only its record. bin/gatebraid-capture.py --verify-record
applies the same guard the write path uses; --rederive adds the re-derivation
layer, so a capture whose recorded digests do not reproduce is rejected rather
than trusted.

This driver's own capture does not appear in the set it checks: the capture tool
writes that file after this process exits, so at run time it does not exist.
Stated rather than left to be noticed.
"""
import glob, os, subprocess, sys

CAP = "docs/evidence/gatebraid/P2-S4/captures"
PY = "C:/Python312/python.exe"
TOOL = "bin/gatebraid-capture.py"

files = sorted(glob.glob(os.path.join(CAP, "*.json")))
ok = bad = 0
failures = []
for f in files:
    r = subprocess.run([PY, "-B", TOOL, "--verify-record", f, "--rederive"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    tail = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    verdict = tail[-1] if tail else "(no output)"
    if r.returncode == 0:
        ok += 1
    else:
        bad += 1
        failures.append((os.path.basename(f), r.returncode, verdict))
    print("%-46s exit=%d  %s" % (os.path.basename(f), r.returncode, verdict[:60]))

print()
print("captures verified : %d" % len(files))
print("accepted          : %d" % ok)
print("rejected          : %d" % bad)
for name, rc, v in failures:
    print("   REJECTED %-42s exit=%d  %s" % (name, rc, v[:70]))
sys.exit(1 if bad else 0)
