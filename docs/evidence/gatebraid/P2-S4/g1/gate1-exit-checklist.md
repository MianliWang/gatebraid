# Gatebraid Gate 1 exit checklist — P2-S4

Every item checked with evidence, not asserted. Evidence is a capture under
`docs/evidence/gatebraid/P2-S4/g1/` or a named section of
`docs/evidence/gatebraid/P2-S4/gate1.md`.

## Plan completeness

- [x] **The approach is written and self-contained** — an executor with only
      repo + plan could implement it.
      *Evidence:* `gate1.md` § Plan (frozen at exit), Approach bullet — three
      tasks, each naming its files, the P0 clauses it carries, and the document
      fields those clauses turn into.
- [x] **The plan decomposes into 2–3 independently verifiable tasks.**
      *Evidence:* T1, T2, T3. Each is verified by its own selftest command
      (D1a/D1b, D2a/D2b, D3a/D3b) which passes or fails without the others.
- [x] **Every acceptance criterion in the Slice body maps to a declared
      test-plan command, named item by item.**
      *Evidence:* `gate1.md` § Plan, "Acceptance mapping, item by item" —
      Acceptance 1 → D3a/D3b/D4; 2 → D8, D7; 3 → D6a/D6b, D3a/D3b;
      4 → D1a/D1b, D2a/D2b, D5, D4.
- [x] **Rollback note exists** (how to abandon safely at any point).
      *Evidence:* `gate1.md` § Plan, Rollback note bullet.

## Allowlist exactness

- [x] **`write_domains` lists exactly the path prefixes the plan touches** —
      nothing speculative.
      *Evidence:* `bin/` and `docs/evidence/gatebraid/P2-S4/`, matching ADR-0032
      decision 2 and `#14`'s own declared block —
      `g1/G1-writedomains-check.json`, exit 0, equal as sequences and as sets.
- [x] **No path outside the allowlist appears anywhere in the plan.**
      *Measured, not asserted:* `g1/G1-plan-path-scan.json`, exit 0 — 15 write
      targets, all inside the allowlist; 0 unclassified. Read-only inputs and
      the two disclaimed lane names are classified explicitly, and the reading
      applied ("touches" = writes) is stated in the scanner's own docstring so it
      can be disputed. Pass 1 at `g1/G1-plan-path-scan-pass1.json` (exit 1) is
      retained as the scan's falsification.
- [x] **The allowlist hash is computed and recorded in the gate1 evidence yaml.**
      *Evidence:* `g1/G1-allowlist-hash.json`, exit 0 —
      `feb6d9c8ffbbaa08242d68e64db7b13b3f080aaae3667f01d7d22bdb0c061655`,
      recorded in the metadata block with its reproducing command.

## Test plan

- [x] **Every task has its verification command(s), and each was dry-run on the
      slice's declared `environment`.**
      *Evidence:* `g1/G1-dryrun-matrix.json`, exit 0 — 3 declared commands with a
      live target ran green; 8 targeting deliverables this Slice will write ran
      and failed only on target-absent, each naming its declared path; 2 form
      twins of identical shape resolved on both halves. `g1/G1-dryrun-D7-windows.json`
      carries D7 separately for runtime. The two-part method and its limit are
      disclosed in `gate1.md` § Required disclosures.
- [x] **Expected-green criteria are stated** (what output counts as pass).
      *Evidence:* `gate1.md` § Plan, test-plan table, "expected green" column —
      one row per declared command, stated as predicates rather than tallies.
- [x] **Test commands respect the project's prohibited-operations overlay, or
      the project declares none and the item is recorded `n/a`.**
      **`n/a`** — no prohibited-operations overlay is declared. *Evidence:*
      `grep -n -i "prohibited" projects/*.md` returns no line, over the three
      files `projects/gatebraid-scratch.md`,
      `projects/mianli-engineering.md`,
      `projects/mianli-engineering-views-checklist.md`.

## Dependencies and risk

- [x] **All `depends_on` entries re-checked against predecessors' current `Gate`
      field.** `depends_on: []` — there are no entries, and the emptiness is not
      assumed: this Slice's Gate 0 read the native dependency relation in both
      directions and measured zero edges each way.
      *Evidence:* `#14` metadata via `g1/G1-writedomains-check.json`;
      `../captures/G0-Q7-blocked-by.json` and `../captures/G0-Q7-blocking.json`,
      both exit 0 and both empty.
- [x] **Risk notes cover the `risk` rating's justification.**
      *Evidence:* `gate1.md` § Plan, Risk notes bullet — `low` justified by blast
      radius, with the counter-consideration stated rather than omitted: the
      consequence if the pair is wrong is not low, because from Gate 3 it becomes
      the sole startability authority.
- [x] **`consult_first` considered and set deliberately for high-risk slices.**
      `consult_first: false`, `risk: low`. Considered and left unchanged; the
      Risk notes bullet states the condition under which it is revisited (a spent
      repair at Gate 2).

## Freeze

- [x] **Plan frozen; `plan_hash` recorded.**
      *Evidence:* `g1/G1-plan-hash.json`, exit 0 —
      `cb577dbf7fd1c0443b5e7ffbb94aacd7ada64385230afb6faa498815a4828913`, over the
      161 lines strictly between the load-bearing heading and the next `## ` line,
      with its reproducing command recorded beside it.
- [x] **Allowlist frozen; `allowlist_hash` recorded.**
      *Evidence:* as above — `feb6d9c8…`, recipe applied verbatim from
      gate-1-contract action 6, Python 3 standard library only.
- [x] **Team findings (if any) flushed to the Slice issue before team
      dissolution.**
      **No team ran.** gate-1-contract Action 2 makes the read-only team
      optional; the option was considered and declined, so there are no findings
      and no flush comment exists. *Evidence:* `gate1.md` § Records, P1 row —
      recorded rather than left silent.

**Exit:** all items checked → `Gate = G1 passed`, Workflow → `Needs Plan
Approval`, `Next Approval = Plan Approval (G1→G2)`, `needs-human` ON. The
recorded human approval comment is the only door to Gate 2.
