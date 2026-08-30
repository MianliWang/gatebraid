- **Approach.** Repair the live half of `bin/gatebraid-snapshot.py` in two
  layers, leaving the replay half and the assembly untouched. The two defects
  are shape defects and each gets its own layer.

  **D-A, per-source endpoints.** `LiveTransport.read` today answers every
  source other than `project_items` with one bulk call,
  `gh api repos/<repo>/issues`, and `page_index` reaches nothing. The measured
  surfaces are four, not one, and three of them are per-issue:
  `project_items` is `gh project item-list <n> --owner <owner> --format json`;
  `issue_states` is `gh api repos/<repo>/issues/<number>`; `dep_blocked_by` is
  `gh api repos/<repo>/issues/<number>/dependencies/blocked_by`; `dep_blocking`
  is the same path ending `blocking`. The three issue-backed sources therefore
  become a **per-issue fan-out** over the issue numbers discovered from the
  item-list read, and the second argument of `read` indexes that issue list
  rather than a page of a connection that does not exist. `project_items` is
  read first and is the only source that can supply the fan-out set; if it is
  not `ok` and complete, the three dependent sources are not invented — they
  are reported not-read, which keeps the existing fail-closed direction.

  **D-B, live-shape parsing.** The reading loop and `merge_pages` consume
  `nodes`, `hasNextPage`, `states` and `edges` — the **replay transcript's**
  keys, which no live body carries, so a live page yields zero rows while the
  source reports complete. The repair adds a normalisation step that maps each
  live body onto the internal payload contract `build_items` already consumes,
  and nothing downstream of that contract changes. The item-list envelope is
  `{items, totalCount}` and **carries no pagination key of any kind**, measured
  twice in the frozen corpus, so completeness is arithmetic:
  `len(items) < totalCount` is an incomplete read and is reported bounded, never
  complete. Element keys are Project field names as the surface emits them,
  including the space-bearing `active Branch`, `base SHA`, `last Checkpoint` and
  `next Approval`, and a field key is present **only when populated** — so an
  absent `workflow` is read as absent and mapped through the existing `closed()`
  helper to `UNKNOWN`, never defaulted and never a `KeyError`. Per-issue
  dependency answers are lists whose elements carry `repository`; a bulk issue
  list offered in that position lacks it on every element and is rejected as the
  wrong surface rather than parsed, which is what keeps B-2 out of `startable`.

  The classifier, `build_items`, `cross_check`, `verdict_for` and the whole
  replay transport are **not** modified: every existing selftest condition must
  stay green, and that is the regression proof.

- **Exact `write_domains` allowlist:**
  - `bin/`
  - `docs/evidence/gatebraid/P2-S6/`

- **Tasks — three, independently verifiable.**
  - **T1 — per-source endpoints (D-A).** `LiveTransport` gains per-source argv
    construction and the per-issue fan-out; `project_items` sequencing and the
    not-read reporting of dependents. Verified by D3's live-argv conditions and
    by D5.
  - **T2 — live-shape normalisation (D-B).** The live-to-internal mapping for
    the four surfaces, the arithmetic completeness rule, byte-exact optional-key
    reading, and absent-`workflow` to `UNKNOWN`. Verified by D3's LS and LB
    conditions and by D5 and D6.
  - **T3 — selftest extension.** `bin/gatebraid-snapshot-selftest.py` gains
    conditions driven by the seven O1-B1 provenance transcripts, covering
    LS-01..07 and the four behavioural criteria B-1..B-4, each seeded and each
    emitting its own summary row. Verified by D3 and D4.

