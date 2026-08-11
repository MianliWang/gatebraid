# External audit — sanitized adjudication (2026-08-11)

**Source:** an operator-commissioned external read-only audit (GPT-5.6),
two rounds (2026-08-10 initial findings; 2026-08-11 ruling), conducted
over the External Audit Pack and the repositories' state as available to
the auditor at control `731f62aa…`. **The raw audit texts are retained by
the operator, never committed** (standing rule: they reference
protected business-project names, which appear in no committed file).
Raw-artifact identity, recorded at N0 execution from the operator-
supplied file: `_handoff/audits/external-audit-gpt-raw-2026-08-11.md` ·
SHA-256 `f23495edd7032da26a48b3bbcbcbb9a1cc5c3281efc7b325635d049849d961d8`
· source: operator export of the external audit session. The audit's
substrate, the External Audit Pack, is likewise retained:
`_handoff/audits/GATEBRAID-AUDIT-PACK-2026-08-10.md` · 20,251 bytes ·
SHA-256 `33cecdaf5b644655ec2bbd9fc021d37ea9e045d9e7ffdbea6f13aba4ef0f6f2a`
(each hash recomputed by the executor from the file as retained). This
sanitized adjudication is the committed record; it contains no protected
name.

**Adjudication method:** every code-level finding was independently
verified by the coordinator against the committed sources on the
operator's disk before adoption (the project's standing
external-consultant discipline: independent verification before any
application, per templates/consult.md).

| # | Finding (paraphrased, sanitized) | Verdict | Verification |
|---|---|---|---|
| P0-1 | `gh_rest()` returns `None` on every non-zero `gh` exit (docstring claims 404/409 only); dependency collection silently omits edges — fail-open on control-plane input | **ACCEPT** | Source read: `bin/gatebraid-snapshot.py` lines 39–44 as committed; downstream `continue`-on-falsy confirmed |
| P0-2 | Producer emits platform-encoded stdout (`ensure_ascii=False`); consumer forces UTF-8 — inconsistent byte contract | **ACCEPT** | Source read: snapshot L324, frontier L171. **Provenance note:** supported by current source inspection and friction #60; the audit's attribution of this to the External Audit Pack's text was loose — the pack did not state it; the finding stands on the stronger ground |
| P0-3 | Snapshot completeness asserted, not established (bounded connections without pagination/truncation flags outside Project items) | **ACCEPT** | Source read: `labels(first: 20)`, `subIssues(first: 50)`, `views(first: 50)`; `pageInfo` on items only. In fairness (N0-3 review, verified against source at review): the audit's "without truncation flags" is broader than source — four bounded connections do emit `totalCount`, `views` among them; emitted but never compared to returned length, so the substance stands |
| P0-4 | Frontier implicit-allow and scope limits: unknown Issue state treated as not-OPEN ⇒ unblocked; no snapshot version check; no Slice-identity filter; native `blocked_by` only | **ACCEPT (substance)** | Source read; consistent with measured friction #85. Noted in fairness: direction values are validated fail-closed, and the tool's docstring honestly scopes its predicate; ADR-0025 §8 had already demoted its verdict to a dependency verdict |
| P0-5 | ADR-0028's "law" is over-broad as a universal claim; committed tooling concentrates rather than eliminates risk; toolchain needs fixtures-first, independent validator, mutation tests, dual-platform, external negative cases, freezing | **ACCEPT** | Adopted as ADR-0029 §1's interpretation; ADR-0028's historical text untouched |
| P0-6 | The Express path (early business pilot) is unsafe while reviewer read-only is mandate-not-enforcement and state tools fail open | **ACCEPT** | Express withdrawn (ADR-0029 §2); enforcement-minimum precedes any business contact |
| P1-1 | Schema permits 7–40-hex SHAs and optional approval author, conflicting with full-values and verified-author rules | **ACCEPT via versioning** | Verified in `schema/gate-run.schema.json` as committed; remedy is `gate-run@2` for new records (full 40-hex, or 40/64 if SHA-256 support arrives; author structurally required); `@1` history not retro-broken |
| P1-2 | Original M2 scope and actual M2 delivery diverged and must be formally rebaselined | **ACCEPT** | Reconciliation table in M3-PLAN §3 |
| P1-3 | v1 metric could not see the failure mode that terminated three slices; four-dimension metric needed | **ACCEPT** | `protocols/convergence-metrics-v2.md`; v1 frozen as the M2 historical instrument |
| — | Recurrence-as-permanent-divergence re-read as immediate alarm | **ACCEPT** | Metric v2 §3 |
| — | Governance ceremony requires a budget with exit criteria | **ACCEPT** | M3-PLAN §5 |
| — | Revised order N0→N1→N2→N3→O0→O1→P→R-min→Q-min | **ACCEPT (as refined)** | M3-PLAN §2; three adaptations: batch mechanics follow the project's established approval protocol; no committed document names a business repository — the post-closure pilot's authorizing document names its target, operator-authored, at authorization time; and the audit's linear N2 → N3 is refined to N1 → {N2 ⟂ N3} — a normative N2→N3 arrow would license authoring the validator with the generator in hand, which independence forbids |
| — | Blind-spot list (fail-open code; model-family correlation of implementer/reviewer/coordinator; optimizing certification over delivery; manual cross-window transport; identity isolation below OS level; no formal cross-platform matrix; roadmap drift; locally-retained branches unauditable externally) | **ACCEPT as standing risks** | Each is either addressed by a named M3 phase (O0, R-min, N1 dual-platform, §3 rebaseline) or recorded as residual (model-family correlation — mitigated by external audits at milestone closures and consult steps; retained-branch external auditability — inherent to ADR-0025 §3's unpublished-records design, recorded) |

**Overall disposition: PARTIAL** (the consult enum ACCEPT|PARTIAL|REJECT):
the code-level findings are adopted on independent source verification,
the process and planning findings by enactment in the ratified documents
— each row's Verification cell names which, with adaptations recorded
in-row. **Not adopted verbatim:** the audit's proposed task-prompt
mechanics (generic branch/PR instructions) — replaced by the project's
established batch protocol, which is stricter; its use of a protected
project name in the post-closure pilot recommendation — the
recommendation is adopted with the name removed per standing rule.
