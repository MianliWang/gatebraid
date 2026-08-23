# Gate 3 evidence — P2-S3

## Publication records

**E1 — the writer role transferred: the `Writer Lease` taken by this session and read back (the reassignment's own requirement — the superseded value is named, not silently overwritten)**

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f query=mutation($p:ID!,$i:ID!,$f:ID!,$t:String!){updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,value:{text:$t}}){projectV2Item{id}}} -f p=PVT_kwHOBRofUs4Beum7 -f i=PVTI_lAHOBRofUs4Beum7zg3i6M0 -f f=PVTF_lAHOBRofUs4Beum7zhZJcSU -f t=RoughEgoist:p2s3-gate3-claude-writer:2026-08-23T04:17:31Z
{"data":{"updateProjectV2ItemFieldValue":{"projectV2Item":{"id":"PVTI_lAHOBRofUs4Beum7zg3i6M0"}}}}
  exit=0

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query($item:ID!){ node(id:$item){ ... on ProjectV2Item { content{ ... on Issue { number state labels(first:20){nodes{name}} } } fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldTextValue{ text field{ ... on ProjectV2FieldCommon{ name } } } ... on ProjectV2ItemFieldSingleSelectValue{ name optionId field{ ... on ProjectV2FieldCommon{ name } } } } } } } }' -F item=PVTI_lAHOBRofUs4Beum7zg3i6M0
{"data":{"node":{"content":{"number":12,"state":"OPEN","labels":{"nodes":[]}},"fieldValues":{"nodes":[{},{"text":"P2-S3 — gatebraid-validate repair: heuristic scope, markdown records, N2 re-validation completion","field":{"name":"Title"}},{"name":"Todo","optionId":"f75ad846","field":{"name":"Status"}},{"name":"Needs Review","optionId":"9b8a5a62","field":{"name":"Workflow"}},{"name":"G1 passed","optionId":"2a2ff00e","field":{"name":"Gate"}},{"name":"—","optionId":"450ee130","field":{"name":"Next Approval"}},{"name":"mixed-see-prose","optionId":"1e43ec85","field":{"name":"Environment"}},{"name":"Claude Lead","optionId":"ce859c7d","field":{"name":"Executor"}},{"name":"low","optionId":"e291249c","field":{"name":"Risk"}},{"text":"S2","field":{"name":"Stage"}},{"text":"P2","field":{"name":"Phase"}},{"text":"P2-S3","field":{"name":"Slice"}},{"text":"63c8401f5df6ba446cf002232fcb280673c28e00","field":{"name":"Base SHA"}},{"text":"2026-08-22T05:36:00Z Gate 2 built to the frozen plan; T1-T9 green; gate2.md needs_approval, fingerprint 28d5dfcd...; awaiting Review 1. Not pushed.","field":{"name":"Last Checkpoint"}},{"text":"RoughEgoist:p2s3-gate3-claude-writer:2026-08-23T04:17:31Z","field":{"name":"Writer Lease"}},{"text":"slice/P2-S3","field":{"name":"Active Branch"}}]}}}}
  exit=0
