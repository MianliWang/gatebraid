# CONSULT-19-01 — three self-referential defects in one Gate 2 evidence record

## Problem statement

`docs/evidence/gatebraid/P2-S6/gate2.md` is a Gate 2 evidence record. Review
item R3 requires that every record row's output reproduces and that the file
contains no content outside ADR-0026's classes. R3 failed once; repair 1
applied the two lawful treatments ADR-0028 decision 2 admits for a mutable
reference (pin it, or exclude it and say so). The re-review confirms the
reproduction limb now passes in full — **and finds three new defects, all of
one class: a statement the file makes about itself has gone false.** Two of
them were introduced by repair 1 itself.

Repair 2 is the **last** attempt in the contract's repair sequence. A third
does not exist; if R3 is still red afterwards the gate routes to
`Human Diagnosis Required`. The risk to be avoided is not "failing to fix
these three" — each is small — but **introducing a fourth defect of the same
class while fixing them**, which is exactly what repair 1 did.

## Constraints and forbidden operations

- **Record scope only.** Not one byte under `bin/`, `schema/` or `fixtures/`.
  The frozen allowlist is `bin/` + `docs/evidence/gatebraid/P2-S6/`, and this
  repair may write only inside the latter.
- No Project field write, no label change, **nothing pushed**. One record-only
  commit on branch `slice/P2-S6`.
- **You are read-only and author nothing in this tree.** Recommend; do not
  apply. The directory given by `-C` is a disposable copy, not the working
  repository.
- **ADR-0026 content classes** — the file may contain only: (a) the
  `## gatebraid-metadata` block; (b) record rows (a fixed label, a `$ command`
  line carrying its environment visibly, and that command's generated output,
  never transcribed); (c) the required disclosures; (d) template-fixed headings
  and row labels. No narrative prose outside those classes.
- **ADR-0028 decision 2** — no row may name `HEAD`, `git status`, or any state
  the act of recording it will move: a mutable reference is **pinned to a SHA**
  or **excluded from the deterministic subset and said so**.
- **ADR-0027** — a repair is measured before it is graded: an unchanged tree is
  not a repair.
- The superseded-marking convention this record already established: prose that
  was true when written and has been overtaken is **marked superseded**, not
  silently deleted.

## Files in scope

- `docs/evidence/gatebraid/P2-S6/gate2.md` — the record carrying all three
  defects.
- `docs/evidence/gatebraid/P2-S6/g2/render-gate2.py` — the renderer that
  generates that record from committed captures; the record is not hand-edited,
  so any fix is made here and re-rendered.

## Hypotheses already tried

| # | Hypothesis | Outcome |
|---|---|---|
| 1 | The record lacks decision 2's treatment for head-mutable rows and carries an unpinned diff base | **Repair 1.** Both limbs applied. The re-review confirms F-01, F-02 and F-03 repaired and the pinned row reproducing byte-identically. But repair 1 introduced G-02 and G-03 and missed G-01 — three defects of the self-reference class. |
| 2 | Within repair 1, the deterministic-subset statement listed the retained unpinned row `V7b` among rows "reproducing byte-identically" | Caught by re-measuring the claim rather than asserting it, and corrected in a second commit: `V7b` moved to the exclusion limb. This is the same class as G-01/G-02 and is why the class, not the instances, is the concern. |

## Embedded evidence

### The three findings, quoted verbatim from the re-review report

Source: `_handoff/batch-p2s6/REVIEW-P2S6-G2-REREVIEW.md`, sha256
`47bd2eb9956197e81cb1f4ad13efb3561e6449e9361dbf6b6bb2ff183ae6fda4`, 19,909
bytes. (That report is session material and is not in the tree you can read via
`-C`; it is quoted here in full for the parts that matter.)

**G-01 — material. The record contradicts itself on a machine-checkable
field.** A required-disclosure bullet still reads:

> Deviations: no repair sequence ran. Every declared command was green on
> its first run at this gate, so `repair_attempts` is empty and
> `repair_limit` is unspent. No Codex consult was needed or made.

The same file's metadata block carries `repair_attempts` with one entry
(`number: 1`, `result: green`), and the file carries a `### Repair 1`
block. `repair_limit` is 2 with one attempt spent, so it is not unspent
either. Both clauses of that sentence are now false.

