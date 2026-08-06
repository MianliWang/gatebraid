<!-- Template: Gate 0 evidence file.
     Location (M2+): docs/evidence/gatebraid/<slice_id>/gate0.md in the working
     repo; cross-project artifacts in MianliWang/gatebraid/evidence/.
     Gate 0 is READ-ONLY: any write, fetch/pull, or branch creation is a
     contract violation (protocols/gate-0-contract.md). -->

# Gate 0 evidence — <P_nn-S_nn>

## Authority & baseline

- Repository identity / remote: `<git remote -v output>`
- Plan baseline: `<sha>` — the head of the base branch now, i.e. the tree this slice's plan will be made against. Recorded **here only**. The `Base SHA` Project field is set at Gate 2, from the head re-read after the `Writer Lease` is taken (ADR-0011 §9).
- Working tree: clean | **DIRTY — gate stopped**, `Next Approval = Dirty Baseline Acceptance`; no remediation of any kind, ever
- Environment check: Project `Environment` = `<value>` matches host `<evidence>`
- Tool versions: `<claude/gh/git/codex versions as run>`
- Slice metadata: `## gatebraid-metadata` parses against `gatebraid/slice@1`: pass | fail

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@1
slice_id: P<nn>-S<nn>
gate: 0
environment: <wsl|windows|macos-authority|mixed-see-prose>
executor: Claude Lead
base_sha: <sha>
started_at: "<ISO8601>"
ended_at: "<ISO8601>"
result: passed          # passed | stopped | needs_approval | blocked | human_diagnosis_required
checks:
  - name: repo-identity-and-remote
    command: "git remote -v"
    result: pass
    output_ref: "#authority--baseline"
  - name: base-sha-recorded
    command: "git rev-parse HEAD"
    result: pass
    output_ref: "#authority--baseline"
  - name: working-tree-clean
    command: "git status --porcelain"
    result: pass        # fail → result: stopped + Next Approval = Dirty Baseline Acceptance
    output_ref: "#authority--baseline"
  - name: environment-matches-host
    result: pass
    output_ref: "#authority--baseline"
  - name: tool-versions
    result: pass
    output_ref: "#authority--baseline"
  - name: slice-metadata-parses
    result: pass
    output_ref: "#authority--baseline"
evidence_files:
  - docs/evidence/gatebraid/P<nn>-S<nn>/gate0.md
notes: "<free text; do NOT record a transition the contract does not define>"

# --- If the gate STOPPED, use this shape instead of result: passed (ADR-0013) ---
# result: stopped               # or: blocked, for an error disposition
# stop_record:
#   stopped_at: "<action number and name>"
#   disposition: decidable      # decidable | error
#   next_approval: "<Dirty Baseline Acceptance | Environment Change>"   # decidable only
#   workflow: Blocked           # error only; pair with a typed needs_input comment
#   observed: "<what was measured>"
#   expected: "<what the record says>"
#   remediation_attempted: none # ALWAYS none — the schema enforces it
```

<!-- A claimed schema validation names its loader: interpreter path, PyYAML and jsonschema versions (friction #55). -->

<!-- Exit: Gate = G0 passed; Workflow → Gate 1 — Planning; handoff comment
     (gatebraid/handoff@1) on the Slice issue; Last Checkpoint updated. -->
