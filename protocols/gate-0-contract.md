# Gate 0 contract — Authority & baseline (read-only)

**Normative.** Inherits the common rules of `gatebraid-control-plane-spec-v1.md` §4 (single writer per repository; Codex always read-only; no worktrees without a `Worktree Exception` approval; no API keys; resumable from Issue + fields + committed evidence + Git state alone; every gate ends with evidence file + `gatebraid/handoff@1` comment + `Gate`/`Workflow`/`Last Checkpoint` updates). Changes only by ADR.

## Entry

- **Position the working tree:** verify `HEAD` is at the base branch, or run `git checkout <base-branch>` to put it there — performed **before** the gate's read-only actions begin (friction #84; the one-time operator authorization of 2026-08-08, made standing). A retained branch (ADR-0025 §3) is a record, never the next slice's silent baseline. Inside the gate, the prohibition on state-changing Git commands is unchanged.
- **Startability authority (re-pointed for M3 by `M3-PLAN.md` §2).** The verdict that the Slice is startable comes from a different source before and after O0, and the boundary is not a preference:
  - **Before O0** — an **operator-approved closed-set state packet**: the exact repositories and issues enumerated; direct read-only queries only; every non-zero query exit failing closed; no broad enumeration. The exact outputs and query identities are recorded in this gate's record by `checks[].output_ref` pointers to committed capture files, and the record is marked `bootstrap_exception: true`. This is a one-time, expiring boundary: it serves N2's and N3's own gate landings, expires at their Gate 3 completion, and **no later Slice may use it**.
  - **After O0** — the hardened `gatebraid-snapshot` / `gatebraid-frontier` pair.
  - **O0's own Gate 0** — the explicit third case (operator ruling 2026-08-12, recorded with the N1 approval entries): the expiry above ends the *bounded evidence bootstrap*, not packet-based state reading. O0's startability is read from a **fresh operator-approved closed-set state packet** under its own `State Packet Approval`, with `checks[].output_ref` pointers to committed capture files exactly as above, and **without** `bootstrap_exception` — N2 and N3 exist, so O0's records carry full validation and nothing about the bounded bootstrap applies. This is the packet mechanism's final enumerated use; from O0's Gate 3 exit the hardened pair is the sole startability authority.
  - The **unhardened** snapshot/frontier pair is **not** startability authority before O0. It fails open on the control plane's input — a non-zero `gh` exit folded into `None` drops a dependency edge silently, and an unknown Issue state is treated as unblocked (ADR-0029 decision 2, P0-1 and P0-4, both verified at source). A verdict from a tool that fails open is not a verdict.
  - Historical, for readers of older records: M2 used `next` skill reasoning; M1, manual derivation only.
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

1. Verify repository identity and remote. **Failure → error.** Enumerate the ref namespace with `git for-each-ref`: any ref outside `refs/heads/`, `refs/remotes/` and `refs/tags/` is **reported, not adopted** — a write into an unwatched namespace is invisible to `git status` and to every diff (friction #103).
2. Record the **plan baseline** — the head of the base branch now — into this evidence file. This is the tree the plan will be made against (ADR-0011 §9). It is *not* the commit `Active Branch` is cut from: that is chosen at Gate 2, after the `Writer Lease` is held, and only then written to the `Base SHA` Project field. **Cannot read the base branch head → error.**
3. Record working-tree state as one predicate: `git status --porcelain` empty **and** `HEAD == <base-branch head>` (friction #84 — a clean tree at the wrong commit passes a cleanliness-only check, and Gate 1's dry-runs would then measure an artifact absent from the base branch). **A dirty tree stops the gate**: `result: stopped`, `Next Approval = Dirty Baseline Acceptance` (the row enters Needs Me via `Next Approval`; the `needs-human` label is not set here — its coupling is exactly the spec §1 rule). **No remediation of any kind, ever** — no stash, no clean, no checkout, no "helpful" commit. **HEAD not at the base branch → error** — entry positioning was sanctioned and did not land; something is wrong.
4. Verify the Project `Environment` field matches the **actual host this gate is running on** — not a target, not a preference. **Mismatch → decidable: `result: stopped`, `Next Approval = Environment Change`** (an option that already exists, spec §2). Do not write the field, do not edit the slice metadata, and do not reinterpret the check as being about a target environment (ADR-0013 §2).
5. Verify tool versions (Claude Code, `gh`, `git`, Codex CLI as relevant). **A required tool missing or non-functional → error.** A version differing from the record is **recorded only** and blocks nothing, unless the plan declares a dependency on that version, which is Gate 1's job to state.
6. Verify the slice's `## gatebraid-metadata` block parses against `gatebraid/slice@1`. **Failure → error.**

## Prohibited

Any write; any fetch/pull; branch creation; dependency installation; **any state-changing Git command against the slice's working tree or branches**. Writing and committing this gate's own evidence file is the Exit step and is **not** a violation: the prohibition protects the baseline under inspection, and ADR-0001 requires the evidence to reach GitHub to exist at all.

## Exit

- `docs/evidence/gatebraid/<slice_id>/gate0.md` written from `templates/gate0-evidence.md` (embedded `gatebraid/gate-run@2` block, `gate: 0`). Every M3 gate record is `@2` from the first; `@1` is the frozen historical schema and no new M3 record falls back to it (ADR-0029 decision 2, P1-1).
- `Gate = G0 passed`; Workflow → `Gate 1 — Planning`. **Every slice passes through Gate 1** — there is no shortcut to `Needs Plan Approval`. The former exception described a 2→4 transition absent from the spec's legal-transition table and would have produced a slice with no `plan_hash`, no `allowlist_hash` and no exit checklist, while Gate 2 requires an allowlist pinned at Gate 1 (ADR-0011 §8).
- Handoff comment posted; `Last Checkpoint` updated.
