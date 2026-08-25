# Gate 2 evidence — P2-S4

## Entry records

**E1 — Plan Approval verified (author must be `MianliWang`, not this session — ADR-0020 §4; hashes must match the frozen values)**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5394791863 --jq '{author: .user.login, url: .html_url, created: .created_at, updated: .updated_at, association: .author_association}'
{"association":"OWNER","author":"MianliWang","created":"2026-08-24T11:51:54Z","updated":"2026-08-24T11:51:54Z","url":"https://github.com/MianliWang/gatebraid/issues/14#issuecomment-5394791863"}
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login
mianliwang492-source
(exit 0)
```

**E1b — Writer Assignment verified (the operator ruling that opens Gate 2 in this session — its clause 2 amends the Plan Approval's §5 window clause)**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5395086921 --jq '{author: .user.login, url: .html_url, created: .created_at, updated: .updated_at, association: .author_association}'
{"association":"OWNER","author":"MianliWang","created":"2026-08-24T12:19:15Z","updated":"2026-08-24T12:19:15Z","url":"https://github.com/MianliWang/gatebraid/issues/14#issuecomment-5395086921"}
(exit 0)
```

- Approval author `MianliWang`, executor identity `mianliwang492-source`: the approval was not written by the session it authorises.
- `created_at` equals `updated_at` on both comments, so the grant that was posted is the grant that was read.
- Both frozen hashes appear in the Plan Approval body — `plan_hash` `cb577dbf7fd1c0443b5e7ffbb94aacd7ada64385230afb6faa498815a4828913` and `allowlist_hash` `feb6d9c8ffbbaa08242d68e64db7b13b3f080aaae3667f01d7d22bdb0c061655`.
- Writer-role certification (Writer Assignment clause 3): this session held no prior role on Slice P2-S4 — it authored neither Gate 0 nor Gate 1 — and is not the Review session.

**E2 — Writer Lease taken, and the entry field writes, each by option id**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project item-edit --id PVTI_lAHOBRofUs4Beum7zg3ogLM --project-id PVT_kwHOBRofUs4Beum7 --field-id PVTSSF_lAHOBRofUs4Beum7zhZJcC8 --single-select-option-id 450ee130
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh issue edit 14 --repo MianliWang/gatebraid --remove-label needs-human
https://github.com/MianliWang/gatebraid/issues/14
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project item-edit --id PVTI_lAHOBRofUs4Beum7zg3ogLM --project-id PVT_kwHOBRofUs4Beum7 --field-id PVTF_lAHOBRofUs4Beum7zhZJcSU --text RoughEgoist:p2s4-gate2-claude-lead:2026-08-24T12:21:53Z
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project item-edit --id PVTI_lAHOBRofUs4Beum7zg3ogLM --project-id PVT_kwHOBRofUs4Beum7 --field-id PVTSSF_lAHOBRofUs4Beum7zhZGqt0 --single-select-option-id 413117f9
(exit 0)
```

**E3 — baseline re-read (ADR-0011 §9; ADR-0014 §1 excludes `docs/evidence/gatebraid/P2-S4/` before the intersection)**
```
$ git ls-remote origin refs/heads/main
df666070ead7fa21bc72b6c99d2644923b37e787	refs/heads/main
(exit 0)
```

- X, the plan baseline recorded in `gate0.md`: `df666070ead7fa21bc72b6c99d2644923b37e787`
- Y, the head of the base branch at entry: `df666070ead7fa21bc72b6c99d2644923b37e787`
- baseline: `unchanged`

**E4 — Active Branch created from Y; `Base SHA` field set to Y**
```
$ git checkout -b slice/P2-S4 df666070ead7fa21bc72b6c99d2644923b37e787

Switched to a new branch 'slice/P2-S4'
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project item-edit --id PVTI_lAHOBRofUs4Beum7zg3ogLM --project-id PVT_kwHOBRofUs4Beum7 --field-id PVTF_lAHOBRofUs4Beum7zhZJcQM --text slice/P2-S4
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project item-edit --id PVTI_lAHOBRofUs4Beum7zg3ogLM --project-id PVT_kwHOBRofUs4Beum7 --field-id PVTF_lAHOBRofUs4Beum7zhZJcPU --text df666070ead7fa21bc72b6c99d2644923b37e787
(exit 0)
```

**E5 — every entry field read back, by option id, with the issue's labels**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query($item:ID!){ node(id:$item){ ... on ProjectV2Item { content{ ... on Issue { number state labels(first:20){ nodes{ name } } } } fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldTextValue{ text field{ ... on ProjectV2FieldCommon{ name } } } ... on ProjectV2ItemFieldSingleSelectValue{ name optionId field{ ... on ProjectV2FieldCommon{ name } } } } } } } }' -F item=PVTI_lAHOBRofUs4Beum7zg3ogLM
{"data":{"node":{"content":{"number":14,"state":"OPEN","labels":{"nodes":[]}},"fieldValues":{"nodes":[{},{"text":"P2-S4 — O0 snapshot/frontier hardening: the fail-closed pair","field":{"name":"Title"}},{"name":"Todo","optionId":"f75ad846","field":{"name":"Status"}},{"name":"Gate 2 — Implementing","optionId":"413117f9","field":{"name":"Workflow"}},{"name":"G1 passed","optionId":"2a2ff00e","field":{"name":"Gate"}},{"name":"—","optionId":"450ee130","field":{"name":"Next Approval"}},{"name":"mixed-see-prose","optionId":"1e43ec85","field":{"name":"Environment"}},{"name":"Claude Lead","optionId":"ce859c7d","field":{"name":"Executor"}},{"name":"low","optionId":"e291249c","field":{"name":"Risk"}},{"text":"S2","field":{"name":"Stage"}},{"text":"P2","field":{"name":"Phase"}},{"text":"P2-S4","field":{"name":"Slice"}},{"text":"df666070ead7fa21bc72b6c99d2644923b37e787","field":{"name":"Base SHA"}},{"text":"2026-08-24T09:54:19Z Gate 1 passed; record docs/evidence/gatebraid/P2-S4/gate1.md sha256 2a3e8ee3991bb7686459e2c8dd4f18d6293e512b69c0c0a75466d045187e4be3 (working file, committed at Gate 2); plan_hash cb577dbf7fd1c0443b5e7ffbb94aacd7ada64385230afb6faa498815a4828913; allowlist_hash feb6d9c8ffbbaa08242d68e64db7b13b3f080aaae3667f01d7d22bdb0c061655; handoff comment 5393577673; needs-human ON; Plan Approval is the only door to Gate 2, which does not open on this grant.","field":{"name":"Last Checkpoint"}},{"text":"RoughEgoist:p2s4-gate2-claude-lead:2026-08-24T12:21:53Z","field":{"name":"Writer Lease"}},{"text":"slice/P2-S4","field":{"name":"Active Branch"}}]}}}}
(exit 0)
```

