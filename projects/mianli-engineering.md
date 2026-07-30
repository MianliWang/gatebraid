# GitHub Project configuration — "Mianli Engineering"

**Normative record** of the private user-level GitHub Project that is the
Gatebraid portfolio board (name unchanged per ADR-0010 Part II, unchanged
names). The board is a
**view and state surface** over issues; authorities are per ADR-0001. This
document is what the live Project is verified against; any drift is corrected
toward this document (or this document is changed by ADR).

- **Owner:** user `MianliWang` (user-level Project, not repo-level)
- **Visibility:** Private
- **Verified limits (report 12 §3):** 50 options per single-select; 50 fields
  per Project including system fields. The 13-option Workflow and 14 custom
  fields fit with headroom. If any limit is hit anyway: stop and report; do
  not improvise.

## Custom fields — exactly 14

| # | Field | Type | Options (in order) |
|---|---|---|---|
| 1 | `Workflow` | single-select | `Backlog` · `Gate 0 — Verifying` · `Gate 1 — Planning` · `Needs Plan Approval` · `Gate 2 — Implementing` · `Needs Review` · `Repair Required` · `Codex Consultation` · `Human Diagnosis Required` · `Blocked` · `Needs Release Approval` · `Gate 3 — Releasing` · `Done` (13) |
| 2 | `Gate` | single-select | `—` · `G0 passed` · `G1 passed` · `G2 passed` · `G3 passed` (5) |
| 3 | `Executor` | single-select | `Human` · `Claude Lead` · `Claude Read-Only Team` · `Codex Consultant` · `Cowork Coordinator` (5) |
| 4 | `Next Approval` | single-select | `—` · `Plan Approval (G1→G2)` · `Release Approval (G2→G3)` · `Dirty Baseline Acceptance` · `Scope / Allowlist Change` · `Environment Change` · `Session Persistence` · `Worktree Exception` · `Human Diagnosis` (9) |
| 5 | `Environment` | single-select | `wsl` · `windows` · `macos-authority` · `mixed-see-prose` (4) |
| 6 | `Risk` | single-select | `low` · `medium` · `high` (3) |
| 7 | `Stage` | text | e.g. `S1` |
| 8 | `Phase` | text | e.g. `P1` |
| 9 | `Slice` | text | e.g. `P1-S1` |
| 10 | `Base SHA` | text | |
| 11 | `Active Branch` | text | |
| 12 | `Parallel Group` | text | |
| 13 | `Writer Lease` | text | `<host>:<session-label>:<ISO8601>` or empty |
| 14 | `Last Checkpoint` | text | ISO8601 + one-line note |

## Views — exactly 12 (definitions: spec §3)

Needs Me · Ready Frontier · Active (board by `Workflow`) · Planning · Codex
Consultations · Review Queue · Repair Queue · Blocked · Release Queue ·
By Project · By Stage · All Work.

Full filter/layout definitions are normative in
`protocols/gatebraid-control-plane-spec-v1.md` §3 and are not duplicated here.

## Setup method (M1)

Fields and options are created through the GitHub connector / structured API.
**All twelve views are M1 acceptance requirements.**

**Finding of record (M1 execution, 2026-07-30 — replaces the anticipated
conditional this section previously carried).** On the authenticated `gh`/GraphQL
path actually used, view management is *partially* available:

- `gh` 2.96.0 exposes **no** view-management subcommand (`gh project view`
  displays a project; it does not manage views).
- GraphQL **does** expose `createProjectV2View` / `updateProjectV2View` /
  `deleteProjectV2View`. Create takes `projectId`, `name`, `layout`; update
  additionally takes `filter`.
- **No API input exists for grouping, sorting, visible fields, or
  `Show hierarchy`.** Those four are UI-only.

So views are created programmatically as name + layout + filter, and the rest is
configured by hand from
`projects/mianli-engineering-views-checklist.md`; work **pauses** until all
twelve exist and are configured, and a read-only verification pass then checks
every attribute the API can read. Views are never downgraded to
documentation-only. Any further element this path cannot express is stopped on
and recorded in the M1 verification manifest — never improvised.

## Membership rule (M1)

Only issues from `MianliWang/gatebraid` and `MianliWang/gatebraid-scratch` are
added in M1. **No business repository, its issues, or an auto-add rule naming
one may appear in this Project until a milestone explicitly authorizes it.**
