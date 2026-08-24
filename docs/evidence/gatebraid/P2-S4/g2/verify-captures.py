"""Verify every Gate 2 capture with the capture tool's own guard, layer B included.

`bin/gatebraid-capture.py --verify-record` applies the SAME guard the write path
uses; `--rederive` adds the re-derivation layer, so a capture whose recorded
digests do not reproduce is rejected rather than trusted. Machine-validating this
gate's captures, and not only its record, is what makes the record's
`output_ref` targets evidence rather than filenames.

Takes the directory as an argument rather than hard-coding it, so the same
instrument serves any gate's capture set.

TWO CAPTURES CANNOT BE IN THE SET THIS CHECKS, and both are named rather than
left to be noticed: this driver's own capture, which the capture tool writes
after this process exits, and any capture written later in the gate.

Usage: verify-captures.py <capture-dir>
Exit codes: 0 every capture verified - 1 at least one did not - 2 usage error.
"""
import glob
import os
import subprocess
import sys

if len(sys.argv) != 2:
    print("USAGE: verify-captures.py <capture-dir>")
    raise SystemExit(2)

CAP = sys.argv[1]
TOOL = "bin/gatebraid-capture.py"

if not os.path.isdir(CAP):
    print("USAGE: %s is not a directory" % CAP)
    raise SystemExit(2)

files = sorted(glob.glob(os.path.join(CAP, "*.json")))
if not files:
    print("USAGE: no captures found under %s; a sweep that checked nothing "
          "must not report a pass" % CAP)
    raise SystemExit(2)

env = dict(os.environ)
env["PYTHONDONTWRITEBYTECODE"] = "1"

ok = 0
failures = []
for f in files:
    r = subprocess.run([sys.executable, "-B", TOOL, "--verify-record", f,
                        "--rederive"],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       env=env)
    text = r.stdout.decode("utf-8", "replace")
    tail = [l for l in text.splitlines() if l.strip()]
    verdict = tail[-1] if tail else "(no output)"
    if r.returncode == 0:
        ok += 1
    else:
        failures.append((os.path.basename(f), r.returncode, verdict))

print("capture directory             : %s" % CAP)
print("guard                         : %s --verify-record --rederive" % TOOL)
print("interpreter                   : %s" % sys.executable)
print("captures found                : %d" % len(files))
print("captures verified             : %d" % ok)
print("captures rejected             : %d" % len(failures))
for name, rc, verdict in failures:
    print("   %-40s exit=%d  %s" % (name, rc, verdict))
print("not in this set               : this driver's own capture, written by "
      "the capture tool after this process exits")
if failures:
    print("CAPTURES NOT CLEAN: see the rejected rows above")
    raise SystemExit(1)
print("CAPTURES CLEAN: every capture reproduced its recorded digests under the "
      "write path's own guard")
