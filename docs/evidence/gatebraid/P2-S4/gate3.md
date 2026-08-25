# Gate 3 evidence — P2-S4

## Publication records

**G1 — Release Approval verified (author must be `MianliWang`, not this session — ADR-0020 §4; terms cited by rule number, never restated — ADR-0018 §3)**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5415966794 --jq '{author: .user.login, url: .html_url, created: .created_at, updated: .updated_at, association: .author_association}'
{"association":"OWNER","author":"MianliWang","created":"2026-08-25T19:57:24Z","updated":"2026-08-25T19:57:24Z","url":"https://github.com/MianliWang/gatebraid/issues/14#issuecomment-5415966794"}
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login
mianliwang492-source
(exit 0)
```

- Approval author `MianliWang`, `author_association` `OWNER`; executor identity `mianliwang492-source`. The approval was not written by the session it authorises.
- `created_at` equals `updated_at`, so the grant that was posted is the grant that was read.
- Entry conditions (a), (b), (c) of the Gate 3 contract are met: the comment is not a `gatebraid/handoff@1` block, it states the publication terms in its clause 2, and it is authored by the operator's personal account. **Its clause 2 is cited, not restated** — the terms bind from the comment, and a copy here would be a second thing to keep true.

**G2a — closure precondition (a): platform automation (ADR-0012 §2)**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query{ user(login:"MianliWang"){ projectV2(number:1){ workflows(first:20){ nodes{ name enabled updatedAt } } } } }'
{"data":{"user":{"projectV2":{"workflows":{"nodes":[{"name":"Auto-add sub-issues to project","enabled":true,"updatedAt":"2026-07-28T19:47:31Z"},{"name":"Auto-close issue","enabled":false,"updatedAt":"2026-07-30T21:45:57Z"},{"name":"Item added to project","enabled":true,"updatedAt":"2026-07-28T19:47:31Z"},{"name":"Item closed","enabled":true,"updatedAt":"2026-07-28T19:47:31Z"},{"name":"Pull request linked to issue","enabled":true,"updatedAt":"2026-07-28T19:47:31Z"},{"name":"Pull request merged","enabled":true,"updatedAt":"2026-07-28T19:47:31Z"}]}}}}}
(exit 0)
```

- `Auto-close issue` is **disabled**, `updatedAt 2026-07-30T21:45:57Z`. Of the five enabled built-in workflows none closes an issue: the chain that would — `Pull request merged` writing `Status` to `Done`, then `Auto-close issue` closing on that write — is **broken at exactly the disabled link**.

