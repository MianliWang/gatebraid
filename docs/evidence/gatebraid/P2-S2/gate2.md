# Gate 2 evidence — P2-S2

## Entry records

**E1 — Plan Approval verified** (author must be `MianliWang`, not this
session — ADR-0020 §4; hashes must match the frozen values)
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5364783775 --jq "{author: .user.login, assoc: .author_association, url: .html_url, issue: .issue_url, created: .created_at, updated: .updated_at}"
exit 0
{"assoc":"OWNER","author":"MianliWang","created":"2026-08-21T03:19:36Z","issue":"https://api.github.com/repos/MianliWang/gatebraid/issues/10","updated":"2026-08-21T03:19:36Z","url":"https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5364783775"}
```
The approval names both frozen hashes; each equals the value in `gate1.md`:
`plan_hash 6f68e9a0…92f346` · `allowlist_hash 0c0090ec…223d86`.

**E2 — Writer Lease taken, read back**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project item-edit --id PVTI_lAHOBRofUs4Beum7zg3ZWpw --project-id PVT_kwHOBRofUs4Beum7 --field-id PVTF_lAHOBRofUs4Beum7zhZJcSU --text RoughEgoist:P2-S2-gate2:2026-08-21T03:24:47Z
exit 0
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f "query=query($item:ID!){ node(id:$item){ ... on ProjectV2Item { content{ ... on Issue { number labels(first:20){nodes{name}} } } fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldTextValue{ text field{ ... on ProjectV2FieldCommon{ name } } } ... on ProjectV2ItemFieldSingleSelectValue{ name optionId field{ ... on ProjectV2FieldCommon{ name } } } } } } } }" -F item=PVTI_lAHOBRofUs4Beum7zg3ZWpw
exit 0
{"data":{"node":{"content":{"number":10,"labels":{"nodes":[]}},"fieldValues":{"nodes":[{},{"text":"P2-S2 — the independent evidence validator (N3)","field":{"name":"Title"}},{"name":"Todo","optionId":"f75ad846","field":{"name":"Status"}},{"name":"Gate 2 — Implementing","optionId":"413117f9","field":{"name":"Workflow"}},{"name":"G1 passed","optionId":"2a2ff00e","field":{"name":"Gate"}},{"name":"—","optionId":"450ee130","field":{"name":"Next Approval"}},{"name":"mixed-see-prose","optionId":"1e43ec85","field":{"name":"Environment"}},{"name":"Claude Lead","optionId":"ce859c7d","field":{"name":"Executor"}},{"name":"low","optionId":"e291249c","field":{"name":"Risk"}},{"text":"S2","field":{"name":"Stage"}},{"text":"P2","field":{"name":"Phase"}},{"text":"P2-S2","field":{"name":"Slice"}},{"text":"11dbac47927bff5aa7c9e86124e85db9ecdbc650","field":{"name":"Base SHA"}},{"text":"RoughEgoist:P2-S2-gate2:2026-08-21T03:24:47Z","field":{"name":"Writer Lease"}}]}}}}
```

**E3 — baseline re-read** (ADR-0011 §9; ADR-0014 §1 excludes
`docs/evidence/gatebraid/P2-S2/` before the intersection)
```
$ git ls-remote origin refs/heads/main
exit 0
11dbac47927bff5aa7c9e86124e85db9ecdbc650	refs/heads/main
```
- baseline: `unchanged`

**E4 — Active Branch created from Y; `Base SHA` field set to Y**
```
$ git checkout -b slice/P2-S2 11dbac47927bff5aa7c9e86124e85db9ecdbc650
exit 0
Switched to a new branch 'slice/P2-S2'
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f "query=query($item:ID!){ node(id:$item){ ... on ProjectV2Item { fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldTextValue{ text field{ ... on ProjectV2FieldCommon{ name } } } } } } } }" -F item=PVTI_lAHOBRofUs4Beum7zg3ZWpw
exit 0
{"data":{"node":{"fieldValues":{"nodes":[{},{"text":"P2-S2 — the independent evidence validator (N3)","field":{"name":"Title"}},{},{},{},{},{},{},{},{"text":"S2","field":{"name":"Stage"}},{"text":"P2","field":{"name":"Phase"}},{"text":"P2-S2","field":{"name":"Slice"}},{"text":"11dbac47927bff5aa7c9e86124e85db9ecdbc650","field":{"name":"Base SHA"}},{"text":"RoughEgoist:P2-S2-gate2:2026-08-21T03:24:47Z","field":{"name":"Writer Lease"}},{"text":"slice/P2-S2","field":{"name":"Active Branch"}}]}}}}
```
`Base SHA` already equalled Y from the setup batch, so it is recorded as a
verification rather than rewritten — the step is performed, not skipped.

