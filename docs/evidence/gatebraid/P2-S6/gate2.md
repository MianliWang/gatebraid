# Gate 2 evidence - P2-S6

## Entry records

**E1 - Plan Approval verified: the author observed, and the executor identity it is compared against**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5466316139 --jq '{author: .user.login, url: .html_url, created_at: .created_at}'
{"author":"MianliWang","created_at":"2026-08-30T02:48:13Z","url":"https://github.com/MianliWang/gatebraid/issues/19#issuecomment-5466316139"}
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login
mianliwang492-source
(exit 0)
```

**E2 - Writer Lease taken, read back**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query{node(id:"PVTI_lAHOBRofUs4Beum7zg4gxqQ"){... on ProjectV2Item{fieldValues(first:60){nodes{... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2FieldCommon{name}}}}}}}}' --jq '[.data.node.fieldValues.nodes[] | select(.field.name=="Writer Lease" or .field.name=="Active Branch" or .field.name=="Base SHA") | {(.field.name): .text}]'
[{"Base SHA":"3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8"},{"Writer Lease":"RoughEgoist:claude-p2s6-executor:2026-08-30T02:58:49Z"},{"Active Branch":"slice/P2-S6"}]
(exit 0)
```

**E3 - baseline re-read: Y measured, and the changed-path set X..Y**
```
$ git rev-parse refs/remotes/origin/main
3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
(exit 0)
$ git diff --name-only 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8..3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
(no output)
(exit 0)
```

- baseline: `unchanged`

**E4 - Active Branch created from Y; the Base SHA field set to Y (read back in E2)**
```
$ git rev-parse --abbrev-ref HEAD
slice/P2-S6
(exit 0)
$ git rev-parse HEAD
5386ce382bac5b4bc1c76a38bcbe86717adf9c1c
(exit 0)
```

## Verification outputs

**V1 D1 - the frozen corpus digest is unmoved by this Slice**
```
$ C:/Python312/python.exe -B fixtures/runner-selftest.py
condition                           want  got  verdict  required observation
S00 untouched copy                     0    0  PASS     CORPUS CLEAN
[... shown 18 of 37 lines; full output: docs/evidence/gatebraid/P2-S6/g2/captures/G2-D1-corpus-digest.json]
S25 validator cannot resolve           3    3  PASS     ENVIRONMENT
S26 validator library absent           3    3  PASS     not importable
S27 __pycache__ present                0    0  PASS     CORPUS CLEAN
S11 unexpected argument                2    2  PASS     unexpected argument
S15 cwd-independence holds             0    0  PASS     CORPUS CLEAN from both
S16 cwd-independence falsified       !=0    2  PASS     must NOT be clean from elsewhere
S21 digest sees run-corpus.py       moves  moves  PASS     digest must change when the file changes
S22 digest sees runner-selftest.py  moves  moves  PASS     digest must change when the file changes
S28 __pycache__ moves no digest     same  same  PASS     digest must ignore interpreter output

digest scope                  : bytes-platform, evidence-capture-v1, gate-run-v2, instruments, live-shapes, metrics-v1, state-pipeline, CORPORA.json, schema, run-corpus.py, runner-selftest.py, fixtures/ listing
digest before                 : 73c5e059091982ac8cda43d9f59902f3934444b742e7a383ad9422448cd5fdfc
digest after                  : 73c5e059091982ac8cda43d9f59902f3934444b742e7a383ad9422448cd5fdfc
seed-reachable surface UNMODIFIED: True
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
(exit 0)
```

