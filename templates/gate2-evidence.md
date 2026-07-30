<!-- Template: Gate 2 evidence file.
     Location (M2+): docs/evidence/gatebraid/<slice_id>/gate2.md.
     Gate 2: single writer under the frozen allowlist; commits yes, PUSH NO
     (publication is Gate 3). Repair sequence per ADR-0002 §4.
     Mid-slice scope discovery → templates/gatebraid-correct-course.md. -->

# Gate 2 evidence — <P_nn-S_nn>

## Implementation summary

- Human Plan Approval: <approval comment URL>
- Writer Lease taken: `<host>:<session-label>:<ISO8601>`
- Active Branch: `<branch>` (created from Base SHA `<sha>`)
- Scope: strictly inside the frozen allowlist (hash `<allowlist_hash>`)

## Verification outputs

<Declared test-plan commands with their outputs embedded or committed-log
referenced. Evidence, not assertion.>

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
