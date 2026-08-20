#!/usr/bin/env python3
"""T6/V6 — negative criterion N1: no path outside the frozen allowlist.

Reconstruction. The script the Gate 2 V6 row invoked (`_t6.py`) was written at
the repository root, was never committed, and is not recoverable. This file
reproduces that row's check and its output shape, and is committed so the row
is re-runnable as written. It is not the original bytes (gate2.md, Required
disclosures).

Reads the changed-path set on stdin, one path per line, so the CALLER fixes the
comparison range. gate1.md states N1's scope as "the complete output of
`git diff --name-only <base>..<rev>`"; passing that output in keeps the range
explicit and auditable instead of burying a moving ref inside the checker
(ADR-0028 section 4: no row names a state the act of recording it will move).

The criterion ERRS TOWARD FALSE FAILURE by design: any path outside the two
prefixes fails it whether or not the path is benign, so a pass is informative
and a failure requires a human look.

Usage:  git diff --name-only <base>..<rev> | python3 t6.py
Exit 0 when every path is inside the allowlist, 1 otherwise.
"""
from __future__ import annotations

import sys

ALLOWLIST = ("bin/", "docs/evidence/gatebraid/P2-S1/")


def main() -> int:
    paths = [line.strip() for line in sys.stdin.read().splitlines() if line.strip()]

    outside = []
    for p in paths:
        inside = any(p.startswith(prefix) for prefix in ALLOWLIST)
        print("    %s %s" % (p, "OK" if inside else "OUTSIDE"))
        if not inside:
            outside.append(p)

    print("paths scanned: %d" % len(paths))
    print("allowlist: %s" % list(ALLOWLIST))
    print("outside allowlist: %s" % ("NONE" if not outside else outside))
    return 1 if outside else 0


if __name__ == "__main__":
    sys.exit(main())
