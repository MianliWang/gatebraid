# Gate 3 evidence — P2-S1

## Publication records

**G1 — Release Approval verified** (author must be `MianliWang`, not this
session — ADR-0020 §4; terms cited by rule number, never restated —
ADR-0018 §3)

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5361194479 --jq '{author: .user.login, url: .html_url, created: .created_at}'
{"author":"MianliWang","created":"2026-08-20T20:18:28Z","url":"https://github.com/MianliWang/gatebraid/issues/8#issuecomment-5361194479"}
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login
mianliwang492-source
```

- The approval states its publication terms and enumerates what is not
  authorized; it is not a `gatebraid/handoff@1` block; its author differs from
  the executing session's identity above. Valid on all three entry conditions.

**G2a — closure precondition (a): platform automation** (ADR-0012 §2)

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f query='query{ node(id:"PVT_kwHOBRofUs4Beum7"){ ... on ProjectV2 { workflows(first:20){ nodes{ name enabled } } } } }' --jq '.data.node.workflows.nodes[] | select(.name=="Auto-close issue") | "\(.name): enabled=\(.enabled)"'
Auto-close issue: enabled=false
```

**G2b — closure precondition (b): the pull request** (pattern stated, matches
printed — `keyword #n | keyword owner/repo#n | keyword <url>`, keyword ∈
close(s|d)/fix(es|ed)/resolve(s|d), any case — ADR-0018 §1)

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr view 9 --repo MianliWang/gatebraid --json closingIssuesReferences
{"closingIssuesReferences":[]}

$ { gh pr view 9 --json body --jq .body; gh pr view 9 --json commits --jq '.commits[].messageHeadline, .commits[].messageBody'; } \
    | grep -o -i -E '(clos(e|es|ed)|fix(|es|ed)|resolve(|s|d))[[:space:]]+(#[0-9]+|[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#[0-9]+|https?://[^ ]*issues/[0-9]+)' | wc -l
0
(searched: pull request #9's body plus every commit headline and body the pull
request carries. Zero matches; any match would be printed above this count.)

$ ... | grep -o -i -E '(refs|part of)[[:space:]]+#[0-9]+' | sort | uniq -c
      2 Refs #8
```

- The Slice issue is linked by plain reference only. `Refs` is not a closing
  keyword; the conventional-commit `fix(scope):` form does not appear, and no
  keyword precedes any reference.

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/8 --jq '{state:.state}'
{"state":"open"}
```

**G3 — drift check against the Gate 2 fingerprint** (ADR-0011 §2 as amended
by ADR-0016 §1)

```
$ git diff --name-only 16b74f43307b57f326cc086714e468f4c7874461 382c734f5035dbe8130ded9fcc67cb3e241edc33
docs/evidence/gatebraid/P2-S1/captures/K1-blobs.json
docs/evidence/gatebraid/P2-S1/captures/K2b-gate-records.json
docs/evidence/gatebraid/P2-S1/checks/k1_blobs.py
docs/evidence/gatebraid/P2-S1/checks/k2b_gate_records.py
docs/evidence/gatebraid/P2-S1/checks/t5.py
docs/evidence/gatebraid/P2-S1/checks/t6.py
docs/evidence/gatebraid/P2-S1/checks/t7.py
docs/evidence/gatebraid/P2-S1/gate2-full/V1-windows-selftest.json
docs/evidence/gatebraid/P2-S1/gate2-full/V2-wsl-selftest.json
docs/evidence/gatebraid/P2-S1/gate2-full/V3-corpus-digest.json
docs/evidence/gatebraid/P2-S1/gate2-full/V6-path-containment.json
docs/evidence/gatebraid/P2-S1/gate2.md

$ git diff --name-only 16b74f43... 382c734f... | grep -v '^docs/evidence/gatebraid/P2-S1/' | wc -l
0

$ git log --format='%H' 1f2335e05c3aaade83cf33930a748bc60103cfde..382c734f5035dbe8130ded9fcc67cb3e241edc33 -- ':!docs/evidence/gatebraid/P2-S1/'
(empty — every commit past the fingerprint touches only the evidence directory)

$ git status --porcelain
(empty)

$ git for-each-ref --format='%(refname)' | grep -v -E '^refs/(heads|remotes|tags)/'
refs/codex/turn-diffs/checkpoints/<64-hex>/<64-hex>/1785489900931/<uuid>   (objecttype: tree)
```

