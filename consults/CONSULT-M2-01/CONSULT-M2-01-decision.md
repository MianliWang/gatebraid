<!-- Archived under ADR-0021 §5 — predates the structured gatebraid-metadata block; content below unchanged. -->

# CONSULT-M2-01 — coordinator decision record

**Verdict: PARTIAL.** · `independently_verified: yes` · `rebuttal_rounds: 0`
Consultant: Codex (read-only, ADR-0004). Response saved verbatim alongside this
file. Nothing was blind-applied.

---

## 0. Independent verification performed

Three claims were load-bearing enough to check rather than accept.

**V1 — GitHub ToS permits a machine account. CONFIRMED, and the primary source is
stronger than the consultant's paraphrase.** GitHub Terms of Service §B.3:

> "One person or legal entity may maintain no more than one free Account (if you
> choose to control a machine account as well, that's fine, but it can only be
> used for running a machine)." … "We do permit machine accounts: A machine
> account is an Account set up by an individual human who accepts the Terms on
> behalf of the Account, provides a valid email address, and is responsible for
> its actions."

**V2 — Rulesets and branch protection on *private* repositories require a paid
plan. The consultant did not state this, and it is decisive for Q2's enforcement
half.** GitHub docs, *About rulesets*:

> "Rulesets are available in public repositories with GitHub Free and GitHub Free
> for organizations, and in public and private repositories with GitHub Pro,
> GitHub Team, and GitHub Enterprise Cloud."

If both Gatebraid repositories are private on a Free plan, then *every*
enforcement mechanism the consultant recommends for Release Approval — required
PR, required review, dismiss-stale-approvals, non-last-pusher approval, no
machine-account bypass — is unavailable. **This must be observed before the Q2
recommendation is planned, not assumed.** It is written into Batch E as a read.

**V3 — the batch-count inconsistency the consultant flagged is real, and it is
the coordinator's error.** `CONSULT-M2-01` §3.2 wrote "~6" while listing nine
names, and Q6 wrote "two of the six batches". The true M2 batch count is **9**
(Batch 0, A, A-2, A-3, B, B-2, C, C-2, D). Further, the two briefing errors did
not both occur in M2 — one was in M1 Batch 2, one in M2 Batch D — so the ratio was
malformed in numerator and denominator alike. **This is the same defect class as
the two briefing errors themselves: a number asserted rather than counted.**
Corrected here; no metric may cite it until Q1's definitions are frozen.

---

## 1. Per-question decisions

### Q1 — Convergence · **ACCEPT**

The consultant's position — *"not yet proven to converge; not proven to be
diverging"* — is better calibrated than the coordinator's stated leaning toward
convergence, and its reason is one the coordinator did not supply: a clean Slice B
is only **weak** evidence, because B may simply not traverse new contract paths,
whereas recurrence of an already-fixed defect is **strong** evidence of divergence.
Asymmetric evidence weight is the right frame.

The four metrics are adopted as proposed. Adopted with one addition of the
consultant's own making: **the classification rules and the batch definition must
be frozen before Slice B starts**, because V3 shows the denominator is not
currently defined, and a metric whose classification is adjusted after observation
is worthless.

### Q2 — Identity · **ACCEPT the direction, PARTIAL on the mechanism**

The forgery story is correct and is the sharpest statement of the risk anyone has
produced: a mistaken or prompt-injected agent writes "APPROVED" under the
operator's OAuth identity, reads its own comment back as authorisation, then
pushes, merges and closes — and a second agent sees a perfectly ordinary,
perfectly durable GitHub record. Nothing afterwards can distinguish it from a real
approval. That is a single point of failure in the safety model, not process
friction, and the coordinator accepts it as stated.

**The correction the consultant missed, and it changes the plan's shape:**
*attribution* and *enforcement* are separable, and only enforcement is
plan-gated.

- **Attribution — free, available today.** The moment the executor authenticates
  as a distinct machine account, an approval comment authored by the operator's
  personal account *is* evidence that the executor did not write it. This is
  detection, not prevention, and it removes the entire indistinguishability
  problem. Nothing in V2 restricts it.
