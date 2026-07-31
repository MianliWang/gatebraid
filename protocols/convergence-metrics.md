# Convergence metrics — are the contracts converging?

**Normative for measurement, not for gate behaviour.** Frozen at M2 Batch E,
**before Slice B produces any data**. Adopted from CONSULT-M2-01 Q1.

The question this exists to answer is whether the Gatebraid contracts are
settling or whether each slice keeps finding as much new breakage as the last.
That question has been argued in prose twice. It is not answerable in prose,
because both stories fit the same observations.

**Why these definitions are frozen now.** A classification adjusted after seeing
the data is worthless — it measures the classifier. The consult that proposed
these metrics contained, in the same document, a batch count written as "~6"
beside a list of nine names, and a ratio computed against the wrong denominator.
That is the same defect the metrics are meant to detect: **a number asserted
rather than counted.** So the definitions come first, and they do not move.

---

## 1. What counts as a batch

**The rule, not just the count.** A **batch** is one unit of approved work
announced to the executor as a single brief and carried to its own stop
condition. Concretely, one batch is:

- one `NEXT.md` (or one equivalent instruction in the session) that
- the operator has approved as a unit, and that
- ends at a declared stop condition with a readback report.

A batch is **not** subdivided by:

- the number of commits in it — Batch E has three approved commits and is one
  batch;
- the number of gates it traverses — Batch B-2 ran Gate 0 and Gate 1 and is one
  batch;
- a stop for approval inside it, when the same brief resumes afterwards.

A brief that is **superseded before completing** and then re-issued counts as
**two** batches if the first one executed anything, and one if it did not.
Batch C stopped at Gate 2's entry gate having committed ADR-0014; Batch C-2
resumed and completed. Both count.

**M2 = 9 batches:** Batch 0, A, A-2, A-3, B, B-2, C, C-2, D. Batch E is the
tenth and is the first measured under these definitions.

Superseded, non-executed drafts are not batches. The withdrawn ADR-0017 draft is
not a batch and not a defect: it was caught in review before reaching the
executor, which is the review working.

## 2. The unit of measurement: gate exits attempted

Defect density is per **gate exit attempted**, not per batch and not per slice.
A gate exit is *attempted* when the gate's actions have run and the executor
begins its exit sequence — including exits that then stop.

Slice A attempted **five**: Gate 0 twice (the first stopped at action 4 on the
`Environment` mismatch), Gate 1, Gate 2, Gate 3.

Per-batch counting was rejected: batches vary in size by an order of magnitude,
and the metric would move when brief-writing style changed rather than when the
contracts did.

## 3. The four metrics

### 3.1 `new_contract_defects / gate_exits_attempted`

A **new contract defect** is a defect found for the first time that **requires a
change to a contract, schema or template** to resolve. Three conditions, all
required:

- it was **not** already recorded as a known defect or a deferred item;
- resolving it changes a normative artefact — `protocols/`, `schema/`,
  `templates/`, or an ADR — not merely how an executor behaved;
- it was found **by executing the contracts**, not by reading them.

Excluded, and each exclusion is a rule rather than a judgement:

- **Environmental** — a tool, host or platform behaviour that no contract change
  fixes. Friction #10 (permission classifier), #18 (`gh` list-variable limit).
- **Cosmetic** — no normative artefact changes. Friction #1, #5.
- **Executor error** — the contract was correct and was misapplied. Friction #8
  (a flat YAML parser), #17 (a pre-recorded verdict) are *executor* errors that
  nonetheless produced template changes; where a defect has both a contract half
  and an executor half, it counts **once, as a contract defect**, because the
  contract change is what was needed.
- **Coordinator briefing errors** are counted separately (§3.5) and never as
  contract defects.

### 3.2 `resolved_defect_recurrence`

Does a defect already adjudicated by an ADR or a wording fix **reappear** in a
later slice? Counted as an integer, per slice, and **the target is zero**.

A recurrence is: the same normative artefact fails in the same way, after a
change intended to prevent exactly that. It is **not** a recurrence when a
*related* defect of the same class appears in a *different* artefact — that is a
new defect, and it is what §3.4 is for.

