<!-- Template: Gate 3 evidence file.
     Location (M2+): docs/evidence/gatebraid/<slice_id>/gate3.md.
     Gate 3: human-approved publication only. Prohibited: force-push,
     publishing beyond the approved set, merging with red CI
     (protocols/gate-3-contract.md). -->

# Gate 3 evidence — <P_nn-S_nn>

## Publication record

- Human Release Approval: <approval comment URL> (terms: <…>)
- Closure preconditions (ADR-0012 §2) — **both required**:
  - (a) platform automation: no enabled Project rule closes an issue on merge or on a `Status` write — verified: yes | **no → stop, do not merge**
  - (b) this pull request: `closing_keywords: none` · `closing_issues_references: 0` — verified: yes | **no → stop, do not merge**
- Drift check against the Gate 2 fingerprint (ADR-0011 §2): head `<sha>` == recorded · tree `<sha>` == recorded · `git status --porcelain` empty — pass | **fail → back to Needs Review**
- Exact publication commands run (from the approved plan):
  - `<git push …>` → <output ref>
  - `<gh pr create … --draft/…>` → PR: <url>
- CI: `green` | `red` | `none-configured` — <run url, or why none exists>. `none-configured` is a recorded finding, not a pass (ADR-0011 §7); record it as `result: none_configured` in the check list (ADR-0019 §1)
- Pull request: <url> — **referenced, not duplicated.** This file records no merge SHA and no closure timestamp: GitHub holds the merge event and the closure event natively, and a second copy is a second source of truth that will drift (ADR-0017 §2). This file is written and committed **before** the merge and reaches the base branch through the pull request.

<!-- Consumer note (ADR-0017 §4): the authoritative Gate 3 record is the
     COMPOSITE of this file, the PR's merge event, the issue's closure event and
     the Project's Workflow. Reconstruct state by reading the native EVENT
     SEQUENCE, not the last state — an issue can be reopened and a comment can
     be edited, so "currently closed" and "was closed by Gate 3" are different
     claims. -->

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@1
slice_id: P<nn>-S<nn>
gate: 3
environment: <…>
executor: Claude Lead
base_sha: <sha>
active_branch: <branch>
started_at: "<ISO8601>"
ended_at: "<ISO8601>"
result: passed
checks:
  - name: staged-set-matches-gate2-handoff
    result: pass
    output_ref: "#publication-record"
  - name: closure-precondition-automation
    result: pass
    output_ref: "#publication-record"
  - name: closure-precondition-pull-request
    result: pass          # closing_keywords: none; closing_issues_references: 0
    output_ref: "#publication-record"
  - name: ci-status
    result: pass          # green -> pass; red -> fail; no workflow at all ->
                          # none_configured (ADR-0019 §1), which is a finding,
                          # not a pass, and not `skipped`
    output_ref: "#publication-record"
  # The merge and the closure are post-merge facts; they live in the composite record (ADR-0017 §1) — the PR's merge event, the issue's closure event, Workflow — and are not pre-attestable in a file written before the merge (friction #56).
approvals:
  - type: "Release Approval (G2→G3)"
    comment_url: "<url>"
    author: "<login observed at verification — must be MianliWang (ADR-0020 §4)>"
evidence_files:
  - docs/evidence/gatebraid/P<nn>-S<nn>/gate3.md
notes: "PR <url>. No merge SHA and no closure timestamp are recorded here — GitHub holds both natively and this file references rather than duplicates them (ADR-0017 §2)."
```

<!-- A claimed schema validation names its loader: interpreter path, PyYAML and jsonschema versions (friction #55). -->

<!-- Exit: Gate = G3 passed; Workflow → Done; CLOSE the Slice issue (this is
     what releases native blocked-by dependents — ADR-0007); release the
     Writer Lease; clear Next Approval; handoff comment posted. -->
