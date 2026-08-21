# Gate 3 evidence — P2-S2

## Publication records

**G0 — the two granted field writes, by option id, read back by id** (the
Release Approval's step 2; the option ids and the field ids were verified
against the live option set before either write, and the value carrying
U+2014 EM DASH was never re-typed — CLAUDE.md's byte rule)

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project item-edit --id PVTI_lAHOBRofUs4Beum7zg3ZWpw --project-id PVT_kwHOBRofUs4Beum7 --field-id PVTSSF_lAHOBRofUs4Beum7zhZJbxQ --single-select-option-id bd280e21
exit 0
(no output)

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project item-edit --id PVTI_lAHOBRofUs4Beum7zg3ZWpw --project-id PVT_kwHOBRofUs4Beum7 --field-id PVTSSF_lAHOBRofUs4Beum7zhZGqt0 --single-select-option-id fb82cff0
exit 0
(no output)

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query($item:ID!){ node(id:$item){ ... on ProjectV2Item { content{ ... on Issue { number state labels(first:20){nodes{name}} } } fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldTextValue{ text field{ ... on ProjectV2FieldCommon{ name } } } ... on ProjectV2ItemFieldSingleSelectValue{ name optionId field{ ... on ProjectV2FieldCommon{ name } } } } } } } }' -F item=PVTI_lAHOBRofUs4Beum7zg3ZWpw
exit 0
{"data":{"node":{"content":{"number":10,"state":"OPEN","labels":{"nodes":[]}},"fieldValues":{"nodes":[{},{"text":"P2-S2 — the independent evidence validator (N3)","field":{"name":"Title"}},{"name":"Todo","optionId":"f75ad846","field":{"name":"Status"}},{"name":"Gate 3 — Releasing","optionId":"fb82cff0","field":{"name":"Workflow"}},{"name":"G2 passed","optionId":"bd280e21","field":{"name":"Gate"}},{"name":"—","optionId":"450ee130","field":{"name":"Next Approval"}},{"name":"mixed-see-prose","optionId":"1e43ec85","field":{"name":"Environment"}},{"name":"Claude Lead","optionId":"ce859c7d","field":{"name":"Executor"}},{"name":"low","optionId":"e291249c","field":{"name":"Risk"}},{"text":"S2","field":{"name":"Stage"}},{"text":"P2","field":{"name":"Phase"}},{"text":"P2-S2","field":{"name":"Slice"}},{"text":"11dbac47927bff5aa7c9e86124e85db9ecdbc650","field":{"name":"Base SHA"}},{"text":"RoughEgoist:P2-S2-gate2:2026-08-21T03:24:47Z","field":{"name":"Writer Lease"}},{"text":"slice/P2-S2","field":{"name":"Active Branch"}}]}}}}
```

- Read back by option id, not by name: `Gate` = `bd280e21`, `Workflow` =
  `fb82cff0` — the two ids the Release Approval names. `Writer Lease` is still
  held, the Slice issue is `OPEN`, and the label set is empty, so the
  `needs-human` removal this gate's Entry requires was already in force and no
  label operation was performed on this grant.
- `Status = Todo` is written by GitHub's own built-in workflow and is not
  Gatebraid state.

**G1 — Release Approval verified** (author must be `MianliWang`, not this
session — ADR-0020 §4; terms cited by rule number, never restated —
ADR-0018 §3)

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5373791858 --jq '{author: .user.login, assoc: .author_association, url: .html_url, issue: .issue_url, created: .created_at, updated: .updated_at}'
exit 0
{"assoc":"OWNER","author":"MianliWang","created":"2026-08-21T18:34:43Z","issue":"https://api.github.com/repos/MianliWang/gatebraid/issues/10","updated":"2026-08-21T18:34:43Z","url":"https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5373791858"}

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login
exit 0
mianliwang492-source
```

- The approval states its publication terms and enumerates what is not
  authorized; it is not a `gatebraid/handoff@1` block; its author differs from
  the executing session's identity above. Valid on all three entry conditions.
- `created_at` equals `updated_at`, so the comment read here is the comment as
  posted: an edited grant cannot pass as an original one (ADR-0017 §4).