## Verification outputs

**V1 — D1a · T1 producer selftest, Windows half (acceptance 4: fail-closed per class; the seven P0-1 classes each carry a seeded condition)**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-snapshot-selftest.py
S31    P0-2 stdout carries the document and nothing else              True          True          PASS    the summary goes to stderr so the byte contract stays clean
S32    a document that fails self-validation is not emitted           1             1             PASS    emitting a malformed snapshot is worse than emitting none
S33    and nothing was written to the output path                     False         False         PASS    a partial file on disk would be read by the next consumer
S34    an absent transcript is a usage error                          2             2             PASS    input failure must not be reported as a degraded read
S35    a nonsense page cap is a usage error                           2             2             PASS    a cap of zero would make every read bounded and look like P0-3
S36    an absent schema is a usage error, never a pass                2             2             PASS    a tool that cannot self-validate must not emit
S37    a page naming no exit status is not read as success            3             3             PASS    defaulting an absent exit to 0 is an implicit success assumption on a verdict-relevant path; N2 found it here

scratch directory             : outside every repository (tempfile.mkdtemp)
tool under test               : D:\Github repo\Gatebraid\bin\gatebraid-snapshot.py
interpreter                   : C:\Python312\python.exe
network reads performed       : 0 (every seed served by the replay transport)
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
[... shown 14 of 45 lines (tail); full output: docs/evidence/gatebraid/P2-S4/g2/G2-D1a.json]
(exit 0)
```

**V2 — D1b · T1 producer selftest, WSL half (acceptance 3: the declared platforms)**
```
$ wsl -e bash -lc 'cd '\''/mnt/d/Github repo/Gatebraid'\'' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-snapshot-selftest.py'
S31    P0-2 stdout carries the document and nothing else              True          True          PASS    the summary goes to stderr so the byte contract stays clean
S32    a document that fails self-validation is not emitted           1             1             PASS    emitting a malformed snapshot is worse than emitting none
S33    and nothing was written to the output path                     False         False         PASS    a partial file on disk would be read by the next consumer
S34    an absent transcript is a usage error                          2             2             PASS    input failure must not be reported as a degraded read
S35    a nonsense page cap is a usage error                           2             2             PASS    a cap of zero would make every read bounded and look like P0-3
S36    an absent schema is a usage error, never a pass                2             2             PASS    a tool that cannot self-validate must not emit
S37    a page naming no exit status is not read as success            3             3             PASS    defaulting an absent exit to 0 is an implicit success assumption on a verdict-relevant path; N2 found it here

scratch directory             : outside every repository (tempfile.mkdtemp)
tool under test               : /mnt/d/Github repo/Gatebraid/bin/gatebraid-snapshot.py
interpreter                   : /usr/bin/python3
network reads performed       : 0 (every seed served by the replay transport)
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
[... shown 14 of 45 lines (tail); full output: docs/evidence/gatebraid/P2-S4/g2/G2-D1b.json]
(exit 0)
```

**V3 — D2a · T2 consumer selftest, Windows half (acceptance 4: P0-4's closed enumerations and both dependency directions)**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-frontier-selftest.py
F24    P0-2 a non-UTF-8 document is refused, not repaired       1             1             PASS    errors=replace here would manufacture the very corruption the contract detects
F25    P0-2 the report reaches stdout as UTF-8 bytes            True          True          PASS    a text-layer write under a cp936 console corrupts this exact mark
F26    P0-2 stdout carries the report and nothing else          True          True          PASS    the summary goes to stderr so the byte contract stays clean
F27    a document that is not JSON is refused                   1             1             PASS    a broken input must not become a verdict
F28    an absent document is a usage error, not a refusal       2             2             PASS    the caller must tell its own mistake from a measurement
F29    an absent schema is a usage error, never a pass          2             2             PASS    a tool that cannot validate must not emit a verdict

scratch directory             : outside every repository (tempfile.mkdtemp)
tool under test               : D:\Github repo\Gatebraid\bin\gatebraid-frontier.py
interpreter                   : C:\Python312\python.exe
seeds derived from            : D:\Github repo\Gatebraid\fixtures\state-pipeline\valid-canonical-snapshot.json
network reads performed       : 0
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
[... shown 14 of 38 lines (tail); full output: docs/evidence/gatebraid/P2-S4/g2/G2-D2a.json]
(exit 0)
```

**V4 — D2b · T2 consumer selftest, WSL half**
```
$ wsl -e bash -lc 'cd '\''/mnt/d/Github repo/Gatebraid'\'' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-frontier-selftest.py'
F24    P0-2 a non-UTF-8 document is refused, not repaired       1             1             PASS    errors=replace here would manufacture the very corruption the contract detects
F25    P0-2 the report reaches stdout as UTF-8 bytes            True          True          PASS    a text-layer write under a cp936 console corrupts this exact mark
F26    P0-2 stdout carries the report and nothing else          True          True          PASS    the summary goes to stderr so the byte contract stays clean
F27    a document that is not JSON is refused                   1             1             PASS    a broken input must not become a verdict
F28    an absent document is a usage error, not a refusal       2             2             PASS    the caller must tell its own mistake from a measurement
F29    an absent schema is a usage error, never a pass          2             2             PASS    a tool that cannot validate must not emit a verdict

scratch directory             : outside every repository (tempfile.mkdtemp)
tool under test               : /mnt/d/Github repo/Gatebraid/bin/gatebraid-frontier.py
interpreter                   : /usr/bin/python3
seeds derived from            : /mnt/d/Github repo/Gatebraid/fixtures/state-pipeline/valid-canonical-snapshot.json
network reads performed       : 0
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
[... shown 14 of 38 lines (tail); full output: docs/evidence/gatebraid/P2-S4/g2/G2-D2b.json]
(exit 0)
```

**V5 — D3a · induced-failure matrix, Windows half (acceptance 3: `undecidable` demonstrably produced by each induced failure)**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-o0-acceptance.py --induced-failures --out docs/evidence/gatebraid/P2-S4/acceptance/induced.json
case              clause                          required           observed           verdict
I-P0-1-auth       P0-1 auth_failure               undecidable        undecidable        PASS
I-P0-1-perm       P0-1 permission_failure         undecidable        undecidable        PASS
I-P0-1-rate       P0-1 rate_limited               undecidable        undecidable        PASS
I-P0-1-net        P0-1 network_error              undecidable        undecidable        PASS
I-P0-1-server     P0-1 server_error               undecidable        undecidable        PASS
I-P0-1-parse      P0-1 parse_error                undecidable        undecidable        PASS
I-P0-1-endpoint   P0-1 unexpected_endpoint        undecidable        undecidable        PASS
I-P0-3-cap        P0-3 page cap                   undecidable        undecidable        PASS
I-P0-4-state      P0-4 unknown issue state        undecidable        undecidable        PASS
I-P0-4-workflow   P0-4 unknown workflow           undecidable        undecidable        PASS
I-P0-4-crosscheck P0-4 cross-check mismatch       undecidable        undecidable        PASS
I-P0-4-soft       P0-4 soft dependency not parsed undecidable        undecidable        PASS