**V2 D2 - the whole frozen corpus passes unchanged; the four live-shapes mutations stay killed**
```
$ C:/Python312/python.exe -B fixtures/run-corpus.py
corpus bytes-platform (v1.1)  <- fixtures\bytes-platform\EXPECTATIONS.json
  loader recorded: CPython 3.12.2 (C:/Python312/python.exe), jsonschema 4.23.0, Draft202012Validator; re-measured identical under CPython 3.12.3 / jsonschema 4.10.3 on WSL
  ok   BP1-01  valid as recorded  [positive control �� one report, one platform, honestly claimed]
  ok   BP1-02  valid as recorded  [positive control �� the only legitimate way to claim both platforms]
  ok   BP1-03  killed on required@properties/1/replay:rederived_sha256 [properties/properties/items/properties/replay/required]  [BP-01 blocked remainder �� sha256 over raw bytes fails to re-derive]
  ok   BP1-04  killed on pattern@properties/1/replay/rederived_sha256 [properties/properties/items/properties/replay/properties/rederived_sha256/pattern]  [BP-02 blocked remainder �� byte_length mismatch caught]
[... shown 16 of 156 lines; full output: docs/evidence/gatebraid/P2-S6/g2/captures/G2-D2-corpus.json]
  ok   SP1-11  killed on const@sources/0/complete [properties/sources/items/allOf/5/then/properties/complete/const]  [SP-07 truncated connections]
  ok   SP1-12  killed on const@items/0/verdict [properties/items/items/allOf/0/then/properties/verdict/const]  [SP-08 unknown Issue state]
  ok   SP1-13  killed on not@items/0 [properties/items/items/allOf/1/then/not], required@items/0:excluded_reason [properties/items/items/allOf/1/then/required]  [SP-09 non-Slice Project item]
  ok   SP1-14  killed on required@(root):schema [required]  [SP-10 missing snapshot schema / version]
  ok   SP1-15  killed on required@items/0/dependencies:blocking [properties/items/items/properties/dependencies/required]  [SP-11 one-direction dependency loss]
  ok   SP1-16  killed on required@items/0/soft_dependencies:parse_status [properties/items/items/properties/soft_dependencies/required]  [SP-12 soft Gate-1/Gate-2 dependency unsatisfied]
  ok   SP1-17  killed on not@items/0/verdict [properties/items/items/allOf/5/then/properties/verdict/not]  [SP-13 aborted item presented as ready]

TOTAL: 133 passed, 0 failed
CORPUS CLEAN
(exit 0)
```

**V3 D3 - snapshot selftest, Windows half: the live shapes and B-1..B-4**
```
$ C:/Python312/python.exe -B bin/gatebraid-snapshot-selftest.py
id     condition                                                      want          got           verdict required observation
S01    a healthy read emits and exits 0                               0             0             PASS    a fail-closed tool that rejected everything would fail HERE and pass every negative below
S02    the healthy positive control is startable                      startable     startable     PASS    the tool can still say yes; fail-closed is not reject-everything
S03    P0-1 auth_failure (401 answered on a read)                     auth_failure  auth_failure  PASS    a class with no seeded condition is a class nobody has shown to fire
S04    P0-1 permission_failure (403 with budget remaining)            permission_fa permission_fa PASS    a class with no seeded condition is a class nobody has shown to fire
S05    P0-1 rate_limited (403 with the budget exhausted)              rate_limited  rate_limited  PASS    a class with no seeded condition is a class nobody has shown to fire
S06    P0-1 network_error (the read could not be performed)           network_error network_error PASS    a class with no seeded condition is a class nobody has shown to fire
S07    P0-1 server_error (the endpoint answered 503)                  server_error  server_error  PASS    a class with no seeded condition is a class nobody has shown to fire
S08    P0-1 parse_error (a body that is not JSON)                     parse_error   parse_error   PASS    a class with no seeded condition is a class nobody has shown to fire
S09    P0-1 unexpected_endpoint (a shape the tool does not recognise) unexpected_en unexpected_en PASS    a class with no seeded condition is a class nobody has shown to fire
S10    a degraded snapshot exits 3, never 0                           3             3             PASS    the exit status is the only thing a shell caller reads
S11    degraded forces verdict undecidable                            undecidable   undecidable   PASS    the dropped-edge-read-as-no-blocker defect, structurally refused
S12    the non-zero process exit reaches the document                 1             1             PASS    ADR-0029 decision 2 P0-1: a non-zero gh exit folded into None
S13    a zero-exit failed read carries the sentinel                   65            65            PASS    the schema forbids a non-ok status reporting a success exit
S14    and names the real process exit in failure_detail              True          True          PASS    the process status stays recoverable rather than being lost
S15    P0-3 the cap sets bounded and degrades                         page_cap_reac page_cap_reac PASS    a truncated list reported as whole is the P0-3 defect
S16    P0-3 the capped read is not complete                           False         False         PASS    completeness asserted without pagination
S17    P0-3 a capped read exits 3                                     3             3             PASS    reaching a cap fails closed rather than passing
S18    a failed read carries bounded query_failed                     query_failed  query_failed  PASS    an incomplete read that does not say where it stopped is indistinguishable from a complete one
S19    P0-4 an unknown issue state maps to UNKNOWN                    UNKNOWN       UNKNOWN       PASS    state != OPEN read as unblocked is the defect
S20    P0-4 and yields undecidable, never unblocked                   undecidable   undecidable   PASS    the unblocked reading is what P0-4 names
S21    P0-4 the unrecognised value is kept for diagnosis              True          True          PASS    diagnosable without being trusted
S22    P0-4 an unrecognised workflow yields undecidable               undecidable   undecidable   PASS    an open vocabulary would let a new value arrive as a string nobody checks
S23    P0-4 a non-Slice row carries no verdict                        True          True          PASS    a verdict emitted for a non-Slice row is SP-09
S24    P0-4 and states why it was excluded                            True          True          PASS    an exclusion nobody can read is indistinguishable from an omission
S25    P0-4 a one-directional read is a mismatch                      mismatch      mismatch      PASS    one direction trusted without the cross-check is SP-11
[... shown 34 of 67 lines; full output: docs/evidence/gatebraid/P2-S6/g2/captures/G2-D3-selftest-windows.json]

scratch directory             : outside every repository (tempfile.mkdtemp)
tool under test               : D:\Github repo\Gatebraid\bin\gatebraid-snapshot.py
interpreter                   : C:\Python312\python.exe
network reads performed       : 0 (replay transport, and frozen O1-B1
                                bodies for the live half)
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
(exit 0)
```

