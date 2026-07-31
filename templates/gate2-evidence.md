<!-- Template: Gate 2 evidence file.
     Location (M2+): docs/evidence/gatebraid/<slice_id>/gate2.md.
     Gate 2: single writer under the frozen allowlist; commits yes, PUSH NO
     (publication is Gate 3). Repair sequence per ADR-0002 §4.
     Mid-slice scope discovery → templates/gatebraid-correct-course.md. -->

# Gate 2 evidence — <P_nn-S_nn>

## Implementation summary

- Human Plan Approval: <approval comment URL>
- Writer Lease taken: `<host>:<session-label>:<ISO8601>`
- Baseline re-read (ADR-0011 §9, as amended by ADR-0014 §1 and ADR-0019 §2): plan baseline `X` = `<sha from gate0.md>` · current head `Y` = `<sha>` · **`baseline: unchanged | changed-only-in-own-evidence | changed-outside-allowlist | changed-inside-allowlist`** — record this in every case, including no change.
  `changed-only-in-own-evidence` is the expected value once a slice has committed its own gate evidence: `X != Y`, and every changed path is inside `docs/evidence/gatebraid/<slice_id>/`, which ADR-0014 §1 excludes before the intersection test. It is not `unchanged`, and calling it `changed-outside-allowlist` is false — that directory *is* in the allowlist.
- Active Branch: `<branch>` (created from `Y`; the `Base SHA` field carries `Y`)
- Scope: strictly inside the frozen allowlist (hash `<allowlist_hash>`)

## Verification outputs

<Declared test-plan commands with their outputs embedded or committed-log
referenced. Evidence, not assertion.>

## Review verdict (read-only reviewer, ADR-0011 §4)

**Leave every verdict blank until the reviewer has reported.** The implementer
does not pre-fill this table, and `result:` in the metadata block below is the
**last** thing written in this file. A self-recorded pass on the one item whose
purpose is external verification is worthless even when it turns out correct —
Slice A's reviewer caught exactly that.

| Item | Verdict | Evidence |
|---|---|---|
| R1 allowlist confinement | | `git diff --name-only <base>..<head>` output |
| R2 test-plan coverage | | acceptance item → command mapping |
| R3 evidence is evidence | | which outputs were re-run or traced |
| R4 negative criterion | | the criterion, and how it was checked |
| R5 no prohibited action | | what was checked |

Reviewer ran as `Executor = Claude Read-Only Team`, no write tools. Any fail → `Repair Required`. Record what the reviewer found in this file that was wrong, if anything: a review that changes nothing is not evidence that it happened.

## Repair record (if any)

<Per attempt: the NEW hypothesis, what changed, result. Consult reference if
the sequence reached the Codex consult.>

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@1
slice_id: P<nn>-S<nn>
gate: 2
environment: <…>
executor: Claude Lead
base_sha: <sha>
active_branch: <branch>
started_at: <ISO8601>
ended_at: <ISO8601>
result: passed           # exits into Needs Review, then (reviewers pass) Needs Release Approval
checks:
  - name: tests-green-per-plan
    command: "<declared test command>"
    result: pass
    output_ref: "#verification-outputs"
  - name: allowlist-respected
    command: "git diff --name-only <base_sha>..HEAD"
    result: pass
    output_ref: "#implementation-summary"
  - name: baseline-reread
    command: "git rev-parse <base-branch>"
    result: pass
    output_ref: "#implementation-summary"
  - name: review-five-items
    result: pass
    output_ref: "#review-verdict-read-only-reviewer-adr-0011-4"
handoff_fingerprint:      # ADR-0011 §2, amended by ADR-0016 — Gate 3's drift comparand.
                          # These are the values at the moment the implementation was
                          # complete and reviewed, i.e. BEFORE this file's own commit.
                          # Gate 3 does not expect head equality; it requires that
                          # nothing outside docs/evidence/gatebraid/<slice_id>/ differs.
  active_branch_head: "<commit sha as reviewed>"
  tree_sha: "<git rev-parse <head>^{tree}, as reviewed>"
  changed_paths: []       # sorted `git diff --name-only <base_sha>..<head>`
repair_attempts: []
# repair_attempts:
#   - number: 1
#     hypothesis: "<new hypothesis>"
#     result: still_red
#     consult_ref: CONSULT-<issue#>-<seq>
approvals:
  - type: "Plan Approval (G1→G2)"
    comment_url: "<url>"
plan_hash: "<unchanged unless re-frozen via gatebraid-correct-course>"
allowlist_hash: "<unchanged unless re-frozen via gatebraid-correct-course>"
evidence_files:
  - docs/evidence/gatebraid/P<nn>-S<nn>/gate2.md
```

<!-- Exit: Workflow → Needs Review; reviewers (read-only) pass →
     Gate = G2 passed, Workflow → Needs Release Approval, needs-human ON. -->
