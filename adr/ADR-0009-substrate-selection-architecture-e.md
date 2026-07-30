# ADR-0009 — Substrate selection: Architecture E

**Status:** Accepted · M1 (2026-07-29) · Product: Gatebraid (ADR-0010)
**Provenance:** report 12 §1 (executive decision), §4–§8 (framework audit, reuse matrix, weighted comparison 8.21/10 with sensitivity), §18–§19; report 11 (re-sequencing M0–M3).

## Decision

The Gatebraid substrate is **Architecture E**: a thin, standalone `gatebraid` Claude Code plugin built entirely on native primitives (skills, subagents, permissions, hooks, `/goal`, plugin `bin/`), with GitHub Issues + Projects + sub-issues + dependencies as the **only** engine of record, and with algorithms/templates **ported** (vendored, attributed, re-written) from the surveyed frameworks. **Zero runtime dependency on any external workflow framework.** Runtime upstreams are exactly: Claude Code (native features), `git`, `gh`, Codex CLI, GitHub. Plugin scripts: Python 3 stdlib only.

## Framework dispositions (recorded; no framework is installed or executed in any milestone — they enter as ADR/schema/template-level specification only)

| Framework | Disposition | What is taken (as owned, attributed ports — ADR-0010) |
|---|---|---|
| **Spec Kit** (github/spec-kit) | Design reference now; optional within-Slice runner at v1.1 **only** if all four §19 falsifiers pass; never a required backend; never the ledger | Gate/resume semantics, step taxonomy, workflow YAML shape, validation-first testing |
| **GSD** (gsd-build/get-shit-done) | **Reject** as dependency/extension/fork (multi-writer waves, `--no-verify`, local `.planning` authority, worktree toggle; maintainer discontinuity) | Wave/frontier grouping; file-overlap serialization (= `write_domains` conflict rule); checkpoint taxonomy; doctor concept; 2–3-task atomic sizing heuristic |
| **CCPM** (automazeio/ccpm) | **Reject** as runtime (worktree-per-epic, multi-writer, local ledger) | Epic-parent/sub-issue/mapping sync shape; `depends_on`/`parallel`/`conflicts_with` metadata semantics; progress-comment handoffs; "status is a script, not a model call" |
| **BMAD** (bmad-code-org/BMAD-METHOD) | Methodology donor only; never the task authority; trademarked name not reused | Readiness checklist → Gate 1 exit checklist; correct-course → mid-slice change protocol; story context → Slice body template; sprint-status → weekly portfolio brief (all renamed `gatebraid-*`) |
| **Superpowers** (obra/superpowers) | Port, do not install (worktree-centric workflow conflicts) | Skill-TDD as the **mandatory** acceptance method for Gatebraid's own skills (M2/M3); verification-before-completion → handoff contract; systematic-debugging → "new hypothesis" repair rule; code-review pair → reviewer subagents |
| **Paperclip / Hermes** | Unchanged — ADR-0005 / ADR-0006 | Assets/rules already recorded there |

## Structural decisions bound by this ADR

- **No workflow engine in v1**; ordering, pause, resume are properties of GitHub state + skills; bounded loops are metadata-declared limits enforced by the M3 guard.
- **No monolithic CLI**: M2 ships zero CLI; M3 ships 3–4 single-purpose, stateless, JSON-out scripts (`gatebraid-frontier`, `gatebraid-guard`, `gatebraid-doctor`, `gatebraid-snapshot`) in plugin `bin/`. No daemon, no database.
- **The not-built list (report 12 §18) is normative**: any addition to it requires a new ADR against this one.
- **Spec Kit v1.1 falsifiers (all four required)**: nested-step exact resume shipped; two consecutive minor windows without crash/validation-class `fix(workflows)` patches; a Gatebraid pilot workflow in `gatebraid-scratch` passes gate/resume/if/`continue_on_error` end-to-end; run-state-as-cache proven by delete-and-recover. Its shell-step interpolation surface keeps `shell` steps out of any future Gatebraid workflow regardless.

## Consequences

- Enforcement lives in Claude-native permissions first (report 11 D4), M3 guard hooks second, human approvals always — no framework would have removed that layer.
- Upstream drift in the surveyed frameworks is irrelevant by construction; ports are owned code.
