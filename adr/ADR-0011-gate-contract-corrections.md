# ADR-0011 — Gate contract corrections before first execution

**Status:** Accepted · M2 (2026-07-30) · Product: Gatebraid (ADR-0010)
**Provenance:** Pre-execution audit of the four Gate contracts as merged at
`main` (`91546fe`), conducted with the operator on 2026-07-30; M1 verification
manifest §6.1, §8, §9; ADR-0002 (gate workflow), ADR-0003 (single writer),
ADR-0007 (dependency encoding), ADR-0008 (Workflow as sole state authority);
`protocols/gatebraid-control-plane-spec-v1.md` §1–§2.

## Context

M1 wrote and merged four Gate contracts. Nothing had ever executed them. Before
the first slice was run by hand, the four contracts were audited line by line
against each other and against the spec. Nine defects were found — eight
internal contradictions or omissions, and one behaviour the contracts never
defined at all.

They fall into three kinds, and the distinction matters because it decides who
can fix them:

- **Contract-internal** — a contract omits a required action, or two contracts
  disagree. Fixed by editing the text. Items 1, 2, 3, 4, 5, 8.
- **Contract vs. platform** — the contract asserts something the GitHub Project
  can override. Fixed by making the contract state its precondition explicitly,
  and by changing the platform configuration in a separate approved batch.
  Items 6, 7.
- **Undefined** — a real situation the contracts simply never addressed.
  Item 9.

Every one of these would have surfaced during the first hand-run as either a
stall or an improvisation. Improvisation is prohibited by the operating rules,
so a stall was the likely outcome. Fixing them first is cheaper than
discovering them one at a time from inside a half-executed slice.

The Gate contracts each carry the clause *"Changes only by ADR."* This ADR is
that authority.

## Decision

**1. Gate 2's exit sets `Next Approval`.** On passing review, Gate 2 sets
`Next Approval = Release Approval (G2→G3)` in addition to `Gate = G2 passed`,
`Workflow = Needs Release Approval` and the `needs-human` label.

*Why:* Gate 1's exit sets its approval field; Gate 2's did not. Gate 2's entry
had already returned the field to `—`, so a slice awaiting release approval
carried `—` and was filtered **out** of the `Needs Me` view. Its only marker was
the `needs-human` label — precisely the half of the view's definition the
filter bar cannot express (manifest §8). The result was that of the system's two
human doors, the release door was invisible in the human attention queue. Gate
3's exit already said to set `Next Approval` "back to `—`", which presupposes it
had been set; the omission was clerical, not intentional.

**2. Gate 2's exit records a handoff fingerprint, and Gate 3's drift check
compares against it.** Gate 2 records, in `gate2.md`: `active_branch_head` (the
commit SHA), `tree_sha` (`git rev-parse <head>^{tree}`), and the sorted output
of `git diff --name-only <base_sha>..<head>`. Gate 3's first action verifies
that the current head and tree equal the recorded values and that
`git status --porcelain` is empty.

*Why:* Gate 3 required the working tree and staged set to "match the Gate 2
handoff exactly", but Gate 2 produced no artefact to match against, so the
check was unperformable as written. Git's own content addressing is used rather
than a hash of diff text, because a tree SHA is exact and reproducible while
diff output varies with git version and configuration.

**3. `plan_hash` and `allowlist_hash` are defined exactly.** Both are SHA-256,
lowercase hex, over UTF-8 bytes, computed as:

- `allowlist_hash` — each `write_domains` entry stripped of surrounding
  whitespace, sorted by byte value, joined with `\n`, one trailing `\n`.
- `plan_hash` — the lines of `gate1.md` strictly between the
  `## Plan (frozen at exit)` heading and the next line beginning with `## `,
  each stripped of trailing whitespace, with leading and trailing blank lines
  removed, joined with `\n`, one trailing `\n`.

Both are recomputable with Python 3's standard library alone (ADR-0009), and the
recomputation command is recorded in the evidence file beside the value.

