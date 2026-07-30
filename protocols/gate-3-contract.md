# Gate 3 contract — Publication (human-approved)

**Normative.** Inherits the common rules of `gatebraid-control-plane-spec-v1.md` §4. Changes only by ADR.

## Entry

- Recorded human `Release Approval (G2→G3)` comment exists, including its terms (what may be pushed/merged and how). Workflow → `Gate 3 — Releasing`; **the `needs-human` label is removed** (this gate consumes the approval — spec §1, ADR-0011 §8).
- **Automation precondition (ADR-0011 §6).** Verify that no enabled Project automation closes an issue as a consequence of a merge or a status write. At the time of writing the built-in `Auto-close issue` rule does exactly that: it closes an issue whenever `Status` becomes `Done`, and `Status` is written to `Done` by other built-in rules including `Pull request merged`. A Slice's pull request is linked to its issue, so such a rule could close the Slice during step 2 below — before the evidence file exists and before `Gate = G3 passed` — releasing native dependents early and breaking the spec §2 invariant that a Slice is closed **iff** `G3 passed`. **If such a rule is enabled, stop and record the reason. Do not merge.**

## Actions

1. **Drift check first**, against the fingerprint Gate 2 recorded (ADR-0011 §2): current head equals `active_branch_head`; `git rev-parse HEAD^{tree}` equals `tree_sha`; `git status --porcelain` is empty. Any drift → back to `Needs Review`; no publication. Never accept "looks the same" — compare the recorded values.
2. Run the **exact publication commands from the approved plan**: push `Active Branch`; open the PR linked to the Slice issue; watch CI; merge per the approval's terms.
3. Record PR URL and merge SHA in the evidence file, and record CI status honestly as one of `ci: green` · `ci: red` · `ci: none-configured` (ADR-0011 §7). **`none-configured` is a recorded finding, not a pass:** where no check exists, the prohibition on merging with red CI is inert, and the evidence must say so rather than implying a check occurred. Neither Gatebraid repository has a workflow at the time of writing.

## Prohibited

Force-push; publishing anything beyond the approved set; merging with red CI; improvised command variants.

## Exit

- `docs/evidence/gatebraid/<slice_id>/gate3.md` written from `templates/gate3-evidence.md` (`gate: 3`).
- `Gate = G3 passed`; Workflow → `Done`; **close the Slice issue** — closure is what releases native `blocked-by` dependents (ADR-0007), so it happens exactly here and never earlier.
- Release the `Writer Lease`; set `Next Approval` back to `—`; handoff comment posted; `Last Checkpoint` updated.