- **Test plan (commands, runnable as written on the declared environment).**
  Every command is repository-relative and was dry-run on this environment at
  Gate 1; the rows are in `## Records`. `environment: mixed-see-prose` — the
  tool runs on the Windows host and the WSL half is evidence, so the
  transport-independent selftest is declared on both halves.
  - **D1** `PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B fixtures/runner-selftest.py`
    — green: `digest after` equals
    `73c5e059091982ac8cda43d9f59902f3934444b742e7a383ad9422448cd5fdfc`,
    `seed-reachable surface UNMODIFIED: True`, `conditions failed : 0`, exit 0.
    Covers: the frozen digest is unmoved by this Slice.
  - **D2** `PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B fixtures/run-corpus.py`
    — green: `TOTAL: 133 passed, 0 failed`, `CORPUS CLEAN`, exit 0, with
    `LS-M1`, `LS-M2`, `LS-M3` and `LS-M4` each shown `killed on`.
    Covers: the four `live-shapes` mutations stay killed and the entire frozen
    corpus passes unchanged.
  - **D3** `PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-snapshot-selftest.py`
    — green: exit 0, `conditions failed : 0`, `SELFTEST CLEAN`, every pre-existing
    condition still present and passing, and new condition rows present and
    passing for `LS-01`..`LS-07` and for `LB-1`..`LB-4`.
    Covers: every O1-B1 transcript parses to the true item set; B-1..B-4 each
    shown by a seeded run whose summary the instrument itself emits; the live
    transport's argv construction and classification covered by a declared
    command. The selftest takes no arguments and its falsification is intrinsic:
    `S01` is the positive control that a tool rejecting everything would fail,
    and every other condition seeds a mutation and requires it to be caught.
  - **D4** `wsl.exe -e bash -lc "cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-snapshot-selftest.py"`
    — green: exit 0, `SELFTEST CLEAN`, `network reads performed : 0`.
    Covers: the WSL half of the declared environment.
  - **D5** `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid C:/Python312/python.exe -B bin/gatebraid-capture.py --out docs/evidence/gatebraid/P2-S6/g2/captures/G2-live-smoke-snapshot.json --capture-id G2-live-smoke-snapshot --env GH_CONFIG_DIR --input bin/gatebraid-snapshot.py --output docs/evidence/gatebraid/P2-S6/g2/captures/g2-snapshot.json -- C:/Python312/python.exe -B bin/gatebraid-snapshot.py --out docs/evidence/gatebraid/P2-S6/g2/captures/g2-snapshot.json --generated-at <measured>`
    — green: the captured snapshot run exits 0; every one of the four sources
    carries `status: ok` and `complete: true`; `items` is non-empty and contains
    an item whose `slice_id` is `P2-S5`.
    Covers: the captured live smoke read, healthy, items including `P2-S5`.
  - **D6** `C:/Python312/python.exe -B bin/gatebraid-capture.py --out docs/evidence/gatebraid/P2-S6/g2/captures/G2-live-smoke-frontier.json --capture-id G2-live-smoke-frontier --input bin/gatebraid-frontier.py --input docs/evidence/gatebraid/P2-S6/g2/captures/g2-snapshot.json --output docs/evidence/gatebraid/P2-S6/g2/captures/g2-frontier-report.json -- C:/Python312/python.exe -B bin/gatebraid-frontier.py docs/evidence/gatebraid/P2-S6/g2/captures/g2-snapshot.json --out docs/evidence/gatebraid/P2-S6/g2/captures/g2-frontier-report.json`
    — green: the captured frontier run exits 0, the report carries
    `snapshot_degraded: false`, and a verdict exists for `P2-S5`.
    Covers: the frontier consumes the healthy snapshot with exit 0.
  - **D7** `PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/g1/negative-criteria.py`
    — green: exit 0, `NEGATIVE CRITERIA HOLD: N1, N2, N3, N4, N5`.
    Covers: review item R4 at Gate 2.
  - **D8** `PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/g1/negative-criteria.py --changed-from docs/evidence/gatebraid/P2-S6/g1/SEED-negative-criteria.txt --code-surface-dir docs/evidence/gatebraid/P2-S6/g1/falsification`
    — green: exit 1, `NEGATIVE CRITERIA FIRED: N1, N2, N3, N4, N5`.
    Covers: the negative criteria are falsified, not merely asserted. A
    criterion that has only ever held has never been shown able to fire.

