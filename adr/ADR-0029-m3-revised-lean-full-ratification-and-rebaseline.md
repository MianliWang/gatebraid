# ADR-0029 — M3 Revised Lean Full: ratification and rebaseline

**Status:** Drafted for N0 (2026-08-11) · becomes Accepted only when the N0
draft PR is operator-merged · Product: Gatebraid (ADR-0010)
**Amends:** nothing retroactively. ADR-0028 is not edited. The M2 metric
contract (frozen at `3a96b71`) is not edited; `convergence-metrics-v2`
governs M3 forward. The coordinator's pre-audit M3-PROPOSAL (session
material) is superseded in full.
**Provenance:** M2-CLOSURE.md at `731f62aa…`; ADR-0028; an external
read-only audit (GPT-5.6, 2026-08-10/11, operator-commissioned), adopted
PARTIAL-ACCEPT after independent line-level source verification by the
coordinator against `bin/gatebraid-snapshot.py` and
`bin/gatebraid-frontier.py` as committed; friction #60, #85, #92, #100,
#106, #108–#117; the sanitized adjudication committed beside this ADR.

## 1. Interpretation of ADR-0028 (historical text untouched)

ADR-0028 stands as the accepted M2 historical decision, in its own words.
This ADR fixes its operative reading for M3: its strong conclusion holds
**within the observed M2 workflow**. Operationalized: per-slice, ad-hoc
self-certification is prohibited as a source of trusted evidence;
committed, negative-case-falsified, independently validated, frozen and
reused tooling is the required control. This control **concentrates and
reduces** trust risk — into the toolchain's implementation, fixtures,
validator and environments — and does not claim to eliminate every
unexamined link. The residual is managed by N1's precommitted corpus,
N2/N3 implementation independence, mutation testing, dual-platform runs,
and version freezing, not by assertion.

## 2. External audit adopted, with verified provenance

Adopted PARTIAL-ACCEPT (finding-by-finding record in
`evidence/sanitized/external-audit-adjudication-2026-08-11.md`):

- **P0-1** `gh_rest()` folds every non-zero `gh` exit into `None`;
  dependency collection then silently omits the edge — fail-open on the
  control plane's input. Verified at source (lines 39–44 as committed).
- **P0-2** producer writes platform-encoded stdout
  (`ensure_ascii=False`), consumer forces UTF-8 — inconsistent byte
  contract. Supported by current source inspection and friction #60.
- **P0-3** snapshot completeness is asserted, not established (bounded
  connections without pagination or truncation flags outside Project
  items). Verified at source.
- **P0-4** frontier retains implicit-allow and scope limits (unknown
  Issue state ≠ OPEN ⇒ treated unblocked; no snapshot version check; no
  Slice-identity filter; native `blocked_by` only). Verified at source;
  consistent with measured #85.
- **P1** new records require a future `gate-run@2`: full 40-hex SHAs,
  structurally required verified approval authors. `@1` history is not
  broken retroactively.
- The previously offered **Express path is withdrawn**. State-reading
  tools that fail open disqualify any business contact regardless of
  schedule.

## 3. The M3 path: Revised Lean Full

Order and gates, normative (full definitions, acceptance criteria and DAG
in `M3-PLAN.md`): **N0** ratification/rebaseline (this batch; planning
only) → **N1** precommitted fixture and mutation corpus → **N2** evidence
generator → **N3** independent evidence validator (implementation-
independent of N2; shared artifacts limited to frozen schemas/fixtures) →
**O0** snapshot/frontier state-pipeline hardening (fail-closed, explicit
UTF-8, completeness proofs, version/identity checks) → **O1** fourth
`gatebraid-ready` attempt (requires N2+N3+O0; success is metric-defined:
R3 first-pass, zero evidence-only repairs/aborts, all historical
mutations killed) → **P** guard and doctor → **R-min** minimum host
permission/hook and identity enforcement → **Q-min** minimum
status/Gate-0/Gate-1/handoff/consult skills → **M3 Core Closure**.

**Blocked until their prerequisites, by this ADR:** tool implementation
(until N0 is merged and N1 approved); the fourth ready attempt (until
N2+N3+O0 accepted); any business-repository contact (until the admission
checklist in `M3-PLAN.md` §7 is objectively met — first contact is
read-only Gate 0/Gate 1 under its own approval; any business Gate 2 is a
further separate approval).

## 4. Rebaseline, stated plainly

The original M2 plan (advisory plugin, skill set, read-only subagents,
consult wrappers, one real read-only business-repo Gate 0/1) was
superseded by measured contract-machine work; the actual M2 delivered the
delivery machine, two scratch tools, the gate/evidence experiment, and
ADR-0011–0028. This is a rebaseline on real measurement, not a completion
claim and not concealment. Every deferred original deliverable is
reassigned to a named Revised-M3 (or post-M3) destination in
`M3-PLAN.md` §3's reconciliation table; planning statements superseded by
this ADR are listed in `M3-PLAN.md` §9.

## 5. Metric v2 and governance budget

`protocols/convergence-metrics-v2.md` governs M3: four dimensions
(contract quality, evidence quality, delivery efficiency, product
quality); recurrence becomes an immediate alarm condition rather than a
permanent divergence verdict. The governance budget in `M3-PLAN.md` §5 is
normative: zero new ADRs for ordinary friction items by default; the two
human doors remain exactly two; extra human round trips carry typed
exceptions; evidence is generated, never hand-narrated or transported; a
successful small slice trends toward 2–3 operator-attended work units;
friction entries have no normative force until promoted by an approved
committed change (ADR-0027 §3 restated as a budget line).

## Reopening conditions

- Any measured failure class the N1 corpus cannot express — extend the
  corpus by approved change before any tool relying on it advances.
- The governance budget measurably suppressing a defect report — the
  budget yields to disclosure, and the clause is revised.
- A business-admission criterion found untestable as written.
