# Gate 0 contract — Authority & baseline (read-only)

**Normative.** Inherits the common rules of `gatebraid-control-plane-spec-v1.md` §4 (single writer per repository; Codex always read-only; no worktrees without a `Worktree Exception` approval; no API keys; resumable from Issue + fields + committed evidence + Git state alone; every gate ends with evidence file + `gatebraid/handoff@1` comment + `Gate`/`Workflow`/`Last Checkpoint` updates). Changes only by ADR.

## Entry

- Frontier verdict says the Slice is startable (M2: `next` skill reasoning; M3: `gatebraid-frontier`; M1: manual derivation only).
- `Executor = Claude Lead`; Workflow → `Gate 0 — Verifying`.

## Actions (all read-only)

1. Verify repository identity and remote.
2. Record the **plan baseline** — the head of the base branch now — into this evidence file. This is the tree the plan will be made against (ADR-0011 §9). It is *not* the commit `Active Branch` is cut from: that is chosen at Gate 2, after the `Writer Lease` is held, and only then written to the `Base SHA` Project field.
3. Record working-tree cleanliness. **A dirty tree stops the gate**: `result: stopped`, `Next Approval = Dirty Baseline Acceptance` (the row enters Needs Me via `Next Approval`; the `needs-human` label is not set here — its coupling is exactly the spec §1 rule). **No remediation of any kind, ever** — no stash, no clean, no checkout, no "helpful" commit.
4. Verify the Project `Environment` field matches the actual host.
5. Verify tool versions (Claude Code, `gh`, `git`, Codex CLI as relevant).
6. Verify the slice's `## gatebraid-metadata` block parses against `gatebraid/slice@1`.

## Prohibited

Any write; any fetch/pull; branch creation; dependency installation; any state-changing Git command.

## Exit

- `docs/evidence/gatebraid/<slice_id>/gate0.md` written from `templates/gate0-evidence.md` (embedded `gatebraid/gate-run@1` block, `gate: 0`).
- `Gate = G0 passed`; Workflow → `Gate 1 — Planning`. **Every slice passes through Gate 1** — there is no shortcut to `Needs Plan Approval`. The former exception described a 2→4 transition absent from the spec's legal-transition table and would have produced a slice with no `plan_hash`, no `allowlist_hash` and no exit checklist, while Gate 2 requires an allowlist pinned at Gate 1 (ADR-0011 §8).
- Handoff comment posted; `Last Checkpoint` updated.
