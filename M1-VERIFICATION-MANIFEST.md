# M1 verification manifest — Gatebraid control plane and specification

**Milestone:** M1 (Gatebraid Classic, profile id `classic`) · **Status:**
**COMPLETE** — every `TBD(batch N)` placeholder has been filled by an approved
mutation batch and none remain. Outside this paragraph the string `TBD` appears
exactly twice, and neither is a placeholder: the §2 clause defining when view
items may leave that state, and the §8 catch-all that keeps the deviations record
open to whatever a later batch hits. Nothing in this document is awaiting a
value.

The milestone ends with the draft PR **unmerged**; merging it is a separate
decision recorded in §10, and does not change any statement made here.
**Authority:** M1 tasking (Gatebraid edition, 2026-07-28) + operator M1 execution approval (2026-07-29). ADR-0010 governs names; report 12 overrides earlier documents where they conflict; report 11 D1–D8 in force.

## 1. What was created

| Item | Value |
|---|---|
| Control repository | `MianliWang/gatebraid` (private). Recon 2026-07-29 (RB-1): exists as **`MianliWang/Gatebraid`**, repo id **1315713271**, private ✓, unarchived ✓, default `main`, sole commit `53dc6a6` (README + Apache-2.0 LICENSE; operator-created). Former name `mianli-control`: **404** — no duplicate-identity conflict. **Batch 1 (RB-2; operator-approved, casing Option A):** case-only rename `Gatebraid`→`gatebraid` executed (`gh repo rename`, exit 0); final `full_name` verified exactly `MianliWang/gatebraid`; pre-existing repo, case C1 — no bootstrap |
| Scratch repository | `MianliWang/gatebraid-scratch` (private) — reused authoritative repository ID **1315376699**. Recon 2026-07-29 (RB-1): currently **`MianliWang/classic-scratch`** (former name; private ✓, unarchived ✓, default `main`; same id confirmed by direct former-name probe). **Batch 1 (RB-2):** renamed `classic-scratch`→`gatebraid-scratch` (`gh repo rename`, exit 0), id preserved; redirect verified — the former name resolves to the same id under the official name |
| Branch | `m1-control-plane` — **created (RB-2)** @ `53dc6a6543213b76bce4d694d74d5c11bf244d97` (= `main` head, API `POST git/refs`); verified present alongside `main` |
| Draft PR | **#1 — https://github.com/MianliWang/gatebraid/pull/1** (RB-3): `isDraft:true`, `state:OPEN`, `changedFiles:40`, base `main` ← head `m1-control-plane`; commit `364ef3097b15c3e7b61245c830dfd3dc22d65df7` (40 files, 1793 insertions; explicit `git add` of the 8 top-level paths, never `-A`; step-5 status showed exactly 40 "A " entries, LICENSE/README untouched). Committed-tree negative check: `git grep` for business-repo names on HEAD → no matches. **Left unmerged** |
| GitHub Project | **#1 — https://github.com/users/MianliWang/projects/1** (pre-existing, created during the M0 probe; discovered at RB-4a), private ✓ (`public:false`), not closed. Carried one pre-existing custom field (`Workflow`, 1 option) and one item (the M0 probe issue) — see §8. **Configuration complete (RB-4b/4c):** 14 custom fields verified option-by-option; 12 views created, configured and read-back-verified (11/12 conforming, 1 sort deviation) — §2. Project id `PVT_kwHOBRofUs4Beum7` |
| Committed tree | `adr/` (ADR-0001…0010 — the complete approved M1 ADR set; no eleventh ADR exists) · `protocols/` (spec + 4 gate contracts) · `schema/` (7 × `gatebraid/*@1`) · `templates/` (12) · `projects/` (3, incl. the manual-view creation checklist) · `evidence/sanitized/` · `NOTICE.md` · this manifest — **40 files** |

## 2. Project configuration result

- **Fields created (Batch 3b, RB-4b pt.1):** the 13 missing fields created in
  spec order, all exit 0 — `Gate` created first as a deliberate **encoding
  probe** (leading em-dash option) and verified back intact (U+2014, U+2192
  character-exact) before the batch continued. Option lists verified
  option-by-option against `projects/mianli-engineering.md`: Gate 5 ·
  Executor 5 · Next Approval 9 · Environment 4 · Risk 3; 8 TEXT fields.
  `dataType` confirmed separately via read-only GraphQL (because
  `gh project field-list` reports TEXT/NUMBER/DATE alike as
  `ProjectV2Field`): 6 SINGLE_SELECT + 8 TEXT. Custom-field count now 14;
  13 system + 14 custom = 27 of the 50 cap. Pre-existing `Workflow` and its
  option `2ad6af85` untouched by the host. **Workflow completed (RB-4b pt.2;
  operator UI, remedy option 3):** 13 options, character-exact, in spec order
  — double-checked by diff against the expected list (13/13) and against the
  committed `projects/mianli-engineering.md` (13/13), plus an `od -tx1`
  byte-level check on all four "Gate N — X" options (U+2014 em-dash, single
  spaces, no hyphen 0x2d, no en-dash); field id
  `PVTSSF_lAHOBRofUs4Beum7zhZGqt0` unchanged (extended, not recreated);
  option id `2ad6af85` still backs `Needs Plan Approval`, now in position 4;
  the M0 probe item still shows `Workflow = Needs Plan Approval`. Final
  roster: 13 system + 14 custom = 27 fields in spec order, under the caps.
  **The 14 fields exist and are verified option-by-option — this item is
  complete.**
