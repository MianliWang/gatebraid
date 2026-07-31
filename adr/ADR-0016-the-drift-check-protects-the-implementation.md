# ADR-0016 — The drift check protects the implementation, not the evidence

**Status:** Accepted · M2 (2026-07-31) · Product: Gatebraid (ADR-0010)
**Amends:** ADR-0011 §2 (the handoff fingerprint) and ADR-0015's third reopening
condition. Both otherwise stand.
**Provenance:** M2 Batch C-2, Slice A's Gate 2 exit (2026-07-31), friction #16;
ADR-0014 §1, which established the same principle one gate earlier.

## Context

ADR-0011 §2 has Gate 2 record `active_branch_head` and `tree_sha` in `gate2.md`,
and Gate 3 verify that the current head and tree still equal those values.

**The specification is circular.** `gate2.md` is evidence, so ADR-0001 requires it
to be committed; committing it moves the head past the value the file records.
The file must contain a value that only exists after the file exists. Slice A's
run produced exactly that: recorded head `6f73af2`, actual head `69fc64e`. The
executor recorded the only value knowable at write time and declined to invent a
reconciliation rule, which is the correct response to a contradictory spec.

The mistake underneath it is a category error about what the check is for. Gate
3's drift check exists to answer one question: **has the reviewed work changed
since it was reviewed?** The reviewed work is the implementation. A gate's own
evidence file is not the implementation — it is the record of having reviewed it,
and it is written *by* the gate whose output is being protected.

This is the same distinction ADR-0014 §1 drew one gate earlier, where a slice's
own evidence commits were invalidating the slice's own plan at Gate 2's baseline
re-read. The correct fix there was to exclude the slice's evidence directory from
the comparison. It is the correct fix here too, and reusing it is better than
introducing a second mechanism for the same idea.

## Decision

**1. Gate 3's drift check verifies that nothing but this slice's own evidence has
changed.** Concretely, against the values Gate 2 recorded:

- `git diff --name-only <tree_sha> HEAD` yields only paths inside
  `docs/evidence/gatebraid/<slice_id>/`; and
- `git status --porcelain` is empty; and
- every commit between `active_branch_head` and `HEAD` touches only that
  directory.

Any path outside it — any change to `bin/`, to anything in the allowlist other
than the evidence directory, to anything at all — is drift, and sends the slice
back to `Needs Review` exactly as before.

This is not a weakening of an exact check into an approximate one. It is an exact
check of the right thing. The previous formulation was not strict; it was
unsatisfiable.

**2. The fingerprint stays in `gate2.md`.** The alternative considered was moving
it to the handoff comment posted after the commit, where the true final head can
be written. That works, and it was the executor's recommendation. It is not
taken, for two reasons: it splits one gate's record across two artefacts, so a
reader reconstructing state must consult both; and it buys an exact head value
that decision 1 shows is not the quantity of interest. The comment is no more
tamper-resistant than the file — both are written by the same executor — so the
move purchases tidiness in one place at the cost of coherence in another.

**3. Gate 2 records what it can honestly record.** `active_branch_head` and
`tree_sha` are the values at the moment the implementation is complete and
reviewed — that is, before `gate2.md`'s own commit. The evidence file states this
explicitly rather than appearing to record a final state it cannot know.

**4. ADR-0015's third reopening condition is corrected.** It said that if GitHub
ever exposed a durable marker distinguishing an API comment from a web-UI
comment, the approval check could become mechanical. GitHub already exposes one —
`performed_via_github_app` — and it is `null` on every comment here, including
the executor's own, because the executor authenticates with an **OAuth user
token** rather than as a GitHub App. The mechanism exists; it fails to
discriminate because of how the executor is credentialed.

So the condition is not waiting on GitHub. It is waiting on the no-API-keys,
no-credential-handling rule named in ADR-0015's own Consequences. Corrected
wording: *if the executor is ever credentialed as a GitHub App or any identity
whose comments carry an attributable marker, decision 4 gains a mechanical check.*

## Consequences

`protocols/gate-3-contract.md` and `templates/gate2-evidence.md` change. No
schema change: `handoff_fingerprint` already exists in `gate-run@1` and its
fields keep their meanings.

The general lesson is worth stating because it has now cost two ADRs: **a rule
that compares "before" against "after" must say which artefacts are part of the
thing being compared and which are part of the comparing.** ADR-0014 §1 and this
decision are the same correction applied at two gates, and both were written into
the contracts by ADR-0011 without that distinction being drawn.

## Reopening conditions

- If a gate ever needs to write outside its own evidence directory as part of
  recording evidence, decision 1's path test is too narrow and the exclusion must
  be defined by commit provenance rather than by path.
- If the evidence file and the handoff comment ever disagree about the
  fingerprint, decision 2 is wrong and the single-artefact argument fails on
  contact with practice.
