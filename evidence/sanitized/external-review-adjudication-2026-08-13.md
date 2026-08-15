# Sanitized adjudication — external read-only review, M3 N1 corpus (2026-08-13)

**Class.** An operator-commissioned external read-only model review, admitted
under the ADR-0029 decision 6 pattern applied to a review rather than an audit:
the raw exchange is retained outside tracking under `_handoff/`, identified here
by filename, byte count and SHA-256; this sanitized adjudication is the committed
record; every adopted finding carries independent verification before adoption. **On binding, this class departs from the ADR:** decision 6 (d) reads *"findings bind only through an **operator-ratified ADR**"*; the commission substitutes coordinator adjudication plus operator approval for a review, and that substitution is the commission's, not the ADR's. Recorded here so the weaker rule is not read as decision 6's own. No protected name appears in
this document.

**Requirement satisfied.** `M3-PLAN.md` §2 N1's Accept-when: *"an external
read-only model review contributes negative cases not authored by the
implementer … recorded as externally contributed."* No internal review
substitutes, and the batch's own L1 round is not offered as one.

**Repository state reviewed.** `MianliWang/gatebraid` at
`e0e6783360d264f4b72e653553bfa6c6618a7469` — local `main` and `origin/main`,
144 tracked files.

---

## 1. Artifact identities

Byte counts and SHA-256 measured by the executor from the files as supplied
(ADR-0029 decision 6 (a)). All retained under `_handoff/audits/`, ignored, never
committed.

| Artifact | Bytes | SHA-256 |
|---|---|---|
| `REVIEW-COMMISSION-M3-N1.md` | 6,345 | `d864ecdb69b1cc6b73f0eb3f90d1f5c595972255757e0aca92772c765b34bda9` |
| `REVIEW-PACK-M3-N1.md` (the material sent) | 179,255 | `cf4376de3535cc84134f6a2c248dea70d8bb38a2bcf025e6df3647785c22ae55` |
| `external-review-m3-n1-report.md` | 10,724 | `476deee90a0caa911d813bb7427c5c169d4c5265b422a57a4cdaf3e2d234ac7b` |
| `external-review-m3-n1-verification.json` | 6,095 | `25b1dfa3b62afbd0b42f9929bdc5f6f17e35c5957d4605f61a709567fef0c85f` |

**The reviewer independently confirmed the pack's own integrity**: all 18
embedded files extracted programmatically, every stated byte count and SHA-256
matched, and all 17 stated git blob ids reproduced from the extracted bytes. The
reviewer's recorded pack SHA-256 equals the executor's.

**Two artifacts named in the build order were ABSENT at intake** and are recorded
as absent rather than assumed: the review ZIP (expected SHA-256
`88f2f6cbe31ad937fcfc60a8a21c5a8ec1f736224d8b3c772d32873677002332`) and
`external-review-m3-n1-fresh-raw.md`. Consequently **the seven adopted fixtures
were transcribed from the report's exact descriptions**, not taken byte-verbatim
from the ZIP, and each fixture's locus was then **re-measured on this host**
against the landed schemas. Where the ZIP later arrives, the transcriptions
should be diffed against it.

**Reviewer environment**, as recorded by the reviewer: Python 3.13.5,
`jsonschema` 4.26.0 — a different interpreter and a newer validator than this
host's CPython 3.12.2 / `jsonschema` 4.23.0. That the seven loci reproduce
across both is stronger evidence than either run alone.

---

## 2. Findings and dispositions — 18, all CONFIRMED

**18 findings: 7 contributed cases, 8 schema defects reproduced from 12 documents, 3 runner defects.** The build order's '22' counts the 12 defect documents individually and is a different unit; 22 is also the number of fixtures this batch first added, and the collision was worth removing. Every claim was reproduced independently before adoption (the `templates/consult.md` closing rule: reproduce, never blind-apply).

### 2.1 Seven contributed negative cases — ADOPTED

Each rejected by the landed schemas with exactly the reviewer's stated locus and
D6 schema path, re-measured on this host:

| ID | Class | Locus (re-measured) |
|---|---|---|
| GR2-11 | bootstrap exception omitting the `approvals` field | `required@(root):approvals` `[allOf/1/then/required]` |
| GR2-12 | the `blocked` arm of the stop_record conditional | `required@(root):stop_record` `[allOf/2/then/required]` |
| GR2-13 | gates never remediate — the interior assertion | `const@stop_record/remediation_attempted` |
| MT1-13 | `measured` requires a value, not only a command | `required@metrics/0:value` `[…allOf/0/then/required]` |
| MT1-14 | `undefined_zero_denominator` requires the denominator present | `required@metrics/0:denominator` `[…allOf/1/then/required]` |
| EC1-38 | an interior field of declared shell semantics | `required@invocation/shell_semantics:pipefail` |
| EC1-39 | output length rather than stream length | `minimum@outputs/0/byte_length` |

### 2.2 Eight schema defects — CONFIRMED, all repaired pre-freeze

Each was a document that **validated** against the landed schemas while explicit
contrary prose stood beside it.

