<!-- Template: Gate 3 evidence file.
     Location (M2+): docs/evidence/gatebraid/<slice_id>/gate3.md.
     Gate 3: human-approved publication only. Prohibited: force-push,
     publishing beyond the approved set, merging with red CI
     (protocols/gate-3-contract.md). -->

# Gate 3 evidence — <P_nn-S_nn>

## Publication record

- Human Release Approval: <approval comment URL> (terms: <…>)
- Automation precondition (ADR-0011 §6): no enabled Project rule closes an issue on merge or on a `Status` write — verified: yes | **no → stop, do not merge**
- Drift check against the Gate 2 fingerprint (ADR-0011 §2): head `<sha>` == recorded · tree `<sha>` == recorded · `git status --porcelain` empty — pass | **fail → back to Needs Review**
- Exact publication commands run (from the approved plan):
  - `<git push …>` → <output ref>
  - `<gh pr create … --draft/…>` → PR: <url>
- CI: `green` | `red` | `none-configured` — <run url, or why none exists>. `none-configured` is a recorded finding, not a pass (ADR-0011 §7)
- Merge: <merge SHA> per the approval's terms

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@1
slice_id: P<nn>-S<nn>
gate: 3
environment: <…>
executor: Claude Lead
base_sha: <sha>
active_branch: <branch>
started_at: <ISO8601>
ended_at: <ISO8601>
result: passed
checks:
  - name: staged-set-matches-gate2-handoff
    result: pass
    output_ref: "#publication-record"
  - name: automation-precondition
    result: pass
    output_ref: "#publication-record"
  - name: ci-status
    result: pass          # pass only for `green`; `none-configured` is a finding
    output_ref: "#publication-record"
  - name: merged-per-approval-terms
    result: pass
    output_ref: "#publication-record"
approvals:
  - type: "Release Approval (G2→G3)"
    comment_url: "<url>"
evidence_files:
  - docs/evidence/gatebraid/P<nn>-S<nn>/gate3.md
notes: "PR <url>; merge <sha>"
```

<!-- Exit: Gate = G3 passed; Workflow → Done; CLOSE the Slice issue (this is
     what releases native blocked-by dependents — ADR-0007); release the
     Writer Lease; clear Next Approval; handoff comment posted. -->
