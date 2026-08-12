# Gatebraid negative and mutation fixture corpus — v1 specification

**Authority.** `M3-PLAN.md` §6 is the catalog; this document is its build
specification and adds nothing to it. Where the two differ, §6 wins and this
file is corrected. Designed **before** any tool implementation, which is the
whole point: N2, N3 and O0 are written against a corpus that already exists and
already says what they must reject (`M3-PLAN.md` §2 N1).

**Freeze discipline.** This is the **v1** freeze, covering the state-pipeline,
byte/platform and instrument classes. Later phases extend it only by versioned,
approved freezes — corpus **v2** at P's start, one negative case per guard
check, with frictions #92 and #106 entering as cases — **never by unfrozen
additions**. The freeze is by commit SHA, recorded in the batch approval.

**Rule for every item.** One fixture, one mutation that a correct tool MUST
reject, and the expected failure recorded beside it. A mutation a tool rejects
*for a different reason than recorded* is **not** killed, and a fixture that
fails for four reasons where the corpus records one is **over-mutated** and is
also not a kill. The corpus records exact loci in both directions, and the
runner enforces set equality, because a validator can otherwise pass a
loosely-specified corpus by rejecting everything.

---

## 1. Layout

```
fixtures/
  CORPUS-v1-PLAN.md          this file
  CORPORA.json               the declared corpus set (§5)
  run-corpus.py              the runner (§5)
  runner-selftest.py         the runner's committed falsification (§5)
  gate-run-v2/               DELIVERED — 10 cases (§4)
    EXPECTATIONS.json
    *.json
  metrics-v1/                DELIVERED — 12 cases (§4)
    EXPECTATIONS.json
    *.json
  state-pipeline/            specified here, authored in N1 (§2)
  bytes-platform/            specified here, authored in N1 (§3)
  instruments/               specified here, authored in N1 (§3)
```

Every corpus directory carries its own `EXPECTATIONS.json` in the shape
`gate-run-v2/EXPECTATIONS.json` establishes, **and is declared in
`CORPORA.json`**. Discovery alone is not enough: a corpus landed without a
manifest, or a fixture file no case references, would otherwise be reported as
clean by a runner that simply never looked at it. Both are now structure errors.

**Status key:** **D** delivered in this batch · **S** specified here, fixture
authored in N1 under this batch's approval · **X** requires an input this batch
does not hold.

---

## 2. State pipeline — 13 items

Bind to **O0** (snapshot/frontier hardening). Fixtures are recorded API
responses and synthetic snapshot documents; **no fixture performs a live call**,
so the corpus is runnable offline and on both platforms. Every one derives from
a verified P0 finding (ADR-0029 decision 2) or a measured friction.

| # | §6 item | Fixture | Mutation the tool MUST reject | Expected failure | St |
|---|---|---|---|---|---|
| SP-01 | auth failure | `gh` exit 4, stderr auth message | response folded into `None` and treated as an empty edge set | `undecidable`; non-zero exit surfaced, never swallowed (P0-1) | S |
| SP-02 | permission failure | HTTP 403 with `Resource not accessible` | 403 read as "no such dependency" | `undecidable`, fail closed | S |
| SP-03 | rate limit | HTTP 403 + `X-RateLimit-Remaining: 0` | retry-less silent truncation of the result set | `undecidable`; rate-limit state named distinctly from permission | S |
| SP-04 | network / server error | HTTP 502 and a connection reset | partial result returned as complete | `undecidable`, fail closed | S |
| SP-05 | malformed GitHub response | valid HTTP 200, body not the expected JSON shape | parse exception caught and flattened to empty | `undecidable`; parse failure is a finding | S |
| SP-06 | missing dependency page | paginated `blocked_by` truncated after page 1 | page-1-only result reported as the full edge set | bounded-snapshot flag + fail closed at the cap (P0-3) | S |
| SP-07 | truncated labels / sub-issues / dependencies | connection with `hasNextPage: true` | completeness asserted without pagination | per-source integrity status says incomplete | S |
| SP-08 | unknown Issue state | Issue `state` outside the closed enum | unknown state ≠ OPEN treated as unblocked | `undecidable`, **never** unblocked (P0-4) | S |
| SP-09 | non-Slice Project item | Project item with no Slice metadata | a verdict emitted for a non-Slice row | no verdict; item excluded with reason | S |
| SP-10 | missing snapshot schema / version | snapshot document with no `schema` key | consumed as if current | refuse to consume; version check is mandatory (P0-4) | S |
| SP-11 | one-direction dependency loss | `#4 blocked_by #2` present, `#2 blocking #4` absent | one direction trusted without the cross-check | both directions cross-checked; mismatch is `undecidable` | S |
| SP-12 | soft Gate-1/Gate-2 dependency unsatisfied | declared soft dependency, unparsed | silent ignore | output states it did not parse the declaration | S |
| SP-13 | aborted item presented as ready | item with `Workflow = Aborted` in the candidate pool | Aborted item returned as startable | excluded per ADR-0025 §8's candidacy intersection | S |