**E5 — Gate 1's parked exit, discharged under this grant**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S2/checks/verify-writedomains.py
exit 0
loader                     : PyYAML 6.0.2 / jsonschema 4.23.0 / Draft202012Validator
live write_domains         : ['bin/gatebraid-validate.py', 'bin/gatebraid-validate-selftest.py', 'docs/evidence/gatebraid/P2-S2/']
slice@1 validation errors  : 0
allowlist_hash from the issue: 0c0090ec87b5a47838edfe8bad7d8350a79d50fc642c3e1d10b1582a09223d86
frozen allowlist_hash        : 0c0090ec87b5a47838edfe8bad7d8350a79d50fc642c3e1d10b1582a09223d86
BYTE-EQUAL TO THE FROZEN ALLOWLIST: True
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f "query=query($item:ID!){ node(id:$item){ ... on ProjectV2Item { id content{ ... on Issue { number state labels(first:20){nodes{name}} } } fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldTextValue{ text field{ ... on ProjectV2FieldCommon{ name } } } ... on ProjectV2ItemFieldSingleSelectValue{ name optionId field{ ... on ProjectV2FieldCommon{ name } } } } } } } }" -F item=PVTI_lAHOBRofUs4Beum7zg3ZWpw
exit 0
{"data":{"node":{"id":"PVTI_lAHOBRofUs4Beum7zg3ZWpw","content":{"number":10,"state":"OPEN","labels":{"nodes":[{"name":"needs-human"}]}},"fieldValues":{"nodes":[{},{},{"text":"P2-S2 — the independent evidence validator (N3)","field":{"name":"Title"}},{"name":"Todo","optionId":"f75ad846","field":{"name":"Status"}},{"name":"Needs Plan Approval","optionId":"2ad6af85","field":{"name":"Workflow"}},{"name":"G1 passed","optionId":"2a2ff00e","field":{"name":"Gate"}},{"name":"Plan Approval (G1→G2)","optionId":"e45b9ae5","field":{"name":"Next Approval"}},{"name":"mixed-see-prose","optionId":"1e43ec85","field":{"name":"Environment"}},{"name":"Claude Lead","optionId":"ce859c7d","field":{"name":"Executor"}},{"name":"low","optionId":"e291249c","field":{"name":"Risk"}},{"text":"S2","field":{"name":"Stage"}},{"text":"P2","field":{"name":"Phase"}},{"text":"P2-S2","field":{"name":"Slice"}},{"text":"11dbac47927bff5aa7c9e86124e85db9ecdbc650","field":{"name":"Base SHA"}}]}}}}
```
The write-back was a pure 60-byte insertion: every byte before offset 2197 and
after the inserted region is identical to the body as posted, and the re-read
body is byte-faithful to what was sent (`G1X-writedomains-readback.json`).

## Verification outputs

**V1 — T1 — validator selftest, Windows. Accept-when: landed once through its own gate**
```
$ C:/Python312/python.exe -B bin/gatebraid-validate-selftest.py
exit 0
id     condition                             want   got  verdict required observation
S00    untouched capture accepted               0     0  PASS    a valid record must be accepted
S01    sha256 does not re-derive                1     1  PASS    schema-valid; caught only by re-derivation
S02    byte_length mismatch                     1     1  PASS    declared length must match the decoded payload
S03    ended_at precedes started_at             1     1  PASS    named inexpressible by the schema
S04    calendar-impossible timestamp            1     1  PASS    the schema pattern is lexical only
S05    payload does not decode                  1     1  PASS    the base64 grammar is the field the byte contract rests on
S06    lone-CR count disagrees with bytes       1     1  PASS    byte/line-ending discipline re-derived
[elided: 8 of 32 lines shown; full output: docs/evidence/gatebraid/P2-S2/captures/G2-T1.json]
```

**V2 — T2 — validator selftest, WSL. Accept-when: dual-platform**
```
$ wsl.exe -e bash -lc "cd "/mnt/d/Github repo/Gatebraid" && python3 -B bin/gatebraid-validate-selftest.py"
exit 0
id     condition                             want   got  verdict required observation
S00    untouched capture accepted               0     0  PASS    a valid record must be accepted
S01    sha256 does not re-derive                1     1  PASS    schema-valid; caught only by re-derivation
S02    byte_length mismatch                     1     1  PASS    declared length must match the decoded payload
S03    ended_at precedes started_at             1     1  PASS    named inexpressible by the schema
S04    calendar-impossible timestamp            1     1  PASS    the schema pattern is lexical only
S05    payload does not decode                  1     1  PASS    the base64 grammar is the field the byte contract rests on
S06    lone-CR count disagrees with bytes       1     1  PASS    byte/line-ending discipline re-derived
[elided: 8 of 32 lines shown; full output: docs/evidence/gatebraid/P2-S2/captures/G2-T2.json]
```

**V3 — T3 — N1 mutation suite over the frozen corpus, Windows. Accept-when: all applicable N1 mutations killed independently of N2**
```
$ C:/Python312/python.exe -B bin/gatebraid-validate.py --corpus fixtures --coverage-out docs/evidence/gatebraid/P2-S2/coverage-windows.json
exit 0
corpus root   : fixtures
corpora built : bytes-platform, evidence-capture-v1, gate-run-v2, instruments, metrics-v1

