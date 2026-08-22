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
unexpected dispositions       : 0
positive controls with semantic findings : 0

CORPUS CLEAN: every declared case reached its recorded disposition and locus set
unexpected dispositions       : 0
  exit=0
```

*V12 — T7 WSL*
```
$ wsl -e python3 bin/gatebraid-validate.py --corpus fixtures
unexpected dispositions       : 0
positive controls with semantic findings : 0

CORPUS CLEAN: every declared case reached its recorded disposition and locus set
unexpected dispositions       : 0
  exit=0
```

*V13 — T9 Windows — Task C: the N2 re-validation run to completion (acceptance boxes 2 and 3)*
```
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py C:/Python312/python 'docs/evidence/gatebraid/P2-S1/captures/*.json' docs/evidence/gatebraid/P2-S1/gate0.json docs/evidence/gatebraid/P2-S1/gate1.md docs/evidence/gatebraid/P2-S1/gate2.md docs/evidence/gatebraid/P2-S1/gate3.md
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
| R1 allowlist confinement | | V16 and the `changed_paths` array; `git status --porcelain --untracked-files=all` at review time |
| R2 test-plan coverage | | V1–V15, mapped item by item in the frozen plan's acceptance mapping |
| R3 evidence is rows that reproduce | | every row above is a command and its generated output; the deterministic subset is V16 and the freeze hashes |
| R4 negative criterion | | N1 at V16; N2 at V3; N3 by the module-level import scan of the two subject files |
| R5 no prohibited action | | no push, PR, tag or merge; no dependency installed; no second writer; the lease at E2 |

**The verdict column is deliberately empty.** Review 1 has not run: it is a
fresh read-only window under its own dispatch, and a gate does not transcribe
a verdict nobody reached. `checks[].review-five-items` is recorded `not_run`
rather than `pass` for the same reason — `not_run` means the thing exists and
was not executed, which is exactly the state.

- Reviewer write disclosure: *(to be recorded by Review 1)*
- Rules given to the reviewer: *(to be recorded by Review 1)*

## Repair record

No repair attempt was made. Every declared test command reached its frozen
expected-green state on its first run, so the repair sequence was never
entered and `repair_attempts` is empty. `repair_limit` remains 2, unspent.

## Required disclosures

- Deviations: **`bin/__pycache__/` was created and removed inside this gate.** The standing rule is `PYTHONDONTWRITEBYTECODE=1` on every Python invocation; it was set on every Windows invocation but does **not** cross into WSL, which inherits none of the Windows process environment, so the WSL halves of T1, T3, T5, T7 and T9 wrote bytecode for the two files they executed. Measured, not inferred: `wsl -e printenv PYTHONDONTWRITEBYTECODE` returns empty. The directory was removed before the first commit and no `.pyc` reached the index; it is disclosed here because a write created and removed inside a gate is invisible to the diff and R1 exists to catch exactly that (friction #107). `__pycache__` is not in this repository's `.gitignore` — a pre-existing gap outside this Slice's frozen allowlist, reported and not fixed. The corpus digest is unaffected and V10 confirms it: the runner's own seed set asserts the digest ignores interpreter output · **a raw GraphQL response was written into `captures/` with a shell redirect during entry and removed.** It was not an `evidence-capture@1` record and did not belong in a directory whose contract is that every file is one; T8 caught it as an exit-2 input error, which is the sweep doing its job on its own evidence. It was replaced by a proper capture, `G2-entry-readback`, whose field values are unchanged since entry; both the creation and the removal are disclosed here · the capture tool's `--form shell` was not used: it returned `STRUCTURE: the command could not be executed (FileNotFoundError)` on this host at Gate 1 and the behaviour was not investigated, because inspecting the capture tool beyond its documented interface is a STOP-and-ask under the ratified isolation rule; every capture here is argv form · **T8 does not include the captures written after it ran** — its own capture, the fingerprint and changed-path captures, and this record — the same inherent boundary a sweep always has over its own output · **T8 is not a clean sweep and was not made one.** Six documents are rejected: five at `/streams/stdout/rendered/text` and one at `/notes`. Both loci are outside the frozen exemption by design. `rendered.text` is not re-derived from `data` anywhere in the validator, so exempting it would delete the only check that field has; the `/notes` case is this gate's own lease note, which quotes the lease *format* in angle brackets, and angle-bracket stand-ins never qualify as a mention. The frozen plan predicted this state and the Plan Approval endorsed the prediction as binding acceptance semantics · **commit messages carry a `Co-Authored-By` trailer**, which prior commits in this repository do not; it is added per the executing harness's standing instruction and is noted so the change in convention is not mistaken for drift.
- Reviewer write disclosure: *(to be recorded by Review 1)*
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
ended_at: "2026-08-22T05:35:00Z"
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
    result: not_run
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
repair_attempts: []
approvals:
  - type: "Plan Approval (G1→G2)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5378088991"
    author: "MianliWang"
    at: "2026-08-22T05:06:55Z"
plan_hash: "eb89d3eaedc2690babb3086e3be7529f62fa03e7195746b3b8106ad85a626b18"
allowlist_hash: "81a0bb015ffbc5f3f6a27abfaec0a089c2b5522aa69e5ee30d5d7a01ecd404c0"
evidence_files:
  - docs/evidence/gatebraid/P2-S3/gate2.md
notes: "Implementation of the frozen plan; no repair attempt was entered. result is needs_approval, never passed: passed is the Release Approval's to grant after Review 1, and this gate does not grade itself. The Review 1 verdict column is left empty and review-five-items is not_run for the same reason. Task C, the N2 re-validation, ran to completion on both declared platforms with identical results (V13, V14): every P2-S1 capture accepted and all four of its gate records READ, with the only surviving findings the historical records' own - gate0.json's #171-class command citations and gate3.md's elision - recorded and not repaired, as the grant requires. That discharges the remainder the P2-S2 closure left owed. The corpus digest is unmoved at f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686 and the digest's scope does not cover bin/, so this Slice's allowlist could not have moved it. No push, PR, tag or merge; publication is Gate 3."
```