- **Views — M1 acceptance requirement (all twelve must exist and be checked,
  including grouping, sorting, and visible fields).**
  **Actual finding (RB-4a) — supersedes the anticipated wording, which was
  factually wrong on this host:** `gh` 2.96.0 exposes **no view-management
  subcommand** (`gh project view` displays a project; it does not manage
  views). GraphQL on this authenticated path **does** expose
  `createProjectV2View` / `updateProjectV2View` / `deleteProjectV2View` —
  introspected inputs: Create takes `projectId!, name!, layout!`; Update takes
  `viewId, name, layout, filter`. **No API input exists for grouping,
  sorting, or visible-field configuration.** Views can therefore be
  API-created with name + layout (and filter via update) but cannot be fully
  configured; because the checklist makes grouping/sorting/visible fields
  acceptance criteria for all 12 views, manual UI configuration remains
  required.
  Procedure (execution-time; operator decisions recorded at RB-4b/4c):
  1. Fields and options through `gh` (Batch 3/3b).
  2. Views completed per `projects/mianli-engineering-views-checklist.md` by
     the operator / ChatGPT Work — API-assisted creation of name/layout/filter
     is permitted only under a separately approved batch.
  3. **Pause** until all twelve exist and are fully configured.
  4. Read-only verification pass of all twelve against the checklist.
  5. Only then may this manifest's view items leave TBD. **This manifest is
     not complete until all twelve views actually exist and are checked.**
  Views are never downgraded to a documentation-only deliverable.
  Wording note: the committed `projects/mianli-engineering.md` and the views
  checklist phrase this as the anticipated conditional ("may not support
  creation…"); this manifest records the actual finding. A precise-wording
  amendment to those two committed files may be folded into the final
  manifest commit on operator approval.
- Preflight pre-confirmation (RB-1; `gh` 2.96.0): `gh project` exposes **no
  view-creation subcommand** — consistent with the narrow finding above;
  formal verbatim record at Batch 3.
- **View creation record (Batch 3c, host GraphQL):** all twelve views created
  with name + layout, filters applied via `updateProjectV2View` — the only
  three attributes the API accepts.
- **View configuration (operator UI pass, 2026-07-29 → 2026-07-30):** Fields /
  Group by / Sort set per view following the host-delivered UI guide; each view
  saved with **Save to current view**.
- **Read-only verification (RB-4c, 2026-07-30; GraphQL `projectV2.views` +
  `fields` + `items`):** project id `PVT_kwHOBRofUs4Beum7`, user `MianliWang`
  #1, private ✓, open ✓. `views.totalCount = 13` at RB-4c — the twelve spec
  views plus the pre-existing default `View 1`, which Batch 3d subsequently
  deleted (RB-4d), leaving **12**. View names compared
  code-point by code-point against
  `projects/mianli-engineering-views-checklist.md`: **12/12 character-exact**,
  no homoglyph substitution. Per-view verdict at RB-4c — layout, filter,
  group-by, sort and visible-field set: 11 of 12 conforming, 1 deviation
  (`By Project` sort). That deviation was closed in the UI and confirmed at
  **RB-4f: 12/12 conforming — final** (table below).
  `All Work` carries 17 columns and all **14** custom fields were
  independently enumerated as present (Workflow · Gate · Executor · Next
  Approval · Environment · Risk · Stage · Phase · Slice · Base SHA · Active
  Branch · Parallel Group · Writer Lease · Last Checkpoint). Spec's `State`
  column is carried by the system field `Closed` — the Project has no field
  literally named `State`; naming note, not a deviation. `By Stage` confirmed
  to carry `Parent issue` + `Sub-issues progress`. `Active` confirmed
  `BOARD_LAYOUT` with column field `Workflow`.
  Persistence evidence: all twelve `createdAt` 2026-07-29 13:41,
  `updatedAt` 2026-07-30 04:03–04:28 — configuration is server-side; the
  "configure, navigate away, lose everything" failure mode did not occur.
- **Exact filter strings, byte-for-byte from the API (RB-4c):**

  | # | View | Filter |
  |---|---|---|
  | 2 | Needs Me | `-next-approval:"—"` |
  | 3 | Ready Frontier | `workflow:Backlog is:open` |
  | 4 | Active | `workflow:"Gate 0 — Verifying","Gate 1 — Planning","Gate 2 — Implementing","Gate 3 — Releasing"` |
  | 5 | Planning | `workflow:"Gate 0 — Verifying","Gate 1 — Planning","Needs Plan Approval"` |
  | 6 | Codex Consultations | `workflow:"Codex Consultation"` |
  | 7 | Review Queue | `workflow:"Needs Review"` |
  | 8 | Repair Queue | `workflow:"Repair Required","Human Diagnosis Required"` |
  | 9 | Blocked | `workflow:Blocked` |
  | 10 | Release Queue | `workflow:"Needs Release Approval","Gate 3 — Releasing"` |
  | 11 | By Project | `is:open` |
  | 12 | By Stage | *(empty)* |
  | 13 | All Work | *(empty — includes closed items, as specified)* |

  Em-dash integrity: every dash inside views 2/4/5/10 is **U+2014**, the same
  code point as the four `Gate N — X` Workflow options and the `—` options of
  `Gate` / `Next Approval`. No en-dash or hyphen contamination anywhere in the
  filter set.
- **Final view verification table — RB-4f, 2026-07-30T07:12:28Z. 12/12
  conforming.** Layout / filter / group-by / sort compared by exact equality
  (filters constructed with U+2014, so a pass also proves dash code-point
  identity); visible fields compared as sets. Checklist row number and GitHub
  view `number` differ by a fixed +1 offset — see §8.

  | Row | View | GH # | Layout | Group by | Sort | Fields |
  |---|---|---|---|---|---|---|
  | 1 | Needs Me | 2 | Table | none | Risk DESC → Created ASC | 7/7 |
  | 2 | Ready Frontier | 3 | Table | Parallel Group | Slice ASC | 8/8 |
  | 3 | Active | 4 | **Board**, column field `Workflow` | — | board default | 6/6 |
  | 4 | Planning | 5 | Table | none | Workflow ASC → Slice ASC | 7/7 |
  | 5 | Codex Consultations | 6 | Table | none | Last Checkpoint DESC | 6/6 |
  | 6 | Review Queue | 7 | Table | none | Risk DESC → Created ASC | 6/6 |
  | 7 | Repair Queue | 8 | Table | none | Risk DESC | 6/6 |
  | 8 | Blocked | 9 | Table | none | Created ASC | 5/5 |
  | 9 | Release Queue | 10 | Table | none | Workflow ASC | 6/6 |
  | 10 | By Project | 11 | Table | Repository | Slice ASC | 6/6 |
  | 11 | By Stage | 12 | Table | Stage | Phase ASC → Slice ASC | 8/8 |
  | 12 | All Work | 13 | Table | none | Created ASC | 17/17 |

  `views.totalCount = 12`; no view numbered 1 exists; all twelve ids and names
  identical to the RB-4d post-deletion snapshot — no rebuild, no id drift.
  Persistence: eleven views last written 2026-07-30 04:03–04:28 (the UI pass),
  `By Project` 07:08:14Z (the sort correction). Server-side `updatedAt` proves
  the earlier `[Repository ASC]` readings were a genuine ordering artefact —
  three reads that preceded the operator's save — and **not** an API read-back
  defect and not a configuration error.
- **Grouping and sorting are independent (RB-4f).** After the correction
  `By Project` reports `sortByFields = [Slice ASC]` **only** — the previous
  `Repository ASC` was replaced, not appended. Grouping by `Repository` neither
  produces nor requires a `Repository` sort entry; the earlier value was the
  UI's default sort seed. Setting a sort replaces rather than extends.
- **Elements this path cannot express or read back (RB-4c, reaffirmed at
  RB-4f) — recorded, not worked around. Any claim that "the views are fully
  verified" must carry these three qualifiers:**
  1. **Column order** — UI-only. `visibleFields` returns in Project
     field-definition order for all 13 views, i.e. the API normalises order
     and does not reflect the UI. Verification therefore asserts *set*
     conformance, never order.
  2. **Board column rendering** — UI-only. The API exposes
     `layout = BOARD_LAYOUT` and the column field, but not which of the 13
     `Workflow` options render as columns. `Active` showing exactly the four
     Gate columns is an operator visual finding, accepted but not
     independently reproduced.
  3. **Filter evaluation** — GraphQL offers no "items matching this view's
     filter" query. Filter *strings* are verified character-exact; **which and
     how many rows a view actually shows is not verified**. Behavioural
     verification was carried out at Batch 4 against the sample hierarchy — see
     the measured table in §6.1.
  4. **`Show hierarchy`** — UI-only, and consequential: it changes what a row
     count *means*, and it defeats `By Project`'s repository grouping. Not
     exposed by the API, never specified by the checklist, and therefore left at
     GitHub's default until the Batch-4 read exposed it. See §8.

## 3. Sample hierarchy (exact)

**Created and verified — Batch 4, RB-5, 2026-07-30.** Actual issue numbers match
the RB-4a forecast exactly.

| Item | Issue | Repo | Title | Sub-issue of |
|---|---|---|---|---|
| Stage 1 | **#2** | `gatebraid` | Stage S1 — Control-plane validation | — |
| Phase 1 | **#3** | `gatebraid` | Phase P1 — Sample hierarchy and dependency encoding | Stage 1 |
| Slice A `P1-S1` | **#2** | `gatebraid-scratch` | P1-S1 — Define the shared interface | Phase 1 (cross-repo) |
| Slice B `P1-S2` | **#3** | `gatebraid-scratch` | P1-S2 — Build on the interface A fixes at Gate 1 | Phase 1 (cross-repo) |
| Slice C `P1-S3` | **#4** | `gatebraid-scratch` | P1-S3 — Consume A's released output | Phase 1 (cross-repo) |
| Slice D `P1-S4` | **#5** | `gatebraid-scratch` | P1-S4 — Integrate B and C | Phase 1 (cross-repo) |

Hierarchy read back: `gatebraid#2` has exactly one sub-issue (`gatebraid#3`);
`gatebraid#3` has `parent = gatebraid#2` and exactly four sub-issues, all four in
`gatebraid-scratch`. **Cross-repository sub-issues are therefore exercised and
confirmed working**, as report 11 predicted. Every `## gatebraid-metadata` block
was schema-validated before creation and re-extracted from GitHub's stored body
and re-validated after — 0 errors on all six (`gatebraid/stage@1`,
`gatebraid/phase@1`, `gatebraid/slice@1` ×4).

All six added to the Project, with fields set **by node kind** (operator
correction, 2026-07-29):

- **Slices A–D:** `Workflow = Backlog` · `Gate = —` · **`Next Approval = —`** ·
  `Stage = S1` · `Phase = P1` · `Slice = P1-S1…P1-S4` · `Environment = wsl` ·
  `Risk = low` · `Executor = Cowork Coordinator` (M1 setup only).
  `Next Approval = —` is set **explicitly**, not left unset: `—` is the
  designed resting value ("no human decision pending"), exactly as `Gate = —`
  is, and the `Needs Me` filter is written against it (§8, spec-wording
  entry). A Backlog slice has no pending approval, so `—` is its correct
  value from creation.
- **Stage S1 and Phase P1: `Workflow` and `Gate` are left EMPTY.** Those two
  fields are per-Slice by definition (spec §1–§2); setting `Backlog` on a
  container node would wrongly place it in the Ready Frontier candidate pool.
  Only the `Stage` (and, for P1, `Phase`) text fields are set. Container
  status is **derived** from children — sub-issue progress + the children's
  own `Workflow`/`Gate` — consistent with the "no stored `Ready` state"
  design note.
- Display consequence: the **By Stage** view is the structural/tree view; its
  visible fields include `Parent issue` and the system **Sub-issues progress**
  column, so Phase rows show roll-up progress beside their Slice rows. Known
  limitation recorded: sub-issue progress counts *closed* children, and a
  Slice closes only at Gate 3 — a Phase whose slices are all mid-Gate-2 reads
  0/N. The children's `Workflow` values in the same group are the compensating
  signal.

**Actual field-set record — RB-5, read back item by item:**

| Field | S1 `gatebraid#2` | P1 `gatebraid#3` | A `#2` | B `#3` | C `#4` | D `#5` |
|---|---|---|---|---|---|---|
| Workflow | *unset* | *unset* | Backlog | Backlog | Backlog | Backlog |
| Gate | *unset* | *unset* | — | — | — | — |
| Next Approval | *unset* | *unset* | — | — | — | — |
| Executor | *unset* | *unset* | Cowork Coordinator | Cowork Coordinator | Cowork Coordinator | Cowork Coordinator |
| Environment | *unset* | *unset* | wsl | wsl | wsl | wsl |
| Risk | *unset* | *unset* | low | low | low | low |
| Stage | S1 | S1 | S1 | S1 | S1 | S1 |
| Phase | *unset* | P1 | P1 | P1 | P1 | P1 |
| Slice | *unset* | *unset* | P1-S1 | P1-S2 | P1-S3 | P1-S4 |
| Base SHA · Active Branch · Parallel Group · Writer Lease · Last Checkpoint | *unset* | *unset* | *unset* | *unset* | *unset* | *unset* |

Container assertion verified at the storage layer: S1 and P1 have **no
`fieldValue` record at all** for `Workflow` / `Gate` / `Next Approval` — genuinely
unset, not set to `—`. That distinction is what makes the §6.1 probe meaningful.
Option-id precheck before writing: `Cowork Coordinator` = `01c6f861`, `Next
Approval —` = `450ee130`, `Gate —` = `39696bb5`; no approximate value was used.
Code-point audit of every stored dash (4 × Gate, 4 × Next Approval, 6 × titles):
**U+2014 throughout, no exceptions**.

**Labels — created only in `gatebraid-scratch` (RB-5, Gate 4A):**

| Label | Colour | Description | Provenance |
|---|---|---|---|
| `needs-human` | `D4C5F9` | Requires human attention | M0; **untouched** — colour and description verified byte-identical after the batch |
| `strict-gate` | `B60205` | Strict Gate slice: mandatory pre-release adversarial review (ADR-0004). | created; description grounded in ADR-0004 |
| `security-sensitive` | `D93F0B` | Security-sensitive diff: mandatory Codex consult trigger (ADR-0004). | created; description grounded in ADR-0004 |
| `scientific-evidence` | `0E8A16` | Scientific-evidence slice: evidence artifacts require preservation. | created; description is a host drafting choice with no in-tree authority — see §8 |

The control repository `gatebraid` received **no** labels (still only GitHub's
nine repository defaults). See §8 for the criterion-wording correction about
those defaults.

## 4. Dependency encodings (exact; ADR-0007)

| Dependency | `## gatebraid-metadata` block (read back) | Native blocked-by (read back) | Verified |
|---|---|---|---|
| B requires A **Gate 1** | `issue: MianliWang/gatebraid-scratch#2` · `requires_gate: 1` (1 entry) | **none** — B `blocked_by=[]`, `blocking=[]` | ✅ RB-5 — metadata only |
| C requires A **Gate 3** | `issue: MianliWang/gatebraid-scratch#2` · `requires_gate: 3` (1 entry) | **C blocked-by #2 (= A)** | ✅ RB-5 — metadata **and** native |
| D requires B **Gate 2** and C **Gate 2** | `#3 requires_gate: 2` + `#4 requires_gate: 2` (2 entries) | **none** — D `blocked_by=[]`, `blocking=[]` | ✅ RB-5 — metadata only |

`requires_gate` values are stored as integers, matching the schema enum
`[1, 2, 3]`. Both directions were queried (`blocked_by` and `blocking`), because
checking only one would miss the reverse edge: **total native edges in the whole
graph = 1**. A's `blocking = [C]` is that same single edge seen from the other
end, not a second dependency.

**What the sample proves.** D has *two* predecessors and *zero* native edges,
while C has *one* predecessor and *one* native edge. Predecessor count therefore
has no bearing on the native/metadata choice — only the required gate does,
exactly as ADR-0007 asserts. This is the control experiment the sample exists
for, and it holds.

**Not exercised by this sample:** all four dependency edges are
`gatebraid-scratch` → `gatebraid-scratch`, so **cross-repository native
`blocked-by` is not tested here**. It was confirmed available (GitHub staff
statement, community discussion #165749) but not demonstrated on this
installation. Recorded as an M2 verification item, not an M1 claim.

## 5. Expected frontier — manually derived (M1 claims NO automatic calculation)

Initial state: all four Slices `Workflow = Backlog`, `Gate = —`, all issues open.
**Confirmed as the actual state at RB-5** (§3 field table), so the derivation
below describes the system as it really stands, not a hypothetical.

| Slice | Dependencies | Native badge | Manually derived verdict |
|---|---|---|---|
| A | none | none | **Ready for Gate 0** — the only startable slice |
| B | A ≥ `G1 passed` (metadata) | none | Not ready until A's `Gate` ∈ {G1,G2,G3 passed} |
| C | A ≥ `G3 passed` (metadata + native) | **Blocked** (by A, open) | Not ready until A closes (= `G3 passed`, ADR-0007 invariant) |
| D | B ≥ `G2 passed` and C ≥ `G2 passed` (metadata) | none | Not ready until both hold; **no native badge by design** |

Progression check (derived by hand): A `G1 passed` → B becomes startable while
C stays natively Blocked and D stays waiting — soft vs hard encoding visibly
diverges, which is the ADR-0007 behavior under test.

## 6. How the Ready Frontier view reads

The view filters `Workflow = Backlog` (open issues, grouped by
`Parallel Group`), so it shows **all four** slices as the candidate pool —
including B, C, D, which are not startable. This is correct by design: the
view never claims startability (spec, design note); the verdict above is
manual in M1, the `next` skill's job in M2, and `gatebraid-frontier`'s job in
M3. On the phone, C additionally shows GitHub's native Blocked indicator; B
and D do not — soft dependencies are invisible to the native UI by design
(ADR-0007 accepted consequence).

### 6.1 Expected view contents immediately after Batch 4 — manually derived

Derived by hand from §3 (field sets by node kind) and §2 (verbatim filters),
with the pre-existing M0 probe item archived out of the Project.
This table is the RB-5 acceptance baseline; a view that disagrees is a finding,
not a rounding error.

**Measured 2026-07-30 after Batch 4, operator UI read: every row matches.**
The first reading did not — it showed 1 row nearly everywhere — because
`Show hierarchy` was On and GitHub was collapsing P1 into S1 and A–D into P1,
so the visible count was the number of *roots*, not of matching items. The
expected-row column below is therefore only meaningful with `Show hierarchy`
**Off**; see §8 for the specification gap that allowed the default through.

| View | Expected rows | Measured | Derivation |
|---|---|---|---|
| Ready Frontier | **4** — A, B, C, D | ✅ 4 | `workflow:Backlog is:open`; containers carry no `Workflow`, so S1/P1 are excluded — this is exactly why §3 leaves container `Workflow` empty |
| Active | **0** | ✅ 0 | no slice has reached a Gate-N Workflow value |
| Planning | **0** | ✅ 0 | no item is `Gate 0/1` or `Needs Plan Approval` |
| Codex Consultations / Review Queue / Repair Queue / Blocked / Release Queue | **0** each | ✅ 0 each | no matching `Workflow` value exists yet |
| By Project | **6** — grouped `gatebraid` (2) / `gatebraid-scratch` (4) | ✅ 6, both groups | `is:open`, all six open |
| By Stage | root S1, expanding to P1 → A–D | ✅ | no filter; `Show hierarchy` **On** — this is the structural view |
| All Work | **6** | ✅ 6 | no filter |
| Needs Me | **0 or 2 — an empirical probe** | **2 (S1, P1)** | Slices A–D carry `Next Approval = —`; containers S1/P1 carry no value |

**`Blocked` reading 0 is a load-bearing observation, not a trivial zero.** C
carries GitHub's native blocked-by badge, yet does not appear in the `Blocked`
view, whose filter is `workflow:Blocked`. Native dependency state and the
`Workflow` field are therefore genuinely independent surfaces — a direct
confirmation of ADR-0008's claim that `Workflow` is the sole state authority and
that the native badge is decoration, not state. Had C appeared here, ADR-0008
would have needed revisiting.

**Correction to a coordinator-authored expected value.** The host UI guide's
post-Batch-4 self-check stated "`Needs Me` should show exactly 1 row (B)". That
is **wrong and is hereby superseded**: no Batch-4 item has a pending approval,
so no derivation yields one row.

The correct expectation is conditional on GitHub's negation semantics over
empty values, which §8 records as not machine-checkable. Because §3 now sets
`Next Approval = —` explicitly on the four slices, the two container nodes are
the only items with an empty value, which narrows the probe:

- `Needs Me` reads **0 rows** → `-next-approval:"—"` excludes empty values. The
  filter matches the spec's "is set and ≠ —" for every item that participates
  in the approval machinery, and no change is needed.
- `Needs Me` reads **2 rows** (S1 and P1) → the negation *includes* empty
  values, so any item without a `Next Approval` value is a false positive. The
  recorded remedy is to require the field to have a value; the candidate syntax
  must be tested in the filter bar and never assumed, and if the bar rejects it
  the over-breadth stands as a documented limitation. A second remedy available
  in that branch — setting `Next Approval = —` on container nodes too — is
  **not** to be applied without a separate decision, because it would mask the
  defect rather than record it.
- Any other count is a finding: stop and report.

**Result: 2 rows — S1 and P1. The negation includes empty values.** The four
slices, all carrying an explicit `—`, were correctly excluded; the only two items
that surfaced are the two with no value at all. `-next-approval:"—"` therefore
does **not** implement the spec's "is set and ≠ `—`" — it implements "≠ `—`, or
unset", and every item added to the Project before its `Next Approval` is
written is a false positive in the human attention queue. Recorded as a
**confirmed defect of the `Needs Me` filter**, carried to M2 in §8; deliberately
not patched inside M1, since the M1 stop condition is reached and any filter
change would need its own verification pass.

**The observation window for this probe was closed once and must not be closed
again.** RB-4c proposed reading it off the M0 probe item; Batch 3d archived that
item first, and archiving removes a row from every view, so a 0-row reading
after archiving proved only that archiving worked. Batch 4 was the next and only
scheduled opportunity, and it was taken.

## 7. Business-repository guard (negative check)

Zero business repositories appear in: the Project (items, auto-add rules,
drafts), either Gatebraid repo's issues/labels, the sample metadata blocks, or
any new resource created in M1.

**Committed tree (RB-3, Batch 2):** `git grep` for all six protected names over
the PR head → **no matches**. Those names are deliberately absent from this
manifest and from every committed file, so the zero-match invariant is
re-checkable at any time; they are referenced only indirectly, as here. The only
superseded identifiers present anywhere in the tree are the former *Gatebraid*
names inside ADR-0010 Part II's historical mapping table.

**Project side (RB-4c, 2026-07-30, read-only GraphQL):**

| Surface | Result |
|---|---|
| Repository of every Project item | `MianliWang/gatebraid-scratch` only (1/1 item) — no protected repository |
| `projectV2.repositories` (linked repos) | `totalCount = 0` — nothing linked |
| Case-insensitive match of all six protected names listed in the M1 execution approval | **0 hits** |
| Work-read of any business repository | none — no account-level repository enumeration was performed, deliberately, so protected names never enter the workflow |

Scope boundary: the above exhausts what the API can see (Project items + linked
repositories). The UI's "recently used / suggested repository" dropdowns are not
API-exposed; if any protected name is ever seen preselected or suggested in the
UI, the hard rule requires an immediate pause.

## 8. Deviations and limitations record

- **Execution channel:** M1 GitHub mutations run on the operator's host via
  authenticated `gh` 2.96.0 (operator decision 2026-07-29) — the Cowork
  GitHub connector never attached to the coordinator session. `gh` is a
  sanctioned path; Manual batch approvals unchanged.
- Views — actual finding recorded in §2 (RB-4a), superseding the anticipated
  wording, which was factually wrong on this host: `gh` exposes no
  view-management subcommand, but GraphQL on this path DOES expose
  `createProjectV2View` / `updateProjectV2View` / `deleteProjectV2View`
  (create: projectId+name+layout; update additionally filter), while
  grouping, sorting, and visible-field sets have no API input at all —
  manual UI configuration of the 12 views therefore remains required. The
  twelve views remain acceptance requirements.
- **gh token scopes** (RB-1): present `gist, read:org, repo, workflow` —
  lacked `project`/`read:project`; R6 (Project existence) blocked with the
  error recorded verbatim in RB-1. Operator runs
  `gh auth refresh -s project,read:project` (re-auth of gh itself, not a
  repo mutation); R6 re-ran read-only at RB-4a and **succeeded** — Project #1
  read back in full, so the scope gap is closed. Scope-wording follow-up in the
  next entry.
- Host Git Bash lacks `jq`; `gh` built-in `--jq` used instead (syntax-only
  adaptation; semantics unchanged).
- Scope-wording note (RB-4a): after the refresh the token lists
  `gist, project, read:org, repo, workflow` — `read:project` is not listed
  separately because GitHub collapses it into the `project` superset;
  capability functionally proven by R6 succeeding. Coordinator verdict:
  proceed; no literal-mismatch stop.
- **Pre-existing Project state discovered at RB-4a** (M0-probe provenance,
  predates M1): custom single-select `Workflow` field with exactly one option
  (`Needs Plan Approval`, option id `2ad6af85`) — name collision + options
  mismatch vs the 13-option spec → host stopped under rule B3 with **zero
  mutations**. One pre-existing item: the M0 probe issue
  (`gatebraid-scratch#1`, label `needs-human`,
  `Workflow = Needs Plan Approval`, body "M0-only mobile visibility probe.
  Retain for M1.") — business-repository check clean. Remedy options
  recorded: (1) GraphQL field-update carrying the existing option id
  (requires 13 colors + 13 descriptions the spec does not define);
  (2) delete + recreate (destroys the probe item's field value);
  (3) operator completes the option list in the Project UI (no out-of-spec
  values, no data loss) — host + coordinator recommendation. **Operator
  decision: option 3, executed and verified (RB-4b pt.2)** — field extended
  in place, id continuity and the probe item's value both confirmed; details
  in §2.
- Batch-4 forward intel (RB-4a, read-only): `needs-human` already exists in
  `gatebraid-scratch` with color `D4C5F9` / description "Requires human
  attention" (M0 provenance). The runbook §6 color/description were drafting
  choices, not authority requirements — the authoritative constraints are the
  label *name* and scratch-only placement. The other three labels are absent
  (clean creates). Issue-numbering forecast: control repo #1 is the draft PR
  (issues/PRs share one sequence) → Stage S1 = #2, Phase P1 = #3; scratch #1 is
  the M0 probe → Slices A–D = #2–#5. **Disposition: RESOLVED (RB-5).**
  `needs-human` left untouched and verified byte-identical; the forecast proved
  exact — all six issues landed on their predicted numbers.
- **Label colours and descriptions are host drafting choices, not authority
  (RB-5).** The control-plane tree fixes only the three label *names* and their
  scratch-only placement; it defines no colour and no description (grepped
  across `adr/`, `protocols/`, `projects/`, `schema/`, `templates/`). The values
  in §3 were selected at execution time. `strict-gate` and `security-sensitive`
  descriptions paraphrase ADR-0004; **`scientific-evidence`'s description has no
  in-tree source and was authored by the host.** Accepted as-is by the operator
  — the same disposition already on record for `needs-human` — and recorded here
  so no later reader mistakes them for normative. Each is a one-command change
  if a future ADR defines them. Cosmetic note, deliberately not acted on:
  `strict-gate` `B60205` and `security-sensitive` `D93F0B` are both reds and are
  hard to tell apart at a glance; accessibility work is deferred by operator
  decision, so this is logged for M2, not fixed.
- **Coordinator error — label acceptance criterion was ambiguous (RB-5).** The
  Batch 4 Gate 4A criterion read "the scratch label list contains exactly these
  four". `gatebraid-scratch` also carries GitHub's nine repository-creation
  defaults (`bug`, `documentation`, `duplicate`, `enhancement`,
  `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`), so the
  literal reading was unsatisfiable at 13 total. **Corrected criterion of
  record: all four Gatebraid labels exist, and no Gatebraid label beyond those
  four exists** — which is what was actually verified. The nine defaults are
  inert (nothing in Gatebraid reads them) and were deliberately not deleted:
  deletion was outside the approved batch. Cleaning them is available as a
  separate trivial batch and buys nothing for M1.
- **Stage/Phase issue titles and the Stage `projects` value are host drafting
  choices (RB-5).** §3 fixes ids and structure, not prose titles. The host
  authored both titles and set `projects: ["MianliWang/gatebraid-scratch"]` on
  the Stage block — schema-legal (the field is documented "Informational;
  authorization is per-milestone") and consistent with the ratified rule that
  every committed example stays self-contained within Gatebraid resources.
  Accepted; recorded as drafting, not authority.
- **Validation tooling note (RB-5).** `jsonschema` and `pyyaml` were absent on
  the host. Rather than install anything — installs are outside every approved
  batch — the host wrote a self-contained YAML-subset parser plus a JSON-Schema
  subset validator covering `const` / `type` / `pattern` / `enum` / `required` /
  `additionalProperties` / `items` / min-max / `minLength`, i.e. every construct
  the three schemas actually use. Correct call under the no-improvisation rule.
  Consequence to carry forward: the metadata blocks are validated against a
  *subset* implementation, not a reference validator. Re-validating the six
  bodies with a reference `jsonschema` is an M2 item.
- Batch 2 environment notes (RB-3): `core.autocrlf` on the Windows host
  emitted 40 "LF will be replaced by CRLF" warnings at `git add` — the index
  stores LF; no content change. The local clone's remote URL still carries
  the pre-rename casing (`…/Gatebraid.git`); GitHub redirected the push to
  the renamed repo correctly; the URL was deliberately not altered (outside
  Batch 2's approved list — `git remote set-url` left to the operator).
- Host working-folder note: the pre-existing local `LICENSE` modification
  (201/201-line churn, likely CRLF/LF) was found already resolved at recon —
  working tree clean. Operator confirmed intentional (2026-07-29, recorded
  with the Batch 1 approval) — the Batch 2 clean-tree precondition is
  satisfied.
- **TEXT-field grouping — anticipated limitation RESOLVED as available
  (RB-4c).** The views checklist and the UI guide flagged `Parallel Group` and
  `Stage` as TEXT fields whose groupability was unverified, with instructions to
  leave them ungrouped and record the limitation if the dropdown omitted them.
  Verification confirms both are `dataType = TEXT` **and** that grouping was
  set and persisted — `Ready Frontier` groups by `Parallel Group`, `By Stage`
  groups by `Stage`. GitHub Projects v2 permits grouping on TEXT fields. This
  entry supersedes the anticipated limitation; no downgrade was needed. The
  documented non-groupable set remains title / labels / reviewers / linked PRs.
- **Deviation — `By Project` sort incomplete (RB-4c).** Verified
  `sortByFields = [Repository ASC]`; the checklist requires `Slice ASC`. The
  two other grouped views (`Ready Frontier`, `By Stage`) each retained their
  specified sort, so this is not group-forced system behaviour; cause not
  asserted. Remedy is a single UI action (By Project → View → Sort → `Slice`
  ascending → Save to current view). Approved as Batch 3d step 1; **still
  open at RB-4d** — the UI action had not been performed when the host ran its
  verification, which read `[Repository ASC]` both before and after. Not a
  configuration failure; the host correctly declined to self-remediate.
  **Disposition: RESOLVED (RB-4f, 2026-07-30).** `sortByFields = [Slice ASC]`,
  `groupByFields = [Repository]`. Server `updatedAt = 07:08:14Z` sits between
  the RB-4e read (06:54:40Z) and the RB-4f read (07:12:28Z), proving the three
  earlier `[Repository ASC]` readings were an ordering artefact of an
  unsynchronised handshake, not an API defect and not a misconfiguration.
  **Process lesson, recorded deliberately:** the coordinator assigned the UI
  action to the operator in Batch 3d step 1 but placed its read-back in step 4
  of the same host batch, with no wait between them — a batch must never
  interleave an operator action and a host verification of that action without
  an explicit handshake. Future batches split at that boundary.
- **`Needs Me` filter — OR-gap plus an unset-value precision issue.** The
  spec's condition is `Next Approval` *is set and* ≠ `—` **OR** label
  `needs-human`; the Projects filter bar is AND-only, so only the first half is
  expressed: `-next-approval:"—"`. Consequence already documented: a row that
  is `Blocked` + `needs_input` carrying only the label surfaces in `Blocked`,
  not in `Needs Me`. **Additional precision issue found at RB-4c:** the
  implemented filter is purely negative and does not require the field to be
  set, so an item with `Next Approval` *unset* may also match — the spec says
  "is set and ≠ —". Whether it does match depends on GitHub's negation
  semantics over empty values, which falls under the "filter evaluation is not
  machine-checkable" limitation in §2 and must be read in the UI.
  Candidate tightening: prefix a `-no:` clause so the field must have a value.
  **This syntax is to be tested in the filter bar, never assumed** — if the bar
  rejects it, the filter stays as-is and the gap stands as recorded. No
  alternative syntax is to be invented.
- **Pre-existing Project item — `items.totalCount = 1`, not 0 (RB-4c).**
  `PVTI_lAHOBRofUs4Beum7zg0bhMg` · ISSUE · `archived = false` · added
  2026-07-28T19:54:16Z → `MianliWang/gatebraid-scratch#1` "M0 Mobile Visibility
  Probe", `state = OPEN`, label `needs-human`, `Status = Todo`,
  `Workflow = Needs Plan Approval`, every other field unset. M0 provenance,
  scratch repository, predates the view session — **not** produced by M1.
  Static projection against the twelve filters: it falls **outside** `Ready
  Frontier`, `Active`, `Codex Consultations`, `Review Queue`, `Repair Queue`,
  `Blocked`, `Release Queue`; it falls **inside** `Planning` (its filter names
  `Needs Plan Approval` explicitly), `By Project`, `By Stage`, `All Work`; its
  `Needs Me` membership is undecided for the reason above.
  **Impact on the Batch 4 acceptance criteria:** `Ready Frontier` = 4 rows
  (A–D) is unaffected, but `Needs Me` = exactly 1 row (B) is broken by this
  item, which carries precisely the `needs-human` label the filter cannot
  express. **Disposition: RESOLVED — archived, not deleted (Batch 3d step 2,
  RB-4d).** `gh project item-archive` (present in gh 2.96.0; no GraphQL
  fallback needed, `item-delete` never used), exit 0. Read-back:
  `isArchived = true`; the underlying issue untouched — `state = OPEN`, label
  `needs-human` intact, `Workflow = Needs Plan Approval` intact, and
  `gh issue view` reports `updatedAt = 2026-07-28T19:47:17Z`, two days older
  than the operation, independently proving nothing was written to the issue.
  Its body ("M0-only mobile visibility probe. Retain for M1.") is preserved, so
  the M0 evidence survives while the row leaves every view. Archiving was chosen
  over deletion precisely because it is reversible.
- **Default view `View 1` — still present (RB-4c).** `number = 1`,
  `name = "View 1"` (pure ASCII), `TABLE_LAYOUT`, no filter, no sort; fields
  Title · Assignees · Status · Linked pull requests · Sub-issues progress ·
  Workflow. `updatedAt = 2026-07-28T19:51:51Z` — earlier than the twelve-view
  session, confirming the UI pass never touched it; it is M0-probe residue.
  It makes `views.totalCount = 13`, so any later "view count = 12" assertion
  would fail spuriously, and it is the only view surfacing the system `Status`
  field, which competes visually with `Workflow` as the state authority
  (ADR-0008). `All Work` covers its entire purpose. **Disposition: RESOLVED —
  deleted (Batch 3d step 3, RB-4d).** Gated: step 2 read-back green, all twelve
  spec views re-read and character-exact, and the full pre-deletion id set
  recorded. Target identity proved before the call — `PVTV_lAHOBRofUs4Beum7zgLHw_k`,
  name code points `56 69 65 77 20 31` = `View 1`, ASCII-only, matching exactly
  one view. A first `deleteProjectV2View` attempt was **rejected at GraphQL
  validation** (`undefinedField` on the payload selection set) and therefore
  never executed; the host read back `views.totalCount = 13` with View 1 intact,
  introspected the real payload (`clientMutationId`, `projectV2View`), and
  retried. Post-deletion: `13 → 12`; the surviving id set equals the pre-set
  minus View 1 exactly, with no unexpected additions or removals and all twelve
  names unchanged.
- **View numbering carries a permanent +1 offset (RB-4d).** GitHub does not
  renumber views after a deletion, so the twelve are numbered **2–13** and no
  view numbered 1 exists. Checklist rows 1–12 therefore map to GitHub view
  numbers 2–13. Any verification that indexes views by GitHub `number` must
  apply this offset; index by `name` where possible.
- **Coordinator error — archived-item counting semantics (RB-4d).** The Batch 3d
  read-back criteria asserted that `items.totalCount` "may still read 1" after
  archiving because archived items remain in the collection. **That is wrong.**
  Measured on this Project: `items` **excludes** archived items by default —
  `items` → 0, `items(archivedStates:[NOT_ARCHIVED])` → 0,
  `items(archivedStates:[ARCHIVED])` → 1,
  `items(archivedStates:[ARCHIVED, NOT_ARCHIVED])` → 1. The item still exists
  and is still bound to the Project (direct `node(id:)` fetch succeeds), but
  enumerating it requires passing `archivedStates` explicitly; the enum has
  exactly two values. **Standing consequence: every future "what is in the
  Project" check — including the protected-repository negative check — must pass
  `archivedStates:[ARCHIVED, NOT_ARCHIVED]`, or it will silently miss archived
  items.** The host was right to treat the four substantive criteria, not the
  count, as the gate.
- **Spec wording — "clear `Next Approval`" must mean "set to `—`" (found while
  deriving §6.1).** The Gate 1 and Gate 3 contracts and spec §2 describe the
  approval door as "the `Next Approval` field clearing" / "clear
  `Next Approval`", while the `Needs Me` view is filtered on
  `Next Approval != —`. If "clear" is implemented as *removing* the value, and
  GitHub's negation includes empty values, then every slice that has passed its
  approvals — including closed, Done slices, since `Needs Me` carries no
  `is:open` clause — would reappear in the attention queue permanently. The
  field's designed resting value is the `—` option, exactly as for `Gate`.
  **Reading of record: "clear" = set to `—`, never unset.** A wording amendment
  to `protocols/gatebraid-control-plane-spec-v1.md`, `protocols/gate-1-contract.md`
  and `protocols/gate-3-contract.md` is proposed for the final M1 commit; §3 already
  applies the reading by setting `Next Approval = —` on the Batch-4 slices.
  Whether `Needs Me` should additionally carry `is:open` is deferred to §9.
- **Validity conditions for the Batch-4 empty-value probe (§6.1).** The 0-vs-2
  reading is only diagnostic if all three hold; if any fails the observation is
  uninterpretable and must be reported as such rather than scored:
  1. The Project's **active** items at the end of Batch 4 are exactly the six
     new ones. Any additional item with an empty `Next Approval` adds a row and
     destroys the 2-row arm of the test.
  2. `Next Approval = —` is **written explicitly** on all four slices. "Unset"
     and "set to the `—` option" are different states and telling them apart is
     the entire measurement.
  3. The M0 probe item stays **archived**. It carries `needs-human` and an empty
     `Next Approval`; un-archiving it would contribute a third row.
- **Specification gap — `Show hierarchy` was never specified per view, and its
  default broke two views (found at the Batch-4 UI read).** The twelve-view
  specification in `projects/mianli-engineering-views-checklist.md` fixes
  layout, filter, grouping, sorting and visible fields, but says nothing about
  the `Show hierarchy` toggle, so every view kept GitHub's default of **On**.
  Two consequences, both observed:
  1. **Row counts became meaningless.** With hierarchy on, GitHub nests P1 under
     S1 and A–D under P1, so a queue view displays the number of *roots* — 1 —
     regardless of how many items match. The first post-Batch-4 reading showed
     1 row nearly everywhere and briefly looked like data loss; the API had
     already read back all six items with full field values.
  2. **`By Project` grouping was defeated.** Its purpose is per-repository
     grouping, but child items render under their *parent's* group: the four
     `gatebraid-scratch` slices appeared beneath `gatebraid`, and the
     `gatebraid-scratch` group did not render at all. A view that answers "how
     much work sits in which repository" answered it wrongly.
  **Resolution applied (operator UI, 2026-07-30):** `Show hierarchy` set **Off**
  on the ten table queue views — Needs Me · Ready Frontier · Planning · Codex
  Consultations · Review Queue · Repair Queue · Blocked · Release Queue · By
  Project · All Work — and left **On** for `By Stage` alone, which is the
  structural view and the only one whose job is to render the tree. `Active` is
  a board and exposes no such toggle. All measurements in §6.1 were re-taken
  afterwards and every one matched.
  **`Show hierarchy` is a per-view attribute the API does not expose**, so it
  joins column order, board column rendering and filter evaluation on the
  UI-only list in §2 — it cannot be machine-verified and must be checked by eye.
  A checklist amendment adding an explicit `Show hierarchy` column for all
  twelve views is proposed for the final M1 commit.
  Note that this change post-dates the RB-4f verification table; that table
  remains valid, because `Show hierarchy` appears in none of the attributes it
  asserts (`layout`, `filter`, `groupByFields`, `sortByFields`, `visibleFields`).
- **Confirmed defect carried to M2 — the `Needs Me` filter is over-broad.**
  Measured at Batch 4 (§6.1): `-next-approval:"—"` returns items whose
  `Next Approval` is *unset*, so the view showed S1 and P1. The spec's condition
  is "is set and ≠ `—`". Every item added to the Project before its
  `Next Approval` is written will therefore appear in the human attention queue
  as a false positive. Two remedies exist and **neither is applied in M1**:
  (a) tighten the filter so the field must have a value — the candidate syntax
  must be tested in the filter bar, never assumed, and if the bar rejects it the
  over-breadth stands as a documented limitation; (b) set `Next Approval = —` on
  container nodes as well — rejected as a *masking* fix, since it hides the
  defect for this sample without correcting the filter for anything else.
  Deliberately left unpatched: M1's stop condition is reached, and changing a
  view filter requires its own verification pass.
- **A second, automatically maintained state field exists: built-in `Status`
  (found at the post-crash state reconstruction, RB-R).** All six Batch-4 items
  carry `Status = Todo`, which **no batch ever set**. GitHub Projects ships
  built-in workflows, and one of them ("item added to project → set Status:
  Todo") is enabled on this Project — the badge in the UI reads `Workflows 6`.
  Consequences worth stating plainly:
  1. ADR-0008 makes `Workflow` the sole state authority. `Status` does not
     contradict that — nothing in Gatebraid reads it — but it is a second field
     that *looks* like state and is kept current by machinery outside our
     control. This is the same hazard that justified deleting the default
     `View 1`, which was the only view surfacing `Status`. No M1 view displays
     `Status`, so the hazard is contained.
  2. **The Project's built-in workflows were never inventoried during M1.** That
     is a genuine gap: fields, options and views were specified in detail while
     the Project's own automation was left at whatever GitHub enabled by
     default. Some defaults are harmless (`item closed → Status: Done`); others
     would matter a great deal (`auto-archive items` could remove rows from
     every view; `auto-add to project` could pull in items from repositories we
     never authorised — including, in principle, a protected one).
  **Inventory completed before the final commit** — see the next entry. M1
  changes none of them.
- **Built-in Project workflow inventory (2026-07-30).** `workflows.totalCount`
  = 6, all six `enabled`, every `createdAt` = `updatedAt` =
  `2026-07-28T19:47:31Z`, i.e. the Project's creation moment — no one has ever
  toggled or edited one, and no M1 batch touched them. GraphQL exposes only
  `id · number · name · enabled · createdAt · updatedAt · project ·
  fullDatabaseId` (introspected; there is no trigger/action/condition field), so
  the triggers and actions below were read from the Project UI and are recorded
  verbatim, not inferred:

  | # | Rule | Trigger | Action | State |
  |---|---|---|---|---|
  | 1 | Auto-add sub-issues to project | an item in the project has sub-issues | add the sub-issues to the project | **On** |
  | 2 | Auto-close issue | the status is updated to `Done` | **close the issue** | **On** |
  | 3 | Item added to project | an item is added (issue, pull request) | set `Status: Todo` | **On** |
  | 4 | Item closed | an item is closed (issue, pull request) | set `Status: Done` | **On** |
  | 5 | Pull request linked to issue | a pull request is linked to an issue | set `Status: In Progress` | **On** |
  | 6 | Pull request merged | a pull request is merged | set `Status: Done` | **On** |

  Confirmed **off**: `Auto-add to project`, `Auto-archive items`,
  `Code changes requested`, `Code review approved`, `Item reopened`. The two
  rules named as stop conditions for the final batch — a repository-scoped
  auto-add, and auto-archive — are therefore both disabled, and the batch
  proceeded.
  This also settles the provenance of `Status = Todo`: rule 3 wrote it. The
  earlier attribution was an inference from observation; it is now read from the
  rule itself.
- **Live hazard — the Slice closure invariant is not enforced, and one enabled
  rule can bypass it.** ADR-0007/0008 hold that a Slice issue closes **iff**
  `Gate = G3 passed`, and closing a Slice is precisely what releases its native
  `blocked-by` dependents. Rule 2 (`Auto-close issue`) creates a second, fully
  automatic closure path: **anything that writes `Status = Done` closes the
  issue.** Writers of `Status = Done` include rule 4, rule 6, and a human
  dragging a card into a Done column on any board view. A Slice could therefore
  close — releasing its dependents — without Gate 3 ever being recorded.
  Nothing enforces the invariant today; it is a documented intention.
  **Unresolved sub-question, deliberately not guessed:** whether rule 6 writes
  `Status` on the merged pull request's own item or on the *linked issue's*
  item. The screenshot shows no target selector. Rule 5 demonstrably writes to
  the linked issue, so cross-writing is possible in principle. The test is one
  throwaway pull request in `gatebraid-scratch` linked to a scratch issue —
  an M2 item (§9), not an M1 claim.
  **Disposition: recorded, not mitigated in M1.** The hazard cannot fire in the
  current state — no pull request is linked to any Slice, no board drag has
  occurred, and M2 has not begun — and disabling rule 2 would contradict this
  milestone's explicit "inventory only, change nothing" scope. Disabling it is
  the recommended first action of the next milestone, ahead of any slice
  execution.
- **The Project's membership rule is documented but unenforced (2026-07-30).**
  `projects/mianli-engineering.md` states that only issues from `gatebraid` and
  `gatebraid-scratch` may join the Project. Rule 1 above means any issue linked
  as a sub-issue of an item already in the Project is added automatically —
  including, in principle, one from a protected business repository. The
  protection today is entirely the standing prohibition on creating such a link,
  not a mechanism. Risk is lower than a repository-scoped auto-add, because it
  requires a deliberate linking action that is itself forbidden; but the
  membership rule should be understood as a convention, not a guard. Carried to
  M2 (§9).
- **`core.autocrlf = true` with no `.gitattributes` (RB-R).** This is the root
  cause of the LICENSE 201/201-line churn recorded in the Batch 2 notes. The
  working tree is clean now, but the configuration remains, so any fresh clone
  or checkout can reproduce line-ending churn. The fix — committing a
  `.gitattributes` with `* text=auto eol=lf` — is **deliberately not applied in
  M1**: it would add a 41st file to a tree whose 40-file composition is part of
  the M1 acceptance criteria. Carried to M2 (§9).
- **Local `origin` URL still carries the pre-rename casing (RB-R).**
  `https://github.com/MianliWang/Gatebraid.git` while the server canonical is
  `MianliWang/gatebraid`. GitHub is case-insensitive here and redirects, so
  nothing is broken, but it is the last artefact of the casing decision
  (ADR-0010, Option A) still pointing at the old form. Corrected at the final
  commit — a local git-config change, not a GitHub mutation.
- **Host session files went dangerously stale (RB-R).** `CLAUDE.md` and
  `_handoff/M1-STATUS.md` (both untracked, in `.git/info/exclude`) still read
  "no GitHub mutation has occurred anywhere yet" long after Batches 1–4 had
  landed. They are the first thing a fresh host session reads after a crash, so
  a stale copy actively misleads recovery. Refreshed at the final commit.
  **Standing rule adopted: the host state file is updated at the end of every
  batch, not at the end of the milestone.**
- TBD: anything else hit during batches, each with exact manual steps or the
  stop-and-ask record.

## 9. Open questions for M2

1. Fold the assignment/@mention **notification-sufficiency** result into
   ADR-0008 (`needs_human_notification_sufficient` is `null`; non-blocking
   follow-up before M2 — M2 entry condition).
2. `gate-run`/`consult`/`handoff` schema field sets are v1 designs consistent
   with reports 10/12 and the spec; M2's real Gate 0/1 cycle is expected to
   produce a correction list (that list is the M3 requirements input — report
   12 §8 Q10).
3. Exact UI filter syntax for the 12 views as actually configured (record in
   §2 when views are created manually).
4. Whether `Executor = Cowork Coordinator` on Backlog items should instead be
   empty until a gate starts — decide when the `next` skill defines its
   preconditions.
5. **Container-node status sufficiency.** Stage/Phase rows carry no
   `Workflow`/`Gate` (§3); their status is derived from sub-issue progress
   plus children's fields. Decide from real M2 use whether that is legible
   enough, or whether a `Phase State` field is warranted — noting it would
   store derived data and can drift from its children, the failure mode the
   "no stored `Ready` state" note warns about. Any such field requires a new
   ADR. Decide from use, not taste.
6. **Hierarchy depth.** `gatebraid/slice@1` fixes three levels
   (`stage`/`phase` as flat strings) and the Project mirrors them as three
   text fields, while GitHub natively supports 8 sub-issue levels. The
   authoritative hierarchy is the sub-issue links, not the text fields, so a
   deeper tree would not break GitHub — it would lose fidelity in the
   metadata and in frontier grouping. Whether v1.1 needs a fourth level is an
   open schema question (new ADR if yes).
7. **Gate-expanded frontier model (design input for `next` / `gatebraid-frontier`).**
   Expanding each Slice into its four Gate nodes (internal chain G0→G1→G2→G3)
   turns every gate-graded `depends_on` edge into a uniform "predecessor gate
   node must complete" edge — a standard layered-graph/node-expansion move.
   **Expand in the computation, never in the ledger**: ADR-0007's refusal to
   create per-gate sub-issues is a representation decision and stands
   unchanged. Consequences to design against:
   - It legitimises **mutual dependencies at different gate levels** (e.g.
     `A.G3 ← B.G1` together with `B.G3 ← A.G1`), which a slice-level cycle
     check would wrongly reject even though the gate-level graph is acyclic.
     This is a common real coupling (one side needs a frozen design, the
     other needs a released implementation).
   - Cycle detection belongs to `gatebraid-doctor` at gate granularity.
   - Priority heuristics: out-degree / transitive-descendant count identifies
     unblocking bottlenecks; articulation points are candidates for
     `consult_first: true` and a raised `risk`; out-degree-0 slices are
     safely deferrable.
   - The two human approval nodes share one single-capacity resource (the
     operator) — the scheduling argument behind batching approvals into a
     fixed window.
   - **Do not solve for optimality.** With single-writer, `write_domains`,
     `resource_locks` and the concurrency caps this is RCPSP (NP-hard).
     Keep the greedy topological wave grouping already chosen (O(V+E)) and
     keep it explainable — the "status is a script, not a model call"
     principle. Critical-path work needs duration data that `gate-run`
     records will only accumulate over time; v1.1 at the earliest.
   - A **generated** gate-expanded diagram (Mermaid/DOT from
     `gatebraid-snapshot`, M3) is the right home for "show me the graph at
     gate granularity" — a disposable regenerable cache per ADR-0001, leaving
     the board at Slice granularity.
7b. **Four-level display model (design input for `gatebraid-snapshot`, M3).**
   Render Stage / Phase / Slice / Gate, with the two edge kinds drawn
   differently: **containment as nesting** (Mermaid `subgraph`), **dependency
   as arrows**. Progress differs by level and must not be conflated:
   - A Gate is discrete (not started / in progress / passed), so a Slice row
     is a **four-segment stepper** (`▰▰▱▱` = `G1 passed`) — this is the
     compact way to show gate granularity without per-gate issues.
   - **Gate-weighted roll-up fixes the container-progress limitation recorded
     in §3.** GitHub's native sub-issue progress counts only *closed*
     children, and a Slice closes only at Gate 3, so a Phase whose slices sit
     at Gate 2 reads 0/N. Instead compute
     `steps(slice) = {—:0, G0:1, G1:2, G2:3, G3:4}` from the `Gate` field and
     `phase progress = Σ steps / (4 × slice count)` (Stage rolls up the same
     way). Worked example: 4 slices, three at `G2 passed` and one at
     `G0 passed` → 10/16 = 62.5%, versus 0/4 from sub-issue progress.
   - Label it **steps completed, not effort completed**: the four gates are
     not equal work (Gate 2 dominates), so equal weighting over-reports early
     progress. Do not invent effort weights — that is false precision.
   - Output format: **Mermaid inside Markdown** is the primary target
     (GitHub renders it natively in issues/PRs/README, desktop and mobile,
     zero dependencies). A self-contained HTML variant with real progress
     bars is an optional extra, not the main path — GitHub will not render it.
   - Scale limit: gate expansion is 4×, and Mermaid becomes unreadable past
     roughly 15–20 slices. Emit **layered diagrams** — one Stage/Phase
     overview with aggregate bars, plus a per-Phase slice+gate detail
     diagram — rather than one large graph.
   - The boundary that keeps this legitimate: a regenerated, deletable file
     built from GitHub state is a cache (ADR-0001); a stateful dashboard app
     or any daemon remains excluded by report 12 §18.
7c. **Encoding rules for the HTML variant** (settled 2026-07-29 against the
   data-viz method; a working reference mock-up exists outside the repo and
   should be committed as an M3 design reference, not in M1):
   - **Uniform mark: every node is a ring.** Containers (Stage/Phase) use a
     continuous arc; a Slice uses **four segmented arcs** with a ~2px gap, so
     the shape vocabulary stays uniform while the gates stay countable.
     Gate names, dependencies and evidence links live in a **click-to-expand**
     panel, not at rest.
   - **Values are never gated behind a pointer.** The fraction is always
     visible in the ring; click/tap only adds detail. Hover-only is both an
     anti-pattern and unusable on phones — and mobile legibility is a
     first-class requirement (ADR-0008). A table-view twin is mandatory.
   - **Progress fill never carries status.** More progress is not "more
     severe": the fill stays the accent hue and status lives in a separate
     badge.
   - **No alpha-based state encoding.** "In progress" is a distinct step of
     the same hue ramp (`#86b6ef` light / `#256abf` dark), and the unfilled
     track is a lighter step of that same ramp — not neutral gray — per the
     meter spec.
   - **Status colors, validator-checked.** The first attempt paired
     `warning` (needs-you) with `serious` (blocked); the palette validator
     measured normal-vision ΔE 13.6 between them — below the 15 floor, i.e.
     hard to separate even with full colour vision. `serious` was dropped and
     "blocked" is now rendered in **muted neutral** (semantically better too:
     blocked is "not your turn", not "bad"). The shipped set — accent /
     `warning` / `critical` — validates at ΔE 24.4 CVD and 28.4 normal in
     both modes. `warning` sits below 3:1 on the light surface by documented
     design, so every badge ships **dot icon + text label, never colour
     alone**; documented palette steps are not re-stepped.
   - **The two dependency edge kinds are drawn differently**: solid for the
     native `blocked-by` (Gate-3 only) and dashed for metadata-only soft
     dependencies. Surfacing the dashed ones is the main reason this diagram
     exists — the board cannot show them (ADR-0007).
7d. **Agent communication and the knowledge base (design input for M2).**
   Confirmed against current Claude Code docs (fetched 2026-07-29), which
   cover mechanisms reports 09–12 predate:
   - **No message bus is needed or wanted.** Inter-agent alignment is state
     flushed to GitHub, per ADR-0001: teammate findings → issue comment
     before dissolution; Lead → future Lead → `gatebraid/handoff@1` +
     Project fields + committed evidence + Git state; Lead ↔ Codex → the
     consult file; Lead ↔ human → `Next Approval` / `needs-human`; Lead ↔
     Lead across repos → **no channel at all** (single writer +
     `Writer Lease` + `resource_locks`, coordinated by the frontier reading
     GitHub). Agent Teams' shared task list and mailbox are session-scoped
     and are used only inside read-only Gate 1.
   - **Teammates do not inherit the lead's conversation history** — they load
     CLAUDE.md, MCP servers and skills like a fresh session. Task-specific
     context must therefore be written into the spawn prompt, and role
     knowledge into the subagent definition **body** (its `skills` /
     `mcpServers` frontmatter is ignored for teammates; `tools` and `model`
     are honored).
   - **The knowledge base is this repository.** ADRs (decisions), protocols
     (Gate contracts), schemas, templates, per-project overlays, and
     `docs/evidence/gatebraid/`. Its extension mechanism is the ADR process
     — reviewed, attributable, in a PR. A thin per-repo `CLAUDE.md` (<200
     lines) acts as the **loader**: hard rules plus pointers into these
     protocol documents, so the Lead and every teammate start aligned.
     `.claude/rules/` with `paths:` frontmatter is available for
     path-scoped instructions.
   - **Auto memory needs an explicit decision (candidate ADR, M2).** Claude
     Code's auto memory is **on by default** and writes agent-authored notes
     to `~/.claude/projects/<project>/memory/`. Two properties conflict with
     the architecture: it is **machine-local and not shared across machines
     or cloud environments** (this operator runs Windows + WSL, so it would
     fork into two divergent stores — the dual-ledger failure ADR-0001
     exists to prevent), and it is **unaudited agent-written state that
     shapes later behavior** — the precise property for which report 10
     rejected Hermes's self-improvement loop ("behaviour drifts by design
     between your audits"), now recorded in ADR-0006. Recommendation:
     `autoMemoryEnabled: false` in the project settings of every governed
     business repository; permitted in `gatebraid-scratch` as a sandbox.
     Decide by ADR, not by leaving the default in place.
   - **Open gap: cross-slice lesson accumulation.** M2's correction list is
     a one-shot input to M3. A recurring path is needed for turning
     operational lessons into ADR/protocol amendments, so learning lands in
     reviewed durable form rather than in machine-local memory.
8. **Operating rhythm (candidate ADR-0011, M2 — deliberately NOT added to
   M1's fixed ADR-0001…0010 set).** Three rules to specify and then encode:
   batched approval windows (the Needs Me queue as the agenda, `Risk`-sorted);
   quiet hours (e.g. 02:00–07:00 America/Toronto: no approvals expected, no
   new gate started — a soft check the M3 guard could surface); and an
   **unattended read-only night shift** — Gate 0 and Gate 1 write nothing to
   the repository, so running them unattended has zero write blast radius and
   parks each slice at `Needs Plan Approval` for the morning review. That
   needs (a) an ADR explicitly authorising unattended read-only gate
   execution, and (b) a host-side launcher, since Gate 0 verifies the real
   host working tree and cannot be run from the remote Cowork shell (D7).
   Prior art the operator flagged: the ShiftX / "Night Shift Detective"
   asynchronous loop (AdventureX 2026) — work overnight, review evidence and
   set the next night's direction in the morning.

9. **Built-in Project workflows — decide per rule and record it in an ADR
   (inventory in §8).** Three concrete tasks, in priority order:
   (a) **Disable `Auto-close issue` before any slice executes.** It is the one
   enabled rule that can close a Slice — and thereby release its native
   dependents — without Gate 3. This should be the first action of M2.
   (b) **Test what `Pull request merged` writes to**: the merged pull request's
   own item, or the linked issue's item. One throwaway pull request in
   `gatebraid-scratch`. The answer decides whether merging a Slice's PR can
   set that Slice to `Done`.
   (c) Decide the standing of `Status`: hide it, repurpose it, or leave it as
   GitHub's own bookkeeping with a written note that it is not Gatebraid state.
   Related: the Project membership rule is a convention, not a guard (§8) —
   decide whether M3's guard should enforce it.
10. **Repository hygiene deferred out of M1:** commit a `.gitattributes`
    (`* text=auto eol=lf`) to end the `core.autocrlf` line-ending churn; decide
    whether to delete the nine GitHub default labels in `gatebraid-scratch`;
    re-validate the six `## gatebraid-metadata` blocks with a reference
    `jsonschema` implementation rather than the host's subset validator.
11. **Fix the `Needs Me` filter** (§8, confirmed defect): make the field's
    presence required so unset items stop appearing. Test the syntax in the
    filter bar; if it cannot be expressed, record the limitation rather than
    writing `—` onto container nodes, which would mask it.
12. **Demonstrate cross-repository native `blocked-by`** (§4): available per
    GitHub's own statement but not exercised by the M1 sample, which is
    single-repository throughout.

## 10. Stop condition

M1 ends with this manifest complete and the draft PR **unmerged**. Merge and
M2 are two separate explicit operator approvals.