This is not a matter of an append-only log read charitably: the repair
established the opposite convention in the very same pass. The F-03
disclosure explicitly marks its superseded prose — *"was true when
written and is superseded by this attempt rather than deleted as wrong"*
— so an **unmarked** statement reads as a live assertion. One bullet was
marked; this one was missed.

It is also the ADR-0026 §5 heuristic landing exactly where that ADR says
to look: *the fix for X is the first place to look for a fresh X*. The
repair updated the metadata and the Repair record and left the
disclosure asserting there was no repair.

**G-02 — material. `E4b` names a different commit than its label
claims.** The row's label reads *"the same commit named as a SHA rather
than reached through HEAD"*. But:

```
E4 recorded (via HEAD)              : 5386ce382bac5b4bc1c76a38bcbe86717adf9c1c
E4b names                           : 44906edc4d49cc090673a2220d3b66246b187bca
handoff_fingerprint.active_branch_head : 5386ce382bac5b4bc1c76a38bcbe86717adf9c1c
```

They are not the same commit. The nomination disclosure then relies on
this row: *"everything the fingerprint must SPECIFY is carried by rows
that do reproduce: E4b names the commit as a SHA, V9 derives its tree and
its changed-path set from pinned arguments."* `E4b` does not name the
fingerprint's commit, so it does not carry that identity.

**The protection itself is intact** — `V9` takes `5386ce38…` as its own
argument and derives tree `3f88cc11…` and the two-path changed set, which
genuinely ties the fingerprint commit to its content. What is wrong is
the row's label and the disclosure's attribution, not the underlying
specification.

**G-03 — minor, and pointed. `E4b`'s construction establishes nothing.**
`git rev-parse` on a bare 40-hex string echoes its argument without
consulting the object database. Measured on a SHA that does not exist in
this repository:

```
$ git rev-parse 0123456789abcdef0123456789abcdef01234567    → prints it, exit 0
$ git rev-parse 0123456789abcdef0123456789abcdef01234567^{commit}  → exit 128
$ git cat-file -e 0123456789abcdef0123456789abcdef01234567         → exit 1
```

So `E4b` would produce identical output for a commit that does not exist.
It asserts neither identity nor existence — which is precisely the
*"would echo its own argument and establish nothing"* construction the
record condemns one paragraph earlier as its reason for not pinning `E4`.
The same applies to the committed capture `G2-R1-failed-state-head.json`
and to the second command of the repair-1 novelty row. The novelty row's
**first** command, `…^{tree}`, does resolve the object and is sound —
that form is the available fix.

### The touched passages, quoted from the record as it now stands

`gate2.md` line 321 — the G-01 bullet, unmarked:

```
- Deviations: no repair sequence ran. Every declared command was green on its first run at this gate, so `repair_attempts` is empty and `repair_limit` is unspent. No Codex consult was needed or made.
```

`gate2.md` lines 44–49 — the `E4b` row carrying G-02 and G-03:

```
**E4b - the same commit named as a SHA rather than reached through HEAD, so the identity the row asserts is reproducible on its own**
```
$ git rev-parse 44906edc4d49cc090673a2220d3b66246b187bca
44906edc4d49cc090673a2220d3b66246b187bca
(exit 0)
```
```

The attribution clause inside the nomination disclosure, which G-02 says is
now false:

```
everything the fingerprint must SPECIFY is carried by rows that do reproduce: E4b names the commit as a SHA, V9 derives its tree and its changed-path set from pinned arguments.
```

### G-03 re-measured independently in this repository, before consulting

```
$ git rev-parse 0123456789abcdef0123456789abcdef01234567
0123456789abcdef0123456789abcdef01234567
  bare rev-parse exit=0
$ git rev-parse 0123456789abcdef0123456789abcdef01234567^{commit}
  ^{commit} exit=128
$ git cat-file -e 0123456789abcdef0123456789abcdef01234567
  cat-file -e exit=1
$ git rev-parse 44906edc4d49cc090673a2220d3b66246b187bca^{commit}
44906edc4d49cc090673a2220d3b66246b187bca
  real ^{commit} exit=0
```

The finding reproduces exactly: the bare form cannot distinguish an existing
commit from a fabricated SHA; both peel forms can.

