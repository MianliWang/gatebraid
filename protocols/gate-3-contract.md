# Gate 3 contract — Publication (human-approved)

**Normative.** Inherits the common rules of `gatebraid-control-plane-spec-v1.md` §4. Changes only by ADR.

## Entry

- Recorded human `Release Approval (G2→G3)` comment exists, including its terms (what may be pushed/merged and how). **It is an approval only if it (a) is not a `gatebraid/handoff@1` block, (b) states the publication terms, and (c) was not authored by this executing session and is authored by the operator's personal account (`MianliWang`) (ADR-0015 §4, ADR-0020 §4)** — an approval authored by any other account, the executor's included, is invalid as if absent, and the observed author is recorded as `approvals[].author` — Gate 2's exit comment names the field and will match a naive search. **An executor never writes its own authorisation** (ADR-0015 §3). Workflow → `Gate 3 — Releasing`; **the `needs-human` label is removed** (this gate consumes the approval — spec §1, ADR-0011 §8).
- **Closure preconditions — two mechanisms, both checked (ADR-0012, superseding ADR-0011 §6).** A Slice must not be closable by anything except this gate's exit, because closure is what releases native `blocked-by` dependents (ADR-0007) and the spec §2 invariant is that a Slice is closed **iff** `G3 passed`. Verify both, and record both:
  - **(a) Platform automation.** No enabled Project workflow closes an issue as a consequence of a merge or a `Status` write. The built-in `Auto-close issue` rule does exactly that — it closes an issue whenever `Status` becomes `Done`, and `Status` is written to `Done` by other built-in rules. It is disabled; confirm it still is.
  - **(b) The pull request itself.** `closingIssuesReferences` is empty, and neither the body nor any commit message the pull request carries contains a **closing keyword immediately preceding an issue reference** — `keyword #n`, `keyword owner/repo#n`, `keyword <issue-url>`, in any case, where keyword is one of `close`/`closes`/`closed`, `fix`/`fixes`/`fixed`, `resolve`/`resolves`/`resolved` (ADR-0018 §1). **Test the pattern, not the bare token:** a conventional-commit `fix(scope):` prefix references nothing and is not prohibited. **Measured 2026-07-30: a merged pull request saying `Closes #n` closed its issue one second later with `Auto-close issue` disabled throughout.** That is GitHub's own behaviour, not Project automation, so check (a) cannot see it. Link the Slice issue by plain reference — `Refs #n`, `Part of #n`, or a bare URL.
  **Either check failing stops the gate. Record `(a) pass` alone is not compliance.**

## Actions

1. **Drift check first**, against the fingerprint Gate 2 recorded (ADR-0011 §2 as amended by ADR-0016 §1). The question it answers is *has the reviewed work changed since it was reviewed* — and a gate's own evidence file is the record of the review, not the work. So verify:
   - `git diff --name-only <tree_sha> HEAD` yields **only** paths inside `docs/evidence/gatebraid/<slice_id>/`;
   - every commit between `active_branch_head` and `HEAD` touches only that directory;
   - `git status --porcelain` is empty.
   Any path outside the evidence directory is drift → back to `Needs Review`; no publication. Never accept "looks the same" — run the comparison. Requiring exact head equality was not strict but unsatisfiable: committing `gate2.md` necessarily moves the head past the value `gate2.md` records.
2. Run the **exact publication commands from the approved plan**, in this order (ADR-0017 §3): push `Active Branch`; open the PR referencing the Slice issue **by plain reference, never by a closing keyword preceding a reference** (ADR-0012 §1 as amended by ADR-0018 §1); watch CI; **author and commit `gate3.md`, and push it to `Active Branch`**; then merge per the approval's terms.
3. `gate3.md` records CI status honestly as one of `ci: green` · `ci: red` · `ci: none-configured` (ADR-0011 §7). **`none-configured` is a recorded finding, not a pass:** where no check exists, the prohibition on merging with red CI is inert, and the evidence must say so rather than implying a check occurred. Neither Gatebraid repository has a workflow at the time of writing. It records the PR by URL and **does not record the merge SHA or the closure timestamp** — those are natively held and are referenced, not duplicated (ADR-0017 §2).

## Prohibited

Force-push; publishing anything beyond the approved set; merging with red CI; improvised command variants; **a closing keyword immediately preceding a reference to a Gatebraid issue**, in the pull-request body or in any commit message the branch carries (ADR-0012 §1 as amended by ADR-0018 §1); **any write to the base branch that does not arrive through the pull request** (ADR-0017 §3).

## Failure dispositions (ADR-0025 §6, executing ADR-0013's last reopening condition)

