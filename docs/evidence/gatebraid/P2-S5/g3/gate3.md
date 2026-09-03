# Gate 3 evidence - P2-S5

## Publication records

**G1 - Release Approval verified: located by fidelity against its committed source, then fetched by id, and the executor identity it is compared against**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5523023378 --jq '{author: .user.login, url: .html_url, association: .author_association}'
{"association":"OWNER","author":"MianliWang","url":"https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5523023378"}
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login
mianliwang492-source
(exit 0)
```

**G2a - closure precondition (a): platform automation**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query{node(id:"PVT_kwHOBRofUs4Beum7"){... on ProjectV2{workflows(first:30){nodes{name enabled}}}}}' --jq '.data.node.workflows.nodes[]|"\(if .enabled then "ENABLED " else "disabled" end)  \(.name)"'
ENABLED   Auto-add sub-issues to project
disabled  Auto-close issue
ENABLED   Item added to project
ENABLED   Item closed
ENABLED   Pull request linked to issue
ENABLED   Pull request merged
(exit 0)
```

**G2b - closure precondition (b), first half: the pull request's own closing references**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr view 21 --repo MianliWang/gatebraid --json number,state,baseRefName,headRefOid,closingIssuesReferences
{"baseRefName":"main","closingIssuesReferences":[],"headRefOid":"875d50c808d59ee49fecdf6c8d8f4f8e5c87b4b7","number":21,"state":"OPEN"}
(exit 0)
```

**G2b - closure precondition (b), falsified BEFORE the clean run is trusted: the same instrument over a seeded body carrying all three lawful reference shapes, and a conventional-commit near-miss that must not match**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g3/closing-keyword-scan.py --pr 21 --base cbd065893b37f20713ae35b8d2673bf26fe4d2ad --head HEAD --body-from docs/evidence/gatebraid/P2-S5/g3/falsification/SEED-closing-keyword-body.md
keyword pattern    : (?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(?:#\d+|[A-Za-z0-9._-]+/[A-Za-z0-9._-]+#\d+|https?://github\.com/\S+/issues/\d+)
scope              : the pull-request body and every commit message in cbd065893b37..HEAD

PR body (file:docs/evidence/gatebraid/P2-S5/g3/falsification/SEED-closing-keyword-body.md)
   pattern matches : 3  ['Closes #17', 'Fixes MianliWang/gatebraid#17', 'resolves https://github.com/MianliWang/gatebraid/issues/17']
   bare tokens     : 5  (a conventional-commit prefix references nothing and is not prohibited)

commit messages the pull request carries: 15
[... shown 14 of 29 lines; full output: docs/evidence/gatebraid/P2-S5/g3/captures/G3-G2b-keyword-scan-falsify.json]

total pattern matches: 3
   body  'Closes #17'
   body  'Fixes MianliWang/gatebraid#17'
   body  'resolves https://github.com/MianliWang/gatebraid/issues/17'
CLOSING-KEYWORD SCAN: FOUND - closure precondition (b) FAILS
(exit 1)
```

**G2b - closure precondition (b), second half: the pattern search over the pull-request body and every commit message the pull request carries, run against the FINAL pull-request state**
```
PENDING FIRST RENDER: G3-G2b-keyword-scan
```

**G3 - drift check against the Gate 2 fingerprint**
```
PENDING FIRST RENDER: G3-G3-drift
```

**G4 - publication commands, in the contract's order**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'echo "remote branch after git push -u origin slice/P2-S5:"; git ls-remote origin refs/heads/slice/P2-S5 | sed "s/^/   /"; echo "local HEAD: $(git rev-parse HEAD)"; echo; echo "base branch, measured immediately before the pull request was opened:"; git ls-remote origin refs/heads/main | sed "s/^/   /"; echo; echo "pull request:"; gh pr view 21 --repo MianliWang/gatebraid --json number,url,state,baseRefName,headRefName,headRefOid,mergeable --jq "to_entries[]|\"   \(.key): \(.value)\""'
remote branch after git push -u origin slice/P2-S5:
   875d50c808d59ee49fecdf6c8d8f4f8e5c87b4b7	refs/heads/slice/P2-S5
local HEAD: 875d50c808d59ee49fecdf6c8d8f4f8e5c87b4b7

base branch, measured immediately before the pull request was opened:
   cbd065893b37f20713ae35b8d2673bf26fe4d2ad	refs/heads/main

pull request:
   baseRefName: main
   headRefName: slice/P2-S5
   headRefOid: 875d50c808d59ee49fecdf6c8d8f4f8e5c87b4b7
   mergeable: MERGEABLE
   number: 21
   state: OPEN
   url: https://github.com/MianliWang/gatebraid/pull/21
(exit 0)
```

**G5 - CI status**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'echo "repository workflows : $(gh api repos/MianliWang/gatebraid/actions/workflows --jq .total_count)"; echo "workflow files in tree: $(git ls-tree -r --name-only HEAD | grep -c "^.github/workflows/" || true)"; echo "check runs on the PR head: $(gh api repos/MianliWang/gatebraid/commits/875d50c808d59ee49fecdf6c8d8f4f8e5c87b4b7/check-runs --jq .total_count)"; echo; echo "gh pr checks 21:"; gh pr checks 21 --repo MianliWang/gatebraid 2>&1 | sed "s/^/   /" || true'
repository workflows : 0
workflow files in tree: 0
check runs on the PR head: 0

gh pr checks 21:
   no checks reported on the 'slice/P2-S5' branch
(exit 0)
```

- Pull request: https://github.com/MianliWang/gatebraid/pull/21 - referenced, not duplicated (ADR-0017 section 2)
- CI: `ci: none-configured` - 0 repository workflows and 0 check runs on the pull-request head. A recorded finding, not a pass: where no check exists the prohibition on merging with red CI is inert, and this record says so rather than implying a check occurred.

