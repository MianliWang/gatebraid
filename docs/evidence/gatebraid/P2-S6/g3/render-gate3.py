"""Render docs/evidence/gatebraid/P2-S6/gate3.md from the captures.

Record-row outputs are GENERATED from the capture records, never transcribed
(friction #96). This file is written and committed BEFORE the merge and reaches
`main` through the pull request; it records the PR by URL and carries NO merge
SHA and NO closure timestamp - GitHub holds both natively (ADR-0017 section 2).

Usage: render-gate3.py <ended_at>
"""
import base64, json, os, sys

G = "docs/evidence/gatebraid/P2-S6/g3/captures"
OUT = "docs/evidence/gatebraid/P2-S6/gate3.md"
STARTED = "2026-08-30T14:05:00Z"
ENDED = sys.argv[1]

L = []


def w(s=""):
    L.append(s)


def cap(cid):
    return json.load(open(os.path.join(G, cid + ".json"), encoding="utf-8"))


def argv_line(d):
    inv = d["invocation"]
    env = inv.get("environment") or {}
    prefix = " ".join("%s=%s" % (k, env[k]) for k in sorted(env))
    body = " ".join(
        (a if (a and not any(c in a for c in " \t\n\"'")) else "'" + a.replace("'", "'\\''") + "'")
        for a in inv.get("argv", []))
    return ("%s %s" % (prefix, body)).strip()


def stream_text(d, name):
    s = d.get("streams", {}).get(name, {})
    if not s.get("data"):
        return ""
    return base64.b64decode(s["data"]).decode("utf-8", "replace")


def row(label, cids, limit=None, head=None):
    w("**%s**" % label)
    w("```")
    for cid in cids:
        d = cap(cid)
        w("$ " + argv_line(d))
        text = stream_text(d, "stdout")
        err = stream_text(d, "stderr")
        combined = text + (("\n" + err) if err.strip() else "")
        lines = combined.splitlines()
        total = len(lines)
        if limit is not None and total > limit:
            keep = lines[:head] if head else []
            tail = lines[-(limit - len(keep)):]
            for l in keep:
                w(l)
            w("[... shown %d of %d lines; full output: %s/%s.json]"
              % (limit, total, G, cid))
            for l in tail:
                w(l)
        else:
            for l in lines:
                w(l)
        if not lines:
            w("(no output)")
        w("(exit %d)" % d["exit_code"])
    w("```")
    w()


