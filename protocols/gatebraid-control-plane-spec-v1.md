# Gatebraid Control-Plane Specification v1

**Artifact:** `protocols/gatebraid-control-plane-spec-v1.md` — normative definitions for the "Mianli Engineering" GitHub Project and the Gate contracts.

> **Provenance (Gatebraid edition).** This is the ADR-0010 edition of
> `classic-control-plane-spec-v1.md` (issued 2026-07-27 by the architecture
> owner, report 12; that file remains the historical original under its former
> title). Ported into this repository at M1 (2026-07-29): **only names moved**
> per the ADR-0010 mapping (product → Gatebraid; control repo →
> `MianliWang/gatebraid`; schema ids → `gatebraid/*@1`; metadata heading →
> `## gatebraid-metadata`; `gatebraid-*` template/script names; evidence path →
> `docs/evidence/gatebraid/`). The workflow profile id **`classic`** is a
> stable identifier and is retained. **One flagged content substitution:** the
> illustrative `depends_on` example now references the scratch repository
> instead of a business repository (business-repository names do not appear in
> new M1 resources). No other content changed.

**Issued:** 2026-07-27, by the architecture owner (Claude, report 12). **Authority:** for the items defined here — Workflow options, field option lists, view definitions, Gate contracts — this file **supersedes the GPT-5.6 proposal text**. It is consolidated from reports 09–12 and incorporates corrections D1–D8 (report 11) and ADR-0007/0008 semantics (report 12 §9). Referenced from ADR-0002.

Design note (deliberate change): there is **no stored `Ready` state**. Readiness is *derived* — computed by the frontier logic from dependencies, Gate fields, leases, and locks. Storing it as a Workflow option would duplicate computed data and drift. The "Ready Frontier" view shows candidates; the `next` skill (M2) / `gatebraid-frontier` script (M3) delivers the verdict.

---

## 1. `Workflow` field — single-select, exactly 14 options (in order)

| # | Option | Meaning | Terminal action lives with |
|---|---|---|---|
| 1 | `Backlog` | Captured; no gate work started. The frontier's candidate pool. | frontier |
| 2 | `Gate 0 — Verifying` | Read-only authority & baseline verification in progress. | Lead |
| 3 | `Gate 1 — Planning` | Read-only planning in progress (temporary team permitted). | Lead |
| 4 | `Needs Plan Approval` | Gate 1 exit checklist complete; plan + allowlist frozen; awaiting human G1→G2 approval. | **Human** |
| 5 | `Gate 2 — Implementing` | Single-writer implementation under the frozen allowlist. | Lead |
| 6 | `Needs Review` | Implementation paused for review (adversarial / test-compat reviewers, read-only). | reviewers |
| 7 | `Repair Required` | Review or checks red; a repair attempt (with a **new hypothesis**) is owed. | Lead |
| 8 | `Codex Consultation` | Read-only Codex consult in flight (after repair-1 fails, or `consult_first`). | Lead + Codex |
| 9 | `Human Diagnosis Required` | Repair budget exhausted (2) or blocker-recurrence limit hit; human decides. | **Human** |
| 10 | `Blocked` | Waiting on an external dependency, input, or capability. Typed reason in a comment. | varies |
| 11 | `Needs Release Approval` | Review clean; awaiting human G2→G3 approval to publish. | **Human** |
| 12 | `Gate 3 — Releasing` | Approved publication in progress (push / PR / CI / merge, exact commands). | Lead |
| 13 | `Done` | Gate 3 evidence recorded; `Gate = G3 passed`; the Slice issue is closed. | — |
| 14 | `Aborted` | **Terminal.** The slice's work ended without publication, by an operator-authored disposition from `Human Diagnosis Required` (ADR-0025 §2–§4). Records retained, operational values cleared, and the Slice issue is **not** closed — closure remains `iff G3 passed` (§2). | — |

**Label coupling (ADR-0008):** the `needs-human` repository label is set **exactly** when Workflow ∈ {4, 9, 11} or Workflow = 10 with a `needs_input`-typed block reason — and removed on exit (executor-maintained in M2 — the label moves because the executor moves it at the transition; the M3 guard mechanizes the coupling). It is the only mirrored label unless the M0 phone probe demanded a second (probe results recorded in ADR-0008 — no second label was demanded).

**Legal transitions (enforced by skills in M2, guard in M3):** 1→2→3→4→5; 5→6; 6→{11, 7}; 7→{6 after repair-1, 8 after repair-1 fails}; 8→{6 after applied fix, 9}; 6→7→…→9 caps repairs at `repair_limit` (default 2); any state →10 and back to its origin on unblock (recurrence ≥2 for the same cause → 9, not 10 — the Hermes-derived loop breaker); 11→12→13; **9→14** is terminal and operator-only (ADR-0025 §2, §4); the edge is directional — 9 is the only state that enters 14; operator-directed remediation runs under state 9 and, on success, re-enters the machinery at the state the directing gate's contract defines for the completed step (Gate 2: the directed full re-review passing exits as a passing review exits). Approvals 4→5 and 11→12 are human-only and recorded as an approval comment plus the `Next Approval` field returning to `—`.

