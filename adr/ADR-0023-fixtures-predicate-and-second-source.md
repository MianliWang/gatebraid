# ADR-0023 — Conformance fixtures: the correct predicate, and the second source

**Status:** Accepted · M2 (2026-08-01) · Product: Gatebraid (ADR-0010)
**Amends:** the fixtures clause of CONSULT-M2-01 Q5's adopted outcome. The
archived consult record (`consults/CONSULT-M2-01/`) is history and is not
edited; this ADR is the normative home that clause never had.
**Provenance:** friction #42, found by executing the rule; RB-M2-N §6–§7;
`_handoff/batch-n/fixtures.md` (24 pairs from 41 entries, every non-yield
named); the executor's H2 pre-landing review, which found §1's original
identity claim false against the log and is the reason §1 states containment.

## Context

The adopted rule said *"every resolved friction entry becomes a positive and a
negative conformance fixture."* Executing it over the whole log yields 24 pairs
from 41 entries — and the shortfall includes entries that are **resolved and
still un-fixturable** (environmental tool limits, an approved deviation, a
discharged deferral), which the rule's wording says cannot exist. Meanwhile
five of the strongest pairs derive from no friction entry at all: measured
platform behaviour and known-not-wrong state that no defect ever generated.

The rule over-promised in one direction and under-scoped in the other.

## Decision

**1. The predicate.** A friction entry yields a fixture pair **iff its
resolution changed a normative artefact** — `protocols/`, `schema/`,
`templates/`, or an ADR. This is the **second of convergence-metrics §3.1's
three conditions**, adopted by citation as the single source of its wording.
The other two conditions — first discovery, and found-by-executing — scope
§3.1's *defect count* and do not scope fixtures: **an entry may yield a
fixture pair without being a counted defect.** #19, #20, #26 and #34 are
exactly such entries — editorial or found by reading, uncounted under §3.1,
fixture-yielding here. Containment, not identity: every counted §3.1 defect
yields a pair; not every pair marks a counted defect.

**2. The second source.** Fixtures also derive from **measured platform
behaviour and known-not-wrong state** — the recorded-facts class: an edge
persisting after its blocker closes, `requires_gate` comparing ordered rather
than equal, a field that returns the same value in both states of the world.
Any measured fact a Gatebraid mechanism depends on carries a pair, defect or no
defect. A fixture set derived only from past failures tests only the past.

**3. Pairs cite their deciding clause.** Every fixture names the contract or
schema clause that decides it. When that clause is amended or removed, the pair
is re-derived or retired **in the same change** — ADR-0014 §2's discipline,
applied to fixtures.

## Consequences

- `_handoff/batch-n/fixtures.md`'s 24 pairs stand as drafted, and its 17
  non-yields are correct rather than a shortfall.
- The skills work consumes this rule: the evidence-render and
  unsupported-observation skills declare the fixture set they were verified
  against, alongside the contract and schema versions they support.
- Friction #42 is resolved by this ADR — under §3.1's own predicate, this
  entry itself yields a fixture pair.

## Reopening conditions

- A fixture class arises that neither source covers.
- The fixtures move from specification to an executable suite — the format
  decisions taken then may amend §3.
