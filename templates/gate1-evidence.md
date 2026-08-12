<!-- Template: Gate 1 evidence file — ADR-0026 shape.
     Location (M2+): docs/evidence/gatebraid/<slice_id>/gate1.md.
     Gate 1 is READ-ONLY (temporary read-only team of ≤3 permitted; lead never
     in bypass mode; findings flushed to the issue before dissolution).
     Exit freezes the plan + write allowlist (protocols/gate-1-contract.md).

     An instantiated file contains ONLY (ADR-0026 §1): (a) the
     gatebraid-metadata block; (b) record rows — fixed label, `$ command` line
     carrying its environment visibly (friction #89), GENERATED output
     (friction #96); (c) the required disclosures below; (d) fixed headings
     and row labels; (e) the frozen-plan section — the ONE prose class, the
     design artifact plan_hash covers. After the freeze the plan is cited,
     never re-described. Team findings live on the Slice issue (the contract
     flushes them there); the row below references them, it does not restate
     them (ADR-0017). ALL template comments are DELETED at instantiation.
     The heading "## Plan (frozen at exit)" is load-bearing byte-for-byte:
     plan_hash covers the lines strictly between it and the next "## " line
     (gate-1-contract action 6).
     `bootstrap_exception: true` appears in the metadata block ONLY on N2's and
     N3's own gate landings, and only before O0. On THIS gate it records the
     BOUNDED EVIDENCE BOOTSTRAP, which is a different claim from Gate 0's: the
     record claims NO N3 independent validation, because N3 does not exist yet
     — N2's records are re-validated after N3's own Gate 3 — and the record is
     excluded from V's admission series. It requires a `State Packet Approval`
     in `approvals[]` and an `output_ref` on every check (gatebraid/gate-run@2
     enforces both). One-time and expiring: dead after N2 + N3 Gate 3, and no
     later Slice may use it (M3-PLAN §2). -->

# Gate 1 evidence — <P_nn-S_nn>

## Plan (frozen at exit)

- Approach: <…>
- Exact `write_domains` allowlist: <list — becomes the frozen allowlist>
- Test plan (commands, runnable as written on the declared environment): <…>
- Risk notes: <…>
- Rollback note: <…>
- **Negative criterion (checkable):** <the property the diff must NOT have —
  state the pattern it proxies for AND the scope it will search (ADR-0018 §2);
  this is what review item R4 checks at Gate 2>

## Records

**P1 — team findings flushed** (only if a read-only team ran)
```
$ GH_CONFIG_DIR=<store> gh <the comment-listing read used, in full>
<output — the flushed-finding comment ids/urls; nothing restated here>
```

**P2 — dry-run of every declared test command, on the declared environment**
(gate-1-contract action 4 — one row per declared command)
```
$ <declared command 1, exactly as frozen>
<output>
```

**P3 — exit checklist completed, every item evidence-backed**
```
<the completed gatebraid-gate1-exit-checklist location/anchor, one line>
```

**P4 — allowlist_hash reproduced**
```
$ <the exact Python 3 stdlib command — also recorded in hash_commands>
<output — the hash>
```

**P5 — plan_hash reproduced**
```
$ <the exact Python 3 stdlib command — also recorded in hash_commands>
<output — the hash>
```

**P6 — the sanctioned `write_domains` write-back to the Slice issue**
(gate-1-contract Exit; byte-identical re-emission apart from that field)
```
$ GH_CONFIG_DIR=<store> gh <the edit + the read-back verifying it, in full>
<output>
```

## Required disclosures

- Deviations: none | <one line each, citing the friction entry or ruling>
- Environment: <one line — host, shell, and every variable a recorded
  command's meaning depends on>

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P<nn>-S<nn>
gate: 1
environment: <…>
executor: Claude Lead
base_sha: <full 40-hex sha>
started_at: "<ISO8601>"
ended_at: "<ISO8601>"
result: needs_approval   # Gate 1 always exits into Needs Plan Approval
checks:
  - name: plan-complete
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: allowlist-exact
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: test-plan-dry-run
    result: pass
    output_ref: "#records"
  - name: gate1-exit-checklist
    result: pass
    output_ref: "#records"
# refrozen: true   # only after a correct-course re-freeze (friction #50)
plan_hash: "<sha256, lowercase hex>"
allowlist_hash: "<sha256, lowercase hex>"
hash_commands:           # ADR-0011 §3 — a hash nobody can recompute is decoration
  allowlist: "<the exact command run, Python 3 stdlib only>"
  plan: "<the exact command run, Python 3 stdlib only>"
evidence_files:
  - docs/evidence/gatebraid/P<nn>-S<nn>/gate1.md
```

<!-- Exit: Gate = G1 passed; Workflow → Needs Plan Approval;
     Next Approval = Plan Approval (G1→G2); needs-human ON.
     A recorded human approval comment is the ONLY door to Gate 2. -->
