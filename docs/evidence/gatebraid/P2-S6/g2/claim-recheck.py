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

# ---- claims the EXIT-completion edit adds --------------------------------
REPORTS = {
    "REVIEW-P2S6-G2.md":
        ("76ef86a1293755f99351236e0e86301082067ade6ce7ef47db1108bf479225de", 46091),
    "REVIEW-P2S6-G2-REREVIEW.md":
        ("47bd2eb9956197e81cb1f4ad13efb3561e6449e9361dbf6b6bb2ff183ae6fda4", 19909),
    "REVIEW-P2S6-G2-FINAL.md":
        ("2cf44ec8656d568573d3aa342185ac5ac4725b62e4af229a1538b7686d94bb68", 20795),
}

# 15 - every cited report pin matches the file it names, and the record cites it.
import hashlib as _h
_bad = []
for _name, (_want, _size) in REPORTS.items():
    _fp = os.path.join("_handoff", "batch-p2s6", _name)
    if not os.path.isfile(_fp):
        _bad.append(_name + ":absent")
        continue
    _raw = open(_fp, "rb").read()
    if _h.sha256(_raw).hexdigest() != _want or len(_raw) != _size:
        _bad.append(_name + ":file-mismatch")
    if _want not in text:
        _bad.append(_name + ":pin-not-cited")
claim("C15", "every cited review-report pin matches the file it names",
      not _bad, "problems=%s" % _bad)

# 16 - those reports are on the ignored lane and are NOT in the tree.
_rc, _out = git("check-ignore", "-v", "_handoff/batch-p2s6/REVIEW-P2S6-G2-FINAL.md")
_rc2, _listing = git("status", "--porcelain", "--untracked-files=all")
claim("C16", "the cited reports are ignored and absent from the porcelain listing",
      _rc == 0 and "REVIEW-P2S6" not in _listing,
      "check-ignore=%d in-listing=%s" % (_rc, "REVIEW-P2S6" in _listing))

# 17 - review-five-items is pass, and Review 3 reads pass on all five.
_r3 = text.split("### Review 3")[-1] if "### Review 3" in text else ""
_five = len(re.findall(r"^\| R[1-5][^|]*\| \*\*pass\*\* \|", _r3, re.M))
_rfi = re.search(r"name: review-five-items.*?result: (\w+)", MB, re.S)
claim("C17", "review-five-items is pass and Review 3 reads pass on all five items",
      _rfi is not None and _rfi.group(1) == "pass" and _five == 5,
      "check=%s review3_pass_rows=%d" % (_rfi.group(1) if _rfi else None, _five))

# 18 - every review block names its head as a pinned SHA, never HEAD.
_blocks = re.findall(r"^### Review \d[^\n]*\n(.*?)(?=^### |^## )", text, re.S | re.M)
_heads = ["44906edc4d49cc090673a2220d3b66246b187bca",
          "8d4fa4188c8fecc552448e1fff152e133abb3229",
          "73e489f1976f4b360858b27e4ef1fdaf5501b8f7"]
_ok18 = (len(_blocks) == 3
         and all(_h2 in _b for _h2, _b in zip(_heads, _blocks))
         and not any(re.search(r"at head `?HEAD", _b) for _b in _blocks))
claim("C18", "each review block names its head as a pinned SHA, never HEAD",
      _ok18, "blocks=%d" % len(_blocks))

# 19 - the head Review 3 examined is a real commit and an ancestor of the tip.
_rc, _out = git("rev-parse", "73e489f1976f4b360858b27e4ef1fdaf5501b8f7^{commit}")
_rc2, _ = git("merge-base", "--is-ancestor",
              "73e489f1976f4b360858b27e4ef1fdaf5501b8f7", "HEAD")
claim("C19", "the head Review 3 examined is a real commit and an ancestor of the tip",
      _rc == 0 and _out == "73e489f1976f4b360858b27e4ef1fdaf5501b8f7" and _rc2 == 0,
      "peel=%d ancestor=%d" % (_rc, _rc2))

# 20 - result records a gate still awaiting its human door.
claim("C20", "result records needs_approval, the human Release Approval still owed",
      re.search(r"^result: needs_approval$", MB, re.M) is not None, "as written")

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
