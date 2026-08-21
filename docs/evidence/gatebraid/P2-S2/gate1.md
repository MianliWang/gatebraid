# Gate 1 evidence — P2-S2

## Plan (frozen at exit)

- Approach: author **`gatebraid-validate`** — the ratified name (ADR-0030 route,
  ratified in this Slice's State Packet Approval) — as M3 node N3's independent
  evidence validator, in the control repository under `bin/` (ADR-0032 decision
  1), together with this Slice's gate evidence. **The authorship-independence
  mandate is a constraint on how these files are written, not only on what they
  do (M3-PLAN §2 N3): the authoring session's inputs are the frozen schemas, the
  N1 corpus, and `gatebraid/evidence-capture@1` read as a specification — never
  N2's implementation.** `bin/gatebraid-capture.py` is EXECUTED as committed
  repository tooling (ADR-0028 §4) and its contents are never read. Three
  independently verifiable tasks. **K1** — author `bin/gatebraid-validate.py`:
  re-derives verdicts from captured evidence JSON plus the frozen schemas alone;
  verifies immutable SHAs, absence of placeholders, absence of self-reference,
  absence of undeclared sections, and byte/line-ending discipline; emits a
  `gatebraid/coverage-report@1` document classifying every verified property as
  `structural`, `semantic`, `replayed` or `capture-trusted`, with no
  `replayable` claim credited unlabelled. **K2** — author
  `bin/gatebraid-validate-selftest.py`: seeded-condition falsification of K1,
  every condition asserting a required exit status, green on both declared
  platforms. **K3** — produce this Slice's Gate 2 evidence under
  `docs/evidence/gatebraid/P2-S2/`, every capture written by the landed
  `bin/gatebraid-capture.py` and every record validating against the frozen
  interfaces with its loader named. `fixtures/`, `schema/`, `protocols/` and
  `bin/gatebraid-capture*.py` are READ-or-EXECUTE sources only; no write reaches
  any of them.
- Exact `write_domains` allowlist: `bin/gatebraid-validate.py`,
  `bin/gatebraid-validate-selftest.py`, and `docs/evidence/gatebraid/P2-S2/`.
  Nothing else. The Slice body's declared `write_domains` are the prefixes
  `bin/` and `docs/evidence/gatebraid/P2-S2/`; the frozen allowlist narrows the
  first prefix to the two named files, so every path this plan may write is
  covered by the declaration and the declaration is wider than the freeze.
  `NOTICE.md` is untouched — neither file derives from a surveyed framework, so
  no attribution is owed (ADR-0010, ADR-0027).
- Test plan (commands, runnable as written on the declared environment
  `mixed-see-prose` = Windows AND WSL; each was dry-run in this gate and each
  row in Records carries its generated output). **Acceptance is stated against
  each instrument's own emitted summary rather than against a count, because a
  frozen count is falsified by the next legitimate corpus or condition change
  and the plan cannot be repaired after the freeze.**
  **T1** `C:/Python312/python.exe -B bin/gatebraid-validate-selftest.py` —
  green: exit 0, the selftest's own summary line reports it clean, and its
  `conditions failed` line reads `0`.
  **T2** `wsl.exe -e bash -lc 'cd "/mnt/d/Github repo/Gatebraid" && python3 -B bin/gatebraid-validate-selftest.py'`
  — green: the same two criteria on the second platform, on jsonschema 4.10.3.
  **T3** `C:/Python312/python.exe -B bin/gatebraid-validate.py --corpus fixtures --coverage-out docs/evidence/gatebraid/P2-S2/coverage-windows.json`
  — green: exit 0; every applicable N1 corpus case reaches its recorded expected
  disposition with zero unexpected dispositions, as reported by the validator's
  own emitted summary; the emitted document validates against the committed
  `schema/coverage-report.schema.json` with 0 errors, loader named.
  **T4** the T3 command under the T2 harness, writing
  `docs/evidence/gatebraid/P2-S2/coverage-wsl.json` — green: identical criteria,
  satisfying M3-PLAN §2 N3's dual-platform Accept-when.
  **T5** `C:/Python312/python.exe -B bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S2/checks/corrupted-capture.json --coverage-out docs/evidence/gatebraid/P2-S2/coverage-corrupted.json`
  — green: **non-zero** exit and an emitted verdict of rejection naming the
  corrupted locus. The input is a deliberately corrupted copy of a committed
  P2-S1 capture, produced under this Slice's allowlist; the committed original
  is never modified. This is M3-PLAN §2 N3's "deliberately corrupted N2 output
  is rejected" item.
  **T6** `C:/Python312/python.exe -B bin/gatebraid-validate.py --verify-coverage docs/evidence/gatebraid/P2-S2/coverage-windows.json`
  — green: exit 0 and the emitted summary reporting every verified property
  carrying exactly one of the four classes and zero `replayable` claims credited
  without a label. This is the Accept-when's classification item, and it is
  checked by re-reading the emitted report rather than by the emitting run's own
  say-so.
  **T7** `C:/Python312/python.exe -B fixtures/runner-selftest.py` — green: exit
  0, `SELFTEST CLEAN`, `conditions failed : 0`, `seed-reachable surface
  UNMODIFIED: True`, and `digest before` equal to `digest after`. This is the
  frozen corpus proving it did not move under the Slice.
  **T8** and **T9** are the negative criteria below.
- Risk notes (`risk: low`, stated as what would have to be true for that rating
  to be wrong): (1) the two new files are additive and touch no existing tracked
  file — falsified by T8; (2) the validator is independent of N2 in imports as
  well as authorship, so no shared implementation can carry a shared defect —
  falsified by T9, which is the mechanised half of M3-PLAN §2 N3's independence
  Accept-when, the authorship half being the coordinator's review from the
  record; (3) the frozen corpus is a read input and cannot move — falsified by
  T7's digest comparison; (4) the validator carries its own falsified selftest
  on both platforms — falsified by T1 and T2; (5) no contract, schema, ADR or
  template text changes, so nothing normative moves; the corpus is out of scope
  and IN-01 remains re-assigned to corpus v2 at P. `consult_first: false` is set
  deliberately on the same grounds: the diff adds two files behind their own
  falsification and alters no contract.
- Rollback note: nothing is committed until Gate 2, and Gate 2 lands exactly two
  additive files plus this evidence directory. To abandon at any point before
  the Gate 3 merge, delete `bin/gatebraid-validate.py`,
  `bin/gatebraid-validate-selftest.py` and `docs/evidence/gatebraid/P2-S2/` from
  the working tree; if commits already exist on the slice branch, leave the
  branch unpushed and unmerged — ADR-0025 §3 retains aborted slice branches
  rather than deleting them. No tracked file is modified, so there is nothing to
  restore and no revert to author.
- **Negative criterion (checkable):** **N-A — the landed diff touches no path
  outside the frozen allowlist.** Scope, stated as an explicit path set rather
  than "the added files" (friction #110): the complete output of
  `git diff --name-only 11dbac47927bff5aa7c9e86124e85db9ecdbc650..HEAD`, every
  line of which must be `bin/gatebraid-validate.py`,
  `bin/gatebraid-validate-selftest.py`, or a path under
  `docs/evidence/gatebraid/P2-S2/`. Mechanised proxy **T8**; it **errs toward
  false failure** — any path outside the three entries fails the criterion
  whether or not it is benign, so a pass is informative and a failure requires a
  human look. **N-B — neither landed file reaches N2's implementation, and
  neither imports a third-party module at module level.** Scope: exactly
  `bin/gatebraid-validate.py` and `bin/gatebraid-validate-selftest.py`, parsed
  with `ast`; module-level `Import`/`ImportFrom` names compared against
  `sys.stdlib_module_names`, and the whole parse tree searched for any reference
  to `gatebraid-capture`, `gatebraid_capture`, or an import of any module whose
  resolved file is `bin/gatebraid-capture.py` or
  `bin/gatebraid-capture-selftest.py`. Mechanised proxy **T9**; it **errs toward
  false failure** for the third-party half — it inspects only module-level
  import nodes, so a guarded optional import inside a function or `try` block is
  deliberately out of scope and passes — and **errs toward false failure** for
  the N2 half as well, since a string mentioning the capture tool's *path* in a
  comment or a `--verify-record` invocation is flagged even though executing the
  committed tool is expressly permitted; a flagged occurrence is read by a human
  against this criterion's text, never auto-accepted.

## Records

**P1 — team findings flushed** (only if a read-only team ran)
```
n/a — no read-only Agent Team was spawned in this gate; the plan was produced by the lead alone, so there are no team findings to flush and no comment to cite (gate-1-contract action 2 is optional).
```

**P2 — dry-run of every declared test command, on the declared environment**
(gate-1-contract action 4 — one row per declared command)
```
$ C:/Python312/python.exe -B bin/gatebraid-validate-selftest.py
exit 2
C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-validate-selftest.py': [Errno 2] No such file or directory
```
```
$ wsl.exe -e bash -lc "cd "/mnt/d/Github repo/Gatebraid" && python3 -B bin/gatebraid-validate-selftest.py"
exit 2
python3: can't open file '/mnt/d/Github repo/Gatebraid/bin/gatebraid-validate-selftest.py': [Errno 2] No such file or directory
```
```
$ C:/Python312/python.exe -B bin/gatebraid-validate.py --corpus fixtures --coverage-out docs/evidence/gatebraid/P2-S2/coverage-windows.json
exit 2
C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-validate.py': [Errno 2] No such file or directory
```
```
$ wsl.exe -e bash -lc "cd "/mnt/d/Github repo/Gatebraid" && python3 -B bin/gatebraid-validate.py --corpus fixtures --coverage-out docs/evidence/gatebraid/P2-S2/coverage-wsl.json"
exit 2
python3: can't open file '/mnt/d/Github repo/Gatebraid/bin/gatebraid-validate.py': [Errno 2] No such file or directory
```
```
$ C:/Python312/python.exe -B bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S2/checks/corrupted-capture.json --coverage-out docs/evidence/gatebraid/P2-S2/coverage-corrupted.json
exit 2
C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-validate.py': [Errno 2] No such file or directory
```
```
$ C:/Python312/python.exe -B bin/gatebraid-validate.py --verify-coverage docs/evidence/gatebraid/P2-S2/coverage-windows.json
exit 2
C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-validate.py': [Errno 2] No such file or directory
```
```
$ C:/Python312/python -B fixtures/runner-selftest.py
exit 0
condition                           want  got  verdict  required observation
S00 untouched copy                     0    0  PASS     CORPUS CLEAN
S01 mutation not killed                1    1  PASS     mutation not killed
S02 recorded locus silent              1    1  PASS     recorded locus did not fire
S03 unrecorded locus fired             1    1  PASS     unrecorded locus fired
S04 valid case broken                  1    1  PASS     expected valid
S05 fixture missing                    2    2  PASS     fixture missing
S06 schema missing                     2    2  PASS     schema missing
[elided: 8 of 37 lines shown; full output: docs/evidence/gatebraid/P2-S2/captures/G1-T7-dryrun.json]
```
```
$ git diff --name-only 11dbac47927bff5aa7c9e86124e85db9ecdbc650..HEAD
exit 0
```
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S2/checks/independence-check.py bin/gatebraid-validate.py bin/gatebraid-validate-selftest.py
exit 2
C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\docs\\evidence\\gatebraid\\P2-S2\\checks\\independence-check.py': [Errno 2] No such file or directory
```

**P3 — exit checklist completed, every item evidence-backed**
```
docs/evidence/gatebraid/P2-S2/gate1-exit-checklist.md
```

**P4 — allowlist_hash reproduced**
```
$ C:/Python312/python.exe -B -c "import hashlib;e=['bin/gatebraid-validate.py','bin/gatebraid-validate-selftest.py','docs/evidence/gatebraid/P2-S2/'];b=('\n'.join(sorted(x.strip() for x in e))+'\n').encode('utf-8');print(hashlib.sha256(b).hexdigest())"
0c0090ec87b5a47838edfe8bad7d8350a79d50fc642c3e1d10b1582a09223d86
```

**P5 — plan_hash reproduced**
```
$ C:/Python312/python.exe -B -c "import hashlib,re;t=open('docs/evidence/gatebraid/P2-S2/gate1.md',encoding='utf-8').read();m=re.search(r'^## Plan \(frozen at exit\)$',t,re.M);r=t[m.end():];n=re.search(r'^## ',r,re.M);s=r[:n.start()] if n else r;b=('\n'.join(x.rstrip() for x in s.split('\n')).strip('\n')+'\n').encode('utf-8');print(hashlib.sha256(b).hexdigest())"
6f68e9a09fe89242dff6d8cec2052d27e9e9ed42e32d45ef061aaeff2592f346
```

**P6 — the sanctioned `write_domains` write-back to the Slice issue**
(gate-1-contract Exit; byte-identical re-emission apart from that field)
```
NOT PERFORMED IN THIS WINDOW — the Exit step is not granted here. The
adjudication comment https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5364439544
grants the plan and allowlist freeze and stops at the Gate 1 report; it
authorizes no field write beyond Gate -> G0 passed and Workflow -> Gate 1
Planning, and no other mutation. The declared write_domains ['bin/', 'docs/evidence/gatebraid/P2-S2/']
are prefixes that COVER the frozen allowlist but are not byte-equal to it,
so the contract's 'already equals' branch does not apply and a rewrite IS
required. It is carried as OWED at the Exit grant, named here rather than
skipped silently — friction #65 is the case where an action-7 write-back
was never attempted and never recorded.
```

## Required disclosures

- Deviations: the `write_domains` write-back required by gate-1-contract Exit is **not performed in this window** and is recorded `not_run` — the grant at https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5364439544 stops at the Gate 1 report and authorizes no further field write or issue edit; it is carried as owed rather than skipped (friction #65 is the case where exactly this step was never attempted and never recorded) · T1–T6 and T9 dry-ran against an artifact that does not yet exist, because the authorship-independence mandate places its authoring at Gate 2; what the dry-run establishes is command form and path resolution on both declared platforms, and the expected-green criteria are frozen here for Gate 2 to satisfy · no read-only Agent Team was spawned, so P1 is `n/a` rather than a flushed-findings citation.
- Environment: Windows 11 host, Git Bash (MSYS2) shell; declared `environment: mixed-see-prose` = Windows loader host `C:\Python312\python.exe` (CPython 3.12.2, jsonschema 4.23.0, PyYAML 6.0.2) AND WSL `/usr/bin/python3` (CPython 3.12.3, jsonschema 4.10.3, PyYAML 6.0.1), the gate itself running on the Windows host; `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` call; `PYTHONDONTWRITEBYTECODE=1` on every Python invocation; every `gh api` endpoint written without a leading slash (MSYS rewrites leading-slash endpoints into filesystem paths).

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S2
gate: 1
environment: mixed-see-prose
executor: Claude Lead
base_sha: 11dbac47927bff5aa7c9e86124e85db9ecdbc650
started_at: '2026-08-21T02:30:00Z'
ended_at: '2026-08-21T02:52:00Z'
result: needs_approval
bootstrap_exception: true
checks:
- name: plan-complete
  result: pass
  output_ref: '#plan-frozen-at-exit'
- name: allowlist-exact
  result: pass
  output_ref: '#plan-frozen-at-exit'
- name: test-plan-dry-run
  result: pass
  command: each declared T1-T9 command, run as written on the declared environment
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G1-T7-dryrun.json
- name: gate1-exit-checklist
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/gate1-exit-checklist.md
- name: gate0-adjudication-door-author
  result: pass
  command: gh api repos/MianliWang/gatebraid/issues/comments/5364439544 --jq '{author,url,created,updated}'
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G1-Q2-approval.json
- name: gate-and-workflow-write-readback
  result: pass
  command: gh project item-edit (Gate 6922003a; Workflow f6b57153) then one read-back by item id
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G1-fields-readback.json
- name: write-domains-writeback
  result: not_run
  command: gate-1-contract Exit, the one sanctioned Slice-body rewrite
  output_ref: '#records'
approvals:
- type: State Packet Approval
  comment_url: https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5363954606
  author: MianliWang
  at: '2026-08-21T01:07:41Z'
plan_hash: 6f68e9a09fe89242dff6d8cec2052d27e9e9ed42e32d45ef061aaeff2592f346
allowlist_hash: 0c0090ec87b5a47838edfe8bad7d8350a79d50fc642c3e1d10b1582a09223d86
hash_commands:
  allowlist: C:/Python312/python.exe -B -c "import hashlib;e=['bin/gatebraid-validate.py','bin/gatebraid-validate-selftest.py','docs/evidence/gatebraid/P2-S2/'];b=('\n'.join(sorted(x.strip()
    for x in e))+'\n').encode('utf-8');print(hashlib.sha256(b).hexdigest())"
  plan: C:/Python312/python.exe -B -c "import hashlib,re;t=open('docs/evidence/gatebraid/P2-S2/gate1.md',encoding='utf-8').read();m=re.search(r'^##
    Plan \(frozen at exit\)$',t,re.M);r=t[m.end():];n=re.search(r'^## ',r,re.M);s=r[:n.start()] if n else
    r;b=('\n'.join(x.rstrip() for x in s.split('\n')).strip('\n')+'\n').encode('utf-8');print(hashlib.sha256(b).hexdigest())"
evidence_files:
- docs/evidence/gatebraid/P2-S2/gate1.md
- docs/evidence/gatebraid/P2-S2/gate1-exit-checklist.md
notes: 'Gate 1 planning only; no code was authored in this window. The validator and its selftest are
  authored at Gate 2, which is why T1-T6 and T9 dry-ran against an absent artifact: each resolved to a
  fully-qualified path on its own platform - D:\Github repo\Gatebraid\bin\... on Windows and /mnt/d/Github
  repo/Gatebraid/bin/... under WSL, the embedded space surviving quoting on both - and failed with [Errno
  2] naming that resolved path, never with a shell parse error or a /tmp-style semantic mismatch. That
  is the Slice A defect class gate-1-contract action 4 exists to catch, and it is demonstrably absent
  on both declared platforms. T7 and T8 ran green. The write_domains write-back (contract Exit) is required
  and is NOT performed here: this window''s grant stops at the Gate 1 report. It is recorded not_run and
  carried as owed. Acceptance criteria are frozen against each instrument''s own emitted summary rather
  than against counts, so a legitimate later corpus or condition change cannot falsify a frozen number
  the plan can no longer repair.'
```
