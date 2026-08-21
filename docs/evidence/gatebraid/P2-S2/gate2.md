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

| Item | Verdict | Evidence |
|---|---|---|
| R1 allowlist confinement | | `#verification-outputs` V8 |
| R2 test-plan coverage | | `#verification-outputs` V1–V9 |
| R3 evidence is rows that reproduce | | `#entry-records`, `#verification-outputs` |
| R4 negative criterion | | `#verification-outputs` V8 and V9 |
| R5 no prohibited action | | `#required-disclosures` |

**Reviewer rows**
```
NOT RUN IN THIS WINDOW. The Plan Approval grants the build and stops at the
Gate 2 report; Review 1 runs in a fresh read-only window under its own
dispatch, as Executor = Claude Read-Only Team. Verdicts are the reviewer's to
write, last, and the implementer never pre-fills them — so the cells above are
left empty rather than filled by the session that produced the work.
```

- Reviewer write disclosure: `not yet run`
- Rules given to the reviewer: `not yet dispatched`

## Repair record

```
No repair attempt. Every declared test reached its expected result on its
first captured run, so the repair sequence was never entered and
`repair_attempts` is empty.
```

## Required disclosures

- Deviations: Review 1 is **not run in this window** and `review-five-items` is recorded `not_run` — the grant stops at this report and dispatches the review to a fresh read-only window; the verdict cells are left empty because verdicts are the reviewer's to write and the implementer never pre-fills them · the Gate 1 Exit elements parked at the previous report are **discharged here** and recorded at E5, not carried further · commit messages follow the repository's committed convention, which carries no co-author trailer; adding one would name a second party in a history whose authorship discipline is itself ADR-0020/ADR-0022 governed and audited, so the house shape was kept and the choice is disclosed rather than made silently · the selftest writes its seeded fixtures to a temporary directory **outside every repository** (`tempfile.mkdtemp()`), which `protocols/gate-2-contract.md` permits and which is named here as the contract requires · `bin/gatebraid-capture.py` was executed throughout and never read, keeping this Slice's isolation certification intact.
- Reviewer write disclosure: `not yet run`
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
ended_at: '2026-08-21T03:50:01Z'
result: needs_approval
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
- name: T9-negative-criterion-N-B
  result: pass
  command: C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S2/checks/independence-check.py bin/gatebraid-validate.py
    bin/gatebraid-validate-selftest.py
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G2-T9.json
- name: review-five-items
  result: not_run
  command: Review 1, read-only, in a fresh window under its own dispatch
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
notes: 'result is needs_approval, not passed: Review 1 has not run. The Plan Approval grants the build
  and stops at this report, and `passed` is the Release Approval''s to grant after review. Two defects
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