**G2a — closure precondition (a): platform automation** (ADR-0012 §2)

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query($p:ID!){ node(id:$p){ ... on ProjectV2 { workflows(first:20){ nodes{ name enabled } } } } }' -F p=PVT_kwHOBRofUs4Beum7
exit 0
{"data":{"node":{"workflows":{"nodes":[{"name":"Auto-add sub-issues to project","enabled":true},{"name":"Auto-close issue","enabled":false},{"name":"Item added to project","enabled":true},{"name":"Item closed","enabled":true},{"name":"Pull request linked to issue","enabled":true},{"name":"Pull request merged","enabled":true}]}}}}
```

- `Auto-close issue: enabled=false`. All six built-in workflows are read and
  printed, so the row is read in context rather than asserted alone, and it is
  the only one disabled — the state the manifest §8 and ADR-0011 §6 record.
  Were it enabled it would give a Slice a closure path that bypasses this gate,
  which is why the gate refuses to publish while it is on.

**G2b — closure precondition (b): the pull request** (pattern stated, matches
printed — `keyword #n | keyword owner/repo#n | keyword <url>`, keyword ∈
close(s|d)/fix(es|ed)/resolve(s|d), any case — ADR-0018 §1)

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr view 11 --repo MianliWang/gatebraid --json number,state,isDraft,baseRefName,headRefName,headRefOid,closingIssuesReferences,url
exit 0
{"baseRefName":"main","closingIssuesReferences":[],"headRefName":"slice/P2-S2","headRefOid":"16c3f16939787c135c3aa1f1982995c854c9e32e","isDraft":false,"number":11,"state":"OPEN","url":"https://github.com/MianliWang/gatebraid/pull/11"}

$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S2/checks/closing-keyword-scan.py --range 11dbac47927bff5aa7c9e86124e85db9ecdbc650..16c3f16939787c135c3aa1f1982995c854c9e32e
exit 0
SEARCHED:
  git range 11dbac47927bff5aa7c9e86124e85db9ecdbc650..16c3f16939787c135c3aa1f1982995c854c9e32e -- 4 commit message(s), headline and body
