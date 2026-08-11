# M3-PLAN — Revised Lean Full (authority document; ratified by ADR-0029)

**Drafted for N0, 2026-08-11. Normative once the N0 draft PR is merged.
Committed at the repository root beside M2-CLOSURE.md. Changes only by
ADR. This document contains no protected business-repository name, by
standing rule; the pre-M1 authority documents that named one are
superseded on that point (§9).**

## 1. Mandate

Convert M2's measured findings into a reviewable, refusable, non-expanding
M3: harden the state pipeline, build the committed evidence toolchain,
repay the ready-scope debt, add guard/doctor, minimum enforcement, minimum
skills — then stop at a closure with objective business-admission
criteria. External audit findings P0-1…P0-4 are adopted with verified
provenance (ADR-0029 §2; sanitized adjudication in `evidence/sanitized/`).

## 2. Phases, acceptance criteria, DAG

Dependencies: `N0 → N1 → {N2, N3} → O0 → O1 → P → R-min → Q-min → V →
Closure` — with **N1 preceding both N2 and N3**; **N2 ⟂ N3**
(implementation- and authorship-independent — the discipline is defined
in N3's paragraph; shared artifacts limited to frozen schemas and the N1
corpus); **O0 consumes N1's state-pipeline fixtures**;
**O1 requires N2 + N3 + O0 accepted**; **P follows O1's measurements**;
**R-min follows P**; **Q-min wraps only stable tools**; **V consumes the
whole delivered stack and precedes Closure**.

**N0 — Ratification and rebaseline** (this package). Planning
documents, their evidence-directory records, and one repository-hygiene
control — nothing else. *Accept when:* the PR's path set equals exactly
these seven, verified by `git diff --name-only` against base at merge
time: `adr/ADR-0029-m3-revised-lean-full-ratification-and-rebaseline.md`;
`M3-PLAN.md`; `protocols/convergence-metrics-v2.md`; the two
`evidence/sanitized/external-audit-*adjudication-2026-08-11.md` records;
`evidence/sanitized/README.md` (brought current);
`.gitignore` (the reviewed hygiene control — it changes tracking
behaviour and is named for that reason); and the set is merged from a
reviewed draft PR.

**N1 — Precommitted fixture and mutation corpus.** The catalog in §6,
committed as runnable fixtures BEFORE any tool implementation; each
historical failure class carries at least one reproducing mutation; an
external read-only model review contributes negative cases not authored
by the implementer. N1 also admits **`gate-run@2`** — the P1-1 remedy's
delivery home: the schema lands with its own fixture set (a valid `@2`
record; an `@1`-shaped record rejected under `@2`; a missing approval
author rejected; a short SHA rejected; `@1` history still validating as
`@1`), fixtures-first like everything else in the corpus. N1 freezes,
before any N2/N3 authoring, all three shared interfaces:
`gatebraid/gate-run@2`; `gatebraid/evidence-capture@1`, carrying the
base64 byte contract N2's paragraph specifies — the contract is fixed
here, never by the generator that implements it; and
`gatebraid/metrics@1`, the metrics file's schema. N2 and N3 receive
only the frozen schemas and the corpus; neither may redefine an
interface during implementation — any interface change returns to an
approved N1 correct-course. **N1 is a contract batch under the
standing batch protocol, not a gated Slice:** it delivers schemas,
fixtures and mutations — test inputs with expected-failure assertions,
none of which executes in a production path — and its admission is the
batch's operator approval plus the independent read-only review this
paragraph already requires before freeze. **Hard precondition to N1's
start:** the executor enumerates the exact host instruction files the
session loads, records each file's full SHA-256, and the operator
approves or disables each; any later drift from the approved hashes
stops the batch. An ignored instruction file has no normative
authority, but a non-normative file can still affect runtime — that is
why this check precedes N1 and why R-min later mechanizes it. The
first M3 gate records are N2's and N3's own gate landings (ADR-0028
decision 4, which §9 does not supersede); N1 precedes both, so every
M3 gate record from the first is written as `@2` — no new M3 gate
record uses `@1`.
*Accept when:* every §6 item exists as a fixture with
an expected-failure assertion; the external review's contributed negative
cases are in the corpus, recorded as externally contributed; the
`gate-run@2` schema and its fixtures are in the frozen corpus; corpus is
frozen by commit SHA.

