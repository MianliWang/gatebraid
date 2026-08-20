# Gatebraid Gate 1 exit checklist — P2-S1

Every item checked with evidence. Anchors refer to `gate1.md` in this
directory unless another path is named.

## Plan completeness

- [x] The approach is written and self-contained — an executor with only repo +
      plan could implement it. Evidence: `gate1.md#plan-frozen-at-exit`, the
      Approach bullet names both source paths, both target paths, both bound
      blobs and both byte counts.
- [x] The plan decomposes into 2–3 independently verifiable tasks (split the
      Slice if more). Evidence: `gate1.md#plan-frozen-at-exit`, Approach —
      **three** tasks (K1 land the two files; K2 produce the gate evidence;
      K3 verify dual-platform + corpus-unmoved + closed-set), each with its own
      declared verification command in the Test plan.
- [x] Every acceptance criterion in the Slice body maps to a declared test-plan
      command, named item by item. Evidence: `gate1.md#plan-frozen-at-exit`,
      Test plan — the Slice body's dual-platform criterion maps to **T1 + T2**;
      "guard-versus-Draft202012Validator cross-check a real pass/fail on both
      platforms" maps to the `F schema cross-check` row inside T1/T2 (asserted
      `run`, never `ABSENT`); "corpus out of scope / frozen" maps to **T3**;
      the evidence-records criterion maps to **T4**; closed-set maps to **T5**.
- [x] Rollback note exists. Evidence: `gate1.md#plan-frozen-at-exit`, Rollback
      note bullet.

## Allowlist exactness

- [x] `write_domains` lists exactly the path prefixes the plan touches —
      nothing speculative. Evidence: `gate1.md#plan-frozen-at-exit`; the two
      prefixes are `bin/` and `docs/evidence/gatebraid/P2-S1/`, and T6's
      dry-run enumerates the four paths the plan names and finds none outside
      them.
- [x] No path outside the allowlist appears anywhere in the plan. Evidence: T6
      dry-run, `gate1.md#records` — `outside allowlist: NONE`. Paths that
      appear in the plan as *read* sources (`_handoff/batch-n2/candidates/bin/`,
      `fixtures/`, `schema/`) are inputs, not writes, and are named as such.
- [x] The allowlist hash is computed and recorded in the gate1 evidence yaml.
      Evidence: `gate1.md#records` P4, and `allowlist_hash` in the metadata
      block with its reproducing command beside it in `hash_commands`.

## Test plan

- [x] Every task has its verification command(s), and each was dry-run on the
      slice's declared `environment`. Evidence: `gate1.md#records` P2 — seven
      commands T1–T7, each with its `$` line carrying its environment visibly
      and its generated output. T1 ran on Windows; T2 ran on WSL Ubuntu 24.04;
      T3–T7 ran on Windows. **Not satisfiable by reading:** each row shows the
      measured output, not an inspection verdict.
- [x] Expected-green criteria are stated. Evidence:
      `gate1.md#plan-frozen-at-exit`, Test plan — each command carries its
      expected-green line (exit status plus the specific token or value that
      counts as pass).
- [x] Test commands respect the project's prohibited-operations overlay.
      Evidence: every declared command is read-only with respect to the
      repository — none writes to a tracked path, none is a state-changing Git
      command, none installs a dependency, none touches a business repository,
      and none enumerates account repositories. T5's scan is bounded to the two
      allowlist prefixes by construction.

## Dependencies and risk

- [x] All `depends_on` entries re-checked against predecessors' current `Gate`
      field. Evidence: `depends_on` is `[]` in the Slice metadata, and Gate 0's
      Q7 measured **zero native edges in both directions** on `gatebraid#8`
      (`gate0.json` checks "Q7 dependency read, blocked_by direction" and
      "blocking direction"). There is no predecessor to re-check; the empty set
      was measured, not assumed.
- [x] Risk notes cover the `risk` rating's justification. Evidence:
      `gate1.md#plan-frozen-at-exit`, Risk notes — five entries, each naming
      what would have to be true for the `low` rating to be wrong.
- [x] `consult_first` considered and set deliberately. Evidence: `false` in the
      Slice metadata; recorded in Risk notes with its reason — the diff adds two
      self-contained stdlib-only files behind their own falsified selftest and
      touches no contract, no schema and no corpus.

## Freeze

- [x] Plan frozen; `plan_hash` recorded. Evidence: `gate1.md#records` P5 and
      the metadata block.
- [x] Allowlist frozen; `allowlist_hash` recorded. Evidence:
      `gate1.md#records` P4 and the metadata block.
- [x] Team findings flushed to the Slice issue before team dissolution.
      **n/a — no read-only team was spawned.** Recorded rather than left blank:
      the optional Agent Team of gate-1-contract action 2 did not run, so there
      is nothing to flush and no team constraint could be violated.

**Exit:** all items checked. The exit transition itself is executed only to the
extent the posted window authorizes it — see `gate1.md` Required disclosures,
which records that `Gate = G1 passed` and the `needs-human` label are contract
exit elements this window does not authorize, and that they are reported
unperformed rather than skipped silently (gate-1-contract, "a step that is
skipped rather than failed is executor error").
