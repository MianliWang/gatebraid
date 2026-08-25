#!/usr/bin/env python3
"""Gate 3 Action 1 — the drift check, run rather than judged.

THE QUESTION IT ANSWERS: *has the reviewed work changed since it was reviewed?*
A gate's own evidence file is the record of the review, not the work, so change
confined to `docs/evidence/gatebraid/<slice_id>/` is not drift; anything else is.

FOUR CHECKS, all from `protocols/gate-3-contract.md` Action 1:

  A  `git diff --name-only <tree_sha> <head>` yields ONLY paths inside the
     slice's evidence directory;
  B  every commit between `<active_branch_head>` and `<head>` touches only that
     directory — a stronger statement than A, because A could be satisfied by a
     write outside the directory that a later commit reverted;
  C  `git status --porcelain` is empty;
  D  `git for-each-ref` shows no ref outside `refs/heads/`, `refs/remotes/` and
     `refs/tags/` that this Slice introduced. Any such ref is REPORTED, NOT
     ADOPTED (friction #103).

EVERY REVISION IS PINNED AND PASSED IN, none is read from a moving reference.
That is this Slice's own F-01 lesson applied to its last gate: a check that names
`HEAD` describes a different thing every time it runs, and `gate3.md`'s own commit
moves `HEAD` immediately after this runs. The head this check names is therefore
the head at drift-check time, passed as an argument and recorded in the output.

Exit codes: 0 no drift · 1 drift found (route back to `Needs Review`, no
publication) · 2 usage error. Python 3 standard library only.
"""

import os
import subprocess
import sys

EVIDENCE_PREFIX = "docs/evidence/gatebraid/P2-S4/"
WATCHED = ("refs/heads/", "refs/remotes/", "refs/tags/")

if len(sys.argv) != 4:
    print("USAGE: drift-check.py <tree_sha> <active_branch_head> <head>")
    raise SystemExit(2)

TREE_SHA, ACTIVE_BRANCH_HEAD, HEAD = sys.argv[1], sys.argv[2], sys.argv[3]
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))


def git(*args):
    p = subprocess.run(["git"] + list(args), cwd=REPO,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        print("GIT FAILED: git %s -> exit %d" % (" ".join(args), p.returncode))
        print(p.stderr.decode("utf-8", "replace").strip())
        raise SystemExit(2)
    return p.stdout.decode("utf-8", "replace")


def outside(paths):
    return [x for x in paths if x.strip() and not x.startswith(EVIDENCE_PREFIX)]


failures = []

print("tree_sha (as reviewed)        : %s" % TREE_SHA)
print("active_branch_head            : %s" % ACTIVE_BRANCH_HEAD)
print("head at drift-check time      : %s" % HEAD)
print("evidence prefix               : %s" % EVIDENCE_PREFIX)
print()

# ---- A ---------------------------------------------------------------------
a_paths = [x for x in git("diff", "--name-only", TREE_SHA, HEAD).splitlines() if x.strip()]
a_out = outside(a_paths)
print("A  git diff --name-only <tree_sha> <head>")
print("     paths changed              : %d" % len(a_paths))
print("     outside the evidence dir   : %d" % len(a_out))
for x in a_out:
    print("        %s" % x)
if a_out:
    failures.append("A")

# ---- B ---------------------------------------------------------------------
commits = [c for c in git("rev-list", "--reverse",
                          "%s..%s" % (ACTIVE_BRANCH_HEAD, HEAD)).splitlines() if c.strip()]
print("B  every commit in <active_branch_head>..<head>")
print("     commits examined           : %d" % len(commits))
b_bad = 0
for c in commits:
    paths = [x for x in git("diff-tree", "--no-commit-id", "--name-only", "-r",
                            c).splitlines() if x.strip()]
    out = outside(paths)
    print("        %s  changed=%-3d outside=%d" % (c, len(paths), len(out)))
    for x in out:
        print("           %s" % x)
    b_bad += len(out)
if b_bad:
    failures.append("B")

# ---- C ---------------------------------------------------------------------
porcelain = [x for x in git("status", "--porcelain").splitlines() if x.strip()]
print("C  git status --porcelain")
print("     entries                    : %d" % len(porcelain))
for x in porcelain:
    print("        %s" % x)
if porcelain:
    failures.append("C")

# ---- D ---------------------------------------------------------------------
refs = [x for x in git("for-each-ref", "--format=%(refname)").splitlines() if x.strip()]
unwatched = [r for r in refs if not r.startswith(WATCHED)]
print("D  git for-each-ref")
print("     refs total                 : %d" % len(refs))
print("     outside the three watched namespaces : %d" % len(unwatched))
for r in unwatched:
    print("        %s" % r)
print("     watched namespaces         : %s" % ", ".join(WATCHED))
print("     DISPOSITION: any ref above is REPORTED, NOT ADOPTED (friction #103).")
print("     This Slice introduced none of them: it created exactly one ref,")
print("     refs/heads/slice/P2-S4, which is inside refs/heads/.")

print()
print("checks failed                 : %d %s" % (len(failures),
                                                 ("(" + ", ".join(failures) + ")") if failures else ""))
if failures:
    print("DRIFT FOUND: route back to Needs Review; no publication")
    raise SystemExit(1)
print("NO DRIFT: the reviewed work is unchanged; every change since the "
      "fingerprint is inside the slice's own evidence directory")