```

- Superseded value: `RoughEgoist:p2s3-gate2-claude-lead:2026-08-22T05:08:51Z` — the lease the closed writer session held, read live immediately before the write.
- New value: `RoughEgoist:p2s3-gate3-claude-writer:2026-08-23T04:17:31Z`, this session's own label in the recorded `<host>:<session-label>:<ISO8601>` format.
- One writer before, one writer after, never two at once. The prior writer session is closed and made no write after its lease was superseded.

**G0 — the two granted field writes, by option id, read back by id (the Release Approval's item 2; both option ids were verified against the live option set before either write, and neither value string was re-typed — CLAUDE.md's byte rule)**

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project item-edit --id PVTI_lAHOBRofUs4Beum7zg3i6M0 --project-id PVT_kwHOBRofUs4Beum7 --field-id PVTSSF_lAHOBRofUs4Beum7zhZJbxQ --single-select-option-id bd280e21
(no output)
  exit=0

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project item-edit --id PVTI_lAHOBRofUs4Beum7zg3i6M0 --project-id PVT_kwHOBRofUs4Beum7 --field-id PVTSSF_lAHOBRofUs4Beum7zhZGqt0 --single-select-option-id fb82cff0
(no output)
  exit=0

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query($item:ID!){ node(id:$item){ ... on ProjectV2Item { content{ ... on Issue { number state labels(first:20){nodes{name}} } } fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldTextValue{ text field{ ... on ProjectV2FieldCommon{ name } } } ... on ProjectV2ItemFieldSingleSelectValue{ name optionId field{ ... on ProjectV2FieldCommon{ name } } } } } } } }' -F item=PVTI_lAHOBRofUs4Beum7zg3i6M0
{"data":{"node":{"content":{"number":12,"state":"OPEN","labels":{"nodes":[]}},"fieldValues":{"nodes":[{},{"text":"P2-S3 — gatebraid-validate repair: heuristic scope, markdown records, N2 re-validation completion","field":{"name":"Title"}},{"name":"Todo","optionId":"f75ad846","field":{"name":"Status"}},{"name":"Gate 3 — Releasing","optionId":"fb82cff0","field":{"name":"Workflow"}},{"name":"G2 passed","optionId":"bd280e21","field":{"name":"Gate"}},{"name":"—","optionId":"450ee130","field":{"name":"Next Approval"}},{"name":"mixed-see-prose","optionId":"1e43ec85","field":{"name":"Environment"}},{"name":"Claude Lead","optionId":"ce859c7d","field":{"name":"Executor"}},{"name":"low","optionId":"e291249c","field":{"name":"Risk"}},{"text":"S2","field":{"name":"Stage"}},{"text":"P2","field":{"name":"Phase"}},{"text":"P2-S3","field":{"name":"Slice"}},{"text":"63c8401f5df6ba446cf002232fcb280673c28e00","field":{"name":"Base SHA"}},{"text":"2026-08-22T05:36:00Z Gate 2 built to the frozen plan; T1-T9 green; gate2.md needs_approval, fingerprint 28d5dfcd...; awaiting Review 1. Not pushed.","field":{"name":"Last Checkpoint"}},{"text":"RoughEgoist:p2s3-gate3-claude-writer:2026-08-23T04:17:31Z","field":{"name":"Writer Lease"}},{"text":"slice/P2-S3","field":{"name":"Active Branch"}}]}}}}
  exit=0
```

- Read back **by option id**, not by name: `Gate` = `bd280e21`, `Workflow` = `fb82cff0` — the two ids the Release Approval names. A name comparison cannot distinguish U+2014 EM DASH from U+2192 RIGHTWARDS ARROW, which is why the id is the thing compared.
- The `Writer Lease` is held by this session, the Slice issue is `OPEN`, and the label set is empty — so the `needs-human` removal this gate's Entry requires was already in force and **no label operation was performed**, which the Release Approval also does not authorise.
- `Status = Todo` is written by GitHub's own built-in workflow and is not Gatebraid state.

**G1 — Release Approval verified, and the reassignment that transfers it (author must be `MianliWang`, not this session — ADR-0020 §4; terms cited by rule number, never restated — ADR-0018 §3)**

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5381788134 --jq '{author: .user.login, assoc: .author_association, url: .html_url, issue: .issue_url, created: .created_at, updated: .updated_at}'
{"assoc":"OWNER","author":"MianliWang","created":"2026-08-22T17:54:08Z","issue":"https://api.github.com/repos/MianliWang/gatebraid/issues/12","updated":"2026-08-22T17:54:08Z","url":"https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5381788134"}
  exit=0

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5384146247 --jq '{author: .user.login, assoc: .author_association, url: .html_url, issue: .issue_url, created: .created_at, updated: .updated_at}'
{"assoc":"OWNER","author":"MianliWang","created":"2026-08-23T04:10:45Z","issue":"https://api.github.com/repos/MianliWang/gatebraid/issues/12","updated":"2026-08-23T04:10:45Z","url":"https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5384146247"}
  exit=0

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login
mianliwang492-source
  exit=0
```

- The approval states its publication terms and enumerates what is not authorised; it is not a `gatebraid/handoff@1` block; its author differs from the executing session's identity above. Valid on all three entry conditions.
- `created_at` equals `updated_at` on **both** comments, so each was read as posted: an edited grant cannot pass as an original one (ADR-0017 §4).
- The reassignment supplements the approval and edits none of it. It transfers the writer role, the lease and the grant to this session; every term of the approval stands. It is disclosed below and cited by id.

**G2a — closure precondition (a): platform automation (ADR-0012 §2)**

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query($p:ID!){ node(id:$p){ ... on ProjectV2 { workflows(first:20){ nodes{ name enabled } } } } }' -F p=PVT_kwHOBRofUs4Beum7
{"data":{"node":{"workflows":{"nodes":[{"name":"Auto-add sub-issues to project","enabled":true},{"name":"Auto-close issue","enabled":false},{"name":"Item added to project","enabled":true},{"name":"Item closed","enabled":true},{"name":"Pull request linked to issue","enabled":true},{"name":"Pull request merged","enabled":true}]}}}}
  exit=0
```

