# ADR-0025 — The terminal disposition, and the Gates 1–3 pass ADR-0013 asked for

**Status:** Accepted · M2 (2026-08-07) · Product: Gatebraid (ADR-0010)
**Amends:** ADR-0013 §1 (two disposition kinds become three) and its
`needs-human` sentence (reconciled with spec §1). Executes ADR-0013's last
reopening condition — *"if Gate 1, 2 or 3 turn out to have verifications with
no stated failure disposition … the same treatment applies and should be done
in one pass"* — which is exactly what Slice C's Gate 2 hit.
**Provenance:** friction #72 (the pre-declared extension, and the label
conflict), #75 (no abort mechanics exist; the token's single occurrence means
re-planning), #76 (no Workflow option can say "aborted"), #77 (closure
forbidden by spec §2's invariant, three documents away), #78 (branch and
lease silences pulling in opposite directions); the P1-S3 disposition
comment `5221166545` and its executed defaults; RB-M2-I.

## Context

Slice C reached a state the contracts could not express. `repair_limit` was
spent, review 4 failed R3, the Human Diagnosis said "no fifth review" — and
ADR-0013, written from Gate 0 where every failure is recoverable, offered
only `decidable` and `error`. Termination first becomes reachable at Gate 2,
and the executor navigating it honestly had to record four separate silences
(#75–#78). Each was resolved correctly on the day — by the disposition
comment's defaults, by spec §2's closure invariant, by ADR-0003's lease
semantics — but a terminal outcome of the gate machinery is an observable
outcome, and ADR-0019 requires observable outcomes to be expressible.

## Decision

**1. There are exactly three disposition kinds.** ADR-0013's `decidable` and
`error` stand as written. The third is **terminal**: the slice's work ends
without publication.

**2. Terminal is reachable only from `Human Diagnosis Required`, only by the
operator.** The route is: repair budget exhausted (or blocker-recurrence
limit) → `Human Diagnosis Required` → an operator-authored disposition
comment on the Slice issue (ADR-0015 §2/§3 and ADR-0020 §4 apply to it as to
any door) directing termination. No gate, review outcome, or executor
judgment reaches terminal on its own. "No remediation, ever" carries over
from `decidable`: the record is disposed of as it stands.

**3. Terminal sorts every field into records and operational values** —
#78's transferable rule, adopted as the rule:

- **Records, retained:** `Active Branch`, `Base SHA`, `Last Checkpoint`,
  `Gate` (unchanged — it states the highest gate completed, which remains
  true), all committed evidence, and the git branch itself — **retained
  local, unpushed, undeleted**; it is the only durable trace of an attempt
  that published nothing.
- **Operational values, cleared:** `Writer Lease` (ADR-0003 makes it a
  blocking condition; a terminated slice must not obstruct a successor);
  `Next Approval` → `—`; the `needs-human` label comes off with the Workflow
  transition below.
- **The Slice issue is not closed.** Spec §2's invariant — closed iff
  `G3 passed` — governs, and closure is what releases native `blocked-by`
  dependents; a terminated slice delivered nothing. Stated here so no reader
  derives it from three documents away (#77).

**4. `Workflow` gains option 14: `Aborted`.** Terminal state of the field;
ADR-0019 satisfied at the slice level exactly as `none_configured` satisfied
it at the check level. Legal transition: **9 → 14 only** (`Human Diagnosis
Required` → `Aborted`), which encodes decision 2 structurally. Spec §1's
label coupling is unchanged (`needs-human` ⇔ Workflow ∈ {4, 9, 11} or typed
blocked) — entering `Aborted` therefore removes the label, and the Repair
Queue and Needs Me views shed the slice without filter changes.

**5. The `needs-human` sentence in ADR-0013 §1 is reconciled:** the label
follows spec §1 always. A `decidable` stop whose Workflow state is not one of
§1's label states sets no label (Gate 0's case, unchanged); where a stop
coincides with `Human Diagnosis Required` (reachable from Gate 2 on), spec §1
governs and the label is set until the state exits — to a resumed gate or to
`Aborted` (#72's conflict, resolved in spec §1's favour).

**6. The one-pass disposition tables for Gates 1 and 3** are drafted as
contract text in the same batch that lands this ADR, by walking each
contract's own verification list and assigning each failure one of the three
kinds — announced verification-by-verification and approved against the
announcement, not invented here away from the contracts' text. Gate 2's are
fixed by this ADR and the lived path: R1–R5 fail → `Repair Required` while
repair budget remains → the unified repair sequence as written → budget spent
→ `Human Diagnosis Required` → the human directs remediation-with-one-full-
re-review (the review-4 precedent) or terminal.

**7. Application to `P1-S3` (`gatebraid-scratch#4`).** The slice that forced
this ADR receives its state under it, as an announced batch action (the
ADR-0013 data-correction precedent): `Workflow → Aborted`; lease already
cleared, records already retained, issue open — verified, not re-done.

## Consequences

- An aborted slice is a first-class, queryable outcome. The successor-slice
  pattern (same scope, new issue, predecessor cited) runs against a truthful
  record.
- `Aborted` keeps Workflow at 14 options, within the 50-option cap; no view
  definition changes.
- ADR-0013 remains the Gate 0 authority it always was; this ADR is the pass
  its reopening condition booked.

## Reopening conditions

- A terminal state reached, or proposed, from anywhere but
  `Human Diagnosis Required`.
- A second terminal kind (e.g. superseded-by-redesign) genuinely distinct
  from `Aborted`.
- Frontier or native-edge logic found treating an `Aborted` slice as
  anything other than a non-delivering, non-blocking record.
