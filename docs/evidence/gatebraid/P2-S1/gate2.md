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
[... 52 of 62 lines elided; full output at docs/evidence/gatebraid/P2-S1/gate2-full/see note ...]
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
[... 52 of 62 lines elided; full output at docs/evidence/gatebraid/P2-S1/gate2-full/see note ...]
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
[... 30 of 37 lines elided; full output at docs/evidence/gatebraid/P2-S1/gate2-full/see note ...]

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
```

**V6 — negative criterion N1: no path outside the frozen allowlist**

```
$ git diff --name-only 5bc41d7667d1ae019b228d43ed1ef29ea5c0b928..HEAD | C:/Python312/python.exe -B _t6.py
[... 27 of 41 lines elided; full output at docs/evidence/gatebraid/P2-S1/gate2-full/see note ...]
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
```

## Review record

### Review 1

| Item | Verdict | Evidence |
|---|---|---|
| R1 allowlist confinement | | `#verification-outputs` V6 |
| R2 test-plan coverage | | `#verification-outputs` V1–V7 |
| R3 evidence is rows that reproduce | | `#verification-outputs`, `#entry-records` |
| R4 negative criterion | | `#verification-outputs` V6, V7 |
| R5 no prohibited action | | `#entry-records`, `#required-disclosures` |

**Reviewer rows** (the commands the reviewer ran, with outputs)
```
NOT RUN. The review has not been performed. This grant's step 3 ends at
Workflow -> Needs Review; the read-only review is a separate step under
Executor = Claude Read-Only Team. Verdicts are the reviewer's and are left
unfilled here -- the implementer never pre-fills them (templates/gate2-evidence.md).
```

- Reviewer write disclosure: `not applicable — no review has run`
- Rules given to the reviewer: `not applicable — no reviewer dispatched`

## Repair record

```
No repair attempt. No declared test command returned red at any point in this
gate; the repair sequence was never entered and repair_limit remains unspent.
```

## Required disclosures

- Deviations: **(1)** `result` is recorded as `needs_approval`, not the
  template's `passed`. The review that would justify `passed` has not run — this
  grant stops at `Needs Review` — and writing `passed` beforehand would be the
  implementer certifying its own gate, which ADR-0028 exists against.
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
- Reviewer write disclosure: `none — no reviewer has run`
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
ended_at: "2026-08-20T09:02:41.103982Z"
result: needs_approval
bootstrap_exception: true
checks:
  - name: tests-green-per-plan
    command: "C:/Python312/python.exe -B bin/gatebraid-capture-selftest.py (Windows) and the WSL twin"
    result: pass
    output_ref: "#verification-outputs"
  - name: allowlist-respected
    command: "git diff --name-only 5bc41d7667d1ae019b228d43ed1ef29ea5c0b928..HEAD"
    result: pass
    output_ref: "#verification-outputs"
  - name: baseline-reread
    command: "git ls-remote origin refs/heads/main"
    result: pass
    output_ref: "#entry-records"
  - name: landed-blobs-match-bound
    command: "git ls-tree HEAD bin/"
    result: pass
    output_ref: "#verification-outputs"
  - name: review-five-items
    result: not_run
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
