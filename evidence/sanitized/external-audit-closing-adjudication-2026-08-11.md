# External audit — closing (pre-merge) adjudication (2026-08-11)

**Source:** the same operator-commissioned external auditor (GPT-5.6),
third round: a closing read of PR #5 at head `32ec0283…` against base
`731f62aa…`, conducted over the coordinator's pre-merge review package
and the live PR. Verdict as issued: `CHANGES_REQUIRED / MERGE_READY: NO`,
eight blocking findings (B1–B8), an N0-D-specific table, and a required
N0-E planning-only correction round. **The raw relay is retained by the
operator, never committed:** `_handoff/audits/external-audit-gpt-closing-2026-08-11.md`
· SHA-256 `a88a08de71220f6402e148256351f40ff0670dc87cc87aa96c19421e630efb2b`.
The audit's substrate is likewise retained:
`_handoff/audits/GATEBRAID-PR5-REVIEW-PACKAGE.md` · SHA-256
`19ee341a419669f2506c9c5f753e7099a1ba2a996751cc229c66e3b0627747f4`
(byte counts recorded in the batch readback, per ADR-0029 decision 6(a)).
This sanitized adjudication is the committed record; it contains no
protected name.

**Adjudication method:** every finding independently verified by the
coordinator against the committed candidates, the recorded commit
series, and the coordinator's own artifacts before adoption (the
standing discipline, per templates/consult.md). **Sanitization
applied** (README rule 1): none — the relay contained no protected
name; findings are paraphrased for compression, not redaction.

| # | Finding (paraphrased) | Verdict | Verification | Enacted by |
|---|---|---|---|---|
| B1 | PR body still describes the N0-2 state (four files, one commit each); the review package's own header said "nine commits" against its own 4+5+4 process table and the live PR's 13 | **ACCEPT** | The commit series in the batch records sums 4+5+4=13; no batch instruction ever updated the PR body; the "nine" was the coordinator's hand count, refuted by the coordinator's own table | N0-E replaced the stale body with machine-derived tables; that body went stale again at N0-F (embedded state rots with every commit), so N0-G made the body state-invariant — no embedded counts, hashes or head; the PR's own Commits/Files tabs and the per-batch PR comments are the authoritative lists. Superseding correction of this cell, disclosed, N0-G |
| B2 | P1-1 adopted with no phase delivering `gate-run@2`; new M3 gate records would have no valid schema | **ACCEPT (placement adapted)** | M3-PLAN §2 as committed names no `@2` delivery home — confirmed. The audit's "N1/N2/N3 will generate gate records" is right for N2 and N3: ADR-0028 decision 4 lands each through its own gate. The coordinator's first version of this cell said the first M3 gate exit is O1's — wrong against that unsuperseded decision, withdrawn here (N0-F) | `@2` admitted at N1 as schema-with-fixtures; N2's and N3's gate landings write the first M3 gate records, as `@2` (M3-PLAN §2 N1; ADR-0029 P1-1 bullet). Superseding correction, disclosed (N0-I): this cell's original "no bootstrap exception needed" was overtaken by the final pass's C1 — the one-time expiring `bootstrap_exception` now governs those two landings |
| B3 | Metrics v2 not a repeatable instrument: §1's per-slice collection contradicts the per-batch metric (a slice-free batch records nothing), and the new metrics lack operational definitions | **ACCEPT** | Contradiction confirmed in the committed §1 vs §2 — introduced by the N0-D denominator repair (the #121 class, conceded); the missing-definitions list checked item by item, all absent | Metrics v2 §1 rewritten (collection loci by scope); new §5 fixes numerator, denominator, home, time, authority, zero-denominator, correction and aggregation per metric |
| B4 | Admission checklist items 1 and 10 have no producing phase; identity-drift window undefined | **ACCEPT** | Confirmed: no phase produced the three-slice series or install/uninstall/rollback; §7 item 8 named no window | New phase **V — Admission rehearsal** (three named-path scratch slices + install/uninstall/rollback), DAG extended; §7 items 1/8/10 bound to V and to the ADR-0024 instrumentation record; reconciliation rows added |
| B5 | "Raw stdout/stderr bytes" in JSON has no representation contract; the byte-boundary class would recur inside the evidence format | **ACCEPT** | Confirmed: N2's paragraph named no encoding | N2 byte representation contract: `{encoding: "base64", byte_length, sha256, data}`; decoded text derived-only with codec/result/error (M3-PLAN §2 N2) |
| B6 | N3's "re-derives verdicts from JSON + schemas alone" overstates: semantic re-derivation is not attestation of the capture event | **ACCEPT** | Confirmed against N3's committed text | N3 trust boundary stated; four-class coverage report (`structural`/`semantic`/`replayed`/`capture-trusted`); `replayable` never silently credited (M3-PLAN §2 N3) |
| B7 | Governance budget's "evidence never transported by hand" conflicts literally with decision 6's operator-relayed audit class | **ACCEPT** | Confirmed: both committed texts read as stated; the conflict was introduced when decision 6 landed without propagating scope to the budget (the #121 class, conceded) | Budget line 3 scoped to machine-verifiable evidence with the admitted human/relayed classes named beside it (M3-PLAN §5); ADR-0029 decision 5 now cites rather than restates the budget |
| B8 | N0's "planning only / no other path touched" excludes the `.gitignore` the PR ships; ignored `CLAUDE.md` is an unreviewable behavior surface | **ACCEPT** | Confirmed: N0's acceptance line predated the C5 hygiene commit and was never updated; `CLAUDE.md` risk as stated | N0 acceptance names the hygiene control; `CLAUDE.md` declared non-normative with a doctor baseline-conformance check at R-min (M3-PLAN §2) |

**N0-D table:** the four PASS verdicts recorded; the FAIL (metrics
collection locus) and both PARTIALs (budget conflict; status-transition
ambiguity) adopted and enacted as B3, B7, and the acceptance-event
clause in ADR-0029's Consequences (merge = acceptance; the Status edit
records it; N1 blocked until the reflection is verified).

