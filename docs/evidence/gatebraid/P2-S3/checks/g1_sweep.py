#!/usr/bin/env python3
"""P2-S3 verification sweep — runs `gatebraid-validate --record` over a path set
and reports each non-accepted document with the instrument's OWN emitted
findings.

This is verification tooling, not Slice implementation: the Slice's
implementation is `bin/gatebraid-validate.py` and
`bin/gatebraid-validate-selftest.py`. It lives under this Slice's evidence
prefix, which is inside the frozen allowlist.

It prints no totals it did not observe and asserts no expected count: the
acceptance it serves is count-free (friction #173 — a count carried from a
document rather than re-derived at execution). The trailing
`rejected_or_errored=` figure is a re-derivation from this run, offered as an
observation, never as a threshold.

Usage:
    g1_sweep.py <python-interpreter> <glob> [<glob> ...]

Exit 0 = every document in the path set was accepted.
Exit 1 = at least one was rejected (exit 1) or errored (exit 2).
Exit 2 = the path set matched nothing, which is a usage error rather than a
         clean sweep: an empty set trivially satisfies "all accepted" and that
         is the P0-3 shape (a truncated list silently treated as complete).
"""
import glob
import os
import re
import subprocess
import sys

FINDING = re.compile(r"\s+F\d+\s")


def main(argv):
    if len(argv) < 3:
        print("usage: g1_sweep.py <python-interpreter> <glob> [<glob> ...]")
        return 2
    py, patterns = argv[1], argv[2:]

    paths = []
    for pat in patterns:
        paths.extend(glob.glob(pat))
    paths = sorted(set(paths))
    if not paths:
        print("USAGE: the path set matched nothing; an empty sweep is not a clean sweep")
        return 2

    print("interpreter   : %s" % py)
    print("documents     : %d" % len(paths))
    bad = 0
    for path in paths:
        proc = subprocess.run([py, "bin/gatebraid-validate.py", "--record", path],
                              capture_output=True, text=True)
        if proc.returncode == 0:
            continue
        bad += 1
        print("%s rc=%d" % (os.path.basename(path), proc.returncode))
        for line in proc.stdout.splitlines():
            if FINDING.match(line):
                print(line)
        if proc.returncode == 2:
            first = (proc.stdout.strip().splitlines() or [""])[0]
            print("   %s" % first[:110])
    print("SWEEP COMPLETE rejected_or_errored=%d" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
