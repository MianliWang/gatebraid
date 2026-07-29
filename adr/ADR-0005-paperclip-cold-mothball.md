# ADR-0005 — Paperclip cold-mothball (decision record only)

**Status:** Accepted · M1 (2026-07-29) · Product: Gatebraid (ADR-0010) · **This ADR records a decision made in reports 08/09; it authorizes no action.**
**Provenance:** report 08 §18-A (mothball procedure), §17 (eleven required upstream capabilities); report 09 §1 (`PAPERCLIP_EXECUTION_DECISION: NO_GO`, `FORK_DECISION: NO_FORK`), §16 (reactivation criteria), §17 A7; report 12 §4F (unchanged).

## Decision

1. The Paperclip pilot is **cold-mothballed in place**: service stopped, state tree, checksummed backups, and export retained intact, nothing deleted, restart documented in its `MOTHBALL.md`. This is 08 §18-A — not the unverified destructive restore (§18-B) and not retirement (§18-C).
2. Paperclip holds **no role** in the Gatebraid architecture: not a control plane, not an execution runtime, not an approval or evidence store. `PAPERCLIP_EXECUTION_DECISION: NO_GO` stands.
3. **No fork.** The narrow safety patches are offered upstream instead (report 09 §13/§17 A8); re-evaluate forking only under 09 §13's three joint conditions.

## Reactivation criteria (report 09 §16, binding)

Reopen only if **all** of: (a) upstream ships at least capabilities 1–4 of report 08 §17 (preventative read-only ACL; atomic create-as-paused; manual one-shot execution; OS-enforced immutable workspace); (b) a fresh installed-version audit passes; (c) a separately approved, disposable execution pilot is run. Additionally (report 12 §8 Q13): an execution-in-Paperclip need must exist that the Gatebraid external protocol cannot meet. Documentation alone is insufficient.

## Retained assets (already incorporated; report 12 §4F)

The 13-state workflow mapping (now the `Workflow` field option list); the exported role `AGENTS.md` bundles (→ subagent definition bodies, M2); sanitized-evidence discipline and provenance headers; the persistence-test and negative-write-probe methodology (reused in M3 validation); the single-writer read/compare/write/read pattern; the upstream security filings.

## Consequences

- Any impulse to restart, upgrade, or point Paperclip at a repository is out of scope for every Gatebraid milestone and requires reopening this ADR first.