**Answers adopted:** P1-1 now fully enacted (B2); the two
repair-inherits-burden instances conceded as coordinator defects
(friction-recorded); the eight missed-items list acknowledged — six were
missed by both internal reviews, two (package header, PR body) were
outside their given scope, which the N0-E review's whole-set scope
corrects.

**Overall disposition: PARTIAL** — all eight findings adopted on
verification, two with recorded adaptations (B2 placement at N1 rather
than a new phase or exception; B4 as one V phase rather than V plus
I-min); the audit's proposed task-prompt mechanics again replaced by the
project's established batch protocol. **Not adopted verbatim:** none
withheld on substance.

---

## Final-pass adjudication (appended at N0-H)

**Source:** the same external auditor's final pass over review package
v2 and PR #5 at head `27f09c76…`. Raw relay retained:
`_handoff/audits/external-audit-gpt-final-pass-2026-08-11.md` · SHA-256
`94cbfeb09228d11a21a88c81845df1a549883ec40a4bc954a7b8576aa43fe270`
(byte count in the batch readback, per decision 6(a)). **Sanitization
applied** (README rule 1): none — the relay contained no protected
name. **B1–B8: CLOSED**, accepted by the auditor as closed and not
reopened. **Final-pass verdict: CHANGES_REQUIRED**, four substantive
findings and two mechanics items, all adjudicated ACCEPT and enacted at
N0-H:

| # | Finding (paraphrased) | Verdict | Enacted at |
|---|---|---|---|
| C1 | N2/N3 need a startability authority before O0 — the fail-open snapshot/frontier pair cannot be it — and a bounded, expiring evidence bootstrap (no N3 validation exists before N3; records marked, excluded from V's series, exception dead after N2+N3 Gate 3); N1's non-Slice nature must be stated with grounds | **ACCEPT** | M3-PLAN §2 — the N2/N3 bootstrap-boundary block (closed-set state packet; `bootstrap_exception: true`; expiry) and N1's contract-batch statement; ADR-0029 P1-1 bullet cites the boundary |
| C2 | The three shared interfaces (`gate-run@2`, `evidence-capture@1` carrying the base64 contract, `metrics@1`) freeze at N1 before N2/N3 authoring; no implementer defines its own interface — supersedes the G-round assignment of the metrics format to N2, which had the generator authoring its own output contract (disclosed supersession) | **ACCEPT** | M3-PLAN §2 N1 (the three freezes; interface changes only via approved N1 correct-course); metrics v2 §5 (format fixed by `gatebraid/metrics@1`) |
| C3 | Host-instruction verification becomes a hard pre-N1 condition (enumerate loaded files, full hashes, operator approves or disables, drift stops the batch; R-min mechanizes later); ignore patterns root-anchored | **ACCEPT** | M3-PLAN §2 N1 (the hard precondition, with the non-normative-yet-runtime-affecting rationale); `.gitignore` (patterns anchored to `/_handoff/` and `/CLAUDE.md`; comment covers sibling instruction files — folding the queued F9 item, disclosed) |
| C4 | Slice metrics finalize at Gate 3 exit or operator-authored terminal disposition — never at Issue closure — giving aborted slices a committed final home; the three terminal states (`no_eligible_unit_ran`, `undefined_zero_denominator`, numeric zero) defined distinctly | **ACCEPT** | metrics v2 §5 (slice-scoped home finalization; the three-state rule in the common rules) |
| — | N2 ⟂ N3 is design/authorship independence; their Gate 2 executions serialize on the single-writer lease | **ACCEPT** | M3-PLAN §2 — the bootstrap-boundary block's closing sentence |
| — | This final-pass adjudication appended here, no eighth path | **ACCEPT** | This section |

**H6 seam-read disposition (appended at N0-I).** The seam read after
enactment returned four high findings, all verified at source. Three
sit in committed contract files outside this PR's seven-path set — the
Gate 0 contract's startability clause still naming the unhardened
frontier; the four evidence templates hard-coding `gate-run@1`; the
`approvals[].type` closed enum unable to carry the bootstrap's two
operator approvals — and are **scheduled, in writing, as N1's contract
reconciliation** (M3-PLAN §2 N1), performed under N1's own approval
before any gate runs; this PR's path set does not widen. The fourth was
a **recurrence of B1** — the PR body's round history went stale again —
and is the first live invocation of metrics v2 §3's alarm semantics:
adjudicated at the stop, ruling recorded, the body reduced to
pointer-only content so no round-mutable statement remains in it. Of
the ten remaining findings: seven enacted at N0-I (the unlock-home
precondition; `output_ref`/`bootstrap_exception` recordability;
interface validation in the implementers' own acceptance; the stale
post-date anchor; the preflight's exit-status form; the aborted-metrics
control-plane carriage; the terminal/result naming collision), one
scheduled into N1's reconciliation (ADR-0025 terminal-procedure
alignment), one recorded as intended behavior (the anchored ignore
rule's narrower scope — visible-untracked is the designed alarm state
for unexpected instruction files), and this cell's own supersession
closes the last.
