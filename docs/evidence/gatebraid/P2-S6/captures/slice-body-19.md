# P2-S6 — snapshot live-transport repair: per-source endpoints, live-shape parsing, fail-closed preserved

## Goal

Repair the live half of `bin/gatebraid-snapshot.py` — the two defects
the P2-S5 Gate 0 stop diagnosed byte-exactly against the source that
ran: **D-A**, the live transport serves `issue_states`,
`dep_blocked_by` and `dep_blocking` from one bulk endpoint whose
response shape can never satisfy the classifier, with `page_index`
structurally unused; **D-B**, the page parser reads the
replay-transcript key shape and silently extracts zero rows from live
pages. After this Slice the pair reads the real control plane, and
`P2-S5`'s Gate 0 can re-run on the operator's word. The fail-closed
direction is preserved everywhere: an outcome nobody anticipated
degrades the snapshot, never passes through it. Scope is the snapshot
pair alone — `bin/gatebraid-snapshot.py` and
`bin/gatebraid-snapshot-selftest.py`; one Slice, one tool.

## Context

- Why now: `P2-S5` (`#17`) is parked on its Gate 0 stop — the
  startability authority cannot read the live control plane. Batch
  O1-B1 (approval `5448556399`, PR `#18`, merged by the operator)
  froze the ground this repair builds on: the four
  `gatebraid/live-*@1` schemas, the `live-shapes` corpus at digest
  `73c5e059…` (seven live transcripts as provenance, seven valid
  cases, four mutations), and ADR-0033.
- Startability for THIS Slice travels the operator's ruled exception
  (D-2, 2026-08-27): its Gate 0 runs the broken pair, and the
  reproduced deterministic failure — not a `startable` verdict — is
  the startability evidence, for this Slice only, ruled explicitly in
  its Gate 0 opening comment. The packet mechanism remains dead.
- The behavioural acceptance criteria below are SEED-SPEC-O1B1-v2
  §4's B-1..B-4, carried here verbatim under the O1-B1 Batch
  Approval's clause that they cannot silently drop.
- Related: Phase P2 `#7` · P2-S5 `#17` · P2-S4 `#14` · PR `#18` ·
  ADR-0033 · M3-PLAN §2 O0 (P0-1…P0-4) and O1 · SEED-SPEC-O1B1-v2.

## Acceptance

- [ ] Every O1-B1 transcript parses to the true item set: LS-01..07's
      bodies yield their measured envelopes and counts (15/15 items
      with per-item optional keys read byte-exactly, space-bearing
      names included; per-issue objects; dependency edge sets
      `[8, 10, 12, 14]` / `[]` / `[17]`).
- [ ] **B-1:** an item-list read where `len(items) < totalCount`
      (seed: the frozen C-4 body) yields incomplete/bounded —
      `complete: true` is the seeded wrong outcome.
- [ ] **B-2:** a bulk-list body offered as a per-issue dependency
      answer (seed: the frozen C-1 body) ends `undecidable` via the
      two-direction cross-check — never `startable`.
- [ ] **B-3:** an element with `workflow` absent (seed: C-3's frozen
      6-key element) maps to UNKNOWN, hence `undecidable` — never a
      KeyError, never a default toward healthy.
- [ ] **B-4:** the repaired `issue_states` source observes CLOSED
      issues; C-1 (open-only, the four blockers absent) beside C-5
      (the same blockers present and closed) is the frozen evidence
      that disqualifies the bulk endpoint.
- [ ] Each of B-1..B-4 is shown by seeded runs with summaries emitted
      by the instruments themselves — never by narration.
- [ ] The four `live-shapes` mutations stay killed and the entire
      frozen corpus passes unchanged; the frozen digest `73c5e059…`
      is unmoved by this Slice (shown by measurement).
- [ ] `bin/gatebraid-snapshot-selftest.py` is extended to exercise
      the live shapes via the O1-B1 transcripts, checker falsified
      before trust; the live transport's argv construction and
      classification are covered by declared commands — the F-04 debt
      paid at the level the frozen bodies allow.
- [ ] A captured live smoke read against the real control plane
      returns a healthy snapshot — every source `ok` and complete —
      whose `items` include `P2-S5`, and the frontier consumes it
      with exit 0; captured with `bin/gatebraid-capture.py`, not
      narrated.

## Non-goals

No edit to any tool but the snapshot pair — `bin/gatebraid-capture*`,
`bin/gatebraid-validate*`, `bin/gatebraid-frontier*` and
`bin/gatebraid-o0-acceptance*` are untouched (the frontier
identity-key change is its own later Slice per ADR-0033; the validate
stream-scope repair likewise). No `schema/` or `fixtures/` write —
both frozen, consumed only. No `gate-run@2` revision. No edit to any
merged historical record. No edit to `docs/evidence/gatebraid/P2-S5/**`
— the retained failure is evidence. No closure of, or gate action on,
`#17`.

## Gate evidence

<!-- Filled as gates complete: docs/evidence/gatebraid/P2-S6/ -->

## gatebraid-metadata

```yaml
schema: gatebraid/slice@1
slice_id: P2-S6
stage: S2
phase: P2
workflow_profile: classic
environment: mixed-see-prose
risk: low
depends_on: []
write_domains:
  - bin/
  - docs/evidence/gatebraid/P2-S6/
resource_locks: []
repair_limit: 2
consult_first: false
parallel_mode: safe-single-writer
```

