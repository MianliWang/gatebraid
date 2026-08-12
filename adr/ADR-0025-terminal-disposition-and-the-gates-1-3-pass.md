# ADR-0025 — The terminal disposition, and the Gates 1–3 pass ADR-0013 asked for

**Status:** Accepted · M2 (2026-08-07) · Product: Gatebraid (ADR-0010)
**Amended:** 2026-08-09 (M2 Batch K), from the terminal disposition's first
execution — §3 sorts records into immutable and narrative and gains the
working-tree sentence (friction #98, #84); §4's transition wording is made
directional (#79 raised the kind question, #80 the direction contradiction);
§6 is brought into agreement with the tables as landed at `78c4a1a`; §8 and
§9 are added (#85 — the third reopening condition, fired on its first run —
and #81). Decisions 1, 2, 5, 7 unchanged.
**Amended:** 2026-08-12 (M3 Batch N1) — §3 gains the metrics-finalization
reference, by `M3-PLAN.md` §2 N1's contract-reconciliation item
("the terminal-disposition procedure gains its metrics-finalization
reference"); the rule itself lives in `protocols/convergence-metrics-v2.md` §5
and is cited, not restated. No other decision touched.
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
comment `5221166545` and its executed defaults; RB-M2-I. For the Batch K
amendment: #79, #80, #81 (read-found, uncounted), #84's fifth silence, #85
(counted), #98 (counted); the P1-S5 terminal execution record; RB-M2-J.

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

The first formal execution of this ADR (P1-S5, RB-M2-J) then measured what
drafting from a clearing-question could not see: a retained field whose
content the transition falsifies (#98), a retained branch left checked out
as the next slice's silent baseline (#84), a frontier presenting the aborted
slice beside its live successor (#85), and two wording defects found by
reading (#79, #80). The Batch K amendment resolves all five here, in the
document that owns them.

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
#78's transferable rule, adopted as the rule; the record class split by its
first execution (#98):

- **Immutable records, retained byte-for-byte:** `Active Branch`,
  `Base SHA`, `Gate` (unchanged — it states the highest gate completed,
  which remains true), all committed evidence, and the git branch itself —
  **retained local, unpushed, undeleted**; it is the only trace of an
  attempt that published nothing, durable exactly as far as the disposition
  comment's citation of its name and head SHA makes it so.
- **The narrative record, written once more:** `Last Checkpoint` is a
  sentence about the present, and the transition moves the present. Its
  history is not erased; the disposition writes one final checkpoint of
  fixed content — `<ISO8601> — Aborted per <disposition comment id> ·
  branch <name> at <head sha>, local, unpushed · Gate <value>` — and
  nothing else, so it cannot be improvised either. The general rule, worth
  more than the instance: **a state transition states what happens to every
  field whose value is a sentence about the state.**
- **The metrics record, finalized here** (added at N1): the slice's metrics file
  reaches its authoritative committed value at this disposition, carried on the
  control plane in the disposition itself.
  **`protocols/convergence-metrics-v2.md` §5 (Slice-scoped) is the single home
  of that rule and of its reasons**; this bullet points at it and does not
  repeat it, so the two cannot drift (ADR-0029 decision 3's rationale, and
  metrics v2 §4's one-source clause). The *Slice issue is not closed* bullet
  below is why issue closure could not be this event even in principle.
- **Operational values, cleared:** `Writer Lease` (ADR-0003 makes it a
  blocking condition; a terminated slice must not obstruct a successor);
  `Next Approval` → `—`; the `needs-human` label comes off with the Workflow
  transition below.
- **The working tree:** the disposition ends with the clone checked out at
  the base branch (#84's fifth silence — the retained branch is a record,
  not a working position, and leaving it checked out sets a trap Gate 0's
  entry positioning now also closes from its side).
- **The Slice issue is not closed.** Spec §2's invariant — closed iff
  `G3 passed` — governs, and closure is what releases native `blocked-by`
  dependents; a terminated slice delivered nothing. Stated here so no reader
  derives it from three documents away (#77).

**4. `Workflow` gains option 14: `Aborted`.** Terminal state of the field;
ADR-0019 satisfied at the slice level exactly as `none_configured` satisfied
it at the check level. **The only transition into `Aborted` is from 9**
(`Human Diagnosis Required`), which encodes decision 2 structurally. State
9's other exit is not a Workflow edge of its own: operator-directed
remediation runs **under** `Human Diagnosis Required`, and its success
re-enters the machinery at the state the directing gate's contract defines
for the completed step (Gate 2: the directed full re-review passing exits
as a passing review exits). Spec §1 states both (#80 — "9 → 14 only" read
as state 9's sole exit contradicted §6's remediation branch; the rule was
always about the edge's direction). Spec §1's label coupling is unchanged
(`needs-human` ⇔ Workflow ∈ {4, 9, 11} or typed blocked) — entering
`Aborted` therefore removes the label, and the Repair Queue and Needs Me
views shed the slice without filter changes.

**5. The `needs-human` sentence in ADR-0013 §1 is reconciled:** the label
follows spec §1 always. A `decidable` stop whose Workflow state is not one of
§1's label states sets no label (Gate 0's case, unchanged); where a stop
coincides with `Human Diagnosis Required` (reachable from Gate 2 on), spec §1
governs and the label is set until the state exits — to a resumed gate or to
`Aborted` (#72's conflict, resolved in spec §1's favour).

**6. The one-pass disposition tables for Gates 1 and 3** are drafted as
contract text in the same batch that lands this ADR, by walking each
contract's own verification list and assigning each failure **one of the
table kinds — in-machine routing, decidable, or error. `Terminal` never
appears directly in a table:** it is reachable only through the
Human-Diagnosis route decision 2 defines, and each table states that route
once rather than per row (#79; the tables as landed at `78c4a1a` carry
exactly this form, and this sentence follows them). The tables are announced
verification-by-verification and approved against the announcement, not
invented here away from the contracts' text. Gate 2's are fixed by this ADR
and the lived path: R1–R5 fail → `Repair Required` while repair budget
remains → the unified repair sequence as written → budget spent →
`Human Diagnosis Required` → the human directs remediation-with-one-full-
re-review (the review-4 precedent) or terminal.

**7. Application to `P1-S3` (`gatebraid-scratch#4`).** The slice that forced
this ADR receives its state under it, as an announced batch action (the
ADR-0013 data-correction precedent): `Workflow → Aborted`; lease already
cleared, records already retained, issue open — verified, not re-done.

**8. The Ready Frontier is a dependency verdict, not a work queue** (#85 —
the original third reopening condition, fired on the frontier's first run
after this ADR). The frozen frontier artifact (Slice B) computes exactly
what its docstring scopes: whether any `blocked_by` entry resolves to an
OPEN blocker. That verdict is one conjunct of workability, not workability:
**what may be worked on next = the candidate pool (`Workflow = Backlog`,
issue OPEN) ∩ no open blockers.** An `Aborted` slice is never a candidate,
whatever its edges say; the spec's design note ("readiness is derived …
from dependencies, Gate fields, leases, and locks") already names the
composition, and B's artifact is correct on its own terms and unchanged.
Any consumer — a Gate 0 entry, a coordinator brief, a future skill —
performs the intersection or does not claim readiness.

**9. Dependents of a terminated slice re-point at successor creation**
(#81, codifying the executed `#5 → #14` precedent). A native `blocked-by`
edge, or a metadata dependency, naming an `Aborted` slice is re-pointed to
the successor **when the successor is created**, as an announced action —
never before a successor exists, never silently. Until then the dependent
stays blocked in fact, whatever the edge resolver reports (§8), because a
terminated slice delivered nothing.

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
- Frontier or native-edge logic **presenting** an `Aborted` slice as
  available work without §8's candidacy intersection — the original
  condition, re-scoped now that #85 discharged its first firing into §8.
- A terminal disposition encountering a field, or a piece of host state,
  that §3's sort does not cover — the fifth silence (#84) was found by
  executing; a sixth is found the same way and lands here, not in practice.
