# ADR-0015 — Approval authenticity rests on discipline, not access control

**Status:** Accepted · M2 (2026-07-31) · Product: Gatebraid (ADR-0010)
**Provenance:** M2 Batch C, Gate 2's entry check on Slice A (2026-07-31). ADR-0001
(GitHub is the only durable authority), ADR-0002 (exactly two human approval
doors), ADR-0003 (single writer), the M1 execution approval's no-credential rule,
`protocols/gatebraid-control-plane-spec-v1.md` §1.

## Context

The whole safety design of this system reduces to two human doors per slice:
Plan Approval at G1→G2 and Release Approval at G2→G3. Everything else — gates,
allowlists, hashes, repair budgets — controls *how* work proceeds. The doors
control *whether* it proceeds at all.

Gate 2's entry check ran for the first time and found no approval comment, which
was correct: the operator had given the approval in the coordinating session, in
full and with terms, but it had never been written to GitHub. ADR-0001 makes
GitHub the only durable authority, so an approval that exists only in a chat
transcript does not exist. A fresh session recovering from issue, fields,
evidence and git state alone would find Gate 2 unauthorised. That much is the
system working.

Two things surfaced underneath it that were not previously written down.

**The near-miss.** Gate 1's own handoff comment contains both hashes *and* the
string `Plan Approval`, because Gate 1's exit sets
`Next Approval = Plan Approval (G1→G2)`. Any check that looks for "a comment
mentioning Plan Approval and the hashes" finds the gate's own handoff and
concludes the door is open. The executor wrote that comment; its content is
"the door is shut". A naive entry check would have read it as consent.

**The structural fact.** The executor authenticates with the operator's own
credentials — that is a deliberate consequence of the no-API-keys rule, which
forbids issuing or handling a separate machine identity. So an approval comment
written by the executor and one written by the operator are **indistinguishable
in the record**: same author, same association, no API-versus-UI marker that
GitHub exposes.

Therefore the doors are not access-controlled. They are honoured. The executor
declined to write its own authorisation here, and was right to, but "the
executor chose not to" is not a control — it is the very thing the doors exist
so as not to depend on.

## Decision

**1. The property is stated, not assumed.** Gatebraid's two approval doors are
enforced by executor discipline, not by access control, for as long as the
executor authenticates as the operator. Any claim that the system "requires
human approval" means "no compliant executor proceeds without one". Nothing in
the record can distinguish a forged approval from a genuine one, so nothing
downstream — including M3's guard — may treat comment authorship as evidence of
human intent.

**2. Approvals are posted by the human, in a separate act.** The operator writes
the approval comment on the Slice issue themselves. This costs one action per
door, twice per slice. It is the only step in the workflow where the round trip
*is* the product rather than overhead, and it is not to be optimised away.

**3. An executor never writes its own authorisation.** Not as a transcription,
not with an attribution marker, not when explicitly invited to — because the
marker would be written by the same party whose authority is in question, which
is circular. If the operator insists in a specific instance, the executor
records the instruction verbatim, states in the evidence file that the approval
is executor-transcribed and therefore carries no independent authority, and
proceeds only on that basis. This is a degraded mode, and it is named as one.

**4. Gate 2 and Gate 3 entry checks must exclude the gates' own handoff
comments.** An approval comment is one that (a) is not a `gatebraid/handoff@1`
block, (b) names the artefact it approves — for Plan Approval, both `plan_hash`
and `allowlist_hash`; for Release Approval, the terms of publication — and (c)
was not authored by the executing session. Matching on the phrase
`Plan Approval` or on the presence of the hashes is insufficient and will
succeed against the gate's own exit comment.

## Consequences

`protocols/gate-2-contract.md` and `protocols/gate-3-contract.md` gain the
entry-check refinement. No field, view, option or schema changes.

The honest reading of this ADR is that a milestone's worth of gate machinery
rests on a property the machinery cannot check. That is acceptable while the
executor is a single cooperating agent under direct human supervision, and it is
recorded here precisely so that it is re-examined before it stops being true —
before an agent team runs slices unattended, and before anything schedules work
into hours when nobody is watching.

The real fix is a separate identity for the executor: a machine account or a
fine-grained token whose comments are attributably not the operator's. That is
currently forbidden by the no-API-keys, no-credential-handling rule, which was
adopted for its own good reasons. The tension is genuine and is left standing
rather than resolved by weakening either side.

## Reopening conditions

- **Before any unattended or scheduled execution.** Discipline is a sufficient
  control only while a human is watching the session that holds the credential.
  The operating-rhythm ADR must not authorise unattended gate execution without
  revisiting this one.
- **Before an agent team executes slices.** More executors sharing one identity
  multiplies the surface without adding any way to tell them apart.
- If GitHub exposes a durable, queryable marker distinguishing a comment made
  through the API from one made in the web UI, decision 4 can gain a mechanical
  check instead of a heuristic.
- If the no-credential rule is ever relaxed for a scoped, read-limited executor
  identity, decisions 2 and 3 can be reconsidered — but the burden is to show
  the new identity cannot post approvals, not merely that it is different.
