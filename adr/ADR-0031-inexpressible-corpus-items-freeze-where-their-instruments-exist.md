# ADR-0031 — §6 items whose assertions no committed instrument can evaluate freeze where their instruments exist

**Status:** Accepted · M3 Batch N1C (2026-08-12) · Product: Gatebraid (ADR-0010)
**Amends:** nothing retroactively. `M3-PLAN.md` §2 N1's Accept-when is read
through the route this ADR records; the clause itself is unedited, and
`M3-PLAN.md` §6's catalog of 21 items is unchanged.
**Provenance:** `fixtures/DETERMINACY-REPORT.md`, committed at
`350ededad59b2e3cef9b65154b6d51b35a43d3de`, 15,692 B, SHA-256
`716ec4d87746948181d7a8d5c33687d8bc77d5f2916f1152a614185fc3a39324` — its §2
item verdicts and §3 falsification case; ADR-0029 **Reopening conditions**,
first bullet — the operative authority; `M3-PLAN.md` §6's
versioned-approved-freeze clause, which supplies the required form and not the
authority (decision 1); the operator's
A4 ruling in the N1B/N1C advance-approval entries (2026-08-12), which this ADR
records durably because the approval surfaces live under ignored `_handoff/`
paths and are not committed record.

## Context

`M3-PLAN.md` §2 N1's Accept-when requires "every §6 item exists as a fixture
with an expected-failure assertion". Batch N1B measured that **16 of the 21
items cannot be expressed against any committed instrument**, and recorded the
falsification of that classification rather than merely asserting it.

The cause is not draftsmanship. The corpus runner asserts exactly one thing — a
document is valid or invalid against a JSON Schema. The §6 state-pipeline items
assert **tool outcomes** (`undecidable`, fail closed, a bounded-snapshot flag)
against a **snapshot-document schema that does not exist**; SP-10 tests for a
missing snapshot version that does not exist to be missing. The remaining
blocked items assert byte re-derivation, detector behaviour, or N3
coverage-report semantics — artifacts N1 is forbidden to implement, since
ADR-0029 decision 3 scopes N1 as "fixtures, `@2` admission and contract
reconciliation; **no tool implementation**".

Writing the 16 anyway would produce a corpus reporting `CORPUS CLEAN` while
asserting nothing, which is worse than an empty corpus because it looks like
coverage. Leaving them undecided would leave N1's Accept-when unsatisfiable with
no recorded reason.

## Decision

**1. The 16 inexpressible items — and the five HALF-BUILT remainders — are
corpus extensions, frozen where their assertion instruments exist.**

This is the route ADR-0029's first Reopening condition already names — *"Any
measured failure class the N1 corpus cannot express — **extend the corpus by
approved change before any tool relying on it advances**"* — and **that
condition, not `M3-PLAN.md` §6, is the authority for the two freeze points
below.**

`M3-PLAN.md` §6 is quoted here in full precisely because it does not authorize
them: *"Later phases extend it only by versioned, approved freezes **(corpus v2
at P's start, per §2)** — never by unfrozen additions."* §6 contemplates exactly
**one** later freeze, at P's start. This ADR adds two more. What §6 supplies is
the *form* every extension must take — versioned, approved, never an unfrozen
addition — and both freezes below take it. An earlier draft of this ADR elided
that parenthetical and leaned on the truncated clause as its authority; the
internal review caught the elision, and the citation is restored.

**2. The two freeze points.**

- **SP-01…SP-13 freeze at O0's start**, before O0's implementation, against the
  snapshot-document schema O0 defines as its own first deliverable.
- **IN-03, IN-04, IN-05 and the HALF-BUILT remainders freeze at N3's start**,
  before N3's implementation, against N3's coverage report and its
  re-derivation duties. The remainders are: BP-01's `sha256` re-derivation,
  BP-02's `byte_length` mismatch, BP-03's cross-document dual-platform claim,
  IN-01's interpretation of a pipeline exit code, and IN-02's *check that
  failed to notice*.

