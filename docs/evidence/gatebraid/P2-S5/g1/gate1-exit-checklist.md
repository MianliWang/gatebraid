# Gatebraid Gate 1 exit checklist — P2-S5

Completed from `templates/gatebraid-gate1-exit-checklist.md`. Every item is
checked **with evidence** — a capture id under
`docs/evidence/gatebraid/P2-S5/g1/captures/`, or an anchor in
`docs/evidence/gatebraid/P2-S5/gate1.md` — never asserted. An item satisfiable
by reading is not evidence-backed (friction #48), and where an item cannot be
backed the fact is written here rather than ticked.

## Plan completeness

- [x] **The approach is written and self-contained — an executor with only repo
      + plan could implement it.** `## Plan (frozen at exit)`, first bullet and
      the four delta paragraphs. The approach names the deliverable, both
      composed tools, the exit algebra, the flag surface, and the four points at
      which the frozen scope and the current tools disagree. Each delta states
      the rule it applies and where that rule was read from, so an executor does
      not have to re-derive any of it. Backed by `G1-dryrun-D0-scope-pin`, which
      re-derives the scope the approach is written against.
- [x] **The plan decomposes into 2–3 independently verifiable tasks.** Three:
      T1 the producer boundary and its encoding contract, verified by D6, D7 and
      the D3 degraded-producer condition; T2 the composition and its exit
      algebra, verified by D5 and D8; T3 the selftest, verified by D3 and D4.
      No task is verified only by a command that also verifies another.
- [x] **Every acceptance criterion in the Slice body maps to a declared
      test-plan command, named item by item.** The mapping is written out in the
      plan under *Acceptance criteria of the Slice body, mapped item by item*.
      Item 1 (`R3 first-pass = pass`) and item 2 (`evidence-only repairs = 0`
      and `evidence-only aborts = 0`) are **gate outcomes, not commands**, and
      the plan says so rather than inventing a command for them; it names where
      each is evaluated and what the plan contributes to it. Item 3 maps to
      **D2** for the seven classes the frozen corpus holds and to **D3** for
      IN-01, which it does not. Item 4 maps to **D5** and **D11**.
- [x] **Rollback note exists.** `## Plan (frozen at exit)`, rollback bullet: no
      commit before Gate 2 under a lease, branch retained never merged if
      abandoned, no force push available, and a revert after merge removes two
      new files that nothing imports.

## Allowlist exactness

- [x] **`write_domains` lists exactly the path prefixes the plan touches —
      nothing speculative.** Two entries: `bin/` for the two added files, and
      `docs/evidence/gatebraid/P2-S5/` for this Slice's own gate evidence, which
      Gate 2's R1 requires because the gate records are themselves part of the
      diff.
- [x] **No path outside the allowlist appears anywhere in the plan.** Mechanised
      rather than read: `plan-path-scan.py` enumerates every repository path the
      plan section names and classifies each as a write target, a read-only
      input, or an excluded lane the plan names in order to disclaim it, then
      requires every write target to be inside the allowlist. Capture
      `G1-plan-path-scan`, record anchor `#records`, row **P2b**.
- [x] **The allowlist hash is computed and recorded in the gate1 evidence yaml.**
      `allowlist_hash` in the metadata block, with its reproducing command in
      `hash_commands`. Capture `G1-allowlist-hash`, row **P4**.

## Test plan

- [x] **Every task has its verification command(s), and each was dry-run on the
      slice's declared `environment`.** All fourteen declared rows ran at this
      gate and the outcomes are recorded in three honest classes, not asserted
      as one. Six reached full green: D0, D0F, D1, D2, D10, and the path limbs
      of D9. Seven name the deliverable this read-only gate may not create — D3,
      D4, D5, D6, D7, D8, D11 — and each was **run as declared on the declared
      platform**, producing an interpreter error naming exactly the absent file.
      For every one of those, a **companion probe** ran the same boundary
      against the real tools, so the parts other than the program under test are
      measured: `G1-probe-D6-no-document`, `G1-probe-D6-producer-failure`,
      `G1-probe-D7-stub`, `G1-probe-D8-consumer-refusal`, `G1-probe-boundary`,
      `G1-probe-D11-wsl-capture`, `G1-probe-D11-wsl-validate`. The WSL half is
      exercised by D4, D11 and the two WSL probes; the Windows half by the rest.
- [x] **Expected-green criteria are stated.** Each numbered row says what counts
      as green, including the exact exit code where the exit code is the
      assertion. **Two were corrected by the dry-run before the freeze**: D6's,
      because the real producer returns exit 3 with a degraded document rather
      than a producer failure, and D11's, because the capture tool stamps
      `platform.os` as `wsl` and not `linux`. A criterion written from either
      assumption would have failed a correct run — which is the defect action 4
      exists to catch.
- [x] **Test commands respect the project's prohibited-operations overlay, or
      the project declares none and the item is recorded `n/a`.** **`n/a`.** No
      overlay document exists in `projects/`; the item is recorded `n/a` rather
      than ticked against an invented gloss (friction #54). Stated positively:
      no declared command makes a network write, installs anything, or uses a
      temporary directory; the reads that touch the network are authenticated
      read-only calls through the command-line client, and negative criterion N5
      mechanises the no-mutation property over both the deliverable and the
      default producer it invokes.

## Dependencies and risk

- [x] **All `depends_on` entries re-checked against predecessors' current `Gate`
      field.** Re-checked at this gate through the O0 outputs, not from memory:
      the entry snapshot reports this Slice's `blocked_by` as five edges — 8,
      10, 12, 14 and 19 — every one `CLOSED`, with `cross_check: consistent`,
      and the frontier re-derived the verdict `startable` from that document
      rather than adopting the producer's. Capture `G1-entry-snapshot` and
      `G1-entry-frontier`, row **P2 entry**. The declared block names four of
      those five; the fifth, the repair Slice, is the body-edit finding the
      Gate 0 re-run recorded under Ruling 5b and this gate does not act on it.
- [x] **Risk notes cover the `risk` rating's justification.** `## Plan`, risk
      bullet: `low` on blast radius and reversibility, with four named
      correctness risks each paired with the check that fails it, and two risks
      carried rather than mitigated and named as carried.
- [x] **`consult_first` considered and set deliberately for high-risk slices.**
      `false`, and the reasoning is written rather than inherited: the scope is
      frozen and was read, both composed tools are landed and byte-pinned, and
      each of the four deltas is a mechanical application of a frozen rule to a
      surface that was measured. There is no open design question a consultation
      would settle.

## Freeze

- [x] **Plan frozen; `plan_hash` recorded.** In the metadata block with its
      reproducing command in `hash_commands`; recomputed from the final rendered
      file after the last render pass. Capture `G1-plan-hash`, row **P5**.
- [x] **Allowlist frozen; `allowlist_hash` recorded.** As above. Capture
      `G1-allowlist-hash`, row **P4**.
- [x] **Team findings (if any) flushed to the Slice issue before team
      dissolution.** **Not applicable, and the reason is recorded rather than
      left implicit.** No read-only Agent Team was spawned; the decision and its
      two reasons are in row **P1**. Nothing was flushed because nothing was
      spawned, so the constraint is vacuously satisfied rather than exercised.

**Exit:** all items checked → `Gate = G1 passed`, Workflow → `Needs Plan
Approval`, `Next Approval = Plan Approval (G1→G2)`, `needs-human` ON. The
recorded human approval comment is the only door to Gate 2.

**Two checks in this gate are typed `fail` and neither is an unchecked item.**
The source limbs of the negative criteria report `bin/gatebraid-ready.py`
absent, which is the only thing a read-only gate can report about a file it is
forbidden to create; and the closed-set sweep's explanation limb leaves residue
that this window did not clear by editing the instrument. Both are disclosed in
full in the record, and the sweep's hard-rule limb — the repository identity set
— is closed.
