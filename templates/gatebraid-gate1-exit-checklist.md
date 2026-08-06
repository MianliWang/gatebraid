<!-- gatebraid-gate1-exit-checklist — adapted from BMAD-METHOD's
     implementation-readiness checklist (MIT © BMad Code, LLC; renamed per
     ADR-0010 — the BMAD trademark is not reused).
     Completed by the Lead at Gate 1 exit; its pass is a precondition of
     Workflow → Needs Plan Approval. Copy into the gate1 evidence file. -->

# Gatebraid Gate 1 exit checklist — <P_nn-S_nn>

Every item must be **checked with evidence** (anchor/link), not asserted.

## Plan completeness

- [ ] The approach is written and self-contained — an executor with only repo + plan could implement it
- [ ] The plan decomposes into 2–3 independently verifiable tasks (split the Slice if more)
- [ ] Every acceptance criterion in the Slice body maps to a declared test-plan command, named item by item
- [ ] Rollback note exists (how to abandon safely at any point)

## Allowlist exactness

- [ ] `write_domains` lists exactly the path prefixes the plan touches — nothing speculative
- [ ] No path outside the allowlist appears anywhere in the plan
- [ ] The allowlist hash is computed and recorded in the gate1 evidence yaml

## Test plan

- [ ] Every task has its verification command(s), and **each was dry-run on the slice's declared `environment`** — "runnable as written" means runnable *there*, not well-formed on inspection. Record that they ran; an item satisfiable by reading is not evidence-backed
- [ ] Expected-green criteria are stated (what output counts as pass)
- [ ] Test commands respect the project's prohibited-operations overlay, or the project declares none and the item is recorded `n/a`

## Dependencies and risk

- [ ] All `depends_on` entries re-checked against predecessors' current `Gate` field
- [ ] Risk notes cover the `risk` rating's justification
- [ ] `consult_first` considered and set deliberately for high-risk slices

## Freeze

- [ ] Plan frozen; `plan_hash` recorded
- [ ] Allowlist frozen; `allowlist_hash` recorded
- [ ] Team findings (if any) flushed to the Slice issue before team dissolution

**Exit:** all checked → `Gate = G1 passed`, Workflow → `Needs Plan Approval`,
`Next Approval = Plan Approval (G1→G2)`, `needs-human` ON. The recorded human
approval comment is the only door to Gate 2.
