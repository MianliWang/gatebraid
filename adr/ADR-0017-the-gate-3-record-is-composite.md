# ADR-0017 — The Gate 3 record is composite; the evidence file references rather than duplicates

**Status:** Accepted · M2 (2026-07-31) · Product: Gatebraid (ADR-0010)
**Amends:** `protocols/gate-3-contract.md`'s exit order and
`templates/gate3-evidence.md`. ADR-0012 stands unchanged.
**Provenance:** Slice A's Gate 3, the first real publication (2026-07-31),
friction #22; CONSULT-M2-01 Q4, which withdrew this ADR's first draft;
ADR-0001 (GitHub is the only durable authority), ADR-0016 (a gate's own evidence
is not the work).

**This ADR replaces an earlier draft** that had Gate 3 commit `gate3.md` directly
to the base branch under a standing approval term. That draft was withdrawn before
it was committed, for the reason in §1.

## Context

Slice A merged, closed correctly, and left the working repository's `main`
carrying `gate0.md`, `gate1.md` and `gate2.md` — but not `gate3.md`.

The cause is a genuine ordering constraint. `gate3.md`, as templated, records the
**merge SHA** and the **closure timestamp**, and neither exists until after the
pull request has merged — so the file could not travel inside the slice's own
pull request. The Release Approval authorised pushing exactly one branch, so
landing the file on `main` afterwards was outside the approved set. The executor
committed it on the retained branch and recorded the gap rather than improvising,
which is why this decision is being made deliberately instead of discovered later.

The first draft accepted the duplication and solved the placement problem by
authorising a direct commit to the base branch. **That was wrong, and the reason
is not aesthetic.** The identity work under consideration (CONSULT-M2-01 Q2) points
at a protection requiring every base-branch update to go through a pull request. A
contract that writes its own first exception into a control it intends to adopt has
chosen the exception over the control.

The deeper error was accepted without noticing: **`gate3.md` was being asked to
restate facts GitHub already holds natively.** The merge SHA, the merge actor and
time, the closure actor and time are all native objects with their own events. A
copy of a fact is a second source of truth that can disagree with the first — and
the two most expensive defects of this milestone, friction #16 and #22, are both
exactly that.

## Decision

**1. The authoritative Gate 3 record is composite.** It consists of:

- the **pull request's merge event** — merge SHA, actor, timestamp;
- the **Slice issue's native closed event** — actor, timestamp;
- the **Project `Workflow` field** — authoritative state (ADR-0008);
- the **Gate 3 handoff comment** — `gatebraid/handoff@1`;
- **`gate3.md`** — the gate's own checks, and nothing GitHub already holds.

**2. `gate3.md` never duplicates a natively held fact; it references it.** It
records what Gate 3 uniquely did and what no GitHub object states: the approval
verification, both closure preconditions (ADR-0012 §2), the drift check (ADR-0016
§1), the CI finding, and the declared intent to close at exit. Where it needs the
merge or the closure, it names the pull request and the issue.

**3. Consequently `gate3.md` carries no post-merge value, and reaches the base
branch through the pull request.** It is authored after the pull request is opened
— when the PR number exists — committed to the slice branch, pushed, and merged
with everything else. **No gate writes to a base branch outside a pull request.**

Revised Gate 3 order: entry checks → drift check → push branch → open PR
(`Refs #n`, no closing keyword) → author and commit `gate3.md` → push → merge →
`Gate = G3 passed` → `Workflow → Done` → **close the Slice issue explicitly** →
release lease → `Next Approval = —` → handoff comment → `Last Checkpoint`.

Committing `gate3.md` after the drift check does not weaken it: the check answers
*has the reviewed work changed since it was reviewed*, and ADR-0016 §1 already
excludes the slice's own evidence directory. This is that exclusion doing the job
it was written for.

**4. Consumers read the native event sequence, not the last state.** An issue can
be reopened; a comment can be edited in place, and nothing in any gate reads
`lastEditedAt`. Anything reconstructing a slice's history — an audit, a frontier
computation, M3's guard — reads the ordered timeline, not the current values. A
Slice that reads `closed` today is not evidence it was closed once, by Gate 3, at
its exit.

**5. Branch retention stays and is not load-bearing.** `deleteBranchOnMerge`
remains `false` and remains a Gate 3 precondition, because the branch is still the
only place a slice's intermediate commits are named. The *record* no longer depends
on it.

## Consequences

`protocols/gate-3-contract.md` and `templates/gate3-evidence.md` change. The
template loses `Merge: <merge SHA>` and the closure timestamp as recorded values
and gains references to the pull request and the issue. No schema change:
`gate-run@1` does not mandate either field.

**Slice A is not retro-fitted by a gate.** Its composite record is already
complete — PR #11's merge event, the issue's closed event and `Workflow = Done`
all exist natively. Only its `gate3.md` sits on the retained branch in the older,
duplicating form. Rewriting it to §2's shape and landing it on `main` through an
ordinary pull request is a records correction outside the gate system, needs its
own approval, and is not urgent.

The general shape, and it is the third time this milestone has produced it:
**one fact, one home.** ADR-0014 §2 said schema and template must not disagree
about a field; ADR-0018 says an approval must not restate the rule it cites; this
says an evidence file must not restate what the platform records. Every expensive
defect in M2 has been two copies of one thing, one of them stale.

## Reopening conditions

- If a consumer emerges that genuinely requires a single self-contained file — an
  external auditor, an offline archive — then decision 2 needs a *generated*
  projection with a named generator and a stated generation time, not a
  hand-maintained duplicate.
- If GitHub ever stops exposing merge or closure events with actor and timestamp
  through the API, decision 1's composite loses a member and the balance changes.
- If a future gate genuinely cannot know a value until after its own merge,
  decision 3's ordering fails for that gate and the case must be argued on its own
  facts rather than by analogy to this one.
