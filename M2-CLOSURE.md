# M2 Closure Record — Gatebraid milestone M2 (2026-07-30 → 2026-08-10)

**Committed at repository root beside `M1-VERIFICATION-MANIFEST.md`, as that
manifest closed M1. Authority: the committed tree; this record cites, never
restates (ADR-0017 §2). Closure declared by ADR-0028 §5.**

## What M2 delivered

- **The delivery machine.** ADR-0011 through ADR-0028; the four gate
  contracts with full failure-disposition tables; `gatebraid/gate-run@1`,
  `consult@1`, `handoff@1` (with `consults[]`, the #94 conditional,
  `preserve_verbatim`); the ADR-0026 evidence templates; the terminal
  disposition (ADR-0025, amended from its own first execution);
  convergence-metrics as frozen at `3a96b71`.
- **Two slices, end to end:** P1-S1 (Slice A) and P1-S2 (Slice B), each
  through all four gates, published, issues closed.
- **The measurement chain.** Three attempts at one scope
  (`bin/gatebraid-ready.py`), all terminated at Gate 2 under operator
  disposition: P1-S3 (`gatebraid-scratch#4`, branch `344ae09`), P1-S5
  (`#14`, `9983a32`), P1-S6 (`#15`, `0df5a88`) — branches retained local,
  unpushed, undeleted (ADR-0025 §3). The implementation was green in every
  review of every attempt; every failure was in the evidence record. The
  chain of findings: narrative self-description is unwritable at standard
  (→ ADR-0026); hand-authoring persists past templates (→ mechanical
  generation); self-authored instruments each carry one unexamined trust
  point, ascending one level per repair (→ ADR-0028). The one instrument
  with zero failures across the span — the K4 schema conditional — was
  committed before use, falsified before trust, reused without rewrite;
  ADR-0028 makes that shape the law and hands M3 the toolchain mandate.

## Metrics, final (convergence-metrics §5, read as written)

| | A | B | P1-S3 | P1-S5 | P1-S6 |
|---|---|---|---|---|---|
| Gate exits attempted | 5 | 5 | 6 | 6 | 6 |
| Counted new contract defects | 13 | 8 | 3 | 6 | 4 |
| Density | 2.6 | 1.6 | 0.50 | 1.00 | 0.67 |
| §3.2 recurrence | 0 | 0 | 0 | 1 (#90) | 1 (ADR-0026 §1) |
| Contract-caused round trips | 2 | 1 | 0 | 2 | 1 |
| Outcome | delivered | delivered | Aborted | Aborted | Aborted |

Convergence half: **unevaluable** — two of three required end-to-end
slices. Divergence half: **met** — at P1-S5 on both grounds, at P1-S6 by
recurrence. Boundary finding: §3.1 counts contract defects; the defect mass
that terminated the attempts was never in the contracts.

## Open at closure, carried to M3

- The instrument toolchain (ADR-0028 §4) — M3's first delivery; the
  `gatebraid-ready` scope ships under it.
- `gatebraid-scratch#5`'s dependency points at aborted `#15`; re-points at
  successor creation only (ADR-0025 §9).
- #108's generator invariants — named in ADR-0028 §4, implemented with the
  toolchain. The skills batch (R1/R2) and enforcement design (ADR-0020 §6)
  remain queued as recorded in `_handoff/M1-STATUS.md`.
- `AGENTS.md` (7,503 B, untracked, #74's evidence) — disposal is the
  operator's.

## Record pointers

Batch readbacks `RB-M2-E` … `RB-M2-M` under `_handoff/reports/`; friction
log entries 1–114 at closure (session material; normative force only where
landed — ADR-0027 §3); disposition comments: `#4` `5221166545`, `#14`
`5229554313`, `#15` `5246821761` (its title's placeholder corrected by
follow-up comment); consults CONSULT-M2-01 (`consults/`), CONSULT-14-01
(branch `9983a32`), CONSULT-15-01 (branch `0df5a88`).
