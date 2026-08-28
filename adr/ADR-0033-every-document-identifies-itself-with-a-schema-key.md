# ADR-0033 — Every Gatebraid document identifies itself with a top-level `schema` key

**Status:** Accepted · M3 Batch O1-B1 (2026-08-27) · Product: Gatebraid (ADR-0010)
**Amends:** nothing retroactively — retained `gatebraid/frontier-report@1`
documents remain historical record in their emitted form.
**Provenance:** the P2-S5 Gate 0 stop's finding 3, measured from the retained
runs (`docs/evidence/gatebraid/P2-S5/gate0.md`, sha256 `be7c3388…`, and its
captures): `g0-snapshot.json` identifies itself as
`"schema": "gatebraid/snapshot@1"` while `g0-frontier-report.json` carries
`"report": "gatebraid/frontier-report@1"` and no `schema` key at all — so the
validator, which routes on `schema`, can route neither O0 document kind
consistently and no frozen `frontier-report` schema file exists to route to.
The operator's D-3 ruling (2026-08-27, the a-revised option), recorded durably
by the Batch Approval for O1-B1 on `#17`: the rule is decided now; the
conforming frontier change is deferred to its own repair Slice — never P2-S6,
whose scope is `gatebraid-snapshot` alone (one Slice, one tool).

## Decision

1. **The rule.** Every committed Gatebraid document kind identifies itself
   with a top-level `schema` key carrying its `gatebraid/<name>@<version>` id
   (the ADR-0030 namespace). A document kind whose identity travels under any
   other key does not conform, whatever its other merits.
2. **The known violation.** `gatebraid/frontier-report@1` does not conform:
   its identity travels under `report`. The conforming revision —
   `gatebraid/frontier-report@2`, emitting `schema` and retiring `report`,
   landing together with a frozen `schema/frontier-report.schema.json` and its
   own fixture set, fixtures-first — is **deferred to a dedicated
   `gatebraid-frontier` repair Slice**, scheduled by the operator. Until that
   Slice lands, the validator's inability to route frontier reports is a
   registered known limitation, and `@1` reports remain valid historical
   record identified by their `report` key.
3. **Version discipline.** The identity-key change is a format change and
   takes a version increment; the increment never retro-breaks the frozen
   prior form (ADR-0030's rule; the retained P2-S5 evidence stays exactly as
   captured).

## Consequences

- O1's `gatebraid-ready` consumes whichever frontier-report version is landed
  when its Gate 1 freezes its plan; whether the frontier repair Slice runs
  before or after O1's re-entry is the operator's scheduling decision, made
  there and not here.
- New document kinds introduced by future milestones carry `schema` from
  birth; a kind proposed without it is returned at review, not patched after.
- Under `M3-PLAN.md` §5.1 this ADR is justified as a public-interface
  decision (a document self-identity contract shared by producer, validator
  and consumers).
