# Gate 0 contract — Authority & baseline (read-only)

**Normative.** Inherits the common rules of `gatebraid-control-plane-spec-v1.md` §4 (single writer per repository; Codex always read-only; no worktrees without a `Worktree Exception` approval; no API keys; resumable from Issue + fields + committed evidence + Git state alone; every gate ends with evidence file + `gatebraid/handoff@1` comment + `Gate`/`Workflow`/`Last Checkpoint` updates). Changes only by ADR.

## Entry

- Frontier verdict says the Slice is startable (M2: `next` skill reasoning; M3: `gatebraid-frontier`; M1: manual derivation only).
- `Executor = Claude Lead`; Workflow → `Gate 0 — Verifying`.

## Failure dispositions (ADR-0013)

Every verification below states what happens when it fails, in one of two kinds.
A check with no defined failure mode carries no information (ADR-0011 §4).

- **Decidable** — the state is defensible and the operator may accept it:
  `result: stopped`; set the matching `Next Approval`; the row reaches the human
  through that field, and `needs-human` is **not** set here (spec §1 governs the
  label and this is not one of its states). **No remediation, ever.**
- **Error** — nothing for a human to accept; something is wrong:
  `Workflow = Blocked` with a typed `needs_input` reason in a comment, which is
  the one case where spec §1 does set `needs-human`. Stop and report.

## Actions (all read-only)

1. Verify repository identity and remote. **Failure → error.**
2. Record the **plan baseline** — the head of the base branch now — into this evidence file. This is the tree the plan will be made against (ADR-0011 §9). It is *not* the commit `Active Branch` is cut from: that is chosen at Gate 2, after the `Writer Lease` is held, and only then written to the `Base SHA` Project field. **Cannot read the base branch head → error.**
3. Record working-tree cleanliness. **A dirty tree stops the gate**: `result: stopped`, `Next Approval = Dirty Baseline Acceptance` (the row enters Needs Me via `Next Approval`; the `needs-human` label is not set here — its coupling is exactly the spec §1 rule). **No remediation of any kind, ever** — no stash, no clean, no checkout, no "helpful" commit.
4. Verify the Project `Environment` field matches the **actual host this gate is running on** — not a target, not a preference. **Mismatch → decidable: `result: stopped`, `Next Approval = Environment Change`** (an option that already exists, spec §2). Do not write the field, do not edit the slice metadata, and do not reinterpret the check as being about a target environment (ADR-0013 §2).
5. Verify tool versions (Claude Code, `gh`, `git`, Codex CLI as relevant). **A required tool missing or non-functional → error.** A version differing from the record is **recorded only** and blocks nothing, unless the plan declares a dependency on that version, which is Gate 1's job to state.
6. Verify the slice's `## gatebraid-metadata` block parses against `gatebraid/slice@1`. **Failure → error.**

## Prohibited

Any write; any fetch/pull; branch creation; dependency installation; any state-changing Git command.

## Exit

- `docs/evidence/gatebraid/<slice_id>/gate0.md` written from `templates/gate0-evidence.md` (embedded `gatebraid/gate-run@1` block, `gate: 0`).
- `Gate = G0 passed`; Workflow → `Gate 1 — Planning`. **Every slice passes through Gate 1** — there is no shortcut to `Needs Plan Approval`. The former exception described a 2→4 transition absent from the spec's legal-transition table and would have produced a slice with no `plan_hash`, no `allowlist_hash` and no exit checklist, while Gate 2 requires an allowlist pinned at Gate 1 (ADR-0011 §8).
- Handoff comment posted; `Last Checkpoint` updated.
