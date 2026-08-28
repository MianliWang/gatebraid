# Batch N1B — determinacy report for the 21 §6 items

**The addendum's rule: where the spec under-determines a fixture, stop on that
item and name the gap; never invent.** This report is that stop, item by item.
It is a finding about what is committed, not a request to relax anything.

**Result: 0 of 21 items are fully buildable tonight. 5 have a
schema-expressible half, and those halves are built** — BP-01, BP-02, BP-03,
IN-01 and IN-02, all carried in `evidence-capture-v1` and labelled there by
class. **16 items have no buildable half at all**: SP-01…SP-13, IN-03, IN-04,
IN-05. The three planned corpus directories are therefore **not created**;
`CORPORA.json` leaves them in `planned`, the only state that does not misreport
them.

> **This report's first draft said 3 half-built and 18 blocked, and both numbers
> were wrong.** The body already marked four items half-built, so the headline
> contradicted the table beneath it; and IN-02 was classified BLOCKED when three
> committed patterns express it. The internal review caught both. The corrected
> counts are above, and §5 records why the error was possible.

---

## 1. The structural cause, measured

`fixtures/run-corpus.py`, committed at blob `f64e3801`, has exactly one
assertion shape:

```
Draft202012Validator(schema).iter_errors(doc)
```

**It asserts that a document is valid or invalid against a JSON Schema, and
nothing else** — not that a tool returned `undecidable`, not that a process
failed closed, not that a digest re-derives, not that a coverage claim is
honest.

Every §6 state-pipeline expectation is a **tool outcome**. From the committed
`CORPUS-v1-PLAN.md` §2, the "Expected failure" column reads `undecidable;
non-zero exit surfaced`, `undecidable, fail closed`, `bounded-snapshot flag +
fail closed at the cap`. Those describe what `gatebraid-snapshot` /
`gatebraid-frontier` must **do**.

And no schema exists to validate a snapshot document against. The complete
committed set, measured:

```
gatebraid/consult@1           gatebraid/handoff@1     gatebraid/project@1
gatebraid/evidence-capture@1  gatebraid/metrics@1     gatebraid/slice@1
gatebraid/gate-run@1          gatebraid/phase@1       gatebraid/stage@1
gatebraid/gate-run@2
```

**None describes a snapshot document, a GitHub API response, or a validator
coverage report.** SP-10's own text — "missing snapshot schema/version" — names
a schema that does not exist; the item presupposes an artifact O0 will define.

Two things are missing before SP-01…SP-13 can be runnable fixtures: a
snapshot-document schema, and a runner assertion mode for tool behaviour.
**Neither is this batch's to create.** The binding clause is ADR-0029 decision
3's blocked-list, which scopes N1 as *"fixtures, `@2` admission and contract
reconciliation; **no tool implementation**"*. (An earlier draft grounded this on
`M3-PLAN.md` §2's clause forbidding **N2 and N3** from redefining a frozen
interface. That clause binds N2/N3; this is an N1 batch, and N1 is the phase
that *defines* interfaces. Right conclusion, wrong citation — the review
corrected it, and decision 3 is the stronger ground.)

---

## 2. Item-by-item

**Legend.** **BLOCKED** — no buildable half. **HALF-BUILT** — the
schema-expressible part is built in `evidence-capture-v1`; the remainder is
blocked and named. §3 carries the falsification case for every BLOCKED label.

### State pipeline — 13 items, all BLOCKED, one cause

| # | Item | Expected failure per the plan | Needs |
|---|---|---|---|
| SP-01 | auth failure | `undecidable`; non-zero exit surfaced | snapshot schema + behaviour assertion |
| SP-02 | permission failure | `undecidable`, fail closed | same |
| SP-03 | rate limit | `undecidable`; state named distinctly | same |
| SP-04 | network / server error | `undecidable`, fail closed | same |
| SP-05 | malformed GitHub response | `undecidable`; parse failure is a finding | same |
| SP-06 | missing dependency page | bounded flag + fail closed at cap | same |
| SP-07 | truncated connections | per-source integrity status | same |
| SP-08 | unknown Issue state | `undecidable`, never unblocked | same |
| SP-09 | non-Slice Project item | no verdict; excluded with reason | same |
| SP-10 | missing snapshot schema/version | refuse to consume | **the very schema it tests for** |
| SP-11 | one-direction dependency loss | both directions cross-checked | same |
| SP-12 | soft dependency unsatisfied | output states it did not parse | same |
| SP-13 | aborted item presented as ready | excluded per ADR-0025 §8 | same |

The input side is not the problem — a recorded API response is JSON and could be
written today. **The assertion side is.** Thirteen fixtures whose expectations no
committed instrument can evaluate would produce a corpus reporting `CORPUS
CLEAN` while asserting nothing, which is worse than an empty corpus because it
looks like coverage.