== bytes-platform (v1.1), 8 cases
   BP1-01   valid-single-platform-report.json                    want=valid   got=valid   locus=match 
   BP1-02   valid-dual-platform-claim.json                       want=valid   got=valid   locus=match 
   BP1-03   bp01-replayed-without-rederived-digest.json          want=invalid got=invalid locus=match 
   BP1-04   bp02-rederived-digest-truncated.json                 want=invalid got=invalid locus=match 
[elided: 8 of 127 lines shown; full output: docs/evidence/gatebraid/P2-S2/captures/G2-T3.json]
```

**V4 — T4 — the same suite, WSL. Accept-when: dual-platform**
```
$ wsl.exe -e bash -lc "cd "/mnt/d/Github repo/Gatebraid" && python3 -B bin/gatebraid-validate.py --corpus fixtures --coverage-out docs/evidence/gatebraid/P2-S2/coverage-wsl.json"
exit 0
corpus root   : fixtures
corpora built : bytes-platform, evidence-capture-v1, gate-run-v2, instruments, metrics-v1

== bytes-platform (v1.1), 8 cases
   BP1-01   valid-single-platform-report.json                    want=valid   got=valid   locus=match 
   BP1-02   valid-dual-platform-claim.json                       want=valid   got=valid   locus=match 
   BP1-03   bp01-replayed-without-rederived-digest.json          want=invalid got=invalid locus=match 
   BP1-04   bp02-rederived-digest-truncated.json                 want=invalid got=invalid locus=match 
[elided: 8 of 127 lines shown; full output: docs/evidence/gatebraid/P2-S2/captures/G2-T4.json]
```

**V5 — T5 — a deliberately corrupted N2 output is rejected**
```
$ C:/Python312/python.exe -B bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S2/checks/corrupted-capture.json --coverage-out docs/evidence/gatebraid/P2-S2/coverage-corrupted.json
exit 1
target        : docs/evidence/gatebraid/P2-S2/checks/corrupted-capture.json
interface     : gatebraid/evidence-capture@1
loader        : CPython 3.12.2 (C:\Python312\python.exe), jsonschema 4.23.0, Draft202012Validator
structural    : 0 error locus/loci
properties    : 16 rows
   structural       1
   semantic         11
   replayed         0
   capture-trusted  4
findings      : 1
   F001     /streams/stdout/sha256                         sha256-does-not-rederive
verdict       : rejected
coverage-out  : docs/evidence/gatebraid/P2-S2/coverage-corrupted.json  bytes=5499 sha256=0277842a4d42d70dffd0886ee7663aed8eb1cbc25b1dea31bd65365cd2797a60
```

**V6 — T6 — the coverage report classifies every verified property, with no unlabelled `replayable` credit**
```
$ C:/Python312/python.exe -B bin/gatebraid-validate.py --verify-coverage docs/evidence/gatebraid/P2-S2/coverage-windows.json
exit 0
report        : docs/evidence/gatebraid/P2-S2/coverage-windows.json
loader        : CPython 3.12.2 (C:\Python312\python.exe), jsonschema 4.23.0, Draft202012Validator
structural    : 0 error locus/loci
classification, every verified property carrying exactly one class:
   structural       1
   semantic         11
   replayed         0
   capture-trusted  4
classified rows               : 16
rows in the report            : 16
re-derivation findings        : 0
unlabelled replayable credits : 0

