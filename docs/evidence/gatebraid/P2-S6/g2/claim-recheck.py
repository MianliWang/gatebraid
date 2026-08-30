"""Repair 2: re-measure EVERY prose claim this repair touches or creates.

The class that failed twice at this gate is "a statement the file makes about
itself going false". Fixing three instances does not address the class; this
does: every claim the repair touches is enumerated and re-measured against the
record and the repository, and a claim that cannot be measured is reported
rather than assumed. The inventory is CONSULT-19-01's answer to question 4 plus
the claims this repair itself creates.

Exit 0 = every claim measured true. Exit 1 = at least one is false.
Python 3 standard library only.
"""
import json, re, subprocess, sys

# Overridable ONLY so the SAME checker - not a copy - can be pointed at a seeded
# record and shown able to fire. A checker that has only ever returned TRUE has
# never been falsified.
REC = sys.argv[1] if len(sys.argv) > 1 else "docs/evidence/gatebraid/P2-S6/gate2.md"
FP_COMMIT = "5386ce382bac5b4bc1c76a38bcbe86717adf9c1c"
EV_COMMIT = "44906edc4d49cc090673a2220d3b66246b187bca"
R1_COMMIT = "8d4fa4188c8fecc552448e1fff152e133abb3229"

text = open(REC, encoding="utf-8").read()
meta = json.loads(json.dumps(None))  # placeholder; parsed below without yaml


