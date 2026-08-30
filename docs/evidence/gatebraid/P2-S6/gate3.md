# Gate 3 evidence - P2-S6

## Publication records

**G1 - Release Approval verified: the author observed, and the executor identity it is compared against**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5469136543 --jq '{author: .user.login, url: .html_url}'
{"author":"MianliWang","url":"https://github.com/MianliWang/gatebraid/issues/19#issuecomment-5469136543"}
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login
mianliwang492-source
(exit 0)
```

**G2a - closure precondition (a): platform automation; `Auto-close issue` must read enabled false**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query{node(id:"PVT_kwHOBRofUs4Beum7"){... on ProjectV2{workflows(first:20){nodes{number name enabled}}}}}' --jq '.data.node.workflows.nodes[] | "\(.enabled)\t\(.number)\t\(.name)"'
true	4	Auto-add sub-issues to project
false	3	Auto-close issue
true	6	Item added to project
true	1	Item closed
true	5	Pull request linked to issue
true	2	Pull request merged
(exit 0)
```

**G2b - closure precondition (b): the pull request, at creation. Pattern and matches printed**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr view 20 --repo MianliWang/gatebraid --json closingIssuesReferences
{"closingIssuesReferences":[]}
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/g3/closing-keyword-scan.py --pr 20 --base 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
keyword pattern    : (?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(?:#\d+|[A-Za-z0-9._-]+/[A-Za-z0-9._-]+#\d+|https?://github\.com/\S+/issues/\d+)
scope              : the pull-request body and every commit message in 3d47f8be0b9c..HEAD

PR body (pr#20)
   pattern matches : 0  
   bare tokens     : 1  (a conventional-commit prefix references nothing and is not prohibited)

commit messages the pull request carries: 7
   254981f1a6fb  pattern=0  bare=3   fix(snapshot): the live transport reads per-sour
   5386ce382bac  pattern=0  bare=2   test(snapshot): the selftest exercises the live 
   44906edc4d49  pattern=0  bare=0   docs(p2-s6): the Slice's Gate 0, Gate 1 and Gate
   d1e9dd950d37  pattern=0  bare=2   docs(p2-s6): repair 1 of the R3 fail - decision 
   8d4fa4188c8f  pattern=0  bare=1   docs(p2-s6): repair 1, correction - V7b is exclu
   73e489f1976f  pattern=0  bare=2   docs(p2-s6): repair 2 - remove the self-referent
   bd40ed39e243  pattern=0  bare=2   docs(p2-s6): the Gate 2 review record - R1 throu

total pattern matches: 0
CLOSING-KEYWORD SCAN: CLEAN - no closing keyword precedes any issue reference
(exit 0)
```

**G2b - the same scan FALSIFIED against a seeded body carrying both reference forms**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/g3/closing-keyword-scan.py --pr 20 --base 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8 --body-from C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/b8137b4a-c1e1-40cc-a414-c35fc6d904d6/scratchpad/seeded-body.md
keyword pattern    : (?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(?:#\d+|[A-Za-z0-9._-]+/[A-Za-z0-9._-]+#\d+|https?://github\.com/\S+/issues/\d+)
scope              : the pull-request body and every commit message in 3d47f8be0b9c..HEAD

PR body (file:C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/b8137b4a-c1e1-40cc-a414-c35fc6d904d6/scratchpad/seeded-body.md)
[... shown 14 of 20 lines; full output: docs/evidence/gatebraid/P2-S6/g3/captures/G3-G2b-keyword-scan-falsify.json]
   44906edc4d49  pattern=0  bare=0   docs(p2-s6): the Slice's Gate 0, Gate 1 and Gate
   d1e9dd950d37  pattern=0  bare=2   docs(p2-s6): repair 1 of the R3 fail - decision 
   8d4fa4188c8f  pattern=0  bare=1   docs(p2-s6): repair 1, correction - V7b is exclu
   73e489f1976f  pattern=0  bare=2   docs(p2-s6): repair 2 - remove the self-referent
   bd40ed39e243  pattern=0  bare=2   docs(p2-s6): the Gate 2 review record - R1 throu

total pattern matches: 2
   body  'Closes #19'
   body  'fixes MianliWang/gatebraid#17'
CLOSING-KEYWORD SCAN: FOUND - closure precondition (b) FAILS
(exit 1)
```

**G3 - drift check against the Gate 2 fingerprint: the diff from the fingerprint TREE, and every commit past the fingerprint HEAD that touches anything outside this Slice's evidence directory**
```
$ git diff --name-only 3f88cc11fd11292d7225cb1c914dc860b8956646 HEAD
docs/evidence/gatebraid/P2-S6/CONSULT-19-01-response.json
docs/evidence/gatebraid/P2-S6/CONSULT-19-01.md
docs/evidence/gatebraid/P2-S6/captures/G0-baseline-main.json
docs/evidence/gatebraid/P2-S6/captures/G0-captures-validation.json
docs/evidence/gatebraid/P2-S6/captures/G0-closed-set-sweep-falsify.json
docs/evidence/gatebraid/P2-S6/captures/G0-closed-set-sweep.json
[... shown 14 of 101 lines; full output: docs/evidence/gatebraid/P2-S6/g3/captures/G3-G3-drift-diff.json]
docs/evidence/gatebraid/P2-S6/g2/captures/g2-snapshot.json
docs/evidence/gatebraid/P2-S6/g2/checks-g2-closed-set-sweep.py
docs/evidence/gatebraid/P2-S6/g2/claim-recheck.py
docs/evidence/gatebraid/P2-S6/g2/render-gate2.py
docs/evidence/gatebraid/P2-S6/gate0.md
docs/evidence/gatebraid/P2-S6/gate1.md
docs/evidence/gatebraid/P2-S6/gate2.md
docs/evidence/gatebraid/P2-S6/render-gate0.py
(exit 0)
$ git log --format=%H 5386ce382bac5b4bc1c76a38bcbe86717adf9c1c..HEAD -- :!docs/evidence/gatebraid/P2-S6/
(no output)
(exit 0)
```

**G3 - working tree: tracked changes with no exclusion; the drift predicate excluding this gate's own write domain; the unfiltered view beside it**
```
$ git status --porcelain --untracked-files=no
(no output)
(exit 0)
$ git status --porcelain --untracked-files=all -- . :(exclude)docs/evidence/gatebraid/P2-S6/
?? docs/evidence/gatebraid/P2-S5/captures/G0-baseline-main.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation-pass1.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation-pass2.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-falsify-pass1.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-falsify.json
[... shown 18 of 43 lines; full output: docs/evidence/gatebraid/P2-S6/g3/captures/G3-G3-porcelain.json]
?? docs/evidence/gatebraid/P2-S5/captures/G0-tools-git.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-tools-python-windows.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-tools-python-wsl.json
?? docs/evidence/gatebraid/P2-S5/captures/g0-frontier-report.json
?? docs/evidence/gatebraid/P2-S5/captures/g0-snapshot.json
?? docs/evidence/gatebraid/P2-S5/captures/slice-body-17.md
?? docs/evidence/gatebraid/P2-S5/checks-g0-closed-set-sweep.py
?? docs/evidence/gatebraid/P2-S5/checks-g0-slice-metadata.py
?? docs/evidence/gatebraid/P2-S5/checks-g0-verify-captures.py
?? docs/evidence/gatebraid/P2-S5/falsification/SEED-out-of-set.json
?? docs/evidence/gatebraid/P2-S5/gate0.md
?? docs/evidence/gatebraid/P2-S5/render-gate0.py
(exit 0)
$ git status --porcelain --untracked-files=all
?? docs/evidence/gatebraid/P2-S5/captures/G0-baseline-main.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation-pass1.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation-pass2.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-falsify-pass1.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-falsify.json
[... shown 18 of 59 lines; full output: docs/evidence/gatebraid/P2-S6/g3/captures/G3-G3-porcelain-unfiltered.json]
?? docs/evidence/gatebraid/P2-S6/g3/captures/G3-G2b-keyword-scan-falsify.json
?? docs/evidence/gatebraid/P2-S6/g3/captures/G3-G2b-keyword-scan.json
?? docs/evidence/gatebraid/P2-S6/g3/captures/G3-G3-drift-commits.json
?? docs/evidence/gatebraid/P2-S6/g3/captures/G3-G3-drift-diff.json
?? docs/evidence/gatebraid/P2-S6/g3/captures/G3-G3-porcelain.json
?? docs/evidence/gatebraid/P2-S6/g3/captures/G3-G3-refs.json
?? docs/evidence/gatebraid/P2-S6/g3/captures/G3-G4-lsremote.json
?? docs/evidence/gatebraid/P2-S6/g3/captures/G3-G4-pr.json
?? docs/evidence/gatebraid/P2-S6/g3/captures/G3-G4-push.json
?? docs/evidence/gatebraid/P2-S6/g3/captures/G3-G5-ci-checkruns.json
?? docs/evidence/gatebraid/P2-S6/g3/captures/G3-G5-ci-workflows.json
?? docs/evidence/gatebraid/P2-S6/g3/closing-keyword-scan.py
(exit 0)
```

**G3 - approval term 6 applied: the retained P2-S5 set re-derived**
```
$ 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'find docs/evidence/gatebraid/P2-S5 -type f | sort | tr -d '\''\r'\'' | sha256sum'
83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f *-
(exit 0)
```

**G3 - ref namespace; the one ref outside heads, remotes and tags is reported, not adopted, and is not slice-introduced**
```
$ git for-each-ref '--format=%(refname) %(objecttype)'
refs/codex/turn-diffs/checkpoints/6568734db6429e0860cf0954b19afffaadb93c9960d666efb23d1018f152be37/7f8d802c118042d20382a16a250ea1c5fb0bd87efd6e2a2ee3221558ade9c8f3/1785489900931/c0da4005-1ff6-434a-b1a5-9ad1a2af1b0e tree
refs/heads/batch/o0-b1 commit
refs/heads/batch/o1-b1 commit
[... shown 12 of 22 lines; full output: docs/evidence/gatebraid/P2-S6/g3/captures/G3-G3-refs.json]
refs/remotes/origin/batch/o1-b1 commit
refs/remotes/origin/m1-control-plane commit
refs/remotes/origin/m3/n0-ratification commit
refs/remotes/origin/main commit
refs/remotes/origin/slice/P2-S1 commit
refs/remotes/origin/slice/P2-S2 commit
refs/remotes/origin/slice/P2-S3 commit
refs/remotes/origin/slice/P2-S4 commit
refs/remotes/origin/slice/P2-S6 commit
(exit 0)
```

**G4 - publication: push, read back, and the pull request as opened**
```
$ git push -u origin slice/P2-S6
branch 'slice/P2-S6' set up to track 'origin/slice/P2-S6'.

Everything up-to-date
(exit 0)
$ git ls-remote --heads origin slice/P2-S6
bd40ed39e243acd8d3cc22816b12edbb79ac1a25	refs/heads/slice/P2-S6
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr view 20 --repo MianliWang/gatebraid --json number,url,state,baseRefName,headRefName,headRefOid
{"baseRefName":"main","headRefName":"slice/P2-S6","headRefOid":"bd40ed39e243acd8d3cc22816b12edbb79ac1a25","number":20,"state":"OPEN","url":"https://github.com/MianliWang/gatebraid/pull/20"}
(exit 0)
```

**G5 - CI status: no workflow exists in this repository, and no check ran on the published head**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/actions/workflows --jq '{total_count: .total_count, workflows: [.workflows[].name]}'
{"total_count":0,"workflows":[]}
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/commits/bd40ed39e243acd8d3cc22816b12edbb79ac1a25/check-runs --jq '{total_count: .total_count}'
{"total_count":0}
(exit 0)
```

**G6 - the pull request after gate3.md's first push: the head moved, and closure precondition (b) re-run against that state over all 8 commit messages**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr view 20 --repo MianliWang/gatebraid --json number,url,state,headRefOid,closingIssuesReferences
{"closingIssuesReferences":[],"headRefOid":"43a7c96a9975e9861ce02e9ec9a600fe56082544","number":20,"state":"OPEN","url":"https://github.com/MianliWang/gatebraid/pull/20"}
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/g3/closing-keyword-scan.py --pr 20 --base 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
keyword pattern    : (?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(?:#\d+|[A-Za-z0-9._-]+/[A-Za-z0-9._-]+#\d+|https?://github\.com/\S+/issues/\d+)
scope              : the pull-request body and every commit message in 3d47f8be0b9c..HEAD

PR body (pr#20)
   pattern matches : 0  
   bare tokens     : 1  (a conventional-commit prefix references nothing and is not prohibited)

commit messages the pull request carries: 8
   254981f1a6fb  pattern=0  bare=3   fix(snapshot): the live transport reads per-sour
   5386ce382bac  pattern=0  bare=2   test(snapshot): the selftest exercises the live 
   44906edc4d49  pattern=0  bare=0   docs(p2-s6): the Slice's Gate 0, Gate 1 and Gate
   d1e9dd950d37  pattern=0  bare=2   docs(p2-s6): repair 1 of the R3 fail - decision 
   8d4fa4188c8f  pattern=0  bare=1   docs(p2-s6): repair 1, correction - V7b is exclu
   73e489f1976f  pattern=0  bare=2   docs(p2-s6): repair 2 - remove the self-referent
   bd40ed39e243  pattern=0  bare=2   docs(p2-s6): the Gate 2 review record - R1 throu
   43a7c96a9975  pattern=0  bare=2   docs(p2-s6): gate3.md - the publication record, 

total pattern matches: 0
CLOSING-KEYWORD SCAN: CLEAN - no closing keyword precedes any issue reference
(exit 0)
```

- Pull request: https://github.com/MianliWang/gatebraid/pull/20 - referenced, not duplicated

## Required disclosures

- Deviations: `ci: none-configured` is a RECORDED FINDING, not a pass. This repository has no workflow at all - zero workflow files in the tree, `actions/workflows` total_count 0, and zero check runs on the published head - so the prohibition on merging with red CI is inert here and this record says so rather than implying a check occurred. The combined-status endpoint reports `pending` for a commit carrying zero statuses; that is the absence of any check, not a check in progress, and it is named here so no reader takes it for one.
- Deviations: the drift check's working-tree predicate is evaluated over the baseline EXCLUDING this gate's own write domain, with the unfiltered view recorded beside it - the same treatment Gate 0's A3 and Gate 2's baseline used, and for the same reason: this gate's own evidence directory is created BY the act of recording the gate, and the Gate 3 contract's Exit clause makes writing it not a violation. The filtered predicate is 43 lines, every one an untracked path under the retained P2-S5 evidence; the unfiltered view adds only paths under this Slice's own evidence directory and nothing else. Tracked changes are zero with no exclusion of any kind.
- Deviations: the approval's term 6 is the applied working-tree term and is recorded as applied. The tree lawfully carries the retained P2-S5 evidence - exactly the digest-verified 43-file set, re-derived here to 83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f by the same construction the setup report froze - plus the ignored `_handoff/` lane. No OTHER untracked or modified path exists, which is what that term makes the test.
- Deviations: the ref namespace carries one ref outside refs/heads, refs/remotes and refs/tags - a Codex turn-diff checkpoint pointing at a tree object. It is REPORTED and NOT ADOPTED, and it is NOT slice-introduced: the same ref is recorded in the retained P2-S5 Gate 0 evidence and in this Slice's own Gate 0 record, both of which predate this branch. No write of any kind was made into that namespace.
- Deviations: closure precondition (b) is checked as a PATTERN, never as a bare token, and the scan prints its matches beside its count. Twelve bare keyword tokens occur across the seven commit messages - every one a conventional-commit `fix(scope):` prefix or ordinary prose, which the contract names explicitly as not prohibited because it references nothing. Zero of them precede an issue reference. The scan was FALSIFIED before it was trusted: pointed at a seeded body carrying both `Closes #19` and `fixes owner/repo#17`, it fires on both and exits 1.
- Deviations: closure precondition (b) is recorded TWICE - once at the pull request's creation and once against its FINAL state after `gate3.md` was pushed, because pushing a commit changes what the pull request carries and a check run only before that push would not have covered the commit this record itself is. Both runs are recorded.
- Deviations: row G6 measures the pull request as it stood after this file's FIRST push, and this file's own second commit necessarily moves the head once more - a record cannot contain the aftermath of the commit that carries it. The boundary is stated rather than chased: what G6 establishes is that closure precondition (b) holds over every commit message the pull request carries INCLUDING this record's, which is the property the contract asks for. The check re-run against the truly final head is carried in _handoff/batch-p2s6/G3-PUBLICATION-REPORT-M3-P2S6.md, and the operator sees it before the merge.
- Deviations: this record carries NO merge SHA and NO closure timestamp, and asserts nothing about the merge. It is written and committed BEFORE the merge by the contract's normative order, so that it reaches the base branch through the pull request like every other change. The merge is the operator's own browser action under the approval's term 4; the authoritative Gate 3 record is the composite of this file, the pull request's merge event, the issue's closure event and the Project's Workflow.
- Deviations: the branch was pushed and the pull request opened, which are this gate's authorised publication actions. Nothing was merged, no branch was deleted, no tag was created, and no force-push was made or is available. `Next Approval` deliberately still reads the Release Approval option: the contract returns it to the bare option at Exit, after the merge, and this record is written before that.
- Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; shell Git Bash MINGW64 with Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0. environment=mixed-see-prose: this gate ran wholly on the Windows host.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S6
gate: 3
environment: mixed-see-prose
executor: Claude Lead
base_sha: 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
active_branch: slice/P2-S6
started_at: "2026-08-30T14:05:00Z"
ended_at: "2026-08-30T14:25:10Z"
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
    command: "git log --format=%H 5386ce382bac5b4bc1c76a38bcbe86717adf9c1c..HEAD -- ':!docs/evidence/gatebraid/P2-S6/'"
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
  - type: "Release Approval (G2→G3)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/19#issuecomment-5469136543"
    author: "MianliWang"
plan_hash: "4435c71eaf08bf0605815e5960c8093c4698babf99ae8a7030d05ebe445671d0"
allowlist_hash: "8938efcce4b8b863b14f7a503c808d7c2c67d2975aad180fd153fd45cc6da291"
evidence_files:
  - docs/evidence/gatebraid/P2-S6/gate3.md
notes: "PR https://github.com/MianliWang/gatebraid/pull/20. No merge SHA and no closure timestamp are recorded here - GitHub holds both natively (ADR-0017 section 2), and this file is written BEFORE the merge by the contract's normative order so that it reaches main through the pull request. The Release Approval was targeted BY COMMENT ID, never by matching words, because Gate 2's own exit names the same field and would match a naive search. Approval terms are cited by rule number, never restated. The merge is the operator's browser action under term 4 and is not asserted here."
```