- **Enforcement — needs V2's answer.** Rulesets, required reviews, stale-approval
  dismissal and bypass restrictions prevent rather than detect, and on private
  repositories they require a paid plan.

The consultant bundled these and therefore made the whole recommendation look
plan-contingent. It is not. **The load-bearing half is free.** Sequencing
follows: take attribution first, decide on enforcement after V2 is observed.

**Open for the operator, not for either agent:** does the standing "no API keys,
no credential handling" rule forbid authenticating a *second* account through the
same already-sanctioned browser flow? The coordinator's reading is that it does
not — the rule's purpose is that no secret is ever created, copied, stored in a
file, or exposed to an agent, and a browser OAuth login satisfies that exactly as
the current login does. But it is the operator's rule and the ruling is theirs.

> **OPERATOR RULING, 2026-07-31: it does not violate the rule.** A separate
> machine account authenticated through the browser is permitted. The
> no-credential rule continues to forbid creating, copying, storing or exposing
> any secret, and forbids an agent handling a token; it does not forbid the
> operator logging a second account in themselves.
>
> This ruling is an interpretation of a standing rule and therefore belongs in the
> committed tree, not in a chat transcript (ADR-0001). It is queued for **Batch F**
> as the identity-split ADR, which cannot be drafted until E0 reports repository
> visibility and plan — those determine whether the enforcement half exists at all.
> Until that ADR is committed, this ruling has been given but not recorded, and no
> identity change may be executed on the strength of it.
The consultant's fallback — *if it is forbidden, record plainly that there is no
solution* — is accepted as the correct alternative, including its corollary that
**signed commits do not fix this**, because a signature proves key control, not
human intent at that moment.

### Q3 — Term/rule conflict · **ACCEPT, and the addition is better than the ADR**

`(a) Stop` is confirmed, on the consultant's reasoning rather than merely in
agreement with it: allowing the executor to pick *either* the more reasonable *or*
the stricter reading delegates approval authority in both cases. The coordinator's
draft made this argument only for the first.

**The addition is adopted and improves ADR-0018 §3.** The coordinator's rule was
"terms cite, they do not restate", which is necessary but leaves an ambiguous
approval merely ambiguous. The consultant's structure closes it:

- an approval cites a precise rule **version or hash**;
- it fills only the objects of *this* authorisation — SHAs, `plan_hash`,
  `allowlist_hash`, explicit exceptions;
- overriding a rule requires a structured `override` naming the clause, the scope
  and the reason;
- **a missing field, an ambiguity or a conflict makes the approval invalid**,
  rather than something to interpret selectively.

That answers the coordinator's own worry — that "stop" trains the operator toward
vaguer terms — with a mechanism instead of a hope: a vague approval fails
validation and buys nothing.

Conflicting approvals are superseded by a new corrected approval object, never
resolved by the executor choosing which text is in force.

### Q4 — Post-merge evidence · **PARTIAL — the critique is accepted, both endpoints are rejected**

The consultant's critique of draft ADR-0017 lands, on a ground the coordinator did
not consider: a direct write to the base branch is **not merely a formal
exception** — it collides head-on with the "all base updates go through a PR"
protection that Q2 wants. Designing toward a control and simultaneously building
its first exception into the contract is wrong, and that is enough to withdraw the
draft.

Option `(e)` — the authoritative record is the composite of native GitHub objects
(PR merge event, structured Gate 3 comment, native closure event, Project
`Workflow`) — is accepted **as the principle**: `gate3.md` must not be a second
source of truth for facts GitHub already holds natively. Duplication is precisely
what produced friction #16 and #22.

**But `(e)` as stated leaves `gate3.md` a "read-only projection generated later",
which is rejected.** `gatebraid/gate-run@1` requires a per-gate evidence file, the
whole review and audit surface reads those files, and "generated later" names no
generator. There is a synthesis neither party proposed:

> **(f)** `gate3.md` records only what Gate 3 uniquely did — its entry checks, the
> drift check, both closure preconditions, and the CI finding — and **references**
> the PR and the issue for everything GitHub holds natively. Having no post-merge
> value in it, it can be written *after the PR is opened and before the merge*,
> committed to the slice branch, and reach the base branch **through the pull
> request**.

