# ADR-0014 — A slice's own evidence does not invalidate its own plan

**Status:** Accepted · M2 (2026-07-31) · Product: Gatebraid (ADR-0010)
**Amends:** ADR-0011 §9 (the Gate 2 baseline re-read). ADR-0011 otherwise stands.
**Provenance:** Coordinator pre-check of Gate 2's entry conditions against the
live state of Slice A after Gate 0 and Gate 1 (2026-07-31); host template-vs-schema
audit reported in RB-M2-B2 §7.

## Context

Two defects, both introduced by ADR-0011 itself, both found before they could
stall a gate.

**The first is a live deadlock.** ADR-0011 §9 has Gate 2 re-read the base branch
head at entry, compare it with the plan baseline recorded at Gate 0, and route to
`Scope / Allowlist Change` if the changed paths intersect the frozen
`write_domains`. Slice A's plan baseline is the scratch repository's `main` at
Gate 0. Since then Gate 0 and Gate 1 have each committed their evidence file to
that same branch, under `docs/evidence/gatebraid/P1-S1/` — **which is in the
frozen allowlist**, deliberately, because Gate 2's review item R1 checks the
whole `base..head` diff and an allowlist of `bin/` alone would fail the gate on
its own output.

So the literal rule says: the slice's own gate evidence invalidates the slice's
own plan. Every slice would route to `Scope / Allowlist Change` at Gate 2 entry,
forever. The rule was written to catch *other people's* changes landing under a
slice's feet; a slice's own earlier gates are not that.

**The second is a class of defect, not an instance.** ADR-0011 §2 and §3 added
`handoff_fingerprint` and `hash_commands` to the Gate 2 and Gate 1 evidence
templates, and ADR-0013 §3 added a stop-record shape to the Gate 0 template.
None of the three updated `schema/gate-run.schema.json`, which is
`additionalProperties: false`. Every one of those mandated fields was therefore
*forbidden* by the schema the same ADR left untouched. Gate 1 hit it and worked
around it; Gate 2 would have hit it identically; a stopped Gate 0 could not have
been written at all — which is precisely the hole ADR-0013 §3 was written to
close.

An ADR that mandates evidence it makes unwritable has not been implemented, only
declared.

## Decision

**1. The baseline re-read ignores the slice's own evidence directory.** In
ADR-0011 §9's intersection test, `docs/evidence/gatebraid/<slice_id>/` is
excluded from the changed-path set before the comparison. Changes there made by
this slice's own gates are expected, are not made by a third party, and cannot
invalidate a plan they are the product of.

Everything else about §9 stands: the re-read still happens at Gate 2 entry after
the lease is taken, the outcome is still recorded in `gate2.md` in every case
including no change, and a genuine intersection with the rest of the allowlist
still routes to `Scope / Allowlist Change`.

**2. Any ADR that mandates a new field in an evidence template must update
`schema/gate-run.schema.json` in the same change.** The schema is
`additionalProperties: false`; a template key the schema does not admit is not a
requirement but a contradiction. This is a standing rule, not a one-time
correction.

**3. The three outstanding instances are implemented now**, as part of this
decision rather than as separate decisions of their own:

- `hash_commands` — object of `allowlist` and `plan`, the exact commands that
  reproduce the two hashes (ADR-0011 §3).
- `handoff_fingerprint` — object of `active_branch_head`, `tree_sha` and
  `changed_paths`, which is what Gate 3's drift check compares against
  (ADR-0011 §2).
- `stop_record` — required whenever `result` is `stopped` or `blocked`, carrying
  `stopped_at`, `disposition`, `observed`, `expected`, and
  `remediation_attempted` (ADR-0013). `remediation_attempted` is
  `const: "none"`, so the schema itself enforces that a gate never remediates —
  the rule stops depending on the executor remembering it.

## Consequences

`protocols/gate-2-contract.md`, `schema/gate-run.schema.json` and
`templates/gate0-evidence.md` change. All four gate evidence templates now
validate against the schema with no keys outside it — verified, not assumed.

Decision 1 narrows a safety check, so it is worth being explicit about what it
gives up: if a *third party* were to write into a slice's evidence directory on
the base branch between Gate 0 and Gate 2, that change would no longer trip the
re-read. Under ADR-0003 a slice's evidence directory has exactly one legitimate
writer — the gate sequence executing that slice — so the excluded case is one
that should not occur, and if it does, the single-writer rule is already broken
and a staleness check is the wrong place to discover it.

Decision 2 is the more valuable half. Three ADRs in a row made the same mistake,
which means it was a property of how the ADRs were written, not of who wrote any
one of them.

## Reopening conditions

- If a slice ever legitimately shares its evidence directory with another writer,
  decision 1's exclusion is unsound and the comparison needs to be by commit
  author or by gate provenance rather than by path.
- If the schema ever stops being `additionalProperties: false`, decision 2 loses
  its force and template drift becomes silent again — which is a reason to keep
  the schema closed rather than to relax the rule.