- **Risk notes.** `risk: low` is justified by scope and by reversibility, not by
  ease: the change is confined to two files, adds no dependency, and every
  consumer of the snapshot document is unchanged and independently tested by a
  frozen corpus that this Slice may not write. The real risks are three.
  *First*, the live surfaces are frozen from captures taken on one day; a
  surface that has since changed would be met only at D5, which is why D5 is a
  declared command against the real control plane and not a fixture. *Second*,
  the per-issue fan-out multiplies reads by the number of items, so a large
  Project could meet a rate limit — the existing classifier already types
  `rate_limited` distinctly from a permission failure, and the fan-out must
  report a partial set as incomplete rather than as a whole one. *Third*, the
  repair could satisfy the corpus while loosening the fail-closed direction;
  N5 is the mechanised guard against exactly that, and every pre-existing
  selftest condition staying green is the regression evidence.
  `consult_first: false` is deliberate: the defects were diagnosed byte-exactly
  against the source that ran and the target shapes are frozen, so there is no
  open design question a consultation would settle.

- **Rollback note.** Nothing is committed until Gate 2 under a `Writer Lease`,
  and the whole Slice lives on its own branch cut from
  `3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8`. To abandon at any point: leave
  `main` where it is and stop — no push has occurred, no other Slice depends on
  this branch, and the retained P2-S5 evidence is untouched by construction
  (N3). If a branch already exists, it is retained as a record and never merged;
  ADR-0025 section 3 governs. If abandonment happens after a push but before a
  merge, the branch is retained and the pull request closed unmerged; no force
  push is available under any circumstance. `#17` is never acted on by this
  Slice, so abandonment cannot leave `#17` in a changed state — the one
  dependency edge created at setup is operational tracking only and survives
  abandonment harmlessly.

- **Negative criteria (checkable).** All five are mechanised in
  `docs/evidence/gatebraid/P2-S6/g1/negative-criteria.py`, each stating the
  pattern it proxies for, the scope it searches, and the direction in which it
  errs. All five were **falsified before trust** at Gate 1: each fired against a
  seeded input (D8) and all five hold against the real tree (D7).
  - **N1 — the diff contains no path outside the allowlist.** Scope: every path
    of `git diff --name-only <base_sha>`. Errs toward false alarm: a path
    lawfully inside but spelled differently is reported rather than passed; it
    never passes a path that is outside.
  - **N2 — under `bin/`, only the snapshot pair is touched.** Scope: glob
    `bin/**`; the changed set under it must be a subset of
    `{bin/gatebraid-snapshot.py, bin/gatebraid-snapshot-selftest.py}`. Errs
    toward false alarm: any other file appearing under `bin/` fires even if a
    human would call it in scope; it never passes an edit to another tool. This
    is the Non-goals list mechanised.
  - **N3 — no frozen input is written.** Scope: the explicit prefix set
    `schema/`, `fixtures/`, `docs/evidence/gatebraid/P2-S5/`, `adr/`,
    `protocols/`, `templates/`, `projects/`. Errs toward false alarm: it fires
    on any path under those prefixes without asking whether the change was
    benign; it never passes one.
  - **N4 — the code surface adds no runtime dependency and constructs no HTTP
    client.** Scope: the import sets of the two files of the code surface only,
    compared against the baseline non-stdlib set measured on the frozen base
    (`jsonschema` in the snapshot tool, nothing in the selftest). Errs toward
    false alarm: a stdlib module merely named like a network client is reported
    for a human read, and any new non-stdlib import fires even if benign; it
    never passes a real network client and never passes a new dependency. This
    is the delegate-authentication-to-`gh` hard rule mechanised.
  - **N5 — the fail-closed direction keeps exactly one healthy path.** Scope:
    the single file `bin/gatebraid-snapshot.py`, by enclosing function:
    `member("ok")` may occur only inside `classify()`, and a dict literal
    setting `"complete"` to `True` only inside `read_source()`. Errs toward
    false alarm: a lawful refactor moving either into a new helper fires and
    must be re-frozen deliberately; it never passes a second unguarded path to
    a healthy report.
