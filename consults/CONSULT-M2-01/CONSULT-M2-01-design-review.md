<!-- Archived under ADR-0021 §5 — predates the structured gatebraid-metadata block; content below unchanged. -->

# CONSULT-M2-01 — Is the Gatebraid gate system converging, and is it the right base for an agent team?

**Consultant: read-only.** You cannot execute anything, and nothing you write will
be applied automatically. All ground truth you need is embedded below. Do not ask
for repository access; do not propose commands to run. Recommendations are
suggestion text only, per ADR-0004.

**Schema deviation, disclosed:** `gatebraid/consult@1` requires `slice_id`
(`^P[0-9]+-S[0-9]+$`) and `consult_id` (`CONSULT-<issue#>-<seq>`), both of which
assume a slice-scoped repair. This consult is milestone-level. The schema's own
`trigger` enum already admits `architecture-decision` and `human-request`, which
are not slice-scoped — so the schema contradicts itself, and this document
knowingly does not validate. Logged as friction #25.

---

## 1. What this system is, in ten lines

Gatebraid is a solo-operator delivery system built entirely on GitHub. Work
decomposes Stage → Phase → **Slice**; a Slice is the unit of execution. Every
Slice passes four gates:

| Gate | What it does | Human door |
|---|---|---|
| **0** Baseline | read-only verification that the recorded baseline matches reality | — |
| **1** Plan | writes the plan, freezes it as `plan_hash` + `allowlist_hash` | **exit → Plan Approval (G1→G2)** |
| **2** Implement + review | implements inside the frozen allowlist, then five independent review items | **exit → Release Approval (G2→G3)** |
| **3** Publish | drift check, push, PR, merge, then closes the Slice issue explicitly | — |

Two human approval doors per Slice, and no others. `Workflow` (a GitHub Projects
field) is the sole state authority. **GitHub is the only durable authority** —
anything not on GitHub does not exist (ADR-0001). Closing a Slice issue is
precisely what releases its native `blocked-by` dependents, so closure is
deliberate, explicit, and happens only at Gate 3's exit.

Two repositories are in scope and no others: `MianliWang/gatebraid` (control:
ADRs, protocols, schemas, templates) and `MianliWang/gatebraid-scratch` (working
repo where slices execute).

**The stated long-term goal is an agent team MVP** — multiple agents executing
slices, eventually with less human presence per slice than today.

---

## 2. Who is executing, and how

Three parties:

- **Coordinator** (a Claude session): designs, writes ADRs and batch briefs. Has
  no repository access and cannot run `gh` or `git`. Writes files to the
  operator's disk through a desktop bridge.
- **Executor** (a separate Claude Code session on the operator's Windows
  machine): runs every `git` and `gh` command. Authenticates with the operator's
  own credentials.
- **Operator** (the human): the sole approval authority, and the relay between
  coordinator and executor.

Communication is a file mailbox on the operator's disk: coordinator writes
`_handoff/prompts/NEXT.md`, executor writes `_handoff/reports/RB-*.md`, the
operator carries each across.

---

## 3. Where we actually are

Milestone M1 (control plane + specification) is merged. Milestone M2 is in
progress. **Slice A (`P1-S1`) is the first slice ever to pass all four gates**;
it completed and closed on 2026-07-31.

### 3.1 What Slice A measured

These are observations, not inferences.

- Both closure mechanisms were checked against a real merge and **neither
  fired**. The issue stayed `open` through the merge, through `Gate = G3 passed`,
  and through `Workflow = Done`; it closed only on the explicit command. One
  `closed` event in the timeline, `commit_id: null`.
- **A native `blocked-by` edge does not disappear when the blocker closes.** The
  edge persists; the blocker's `state` flips `open` → `closed`. The correct
  frontier predicate is therefore *"blocked iff any `blocked_by` entry is open"*,
  not *"blocked iff an edge exists"*. An implementation that counts edges would
  consider the dependent slice blocked forever.
- Earlier measurement (a throwaway probe): a merged PR whose body says
  `Closes #n` **closes the issue even with the Project's `Auto-close issue`
  workflow disabled** — that is GitHub's own keyword behaviour, invisible to any
  Project-automation check. This is why slice PRs use `Refs #n` only.
- `deleteBranchOnMerge` was `false` — checked before it could have consequences.
- CI is `none-configured` in both repositories (no workflows at all).

### 3.2 Cost of getting there

| | count |
|---|---|
| Slices completed end-to-end | **1** |
| Execution batches to do it | ~6 (Batch 0, A, A-2, A-3, B, B-2, C, C-2, D) |
| Friction entries logged | **24** |
| ADRs written during M2 | **9** (ADR-0011 … ADR-0019; 0017–0019 drafted, not yet committed) |
| ADRs frozen from M1 | 10 (ADR-0001 … ADR-0010) |

### 3.3 What the 24 friction entries were caused by

Classified by the coordinator; the classification is itself open to challenge.

