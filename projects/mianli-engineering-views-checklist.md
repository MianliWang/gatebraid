# Manual-view creation checklist — "Mianli Engineering" (12 views)

Companion to `projects/mianli-engineering.md` and spec §3. Used when the
connected GitHub connector/authentication path cannot create user-owned
Project views: the operator / ChatGPT Work creates each view below in the
Project UI (desktop web), in this order, with these exact settings; a
read-only verification pass then checks every row. The exact UI filter string
actually used is recorded per view in the M1 verification manifest §2.

Conventions: "sort" is the view's sort order; "fields" is the visible-column
set (Title first; add Repository via the built-in repository column). Filters
are stated in field terms; the UI filter bar ANDs qualifiers — where a spec
filter needs OR across different qualifiers this is noted explicitly.

| # | View | Layout | Filter | Grouping | Sorting | Visible fields |
|---|---|---|---|---|---|---|
| 1 | **Needs Me** | Table | `Next Approval` is set and ≠ `—`. ⚠ Spec definition is `Next Approval ≠ —` **OR** label `needs-human`; if the filter bar cannot express OR across qualifiers, use the `Next Approval` clause as primary and record the gap (a `Blocked`+`needs_input` row carries the label but no pending approval; it remains visible in **Blocked**) in manifest §8 | none | `Risk` desc, then oldest first (created asc) | Title, `Next Approval`, `Workflow`, `Risk`, `Slice`, Repository, `Last Checkpoint` |
| 2 | **Ready Frontier** | Table | `Workflow = Backlog`, open issues only | `Parallel Group` | `Slice` asc | Title, `Slice`, `Stage`, `Phase`, `Parallel Group`, `Risk`, `Environment`, Repository |
| 3 | **Active** | Board — column field `Workflow` | `Workflow` ∈ {`Gate 0 — Verifying`, `Gate 1 — Planning`, `Gate 2 — Implementing`, `Gate 3 — Releasing`} | by `Workflow` (columns) | board default | Card: `Slice`, Repository, `Executor`, `Writer Lease`, `Active Branch` |
| 4 | **Planning** | Table | `Workflow` ∈ {`Gate 0 — Verifying`, `Gate 1 — Planning`, `Needs Plan Approval`} | none | `Workflow` asc, then `Slice` asc | Title, `Workflow`, `Slice`, `Stage`, `Phase`, `Executor`, `Next Approval` |
| 5 | **Codex Consultations** | Table | `Workflow = Codex Consultation` | none | `Last Checkpoint` desc | Title, `Slice`, Repository, `Executor`, `Risk`, `Last Checkpoint` (consult artifact links live in issue comments/evidence) |
| 6 | **Review Queue** | Table | `Workflow = Needs Review` | none | `Risk` desc, oldest first | Title, `Slice`, Repository, `Risk`, `Active Branch`, `Last Checkpoint` |
| 7 | **Repair Queue** | Table | `Workflow` ∈ {`Repair Required`, `Human Diagnosis Required`} | none | `Risk` desc | Title, `Workflow`, `Slice`, Repository, `Risk`, `Last Checkpoint` |
| 8 | **Blocked** | Table | `Workflow = Blocked` | none | oldest first | Title, `Slice`, Repository, `Workflow`, `Last Checkpoint` (native Blocked indicator renders on the item; typed reason in latest comment) |
| 9 | **Release Queue** | Table | `Workflow` ∈ {`Needs Release Approval`, `Gate 3 — Releasing`} | none | `Workflow` asc | Title, `Workflow`, `Slice`, Repository, `Active Branch`, `Base SHA` |
| 10 | **By Project** | Table | open items | Repository | `Slice` asc | Title, `Workflow`, `Gate`, `Slice`, `Writer Lease`, `Executor` |
| 11 | **By Stage** | Table (roadmap layout optional later) | all items | `Stage` | `Phase` asc, `Slice` asc | Title, `Workflow`, `Gate`, `Stage`, `Phase`, `Slice` |
| 12 | **All Work** | Table | none (include closed) | none | oldest first | **All 14 custom fields** + Title + Repository + State |

Verification pass (read-only, after creation): for each view confirm — exact
name · layout · filter behavior against the sample hierarchy (e.g. Ready
Frontier shows exactly the four Backlog slices; Active is empty; Needs Me is
empty until an approval is pending) · grouping · sort · visible fields. Record
per-view results in manifest §2.
