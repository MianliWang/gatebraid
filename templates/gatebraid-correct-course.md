<!-- gatebraid-correct-course — mid-slice change protocol, adapted from
     BMAD-METHOD's correct-course (MIT © BMad Code, LLC; renamed per
     ADR-0010 — the BMAD trademark is not reused).
     Invoked when Gate 2 discovers the frozen Gate 1 contract is wrong.
     The one absolute rule: NEVER silently widen the plan or allowlist. -->

# Gatebraid correct-course — <P_nn-S_nn>

## Procedure (normative)

1. **Stop.** No further edits from the moment the discovery is made. Commit
   nothing new outside what is already written; do not touch the newly
   discovered scope.
2. **Document the delta** (sections below) in the Slice issue as a comment and
   in the gate2 evidence file.
3. **Set state:** `Next Approval = Scope / Allowlist Change`; Workflow stays
   `Gate 2 — Implementing` (paused) or moves to `Blocked` with a `needs_input`
   reason; `needs-human` ON.
4. **Wait for the human decision.** Options: approve the re-freeze · narrow the
   slice · abort to re-planning (back to Gate 1) · abandon the slice.
5. **On approval:** update plan + `write_domains`; recompute and record new
   `plan_hash` / `allowlist_hash` in the evidence file; clear `Next Approval`;
   resume. The re-freeze is as binding as the original freeze.

## Delta record

- **What was discovered:** <the fact the plan didn't anticipate>
- **Why the frozen plan is wrong:** <which assumption failed, with evidence>
- **Proposed change:** <exact plan-task changes; exact allowlist additions/removals>
- **Blast radius:** <what the change makes possible that the approval didn't cover>
- **Alternative considered:** <the no-scope-change path and why it fails>

## Anti-patterns (each is a protocol violation)

- Editing a file outside the frozen allowlist "because it's obviously needed"
- Re-freezing without a recorded human approval comment
- Splitting the discovery across multiple small silent widenings
- Recording the delta after the edits instead of before
