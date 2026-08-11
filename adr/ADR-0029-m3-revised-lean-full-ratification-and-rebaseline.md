# ADR-0029 — M3 Revised Lean Full: ratification and rebaseline

**Status:** Proposed · M3 (2026-08-11) · Product: Gatebraid (ADR-0010)
**Amends:** nothing retroactively — ADR-0028 and the frozen M2 metric
contract (`3a96b71`) are not edited.
**Provenance:** M2-CLOSURE.md at `731f62aa…`; ADR-0028; an external
read-only audit (GPT-5.6, 2026-08-10/11, operator-commissioned), adopted
with adaptations after independent line-level source verification by the
coordinator against `bin/gatebraid-snapshot.py` and
`bin/gatebraid-frontier.py` as committed; friction #60, #85, #92, #100,
#106, #108–#117; the sanitized adjudication at
`evidence/sanitized/external-audit-adjudication-2026-08-11.md`.

## Context

M2 closed at `731f62aa…` with an honest record: the delivery machine and
ADR-0011–0028 delivered; two scratch tools delivered with known defects;
three attempts at one tool terminated by evidence failures while the
implementation was never red; convergence unevaluable at two of three
end-to-end slices. ADR-0028 recorded the measured law and barred a fourth
ready attempt without a toolchain. The operator then commissioned an
external read-only audit of the whole system (two rounds), which
confirmed the coordinator's four verified P0 findings against the state
tools, judged ADR-0028's law over-broad as a universal claim, rejected
the early-business Express path, and proposed a revised M3 order. What
had to be decided: whether to ratify that revised path, under what
interpretation of ADR-0028, on what evidentiary footing for an audit
whose raw text cannot be committed, and how to rebaseline the original
M2/M3 scope formally rather than by reinterpretation.

## Decision

**1. Interpretation of ADR-0028 (historical text untouched).** ADR-0028
stands as the accepted M2 historical decision, in its own words. This ADR
fixes its operative reading for M3: its strong conclusion holds **within
the observed M2 workflow**. Operationalized: per-slice, ad-hoc
self-certification is prohibited as a source of trusted evidence;
committed, negative-case-falsified, independently validated, frozen and
reused tooling is the required control. This control **concentrates and
reduces** trust risk — into the toolchain's implementation, fixtures,
validator and environments — and does not claim to eliminate every
unexamined link. The residual is managed by N1's precommitted corpus,
N2/N3 independence, mutation testing, dual-platform runs, and version
freezing, not by assertion.

**2. External audit adopted, with verified provenance.** Adopted with
adaptations — overall disposition **PARTIAL** under the consult enum
(ACCEPT|PARTIAL|REJECT); the finding-by-finding verdicts, the recorded
adaptations and the not-adopted-verbatim list are in
`evidence/sanitized/external-audit-adjudication-2026-08-11.md`:

- **P0-1** `gh_rest()` folds every non-zero `gh` exit into `None`;
  dependency collection then silently omits the edge — fail-open on the
  control plane's input. Verified at source (lines 39–44 as committed).
- **P0-2** producer writes platform-encoded stdout
  (`ensure_ascii=False`), consumer forces UTF-8 — inconsistent byte
  contract. Supported by current source inspection and friction #60.
