# Gatebraid Gate 1 exit checklist — P2-S3

Every item is checked with evidence (anchor/link), not asserted. Anchors are
into `docs/evidence/gatebraid/P2-S3/gate1.md` and its pinned captures under
`docs/evidence/gatebraid/P2-S3/captures/`.

## Plan completeness

- [x] **The approach is written and self-contained** — `gate1.md` §
      `## Plan (frozen at exit)`, "Approach". It names the defect, the file, the
      function, the two named quoting forms, and the exact discrimination rule;
      an executor with only the repository and this plan has the rule and the
      loci and needs nothing else. Covered by `plan_hash`
      `eb89d3eaedc2690babb3086e3be7529f62fa03e7195746b3b8106ad85a626b18`.
- [x] **The plan decomposes into 2–3 independently verifiable tasks** — Task A
      (heuristic scope), Task B (markdown record mode), Task C (the N2
      re-validation Task A and B unblock). Three, and each carries its own
      verification: A by T1/T2, B by T3/T4, C by T9.
- [x] **Every acceptance criterion in the Slice body maps to a declared test-plan
      command, named item by item** — `gate1.md` §Plan, "Acceptance mapping":
      box 1 → T1 + T2 (+ T5); box 2 → T3 + T9, guarded by T2; box 3 → T9 (+ T8);
      box 4 → T5 + T6 + T7. The mapping is stated as properties of the
      instruments' own emitted summaries and carries no count.
- [x] **Rollback note exists** — `gate1.md` §Plan, "Rollback note": nothing
      durable is at stake before the Gate 3 merge; the branch is left unmerged as
      a record, `main` stays at `63c8401f5df6ba446cf002232fcb280673c28e00`, and
      the corpus is provably unmoved by T6.

## Allowlist exactness

- [x] **`write_domains` lists exactly the path prefixes the plan touches** —
      `bin/gatebraid-validate.py`, `bin/gatebraid-validate-selftest.py`,
      `docs/evidence/gatebraid/P2-S3/`. The two subject files are named
      individually rather than as `bin/`, which is narrower than the Slice body
      originally declared and is what the Gate 1 exit write-back brings the issue
      into agreement with. Nothing speculative: no schema, contract, ADR,
      template or corpus path appears.
- [x] **No path outside the allowlist appears anywhere in the plan** as a write
      target. Paths outside it appear only as **read** subjects — P2-S1's
      captures and gate records, `fixtures/` for T6/T7, `schema/` — and the
      distinction is enforced by negative criterion **N1**, whose scope is the
      explicit path set `git diff --name-only <base_sha>..<head>`.
      `bin/gatebraid-capture.py` and `bin/gatebraid-capture-selftest.py` appear
      in no allowlist entry and are required to appear in no diff.
- [x] **The allowlist hash is computed and recorded in the gate1 evidence yaml** —
      `allowlist_hash`
      `81a0bb015ffbc5f3f6a27abfaec0a089c2b5522aa69e5ee30d5d7a01ecd404c0`,
      reproduced by the command recorded beside it in `gate1.md` § Records P4,
      capture `captures/G1-allowlist-hash.json` (92 bytes hashed, three entries
      sorted by byte value).

## Test plan

- [x] **Every task has its verification command(s), and each was dry-run on the
      slice's declared `environment`** — `environment` is `mixed-see-prose` and
      both halves were exercised. `gate1.md` § Records P2 carries one row per
      declared command with its generated output and exit status:
      T1 Windows `captures/G1-dryrun-T1-windows.json` · T1 WSL
      `captures/G1-dryrun-T1-wsl.json` · T3 surface
      `captures/G1-dryrun-T2-windows.json` · T5 Windows
      `captures/G1-dryrun-T3-windows.json` · T5 WSL
      `captures/G1-dryrun-T3-wsl.json` · T7 Windows
      `captures/G1-dryrun-T7-windows.json` · T7 WSL
      `captures/G1-dryrun-T7-wsl.json` · T8 surface
      `captures/G1-dryrun-T5-windows.json` · T6
      `captures/G1-dryrun-T6-windows.json`. Each ran; none was satisfied by
      reading.
- [x] **Expected-green criteria are stated (what output counts as pass)** —
      each of T1–T9 in `gate1.md` §Plan carries its own "Expected green" line,
      phrased against the instrument's own emitted summary. T8's is stated
      honestly as *not* a clean sweep, with the reason, so that a clean result
      there would itself be a signal that the exemption was widened.
- [x] **Test commands respect the project's prohibited-operations overlay** —
      every declared command is read-only: `--record`, `--corpus`, the two
      selftests, and the sweep driver, which only invokes `--record`. None
      writes to the repository, fetches, installs, or touches Git state. No
      command reads `bin/gatebraid-capture*.py` contents. Recorded as satisfied,
      not `n/a`.

## Dependencies and risk

- [x] **All `depends_on` entries re-checked against predecessors' current `Gate`
      field** — `depends_on` is `[]` in the Slice's metadata block, and the
      dependency graph was measured empty in **both directions** at Gate 0 (Q7,
      `captures/Q7-real-blockedby.json` and `captures/Q7-real-blocking.json`,
      both `[]` at exit 0). There is no predecessor `Gate` field to re-check, and
      the emptiness is measured rather than assumed.
- [x] **Risk notes cover the `risk` rating's justification** — `gate1.md` §Plan,
      "Risk notes": `low` is justified by scope (two functions, one file, no
      interface change, a corpus the allowlist provably cannot reach), and the
      four residual risks are named rather than rated away — including the one
      that matters most, that the exemption could be widened to buy a clean T8.
- [x] **`consult_first` considered and set deliberately** — `false` in the Slice
      metadata. Considered and left as set: `risk` is `low`, the defect is
      reproduced and localised to a named regex and a named function, and the
      discrimination rule was validated against the live populations before the
      freeze. A Codex consult before repair 1 would add nothing a measurement
      has not already settled. It remains available at repair 1 if Gate 2 finds
      the rule wrong.

## Freeze

- [x] **Plan frozen; `plan_hash` recorded** —
      `eb89d3eaedc2690babb3086e3be7529f62fa03e7195746b3b8106ad85a626b18`,
      261 plan lines, 17,059 bytes, reproduced by the command recorded beside it
      in `gate1.md` § Records P5, capture `captures/G1-plan-hash.json`.
- [x] **Allowlist frozen; `allowlist_hash` recorded** — as above, P4.
- [x] **Team findings (if any) flushed to the Slice issue before team
      dissolution** — **no read-only team ran.** Contract action 2 is optional
      and nothing was delegated, so no teammate constraint was engaged and there
      are no findings to flush. Recorded in `gate1.md` § Records P1 as a positive
      statement rather than left blank.

**Exit:** all checked → `Gate = G1 passed`, Workflow → `Needs Plan Approval`,
`Next Approval = Plan Approval (G1→G2)`, `needs-human` ON. The recorded human
approval comment is the only door to Gate 2.