Every verification below states what happens when it fails. Entries are of three kinds: **in-machine routing** (the contract already defines where it goes), **decidable** (the state is defensible and the operator may accept it — `result: stopped`, set the matching `Next Approval`, no remediation ever), and **error** (nothing to accept, something is simply wrong — `Workflow = Blocked` with a typed `needs_input` comment).

**`Terminal` never appears directly in this table.** It is reachable only from `Human Diagnosis Required` and only by an operator-authored disposition (ADR-0025 §2). The route from this gate exists and is already wired: an **error** goes to `Blocked`, and spec §1's loop breaker — *recurrence ≥2 for the same cause → 9, not 10* — carries a cause that will not clear to `Human Diagnosis Required`, where the operator may rule terminal. Row 2b is the case that shape was written for.

| # | Verification | Failure | Disposition |
|---|---|---|---|
| 1 | Entry: the `Release Approval (G2→G3)` is valid — (a) not a `gatebraid/handoff@1` block, (b) states the publication terms, (c) authored by `MianliWang` and not by this executing session | any of (a), (b), (c) | **Outside this table — the gate does not enter.** An invalid approval is *invalid as if absent* (ADR-0020 §4, ADR-0018 §3a), so there is no state transition and nothing to dispose of. The slice stays at `Needs Release Approval`; the executor records the observed author as `approvals[].author` and reports. Friction #71 is the worked example |
| 2a | Closure precondition (a): no enabled Project automation closes an issue on a merge or a `Status` write | `Auto-close issue`, or an equivalent rule, is enabled | **error**. `decidable`'s shape is *the state may be accepted*; this state may not be — merging under it violates the spec §2 closure invariant. That a human must act to clear it does not make it acceptable. The operator disables the rule, clears the `Blocked`, and the gate re-verifies from its origin, per spec §1's *any state →10 and back to its origin on unblock*. No `Next Approval` is set: the error branch does not use one |
| 2b | Closure precondition (b), **commit-message half**: no closing keyword immediately precedes an issue reference in any commit message the pull request carries | found in a commit message | **error**. It cannot be corrected here — amending history is a force-push, which this gate prohibits — so the cause is permanent within the branch. This is the row the introduction's terminal route was written for: repeated failure for the same cause reaches `Human Diagnosis Required`, where the operator rules |
| 2c | Closure precondition (b), **pull-request-body half**: `closingIssuesReferences` empty and no closing keyword before a reference in the body | found in the body | **Not a disposition.** The body is this gate's own draft; correct it and re-run the check. That is the gate's normal loop, the same shape as Gate 1's rewrite-and-re-dry-run |
| 3 | Action 1 drift check: `<tree_sha>..HEAD` touches only the slice's evidence directory, every commit between `active_branch_head` and `HEAD` likewise, `git status --porcelain` empty | any path outside the evidence directory | **in-machine routing, already stated** — back to `Needs Review`; no publication. Recognised here, not restated |
| 4 | Action 3 CI status | `ci: red` | **in-machine routing** — back to `Needs Review`; no publication. Red CI is Gate 2's subject appearing at Gate 3: every repair is a code change and must return through the review machinery, so there is nothing for the operator to arbitrate. `ci: none-configured` is unchanged — a recorded finding, not a pass, and not a failure of this verification |
| 5 | Exit sequence: `gate3.md` committed and pushed to `Active Branch` **before** the merge; the merge per the approval's terms; explicit closure; lease released | a step cannot complete — branch protection blocks the merge, the push is rejected, closure fails | **error**. The publication sequence is ordered and cannot be completed out of order or in part |

## Exit

The order is normative, and `gate3.md` is written *before* the merge because it carries no post-merge value (ADR-0017 §3):

1. `docs/evidence/gatebraid/<slice_id>/gate3.md` written from `templates/gate3-evidence.md` (`gate: 3`), committed to `Active Branch` and pushed — **action 2 above**, before the merge. It therefore reaches the base branch through the pull request like every other change.
2. The merge — action 2 above.
3. `Gate = G3 passed`.
4. Workflow → `Done`.
5. **Then close the Slice issue by an explicit command** — never as a side effect of a merge, a status write, or anything else (ADR-0012 §3). Closure is what releases native `blocked-by` dependents (ADR-0007), so it happens exactly here, once, and never earlier.
6. Release the `Writer Lease`; set `Next Approval` back to `—`; handoff comment posted; `Last Checkpoint` updated.

The authoritative Gate 3 record is the **composite** of this file, the pull request's merge event, the issue's closure event and the Project's `Workflow` (ADR-0017 §1). A consumer reconstructing state reads the native **event sequence**, not the last state — an issue can be reopened and a comment can be edited (ADR-0017 §4).
