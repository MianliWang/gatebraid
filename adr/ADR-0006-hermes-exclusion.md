# ADR-0006 — Hermes exclusion (decision record only)

**Status:** Accepted · M1 (2026-07-29) · Product: Gatebraid (ADR-0010) · **This ADR records a decision made in report 10; it authorizes no action.**
**Provenance:** report 10 (full audit; `HERMES_CONTROL_PLANE_DECISION: REJECT`, `HERMES_EXECUTION_RUNTIME_DECISION: REJECT`, `INSTALL_PILOT_DECISION: NO_INSTALL` on production machines); report 12 §4G (unchanged).

## Decision

1. **Hermes Agent is excluded** from the production stack for all Gatebraid-governed projects: not the control plane (second, single-host, execution-presuming ledger), not an execution runtime (subscription inversion — its brain cannot run on the Claude Max included quota; Claude Code demoted to a scripted subprocess), and not installable on any production machine (its credential pool auto-ingests `~/.claude/.credentials.json`).
2. The bundled Hermes collaboration pattern (worktree + branch + `--full-auto`, Codex as committing second writer) is the operator's explicitly rejected pattern and does not enter Gatebraid in any form.
3. **No third-party consumer of `~/.claude/.credentials.json`, ever** (report 10 §12.5 / R12).

## Reopening conditions (all three required; report 10, restated in report 12 §4G)

(1) a first-class Claude Code worker lane exists upstream; (2) an Anthropic-sanctioned included-quota path for third-party harnesses exists; (3) single-writer / no-worktree / read-only-Codex operation is a first-class supported pattern. As of the 2026-07-27 audit none is met; no release since materially changes the structural result.

## Retained: the seven borrowed rules (already written into the Gatebraid spec)

(1) respawn guard — never relaunch on auth/quota failure or an already-open PR; (2) structured handoff metadata (`changed_files`, `verification` with owners, `residual_risk`) as the required completion trailer; (3) blocker-recurrence escalation — same cause twice → `Human Diagnosis Required`, deterministically; (4) review-required convention (the `Needs Review` state contract); (5) deterministic failure-loop breaker (repair limits enforced by script, not judgment); (6) managed-scope configuration (M3 option to root-pin the WSL-side settings baseline); (7) hard deny rules (native permission profiles).

## Consequences

- Hermes releases, however impressive, do not reopen this question implicitly; only the three conditions above do.
