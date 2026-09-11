# ADR-0037 — `gatebraid/gate-run@3` and `gatebraid/coverage-report@2`: the revision O0 owed, keyed on the sequence the record describes, and the validator revision it forces

**Status:** Proposed · M3 batch P-B1 (drafted 2026-09-10 by the coordinator;
Accepted on the operator's Batch Approval of the P-B1 pull request and its
merge; operator ruling R4 of 2026-09-09 chose a new version over an in-place
edit of `@2`) · Product: Gatebraid (ADR-0010)
**Amends:** nothing retroactively. `gatebraid/gate-run@2` is not edited and
not retro-broken: `@2` records stay valid as `@2` forever, exactly as `@1`
records stayed valid when `@2` was introduced (ADR-0029 P1-1). Every M3 gate
record from Slice P2-S7 on is written as `@3`.
**Provenance:** friction #193 (`_handoff/friction-log.md` `### 193.`: the
`allOf[0]` conditional keys on a bare count while its own `$comment` describes
the D6 red-check sequence — a decidable stop the operator ruled by route A);
friction #194 (`### 194.`: two frozen structures could not express what
happened — no `Writer Assignment` approval type, and a qualification that
could live only in a YAML comment, invisible to `yaml.safe_load`); friction
#238(c) (`### 238.`: the P2-S5 record carries `consults: []` beside
`repair_attempts[1].consult_ref: CONSULT-17-01`, measured in
`docs/evidence/gatebraid/P2-S5/g2/gate2.md`, the fenced record's `consults`
and `repair_attempts` lines); the O0 closeout's "one `gate-run@2` revision, batch lane, by ADR,
three items" (`claude/m3-o0-state.md`); the research report for P-B1's
brief, flag 3 (`plan_hash` and `allowlist_hash` carry no pattern at `@2`
while `protocols/gate-1-contract.md` states "SHA-256, lowercase hex").

## Context

Three records written under `@2` met four limits the schema could not
express, and each record said so rather than misrepresenting the gate. The
O0 closeout queued one revision for all of them. P-B1 is the batch that
freezes node P's interfaces, and P2-S7 is the next Slice to write a gate
record, so the revision lands here, before the record that would meet the
limits a fourth time.

The operator chose a new version (`@3`) over an in-place edit of `@2`
(ruling R4). The reason is the same as at `@2`'s introduction: the change
adds a required member (`kind` on every repair attempt) that no committed
`@2` record carries, so an in-place edit would retro-break every committed `@2` record that
carries a repair attempt — history that ADR-0029 P1-1 promises to keep valid.
The corpus carries the promise as a falsifiable pair: the `@2` canonical
record valid as `@2` and invalid as `@3` (GR3-02, GR3-03), as GR2-02/GR2-03
did for `@1`/`@2`.

## Decision