*Why:* the contracts required these hashes and Gate 2 relied on the allowlist
being "hash-pinned at Gate 1", but no algorithm or canonical input was ever
specified. A hash nobody can recompute is decoration, and the correct-course
procedure's "new hashes recorded" was equally unverifiable.

**4. Gate 2 defines what the review checks.** The read-only review at Gate 2's
exit has five items, each recorded pass/fail with its evidence in `gate2.md`.
Any fail sends the slice to `Repair Required`.

- **R1 — allowlist confinement.** `git diff --name-only <base_sha>..<head>` is a
  subset of the frozen `write_domains`. Mechanical.
- **R2 — test-plan coverage.** Every acceptance item on the Slice issue is
  covered by a declared test-plan command. Judgement; the reviewer states the
  mapping item by item.
- **R3 — evidence is evidence.** The outputs embedded in `gate2.md` are real
  outputs of the declared commands, not assertions about them.
- **R4 — the slice's negative criterion.** The criterion declared in the Gate 1
  plan (see decision 5) does not hold false anywhere in the diff.
- **R5 — no prohibited action.** No push, no PR, no merge, no dependency
  installation outside the approved plan, no disabled hook or check, no second
  writer.

The reviewer runs as `Executor = Claude Read-Only Team` and holds no write
tools, per ADR-0004.

*Why:* Gate 2's exit said only "read-only reviewers pass", naming neither the
criteria nor the artefact reviewed. A review with no defined failure mode
cannot fail, and therefore carries no information.

**5. The Gate 1 plan declares a negative criterion.** Alongside approach,
allowlist, test plan, risk notes and rollback note, the frozen plan states at
least one property the diff must **not** have, chosen to be checkable — for
example "contains no write operation", "adds no runtime dependency", "touches no
file outside `bin/`".

*Why:* it gives R4 something definite to check, and it is the cheapest way to
make a first review non-vacuous. Positive criteria are easy to satisfy
superficially; a negative criterion either holds or does not.

**6. Gate 3 will not publish while an automation can close the Slice issue.**
Before the merge step, Gate 3 verifies that no enabled Project automation closes
an issue as a consequence of a merge or a status write. If one is enabled — at
the time of writing, the built-in `Auto-close issue` rule — Gate 3 stops and
records the reason; it does not merge.

*Why:* Gate 3's exit states that closure "happens exactly here and never
earlier", because closure is what releases native `blocked-by` dependents
(ADR-0007), and the spec's invariant is that a Slice issue is closed **iff**
`Gate = G3 passed`. The `Auto-close issue` rule closes an issue whenever its
`Status` becomes `Done`, and `Status` is written to `Done` by other built-in
rules including `Pull request merged`. A Slice's own pull request is linked to
its issue, so the merge in Gate 3's step 2 could close the Slice before its
evidence file is written and before `Gate = G3 passed` — releasing dependents
early and violating the invariant. Whether `Pull request merged` writes to the
linked issue's item or only to the pull request's own item is not yet measured;
the contract therefore refuses to depend on the answer.

**7. Gate 3 records continuous-integration status honestly.** Gate 3 records one
of `ci: green`, `ci: red`, or `ci: none-configured`. `none-configured` is a
recorded finding, not a pass: the contract's prohibition on merging with red CI
is inert where no check exists, and the evidence file says so rather than
implying a check occurred.

*Why:* neither repository has any workflow, so "watch CI" and "no merging with
red CI" are currently vacuous. A publication guard that silently does nothing is
worse than one that is absent, because it reads as satisfied.

**8. The `needs-human` label is removed at the gate that consumes the approval.**
Gate 2's entry (Workflow 4→5) and Gate 3's entry (11→12) each remove it
explicitly. Gate 0's shortcut from `Gate 0 — Verifying` directly to
`Needs Plan Approval` is **removed**; every slice passes through Gate 1.

*Why:* the spec's label rule says the label is removed "on exit", but neither
gate's text listed the action, and a hand-executed run follows the contract in
front of it. Separately, the Gate 0 shortcut described a 2→4 transition that the
spec's legal-transition table does not contain, and it would have produced a
slice with no `plan_hash`, no `allowlist_hash` and no exit checklist — while
Gate 2 requires an allowlist pinned at Gate 1. Removing the shortcut restores a
single source of truth; Gate 1 for a genuinely trivial slice is cheap.

