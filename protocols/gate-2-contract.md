# Gate 2 contract — Implementation (single writer)

**Normative.** Inherits the common rules of `gatebraid-control-plane-spec-v1.md` §4. Changes only by ADR.

## Entry

- Recorded human `Plan Approval (G1→G2)` comment exists. **It is an approval only if it (a) is not a `gatebraid/handoff@1` block, (b) names both `plan_hash` and `allowlist_hash`, and (c) was not authored by this executing session and is authored by the operator's personal account (`MianliWang`) (ADR-0015 §4, ADR-0020 §4).** An approval authored by any other account — the executor's included — is invalid as if absent; record the observed author as `approvals[].author`. Gate 1's own handoff comment contains both hashes *and* the words `Plan Approval`, because Gate 1's exit sets that field — matching on either will read the gate's own exit as consent. **An executor never writes its own authorisation** (ADR-0015 §3). Then set `Next Approval` back to `—`; **the `needs-human` label is removed** (this gate consumes the approval — spec §1, ADR-0011 §8).
- `Writer Lease` taken (`<host>:<session-label>:<ISO8601>`). Workflow → `Gate 2 — Implementing`.
- **Baseline re-read (ADR-0011 §9).** After taking the lease and before creating the branch, read the head of the base branch as `Y` and compare it with the plan baseline `X` recorded in `gate0.md`. The lease was not held during Gate 1 or the Plan-Approval wait, so the baseline may legitimately have moved. Record the outcome in `gate2.md` **in every case, including no change**, and route:
  - `X == Y` → proceed; record `baseline: unchanged`.
  - `X != Y`, and the paths changed by `X..Y` do not intersect the frozen `write_domains` or any file the plan explicitly cites → proceed; record the delta summary. The plan's assumptions are intact.
  - **Exclude `docs/evidence/gatebraid/<slice_id>/` from the changed-path set before comparing (ADR-0014 §1).** This slice's own Gate 0 and Gate 1 committed their evidence there, and that path is in the allowlist by design — without this exclusion every slice would route to `Scope / Allowlist Change` at its own entry, invalidating a plan by the act of documenting it.
  - `X != Y` **and** the intersection is non-empty → the plan is invalidated. `Next Approval = Scope / Allowlist Change`; follow `templates/gatebraid-correct-course.md` and re-freeze with new hashes. Do not proceed on a stale plan.
- `Active Branch` created from `Y`; the `Base SHA` Project field is set to `Y`. The branch starts from current reality so it merges cleanly; `X` keeps its one job, which is judging whether the plan still holds.

## Actions

1. Implement **strictly inside the frozen allowlist** (`write_domains`, hash-pinned at Gate 1).
2. Small, frequent commits on `Active Branch` — **commits yes, push no**; publication is Gate 3.
3. Run the declared test plan; embed outputs in the evidence file (evidence, not assertion).
4. `/goal` is permitted only here (and in bounded Gate 0/1 evidence tasks), with the turn/time bound written inside the condition — never across an approval boundary.

## Repair sequence (unified, report 11 D6 — fixed)

red check → **repair 1 with a new hypothesis** → still red → **Codex consult** (`templates/consult.md`; embedded evidence; fixed response schema; recorded `ACCEPT/PARTIAL/REJECT`) → apply the independently-verified fix → still red → **repair 2** → still red → `Human Diagnosis Required`. `repair_limit = 2`; no third repair. `consult_first: true` moves the consult before repair 1. Blocker recurrence ≥2 for the same cause → `Human Diagnosis Required`, not another `Blocked` round. **A repair is measured before it is graded** (ADR-0027 §1): before an attempt's `result` is recorded, compare `git rev-parse HEAD^{tree}` against the tree at the previous failed state — the failing review for repair 1, the prior attempt otherwise. **An unchanged tree is not a repair:** record the attempt as consumed — `result: still_red`, hypothesis annotated `(unchanged-tree)` — and advance the sequence without a re-review. The new-hypothesis rule (ADR-0002 §4) keeps its semantic force above this mechanical floor.

## Mid-slice scope discovery

Follow `templates/gatebraid-correct-course.md`: stop → document the delta → `Next Approval = Scope / Allowlist Change` → human re-approval re-freezes plan + allowlist (new hashes recorded). **Never silently widen.**

## Prohibited

Touching files outside the allowlist; push/PR/merge; `git reset` / `git clean` / `git checkout` against baseline state; installing dependencies not in the approved plan; disabling hooks or checks; a second writer of any kind. "Outside the allowlist" means outside the frozen `write_domains` within the working repository; scratch paths outside any repository are unconstrained by this clause and are named in the evidence file when relied on.