- Twelve changed paths past the fingerprint, every one inside this slice's
  evidence directory; the complement is 0. The reviewed work — the two `bin/`
  instruments — is byte-unchanged since it was reviewed, which is the question
  the drift check exists to answer.
- **One ref outside `refs/heads/`, `refs/remotes/`, `refs/tags/` is reported and
  not adopted** (gate-3-contract Action 1, friction #103). It is a `refs/codex/`
  turn-diff checkpoint pointing at a **tree**, not a commit, left by the
  read-only consultant. Its embedded timestamp decodes to
  `2026-07-31T09:25:00.931Z`, three weeks before this slice opened, so the slice
  did not introduce it. It is local-only and unreachable by the publication: the
  push names one ref explicitly, and `push.default`, `push.followTags`,
  `remote.origin.push` and `remote.origin.mirror` are all unset.

**G4 — publication commands, exactly as approved, in contract order**

```
$ git push --dry-run origin slice/P2-S1
To https://github.com/MianliWang/gatebraid.git
 * [new branch]      slice/P2-S1 -> slice/P2-S1

$ git push origin slice/P2-S1
To https://github.com/MianliWang/gatebraid.git
 * [new branch]      slice/P2-S1 -> slice/P2-S1

$ git ls-remote origin
5bc41d7667d1ae019b228d43ed1ef29ea5c0b928        HEAD
823502b4f5eba9e8c60c6056816817980bfea685        refs/heads/m1-control-plane
4ff3f7b1f49f6853b584f255a61cb6b99797acb4        refs/heads/m3/n0-ratification
5bc41d7667d1ae019b228d43ed1ef29ea5c0b928        refs/heads/main
382c734f5035dbe8130ded9fcc67cb3e241edc33        refs/heads/slice/P2-S1
823502b4f5eba9e8c60c6056816817980bfea685        refs/pull/1/head
4ff3f7b1f49f6853b584f255a61cb6b99797acb4        refs/pull/5/head

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr create --repo MianliWang/gatebraid --base main --head slice/P2-S1 --title "P2-S1 — gatebraid-capture: the evidence generator and its selftest" --body-file <body>
https://github.com/MianliWang/gatebraid/pull/9
```

- Exactly one ref reached the remote, by name, with no force and no tags.
  `refs/heads/main` is unmoved at `5bc41d7667d1ae019b228d43ed1ef29ea5c0b928`,
  its value before the push: no write reached the base branch except through
  the pull request.
- Pull request **#9**, head `382c734f5035dbe8130ded9fcc67cb3e241edc33` at open.
  Committing this file necessarily moves the head past the value this file
  records — the same boundary the contract names when it says exact head
  equality "was not strict but unsatisfiable". The live head is the pull
  request's own Commits tab.

**G5 — CI status** (`none-configured` is a recorded finding, not a pass —
ADR-0011 §7, ADR-0019 §1)

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr checks 9 --repo MianliWang/gatebraid
no checks reported on the 'slice/P2-S1' branch
```

- `ci: none-configured`. **A finding, not a pass.** No workflow exists in this
  repository, so the prohibition on merging with red CI is inert here, and this
  record says so rather than implying a check occurred.

**G6 — every gate record validates after the amendment**

```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S1/checks/k2b_gate_records.py docs/evidence/gatebraid/P2-S1/gate0.json docs/evidence/gatebraid/P2-S1/gate1.md docs/evidence/gatebraid/P2-S1/gate2.md
schema: schema/gate-run-v2.schema.json
loader: jsonschema 4.23.0, Draft202012Validator
docs/evidence/gatebraid/P2-S1/gate0.json             schema=gatebraid/gate-run@2   gate=0 result=passed         conforms
docs/evidence/gatebraid/P2-S1/gate1.md               schema=gatebraid/gate-run@2   gate=1 result=needs_approval conforms
docs/evidence/gatebraid/P2-S1/gate2.md               schema=gatebraid/gate-run@2   gate=2 result=passed         conforms
records validated: 3  non-conforming: 0
exit: 0
```

- This discharges the follow-through `gate2.md` row V9 promised: that row's
  capture was necessarily taken before `gate2.md`'s own final write, and this
  row validates the post-amendment state.

- Pull request: https://github.com/MianliWang/gatebraid/pull/9 — referenced, not
  duplicated (ADR-0017 §2)

## Required disclosures

- Deviations: **(1)** This gate's executing session is **the same session that
  performed Review 1**, by explicit operator instruction in the live session,
  given after that session raised the role conflict and the operator reaffirmed
  with the transcription terms. Reviewer/writer separation is therefore not
  preserved for the Gate 2 transcription; the transcription source was
  hash-verified against the value the Release Approval cites before any text was
  copied, and the fact is recorded in `gate2.md` disclosure (7) as well as here.
  **(2)** The `Writer Lease` was taken for this grant although the approval's
  step 2 enumerates only `Gate` and `Workflow`; the approval's own "writer
  session, single writer" term and this contract's Exit 6 ("release the
  `Writer Lease`") both presuppose it is held, and no lease was held when it was
  taken. **(3)** `ci: none-configured` is recorded as a finding, not a pass.
  **(4)** One `refs/codex/` tree ref is reported under G3 and not adopted; it
  predates the slice by three weeks and cannot reach the remote.
  **(5)** This gate stops at the pull request. The merge is not authorized here
  and is never the executor's: the operator merges in the browser, and the
  closure batch — post-merge verification, `Workflow` → `Done`,
  `Gate` → `G3 passed`, explicit issue closure, friction append from #141,
  lease release, `Next Approval` back to the bare option, handoff comment,
  `Last Checkpoint` — runs under its own posted approval. Exit steps 2 through 6
  of this contract are therefore **not performed here, and are reported rather
  than skipped silently**.
- Environment: Windows 11 (10.0.26200), Git Bash over Git for Windows with the
  system `core.autocrlf=true` config in effect and in-tree `.gitattributes`
  `* text=auto eol=lf`; `C:/Python312/python.exe` CPython 3.12.2 (jsonschema
  4.23.0, PyYAML 6.0.2); second platform WSL Ubuntu 24.04.4, `/usr/bin/python3`
  CPython 3.12.3 (jsonschema 4.10.3); `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid`
  set and exported for every `gh` invocation; `PYTHONDONTWRITEBYTECODE=1` set for
  every Python invocation so no interpreter output reaches the tree.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S1
gate: 3
environment: mixed-see-prose
executor: Claude Lead
base_sha: 5bc41d7667d1ae019b228d43ed1ef29ea5c0b928
active_branch: slice/P2-S1
started_at: "2026-08-20T21:44:56Z"
ended_at: "2026-08-20T22:03:27.487798Z"
result: passed
bootstrap_exception: true
checks:
  - name: staged-set-matches-gate2-handoff
    command: "git diff --name-only 16b74f43307b57f326cc086714e468f4c7874461 382c734f5035dbe8130ded9fcc67cb3e241edc33"
    result: pass
    output_ref: "#publication-records"
  - name: closure-precondition-automation
    command: "gh api graphql ... ProjectV2 workflows(first:20) ... Auto-close issue"
    result: pass
    output_ref: "#publication-records"
  - name: closure-precondition-pull-request
    command: "gh pr view 9 --json closingIssuesReferences; keyword pattern over body and every commit"
    result: pass
    output_ref: "#publication-records"
  - name: ci-status
    command: "gh pr checks 9 --repo MianliWang/gatebraid"
    result: none_configured
    output_ref: "#publication-records"
  - name: gate-records-validate-post-amendment
    command: "docs/evidence/gatebraid/P2-S1/checks/k2b_gate_records.py gate0.json gate1.md gate2.md"
    result: pass
    output_ref: "#publication-records"
consults: []
approvals:
  - type: "Release Approval (G2→G3)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/8#issuecomment-5361194479"
    author: "MianliWang"
    at: "2026-08-20T20:18:28Z"
  - type: "State Packet Approval"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/8#issuecomment-5352888364"
    author: "MianliWang"
    at: "2026-08-20T07:38:58Z"
evidence_files:
  - docs/evidence/gatebraid/P2-S1/gate3.md
notes: "PR https://github.com/MianliWang/gatebraid/pull/9. No merge SHA and no closure timestamp are recorded here — GitHub holds both natively (ADR-0017 §2). The merge and the closure batch are not authorized on this grant and are not performed."
```
