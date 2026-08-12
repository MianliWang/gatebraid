# ADR-0030 — Schema-id naming: the namespace binds; ADR-0010's enumeration is M1's inventory

**Status:** Accepted · M3 Batch N1 (2026-08-12) · Product: Gatebraid (ADR-0010)
**Amends:** nothing retroactively — ADR-0010 is frozen with the approved M1 set;
this ADR fixes its operative reading by reference, the method ADR-0028's header
applied to ADR-0004 (following ADR-0027 §4's treatment of ADR-0009).
**Provenance:** ADR-0010 Part II item 4 and its mapping-table row
"`classic/*@1` (schema-id namespace) → `gatebraid/*@1`"; `M3-PLAN.md` §2 N1
(ratified by ADR-0029, merged at `b342178a2b3f99459fcf1d83ee3d401c99a510f4`),
which names `gatebraid/gate-run@2`, `gatebraid/evidence-capture@1` and
`gatebraid/metrics@1` verbatim; the M3 Batch N1 internal review reaching the
same reading independently of the drafter (RB-M3-N1 §0.11.4); the operator's
A2 ruling in the N1 advance-approval entries (2026-08-12), which this ADR
records durably — the approval surfaces themselves live under ignored
`_handoff/` paths and are not committed record.

## Decision

ADR-0010 Part II item 4 ("Schema ids live under `gatebraid/*@1`", followed by
seven ids) binds the **namespace** — `gatebraid/<name>@<version>` — and its
list enumerates **M1's inventory as of that freeze, not a closed set**. A new
schema id under the namespace is admitted by the milestone authority that
introduces it plus the operator's batch approval — for N1:
`M3-PLAN.md` §2, ratified by ADR-0029 — and does not amend ADR-0010. The three
N1 interfaces `gatebraid/gate-run@2`, `gatebraid/evidence-capture@1` and
`gatebraid/metrics@1` are so admitted. A version increment under an existing
id never retro-breaks the frozen prior version: `@1` history still validates
as `@1` (ADR-0029 P1-1; fixture GR2-02 proves it).

## Consequences

- ADR-0010 Part II's naming rules (former names, the migration map, "no
  resource is ever created under a former name") continue to govern every new
  id unchanged.
- Under `M3-PLAN.md` §5.1 this ADR is justified as a public-interface
  decision. A future id introduced by a ratified milestone authority under
  this reading needs no further per-id ADR; a change to the *namespace itself*
  would.