**V4 D4 - snapshot selftest, WSL half**
```
$ wsl.exe -e bash -lc 'cd '\''/mnt/d/Github repo/Gatebraid'\'' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-snapshot-selftest.py'
id     condition                                                      want          got           verdict required observation
S01    a healthy read emits and exits 0                               0             0             PASS    a fail-closed tool that rejected everything would fail HERE and pass every negative below
[... shown 10 of 67 lines; full output: docs/evidence/gatebraid/P2-S6/g2/captures/G2-D4-selftest-wsl.json]

scratch directory             : outside every repository (tempfile.mkdtemp)
tool under test               : /mnt/d/Github repo/Gatebraid/bin/gatebraid-snapshot.py
interpreter                   : /usr/bin/python3
network reads performed       : 0 (replay transport, and frozen O1-B1
                                bodies for the live half)
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
(exit 0)
```

**V5 D5 - live smoke read: the snapshot, healthy on all four sources**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid C:/Python312/python.exe -B bin/gatebraid-snapshot.py --out docs/evidence/gatebraid/P2-S6/g2/captures/g2-snapshot.json --generated-at 2026-08-30T03:08:48Z

generator                     : gatebraid-snapshot 1.0.0
schema                        : D:\Github repo\Gatebraid\schema\snapshot.schema.json sha256=95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6
transport                     : live
sources                       : 4
   project_items    ok                   complete=True  exit=0
   issue_states     ok                   complete=True  exit=0
   dep_blocked_by   ok                   complete=True  exit=0
   dep_blocking     ok                   complete=True  exit=0
items                         : 16
degraded                      : no
SNAPSHOT OK: every source read completely with status `ok`
(exit 0)
```

**V6 D6 - live smoke read: the frontier consumes it, exit 0**
```
$ C:/Python312/python.exe -B bin/gatebraid-frontier.py docs/evidence/gatebraid/P2-S6/g2/captures/g2-snapshot.json --out docs/evidence/gatebraid/P2-S6/g2/captures/g2-frontier-report.json

consumer                      : gatebraid-frontier 1.0.0
validated against             : D:\Github repo\Gatebraid\schema\snapshot.schema.json sha256=95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6
items excluded (no verdict)   : 4
startable                     : 8
blocked                       : 4
undecidable                   : 0
FRONTIER OK: the snapshot validated and every verdict was re-derived from it
(exit 0)
```

**V7 D7 - the five negative criteria hold against the real diff**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/g1/negative-criteria.py
changed-path source : git
base                : 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
changed paths       : 2
   bin/gatebraid-snapshot-selftest.py
   bin/gatebraid-snapshot.py
allowlist           : bin/, docs/evidence/gatebraid/P2-S6/
code surface        : bin/gatebraid-snapshot.py, bin/gatebraid-snapshot-selftest.py

N1 every changed path inside the allowlist        : holds
N2 under bin/, only the snapshot pair is touched  : holds
N3 no frozen input is written                     : holds
N4 no runtime dependency, no HTTP client          : holds
N5 `ok` and `complete: True` each set in one place: holds

NEGATIVE CRITERIA HOLD: N1, N2, N3, N4, N5
(exit 0)
```

