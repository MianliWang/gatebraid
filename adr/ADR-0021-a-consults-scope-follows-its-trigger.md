# ADR-0021 — A consult's scope follows its trigger

**Status:** Accepted · M2 (2026-07-31) · Product: Gatebraid (ADR-0010)
**Amends:** `gatebraid/consult@1` (schema change in the same commit, ADR-0014
§2); ADR-0004's linking rule, extended for non-slice consults. ADR-0004
otherwise stands.
**Provenance:** friction #25; CONSULT-M2-01, the first real consult and the
instance that does not validate; ADR-0019 §4.

## Context

`gatebraid/consult@1` requires `slice_id` (pattern `P<n>-S<n>`) and a consult id
of the form `CONSULT-<issue#>-<seq>`, both presupposing that every consult
belongs to one slice. Its own `trigger` enum admits `architecture-decision` and
`human-request`, which are not slice-scoped. The first real consult,
CONSULT-M2-01, is exactly that case — a milestone-level design review on human
request, belonging to no slice — and knowingly does not validate against the
schema it is nominally an instance of (friction #25).

This is ADR-0019's defect class: an outcome the system really produces has no
expressible form in the record. The schema admits a trigger it then makes
unrepresentable.

## Decision

**1. Triggers are partitioned by scope.** Slice-scoped: `repair-sequence`,
`consult_first`, `parser-type-system-semantic-design`,
`security-sensitive-diff`, `conflicting-evidence`, `low-confidence`,
`strict-gate-release-review`. Not slice-scoped: `architecture-decision`,
`human-request`.

**2. `slice_id` is required exactly when the trigger is slice-scoped, and
absent otherwise.** The schema encodes this conditionally, in the same commit
as this ADR.

**3. The consult id admits a milestone form.** `CONSULT-<issue#>-<seq>` for
slice-scoped consults; `CONSULT-M<n>-<seq>` for milestone-level ones.
CONSULT-M2-01 is retroactively well-formed.

**4. Linking follows scope.** A slice-scoped consult is linked from its Slice
issue (ADR-0004, unchanged). A non-slice consult is linked by citation from the
documents that adopted its outcome — for CONSULT-M2-01, the ADRs whose
provenance cites it and the Batch E record.

**5. CONSULT-M2-01 is archived as the prose pair it was** — the
request/response document and the decision record — each with one archival
header line noting it predates this ADR, content otherwise unchanged. The
structured metadata block binds consults from the next one onward. Retrofitting
a block onto a finished prose consult would create a second copy of its
content, which is the defect class ADR-0014 §2 and ADR-0017 exist to prevent.

## Consequences

- Milestone-level consults become first-class records instead of tolerated
  exceptions.
- The schema gains its first conditional requirement. Any hand-rolled validator
  must handle it; friction #8's lesson applies — test the conditional with both
  a scoped and an unscoped instance before trusting either result.
- `consults/` becomes a top-level home for archived consults
  (`consults/<consult_id>/`), starting with CONSULT-M2-01.

## Reopening conditions

- A consult arises that is neither slice- nor milestone-scoped — the id grammar
  extends again rather than the new case being shoehorned into an existing form.