- `Auto-close issue: enabled=false`. All six built-in workflows are read and printed, so the row is read in context rather than asserted alone, and it is the only one disabled — the state the manifest §8 and ADR-0011 §6 record. Were it enabled it would give a Slice a closure path that bypasses this gate, which is why the gate refuses to publish while it is on.

**G2b — closure precondition (b): the pull request (pattern stated, matches printed — `keyword #n | keyword owner/repo#n | keyword <url>`, keyword ∈ close(s|d)/fix(es|ed)/resolve(s|d), any case — ADR-0018 §1)**

```
$ C:/Python312/python -B docs/evidence/gatebraid/P2-S2/checks/closing-keyword-scan.py --range 63c8401f5df6ba446cf002232fcb280673c28e00..870a0ca026959014bf5bf0a14eaafefc104e6026
SEARCHED:
  git range 63c8401f5df6ba446cf002232fcb280673c28e00..870a0ca026959014bf5bf0a14eaafefc104e6026 -- 7 commit message(s), headline and body
PATTERN : keyword-then-reference, keyword in {close,closes,closed,fix,fixes,fixed,resolve,resolves,resolved}, any case;
          reference in {#n, owner/repo#n, <url ending issues/n>}.
          The bare token is NOT matched: a conventional-commit fix(scope): prefix
          references nothing and is not a match.

CLOSING-KEYWORD MATCHES (defused for the record): 0
  (none -- the zero above is over the sources named at the top of this output)

PLAIN REFERENCES (permitted; this is how a Slice issue is linked): 0
  (none)

VERDICT: PASS -- no closing keyword precedes any issue reference
  exit=0

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr view 13 --repo MianliWang/gatebraid --json number,state,isDraft,baseRefName,headRefName,headRefOid,closingIssuesReferences,url,title
{"baseRefName":"main","closingIssuesReferences":[],"headRefName":"slice/P2-S3","headRefOid":"870a0ca026959014bf5bf0a14eaafefc104e6026","isDraft":false,"number":13,"state":"OPEN","title":"P2-S3 — gatebraid-validate repair: heuristic scope, markdown records, N2 re-validation completion","url":"https://github.com/MianliWang/gatebraid/pull/13"}
  exit=0

$ C:/Python312/python -B docs/evidence/gatebraid/P2-S2/checks/closing-keyword-scan.py --text-file C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/5222090d-c1d9-4991-9d6d-0a48ad99cdd6/scratchpad/pr-13-body-live.md
SEARCHED:
  text file C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/5222090d-c1d9-4991-9d6d-0a48ad99cdd6/scratchpad/pr-13-body-live.md -- 1602 byte(s)
PATTERN : keyword-then-reference, keyword in {close,closes,closed,fix,fixes,fixed,resolve,resolves,resolved}, any case;
          reference in {#n, owner/repo#n, <url ending issues/n>}.
          The bare token is NOT matched: a conventional-commit fix(scope): prefix
          references nothing and is not a match.

CLOSING-KEYWORD MATCHES (defused for the record): 0
  (none -- the zero above is over the sources named at the top of this output)

PLAIN REFERENCES (permitted; this is how a Slice issue is linked): 1
  1  Refs #12

VERDICT: PASS -- no closing keyword precedes any issue reference
  exit=0

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/12 --jq {number,state,state_reason}
{"number":12,"state":"open","state_reason":null}
  exit=0
```

- `closingIssuesReferences` is empty: GitHub's own view is that this pull request would close nothing.
- The commit-message scan ran **before the push**, because contract row 2b makes a closing keyword in a commit message an uncorrectable error — amending history is a force-push, which this gate prohibits. Seven commit messages searched, zero matches.
- The body scan ran over the body **as GitHub holds it**, not over the draft that was submitted, so what is checked is what the platform will act on. The draft was also scanned before the pull request was opened.
- The checker is **P2-S2's committed instrument, reused** — the direction ADR-0028 §4 sets for evidence tooling — and it was falsified in-window before this run was trusted: on seeded input carrying all three reference forms it returned three matches and `VERDICT: FAIL` at exit 1, and it correctly did **not** match a conventional-commit `fix(scope):` prefix. The seed was written to a scratch path outside every repository.
- A match would be printed **defused**, with the keyword-to-reference adjacency broken: a checker never quotes what it forbids into a record in live form, and this record is itself committed (ADR-0028 §4). There were none.
- The Slice issue is linked by the plain reference `Refs #12` in the pull-request body and by no other form. `Refs` is not a closing keyword.
- The Slice issue is still `open`. Closure is this gate's exit by explicit command and is **not authorised on this grant**.

