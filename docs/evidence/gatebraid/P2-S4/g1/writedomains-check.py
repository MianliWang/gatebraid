"""The Gate 1 Exit write_domains step, performed rather than skipped.

The contract states the POST-CONDITION, not the mutation: the Slice issue's
declared write_domains must equal the frozen allowlist. If it already does, the
agreement is recorded as a verification row and no rewrite is made; row 7's
error disposition applies only when a write is REQUIRED and fails. Friction #65
is the case where the write-back was never attempted at all, which is why this
runs and prints its comparison either way.
"""
import json, re, subprocess, sys, yaml

FROZEN = ["bin/", "docs/evidence/gatebraid/P2-S4/"]

r = subprocess.run(
    ["gh", "api", "repos/MianliWang/gatebraid/issues/14", "--jq", ".body"],
    capture_output=True, text=True, encoding="utf-8")
if r.returncode != 0:
    print("STOP: the Slice body could not be read; exit %d" % r.returncode)
    print((r.stderr or "").strip()[:200])
    sys.exit(2)

body = r.stdout
m = re.search(r"^##[ \t]+gatebraid-metadata[ \t]*$", body, re.M)
if not m:
    print("STOP: no '## gatebraid-metadata' heading in the Slice body")
    sys.exit(2)
fence = re.search(r"^```[ \t]*(?:yaml|yml)[ \t]*\n(.*?)^```[ \t]*$",
                  body[m.end():], re.M | re.S)
if not fence:
    print("STOP: no fenced yaml block under the heading")
    sys.exit(2)

declared = yaml.safe_load(fence.group(1)).get("write_domains")

print("frozen allowlist  : %r" % FROZEN)
print("declared on #14   : %r" % declared)
print("equal as sequences: %s" % (declared == FROZEN))
print("equal as sets     : %s" % (set(declared or []) == set(FROZEN)))
print()
if declared == FROZEN:
    print("POST-CONDITION ALREADY HOLDS: the declared write_domains equals the frozen")
    print("allowlist. The agreement is recorded as this verification row and NO rewrite")
    print("of the Slice body is made. The step is performed, not skipped.")
    sys.exit(0)
print("POST-CONDITION DOES NOT HOLD: a write-back is required (contract Exit, row 7).")
sys.exit(1)
