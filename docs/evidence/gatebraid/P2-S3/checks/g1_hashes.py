#!/usr/bin/env python3
"""P2-S3 Gate 1 freeze hashes — the gate-1-contract action 6 algorithms, verbatim.

Python 3 standard library only (ADR-0009). Both hashes are SHA-256, lowercase
hex, over UTF-8 bytes (ADR-0011 §3).

  allowlist  each write_domains entry stripped of surrounding whitespace, sorted
             by BYTE VALUE, joined with "\\n", one trailing "\\n".
  plan       the lines of gate1.md strictly between the "## Plan (frozen at exit)"
             heading and the next line beginning with "## ", each stripped of
             TRAILING whitespace, leading and trailing blank lines removed,
             joined with "\\n", one trailing "\\n".

A hash nobody can recompute is decoration: this file IS the reproducing command
recorded beside each value in the gate record.

Usage:
    g1_hashes.py allowlist <entry> [<entry> ...]
    g1_hashes.py plan <path-to-gate1.md>

Exit 0 on success; 2 on a usage or input error (including a plan section that
cannot be delimited, which must fail loudly rather than hash an empty string).
"""
import hashlib
import sys

HEADING = "## Plan (frozen at exit)"


def allowlist_hash(entries):
    items = sorted((e.strip() for e in entries), key=lambda s: s.encode("utf-8"))
    blob = ("\n".join(items) + "\n").encode("utf-8")
    return items, blob, hashlib.sha256(blob).hexdigest()


def plan_hash(path):
    with open(path, "rb") as fh:
        lines = fh.read().decode("utf-8").split("\n")
    try:
        start = lines.index(HEADING)
    except ValueError:
        print("INPUT: %s carries no %r heading" % (path, HEADING))
        raise SystemExit(2)
    end = None
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    if end is None:
        print("INPUT: no terminating '## ' heading after the plan section")
        raise SystemExit(2)
    section = [l.rstrip() for l in lines[start + 1:end]]
    while section and not section[0]:
        section.pop(0)
    while section and not section[-1]:
        section.pop()
    if not section:
        print("INPUT: the plan section is empty; refusing to hash nothing")
        raise SystemExit(2)
    blob = ("\n".join(section) + "\n").encode("utf-8")
    return section, blob, hashlib.sha256(blob).hexdigest()


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip().splitlines()[-4].strip())
        return 2
    mode = argv[1]
    if mode == "allowlist":
        items, blob, digest = allowlist_hash(argv[2:])
        print("algorithm     : entries stripped, sorted by byte value, joined with LF, one trailing LF")
        for i in items:
            print("entry         : %s" % i)
        print("bytes         : %d" % len(blob))
        print("allowlist_hash: %s" % digest)
        return 0
    if mode == "plan":
        section, blob, digest = plan_hash(argv[2])
        print("algorithm     : lines strictly between %r and the next '## ' line," % HEADING)
        print("                each rstripped, leading/trailing blank lines dropped,")
        print("                joined with LF, one trailing LF")
        print("source        : %s" % argv[2])
        print("plan lines    : %d" % len(section))
        print("bytes         : %d" % len(blob))
        print("plan_hash     : %s" % digest)
        return 0
    print("INPUT: unknown mode %r; expected 'allowlist' or 'plan'" % mode)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