**V8 D8 - the same five, falsified against a seeded input: all five fire**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/g1/negative-criteria.py --changed-from docs/evidence/gatebraid/P2-S6/g1/SEED-negative-criteria.txt --code-surface-dir docs/evidence/gatebraid/P2-S6/g1/falsification
changed-path source : docs/evidence/gatebraid/P2-S6/g1/SEED-negative-criteria.txt
base                : 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
changed paths       : 6
   bin/gatebraid-snapshot.py
   bin/gatebraid-frontier.py
   schema/snapshot.schema.json
   docs/evidence/gatebraid/P2-S5/gate0.md
   README.md
   docs/evidence/gatebraid/P2-S6/gate1.md
allowlist           : bin/, docs/evidence/gatebraid/P2-S6/
[... shown 22 of 28 lines; full output: docs/evidence/gatebraid/P2-S6/g2/captures/G2-D8-negative-falsify.json]
N2 under bin/, only the snapshot pair is touched  : FIRED
      not in the code surface: bin/gatebraid-frontier.py
N3 no frozen input is written                     : FIRED
      frozen: schema/snapshot.schema.json
      frozen: docs/evidence/gatebraid/P2-S5/gate0.md
N4 no runtime dependency, no HTTP client          : FIRED
      docs/evidence/gatebraid/P2-S6/g1/falsification\gatebraid-snapshot.py: requests (network client module)
N5 `ok` and `complete: True` each set in one place: FIRED
      docs/evidence/gatebraid/P2-S6/g1/falsification\gatebraid-snapshot.py:12 "complete": True outside read_source(), in sneaky_healthy_path
      docs/evidence/gatebraid/P2-S6/g1/falsification\gatebraid-snapshot.py:12 member('ok') outside classify(), in sneaky_healthy_path