| cause | count | examples |
|---|---|---|
| **Contract specified something unsatisfiable or self-contradictory** | 8 | Gate 2's baseline re-read invalidated a slice's plan using the slice's own evidence commits; Gate 3's drift check required a file to record a head that only exists after the file is committed; Gate 0 prohibits state-changing git but its exit commits evidence |
| **Schema/template could not express a true observation** | 4 | a stopped Gate 0 was unwritable; `ci-status` had no value for "no CI has ever existed"; baseline re-read had no value for its own commonest outcome |
| **A rule was written as a token list rather than as a pattern** | 2 | the closing-keyword ban caught conventional-commit `fix(` prefixes; a review item scoped to GraphQL caught the word `mutation` in a docstring saying the code performs no mutation |
| **Process defect** | 3 | the Gate 2 evidence file recorded `review-five-items: pass` **before the review ran** (the reviewer caught it; the answer happened to be correct) |
| **Coordinator briefing error** | 2 | told the executor a zip was unpacked when it was not; told the executor two friction entries were logged when they had not been written |
| **Tooling / environment** | 5 | `gh` cannot pass a list-typed GraphQL variable; a stale `index.lock` left by the desktop bridge; `core.autocrlf` set at system level with no `.gitattributes` |

**Notably: zero entries were caused by the implementation work itself.** Every
one was a defect in the machinery around the work. Every one was found by a gate
or a reviewer, and **none was resolved by improvising inside a gate.**

### 3.4 The M2 ADRs, one line each

| ADR | Decision |
|---|---|
| 0011 | nine gate-contract corrections found by audit before any slice ran |
| 0012 | slice closure is explicit and exclusive; slice PRs carry no closing keyword; Gate 3 checks both closure mechanisms |
| 0013 | every Gate 0 verification has a defined failure disposition — *decidable* (stop, set `Next Approval`, never remediate) or *error* (`Blocked` + typed reason) |
| 0014 | a slice's own evidence does not invalidate its own plan; **and** any ADR mandating a template field must update the schema in the same change |
| 0015 | the two approval doors rest on **executor discipline, not access control** (see Q2) |
| 0016 | the drift check protects the implementation, not the evidence |
| **0017** *(drafted)* | the default branch carries the complete gate record; `gate3.md` lands by a direct base-branch commit at Gate 3's exit |
| **0018** *(drafted)* | a prohibition names the pattern it forbids, not the tokens it contains; an approval term cites the rule it enforces rather than restating it; where a term and its cited rule disagree, the executor **stops** |
| **0019** *(drafted)* | every outcome a gate can observe must be expressible in the record |

---

## 4. Constraints your recommendation must respect

These are standing rules, not preferences. A recommendation that violates one is
not usable.

- **Manual approval mode.** Every GitHub mutation batch is announced and waits for
  the operator's explicit approval. Never propose "auto" or "skip".
- **No API keys, no credential handling.** The executor uses already-authenticated
  `gh`/`git` only. This is why the executor authenticates *as the operator*.
- **No worktrees. Single writer per repository. No force-push, ever.**
- **GitHub is the only durable authority.** A decision that lives only in a chat
  transcript does not exist.
- **You (the consultant) are read-only** and your output is suggestion text. The
  coordinator independently verifies before anything is adopted; nothing is
  blind-applied.
- Only the two repositories named in §1 are in scope. Do not ask about others.

---

## 5. Questions

Answer in the order given. **Where you disagree with the coordinator's stated
leaning, say so plainly — a confirming answer is the least useful outcome of this
consult.**

### Q1 — Is the contract-first approach converging, or diverging?

Nine ADRs were written while running a single slice, and **every one of them
corrected a contract written before anything executed**. Two readings:

- **(a) Converging.** This is the normal, one-time cost of discovering that a
  specification written from a static audit does not survive contact with
  execution. Slice B will produce far fewer entries, and the curve is the point.
- **(b) Diverging.** The contracts are over-specified relative to what a
  single-operator system needs. Each ADR adds surface that the next slice can
  contradict, and 24 entries per slice is not a burn-down — it is a rate.

**What observable in Slice B would discriminate between (a) and (b)?** Name the
measurement, not the intuition. If you think the honest answer is "one more slice
will not settle it", say what would.

### Q2 — The approval doors rest on discipline, not access control

ADR-0015 records this and does not resolve it. The executor authenticates with
the operator's own credentials because a no-credential rule forbids issuing a
separate machine identity. Consequence: **an approval comment written by the
executor and one written by the operator are indistinguishable in the record** —
same author, same association, and `performed_via_github_app` is `null` on every
comment because the token is an OAuth user token rather than a GitHub App.

So "this system requires human approval" currently means "no compliant executor
proceeds without one".

The stated goal is an agent team, eventually with less human presence per slice.

1. Is there a design that yields **attributable** approvals without the operator
   handling API keys or secrets? Consider mechanisms we may not have thought of —
   signed commits, a separate GitHub account the operator logs into by hand, a
   branch-protection ruleset, CODEOWNERS, environments with required reviewers,
   anything else GitHub offers natively.
2. Is the current state safe to build M3 on, or is it load-bearing debt that must
   be resolved **before** more agents exist? Give the failure story concretely if
   you think it is the latter.

