# Gatebraid Gate 1 exit checklist — P2-S2

Every item checked with evidence. Anchors refer to `gate1.md` in this
directory unless another path is named.

## Plan completeness

- [x] The approach is written and self-contained — an executor with only repo +
      plan could implement it. Evidence: `gate1.md#plan-frozen-at-exit`, the
      Approach bullet names both target paths, the ratified tool name and its
      authority, the three duties `gatebraid-validate` must discharge, the four
      classification classes its report must carry, and — load-bearing for this
      Slice — the constraint that its inputs are the frozen schemas, the N1
      corpus and `gatebraid/evidence-capture@1` read as a specification, never
      N2's implementation.
- [x] The plan decomposes into 2–3 independently verifiable tasks (split the
      Slice if more). Evidence: `gate1.md#plan-frozen-at-exit`, Approach —
      **three** tasks (K1 author the validator; K2 author its selftest; K3
      produce the Gate 2 evidence), each with its own declared verification
      command in the Test plan.
- [x] Every acceptance criterion in the Slice body maps to a declared test-plan
      command, named item by item. Evidence: `gate1.md#plan-frozen-at-exit`,
      Test plan. The Slice body's first acceptance bullet is M3-PLAN §2 N3's
      Accept-when in full, and it maps clause by clause: "all applicable N1
      mutations killed independently of N2" → **T3 + T4** for the killing and
      **T9** for the independence; "a deliberately corrupted N2 output rejected"
      → **T5**; "dual-platform" → **T2 + T4**; "the independence review (imports
      and authorship) on record" → **T9** is the imports half, and the
      authorship half is the coordinator's review from the record before freeze,
      which is not a command this Slice can run and is named as such; "the
      coverage report classifies every verified property … with no unlabelled
      `replayable` credit" → **T6**, which re-reads the emitted report rather
      than trusting the emitting run; "landed once through its own gate" → this
      Slice's own gate sequence; "frozen at delivery" → Gate 3. The second
      acceptance bullet, that every record validates against the frozen
      interfaces with its loader named, maps to **T3** and **T6** for the
      coverage report and to each gate record's own validation row.
- [x] Rollback note exists (how to abandon safely at any point). Evidence:
      `gate1.md#plan-frozen-at-exit`, Rollback note bullet — names the three
      paths to delete and the ADR-0025 §3 retention rule for an aborted branch.

## Allowlist exactness

- [x] `write_domains` lists exactly the path prefixes the plan touches —
      nothing speculative. Evidence: `gate1.md#plan-frozen-at-exit`, the
      allowlist bullet — exactly `bin/gatebraid-validate.py`,
      `bin/gatebraid-validate-selftest.py` and
      `docs/evidence/gatebraid/P2-S2/`. The freeze is **narrower** than the
      Slice body's declared `bin/` prefix, which is the direction that cannot
      admit an unplanned write.
