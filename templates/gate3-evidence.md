<!-- Template: Gate 3 evidence file — ADR-0026 shape.
     Location (M2+): docs/evidence/gatebraid/<slice_id>/gate3.md.
     Gate 3: human-approved publication only. Prohibited: force-push,
     publishing beyond the approved set, merging with red CI
     (protocols/gate-3-contract.md).

     An instantiated file contains ONLY (ADR-0026 §1): (a) the
     gatebraid-metadata block; (b) record rows — fixed label, `$ command`
     line carrying its environment visibly (friction #89), GENERATED output
     (friction #96); (c) the required disclosures below; (d) fixed headings
     and row labels. No narrative. Proxy checks print their matches beside
     their counts (ADR-0018 §2; friction #87). ALL template comments are
     DELETED at instantiation.

     This file is written and committed BEFORE the merge and reaches the base
     branch through the pull request. It records no merge SHA and no closure
     timestamp: GitHub holds both natively; the authoritative Gate 3 record
     is the COMPOSITE of this file, the PR's merge event, the issue's closure
     event and the Project's Workflow (ADR-0017 §1/§2/§4 — consumers read the
     native EVENT SEQUENCE, not the last state).
     `bootstrap_exception: true` appears in the metadata block ONLY on N2's and
     N3's own gate landings, and only before O0. On THIS gate it records the
     BOUNDED EVIDENCE BOOTSTRAP, which is a different claim from Gate 0's: the
     record claims NO N3 independent validation, because N3 does not exist yet
     — N2's records are re-validated after N3's own Gate 3 — and the record is
     excluded from V's admission series. It requires a `State Packet Approval`
     in `approvals[]` and an `output_ref` on every check (gatebraid/gate-run@2
     enforces both). One-time and expiring: dead after N2 + N3 Gate 3, and no
     later Slice may use it (M3-PLAN §2). -->

# Gate 3 evidence — <P_nn-S_nn>

## Publication records

**G1 — Release Approval verified** (author must be `MianliWang`, not this
session — ADR-0020 §4; terms cited by rule number, never restated —
ADR-0018 §3)
```
$ GH_CONFIG_DIR=<store> gh api repos/<owner>/<repo>/issues/comments/<id> --jq '{author: .user.login, url: .html_url}'
<output>
$ GH_CONFIG_DIR=<store> gh api user --jq .login
<output>
```

**G2a — closure precondition (a): platform automation** (ADR-0012 §2)
```
$ GH_CONFIG_DIR=<store> gh <the workflow-state read used, in full>
<output — Auto-close issue: disabled>
```

**G2b — closure precondition (b): the pull request** (pattern stated, matches
printed — `keyword #n | keyword owner/repo#n | keyword <url>`, keyword ∈
close(s|d)/fix(es|ed)/resolve(s|d), any case — ADR-0018 §1)
```
$ GH_CONFIG_DIR=<store> gh pr view <n> --json closingIssuesReferences
<output — empty>
$ <the pattern search over the PR body and every commit message the PR carries — matches printed beside the count>
<output>
```

**G3 — drift check against the Gate 2 fingerprint** (ADR-0011 §2 as amended
by ADR-0016 §1)
```
$ git diff --name-only <tree_sha> HEAD
<output — only paths inside docs/evidence/gatebraid/<slice_id>/>
$ git log --format='%H' <active_branch_head>..HEAD -- ':!docs/evidence/gatebraid/<slice_id>/'
<output — empty: every commit past the fingerprint touches only the evidence directory>
$ git status --porcelain
<output — empty>
```

**G4 — publication commands, exactly as approved, in contract order**
```
$ <git push …, environment visible>
<output>
$ GH_CONFIG_DIR=<store> gh pr create … <plain reference, never a closing keyword — ADR-0012 §1>
<output — PR url>
```

**G5 — CI status** (`none-configured` is a recorded finding, not a pass —
ADR-0011 §7, ADR-0019 §1)
```
$ GH_CONFIG_DIR=<store> gh <the check/run read used, in full>
<output — green | red | none configured, with run url or the empty listing>
```

- Pull request: <url> — referenced, not duplicated (ADR-0017 §2)

## Required disclosures

- Deviations: none | <one line each, citing the friction entry or ruling>
- Environment: <one line — host, shell, and every variable a recorded
  command's meaning depends on>

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P<nn>-S<nn>
gate: 3
environment: <…>
executor: Claude Lead
base_sha: <full 40-hex sha>
active_branch: <branch>
started_at: "<ISO8601>"
ended_at: "<ISO8601>"
result: passed
checks:
  - name: staged-set-matches-gate2-handoff
    command: "git diff --name-only <tree_sha> HEAD"
    result: pass
    output_ref: "#publication-records"
  - name: closure-precondition-automation
    result: pass
    output_ref: "#publication-records"
  - name: closure-precondition-pull-request
    result: pass          # closingIssuesReferences empty; pattern search: 0 matches, printed
    output_ref: "#publication-records"
  - name: ci-status
    result: pass          # green -> pass; red -> fail; no workflow at all ->
                          # none_configured (ADR-0019 §1) — a finding, not a
                          # pass, and not `skipped`
    output_ref: "#publication-records"
  # The merge and the closure are post-merge facts; they live in the composite
  # record (ADR-0017 §1) and are not pre-attestable in a file written before
  # the merge (friction #56).
consults: []              # every consult this gate ran, whenever it ran (friction #94)
approvals:
  - type: "Release Approval (G2→G3)"
    comment_url: "<url>"
    author: "<login observed at verification — must be MianliWang (ADR-0020 §4)>"
evidence_files:
  - docs/evidence/gatebraid/P<nn>-S<nn>/gate3.md
notes: "PR <url>. No merge SHA and no closure timestamp are recorded here — GitHub holds both natively (ADR-0017 §2)."
```

<!-- Exit (order normative, gate-3-contract): this file committed and pushed
     to Active Branch BEFORE the merge; merge per the approval's terms;
     Gate = G3 passed; Workflow → Done; CLOSE the Slice issue by explicit
     command (this is what releases native blocked-by dependents — ADR-0007,
     ADR-0012 §3); release the Writer Lease; Next Approval → —; handoff
     comment posted; Last Checkpoint updated. -->
