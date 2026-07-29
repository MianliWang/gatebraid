# M1 verification manifest — Gatebraid control plane and specification

**Milestone:** M1 (Gatebraid Classic, profile id `classic`) · **Status:** IN PROGRESS — placeholders marked `TBD(batch N)` are filled as approved mutation batches execute; this manifest is complete only when none remain.
**Authority:** M1 tasking (Gatebraid edition, 2026-07-28) + operator M1 execution approval (2026-07-29). ADR-0010 governs names; report 12 overrides earlier documents where they conflict; report 11 D1–D8 in force.

## 1. What was created

| Item | Value |
|---|---|
| Control repository | `MianliWang/gatebraid` (private). Recon 2026-07-29 (RB-1): exists as **`MianliWang/Gatebraid`**, repo id **1315713271**, private ✓, unarchived ✓, default `main`, sole commit `53dc6a6` (README + Apache-2.0 LICENSE; operator-created). Former name `mianli-control`: **404** — no duplicate-identity conflict. **Batch 1 (RB-2; operator-approved, casing Option A):** case-only rename `Gatebraid`→`gatebraid` executed (`gh repo rename`, exit 0); final `full_name` verified exactly `MianliWang/gatebraid`; pre-existing repo, case C1 — no bootstrap |
| Scratch repository | `MianliWang/gatebraid-scratch` (private) — reused authoritative repository ID **1315376699**. Recon 2026-07-29 (RB-1): currently **`MianliWang/classic-scratch`** (former name; private ✓, unarchived ✓, default `main`; same id confirmed by direct former-name probe). **Batch 1 (RB-2):** renamed `classic-scratch`→`gatebraid-scratch` (`gh repo rename`, exit 0), id preserved; redirect verified — the former name resolves to the same id under the official name |
| Branch | `m1-control-plane` — **created (RB-2)** @ `53dc6a6543213b76bce4d694d74d5c11bf244d97` (= `main` head, API `POST git/refs`); verified present alongside `main` |
| Draft PR | TBD(batch 2): URL — **left unmerged** |
| GitHub Project | "Mianli Engineering", private, user-level — TBD(batch 3): number/URL |
| Committed tree | `adr/` (ADR-0001…0010 — the complete approved M1 ADR set; no eleventh ADR exists) · `protocols/` (spec + 4 gate contracts) · `schema/` (7 × `gatebraid/*@1`) · `templates/` (12) · `projects/` (3, incl. the manual-view creation checklist) · `evidence/sanitized/` · `NOTICE.md` · this manifest — **40 files** |

## 2. Project configuration result

- Fields created: TBD(batch 3) — expected exactly the 14 in `projects/mianli-engineering.md`, with option lists verified option-by-option.
- **Views — M1 acceptance requirement (all twelve must exist and be checked).**
  Narrow finding, to be confirmed at Batch 3 execution: *the currently
  connected GitHub connector / authentication path may not support creation of
  user-owned Project views.* If confirmed, the recorded procedure is:
  1. Create all supported Project fields and options through the connector (Batch 3).
  2. Hand the operator / ChatGPT Work the exact manual-view creation checklist
     — `projects/mianli-engineering-views-checklist.md` (name, layout, filter,
     grouping, sorting, visible fields for each of the 12 views).
  3. **Pause** until the views are created.
  4. Run a read-only verification pass of all twelve against the checklist.
  5. Only then may this manifest's view items leave TBD. **This manifest is
     not complete until all twelve views actually exist and are checked.**
  Views are never downgraded to a documentation-only deliverable.
- Preflight pre-confirmation (RB-1; `gh` 2.96.0): `gh project` exposes **no
  view-creation subcommand** — consistent with the narrow finding above;
  formal verbatim record at Batch 3.
- View creation/verification record: TBD(batch 3) — per view: created by
  (gh | operator | ChatGPT Work), exact UI filter string used, verified
  date.