mode                          : induced-failures
harness                       : gatebraid-o0-acceptance 1.0.0
interpreter                   : C:\Python312\python.exe
network reads performed       : 0
cases declared                : 12
cases meeting required outcome: 12
classes reported unexercised  : 0
cases failing                 : 0
induced classes carrying undecidable : 12 / 12

ACCEPTANCE CLEAN: every declared case met its required outcome
out                           : docs/evidence/gatebraid/P2-S4/acceptance/induced.json
(exit 0)
```

**V6 — D3b · induced-failure matrix, WSL half**
```
$ wsl -e bash -lc 'cd '\''/mnt/d/Github repo/Gatebraid'\'' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-o0-acceptance.py --induced-failures --out docs/evidence/gatebraid/P2-S4/acceptance/induced.json'
I-P0-4-soft       P0-4 soft dependency not parsed undecidable        undecidable        PASS

mode                          : induced-failures
harness                       : gatebraid-o0-acceptance 1.0.0
interpreter                   : /usr/bin/python3
network reads performed       : 0
cases declared                : 12
cases meeting required outcome: 12
classes reported unexercised  : 0
cases failing                 : 0
induced classes carrying undecidable : 12 / 12

ACCEPTANCE CLEAN: every declared case met its required outcome
out                           : docs/evidence/gatebraid/P2-S4/acceptance/induced.json
[... shown 14 of 26 lines (tail); full output: docs/evidence/gatebraid/P2-S4/g2/G2-D3b.json]
(exit 0)
```

**V7 — D4 · dependency directions (acceptance 1 and 4: a NON-EMPTY relation in BOTH directions, `allOf[2]`'s positive arm, `allOf[3]`'s consequence half — the Gate 0 Q7 gap)**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-o0-acceptance.py --dependency-directions --out docs/evidence/gatebraid/P2-S4/acceptance/deps.json
case              clause                                           required           observed           verdict
D-both-consistent allOf[2] positive arm; both directions non-empty blocked            blocked            PASS
D-mismatch        allOf[3] consequence half                        undecidable        undecidable        PASS
D-not-performed   allOf[3] consequence half                        undecidable        undecidable        PASS
D-non-slice       allOf[1]                                         <no verdict>       <no verdict>       PASS
D-aborted         allOf[5]                                         blocked            blocked            PASS

mode                          : dependency-directions
harness                       : gatebraid-o0-acceptance 1.0.0
interpreter                   : C:\Python312\python.exe
network reads performed       : 0
cases declared                : 5
cases meeting required outcome: 5
classes reported unexercised  : 0
cases failing                 : 0
cases exercising a NON-EMPTY relation in BOTH directions : 4
allOf[2] positive arm complete (id, workflow and verdict) : 1

ACCEPTANCE CLEAN: every declared case met its required outcome
out                           : docs/evidence/gatebraid/P2-S4/acceptance/deps.json
(exit 0)
```

**V8 — D5 · the byte contract under a non-UTF-8 parent console (acceptance 4: P0-2 on non-ASCII content)**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-o0-acceptance.py --byte-contract --out docs/evidence/gatebraid/P2-S4/acceptance/bytes.json
case        clause              required           observed           verdict
B-premise   P0-2 premise        corrupted          corrupted          PASS
B-producer  P0-2 producing half byte-exact UTF-8   byte-exact UTF-8   PASS
B-consumer  P0-2 consuming half byte-exact UTF-8   byte-exact UTF-8   PASS
B-roundtrip P0-2 round trip     identical          identical          PASS

mode                          : byte-contract
harness                       : gatebraid-o0-acceptance 1.0.0
interpreter                   : C:\Python312\python.exe
network reads performed       : 0
cases declared                : 4
cases meeting required outcome: 4
classes reported unexercised  : 0
cases failing                 : 0

ACCEPTANCE CLEAN: every declared case met its required outcome
out                           : docs/evidence/gatebraid/P2-S4/acceptance/bytes.json
(exit 0)
```

**V9 — D6a · the frozen corpus under the landed validator, Windows half (acceptance 3; loader named in the output)**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-validate.py --corpus fixtures
   SP1-15   sp11-one-direction-dependency-loss.json              want=invalid got=invalid locus=match 
   SP1-16   sp12-soft-dependency-silently-ignored.json           want=invalid got=invalid locus=match 
   SP1-17   sp13-aborted-item-presented-as-ready.json            want=invalid got=invalid locus=match 

loader                        : CPython 3.12.2 (C:\Python312\python.exe), jsonschema 4.23.0, Draft202012Validator
cases declared                : 122
cases reaching their recorded disposition and locus set : 122
unexpected dispositions       : 0
positive controls with semantic findings : 0

CORPUS CLEAN: every declared case reached its recorded disposition and locus set
unexpected dispositions       : 0
[... shown 12 of 145 lines (tail); full output: docs/evidence/gatebraid/P2-S4/g2/G2-D6a.json]
(exit 0)
```

**V10 — D6b · the same, WSL half**
```
$ wsl -e bash -lc 'cd '\''/mnt/d/Github repo/Gatebraid'\'' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-validate.py --corpus fixtures'
   SP1-15   sp11-one-direction-dependency-loss.json              want=invalid got=invalid locus=match 
   SP1-16   sp12-soft-dependency-silently-ignored.json           want=invalid got=invalid locus=match 
   SP1-17   sp13-aborted-item-presented-as-ready.json            want=invalid got=invalid locus=match 

loader                        : CPython 3.12.3 (/usr/bin/python3), jsonschema 4.10.3, Draft202012Validator
cases declared                : 122
cases reaching their recorded disposition and locus set : 122
unexpected dispositions       : 0
positive controls with semantic findings : 0

CORPUS CLEAN: every declared case reached its recorded disposition and locus set
unexpected dispositions       : 0
[... shown 12 of 145 lines (tail); full output: docs/evidence/gatebraid/P2-S4/g2/G2-D6b.json]
(exit 0)
```

