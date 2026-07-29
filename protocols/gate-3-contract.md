# Gate 3 contract — Publication (human-approved)

**Normative.** Inherits the common rules of `gatebraid-control-plane-spec-v1.md` §4. Changes only by ADR.

## Entry

- Recorded human `Release Approval (G2→G3)` comment exists, including its terms (what may be pushed/merged and how). Workflow → `Gate 3 — Releasing`.

## Actions

1. **Drift check first:** verify the working tree and staged set match the Gate 2 handoff exactly. Any drift → back to `Needs Review`; no publication.
2. Run the **exact publication commands from the approved plan**: push `Active Branch`; open the PR linked to the Slice issue; watch CI; merge per the approval's terms.
3. Record PR URL and merge SHA in the evidence file.

## Prohibited

Force-push; publishing anything beyond the approved set; merging with red CI; improvised command variants.

## Exit

- `docs/evidence/gatebraid/<slice_id>/gate3.md` written from `templates/gate3-evidence.md` (`gate: 3`).
- `Gate = G3 passed`; Workflow → `Done`; **close the Slice issue** — closure is what releases native `blocked-by` dependents (ADR-0007), so it happens exactly here and never earlier.
- Release the `Writer Lease`; clear `Next Approval`; handoff comment posted; `Last Checkpoint` updated.