**9. `Base SHA` is two facts, and they are separated.** The commit recorded at
Gate 0 is the **plan baseline** — the tree the plan was made against — and lives
in `gate0.md`. The **branch baseline** is chosen at Gate 2, after the
`Writer Lease` is held, and is what the `Base SHA` Project field carries and
what `Active Branch` is cut from.

At Gate 2's entry, after taking the lease and before creating the branch, the
head of the base branch is re-read as `Y` and compared with the Gate 0 value
`X`. The result is recorded in `gate2.md` **in every case, including no change**,
and routed as follows:

- `X == Y` → proceed; record `baseline: unchanged`.
- `X != Y` and the paths changed by `X..Y` do not intersect the frozen
  `write_domains` or any file the plan explicitly cites → proceed; record the
  delta summary. The plan's assumptions are intact.
- `X != Y` and the intersection is non-empty → the plan is invalidated. Set
  `Next Approval = Scope / Allowlist Change` and follow
  `templates/gatebraid-correct-course.md`: stop, document the delta, obtain human
  re-approval, re-freeze the plan and allowlist with new hashes.

*Why:* the `Writer Lease` is taken at Gate 2's entry, but `Base SHA` was
recorded at Gate 0 — so the entire Gate 1 planning period and the whole
Plan-Approval wait, which may span days, are unprotected. Another slice can
legitimately merge in that window. Conflating "what the plan assumed" with
"where the branch starts" made the situation impossible to reason about.
Separating them makes the branch start from current reality, which merges
cleanly, while the Gate 0 value does the one job it is good for: judging whether
the plan still holds.

This introduces no new concepts. `write_domains` is already frozen and hashed at
Gate 1; `Scope / Allowlist Change` is already a `Next Approval` option;
`gatebraid-correct-course.md` already specifies stop → document → re-approve →
re-freeze. Only the trigger is new.

Two alternatives were rejected. **Return to Gate 0 on any baseline change** is
too severe: an unrelated merge would destroy a sound plan and burn a human
approval, and in an active repository it could livelock. **Ignore the change** —
the behaviour before this ADR — is not unsafe so much as silent: nobody learns
the plan is stale, and Gate 3 discovers the conflict at the worst possible
moment, after a Release Approval was granted on terms that may no longer hold.

## Consequences

The four Gate contracts and the three gate-evidence templates change; `gate2.md`
and `gate3.md` carry new required fields. No Project field, view, option or
label changes, and no new schema is introduced.

Decisions 6 and 7 make two platform gaps explicit rather than closing them.
Both are owned by M2:

- disable the `Auto-close issue` built-in workflow, then measure what
  `Pull request merged` actually writes to;
- stand up a minimal CI check, or record for each release that none exists.

Until the first is done, decision 6 blocks Gate 3 — deliberately. A slice can be
implemented and reviewed, but not published, while an automation can close it
behind the contract's back.

Decision 9's re-read is expected to be a no-op on the first runs, with a single
solo operator and one slice in flight. That is the right time to introduce it:
the machinery is exercised while the stakes are nil, and `baseline: unchanged`
in the first `gate2.md` is itself evidence the check ran.

ADR numbering: the operating-rhythm ADR sketched in manifest §9 as "candidate
ADR-0011" becomes ADR-0012.

## Reopening conditions

- If a baseline re-read at Gate 2 routes a slice to `Scope / Allowlist Change`
  more than twice in ten slices, the window between Gate 0 and the lease is too
  long, and the fix is to move the lease earlier rather than to relax decision 9.
- If measurement shows `Pull request merged` writes only to the pull request's
  own Project item and never to a linked issue's, decision 6 may be narrowed to
  the `Auto-close issue` rule alone.
- If the review defined in decision 4 never fails across ten slices, either the
  criteria are too weak or the reviewer is not independent; both are grounds to
  revisit, not to celebrate.
