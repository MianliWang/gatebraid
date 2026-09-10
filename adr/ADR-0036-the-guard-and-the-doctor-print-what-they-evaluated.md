# ADR-0036 — The guard and the doctor print what they evaluated: two frozen interfaces, a closed exit set, and the rules node P promotes

**Status:** Proposed · M3 batch P-B1 (drafted 2026-09-10 by the coordinator on
the operator's word of 2026-09-09 to open node P with the corpus-v2 batch
first, and on the five rulings R1–R5 the operator gave with that word;
Accepted on the operator's Batch Approval of the P-B1 pull request and its
merge, which is also corpus v2's freeze commit) · Product: Gatebraid
(ADR-0010)
**Amends:** nothing retroactively. M3-PLAN.md §2 P is unedited; this ADR
records how its two tools are shaped before either is written, and promotes
two friction items into rules (§5.4 of the plan: a friction entry has no
normative force until an approved committed change promotes it).
**Provenance:** M3-PLAN.md §2 P (the twelve checks, the doctor's three
audits, the corpus-v2 freeze, the Accept-when); `fixtures/CORPUS-v1-PLAN.md`
§7 (corpus v2 at P's start); ADR-0031 (a node's output document schema is its
first deliverable; inexpressible items freeze where their instruments
exist); ADR-0028 §1–§3 (falsify first; classifications carry cases; a checker
never quotes what it forbids); ADR-0022, ADR-0024 (identity); friction #92
(the roster: `_handoff/friction-log.md` `### 92.`); friction #106 (the lease:
`### 106.`); friction #230 (the Human Diagnosis choreography wording, `###
230.`); the research note `claude/research-harness-2026-09-borrowable-designs.md`
§1 P1–P2 (three harnesses converging on a dry-run verdict tool that composes
the runtime's own evaluators, prints its normalised trace and exits with a
closed set of codes; a doctor whose findings carry a fix hint and whose
"never" list is written down) — cited as specification only, nothing
installed or executed; the operator's rulings R1–R5 of 2026-09-09, recorded
in the P-B1 brief §8 and repeated in the Batch Approval.

## Context

M3-PLAN.md §2 names node P's two tools by their checks and audits and says how
P begins: "§6's v1 catalog covers at most one of these twelve checks: P
therefore begins by extending the corpus (v2 — designed before guard
implementation, one negative case per check, frictions #92 and #106 entering
as cases, frozen by SHA) — fixtures still precede the tool they test."

The corpus runner asserts one thing: a document is valid or invalid against a
JSON schema, at recorded loci. A guard check is a judgment over host state,
which no schema evaluates. O0 met the same problem and ADR-0031 records the
route: the node defines its output document's schema first, and the corpus
asserts against that schema what the tool must never emit and what it must.
For the guard the schema is the verdict document itself. If the guard prints
the normalised facts it evaluated beside its per-check results, the schema's
conditionals can bind facts to results, and a document that reports a
violating fact beside a passing result is invalid. Each negative case is then
a verdict document a correct guard can never emit, runnable today; the other
half of every item — that the guard extracts the facts correctly from the raw
host readings — freezes where its instrument exists, at Slice P2-S7, by
replaying the same fixture's facts through the guard and comparing the verdict
(spec §4; ADR-0028 §1).

Three of the twelve checks had no written rule to bind, or a rule whose
disposition was not a stop: the roster half of check 1 existed only as
friction #92's suggested fix; check 3's contracts say a foreign ref is
"reported, not adopted" and never say deny; check 12's "hooks-enabled state"
had no definition anywhere, and the hooks it names are installed by R-min,
which follows P. Check 9 met a live wording disagreement (friction #230:
where remediation runs under Human Diagnosis). Check 8 met ADR-0015 §1's
sentence that "nothing downstream — including M3's guard — may treat comment
authorship as evidence of human intent", beside ADR-0020 §4's post-split
attribution. Each needed a decision before a fixture could record an expected
verdict. The operator gave the five rulings on 2026-09-09; this ADR is where
they become committed rule.

## Decision

**1. One evaluator.** Every guard check evaluates with the rule the gate
contracts already bind and, where a committed instrument implements that rule
(the closed-set sweep, the evidence validator, the frontier's candidacy
intersection), with that instrument's own code, never a re-implementation
beside it. The doctor reads the same documents the frontier and the gates
read. A rule enforced in two places is two rules; the corpus and the Slice
falsify one.

**2. The verdict document is the trace.** `gatebraid/guard-verdict@1`
(`schema/guard-verdict.schema.json`, frozen by this batch) is what
`bin/gatebraid-guard.py` emits at every pre-flight: the normalised facts it
evaluated, one group per check; exactly twelve `checks[]` entries, one per
check id in the plan's order, each with `result` in `pass | deny |
not_evaluated`, the governing `rule` by file and line, a `detail`, and a
`trace` from which the result can be disputed without re-running the guard;
a `verdict` in `allow | deny | not_evaluated`, `deny` if any check denied
(strictest wins); and `exit_code` in `0 | 1 | 2` — allow, deny, could not
evaluate — a closed set, because the exit status and not the printed text
decides whether the next command runs (spec §4). The schema binds facts to
results: a violating fact beside a passing result is invalid. A checker never
quotes what it forbids (ADR-0028 §3): an identifier outside the closed set, a
truncated SHA, a foreign ref name enter the document as counts and positions,
never as values, and the schema refuses a position that carries a name.

**3. The roster rule, promoted from friction #92.** Check 1 passes only when
the dedicated store (`GH_CONFIG_DIR` naming it, ADR-0024 §1) lists exactly one
account and it is the executor's, and the clone's git identity is the
executor's (ADR-0022 §1). The active pointer alone is not identity: a store
that lists the operator's account beside the executor's is a partition
delivered as a pointer, and one `gh auth switch` from every identity check
reading the wrong login and passing. Friction #92's measured output is the
corpus case (GV1-02).

**4. Ref namespaces (check 3) — operator ruling R2.** A ref outside
`refs/heads/`, `refs/remotes/` and `refs/tags/` that is absent from the
Slice's recorded Gate 0 baseline listing is a `deny`: the Slice introduced
it. One present at the baseline is the doctor's finding
(`refs.foreign_preexisting`), not the guard's deny — the contracts' "reported,
not adopted" — because a pre-existing ref is the host's state, not the
Slice's act, and denying it would block every Slice on a host that carries
one. Neither the guard nor the doctor adopts, deletes or rewrites a foreign
ref.

**5. Label coupling (check 9) — operator ruling R1.** The guard follows spec
§1's table as written: `needs-human` is on exactly when `Workflow` is one of
states 4, 9, 11, or state 10 with a `needs_input`-typed block reason, and off
otherwise. Four arms, four cases (GV1-10 to GV1-10d). Friction #230 — the
dispositions moved `Workflow` to `Gate 2 — Implementing` for a remediation
that ADR-0025 §4 says runs under `Human Diagnosis Required` — is a wording
disagreement between an ADR sentence and an executed procedure; it is settled
by a prose amendment to ADR-0025 in a text batch, and the guard does not
adjudicate it. Until then a remediation that shows `Gate 2 — Implementing`
with the label on is what the table says it is: a deny (GV1-10b).

**6. Hooks-enabled state (check 12) — operator ruling R3.** The check
compares the host's hook surface — the working clone's `core.hooksPath` and
the designated hook files, and the host agent's hook configuration entries
that invoke the guard — with a tracked baseline document that R-min authors.
While no baseline is tracked the check is `deny`, with that reason in its
trace (GV1-13). The guard is born fail-closed on this check and gates nothing
until R-min wires it into the host, so the deny blocks no Slice before then
and blocks every Slice after R-min until the baseline exists. A baseline that
is tracked and a host surface that does not match it is a deny (GV1-13b).

**7. The doctor never repairs.** `gatebraid/doctor-report@1`
(`schema/doctor-report.schema.json`, frozen by this batch) is what
`bin/gatebraid-doctor.py` emits: facts for its three audits — frontier
composition, closure preconditions, field invariants — beside `findings[]`,
each with `check_id`, `severity`, `message`, `path` and a `fix_hint`; an
`outcome` in `completed | could_not_run`; `exit_code` `0` no finding, `1`
findings, `2` could not run. The schema has no vocabulary for an action taken
and `additionalProperties` is false at every level, so a report that claims
to have changed anything is invalid (DR1-05). The doctor's own README at
P2-S7 lists what it never does, one line per excluded action. The
host-instruction conformance check M3-PLAN §2 R-min adds is reserved as
`host.instruction_divergence` and has no case until R-min.

**8. Approval author (check 8).** The guard's claim is ADR-0020 §4's and no
more: an approval authored by the operator's personal account is evidence the
executor did not write it. It is never evidence of human intent; ADR-0015 §1
stands. An approval authored by the executing session (friction #71), by a
third account, absent where the gate requires one, or not naming both hashes
(Gate 2) or the publication terms (Gate 3), is a deny (GV1-09 to GV1-09d),
and the observed author is recorded, never the expected one.

**9. Fixtures precede the tools, as ADR-0031 reads it.** Corpus v2 —
`fixtures/guard-v1/`, `fixtures/doctor-v1/`, `fixtures/gate-run-v3/`, the
three state-pipeline seeds — is frozen at this batch's merge commit, before
`bin/gatebraid-guard.py` or `bin/gatebraid-doctor.py` exists. The schema half
of every item is asserted by `fixtures/run-corpus.py` from the freeze; the
instrument half — that the guard's fact extraction from raw host readings is
correct — is falsified at P2-S7 against recorded readings and seeded
alterations (spec §4), and each check is shown failing on its corpus negative
case before its first trusted use (M3-PLAN §2 P Accept-when). P2-S7 may not
redefine either interface; an interface change returns to an approved
correct-course (the N1 rule).

**10. Justification under M3-PLAN §5.1.** Two public interfaces and one
changed invariant (the roster rule). One ADR, not three; the `gate-run@3`
revision that O0 owed is ADR-0037's because it is a different subject with its
own history.

## Consequences

- Node P's second act, Slice P2-S7, builds two tools against frozen interfaces
  and a frozen corpus, and its Gate 1 plan must name, per check, the
  instrument-half falsification (recorded readings, seeded alteration,
  expected verdict) before any check's pass is trusted.
- R-min owns the hook baseline document (decision 6), the three permission
  profiles, and the host-instruction conformance check; until R-min lands,
  the guard's check 12 denies and the guard gates nothing.
- ADR-0025 §4 owes a prose amendment for friction #230 (decision 5); the
  guard's verdict does not change when it lands unless spec §1's table does.
- The friction ledger's #92 and #106 are promoted; their entries stay as
  written and the corpus cases cite them.
- Nothing here authorises a tool, a run, a profile, a hook or a business
  repository. Approval mode Manual, the single writer, the closed set and the
  no-credential rule are unchanged.

## Reopening conditions

- A guard check found inexpressible against `gatebraid/guard-verdict@1` at
  P2-S7 — the facts it needs cannot be normalised into the document without
  quoting a forbidden value, or the schema cannot bind them — returns to an
  approved corpus change before P2-S7 advances (ADR-0031's route).
- A second implementation of a rule appearing beside the guard's (decision
  1), or a doctor path that mutates anything (decision 7).
- Spec §1's coupling table changing, or ADR-0025 §4's amendment landing with
  a table change, reopens decision 5's fixtures.
- R-min's hook baseline taking a shape decision 6's facts cannot describe.