## 2. Other single-select option lists

**`Gate` — 5 options.** Semantics: *highest gate completed* for this Slice. `depends_on[].requires_gate` compares against this field on the predecessor.
`—` (none) · `G0 passed` · `G1 passed` · `G2 passed` · `G3 passed`
Invariant: the Slice issue is closed iff `G3 passed` (this is what makes native `blocked-by` = Gate-3 dependency per ADR-0007).

**`Executor` — 5 options.** Who currently holds the active work item.
`Human` · `Claude Lead` · `Claude Read-Only Team` · `Codex Consultant` · `Cowork Coordinator`

**`Next Approval` — 9 options.** What human decision, if any, is pending (drives Needs Me). **`—` is the resting value, and "clearing" this field always means setting it to `—`, never removing the value.** The Needs Me view is filtered on `!= —`, and GitHub's negation also matches items with no value at all (measured, M1 verification manifest §6.1), so an unset field puts the item into the human attention queue permanently.
`—` · `Plan Approval (G1→G2)` · `Release Approval (G2→G3)` · `Dirty Baseline Acceptance` · `Scope / Allowlist Change` · `Environment Change` · `Session Persistence` · `Worktree Exception` · `Human Diagnosis`

**`Environment` — 4 options.** `wsl` · `windows` · `macos-authority` · `mixed-see-prose`

**`Risk` — 3 options.** `low` · `medium` · `high`

**Remaining fields (type only):** `Stage` (text: e.g. `S5`), `Phase` (text: `P53`), `Slice` (text: `P53-S16`), `Base SHA` (text), `Active Branch` (text), `Parallel Group` (text), `Writer Lease` (text: `<host>:<session-label>:<ISO8601>` or empty), `Last Checkpoint` (text: ISO8601 + one-line note). 14 custom fields total — verified under the 50-field Project cap; Workflow's 14 options sit under the 50-option cap (13 verified at M1; option 14 added by ADR-0025 §4).

## 3. View definitions — 12 views

| View | Layout | Filter / grouping | Purpose & notes |
|---|---|---|---|
| **Needs Me** | Table | `Next Approval != —` OR label `needs-human`; sort `Risk` desc, then oldest first | The attention/phone queue. Must render on mobile (probe-dependent: field vs label). |
| **Ready Frontier** | Table | `Workflow = Backlog`, open issues; group by `Parallel Group` | **Candidate pool only.** True readiness is computed by the `next` skill / `gatebraid-frontier`; this view never claims a slice is startable. |
| **Active** | Board (column = `Workflow`) | `Workflow ∈ {Gate 0 — Verifying, Gate 1 — Planning, Gate 2 — Implementing, Gate 3 — Releasing}` | What is running right now; one glance shows the single writer per repo. |
| **Planning** | Table | `Workflow ∈ {Gate 0 — Verifying, Gate 1 — Planning, Needs Plan Approval}` | The pre-implementation pipeline. |
| **Codex Consultations** | Table | `Workflow = Codex Consultation` | Live + recent consults; link column to consult artifacts. |
| **Review Queue** | Table | `Workflow = Needs Review` | Reviewer worklist. |
| **Repair Queue** | Table | `Workflow ∈ {Repair Required, Human Diagnosis Required}`; sort `Risk` desc | Red work; Human Diagnosis rows are also in Needs Me. |
| **Blocked** | Table | `Workflow = Blocked` | Show the native Blocked (dependency) indicator alongside; typed block reason lives in the latest comment. |
| **Release Queue** | Table | `Workflow ∈ {Needs Release Approval, Gate 3 — Releasing}` | Publication pipeline. |
| **By Project** | Table, group by repository | all open items | Per-repo load and lease sanity. |
| **By Stage** | Table (roadmap layout optional), group by `Stage` | all items | Portfolio structure; Stage/Phase progress via sub-issue progress fields. |
| **All Work** | Table, no filter, all fields visible | everything incl. closed | The audit view; source for the weekly brief. |

## 4. Gate contracts (normative, per the locked spec + D6 repair sequence)

