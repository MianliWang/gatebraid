# Gate 2 evidence — P2-S3

## Entry records

**E1 — Plan Approval verified** (author must be `MianliWang`, not this
session — ADR-0020 §4; hashes must match the frozen values)
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5378088991 --jq '{author: .user.login, url: .html_url, created: .created_at, updated: .updated_at, association: .author_association}'
{"association":"OWNER","author":"MianliWang","created":"2026-08-22T05:06:55Z","updated":"2026-08-22T05:06:55Z","url":"https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5378088991"}
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login
mianliwang492-source
```
The author `MianliWang` is not the executor `mianliwang492-source`, so the
approval was not written by the session it authorises. `created_at` equals
`updated_at`, so the grant that was posted is the grant that was read: an
approval edited after posting is not the approval that was given. Both frozen
hashes appear in the approval body — `plan_hash` `eb89d3eaedc2690babb3086e3be7529f62fa03e7195746b3b8106ad85a626b18`
and `allowlist_hash` `81a0bb015ffbc5f3f6a27abfaec0a089c2b5522aa69e5ee30d5d7a01ecd404c0`.

**E2 — Writer Lease taken, read back**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f query=mutation($p:ID!,$i:ID!,$f:ID!,$t:String!){updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,value:{text:$t}}){projectV2Item{id}}} -f p=PVT_kwHOBRofUs4Beum7 -f i=PVTI_lAHOBRofUs4Beum7zg3i6M0 -f f=PVTF_lAHOBRofUs4Beum7zhZJcSU -f t=RoughEgoist:p2s3-gate2-claude-lead:2026-08-22T05:08:51Z
{"data":{"updateProjectV2ItemFieldValue":{"projectV2Item":{"id":"PVTI_lAHOBRofUs4Beum7zg3i6M0"}}}}
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query= query($item:ID!){ node(id:$item){ ... on ProjectV2Item { content{ ... on Issue { number labels(first:20){ nodes{ name } } } } fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldTextValue{ text field{ ... on ProjectV2FieldCommon{ name } } } ... on ProjectV2ItemFieldSingleSelectValue{ optionId field{ ... on ProjectV2FieldCommon{ name } } } } } } } }' -F item=PVTI_lAHOBRofUs4Beum7zg3i6M0
{"Writer Lease": "RoughEgoist:p2s3-gate2-claude-lead:2026-08-22T05:08:51Z"}
```

**E3 — baseline re-read** (ADR-0011 §9; ADR-0014 §1 excludes
`docs/evidence/gatebraid/P2-S3/` before the intersection)
```
$ git ls-remote origin refs/heads/main
63c8401f5df6ba446cf002232fcb280673c28e00	refs/heads/main
```
- X, the plan baseline recorded in `gate0.md`: `63c8401f5df6ba446cf002232fcb280673c28e00`
- Y, the head of the base branch now: `63c8401f5df6ba446cf002232fcb280673c28e00`
- baseline: `unchanged`

`X == Y`, so the plan's assumptions are intact and no changed-path set exists
to intersect with the frozen allowlist. The outcome is recorded here because
the contract requires it in every case, including no change. The `Base SHA`
field already carried this value from setup, and its agreement with `Y` was
confirmed before the branch was cut.

**E4 — Active Branch created from Y; `Base SHA` field set to Y**
```
$ git checkout -b slice/P2-S3 63c8401f5df6ba446cf002232fcb280673c28e00

```
`Active Branch` = `slice/P2-S3`, `Base SHA` = `63c8401f5df6ba446cf002232fcb280673c28e00` — both read back at E-exit.

## Verification outputs

*V1 — T1 Windows: the heuristic accepts what it wrongly rejected (acceptance box 1, positive direction)*
```
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py C:/Python312/python 'docs/evidence/gatebraid/P2-S1/captures/*.json'
interpreter   : C:/Python312/python
documents     : 36
SWEEP COMPLETE rejected_or_errored=0
  exit=0
```

*V2 — T1 WSL: the same, on the second declared platform*
```
$ wsl -e python3 docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py python3 'docs/evidence/gatebraid/P2-S1/captures/*.json'
interpreter   : python3
documents     : 36
SWEEP COMPLETE rejected_or_errored=0
  exit=0
```

