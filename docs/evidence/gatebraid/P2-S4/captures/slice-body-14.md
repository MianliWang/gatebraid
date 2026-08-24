# P2-S4 — O0 snapshot/frontier hardening: the fail-closed pair

## Goal

Deliver the tool half of M3-PLAN §2 node **O0**: the hardened pair,
`bin/gatebraid-snapshot.py` and `bin/gatebraid-frontier.py`, landing in
the control repository per ADR-0032 decision 1 and implementing the O0
paragraph in full — P0-1 fail closed on auth, permission, rate-limit,
network, server, parse and unexpected-endpoint failures, with per-source
integrity status in the document; P0-2 explicit UTF-8 binary stdout, the
producer/consumer byte contract stated and tested with non-ASCII
fixtures; P0-3 every verdict-relevant connection paginated or
bounded-snapshot flags emitted, failing closed at any cap; P0-4 snapshot
schema/version required, Issue states validated against a closed enum
(unknown ⇒ `undecidable`, never unblocked), verdicts only for items
carrying Slice metadata, both dependency directions cross-checked,
declared soft dependencies parsed or the output says it did not,
Aborted/candidacy intersection per ADR-0025 §8, missing or incomplete
data ⇒ `undecidable`.

This Slice's two preconditions land **before its Gate 1, outside this
Slice, by the operator-approved batch O0-B1** (the N1 admission shape:
operator approval plus an independent read-only review before freeze):
the **snapshot-document schema** — O0's first deliverable — and the
**state-pipeline corpus**, the thirteen planned items built and frozen
against that schema (ADR-0031 decision 2), `CORPORA.json` moved
planned→built, `DETERMINACY-REPORT.md` remaining the single
classification home. This Slice consumes both frozen; it authors
neither.

## Context

- Why now: the DAG runs `{N2, N3} → O0 → O1`; the toolchain slices are
  closed (`#8`, `#10`, `#12`; PR `#13` merged) and O1 requires O0
  accepted. The unhardened M2 pair fails open (ADR-0029 decision 2,
  P0-1/P0-4, verified at source) and is not startability authority.
- Lane structure per ADR-0032 decision 2: a control-repository Slice's
  allowlist keeps the ADR-0014/0016 shape — `bin/` plus its evidence
  directory, and nothing else; schemas and the corpus are not Slice
  territory. They travel the batch lane, as every schema and fixture
  before them did (N1, N1E). The freeze-at-O0-start that ADR-0031
  decision 2 mandates is satisfied by O0-B1 preceding this Slice's
  Gate 1, so the frozen corpus precedes the implementation in commit
  history.
- The corpus digest **moves at O0-B1**, not in this Slice — the batch is
  the designed act, and it pins the new value by measurement at the
  freeze. Inside this Slice the batch-pinned digest is then held
  unmoved.
- This Slice's own Gate 0 is the state packet mechanism's **final
  enumerated use** (gate-0-contract Entry, the O0 case): full
  validation, no `bootstrap_exception`. From this Slice's Gate 3 exit
  the hardened pair is the sole startability authority.
- The M2-era tools in `MianliWang/gatebraid-scratch` are superseded
  where re-built, not moved (ADR-0032 decision 1); they remain the
  historical record and may be read as reference.
- Related: Phase P2 `#7` · P2-S1 `#8` · P2-S2 `#10` · P2-S3 `#12` ·
  PR `#13` · M3-PLAN §2 O0 · ADR-0025 §8 · ADR-0029 · ADR-0031 ·
  ADR-0032.

## Acceptance

- [ ] Both tools' outputs validate against the batch-frozen
      snapshot-document schema, schema/version required — P0-4's first
      clause demonstrated by the instruments' own summaries.
- [ ] The O0-B1 freeze precedes this Slice's implementation in commit
      history (fixtures precede the tool they test), and the
      batch-pinned corpus digest is unmoved by this Slice — both shown
      by measurement, not assertion.
- [ ] All state-pipeline fixtures pass on the declared platforms, and
      `undecidable` is demonstrably produced by **each** induced failure
      — M3-PLAN §2 O0's Accept-when, shown by seeded runs with summaries
      emitted by the instruments themselves.
- [ ] Fail-closed behaviour is demonstrated per class: each P0-1 failure
      class carries its induced case and per-source integrity status;
      P0-2's byte contract holds on non-ASCII fixtures on both
      platforms; P0-3 caps fail closed or flag; P0-4's closed enum
      yields `undecidable`, never unblocked, with both dependency
      directions cross-checked.

## Non-goals

No `schema/` or `fixtures/` write in this Slice — both are O0-B1's, the
batch lane (ADR-0032 decision 2). No edit to the four landed evidence
tools (`bin/gatebraid-capture*.py`, `bin/gatebraid-validate*.py`). No
edit to the M2 scratch copies. No O1 work (`gatebraid-ready` is O1's).
No guard or doctor work (P's). No edit to any merged historical record.

## Gate evidence

<!-- Filled as gates complete: docs/evidence/gatebraid/P2-S4/ -->

## gatebraid-metadata

```yaml
schema: gatebraid/slice@1
slice_id: P2-S4
stage: S2
phase: P2
workflow_profile: classic
environment: mixed-see-prose
risk: low
depends_on: []
write_domains:
  - bin/
  - docs/evidence/gatebraid/P2-S4/
resource_locks: []
repair_limit: 2
consult_first: false
parallel_mode: safe-single-writer
```