**Common rules for all gates.** Single writer per repository (the `Writer Lease` field names it); Codex is always read-only (`--ephemeral --sandbox read-only`, no bypass, snapshot disabled); no worktrees (a `Worktree Exception` approval is the only override); no API keys; every gate is resumable from the Issue + fields + committed evidence + Git state alone (the report 12 §9 recovery invariant); every gate ends by writing its evidence file, a structured handoff comment (report-10 schema: `changed_files`, `verification` with owners, `residual_risk`, plus decisions), and updating `Gate`, `Workflow`, `Last Checkpoint`. Evidence lives at `docs/evidence/gatebraid/<slice_id>/gate<N>.md` in the working repo (cross-project artifacts in `MianliWang/gatebraid` `evidence/`). **A check that gates an action is a separate step whose failure prevents the action** — identity, schema, hash, drift, allowlist alike: the exit status, not the printed text, decides whether the next command runs; where check and action must share an invocation, the check comes first and ends in `|| exit 1` (friction #61, #86). **Constraints bind the work, not the worker:** any subagent dispatched to act on Gatebraid state receives the governing rules verbatim in its mandate — the standing hard-rules block plus the contract sections its task touches — and its report states which rules it was given; work a subagent performed without the rules is treated as unreviewed (friction #97). **No command whose output is an unbounded list of repository or project identifiers**, whatever tool produces it — parent-directory listings, tool-config dumps, workspace enumerations included; a path is confirmed with `test -d "<absolute path>"`, never by listing a parent (friction #91, #97; the closed-set negative check remains the method for identifiers inside the tree).

**Gate 0 — Authority & baseline (read-only).**
*Entry:* frontier verdict says startable; `Executor = Claude Lead`. *Actions:* verify repo identity and remote; record `Base SHA`; record working-tree cleanliness — a dirty tree **stops the gate** and sets `Next Approval = Dirty Baseline Acceptance` (no remediation of any kind, ever); verify `Environment` matches the host; verify tool versions; verify the slice's `gatebraid-metadata` block parses against `gatebraid/slice@1`. *Prohibited:* any write, fetch/pull, branch creation. *Exit:* `gate0.md` evidence; `Gate = G0 passed`; Workflow → `Gate 1 — Planning` (or straight to `Needs Plan Approval` for trivial pre-planned slices — record why).

**Gate 1 — Planning (read-only; temporary team permitted).**
*Entry:* `G0 passed`. *Actions:* read-only exploration; optional Agent Team (≤3 read-only teammates from the plugin's subagent definitions, lead never in bypass mode, findings flushed to the issue before dissolution); produce the plan: approach, exact `write_domains` allowlist, test plan with commands, risk notes, rollback note; complete `gatebraid-gate1-exit-checklist` (BMAD-derived); freeze plan + allowlist (hashes recorded in the evidence file). *Prohibited:* any write to the repo; any dependency installation. *Exit:* `gate1.md` + frozen plan; `Gate = G1 passed`; Workflow → `Needs Plan Approval`; `Next Approval = Plan Approval (G1→G2)`; `needs-human` on. **Human approval comment is the only door to Gate 2.**

**Gate 2 — Implementation (single writer).**
*Entry:* recorded human Plan Approval; `Writer Lease` taken; `Active Branch` created from `Base SHA`. *Actions:* implement strictly inside the frozen allowlist; small frequent commits on `Active Branch` (commits yes, **push no** — publication is Gate 3); run the declared tests; `/goal` permitted only here and only with a turn/time bound inside the condition. *Repair sequence (D6, fixed):* red check → **repair 1 with a new hypothesis** → still red → **Codex consult** (consult file with embedded evidence; response schema; recorded `ACCEPT/PARTIAL/REJECT`) → apply verified fix → still red → **repair 2** → still red → `Human Diagnosis Required`. `repair_limit = 2`; `consult_first: true` moves the consult before repair 1. Mid-slice scope discovery → `gatebraid-correct-course`: stop, document the delta, `Next Approval = Scope / Allowlist Change`, human re-approval re-freezes — never silently widen. *Prohibited:* touching files outside the allowlist; push/PR/merge; `git reset/clean/checkout` against baseline state; installing dependencies not in the approved plan; disabling hooks or checks. *Exit:* tests green per the plan; `gate2.md` evidence with verification outputs; Workflow → `Needs Review`; reviewers (read-only) pass → `Gate = G2 passed`, Workflow → `Needs Release Approval`, `needs-human` on.

**Gate 3 — Publication (human-approved).**
*Entry:* recorded human Release Approval. *Actions:* verify the working tree and staged set match the Gate 2 handoff exactly (any drift → back to `Needs Review`); run the exact publication commands from the approved plan: push `Active Branch`, open the PR (linked to the Slice issue), watch CI, merge per the approval's terms; record PR/merge SHAs. *Prohibited:* force-push; publishing anything beyond the approved set; merging with red CI. *Exit:* `gate3.md` evidence; `Gate = G3 passed`; Workflow → `Done`; close the Slice issue (which is what releases native `blocked-by` dependents); release the `Writer Lease`; set `Next Approval` back to `—`.

---

*Provenance: consolidated from reports 09–12 of the audit series; supersedes the GPT-5.6 proposal for the items above; the proposal remains the source for anything not defined here or in reports 11–12. If the original proposal document resurfaces and differs in naming, this file wins unless a new ADR says otherwise — and ADR-0010 governs all names regardless.*