**Note on SP-13.** The Ready Frontier is a dependency verdict, not a work queue
(ADR-0025 §8, from measured friction #85). `Workflow` and native dependency
state are independent surfaces, which is why the `Blocked` view is empty while
a slice carries a native blocked badge — correct, and load-bearing.

---

## 3. Bytes / platform — 3 items · Instruments — 5 items

Bind to **N2** and **N3**.

| # | §6 item | Fixture | Mutation the tool MUST reject | Expected failure | St |
|---|---|---|---|---|---|
| BP-01 | cp936 / UTF-8 / em-dash round trip | a stream of raw bytes containing U+2014 encoded UTF-8, captured on a cp936 console | decoded text stored as the authority; bytes discarded | `sha256` over raw bytes fails to re-derive; `rendered.decode_result` reads `replaced` with `decode_error` present | S |
| BP-02 | CRLF and lone CR | a stream with CRLF pairs and one lone CR | text-mode write silently rewriting LF→CRLF | `zero_lone_cr.count > 0` prevents the write; `byte_length` mismatch caught | S |
| BP-03 | Windows-vs-WSL divergence probe | the same command captured on both platforms | one platform's capture presented as covering both | a dual-platform claim reads two `platform` blocks or it is not made | S |
| IN-01 | wrong pipeline exit code (pipefail) | a pipeline whose first stage fails and last succeeds | exit 0 recorded as the command's status | `shell_semantics.pipefail: false` makes the code uninterpretable; `exit_code_source` must say what was measured | S |
| IN-02 | placeholder survives its own check | a record containing `<sha>` where a hash belongs | placeholder passes the completeness check | placeholder detected; record rejected | S |
| IN-03 | checker self-reference | a detector whose own output contains the token it forbids | detector's report quotes the forbidden token into evidence | findings reported by index and position only (spec §4, ADR-0028 §3) | S |
| IN-04 | moved HEAD / mutable ref recorded as replayable | a row naming `HEAD` and one naming `git status` | a mutable ref credited as `replayable` | classification refuted; mutable refs pinned to SHAs or excluded (spec §4, ADR-0028 §2) | S |
| IN-05 | partial validator coverage claiming completeness | a validator run skipping one section | coverage reported as complete | completeness report names the excluded section; a `replayable` claim is replayed or reported `capture-trusted`, never silently credited | S |

**BP-01 is not hypothetical on this host — it fired twice during this batch.**
While falsifying the corpus runner, the harness captured the runner's UTF-8
output using this host's default console codec (`gbk`/cp936) and raised
`UnicodeDecodeError` on byte `0x94`, the third byte of an em dash. That is BP-01
occurring in the act of building the corpus that catalogues it, and it is the
concrete reason `gatebraid/evidence-capture@1` carries raw bytes as base64 with
a **derived, explicitly non-authoritative** decoded view rather than storing
decoded text. `runner-selftest.py` now pins `encoding="utf-8"` on every
subprocess capture and says why in a comment beside the call. Recorded in the
batch readback at RB-M3-N1 §0.11 and as friction #127's sibling observation.

**IN-04 note.** `no row names HEAD, git status, or any ref or state that the act
of recording it will move` is spec §4 text. The fixture uses real instances and
sanitizes only the report, per IN-03's own rule.

---

## 4. Delivered corpora

### 4.1 `gate-run@2` — 10 cases

Expectations measured under CPython 3.12.2 / jsonschema 4.23.0 and recorded in
`EXPECTATIONS.json` with exact `(keyword, path)` loci.

| id | Fixture | Schema | Expect | Killed on | St |
|---|---|---|---|---|---|
| GR2-01 | `valid-at2-record.json` | `@2` | valid | — | D |
| GR2-02 | `at1-history-record.json` | `@1` | **valid** | — | D |
| GR2-03 | `at1-history-record.json` | `@2` | invalid | `const@schema`, `pattern@base_sha`, `required@approvals/0` | D |
| GR2-04 | `missing-approval-author.json` | `@2` | invalid | `required@approvals/0` | D |
| GR2-05 | `short-sha.json` | `@2` | invalid | `pattern@base_sha` | D |
| GR2-06 | `bootstrap-exception-without-state-packet-approval.json` | `@2` | invalid | `contains@approvals` | D |
| GR2-07 | `bootstrap-exception-with-state-packet-approval.json` | `@2` | **valid** | — | D |
| GR2-08 | `bootstrap-exception-missing-output-ref.json` | `@2` | invalid | `required@checks/0` | D |
| GR2-09 | `stopped-without-stop-record.json` | `@2` | invalid | `required@(root)` | D |
| GR2-10 | `two-repairs-no-consult.json` | `@2` | invalid | `const@result` | D |

GR2-02 and GR2-03 are **the same document under the two schemas**. ADR-0029
P1-1 promises `@1` history is not broken retroactively, and one file required to
pass as `@1` and fail as `@2` turns that promise into a falsifiable assertion
rather than a sentence.

**Three cases exceed the five §2 N1 enumerates**, each flagged in the approval:
GR2-06/GR2-08 falsify `@2`'s new `bootstrap_exception` conditional; GR2-09
falsifies a `stop_record` requirement `@1` stated in prose and enforced with
nothing. **GR2-07 and GR2-10 were added by the internal review**: GR2-07 because
a conditional exercised only by negative cases would pass them all by rejecting
everything, and GR2-10 because the `@1` #94 conditional was carried into `@2`
having never had a fixture in either schema.

### 4.2 `metrics@1` — 12 cases

This corpus exists **because the internal review found the schema had none**.
Its central three-result-state separation — which the schema itself calls "the
whole point of this schema" — was trusted having never been shown able to fail,
which ADR-0028 §1 forbids in one sentence.

| id | Class | Expect | Killed on |
|---|---|---|---|
| MT1-01 | all three result states in one file | valid | — |
| MT1-02 | slice finalized at terminal disposition | valid | — |
| MT1-03 | batch with no slice still records | valid | — |
| MT1-04 | milestone scope | valid | — |
| MT1-05 | `no_eligible_unit_ran` carrying a value | invalid | `not@metrics/0` |
| MT1-06 | a measured value with no command | invalid | `required@metrics/0` |
| MT1-07 | `undefined_zero_denominator` with a non-zero denominator | invalid | `const@metrics/0/denominator` |
| MT1-08 | `no_eligible_unit_ran` carrying counts | invalid | `not@metrics/0` |
| MT1-09 | slice scope with no finalization event | invalid | `required@(root)` |
| MT1-10 | `finalized` on a non-slice scope | invalid | `not@(root)` |
| MT1-11 | a milestone metric name in a gate-exit file | invalid | `enum@metrics/0/name` |
| MT1-12 | a metrics file that cannot name its subject | invalid | `required@subject` |

MT1-05 is the headline conflation metrics v2 §5 exists to forbid: a metric whose
unit never ran, reported as the number zero. MT1-11 validated cleanly before the
review, because the metric `name` was an unconstrained string — the one field
carrying the contract in the document whose purpose is that no generator defines
its own contract.

---

## 5. The runner, and its falsification

`fixtures/run-corpus.py` makes the expectations executable. It is **not** an
evidence instrument: it neither generates nor validates gate evidence, and it is
neither N2 nor N3. **Whether a committed runner is "tool implementation" under
ADR-0029 decision 3's blocked-list is a question for the operator, raised in the
batch approval — this paragraph is a classification, and a classification is a
claim (ADR-0028 §2), so it is not self-ratifying.**

Contract: `expect: valid` → zero errors; `expect: invalid` → observed loci
**equal** the recorded set, in both directions. Structure is asserted too: every
declared corpus exists and carries a manifest, every discovered corpus is
declared, and every fixture file is referenced by a case.

**Exit status decides, not the printed text.**
`0` every expectation held · `1` an **expectation** failed · `2` a
**corpus-structure or usage** error. The split is deliberate: "the corpus is
broken" and "the corpus caught something" are different findings, and one
non-zero code would conflate them.

**Falsified before first trusted use, by a committed program, not by prose.**
`fixtures/runner-selftest.py` seeds each condition into a throwaway copy of the
committed corpus, runs the real runner, and requires the recorded exit status.
It digests the corpus tree before and after and fails if they differ, so
"the real corpus was not touched" is measured rather than promised.

```
$ <python> fixtures/runner-selftest.py
```

| Case | Seeded condition | Required |
|---|---|---|
| S00 | untouched copy | `0`, `CORPUS CLEAN` |
| S01 | an invalid case's fixture repaired so it validates | `1`, `mutation not killed` |
| S02 | a recorded locus pointed somewhere it will not fire | `1`, `recorded locus did not fire` |
| S03 | a second defect added to a single-locus fixture | `1`, `unrecorded locus fired` |
| S04 | a valid case's fixture broken | `1`, `expected valid` |
| S05 | fixture file absent | `2`, `fixture missing` |
| S06 | schema file absent | `2`, `schema missing` |
| S07 | an invalid case recording no expected error | `2`, `records no expected error` |
| S08 | a fixture file referenced by no case | `2`, `referenced by no case` |
| S09 | an undeclared corpus directory | `2`, `not declared in CORPORA.json` |
| S10 | a malformed manifest | `2`, `not valid JSON` |
| S11 | an unexpected command-line argument | `2`, `unexpected argument` |

S02 and S03 are the two that matter most: together they are the difference
between a corpus that measures **kills** and one that measures only rejections.

**An earlier form of this section was a prose table asserting these results with
no re-runnable command and no recorded hash.** The internal review ruled it the
same hand-narration class the batch exists to end (ADR-0028 §1; M3-PLAN §5.3;
metrics v2 §4). It is recorded here because the correction is the point, not the
embarrassment.

---

## 6. What this batch does NOT hold

Stated plainly so no reader mistakes the plan for the delivery:

1. **The 21 fixtures of §2 and §3 are specified, not authored.** Marked **S**;
   built in N1 under this batch's approval. Only the two corpora in §4 are
   delivered.
2. **The external read-only model review has not run.** `M3-PLAN.md` §2 N1
   requires negative cases contributed by a reviewer who is not the implementer,
   recorded in the corpus **as externally contributed**. That input does not
   exist, and N1's Accept-when cannot be met without it. Marked **X**. Nothing
   in this batch may be read as satisfying it — the internal review round
   (lever L1) is a different thing and does not substitute for it.
3. **`gatebraid/evidence-capture@1` has no fixtures.** `gate-run@2` and
   `metrics@1` are now covered; the third frozen interface is not. Its byte
   contract is exercised only indirectly, through §3's BP/IN items, which are
   themselves unbuilt. A corpus directory `evidence-capture-v1/` is required
   before the freeze, on the same reasoning that produced §4.2.
4. **The corpus is therefore not frozen.** The freeze is by commit SHA and
   happens once §2, §3, gap 3 and the external contribution are all in.
   Freezing what is here would freeze an incomplete corpus and make the
   omission permanent.

---

## 7. Corpus versioning

- **v1** — this specification: state-pipeline, bytes/platform, instruments,
  plus the `gate-run@2` and `metrics@1` corpora. Frozen by commit SHA at N1's
  completion.
- **v2** — at **P**'s start, before guard implementation: one negative case per
  guard check, frictions #92 and #106 entering as cases, frozen by SHA before
  the tool that consumes it exists. §6's v1 catalog covers at most one of P's
  twelve checks, which is why P begins by extending the corpus rather than by
  writing the guard.
- Mutants adjudicated equivalent or invalid are reclassified **only** by an
  approved corpus change, recorded, and leave the mutation-kill-rate denominator
  from that freeze forward (`convergence-metrics-v2.md` §5).