## Required disclosures

- Deviations (gate-3-contract Action 1, and the drift check's own meaning): the drift check was run BEFORE publication and was clean - 0 of 76 changed paths outside the Slice's evidence directory, 0 of 9 commits past the fingerprint outside it, `git status --porcelain --untracked-files=all` at 0 lines. The G3 row above is a RE-RUN against the committed tree, because a first capture of it was taken after this gate had begun writing its own evidence and therefore recorded eight untracked `g3/` paths beside a summary line asserting emptiness. That capture is retained at `docs/evidence/gatebraid/P2-S5/g3/captures/G3-G3-drift-pass1.json` rather than deleted: it is a true record of its own instant, and the false line in it is the very class four Gate 2 findings were about.
- Deviations (friction #103): one ref outside `refs/heads/`, `refs/remotes/` and `refs/tags/` exists in this clone - a `refs/codex` checkpoint tree ref whose leaf file is dated 2026-07-31, more than a month before this Slice's work, and which this Slice's own entry report recorded as pre-existing. It is REPORTED and not adopted; this Slice introduced no ref.
- Deviations (ADR-0011 section 7, ADR-0019 section 1): `ci: none-configured`. Neither Gatebraid repository carries a workflow, so no check ran and none could. The figures above are read from the row that measures them.
- Deviations (ADR-0017 section 2): this record carries the pull request by URL and records NO merge SHA and NO closure timestamp. Both are held natively, and the authoritative Gate 3 record is the composite of this file, the merge event, the issue's closure event and the Project's `Workflow` field. A file written before the merge cannot attest to it (friction #56).
- Deviations (Release Approval terms 1 and 4): the merge is the operator's own browser action and no machine account performs it; the branch is retained after the merge, never deleted. This gate stops after pushing this record and holds.
- Deviations (Release Approval rulings 1 through 6, carried unchanged): F-08 leaves the Gate 2 sweep check typed `fail` with its residue diagnosed by class; F-07 and H-02 are queued together for the ADR-0026 clarification; the `--help` frozen-scope tension goes to closeout with the `bin/` docstring unedited; J-01's one-line subset-nomination wording and the `consults[]` recording gap are closeout items; and the Slice issue's Acceptance item 1, `R3 first-pass = pass`, is NOT met - the first-pass R3 verdict was FAIL, and O1's acceptance is decided at closeout, not by this publication.
- Environment (friction #89): Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; Git for Windows 2.51.0.windows.1 whose system configuration carries `core.autocrlf=true`; every `gh` call pins `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` and uses endpoints with no leading slash; every Python invocation carries `-B` with `PYTHONDONTWRITEBYTECODE=1`; Windows interpreter `C:/Python312/python.exe`, CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL `/usr/bin/python3`, CPython 3.12.3, jsonschema 4.10.3. Captures are argv-form unless the row declares shell semantics, in which case the shell, pipefail and the exit-code source are all recorded.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S5
gate: 3
environment: mixed-see-prose
executor: Claude Lead
base_sha: cbd065893b37f20713ae35b8d2673bf26fe4d2ad
active_branch: slice/P2-S5
started_at: "2026-09-03T09:00:00Z"
ended_at: "2026-09-03T08:49:25Z"
result: passed
checks:
  - name: staged-set-matches-gate2-handoff
    command: "git diff --name-only f696944947a342b6163bf4ad7d9137674830a2f7 HEAD; git log --format=%H 5b586029344eb6df4a964c34baa1eb12e2916f6d..HEAD -- ':!docs/evidence/gatebraid/P2-S5/'; git status --porcelain --untracked-files=all"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G3-drift.json"
  - name: closure-precondition-automation
    command: "the Project's built-in workflows read with their enabled state; Auto-close issue is disabled"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G2a-automation.json"
  - name: closure-precondition-pull-request
    command: "closingIssuesReferences empty; the closing-keyword pattern searched over the pull-request body and every commit message the pull request carries, matches printed beside the count"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G2b-keyword-scan.json"
  - name: closure-precondition-pull-request-falsified
    command: "the same instrument over a seeded body: it must fire on each lawful reference shape and must not match a conventional-commit prefix"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G2b-keyword-scan-falsify.json"
  - name: ci-status
    command: "repository workflows, workflow files in the tree, and check runs on the pull-request head"
    result: none_configured
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G5-ci.json"
  - name: publication-commands-in-contract-order
    command: "git push -u origin slice/P2-S5, read back from the remote; then the pull request opened to main by plain reference"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G4-publication.json"
consults: []
approvals:
  - type: "Release Approval (G2→G3)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5523023378"
    author: "MianliWang"
evidence_files:
  - docs/evidence/gatebraid/P2-S5/g3/gate3.md
notes: "PR https://github.com/MianliWang/gatebraid/pull/21. No merge SHA and no closure timestamp are recorded here - GitHub holds both natively (ADR-0017 section 2), and this file is written before the merge. The publication set is the reviewed tree at 5b586029344eb6df4a964c34baa1eb12e2916f6d (tree f696944947a342b6163bf4ad7d9137674830a2f7) plus the record-only evidence commits that follow it, every one inside docs/evidence/gatebraid/P2-S5/. CI is none-configured, a recorded finding rather than a pass. The Slice issue is referenced by plain reference and is closed at this gate's Exit by an explicit command, never by this pull request - closure is what releases native blocked-by dependents. Every figure in this record is derived from the row that measures it; four Gate 2 findings were a count or a status typed as a constant and later contradicted by its own row, and this record does not repeat that."
```
