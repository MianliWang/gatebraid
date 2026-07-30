# ADR-0012 — Slice closure is explicit and exclusive

**Status:** Accepted · M2 (2026-07-30) · Product: Gatebraid (ADR-0010)
**Supersedes:** ADR-0011 §6 (the automation precondition), which defended the
wrong mechanism. ADR-0011 otherwise stands unchanged.
**Provenance:** M2 Batch A-2 measurement in `MianliWang/gatebraid-scratch`
(throwaway issue #7 and pull request #8, 2026-07-30, since cleaned up);
ADR-0007 (`requires_gate` encoding), ADR-0008 (Workflow as sole state
authority), `protocols/gatebraid-control-plane-spec-v1.md` §2.

## Context

The spec's closure invariant is that a Slice issue is closed **iff**
`Gate = G3 passed`, and closing a Slice is precisely what releases its native
`blocked-by` dependents. Gate 3's exit therefore states that closure "happens
exactly here and never earlier".

ADR-0011 §6 defended that invariant by requiring Gate 3 to verify, before
merging, that no enabled Project automation closes an issue. That was written
from a static audit of the Project's six built-in workflows, one of which
(`Auto-close issue`) closes an issue whenever its `Status` becomes `Done`.

**Execution proved the defence points at the wrong mechanism.** With
`Auto-close issue` verified disabled throughout, a throwaway pull request whose
body said `Closes #7` still closed issue #7 one second after the merge —
`state_reason: completed`, timeline `closed` event with `commit_id: null`. That
is GitHub's own closing-keyword behaviour, which fires on merge into the default
branch. It is not Project automation at all, so ADR-0011 §6's precondition
cannot see it, and a Slice pull request written the obvious way — "linked to the
Slice issue" — would have closed its Slice at merge time: before the Gate 3
evidence file exists, before `Gate = G3 passed`, and releasing every native
dependent early.

Two further facts were measured in the same probe and are recorded here because
later decisions rest on them:

1. **Project automation does write across the pull-request → issue link.** Rule
   `Pull request linked to issue` moved the *issue's* Project item from `Todo`
   to `In Progress` at the moment the pull request was opened — while the issue
   was still open, with no other rule able to fire. This is unambiguous, and it
   is the cleanly isolated half of the probe.
2. **What wrote `Status = Done` after the merge is not attributable from this
   experiment.** `Pull request merged` fired at 22:11:18Z and `Item closed`
   fired when the issue closed at 22:11:19Z; both were enabled, one second
   apart. Distinguishing them requires a pull request with no closing keyword —
   which, after this ADR, is exactly what every Slice pull request will be.

## Decision

**1. A Slice pull request must not use a closing keyword.** `close`, `closes`,
`closed`, `fix`, `fixes`, `fixed`, `resolve`, `resolves`, `resolved` — in any
case, in the body or in any commit message the pull request carries — are
forbidden when referencing the Slice issue or any other Gatebraid issue. Link by
plain reference instead: `Refs #n`, `Part of #n`, or a bare URL.

**2. Gate 3's precondition covers both closure mechanisms, not one.** Before
merging, Gate 3 verifies:

- **(a) platform automation** — no enabled Project workflow closes an issue as a
  consequence of a merge or a `Status` write; and
- **(b) the pull request itself** — its `closingIssuesReferences` is empty and
  its body contains no closing keyword.

Either check failing stops the gate. Recording `(a) pass` alone is not
compliance.

**3. Closure is a deliberate act at Gate 3's exit, performed once, explicitly.**
After the evidence file is written and `Gate = G3 passed` is set, Gate 3 closes
the Slice issue by an explicit command. Closure is never a side effect of
anything.

**4. The evidence file records the negative.** `gate3.md` carries
`closing_keywords: none`, `closing_issues_references: 0`, and the automation
check result. A gate that quietly did not check looks identical to one that
checked and passed; the record must distinguish them.

## Consequences

Gate 3's contract and the `gate3-evidence` template change. Nothing else does:
no Project field, view, option, label, or schema is affected, and no Project
automation is toggled by this ADR.

Some ergonomics are lost. A pull request that closes its issue on merge is the
familiar GitHub idiom, and giving it up means one extra explicit step at Gate 3.
That is the correct trade: the invariant that a Slice closes exactly when Gate 3
says so is what makes `requires_gate: 3` dependencies mean anything at all
(ADR-0007). An idiom is not worth a load-bearing invariant.

`Auto-close issue` stays disabled. It is no longer the *primary* defence, but it
remains a second path to the same failure, and there is no reason to re-enable
it.

The residual attribution question from the probe — what `Pull request merged`
writes to when no closing keyword is present — is now the exact configuration
Gate 3 will use on every slice, and is worth measuring before the first slice
runs rather than discovering during one.

## Reopening conditions

- If GitHub adds a repository or organisation setting that disables
  closing-keyword auto-closure outright, decision 1 can become a configuration
  rather than a discipline, and the keyword ban may be relaxed to a check.
- If a measured Slice run shows that `Pull request merged` writes
  `Status = Done` onto the Slice's item even without a closing keyword, then
  `Status` is tracking slice state in a way ADR-0008 does not govern, and the
  standing of the `Status` field must be decided rather than left as GitHub's
  own bookkeeping.
- If closure is ever observed happening outside Gate 3's exit despite both
  precondition checks passing, a third mechanism exists and this ADR is
  incomplete; find it before the next slice runs.
