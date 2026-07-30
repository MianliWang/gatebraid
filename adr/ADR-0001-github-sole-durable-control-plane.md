# ADR-0001 — GitHub is the sole durable control plane

**Status:** Accepted · M1 (2026-07-29) · Product: Gatebraid (ADR-0010)
**Provenance:** report 09 §1/§11/§14 (Architecture B, GitHub consolidation); report 12 §1 (`GITHUB_STATE_DECISION: CONFIRMED`), §9 (recovery invariant); report 11 (verified GitHub primitives).

## Context

The operator runs six private business repositories from a solo, two-host (Windows + WSL) estate, with work executed by Claude Code (Lead) and Codex (read-only Consultant). Report 09 audited a local control-plane pilot (Paperclip) and found the dual-ledger, availability, and integrity costs decisive; report 12 re-confirmed GitHub as sole live authority after verifying the product limits the design depends on (50 options per single-select; 50 fields per Project including system fields; sub-issues cross-repo to 8 levels; native issue dependencies on the Free plan).

## Decision

1. **The only durable authorities are:** GitHub Issues, the private user-level GitHub Project "Mianli Engineering" (fields and views), sub-issue hierarchy, native issue dependencies, issue comments (checkpoints, approvals, handoffs), PRs/CI — plus files committed to `MianliWang/gatebraid`.
2. **Single-homing.** Every datum has exactly one writable home. Every other appearance is a link or an explicitly marked cache. On disagreement, the authority wins and the cache is corrected, never the reverse (report 09 §11 rules 1–2).
3. **Checkpoint flushing.** Chat sessions, task lists, and local scratch are working memory. Any outcome worth keeping is flushed to its authority layer at a checkpoint or it is deemed not to have happened (report 09 §11 rule 3).
4. **Recovery invariant.** A fresh session recovers any Slice's exact position from the Issue (body + comments), the Project fields, the committed Gate evidence, current Git state, and the project overlay — and from nothing else. Every local artifact is a disposable, regenerable cache (report 12 §9).
5. **No second ledger.** No local database, daemon, board, or manually-editable local task store may hold workflow state (report 12 §18).

## Consequences

- The control plane holds no filesystem paths and spawns nothing; it is environment-neutral across Windows/WSL and always available to mobile (report 09 §14).
- Provenance headers are mandatory on migrated or copied artifacts.
- Tooling (M2 skills, M3 scripts) reads GitHub state and computes; it never becomes a store.