**G3 — drift check against the Gate 2 fingerprint (ADR-0011 §2 as amended by ADR-0016 §1) — pinned at both ends, so no row names a state the act of recording it would move (ADR-0028 §4)**

```
$ git diff --name-only 3012c2a70b053721f61f99bb5e2e1c41cdbc7408 870a0ca026959014bf5bf0a14eaafefc104e6026
docs/evidence/gatebraid/P2-S3/captures/G2-changed-paths.json
docs/evidence/gatebraid/P2-S3/captures/G2-executor-identity.json
docs/evidence/gatebraid/P2-S3/captures/G2-exit-readback.json
docs/evidence/gatebraid/P2-S3/captures/G2-fingerprint.json
docs/evidence/gatebraid/P2-S3/checks/g2_render_record.py
docs/evidence/gatebraid/P2-S3/gate2.md
  exit=0

$ git diff --name-only 3012c2a70b053721f61f99bb5e2e1c41cdbc7408 870a0ca026959014bf5bf0a14eaafefc104e6026 -- :!docs/evidence/gatebraid/P2-S3/
(no output)
  exit=0

$ git log --format=%H 28d5dfcd83b83b7541a3d8f73732fb833a3d119c..870a0ca026959014bf5bf0a14eaafefc104e6026 -- :!docs/evidence/gatebraid/P2-S3/
(no output)
  exit=0

$ git status --porcelain -- :!docs/evidence/gatebraid/P2-S3/
(no output)
  exit=0

$ git status --porcelain --untracked-files=all
?? docs/evidence/gatebraid/P2-S3/captures/G3-Q1-reassignment.json
?? docs/evidence/gatebraid/P2-S3/captures/G3-Q1-release-approval.json
?? docs/evidence/gatebraid/P2-S3/captures/G3-drift-commits.json
?? docs/evidence/gatebraid/P2-S3/captures/G3-drift-complement.json
?? docs/evidence/gatebraid/P2-S3/captures/G3-drift-diff.json
?? docs/evidence/gatebraid/P2-S3/captures/G3-fields-readback.json
?? docs/evidence/gatebraid/P2-S3/captures/G3-identity.json
?? docs/evidence/gatebraid/P2-S3/captures/G3-lease-readback.json
?? docs/evidence/gatebraid/P2-S3/captures/G3-lease-take.json
?? docs/evidence/gatebraid/P2-S3/captures/G3-porcelain-complement.json
?? docs/evidence/gatebraid/P2-S3/captures/G3-revalidate-markdown.json
?? docs/evidence/gatebraid/P2-S3/captures/G3-revalidate-structural.json
?? docs/evidence/gatebraid/P2-S3/captures/G3-write-gate.json
?? docs/evidence/gatebraid/P2-S3/captures/G3-write-workflow.json
  exit=0

$ git status --porcelain --untracked-files=all -- :!docs/evidence/gatebraid/P2-S3/
(no output)
  exit=0

$ git for-each-ref '--format=%(refname) %(objecttype)'
refs/codex/turn-diffs/checkpoints/6568734db6429e0860cf0954b19afffaadb93c9960d666efb23d1018f152be37/7f8d802c118042d20382a16a250ea1c5fb0bd87efd6e2a2ee3221558ade9c8f3/1785489900931/c0da4005-1ff6-434a-b1a5-9ad1a2af1b0e tree
refs/heads/m1-control-plane commit
refs/heads/m3/n0-ratification commit
refs/heads/main commit
refs/heads/slice/P2-S1 commit
refs/heads/slice/P2-S2 commit
refs/heads/slice/P2-S3 commit
refs/remotes/origin/HEAD commit
refs/remotes/origin/m1-control-plane commit
refs/remotes/origin/m3/n0-ratification commit
refs/remotes/origin/main commit
refs/remotes/origin/slice/P2-S1 commit
refs/remotes/origin/slice/P2-S2 commit
  exit=0
```