### Bytes / platform — 3 items, all HALF-BUILT

- **BP-01** cp936/UTF-8/em-dash round trip. **Built:** the `rendered` contract,
  as EC1-03, EC1-04, EC1-08, EC1-09, EC1-10, EC1-11, EC1-12, EC1-13 — with the
  cp936 rendering produced by letting the decode raise and recording CPython's
  own exception text and offset. **Blocked remainder:** "`sha256` over raw bytes
  fails to re-derive" — not expressible in JSON Schema, as
  `evidence-capture@1`'s own `data` description states, and belonging to N3's
  re-derivation.
- **BP-02** CRLF and lone CR. **Built:** the guard contract, as EC1-14 (guard
  reported as run *and* overridden) and EC1-15 (silence about the guard).
  **Blocked remainder:** "`byte_length` mismatch caught" — the same
  re-derivation class.
- **BP-03** Windows-vs-WSL divergence probe. **Built:** "a capture must name its
  platform", as EC1-33, and the platform enum as EC1-24. **Blocked remainder:**
  the item itself — "one platform's capture presented as covering both" — is a
  claim spanning **two documents**, and the runner validates one document
  against one schema. No committed artifact makes a dual-platform claim, so
  there is nothing to mutate.

### Instruments — 2 HALF-BUILT, 3 BLOCKED

- **IN-01** wrong pipeline exit code. **Built:** `form: shell` without
  `shell_semantics` (EC1-07), the declared-shell positive (EC1-02), and
  `exit_code_source` outside its enum (EC1-25). **Blocked remainder:** an
  instrument *interpreting* a pipeline exit code is N2/N3 behaviour.
- **IN-02** placeholder survives its own check. **HALF-BUILT — reclassified from
  BLOCKED at the internal review.** `CORPUS-v1-PLAN.md` §3 specifies the fixture
  as "a record containing `<sha>` where a hash belongs" and the expected failure
  as "placeholder detected; record rejected" — **a rejection verdict, which is
  exactly what this runner asserts.** Three committed patterns express it, and
  all three are now built: EC1-16 (`generator.source_sha256`), EC1-17
  (`inputs[].sha256`), EC1-18 (`outputs[].sha256`). **Blocked remainder:** the
  item's own wording is about *a check that failed to notice*, and no such
  checker is committed; a fixture asserting "the placeholder was not caught" has
  nothing to assert against. The schema half stands on its own regardless.
- **IN-03** checker self-reference — **BLOCKED.** Needs a detector whose output
  lands in evidence; none is committed. Its negative case must moreover "use a
  real instance and only its report is sanitized" (spec §4, ADR-0028 §3), which
  requires the detector to exist in order to produce the report.
- **IN-04** moved HEAD / mutable ref recorded as replayable — **BLOCKED.** The
  labels `replayable`, `deterministic` and `covered` appear in **no committed
  schema**; they are spec §4 / ADR-0028 §2 vocabulary for self-asserted row
  labels. The artifact that would carry them is N3's coverage report, whose own
  four classes — `structural`, `semantic`, `replayed`, `capture-trusted`
  (`M3-PLAN.md` §2 N3) — do not exist yet either. *(An earlier draft said
  `M3-PLAN.md` defines `replayable`/`deterministic`/`covered` as N3's four
  classes. It does not; the review corrected it.)*
- **IN-05** partial validator coverage claiming completeness — **BLOCKED.** N3's
  coverage report, as IN-04. N3 is blocked until N1 is delivered and approved,
  so the artifact cannot exist yet by design.

---

## 3. Falsification of the BLOCKED label (ADR-0028 §2)

BLOCKED and HALF-BUILT are classifications, and a classification is a claim
carrying its own falsification case. **The first draft issued 21 such claims
with no falsification case for any, which is exactly how IN-02 got through.**
The case is now run and recorded.

**The claim:** *no constraint in any committed schema can express this item.*
**The falsification:** a constraint search across all ten committed schemas —
**337 constraint sites** enumerated — plus a substring probe over each item's
vocabulary. The probe is **deliberately over-sensitive**: it searches whole
documents including `description` prose, so a real constraint cannot hide behind
wording. Every hit is then inspected.

| Item | Probe | Inspection |
|---|---|---|
| SP-01…SP-13 | flagged `snapshot` | prose in `gate-run-v2`'s description of the snapshot/frontier pair — **not a constraint**; label holds |
| IN-03 | no hits | holds |
| IN-04 | flagged `structural`, `semantic` | prose — "structurally REQUIRED" in a description; **not a constraint**; label holds |
| IN-05 | no hits | holds |
| BP-01 remainder | flagged `re-derive` | prose in the `data` description, which says the relation is *not* expressible; label holds |
| BP-02 / BP-03 / IN-01 remainders | no hits | hold |