*V3 — T2: a genuine elision still rejects (acceptance box 1, negative direction; negative criterion N2)*
```
$ C:/Python312/python bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S1/gate0.json
[elided: 17 of 20 output lines shown; the full output is committed at
docs/evidence/gatebraid/P2-S3/captures/G2-T2-windows.json]
target        : docs/evidence/gatebraid/P2-S1/gate0.json
interface     : gatebraid/gate-run@2
loader        : CPython 3.12.2 (C:\Python312\python.exe), jsonschema 4.23.0, Draft202012Validator
[3 further lines elided here]
   semantic         6
   replayed         0
   capture-trusted  0
findings      : 9
   F001     /checks/5/command                              placeholder-survives-its-own-check
   F002     /checks/13/command                             placeholder-survives-its-own-check
   F003     /checks/14/command                             placeholder-survives-its-own-check
   F004     /checks/15/command                             placeholder-survives-its-own-check
   F005     /checks/23/command                             placeholder-survives-its-own-check
   F006     /checks/24/command                             placeholder-survives-its-own-check
   F007     /checks/25/command                             placeholder-survives-its-own-check
   F008     /checks/27/command                             placeholder-survives-its-own-check
   F009     /checks/28/command                             placeholder-survives-its-own-check
verdict       : rejected
  exit=1
```

*V4 — T3 Windows: the markdown mode reads what it could not read (acceptance box 2)*
```
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py C:/Python312/python docs/evidence/gatebraid/P2-S1/gate1.md docs/evidence/gatebraid/P2-S1/gate2.md docs/evidence/gatebraid/P2-S1/gate3.md
interpreter   : C:/Python312/python
documents     : 3
gate3.md rc=1
   F001     /checks/1/command                              placeholder-survives-its-own-check
SWEEP COMPLETE rejected_or_errored=1
  exit=1
```

*V5 — T3 WSL*
```
$ wsl -e python3 docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py python3 docs/evidence/gatebraid/P2-S1/gate1.md docs/evidence/gatebraid/P2-S1/gate2.md docs/evidence/gatebraid/P2-S1/gate3.md
interpreter   : python3
documents     : 3
gate3.md rc=1
   F001     /checks/1/command                              placeholder-survives-its-own-check
SWEEP COMPLETE rejected_or_errored=1
  exit=1
```

*V6 — T4 seed 1: an invalid embedded record is rejected, not merely read*
```
$ C:/Python312/python bin/gatebraid-validate.py --record C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/0846d62b-0514-43be-8d3b-c1ee296ee47c/scratchpad/t4-invalid.md
[elided: 8 of 13 output lines shown; the full output is committed at
docs/evidence/gatebraid/P2-S3/captures/G2-T4-invalid.json]
target        : C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/0846d62b-0514-43be-8d3b-c1ee296ee47c/scratchpad/t4-invalid.md
interface     : gatebraid/gate-run@2
loader        : CPython 3.12.2 (C:\Python312\python.exe), jsonschema 4.23.0, Draft202012Validator
[5 further lines elided here]
   replayed         0
   capture-trusted  0
findings      : 1
   F001     /base_sha                                      structural:pattern
verdict       : rejected
  exit=1
```

*V7 — T4 seed 2: a file that is not a record stays an input error (the pre-existing broken-input condition does not regress)*
```
$ C:/Python312/python bin/gatebraid-validate.py --record C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/0846d62b-0514-43be-8d3b-c1ee296ee47c/scratchpad/t4-notarecord.md

  exit=2
```

*V8 — T5 Windows: the selftest, carrying both repairs in both directions (acceptance box 4)*
```
$ C:/Python312/python bin/gatebraid-validate-selftest.py
[elided: 14 of 40 output lines shown; the full output is committed at
docs/evidence/gatebraid/P2-S3/captures/G2-T5-windows.json]
S23    GraphQL spread in argv is a mention            0     0  PASS    a captured command may contain an ellipsis because the command did
S24    elided command text still rejects              1     1  PASS    an ellipsis standing alone replaces omitted text and stays a finding
S25    id abbreviation in notes is a mention          0     0  PASS    an ellipsis bounded by identifier characters abbreviates, it does not elide
S26    ellipsis outside a quoting field rejects       1     1  PASS    the exemption is scoped to command and citation loci, not to the document
S27    markdown gate record is read                   0     0  PASS    the ADR-0026 record form its own contracts mandate must be readable
S28    invalid embedded record rejects                1     1  PASS    reading a record is not accepting it; the schema still governs
S29    markdown without a block is an input error     2     2  PASS    a broken input must not become a record by being markdown
S30    heading without a fence is an input error      2     2  PASS    a half-formed record fails closed rather than validating an empty document

scratch directory             : outside every repository (tempfile.mkdtemp)
validator under test          : D:\Github repo\Gatebraid\bin\gatebraid-validate.py
interpreter                   : C:\Python312\python.exe
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
  exit=0
```