**G2b — closure precondition (b): the pull request (pattern stated, matches printed — `keyword #n | keyword owner/repo#n | keyword <url>`, keyword ∈ close(s|d)/fix(es|ed)/resolve(s|d), any case — ADR-0018 §1)**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query{ repository(owner:"MianliWang", name:"gatebraid"){ pullRequest(number:16){ number url baseRefName headRefName mergeable state closingIssuesReferences(first:10){ totalCount nodes{ number } } } } }'
{"data":{"repository":{"pullRequest":{"number":16,"url":"https://github.com/MianliWang/gatebraid/pull/16","baseRefName":"main","headRefName":"slice/P2-S4","mergeable":"MERGEABLE","state":"OPEN","closingIssuesReferences":{"totalCount":0,"nodes":[]}}}}}
(exit 0)
```

**G2b continued — the pattern search over every commit message the pull request carries, and over the pull-request body. **The body was checked BEFORE the pull request was opened**, which is the gate's normal loop for its own draft rather than a correction after the fact**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g3/closure-precheck.py --range df666070ead7fa21bc72b6c99d2644923b37e787..e29756c33d93c3432918c53b2e45e51235521c35
check          : Gate 3 closure precondition (b), keyword half
scope          : every commit message in df666070ead7fa21bc72b6c99d2644923b37e787..e29756c33d93c3432918c53b2e45e51235521c35 (17 commits)
pattern        : a closing keyword IMMEDIATELY PRECEDING an issue reference
keywords       : close/closes/closed, fix/fixes/fixed, resolve/resolves/resolved
reference forms: #n | owner/repo#n | https://github.com/owner/repo/issues/n

PROHIBITED PATTERN matches   : 0

bare keyword tokens          : 18  (NOT prohibited; printed so the count above states what it searched)
   'fix'        e29756c33d93c3432918c53b2e45e51235521c35 fix(m3): P2-S4 Gate 3 instruments emit explic
   'fixed'      his time inside this Slice's OWN gate instrument, and it is fixed by the doctrine the Slice ships.  closu
   'close'      d it is inside refs/heads/.  Closure precondition (a): Auto-close issue is DISABLED, updatedAt 2026-07-30
   'closes'     At 2026-07-30T21:45:57Z. Of the five enabled built-ins none closes an issue; the Pull-request-merged to S
   'close'      closes an issue; the Pull-request-merged to Status-Done to close chain is broken at exactly that disable
   'closed'     ns beside the zero so the count states what it searched -- 'closed by measurement', 'fixtures', 'fix(m3):
   'fix'        count states what it searched -- 'closed by measurement', 'fixtures', 'fix(m3):' are all present and non
   'fix'        s what it searched -- 'closed by measurement', 'fixtures', 'fix(m3):' are all present and none is prohibi
   'closed'     1, R4 PASS with F-02 and F-03, R5 PASS. Supplementary: R3-Q closed by measurement -- the reviewer materia
   'close'      to the batch-frozen value, closing the gap a writer cannot close for itself. R4-B confirmed 12/12 with t
   'fix'        no range row, per the grant: new row V19 shows schema/ and fixtures/ are the same TREE OBJECTS at the pl
   'fix'        baseline and at the fingerprint commit -- schema afbaab4f, fixtures 802366be, identical at both -- compo
   [... shown 12 of 18]
[... shown 22 of 24 lines (head); full output: docs/evidence/gatebraid/P2-S4/g3/G3-closure-b-commits.json]
(exit 0)
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g3/closure-precheck.py --file _handoff/batch-o0/PR-BODY-P2S4.md
check          : Gate 3 closure precondition (b), keyword half
scope          : the file _handoff/batch-o0/PR-BODY-P2S4.md (3881 bytes)
pattern        : a closing keyword IMMEDIATELY PRECEDING an issue reference
keywords       : close/closes/closed, fix/fixes/fixed, resolve/resolves/resolved
reference forms: #n | owner/repo#n | https://github.com/owner/repo/issues/n

PROHIBITED PATTERN matches   : 0

bare keyword tokens          : 6  (NOT prohibited; printed so the count above states what it searched)
   'closed'     ## Slice P2-S4 — O0 snapshot/frontier hardening: the fail-closed pair  Refs #14  Delivers M3-PLAN §2 no
   'closed'     becomes a `sources[]` entry with a status from the schema's closed enumeration. A read that fails while t
   'closed'     an incomplete read and says where it stopped. - **P0-4** — closed enumerations, both dependency directio
   'closed'     unblocked. An `Aborted` slice is never `startable`.  Every closed enumeration is **read from the frozen
   'fix'        nd re-typing either mark is how they drift.  `schema/` and `fixtures/` are the batch lane's, frozen, and
   'closed'     R2 · R3 · R4 · R5 all PASS**, with two supplementary items closed by measurement. Two repairs were spent

CLOSURE PRECONDITION (b) HOLDS: no closing keyword immediately precedes an issue reference in the scope above
(exit 0)
```

