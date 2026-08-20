# Gate 1 evidence — P2-S1

## Plan (frozen at exit)

- Approach: land the two committed instruments of the M3 evidence toolchain in
  the control repository (ADR-0032 decision 2), byte-identical to the blobs
  bound at N2-R2, and produce this Slice's gate evidence beside them. Three
  independently verifiable tasks. **K1** — copy
  `_handoff/batch-n2/candidates/bin/gatebraid-capture.py` (43,335 B, blob
  `43ff5a06c7f7e1e9b0ba5d6f14e956bc8d4c73d0`) to `bin/gatebraid-capture.py`
  and `_handoff/batch-n2/candidates/bin/gatebraid-capture-selftest.py`
  (40,846 B, blob `a40869bea3d1e8dbaf20473456f919838f788eec`) to
  `bin/gatebraid-capture-selftest.py`; verified by `git hash-object` equalling
  the bound blob for each. **K2** — produce the Gate 2 evidence under
  `docs/evidence/gatebraid/P2-S1/`, every capture written by the landed
  `bin/gatebraid-capture.py` and every gate record validating against the
  committed `gatebraid/gate-run@2`. **K3** — verify the landed pair against
  the frozen corpus on both declared platforms without moving it. The
  candidates directory, `fixtures/` and `schema/` are READ sources only; no
  write reaches any of them.
- Exact `write_domains` allowlist: `bin/` and
  `docs/evidence/gatebraid/P2-S1/`. Nothing else. `NOTICE.md` is untouched —
  neither file derives from a surveyed framework, so no attribution is owed
  (ADR-0010, ADR-0027).
- Test plan (commands, runnable as written on the declared environment; each
  was dry-run and each row in Records carries its generated output):
  **T1** `C:/Python312/python.exe -B bin/gatebraid-capture-selftest.py` —
  green: exit 0, `SELFTEST CLEAN`, `conditions failed : 0`, and
  `schema cross-check : run` (never `ABSENT`, which is the exit-3 mute class
  N2-R2 closed). **T2** the same selftest under
  `wsl.exe -e bash -lc 'cd "/mnt/d/Github repo/Gatebraid" && python3 -B bin/gatebraid-capture-selftest.py'`
  — green: identical criteria, on jsonschema 4.10.3. **T3**
  `C:/Python312/python.exe -B fixtures/runner-selftest.py` — green: exit 0 and
  `digest before` == `digest after` ==
  `f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686`. **T4**
  `bin/gatebraid-capture.py --verify-record <each capture> --rederive` over
  every file in `docs/evidence/gatebraid/P2-S1/captures/` — green: every record
  exits 0 with `contract: conforms` and `coherence: conforms`. **T5** the
  closed-set complement over `bin` and `docs/evidence/gatebraid/P2-S1` — green:
  exit 0 and `outside []`. **T6** and **T7** are the negative criteria below.
- Risk notes (`risk: low`, and what would have to be true for that to be
  wrong): (1) the two files are self-contained and stdlib-only at module level,
  so no runtime dependency enters the repository — falsified by T7; (2) they
  are additive, touching no existing tracked file — falsified by T6; (3) the
  frozen corpus is a read input and cannot move — falsified by T3, which
  compares the digest before and after; (4) the instruments carry their own
  falsified selftest, whose 46 conditions include the guard-versus-loader
  cross-check on both platforms — falsified by T1 and T2; (5) no contract,
  schema or ADR text changes, so nothing normative moves. `consult_first:
  false` is set deliberately on the same grounds: the diff adds two files
  behind their own falsification and alters no contract.
- Rollback note: nothing is committed until Gate 2, and Gate 2 lands exactly
  two additive files plus an evidence directory. To abandon at any point before
  the Gate 3 merge, delete `bin/` and `docs/evidence/gatebraid/P2-S1/` from the
  working tree and, if commits exist on the slice branch, leave the branch
  unpushed and unmerged — ADR-0025 §3 retains aborted slice branches rather than
  deleting them. No tracked file is modified, so there is nothing to restore
  and no revert to author.