`(f)` keeps the per-slice file, removes the duplication `(e)` correctly objects
to, and removes the non-PR write `(a)` would have introduced. Draft ADR-0017 is
rewritten to it.

The consultant's risk note is adopted verbatim into the rewrite: **consumers must
read the native event *sequence*, not the last state** — issues can be reopened
and comments can be edited.

### Q5 — Skills · **ACCEPT in full**

The line drawn — mechanism in the skill, policy in the contract — is the right
one, and the fail-closed version rule (*a skill declares the contract and schema
versions it supports and stops on mismatch rather than adapting*) is the part the
coordinator would not have specified. The "second invisible contract" risk is
already evidenced in this project: the Release Approval's term 4 *was* a shadow
copy of ADR-0012 §1, and it drifted in the one clause that mattered. A skill is
that failure at scale.

Adopted: every resolved friction entry becomes a positive **and** negative
conformance fixture, and a contract version change must produce an explicit skill
compatibility verdict.

### Q6 — Topology · **ACCEPT the diagnosis; PARTIAL on the remedy, on grounds of what the tools can currently do**

The diagnosis is accepted without qualification: an offline coordinator with no
repository access has twice written unobserved state as established fact, and V3 is
a third instance in the consult document itself. **Three instances of one defect
is a property of the role, not of any one message.**

**Adopted immediately, at zero cost, effective now:** a coordinator brief states
preconditions as *conditions the executor must re-observe*, never as facts already
established. Everything the coordinator believes about repository state is a
hypothesis until the writer observes it.

**Also adopted immediately, and it removes half the relay:** the coordinator can
already read `_handoff/reports/` and `_handoff/friction-log.md` directly from the
operator's disk, and already writes `_handoff/prompts/NEXT.md` there directly. The
operator has been pasting reports by hand that the coordinator could have read
itself. That stops now. What remains of the human's transport role is starting the
executor session — which is a control action, not transport.

**Not adopted, because the mechanism does not exist:** a single orchestrator with
read-only planning sub-agents receiving writer-produced snapshots. There is no
session-to-session channel between the coordinator and the executor; the only
shared medium is the operator's filesystem. The consultant's fallback — collapse
the coordinator into a read-only planning role inside the executor's own session —
is a real option and is recorded as an M3 design candidate, but adopting it now
would discard the coordinator/executor separation mid-milestone. Deferred with the
reason stated, not rejected.

---

## 2. What changes as a result

| # | Change | Where |
|---|---|---|
| 1 | Draft ADR-0017 withdrawn and rewritten to synthesis `(f)` | Batch E |
| 2 | ADR-0018 §3 gains the structured-approval requirement and the invalid-on-ambiguity rule | Batch E |
| 3 | Q1's four metrics frozen, with batch and classification definitions, **before** Slice B | Batch E |
| 4 | Repository visibility and plan observed before any Q2 planning | Batch E, a read |
| 5 | Coordinator briefs state preconditions as re-observation conditions | **effective now** |
| 6 | Coordinator reads reports and logs from disk; operator stops pasting them | **effective now** |
| 7 | Identity split proposed, pending the operator's ruling on the credential rule | proposal, not yet an ADR |
| 8 | Skill boundary and fail-closed version rule recorded for M2's skills work | Batch F |
| 9 | Single-session topology recorded as an M3 design candidate | M3 backlog |

## 3. Where the consultant was wrong or incomplete

Recorded because a consult whose every point is accepted has not been reviewed.

- **Omitted V2**, the plan gate on private-repository rulesets, which is the single
  fact that determines whether Q2's enforcement half is executable at all.
- **Bundled attribution with enforcement**, making a recommendation whose valuable
  half is free look entirely plan-contingent.
- **Option `(e)`'s "read-only projection generated later"** names no generator and
  conflicts with `gatebraid/gate-run@1`'s per-gate file requirement.
- Q6's remedy assumes an inter-session channel that does not exist in this
  environment.

None of these changes the direction of any answer. All four are the consultant
reasoning correctly from a context it was given incompletely — three of the four
gaps are in the consult document the coordinator wrote.
