# Gatebraid Gate 1 exit checklist — P2-S6

Every item is checked **with evidence**, never asserted. Anchors name a row of
`docs/evidence/gatebraid/P2-S6/gate1.md` or a capture under
`docs/evidence/gatebraid/P2-S6/g1/`.

## Plan completeness

- [x] **The approach is written and self-contained** — an executor with only
      repo + plan could implement it. Evidence: `gate1.md` §"Plan (frozen at
      exit)", bullet *Approach*, which names both defects, the four measured
      endpoints by their exact `gh` form, the internal payload contract the
      normalisation targets, and the three surfaces left untouched.
- [x] **The plan decomposes into 2–3 independently verifiable tasks.** Three:
      T1 per-source endpoints, T2 live-shape normalisation, T3 selftest
      extension. Each names the declared commands that verify it. Evidence:
      plan bullet *Tasks*.
- [x] **Every acceptance criterion in the Slice body maps to a declared
      test-plan command, named item by item.** Evidence: the mapping below,
      and the commands' dry-run rows P2/D1–P2/D8.

  | `#19` Acceptance item | Declared command(s) | Green criterion |
  |---|---|---|
  | Every O1-B1 transcript parses to the true item set (LS-01..07: 15/15 items, optional keys byte-exact, space-bearing names, per-issue objects, edge sets `[8,10,12,14]` / `[]` / `[17]`) | **D3**, **D4** | condition rows `LS-01`..`LS-07` present and passing |
  | **B-1** short read ⇒ incomplete/bounded | **D3** | condition row `LB-1` passing |
  | **B-2** bulk body as dependency answer ⇒ `undecidable`, never `startable` | **D3** | condition row `LB-2` passing |
  | **B-3** absent `workflow` ⇒ UNKNOWN ⇒ `undecidable`, never KeyError | **D3** | condition row `LB-3` passing |
  | **B-4** repaired `issue_states` observes CLOSED issues | **D3** | condition row `LB-4` passing |
  | Each of B-1..B-4 shown by seeded runs, summaries emitted by the instruments themselves, never narrated | **D3**, **D4** | the four `LB-*` rows are emitted by the selftest's own `Conditions` reporter |
  | The four `live-shapes` mutations stay killed and the whole frozen corpus passes unchanged | **D2** | `LS-M1`..`LS-M4` each `killed on`; `TOTAL: 133 passed, 0 failed`; `CORPUS CLEAN` |
  | The frozen digest `73c5e059…` is unmoved (shown by measurement) | **D1** | `digest after` equals the frozen value; `seed-reachable surface UNMODIFIED: True` |
  | Selftest extended over the live shapes via the O1-B1 transcripts, checker falsified before trust; live-transport argv construction and classification covered by declared commands | **D3**, **D4** | `SELFTEST CLEAN`, `conditions failed : 0`, `S01` positive control passing, new live conditions present |
  | A captured live smoke read is healthy, `items` include `P2-S5`, frontier exits 0 | **D5**, **D6** | snapshot exit 0, all four sources `ok` and `complete: true`, an item with `slice_id: P2-S5`; frontier exit 0, `snapshot_degraded: false`, a verdict for `P2-S5` |

- [x] **Rollback note exists** (how to abandon safely at any point). Evidence:
      plan bullet *Rollback note* — nothing committed before Gate 2 under a
      lease, branch retained never merged, no force push available, `#17` never
      acted on so abandonment cannot leave it changed.

## Allowlist exactness

- [x] **`write_domains` lists exactly the path prefixes the plan touches —
      nothing speculative.** Two entries, `bin/` and
      `docs/evidence/gatebraid/P2-S6/`. Evidence: row **P4**, and row **P2b**
      which enumerates every write target the plan names and finds all inside.
- [x] **No path outside the allowlist appears anywhere in the plan.** Evidence:
      row **P2b**, `G1-plan-path-scan.json`, exit 0, `NEITHER a permitted
      read-only input nor inside the allowlist: 0`, `ITEM HOLDS`. The scan
      separates write targets from read-only inputs and from the excluded lanes
      the plan names in order to disclaim them — negative criterion N3 quotes
      its whole frozen-prefix scope inside the plan precisely so it can refuse
      those paths.
