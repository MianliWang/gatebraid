<!-- Template: Gate 2 evidence file — ADR-0026 shape.
     Location (M2+): docs/evidence/gatebraid/<slice_id>/gate2.md.
     Gate 2: single writer under the frozen allowlist; commits yes, PUSH NO
     (publication is Gate 3). Repair sequence per gate-2-contract.
     Mid-slice scope discovery → templates/gatebraid-correct-course.md.

     An instantiated file contains ONLY (ADR-0026 §1): (a) the
     gatebraid-metadata block; (b) record rows — fixed label, `$ command` line
     carrying its environment visibly (friction #89: GH_CONFIG_DIR and any
     other load-bearing variable ON the command line, in heredocs and
     sub-shells too), GENERATED output, never transcribed (friction #96);
     (c) the required disclosures below; (d) fixed headings and row labels.
     No narrative. No statements about this file's own revision history or
     prior reviews — the per-review rows ARE the record. No compliance claims
     about this file itself (friction #88). Attribution only with a
     machine-checkable citation (comment id, response line) or not at all
     (ADR-0026 §3). Elisions carry shown/total + the committed path of the
     full output. A proxy check prints its matching lines beside its count —
     a bare zero states what it searched (ADR-0018 §2; friction #87).
     ALL template comments are DELETED at instantiation.

     Identity-sensitive rows use identity instruments: `gh api user` for who,
     `gh api -i user | grep -i x-oauth-scopes` for what — never a data read
     (friction #89). Schema validations name their loader in the row
     (friction #55) and run as standalone guarded steps (spec §4; #86).

     Review discipline (contract, restated as instruction only): verdicts are
     written by the reviewer, last; the implementer never pre-fills them.
     Result: in the metadata block is the LAST thing written in this file.
     `bootstrap_exception: true` appears in the metadata block ONLY on N2's and
     N3's own gate landings, and only before O0. On THIS gate it records the
     BOUNDED EVIDENCE BOOTSTRAP, which is a different claim from Gate 0's: the
     record claims NO N3 independent validation, because N3 does not exist yet
     — N2's records are re-validated after N3's own Gate 3 — and the record is
     excluded from V's admission series. It requires a `State Packet Approval`
     in `approvals[]` and an `output_ref` on every check (gatebraid/gate-run@2
     enforces both). One-time and expiring: dead after N2 + N3 Gate 3, and no
     later Slice may use it (M3-PLAN §2). -->

# Gate 2 evidence — <P_nn-S_nn>

## Entry records

**E1 — Plan Approval verified** (author must be `MianliWang`, not this
session — ADR-0020 §4; hashes must match the frozen values)
```
$ GH_CONFIG_DIR=<store> gh api repos/<owner>/<repo>/issues/comments/<id> --jq '{author: .user.login, url: .html_url}'
<output>
$ GH_CONFIG_DIR=<store> gh api user --jq .login
<output — the executor identity the author is compared against>
```

**E2 — Writer Lease taken, read back**
```
$ GH_CONFIG_DIR=<store> gh <the field write + the read-back, in full>
<output — `<host>:<session-label>:<ISO8601>`>
```

**E3 — baseline re-read** (ADR-0011 §9; ADR-0014 §1 excludes
`docs/evidence/gatebraid/<slice_id>/` before the intersection)
```
$ git rev-parse <base-branch>
<output — Y; X is gate0.md's recorded baseline>
$ git diff --name-only <X>..<Y>
<output — the changed-path set before exclusion>
```
- baseline: `unchanged | changed-only-in-own-evidence | changed-outside-allowlist | changed-inside-allowlist`
  <!-- record in every case, including no change. changed-only-in-own-evidence
       is the expected value once a slice has committed its own gate evidence
       — it is not `unchanged`, and it is not `changed-outside-allowlist`:
       that directory IS in the allowlist. changed-inside-allowlist →
       Scope / Allowlist Change per the contract. -->

**E4 — Active Branch created from Y; `Base SHA` field set to Y**
```
$ git rev-parse --abbrev-ref HEAD; git rev-parse HEAD
<output>
```

## Verification outputs

<!-- One row per declared test-plan command, exactly as frozen. Evidence,
     not assertion. -->

**V<n> — <the acceptance item this command covers>**
```
$ <declared command, environment visible>
<output>
```

## Review record

<!-- One block per review, appended in order; blocks are never rewritten.
     The reviewer runs as Executor = Claude Read-Only Team under a read-only
     mandate it attests to, dispatched WITH the spec §4 conduct rules
     (friction #97); its report states which rules it was given. -->

### Review <n>

| Item | Verdict | Evidence |
|---|---|---|
| R1 allowlist confinement | | <anchor to the R1 row below> |
| R2 test-plan coverage | | <anchor — item → command mapping rows> |
| R3 evidence is rows that reproduce | | <anchor — which rows were re-run> |
| R4 negative criterion | | <anchor — pattern, scope, matches printed> |
| R5 no prohibited action | | <anchor — what was checked> |

**Reviewer rows** (the commands the reviewer ran, with outputs — including,
for R3's deterministic subset, the byte-identity re-runs)
```
$ <command>
<output>
```

**Findings** (only if any verdict is fail — one row per finding: what was
measured, not a story about it)
```
$ <the command that exhibits the defect>
<output>
```

- Reviewer write disclosure: `none` | <path — scope of what it affects>
- Rules given to the reviewer: <the mandate's rule set, one line>

## Repair record

<!-- One block per attempt. The hypothesis is ONE line. Novelty is measured
     before the result is graded (ADR-0027 §1; gate-2-contract): an unchanged
     tree is not a repair — record consumed, still_red, no re-review. -->

### Repair <n>

- Hypothesis (new): <one line>

**Novelty measured**
```
$ git rev-parse HEAD^{tree}
<output — compare: tree at the previous failed state was <sha>>
```

**Changed by this repair**
```
$ git diff --name-only <previous-failed-head>..HEAD
<output>
```

- Result: `green | still_red`
- Consult: `none | <consult_id> (in sequence — also on repair_attempts[].consult_ref) | <consult_id> (HDR-directed — recorded in consults, never as consult_ref: friction #94)`

## Required disclosures

- Deviations: none | <one line each, citing the friction entry or ruling>
- Reviewer write disclosure: `none` | <mirrored from the review record>
- Environment: <one line — host, shell, and every variable a recorded
  command's meaning depends on>

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P<nn>-S<nn>
gate: 2
environment: <…>
executor: Claude Lead
base_sha: <full 40-hex sha>
active_branch: <branch>
started_at: "<ISO8601>"
ended_at: "<ISO8601>"
result: passed           # exits into Needs Review, then (reviewers pass) Needs Release Approval
checks:
  - name: tests-green-per-plan
    command: "<declared test command>"
    result: pass
    output_ref: "#verification-outputs"
  - name: allowlist-respected
    command: "git diff --name-only <base_sha>..HEAD"
    result: pass
    output_ref: "#entry-records"
  - name: baseline-reread
    command: "git rev-parse <base-branch>"
    result: pass
    output_ref: "#entry-records"
  - name: review-five-items
    result: pass
    output_ref: "#review-record"
handoff_fingerprint:      # ADR-0011 §2, amended by ADR-0016 — Gate 3's drift comparand.
                          # Values at the moment the implementation was complete
                          # and reviewed, i.e. BEFORE this file's own commit.
  active_branch_head: "<full 40-hex commit sha as reviewed>"
  tree_sha: "<full 40-hex; git rev-parse <head>^{tree}, as reviewed>"
  changed_paths: []       # sorted `git diff --name-only <base_sha>..<head>`
consults: []              # every consult this gate ran, whenever it ran (friction #94)
repair_attempts: []
# repair_attempts:
#   - number: 1
#     hypothesis: "<new hypothesis — '(unchanged-tree)' annotated if consumed>"
#     result: still_red
#     consult_ref: CONSULT-<issue#>-<seq>   # in-sequence consults ONLY (friction #94)
approvals:
  - type: "Plan Approval (G1→G2)"
    comment_url: "<url>"
    author: "<login observed at verification — must be MianliWang (ADR-0020 §4)>"
plan_hash: "<unchanged unless re-frozen via gatebraid-correct-course>"
allowlist_hash: "<unchanged unless re-frozen via gatebraid-correct-course>"
evidence_files:
  - docs/evidence/gatebraid/P<nn>-S<nn>/gate2.md
```

<!-- Exit: Workflow → Needs Review; reviewers (read-only) pass →
     Gate = G2 passed, Workflow → Needs Release Approval,
     Next Approval = Release Approval (G2→G3), needs-human ON. -->
