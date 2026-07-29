# ADR-0004 — Claude Lead / Codex read-only Consultant separation

**Status:** Accepted · M1 (2026-07-29) · Product: Gatebraid (ADR-0010)
**Provenance:** report 09 §12 (CLAUDE-LEAD / CODEX-CONSULT v1); reports 02/08 (validated Codex sandbox boundary, `WRITE_BLOCKED` negative probes); report 12 §14.

## Context

Two frontier models are available under existing subscriptions. Roles must be cast so that the single-writer invariant (ADR-0003) is technically enforced, not merely conventional, and so that no API keys or credential handling enter the system.

## Decision

1. **Claude Code is the Lead:** planning, decomposition, implementation, tests, integration, long-lived project context via committed files (never provider-session persistence).
2. **Codex (`gpt-5.6-sol`) is the Consultant:** read-only adversarial review and stuck-point diagnosis, invoked with the validated boundary — `--ephemeral --sandbox read-only`, no bypass flags, snapshot disabled, subscription OAuth. The read-only guarantee is enforced by Codex's own sandbox flag (validated in reports 02/08), so the two models can never write concurrently: only one of them can write at all.
3. **Consult mechanics** (normative; see `templates/consult.md`, `schema/consult.schema.json`): the Lead writes a consult file — problem, constraints and forbidden operations, files in scope, hypotheses already tried with outcomes, embedded command outputs (evidence travels in the file; the Consultant cannot execute), explicit questions, required response schema. The response uses the fixed schema (findings / ranked root-cause hypotheses with file-path evidence / recommended change as suggestion text / risks / verification steps / confidence). The Lead independently verifies before applying anything — never blind-apply — and records `ACCEPT | PARTIAL | REJECT` with reasons. Maximum one structured rebuttal round each; persistent disagreement produces a decision memo with a minimal discriminating experiment and goes to the human (`Human Diagnosis Required`).
4. **Triggers:** the unified repair sequence position (ADR-0002 §4); hard architecture calls; parser/type-system/semantic design; security-sensitive diffs; conflicting evidence; low Lead confidence; mandatory pre-release adversarial review on Strict Gate slices; explicit human request; `consult_first: true` slices.
5. **Consult state** is visible in the Project (`Workflow = Codex Consultation`, `Executor = Codex Consultant` during the consult); artifacts are committed and linked from the Slice issue with before/after semantic Git fingerprints.
6. **No API keys, no credential handling, ever** — both CLIs run on their existing subscription auth, launched by the human or the Lead's approved shell step.

## Consequences

- Codex output is advice with evidence, never applied state; authority stays with the Lead and the human.
- One consult at a time globally (ADR-0003 §5 caps).
