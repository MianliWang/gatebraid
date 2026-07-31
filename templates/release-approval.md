<!-- Template: Release Approval (G2→G3). OPERATOR-FILLED, posted by the human on
     the Slice issue as its own act (ADR-0015 §2). An executor never writes its
     own authorisation, transcription included (ADR-0015 §3).
     Structured per ADR-0018 §3a. This is the publication door: what is not
     named here is not approved.
     Copy from here, fill every field, delete nothing. -->

## Release Approval (G2→G3) — `<slice_id>`

**An approval missing a required field, self-conflicting, or ambiguous is
invalid. The gate stops as if none existed** (ADR-0018 §3a). It is corrected by
posting a *new* approval that supersedes this one, cited by comment URL — never
by the executor deciding which text is in force.

**Where a term and the rule it cites disagree, the executor stops and asks**
(ADR-0018 §4). It does not choose, and it does not resolve the conflict in
favour of the better reasoning — that is an authority question, and keeping it
out of the executor's hands is what this door is for.

### Rules relied on

Cited by number **and by the commit in which that version stands**. Terms do not
restate contract rules (ADR-0018 §3): Slice A's approval restated ADR-0012 §1's
keyword ban, dropped the qualifier that scoped it, and manufactured a conflict
the executor then had to adjudicate.

| Rule | Version (commit SHA in `MianliWang/gatebraid`) |
|---|---|
| `protocols/gate-3-contract.md` | `<sha>` |
| ADR-0012 (slice closure is explicit and exclusive) | `<sha>` |
| ADR-0016 (the drift check protects the implementation) | `<sha>` |
| ADR-0017 (the Gate 3 record is composite) | `<sha>` |
| <any other rule this approval leans on> | `<sha>` |

### Objects of this authorisation

Only the things this approval is about. **Anything not named here is not
approved**, and the gate stops rather than interpreting.

- Slice issue: `<owner/repo#n>`
- Repository: `<owner/repo>` — and no other, in this or any repository
- Branch to push: `<branch>`
- Head SHA as reviewed: `<sha>` — the `handoff_fingerprint` in
  `docs/evidence/gatebraid/<slice_id>/gate2.md` is authoritative for what is
  being published
- Base branch: `<branch>`
- Merge method: `merge commit` | `squash` | `rebase`
- Head branch after merge: `retained` | `deleted`

### Preconditions this approval requires the gate to observe

State only what the contracts do not already require. Everything below is a
read; each is confirmed, not assumed.

- `deleteBranchOnMerge` on the target repository is `<expected value>` — if it
  differs, **stop and report**; do not change it mid-gate.
- <any other platform setting whose value this approval depends on>

### CI disposition

- Merging is approved when CI is: `green` | `green or none-configured`
- `none-configured` is recorded as a **finding, not a pass** (ADR-0011 §7).
- **If any check reports red, the merge is not approved** and the gate stops.

### Overrides

```yaml
override: none
# override:
#   - clause: "<ADR-nnnn §n, or contract file and section>"
#     scope: "<exactly what the departure covers>"
#     reason: "<why, in one sentence>"
```

### Closure

- The Slice issue is closed **only** by an explicit command at Gate 3's exit,
  after `Gate = G3 passed` and `Workflow = Done` are set (ADR-0012 §3).
- **If the issue is observed closed at any point before that command, stop and
  report what was observed.** Do not reopen it and continue.

### Scope

- This slice only. It does not authorise starting another slice, a
  contract-cleanup pass, or any change to the control repository.

— `<operator name>`, operator · `<ISO 8601 date>`