**N2 — Evidence generator.** Canonical output is structured JSON (raw
stdout/stderr bytes, exit code, argv, cwd identity, environment, input
SHAs, output hashes, timestamps); markdown is a derived view, never a
second hand-written authority. Executes argv-form by default; any shell
use declares platform and exit-code semantics. Binary writes; zero-lone-CR
self-assertion as a guarded step (#108). Byte representation contract
(the P0-2 class, fixed at specification, not left to the implementer):
each captured stream is carried as an object `{encoding: "base64",
byte_length, sha256, data}`; any human-readable rendering is a derived
field carrying `decode_codec`, `decode_result` and `decode_error`, never
authoritative; the JSON document itself is UTF-8 and no raw byte is ever
embedded directly in a JSON string. *Accept when:* all applicable N1
mutations are killed on Windows AND WSL; self-test exercises the
production path; landed once through its own gate (ADR-0028 decision 4);
version frozen at delivery.

**N3 — Independent evidence validator.** Re-derives verdicts from the
JSON + schemas alone; does not import N2 internals, and is not authored
from N2's source — the authoring sessions receive the frozen schemas and
the N1 corpus, never N2's implementation (ADR-0028's chain terminated in
an unexamined link by shared *authorship*, not shared imports); an
independent read-only review confirms both disciplines before freeze.
Full-file coverage with an explicit completeness report (no excluded
section — the review-4 lesson); verifies immutable SHAs, absence of
placeholders/self-reference/undeclared sections, byte/line-ending
discipline; runs the mutation suite. Trust boundary, stated: N3
independently re-derives record semantics from the captured evidence —
it does **not** independently attest that the capture event occurred as
described (that a command ran, in that cwd, with that unmodified
output). Its coverage report classifies every verified property as
`structural`, `semantic`, `replayed` (independently re-executed), or
`capture-trusted` (accepted on the generator's capture, labelled so);
a `replayable` claim is either replayed or reported `capture-trusted`,
never silently credited. *Accept when:* all applicable N1
mutations are killed independently of N2; a deliberately corrupted N2
output is rejected; dual-platform; the independence review (imports and
authorship) is on record; the coverage report classifies every verified
property into the four classes — a class may legitimately be empty —
with no unlabelled `replayable` credit; landed once through its own
gate (ADR-0028 decision 4); frozen at delivery.

**N2/N3 bootstrap boundary (one-time, expiring).** The known-fail-open
snapshot/frontier pair is **not** startability authority before O0.
N2's and N3's Gate 0 reads state through an **operator-approved
closed-set state packet**: the exact repositories and issues
enumerated; direct read-only queries only; every non-zero query exit
failing closed; no broad enumeration; exact outputs and query
identities recorded in the gate record. Their gate evidence runs under
a **bounded evidence bootstrap**: records are `gate-run@2`, marked
`bootstrap_exception: true`; they claim no N3 independent validation
before N3 exists — N2's records are re-validated by N3 after N3's own
Gate 3; bootstrap-marked records are excluded from V's admission
series; the exception expires at N2 + N3 Gate 3 completion, and no
later Slice may use it. N2 and N3 are DAG- and authorship-independent,
but their Gate 2 executions are **serialized by the single-writer
lease** — independence is of design and authorship, never of write
access.

**O0 — Snapshot/frontier hardening.** P0-1: fail closed on auth,
permission, rate-limit, network, server, parse and unexpected-endpoint
failures; per-source integrity status in the document. P0-2: explicit
UTF-8 binary stdout; producer/consumer byte contract stated and tested
with non-ASCII fixtures. P0-3: paginate every verdict-relevant connection
or emit bounded-snapshot flags and fail closed at any cap. P0-4: snapshot
schema/version required; Issue states validated against a closed enum
(unknown ⇒ undecidable, never unblocked); verdicts only for items
carrying Slice metadata; both dependency directions cross-checked;
declared soft dependencies parsed or the output says it did not; Aborted/
candidacy intersection per ADR-0025 §8; missing or incomplete data ⇒
`undecidable`. *Accept when:* all N1 state-pipeline fixtures pass;
`undecidable` demonstrably produced by each induced failure.

**O1 — Fourth `gatebraid-ready` attempt.** Same frozen scope; evidence
generated by N2, validated by N3, state read through O0 outputs. *Accept
when:* Gate 3 exit with `R3 first-pass = pass`, `evidence-only repairs =
0`, `evidence-only aborts = 0`, all historical mutations killed.
Implementation greenness alone is explicitly not the success criterion.

**P — Guard and doctor.** Guard (pre-flight, exit codes): executor
identity + full roster; closed repository set; ref namespaces; full-SHA
discipline; allowlist including untracked; writer lease; plan/allowlist
hash; approval author; label coupling; snapshot completeness flags;
repair-novelty floor; hooks-enabled state. Doctor: platform/configuration
audit (frontier composition, closure preconditions, field invariants);
reports, never repairs. §6's v1 catalog covers at most one of these
twelve checks: P therefore begins by extending the corpus (v2 — designed before
guard implementation, one negative case per check, frictions #92 and
#106 entering as cases, frozen by SHA) — fixtures still precede the tool
they test. *Accept when:* the corpus-v2 freeze precedes the guard
implementation in commit history; each check demonstrably fails on its
corpus negative case before first trusted use (spec §4).

**R-min — Minimum host enforcement.** Native permission denies; hooks
invoking guard; reviewer read-only enforcement to the extent the host
permits, the remainder recorded as typed residual risk; identity
enforcement beyond the active-pointer (separate OS profile evaluated;
outcome recorded either way). Host-local instruction state: `CLAUDE.md`
**and any sibling agent-instruction file** carry **no normative
authority** — committed contracts and the batch briefs bind, never an
untracked host file; doctor gains a check verifying them against a
tracked baseline template, every divergence reported, before any may
influence trusted execution. Operator present
for all configuration.
*Accept when:* each enforced rule is shown blocking a violating action in
a controlled test; the host-instruction conformance check demonstrably
reports a seeded divergence; residual-risk register committed.

**Q-min — Minimum skills.** Exactly: status, Gate 0, Gate 1, handoff,
consult. Skill-TDD mandatory; skills compute over state and never paste
state; each wraps only frozen tools. The fuller experience layer is
post-closure. *Accept when:* each skill's failing acceptance existed
before the skill and passes after, on both platforms.

**V — Admission rehearsal.** Three consecutive scratch end-to-end
slices, each on the full delivered stack (N2/N3 evidence, O0 state
reads, the O1-delivered `gatebraid-ready`, guard/doctor pre-flight,
R-min enforcement, Q-min skills), one
per §7-item-1 path: a clean pass; a repair; a blocked/decision path.
These three are §7's admission series (items 1–3 read from them); O1
does not count toward the series — it repays the ready debt under the
same stack but precedes P/R-min/Q-min. V also verifies §7 item 10:
install, uninstall and rollback of the complete M3 deliverable set
(scripts, hooks, skills, schemas) on a clean host profile, before/after
host state recorded. *Accept when:* the three slices close with §7's
item-2 and item-3 values; the install/uninstall/rollback run is recorded
with before/after state and restores the pre-install state exactly.

**M3 Core Closure.** *Accept when:* all prior acceptance criteria hold;
metric-v2 report published; closure record committed beside M2's; the
business-admission checklist (§7) evaluated line by line with evidence.

## 3. Scope reconciliation (rebaseline table)

| Original plan item | Original home | Actual M2 outcome | Revised destination |
|---|---|---|---|
| Advisory plugin shell | M2 | Not built | Post-M3 (experience layer) |
| Skill set — no committed record fixes the original plan's count; the committed clause on forward naming defers naming, not number: "skills/subagents named under the product convention when those milestones are tasked" — ADR-0010 Part II, Official names item 7 | M2 | Not built (5 skill specs prepared as session material, uncommitted) | Q-min (5 minimum) + post-M3 (remainder) |
| Read-only subagents — likewise no committed count (same clause, same deferral) | M2 | Reviewer/consult roles proven ad hoc | P/Q-min formalize the two load-bearing ones; rest post-M3 |
| Codex consult wrappers | M2 | Manual hermetic invocation proven | Q-min consult skill |
| Skill-TDD adoption | M2 | Unused (no skills built) | Q-min, mandatory |
| One real business-repo read-only Gate 0/1 | M2 | **Not attempted** (correctly, per closed-set rule) | Post-M3-Closure, first business contact, own approval |
| Contract machine, ADR-0011–0028 | (grew from M2 batch work) | Delivered | Standing |
| snapshot + frontier tools | M2 slices A/B | Delivered, with P0 defects | O0 hardening |
| ready tool | M2 slice C | 3 attempts, 3 terminals, implementation green | O1 |
| Guard/doctor/enforcement | M3 | Untouched (correctly) | P, R-min |
| Evidence toolchain | (not in any original plan) | Mandated by measurement (ADR-0028 §4) | N1–N3 |
| Install/uninstall/rollback verification | (not in any original plan — audit admission item 10) | Not attempted | V rehearsal |
| Admission slice series (clean/repair/blocked) | (not in any original plan — audit admission item 1) | Not attempted | V rehearsal |

## 4. Metric v2

Defined normatively in `protocols/convergence-metrics-v2.md`; v1 remains
the frozen M2 historical instrument. Headline change: recurrence is an
**immediate alarm** (stop, adjudicate, record) rather than a permanent
divergence verdict; success/admission read from the four-dimension set.

## 5. Governance budget (normative)

1. Zero new ADRs for an ordinary friction item, by default. An ADR is
   justified only by a changed invariant, permission boundary, public
   interface, or milestone authority.
2. Exactly two standing human doors. Every additional human round trip
   carries a typed exception naming its cause.
3. Machine-verifiable evidence — gate execution records, tool outputs,
   hashes — is generated by committed tools, never hand-narrated, never
   transported by hand between windows (the #100/#116 mechanism). Human
   approvals, operator decisions, and operator-relayed external audits
   are distinct admitted classes under their own provenance rules
   (ADR-0029 decision 6) — not exceptions to this line, and not covered
   by it.
4. Friction entries are a candidate queue with no normative force until
   promoted by an approved committed change (ADR-0027 §3).
5. A successful small slice trends toward 2–3 operator-attended work
   units; persistent exceedance is itself a metric-v2 signal, not a
   verdict.
6. The budget never suppresses disclosure: reporting a defect is always
   in budget.

## 6. Negative and mutation fixture catalog (N1's specification — designed before implementation)

**State pipeline:** auth failure; permission failure; rate limit;
network/server error; malformed GitHub response; missing dependency
page; truncated labels/sub-issues/dependencies; unknown Issue state;
non-Slice Project item; missing snapshot schema/version; one-direction
dependency loss; soft Gate-1/Gate-2 dependency unsatisfied; aborted item
presented as ready.
**Bytes and platform:** cp936/UTF-8/em-dash round trip; CRLF and lone CR;
Windows-vs-WSL divergence probes.
**Instruments:** wrong pipeline exit code (pipefail); placeholder
survives its own check; checker self-reference (quoting the forbidden
token); moved HEAD / mutable ref recorded as replayable; partial
validator coverage claiming completeness.
Each item: one fixture + one mutation that a correct tool MUST reject,
with the expected failure recorded beside it.
This is N1's v1 freeze, covering the state-pipeline, byte/platform and
instrument classes. Later phases extend it only by versioned, approved
freezes (corpus v2 at P's start, per §2) — never by unfrozen additions.

## 7. Business-admission checklist (evaluated at M3 Core Closure; no repository named here — the authorizing document names its target, operator-authored, at authorization time)

1. Three consecutive scratch end-to-end slices covering distinct paths
   (clean pass; repair; blocked/decision) — produced by V, which names
   them.
2. Evidence-only aborts = 0 across them.
3. R3 first-pass rate = 100% across them.
4. Every historical failure mutation killed by the toolchain.
5. Broader mutation-suite kill rate ≥ 90%.
6. Dependency/read errors 100% fail-closed (induced-failure test).
7. Toolchain green on Windows and WSL.
8. Three consecutive write batches with zero identity drift — evaluated
   over the three most recent write batches at Closure evaluation; the
   identity check has been recorded per write batch since ADR-0024, so
   instrumentation precedes any candidate window.
9. No open P0/P1 security finding.
10. Install/uninstall/rollback of the M3 deliverables verified — by V.
First contact: read-only Gate 0/Gate 1 only, under its own approval; any
business Gate 2 requires a further separate approval with this checklist
re-evaluated.

## 8. Execution mechanics

N0 lands via a dedicated branch and draft PR in the control repository,
merged only on explicit operator approval after independent read-only
review. Subsequent phases follow the established batch protocol
(pre-adjudicated approvals binding to announcements; blob-hash bindings
for coordinator-delivered files; the two doors always live). Raw external
audit texts are never committed; the committed record is the sanitized
adjudication with the raw artifact's identity and SHA-256.

## 9. Superseded planning statements

- The coordinator's pre-audit M3-PROPOSAL (both Full and Express paths)
  — superseded in full by ADR-0029 and this plan.
- Any pre-M1 authority statement naming a specific business repository
  as an M2/M3 pilot target — superseded as to the naming; the pilot
  itself is re-scoped to post-Closure under §7.
- The M2-era reading of recurrence as a permanent divergence verdict —
  superseded by metric v2's alarm semantics for M3 forward (v1 remains
  the historical record of M2 as measured).
- ADR-0028 §4's toolchain sketch — superseded by §2's N1–N3 definitions
  where they differ (fixtures-first as a distinct prior phase;
  generator/validator implementation independence made explicit).
  Explicitly NOT superseded and standing: decision 4's gate-landing of
  the generator and the validator, each once through its own gate —
  carried in N2's and N3's acceptance criteria above.