- `closingIssuesReferences` `totalCount` **0**, nodes empty.
- Prohibited-pattern matches: **0** in the commit messages, **0** in the body. Bare keyword tokens are printed beside each zero so the count states what it searched (friction #87): the branch carries ten — `closed by measurement`, `fixtures`, `fix(m3):` among them — and **none is prohibited**. A check that flagged those is one correct work cannot satisfy (ADR-0018 §2).
- **`(a) pass` alone is not compliance**; both halves are recorded, and (b) exists because the 2026-07-30 measurement was GitHub's own behaviour, which (a) cannot see.

**G3 — drift check against the Gate 2 fingerprint (ADR-0011 §2 as amended by ADR-0016 §1). Every revision is PINNED and passed in as an argument: this Slice's own F-01 lesson applied to its last gate, since `gate3.md`'s commit moves the branch head immediately after this runs**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g3/drift-check.py f797297005d35d150799af300ecc22daef35dac9 50d08de65158faf23f1ae86aeebcde39e929c359 e29756c33d93c3432918c53b2e45e51235521c35
tree_sha (as reviewed)        : f797297005d35d150799af300ecc22daef35dac9
active_branch_head            : 50d08de65158faf23f1ae86aeebcde39e929c359
head at drift-check time      : e29756c33d93c3432918c53b2e45e51235521c35
evidence prefix               : docs/evidence/gatebraid/P2-S4/

A  git diff --name-only <tree_sha> <head>
     paths changed              : 41
     outside the evidence dir   : 0
B  every commit in <active_branch_head>..<head>
     commits examined           : 9
        b3671fc99c18d56bb87b65876a547bfd1671d63a  changed=8   outside=0
        0964979cc58a6726a1e4c40debc4e0e887ad3d0d  changed=5   outside=0
        3a0f4ac96fa8f4572443820720033f6f1c929657  changed=13  outside=0
        32fb583f7c1da221f09f8e83c795eb6ed1d06a75  changed=6   outside=0
        aa3a905e6e18d3c0d3aec0a8307bc55dbe4cf362  changed=2   outside=0
        4b16273efdaaefe0bc2f6538cf7da3fd1d53a68d  changed=8   outside=0
        2225381aa6d701521236f6e8832fc7403806bfdf  changed=6   outside=0
        54eb5afd1c767c9ca37e6867da3c4bfcd578859a  changed=4   outside=0
        e29756c33d93c3432918c53b2e45e51235521c35  changed=3   outside=0
C  git status --porcelain
     entries                    : 0
D  git for-each-ref
     refs total                 : 18
     outside the three watched namespaces : 1
        refs/codex/turn-diffs/checkpoints/6568734db6429e0860cf0954b19afffaadb93c9960d666efb23d1018f152be37/7f8d802c118042d20382a16a250ea1c5fb0bd87efd6e2a2ee3221558ade9c8f3/1785489900931/c0da4005-1ff6-434a-b1a5-9ad1a2af1b0e
     watched namespaces         : refs/heads/, refs/remotes/, refs/tags/
     DISPOSITION: any ref above is REPORTED, NOT ADOPTED (friction #103).
     This Slice introduced none of them: it created exactly one ref,
     refs/heads/slice/P2-S4, which is inside refs/heads/.

checks failed                 : 0 
NO DRIFT: the reviewed work is unchanged; every change since the fingerprint is inside the slice's own evidence directory
(exit 0)
```

- The head this check names is the head at drift-check time, `e29756c33d93c3432918c53b2e45e51235521c35`, recorded in its own output. Commits after it are this record and its captures, inside the slice's evidence directory.

**G3-pass1 — the drift check's own falsification, retained (exit 1)**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g3/drift-check.py f797297005d35d150799af300ecc22daef35dac9 50d08de65158faf23f1ae86aeebcde39e929c359 4b16273efdaaefe0bc2f6538cf7da3fd1d53a68d
        ?? docs/evidence/gatebraid/P2-S4/g3/
D  git for-each-ref
     refs total                 : 17
     outside the three watched namespaces : 1
        refs/codex/turn-diffs/checkpoints/6568734db6429e0860cf0954b19afffaadb93c9960d666efb23d1018f152be37/7f8d802c118042d20382a16a250ea1c5fb0bd87efd6e2a2ee3221558ade9c8f3/1785489900931/c0da4005-1ff6-434a-b1a5-9ad1a2af1b0e
     watched namespaces         : refs/heads/, refs/remotes/, refs/tags/
     DISPOSITION: any ref above is REPORTED, NOT ADOPTED (friction #103).
     This Slice introduced none of them: it created exactly one ref,
     refs/heads/slice/P2-S4, which is inside refs/heads/.

checks failed                 : 1 (C)
DRIFT FOUND: route back to Needs Review; no publication
[... shown 12 of 30 lines (tail); full output: docs/evidence/gatebraid/P2-S4/g3/G3-drift-pass1.json]
(exit 1)
```

- Check **C fired** on the gate's own untracked evidence directory, created moments earlier to hold this very capture. **A drift check that had only ever passed would never have been shown able to fire**; pass 2 ran from a committed tree, where C measures what it is for. The same convention Gate 0 used for its sweep's first pass.

**G4 — publication commands, exactly as approved, in contract order**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr create --repo MianliWang/gatebraid --base main --head slice/P2-S4 --title 'Slice P2-S4 - O0 snapshot/frontier hardening: the fail-closed pair' --body-file _handoff/batch-o0/PR-BODY-P2S4.md
https://github.com/MianliWang/gatebraid/pull/16
(exit 0)
```

- Push, then pull request, per contract Action 2. `slice/P2-S4` and nothing else was published: no other branch, no tag, **no direct write to `main`**, and **no force-push at any point**.
- The pull request references the Slice issue by **plain reference only**.

**G5 — CI status (`none-configured` is a recorded finding, not a pass — ADR-0011 §7, ADR-0019 §1)**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh pr checks 16 --repo MianliWang/gatebraid

no checks reported on the 'slice/P2-S4' branch
(exit 1)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/actions/workflows --jq '{total_count: .total_count, names: [.workflows[].name]}'
{"names":[],"total_count":0}
(exit 0)
```

- `ci: none-configured`, established by measurement and not by the absence of a report: the repository has **`total_count` 0 workflows** and the tree at this head carries **no `.github/` path at all**.
- **Recorded as a finding.** Where no check exists, the prohibition on merging with red CI is inert; this record says so rather than implying a check occurred. `gh pr checks` exits 1 with *no checks reported*, which is the absence of a check and not a failing one.

- Pull request: https://github.com/MianliWang/gatebraid/pull/16 — referenced, not duplicated (ADR-0017 §2)

## Required disclosures

- Deviations: **BP-01 fired inside this gate's own instrument, and is fixed by the doctrine this Slice ships.** `closure-precheck.py` echoes matched context from arbitrary text, so its output carries whatever non-ASCII its input carries; run against the pull-request body under this host's cp936 console, `print()` re-encoded it and the capture recorded `decode_result: replaced` with a `0xa1` lead byte. The verdict was unaffected — exit 0, 0 prohibited matches — but **a check whose own output cannot be decoded is not evidence**. Both Gate 3 instruments now write explicit UTF-8 bytes to a binary sink, which is exactly what this Slice's P0-2 requires of its producer. The first run is retained at `g3/G3-closure-b-prbody-pass1.json`. Two defects in that patch were caught before it ran — a broken string literal, and a local variable that shadowed the new helper and would have raised at the first commit examined · **one commit message was rewritten on an unpushed commit.** The first attempt passed backticks through a shell, which substituted two words away, leaving *"a local named  in"*. The remote did not carry that commit — remote head was `54eb5afd…` — so the rewrite is a fast-forward and **no force-push was involved**; the Gate 3 prohibition is untouched. Later commit messages are passed through a file rather than a shell argument, which is the root fix · **one ref sits outside the three watched namespaces**, the pre-existing `refs/codex/turn-diffs/checkpoints/…` tree ref. **Reported, not adopted** (friction #103). This Slice created exactly one ref, `refs/heads/slice/P2-S4`, which is inside `refs/heads/` · **`ci: none-configured` is carried as a finding**, not a pass and not `skipped` · the debt this Slice carries past its own close is named in `gate2.md` and belongs to the batch lane and the closure ledger, not to this gate: the `gate-run@2` revision owing three items, N4's `isinstance` guard, N2's shape coverage, `bin/gatebraid-frontier.py`'s surviving docstring word, and F-04's unmeasured live transport.
- Environment: Windows 11 host, Git Bash (MSYS2) shell; git 2.51.0.windows.1 with `core.autocrlf=true` from the system gitconfig; Windows loader `C:\Python312\python.exe` (CPython 3.12.2, jsonschema 4.23.0); `PYTHONDONTWRITEBYTECODE=1` and `-B` on every Python invocation; `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` call, every endpoint written without a leading slash (friction #33). The console codec is cp936 and mangles U+2014 and U+2192, so every mark that decided an outcome here was compared by **codepoint**, never by rendered text.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S4
gate: 3
environment: mixed-see-prose
executor: Claude Lead
base_sha: df666070ead7fa21bc72b6c99d2644923b37e787
active_branch: slice/P2-S4
started_at: "2026-08-25T20:00:22.317616Z"
ended_at: "2026-08-25T20:11:12Z"
result: passed
checks:
  - name: release-approval-verified
    command: "gh api repos/MianliWang/gatebraid/issues/comments/5415966794 --jq '{author,url,created,updated}'"
    result: pass
    output_ref: "#publication-records"
  - name: staged-set-matches-gate2-handoff
    command: "drift-check.py f797297005d35d150799af300ecc22daef35dac9 50d08de65158faf23f1ae86aeebcde39e929c359 e29756c33d93c3432918c53b2e45e51235521c35"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g3/G3-drift.json"
  - name: closure-precondition-automation
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g3/G3-closure-a-workflows.json"
  - name: closure-precondition-pull-request
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g3/G3-closure-b-refs.json"
  - name: closure-precondition-keyword-commits
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g3/G3-closure-b-commits.json"
  - name: closure-precondition-keyword-body
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g3/G3-closure-b-prbody.json"
  - name: publication-push-and-pull-request
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g3/G3-pr-open.json"
  - name: ci-status
    command: "gh pr checks 16 --repo MianliWang/gatebraid"
    result: none_configured
    output_ref: "docs/evidence/gatebraid/P2-S4/g3/G3-ci-none-configured.json"
# The merge and the closure are post-merge facts. They live in the
# composite record (ADR-0017 section 1) and are not pre-attestable in a
# file written before the merge (friction #56).
consults: []
approvals:
  - type: "Release Approval (G2→G3)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/14#issuecomment-5415966794"
    author: "MianliWang"
    at: "2026-08-25T19:57:24Z"
evidence_files:
  - docs/evidence/gatebraid/P2-S4/gate3.md
notes: "PR https://github.com/MianliWang/gatebraid/pull/16. No merge SHA and no closure timestamp are recorded here -- GitHub holds both natively (ADR-0017 section 2), and the authoritative Gate 3 record is the COMPOSITE of this file, the pull request merge event, the issue closure event and the Project Workflow. A consumer reconstructing state reads the native EVENT SEQUENCE, not the last state: an issue can be reopened and a comment can be edited. ci is none_configured, carried as a FINDING and not as a pass -- the repository has zero workflows and the tree carries no .github path, so the prohibition on merging red is inert here and this record says so rather than implying a check occurred. The merge is the operator ACT, made in the browser with Create a merge commit, never squash and never rebase, because the commit structure is part of what was reviewed. This file is committed and pushed BEFORE that merge and reaches main through the pull request like every other change. repair_limit 2, both spent at Gate 2, zero remaining -- no repair is available at this gate and a failure here routes per the contract own table."
```
