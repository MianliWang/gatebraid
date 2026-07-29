# ADR-0007 — `requires_gate` dependency encoding

**Status:** Accepted · M1 (2026-07-29) · Product: Gatebraid (ADR-0010)
**Provenance:** report 11 D1 (the gap and the recommended resolution); report 12 §9 (confirmed encoding, scratch example); GitHub product facts verified in report 11 §2.6 (native dependencies unblock only when the blocking issue **closes**).

## Context

Gatebraid dependencies are gate-graded — "B requires A **Gate 1**" is different from "C requires A **Gate 3**" — but GitHub's native `blocked-by` primitive has exactly one unblock semantic: the blocking issue closing. Exploding each Slice into per-gate sub-issues to force everything native would quadruple issue count and bury the board.

## Decision

1. **Closure invariant.** A Slice issue is closed **exactly** when its Gate 3 completes (`Gate = G3 passed`). This makes native `blocked-by` semantics coincide with Gate-3 dependency semantics.
2. **`requires_gate: 3` → metadata + native `blocked-by`.** The dependency is recorded in the slice's `## gatebraid-metadata` block **and** as a native GitHub dependency; it gets the native Blocked badge.
3. **`requires_gate: 1` and `2` → metadata only.** Recorded in the `## gatebraid-metadata` block (`depends_on[].requires_gate`) and evaluated by frontier logic reading the predecessor's `Gate` field. **No native dependency is created** — native would wrongly wait for the predecessor's Gate 3 closure.
4. **No per-gate sub-issue explosion.** Rejected per report 11 D1(c).
5. **Accepted consequence:** the native Blocked badge reflects hard (Gate-3) dependencies only; soft dependencies surface through the frontier computation (M2 `next` skill; M3 `gatebraid-frontier`), not on the board. The Ready Frontier view is a candidate pool and never claims startability.

## Canonical example (the M1 scratch hierarchy encodes exactly this)

| Dependency | Metadata block | Native blocked-by |
|---|---|---|
| B requires A Gate 1 | yes (`requires_gate: 1`) | **no** |
| C requires A Gate 3 | yes (`requires_gate: 3`) | **yes** (C blocked-by A) |
| D requires B Gate 2 and C Gate 2 | yes (`requires_gate: 2`, both) | **no** |

## Consequences

- Frontier logic is mandatory for correctness of soft dependencies; in M1 it exists only as a manually derived expected-frontier table in the verification manifest — M1 claims no automatic computation.
- Closing a Slice early (before G3) would falsely release native dependents; the closure invariant is therefore guard-checked in M3.