### Q3 — When an approval term and the rule it cites disagree, what should the executor do?

**The concrete case.** ADR-0012 §1 forbids `close`/`fix`/`resolve` and their
variants *"when referencing the Slice issue or any other Gatebraid issue"*. The
operator's Release Approval restated the list and **dropped the qualifier** — its
term 4 read "no closing keyword … in any commit message the branch carries". The
branch carried two conventional-commit prefixes, `fix(P1-S1): …`, written and
reviewed one gate earlier.

Read literally, the branch violated the approval. Read against the cited ADR, it
did not. The term's own mechanical test — `closingIssuesReferences` read back
after opening the PR — returned **0**.

**The executor did not stop.** It stated its reasoning on the record *before*
opening the PR: the cited authority scopes the ban, no `keyword + #number` pattern
exists on the branch, and the term's own test agrees.

The coordinator's ruling (drafted as ADR-0018 §4) is that **the conclusion was
right and the action was wrong**: an approval outranks the committed tree on
precedence, the ADR outranks the term on merit, and adjudicating between two
authorities is exactly what the doors exist to keep out of the executor's hands.
So: stop and ask.

Candidate rules:

- **(a) Stop.** Any term/rule conflict halts the gate. *Cost:* a round trip in
  every case, including the ones where the executor is right — as here.
- **(b) Narrower governs.** The more restrictive reading wins automatically.
  *Cost:* the executor still adjudicates, just by a fixed rule.
- **(c) Proceed and record a typed deviation**, notifying the human, gate
  continues. *Cost:* the executor has overridden a literal instruction.

Which is right for a system whose entire safety story is two human doors? And a
specific worry: **does (a) train the operator to write vaguer terms so conflicts
never arise** — trading a visible cost for an invisible one?

### Q4 — Where does a post-merge evidence file live?

`gate3.md` must record the merge SHA and the closure timestamp. Neither exists
until after the merge, so the file **cannot** travel in the slice's own pull
request. Today it is committed on the retained slice branch, and the working
repo's `main` carries `gate0.md`, `gate1.md`, `gate2.md` but **not** `gate3.md`.

Options considered:

- **(a) Direct commit to the base branch at Gate 3's exit** — one path only,
  authorised by a standing term in every Release Approval. *This is the
  coordinator's draft decision (ADR-0017).* Cost: one commit per slice on the
  base branch that did not come from a PR.
- **(b) Write `gate3.md` before the merge** so it rides in the PR. Cleaner in
  form; the file then cannot state what it published or when it closed.
- **(c) A per-slice evidence PR after the merge.** Consistent in form; adds a PR
  and an approval per slice, and that PR sits outside the gate system entirely —
  no gate governs it.
- **(d) Branch retention is the record** — never delete slice branches, treat
  `Active Branch` as the index. Zero mechanism; the record's completeness then
  depends on a repository setting.

**Is there an option (e) we have missed?** And is (a)'s precedent — the only
non-PR write to a base branch in the whole system — acceptable, or is it the kind
of exception that quietly becomes the rule?

### Q5 — Will "encode into skills" work, or will it freeze the defects?

M2's plan is: run one slice by hand, then encode what worked into reusable skills
so later slices cost less. But **§3.3 shows the cost was almost entirely contract
defects, not execution technique** — the executor's technique was, by and large,
correct throughout.

If the expensive part was the contracts and not the doing, what exactly is there
to encode? Specifically:

1. What belongs in a skill versus what must stay in a contract? Draw the line.
2. Is there a real risk that skills freeze the current contracts — including
   defects not yet found — and make the next correction harder rather than
   easier?

### Q6 — Is the coordinator/executor split with a human relay the right prototype?

Two of the six batches contained a **coordinator briefing error** where the
coordinator asserted a state it had not created — "the zip is unpacked" when it
was not, and "these two friction entries are logged" when they had not been
written. In both cases the executor behaved correctly on the information it was
given; the defect was upstream, in the brief.

The operator has explicitly asked to relay less. Is the two-agent split with a
human mailbox the right prototype for the agent-team goal, or is the relay itself
the defect — and if so, what replaces it **without** violating the constraints in
§4 (in particular: no credentials, manual approval, single writer)?

---

## 6. What we are *not* asking

- Not asking whether to use GitHub. That is settled (ADR-0001) and not reopening.
- Not asking for a rewrite of the gate model. Incremental corrections only,
  unless you believe the model is unsalvageable — in which case say so once,
  plainly, with the reasoning, and then answer the questions as asked anyway.
- Not asking for anything to be executed. You are read-only.

---

## 7. Required response schema

Respond in exactly this structure (`gatebraid/consult@1` `response`):

- `findings`
- `root_cause_hypotheses` — ranked, each with concrete evidence from this document
- `recommended_change` — suggestion text per question, **do not apply anything**
- `risks`
- `verification_steps` — what the operator could observe to check you were right
- `confidence` — `low` | `medium` | `high`, **per question**, not overall

Where a question admits no confident answer, say `low` and say why. A calibrated
"I don't know, and here is what would tell you" is worth more here than a
confident recommendation.