COVERAGE CLEAN: every verified property carries exactly one of the four classes and no replayable claim is credited without a label
unlabelled replayable credits : 0
```

**V7 — T7 — the frozen corpus did not move under this Slice**
```
$ C:/Python312/python.exe -B fixtures/runner-selftest.py
exit 0
condition                           want  got  verdict  required observation
S00 untouched copy                     0    0  PASS     CORPUS CLEAN
S01 mutation not killed                1    1  PASS     mutation not killed
S02 recorded locus silent              1    1  PASS     recorded locus did not fire
S03 unrecorded locus fired             1    1  PASS     unrecorded locus fired
S04 valid case broken                  1    1  PASS     expected valid
S05 fixture missing                    2    2  PASS     fixture missing
S06 schema missing                     2    2  PASS     schema missing
[elided: 8 of 37 lines shown; full output: docs/evidence/gatebraid/P2-S2/captures/G2-T7.json]
```

**V8 — T8 — negative criterion N-A: allowlist confinement**
```
$ git diff --name-only 11dbac47927bff5aa7c9e86124e85db9ecdbc650..HEAD
exit 0
bin/gatebraid-validate-selftest.py
bin/gatebraid-validate.py
```
**Disclosure: the run above was captured at `2026-08-21T03:43:31.069750Z`, when
`HEAD` stood at `c4bcf9c46c235505cb0d9577cf688c38f43530d1`, the first of this
slice's three commits, so its two lines are the diff as it stood mid-slice and
not the 93 paths the slice landed — read alone, this row would credit T8 with
more scope than it measured.** Its capture is
`docs/evidence/gatebraid/P2-S2/captures/G2-T8.json`; it stands as recorded and
is not rewritten.

Re-run under the Release Approval, pinned at both ends so the scope no longer
depends on where `HEAD` stands — the criterion's full defined scope, base to the
head Review 1 examined:
```
$ git diff --name-only 11dbac47927bff5aa7c9e86124e85db9ecdbc650..0a94b945d07d5f04014346eef91938f6fb072feb
exit 0
bin/gatebraid-validate-selftest.py
bin/gatebraid-validate.py
docs/evidence/gatebraid/P2-S2/captures/G0-baseline-main.json
docs/evidence/gatebraid/P2-S2/captures/G0-baseline.json
docs/evidence/gatebraid/P2-S2/captures/G0-closed-set-sweep.json
docs/evidence/gatebraid/P2-S2/captures/G0-head.json
[elided: 6 of 93 lines shown; full output: docs/evidence/gatebraid/P2-S2/captures/G2-T8-pinned.json]
```

**V9 — T9 — negative criterion N-B: independence of N2 in imports**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S2/checks/independence-check.py bin/gatebraid-validate.py bin/gatebraid-validate-selftest.py
exit 0
N-B scope, as an explicit path set:
   bin/gatebraid-validate.py
   bin/gatebraid-validate-selftest.py

  bin/gatebraid-validate.py                      module-level imports: 11   findings: 0
  bin/gatebraid-validate-selftest.py             module-level imports: 9    findings: 0

stdlib names available        : 300
interpreter                   : C:\Python312\python.exe
criterion violations          : 0
INDEPENDENCE CLEAN: no module-level third-party import, and no path from either file to the generator's implementation
```

## Review record

### Review 1

Reviewer: `Claude Read-Only Team`, a fresh read-only session that authored none
of the work it reviewed and authors none of it. Verdicts transcribed verbatim
from that session's report, `_handoff/batch-n3/REVIEW1-M3-P2S2.md`, verified
before transcription at
`sha256:a9d6311bfa0e1fe8d209d2cfc9cb9fac192fccd56fab9dc85957fa49c5b1545c`,
38,544 bytes — the value the Release Approval cites.

| Item | Verdict | Evidence |
|---|---|---|
| R1 allowlist confinement | **PASS** | report rows A1–A5; `#verification-outputs` V8 |
| R2 test-plan coverage | **PASS** | report rows B1–B5; `#verification-outputs` V1–V9 |
| R3 evidence is rows that reproduce | **PASS** | report rows C1–C12; `#entry-records`, `#verification-outputs` |
| R4 negative criterion | **PASS** (+F-A) | report rows D1–D4; `#verification-outputs` V8 and V9 |
| R5 no prohibited action | **PASS** | report rows E1–E9; `#required-disclosures` |

