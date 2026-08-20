#!/usr/bin/env python3
"""T5/V5 — closed-set complement over a set of roots.

Reconstruction. The script the Gate 2 V5 row invoked (`_t5.py`) was written at
the repository root, was never committed, and is not recoverable. This file
reproduces that row's check and its output shape, and is committed so the row
is re-runnable as written. It is not the original bytes (gate2.md, Required
disclosures).

Method is the negative check by COMPLEMENT, not a search for known-bad names:
enumerate every `owner/repo` identity reachable in the scanned bytes, then
subtract the permitted set. A name that is not on any list still appears.

Usage:  python3 t5.py <root> [<root> ...]
Exit 0 when the complement is empty, 1 otherwise.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PERMITTED = {"mianliwang/gatebraid", "mianliwang/gatebraid-scratch"}

# `users`, `orgs`, `rest`, ... are GitHub URL namespaces, not account names:
# `github.com/users/<login>/projects/1` and a `docs.github.com/rest/...`
# documentation link both match an owner/repo shape without naming a repository.
NAMESPACES = {
    "users", "orgs", "rest", "enterprises", "sponsors", "apps",
    "settings", "notifications", "repos", "graphql", "user", "about",
}

IDENTITY = re.compile(
    r"(?:github\.com[/:]|\brepos/)([A-Za-z0-9][\w.-]*)/([A-Za-z0-9][\w.-]*)"
)


def identities(text: str) -> set[str]:
    found = set()
    for owner, repo in IDENTITY.findall(text):
        if owner.lower() in NAMESPACES:
            continue
        repo = repo.lower()
        if repo.endswith(".git"):
            repo = repo[:-4]
        found.add("%s/%s" % (owner.lower(), repo))
    return found


def main(argv: list[str]) -> int:
    roots = argv[1:]
    if not roots:
        print("usage: t5.py <root> [<root> ...]", file=sys.stderr)
        return 2

    files: list[Path] = []
    for root in roots:
        p = Path(root)
        if p.is_file():
            files.append(p)
        else:
            files.extend(sorted(q for q in p.rglob("*") if q.is_file()))

    found: set[str] = set()
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:  # unreadable is a finding, not a silent skip
            print("UNREADABLE %s: %s" % (f.as_posix(), exc))
            return 1
        found |= identities(text)

    outside = sorted(found - PERMITTED)
    print("files scanned: %d" % len(files))
    print("identities found: %s" % sorted(found))
    print("outside permitted set: %s" % ("NONE" if not outside else outside))
    return 1 if outside else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
