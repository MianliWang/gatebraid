<!-- Template: Gate 1 evidence file.
     Location (M2+): docs/evidence/gatebraid/<slice_id>/gate1.md.
     Gate 1 is READ-ONLY (temporary read-only team of ≤3 permitted; lead never
     in bypass mode; findings flushed to the issue before dissolution).
     Exit freezes the plan + write allowlist (protocols/gate-1-contract.md). -->

# Gate 1 evidence — <P_nn-S_nn>

## Plan (frozen at exit)

- Approach: <…>
- Exact `write_domains` allowlist: <list — becomes the frozen allowlist>
- Test plan (commands): <…>
- Risk notes: <…>
- Rollback note: <…>

## Team findings (if a read-only team ran)

<Flushed findings, per teammate role.>

## Exit checklist

- `gatebraid-gate1-exit-checklist` completed: <link/anchor> — all items pass

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@1
slice_id: P<nn>-S<nn>
gate: 1
environment: <…>
executor: Claude Lead
base_sha: <sha>
started_at: <ISO8601>
ended_at: <ISO8601>
result: needs_approval   # Gate 1 always exits into Needs Plan Approval
checks:
  - name: plan-complete
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: allowlist-exact
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: test-plan-has-commands
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: gate1-exit-checklist
    result: pass
    output_ref: "#exit-checklist"
plan_hash: "<sha256 of the frozen plan section>"
allowlist_hash: "<sha256 of the frozen allowlist>"
evidence_files:
  - docs/evidence/gatebraid/P<nn>-S<nn>/gate1.md
```

<!-- Exit: Gate = G1 passed; Workflow → Needs Plan Approval;
     Next Approval = Plan Approval (G1→G2); needs-human ON.
     A recorded human approval comment is the ONLY door to Gate 2. -->