PATTERN : keyword-then-reference, keyword in {close,closes,closed,fix,fixes,fixed,resolve,resolves,resolved}, any case;
          reference in {#n, owner/repo#n, <url ending issues/n>}.
          The bare token is NOT matched: a conventional-commit fix(scope): prefix
          references nothing and is not a match.

CLOSING-KEYWORD MATCHES (defused for the record): 0
  (none -- the zero above is over the sources named at the top of this output)

PLAIN REFERENCES (permitted; this is how a Slice issue is linked): 0
  (none)

VERDICT: PASS -- no closing keyword precedes any issue reference

$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S2/checks/closing-keyword-scan.py --text-file C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/1b6d872a-4ff2-49a8-aa6c-d5398a852e3b/scratchpad/pr-11-body-live.md
exit 0
SEARCHED:
  text file C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/1b6d872a-4ff2-49a8-aa6c-d5398a852e3b/scratchpad/pr-11-body-live.md -- 2671 byte(s)
PATTERN : keyword-then-reference, keyword in {close,closes,closed,fix,fixes,fixed,resolve,resolves,resolved}, any case;
          reference in {#n, owner/repo#n, <url ending issues/n>}.
          The bare token is NOT matched: a conventional-commit fix(scope): prefix
          references nothing and is not a match.

CLOSING-KEYWORD MATCHES (defused for the record): 0
  (none -- the zero above is over the sources named at the top of this output)

PLAIN REFERENCES (permitted; this is how a Slice issue is linked): 1
  1  Refs #10

VERDICT: PASS -- no closing keyword precedes any issue reference

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/10 --jq '{number,state,state_reason}'
exit 0
{"number":10,"state":"open","state_reason":null}
```

- `closingIssuesReferences` is empty: GitHub's own view is that this pull
  request would close nothing.
- The keyword scan ran **before the push**, because contract row 2b makes a
  closing keyword in a commit message an uncorrectable error — amending history
  is a force-push, which this gate prohibits. The checker was falsified in-window
  on seeded input carrying all three reference forms, and correctly did not
  match a conventional-commit `fix(scope):` prefix, before this run was trusted.
  It is committed at `docs/evidence/gatebraid/P2-S2/checks/closing-keyword-scan.py`
  and the row reproduces by running it.
- A match would be printed **defused**, with the keyword-to-reference adjacency
  broken: a checker never quotes what it forbids into a record in live form, and
  this record is itself committed (ADR-0028 §4). There were none.
- The Slice issue is linked by the plain reference `Refs #10` in the pull-request
  body and by no other form. `Refs` is not a closing keyword.
- The Slice issue is still `open`. Closure is this gate's exit by explicit
  command and is **not authorized on this grant**.

**G3 — drift check against the Gate 2 fingerprint** (ADR-0011 §2 as amended
by ADR-0016 §1) — pinned at both ends, so no row names `HEAD` (ADR-0028 §4)

```
$ git diff --name-only fa2c965c45ca9402588fa46f1f7d2c90e209679c 16c3f16939787c135c3aa1f1982995c854c9e32e
exit 0
docs/evidence/gatebraid/P2-S2/captures/G2-T8-pinned.json
docs/evidence/gatebraid/P2-S2/captures/G2-handoff-fingerprint.json
docs/evidence/gatebraid/P2-S2/captures/G2-writedomains-verify.json
docs/evidence/gatebraid/P2-S2/checks/verify-writedomains.py
docs/evidence/gatebraid/P2-S2/gate2.md

$ git diff --name-only fa2c965c45ca9402588fa46f1f7d2c90e209679c 16c3f16939787c135c3aa1f1982995c854c9e32e -- :!docs/evidence/gatebraid/P2-S2/
exit 0
(no output)

$ git log --format=%H dd56346221f2b65d78202fdc59479f243fc9cb4d..16c3f16939787c135c3aa1f1982995c854c9e32e -- :!docs/evidence/gatebraid/P2-S2/
exit 0
(no output)

$ git status --porcelain -- :!docs/evidence/gatebraid/P2-S2/
exit 0
(no output)

$ git status --porcelain
exit 0
?? docs/evidence/gatebraid/P2-S2/captures/G3-Q1-release-approval.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-autoclose.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-ci.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-commit-keywords.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-drift-commits.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-drift-complement.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-drift-diff.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-fields-readback.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-gate-records.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-identity.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-issue-state.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-lsremote-after.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-lsremote-before.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-porcelain-complement.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-porcelain-full.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-pr-body-keywords.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-pr-closing-refs.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-pr-create.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-push-dryrun.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-push.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-refns.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-write-gate.json
?? docs/evidence/gatebraid/P2-S2/captures/G3-write-workflow.json
?? docs/evidence/gatebraid/P2-S2/checks/closing-keyword-scan.py
?? docs/evidence/gatebraid/P2-S2/checks/validate-gate-records.py
?? docs/evidence/gatebraid/P2-S2/gate3.md

$ git for-each-ref '--format=%(refname) %(objecttype)'
exit 0
refs/codex/turn-diffs/checkpoints/6568734db6429e0860cf0954b19afffaadb93c9960d666efb23d1018f152be37/7f8d802c118042d20382a16a250ea1c5fb0bd87efd6e2a2ee3221558ade9c8f3/1785489900931/c0da4005-1ff6-434a-b1a5-9ad1a2af1b0e tree
refs/heads/m1-control-plane commit
refs/heads/m3/n0-ratification commit
refs/heads/main commit
refs/heads/slice/P2-S1 commit
refs/heads/slice/P2-S2 commit
refs/remotes/origin/HEAD commit
refs/remotes/origin/m1-control-plane commit
refs/remotes/origin/m3/n0-ratification commit
refs/remotes/origin/main commit
refs/remotes/origin/slice/P2-S1 commit
```

- Five changed paths past the fingerprint, every one inside this slice's
  evidence directory; the complement is **0**, over the diff from tree
  `fa2c965c45ca9402588fa46f1f7d2c90e209679c` to commit `16c3f16939787c135c3aa1f1982995c854c9e32e`. The reviewed work — the two
  `bin/` instruments — is byte-unchanged since it was reviewed, which is the
  question the drift check exists to answer.
- No commit between the fingerprint's `active_branch_head` `dd56346221f2b65d78202fdc59479f243fc9cb4d`
  and the amendment commit touches anything outside that directory.
- **The unrestricted `git status --porcelain` is not empty, and is recorded in
  full rather than only in the form that passes.** Its entries are this gate's
  own capture files and two committed check scripts, written moments earlier and
  committed together with this file. The contract's criterion is met on the
  complement — nothing outside this slice's evidence directory is modified or
  untracked — and that restricted row is the substantive one: it is what
  distinguishes drift in the reviewed work from a gate writing its own evidence.
  The unrestricted row is disclosed below as a deviation rather than smoothed
  away.
- **One ref outside `refs/heads/`, `refs/remotes/` and `refs/tags/` is reported
  and not adopted** (gate-3-contract Action 1, friction #103). It is a
  `refs/codex/` turn-diff checkpoint pointing at a **tree**, not a commit, left
  by the read-only consultant; its embedded timestamp decodes to
  `2026-07-31T09:25:00.931Z`, three weeks before this slice opened, so the slice
  did not introduce it. It is the same ref P2-S1's Gate 3 reported. It is
  local-only and unreachable by the publication: the push names one ref
  explicitly, and `push.default`, `push.followTags`, `remote.origin.push` and
  `remote.origin.mirror` are all unset.

**G4 — publication commands, exactly as approved, in contract order**

```
$ git ls-remote origin
exit 0
11dbac47927bff5aa7c9e86124e85db9ecdbc650	HEAD
823502b4f5eba9e8c60c6056816817980bfea685	refs/heads/m1-control-plane
4ff3f7b1f49f6853b584f255a61cb6b99797acb4	refs/heads/m3/n0-ratification
11dbac47927bff5aa7c9e86124e85db9ecdbc650	refs/heads/main
f4186342037870c33c50bb5b64a31430b462ac3e	refs/heads/slice/P2-S1
823502b4f5eba9e8c60c6056816817980bfea685	refs/pull/1/head
4ff3f7b1f49f6853b584f255a61cb6b99797acb4	refs/pull/5/head
f4186342037870c33c50bb5b64a31430b462ac3e	refs/pull/9/head

$ git push --dry-run origin slice/P2-S2
exit 0
To https://github.com/MianliWang/gatebraid.git
 * [new branch]      slice/P2-S2 -> slice/P2-S2

$ git push origin slice/P2-S2
exit 0
remote: 
remote: Create a pull request for 'slice/P2-S2' on GitHub by visiting:        
remote:      https://github.com/MianliWang/gatebraid/pull/new/slice/P2-S2        
remote: 
To https://github.com/MianliWang/gatebraid.git
 * [new branch]      slice/P2-S2 -> slice/P2-S2

$ git ls-remote origin
exit 0
11dbac47927bff5aa7c9e86124e85db9ecdbc650	HEAD
823502b4f5eba9e8c60c6056816817980bfea685	refs/heads/m1-control-plane
4ff3f7b1f49f6853b584f255a61cb6b99797acb4	refs/heads/m3/n0-ratification
11dbac47927bff5aa7c9e86124e85db9ecdbc650	refs/heads/main
f4186342037870c33c50bb5b64a31430b462ac3e	refs/heads/slice/P2-S1
16c3f16939787c135c3aa1f1982995c854c9e32e	refs/heads/slice/P2-S2
823502b4f5eba9e8c60c6056816817980bfea685	refs/pull/1/head
4ff3f7b1f49f6853b584f255a61cb6b99797acb4	refs/pull/5/head
f4186342037870c33c50bb5b64a31430b462ac3e	refs/pull/9/head

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr create --repo MianliWang/gatebraid --base main --head slice/P2-S2 --title 'P2-S2 — gatebraid-validate: the independent evidence validator and its selftest' --body-file C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/1b6d872a-4ff2-49a8-aa6c-d5398a852e3b/scratchpad/pr-body-P2-S2.md
exit 0
https://github.com/MianliWang/gatebraid/pull/11
```

- Exactly one ref reached the remote, by name, with no force and no tags.
  `refs/heads/main` is unmoved at `11dbac47927bff5aa7c9e86124e85db9ecdbc650`, its value
  before the push: no write reached the base branch except through the pull
  request (ADR-0017 §3).
- Every remote ref is accounted for: `main`; `m1-control-plane`, kept because
  the M1 manifest cites it; `m3/n0-ratification`, retained at its recorded head;
  `slice/P2-S1`, retained per ADR-0025 §3; this slice's new ref; and three
  `refs/pull/<n>/head` refs GitHub maintains for pull requests 1, 5 and 9. The
  set is closed and every member is explained.
- Pull request **#11**, head `16c3f16939787c135c3aa1f1982995c854c9e32e` at open, base
  `main`. Committing this file necessarily moves the head past the value this
  file records — the same boundary the contract names when it says exact head
  equality "was not strict but unsatisfiable". The live head is the pull
  request's own Commits tab.
- The pull-request body was submitted from a file pinned by sha256 as a capture
  input, hashed before the command ran.

**G5 — CI status** (`none-configured` is a recorded finding, not a pass —
ADR-0011 §7, ADR-0019 §1)

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr checks 11 --repo MianliWang/gatebraid
exit 1
no checks reported on the 'slice/P2-S2' branch
```

- `ci: none-configured`. **A finding, not a pass.** No workflow exists in this
  repository, so the prohibition on merging with red CI is inert here, and this
  record says so rather than implying a check occurred. The non-zero exit is the
  tool reporting an empty check set, not a failing check.

**G6 — every gate record validates after the Gate 2 amendment**

```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S2/checks/validate-gate-records.py docs/evidence/gatebraid/P2-S2/gate0.md docs/evidence/gatebraid/P2-S2/gate1.md docs/evidence/gatebraid/P2-S2/gate2.md
exit 0
schema: schema/gate-run-v2.schema.json
loader: PyYAML 6.0.2 / jsonschema 4.23.0 / Draft202012Validator
docs/evidence/gatebraid/P2-S2/gate0.md         schema=gatebraid/gate-run@2   gate=0 result=passed         checks=25  conforms
docs/evidence/gatebraid/P2-S2/gate1.md         schema=gatebraid/gate-run@2   gate=1 result=needs_approval checks=7   conforms
docs/evidence/gatebraid/P2-S2/gate2.md         schema=gatebraid/gate-run@2   gate=2 result=passed         checks=18  conforms
records validated: 3  non-conforming: 0
```

- Deliberately **not** this Slice's own validator. A record carrying
  `bootstrap_exception: true` claims no N3 independent validation — N2's and
  N3's own gate landings are re-validated with the landed validator only after
  N3's Gate 3, where the exception expires — so using N3's validator to bless
  N3's own gate records would be exactly the circularity the exception exists to
  name. The checker reaches `jsonschema` directly, names its loader, and was
  falsified in-window on a seeded record before this run was trusted.
- `gate1.md` is `needs_approval` by design: Gate 1's record is frozen at its
  report and the Plan Approval is the transition, not a rewrite of the record.
- This file is absent from the run above because it is written after that row.
  It is validated as a follow-through before its own commit, and that run is
  reported in the commit message — the same boundary `gate2.md`'s own final
  write met.

- Pull request: https://github.com/MianliWang/gatebraid/pull/11 — referenced, not duplicated (ADR-0017 §2)

## Required disclosures

- Deviations: **(1)** The unrestricted `git status --porcelain` at the drift
  check is **not empty**, and is recorded in full at G3. Its entries are this
  gate's own evidence — the capture files and two check scripts committed with
  this record. The contract's criterion is met on the complement of this slice's
  evidence directory, which is the row that answers the question the drift check
  asks; P2-S1's Gate 3 met the criterion unrestricted because that gate wrote no
  captures at all. Reported, not smoothed away.
  **(2)** This gate records captures where the template's rows are inline
  command-and-output; the rows below are generated from those capture records,
  so each is pinned by a `gatebraid/evidence-capture@1` document as well as
  printed here. The template's `output_ref: "#publication-records"` is kept, and
  the capture paths are named in the rows.
  **(3)** Two rows beyond the template's fixed set are added — **G0**, the two
  granted field writes read back by id, which are otherwise recorded nowhere,
  and **G6**, the post-amendment record validation, following P2-S1's Gate 3.
  The headings are new and the choice is disclosed rather than made silently.
  **(4)** `ci: none-configured` is recorded as a finding, not a pass.
  **(5)** One `refs/codex/` tree ref is reported under G3 and not adopted; it
  predates the slice by three weeks and cannot reach the remote.
  **(6)** This gate stops at the pull request. **The merge is not authorized
  here and is never the executor's**: the operator merges in the browser, and
  the closure batch — post-merge verification, `Workflow` → `Done`,
  `Gate` → `G3 passed`, explicit closure of the Slice issue, the friction append
  from #162, lease release, `Next Approval` back to the bare option, RB and brief
  updates, and the plan's after-N3-Gate-3 duty of re-validating N2's
  bootstrap-marked records with the landed validator — runs under its own posted
  approval. Exit steps 2 through 6 of this contract are therefore **not
  performed here, and are reported rather than skipped silently**.
  **(7)** Commit messages follow the repository's committed convention, which
  carries no co-author trailer, and this slice's commits carry no `Refs`
  trailer; the Slice issue is linked by the plain `Refs #10` in the pull-request
  body, which is the single linkage the Release Approval names.
- Environment: Windows 11 (10.0.26200), Git Bash over Git for Windows with the
  system `core.autocrlf=true` config in effect and in-tree `.gitattributes`
  `* text=auto eol=lf`; `C:/Python312/python.exe` CPython 3.12.2 (jsonschema
  4.23.0, PyYAML 6.0.2); declared `environment: mixed-see-prose`, the second
  platform being WSL Ubuntu 24.04.4 `/usr/bin/python3` CPython 3.12.3
  (jsonschema 4.10.3, PyYAML 6.0.1), exercised at Gate 2 and not re-entered
  here; `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` set and exported for every
  `gh` invocation, with the identity check run first and alone; every `gh api`
  endpoint written without a leading slash, because MSYS rewrites leading-slash
  endpoints into filesystem paths; `PYTHONDONTWRITEBYTECODE=1` and `-B` on every
  Python invocation so no interpreter output reaches the tree.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S2
gate: 3
environment: mixed-see-prose
executor: Claude Lead
base_sha: 11dbac47927bff5aa7c9e86124e85db9ecdbc650
active_branch: slice/P2-S2
started_at: "2026-08-21T18:50:12.735393Z"
ended_at: "2026-08-21T19:02:43.637964Z"
result: passed
bootstrap_exception: true
checks:
  - name: granted-field-writes-readback
    command: "gh project item-edit x2 by option id, then one read-back by item id"
    result: pass
    output_ref: "#publication-records"
  - name: release-approval-verified
    command: "gh api repos/MianliWang/gatebraid/issues/comments/5373791858 --jq {author,url,created,updated}"
    result: pass
    output_ref: "#publication-records"
  - name: closure-precondition-automation
    command: "gh api graphql ... ProjectV2 workflows(first:20) ... Auto-close issue"
    result: pass
    output_ref: "#publication-records"
  - name: closure-precondition-pull-request
    command: "gh pr view 11 --json closingIssuesReferences; checks/closing-keyword-scan.py run twice - over every commit message before the push, and over the pull-request body as GitHub holds it"
    result: pass
    output_ref: "#publication-records"
  - name: staged-set-matches-gate2-handoff
    command: "git diff --name-only fa2c965c45ca9402588fa46f1f7d2c90e209679c 16c3f16939787c135c3aa1f1982995c854c9e32e"
    result: pass
    output_ref: "#publication-records"
  - name: ref-namespace-clean
    command: "git for-each-ref --format=%(refname) %(objecttype)"
    result: pass
    output_ref: "#publication-records"
  - name: publication-push-one-ref
    command: "git push origin slice/P2-S2, with git ls-remote origin before and after"
    result: pass
    output_ref: "#publication-records"
  - name: pull-request-opened
    command: "gh pr create --repo MianliWang/gatebraid --base main --head slice/P2-S2"
    result: pass
    output_ref: "#publication-records"
  - name: ci-status
    command: "gh pr checks 11 --repo MianliWang/gatebraid"
    result: none_configured
    output_ref: "#publication-records"
  - name: gate-records-validate-post-amendment
    command: "checks/validate-gate-records.py gate0.md gate1.md gate2.md"
    result: pass
    output_ref: "#publication-records"
consults: []
approvals:
  - type: "Release Approval (G2→G3)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5373791858"
    author: "MianliWang"
    at: "2026-08-21T18:34:43Z"
  - type: "State Packet Approval"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5363954606"
    author: "MianliWang"
    at: "2026-08-21T01:07:41Z"
evidence_files:
  - docs/evidence/gatebraid/P2-S2/gate3.md
notes: "PR https://github.com/MianliWang/gatebraid/pull/11, head 16c3f16939787c135c3aa1f1982995c854c9e32e at open. No merge SHA and no closure timestamp are recorded here - GitHub holds both natively (ADR-0017 2). The merge and the closure batch are not authorized on this grant and are not performed: the operator merges in the browser."
```
