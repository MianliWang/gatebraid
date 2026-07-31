<!-- Template: Slice issue body. The Slice is the unit of execution and
     approval (ADR-0002). Slice issues live in the working repository and are
     sub-issues of their Phase issue in MianliWang/gatebraid.

     Convention (normative, spec §9): the body contains one '## gatebraid-metadata'
     heading followed by exactly ONE fenced yaml block; parsers take the first
     such fence under that heading. Everything else is prose for humans.

     Sizing heuristic (GSD-derived, ADR-0010): a Slice body should decompose
     into 2–3 independently verifiable tasks; larger means split the Slice. -->

# <P_nn-S_nn> — <title>

## Goal

<What this Slice changes or produces, in one short paragraph.>

## Context

<!-- Story-context section (BMAD-derived, ADR-0010): everything an executor
     needs that is not obvious from the repo — prior decisions, links to the
     Phase/Stage, constraints, non-goals. -->
- Why now: <…>
- Non-goals: <…>
- Related: <links>

## Acceptance

- [ ] <Independently verifiable outcome 1, with its check command>
- [ ] <Independently verifiable outcome 2, with its check command>

## Gate evidence

<!-- Filled as gates complete: links to docs/evidence/gatebraid/<slice_id>/gateN.md -->

## gatebraid-metadata

```yaml
schema: gatebraid/slice@1
slice_id: P<nn>-S<nn>
stage: S<n>                # Stage issue: MianliWang/gatebraid#<n>
phase: P<nn>               # Phase issue: MianliWang/gatebraid#<n>
workflow_profile: classic
environment: windows       # wsl | windows | macos-authority | mixed-see-prose
                           # MUST equal the host Gate 0 runs on — not a target,
                           # not a preference. Gate 0 action 4 compares them.
risk: low                  # low | medium | high
depends_on: []
# depends_on:
#   - issue: MianliWang/gatebraid-scratch#<n>
#     requires_gate: 3     # 3 → ALSO create native blocked-by (ADR-0007)
#     reason: "<why>"
#   - issue: MianliWang/gatebraid-scratch#<n>
#     requires_gate: 1     # 1|2 → metadata only; NEVER native (ADR-0007)
#     reason: "<why>"
write_domains: []          # frozen at Gate 1 exit; empty = read-only slice
resource_locks: []         # e.g. project:<repo>:writer · test:<repo>:full-suite
repair_limit: 2
consult_first: false
parallel_mode: safe-single-writer   # isolated-write is reserved (v1.1+, per-slice approval)
```