| # | Defect | Disposition |
|---|---|---|
| F1 | `format: date-time` a no-op in `gate-run@2` (×3 fields) and `metrics@1` (×1) | RFC3339 lexical pattern applied, `format` removed, 4 killing fixtures |
| F2 | `measured` conflated with a zero denominator | conditional added, 1 killing fixture |
| F3 | metric value type untied to the metric name | per-family typing from metrics v2 §5, 2 killing fixtures (numeric and interval). **One name left unconstrained and escalated:** §5 places `evidence_only_abort_flag` in neither family — it says only "per-slice it is a flag" — and a branch asserting the base type would be inert, so none is written. Recorded in the metrics `known_limitation` and in Part A. |
| F4 | stop-record branch exclusivity prose-only | both exclusions **and** both requirements enforced, 4 killing fixtures |
| F5 | one metrics file could name two subjects | per-scope exclusivity, 1 killing fixture |
| F6 | an `argv` invocation could carry shell semantics | opposite branch added, 1 killing fixture |
| F7 | a required `decode_error` could be the empty string | `minLength: 1`, 1 killing fixture |
| F8 | repair-attempt cardinality and order unenforced | `maxItems: 2` + positional `number` via `$defs/repairAttempt`, 5 killing fixtures |

**F1 is the batch's most consequential finding.** The identical class was found
and closed on `evidence-capture@1` at N1C, one batch earlier, and **was not
propagated to the two sibling interfaces**. The N1C sheet scoped the
correct-course to one interface; the ruling that authorized it inherited that
scope; neither internal round questioned it. The external reviewer did.

**F4 and F8 required a grounding search before implementation**, per the build
order, and both were grounded in committed text, so both were implemented in
full rather than deferred to `known_limitation`:

- F4 — `protocols/gate-0-contract.md`: *"**Decidable** … `result: stopped`; set
  the matching `Next Approval`"* and *"**Error** … `Workflow = Blocked` with a
  typed `needs_input` reason"*. Both branches therefore have a required field and
  a forbidden one.
**F8's first repair was itself defective and the internal review measured it.** Setting `prefixItems` beside a sibling `items` orphaned the per-attempt schema — in JSON Schema 2020-12 `items` applies only past `prefixItems`, so with `maxItems: 2` every per-attempt constraint became unreachable and a repair attempt carrying neither a hypothesis nor a result validated. The item schema is now hoisted to `$defs/repairAttempt`, referenced from each position, with `items: false` closing the tail, and three further killing fixtures falsify the restored constraints rather than trusting them after restructuring.

- F8 — `protocols/gate-2-contract.md`: *"`repair_limit = 2`; no third repair"* — the emphasis is mine, the words are the contract's, with the D6 sequence fixing repair 1 before repair 2; the
  control-plane spec caps repairs at `repair_limit`; ADR-0002 §4 and
  `templates/slice.md` carry the same.

### 2.3 Three runner/selftest defects — CONFIRMED, all repaired

| # | Defect | Disposition |
|---|---|---|
| R1 | exact-locus equality could not distinguish one unexpected property from two — and D6's schema path does not repair it | `extra_count` added to `additionalProperties` observations; **multiplicity only, never the offending names or values** (spec §4, ADR-0028 §3); selftest seed S17 |
| R2 | `load_json` accepted `NaN`/`Infinity`/`-Infinity`, which RFC 8259 does not admit — a measured metrics value of `NaN` then validated as a number | `parse_constant` rejects them as a structure error, exit 2; seed S18 |
| R3 | the digest omitted `fixtures/run-corpus.py`, which S16 edits — an escape into the real runner would have left "surface UNMODIFIED" green | both scripts added to `digest_scope()`; direct sensitivity seeds S21/S22 |

**Numbering note.** `external-review-m3-n1-verification.json` labels these
`R1_nonfinite_json` and `R2_additional_properties_multiplicity` — **swapped
relative to the report and the build order**. This adjudication follows the
report's numbering, which the build order also uses. Recorded because two
supplied artifacts disagree and a silent choice between them is how a
mis-implementation happens.

---

## 3. Scope ruling

**FULL** — all review findings repaired before the corpus freeze, rather than
ingesting the seven cases and deferring the schema defects. The operator so
ruled. The reasoning on record: seven of the twelve schema-defect documents
target contracts whose prose already asserted the constraint, so freezing with
them open would freeze a corpus whose manifests describe enforcement that does
not exist.

---

## 4. Reviewer-declared boundaries, accepted

Read-only; no repository file edited, no dependency installed, no deferred
SP/IN §6 fixture authored, no live service called. **The Git repository itself
was not supplied**, so the declared commit, tracked-file count and git blob ids
were not independently fetched — the reviewer verified the pack's internal
consistency, not its correspondence to a repository it could not see. The
reviewer did not duplicate the disclosed EC1-28/29 collision or the queued D9
platform-collation defect.

---

## 5. Slots this document cannot fill

Named rather than composed, and escalated in the batch's approval sheet. Each is
coordinator-held and appears in no artifact on this host:

1. **The reviewer's isolation beyond the pack.** The commissioning half is NOT
   missing and is hashed in §1 above: `REVIEW-COMMISSION-M3-N1.md` fixes the
   mandate (§1), the exact reading list (§2), the ingestibility rules (§3) and the
   operator-executed relay mechanics (§5), and the report's own *Independence and
   scope* paragraph attests what the reviewer did not do and records that the Git
   repository was not supplied. What no artifact on this host records is **what
   other context the reviewer held and how it was excluded**. An earlier draft of
   this section claimed the whole protocol was absent — a composed absence, in the
   one section whose purpose is to avoid composing anything, caught at the
   internal review.
2. **The attempt-1 bounce and its classification** — the build order names it;
   no record of it exists in the commission, the report, the verification JSON,
   or any file under `_handoff/audits/`.
3. **The coordinator's own F8 first-probe construction error and its
   correction** — likewise named by the build order and likewise absent here.

The executor searched for all three and found nothing. They are left as slots
because inventing a protocol description or an incident narrative would be the
defect class this project has recorded six times running (#127–#132), and
because a sanitized adjudication is precisely the document where a composed
sentence would become durable.
