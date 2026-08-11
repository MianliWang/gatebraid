# Convergence metrics v2 — the M3 instrument

**Normative for M3 from the merge of the N0 draft PR (ADR-0029 §5).
`convergence-metrics.md` (v1, frozen at `3a96b71`) remains the M2
historical instrument and is not edited. Rationale for v2: v1 counted
defects in the contracts, and M2's closure records that the defect mass
which terminated three slices was never in the contracts.**

## 1. Unit and collection

The unit remains the gate exit attempted. Every slice records, at write
time, the metrics below; batch readbacks aggregate them; the M3 closure
report publishes the series.

## 2. Four dimensions

**Contract quality** — new contract defects per gate exit (§3.1 of v1,
definition unchanged); contract recurrence (§3.2, definition unchanged);
normative surface delta per batch — a declared change from v1 §3.4's
per-slice denominator: M3's approved unit of work is the batch, and
normative growth accrues whether or not a slice runs; v1 §3.4 remains
the M2 reading. Reconciled with v1 §2's recorded rejection of per-batch
counting: that rejection governs the thresholded defect-density unit
and stands unchanged; surface delta is an unthresholded trend series,
and an M3 batch can contain no slice at all, leaving a per-slice
denominator undefined.

**Evidence quality** — R3 first-pass rate; instrument defects per
evidence run; evidence-only repair count; evidence-only abort rate;
classification-falsification failures (a `replayable`/`deterministic`/
`covered` label refuted by its negative case or by re-run).

**Delivery efficiency** — delivered / started slices; operator-attended
work units per delivered slice; human round trips per slice, typed by
mechanism (door, exception, stop) and by cause (contract defect,
instrument defect, operator decision, external) — the cause axis
succeeds v1 §3.3's contract-caused-only counter, which had no category
for M2's instrument-caused trips; elapsed calendar time per slice.
Evidence bytes / implementation bytes is recorded as an observational
ratio, never a target.

**Product quality** — implementation test failures at review;
false-positive checks (a check that failed correct work); false-negative
checks (a check that passed and was later refuted); mutation kill rate;
post-Gate-3 escaped defects.

## 3. Alarm and criterion semantics

- **Recurrence (§3.2) is an immediate alarm**: stop, adjudicate at the
  next stop point, record the ruling. It is no longer a standing
  divergence verdict; three unresolved alarms in a milestone escalate to
  a milestone-level review.
- **Convergence (M3 reading):** over three consecutive delivered slices —
  R3 first-pass = 100%, evidence-only aborts = 0, contract-defect density
  median < 1.3, work units per delivered slice non-increasing.
- **Divergence (M3 reading):** evidence-only abort recurring after the
  toolchain is in force; or mutation kill rate falling below 90% at any
  freeze; or false-negative checks recurring in one instrument after its
  corpus was extended for exactly that class.
- **Admission gate:** the business-admission checklist (M3-PLAN §7)
  consumes these series directly; no criterion is evaluated from memory
  or narrative.

## 4. Honesty clauses (carried from v1's lessons)

A metric moves only when its unit actually runs — no reading medians
over aborted attempts as if delivered. A claimed value names the command
that establishes it — for a value counted from committed records, the
counting command over those records (ADR-0018 §2a: an unrun check is not
evidence; the reader must be able to re-run what the writer relied on).
Numbers appearing in two homes cite one source (the #101/#115 class).
