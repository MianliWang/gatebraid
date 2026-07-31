# Gate 2 contract — Implementation (single writer)

**Normative.** Inherits the common rules of `gatebraid-control-plane-spec-v1.md` §4. Changes only by ADR.

## Entry

- Recorded human `Plan Approval (G1→G2)` comment exists. **It is an approval only if it (a) is not a `gatebraid/handoff@1` block, (b) names both `plan_hash` and `allowlist_hash`, and (c) was not authored by this executing session (ADR-0015 §4).** Gate 1's own handoff comment contains both hashes *and* the words `Plan Approval`, because Gate 1's exit sets that field — matching on either will read the gate's own exit as consent. **An executor never writes its own authorisation** (ADR-0015 §3). Then set `Next Approval` back to `—`; **the `needs-human` label is removed** (this gate consumes the approval — spec §1, ADR-0011 §8).
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

red check → **repair 1 with a new hypothesis** → still red → **Codex consult** (`templates/consult.md`; embedded evidence; fixed response schema; recorded `ACCEPT/PARTIAL/REJECT`) → apply the independently-verified fix → still red → **repair 2** → still red → `Human Diagnosis Required`. `repair_limit = 2`; no third repair. `consult_first: true` moves the consult before repair 1. Blocker recurrence ≥2 for the same cause → `Human Diagnosis Required`, not another `Blocked` round.

## Mid-slice scope discovery

Follow `templates/gatebraid-correct-course.md`: stop → document the delta → `Next Approval = Scope / Allowlist Change` → human re-approval re-freezes plan + allowlist (new hashes recorded). **Never silently widen.**

## Prohibited

Touching files outside the allowlist; push/PR/merge; `git reset` / `git clean` / `git checkout` against baseline state; installing dependencies not in the approved plan; disabling hooks or checks; a second writer of any kind.

## Review (read-only, at exit)

Five items, each recorded pass/fail with its evidence in `gate2.md`. Any fail → `Repair Required`. The reviewer runs as `Executor = Claude Read-Only Team` and holds no write tools (ADR-0004). A review with no defined failure mode carries no information (ADR-0011 §4).

- **R1 — allowlist confinement.** `git diff --name-only <base_sha>..<head>` is a subset of the frozen `write_domains`. Mechanical.
- **R2 — test-plan coverage.** Every acceptance item on the Slice issue is covered by a declared test-plan command; the reviewer states the mapping item by item.
- **R3 — evidence is evidence.** The outputs embedded in `gate2.md` are real outputs of the declared commands, not assertions about them.
- **R4 — the slice's negative criterion.** The property declared in the frozen Gate 1 plan does not hold false anywhere in the diff. Where the criterion is mechanised as a token search, **the check must state the pattern it proxies for, and where the proxy over-matches the pattern governs** (ADR-0018 §2). For the standard "no GitHub mutation" criterion that means GraphQL **mutation operations** — a document whose operation type is `mutation` — not the string `mutation`, which occurs in ordinary prose and in comments asserting that the code performs none. A check that correct work cannot satisfy is not strict; it is broken, and it trains the executor to route around checks.
- **R5 — no prohibited action.** No push, no PR, no merge, no dependency installation outside the approved plan, no disabled hook or check, no second writer.

## Exit

- Tests green per the plan; `docs/evidence/gatebraid/<slice_id>/gate2.md` written from `templates/gate2-evidence.md` with verification outputs.
- **Handoff fingerprint recorded** in `gate2.md`, so Gate 3's drift check has something to compare against (ADR-0011 §2): `active_branch_head` (commit SHA) · `tree_sha` (`git rev-parse <head>^{tree}`) · the sorted output of `git diff --name-only <base_sha>..<head>`. Git's own content addressing is used rather than a hash of diff text, because a tree SHA is exact and reproducible.
- Workflow → `Needs Review`; reviewers pass → `Gate = G2 passed`, Workflow → `Needs Release Approval`, **`Next Approval = Release Approval (G2→G3)`**, `needs-human` on.
  Setting `Next Approval` is what puts the release door into the `Needs Me` queue. Without it the slice carries `—` and is filtered out, leaving only the `needs-human` label — the half of the view definition the filter bar cannot express (ADR-0011 §1).