**Positive control — the claim that was refutable.** Searching for
digest-shaped patterns returns ten sites, including
`evidence-capture.schema.json` `generator.source_sha256`, `inputs[].sha256`,
`outputs[].sha256` (`^[0-9a-f]{64}$`) and `gate-run-v2.schema.json` `base_sha`
(`^[0-9a-f]{40}$`). A digest-shaped pattern rejects a placeholder token.
**IN-02's BLOCKED label was refuted by its own falsification case, three greps
deep — and the first pass did not run it.**

---

## 4. What this means for N1's Accept-when

`M3-PLAN.md` §2 N1 requires "every §6 item exists as a fixture with an
expected-failure assertion". **On the committed instrument set that clause is
not satisfiable for 16 of 21 items**, and careful drafting does not close the
gap: the assertions are about tools N1 is forbidden to implement.

**Stated plainly, because §4 of the first draft came close to saying it and did
not:** `evidence-capture-v1` is **not a §6 item**, so this batch advances
`M3-PLAN.md` §2 N1's Accept-when **by zero items**. What it discharges is gap 3
of `CORPUS-v1-PLAN.md` §6's list — the third frozen interface's missing
fixtures.

Three readings, and the choice is the operator's and the coordinator's:

- **(a) Sequence it.** §6's state-pipeline items become fixtures at **O0**,
  where the snapshot schema is defined; the instrument items at **N3**, where
  the coverage report exists. Fixtures still precede the tool they test, since
  the O0 corpus lands before O0's implementation — the discipline the plan
  already requires of P's corpus-v2.
- **(b) Extend N1.** A snapshot-document schema and a behaviour-assertion mode
  are designed and frozen inside N1, and the 21 items built against them.
  **The first draft priced this as enlarging "N1's frozen-interface set beyond
  the three `M3-PLAN.md` §2 names", and the review showed that overstates it:**
  the runner is not one of the three, and `CORPUS-v1-PLAN.md` §5 already flags
  the runner's own classification as an open question for the operator. The real
  cost is a snapshot schema authored before O0 measures what it must describe.
- **(c) Extend the corpus by approved change — ADR-0029's own clause.** The
  first draft omitted this and it is the most on-point authority in the
  repository. ADR-0029's **Reopening conditions**, first bullet: *"Any measured
  failure class the N1 corpus cannot express — **extend the corpus by approved
  change before any tool relying on it advances**."* That is this situation
  exactly, it is committed, and it makes the route a governed one rather than a
  choice between reinterpreting an Accept-when and enlarging a phase.

The first draft bolded an endorsement of (a) while giving (b) three lines and no
steelman. That steer is withdrawn: **(c) is the committed route**, (a) is how
(c) would most naturally be sequenced, and (b) remains available at a cost the
operator should price rather than inherit from this report.

---

## 5. Why the first draft's error was possible

Recorded because the correction is the point. The first pass classified 21 items
and ran **no falsification case for any classification** — the very rule
(ADR-0028 §2) that `CORPUS-v1-PLAN.md` §5 applies to itself in bold, one file
away, when it says the runner's own non-instrument classification "is not
self-ratifying". Had §3's search been run first, IN-02 would have been caught by
this batch instead of by its reviewer, and the headline count would have been
consistent with the table beneath it.

**The transferable rule: a report whose deliverable is a refusal must falsify
the refusal, not only justify it.** A refusal is a claim like any other, and a
false refusal costs exactly what an invention costs — it just fails quietly
instead of loudly.

---

## 6. Adjudication addendum (coordinator, 2026-08-12) — two counts withdrawn, the probes made re-runnable

Recorded as a dated addendum, never a silent edit (metrics v2 §5's correction
rule). The item-by-item verdicts of §2 are **unchanged**; the coordinator
independently re-ran the delivered union corpus (55 passed, 0 failed, exit 0),
verified the runner's single assertion shape at blob `f64e3801` by code
inspection, and reproduced §3's inspections before ratifying them.

1. **Two quantitative claims in §3 are withdrawn as written**: "337 constraint
   sites" and the digest search "returns ten sites". Neither named the command
   that established it (metrics v2 §4: a claimed value names the command; the
   reader must be able to re-run what the writer relied on), and the
   coordinator's reproduction under a stated counting rule produced different
   totals — the numbers are not re-derivable from the record. The
   falsification's force never rested on them: it rests on the per-item probes
   and the positive control, both re-runnable below.