NEGATIVE CRITERIA FIRED: N1, N2, N3, N4, N5
(exit 1)
```

**V9 - handoff fingerprint: the tree and the changed-path set at the implementation-complete commit**
```
$ git rev-parse 5386ce382bac5b4bc1c76a38bcbe86717adf9c1c^{tree}
3f88cc11fd11292d7225cb1c914dc860b8956646
(exit 0)
$ git diff --name-only 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8..5386ce382bac5b4bc1c76a38bcbe86717adf9c1c
bin/gatebraid-snapshot-selftest.py
bin/gatebraid-snapshot.py
(exit 0)
```

## Review record

### Review 1

| Item | Verdict | Evidence |
|---|---|---|
| R1 allowlist confinement | | |
| R2 test-plan coverage | | |
| R3 evidence is rows that reproduce | | |
| R4 negative criterion | | |
| R5 no prohibited action | | |

- Reviewer write disclosure: 
- Rules given to the reviewer: 

## Repair record

- No repair attempt was made: every declared command was green on its first
  run at this gate. `repair_limit` is unspent and `repair_attempts` is empty.

## Required disclosures

- Deviations: THE REVIEW RECORD SECTION OF THIS FILE IS DELIBERATELY EMPTY. The five review items are not this session's to answer: it built this tree, and R3's independence is exactly what a self-review destroys. No verdict is pre-filled, the `review-five-items` check is typed `not_run` rather than guessed, and `Gate` was NOT set to `G2 passed`. The reviewer appends its block, writes the verdicts, and the record's `result` is re-affirmed then.
- Deviations: `result: needs_approval` records the disposition this gate run actually reached - the build is complete, every declared command is green, and what stands between here and Gate 3 is human: a review and then a Release Approval. It is NOT a claim that the review passed. gate-run@2's enumeration carries no `needs_review` member, and the nearest true member is used rather than a member that would assert more than was measured.
- Deviations: the two behavioural criteria that could not be shown at Gate 1 are now shown, and the difference is worth naming precisely. At Gate 1 the declared commands D5 and D6 ran as declared and exited 3, reproducing the defect. At this gate the same two commands exit 0: all four sources `ok` and complete, sixteen items, and a frontier report carrying a verdict for P2-S5. The repair is measured by the same commands that measured its absence.
- Deviations: the item-list envelope carries NO pagination key of any kind, so a short read is detectable only by arithmetic. `connection_truncated` was used for it - already a member of the frozen bounded-reason enumeration and exactly this case. NO `schema/` byte was written and none was needed; the Non-goals hold.
- Deviations: the live surface spells issue state in lower case and the frozen schema's enumeration is upper case. The map is explicit and one-directional - `open` and `closed` only - and any other value passes through unchanged so `closed()` turns it into `UNKNOWN`. Upper-casing whatever arrived would coerce an unrecognised value toward a member, which is the one direction this tool must never move in; it is written as a named map rather than a case transform for that reason.
- Deviations: `slice_metadata_present` is derived from the presence of a non-empty Project `Slice` field on the row. That is the control plane's own declaration that a row is a Slice, and it matches the measured data exactly - eleven of the fifteen frozen elements carry `slice` and `workflow`, and the four that carry neither are the Stage and Phase container rows, which by design carry no Workflow. The reading is stated here so it can be disputed rather than applied silently.
- Deviations: B-3's frozen seed is described in the Acceptance as C-3's six-key element, and a six-key element is a CONTAINER row - it carries no Slice field, so it is excluded and never reaches a verdict at all. The behavioural property B-3 asserts is about a row that DOES reach a verdict, so LB-3 seeds the frozen envelope with the `workflow` key removed from the P2-S5 row and asserts the end-to-end result: `workflow` UNKNOWN, verdict `undecidable`, no KeyError. The container case is asserted separately at LS-01b. The substitution is named rather than left to be noticed.
- Deviations: the selftest reaches the live half by importing the tool in-process and replacing only the process-execution boundary (`_run`) with the frozen O1-B1 bodies. Endpoint construction, body normalisation, classification, pagination, assembly and verdicts are the tool's own and unmodified. This is what pays down the F-04 debt P2-S4 recorded: the live path was committed and exercised by no declared command. `network reads performed : 0` still holds.
- Deviations: `--page-cap` no longer governs the three issue-backed sources, because a per-issue fan-out is bounded by construction rather than being an open-ended connection; the transport DECLARES its read count and the loop honours it. The cap still governs any transport that declares nothing, which is every replay seed - which is why all pre-existing conditions travel exactly the path they did before and stay green. Had the cap been left applying, a fifteen-issue fan-out under the default cap of ten would have reported a complete read as bounded.
- Deviations: P2-S5 reads `blocked` in the live smoke read, not `startable`, because `#19` - this Slice - is open and blocks it. That is the setup batch's operational unblock edge working exactly as intended and is not a defect. The Acceptance asks that `items` include P2-S5 and that the frontier consume the snapshot with exit 0; both hold, and the verdict's reason is carried verbatim in the frontier report.
- Deviations: the handoff fingerprint is measured at the last IMPLEMENTATION commit, before this record and the rest of this Slice's evidence are committed, which is what the fingerprint's definition requires and what makes it Gate 3's comparand. Every commit after it is record-only and confined to docs/evidence/gatebraid/P2-S6/, which is inside the frozen allowlist.
- Deviations: this Slice's Gate 0 and Gate 1 evidence was uncommitted working material until this gate. It is committed here under the lease, per the recorded procedure those gates' records state. The retained P2-S5 evidence is NOT committed and NOT touched - it is outside the allowlist and negative criterion N3 fires on it, as its falsification run shows.
- Deviations: no repair sequence ran. Every declared command was green on its first run at this gate, so `repair_attempts` is empty and `repair_limit` is unspent. No Codex consult was needed or made.
- Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; shell Git Bash MINGW64 with Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL /usr/bin/python3 with CPython 3.12.3. The selftest writes its seeds to a temporary directory OUTSIDE every repository (tempfile.mkdtemp), which gate-2-contract permits explicitly and which this row names. environment=mixed-see-prose: the tool runs on the Windows host and the WSL half is evidence.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S6
gate: 2
environment: mixed-see-prose
executor: Claude Lead
base_sha: 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
active_branch: slice/P2-S6
started_at: "2026-08-30T02:58:49Z"
ended_at: "2026-08-30T03:12:32Z"
result: needs_approval
checks:
  - name: plan-approval-verified
    command: "gh api repos/MianliWang/gatebraid/issues/comments/5466316139 (author observed, compared against gh api user)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-E1-approval.json"
  - name: writer-lease-taken
    command: "Writer Lease field write and read-back"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-E2-lease.json"
  - name: baseline-reread
    command: "git rev-parse refs/remotes/origin/main; git diff --name-only X..Y"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-E3-baseline-Y.json"
  - name: active-branch-created-from-Y
    command: "git rev-parse --abbrev-ref HEAD"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-E4-branch.json"
  - name: D1-corpus-digest-unmoved
    command: "fixtures/runner-selftest.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-D1-corpus-digest.json"
  - name: D2-frozen-corpus-passes-unchanged
    command: "fixtures/run-corpus.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-D2-corpus.json"
  - name: D3-snapshot-selftest-windows
    command: "bin/gatebraid-snapshot-selftest.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-D3-selftest-windows.json"
  - name: D4-snapshot-selftest-wsl
    command: "wsl.exe -e bash -lc \"cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-snapshot-selftest.py\""
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-D4-selftest-wsl.json"
  - name: D5-live-smoke-snapshot
    command: "gatebraid-capture.py -- gatebraid-snapshot.py --out g2-snapshot.json --generated-at (measured)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-live-smoke-snapshot.json"
  - name: D6-live-smoke-frontier
    command: "gatebraid-capture.py -- gatebraid-frontier.py g2-snapshot.json --out g2-frontier-report.json"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-live-smoke-frontier.json"
  - name: D7-negative-criteria-hold
    command: "g1/negative-criteria.py (real diff against the frozen base)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-D7-negative.json"
  - name: D8-negative-criteria-falsified
    command: "g1/negative-criteria.py --changed-from SEED --code-surface-dir g1/falsification (all five must fire)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-D8-negative-falsify.json"
  - name: allowlist-respected
    command: "git diff --name-only 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8..5386ce382bac5b4bc1c76a38bcbe86717adf9c1c"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-fp-diff.json"
  - name: closed-set-sweep-falsified
    command: "g2/checks-g2-closed-set-sweep.py (seeded domain; must fire on the repository, node and issue limbs)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-closed-set-sweep-falsify.json"
  - name: closed-set-sweep-over-captures
    command: "g2/checks-g2-closed-set-sweep.py docs/evidence/gatebraid/P2-S6/g2/captures"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-closed-set-sweep.json"
  - name: gate2-record-machine-validated
    command: "bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S6/gate2.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-record-validation.json"
  - name: review-five-items
    command: "R1-R5, by an independent read-only reviewer; NOT run by the implementing session"
    result: not_run
    output_ref: "#review-record"