**V11 — D7 · the frozen surface held unmoved (acceptance 2: the batch-pinned digest), at two of the plan's three named points — after the last implementation commit, and at Gate 2 exit; the third, before the first implementation commit, was missed and is disclosed**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B fixtures/runner-selftest.py
S21 digest sees run-corpus.py       moves  moves  PASS     digest must change when the file changes
S22 digest sees runner-selftest.py  moves  moves  PASS     digest must change when the file changes
S28 __pycache__ moves no digest     same  same  PASS     digest must ignore interpreter output

digest scope                  : bytes-platform, evidence-capture-v1, gate-run-v2, instruments, metrics-v1, state-pipeline, CORPORA.json, schema, run-corpus.py, runner-selftest.py, fixtures/ listing
digest before                 : 66051715f76cf52d881aa143d9267f932407dbf5b9c4e6be9f81395ec641ef8e
digest after                  : 66051715f76cf52d881aa143d9267f932407dbf5b9c4e6be9f81395ec641ef8e
seed-reachable surface UNMODIFIED: True
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
[... shown 10 of 37 lines (tail); full output: docs/evidence/gatebraid/P2-S4/g2/G2-D7.json]
(exit 0)
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B fixtures/runner-selftest.py
S21 digest sees run-corpus.py       moves  moves  PASS     digest must change when the file changes
S22 digest sees runner-selftest.py  moves  moves  PASS     digest must change when the file changes
S28 __pycache__ moves no digest     same  same  PASS     digest must ignore interpreter output

digest scope                  : bytes-platform, evidence-capture-v1, gate-run-v2, instruments, metrics-v1, state-pipeline, CORPORA.json, schema, run-corpus.py, runner-selftest.py, fixtures/ listing
digest before                 : 66051715f76cf52d881aa143d9267f932407dbf5b9c4e6be9f81395ec641ef8e
digest after                  : 66051715f76cf52d881aa143d9267f932407dbf5b9c4e6be9f81395ec641ef8e
seed-reachable surface UNMODIFIED: True
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
[... shown 10 of 37 lines (tail); full output: docs/evidence/gatebraid/P2-S4/g2/G2-D7-exit.json]
(exit 0)
```

**V12 — D8 · the freeze precedes the implementation in commit history (acceptance 2) — the reference is PINNED to the fingerprint commit at repair 1; it named `HEAD` before, which does not reproduce**
```
$ git merge-base --is-ancestor df666070ead7fa21bc72b6c99d2644923b37e787 50d08de65158faf23f1ae86aeebcde39e929c359
(exit 0)
```

**V13 — N1 · path scope: the diff touches nothing outside the frozen allowlist — PINNED to the fingerprint commit at repair 1, and it now reproduces the recorded 137 rather than moving with the tip**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/negative-criterion-N1.py df666070ead7fa21bc72b6c99d2644923b37e787 50d08de65158faf23f1ae86aeebcde39e929c359
range          : df666070ead7fa21bc72b6c99d2644923b37e787..50d08de65158faf23f1ae86aeebcde39e929c359
allowed prefixes:
   bin/
   docs/evidence/gatebraid/P2-S4/
changed paths  : 137
inside allowlist: 137
outside         : 0

N1 HOLDS: every changed path is inside the frozen allowlist
(exit 0)
```

**V14 — N2 · no fail-open on a verdict-relevant path (proxy, scope and matches printed; the scope statement names its false-NEGATIVE channels from repair 1)**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g2/negative-criterion-N2.py
criterion      : N2 - no fail-open on a verdict-relevant path
pattern proxied: a failure silently becoming a default, empty or absent value
errs toward    : FALSE POSITIVE (a missed fail-open is the defect itself)
scope          : an explicit path set, 2 file(s)
   bin/gatebraid-snapshot.py
   bin/gatebraid-frontier.py
shapes searched:
   N2a  bare `except:` / `except Exception:` with no re-raise and no fail-closed assignment
   N2b  a `returncode` read that is not compared and not carried into exit_code
   N2c  `.get(` with a non-None default on a verdict-relevant field
verdict-relevant fields : status, complete, exit_code, issue_state, verdict, workflow, cross_check, parse_status, slice_metadata_present, blocked_by, blocking, sources, items
NOT searched by this proxy (false-negative channels, Review 1 F-02):
   the `X or <empty-literal>` idiom -- 32 or-expressions in bin/gatebraid-snapshot.py by AST count, 3 in bin/gatebraid-frontier.py.
   Review 1 adjudicated all 32 independently and the property holds;
   N2 is NOT what establishes that, and a zero here is not evidence about that idiom.
   N2a's fail_closed test is a substring search for "raise", which a comment or
   string literal could satisfy -- a handler merely mentioning the word is credited.

matches        : 0

N2 HOLDS: no fail-open shape found on any verdict-relevant path in the scope above
(exit 0)
```

**V15 — N3 · no live network call in any declared test command**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g2/negative-criterion-N3.py
criterion      : N3 - no live network call in any declared test command
pattern proxied: a declared test depending on the live control plane
errs toward    : FALSE POSITIVE (a mention in prose trips it)
scope          :
   the declared-command table of docs/evidence/gatebraid/P2-S4/gate1.md
   bin/gatebraid-o0-acceptance.py
   NOT in scope: bin/gatebraid-snapshot.py, which carries a live gh transport by design
shapes searched:
   N3a  a `gh` invocation in a declared command's argv
   N3b  an HTTP client named in the harness source: requests, httpx, aiohttp, urllib, urlopen, http.client, HTTPConnection, socket

declared commands read from the frozen plan : 13
   D1a  `C:/Python312/python.exe -B bin/gatebraid-snapshot-selftest.py`
   D1b  `wsl -e bash -lc "cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-snapshot-sel
   D2a  `C:/Python312/python.exe -B bin/gatebraid-frontier-selftest.py`
   D2b  `wsl -e bash -lc "cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-frontier-sel
   D3a  `C:/Python312/python.exe -B bin/gatebraid-o0-acceptance.py --induced-failures --out docs/evidence/gatebraid/P2-S4/acce
   D3b  the D3a command under `wsl -e bash -lc` with `PYTHONDONTWRITEBYTECODE=1 python3 -B`
   D4   `C:/Python312/python.exe -B bin/gatebraid-o0-acceptance.py --dependency-directions --out docs/evidence/gatebraid/P2-S4
   D5   `C:/Python312/python.exe -B bin/gatebraid-o0-acceptance.py --byte-contract --out docs/evidence/gatebraid/P2-S4/accepta
   D6a  `C:/Python312/python.exe -B bin/gatebraid-validate.py --corpus fixtures`
   D6b  the D6a command under `wsl -e bash -lc` with `PYTHONDONTWRITEBYTECODE=1 python3 -B`
   D7   `C:/Python312/python.exe -B fixtures/runner-selftest.py`
   D8   `git merge-base --is-ancestor df666070ead7fa21bc72b6c99d2644923b37e787 HEAD`
   N1   `C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/negative-criterion-N1.py df666070ead7fa21bc72b6c99d264492

[... shown 26 of 29 lines (head); full output: docs/evidence/gatebraid/P2-S4/g2/G2-N3.json]
(exit 0)
```