def git(*args):
    p = subprocess.run(["git"] + list(args), stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    return p.returncode, p.stdout.decode("utf-8", "replace").strip()


def meta_block():
    m = re.search(r"## gatebraid-metadata\n\n```yaml\n(.*?)\n```", text, re.S)
    return m.group(1) if m else ""


MB = meta_block()
rows = []


def claim(cid, statement, ok, measured):
    rows.append((cid, statement, ok, measured))


# 1 — E4b's label claims the evidence SHA exists and is a commit.
rc, out = git("rev-parse", EV_COMMIT + "^{commit}")
claim("C1", "E4b: the evidence SHA resolves and peels to a commit",
      rc == 0 and out == EV_COMMIT, "exit=%d out=%s" % (rc, out[:12]))

# 2 — E4b's row in the record carries the peel form, not the bare form.
claim("C2", "E4b's recorded command is the peel form, not the echoing form",
      ("$ git rev-parse %s^{commit}" % EV_COMMIT) in text
      and ("$ git rev-parse %s\n" % EV_COMMIT) not in text,
      "peel present, bare absent")

# 3 — the exclusion count says TWO and names exactly V7b and E4's second command.
excl = "OUTSIDE the subset, by the exclusion limb, TWO rows" in text
claim("C3", "the exclusion limb still names exactly two rows (V7b, E4's HEAD row)",
      excl and "First, V7b" in text and "Second, E4's second command" in text,
      "TWO=%s" % excl)

# 4 — V9's pinned argument IS the metadata's active_branch_head.
abh = re.search(r'active_branch_head: "([0-9a-f]{40})"', MB)
abh = abh.group(1) if abh else ""
claim("C4", "V9's pinned argument is the metadata active_branch_head",
      abh == FP_COMMIT and ("$ git rev-parse %s^{tree}" % FP_COMMIT) in text,
      "metadata=%s" % abh[:12])

# 5 — V9's first output is the metadata tree_sha.
ts = re.search(r'tree_sha: "([0-9a-f]{40})"', MB)
ts = ts.group(1) if ts else ""
rc, out = git("rev-parse", FP_COMMIT + "^{tree}")
claim("C5", "V9 derives the fingerprint tree and it equals metadata tree_sha",
      rc == 0 and out == ts and ts != "", "derived=%s meta=%s" % (out[:12], ts[:12]))

# 6 — V9's second output is the metadata changed_paths, in order.
rc, out = git("diff", "--name-only", "%s..%s" % (
    "3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8", FP_COMMIT))
derived = out.split("\n") if out else []
declared = re.findall(r"^    - (\S+)$", MB, re.M)
claim("C6", "V9 derives the fingerprint changed-path set and it equals metadata",
      derived == declared and derived != [], "%s vs %s" % (derived, declared))

# 7 — the repair-1 novelty row's tree is the failed state's tree.
rc, out = git("rev-parse", EV_COMMIT + "^{tree}")
claim("C7", "repair 1 novelty: the pinned tree resolves to the recorded value",
      rc == 0 and out in text, "tree=%s in record=%s" % (out[:12], out in text))

# 8 — the repair-1 novelty row's second command is a peel and resolves.
rc, out = git("rev-parse", EV_COMMIT + "^{commit}")
claim("C8", "repair 1 novelty: the second command peels and resolves the object",
      rc == 0 and out == EV_COMMIT, "exit=%d" % rc)

# 9 — Repair-record blocks and metadata repair_attempts agree.
n_blocks = len(re.findall(r"^### Repair \d+$", text, re.M))
n_meta = len(re.findall(r"^  - number: \d+$", MB, re.M))
has_ref = "consult_ref: CONSULT-19-01" in MB
in_block = "Consult: `CONSULT-19-01` (in sequence; ACCEPT)" in text
claim("C9", "Repair blocks and metadata repair_attempts agree, consult_ref present",
      n_blocks == n_meta == 2 and has_ref and in_block,
      "blocks=%d meta=%d ref=%s" % (n_blocks, n_meta, has_ref))

# 10 — no residual live assertion that no repair or consult occurred.
stale = [s for s in ["no repair sequence ran", "`repair_attempts` is empty",
                     "`repair_limit` is unspent",
                     "No Codex consult was needed or made"] if s in text]
claim("C10", "no residual assertion that no repair or consult occurred",
      not stale, "matches=%s" % stale)

# 11 — nowhere is the evidence SHA called the fingerprint / implementation commit.
bad = []
for m in re.finditer(re.escape(EV_COMMIT), text):
    ctx = text[max(0, m.start() - 260):m.end() + 260]
    if re.search(r"fingerprint|implementation-complete|active_branch_head", ctx):
        if "NOT the fingerprint commit" not in ctx:
            bad.append(text[:m.start()].count("\n") + 1)
claim("C11", "the evidence SHA is nowhere called the fingerprint commit",
      not bad, "lines=%s" % bad)

# 12 — the repair record's own hypothesis is carried identically in both places.
h_meta = re.search(r'hypothesis: "the failing class is a statement the file makes '
                   r'about itself going false[^"]*"', MB)
claim("C12", "repair 2's hypothesis appears in the metadata as well as the block",
      h_meta is not None and "the failing class is a statement the file makes about "
      "itself going false" in text, "meta=%s" % (h_meta is not None))

# 13 — the consult pair exists and is declared in evidence_files.
import os
claim("C13", "the consult request and its verbatim response exist and are declared",
      os.path.isfile("docs/evidence/gatebraid/P2-S6/CONSULT-19-01.md")
      and os.path.isfile("docs/evidence/gatebraid/P2-S6/CONSULT-19-01-response.json")
      and "CONSULT-19-01.md" in MB and "CONSULT-19-01-response.json" in MB,
      "declared in evidence_files")

# 14 — E4's excluded row still records the value it recorded, unchanged.
claim("C14", "E4's excluded HEAD row still carries its original recorded value",
      ("$ git rev-parse HEAD\n%s" % FP_COMMIT) in text,
      "unchanged")

width = max(len(r[1]) for r in rows)
print("%-5s %-*s %-8s %s" % ("id", width, "claim", "verdict", "measured"))
failed = 0
for cid, st, ok, meas in rows:
    if not ok:
        failed += 1
    print("%-5s %-*s %-8s %s" % (cid, width, st, "TRUE" if ok else "FALSE", meas))
print()
print("claims re-measured           : %d" % len(rows))
print("claims measured FALSE        : %d" % failed)
print("CLAIM RECHECK CLEAN" if failed == 0 else "CLAIM RECHECK NOT CLEAN")
sys.exit(0 if failed == 0 else 1)
