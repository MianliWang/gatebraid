<!-- Template: Plan Approval (G1→G2). OPERATOR-FILLED, posted by the human on
     the Slice issue as its own act (ADR-0015 §2). An executor never writes its
     own authorisation, transcription included (ADR-0015 §3).
     Structured per ADR-0018 §3a: cite rule versions, fill only the objects of
     THIS authorisation, express departures as a structured override.
     Copy from here, fill every field, delete nothing. -->

## Plan Approval (G1→G2) — `<slice_id>`

**An approval missing a required field, self-conflicting, or ambiguous is
invalid. The gate stops as if none existed** (ADR-0018 §3a). It is corrected by
posting a *new* approval that supersedes this one, cited by comment URL — never
by the executor deciding which text is in force.

### Rules relied on

Cited by number **and by the commit in which that version stands**, so the text
being relied on is unambiguous. Terms do not restate contract rules (ADR-0018 §3)
— a restatement is a second copy that drifts.

| Rule | Version (commit SHA in `MianliWang/gatebraid`) |
|---|---|
| `protocols/gate-2-contract.md` | `<sha>` |
| ADR-0011 (gate contract corrections) | `<sha>` |
| ADR-0012 (slice closure) | `<sha>` |
| <any other rule this approval leans on> | `<sha>` |

### Objects of this authorisation

Only the things this approval is about. No general statements.

- Slice issue: `<owner/repo#n>`
- `plan_hash`: `<64 hex>`
- `allowlist_hash`: `<64 hex>`
- `write_domains`, exactly: `<path prefix>` · `<path prefix>`
- Base branch the work targets: `<branch>`

This approval is **bound to those two hashes. If either changes, it lapses** and
Gate 2 stops.

### Overrides

Any departure from a cited rule goes here as a structured entry, never as prose
elsewhere that happens to differ. Leave as `none` if there are none.

```yaml
override: none
# override:
#   - clause: "<ADR-nnnn §n, or contract file and section>"
#     scope: "<exactly what the departure covers — one slice, one path, one run>"
#     reason: "<why, in one sentence>"
```

### Scope

- This authorises Gate 2 for this slice only. It does not authorise publication
  — that is Gate 3 and needs its own approval.
- Commits on `Active Branch` only. No push, no pull request, no merge.

— `<operator name>`, operator · `<ISO 8601 date>`