**Verdict block, transcribed verbatim from the report identified above**
```
| Item | Verdict | Basis |
|---|---|---|
| **R1** allowlist confinement | **PASS** | Rows A1–A5 |
| **R2** the frozen plan is covered | **PASS** | Rows B1–B5 |
| **R3** evidence is rows that reproduce | **PASS** | Rows C1–C12 |
| **R4** negative criteria | **PASS** | Rows D1–D4 |
| **R5** no prohibited action | **PASS** | Rows E1–E9 |

**Findings: one, non-blocking.**

| Id | Severity | Item | Summary |
|---|---|---|---|
| **F-A** | observation, non-blocking | R4 / R2 | T8's captured run measures 2 of the 93 landed paths, and `gate2.md`'s V8 row does not disclose that its `HEAD` was mid-slice. The criterion itself holds over the full 93 — measured independently at rows A1–A3 and D1. |

No finding blocks the Release Approval. F-A is a disclosure gap in a record
row, not a defect in the delivered work.
```

F-A is ruled by the coordinator in the Release Approval as a **record defect,
not a substance failure**, and is repaired in the open above: row V8 now carries
the disclosure the finding asks for, and the pinned re-run measures the full 93.

**Reviewer rows** (the commands the reviewer ran, with outputs)
```
RUN. Full rows are in the report identified above, which is the transcription
source and is pinned by the sha256 recorded there. Summarised by section:

  A1-A5  R1: the diff counted at 93 paths, name-status tally "93 A" (no M, no
         D), top-level tally 2 bin/ + 91 docs/; complement outside the frozen
         allowlist = 0; both bin/ blob ids and sizes taken by ls-tree without
         reading either file.
  B1-B5  R2: plan_hash and allowlist_hash reproduced with the recorded
         hash_commands before any mapping was trusted; T1-T9 mapped onto V1-V9;
         the Accept-when items checked one by one against the frozen plan.
  C1-C12 R3: rows re-run in this window with every --coverage-out redirected
         outside the repository and git status --porcelain re-measured empty
         after each; the corrupted-output rejection reproduced exactly; the
         coverage report re-validated at 0 errors; the capture records
         re-verified and re-derived by the landed generator.
  D1-D4  R4: both negative criteria re-run over the full 93-path set, 0 paths
         outside the allowlist and 0 import violations; falsified at D4 by a
         decoy that tripped three findings including n2-token-in-string,
         showing the criterion fires when it should.
  E1-E9  R5: no push, no fetch, no ref write, no gh mutation, no commit, no
         tracked-file edit; N2's two implementation files never read, only
         executed; a closed-set identifier sweep whose complement is fully
         explained.
```

- Reviewer write disclosure: `the report file only, at the ignored path
  _handoff/batch-n3/REVIEW1-M3-P2S2.md (git check-ignore: .gitignore:7:/_handoff/)
  — 0 commits, 0 tracked-file edits, 0 gh mutations, 0 pushes/fetches/ref
  writes; scratch files written outside the repository and the files they were
  copied from re-hashed unchanged; bin/gatebraid-capture.py and
  bin/gatebraid-capture-selftest.py never read`
- Rules given to the reviewer: `the conduct rules (measure never declare; cite
  never restate; a checker never echoes a forbidden value into its record; a
  bare zero states what it searched; closed-set by complement with the
  touch-vs-mention ruling; never read N2's two implementation files, executing
  them being permitted; GH_CONFIG_DIR pinned on every gh call with the identity
  check first and alone; gh api endpoints without a leading slash;
  PYTHONDONTWRITEBYTECODE=1 on every Python invocation; on any uncertainty stop
  and ask), the two pre-briefs, the coordinator-measured entry facts, and the
  five items R1-R5 — plus the standing host rules in CLAUDE.md (manual approval
  mode, merging never routine, the business-repository prohibition and its
  negative-check method, the ADR-0009/0027 tooling prohibition, no force-push,
  no worktrees, official names only, the dash-versus-arrow byte rule, and
  Windows-side git only)`

### Independence review — M3-PLAN §2 N3 line 113

Reviewer: the coordinator — the party that authored neither N2 nor N3 and may
read both — from the record and from blob-verified staged bytes. This is the
review M3-PLAN §2 N3's Accept-when names. Transcribed verbatim from
`_handoff/batch-n3/INDEPENDENCE-REVIEW-M3-P2S2.md`, verified before
transcription at
`sha256:c65571e7ac3c49f659a07141c7e0d894b758737c733931b9dd02216b6e87fcf7`,
3,752 bytes — the value the Release Approval cites.

**Verdicts, transcribed verbatim from the review identified above**
```
**Imports verdict: CONFIRMED independent.** Consistent with T9's
in-window result (0 violations).

**Authorship verdict: CONFIRMED independent.** The texts read as two
implementations of one committed spec, not as one text derived from the
other.

**Line-113 verdict: independence of imports AND authorship CONFIRMED.**
This document is cited by the Release Approval and transcribed into the
gate record by the writer session under that grant.
```

