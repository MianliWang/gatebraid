# Convergence metrics v2 — the M3 instrument

**Normative for M3 from the merge of the N0 draft PR (ADR-0029 §5).
`convergence-metrics.md` (v1, frozen at `3a96b71`) remains the M2
historical instrument and is not edited. Rationale for v2: v1 counted
defects in the contracts, and M2's closure records that the defect mass
which terminated three slices was never in the contracts.**

## 1. Unit and collection

The base unit remains the gate exit attempted; §5 fixes every metric's
own unit, scope and collection locus. Gate-exit- and slice-scoped
metrics are recorded at write time — working locus the batch readback,
authoritative home the slice's committed evidence records (§5).
Batch-scoped metrics are recorded by the batch readback at batch
close — a batch containing no slice still records them — and flushed to
the committed milestone record. Milestone-scoped
metrics are computed at closure from the committed series, never from
memory or narrative; no criterion consumes an uncommitted value.

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

## 5. Operational definitions and collection loci (normative)

Common rules. **Recording time:** at the unit's own event (gate exit,
stop, batch close, terminal disposition), never retrospectively;
classifications are assigned when the entry is written (v1 §6, kept).
**Classification authority:** the coordinator's adjudication recorded at
the next stop; disputes recorded with both readings (v1 §6, kept); the
operator rules where readings persist. **Terminal states:** per the
three-state rule below — `no_eligible_unit_ran`,
`undefined_zero_denominator`, and numeric zero are distinct and named.
**Correction:** by a superseding entry citing the original — never
silent edit. **Aggregation:** milestone reports publish the raw series
plus the named statistic; a median is taken only over delivered units.
**Metrics-file format:** fixed by `gatebraid/metrics@1`, frozen at N1
with the other shared interfaces (M3-PLAN §2) — no generator defines
its own output contract. Until that freeze, values collect in working
records only, and no criterion consumes them before then — none is
defined to (§3's readings and §7's gate all post-date N2).
**Three terminal states, never conflated:** `no_eligible_unit_ran` —
the metric's unit never executed in the period, the metric does not
move; `undefined_zero_denominator` — units ran but the denominator is
empty, reported as undefined and never as a number; numeric zero —
units ran and the numerator is genuinely zero, a real measurement.
Every report names which state it is in.

**Gate-exit-scoped** (recorded, per gate exit, in a metrics file
committed beside the gate record in the slice's evidence directory;
never inside the gate record):
- `new_contract_defects / gate_exits_attempted` — numerator and
  exclusions per v1 §3.1 verbatim; denominator per v1 §2 verbatim.
- `R3 first-pass rate` — numerator: gate exits whose R3 evidence review
  passes on its first review round; denominator: gate exits attempted
  that reached an R3 review; an exit aborted before R3 does not enter.
- `implementation test failures at review` — numerator: distinct failing
  implementation tests found in a gate review; denominator: gate reviews
  held.

**Slice-scoped** (working record at write time in the batch readback;
the authoritative committed home is the slice's evidence-directory
metrics file, **finalized at Gate 3 exit or at an operator-authored
terminal disposition — GitHub Issue closure is never the finalization
event**, so an aborted slice's metrics finalize with its terminal
record; the milestone closure record
aggregates by citation and never re-states independently — §4's
one-source clause; criteria consume the committed values):
- `contract recurrence` — integer per slice, v1 §3.2 verbatim; also an
  immediate alarm (§3).
- `evidence-only repair count` — repair attempts whose whole diff
  touches evidence artifacts only, from `repair_attempts[]`.
- `evidence-only abort rate` — numerator: slices reaching terminal
  disposition with implementation never red across all reviews (the
  M2-CLOSURE reading); denominator: slices started (first gate record
  written). Per-slice it is a flag; the rate is milestone-scoped.
- `human round trips per slice` — stops recorded in the slice's batches,
  typed by mechanism (door, exception, stop) and cause (contract defect,
  instrument defect, operator decision, external).
- `operator-attended work units` — operator actions (approval message,
  door, relay) recorded in the stop lists of batches serving this slice.
  A batch serving no slice, or more than one, records its units in the
  batch readback as unattributed phase overhead — never divided by
  formula among slices.
- `elapsed calendar time` — first gate record timestamp to Gate 3 exit
  or terminal disposition.
- `classification-falsification failures` — labels
  (`replayable`/`deterministic`/`covered`) refuted by their negative
  case, a re-run, or N3's coverage report; denominator: such labels
  asserted in the slice's evidence.
- `instrument defects per evidence run` — numerator: defects in
  committed instruments surfacing during evidence generation or
  validation, classified by the ADR-0028 ladder (narrative;
  hand-authoring; bytes/encoding; measurement domain; temporal/
  classification); denominator: evidence runs (one invocation of the
  committed generator producing a record).
- `evidence bytes / implementation bytes` — observational only, never a
  criterion (§2's declaration): numerator: byte total of the slice's
  committed evidence artifacts; denominator: byte total of the slice's
  implementation diff; both counted by `git` commands named in the
  record.

**Batch-scoped** (working record in the batch readback at close, slice
or no slice; the executor flushes the series to the committed milestone
closure record at the closure batch — that record is the committed home
criteria consume):
- `normative_surface_delta` — clauses added/removed/modified per batch;
  clause unit per v1 §3.4 verbatim; counted from the batch's diff by the
  executor, command named.

**Milestone-scoped** (computed at closure from the series):
- `delivered / started slices`; the abort rate over the abort flags; the
  convergence/divergence readings (§3); work units per delivered slice
  (attributed units only, phase overhead reported beside, never divided);
- `mutation kill rate` — numerator: mutations killed; denominator:
  mutations valid at the current frozen corpus version. A mutant
  adjudicated equivalent or invalid is reclassified only by an approved
  corpus change, recorded, and leaves the denominator from that freeze
  forward.
- `false-positive checks` — checks that failed work later adjudicated
  correct; `false-negative checks` — checks that passed and were refuted
  before Closure evaluation. Both from the friction log, adjudicated.
- `post-Gate-3 escaped defects` — defects in delivered work found after
  its Gate 3 exit, window closing at M3 Core Closure evaluation; a
  defect surfacing later is recorded against the then-current milestone
  with its origin slice named.
