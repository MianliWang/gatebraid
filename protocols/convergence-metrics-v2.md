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
normative surface delta per batch.

**Evidence quality** — R3 first-pass rate; instrument defects per
evidence run; evidence-only repair count; evidence-only abort rate;
classification-falsification failures (a `replayable`/`deterministic`/
`covered` label refuted by its negative case or by re-run).

**Delivery efficiency** — delivered / started slices; operator-attended
work units per delivered slice; human round trips per slice (typed:
door, exception, stop); elapsed calendar time per slice. Evidence bytes /
implementation bytes is recorded as an observational ratio, never a
target.

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

A metric next moves only when its unit actually runs — no reading medians
over aborted attempts as if delivered (v1 §5's asymmetry, kept). A
claimed value names the command or record that establishes it (ADR-0018
§2a). Numbers appearing in two homes cite one source (the #101/#115
class).