**V16 — N4 · no verdict without validation, both halves; the structural half's claim is corrected at repair 1 to what was measured — one guarded construction site, NOT an unforgeable type**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g2/negative-criterion-N4.py
criterion      : N4 - no verdict without validation
pattern proxied: a verdict emitted for a document that was never validated against gatebraid/snapshot@1
errs toward    : FALSE POSITIVE (a rename or a split of validate() trips the structural half)
scope          :
   bin/gatebraid-frontier.py                 (N4a, structural)
   fixtures/state-pipeline/sp10-snapshot-missing-schema-key.json (N4b, behavioural)

N4a measured:
   ValidatedSnapshot construction sites : 1
      line 232   inside validate()
   constructor refuses a wrong token    : True
   consume() takes the validated object : True
   NOT established by N4a               : that the type cannot be forged. _VALIDATION_TOKEN is a reachable module attribute and consume() has no isinstance guard, so a caller holding the module can construct one (Review 1, F-03).

N4b measured on fixtures/state-pipeline/sp10-snapshot-missing-schema-key.json:
   exit status                          : 1 (a refusal is 1)
   report file written                  : False
   bytes reaching stdout                : 0

matches        : 0

N4 HOLDS: one construction site, inside validate(), guarded by a token so an accidental second site fails loudly -- strong against refactor drift, NOT proof against a determined caller in the same module -- and the corpus fixture the plan names produces no verdict
(exit 0)
```

**V17 — T3 harness selftest, both platforms (NOT a declared test-plan command; recorded because it is the falsification of the instrument the declared commands rely on)**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-o0-acceptance-selftest.py
A14    and carries every declared case                      12            12            PASS    the file is the record, not a summary of one
A15    and records a failing run as NOT clean               False         False         PASS    the file must not disagree with the exit status
A16    no mode selected is a usage error                    2             2             PASS    a harness with no mode must not default to the cheapest one
A17    two modes at once is a usage error                   2             2             PASS    one mode, one summary, one exit status

scratch directory             : outside every repository (tempfile.mkdtemp)
harness under test            : D:\Github repo\Gatebraid\bin\gatebraid-o0-acceptance.py
interpreter                   : C:\Python312\python.exe
falsification method          : a complete parallel tree with the consumer replaced by a fail-open stub
network reads performed       : 0
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
[... shown 12 of 26 lines (tail); full output: docs/evidence/gatebraid/P2-S4/g2/G2-T3selftest-windows.json]
(exit 0)
$ wsl -e bash -lc 'cd '\''/mnt/d/Github repo/Gatebraid'\'' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-o0-acceptance-selftest.py'
A14    and carries every declared case                       12            12            PASS    the file is the record, not a summary of one
A15    and records a failing run as NOT clean                False         False         PASS    the file must not disagree with the exit status
A16    no mode selected is a usage error                     2             2             PASS    a harness with no mode must not default to the cheapest one
A17    two modes at once is a usage error                    2             2             PASS    one mode, one summary, one exit status

scratch directory             : outside every repository (tempfile.mkdtemp)
harness under test            : /mnt/d/Github repo/Gatebraid/bin/gatebraid-o0-acceptance.py
interpreter                   : /usr/bin/python3
falsification method          : a complete parallel tree with the consumer replaced by a fail-open stub
network reads performed       : 0
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
[... shown 12 of 26 lines (tail); full output: docs/evidence/gatebraid/P2-S4/g2/G2-T3selftest-wsl.json]
(exit 0)
```

**V18 — this gate's captures machine-validated under the capture tool's own write-path guard, re-derivation layer included (NOT a declared test-plan command; it is what makes the `output_ref` targets evidence rather than filenames). The count in this row is the WORKING TREE at `2026-08-24T13:02:34Z`; see the disclosures for the three instants and their three figures**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g2/verify-captures.py docs/evidence/gatebraid/P2-S4/g2
capture directory             : docs/evidence/gatebraid/P2-S4/g2
guard                         : bin/gatebraid-capture.py --verify-record --rederive
interpreter                   : C:\Python312\python.exe
captures found                : 34
captures verified             : 34
captures rejected             : 0
not in this set               : this driver's own capture, written by the capture tool after this process exits
CAPTURES CLEAN: every capture reproduced its recorded digests under the write path's own guard
(exit 0)
```

## Review record

### Review 1

| Item | Verdict | Evidence |
|---|---|---|
| R1 allowlist confinement | | V13, and `git status --porcelain --untracked-files=all` at review time |
| R2 test-plan coverage | | V1–V13, item-by-item mapping in the frozen plan's acceptance mapping |
| R3 evidence is rows that reproduce | | every row above; the deterministic subset is V12, V13, V14, V15, V16 |
| R4 negative criterion | | V13 (N1), V14 (N2), V15 (N3), V16 (N4) |
| R5 no prohibited action | | E2–E5; no push, PR, merge, tag or dependency install appears in any capture |

**Reviewer rows** (the commands the reviewer ran, with outputs — including, for R3's deterministic subset, the byte-identity re-runs)
```
[written by the reviewer]
```

**Findings** (only if any verdict is fail — one row per finding: what was measured, not a story about it)
```
[written by the reviewer]
```

- Reviewer write disclosure: [written by the reviewer]
- Rules given to the reviewer: [written by the reviewer]

## Repair record

### Repair 1

- Hypothesis (new): the record's own reproducibility, not its measurements, is what is defective — two rows nominated as deterministic name a moving ref, and three prose claims (N4's reach, N2's reach, the capture count) assert more or less than what was measured.

**Novelty measured** (ADR-0027 §1; the comparand is the tree Review 1 examined, not a failed state — no review item was red)
**tree at the reviewed state, and the paths this repair changes**
```
$ git rev-parse 0964979cc58a6726a1e4c40debc4e0e887ad3d0d^{tree}
7440e0257e9bdd98f0825f87959ac9f56aa0b548
(exit 0)
$ git status --porcelain --untracked-files=all
 M docs/evidence/gatebraid/P2-S4/g2/G2-D8.json
 M docs/evidence/gatebraid/P2-S4/g2/G2-N1.json
 M docs/evidence/gatebraid/P2-S4/g2/G2-N2.json
 M docs/evidence/gatebraid/P2-S4/g2/G2-N4.json
 M docs/evidence/gatebraid/P2-S4/g2/G2-fp-diff.json
 M docs/evidence/gatebraid/P2-S4/g2/G2-fp-tree.json
 M docs/evidence/gatebraid/P2-S4/g2/negative-criterion-N2.py
 M docs/evidence/gatebraid/P2-S4/g2/negative-criterion-N4.py
 M docs/evidence/gatebraid/P2-S4/g2/render-gate2.py
