#!/usr/bin/env python3
"""K1 — the landed bin/ pair is byte-identical to the blobs bound at N2-R2.

Discharges plan task K1 ("verified by `git hash-object` equalling the bound
blob for each"). The Gate 2 record asserted this check as `pass` behind an
`output_ref` that resolved to no row; this script is the row's generator.

The commit is taken as an ARGUMENT and must be a full 40-hex sha, never `HEAD`:
ADR-0028 section 4 forbids a record naming a state the act of recording it will
move. Blob ids are read from the object database, so the answer does not depend
on the working tree at all.

Usage:  python3 k1_blobs.py <40-hex-commit-sha>
Exit 0 when both blobs match and bin/ carries no extra path, 1 otherwise.
"""
from __future__ import annotations

import re
import subprocess
import sys

# Frozen at N2-R2 and restated in gate1.md's plan; these are the bound values.
BOUND = {
    "bin/gatebraid-capture.py": ("43ff5a06c7f7e1e9b0ba5d6f14e956bc8d4c73d0", 43335),
    "bin/gatebraid-capture-selftest.py": ("a40869bea3d1e8dbaf20473456f919838f788eec", 40846),
}


def git(*args: str) -> str:
    out = subprocess.run(("git",) + args, capture_output=True, check=True)
    return out.stdout.decode("utf-8").strip()


def main(argv: list[str]) -> int:
    if len(argv) != 2 or not re.fullmatch(r"[0-9a-f]{40}", argv[1]):
        print("usage: k1_blobs.py <40-hex-commit-sha>", file=sys.stderr)
        return 2
    commit = argv[1]

    landed: dict[str, str] = {}
    for line in git("ls-tree", commit, "bin/").splitlines():
        meta, path = line.split("\t", 1)
        landed[path] = meta.split()[2]

    print("commit: %s" % commit)
    print("%-34s %-42s %-42s %s" % ("path", "bound", "landed", "verdict"))

    mismatches = 0
    for path, (want, want_size) in sorted(BOUND.items()):
        got = landed.get(path, "<absent>")
        size = int(git("cat-file", "-s", got)) if got != "<absent>" else -1
        ok = got == want and size == want_size
        if not ok:
            mismatches += 1
        print("%-34s %-42s %-42s %s" % (path, want, got, "MATCH" if ok else "DIFFER"))
        print("%-34s %-42d %-42d %s"
              % ("  bytes", want_size, size, "MATCH" if size == want_size else "DIFFER"))

    extra = sorted(set(landed) - set(BOUND))
    print("extra paths under bin/: %s" % ("NONE" if not extra else extra))
    print("blobs compared: %d  mismatches: %d" % (len(BOUND), mismatches))
    return 1 if (mismatches or extra) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