handoff_fingerprint:
  active_branch_head: "5386ce382bac5b4bc1c76a38bcbe86717adf9c1c"
  tree_sha: "3f88cc11fd11292d7225cb1c914dc860b8956646"
  changed_paths:
    - bin/gatebraid-snapshot-selftest.py
    - bin/gatebraid-snapshot.py
consults: []
repair_attempts: []
approvals:
  - type: "Plan Approval (G1→G2)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/19#issuecomment-5466316139"
    author: "MianliWang"
plan_hash: "4435c71eaf08bf0605815e5960c8093c4698babf99ae8a7030d05ebe445671d0"
allowlist_hash: "8938efcce4b8b863b14f7a503c808d7c2c67d2975aad180fd153fd45cc6da291"
evidence_files:
  - docs/evidence/gatebraid/P2-S6/gate2.md
notes: "Implementation of the frozen plan's T1, T2 and T3. The plan and allowlist are UNCHANGED - no correct-course, no re-freeze - so both hashes carry their Gate 1 values. The two defects are repaired in the two layers the plan named, and the classifier, the assembly and the whole replay transport are untouched: every pre-existing selftest condition stays green, which is the regression evidence the plan nominated. The Plan Approval was targeted BY COMMENT ID, never by matching words or hashes, because Gate 1's own handoff comment carries both hashes and the phrase `Plan Approval` and an id-anchored fetch cannot read the gate's own exit as consent. Review verdicts are absent by design and belong to an independent reviewer."
```
