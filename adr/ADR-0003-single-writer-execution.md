# ADR-0003 — Single-writer execution model

**Status:** Accepted · M1 (2026-07-29) · Product: Gatebraid (ADR-0010)
**Provenance:** report 09 §12 (single-writer invariant; validated Codex read-only boundary per 02/08); report 12 §1 (GSD/CCPM rejected as runtimes over multi-writer/worktree conflicts), §9–§12.

## Context

Every surveyed multi-agent framework (GSD waves, CCPM worktree-per-epic, Hermes lanes) is built around parallel committing writers. The operator's constraint set — auditable Strict Gate work on protected repositories — requires that at any moment, at most one process can be writing a given repository, and that this is knowable from the control plane.

## Decision

1. **One writer per repository.** At most one active writing session (the Claude Code Lead) per repository at a time; the Project's `Writer Lease` field (`<host>:<session-label>:<ISO8601>`, or empty) names it. Taking the lease is part of Gate 2 entry; releasing it is part of Gate 3 exit.
2. **No worktrees.** Per-task Git worktrees are prohibited. The only override is an explicitly approved `Worktree Exception` (`Next Approval` option), granted per slice, never a default.
3. **Everything else reads.** Planning/review teams (Agent Teams) are read-only; Codex is read-only always (ADR-0004); reviewers are read-only. Parallelism is for reading, never for writing.
4. **Branch-per-slice is permitted** (`Active Branch` field); commits during Gate 2 are frequent and local — **push is Gate 3 only**.
5. **Concurrency caps** (frontier policy): read-only teammates ≤3 per project, ≤5 global; project writers ≤2 global, 1 per project; heavy validation ≤1; Codex consultation ≤1 (report 12 §10).
6. **Reserved forward-compatibility:** `parallel_mode: isolated-write` exists in the slice schema as a reserved value only — per-slice, separately approved, v1.1+; never a default and never used in v1 (report 12 §8 Q14).

## Consequences

- The frontier computation must treat `write_domains` intersection and `Writer Lease` occupancy as blocking conditions (report 12 §10).
- A second writer appearing anywhere is a protocol violation and a stop-the-line event.
