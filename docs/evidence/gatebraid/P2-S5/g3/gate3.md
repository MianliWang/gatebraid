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
{"baseRefName":"main","closingIssuesReferences":[],"headRefOid":"997606839e16e7b5d77135294320147769c442b4","number":21,"state":"OPEN"}
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
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g3/closing-keyword-scan.py --pr 21 --base cbd065893b37f20713ae35b8d2673bf26fe4d2ad --head HEAD
keyword pattern    : (?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(?:#\d+|[A-Za-z0-9._-]+/[A-Za-z0-9._-]+#\d+|https?://github\.com/\S+/issues/\d+)
scope              : the pull-request body and every commit message in cbd065893b37..HEAD

PR body (pr#21)
   pattern matches : 0  
   bare tokens     : 3  (a conventional-commit prefix references nothing and is not prohibited)

commit messages the pull request carries: 17
[... shown 16 of 28 lines; full output: docs/evidence/gatebraid/P2-S5/g3/captures/G3-G2b-keyword-scan.json]
   f5b42d8a719d  pattern=0  bare=1   evidence(p2-s5): the remediated record, its nove
   1fce6fb92914  pattern=0  bare=0   evidence(p2-s5): the extended claim re-check, an
   875d50c808d5  pattern=0  bare=3   evidence(p2-s5): the Exit record - the full re-r
   997606839e16  pattern=0  bare=2   evidence(p2-s5): Gate 3 publication record, firs
   5f9ac65ae5ef  pattern=0  bare=2   evidence(p2-s5): gate3.md - the sweep, and two m

total pattern matches: 0
CLOSING-KEYWORD SCAN: CLEAN - no closing keyword precedes any issue reference
(exit 0)
```

**G2b - closure precondition (b), the TAIL: the pattern applied to the message of the commit that carries this record, which the scan above cannot see because it runs before that commit exists. The pattern is read out of the scan's own output rather than retyped**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B -c '
import base64, io, json, re, sys
cap = json.load(io.open(sys.argv[1], encoding='\''utf-8'\''))
line = base64.b64decode(cap['\''streams'\'']['\''stdout'\'']['\''data'\'']).decode('\''utf-8'\'').split(chr(10))[0]
pat = line.split('\'':'\'', 1)[1].strip()
print('\''pattern, READ FROM %s and not retyped:'\'' % sys.argv[1])
print('\''   '\'' + pat)
msg = io.open(sys.argv[2], encoding='\''utf-8'\'').read()
p = re.findall(pat, msg, re.I)
bare = re.findall(r'\''(?i)(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)'\'', msg)
hashref = re.findall(r'\''(?<![A-Za-z0-9_])#[0-9]+'\'', msg)
url = re.findall(r'\''https?://github[.]com/[^ ]*/(?:issues|pull)/[0-9]+'\'', msg)
print()
print('\''message measured    : %s (%d bytes)'\'' % (sys.argv[2], len(msg.encode('\''utf-8'\''))))
print('\''   pattern matches  : %d'\'' % len(p))
print('\''   bare tokens      : %d  (a keyword referencing nothing is not prohibited)'\'' % len(bare))
print('\''   hash references  : %d'\'' % len(hashref))
print('\''   reference URLs   : %d'\'' % len(url))
print()
if p:
    print('\''MESSAGE CHECK: FAILED - a closing keyword precedes a reference'\'')
    raise SystemExit(1)
print('\''MESSAGE CHECK: CLEAN - no closing keyword precedes any reference, and the'\'')
print('\''message carries no reference of any shape for one to precede'\'')
' docs/evidence/gatebraid/P2-S5/g3/captures/G3-G2b-keyword-scan.json C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/3d38558d-0a4f-4c7a-aee0-96dab90c3692/scratchpad/pending-message.txt
pattern, READ FROM docs/evidence/gatebraid/P2-S5/g3/captures/G3-G2b-keyword-scan.json and not retyped:
   (?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?\s+(?:#\d+|[A-Za-z0-9._-]+/[A-Za-z0-9._-]+#\d+|https?://github\.com/\S+/issues/\d+)

message measured    : C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/3d38558d-0a4f-4c7a-aee0-96dab90c3692/scratchpad/pending-message.txt (2042 bytes)
   pattern matches  : 0
   bare tokens      : 3  (a keyword referencing nothing is not prohibited)
   hash references  : 0
   reference URLs   : 0

MESSAGE CHECK: CLEAN - no closing keyword precedes any reference, and the
message carries no reference of any shape for one to precede
(exit 0)
```

**G3 - drift check against the Gate 2 fingerprint**
```
$ PYTHONDONTWRITEBYTECODE=1 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'echo "paths changed tree_sha..HEAD                     : $(git diff --name-only f696944947a342b6163bf4ad7d9137674830a2f7 HEAD | wc -l)"; echo "of those, OUTSIDE the Slice evidence directory   : $(git diff --name-only f696944947a342b6163bf4ad7d9137674830a2f7 HEAD | grep -vc "^docs/evidence/gatebraid/P2-S5/")"; echo "commits past the fingerprint                     : $(git rev-list 5b586029344eb6df4a964c34baa1eb12e2916f6d..HEAD | wc -l)"; echo "of those, touching anything outside it           : $(git log --format="%H" 5b586029344eb6df4a964c34baa1eb12e2916f6d..HEAD -- ":!docs/evidence/gatebraid/P2-S5/" | wc -l)"; echo "git status --porcelain --untracked-files=all      : $(git status --porcelain --untracked-files=all | wc -l) lines"; echo "refs outside heads/remotes/tags                  : $(git for-each-ref --format="%(refname)" | grep -vcE "^refs/(heads|remotes|tags)/")"; echo; echo "the ref, reported and not adopted (friction #103):"; git for-each-ref --format="   %(refname) -> %(objecttype) %(objectname)" | grep -vE "refs/(heads|remotes|tags)/"'
paths changed tree_sha..HEAD                     : 88
of those, OUTSIDE the Slice evidence directory   : 0
commits past the fingerprint                     : 10
of those, touching anything outside it           : 0
git status --porcelain --untracked-files=all      : 0 lines
refs outside heads/remotes/tags                  : 1

the ref, reported and not adopted (friction #103):
   refs/codex/turn-diffs/checkpoints/6568734db6429e0860cf0954b19afffaadb93c9960d666efb23d1018f152be37/7f8d802c118042d20382a16a250ea1c5fb0bd87efd6e2a2ee3221558ade9c8f3/1785489900931/c0da4005-1ff6-434a-b1a5-9ad1a2af1b0e -> tree 8c7df84d62a5d70d4a9ed2f05edf2661bbf5bd43
(exit 0)
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

**G6 - the closed-set sweep over this gate's whole captured domain, run only AFTER the three seeded runs below proved this copy can fire**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g3/checks-g3-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g3/captures
captures swept : 38

=== candidate classification (every rule applied explicitly) ===
  E1 permitted repository                                    12
  E3 API-path fragment                                       3
  E4 git ref namespace, not a repository                     8
  E5 filesystem or URL path segment                          105
  E6 schema-id namespace                                     16
  E8 prose slash between ordinary words (named, not matched) 22
  I0 friction citation, not an issue reference               4
  I1 the subject issue                                       2
  N1 the permitted Project                                   1
  UNEXPLAINED                                                3

=== every REPOSITORY identity named anywhere ===
  MianliWang/gatebraid           x12   PERMITTED
[... shown 22 of 25 lines; full output: docs/evidence/gatebraid/P2-S5/g3/captures/G3-closed-set-sweep.json]

domain      : 38 documents (11 of this sweep's own reports excluded)
UNEXPLAINED RESIDUE: 3
    G3-G2b-message-check-pass1.json              stdout       repo
    G3-G2b-message-check-pass1.json              invocation   repo
    G3-G2b-message-check-pass2.json              notes        repo
(exit 1)
```

**G6 - falsified three ways BEFORE the run above is trusted: the retained Gate 1 seeds through this copy, the Gate 2 near-miss seed through this copy, and a new seed carrying a one-character near-miss for every domain fact this copy adds**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g3/checks-g3-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g3/../g1/falsification
captures swept : 2

=== candidate classification (every rule applied explicitly) ===
[... shown 8 of 19 lines; full output: docs/evidence/gatebraid/P2-S5/g3/captures/G3-closed-set-sweep-falsify-retained.json]
    SEED-out-of-namespace-item.json              stdout       node
    SEED-out-of-namespace-item.json              stdout       node
    SEED-out-of-set.json                         stdout       repo
    SEED-out-of-set.json                         stdout       node
    SEED-out-of-set.json                         stdout       issue
(exit 1)
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g3/checks-g3-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g3/../g2/falsification
captures swept : 1

=== candidate classification (every rule applied explicitly) ===
[... shown 8 of 27 lines; full output: docs/evidence/gatebraid/P2-S5/g3/captures/G3-closed-set-sweep-falsify-g2-seeds.json]
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
(exit 1)
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g3/checks-g3-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g3/falsification
captures swept : 1

=== candidate classification (every rule applied explicitly) ===
[... shown 8 of 27 lines; full output: docs/evidence/gatebraid/P2-S5/g3/captures/G3-closed-set-sweep-falsify-near-miss.json]
    SEED-near-miss-gate3-classes.json            document     repo
    SEED-near-miss-gate3-classes.json            document     repo
    SEED-near-miss-gate3-classes.json            document     repo
    SEED-near-miss-gate3-classes.json            document     issue
    SEED-near-miss-gate3-classes.json            document     issue
(exit 1)
```

- Pull request: https://github.com/MianliWang/gatebraid/pull/21 - referenced, not duplicated (ADR-0017 section 2)
- CI: `ci: none-configured` - 0 repository workflows and 0 check runs on the pull-request head. A recorded finding, not a pass: where no check exists the prohibition on merging with red CI is inert, and this record says so rather than implying a check occurred.

## Required disclosures

- Deviations (gate-3-contract Action 1, and the drift check's own meaning): the drift check was run BEFORE publication and was clean - 0 of 88 changed paths outside the Slice's evidence directory, 0 of 10 commits past the fingerprint outside it, `git status --porcelain --untracked-files=all` at 0 lines. The G3 row above is a RE-RUN against the committed tree, because a first capture of it was taken after this gate had begun writing its own evidence and therefore recorded eight untracked `g3/` paths beside a summary line asserting emptiness. That capture is retained at `docs/evidence/gatebraid/P2-S5/g3/captures/G3-G3-drift-pass1.json` rather than deleted: it is a true record of its own instant, and the false line in it is the very class four Gate 2 findings were about.
- Deviations (friction #103): one ref outside `refs/heads/`, `refs/remotes/` and `refs/tags/` exists in this clone - a `refs/codex` checkpoint tree ref whose leaf file is dated 2026-07-31, more than a month before this Slice's work, and which this Slice's own entry report recorded as pre-existing. It is REPORTED and not adopted; this Slice introduced no ref.
- Deviations (ADR-0011 section 7, ADR-0019 section 1): `ci: none-configured`. Neither Gatebraid repository carries a workflow, so no check ran and none could. The figures above are read from the row that measures them.
- Deviations (closure precondition (b), its own boundary): the scan covers the pull-request body and every commit message the pull request carried WHEN IT RAN, which cannot include the commit that carries this record. That tail is not waved through. Every Gate 3 commit message is written deliberately free of any issue or pull-request reference in any shape, and the message of the final one is measured before it is used, by the scanner's own pattern read out of the scanner's own output. The two measurements together cover the complete published set, and nothing is committed after them.
- Deviations (the captures sweep's own boundary): the sweep runs over the directory it also writes into, so it cannot cover captures created after it. It is re-run as late as the ordering allows, and the captures that still postdate it are exactly the `G3-record-*` ones: the record validator on each declared half, and the sweep pointed at this record's own bytes. Each is an instrument's output over files already inside the swept domain, and the record-sweep row above covers this file itself. The renderer verifies that claim at render time and found no other. This sentence states the STRUCTURE rather than a count on purpose: a count would be true when rendered and false one capture later, and re-rendering it would invalidate the very validations it counted.
- Deviations (ADR-0017 section 2): this record carries the pull request by URL and records NO merge SHA and NO closure timestamp. Both are held natively, and the authoritative Gate 3 record is the composite of this file, the merge event, the issue's closure event and the Project's `Workflow` field. A file written before the merge cannot attest to it (friction #56).
- Deviations (Release Approval terms 1 and 4): the merge is the operator's own browser action and no machine account performs it; the branch is retained after the merge, never deleted. This gate stops after pushing this record and holds.
- Deviations (Release Approval rulings 1 through 6, carried unchanged): F-08 leaves the Gate 2 sweep check typed `fail` with its residue diagnosed by class; F-07 and H-02 are queued together for the ADR-0026 clarification; the `--help` frozen-scope tension goes to closeout with the `bin/` docstring unedited; J-01's one-line subset-nomination wording and the `consults[]` recording gap are closeout items; and the Slice issue's Acceptance item 1, `R3 first-pass = pass`, is NOT met - the first-pass R3 verdict was FAIL, and O1's acceptance is decided at closeout, not by this publication.
- Deviations (ADR-0028 sections 2 and 3, the closed-set sweep): this gate's copy of the sweep adds 5 allowlist entries to the Gate 2 copy - 3 to the filesystem-segment set and 2 to the prose-pair set - removes 0, and additionally moves only its own default captures directory and its own self-exclusion prefix. It changes no rule, no regex and no residue criterion; its header names each entry and the reason for it, and these counts are computed by diffing the two files' allowlists rather than typed beside them, because the sentence said FOUR for one revision and went false the moment a fifth was admitted mid-gate. One entry was NOT anticipated - the copy was run unextended first, reported 2 residues, and both were this gate's own drift column heading, a slash-joined list of three git ref namespaces. It is admitted as an exact string and the new seed proves it is not acting as a prefix: the same token with a trailing period stays residue. Residue over this gate's own captures domain is 3, and the check above is typed from that number rather than beside it - for one pushed revision it was typed `pass` while the sweep it cites exited 1, and the fix was to derive the verdict from the capture. The residue that remains is entirely inside RETAINED SUPERSEDED captures - failing or replaced passes, kept because each is a true record of its instant - at these loci, printed by file, stream and kind and never by token: `G3-G2b-message-check-pass1.json stdout repo`; `G3-G2b-message-check-pass1.json invocation repo`; `G3-G2b-message-check-pass2.json notes repo`. Two shapes account for all of them. One is a column label that the live run of that check no longer prints, because the LABEL was reworded the moment this sweep caught it; the other is a hyphenated compound inside the very capture note that records the rewording, whose trailing hyphenated word carries it past the admitted exact string. Neither is admitted. Admitting the first would weaken the sweep for exactly the string it correctly caught, in order to tidy away the evidence that it worked; admitting the second would need a leading-segment rule, and this copy's whole method is exact strings. They stay residue under standing ruling F-08. No residue is a repository identity. Each seeded run left its own seeds unexplained (5, 15 and 14). The deliberate residue the Gate 2 copy discloses is a different one and does not arise here, because this gate ran no frozen corpus - a fact about the domain, not a loosened rule.
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
started_at: "2026-09-03T08:46:17Z"
ended_at: "2026-09-03T09:14:12Z"
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
  - name: closure-precondition-pull-request-tail
    command: "the scanner's own printed pattern, read out of its capture and not retyped, applied to the message of the commit that carries this record - the one commit the scan cannot cover because it runs first"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G2b-message-check.json"
  - name: ci-status
    command: "repository workflows, workflow files in the tree, and check runs on the pull-request head"
    result: none_configured
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G5-ci.json"
  - name: closed-set-sweep-explains-every-candidate
    command: "g3/checks-g3-closed-set-sweep.py over this gate's captures domain; every candidate classified by an explicit rule, residue 3"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-closed-set-sweep.json"
  - name: closed-set-sweep-falsified-three-ways
    command: "the same instrument over the retained Gate 1 seeds (residue 5, repository, node and issue limbs all firing), over the Gate 2 near-miss seed (residue 15), and over a new seed carrying a one-character near-miss for every fact this copy adds (residue 14)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-closed-set-sweep-falsify-near-miss.json"
  - name: record-sweep-over-this-records-final-bytes
    command: "the same instrument pointed at this file, after the bytes it sweeps were final"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-record-sweep.json"
  - name: record-validates-on-both-declared-halves
    command: "bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S5/g3/gate3.md --report-id explicit, on the Windows interpreter and on WSL"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-record-validation.json"
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
  - docs/evidence/gatebraid/P2-S5/g3/closing-keyword-scan.py
  - docs/evidence/gatebraid/P2-S5/g3/checks-g3-closed-set-sweep.py
  - docs/evidence/gatebraid/P2-S5/g3/render-gate3.py
  - docs/evidence/gatebraid/P2-S5/g3/falsification/SEED-closing-keyword-body.md
  - docs/evidence/gatebraid/P2-S5/g3/falsification/SEED-near-miss-gate3-classes.json
  - docs/evidence/gatebraid/P2-S5/g3/falsification/SEED-closing-keyword-body.md
notes: "PR https://github.com/MianliWang/gatebraid/pull/21. No merge SHA and no closure timestamp are recorded here - GitHub holds both natively (ADR-0017 section 2), and this file is written before the merge. The publication set is the reviewed tree at 5b586029344eb6df4a964c34baa1eb12e2916f6d (tree f696944947a342b6163bf4ad7d9137674830a2f7) plus the record-only evidence commits that follow it, every one inside docs/evidence/gatebraid/P2-S5/. CI is none-configured, a recorded finding rather than a pass. The Slice issue is referenced by plain reference and is closed at this gate's Exit by an explicit command, never by this pull request - closure is what releases native blocked-by dependents. Every figure in this record is derived from the row that measures it; four Gate 2 findings were a count or a status typed as a constant and later contradicted by its own row, and this record does not repeat that."
```
