# ADR-0002 — Stage / Phase / Slice hierarchy with Gate 0–3 workflow

**Status:** Accepted · M1 (2026-07-29) · Product: Gatebraid, workflow profile **Gatebraid Classic** (profile id `classic`)
**Provenance:** the locked Gatebraid product spec; `protocols/gatebraid-control-plane-spec-v1.md` (normative for Workflow options, field option lists, views, Gate contracts); report 11 D6 (unified repair sequence); report 12 §9–§11.

## Context

Work must be decomposed so that a solo operator can plan, approve, execute, review, and release in bounded, auditable increments, with exactly two human approval doors per increment and full resumability from GitHub state alone.

## Decision

1. **Hierarchy.** `Stage` issues live in `MianliWang/gatebraid`; `Phase` issues are their sub-issues, also in `gatebraid`; `Slice` issues are Phase sub-issues living in the repository where the work happens (cross-repo sub-issues). A Slice is the unit of execution and approval. Identifiers: Stage `S<n>`, Phase `P<nn>`, Slice `P<nn>-S<nn>`.
2. **Gates.** Every Slice passes Gate 0 (authority & baseline, read-only) → Gate 1 (planning, read-only; plan + write allowlist frozen at exit) → Gate 2 (single-writer implementation under the frozen allowlist) → Gate 3 (human-approved publication). The two human approval doors are G1→G2 (`Needs Plan Approval`) and G2→G3 (`Needs Release Approval`).
3. **State.** The Project `Workflow` single-select (13 options) is the state authority (ADR-0008); the `Gate` field records the highest gate completed. There is **no stored `Ready` state** — readiness is derived by frontier logic, never stored (spec, design note).
4. **Repair sequence (unified, report 11 D6):** implementation → review → repair 1 (new hypothesis) → review → Codex consult (ACCEPT/PARTIAL/REJECT recorded) → repair 2 → review → `Human Diagnosis Required`. `repair_limit: 2`; `consult_first: true` moves the consult before repair 1.
5. **Gate contracts** for Gates 0–3 are the documents in `protocols/gate-0-contract.md` … `gate-3-contract.md`; they are normative and change only by ADR.
6. **Mid-slice scope discovery** follows `templates/gatebraid-correct-course.md`: stop, document the delta, human re-approval re-freezes plan and allowlist — never silently widen.

## Consequences

- A Slice issue is closed **iff** `Gate = G3 passed` — this invariant is what makes native blocked-by equal a Gate-3 dependency (ADR-0007).
- Every gate is resumable from the Issue + fields + committed evidence + Git state alone (ADR-0001 invariant).
- M1 creates the structures and documents only; no gate is executed in M1.
