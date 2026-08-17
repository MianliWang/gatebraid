# ADR-0032 — the M3 evidence toolchain lands in the control repository, and a gated Slice may have the control repository as its working repository

**Status:** Accepted · M3 Batch N1E (2026-08-17) · Product: Gatebraid (ADR-0010)
**Amends:** `templates/release-approval.md` (the control-repository clause,
decision 3 below) — the first amendment this project makes to a template
rather than by supersession, and it is made explicitly because the ruling
would otherwise contradict committed text silently. Records
`consults/CONSULT-M2-01`'s two-repository division of labour as M2-scoped
(decision 4). `M3-PLAN.md` §2 and ADR-0028 §4 are unedited; this ADR
records the reading that resolves them.
**Provenance:** the N2 and N3 build sessions' stop reports and approval
drafts, 2026-08-17 (`_handoff/batch-n2/STOP-REPORT-M3-N2.md`,
`_handoff/batch-n3/STOP-REPORT-M3-N3-BUILD.md` and the two APPROVALS
drafts, all host-local under an ignored path); the coordinator's
adjudication of the same date; the operator's ruling, same date.
Re-issued as **rev 2** at the N1E adjudication (2026-08-17), two grounds
corrected in the open and no decision changed: the first draft's Context
misattributed `gatebraid-ready.py` to ADR-0029's provenance line — ADR-0029
names two scripts there (lines 9–11) and `gatebraid-ready` only in the
phase DAG (line 96), while `M2-CLOSURE.md:17–24` records that scope as
three attempts terminated at Gate 2 with nothing published — caught by the
executor's verify-before-adopt citation check; and decision 5's ground
"nothing committed named M3's" failed reproduction as a measurement claim —
45 committed fixture files carry `P2-S1` as synthetic data (coordinator
re-measurement at adjudication) — and is re-worded to survive it.

## Context

`M3-PLAN.md` §2 requires N2 (evidence generator) and N3 (independent
validator) to be built and "landed once through their own gate"
(ADR-0028 decision 4). Neither the plan nor any ADR says **which
repository** they land in, and both entry documents therefore instructed
their sessions to stop and ask rather than choose. Both did.

The committed record carries evidence in both directions, and every
citation below was verified against the frozen tree at
`1e2f11ae3b187a08a758b81b85de85d43f210757`:

*Toward the scratch repository* — `CONSULT-M2-01`: "`MianliWang/gatebraid`
(control: ADRs, protocols, schemas, templates)" and "`gatebraid-scratch`
(working repo where slices execute)"; `templates/slice.md`: "Slice issues
live in the working repository"; `templates/release-approval.md`: a
Release Approval does not authorise "any change to the control
repository"; ADR-0014/ADR-0016: a Slice's allowlist is `bin/` plus
`docs/evidence/gatebraid/<slice_id>/`; ADR-0029's provenance line:
`bin/gatebraid-snapshot.py` and `bin/gatebraid-frontier.py` are committed
in the scratch repository.

*Toward the control repository* — ADR-0009: the substrate is a plugin and
M3's scripts ship "in plugin `bin/`"; `M3-PLAN.md` §2 V item 10 verifies
install, uninstall and rollback of "the complete M3 deliverable set
(scripts, hooks, skills, schemas)" as one set; `M3-PLAN.md` §2 P's
Accept-when requires "the corpus-v2 freeze precedes the guard
implementation **in commit history**", which is unverifiable across two
histories; ADR-0028 §4 mandates "committed, falsified, reused **repository
tooling**" as the correction of the per-slice scratch tools M2 delivered
with P0 defects.

**The decisive fact is a precedent, not a derivation:** the only two M3
evidence instruments that exist — `fixtures/run-corpus.py` and
`fixtures/runner-selftest.py` — are already committed **in the control
repository**, landed under the operator's N1 approvals. The toolchain's
home was settled by an approved landing before the question was asked.