### 3.3 `contract_caused_round_trips`

Extra batches and human round trips caused **only** by contract defects. A round
trip caused by scope change, by an operator decision, or by a genuine external
blocker does not count.

Slice A's Gate 0 stop (`Environment` mismatch, no defined disposition) is one:
the contract had no routing, and a batch was spent adding it. Batch C's stop at
the entry gate is **not** one — the approval genuinely had not been recorded, and
the gate did what it should.

### 3.4 `normative_surface_delta`

Normative clauses **added, removed or modified** per slice, across `protocols/`,
`schema/`, `templates/` and `adr/`. A clause is one numbered decision, one
contract bullet, or one schema property.

This is the counterweight. Defect density can be driven to zero by writing more
contract, and a system whose rules grow without bound is not converging even if
each slice is clean. **Rising surface and rising defect density together is the
divergence signature.**

## 3.5 Recorded separately: coordinator briefing errors

Not a contract metric, but tracked because it was the subject of CONSULT-M2-01 Q6
and has its own remedy. A briefing error is unobserved state asserted as
established fact. Known: one in M1 Batch 2, one in M2 Batch D, one in the consult
document itself (the batch count). The remedy — briefs state preconditions as
conditions to re-observe — took effect at Batch E.

---

## 4. Slice A baseline, computed under these definitions

Slice A is the only end-to-end slice. Its friction log entries are #1–#24.

| Metric | Value |
|---|---|
| Gate exits attempted | **5** |
| New contract defects | **13** — friction #2, #3, #6, #7, #9, #11, #12, #14, #15, #16, #21, #22, #23 |
| **Defect density** | **13 / 5 = 2.6 per gate exit** |
| Resolved defect recurrence | **0** — no adjudicated defect reappeared |
| Contract-caused round trips | **2** — the Gate 0 `Environment` stop, and the ADR-0016 drift-check correction |
| Normative surface delta | **+7 ADRs** (0011–0017 span M2; 0011–0016 land during Slice A) plus contract, schema and template edits across 4 batches |

Not counted as contract defects, with the rule that excludes each: #1 and #5
(cosmetic), #10 and #18 (environmental), #4 (already ADR'd at the time it was
raised), #8 and #17 (executor error — though both produced template changes and
are counted once as contract defects above; #8 is *not* in the 13 because the
parser was the executor's, and the template change it prompted came later),
#13 (a coordinator ruling, not a defect), #19, #20 (editorial), #24 (known
state, not a defect).

**2.6 defects per gate exit is high, and it should be.** Slice A is the first
execution of contracts written without any execution behind them; the expected
shape is a large first number falling steeply. A first slice that found nothing
would have meant the gates were not being followed literally.

---

## 5. The pre-declared criterion

**Declared before the data exists.** Not to be adjusted afterwards.

**Provisional convergence** is supported when all three hold over the next three
end-to-end slices:

1. **median defect density below 1.3** — half of Slice A's 2.6;
2. **zero recurrence** of any resolved defect;
3. **contract-caused round trips falling** slice over slice.

**Divergence** is supported by either:

- **any recurrence** of a resolved defect, or
- **normative surface and new-defect density rising together** — more rules
  producing more breakage.

### The evidence is asymmetric, and the criterion says so

**A clean Slice B is only weak evidence of convergence.** Slice B may simply not
traverse the contract paths that break: it may not stop a gate, not hit a
platform default, not need a repair. Absence of defects in one slice is
consistent with both "the contracts are settling" and "this slice was easy".

**A recurrence is strong evidence of divergence.** It means a defect was
adjudicated, a fix was written, and the fix did not hold — which indicts the
process that produced the fix, not just the fix.

This is why the criterion requires **three** slices for convergence and **one**
recurrence for divergence. Anyone reading a single clean slice as vindication is
reading the weak half.

## 6. Recording obligation

Each slice's readback records the four values and the classification of every
friction entry raised, under §3's rules. **Classifications are assigned when the
entry is written, not retrospectively.** An entry whose classification is
disputed is recorded with both readings and the dispute noted, never silently
reassigned.