**1. `repair_attempts[].kind`, required, in `red_check | record_correction`
(friction #193).** `red_check` is the D6 repair sequence of
`protocols/gate-2-contract.md` — a review or check red, a repair with a new
hypothesis; `record_correction` is a repair to the record itself under the
route-A ruling. Friction #94's conditional (`allOf[0]`) now keys on the
sequence its `$comment` always described: two `red_check` attempts, neither
carrying an in-sequence `consult_ref`, validate only as
`human_diagnosis_required`. Two `record_correction` attempts do not trip it
(GR3-05); one of each does not (GR3-06); two `red_check` without a consult
does (GR3-04). The positional cap of two and the `number` constants apply to
both kinds unchanged. The route-A guardrail of #193 — both the array and the
budget state "two spent, zero remaining, no third available" — is now
expressible in data (decision 3) rather than only in `notes`.

**2. `approvals[].type` gains `Writer Assignment` (friction #194).** The
operator's act that names the writer for Gate 2 is typed as itself (GR3-10);
at `@2` it could only be typed `Plan Approval`, so two distinct operator acts
read as one. `stop_record.next_approval` is unchanged: a Writer Assignment is
never a `Next Approval` option.

**3. Top-level `qualifications[]` (friction #194).** Each entry names the
`field` it qualifies, the `statement`, and what it is `cited` to — a ruling,
a friction entry, a contract clause. It is the data-layer home for a
statement a record could previously carry only in a YAML comment; the P2-S5
route-A caveat is its first instance in intent (GR3-11). An entry without its
citation is invalid (GR3-12): a qualification is a claim and names its
ground.

**4. `plan_hash` and `allowlist_hash` carry the 64-hex pattern the Gate 1
contract states** (GR3-13). At `@2` both were unconstrained strings.

**5. A `consult_ref` requires a roster (friction #238(c)).** `consults[]`
enumerates every consult the gate ran, in sequence or at the Human Diagnosis
stop; a `repair_attempts[].consult_ref` is a position in that roster. A
record that names a `consult_ref` while `consults[]` is empty — the P2-S5
record's shape — is invalid at `@3` (GR3-08); the same attempts with the
consult on the roster are valid (GR3-07). That the named `consult_ref`
matches a roster entry is cross-field membership the schema cannot express;
it is the validator's duty and is named in the corpus manifest's
`known_limitation` rather than left looking enforced.

**6. What is carried unchanged, and one character that is not.** Every other
property, conditional and description of `@2` stands in `@3` byte for byte
in intent, with the schema id, title and description moved to `@3` and each
delta's description added beside the field it changes. One carried
description (`environment`) contained U+2194 in `@2`; the scan over every file a
batch adds or modifies refuses that code point, so `@3` spells the pairing out in words — "windows
to windows and wsl to wsl". The meaning is unchanged. `@2` itself is frozen
history and is not edited for it; the residue is recorded here and in the
batch's ledger entry.

**7. `gatebraid/coverage-report@2`, the revision decision 6's promise
forces, and IN-01's home.** `gatebraid/coverage-report@1` names its target by
a closed `schema_id` enumeration — `evidence-capture@1`, `gate-run@2`,
`metrics@1` — so the validator could not name a `@3` record at all: the
first `@3` gate record would be a record the independent validator cannot
route, which is the ADR-0019 class (an outcome that cannot be expressed).
`schema/coverage-report-v2.schema.json` (`gatebraid/coverage-report@2`)
adds `gatebraid/gate-run@3` to that enumeration (IN2-04; the `@1` report
over a `@3` target is invalid, IN2-05, which is why `@2` exists). The same
revision is the home the one unfrozen M3-PLAN §6 item needed: IN-01, "wrong
pipeline exit code", which the N1E correct-course re-assigned from the
N3-start freeze to corpus v2 at P's start because its assertion spanned two
documents (`fixtures/instruments/EXPECTATIONS.json` `known_limitation` (2);
`fixtures/DETERMINACY-REPORT.md` §7). A verified property may now carry
`exit_code_basis` — the validator's reading of the target capture's
`invocation.form` and `shell_semantics` — and the schema binds it in both
directions: a basis that is uninterpretable cannot sit beside a passing
verdict (IN2-02), and a shell basis without `pipefail` whose exit code is
the pipeline's last element's is uninterpretable whatever the validator
wrote (IN2-03). The cross-document half — that the validator read the
capture correctly — is the validator's own falsification at P2-S7 against
EC1-02, EC1-07 and EC1-25, and is named in the corpus manifest's
`known_limitation`. `@1` is not edited; `@1` reports stay valid as `@1`
(IN2-01a). Corpus `instruments-v2/` carries all of this; corpus
`instruments/` (v1.1) is untouched and its re-assignment note is discharged
by the dated addendum to `fixtures/DETERMINACY-REPORT.md`.

**8. Templates.** `templates/gate0..3-evidence.md` declare
`gatebraid/gate-run@3` from this batch, carry `kind` and `qualifications` in
their commented record skeletons, and — a separate amendment landing in the
same batch for replay A's F-2 — prescribe no row that names `HEAD`,
`--abbrev-ref HEAD` or a bare branch name inside a replayable claim (ADR-0028
§2). Each row is classed `[instant]` (read once, excluded from the
deterministic subset) or `[pinned]` (full SHAs only, replayable).

## Consequences

- P2-S7's gate records are the first `@3` records; the evidence validator
  (N3's `bin/` tool) routes on the `schema` key and must accept `@3` beside
  `@2` and emit `coverage-report@2` — a validator change P2-S7's plan names,
  under its own falsification, against `instruments-v2/`.
- IN-01 is frozen. Every M3-PLAN §6 item now has a freeze point that has
  been reached: thirteen at O0's start, seven at N3's start, one here.
- The friction ledger's #193, #194 and #238(c) are discharged as queued
  items; their entries stay as written.
- Corpus `gate-run-v2/` is untouched and stays in `CORPORA.json` as `@2`'s
  history; `gate-run-v3/` is corpus v2's.
- Under M3-PLAN §5.1 this ADR is justified as a public-interface change; it
  is the one O0's closeout named, and the companion revision it forces is
  part of the same decision rather than a second ADR.

## Reopening conditions

- A `@3` record meeting a limit the four deltas do not cover — the same event
  a fourth time — returns here for `@4`, never for an in-place edit.
- The validator found unable to route `@3` at P2-S7 without touching `@2`'s
  path (decision 6's promise).
- A `kind` value the two members cannot name — a repair that is neither the
  D6 sequence nor a record correction — is a contract question for
  `protocols/gate-2-contract.md` first and this schema second.
