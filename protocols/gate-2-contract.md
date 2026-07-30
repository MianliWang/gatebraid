# Gate 2 contract — Implementation (single writer)

**Normative.** Inherits the common rules of `gatebraid-control-plane-spec-v1.md` §4. Changes only by ADR.

## Entry

- Recorded human `Plan Approval (G1→G2)` comment exists; `Next Approval` set back to `—`.
- `Writer Lease` taken (`<host>:<session-label>:<ISO8601>`); `Active Branch` created from `Base SHA`. Workflow → `Gate 2 — Implementing`.

## Actions

1. Implement **strictly inside the frozen allowlist** (`write_domains`, hash-pinned at Gate 1).
2. Small, frequent commits on `Active Branch` — **commits yes, push no**; publication is Gate 3.
3. Run the declared test plan; embed outputs in the evidence file (evidence, not assertion).
4. `/goal` is permitted only here (and in bounded Gate 0/1 evidence tasks), with the turn/time bound written inside the condition — never across an approval boundary.

## Repair sequence (unified, report 11 D6 — fixed)

red check → **repair 1 with a new hypothesis** → still red → **Codex consult** (`templates/consult.md`; embedded evidence; fixed response schema; recorded `ACCEPT/PARTIAL/REJECT`) → apply the independently-verified fix → still red → **repair 2** → still red → `Human Diagnosis Required`. `repair_limit = 2`; no third repair. `consult_first: true` moves the consult before repair 1. Blocker recurrence ≥2 for the same cause → `Human Diagnosis Required`, not another `Blocked` round.

## Mid-slice scope discovery

Follow `templates/gatebraid-correct-course.md`: stop → document the delta → `Next Approval = Scope / Allowlist Change` → human re-approval re-freezes plan + allowlist (new hashes recorded). **Never silently widen.**

## Prohibited

Touching files outside the allowlist; push/PR/merge; `git reset` / `git clean` / `git checkout` against baseline state; installing dependencies not in the approved plan; disabling hooks or checks; a second writer of any kind.

## Exit

- Tests green per the plan; `docs/evidence/gatebraid/<slice_id>/gate2.md` written from `templates/gate2-evidence.md` with verification outputs.
- Workflow → `Needs Review`; read-only reviewers pass → `Gate = G2 passed`, Workflow → `Needs Release Approval`, `needs-human` on.