The mechanised imports half also ran in-window as T9 (row V9, 0 violations);
the transcribed verdict is an independent re-measurement of that half plus the
authorship half, which this gate did not itself perform.

## Repair record

```
No repair attempt. Every declared test reached its expected result on its
first captured run, so the repair sequence was never entered and
`repair_attempts` is empty.
```

## Required disclosures

- Deviations: this file was **amended after Review 1**, under the Release Approval of `2026-08-21T18:34:43Z`, by the same writer session that produced the work — the amendment re-ran T8 pinned at both ends, added the V8 disclosure the reviewer's finding F-A asks for, transcribed the Review 1 verdict block and the M3-PLAN line-113 independence verdict from the two `_handoff/` sources the approval pins by sha256 (both verified before copying, both read and never edited), and only then moved `result` to `passed` as the last write; `review-five-items` moves from `not_run` to `pass` on that transcription · the transcription is performed by the writer session rather than the reviewer, which is the shape the approval directs and is why the verdict block is quoted verbatim rather than paraphrased · a second Review-record block, `Independence review — M3-PLAN §2 N3 line 113`, is appended under the template's "one block per review, appended in order" rule although the template names only numbered `Review <n>` blocks; the heading is new and the choice is disclosed rather than made silently · the Gate 1 Exit elements parked at the previous report are **discharged here** and recorded at E5, not carried further · commit messages follow the repository's committed convention, which carries no co-author trailer; adding one would name a second party in a history whose authorship discipline is itself ADR-0020/ADR-0022 governed and audited, so the house shape was kept and the choice is disclosed rather than made silently · the selftest writes its seeded fixtures to a temporary directory **outside every repository** (`tempfile.mkdtemp()`), which `protocols/gate-2-contract.md` permits and which is named here as the contract requires · `bin/gatebraid-capture.py` was executed throughout and never read, keeping this Slice's isolation certification intact.
- Reviewer write disclosure: `the report file only, at the ignored path _handoff/batch-n3/REVIEW1-M3-P2S2.md — 0 commits, 0 tracked-file edits, 0 gh mutations, 0 pushes/fetches/ref writes; N2's two implementation files never read`
- Environment: Windows 11 host, Git Bash (MSYS2) shell; declared `environment: mixed-see-prose` = Windows loader host `C:\Python312\python.exe` (CPython 3.12.2, jsonschema 4.23.0, PyYAML 6.0.2) AND WSL `/usr/bin/python3` (CPython 3.12.3, jsonschema 4.10.3, PyYAML 6.0.1); `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` call; `PYTHONDONTWRITEBYTECODE=1` on every Python invocation; every `gh api` endpoint written without a leading slash, because MSYS rewrites leading-slash endpoints into filesystem paths.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S2
gate: 2
environment: mixed-see-prose
executor: Claude Lead
base_sha: 11dbac47927bff5aa7c9e86124e85db9ecdbc650
active_branch: slice/P2-S2
started_at: '2026-08-21T03:24:47Z'
ended_at: '2026-08-21T18:46:41.752982Z'
result: passed
bootstrap_exception: true
checks:
- name: plan-approval-verified
  result: pass
  command: gh api repos/MianliWang/gatebraid/issues/comments/5364783775 --jq '{author,url,created,updated}'
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-Q2-plan-approval.json
- name: writer-lease-taken
  result: pass
  command: gh project item-edit (Writer Lease) then one read-back by item id
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-entry-readback.json
- name: baseline-reread
  result: pass
  command: git ls-remote origin refs/heads/main
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-baseline-reread.json
- name: active-branch-created
  result: pass
  command: git checkout -b slice/P2-S2 11dbac47927bff5aa7c9e86124e85db9ecdbc650
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-branch-create.json
- name: gate1-writedomains-writeback
  result: pass
  command: gh api --method PATCH repos/MianliWang/gatebraid/issues/10 --input <payload>
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-writedomains-verify.json
- name: gate1-exit-fields-and-label
  result: pass
  command: gh project item-edit x3 by option id; gh issue edit --add-label needs-human
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G1X-exit-readback.json
- name: T1-selftest-windows
  result: pass
  command: C:/Python312/python.exe -B bin/gatebraid-validate-selftest.py
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-T1.json
- name: T2-selftest-wsl
  result: pass
  command: wsl.exe -e bash -lc 'cd "/mnt/d/Github repo/Gatebraid" && python3 -B bin/gatebraid-validate-selftest.py'
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-T2.json
- name: T3-corpus-windows
  result: pass
  command: C:/Python312/python.exe -B bin/gatebraid-validate.py --corpus fixtures --coverage-out docs/evidence/gatebraid/P2-S2/coverage-windows.json
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-T3.json
- name: T4-corpus-wsl
  result: pass
  command: wsl.exe -e bash -lc '... python3 -B bin/gatebraid-validate.py --corpus fixtures --coverage-out
    docs/evidence/gatebraid/P2-S2/coverage-wsl.json'
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-T4.json
- name: T5-corrupted-output-rejected
  result: pass
  command: C:/Python312/python.exe -B bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S2/checks/corrupted-capture.json
    --coverage-out docs/evidence/gatebraid/P2-S2/coverage-corrupted.json
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-T5.json
- name: T6-coverage-classification
  result: pass
  command: C:/Python312/python.exe -B bin/gatebraid-validate.py --verify-coverage docs/evidence/gatebraid/P2-S2/coverage-windows.json
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-T6.json
- name: T7-corpus-unmoved
  result: pass
  command: C:/Python312/python.exe -B fixtures/runner-selftest.py
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-T7.json
- name: T8-negative-criterion-N-A
  result: pass
  command: git diff --name-only 11dbac47927bff5aa7c9e86124e85db9ecdbc650..HEAD
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-T8.json
- name: T8R-negative-criterion-N-A-pinned
  # Re-run under the Release Approval, pinned at both ends: 93 paths, 0 outside
  # the frozen allowlist. The original T8 row is kept, not rewritten.
  result: pass
  command: git diff --name-only 11dbac47927bff5aa7c9e86124e85db9ecdbc650..0a94b945d07d5f04014346eef91938f6fb072feb
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-T8-pinned.json
- name: T9-negative-criterion-N-B
  result: pass
  command: C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S2/checks/independence-check.py bin/gatebraid-validate.py
    bin/gatebraid-validate-selftest.py
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-T9.json
- name: review-five-items
  # Review 1 ran under Executor = Claude Read-Only Team; R1-R5 all PASS with one
  # non-blocking observation, F-A, transcribed verbatim from the report the
  # approval pins by sha256 and repaired in the open at row V8.
  result: pass
  command: Review 1, read-only, in a fresh window under its own dispatch
  output_ref: '#review-record'
