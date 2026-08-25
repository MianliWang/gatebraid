"""Negative criterion N1 -- the diff touches no path outside the frozen allowlist.

Scope is an EXPLICIT path set, never "the added file" (friction #110):

    bin/**
    docs/evidence/gatebraid/P2-S4/**

Direction of error (ADR-0018 section 2): this proxy errs toward FALSE ALARM. It
reports any changed path not matching the two prefixes, including a path that a
future rename might place legitimately elsewhere; it cannot err toward silence,
because containment is decided by the prefix set itself rather than by a
heuristic. A false alarm stops the gate for a human to look at; a false silence
would let scope creep land, which is the failure this criterion exists to
prevent.

Usage: negative-criterion-N1.py <base-sha> [<head-ref>]
Exit 0 = every changed path is inside the allowlist. Exit 1 = at least one is not.
"""
import subprocess, sys

ALLOWED_PREFIXES = ("bin/", "docs/evidence/gatebraid/P2-S4/")

base = sys.argv[1]
head = sys.argv[2] if len(sys.argv) > 2 else "HEAD"

r = subprocess.run(["git", "diff", "--name-only", "%s..%s" % (base, head)],
                   capture_output=True, text=True, encoding="utf-8")
if r.returncode != 0:
    print("STRUCTURE: git diff failed:", (r.stderr or "").strip()[:200])
    sys.exit(2)

paths = [p for p in r.stdout.splitlines() if p.strip()]
inside = [p for p in paths if p.startswith(ALLOWED_PREFIXES)]
outside = [p for p in paths if not p.startswith(ALLOWED_PREFIXES)]

print("range          : %s..%s" % (base, head))
print("allowed prefixes:")
for a in ALLOWED_PREFIXES:
    print("   %s" % a)
print("changed paths  : %d" % len(paths))
print("inside allowlist: %d" % len(inside))
print("outside         : %d" % len(outside))
for p in outside:
    print("   OUTSIDE %s" % p)
print()
if outside:
    print("N1 VIOLATED: the diff touches a path outside the frozen allowlist")
else:
    print("N1 HOLDS: every changed path is inside the frozen allowlist")
sys.exit(1 if outside else 0)