*V9 — T5 WSL*
```
$ wsl -e python3 bin/gatebraid-validate-selftest.py
[elided: 6 of 40 output lines shown; the full output is committed at
docs/evidence/gatebraid/P2-S3/captures/G2-T5-wsl.json]

scratch directory             : outside every repository (tempfile.mkdtemp)
validator under test          : /mnt/d/Github repo/Gatebraid/bin/gatebraid-validate.py
interpreter                   : /usr/bin/python3
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
  exit=0
```

*V10 — T6: the frozen corpus is unmoved (acceptance box 4; friction #165 budget case, 420,000 ms, measured 147,993 ms)*
```
$ C:/Python312/python fixtures/runner-selftest.py
[elided: 7 of 37 output lines shown; the full output is committed at
docs/evidence/gatebraid/P2-S3/captures/G2-T6-windows.json]

digest scope                  : bytes-platform, evidence-capture-v1, gate-run-v2, instruments, metrics-v1, CORPORA.json, schema, run-corpus.py, runner-selftest.py, fixtures/ listing
digest before                 : f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686
digest after                  : f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686
seed-reachable surface UNMODIFIED: True
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
  exit=0
```

*V11 — T7 Windows: the corpus mutation suite still passes*
```
$ C:/Python312/python bin/gatebraid-validate.py --corpus fixtures
[elided: 5 of 126 output lines shown; the full output is committed at
docs/evidence/gatebraid/P2-S3/captures/G2-T7-windows.json]
unexpected dispositions       : 0
positive controls with semantic findings : 0

CORPUS CLEAN: every declared case reached its recorded disposition and locus set
unexpected dispositions       : 0
  exit=0
```

*V12 — T7 WSL*
```
$ wsl -e python3 bin/gatebraid-validate.py --corpus fixtures
[elided: 5 of 126 output lines shown; the full output is committed at
docs/evidence/gatebraid/P2-S3/captures/G2-T7-wsl.json]
unexpected dispositions       : 0
positive controls with semantic findings : 0

CORPUS CLEAN: every declared case reached its recorded disposition and locus set
unexpected dispositions       : 0
  exit=0
```

*V13 — T9 Windows — Task C: the N2 re-validation run to completion (acceptance boxes 2 and 3)*
```
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py C:/Python312/python 'docs/evidence/gatebraid/P2-S1/captures/*.json' docs/evidence/gatebraid/P2-S1/gate0.json docs/evidence/gatebraid/P2-S1/gate1.md docs/evidence/gatebraid/P2-S1/gate2.md docs/evidence/gatebraid/P2-S1/gate3.md
[elided: 14 of 15 output lines shown; the full output is committed at
docs/evidence/gatebraid/P2-S3/captures/G2-T9-windows.json]
documents     : 40
gate0.json rc=1
   F001     /checks/5/command                              placeholder-survives-its-own-check
   F002     /checks/13/command                             placeholder-survives-its-own-check
   F003     /checks/14/command                             placeholder-survives-its-own-check
   F004     /checks/15/command                             placeholder-survives-its-own-check
   F005     /checks/23/command                             placeholder-survives-its-own-check
   F006     /checks/24/command                             placeholder-survives-its-own-check
   F007     /checks/25/command                             placeholder-survives-its-own-check
   F008     /checks/27/command                             placeholder-survives-its-own-check
   F009     /checks/28/command                             placeholder-survives-its-own-check
gate3.md rc=1
   F001     /checks/1/command                              placeholder-survives-its-own-check
SWEEP COMPLETE rejected_or_errored=2
  exit=1
```

*V14 — T9 WSL: Task C on the second declared platform*
```
$ wsl -e python3 docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py python3 'docs/evidence/gatebraid/P2-S1/captures/*.json' docs/evidence/gatebraid/P2-S1/gate0.json docs/evidence/gatebraid/P2-S1/gate1.md docs/evidence/gatebraid/P2-S1/gate2.md docs/evidence/gatebraid/P2-S1/gate3.md
[elided: 14 of 15 output lines shown; the full output is committed at
docs/evidence/gatebraid/P2-S3/captures/G2-T9-wsl.json]
documents     : 40
gate0.json rc=1
   F001     /checks/5/command                              placeholder-survives-its-own-check
   F002     /checks/13/command                             placeholder-survives-its-own-check
   F003     /checks/14/command                             placeholder-survives-its-own-check
   F004     /checks/15/command                             placeholder-survives-its-own-check
   F005     /checks/23/command                             placeholder-survives-its-own-check
   F006     /checks/24/command                             placeholder-survives-its-own-check
   F007     /checks/25/command                             placeholder-survives-its-own-check
   F008     /checks/27/command                             placeholder-survives-its-own-check
   F009     /checks/28/command                             placeholder-survives-its-own-check
gate3.md rc=1
   F001     /checks/1/command                              placeholder-survives-its-own-check
SWEEP COMPLETE rejected_or_errored=2
  exit=1
```

*V15 — T8: the self-validation point — the repaired validator over this Slice's own evidence, discharging the state packet §5 disclosed limit*
```
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py C:/Python312/python 'docs/evidence/gatebraid/P2-S3/captures/*.json' docs/evidence/gatebraid/P2-S3/gate0.md docs/evidence/gatebraid/P2-S3/gate1.md
interpreter   : C:/Python312/python
documents     : 83
G0-slice-body.json rc=1
   F001     /streams/stdout/rendered/text                  placeholder-survives-its-own-check
G1-exit-fields-readback.json rc=1
   F001     /streams/stdout/rendered/text                  placeholder-survives-its-own-check
G1-writedomains-edit.json rc=1
   F001     /streams/stdout/rendered/text                  placeholder-survives-its-own-check
G1-writedomains-readback.json rc=1
   F001     /streams/stdout/rendered/text                  placeholder-survives-its-own-check
G2-entry-readback.json rc=1
   F001     /streams/stdout/rendered/text                  placeholder-survives-its-own-check
G2-lease-take.json rc=1
   F001     /notes                                         placeholder-survives-its-own-check
SWEEP COMPLETE rejected_or_errored=6
  exit=1
```

**V16 — the handoff fingerprint, both ends pinned**
```
$ git rev-parse 28d5dfcd83b83b7541a3d8f73732fb833a3d119c 28d5dfcd83b83b7541a3d8f73732fb833a3d119c^{tree}
28d5dfcd83b83b7541a3d8f73732fb833a3d119c
3012c2a70b053721f61f99bb5e2e1c41cdbc7408
$ git diff --name-only 63c8401f5df6ba446cf002232fcb280673c28e00 28d5dfcd83b83b7541a3d8f73732fb833a3d119c
[elided: 6 of 93 changed paths shown; the full sorted set is the
 `changed_paths` array of the metadata block below, and the full output is
 committed at docs/evidence/gatebraid/P2-S3/captures/G2-changed-paths.json]
bin/gatebraid-validate-selftest.py
bin/gatebraid-validate.py
docs/evidence/gatebraid/P2-S3/captures/G0-baseline-main.json
docs/evidence/gatebraid/P2-S3/captures/G0-closed-set-sweep.json
docs/evidence/gatebraid/P2-S3/captures/G0-exit-fields-readback.json
docs/evidence/gatebraid/P2-S3/captures/G0-head.json
```

## Review record

### Review 1

| Item | Verdict | Evidence |
|---|---|---|
| R1 allowlist confinement | **PASS** | §R1 — both diffs re-run; `changed_paths` byte-equal to the committed capture at sha256 `4d856126…9215b45f`; 0 of 99 paths outside the frozen allowlist; porcelain empty; both in-gate writes disclosed |
| R2 test-plan coverage | **PASS** | §R2 — issue `#12`'s four boxes read live and mapped item by item to committed captures; box 1's "11" independently reproduced exactly |
| R3 evidence is rows that reproduce | **FAIL** | §R3 — every deterministic row reproduces byte-exactly and nothing is transcribed, **but nine V-rows elide without `shown/total`** (F-1) |
| R4 negative criteria (N1, N2, N3) | **PASS** | §R4 — N1 by diff + `ls-tree` blob identity; N2 re-run rejects with nine findings at `/checks/N/command`; N3 proven by AST |
| R5 no prohibited action | **PASS** | §R5 — no remote ref, no PR, no tag, no merge, no install, no disabled hook, no second writer |

**Findings** — Review 1's own one-line summaries, read from the report:

- F-1 — nine V-rows elide without `shown/total` or an in-row path. Material. Drives the R3 FAIL.
- F-2 — the frozen plan's `gate3.md` expectation was wrong when frozen. Material to the plan, not to the work.
- F-3 — the `bin/__pycache__` disclosure's attribution does not reproduce. Minor; errs in the safe direction.
- F-4 — Task A's descriptive prose over-counts `gate0.json` by one. Minor.
- F-5 — explanatory prose outside ADR-0026 §1's content classes. Observation, not a P2-S3 defect.
- F-6 — T8 re-run now returns seven rejections, not six. Not a defect.

- Reviewer: `Claude Read-Only Team`, a fresh read-only window under its own dispatch. Source: `_handoff/batch-p2s3/REVIEW1-M3-P2S3.md`, sha256 `dab4ae857e60388a9bed0f093eead9e2b2ee0725ebf4b2ffc97444e508fad6c3`, 40494 bytes. Every row of the table above and every summary above is generated from that file, not retyped.
- Reviewer write disclosure: one write, `_handoff/batch-p2s3/REVIEW1-M3-P2S3.md`, on the ignored `_handoff/` path — no commit, no tracked-file edit, no `gh` mutation, no label, field or comment operation, no lease taken. The five WSL halves it re-ran in recorded form wrote no bytecode, verified after each run and by an empty `--untracked-files=all` porcelain at the end.
- Rules given to the reviewer: the spec §4 conduct rules, enumerated in full at the report's own `## Conduct rules this review was given` — measure never declare; cite never restate; never echo a forbidden value into the record, name loci and counts; a bare zero states what it searched; closed-set by complement with the ruled touch-vs-mention distinction; the capture pair never read, only executed; `GH_CONFIG_DIR` pinned per call and identity checked first and alone; `PYTHONDONTWRITEBYTECODE=1` with the measured caveat that it does not cross `wsl -e`; dash and arrow marks never retyped; business repositories untouchable; single writer; STOP and ask on any uncertainty.

## Repair record

### Repair 1

- Finding addressed: **F-1**, the finding Review 1's R3 fail rests on — nine
  rows showed a window smaller than their capture with no `shown/total` and
  no committed path in the row.
- Hypothesis (new): the rule was broken at RENDER rather than at measurement
  — the row writer emitted a tail window and never a marker, so every row
  whose window was smaller than its capture elided silently.
- Remedy: the row writer now emits `shown/total` and the capture's committed
  path whenever the window is smaller than the capture, and can hold a
  capture's opening lines when the row must carry them. Every restored line
  is read from the capture bytes by the instrument, never retyped.

**Novelty measured** (ADR-0027 §1: an unchanged tree is not a repair. The
comparand is the state Review 1 failed, named by full sha, never by `HEAD`.)
```
$ git rev-parse 43022db1721940bfdcd0abcc9c55b150b77fa89d^{tree}
3d934d46c18e7c68bad01974bd4a0ac8e0ebbef0
$ git rev-parse 43022db1721940bfdcd0abcc9c55b150b77fa89d:docs/evidence/gatebraid/P2-S3/checks/g2_render_record.py
2e91706f1bf36d4f60f0622888d4979b93f6bd2a
$ git hash-object docs/evidence/gatebraid/P2-S3/checks/g2_render_record.py
3786265b60156bf197f5055715cbd1e5f2b35bc8
```
The render instrument's blob differs from the one the failed state carried, so
the amended tree cannot equal `3d934d46c18e7c68bad01974bd4a0ac8e0ebbef0`.
This renderer exits 3 rather than grade a repair green when those two blob ids
are equal.

- Changed by this repair: `docs/evidence/gatebraid/P2-S3/gate2.md` and
  `docs/evidence/gatebraid/P2-S3/checks/g2_render_record.py` — record text and the
  instrument that generates it, both inside the frozen allowlist. No `bin/`
  file, no frozen-plan text, no historical record, and no capture: the
  measurements are the ones Review 1 already re-ran and confirmed.
- Result: `green`
- Consult: `none`

`repair_limit` is 2; this is attempt 1, so one attempt remains unspent.

## Required disclosures

- Deviations: **`bin/__pycache__/` was created and removed inside this gate, and the attribution this record first carried for it is WITHDRAWN (Review 1's F-3).** The standing rule is `PYTHONDONTWRITEBYTECODE=1` on every Python invocation; it was set on every Windows invocation and does **not** cross into WSL, which inherits none of the Windows process environment. That much is measured, and measured twice — at this gate and again by Review 1: `wsl -e printenv PYTHONDONTWRITEBYTECODE` returns empty. What is withdrawn is the sentence that followed it, that the WSL halves of T1, T3, T5, T7 and T9 wrote the bytecode. Review 1 ran all five in their recorded form and none wrote any, and the mechanism says why: `g1_sweep.py` and the selftest reach the validator by `subprocess.run`, so no module under `bin/` is ever imported and no bytecode can be generated there, while `fixtures/run-corpus.py` documents that importing the corpus instruments writes `fixtures/__pycache__/` — a different path, which that runner excludes by name. The claim was an inference from a true premise, presented as a measurement. What stands: the directory was observed, it was removed before the first commit, and no `.pyc` reached the index. What is undetermined: what created it. The error direction was OVER-disclosure — this record disclosed a write more broadly than it occurred, which is the safe direction and the opposite of the failure R1 exists to catch (friction #107). A CANDIDATE mechanism was measured while repairing this record and is offered as a candidate only, not as a finding of cause: `python -m py_compile` writes `__pycache__/` beside its target even with `PYTHONDONTWRITEBYTECODE=1` set, because explicit compilation is not import-time caching. It was reproduced on a file in a scratch directory outside every repository. Whether anything of that shape ran against `bin/` at this gate is not known and is not claimed · **repair 1 itself created and removed `docs/evidence/gatebraid/P2-S3/checks/__pycache__/`**, by the `py_compile` syntax check named above, on this record's own render instrument. It was removed before the amendment commit, no `.pyc` reached the index, and it is disclosed here for the same reason the first one is: a write created and removed inside a gate is invisible to the diff. `__pycache__` is not in this repository's `.gitignore` — a pre-existing gap outside this Slice's frozen allowlist, reported and not fixed. The corpus digest is unaffected and V10 confirms it: the runner's own seed set asserts the digest ignores interpreter output · **a raw GraphQL response was written into `captures/` with a shell redirect during entry and removed.** It was not an `evidence-capture@1` record and did not belong in a directory whose contract is that every file is one; T8 caught it as an exit-2 input error, which is the sweep doing its job on its own evidence. It was replaced by a proper capture, `G2-entry-readback`, whose field values are unchanged since entry; both the creation and the removal are disclosed here · the capture tool's `--form shell` was not used: it returned `STRUCTURE: the command could not be executed (FileNotFoundError)` on this host at Gate 1 and the behaviour was not investigated, because inspecting the capture tool beyond its documented interface is a STOP-and-ask under the ratified isolation rule; every capture here is argv form · **T8 does not include the captures written after it ran** — its own capture, the fingerprint and changed-path captures, and this record — the same inherent boundary a sweep always has over its own output · **T8 is not a clean sweep and was not made one.** Six documents are rejected: five at `/streams/stdout/rendered/text` and one at `/notes`. Both loci are outside the frozen exemption by design. `rendered.text` is not re-derived from `data` anywhere in the validator, so exempting it would delete the only check that field has; the `/notes` case is this gate's own lease note, which quotes the lease *format* in angle brackets, and angle-bracket stand-ins never qualify as a mention. The frozen plan predicted this state and the Plan Approval endorsed the prediction as binding acceptance semantics · **commit messages carry a `Co-Authored-By` trailer**, which prior commits in this repository do not; it is added per the executing harness's standing instruction and is noted so the change in convention is not mistaken for drift · **the frozen plan's `gate3.md` expectation was wrong when frozen (Review 1's F-2), and is reconciled HERE rather than in the frozen text.** The plan states at T3, and again at T9, that `docs/evidence/gatebraid/P2-S1/gate3.md` is rejected on its own **two** `/checks/N/command` elisions. Measured, on both declared platforms: **one** finding, at the single locus `/checks/1/command`. The document does carry two elisions, but both sit in one string at that one locus, and `check_placeholders` emits at most one finding per string value — behaviour that PREDATES this Slice's repair, where the walk was a single search per string. The mention count for that document is zero, so nothing was reclassified as a mention: the count is what the instrument emits, not what the exemption suppressed. The Gate 2 report's `one` is the measured value and stands. The plan section is deliberately NOT edited: it is frozen under `plan_hash`, its author had not measured this when it was frozen, and a later measurement belongs in a record rather than in a silently rewritten plan — the same treatment this gate already gave the T6 WSL timing · **the frozen plan's `gate0.json` citation count is off by one (Review 1's F-4), corrected HERE for the same reason.** Task A's prose reads as nine ellipsis-form citations plus one angle-bracket stand-in, which is ten. Measured, the population is nine in total: eight ellipsis-kind, and one angle-bracket-kind at `/checks/5/command`. The negative criterion N2's own count of nine was exact throughout, and nine is what every run of T2 and T9 reproduces; only the surrounding prose over-counted.
- Reviewer write disclosure: one write, `_handoff/batch-p2s3/REVIEW1-M3-P2S3.md`, on the ignored `_handoff/` path — no commit, no tracked-file edit, no `gh` mutation, no label, field or comment operation, no lease taken; the five WSL halves Review 1 re-ran wrote no bytecode. This gate's own writes are disclosed above.
- Environment: Windows 11 host, Git Bash (MSYS2) shell, with the WSL half of `mixed-see-prose` exercised for T1, T3, T5, T7 and T9; Windows loader `C:\Python312\python.exe` (CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0), WSL `/usr/bin/python3` (3.12.3, PyYAML 6.0.1, jsonschema 4.10.3); `PYTHONDONTWRITEBYTECODE=1` on every Windows Python invocation and, as disclosed above, not inherited by WSL; `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` call; every `gh api` endpoint written without a leading slash (friction #33); the T4 seeds were written to a scratch path outside every repository, as the contract requires such a path to be named.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S3
gate: 2
environment: mixed-see-prose
executor: Claude Lead
base_sha: 63c8401f5df6ba446cf002232fcb280673c28e00
active_branch: slice/P2-S3
started_at: "2026-08-22T05:07:00Z"
ended_at: "2026-08-22T07:26:00Z"
result: needs_approval
checks:
  - name: plan-approval-verified
    command: "gh api repos/MianliWang/gatebraid/issues/comments/5378088991 --jq '{author,url,created,updated}'"
    result: pass
    output_ref: "#entry-records"
  - name: writer-lease-taken
    command: "gh api graphql updateProjectV2ItemFieldValue (Writer Lease) + read-back"
    result: pass
    output_ref: "#entry-records"
  - name: baseline-re-read
    command: "git ls-remote origin refs/heads/main"
    result: pass
    output_ref: "#entry-records"
  - name: active-branch-created-from-Y
    command: "git checkout -b slice/P2-S3 63c8401f5df6ba446cf002232fcb280673c28e00"
    result: pass
    output_ref: "#entry-records"
  - name: T1-heuristic-accepts-windows
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T1-windows.json"
  - name: T1-heuristic-accepts-wsl
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T1-wsl.json"
  - name: T2-genuine-elision-still-rejects
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T2-windows.json"
  - name: T3-markdown-records-read-windows
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T3-windows.json"
  - name: T3-markdown-records-read-wsl
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T3-wsl.json"
  - name: T4-invalid-embedded-record-rejected
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T4-invalid.json"
  - name: T4-non-record-stays-input-error
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T4-notarecord.json"
  - name: T5-selftest-windows
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T5-windows.json"
  - name: T5-selftest-wsl
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T5-wsl.json"
  - name: T6-corpus-digest-unmoved
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T6-windows.json"
  - name: T7-corpus-suite-windows
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T7-windows.json"
  - name: T7-corpus-suite-wsl
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T7-wsl.json"
  - name: T9-n2-revalidation-complete-windows
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T9-windows.json"
  - name: T9-n2-revalidation-complete-wsl
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T9-wsl.json"
  - name: T8-self-validation-point
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G2-T8-windows.json"
  - name: review-five-items
    result: fail
    output_ref: "#review-record"
handoff_fingerprint:
  active_branch_head: "28d5dfcd83b83b7541a3d8f73732fb833a3d119c"
  tree_sha: "3012c2a70b053721f61f99bb5e2e1c41cdbc7408"
  changed_paths:
    - bin/gatebraid-validate-selftest.py
    - bin/gatebraid-validate.py
    - docs/evidence/gatebraid/P2-S3/captures/G0-baseline-main.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-closed-set-sweep.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-exit-fields-readback.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-head.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-porcelain-baseline.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-porcelain-full.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-record-falsify-abbrev-sha.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-record-falsify-bootstrap-no-approval.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-record-falsify-check-no-result.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-record-falsify-no-author.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-record-falsify-no-heading.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-record-falsify-unquoted-ts.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-record-validation.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-ref-namespace.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-remote.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-slice-body.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-slice-metadata-falsify-seedA.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-slice-metadata-falsify-seedB.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-slice-metadata-falsify-seedC.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-slice-metadata-validation.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-tools-claude.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-tools-codex.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-tools-gh.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-tools-git.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-tools-python-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G0-tools-python-wsl.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-Q2-approval.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-allowlist-hash.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T1-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T1-wsl.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T2-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T3-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T3-wsl.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T5-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T6-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T7-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T7-wsl.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-exit-fields-readback.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-plan-hash.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-record-validation.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-writedomains-edit.json
    - docs/evidence/gatebraid/P2-S3/captures/G1-writedomains-readback.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T1-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T1-wsl.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T2-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T3-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T3-wsl.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T4-invalid.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T4-notarecord.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T5-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T5-wsl.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T6-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T7-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T7-wsl.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T8-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T9-windows.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-T9-wsl.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-approval-provenance.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-baseline-reread.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-branch-create.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-entry-readback.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-label-remove.json
    - docs/evidence/gatebraid/P2-S3/captures/G2-lease-take.json
    - docs/evidence/gatebraid/P2-S3/captures/Q1-falsify.json
    - docs/evidence/gatebraid/P2-S3/captures/Q1-real.json
    - docs/evidence/gatebraid/P2-S3/captures/Q2-correction.json
    - docs/evidence/gatebraid/P2-S3/captures/Q2-falsify.json
    - docs/evidence/gatebraid/P2-S3/captures/Q2-real.json
    - docs/evidence/gatebraid/P2-S3/captures/Q3-falsify.json
    - docs/evidence/gatebraid/P2-S3/captures/Q3-real.json
    - docs/evidence/gatebraid/P2-S3/captures/Q4-falsify.json
    - docs/evidence/gatebraid/P2-S3/captures/Q4-real.json
    - docs/evidence/gatebraid/P2-S3/captures/Q5-falsify.json
    - docs/evidence/gatebraid/P2-S3/captures/Q5-real-plain.json
    - docs/evidence/gatebraid/P2-S3/captures/Q5-real.json
    - docs/evidence/gatebraid/P2-S3/captures/Q6-falsify.json
    - docs/evidence/gatebraid/P2-S3/captures/Q6-real-ids.json
    - docs/evidence/gatebraid/P2-S3/captures/Q6-real.json
    - docs/evidence/gatebraid/P2-S3/captures/Q7-falsify.json
    - docs/evidence/gatebraid/P2-S3/captures/Q7-real-blockedby.json
    - docs/evidence/gatebraid/P2-S3/captures/Q7-real-blocking.json
    - docs/evidence/gatebraid/P2-S3/checks/g0_closed_set_sweep.py
    - docs/evidence/gatebraid/P2-S3/checks/g0_record_validation.py
    - docs/evidence/gatebraid/P2-S3/checks/g0_render_record.py
    - docs/evidence/gatebraid/P2-S3/checks/g0_slice_metadata.py
    - docs/evidence/gatebraid/P2-S3/checks/g1_hashes.py
    - docs/evidence/gatebraid/P2-S3/checks/g1_render_record.py
    - docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py
    - docs/evidence/gatebraid/P2-S3/gate0.md
    - docs/evidence/gatebraid/P2-S3/gate1-exit-checklist.md
    - docs/evidence/gatebraid/P2-S3/gate1.md
consults: []
repair_attempts:
  - number: 1
    hypothesis: "F-1: the elision rule was broken at RENDER rather than at measurement - the row writer emitted a tail window and never a shown/total marker, so every row whose window was smaller than its capture elided silently."
    result: green
approvals:
  - type: "Plan Approval (G1→G2)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5378088991"
    author: "MianliWang"
    at: "2026-08-22T05:06:55Z"
plan_hash: "eb89d3eaedc2690babb3086e3be7529f62fa03e7195746b3b8106ad85a626b18"
allowlist_hash: "81a0bb015ffbc5f3f6a27abfaec0a089c2b5522aa69e5ee30d5d7a01ecd404c0"
evidence_files:
  - docs/evidence/gatebraid/P2-S3/gate2.md
notes: "Implementation of the frozen plan, then repair 1 under Review 1. result is needs_approval, never passed: passed is the Release Approval's to grant, and this gate does not grade itself. Review 1 returned R1 pass, R2 pass, R3 FAIL on finding F-1, R4 pass, R5 pass; review-five-items is recorded fail because fail is what the review returned, and it is carried rather than smoothed. Repair 1 addresses F-1 and nothing else: every row whose window is smaller than its capture now carries shown/total and the committed path of the full output, V3 and V6 keep the loader line friction #55 requires of a schema-validation row, and V8's window starts at S23 so Task A's positive-direction pair sits in the row a reader checks acceptance box 1 against. No measurement changed and no capture was rewritten - the repair is to how rows are rendered, and every restored line is read from the capture bytes. R3 stays FAIL as reviewed; only Review 1's own re-review may turn it, in its own window, and the Release Approval follows that. The review's F-3, F-2 and F-4 are answered in the disclosures: an over-disclosed write withdrawn, and two frozen-plan counts corrected in the record rather than in the frozen text. Task C, the N2 re-validation, ran to completion on both declared platforms with identical results (V13, V14): every P2-S1 capture accepted and all four of its gate records READ, with the only surviving findings the historical records' own - gate0.json's #171-class command citations and gate3.md's elision - recorded and not repaired, as the grant requires. That discharges the remainder the P2-S2 closure left owed. The corpus digest is unmoved at f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686 and the digest's scope does not cover bin/, so this Slice's allowlist could not have moved it. No push, PR, tag or merge; publication is Gate 3."
```