Two further facts belong in this record. The question was put to the two
sessions separately and answered separately — control for the generator,
scratch for the validator — which would have split a symmetric pair
across two repositories; that is a coordinator defect, recorded in the
friction log, and this ADR is its repair. And no available answer is a
pure reading of the record: whichever repository wins, committed text must
be amended. Decision 3 is that amendment, made in the open.

## Decision

**1. The M3 evidence toolchain lands in the control repository,
`MianliWang/gatebraid`, under `bin/`.** This binds N2's generator and N3's
validator identically, and every later member of the same family built
under M3 (guard, doctor, and the O0-hardened snapshot and frontier) unless
a later ADR says otherwise. The M2-era tools in the scratch repository are
**superseded where re-built, not moved**: no history is rewritten, and the
scratch copies remain the historical record of what M2 delivered.

**2. A gated Slice may have the control repository as its working
repository.** `templates/slice.md`'s rule is unchanged and now reads
straightforwardly: the Slice issue lives in the working repository — for
N2 and N3, that is `MianliWang/gatebraid` — as a sub-issue of its Phase
issue. The Slice's frozen allowlist keeps its ADR-0014/0016 shape:
`bin/` plus `docs/evidence/gatebraid/<slice_id>/`, and nothing else. A
control-repository Slice does not thereby gain permission to touch
protocols, schemas, ADRs, templates or the frozen corpus: those remain
outside every Slice allowlist and reachable only by a contract batch or an
approved N1 correct-course.

**3. `templates/release-approval.md`'s control-repository clause is
amended** to read, in substance: a Release Approval does not authorise a
contract-cleanup pass, or any change to the control repository **outside
the Slice's own frozen allowlist**. The clause was written when every
Slice executed in the scratch repository and its purpose was to stop a
Slice's scope creeping into the control repository; decision 2 preserves
that purpose exactly, by the allowlist rather than by the repository
name. The executing batch makes this edit and no other in that template.

**4. `CONSULT-M2-01`'s division of labour is M2-scoped.** Its sentence
remains true of M2 and is not edited (it is a consult record, not a
contract). From M3, the control repository additionally holds the
evidence toolchain and its corpus; the scratch repository remains the
rehearsal repository, and V's three admission slices still execute there,
on the installed stack.

**5. M3's phase number is P2.** `gatebraid/slice@1`'s `slice_id` pattern
is `^P[0-9]+-S[0-9]+$`; M2's phase P1 is closed and no committed
**governance record** assigns M3 a phase number. Committed corpus fixtures
do carry `P2-S1` as a synthetic identifier — 45 files, authored at N1 as
plausible test data before any phase ruling existed. They are fixtures,
not authority; this decision now makes that identifier N2's real slice
id, and the coincidence is named here so no later reader takes the
fixture data for a prior assignment. **N2 = `P2-S1`; N3 = `P2-S2`**;
later M3 Slices continue the series. The Phase P2 issue lives in
`MianliWang/gatebraid`.

## Consequences

- N2's and N3's evidence paths are `docs/evidence/gatebraid/P2-S1/` and
  `docs/evidence/gatebraid/P2-S2/` in the control repository; their gate
  records are `gate-run@2` with `bootstrap_exception: true`, their Gate 0
  authority is the operator-approved closed-set state packet, and their
  Gate 2 executions remain serialized on the single-writer lease.
- V item 10's deliverable set stays single-repository, which is what makes
  install, uninstall and rollback verifiable at all.
- `M3-PLAN.md` §2 P's "in commit history" is satisfiable: corpus and guard
  share one history.
- The first gated Slice in the control repository is a genuinely new
  event. Nothing about the gate contracts changes; what changes is the
  value of "the working repository" in them, which was always a variable.
- The two repositories in scope remain exactly two. This ADR introduces no
  identifier outside the permitted set.

## Reopening conditions

- A measured demonstration that a control-repository Slice cannot satisfy
  a gate contract as written — which would reopen decision 2, not
  decision 1.
- The plugin's packaging, when built, requiring a distribution boundary
  that the control repository cannot express.
- An operator ruling moving the toolchain, which supersedes this ADR
  rather than amending it.
