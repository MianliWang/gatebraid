<!-- Template: Gate 0 evidence file — ADR-0026 shape.
     Location (M2+): docs/evidence/gatebraid/<slice_id>/gate0.md in the working
     repo; cross-project artifacts in MianliWang/gatebraid/evidence/.
     Gate 0 is READ-ONLY: any write, fetch/pull, or branch creation is a
     contract violation (protocols/gate-0-contract.md). Entry positioning —
     checkout to the base branch — happens BEFORE entry, per the contract; it
     is not one of this file's rows.

     An instantiated file contains ONLY (ADR-0026 §1): (a) the
     gatebraid-metadata block; (b) record rows — a fixed one-line label, a
     `$ command` line carrying its environment visibly (friction #89), and
     that command's GENERATED output, never transcribed (friction #96);
     (c) the required disclosures enumerated below; (d) this template's fixed
     headings and row labels. No narrative sections, no statements about this
     file's own history, no explanatory prose. Every elision carries
     shown/total plus the committed path of the full output.
     ALL template comments, this one included, are DELETED at instantiation —
     a surviving comment is content outside the classes.
     A claimed schema validation names its loader in the row itself
     (interpreter path; PyYAML and jsonschema versions printed by the command
     — friction #55) and runs as a standalone guarded step whose failure
     prevents the commit (spec §4; friction #86).
     `bootstrap_exception: true` appears in the metadata block ONLY on N2's and
     N3's own gate landings, and only before O0. On THIS gate it records that
     startability was read from the operator-approved closed-set state packet
     rather than from the snapshot/frontier pair, which fails open on the
     control plane's input and is not startability authority before O0. It
     requires a `State Packet Approval` in `approvals[]` and an `output_ref` on
     every check — gatebraid/gate-run@3 enforces both, so the record cannot
     claim the packet and point at nothing. One-time and expiring: dead after
     N2 + N3 Gate 3, excluded from V's admission series, and no later Slice may
     use it (M3-PLAN §2). -->

<!-- Row classes (ADR-0028 §2; amended at M3 batch P-B1 for replay A's F-2):
     a row marked [instant] reads state the act of recording it will move — a
     branch tip, HEAD, the working tree — and is recorded ONCE, at the moment
     named, and is EXCLUDED from the deterministic subset a reviewer replays;
     its recorded output is the pin the [pinned] rows then name. A [pinned]
     row names full SHAs only and must reproduce byte for byte on replay. No
     row in this file names HEAD, --abbrev-ref HEAD, or a bare branch name
     inside a replayable claim. -->

# Gate 0 evidence — <P_nn-S_nn>

## Records

**A1 — repository identity and remote**
```
$ git remote -v
<output>
```

**A2 — plan baseline: head of the base branch now** `[instant]` (recorded here only; the
`Base SHA` field is set at Gate 2 from the head re-read under lease —
ADR-0011 §9)
```
$ git rev-parse refs/heads/<base-branch>
<output — X, full 40-hex>
```

**A2b — the baseline object, pinned** `[pinned]`
```
$ git rev-parse --verify <X>^{commit}
<output — X>
```

**A3 — working tree clean AND at the base branch** `[instant]` (one
predicate, friction #84)
```
$ git status --porcelain --untracked-files=all; git rev-parse HEAD
<outputs — porcelain empty; the second line equals X above>
```

**A4 — Project `Environment` field vs actual host**
```
$ GH_CONFIG_DIR=<store> gh <the field read used, in full>
<output>
$ <host probe command>
<output>
```

**A5 — tool versions**
```
$ claude --version; git --version; gh --version; codex --version
<output>
```

**A6 — slice metadata parses against `gatebraid/slice@1`**
```
$ <interpreter path> <validator invocation — prints PyYAML + jsonschema versions and the verdict>
<output>
```

## Required disclosures

- Deviations: none | <one line each, citing the friction entry or ruling>
- Environment: <one line — host, shell, and every variable a recorded
  command's meaning depends on>

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@3
slice_id: P<nn>-S<nn>
gate: 0
environment: <wsl|windows|macos-authority|mixed-see-prose>
executor: Claude Lead
base_sha: <full 40-hex sha>
started_at: "<ISO8601>"
ended_at: "<ISO8601>"
result: passed          # passed | stopped | needs_approval | blocked | human_diagnosis_required
checks:
  - name: repo-identity-and-remote
    command: "git remote -v"
    result: pass
    output_ref: "#records"
  - name: base-sha-recorded
    command: "git rev-parse refs/heads/<base-branch>; git rev-parse --verify <X>^{commit}"
    result: pass        # the first read is [instant]; the second is the [pinned] replay row
    output_ref: "#records"
  - name: working-tree-clean-at-base
    command: "git status --porcelain --untracked-files=all; git rev-parse HEAD"
    result: pass        # [instant]. dirty → result: stopped + Next Approval = Dirty Baseline Acceptance
                        # HEAD not at X after entry positioning → error (friction #84)
    output_ref: "#records"
  - name: environment-matches-host
    result: pass
    output_ref: "#records"
  - name: tool-versions
    result: pass
    output_ref: "#records"
  - name: slice-metadata-parses
    result: pass
    output_ref: "#records"
evidence_files:
  - docs/evidence/gatebraid/P<nn>-S<nn>/gate0.md
notes: "<free text; do NOT record a transition the contract does not define>"

# --- If the gate STOPPED, use this shape instead of result: passed (ADR-0013) ---
# result: stopped               # or: blocked, for an error disposition
# stop_record:
#   stopped_at: "<action number and name>"
#   disposition: decidable      # decidable | error
#   next_approval: "<Dirty Baseline Acceptance | Environment Change>"   # decidable only
#   workflow: Blocked           # error only; pair with a typed needs_input comment
#   observed: "<what was measured>"
#   expected: "<what the record says>"
#   remediation_attempted: none # ALWAYS none — the schema enforces it
```

<!-- Exit: Gate = G0 passed; Workflow → Gate 1 — Planning; handoff comment
     (the schema-tagged handoff block, schema/handoff.schema.json) on the
     Slice issue; Last Checkpoint updated. -->
