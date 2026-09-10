# Gatebraid negative and mutation fixture corpus — v2 specification (node P's freeze)

**Authority.** `M3-PLAN.md` §2 P and §6 name this freeze: "corpus v2 at P's
start, one negative case per guard check, frictions #92 and #106 entering as
cases, frozen by SHA" — before the guard exists, "fixtures still precede the
tool they test". `CORPUS-v1-PLAN.md` §7 carries the same sentence. ADR-0031
supplies the route (a node's output-document schema is its first deliverable;
items the schema cannot express freeze where their instruments exist) and
ADR-0036 and ADR-0037 the decisions this corpus asserts. Where this file and
those differ, they win and this file is corrected by a dated addendum.

**Freeze discipline.** This is the **v2** freeze. It lands in one batch
(P-B1) whose merge commit is the freeze SHA, recorded in the operator's Batch
Approval and nowhere restated (a SHA copied into a second home drifts). Later
extensions take the same form — versioned, approved, never an unfrozen
addition — and the next named freeze is none: every `M3-PLAN.md` §6 item has
now reached a freeze point (§4 below).

**Rule for every item, unchanged from v1.** One fixture, one mutation a
correct tool MUST reject, the expected failure recorded beside it as exact
loci; the runner enforces set equality in both directions. New at v2, and
applied to every fact-to-result conditional: **one conditional per rule row,
one negative case per conditional, one positive arm per conditional** — the
positive arm is the same facts with the denying result, so a conditional can
be satisfied and not only violated (GR2-07's lesson, generalised).

---

## 1. Why a verdict document, and what the two halves are

The runner asserts one thing: a document is valid or invalid against a JSON
schema. A guard check is a judgment over host state. O0 met the same problem
(`DETERMINACY-REPORT.md` §1, §7): the node defined its output document's
schema first and the corpus asserted, against it, what the tool must never
emit. For the guard that document is its own verdict: the guard prints the
normalised facts it evaluated beside its per-check results, and the schema's
conditionals bind facts to results. **A verdict document that reports a
violating fact beside a passing result is invalid.** That is the schema half
of every item, asserted by `fixtures/run-corpus.py` from the freeze.

The **instrument half** — that `bin/gatebraid-guard.py` extracts these facts
correctly from raw host readings (`gh auth status`, `git for-each-ref`, the
Project's field values, the snapshot) — freezes where its instrument exists:
Slice P2-S7. Its Gate 1 plan names, per check, a recorded raw reading, a
seeded alteration and the expected verdict, and its Gate 2 shows each check
failing on that case before the check's pass is trusted (spec §4; ADR-0028
§1; `M3-PLAN.md` §2 P's Accept-when). The corpus cases below are the facts and
verdicts that falsification replays; the readings for three of them exist on
the record already (friction #92's `gh auth status` output; friction #106's
GraphQL response; friction #107's porcelain listing) and the rest are seeded
at P2-S7 from live readings.

Facts are counts, booleans and closed enumerations. The values the guard
forbids — an identifier outside the closed set, a truncated SHA, a foreign ref
name — never enter the document (ADR-0028 §3; GV1-18 refuses a position that
carries a name).

---

## 2. The twelve checks — rule, facts, cases, classification

Rules are named here by file and section; the `rule` strings the fixtures
carry cite them by file and line against `main` at
`880f342a0dee29f03aad14198cd09dabf15fcc9f` (the batch's base), re-verified by
the independent review. The sentence, not the number, is the rule.

| # | check id | governing rule | input facts (normalised) | negative cases | half asserted here |
|---|---|---|---|---|---|
| 1 | `identity` | ADR-0024 §1 (the dedicated store), ADR-0022 §1 and §4 (two surfaces; drift is a stop); the roster rule promoted from friction #92 by ADR-0036 decision 3 | `store_is_dedicated`, `active_is_executor`, `account_count`, `git_identity_is_executor` | GV1-01, 01b, 01c, 02 | the four flags to results; that `gh auth status` was read and counted correctly is P2-S7's |
| 2 | `closed_set` | `protocols/state-packet-queries-v1.md` ("no others, ever"; never enumerate); spec §4 (no unbounded identifier lists); the P2-S5 sweep instrument | `identifiers_examined`, `identifiers_outside_set`, `positions[]` | GV1-03 (GV1-18: no name in a position) | count to result; the sweep itself, and its residue rule for superseded `-pass` captures (ledger 238(e)), is P2-S7's with the guard's check 2 |
| 3 | `ref_namespaces` | `protocols/gate-0-contract.md` §Baseline ("reported, not adopted"); `gate-3-contract.md` (no ref the slice introduced); ADR-0028; ADR-0036 decision 4 (introduced → deny; pre-existing → doctor) | `baseline_recorded`, `foreign_refs_present`, `foreign_refs_introduced` | GV1-04; DR1-03d (pre-existing) | introduced count to result; the diff against the Gate 0 listing is P2-S7's |
| 4 | `full_sha` | ADR-0029 P1-1; ADR-0028 §2; `gate-1-contract.md` (64-hex hashes) | `fields_examined`, `fields_not_full` | GV1-05 | count to result; which fields (the Project's free-text Base SHA, approval citations) is P2-S7's |
| 5 | `allowlist` | `protocols/gate-2-contract.md` R1 (the diff a subset of `write_domains`; porcelain with `--untracked-files=all`; friction #107) | `frozen`, `diff_outside`, `untracked_outside` | GV1-06, 06b | counts to result; the subset computation is P2-S7's |
| 6 | `writer_lease` | ADR-0003 §1 (one writer; the field names it), consequences (a second writer is a stop); `gate-2-contract.md` entry; `gate-3-contract.md` exit 6; ADR-0025 §3; friction #106 | `workflow`, `writer_lease_present`, `lease_holders_in_repository`, `lease_names_this_session` | GV1-07 (#106), 07b, 07c | state and counts to result; the lease-holding states are 5, 6, 7, 8, 9, 11, 12 (Gate 2 entry to Gate 3 exit; Blocked is neither) |
| 7 | `plan_allowlist_hash` | `protocols/gate-1-contract.md` (the two recipes; row 6 "a hash that cannot be recomputed is decoration"; exit: the issue body matches; friction #65); ADR-0018 §3 | `plan_hash_reproduces`, `allowlist_hash_reproduces`, `issue_write_domains_match` | GV1-08, 08b, 08c | flags to result; the recomputation by the recorded command is P2-S7's |
| 8 | `approval_author` | `protocols/gate-2-contract.md` entry (a), (b), (c); `gate-3-contract.md` entry and "outside this table"; ADR-0020 §4 as ADR-0036 decision 8 phrases it; ADR-0015 §1 stands; friction #71 | `required`, `found`, `author_is_operator`, `author_is_executor`, `names_both_hashes` | GV1-09, 09b, 09c (#71), 09d | flags to result; locating the comment and reading its author is P2-S7's |
| 9 | `label_coupling` | spec §1's coupling table as written (states 4, 9, 11; Blocked with `needs_input`); ADR-0025 decision 5; ADR-0036 decision 5 (ruling R1; friction #230 is a prose amendment elsewhere) | `workflow`, `needs_human_present`, `blocked_reason_needs_input` | GV1-10, 10b (#230's shape), 10c, 10d | the table, all four arms; reading the label and the typed reason is P2-S7's |
| 10 | `snapshot_flags` | `M3-PLAN.md` §2 O0 P0-3/P0-4; `schema/snapshot.schema.json` `$defs/degradedSource` and the fail-closed conditional; `state-packet-queries-v1.md` (pagination) | `present`, `degraded_sources`, `verdict_consumed` | GV1-11, 11b | flags to result; counting degraded sources from the snapshot is P2-S7's (the snapshot corpus already kills the snapshot's own lies) |
| 11 | `repair_novelty` | `protocols/gate-2-contract.md` (ADR-0027 §1: an unchanged tree is not a repair; `still_red` + `(unchanged-tree)`); `templates/gate2-evidence.md` novelty rows | `attempts[] {number, tree_unchanged, result}` | GV1-12 | the floor; the tree comparison is P2-S7's; "new hypothesis" beyond the tree floor has no mechanical definition and none is claimed |
| 12 | `hooks_enabled` | ADR-0036 decision 6 (ruling R3: compare with a tracked baseline R-min authors; no baseline → deny); `gate-2-contract.md` prohibitions ("disabling hooks or checks") | `baseline_tracked`, `matches_baseline` | GV1-13 (no baseline), 13b | flags to result; reading the host's hook surface is P2-S7's, and the baseline is R-min's |

Every check's negative case is a verdict document with the violating fact and
`result: pass` on that check; its positive arm (`GV1-nnp`) is the same facts
with `result: deny`, `verdict: deny`, `exit_code: 1`, a non-empty `detail` and
`trace`. The structural cases assert the document's own rules: strictest wins
(GV1-14, GV1-19b), full coverage (GV1-15, one case per missing id), the
closed exit set (GV1-16, one per verdict), `not_evaluated`'s two conditions
(GV1-19, GV1-19b), a deny disputable from its trace (GV1-17), and no quoted
value (GV1-18). Every `allOf` entry of every schema names its case in its
`$comment`, and the review's neutralisation table (G3) is where that claim
is measured.

---

## 3. The corpora

### 3.1 `guard-v1` — `gatebraid/guard-verdict@1` — 79 files, 78 cases

| id | class | expect |
|---|---|---|
| GV1-00 | canonical allow: twelve `pass`, `verdict allow`, `exit_code 0` | valid |
| GV1-01 · 01b · 01c · 02 | check 1: store not dedicated · active login not the executor's · git identity not the executor's · roster of two (friction #92) | invalid, each with its `p` twin valid |
| GV1-03 | check 2: one identifier outside the set (count and position only) | invalid + twin |
| GV1-04 | check 3: a foreign ref introduced since the Gate 0 baseline | invalid + twin |
| GV1-05 | check 4: a SHA-bearing field not the full object name | invalid + twin |
| GV1-06 · 06b | check 5: a changed path outside `write_domains` · four untracked paths outside (friction #107) | invalid + twins |
| GV1-07 · 07b · 07c | check 6: inside the gate with no lease (friction #106) · two holders · a lease after Aborted | invalid + twins |
| GV1-08 · 08b · 08c | check 7: `plan_hash` · `allowlist_hash` does not recompute · issue body differs | invalid + twins |
| GV1-09 · 09b · 09c · 09d | check 8: no approval where required · a third account · the executor as author (friction #71) · neither hash named | invalid + twins |
| GV1-10 · 10b · 10c · 10d | check 9: label off in state 4 · label on in state 5 (friction #230's shape) · Blocked, label on, reason not `needs_input` · Blocked, label off, reason `needs_input` | invalid + twins |
| GV1-11 · 11b | check 10: no snapshot · a degraded source beside a `startable` verdict | invalid + twins |
| GV1-12 | check 11: repair 1 with an unchanged tree recorded `green` | invalid + twin |
| GV1-13 · 13b | check 12: no baseline tracked · host does not match the baseline | invalid + twins |
| GV1-14 · 15-`<id>` (twelve) · 16-allow · 16-deny · 16-not_evaluated (+ its `p` twin valid) · 17 · 18 · 19 · 19b | structure: `allow` beside a `deny` · eleven checks, each id missing in turn · `allow` with exit 1 · `deny` with exit 0 · `not_evaluated` with exit 0 · a `deny` with no trace · a position carrying a name · `not_evaluated` while every check passed · `not_evaluated` beside a `deny` | invalid |

### 3.2 `doctor-v1` — `gatebraid/doctor-report@1` — 24 files, 23 cases

| id | audit | fact beside an empty `findings[]` | expect |
|---|---|---|---|
| DR1-00 | — | clean report, exit 0 | valid |
| DR1-01 | frontier composition | an `Aborted` candidate (SP-13's shape; ADR-0025 §8) | invalid + twin |
| DR1-02 · 02b · 02c | closure preconditions | `Auto-close issue` enabled · a closing issue reference · a closing keyword before an issue reference (ADR-0018 §1) | invalid + twins |
| DR1-03 · 03b · 03c | field invariants | a Slice item with `Next Approval` unset · a CLOSED issue with `Gate = G2 passed` · `Done` with `Gate = G2 passed` | invalid + twins |
| DR1-03d | refs | a foreign ref present at the baseline (ADR-0036 decision 4) | invalid + twin (severity warning) |
| DR1-04 · 05 · 06 · 06b · 07 (06p: `could_not_run` with exit 2, valid) | structure | an error finding beside exit 0 · a key naming an action taken · `could_not_run` beside exit 0 · `could_not_run` carrying a finding · a clean completed run beside exit 1 | invalid |

### 3.3 `gate-run-v3` — `gatebraid/gate-run@3` — 14 files, 14 cases

GR3-01 the canonical `@3` record (valid); GR3-02/03 the `@2` canonical valid as
`@2` and invalid as `@3` (the pair); GR3-04 two `red_check` attempts without a
consult, `passed` (invalid: friction #94 as ledger 193 re-keyed it); GR3-05
two `record_correction` attempts (valid: route A); GR3-06 one of each (valid);
GR3-07 two `red_check` with the consult on the roster (valid); GR3-08 a
`consult_ref` with an empty roster (invalid: ledger 238(c)); GR3-09 an
attempt without `kind` (invalid); GR3-10 a `Writer Assignment` approval
(valid: ledger 194); GR3-11 a `qualifications[]` entry (valid: ledger 194);
GR3-12 a qualification without its citation (invalid); GR3-13 a 63-hex
`plan_hash` and GR3-14 a 63-hex `allowlist_hash` (invalid).

### 3.4 `instruments-v2` — `gatebraid/coverage-report@2` — 8 files, 8 cases

IN2-01 the canonical `@2` report (valid); IN2-01a/01b the `@1` canonical valid
as `@1` and invalid as `@2` (the pair); **IN2-02 a property credited `pass` on
an uninterpretable exit code — IN-01, the one §6 item frozen in neither v1
corpus — invalid**; IN2-02p the same basis with `fail` and the report
rejected (valid); IN2-03 `pipeline_last` without `pipefail` written up as
interpretable (invalid: the definition half); IN2-04 a report over a
`gate-run@3` target (valid); IN2-05 an `@1` report over a `@3` target
(invalid: why `@2` exists).

### 3.5 `state-pipeline` — three seeds for the O0-B1 review's F-01

SP1-18 Slice metadata present, no verdict (`$defs/item allOf[2]`'s rejecting
arm); SP1-19 a cross-check `mismatch` beside a `startable` verdict
(`allOf[3]`); SP1-20 a declared soft dependency `not_parsed` beside a
`startable` verdict (`allOf[4]`). The manifest gains `known_limitation` (F-03)
and moves to `v2.0`; `frozen_by` names the dated addendum that corrects its
ordinal wording (F-04).

---

## 4. What is frozen, and where every §6 item now stands

Thirteen state-pipeline items at O0's start (`DETERMINACY-REPORT.md` §7);
IN-03, IN-04, IN-05 and four half-built remainders at N3's start (N1E); and
**IN-01 here** (§3.4; `DETERMINACY-REPORT.md` §8). Twenty-one of twenty-one.
The guard's twelve and the doctor's audits are not §6 items; they are P's own
catalogue, specified here for the first time, one negative case per check as
`M3-PLAN.md` §2 P requires and, beyond the requirement, one per rule row.

The freeze commit is the P-B1 merge. `fixtures/CORPORA.json` declares the four
new corpora `built` in the same commit as their directories; `direct-drive` is
declared `foreign` (§5).

---

## 5. Measurement — the commands, and the runner's amendment

```
<python> -B fixtures/run-corpus.py          # CORPUS CLEAN, exit 0; 259 cases at delivery
<python> -B fixtures/runner-selftest.py     # SELFTEST CLEAN; 32 conditions, S29-S31 new
```

Both are run on Windows and on WSL by the build window and re-run by the
independent review in scratch outside every repository; a locus that differs
from the manifests on either host is a STOP that returns the package, never
a local edit. The manifests' `loader` records the coordinator's sandbox
loader; the landing captures record the host loaders beside `CORPUS CLEAN`.

The (schema, locus-set) collision count `DETERMINACY-REPORT.md` §8 states is
re-derived by:

```
<python> -B -c "import json,pathlib,collections;F=pathlib.Path('fixtures');d=json.loads((F/'CORPORA.json').read_text());g=collections.defaultdict(list);n=0
for c in d['built']:
    for k in json.loads((F/c/'EXPECTATIONS.json').read_text())['cases']:
        if k['expect']!='invalid': continue
        n+=1;g[(k['schema'],tuple(sorted((e['keyword'],e['path'],e['schema_path'],e.get('property'),e.get('extra_count')) for e in k['expect_errors'])))].append(c+':'+k['id'])
print(n,len(g),sum(1 for v in g.values() if len(v)>1))"
```

Expected at delivery: `181 178 3`, the three groups being the ones v1
declared.

**The runner's amendment (P-B1).** Measured at authoring, `run-corpus.py` at
the batch's base exits 2 on `main`: `fixtures/direct-drive/` (the dispatcher's
seeds, landed at DD1) was never declared. `CORPORA.json` gains `foreign`, the
names under `fixtures/` that are another tool's fixture set; the runner skips
them and adds three structure errors so the declaration cannot hide a corpus
(a foreign name whose directory does not exist; a foreign directory carrying
an `EXPECTATIONS.json`; a name declared both foreign and a corpus), each with
a selftest condition (S29–S31) that fails on the runner that preceded the
amendment. The digest scope gains the foreign directories. The selftest's
temp-root leak on Windows (the queue's `gatebraid-cwdneg-*` item) is **not**
touched here: its cause is unmeasured and a guessed fix is not one.

---

## 6. Not in this freeze

The guard and the doctor themselves (P2-S7); the instrument half of every
item (§1); the raw readings for the cases whose instance is not already on
the record (seeded at P2-S7); the hook baseline, the three permission
profiles and the host-instruction conformance check (R-min; the doctor's
`host.instruction_divergence` id is reserved and has no case); the sweep
instrument's residue rule for superseded `-pass` captures (ledger 238(e);
decided at P2-S7 with check 2); the external read-only model review named by
`M3-PLAN.md` §2 N1, untouched by this freeze as by every freeze before it.