- [x] No path outside the allowlist appears anywhere in the plan. Evidence:
      `gate1.md#plan-frozen-at-exit` — every other path the plan names
      (`fixtures/`, `schema/`, `protocols/`, `bin/gatebraid-capture.py`,
      `bin/gatebraid-capture-selftest.py`, and the committed P2-S1 capture T5
      copies from) appears as a **READ-or-EXECUTE source** and is labelled so in
      the Approach bullet's closing sentence. The write scope is mechanised by
      **T8**, whose scope is the complete output of a named `git diff
      --name-only` and not "the added files" (friction #110).
- [x] The allowlist hash is computed and recorded in the gate1 evidence yaml.
      Evidence: `gate1.md#records` P4, and `allowlist_hash`
      `0c0090ec87b5a47838edfe8bad7d8350a79d50fc642c3e1d10b1582a09223d86` in the
      metadata block with its reproducing command beside it in `hash_commands`.

## Test plan

- [x] Every task has its verification command(s), and **each was dry-run on the
      slice's declared `environment`**. Evidence: `gate1.md#records` P2 — nine
      rows T1–T9, each carrying its `$` line and its **generated** output.
      T2 and T4 ran under WSL, the rest on the Windows host; both are the
      declared `mixed-see-prose` matrix. **Not satisfiable by reading:** each
      row shows measured output. **Stated plainly:** T1–T6 and T9 invoke
      artifacts that Gate 2 authors, so their dry-run exit status is 2, not 0.
      What the dry-run establishes is what action 4 exists to establish — the
      command form and its path resolution on each declared platform: every one
      resolved to a fully-qualified platform-native path
      (`D:\Github repo\Gatebraid\bin\…`, `/mnt/d/Github repo/Gatebraid/bin/…`),
      the embedded space surviving quoting on both, and failed with `[Errno 2]`
      naming that resolved path — never a shell parse error and never a
      `/tmp`-style semantic mismatch, which is the Slice A defect the contract's
      action 4 was written against. T7 and T8 ran fully green.
- [x] Expected-green criteria are stated (what output counts as pass). Evidence:
      `gate1.md#plan-frozen-at-exit`, Test plan — every command carries its
      expected-green line. Each is stated against the instrument's **own emitted
      summary** rather than a count, deliberately: a frozen count is falsified
      by the next legitimate corpus or condition change, and a frozen plan
      cannot be repaired at Gate 2.
- [x] Test commands respect the project's prohibited-operations overlay.
      Evidence: every declared command is read-only with respect to the
      repository except where it writes inside the frozen allowlist — none is a
      state-changing Git command, none installs a dependency, none touches a
      business repository, none enumerates account repositories, and none reads
      the contents of `bin/gatebraid-capture.py` or its selftest. T5 writes its
      corrupted input under `docs/evidence/gatebraid/P2-S2/checks/` and leaves
      the committed P2-S1 capture it copies from unmodified.

## Dependencies and risk

- [x] All `depends_on` entries re-checked against predecessors' current `Gate`
      field. Evidence: `depends_on` is `[]` in the Slice metadata, and Gate 0's
      Q7 measured **zero native edges in both directions** on `gatebraid#10`
      (`captures/Q7-real-blocked-by.json` and `captures/Q7-real-blocking.json`,
      both exit 0 with `[]`, against a falsification that returns 404/exit 1 —
      so the empty set is a measured zero, not an absent endpoint). There is no
      predecessor to re-check; the empty set was measured, not assumed.
- [x] Risk notes cover the `risk` rating's justification. Evidence:
      `gate1.md#plan-frozen-at-exit`, Risk notes — five entries, each naming
      what would have to be true for the `low` rating to be wrong and the test
      that would falsify it.
- [x] `consult_first` considered and set deliberately for high-risk slices.
      Evidence: `false` in the Slice metadata; recorded in Risk notes with its
      reason — the diff adds two files behind their own falsified selftest and
      alters no contract, schema, ADR, template or corpus.

## Freeze

- [x] Plan frozen; `plan_hash` recorded. Evidence: `gate1.md#records` P5 and the
      metadata block —
      `6f68e9a09fe89242dff6d8cec2052d27e9e9ed42e32d45ef061aaeff2592f346`,
      recomputed from the final file by the command recorded beside it.
- [x] Allowlist frozen; `allowlist_hash` recorded. Evidence: `gate1.md#records`
      P4 and the metadata block —
      `0c0090ec87b5a47838edfe8bad7d8350a79d50fc642c3e1d10b1582a09223d86`,
      recomputed by the command recorded beside it.
- [x] Team findings (if any) flushed to the Slice issue before team dissolution.
      **n/a — no read-only team was spawned.** Recorded rather than left blank:
      the optional Agent Team of gate-1-contract action 2 did not run, so there
      is nothing to flush and no team constraint could be violated.

**Exit:** all items checked. The exit transition itself is executed only to the
extent the posted window authorizes it — see `gate1.md` Required disclosures,
which records that `Gate = G1 passed`, `Workflow → Needs Plan Approval`,
`Next Approval = Plan Approval (G1→G2)`, the `needs-human` label, and the
sanctioned `write_domains` write-back to the Slice issue are contract exit
elements this window does not authorize. They are reported unperformed and
carried as owed, never skipped silently — gate-1-contract: "a step that is
**skipped** rather than failed is executor error", and friction #65 is the case
where exactly this write-back was never attempted.