- **Negative criterion (checkable):** **N1 — the landed diff touches no path
  outside `bin/` and `docs/evidence/gatebraid/P2-S1/`.** Scope, stated as an
  explicit path set rather than "the added files" (friction #110): the complete
  output of `git diff --name-only 5bc41d7667d1ae019b228d43ed1ef29ea5c0b928..HEAD`.
  Mechanised proxy T6; it **errs toward false failure** — any path outside the
  two prefixes fails the criterion whether or not it is benign, so a pass is
  informative and a failure requires a human look. **N2 — neither landed file
  imports a third-party module at module level.** Scope: exactly
  `bin/gatebraid-capture.py` and `bin/gatebraid-capture-selftest.py`, parsed
  with `ast` and compared against `sys.stdlib_module_names`. Mechanised proxy
  T7; it **errs toward false failure** — it inspects only module-level
  `Import`/`ImportFrom` nodes, so a guarded optional import inside a function or
  `try` block (which is how the selftest reaches `jsonschema`) is deliberately
  out of scope and passes, while any module-level third-party import fails.

## Records

**P1 — team findings flushed** (only if a read-only team ran)
```
n/a — no read-only team was spawned. gate-1-contract action 2's Agent Team is
optional; it did not run, so there are no findings to flush and no team
constraint could be violated. Recorded rather than omitted.
```

**P2 — dry-run of every declared test command, on the declared environment**

Host: Windows 11 (26200), Git Bash, `C:/Python312/python.exe` CPython 3.12.2,
jsonschema 4.23.0. Second platform: WSL Ubuntu 24.04.4, `/usr/bin/python3`
CPython 3.12.3, jsonschema 4.10.3. `environment: mixed-see-prose` covers both;
the gate itself runs on the Windows host.

The frozen commands name `bin/`, where the two files land at Gate 2. The
dry-run executed the identical bytes at their staged path
`_handoff/batch-n2/candidates/bin/`, blob-verified equal to the bound blobs
before use, so runnability on this environment is established for the frozen
form. Both `$` lines are shown per row.

**T1 — Windows selftest**

```
$ C:/Python312/python.exe -B bin/gatebraid-capture-selftest.py
# frozen form above; dry-run executed as:
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B _handoff/batch-n2/candidates/bin/gatebraid-capture-selftest.py
[... 50 earlier lines ...]
interpreter                   : C:\Python312\python.exe
platform                      : win32
corpus cases                  : 41 (6 valid, 35 invalid)
mutations killed              : 35 of 35
valid cases accepted          : 6 of 6
schema cross-check            : run
platform named by the records : windows
surface digest before         : 036c951a74d86ff1c9dda09190c0e2b12db25e1e95279544e7dd0886eac12be8
surface digest after          : 036c951a74d86ff1c9dda09190c0e2b12db25e1e95279544e7dd0886eac12be8
corpus/schema surface UNMODIFIED: True
conditions failed             : 0
SELFTEST CLEAN: every condition produced its required observation
exit: 0
```

**T2 — WSL selftest**

```
$ wsl.exe -e bash -lc 'cd "/mnt/d/Github repo/Gatebraid" && python3 -B bin/gatebraid-capture-selftest.py'
# frozen form above; dry-run executed as:
$ wsl.exe -e bash -lc 'cd "/mnt/d/Github repo/Gatebraid" && PYTHONDONTWRITEBYTECODE=1 python3 -B _handoff/batch-n2/candidates/bin/gatebraid-capture-selftest.py'
[... 50 earlier lines ...]
interpreter                   : /usr/bin/python3
platform                      : linux
corpus cases                  : 41 (6 valid, 35 invalid)
mutations killed              : 35 of 35
valid cases accepted          : 6 of 6
schema cross-check            : run
platform named by the records : wsl
surface digest before         : 036c951a74d86ff1c9dda09190c0e2b12db25e1e95279544e7dd0886eac12be8
surface digest after          : 036c951a74d86ff1c9dda09190c0e2b12db25e1e95279544e7dd0886eac12be8
corpus/schema surface UNMODIFIED: True
conditions failed             : 0
SELFTEST CLEAN: every condition produced its required observation
exit: 0
```

**T3 — corpus digest unmoved**

```
$ C:/Python312/python.exe -B fixtures/runner-selftest.py
# frozen form above; dry-run executed as:
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B fixtures/runner-selftest.py
[... 29 earlier lines ...]
S28 __pycache__ moves no digest     same  same  PASS     digest must ignore interpreter output

digest scope                  : bytes-platform, evidence-capture-v1, gate-run-v2, instruments, metrics-v1, CORPORA.json, schema, run-corpus.py, runner-selftest.py, fixtures/ listing
digest before                 : f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686
digest after                  : f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686
seed-reachable surface UNMODIFIED: True
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
exit: 0
```

**T4 — every evidence record verifies, layer B re-derived**

```
$ for f in docs/evidence/gatebraid/P2-S1/captures/*.json; do C:/Python312/python.exe -B bin/gatebraid-capture.py --verify-record "$f" --rederive || exit 1; done
# frozen form above; dry-run executed as:
$ for f in docs/evidence/gatebraid/P2-S1/captures/*.json; do ... _handoff/batch-n2/candidates/bin/gatebraid-capture.py --verify-record "$f" --rederive; done
32 records verified (contract conforms, coherence conforms, re-derived), 0 failures
exit: 0
```

**T5 — closed-set complement over the landing set**

```
$ C:/Python312/python.exe -B _t5.py bin docs/evidence/gatebraid/P2-S1
# frozen form above; dry-run executed as:
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B _t5.py _handoff/batch-n2/candidates/bin docs/evidence/gatebraid/P2-S1
files 37 identities ['mianliwang/gatebraid'] outside []
exit: 0
```

**T6 — negative criterion 1 — path containment**

```
$ git diff --name-only 5bc41d7667d1ae019b228d43ed1ef29ea5c0b928..HEAD | C:/Python312/python.exe -B _t6.py
# frozen form above; dry-run executed as:
$ git diff --name-only 5bc41d7667d1ae019b228d43ed1ef29ea5c0b928..HEAD | C:/Python312/python.exe -B _t6.py
paths 0 outside allowlist NONE
(at Gate 1 HEAD == base, so the diff is empty and the criterion holds vacuously; the row proves the command RUNS on this environment)
exit: 0
```

**T7 — negative criterion 2 — no module-level third-party import**

```
$ C:/Python312/python.exe -B _t7.py bin/gatebraid-capture.py bin/gatebraid-capture-selftest.py
# frozen form above; dry-run executed as:
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B _t7.py _handoff/batch-n2/candidates/bin/gatebraid-capture.py _handoff/batch-n2/candidates/bin/gatebraid-capture-selftest.py
module-level third-party imports: NONE
exit: 0
```

**P3 — exit checklist completed, every item evidence-backed**
```
docs/evidence/gatebraid/P2-S1/gate1-exit-checklist.md — all 15 items checked,
each citing an anchor or a measured row in this file.
```

**P4 — allowlist_hash reproduced**
```
$ C:/Python312/python.exe -c "import hashlib;e=['bin/','docs/evidence/gatebraid/P2-S1/'];print(hashlib.sha256(('\n'.join(sorted(x.strip() for x in e))+'\n').encode('utf-8')).hexdigest())"
c17fca97c0a7af32faced1f895c62198a133068edf6dca58e43908b088af26a2
```

**P5 — plan_hash reproduced**
```
$ C:/Python312/python.exe -c "import io,hashlib;L=io.open('docs/evidence/gatebraid/P2-S1/gate1.md',encoding='utf-8').read().split('\n');s=L.index('## Plan (frozen at exit)')+1;e=next(i for i in range(s,len(L)) if L[i].startswith('## '));b=[x.rstrip() for x in L[s:e]];\nwhile b and not b[0]: b.pop(0)\nwhile b and not b[-1]: b.pop()\nprint(hashlib.sha256(('\n'.join(b)+'\n').encode('utf-8')).hexdigest())"
8586225b414dee08db6f47d3f0b14b09f5547dfbba52596a2ce01fe4a64755f7
```

**P6 — the sanctioned `write_domains` write-back to the Slice issue**
```
$ GH_CONFIG_DIR=%USERPROFILE%\.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/8 --jq .body
# declared write_domains in the Slice issue metadata block, measured:
["bin/", "docs/evidence/gatebraid/P2-S1/"]
# frozen allowlist, this gate:
["bin/", "docs/evidence/gatebraid/P2-S1/"]
# EQUAL. gate-1-contract Exit: "If the declared write_domains already equals the
# frozen allowlist, the agreement is recorded as a verification row and no
# rewrite is made; the step is performed, not skipped." No rewrite was made.
```

## Required disclosures

- Deviations: **two contract exit elements are not performed, and are reported
  rather than skipped silently** (gate-1-contract: "a step that is skipped
  rather than failed is executor error and is recorded as friction", friction
  #65). The contract's Exit sets `Gate = G1 passed` and turns the `needs-human`
  label ON. The posted window authorizes only `Workflow` → `Needs Plan
  Approval` and `Next Approval` → `Plan Approval (G1→G2)`, and its §3 lists
  "any label" as not authorized. Both unperformed elements await authorization.
  **One measured correction:** the window's acceptance line names "47
  conditions"; the selftest emits **46** condition rows on both platforms
  (A×10, B×1, C×17, D×12, E×3, F×1, G×2), all PASS. The frozen criterion is
  written against the instrument's own summary — exit 0, `SELFTEST CLEAN`,
  `conditions failed : 0` — so it stays checkable whatever the row count, and
  the measured 46 is recorded here rather than a number the instrument does not
  produce.
- Environment: Windows 11 (10.0.26200), Git Bash over Git for Windows with the
  system `core.autocrlf=true` config in effect; `C:/Python312/python.exe`
  (CPython 3.12.2, jsonschema 4.23.0, PyYAML 6.0.2); second platform WSL
  Ubuntu 24.04.4 with `/usr/bin/python3` (CPython 3.12.3, jsonschema 4.10.3);
  `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` set and exported for every `gh`
  invocation; `PYTHONDONTWRITEBYTECODE=1` set for every Python invocation so no
  interpreter output reaches the tree (friction #114 class).

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S1
gate: 1
environment: mixed-see-prose
executor: Claude Lead
base_sha: 5bc41d7667d1ae019b228d43ed1ef29ea5c0b928
started_at: "2026-08-20T07:41:25.261522Z"
ended_at: "2026-08-20T08:41:09.416564Z"
result: needs_approval
bootstrap_exception: true
approvals:
  - type: State Packet Approval
    author: MianliWang
    comment_url: "https://github.com/MianliWang/gatebraid/issues/8#issuecomment-5352888364"
    at: "2026-08-20T07:38:58Z"
checks:
  - name: plan-complete
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: allowlist-exact
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: test-plan-dry-run
    result: pass
    output_ref: "#records"
  - name: gate1-exit-checklist
    result: pass
    output_ref: "#records"
plan_hash: "8586225b414dee08db6f47d3f0b14b09f5547dfbba52596a2ce01fe4a64755f7"
allowlist_hash: "c17fca97c0a7af32faced1f895c62198a133068edf6dca58e43908b088af26a2"
hash_commands:
  allowlist: |-
    C:/Python312/python.exe -c "import hashlib; e=['bin/','docs/evidence/gatebraid/P2-S1/']; print(hashlib.sha256((chr(10).join(sorted(x.strip() for x in e))+chr(10)).encode('utf-8')).hexdigest())"
  plan: |-
    C:/Python312/python.exe -c "import io,hashlib; L=io.open('docs/evidence/gatebraid/P2-S1/gate1.md',encoding='utf-8').read().split(chr(10)); s=L.index('## Plan (frozen at exit)')+1; e=next(i for i in range(s,len(L)) if L[i].startswith('## ')); b=[x.rstrip() for x in L[s:e]]; k=[i for i,x in enumerate(b) if x.strip()]; b=b[k[0]:k[-1]+1] if k else []; print(hashlib.sha256((chr(10).join(b)+chr(10)).encode('utf-8')).hexdigest())"
evidence_files:
  - docs/evidence/gatebraid/P2-S1/gate1.md
  - docs/evidence/gatebraid/P2-S1/gate1-exit-checklist.md
  - docs/evidence/gatebraid/P2-S1/gate0.json
```