?? docs/evidence/gatebraid/P2-S4/g2/G2-R1-tree-before.json
(exit 0)
```

- The changed-path list above is measured before this record is re-rendered, so it does not include this record itself (`gate2.md`) nor any capture written after that measurement — this row's own capture, and the record-validation capture. Every one of them is under `docs/evidence/gatebraid/P2-S4/g2/`, no `bin/` path is among them, and the repair commit's own diff is the comparand the bounded re-check runs.
- Result: `green`
- Consult: `none`
- Scope: `docs/evidence/gatebraid/P2-S4/` only. **No `bin/` file changed — not one byte**, verified by `git status --porcelain --untracked-files=all -- bin/` returning empty and by the repair commit's diff carrying no `bin/` path. No behavioural change was made to either tool or to either checker; every edit is to what a record or a checker SAYS about what it measured.
- `repair_limit` 2: **one spent, one remains.**

## Required disclosures

- Deviations: **D7 was not run at the first of its three named points.** The frozen plan requires the frozen surface to be re-measured by D7 *before the first implementation commit*, after the last, and at Gate 2 exit. It was run after the last implementation commit and at exit, and NOT before the first one; the omission is the executor's. What stands in its place is a stronger statement over a wider interval rather than a substitute measurement at the missed instant: V13 (N1) shows the whole range `df666070ead7fa21bc72b6c99d2644923b37e787..HEAD` touches no path outside `bin/` and `docs/evidence/gatebraid/P2-S4/`, so neither `schema/` nor `fixtures/` was written at any point in this gate, and V11 shows `digest before` equal to `digest after` equal to the batch-frozen value. The schema half was also measured before the first implementation commit incidentally, by the producer's own startup line naming `schema/snapshot.schema.json sha256=95ecf38e…`. The timing requirement was still missed and is recorded as missed · **two seeded cases in the harness were corrected by their own first run**, both disclosed because a seed that measures nothing is the defect this project has recorded most often: a capped transcript whose pages carried no item exercised the bounded flag and then had no item to carry a verdict, and an ASCII-only probe file needed its non-ASCII payload as escapes rather than as literals · **negative criterion N2 fired on this Slice's own implementation and the implementation was changed rather than the criterion.** The replay transport read `exit_code` with a non-`None` default, which places an implicit success assumption on a path that reaches a verdict; commit `1da43d8` removes it and S37 seeds the new behaviour. N2 now holds with zero matches · **`bin/gatebraid-snapshot.py` carries a live `gh` transport that no declared test command exercises.** Every declared command selects the replay transport or reads a frozen fixture, so the live path is committed but unmeasured at this gate; N3's scope names this explicitly rather than leaving it implied · **the three negative-criterion checkers for N2, N3 and N4 were authored at this gate**, not at Gate 1, which committed only N1's. They are instruments authored beside the work they certify — the pattern ADR-0028 §4 warns about — and are offered as mechanical aids to R4 rather than as independent certification; each states the pattern it proxies for, its explicit scope, and the direction in which it errs · **the handoff fingerprint and V18's sweep were measured at the commit BEFORE this record's own commit**, which is what the fingerprint's definition requires and what makes it Gate 3's comparand. V12 (D8) and V13 (N1) described the same instant but named `HEAD` to reach it; **repair 1 pins both to `50d08de6…`** so they reproduce, and N1 now returns the recorded `137` instead of moving with the tip. The files each later commit adds are outside those measurements; every one of them is under `docs/evidence/gatebraid/P2-S4/`, so the allowlist claim is unaffected. This is the boundary any sweep has over its own output, named rather than left to be noticed · **REPAIR 1, F-01 — what was pinned and what was deliberately not.** `V12` and `V13` are pinned, and so are `G2-fp-tree` (`git rev-parse 50d08de6…^{tree}`, which still derives the tree rather than restating it) and `G2-fp-diff` (`git diff --name-only df666070…..50d08de6…`, which reproduces the 137 paths exactly), plus the `allowlist-respected` `checks[]` row. **`G2-fp-head` is left naming `HEAD`, on purpose.** Pinning it would turn `git rev-parse HEAD` into `git rev-parse 50d08de6…`, a command that echoes its own argument and establishes nothing; the row's only content is *what the branch head was at that instant*, and pinning would destroy it while making the row look deterministic. The grant says not to manufacture agreement, and that is what manufacturing it would look like. The claim is corroborated instead: `G2-fp-tree` derives `f797297005…` from that commit and it matches the recorded `tree_sha` · **REPAIR 1, F-03 — an overclaim in this record, corrected.** The N4 structural half was described as making the validated type UNFORGEABLE. Review 1 measured that false: `_VALIDATION_TOKEN` is a reachable module attribute, a holder of the module forged a `ValidatedSnapshot`, and `consume()` carries no `isinstance` guard — it rejected a duck-typed stand-in only incidentally, by `AttributeError`. The accurate claim, now carried by the checker's own output, is one guarded construction site inside `validate()`: strong against accidental refactor, NOT proof against a determined caller in the same module. **The N4 property itself holds in both halves**; the overstatement was in prose. `isinstance` was NOT added — that is hardening, not correction, and shipping un-reviewed behaviour after the review is what this sequence must not do; it is debt. **`bin/gatebraid-frontier.py`'s module docstring carries the same word and was not edited**, because this repair changes no `bin/` byte; that line is debt too, and it is named here so the correction is not mistaken for complete · **REPAIR 1, F-02 — N2's reach was overstated by omission.** N2 declares it errs toward false positives and owed an account of its false-NEGATIVE channels. Two are now named in its own scope statement: the `X or <empty-literal>` idiom is not searched at all — 32 `or`-expressions in `bin/gatebraid-snapshot.py` by AST count, re-derived here and equal to Review 1's — and N2a's `fail_closed` test is a substring search for `"raise"` that a comment or string literal could satisfy. Review 1 adjudicated all 32 independently and the property holds; **the correction is that N2 is not what establishes it.** The checker's behaviour is unchanged: changing what it detects after its gate exited would ship un-reviewed behaviour · **REPAIR 1, F-05 — one figure, three instants.** The capture count in `g2/` is **30** committed at the fingerprint commit `50d08de6…`, **34** in the working tree when the sweep ran (`2026-08-24T13:02:34Z` to `13:02:38Z`, ten seconds before that commit at `13:02:48Z`), and **41** at the tip `0964979c…`; all three are re-derived here and all three are true of their own instant. A fourth figure, **33**, appears in this Slice's posted Gate 2 handoff comment `5395615534` and originated with this executor: it was the standalone sweep run before `G2-D7-exit` and the sweep's own capture existed. The posted comment is durable and is not edited; the figure is corrected here. **The ambiguity was the defect, not any figure** · **REPAIR 1, F-04 is RECORDED, NOT REPAIRED.** The live `gh` transport stays committed and unmeasured: covering it needs a test this frozen plan does not declare, and the boundary is already disclosed above and named in N3's scope. It goes to the closure ledger as debt · **commit messages carry a `Co-Authored-By` trailer** per the executing harness's standing instruction, noted so the convention change is not mistaken for drift.
- Reviewer write disclosure: `none` — no review has run at the time this record is written.
- Environment: Windows 11 host, Git Bash (MSYS2) shell, `mixed-see-prose` with the WSL half exercised for D1b, D2b, D3b, D6b and V17; Windows loader `C:\Python312\python.exe` (CPython 3.12.2, jsonschema 4.23.0), WSL `/usr/bin/python3` (CPython 3.12.3, jsonschema 4.10.3); `PYTHONDONTWRITEBYTECODE=1` on every Windows Python invocation and set inside the `wsl` command on the WSL half, which inherits no Windows process environment; `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` call, every endpoint written without a leading slash (friction #33); the selftest seeds and the harness's parallel tree are written to scratch paths outside every repository, as the contract requires such a path to be named. **BP-01 fired once more during this gate, on the executor's own verification rather than on a deliverable, and is recorded because it is a measurement.** Checking that this record's `Plan Approval (G1→G2)` carries U+2192 was first attempted by piping `gh project field-list --format json` into a Python reader; the console codec re-encoded the response and the live option name arrived as the codepoints U+922B U+625C, so the comparison returned a FALSE mismatch. Re-measured by writing the response to a file and reading it with an explicit UTF-8 decode, the live option is U+2192 and the record string is byte-identical to it; `Gate 2 — Implementing` is U+2014 on the same measurement. The corrupted read was not acted on, and the hazard the frozen plan's P0-2 addresses is therefore live on this host in both directions — which is what D5's `B-premise` case independently establishes.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S4
gate: 2
environment: mixed-see-prose
executor: Claude Lead
base_sha: df666070ead7fa21bc72b6c99d2644923b37e787
active_branch: slice/P2-S4
started_at: "2026-08-24T12:20:50.302787Z"
ended_at: "2026-08-25T03:56:47Z"
result: needs_approval
checks:
  - name: plan-approval-verified
    command: "gh api repos/MianliWang/gatebraid/issues/comments/5394791863 --jq '{author,url,created,updated}'"
    result: pass
    output_ref: "#entry-records"
  - name: writer-assignment-verified
    command: "gh api repos/MianliWang/gatebraid/issues/comments/5395086921 --jq '{author,url,created,updated}'"
    result: pass
    output_ref: "#entry-records"
  - name: writer-lease-taken
    command: "gh project item-edit (Writer Lease) + read-back"
    result: pass
    output_ref: "#entry-records"
  - name: baseline-reread
    command: "git ls-remote origin refs/heads/main"
    result: pass
    output_ref: "#entry-records"
  - name: active-branch-created-from-Y
    command: "git checkout -b slice/P2-S4 df666070ead7fa21bc72b6c99d2644923b37e787"
    result: pass
    output_ref: "#entry-records"
  - name: D1a-producer-selftest-windows
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-D1a.json"
  - name: D1b-producer-selftest-wsl
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-D1b.json"
  - name: D2a-consumer-selftest-windows
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-D2a.json"
  - name: D2b-consumer-selftest-wsl
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-D2b.json"
  - name: D3a-induced-failures-windows
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-D3a.json"
  - name: D3b-induced-failures-wsl
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-D3b.json"
  - name: D4-dependency-directions
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-D4.json"
  - name: D5-byte-contract
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-D5.json"
  - name: D6a-frozen-corpus-windows
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-D6a.json"
  - name: D6b-frozen-corpus-wsl
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-D6b.json"
  - name: D7-frozen-surface-unmoved
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-D7.json"
  - name: D8-freeze-precedes-implementation
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-D8.json"
  - name: N1-path-scope
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-N1.json"
  - name: N2-no-fail-open
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-N2.json"
  - name: N3-no-live-network
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-N3.json"
  - name: N4-no-verdict-without-validation
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-N4.json"
  - name: harness-selftest-windows
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-T3selftest-windows.json"
  - name: harness-selftest-wsl
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-T3selftest-wsl.json"
  - name: captures-machine-validated
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g2/G2-captures-validation.json"
  - name: allowlist-respected
    command: "git diff --name-only df666070ead7fa21bc72b6c99d2644923b37e787..50d08de65158faf23f1ae86aeebcde39e929c359"
    result: pass
    output_ref: "#verification-outputs"
handoff_fingerprint:
  active_branch_head: "50d08de65158faf23f1ae86aeebcde39e929c359"
  tree_sha: "f797297005d35d150799af300ecc22daef35dac9"
  changed_paths:
    - bin/gatebraid-frontier-selftest.py
    - bin/gatebraid-frontier.py
    - bin/gatebraid-o0-acceptance-selftest.py
    - bin/gatebraid-o0-acceptance.py
    - bin/gatebraid-snapshot-selftest.py
    - bin/gatebraid-snapshot.py
    - docs/evidence/gatebraid/P2-S4/acceptance/bytes.json
    - docs/evidence/gatebraid/P2-S4/acceptance/deps.json
    - docs/evidence/gatebraid/P2-S4/acceptance/induced.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q1-falsify-badfield.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q1-falsify-noauth.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q1-identity.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q2-approval.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q2-falsify.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q3-falsify.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q3-issue.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q4-project.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q5-falsify.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q5-field-list-json.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q5-field-list.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q6-falsify-badfield.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q6-falsify-noissue.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q6-falsify-selector.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q6-item-fields.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q7-blocked-by.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q7-blocking.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-Q7-falsify.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-baseline-main.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-captures-validation.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-closed-set-sweep-pass1.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-closed-set-sweep.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-env-field.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-exit-fields-readback.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-exit-handoff-post.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-exit-set-checkpoint.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-exit-set-gate.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-exit-set-workflow.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-handoff-validation.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-head.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-host-probe.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-porcelain-baseline.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-porcelain-full.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-porcelain-outside-domain.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-record-validation-rejected-pass1.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-record-validation.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-ref-namespace.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-remote.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-render-record.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-slice-body-failed-attempt.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-slice-body.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-slice-metadata-loader.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-slice-metadata-selftest.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-slice-metadata-validation-on-empty.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-slice-metadata-validation.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-tools-claude.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-tools-codex.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-tools-gh.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-tools-git.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-tools-python-windows.json
    - docs/evidence/gatebraid/P2-S4/captures/G0-tools-python-wsl.json
    - docs/evidence/gatebraid/P2-S4/captures/slice-body-14.md
    - docs/evidence/gatebraid/P2-S4/checks-g0-closed-set-sweep.py
    - docs/evidence/gatebraid/P2-S4/checks-g0-render-record.py
    - docs/evidence/gatebraid/P2-S4/checks-g0-verify-captures.py
    - docs/evidence/gatebraid/P2-S4/g1/G1-allowlist-hash.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-dryrun-D6a-windows.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-dryrun-D6b-wsl.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-dryrun-D7-windows.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-dryrun-N1-falsify.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-dryrun-N1.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-dryrun-matrix.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-exit-handoff-post.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-exit-label-readback.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-exit-readback.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-exit-set-checkpoint.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-exit-set-gate.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-exit-set-label.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-exit-set-nextapproval.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-exit-set-workflow.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-formprobe-byte-contract.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-formprobe-outpath.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-handoff-validation.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-plan-hash.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-plan-path-scan-pass1.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-plan-path-scan.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-record-validation.json
    - docs/evidence/gatebraid/P2-S4/g1/G1-writedomains-check.json
    - docs/evidence/gatebraid/P2-S4/g1/byteprobe-cp936.cmd
    - docs/evidence/gatebraid/P2-S4/g1/byteprobe-cp936.out
    - docs/evidence/gatebraid/P2-S4/g1/byteprobe.py
    - docs/evidence/gatebraid/P2-S4/g1/dryrun-driver.py
    - docs/evidence/gatebraid/P2-S4/g1/gate1-exit-checklist.md
    - docs/evidence/gatebraid/P2-S4/g1/hash-allowlist.py
    - docs/evidence/gatebraid/P2-S4/g1/hash-plan.py
    - docs/evidence/gatebraid/P2-S4/g1/negative-criterion-N1.py
    - docs/evidence/gatebraid/P2-S4/g1/pathprobe.py
    - docs/evidence/gatebraid/P2-S4/g1/plan-path-scan.py
    - docs/evidence/gatebraid/P2-S4/g1/raw-fieldlist-exit.gh-response.json
    - docs/evidence/gatebraid/P2-S4/g1/render-gate1.py
    - docs/evidence/gatebraid/P2-S4/g1/writedomains-check.py
    - docs/evidence/gatebraid/P2-S4/g2/G2-D1a.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-D1b.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-D2a.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-D2b.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-D3a.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-D3b.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-D4.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-D5.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-D6a.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-D6b.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-D7-exit.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-D7.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-E-exit-readback.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-E1-identity.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-E1-plan-approval.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-E1-writer-assignment.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-E2-remove-label.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-E2-set-lease.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-E2-set-nextapproval.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-E2-set-workflow.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-E3-baseline-Y.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-E4-branch.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-E4-set-activebranch.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-E4-set-basesha.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-N2.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-N3.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-N4.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-T3selftest-windows.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-T3selftest-wsl.json
    - docs/evidence/gatebraid/P2-S4/g2/G2-captures-validation.json
    - docs/evidence/gatebraid/P2-S4/g2/negative-criterion-N2.py
    - docs/evidence/gatebraid/P2-S4/g2/negative-criterion-N3.py
    - docs/evidence/gatebraid/P2-S4/g2/negative-criterion-N4.py
    - docs/evidence/gatebraid/P2-S4/g2/render-gate2.py
    - docs/evidence/gatebraid/P2-S4/g2/verify-captures.py
    - docs/evidence/gatebraid/P2-S4/gate0.md
    - docs/evidence/gatebraid/P2-S4/gate1.md
consults: []
repair_attempts:
  - number: 1
    hypothesis: "The record's reproducibility and the reach of three of its prose claims are defective, not its measurements: two rows nominated as deterministic name a moving ref, N4 was called unforgeable, N2 did not name its false-negative channels, and one capture count was stated without its instant. Corrections only; no bin/ byte and no checker behaviour changed."
    result: green
approvals:
  - type: "Plan Approval (G1→G2)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/14#issuecomment-5394791863"
    author: "MianliWang"
    at: "2026-08-24T11:51:54Z"
  - type: "Plan Approval (G1→G2)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/14#issuecomment-5395086921"
    author: "MianliWang"
    at: "2026-08-24T12:19:15Z"
plan_hash: "cb577dbf7fd1c0443b5e7ffbb94aacd7ada64385230afb6faa498815a4828913"
allowlist_hash: "feb6d9c8ffbbaa08242d68e64db7b13b3f080aaae3667f01d7d22bdb0c061655"
evidence_files:
  - docs/evidence/gatebraid/P2-S4/gate2.md
notes: "Implementation of the frozen plan in three tasks, each shipping a tool and its committed falsification. This gate does not grade itself: `result` is needs_approval and the Review 1 verdict cells are left blank for the reviewer; transcription of a passing review happens under the Release Approval, not here. APPROVALS[] OVER-COUNTS PLAN APPROVALS BY ONE AND CANNOT DO OTHERWISE, so a consumer reading approvals[] alone must read this note too: comment 5394791863 is the Plan Approval, and comment 5395086921 is the operator WRITER ASSIGNMENT, a DIFFERENT act, whose clause 2 amends the Plan Approval window clause so Gate 2 opens in the session presenting its URL and whose clause 7 makes the writer role transferable only by an operator comment on the issue. Both entries carry type Plan Approval because the frozen gatebraid/gate-run@2 enumeration for approvals[].type has ten members and none is Writer Assignment: the typing is SCHEMA-FORCED, not chosen. A reader consuming approvals[] without this sentence counts two Plan Approvals where one Plan Approval and one Writer Assignment occurred. The schema belongs to the batch lane and is not this Slice to change; the missing member is queued for its next revision (Review 1, F-06). Repair 1 of 2 is spent on record corrections only -- no bin/ byte and no checker behaviour changed -- and one repair remains. The frozen schema and corpus were never written: N1 over the whole range touches only bin/ and this Slice evidence path, and D7 shows the digest unmoved at 66051715f76cf52d881aa143d9267f932407dbf5b9c4e6be9f81395ec641ef8e. No push, PR, tag or merge; publication is Gate 3."
```
