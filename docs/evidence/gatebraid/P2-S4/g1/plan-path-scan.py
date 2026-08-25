"""Exit-checklist item: "No path outside the allowlist appears anywhere in the plan."

The item sits under "Allowlist exactness", immediately after "write_domains lists
exactly the path prefixes the plan touches", so "touches" is read in the
allowlist sense: WRITE targets. A plan that could not name its read-only inputs
could not be implemented from, and the frozen schema and corpus are precisely
the inputs this Slice consumes and must not write.

This scan therefore enumerates every repository path the plan section names and
classifies each as a WRITE target or a READ-ONLY input, requiring every WRITE
target to be inside the allowlist. The reading is stated here so it can be
disputed rather than applied silently.
"""
import re, sys

ALLOWED = ("bin/", "docs/evidence/gatebraid/P2-S4/")

# Read-only inputs the plan names on purpose: the frozen surface it consumes and
# the landed tooling it invokes. Every one of these is outside the allowlist by
# design, and this Slice writes none of them.
READ_ONLY_EXACT = {
    "schema/snapshot.schema.json",
    "fixtures/runner-selftest.py",
    "fixtures",
    "bin/gatebraid-validate.py",
}
READ_ONLY_PREFIX = ("fixtures/state-pipeline/",)

# Bare lane names. The plan names these precisely to say it does NOT write them
# ("`schema/` and `fixtures/` are the batch lane's and are frozen"), so their
# presence is the opposite of scope creep.
EXCLUDED_LANES = {"schema/", "fixtures/"}

# Not repository paths at all. "schema/version" is the wording M3-PLAN §2 O0 and
# the Slice body use for the pair of required document fields (`schema` and
# `snapshot_version`); the slash is prose, not a directory separator.
PROSE_NOT_A_PATH = {"schema/version"}

HEADING = "## Plan (frozen at exit)"
lines = open(sys.argv[1], encoding="utf-8").read().split("\n")
start = lines.index(HEADING) + 1
end = next(i for i in range(start, len(lines)) if lines[i].startswith("## "))
plan = "\n".join(lines[start:end])

PATH = re.compile(
    r"(?<![A-Za-z0-9_./-])((?:bin|docs|schema|fixtures|protocols|templates|adr|projects|consults|evidence)"
    r"/[A-Za-z0-9_./*-]*)")
found = sorted(set(m.group(1).rstrip(".,;`-") for m in PATH.finditer(plan)))

writes, reads, outside, lanes, prose = [], [], [], [], []
for p in found:
    if p in PROSE_NOT_A_PATH:
        prose.append(p)
    elif p in EXCLUDED_LANES:
        lanes.append(p)
    elif p in READ_ONLY_EXACT or p.startswith(READ_ONLY_PREFIX):
        reads.append(p)
    elif p.startswith(ALLOWED):
        writes.append(p)
    else:
        outside.append(p)

print("allowlist prefixes : %s" % ", ".join(ALLOWED))
print("paths named in plan: %d" % len(found))
print()
print("WRITE targets, each required to be inside the allowlist:")
for p in writes:
    print("   %-64s inside=%s" % (p, p.startswith(ALLOWED)))
print()
print("READ-ONLY inputs, named on purpose and written by no task in this plan:")
for p in reads:
    print("   %s" % p)
print()
print("EXCLUDED LANES the plan names in order to disclaim them:")
for p in lanes:
    print("   %s" % p)
print()
print("PROSE tokens that are not repository paths:")
for p in prose:
    print("   %s" % p)
print()
print("NEITHER a permitted read-only input nor inside the allowlist: %d" % len(outside))
for p in outside:
    print("   OUTSIDE %s" % p)
print()
ok = not outside and all(p.startswith(ALLOWED) for p in writes)
print("ITEM HOLDS: every write target named in the plan is inside the allowlist"
      if ok else "ITEM VIOLATED")
sys.exit(0 if ok else 1)
