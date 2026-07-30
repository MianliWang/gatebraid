<!-- Template: Gate 3 evidence file.
     Location (M2+): docs/evidence/gatebraid/<slice_id>/gate3.md.
     Gate 3: human-approved publication only. Prohibited: force-push,
     publishing beyond the approved set, merging with red CI
     (protocols/gate-3-contract.md). -->

# Gate 3 evidence — <P_nn-S_nn>

## Publication record

- Human Release Approval: <approval comment URL> (terms: <…>)
- Drift check: working tree and staged set match the Gate 2 handoff exactly: pass | **fail → back to Needs Review**
- Exact publication commands run (from the approved plan):
  - `<git push …>` → <output ref>
  - `<gh pr create … --draft/…>` → PR: <url>
- CI: <run url> — green
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
  - name: ci-green
    result: pass
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