DISCLOSURES = [
    "Deviations: `ci: none-configured` is a RECORDED FINDING, not a pass. This repository has no workflow "
    "at all - zero workflow files in the tree, `actions/workflows` total_count 0, and zero check runs on the "
    "published head - so the prohibition on merging with red CI is inert here and this record says so rather "
    "than implying a check occurred. The combined-status endpoint reports `pending` for a commit carrying "
    "zero statuses; that is the absence of any check, not a check in progress, and it is named here so no "
    "reader takes it for one.",

    "Deviations: the drift check's working-tree predicate is evaluated over the baseline EXCLUDING this "
    "gate's own write domain, with the unfiltered view recorded beside it - the same treatment Gate 0's A3 "
    "and Gate 2's baseline used, and for the same reason: this gate's own evidence directory is created BY "
    "the act of recording the gate, and the Gate 3 contract's Exit clause makes writing it not a violation. "
    "The filtered predicate is 43 lines, every one an untracked path under the retained P2-S5 evidence; the "
    "unfiltered view adds only paths under this Slice's own evidence directory and nothing else. Tracked "
    "changes are zero with no exclusion of any kind.",

    "Deviations: the approval's term 6 is the applied working-tree term and is recorded as applied. The tree "
    "lawfully carries the retained P2-S5 evidence - exactly the digest-verified 43-file set, re-derived here "
    "to 83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f by the same construction the setup "
    "report froze - plus the ignored `_handoff/` lane. No OTHER untracked or modified path exists, which is "
    "what that term makes the test.",

    "Deviations: the ref namespace carries one ref outside refs/heads, refs/remotes and refs/tags - a Codex "
    "turn-diff checkpoint pointing at a tree object. It is REPORTED and NOT ADOPTED, and it is NOT "
    "slice-introduced: the same ref is recorded in the retained P2-S5 Gate 0 evidence and in this Slice's own "
    "Gate 0 record, both of which predate this branch. No write of any kind was made into that namespace.",

    "Deviations: closure precondition (b) is checked as a PATTERN, never as a bare token, and the scan prints "
    "its matches beside its count. Twelve bare keyword tokens occur across the seven commit messages - every "
    "one a conventional-commit `fix(scope):` prefix or ordinary prose, which the contract names explicitly as "
    "not prohibited because it references nothing. Zero of them precede an issue reference. The scan was "
    "FALSIFIED before it was trusted: pointed at a seeded body carrying both `Closes #19` and "
    "`fixes owner/repo#17`, it fires on both and exits 1.",

    "Deviations: closure precondition (b) is recorded TWICE - once at the pull request's creation and once "
    "against its FINAL state after `gate3.md` was pushed, because pushing a commit changes what the pull "
    "request carries and a check run only before that push would not have covered the commit this record "
    "itself is. Both runs are recorded.",

    "Deviations: row G6 measures the pull request as it stood after this file's FIRST push, and this file's own second commit necessarily moves the head once more - a record cannot contain the aftermath of the commit that carries it. The boundary is stated rather than chased: what G6 establishes is that closure precondition (b) holds over every commit message the pull request carries INCLUDING this record's, which is the property the contract asks for. The check re-run against the truly final head is carried in _handoff/batch-p2s6/G3-PUBLICATION-REPORT-M3-P2S6.md, and the operator sees it before the merge.",

    "Deviations: this record carries NO merge SHA and NO closure timestamp, and asserts nothing about the "
    "merge. It is written and committed BEFORE the merge by the contract's normative order, so that it "
    "reaches the base branch through the pull request like every other change. The merge is the operator's "
    "own browser action under the approval's term 4; the authoritative Gate 3 record is the composite of this "
    "file, the pull request's merge event, the issue's closure event and the Project's Workflow.",

    "Deviations: the branch was pushed and the pull request opened, which are this gate's authorised "
    "publication actions. Nothing was merged, no branch was deleted, no tag was created, and no force-push "
    "was made or is available. `Next Approval` deliberately still reads the Release Approval option: the "
    "contract returns it to the bare option at Exit, after the merge, and this record is written before that.",

    "Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; shell Git Bash MINGW64 "
    "with Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh "
    "call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every "
    "Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1; Windows interpreter C:/Python312/python.exe "
    "with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0. environment=mixed-see-prose: this gate ran wholly "
    "on the Windows host.",
]

METADATA = """schema: gatebraid/gate-run@2
slice_id: P2-S6
gate: 3
environment: mixed-see-prose
executor: Claude Lead
base_sha: 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
active_branch: slice/P2-S6
started_at: "%(started)s"
ended_at: "%(ended)s"
result: passed
checks:
  - name: release-approval-verified
    command: "gh api repos/MianliWang/gatebraid/issues/comments/5469136543 (author observed, compared against gh api user)"
    result: pass
    output_ref: "#publication-records"
  - name: staged-set-matches-gate2-handoff
    command: "git diff --name-only 3f88cc11fd11292d7225cb1c914dc860b8956646 HEAD"
    result: pass
    output_ref: "#publication-records"
  - name: no-commit-past-fingerprint-touches-code
    command: "git log --format=%%H 5386ce382bac5b4bc1c76a38bcbe86717adf9c1c..HEAD -- ':!docs/evidence/gatebraid/P2-S6/'"
    result: pass
    output_ref: "#publication-records"
  - name: closure-precondition-automation
    command: "gh api graphql ProjectV2.workflows - Auto-close issue must read enabled false"
    result: pass
    output_ref: "#publication-records"
  - name: closure-precondition-pull-request
    command: "gh pr view 20 --json closingIssuesReferences (empty); g3/closing-keyword-scan.py over the body and all 7 commit messages (0 pattern matches, printed)"
    result: pass
    output_ref: "#publication-records"
  - name: closure-precondition-pull-request-final-state
    command: "gh pr view 20 (headRefOid moved, closingIssuesReferences still empty) and the scan re-run over all 8 commit messages, AFTER gate3.md's first push"
    result: pass
    output_ref: "#publication-records"
  - name: closing-keyword-scan-falsified
    command: "g3/closing-keyword-scan.py --body-from a seeded body carrying both reference forms; it must fire on each"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g3/captures/G3-G2b-keyword-scan-falsify.json"
  - name: closed-set-sweep-falsified
    command: "g3/checks-g3-closed-set-sweep.py against the seeded domain; it must fire on the repository, node and issue limbs"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g3/captures/G3-sweep-falsify.json"
  - name: closed-set-sweep-over-record
    command: "g3/checks-g3-closed-set-sweep.py docs/evidence/gatebraid/P2-S6/gate3.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g3/captures/G3-record-sweep.json"
  - name: gate3-record-machine-validated
    command: "bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S6/gate3.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g3/captures/G3-record-validation.json"
  - name: ci-status
    command: "gh api actions/workflows (total_count 0); check-runs on the published head (total_count 0)"
    result: none_configured
    output_ref: "#publication-records"
consults: []
approvals:
  - type: "Release Approval (G2\\u2192G3)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/19#issuecomment-5469136543"
    author: "MianliWang"
plan_hash: "4435c71eaf08bf0605815e5960c8093c4698babf99ae8a7030d05ebe445671d0"
allowlist_hash: "8938efcce4b8b863b14f7a503c808d7c2c67d2975aad180fd153fd45cc6da291"
evidence_files:
  - docs/evidence/gatebraid/P2-S6/gate3.md
notes: "PR https://github.com/MianliWang/gatebraid/pull/20. No merge SHA and no closure timestamp are recorded here - GitHub holds both natively (ADR-0017 section 2), and this file is written BEFORE the merge by the contract's normative order so that it reaches main through the pull request. The Release Approval was targeted BY COMMENT ID, never by matching words, because Gate 2's own exit names the same field and would match a naive search. Approval terms are cited by rule number, never restated. The merge is the operator's browser action under term 4 and is not asserted here."
"""

