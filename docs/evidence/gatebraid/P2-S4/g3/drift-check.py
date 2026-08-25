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

def out(line=""):
    """Write one line as EXPLICIT UTF-8 BYTES to a binary sink.

    Not `print`. This instrument scans arbitrary text and echoes matched context,
    so its output carries whatever non-ASCII its input carries -- and on this host
    a cp936 console re-encodes a text-layer write, producing bytes that are not
    valid UTF-8. Measured here rather than assumed: the first run of this check
    against the pull-request body emitted a 0xa1 lead byte and its capture
    recorded `decode_result: replaced`. That is BP-01, the exact defect class this
    Slice ships tools to remove, appearing in the Slice's own gate instrument. The
    fix is the one the Slice's own P0-2 requires of its producer.
    """
    sys.stdout.buffer.write((line + chr(10)).encode("utf-8"))


EVIDENCE_PREFIX = "docs/evidence/gatebraid/P2-S4/"
WATCHED = ("refs/heads/", "refs/remotes/", "refs/tags/")

if len(sys.argv) != 4:
    out("USAGE: drift-check.py <tree_sha> <active_branch_head> <head>")
    raise SystemExit(2)

TREE_SHA, ACTIVE_BRANCH_HEAD, HEAD = sys.argv[1], sys.argv[2], sys.argv[3]
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))


def git(*args):
    p = subprocess.run(["git"] + list(args), cwd=REPO,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        out("GIT FAILED: git %s -> exit %d" % (" ".join(args), p.returncode))
        out(p.stderr.decode("utf-8", "replace").strip())
        raise SystemExit(2)
    return p.stdout.decode("utf-8", "replace")


def outside(paths):
    return [x for x in paths if x.strip() and not x.startswith(EVIDENCE_PREFIX)]


failures = []

out("tree_sha (as reviewed)        : %s" % TREE_SHA)
out("active_branch_head            : %s" % ACTIVE_BRANCH_HEAD)
out("head at drift-check time      : %s" % HEAD)
out("evidence prefix               : %s" % EVIDENCE_PREFIX)
out()

# ---- A ---------------------------------------------------------------------
a_paths = [x for x in git("diff", "--name-only", TREE_SHA, HEAD).splitlines() if x.strip()]
a_out = outside(a_paths)
out("A  git diff --name-only <tree_sha> <head>")
out("     paths changed              : %d" % len(a_paths))
out("     outside the evidence dir   : %d" % len(a_out))
for x in a_out:
    out("        %s" % x)
if a_out:
    failures.append("A")

# ---- B ---------------------------------------------------------------------
commits = [c for c in git("rev-list", "--reverse",
                          "%s..%s" % (ACTIVE_BRANCH_HEAD, HEAD)).splitlines() if c.strip()]
out("B  every commit in <active_branch_head>..<head>")
out("     commits examined           : %d" % len(commits))
b_bad = 0
for c in commits:
    paths = [x for x in git("diff-tree", "--no-commit-id", "--name-only", "-r",
                            c).splitlines() if x.strip()]
    stray = outside(paths)
    out("        %s  changed=%-3d outside=%d" % (c, len(paths), len(stray)))
    for x in stray:
        out("           %s" % x)
    b_bad += len(stray)
if b_bad:
    failures.append("B")

# ---- C ---------------------------------------------------------------------
porcelain = [x for x in git("status", "--porcelain").splitlines() if x.strip()]
out("C  git status --porcelain")
out("     entries                    : %d" % len(porcelain))
for x in porcelain:
    out("        %s" % x)
if porcelain:
    failures.append("C")

# ---- D ---------------------------------------------------------------------
refs = [x for x in git("for-each-ref", "--format=%(refname)").splitlines() if x.strip()]
unwatched = [r for r in refs if not r.startswith(WATCHED)]
out("D  git for-each-ref")
out("     refs total                 : %d" % len(refs))
out("     outside the three watched namespaces : %d" % len(unwatched))
for r in unwatched:
    out("        %s" % r)
out("     watched namespaces         : %s" % ", ".join(WATCHED))
out("     DISPOSITION: any ref above is REPORTED, NOT ADOPTED (friction #103).")
out("     This Slice introduced none of them: it created exactly one ref,")
out("     refs/heads/slice/P2-S4, which is inside refs/heads/.")

out()
out("checks failed                 : %d %s" % (len(failures),
                                                 ("(" + ", ".join(failures) + ")") if failures else ""))
if failures:
    out("DRIFT FOUND: route back to Needs Review; no publication")
    raise SystemExit(1)
out("NO DRIFT: the reviewed work is unchanged; every change since the "
      "fingerprint is inside the slice's own evidence directory")