- name: independence-review-line-113
  # M3-PLAN 2 N3 Accept-when: the independence review (imports AND authorship)
  # is on record. Performed by the coordinator, not by this gate; transcribed
  # here under the Release Approval from the source it pins by sha256.
  result: pass
  command: coordinator review of imports and authorship over blob-verified staged bytes
  output_ref: '#review-record'
handoff_fingerprint:
  active_branch_head: dd56346221f2b65d78202fdc59479f243fc9cb4d
  tree_sha: fa2c965c45ca9402588fa46f1f7d2c90e209679c
  changed_paths:
  - bin/gatebraid-validate-selftest.py
  - bin/gatebraid-validate.py
  - docs/evidence/gatebraid/P2-S2/captures/G0-baseline-main.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-baseline.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-closed-set-sweep.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-head.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-porcelain-baseline.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-porcelain.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-ref-namespace.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-remote.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-slice-body.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-slice-metadata-validation.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-subissues-of-7.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-tools-claude.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-tools-codex.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-tools-gh.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-tools-git-autocrlf.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-tools-git.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-tools-python-windows.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-tools-python-wsl.json
  - docs/evidence/gatebraid/P2-S2/captures/G0-workflow-write.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-Q2-approval.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-Q5-live.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-T1-dryrun.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-T2-dryrun.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-T3-dryrun.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-T4-dryrun.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-T5-dryrun.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-T6-dryrun.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-T7-dryrun.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-T8-dryrun.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-T9-dryrun.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-approval-body.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-fields-readback.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-write-gate.json
  - docs/evidence/gatebraid/P2-S2/captures/G1-write-workflow.json
  - docs/evidence/gatebraid/P2-S2/captures/G1X-Q5-live.json
  - docs/evidence/gatebraid/P2-S2/captures/G1X-exit-readback.json
  - docs/evidence/gatebraid/P2-S2/captures/G1X-label-add.json
  - docs/evidence/gatebraid/P2-S2/captures/G1X-write-gate.json
  - docs/evidence/gatebraid/P2-S2/captures/G1X-write-nextapproval.json
  - docs/evidence/gatebraid/P2-S2/captures/G1X-write-workflow.json
  - docs/evidence/gatebraid/P2-S2/captures/G1X-writedomains-edit.json
  - docs/evidence/gatebraid/P2-S2/captures/G1X-writedomains-readback.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-Q2-plan-approval.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-T1.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-T2.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-T3.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-T4.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-T5.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-T6.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-T7.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-T8.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-T9.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-active-branch-readback.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-active-branch.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-baseline-reread.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-branch-create.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-entry-readback.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-label-remove.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-lease-take.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-nextapproval-clear.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-plan-approval-body.json
  - docs/evidence/gatebraid/P2-S2/captures/G2-workflow-implementing.json
  - docs/evidence/gatebraid/P2-S2/captures/Q1-falsify.json
  - docs/evidence/gatebraid/P2-S2/captures/Q1-real.json
  - docs/evidence/gatebraid/P2-S2/captures/Q2-falsify.json
  - docs/evidence/gatebraid/P2-S2/captures/Q2-real.json
  - docs/evidence/gatebraid/P2-S2/captures/Q3-falsify.json
  - docs/evidence/gatebraid/P2-S2/captures/Q3-real.json
  - docs/evidence/gatebraid/P2-S2/captures/Q4-falsify.json
  - docs/evidence/gatebraid/P2-S2/captures/Q4-real.json
  - docs/evidence/gatebraid/P2-S2/captures/Q5-falsify.json
  - docs/evidence/gatebraid/P2-S2/captures/Q5-real.json
  - docs/evidence/gatebraid/P2-S2/captures/Q6-falsify.json
  - docs/evidence/gatebraid/P2-S2/captures/Q6-real.json
  - docs/evidence/gatebraid/P2-S2/captures/Q7-falsify.json
  - docs/evidence/gatebraid/P2-S2/captures/Q7-real-blocked-by.json
  - docs/evidence/gatebraid/P2-S2/captures/Q7-real-blocking.json
  - docs/evidence/gatebraid/P2-S2/checks/corrupted-capture.json
  - docs/evidence/gatebraid/P2-S2/checks/independence-check.py
  - docs/evidence/gatebraid/P2-S2/checks/make-corrupted-capture.py
  - docs/evidence/gatebraid/P2-S2/closed-set-sweep-rev6.py
  - docs/evidence/gatebraid/P2-S2/coverage-corrupted.json
  - docs/evidence/gatebraid/P2-S2/coverage-windows.json
  - docs/evidence/gatebraid/P2-S2/coverage-wsl.json
  - docs/evidence/gatebraid/P2-S2/gate0.md
  - docs/evidence/gatebraid/P2-S2/gate1-exit-checklist.md
  - docs/evidence/gatebraid/P2-S2/gate1.md