- Any additional element this connector path cannot express: TBD(batch 3) —
  each with its exact manual steps; stop-and-record, never improvise.

## 3. Sample hierarchy (exact)

| Item | Issue | Repo | Sub-issue of |
|---|---|---|---|
| Stage 1 | TBD(batch 4) `#n` | `gatebraid` | — |
| Phase 1 | TBD(batch 4) `#n` | `gatebraid` | Stage 1 |
| Slice A `P1-S1` | TBD(batch 4) `#n` | `gatebraid-scratch` | Phase 1 (cross-repo) |
| Slice B `P1-S2` | TBD(batch 4) `#n` | `gatebraid-scratch` | Phase 1 (cross-repo) |
| Slice C `P1-S3` | TBD(batch 4) `#n` | `gatebraid-scratch` | Phase 1 (cross-repo) |
| Slice D `P1-S4` | TBD(batch 4) `#n` | `gatebraid-scratch` | Phase 1 (cross-repo) |

All six added to the Project with fields set (`Workflow = Backlog`, `Gate = —`,
`Stage`/`Phase`/`Slice` text fields, `Environment = wsl`, `Risk` per slice,
`Executor = Cowork Coordinator` during M1 setup): TBD(batch 4).

Labels `needs-human` · `strict-gate` · `security-sensitive` ·
`scientific-evidence` created **only** in `gatebraid-scratch`: TBD(batch 4).

## 4. Dependency encodings (exact; ADR-0007)

| Dependency | `## gatebraid-metadata` block | Native blocked-by | Verified |
|---|---|---|---|
| B requires A **Gate 1** | `requires_gate: 1` | **none** | TBD(batch 4) |
| C requires A **Gate 3** | `requires_gate: 3` | **C blocked-by A** | TBD(batch 4) |
| D requires B **Gate 2** and C **Gate 2** | `requires_gate: 2` ×2 | **none** | TBD(batch 4) |

## 5. Expected frontier — manually derived (M1 claims NO automatic calculation)

Initial state: all four Slices `Workflow = Backlog`, `Gate = —`, all issues open.

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

## 7. Business-repository guard (negative check)

Zero business repositories appear in: the Project (items, auto-add rules,
drafts), either Gatebraid repo's issues/labels, the sample metadata blocks, or
any new resource created in M1. The only occurrences of those names anywhere
in this PR are historical citations inside prior-report quotations: verified —
TBD(pre-PR check).

## 8. Deviations and limitations record

- **Execution channel:** M1 GitHub mutations run on the operator's host via
  authenticated `gh` 2.96.0 (operator decision 2026-07-29) — the Cowork
  GitHub connector never attached to the coordinator session. `gh` is a
  sanctioned path; Manual batch approvals unchanged.
- Views: if the connector/authentication path cannot create user-owned
  Project views, §2's pause-and-verify procedure applies (anticipated
  limitation of this path, recorded narrowly; the twelve views remain
  acceptance requirements either way).
- **gh token scopes** (RB-1): present `gist, read:org, repo, workflow` —
  lacked `project`/`read:project`; R6 (Project existence) blocked with the
  error recorded verbatim in RB-1. Operator runs
  `gh auth refresh -s project,read:project` (re-auth of gh itself, not a
  repo mutation); R6 re-runs read-only before Batch 3 — TBD(batch 3).
- Host Git Bash lacks `jq`; `gh` built-in `--jq` used instead (syntax-only
  adaptation; semantics unchanged).
- Host working-folder note: the pre-existing local `LICENSE` modification
  (201/201-line churn, likely CRLF/LF) was found already resolved at recon —
  working tree clean. Operator confirmed intentional (2026-07-29, recorded
  with the Batch 1 approval) — the Batch 2 clean-tree precondition is
  satisfied.
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

## 10. Stop condition

M1 ends with this manifest complete and the draft PR **unmerged**. Merge and
M2 are two separate explicit operator approvals.