w("# Gate 3 evidence - P2-S6")
w()
w("## Publication records")
w()
row("G1 - Release Approval verified: the author observed, and the executor identity it is compared against",
    ["G3-G1-approval", "G3-G1-executor-identity"])
row("G2a - closure precondition (a): platform automation; `Auto-close issue` must read enabled false",
    ["G3-G2a-automation"])
row("G2b - closure precondition (b): the pull request, at creation. Pattern and matches printed",
    ["G3-G2b-closing-refs", "G3-G2b-keyword-scan"], limit=26, head=8)
row("G2b - the same scan FALSIFIED against a seeded body carrying both reference forms",
    ["G3-G2b-keyword-scan-falsify"], limit=14, head=4)
row("G3 - drift check against the Gate 2 fingerprint: the diff from the fingerprint TREE, and every commit past the fingerprint HEAD that touches anything outside this Slice's evidence directory",
    ["G3-G3-drift-diff", "G3-G3-drift-commits"], limit=14, head=6)
row("G3 - working tree: tracked changes with no exclusion; the drift predicate excluding this gate's own write domain; the unfiltered view beside it",
    ["G3-G3-porcelain-tracked", "G3-G3-porcelain", "G3-G3-porcelain-unfiltered"], limit=18, head=6)
row("G3 - approval term 6 applied: the retained P2-S5 set re-derived",
    ["G3-G3-p2s5-digest"])
row("G3 - ref namespace; the one ref outside heads, remotes and tags is reported, not adopted, and is not slice-introduced",
    ["G3-G3-refs"], limit=12, head=3)
row("G4 - publication: push, read back, and the pull request as opened",
    ["G3-G4-push", "G3-G4-lsremote", "G3-G4-pr"])
row("G5 - CI status: no workflow exists in this repository, and no check ran on the published head",
    ["G3-G5-ci-workflows", "G3-G5-ci-checkruns"])
row("G6 - the pull request after gate3.md's first push: the head moved, and closure "
    "precondition (b) re-run against that state over all 8 commit messages",
    ["G3-G4-pr-final", "G3-G2b-final-scan"], limit=22, head=10)

w("- Pull request: https://github.com/MianliWang/gatebraid/pull/20 - referenced, not duplicated")
w()

w("## Required disclosures")
w()
for d in DISCLOSURES:
    w("- " + d)
w()
w("## gatebraid-metadata")
w()
w("```yaml")
w((METADATA % {"started": STARTED, "ended": ENDED})
  .replace("\\u2192", chr(0x2192)).rstrip())
w("```")

open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("WROTE %s" % OUT)