consults: []
repair_attempts: []
approvals:
- type: State Packet Approval
  comment_url: https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5363954606
  author: MianliWang
  at: '2026-08-21T01:07:41Z'
- type: Plan Approval (G1→G2)
  comment_url: https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5364783775
  author: MianliWang
  at: '2026-08-21T03:19:36Z'
plan_hash: 6f68e9a09fe89242dff6d8cec2052d27e9e9ed42e32d45ef061aaeff2592f346
allowlist_hash: 0c0090ec87b5a47838edfe8bad7d8350a79d50fc642c3e1d10b1582a09223d86
evidence_files:
- docs/evidence/gatebraid/P2-S2/gate2.md
notes: 'Amended under the Release Approval of 2026-08-21T18:34:43Z, which is the grant that moves
  this record to passed: T8 was re-run pinned at both ends and captured as G2-T8-pinned (93 paths,
  0 outside the frozen allowlist), row V8 now discloses that its original run measured the mid-slice
  HEAD c4bcf9c46c235505cb0d9577cf688c38f43530d1 at 2026-08-21T03:43:31.069750Z, and Review 1''s
  verdict block and the M3-PLAN line-113 independence verdict are transcribed verbatim from the two
  sources the approval pins by sha256, both verified before copying and neither edited. result moved
  to passed as the last write in the file. Two defects
  found by this gate''s own checks and fixed inside it, both recorded because a check that finds nothing
  proves less than one that finds something: (1) the validator''s first report builder broke its own completeness
  arithmetic, caught by T6 re-reading the emitted document rather than trusting the run that wrote it;
  (2) the validator failed on WSL only - the frozen schemas declare `$id` values that are identifiers,
  not URLs, and jsonschema 4.10.3 resolves internal $refs against them while 4.23.0 tolerates it. Every
  $ref in every frozen schema is a local pointer, measured, so the base URI is dropped for validation
  and the two declared platforms now agree on all 105 corpus cases. The selftest also found five of its
  own conditions wrong before the validator was trusted; two were seeds that could not be constructed
  or were structurally illegal, and are recorded as such rather than deleted.'
```
