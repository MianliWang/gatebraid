# ADR-0028 — Instruments are committed, falsified, and reused; M2 closes on that finding

**Status:** Accepted · M2 (2026-08-10) · Product: Gatebraid (ADR-0010)
**Amends:** spec §4 and ADR-0018 §2 (executed same batch); corrects ADR-0004's
instrument description **by reference** (ADR-0004 is frozen with the M1 set;
the precedent is ADR-0027 §4's treatment of ADR-0009). Closes milestone M2
(§5). ADR-0026 stands: its content classes held; what it could not reach is
what this ADR names.
**Provenance:** the three-attempt record at one scope — P1-S3, P1-S5, P1-S6:
twelve R3 failures across twelve reviews, the implementation
(`127fc5e87089f317e906df8ac31fe38ff41f53c3` at P1-S6, green in all four of
its reviews and never touched by any repair) red zero times; the P1-S6
instrument ladder (hand-authoring → write-path bytes → measurement domains →
temporal validity → classification semantics), one finite defect class
removed per round, one unexamined trust point remaining per round, ascending
one level per round; friction #111 (a check believed without ever being
shown able to fail), #112 (a checker quoting what it forbids), #113 (the
consult's written prediction adopted and then walked into); CONSULT-15-01
risks[4]; the K4 root conditional — committed before use, falsified with
negative instances before trust, reused unchanged — the only instrument in
the span with zero failures; RB-M2-J, RB-M2-L.

## Context

Three attempts at one scope produced the same result by three different
routes: correct work, uncertifiable record. Each attempt's evidence
instruments were authored beside the work they certified, and each
instrument carried exactly one point its author never examined — the point
moved up a level every time it was fixed. The record now supports a law
rather than a lesson: **a self-authored certification chain terminates in
an unexamined link.** Authoring instruments per slice restarts that
recursion per slice. The one instrument that never failed was the one that
was committed once, falsified before it was trusted, and reused without
rewrite.

## Decision

**1. A check is falsified once before it is trusted** (friction #111;
executed in spec §4 this batch). Before any check's pass is relied on — in
a gate, a generator, a validator, a review — it is run against an input
constructed to violate its property and required to fail, and the
demonstration is recorded beside its first use. A pass from a
never-falsified check is not evidence.

**2. A classification is a claim and carries a falsification case**
(friction #113; spec §4 this batch). A label a record asserts about its own
rows — replayable, deterministic, covered — is tested by a negative case
like any other check. No row names `HEAD`, `git status`, or any ref or
state that the act of recording it will move: mutable references are pinned
to SHAs or excluded from the deterministic subset.

**3. A checker never quotes what it forbids into a record** (friction #112;
spec §4 this batch). A detector whose output lands in evidence reports
findings by index and position; its negative case uses a real instance and
only its report is sanitized.

**4. Evidence instruments become committed, falsified, reused repository
tooling — and until that toolchain exists, this scope is not attempted
again.** The specification, for M3 (ADR-0009's zero-CLI-in-M2 stands; this
section is the mandate its M3 `bin/` line already reserves): an evidence
generator and validator as committed single-purpose scripts, each carrying
its own negative-case suite (decision 1 applied in repository form), landed
once through their own gate, then **used, never re-authored, by every
slice**. Named invariants from the measured failures: binary-mode writes
with a zero-lone-CR self-assertion as a guarded step (friction #108);
pinned-SHA inputs only (decision 2); self-test exercising the production
path, not a parallel one; assembly verified against the section list after
writing. A fourth attempt at the `gatebraid-ready` scope without this
toolchain re-runs the recursion and is not authorized by any standing text.

**5. Milestone M2 closes.** Delivered: P1-S1, P1-S2. Aborted, records
retained: P1-S3 (`344ae09`), P1-S5 (`9983a32`), P1-S6 (`0df5a88`), one
scope, all three local-only. Convergence-metrics §5 final reading, exactly
as the criterion is written: the convergence half ends **unevaluable** —
two end-to-end slices of the required three; the divergence half was **met
at P1-S5 on both independent grounds and again at P1-S6 by recurrence**
(ADR-0026 §1's first live application failing in the class it landed to
remove). The metric's own boundary is part of the finding: §3.1 counted
defects in the contracts, and what killed the slices was never in the
contracts. M2's deliverables are the delivery machine (ADR-0011–0027, the
gate contracts, schemas, templates), the two delivered slices, and this
measurement chain — ending in the specification decision 4 hands to M3.

**6. ADR-0004's instrument description is corrected by reference** (with
templates/consult.md, same batch): the consult sandbox constrains the
*model's commands*; the CLI itself maintains session state and has been
observed, from an interactive session, writing checkpoint refs
(`refs/codex/*`) into the repository named by `-C`; one measured run under
the contract invocation form produced zero such refs (friction #103 and its
CORRECTION). The disposable-copy rule from the P1-S6 ruling is standing:
`-C` points at a disposable full copy outside every governed repository,
deleted after capture — precaution under uncertainty. Gate 0's baseline and
Gate 3's drift check gain ref-namespace visibility (`git for-each-ref`)
so a write into an unwatched namespace cannot recur unseen.

## Consequences

- M3 opens with the instrument toolchain as its first delivery; the
  `gatebraid-ready` scope ships in M3 under it, from whichever retained
  branch M3's plan elects or afresh.
- The falsification rule applies to the toolchain's own suite first —
  decision 1 is what made the K4 conditional the span's only unfailed
  instrument, and it is now the admission bar for every instrument.
- The friction log (1–114 at closure) and the three retained branches are
  M2's measurement archive, cited by this ADR and the closure record.

## Reopening conditions

- Any slice attempt authoring a per-slice evidence instrument after this
  ADR — that is the recursion this ADR exists to end.
- The M3 toolchain's negative-case suite failing to catch a class this
  record already names (#108's bytes, #113's temporal validity, #112's
  self-reference) — the suite is wrong, not the law.
- A measured instance of the contract invocation form writing a
  `refs/codex/*` ref — §6's uncertainty resolves, and the consult text
  restates from measurement.