**`M3-PLAN.md` §2's dependency line is read the same way.** It states "O0
consumes N1's state-pipeline fixtures". After this decision those fixtures are
frozen at O0's start rather than authored inside N1, so O0 consumes a corpus it
freezes rather than one it inherits. The dependency is unchanged in force — O0
still may not proceed without them — and only their authoring point moves. This
is named rather than left to be discovered, because "Amends: nothing
retroactively" above is a claim about every clause, not only the Accept-when.

**Fixtures still precede the tools they test.** Each freeze lands before the
implementation that consumes it, which is the discipline `M3-PLAN.md` §2 already
requires of P's corpus-v2 and the reason N1 exists at all. What moves is *where*
a fixture is written, never *whether* it precedes its tool.

**3. `M3-PLAN.md` §2 N1's Accept-when is read through this route.** "Every §6
item exists as a fixture" is satisfied for N1 by the items expressible against
N1's own frozen interfaces, with the remainder carried as approved, scheduled
corpus extensions rather than as an unmet clause or a silently narrowed one.
**Stated without softening, in the provenance document's own words: batch N1B
"advances `M3-PLAN.md` §2 N1's Accept-when by zero items", and
`fixtures/evidence-capture-v1/` is not a §6 item.** The number of §6 items fully
satisfied at N1 is zero; five carry a schema-expressible half, and those halves
live in `fixtures/evidence-capture-v1/`, labelled by class. This decision
schedules the rest; it does not convert them into satisfaction.

**4. What this decision does not do.** It does not weaken any Accept-when
threshold, retire any §6 item, or authorize a tool. It does not touch ADR-0010's
naming rules, and the frozen `gate-run@1` and `gate-run@2` histories are
unaffected. It grants no schedule relief: an item not frozen at its named point
blocks the phase that names it, exactly as an unmet Accept-when would.

## Consequences

- **O0 gains a first deliverable and a precondition**: the snapshot-document
  schema, and the SP-01…SP-13 freeze against it before O0's implementation.
- **N3 gains the same shape**: its coverage report is specified, then the
  instrument items and remainders freeze, then N3 is written.
- **N1's v1 freeze covers what N1 could express** — `M3-PLAN.md` §6 calls it
  "N1's v1 freeze" and §2 N1's Accept-when ends "corpus is frozen by commit
  SHA", and both stand. The items deferred here are **outside** that v1 freeze
  rather than unfrozen additions to it, which is the distinction §6's last
  clause turns on; §6's catalog remains the authority for what is owed.
- The external read-only model review (`M3-PLAN.md` §2 N1) is **untouched by
  this ADR** and remains outstanding. Its negative cases must be externally
  contributed, and no internal review substitutes for it.
- A future item found inexpressible at its own freeze point returns here, not to
  an ad-hoc decision: the Reopening condition below is the route.
- Under `M3-PLAN.md` §5.1 this ADR is justified as a **milestone-authority**
  decision: it fixes how N1's Accept-when is read and adds two freeze points to
  the milestone's schedule. §5.1's default is zero new ADRs for an ordinary
  friction item, and this is not one — but the ground is named here rather than
  assumed, as ADR-0030 names its own.

## Reopening conditions

- An item still inexpressible at its named freeze point — the instrument was
  built and the assertion still cannot be written. That is a finding about the
  instrument's design and returns to an approved corpus change before the phase
  advances.
- A freeze point reached with its schema undefined — O0 starting without a
  snapshot-document schema, or N3 without a coverage-report format. The freeze
  cannot precede the artifact it validates against, and the phase stops rather
  than freezing an unassertable corpus.
- Measurement showing an item classified expressible-in-half is in fact fully
  expressible, as happened to IN-02 at N1B. The classification is a claim and
  carries its falsification case; a refuted one is corrected by recorded
  change, never by silent reclassification.