### The relevant facts about the record's own commits

```
base (frozen)                       : 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
implementation-complete / fingerprint: 5386ce382bac5b4bc1c76a38bcbe86717adf9c1c
evidence commit (the reviewed state): 44906edc4d49cc090673a2220d3b66246b187bca
repair 1 commits                    : d1e9dd950d37e5756a920ffadc5ebdc78d55c468
                                      8d4fa4188c8fecc552448e1fff152e133abb3229 (current head)
tree at the reviewed state          : 4f2a6130bd2dd93f63380ffa220dd09c43ee153f
tree after repair 1                 : 4ba9e33170621dad043ef767ef9764f2b07d2cb8
```

`E4b` was intended to supply a reproducible name for the commit whose identity
`E4`'s excluded `HEAD` row asserts. `E4`'s recorded value is the fingerprint
commit `5386ce38…`; `E4b` names the evidence commit `44906edc…`, which is a
different commit and is not what the fingerprint specifies.

## Questions

1. **G-01.** Should the stale bullet be *marked superseded* (the convention
   this record established for its F-03 prose) or *corrected outright*? Which
   choice leaves fewer statements capable of going false later, given that the
   metadata block already carries the machine-readable truth?
2. **G-02.** What is the minimal correct treatment of `E4b`'s label and of the
   nomination disclosure's attribution clause, given that `E4b` names the
   evidence commit and the fingerprint identity is genuinely carried by `V9`?
3. **G-03.** Should `E4b`'s command be replaced with a verifying form
   (`^{commit}` peel, or `cat-file -e`), or should the row be removed entirely
   as establishing nothing that `V9` does not already establish? If replaced,
   which form, and what exactly does the new row then establish?
4. **The class.** Enumerate every prose claim in `gate2.md` that these three
   edits touch or create, each of which must be re-measured against the file
   and the repository as they will exist *after* the repair commit. What is the
   complete list, and what is the check for each?

## Required response schema

Respond in exactly this structure (`gatebraid/consult@1` `response`):
`findings` · `root_cause_hypotheses` (ranked, each with file-path evidence) ·
`recommended_change` (patch sketch as suggestion text — do not apply anything) ·
`risks` · `verification_steps` · `confidence` (low|medium|high).

## gatebraid-metadata

```yaml
schema: gatebraid/consult@1
consult_id: CONSULT-19-01
slice_id: P2-S6
trigger: repair-sequence
fingerprint_before: "slice/P2-S6 head 8d4fa4188c8fecc552448e1fff152e133abb3229, tree 4ba9e33170621dad043ef767ef9764f2b07d2cb8, base 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8"
request:
  problem: "Three self-referential defects in one Gate 2 evidence record must be corrected without creating a fourth of the same class."
  constraints:
    - "Record scope only: not one byte under bin/, schema/ or fixtures/."
    - "No Project field write, no label change, nothing pushed."
    - "The consultant is read-only and authors nothing in the tree."
    - "ADR-0026 content classes: metadata block, record rows, required disclosures, template-fixed headings only."
    - "ADR-0028 decision 2: a mutable reference is pinned to a SHA or excluded from the deterministic subset and said so."
  files_in_scope:
    - "docs/evidence/gatebraid/P2-S6/gate2.md"
    - "docs/evidence/gatebraid/P2-S6/g2/render-gate2.py"
  hypotheses_tried:
    - hypothesis: "The record lacks decision 2's treatment for head-mutable rows and carries an unpinned diff base."
      outcome: "Repair 1 applied both limbs. The reproduction limb passes in full; the re-review confirms F-01, F-02 and F-03 repaired. Three NEW defects of the self-reference class were introduced or left by that same repair."
  embedded_evidence: ["#embedded-evidence"]
  questions:
    - "For G-01, is marking the stale bullet superseded the correct fix, or should it be corrected outright, given the record's own established convention?"
    - "For G-02, what is the minimal correct label and attribution for E4b given it names the record-only commit and not the fingerprint commit?"
    - "For G-03, which command form actually verifies a commit's existence and identity, and should E4b be replaced or removed?"
    - "What is the complete set of prose claims in gate2.md that these edits touch or create, each of which must be re-measured after the commit?"
```