- **P0-3** snapshot completeness is asserted, not established (bounded
  connections without pagination outside Project items; the adjudication
  records the audit's over-broad flag phrasing). Verified at source.
- **P0-4** frontier retains implicit-allow and scope limits (unknown
  Issue state ≠ OPEN ⇒ treated unblocked; no snapshot version check; no
  Slice-identity filter; native `blocked_by` only). Verified at source;
  consistent with measured #85.
- **P1-1** new records require a future `gate-run@2`: full 40-hex SHAs,
  structurally required verified approval authors. `@1` history is not
  broken retroactively. (P1-2, the rebaseline, is enacted by decision 4;
  P1-3, the metric revision, by decision 5.)
- The previously offered **Express path is withdrawn**. State-reading
  tools that fail open disqualify any business contact regardless of
  schedule.

**3. The M3 path is Revised Lean Full, as defined in `M3-PLAN.md`.** The
phase definitions, acceptance criteria, dependency DAG, fixture catalog
and reconciliation table of `M3-PLAN.md` (committed at the repository
root in this PR) are ratified as the normative M3 authority; this ADR
cites and does not restate them — restatement creates a second copy
that drifts (ADR-0018 §3's rationale, applied here beyond that
decision's approval-term scope). Informative summary of
the order: N0 ratification (this batch; planning only) → N1 precommitted
fixture and mutation corpus → N2 evidence generator and N3 independent
evidence validator, in parallel and mutually implementation- and
authorship-independent → O0 snapshot/frontier state-pipeline hardening →
O1 fourth `gatebraid-ready` attempt → P guard and doctor → R-min minimum
host enforcement → Q-min minimum skills → M3 Core Closure.

Blocked until their prerequisites, by this decision: tool implementation
(until N0 is merged and N1 approved); the fourth ready attempt (until
N2 + N3 + O0 accepted); any business-repository contact (until the
admission checklist in `M3-PLAN.md` §7 is objectively met — first
contact is read-only Gate 0/Gate 1 under its own approval; any business
Gate 2 is a further separate approval).

**4. Rebaseline, stated plainly.** The original M2 plan (advisory
plugin, skill set, read-only subagents, consult wrappers, one real
read-only business-repo Gate 0/1) was superseded by measured
contract-machine work; the actual M2 delivered the delivery machine, two
scratch tools, the gate/evidence experiment, and ADR-0011–0028. This is
a rebaseline on real measurement, not a completion claim and not
concealment. Every deferred original deliverable is reassigned to a
named Revised-M3 (or post-M3) destination in `M3-PLAN.md` §3's
reconciliation table; planning statements superseded by this ADR are
listed in `M3-PLAN.md` §9.

**5. Metric v2 and governance budget.**
`protocols/convergence-metrics-v2.md` governs M3: four dimensions
(contract quality, evidence quality, delivery efficiency, product
quality); recurrence becomes an immediate alarm condition rather than a
permanent divergence verdict. The governance budget in `M3-PLAN.md` §5
is normative: zero new ADRs for ordinary friction items by default; the
two human doors remain exactly two; extra human round trips carry typed
exceptions; evidence is generated, never hand-narrated or transported; a
successful small slice trends toward 2–3 operator-attended work units;
friction entries have no normative force until promoted by an approved
committed change (ADR-0027 §3 restated as a budget line).

**6. External audits are an admitted evidence class, under these rules.**
An operator-commissioned external read-only audit by a non-Codex model
is admissible milestone-level evidence when and only when: (a) the raw
exchange is retained outside tracking (`_handoff/`), identified in the
committed record by filename and SHA-256 — the hash recomputed by the
executor from the file as supplied, the byte count measured and recorded
in the batch readback — and the audit's substrate document, where one
exists, is retained and identified the same way; (b) the committed
record is a sanitized adjudication under `evidence/sanitized/`
containing no protected name; (c) every adopted technical finding
carries independent verification provenance before adoption — the
verification discipline of `templates/consult.md`'s closing rule
(reproduce, never blind-apply) applies, while the Codex-specific
invocation, id and verbatim-response-commit mechanics do not, because
this class is an operator-relayed document, not a tool invocation;
(d) findings bind only through an operator-ratified ADR; (e) faithfulness
of the raw text is operator-attested — the operator conducted and
relayed the exchange. Residual, accepted: the raw text's content is
unverified by any independent reader, by design; the class trades that
residual for the protected-name rule.

## Consequences

- On merge, `M3-PLAN.md` and `protocols/convergence-metrics-v2.md`
  become normative, as their headers state; until merge, nothing in this
  PR is.
- This ADR's Status moves Proposed → Accepted in one announced
  post-merge commit — the refresh's only commit. `_handoff/M1-STATUS.md`
  and `CLAUDE.md` are refreshed on disk per their headers and stay
  uncommitted by rule (they are ignored paths; nothing in the refresh
  forces an ignored path into a commit), the refresh correcting their
  now-stale naming of the per-clone exclude file as the operative
  ignore mechanism.
- ADR-0028 is byte-unchanged; `protocols/convergence-metrics.md` (v1,
  frozen at `3a96b71`) remains the M2 historical instrument.
- The coordinator's pre-audit M3-PROPOSAL (session material) is
  superseded in full; the further superseded planning statements are
  enumerated in `M3-PLAN.md` §9.
- Tool implementation (N1) requires its own operator approval after the
  merge; the first business contact remains blocked behind `M3-PLAN.md`
  §7 (owner: operator).

## Reopening conditions

- Any measured failure class the N1 corpus cannot express — extend the
  corpus by approved change before any tool relying on it advances.
- The governance budget measurably suppressing a defect report — the
  budget yields to disclosure, and the clause is revised.
- A business-admission criterion found untestable as written.