2. **Re-runnable probe commands**, run by the coordinator from the repository
   root at head `66700c83` over the ten committed schemas; counts are
   case-insensitive matching-line counts per file (`grep -ic`), zero-count
   files omitted:
   - `grep -icE 'snapshot' schema/*.json` → `gate-run-v2` 1; inspected: the
     `bootstrap_exception` description prose — not a constraint. The SP labels
     hold.
   - `grep -icE 'structural|semantic|replayab|covered|deterministic'
     schema/*.json` → `consult` 4, `evidence-capture` 5, `gate-run-v2` 3,
     `metrics` 2; inspected: description prose in every hit — no constraint
     carries the IN-04/IN-05 label vocabulary. The labels hold.
   - `grep -icE 're-deriv|rederiv' schema/*.json` → `evidence-capture` 2,
     `gate-run-v2` 1; inspected: the `data` description itself states the
     relation is not schema-expressible. The BP remainders hold.
   - **Positive control:** `grep -icE '\[0-9a-f\]\{(40|64)\}' schema/*.json` →
     `evidence-capture` 4, `gate-run-v2` 3 — the committed pattern constraints
     that refute IN-02's first-draft BLOCKED label, three of which are now
     killed by EC1-16/17/18.

---

## 7. Freeze addendum (batch O0-B1, 2026-08-23) — the thirteen are built

Recorded as a dated addendum, never a silent edit (metrics v2 §5's correction
rule, the form §6 already used). **§2's item-by-item verdicts are unchanged and
are not withdrawn.** They remain the accurate record of what was measurable at
N1B. What moves is their disposition: the thirteen state-pipeline items were
BLOCKED on an artifact that did not exist, that artifact now exists, and they
are frozen against it.

**Authority.** ADR-0031 decision 2's second freeze point — *"SP-01…SP-13 freeze
at O0's start, before O0's implementation, against the snapshot-document schema
O0 defines as its own first deliverable"* — executed under the operator's Batch
Approval on `MianliWang/gatebraid#14`, comment id `5386631542`, as batch O0-B1.

**What discharged the block.** §1 named two missing things and said neither was
N1's to create: a snapshot-document schema, and a runner assertion mode for tool
behaviour. **Only the first was built.** `schema/snapshot.schema.json`
(`gatebraid/snapshot@1`) landed first in the same batch, and the thirteen items
are asserted against it by the runner's existing single assertion shape — a
document is valid or invalid against a JSON Schema. **No new assertion mode was
added, and none was needed:** each item's tool outcome is expressed as a
property of the document the tool must emit, so "fail closed" becomes "a
document with a degraded source cannot carry a verdict other than
`undecidable`", and the existing runner kills it. §1's second gap is therefore
not closed but *dissolved* for these items; it stands for any future item whose
assertion genuinely spans two documents, which is exactly where IN-01 remains.

**Where they live.** `fixtures/state-pipeline/`, corpus version `v1.2`, thirteen
invalid cases plus four valid seed positives that are **not §6 items** and carry
no SP designation. Each of the thirteen kills on its own distinct ground:
measured across all five corpora, they add **zero** new (schema, locus-set)
collisions to the three already declared. Every locus was measured and then
independently re-derived by `fixtures/run-corpus.py`, which requires observed
and recorded sets to be equal in both directions.

**The corpus digest moved, by measurement and not to a target.** The frozen
value before this batch was
`f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686`, reproduced
on the pre-batch tree before any file was written. **At this batch's freeze,
measured on its final tree, the digest was**

```
73c5e059091982ac8cda43d9f59902f3934444b742e7a383ad9422448cd5fdfc
```

with `conditions failed: 0` and `seed-reachable surface UNMODIFIED: True`, from
`fixtures/runner-selftest.py`. That is the value as of this freeze and not a
claim about any later tree: a subsequent approved change inside the digest's
scope moves it, and the instrument's own output at a given commit is the
authority there. The scope gained `state-pipeline` here; this file's own
contents are not in it, which is why appending this addendum does not move the
value — verified by re-measuring after it was written rather than assumed.

**Where the twenty-one now stand.** Thirteen here; IN-03, IN-04, IN-05 and four
of the five HALF-BUILT remainders at N3's start (batch N1E, in
`fixtures/bytes-platform/` and `fixtures/instruments/`); **one item, IN-01, is
still frozen in neither place** — the N1E correct-course re-assigned it to
corpus v2 at P's start, because its assertion spans a coverage report and its
target's shell semantics and no single locus in one document expresses it. That
is ADR-0031's first reopening condition operating as designed, and the reason is
recorded in `fixtures/instruments/EXPECTATIONS.json`'s `known_limitation`. This
addendum does not restate it and does not change it.

**What this addendum does not claim.** It does not claim the thirteen assert
that the O0 tools *behave* correctly — no tool exists yet, which is the whole
point of fixtures-first. It claims that the document those tools must emit is
now specified, and that thirteen ways of emitting a document that lies about its
own integrity are now rejected before any tool is written to emit one. The
behavioural half is P2-S4's to demonstrate, against this corpus, and
`M3-PLAN.md` §2 O0's Accept-when is what will judge it.