- [x] **The allowlist hash is computed and recorded in the gate1 evidence
      yaml.** `allowlist_hash:
      8938efcce4b8b863b14f7a503c808d7c2c67d2975aad180fd153fd45cc6da291`.
      Evidence: row **P4**, `G1-allowlist-hash.json`, with the reproducing
      command in `hash_commands.allowlist`.

## Test plan

- [x] **Every task has its verification command(s), and each was dry-run on the
      slice's declared `environment`.** Evidence: rows **P2/D1**–**P2/D8**, all
      eight run on this host and captured. D1, D2, D3, D4, D7, D8 reached their
      full green criterion today. D5 and D6 were **run as declared** and exited
      3 naming the unrepaired defect and nothing else — they cannot be green
      before the repair exists, and this is disclosed rather than papered over.
      T1 → D3, D5. T2 → D3, D5, D6. T3 → D3, D4.
- [x] **Expected-green criteria are stated** (what output counts as pass).
      Evidence: each D-row of the plan's *Test plan* bullet carries an explicit
      "green:" clause naming the exact strings and exit status required.
- [x] **Test commands respect the project's prohibited-operations overlay.**
      The project **does** declare one, so this item is checked, not `n/a`. No
      declared command force-pushes, creates a worktree, installs a dependency,
      handles a credential, or runs a state-changing Git command: D1–D4 and
      D7–D8 are pure local Python reads; D5 and D6 read the control plane
      through authenticated `gh` only, with `GH_CONFIG_DIR` pinned and no
      leading slash on any endpoint; the only writes any declared command makes
      are inside the frozen allowlist. Negative criterion **N4** mechanises the
      no-new-dependency and no-HTTP-client half of the overlay and was
      falsified before trust.

## Dependencies and risk

- [x] **All `depends_on` entries re-checked against predecessors' current
      `Gate` field.** `depends_on: []` — the set is empty, so the re-check is
      vacuous and is recorded as such rather than skipped. Evidence: the
      `## gatebraid-metadata` block of `#19`, read live and validated at this
      Slice's Gate 0 (`G0-slice-metadata-validation.json`, `VALID against
      gatebraid/slice@1`). The one native dependency edge that exists —
      `#17` blocked-by `#19` — points *outward*: it makes P2-S5 wait for this
      Slice, and gives this Slice no predecessor.
- [x] **Risk notes cover the `risk` rating's justification.** Evidence: plan
      bullet *Risk notes* — `low` justified by confined scope, no new
      dependency, unchanged consumers, and reversibility; then three named
      residual risks (a live surface that has since moved, rate-limit exposure
      from the per-issue fan-out, and the possibility of satisfying the corpus
      while loosening fail-closed), each with the guard that catches it.
- [x] **`consult_first` considered and set deliberately.** `consult_first:
      false`, deliberate: the defects were diagnosed byte-exactly against the
      source that ran and the target shapes are frozen, so no open design
      question remains for a consultation to settle. Evidence: plan bullet
      *Risk notes*, final sentence.

## Freeze

- [x] **Plan frozen; `plan_hash` recorded.**
      `4435c71eaf08bf0605815e5960c8093c4698babf99ae8a7030d05ebe445671d0`,
      over 170 plan lines / 12,646 payload bytes. Evidence: row **P5**,
      `G1-plan-hash.json`; recomputed from the FINAL rendered record after the
      last render and equal to the embedded value.
- [x] **Allowlist frozen; `allowlist_hash` recorded.**
      `8938efcce4b8b863b14f7a503c808d7c2c67d2975aad180fd153fd45cc6da291`.
      Evidence: row **P4**.
- [x] **Team findings (if any) flushed to the Slice issue before team
      dissolution.** No team was spawned — gate-1-contract action 2 makes it
      optional — so there are no findings and the constraint is vacuously
      satisfied. The decision and its reason are recorded rather than left
      implicit. Evidence: row **P1**.

**Exit:** all items checked → `Gate = G1 passed`, Workflow → `Needs Plan
Approval`, `Next Approval = Plan Approval (G1→G2)`, `needs-human` ON. The
recorded human approval comment is the only door to Gate 2.