## Review (read-only, at exit)

Five items, each recorded pass/fail with its evidence in `gate2.md`. Any fail → `Repair Required`. The reviewer runs as `Executor = Claude Read-Only Team` under a **read-only mandate it attests to** — on this host the restriction is a mandate the reviewer keeps, not a capability the environment withholds, and a clause claiming otherwise asserts a guarantee nothing enforces (ADR-0004, friction #73). **Any write the reviewer makes is disclosed in its report**, naming the path and the scope of what it affects; the gate records that disclosure in `gate2.md` as `none` or as the list. Disclosure is the behaviour this clause requires — a silent write is what would invalidate the independence R3 rests on. A review with no defined failure mode carries no information (ADR-0011 §4). The reviewer's mandate carries the spec §4 conduct rules verbatim — a reviewer, like any subagent, is bound by rules only if dispatched with them (friction #97) — and its report states which rules it was given.

- **R1 — allowlist confinement.** `git diff --name-only <base_sha>..<head>` is a subset of the frozen `write_domains`. Mechanical. R1 additionally verifies at review time that `git status --porcelain --untracked-files=all` shows nothing outside the frozen `write_domains` — a write created and removed inside the gate is invisible to the diff; this catches the live case (friction #107). A gate's commands write only inside the allowlist or outside every repository; where a command needs a scratch path, the plan names it.
- **R2 — test-plan coverage.** Every acceptance item on the Slice issue is covered by a declared test-plan command; the reviewer states the mapping item by item.
- **R3 — evidence is rows that reproduce.** The file contains no content outside ADR-0026's classes — metadata block, record rows, required disclosures, template-fixed headings and labels (and, at Gate 1, the frozen-plan section). Every record row is a command plus its generated output, the command line carrying its environment visibly (friction #89). For the deterministic subset — `git diff`, `git rev-parse`, `grep`/`rg` over committed content, hash computations — the reviewer re-runs the command and compares **bytes** (friction #96); for the rest, the row's label states the load-bearing property and the reviewer checks that property against a re-run or the committed log. Every elision carries `shown/total` and the full output's committed path. The remedy's own section is checked first against the defect class it remedies (ADR-0026 §5; friction #87, #88, #96).
- **R4 — the slice's negative criterion.** The property declared in the frozen Gate 1 plan does not hold false anywhere in the diff. Where the criterion is mechanised as a token search, **the check must state the pattern it proxies for, and where the proxy over-matches the pattern governs** (ADR-0018 §2). For the standard "no GitHub mutation" criterion that means GraphQL **mutation operations** — a document whose operation type is `mutation` — not the string `mutation`, which occurs in ordinary prose and in comments asserting that the code performs none. A check that correct work cannot satisfy is not strict; it is broken, and it trains the executor to route around checks.
- **R5 — no prohibited action.** No push, no PR, no merge, no dependency installation outside the approved plan, no disabled hook or check, no second writer.

## Failure dispositions for R1–R5 (ADR-0025 §6)

Any of R1–R5 failing routes to `Repair Required` **while repair budget remains**, and from there the unified repair sequence above governs — including its Codex consult, which is a step of the sequence and not an option within it. When `repair_limit` is spent and a review item still fails, the gate routes to **`Human Diagnosis Required`**. The operator then directs one of exactly two things: remediation under stated rules followed by **one full re-review**, or the **terminal** disposition.

**No gate, review outcome, or executor judgement reaches terminal on its own** (ADR-0025 §2). Terminal is an operator act, authored on the Slice issue and verified as any door is (ADR-0020 §4). *"No remediation, ever"* carries over from `decidable`: a terminated record is disposed of as it stands, and the defects the last review found are recorded in place rather than corrected.

## Exit

- Tests green per the plan; `docs/evidence/gatebraid/<slice_id>/gate2.md` written from `templates/gate2-evidence.md` with verification outputs.
- **Handoff fingerprint recorded** in `gate2.md`, so Gate 3's drift check has something to compare against (ADR-0011 §2): `active_branch_head` (commit SHA) · `tree_sha` (`git rev-parse <head>^{tree}`) · the sorted output of `git diff --name-only <base_sha>..<head>`. Git's own content addressing is used rather than a hash of diff text, because a tree SHA is exact and reproducible.
- Workflow → `Needs Review`; reviewers pass → `Gate = G2 passed`, Workflow → `Needs Release Approval`, **`Next Approval = Release Approval (G2→G3)`**, `needs-human` on.
  Setting `Next Approval` is what puts the release door into the `Needs Me` queue. Without it the slice carries `—` and is filtered out, leaving only the `needs-human` label — the half of the view definition the filter bar cannot express (ADR-0011 §1).
