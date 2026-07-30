# Manual-view creation checklist — "Mianli Engineering" (12 views)

Companion to `projects/mianli-engineering.md` and spec §3. Name, layout and
filter can be set through GraphQL; **grouping, sorting, visible fields and
`Show hierarchy` have no API input and must be set by hand** in the Project UI
(desktop web), in this order, with these exact settings. A read-only
verification pass then checks every row. The exact UI filter string actually
used is recorded per view in the M1 verification manifest §2.

Conventions: "sort" is the view's sort order; "fields" is the visible-column
set (Title first; add Repository via the built-in repository column). Filters
are stated in field terms; the UI filter bar ANDs qualifiers — where a spec
filter needs OR across different qualifiers this is noted explicitly.

**`Show hierarchy` is normative and is the last column of the table below.**
It defaults to **On**, and that default is wrong for every view except
`By Stage`: with hierarchy on, GitHub nests children under parents, so a queue
view displays the number of *roots* rather than the number of matching items,
and `By Project` renders child items under their *parent's* repository group
instead of their own — defeating the entire point of that view. Verified on the
live Project during M1; see manifest §8.

**Grouping on TEXT fields is available** — verified during M1 for
`Parallel Group` and `Stage`. The non-groupable set is title, labels, reviewers
and linked pull requests.

| # | View | Layout | Filter | Grouping | Sorting | Visible fields | `Show hierarchy` |
|---|---|---|---|---|---|---|---|
| 1 | **Needs Me** | Table | `Next Approval` is set and ≠ `—`. ⚠ Spec definition is `Next Approval ≠ —` **OR** label `needs-human`; if the filter bar cannot express OR across qualifiers, use the `Next Approval` clause as primary and record the gap (a `Blocked`+`needs_input` row carries the label but no pending approval; it remains visible in **Blocked**) in manifest §8 | none | `Risk` desc, then oldest first (created asc) | Title, `Next Approval`, `Workflow`, `Risk`, `Slice`, Repository, `Last Checkpoint` | **Off** |
| 2 | **Ready Frontier** | Table | `Workflow = Backlog`, open issues only | `Parallel Group` | `Slice` asc | Title, `Slice`, `Stage`, `Phase`, `Parallel Group`, `Risk`, `Environment`, Repository | **Off** |
| 3 | **Active** | Board — column field `Workflow` | `Workflow` ∈ {`Gate 0 — Verifying`, `Gate 1 — Planning`, `Gate 2 — Implementing`, `Gate 3 — Releasing`} | by `Workflow` (columns) | board default | Card: `Slice`, Repository, `Executor`, `Writer Lease`, `Active Branch` | n/a (board) |
| 4 | **Planning** | Table | `Workflow` ∈ {`Gate 0 — Verifying`, `Gate 1 — Planning`, `Needs Plan Approval`} | none | `Workflow` asc, then `Slice` asc | Title, `Workflow`, `Slice`, `Stage`, `Phase`, `Executor`, `Next Approval` | **Off** |
| 5 | **Codex Consultations** | Table | `Workflow = Codex Consultation` | none | `Last Checkpoint` desc | Title, `Slice`, Repository, `Executor`, `Risk`, `Last Checkpoint` (consult artifact links live in issue comments/evidence) | **Off** |
| 6 | **Review Queue** | Table | `Workflow = Needs Review` | none | `Risk` desc, oldest first | Title, `Slice`, Repository, `Risk`, `Active Branch`, `Last Checkpoint` | **Off** |
| 7 | **Repair Queue** | Table | `Workflow` ∈ {`Repair Required`, `Human Diagnosis Required`} | none | `Risk` desc | Title, `Workflow`, `Slice`, Repository, `Risk`, `Last Checkpoint` | **Off** |
| 8 | **Blocked** | Table | `Workflow = Blocked` | none | oldest first | Title, `Slice`, Repository, `Workflow`, `Last Checkpoint` (native Blocked indicator renders on the item; typed reason in latest comment) | **Off** |
| 9 | **Release Queue** | Table | `Workflow` ∈ {`Needs Release Approval`, `Gate 3 — Releasing`} | none | `Workflow` asc | Title, `Workflow`, `Slice`, Repository, `Active Branch`, `Base SHA` | **Off** |
| 10 | **By Project** | Table | open items | Repository | `Slice` asc | Title, `Workflow`, `Gate`, `Slice`, `Writer Lease`, `Executor` | **Off** |
| 11 | **By Stage** | Table (roadmap layout optional later) | all items | `Stage` | `Phase` asc, `Slice` asc | Title, `Workflow`, `Gate`, `Stage`, `Phase`, `Slice` | **On** — the structural view |
| 12 | **All Work** | Table | none (include closed) | none | oldest first | **All 14 custom fields** + Title + Repository + State | **Off** |

Verification pass (read-only, after creation): for each view confirm — exact
name · layout · filter behaviour against the sample hierarchy · grouping · sort
· visible fields · `Show hierarchy`. Record per-view results in manifest §2.

Behavioural expectations against the M1 sample (one Stage, one Phase, four
Backlog slices), with `Show hierarchy` set as specified above:

- **Ready Frontier** shows exactly the four Backlog slices — container nodes
  carry no `Workflow` and are correctly absent.
- **Active** and every other `Workflow`-filtered queue are empty.
- **Blocked** is empty *even though one slice carries GitHub's native blocked-by
  badge* — native dependency state and the `Workflow` field are independent
  surfaces, which is the observable form of ADR-0008. A natively blocked item
  appearing here would be a real finding.
- **By Project** shows every open item grouped by its own repository — only true
  with hierarchy off.
- **Needs Me** is **not** empty merely because no approval is pending. Measured
  in M1: `-next-approval:"—"` also matches items whose `Next Approval` has no
  value, so container nodes surface there. Known defect, recorded in manifest
  §8, carried to M2; do not paper over it by writing `—` onto containers.
