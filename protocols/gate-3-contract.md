# Gate 3 contract — Publication (human-approved)

**Normative.** Inherits the common rules of `gatebraid-control-plane-spec-v1.md` §4. Changes only by ADR.

## Entry

- Recorded human `Release Approval (G2→G3)` comment exists, including its terms (what may be pushed/merged and how). **It is an approval only if it (a) is not a `gatebraid/handoff@1` block, (b) states the publication terms, and (c) was not authored by this executing session (ADR-0015 §4)** — Gate 2's exit comment names the field and will match a naive search. **An executor never writes its own authorisation** (ADR-0015 §3). Workflow → `Gate 3 — Releasing`; **the `needs-human` label is removed** (this gate consumes the approval — spec §1, ADR-0011 §8).
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

## Exit

The order is normative, and `gate3.md` is written *before* the merge because it carries no post-merge value (ADR-0017 §3):

1. `docs/evidence/gatebraid/<slice_id>/gate3.md` written from `templates/gate3-evidence.md` (`gate: 3`), committed to `Active Branch` and pushed — **action 2 above**, before the merge. It therefore reaches the base branch through the pull request like every other change, and **no gate ever writes to the base branch outside one**.
2. The merge — action 2 above.
3. `Gate = G3 passed`.
4. Workflow → `Done`.
5. **Then close the Slice issue by an explicit command** — never as a side effect of a merge, a status write, or anything else (ADR-0012 §3). Closure is what releases native `blocked-by` dependents (ADR-0007), so it happens exactly here, once, and never earlier.
6. Release the `Writer Lease`; set `Next Approval` back to `—`; handoff comment posted; `Last Checkpoint` updated.

The authoritative Gate 3 record is the **composite** of this file, the pull request's merge event, the issue's closure event and the Project's `Workflow` (ADR-0017 §1). A consumer reconstructing state reads the native **event sequence**, not the last state — an issue can be reopened and a comment can be edited (ADR-0017 §4).
