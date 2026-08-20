# Gate 2 evidence — P2-S1

## Entry records

**E1 — Plan Approval verified** (author must be `MianliWang`, not this session — ADR-0020 §4)
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5353895987 --jq '{author: .user.login, url: .html_url}'
{"author":"MianliWang","url":"https://github.com/MianliWang/gatebraid/issues/8#issuecomment-5353895987"}
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login
mianliwang492-source
```
- The approval names both frozen hashes (`plan_hash 8586225b…`, `allowlist_hash c17fca97…`); it is not a `gatebraid/handoff@1` block; its author differs from the executing session's identity above.

**E2 — Writer Lease taken, read back**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project item-edit --id PVTI_lAHOBRofUs4Beum7zg3Dr5A --project-id PVT_kwHOBRofUs4Beum7 --field-id PVTF_lAHOBRofUs4Beum7zhZJcSU --text "<lease>"
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f query='...ProjectV2Item fieldValues...' -F id=PVTI_lAHOBRofUs4Beum7zg3Dr5A --jq '...Writer Lease...'
windows-10.0.26200:claude-code-P2-S1:2026-08-20T09:21:55Z
```

**E3 — baseline re-read** (ADR-0011 §9; ADR-0014 §1 excludes this slice's own evidence path)
```
$ git ls-remote origin refs/heads/main
5bc41d7667d1ae019b228d43ed1ef29ea5c0b928	refs/heads/main
$ git diff --name-only 5bc41d7667d1ae019b228d43ed1ef29ea5c0b928..5bc41d7667d1ae019b228d43ed1ef29ea5c0b928
(empty — no changed paths)
```
- baseline: `unchanged`
- X (plan baseline, recorded as `base_sha` in this slice's Gate 0 record) == Y (base-branch head). The changed-path set is empty, so the ADR-0014 §1 exclusion has nothing to exclude and the intersection with the frozen `write_domains` is empty. The plan's assumptions are intact.

**E4 — Active Branch created from Y; `Base SHA` field set to Y**
```
$ git rev-parse --abbrev-ref HEAD; git rev-parse HEAD
slice/P2-S1
1f2335e05c3aaade83cf33930a748bc60103cfde
```
- `Base SHA` field measured already equal to Y (`5bc41d7667d1ae019b228d43ed1ef29ea5c0b928`); the post-condition held and no rewrite was made.

## Verification outputs

**V1 — dual-platform acceptance, half 1 of 2: selftest clean on Windows**

```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-capture-selftest.py
[... 52 of 62 lines elided here. The full 62-line output is materialized at the
 evidence amendment as gate2-full/V1-windows-selftest.json
 @sha256:d6346d7f3faed7fb700cd3a9c0667922ff36c26bec01e9d380a06edf0f92f5e4 ...]
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

**V2 — dual-platform acceptance, half 2 of 2: selftest clean on WSL (jsonschema 4.10.3)**

```
$ wsl.exe -e bash -lc 'cd "/mnt/d/Github repo/Gatebraid" && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-capture-selftest.py'
[... 52 of 62 lines elided here. The full 62-line output is materialized at the
 evidence amendment as gate2-full/V2-wsl-selftest.json
 @sha256:7824100c04427c0fc72e3d4b67f39dc51138d4a246ede40eaf74e6d03b2370f1 ...]
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

**V3 — corpus out of scope: frozen digest unmoved**

```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B fixtures/runner-selftest.py
[... 30 of 37 lines elided here. The full 37-line output is materialized at the
 evidence amendment as gate2-full/V3-corpus-digest.json
 @sha256:3b44a8abca5176a0d33ba8899a60eb779fa548840326e6297d7379a61305d3c3 ...]

digest scope                  : bytes-platform, evidence-capture-v1, gate-run-v2, instruments, metrics-v1, CORPORA.json, schema, run-corpus.py, runner-selftest.py, fixtures/ listing
digest before                 : f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686
digest after                  : f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686
seed-reachable surface UNMODIFIED: True
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
exit: 0
```

**V4 — evidence records validate and re-derive, run by the LANDED generator**

```
$ for f in docs/evidence/gatebraid/P2-S1/captures/*.json; do PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-capture.py --verify-record "$f" --rederive; done
34/34 records: contract conforms, coherence conforms, layer B re-derived. failures: none
exit: 0
```

**V5 — closed-set complement over the landed set**

```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B _t5.py bin docs/evidence/gatebraid/P2-S1
files scanned: 39
identities found: ['mianliwang/gatebraid']
outside permitted set: NONE
exit: 0
# the checker is committed at the amendment; re-runnable as written. The file
# count grows because the amendment adds its own evidence to the scanned set:
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S1/checks/t5.py bin docs/evidence/gatebraid/P2-S1
files scanned: 51
identities found: ['mianliwang/gatebraid']
outside permitted set: NONE
exit: 0
```

**V6 — negative criterion N1: no path outside the frozen allowlist**

```
$ git diff --name-only 5bc41d7667d1ae019b228d43ed1ef29ea5c0b928..HEAD | C:/Python312/python.exe -B _t6.py
# the checker is committed at the amendment; re-runnable as written, range pinned:
$ git diff --name-only 5bc41d7667d1ae019b228d43ed1ef29ea5c0b928..42f16e1881c8f09e1d03acea568b50a8f41c167b | C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S1/checks/t6.py
[... 27 of 41 lines elided here. The full output is materialized at the evidence
 amendment as gate2-full/V6-path-containment.json
 @sha256:e8e77e604e7981b60ce7501e65e5ab10122d8cd6414c3aecff67253d39572534 —
 43 lines over the tip's 40 paths, "outside allowlist: NONE" ...]
    docs/evidence/gatebraid/P2-S1/captures/Q5-real-json.json OK
    docs/evidence/gatebraid/P2-S1/captures/Q5-real.json OK
    docs/evidence/gatebraid/P2-S1/captures/Q6-falsify-a.json OK
    docs/evidence/gatebraid/P2-S1/captures/Q6-falsify-b.json OK
    docs/evidence/gatebraid/P2-S1/captures/Q6-falsify-owner.json OK
    docs/evidence/gatebraid/P2-S1/captures/Q6-real.json OK
    docs/evidence/gatebraid/P2-S1/captures/Q7-falsify-a.json OK
    docs/evidence/gatebraid/P2-S1/captures/Q7-falsify-b.json OK
    docs/evidence/gatebraid/P2-S1/captures/Q7-real-blockedby.json OK
    docs/evidence/gatebraid/P2-S1/captures/Q7-real-blocking.json OK
    docs/evidence/gatebraid/P2-S1/gate0.json OK
    docs/evidence/gatebraid/P2-S1/gate1-exit-checklist.md OK
    docs/evidence/gatebraid/P2-S1/gate1.md OK
outside allowlist: NONE
exit: 0
```

**V7 — negative criterion N2: no module-level third-party import**

```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B _t7.py bin/gatebraid-capture.py bin/gatebraid-capture-selftest.py
module-level imports inspected: 23
third-party at module level: NONE
scope: exactly the two landed files; guarded imports inside try/def are out of scope by design
exit: 0
# the checker is committed at the amendment; re-runnable as written:
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S1/checks/t7.py bin/gatebraid-capture.py bin/gatebraid-capture-selftest.py
module-level imports inspected: 23
third-party at module level: NONE
scope: exactly the 2 named file(s); guarded imports inside try/def are out of scope by design
exit: 0
```

**V8 — K1: the landed pair is byte-identical to the blobs bound at N2-R2**
(added at the evidence amendment. The `landed-blobs-match-bound` check asserted
this as `pass` behind an `output_ref` that resolved to no row in this section;
this row is that output. The commit is named by full sha, never `HEAD`, because
a record must not name a state the act of recording it will move — ADR-0028 §4.)

```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S1/checks/k1_blobs.py 42f16e1881c8f09e1d03acea568b50a8f41c167b
commit: 42f16e1881c8f09e1d03acea568b50a8f41c167b
path                               bound                                      landed                                     verdict
bin/gatebraid-capture-selftest.py  a40869bea3d1e8dbaf20473456f919838f788eec   a40869bea3d1e8dbaf20473456f919838f788eec   MATCH
  bytes                            40846                                      40846                                      MATCH
bin/gatebraid-capture.py           43ff5a06c7f7e1e9b0ba5d6f14e956bc8d4c73d0   43ff5a06c7f7e1e9b0ba5d6f14e956bc8d4c73d0   MATCH
  bytes                            43335                                      43335                                      MATCH
extra paths under bin/: NONE
blobs compared: 2  mismatches: 0
exit: 0
```

- captured: `docs/evidence/gatebraid/P2-S1/captures/K1-blobs.json@sha256:8e8ddf68d4537e10c98a0ebd7b265cc6f44d6c6f5e6762df178aa09754881d07`

**V9 — K2b: every gate record validates against the committed `gatebraid/gate-run@2`**
(added at the evidence amendment. Nothing in the Gate 2 record discharged this
conjunct of plan task K2: the landed generator's contract is
`gatebraid/evidence-capture@1` and it has no gate-run mode, so it could not have
produced this row. The loader is named rather than assumed — "validated" without
a validator is the mute class ADR-0028 exists against.)

```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S1/checks/k2b_gate_records.py docs/evidence/gatebraid/P2-S1/gate0.json docs/evidence/gatebraid/P2-S1/gate1.md docs/evidence/gatebraid/P2-S1/gate2.md
schema: schema/gate-run-v2.schema.json
loader: jsonschema 4.23.0, Draft202012Validator
docs/evidence/gatebraid/P2-S1/gate0.json             schema=gatebraid/gate-run@2   gate=0 result=passed         conforms
docs/evidence/gatebraid/P2-S1/gate1.md               schema=gatebraid/gate-run@2   gate=1 result=needs_approval conforms
docs/evidence/gatebraid/P2-S1/gate2.md               schema=gatebraid/gate-run@2   gate=2 result=needs_approval conforms
records validated: 3  non-conforming: 0
exit: 0
```

- captured: `docs/evidence/gatebraid/P2-S1/captures/K2b-gate-records.json@sha256:1341fde8d137f8cbc21f3b71efe3614d2de389e865454bb11d0a9d7e9aa0d151`
- Taken before this amendment's own final write to `gate2.md`, which necessarily
  moves that file after its own row is written — the same self-reference boundary
  the handoff fingerprint records. The post-amendment state of all four records is
  re-validated in `gate3.md`.

## Review record

### Review 1

Reviewer: `Claude Read-Only Team`, a session that authored none of the work it
reviewed. Verdicts transcribed verbatim from that session's report,
`_handoff/batch-n2/REVIEW1-M3-P2S1.md`, verified before transcription at
`sha256:4257d79bc69056320417fce2e17e740ecdb574bbdeb209f4f29384076bc78191`,
33,324 bytes — the value the Release Approval cites.

| Item | Verdict | Evidence |
|---|---|---|
| R1 allowlist confinement | **PASS** (+F-A) | report rows A1–A2; `#verification-outputs` V6 |
| R2 test-plan coverage | **PASS for the enumerated test plan T1–T7; two coverage gaps referred to the coordinator** (F-B, F-C) | report rows B1–B3; `#verification-outputs` V1–V9 |
| R3 evidence is rows that reproduce | **PASS** (+F-D, F-E) | report rows C1–C6; `#verification-outputs`, `#entry-records` |
| R4 negative criterion | **PASS** | report rows D1–D2; `#verification-outputs` V6, V7 |
| R5 no prohibited action | **PASS** | report rows E1–E7; `#entry-records`, `#required-disclosures` |

The two R2 referrals are ruled by the coordinator in the Release Approval: the
K1 and K2b gaps are **record defects, not substance failures** — both facts were
verified true independently by the reviewer (report rows C1 and C6) — and they
are repaired in the open before the door by rows V8 and V9 above, never waved
through. R2 therefore stands as PASS with its defects repaired and recorded.

**Reviewer rows** (the commands the reviewer ran, with outputs)
```
RUN. Full rows are in the report identified above, which is the transcription
source and is pinned by the sha256 recorded there. Summarised by section:

  A1-A2  R1: 40 changed paths listed in full; complement outside bin/ and
         docs/evidence/gatebraid/P2-S1/ = 0; name-status tally "40 A" (no M,
         no D), so no tracked file was modified or deleted.
  B1-B3  R2: plan_hash and allowlist_hash reproduced with the recorded
         hash_commands, verbatim, before any mapping was trusted; T1-T7 mapped
         one-to-one onto V1-V7; K1 and K2b recorded as having no discharging
         row and referred.
  C1-C6  R3: both landed blobs read from the object database and matched to the
         bound values at the declared sizes; Windows selftest re-run whole
         (SELFTEST CLEAN, conditions failed 0, both surface digests equal,
         46 condition rows counted independently, confirming this file's
         disclosed correction of the window's "47"); corpus digest re-run and
         unmoved at f6128a0a...965686; all 34 capture records re-verified and
         re-derived, 34/34, zero failures; all three gate records validated
         against schema/gate-run-v2.schema.json, 3/3 conforming.
  D1-D2  R4: both negative criteria re-implemented from gate1.md's prose scope
         (the original _t5/_t6/_t7 were absent) and re-run; N1 clean over 40
         paths, N2 clean with 23 module-level imports inspected, reproducing
         V7's count exactly.
  E1-E7  R5: origin/main unmoved; the complete remote ref set enumerated and
         every member explained, with no slice ref pushed; no pull request in
         any state for this branch; Writer Lease read by the Q6 form and found
         empty, that reading falsified by confirming the field exists on the
         project; all three commits' authors and messages read, no
         Co-Authored-By trailer on any; allowlist held in all three trees, not
         only at the tip; and a closed-set identifier sweep over all 40 changed
         paths' contents whose complement, after each candidate was classified,
         contains exactly one real repository identity, the permitted one.
```

- Reviewer write disclosure: `the report file only, at the ignored path
  _handoff/batch-n2/REVIEW1-M3-P2S1.md — zero commits, zero tracked-file edits,
  no gh mutation of any kind; verified at close by an empty git status, zero
  __pycache__, and all three refs unmoved`
- Rules given to the reviewer: `measure, never declare — every verdict cites the
  command and its output; cite, never restate; a checker never echoes a
  forbidden value into its record (name loci and counts); a bare zero states
  what it searched; closed-set by complement over your own outputs; friction
  ordinals only from the log's measured end; on any uncertainty STOP and ask —
  never improvise. Plus the read-only mandate and the entry facts, as dispatched.`

## Repair record

```
No repair attempt. No declared test command returned red at any point in this
gate; the repair sequence was never entered and repair_limit remains unspent.
```

## Required disclosures

- Deviations: **(1)** `result` stood at `needs_approval` throughout the
  implementing grant, because the review that justifies `passed` had not run and
  writing `passed` beforehand would have been the implementer certifying its own
  gate, which ADR-0028 exists against. Review 1 has since run and returned PASS
  on all five items, the coordinator adjudicated Gate 2 **PASS** in the Release
  Approval, and `result` is set to `passed` at this evidence amendment — written
  last, after every repair recorded below.
  **(2)** This slice's Gate 0 record is `gate0.json`, not the `gate0.md` the
  Gate 2 contract's baseline-re-read clause names; the Gate 0 window specified a
  `gate-run@2` record without naming the file, and the baseline `X` is its
  `base_sha` field. Content is unaffected; the filename differs from the
  template convention. **(3)** Commit messages carry no `Co-Authored-By`
  trailer, matching the operator's recorded PUBLISH AS LANDED decision at N1E
  and every M3-era commit. **(4)** The `needs-human` label was applied (grant
  step 1, completing Gate 1's parked exit) and then removed moments later by
  this gate's own entry, which consumes the approval (gate-2-contract Entry).
  Both operations are recorded; neither was skipped.
  **(5) Evidence amendment, under the Release Approval's step 1.** The four
  elided outputs are materialized under `gate2-full/` as `evidence-capture@1`
  records produced **at the amendment**, not the original Gate 2 process bytes,
  which were not retained. V1 and V2 re-derive at exactly **62** lines and V3 at
  **37**, matching the elision notes' own counts; V6 is re-derived over the
  tip's 40-path set rather than the 39 its original run saw, and its
  reconstructed checker prints one extra summary line, so its length differs
  from the original note's 41. **(6)** `_t5.py`/`_t6.py`/`_t7.py` were never
  committed and are unrecoverable; `checks/t5.py`, `checks/t6.py` and
  `checks/t7.py` are **reconstructions** that reproduce each row's check and
  output shape, not the original bytes, and each says so in its own docstring.
  V7's count of 23 reproduces exactly; V5's file count grows from 39 to 51
  because the amendment adds its own evidence to the scanned set. **(7)** The
  writer session for this amendment and for Gate 3 is **the same session that
  performed Review 1**, by explicit operator instruction in the live session,
  given after that session raised the role conflict and the operator reaffirmed
  with the transcription terms. The reviewer/writer separation is therefore not
  preserved for the transcription step; it is recorded here rather than left to
  inference, and the transcription source was hash-verified against the value
  the Release Approval cites before any text was copied. **(8)** The
  `Writer Lease` was taken for this grant although step 2 enumerates only `Gate`
  and `Workflow`; the approval's own "writer session, single writer" term and
  gate-3-contract Exit 6 ("release the `Writer Lease`") both presuppose it is
  held, and no lease was held when it was taken.
- Friction, **drafted here and not appended** — `_handoff/friction-log.md` lies
  outside this slice's frozen allowlist, and the approval routes the append to
  the closure batch under its own approval. Measured end of the log at write:
  **#140**, so this entry takes **#141**:
  `### 141. A gate's evidence asserted four anchors that resolved to nothing —
  a check pointing at its own declaration, a conjunct with no row, four
  elisions pointing at a path that was never created, and three checkers that
  were run and then not committed · P2-S1, Gate 2 · executor record defect,
  §3.5 class, uncounted — every one caught by the independent read-only review,
  none by any check the gate ran on itself; the substance was true in all four
  cases, which is what makes the class a record defect rather than a failure,
  and what makes it survivable only because the review existed.`
- Reviewer write disclosure: `the reviewer wrote only its report, on an ignored
  _handoff/ path — no commit, no tracked-file edit, no gh mutation of any kind;
  verified at its close by an empty git status, zero __pycache__, and all three
  refs unmoved. Its verdicts are transcribed above under Review 1.`
- Environment: Windows 11 (10.0.26200), Git Bash over Git for Windows with
  system `core.autocrlf=true` and in-tree `.gitattributes` `* text=auto eol=lf`;
  `C:/Python312/python.exe` CPython 3.12.2 (jsonschema 4.23.0, PyYAML 6.0.2);
  second platform WSL Ubuntu 24.04.4, `/usr/bin/python3` CPython 3.12.3
  (jsonschema 4.10.3); `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` set and
  exported for every `gh` invocation; `PYTHONDONTWRITEBYTECODE=1` for every
  Python invocation.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S1
gate: 2
environment: mixed-see-prose
executor: Claude Lead
base_sha: 5bc41d7667d1ae019b228d43ed1ef29ea5c0b928
active_branch: slice/P2-S1
started_at: "2026-08-20T07:41:25.261522Z"
ended_at: "2026-08-20T21:57:39.568870Z"
result: passed
bootstrap_exception: true
checks:
  - name: tests-green-per-plan
    command: "C:/Python312/python.exe -B bin/gatebraid-capture-selftest.py (Windows) and the WSL twin"
    result: pass
    output_ref: "#verification-outputs"
  - name: allowlist-respected
    # the range is pinned at both ends: a check must not name a state the act
    # of recording it will move (ADR-0028 §4). Repaired at the amendment.
    command: "git diff --name-only 5bc41d7667d1ae019b228d43ed1ef29ea5c0b928..42f16e1881c8f09e1d03acea568b50a8f41c167b"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S1/gate2-full/V6-path-containment.json@sha256:e8e77e604e7981b60ce7501e65e5ab10122d8cd6414c3aecff67253d39572534"
  - name: baseline-reread
    command: "git ls-remote origin refs/heads/main"
    result: pass
    output_ref: "#entry-records"
  - name: landed-blobs-match-bound
    # output_ref repaired at the amendment: it pointed at a section carrying no
    # such row, so the check resolved to its own declaration. It now pins the
    # capture that generated the comparison, and the commit is named in full.
    command: "docs/evidence/gatebraid/P2-S1/checks/k1_blobs.py 42f16e1881c8f09e1d03acea568b50a8f41c167b"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S1/captures/K1-blobs.json@sha256:8e8ddf68d4537e10c98a0ebd7b265cc6f44d6c6f5e6762df178aa09754881d07"
  - name: gate-records-validate
    # added at the amendment: plan task K2's second conjunct had no row at all.
    command: "docs/evidence/gatebraid/P2-S1/checks/k2b_gate_records.py gate0.json gate1.md gate2.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S1/captures/K2b-gate-records.json@sha256:1341fde8d137f8cbc21f3b71efe3614d2de389e865454bb11d0a9d7e9aa0d151"
  - name: review-five-items
    # Review 1 ran under Executor = Claude Read-Only Team; R1-R5 all PASS,
    # verdicts transcribed verbatim from the report the approval pins by sha256.
    result: pass
    output_ref: "#review-record"
handoff_fingerprint:
  active_branch_head: "1f2335e05c3aaade83cf33930a748bc60103cfde"
  tree_sha: "16b74f43307b57f326cc086714e468f4c7874461"
  changed_paths: ["bin/gatebraid-capture-selftest.py", "bin/gatebraid-capture.py", "docs/evidence/gatebraid/P2-S1/captures/E-head.json", "docs/evidence/gatebraid/P2-S1/captures/E-meta.json", "docs/evidence/gatebraid/P2-S1/captures/E-precedent-2.json", "docs/evidence/gatebraid/P2-S1/captures/E-precedent-3.json", "docs/evidence/gatebraid/P2-S1/captures/E-refns.json", "docs/evidence/gatebraid/P2-S1/captures/E-remote.json", "docs/evidence/gatebraid/P2-S1/captures/G1-fields.json", "docs/evidence/gatebraid/P2-S1/captures/G1-verify-exit.json", "docs/evidence/gatebraid/P2-S1/captures/G1-verify-flip.json", "docs/evidence/gatebraid/P2-S1/captures/G1-writedomains.json", "docs/evidence/gatebraid/P2-S1/captures/M-verify-6.json", "docs/evidence/gatebraid/P2-S1/captures/M-verify-7.json", "docs/evidence/gatebraid/P2-S1/captures/M-verify-8.json", "docs/evidence/gatebraid/P2-S1/captures/Q1-falsify.json", "docs/evidence/gatebraid/P2-S1/captures/Q1-real.json", "docs/evidence/gatebraid/P2-S1/captures/Q2-falsify.json", "docs/evidence/gatebraid/P2-S1/captures/Q2-real.json", "docs/evidence/gatebraid/P2-S1/captures/Q2-superseded-check.json", "docs/evidence/gatebraid/P2-S1/captures/Q3-falsify.json", "docs/evidence/gatebraid/P2-S1/captures/Q3-real.json", "docs/evidence/gatebraid/P2-S1/captures/Q4-falsify.json", "docs/evidence/gatebraid/P2-S1/captures/Q4-real-json.json", "docs/evidence/gatebraid/P2-S1/captures/Q4-real.json", "docs/evidence/gatebraid/P2-S1/captures/Q5-falsify.json", "docs/evidence/gatebraid/P2-S1/captures/Q5-real-json.json", "docs/evidence/gatebraid/P2-S1/captures/Q5-real.json", "docs/evidence/gatebraid/P2-S1/captures/Q6-falsify-a.json", "docs/evidence/gatebraid/P2-S1/captures/Q6-falsify-b.json", "docs/evidence/gatebraid/P2-S1/captures/Q6-falsify-owner.json", "docs/evidence/gatebraid/P2-S1/captures/Q6-real.json", "docs/evidence/gatebraid/P2-S1/captures/Q7-falsify-a.json", "docs/evidence/gatebraid/P2-S1/captures/Q7-falsify-b.json", "docs/evidence/gatebraid/P2-S1/captures/Q7-real-blockedby.json", "docs/evidence/gatebraid/P2-S1/captures/Q7-real-blocking.json", "docs/evidence/gatebraid/P2-S1/gate0.json", "docs/evidence/gatebraid/P2-S1/gate1-exit-checklist.md", "docs/evidence/gatebraid/P2-S1/gate1.md"]
consults: []
repair_attempts: []
approvals:
  - type: "Plan Approval (G1→G2)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/8#issuecomment-5353895987"
    author: "MianliWang"
    at: "2026-08-20T09:16:22Z"
  - type: "State Packet Approval"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/8#issuecomment-5352888364"
    author: "MianliWang"
    at: "2026-08-20T07:38:58Z"
plan_hash: "8586225b414dee08db6f47d3f0b14b09f5547dfbba52596a2ce01fe4a64755f7"
allowlist_hash: "c17fca97c0a7af32faced1f895c62198a133068edf6dca58e43908b088af26a2"
evidence_files:
  - docs/evidence/gatebraid/P2-S1/gate2.md
```