- Six changed paths past the fingerprint tree `3012c2a70b053721f61f99bb5e2e1c41cdbc7408`, every one inside this slice's evidence directory; the **complement is empty**, over the diff to commit `870a0ca026959014bf5bf0a14eaafefc104e6026`. The reviewed work — the two `bin/` instruments — is byte-unchanged since it was reviewed, which is the question the drift check exists to answer.
- No commit between the fingerprint's `active_branch_head` `28d5dfcd83b83b7541a3d8f73732fb833a3d119c` and `870a0ca026959014bf5bf0a14eaafefc104e6026` touches anything outside that directory.
- **The unrestricted `git status --porcelain` is not empty, and is recorded as measured rather than only in the form that passes.** Every entry is this gate's own evidence — its capture files and this record's renderer — committed together with this file. The contract's criterion is met on the complement: nothing outside this slice's evidence directory is modified or untracked, and that restricted row is the substantive one, because it is what distinguishes drift in the reviewed work from a gate writing its own evidence. Disclosed below as a deviation rather than smoothed away.
- **That row lists 14 entries and the commit carries more, which is a boundary and not a discrepancy.** The porcelain was read at `2026-08-23T04:27:28Z`; the captures for the push, the pull request, the CI read and this record's own renderer did not exist yet, because the commands they record had not run. A sweep cannot capture its own later output — the same inherent boundary this Slice's Gate 2 record names for T8. The complement row is unaffected: every path added after the read is inside the evidence directory the complement excludes, and the final pre-commit porcelain was re-read and carries nothing outside it.
- **One ref outside `refs/heads/`, `refs/remotes/` and `refs/tags/` is reported and not adopted** (gate-3-contract Action 1, friction #103). It is a `refs/codex/` turn-diff checkpoint pointing at a **tree**, not a commit, left by the read-only consultant; its embedded timestamp decodes to `2026-07-31T09:25:00.931Z`, more than three weeks before this slice opened, so the slice did not introduce it. It is the same ref P2-S1's and P2-S2's Gate 3 reported. It is local-only and unreachable by the publication: the push names one ref explicitly, and `push.default`, `push.followTags`, `remote.origin.push`, `remote.origin.mirror` and `push.autoSetupRemote` are all unset, verified before the push.

**G4 — publication commands, exactly as approved, in contract order**

```
$ git ls-remote origin
63c8401f5df6ba446cf002232fcb280673c28e00	HEAD
823502b4f5eba9e8c60c6056816817980bfea685	refs/heads/m1-control-plane
4ff3f7b1f49f6853b584f255a61cb6b99797acb4	refs/heads/m3/n0-ratification
63c8401f5df6ba446cf002232fcb280673c28e00	refs/heads/main
f4186342037870c33c50bb5b64a31430b462ac3e	refs/heads/slice/P2-S1
8c710ca0506e300653779d432fd7e56ae58c4212	refs/heads/slice/P2-S2
823502b4f5eba9e8c60c6056816817980bfea685	refs/pull/1/head
8c710ca0506e300653779d432fd7e56ae58c4212	refs/pull/11/head
4ff3f7b1f49f6853b584f255a61cb6b99797acb4	refs/pull/5/head
f4186342037870c33c50bb5b64a31430b462ac3e	refs/pull/9/head
  exit=0

$ git push --dry-run origin slice/P2-S3
--- stderr ---
To https://github.com/MianliWang/gatebraid.git
 * [new branch]      slice/P2-S3 -> slice/P2-S3
  exit=0

$ git push origin slice/P2-S3
--- stderr ---
remote: 
remote: Create a pull request for 'slice/P2-S3' on GitHub by visiting:        
remote:      https://github.com/MianliWang/gatebraid/pull/new/slice/P2-S3        
remote: 
To https://github.com/MianliWang/gatebraid.git
 * [new branch]      slice/P2-S3 -> slice/P2-S3
  exit=0

$ git ls-remote origin
63c8401f5df6ba446cf002232fcb280673c28e00	HEAD
823502b4f5eba9e8c60c6056816817980bfea685	refs/heads/m1-control-plane
4ff3f7b1f49f6853b584f255a61cb6b99797acb4	refs/heads/m3/n0-ratification
63c8401f5df6ba446cf002232fcb280673c28e00	refs/heads/main
f4186342037870c33c50bb5b64a31430b462ac3e	refs/heads/slice/P2-S1
8c710ca0506e300653779d432fd7e56ae58c4212	refs/heads/slice/P2-S2
870a0ca026959014bf5bf0a14eaafefc104e6026	refs/heads/slice/P2-S3
823502b4f5eba9e8c60c6056816817980bfea685	refs/pull/1/head
8c710ca0506e300653779d432fd7e56ae58c4212	refs/pull/11/head
4ff3f7b1f49f6853b584f255a61cb6b99797acb4	refs/pull/5/head
f4186342037870c33c50bb5b64a31430b462ac3e	refs/pull/9/head
  exit=0

$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr create --repo MianliWang/gatebraid --base main --head slice/P2-S3 --title 'P2-S3 — gatebraid-validate repair: heuristic scope, markdown records, N2 re-validation completion' --body-file C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/5222090d-c1d9-4991-9d6d-0a48ad99cdd6/scratchpad/pr-body-P2-S3.md
https://github.com/MianliWang/gatebraid/pull/13
  exit=0
```

- Exactly one ref reached the remote, by name, with no force and no tags; the repository carries no tags at all. `refs/heads/main` is unmoved at `63c8401f5df6ba446cf002232fcb280673c28e00`, its value before the push: no write reached the base branch except through the pull request (ADR-0017 §3).
- Every remote ref is accounted for: `main`; `m1-control-plane`, kept because the M1 manifest cites it; `m3/n0-ratification`, retained at its recorded head; `slice/P2-S1` and `slice/P2-S2`, retained per ADR-0025 §3; this slice's new ref; and four `refs/pull/<n>/head` refs GitHub maintains for pull requests 1, 5, 9 and 11. The set is closed and every member is explained.
- Pull request **#13**, head `870a0ca026959014bf5bf0a14eaafefc104e6026` at open, base `main`. Committing this file necessarily moves the head past the value this file records — the same boundary the contract names when it says exact head equality "was not strict but unsatisfiable". The live head is the pull request's own Commits tab.
- The pull-request body was submitted from a file pinned by sha256 as a capture input, hashed before the command ran. The title carries U+2014 EM DASH, written from explicit UTF-8 bytes and verified at codepoint level both before submission and in the stored value GitHub returned.

**G5 — CI status (`none-configured` is a recorded finding, not a pass — ADR-0011 §7, ADR-0019 §1)**

```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr checks 13 --repo MianliWang/gatebraid
--- stderr ---
no checks reported on the 'slice/P2-S3' branch
  exit=1
```

- `ci: none-configured`. **A finding, not a pass.** No workflow exists in this repository, so the prohibition on merging with red CI is inert here, and this record says so rather than implying a check occurred. The non-zero exit is the tool reporting an empty check set, not a failing check.

**G6 — the Gate 2 amendment re-validates (the Release Approval's item 1: `gate-run@2` 0 errors with the loader named, and the repaired validator's own markdown mode accepting the amended record)**

```
$ C:/Python312/python -B docs/evidence/gatebraid/P2-S3/checks/g0_record_validation.py docs/evidence/gatebraid/P2-S3/gate2.md schema/gate-run-v2.schema.json
{"loader": "PyYAML 6.0.2 / jsonschema 4.23.0 / Draft202012Validator", "interpreter": "C:\\Python312\\python.exe", "record": "docs/evidence/gatebraid/P2-S3/gate2.md", "record_bytes": 42529, "record_sha256": "c16a49b688df3b16f87295ee5b0cce890a3ea8ff89bd8ddf58c565f46b08eebd", "crlf_bytes": 0, "fences_under_heading": 1, "declared_schema": "gatebraid/gate-run@2", "file_id": "gatebraid/gate-run@2", "id_match": true, "gate": 2, "result": "passed", "bootstrap_exception_present": false, "base_sha_len": 40, "checks_total": 20, "checks_with_output_ref": 20, "approvals": [{"type": "Plan Approval (G1\u2192G2)", "author": "MianliWang"}], "started_at_is_str": true, "ended_at_is_str": true, "error_count": 0, "errors": []}
  exit=0

$ C:/Python312/python -B docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py C:/Python312/python docs/evidence/gatebraid/P2-S3/gate2.md
interpreter   : C:/Python312/python
documents     : 1
SWEEP COMPLETE rejected_or_errored=0
  exit=0
```

- Structural: `error_count` 0, `result: passed`, 20 checks and 20 with an `output_ref`, loader named in the output rather than assumed. The amended record is sha256 `c16a49b688df3b16f87295ee5b0cce890a3ea8ff89bd8ddf58c565f46b08eebd`, 42529 bytes.
- The repaired validator's **markdown mode** reads and accepts the amended `gate2.md`: 1 document, 0 rejected or errored, exit 0. That is this Slice's own subject instrument reading this Slice's own record — reported as such, not offered as independent validation.
- The structural check is deliberately **not** this Slice's validator. It reaches `jsonschema` directly and names its loader, so the two rows are independent of each other.

- Pull request: https://github.com/MianliWang/gatebraid/pull/13 — referenced, not duplicated (ADR-0017 §2)

## Required disclosures

- Deviations: **(1) The writer role was reassigned mid-Slice.** The original writer session — the one that took the lease `RoughEgoist:p2s3-gate2-claude-lead:2026-08-22T05:08:51Z` and made the six commits ending `78b2cdfa7340c898b156335415649d6a29b1ffae` — is closed. The operator transferred the writer role, the `Writer Lease` and the Release Approval's grant to this fresh session by the comment at https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5384146247 (id `5384146247`, 2026-08-23T04:10:45Z), which supplements the approval and edits none of it. This session certified it held no prior role on this Slice: it is not the closed writer session and it is not the Review-1 session, whose independence is untouched. The lease's superseded value is named at E1 above. Single-writer is preserved: one writer before, one after, never two.
  **(2)** The unrestricted `git status --porcelain` at the drift check is **not empty**, and is recorded in full at G3. Its entries are this gate's own evidence — the capture files and this record's renderer, committed with this file. The contract's criterion is met on the complement of this slice's evidence directory, which is the row that answers the question the drift check asks. Reported, not smoothed away; the same deviation P2-S2's Gate 3 recorded, for the same reason.
  **(3)** This gate records captures where the template's rows are inline command-and-output; the rows above are generated from those capture records, so each is pinned by a `gatebraid/evidence-capture@1` document as well as printed here. The template's `output_ref: "#publication-records"` is kept, and the capture paths are named by the elision markers wherever a row shows less than its capture.
  **(4)** Three rows beyond the template's fixed set are added — **E1**, the lease transfer, which the reassignment requires be read back and which is otherwise recorded nowhere; **G0**, the two granted field writes read back by id, following P2-S2; and **G6**, the item-1 re-validation. The headings are new and the choice is disclosed rather than made silently.
  **(5)** `ci: none-configured` is recorded as a finding, not a pass.
  **(6)** One `refs/codex/` tree ref is reported under G3 and not adopted; it predates the slice by more than three weeks and cannot reach the remote.
  **(7)** **This gate stops at the pull request.** The merge is not authorised here and is never the executor's: the operator merges in the browser. Exit steps 2 through 6 of the Gate 3 contract — the merge, `Gate → G3 passed`, `Workflow → Done`, explicit closure of the Slice issue, lease release, `Next Approval` back to the bare option, the friction append with its ordinals assigned from the measured end, and the record-keeping updates — are therefore **not performed here, and are reported rather than skipped silently**. They run under the closure batch's own posted approval.
  **(8)** Commit messages carry a `Co-Authored-By` trailer, which prior commits in this repository outside this Slice do not; it is added per the executing harness's standing instruction and is noted so the change in convention is not mistaken for drift. No commit message on this branch carries any issue reference; the Slice issue is linked by the plain `Refs #12` in the pull-request body alone.
  **(9)** **Two Python invocations early in this session did not carry `PYTHONDONTWRITEBYTECODE=1`** — read-only analysis of the schema and the review report during establishment, before this gate's own work began. Measured consequence: none. Both read their program from stdin, so no source file existed beside which a cache could be written, and the tree was checked immediately afterwards — no `__pycache__` and no `.pyc` anywhere outside `.git/`, and `--untracked-files=all` porcelain empty. The rule is nevertheless *every* invocation, so the lapse is disclosed rather than excused by its null result; every invocation after it carried both the environment variable and `-B`. This is the over-disclosure direction (friction #107).
  **(10)** The renderer's pin on the review report was moved from the report as first reviewed to the **full current file**, per the coordinator's ruling, because the re-review addendum changed the bytes and the stale pin failed closed by design. The value the Gate 2 record *cites* is the addendum's own boundary-2 measurement, which is what the Release Approval cites. Both are verified at render time, not carried.
- Environment: Windows 11 (10.0.26200), Git Bash over Git for Windows 2.51.0 with the system `core.autocrlf=true` read from `D:/Program Files/Git/etc/gitconfig` and in-tree `.gitattributes` `* text=auto eol=lf`; `C:/Python312/python.exe` CPython 3.12.2 (jsonschema 4.23.0, PyYAML 6.0.2); declared `environment: mixed-see-prose`, the second platform being WSL Ubuntu `/usr/bin/python3` CPython 3.12.3 (jsonschema 4.10.3, PyYAML 6.0.1), exercised at Gate 2 and not re-entered here; `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` set on every `gh` invocation, with the identity check run first and alone; every `gh api` endpoint written without a leading slash, because MSYS rewrites leading-slash endpoints into filesystem paths (friction #33); `PYTHONDONTWRITEBYTECODE=1` and `-B` on every Python invocation of this gate, with the two establishment-phase exceptions disclosed above; all seeded and scratch files written to a scratch path outside every repository.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S3
gate: 3
environment: mixed-see-prose
executor: Claude Lead
base_sha: 63c8401f5df6ba446cf002232fcb280673c28e00
active_branch: slice/P2-S3
started_at: "2026-08-23T04:17:31Z"
ended_at: "2026-08-23T04:36:55Z"
result: passed
checks:
  - name: writer-lease-transferred-readback
    command: "gh api graphql updateProjectV2ItemFieldValue (Writer Lease) + read-back"
    result: pass
    output_ref: "#publication-records"
  - name: granted-field-writes-readback
    command: "gh project item-edit x2 by option id, then one read-back by item id"
    result: pass
    output_ref: "#publication-records"
  - name: release-approval-verified
    command: "gh api repos/MianliWang/gatebraid/issues/comments/5381788134 --jq {author,url,created,updated}"
    result: pass
    output_ref: "#publication-records"
  - name: closure-precondition-automation
    command: "gh api graphql -f query=query($p:ID!){ node(id:$p){ ... on ProjectV2 { workflows(first:20){ nodes{ name enabled } } } } } -F p=PVT_kwHOBRofUs4Beum7"
    result: pass
    output_ref: "#publication-records"
  - name: closure-precondition-pull-request
    command: "gh pr view 13 --json closingIssuesReferences; closing-keyword-scan.py run twice - over every commit message before the push, and over the pull-request body as GitHub holds it"
    result: pass
    output_ref: "#publication-records"
  - name: staged-set-matches-gate2-handoff
    command: "git diff --name-only 3012c2a70b053721f61f99bb5e2e1c41cdbc7408 870a0ca026959014bf5bf0a14eaafefc104e6026"
    result: pass
    output_ref: "#publication-records"
  - name: ref-namespace-clean
    command: "git for-each-ref --format=%(refname) %(objecttype)"
    result: pass
    output_ref: "#publication-records"
  - name: publication-push-one-ref
    command: "git push origin slice/P2-S3, with git ls-remote origin before and after"
    result: pass
    output_ref: "#publication-records"
  - name: pull-request-opened
    command: "gh pr create --repo MianliWang/gatebraid --base main --head slice/P2-S3"
    result: pass
    output_ref: "#publication-records"
  - name: ci-status
    command: "gh pr checks 13 --repo MianliWang/gatebraid"
    result: none_configured
    output_ref: "#publication-records"
  - name: gate2-amendment-revalidates
    command: "checks/g0_record_validation.py gate2.md schema/gate-run-v2.schema.json; checks/g1_sweep.py over gate2.md"
    result: pass
    output_ref: "#publication-records"
consults: []
approvals:
  - type: "Release Approval (G2→G3)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5381788134"
    author: "MianliWang"
    at: "2026-08-22T17:54:08Z"
evidence_files:
  - docs/evidence/gatebraid/P2-S3/gate3.md
notes: "PR https://github.com/MianliWang/gatebraid/pull/13, head 870a0ca026959014bf5bf0a14eaafefc104e6026 at open. No merge SHA and no closure timestamp are recorded here - GitHub holds both natively (ADR-0017 2). The merge and the closure batch are not authorized on this grant and are not performed: the operator merges in the browser. The writer role was reassigned mid-Slice to this session by comment 5384146247, which supplements the Release Approval and edits none of it; the superseded lease value is recorded at E1. This gate published the amendment commit 870a0ca026959014bf5bf0a14eaafefc104e6026, tree 804bdf1c000b3a0326116b0ae33a81ada57ce1a7, whose parent is exactly 78b2cdfa7340c898b156335415649d6a29b1ffae - two paths, both inside the frozen allowlist, carrying the re-review transcription that turned R3 and the result: passed the Release Approval granted."
```
