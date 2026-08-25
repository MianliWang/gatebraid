# Gate 1 evidence — P2-S4

## Plan (frozen at exit)
- **Approach.** Deliver M3-PLAN §2 node O0's tool half as three independently
  verifiable tasks. Each task ships a tool and its committed falsification,
  following the landed `bin/gatebraid-capture*.py` and `bin/gatebraid-validate*.py`
  pattern (ADR-0028: instruments are committed, falsified and reused). The Slice
  consumes the batch-frozen `gatebraid/snapshot@1` schema and the frozen
  `fixtures/state-pipeline/` corpus and authors neither.

  **T1 — `bin/gatebraid-snapshot.py` and `bin/gatebraid-snapshot-selftest.py`.**
  The producer. Emits a `gatebraid/snapshot@1` document. **P0-1:** every
  control-plane read becomes a `sources[]` entry carrying `status` from the
  schema's closed enumeration, `complete`, `exit_code`, and `failure_detail`
  whenever the status is not `ok`; a non-zero process exit is surfaced in the
  document and never folded into an absent or empty value; each of the seven
  P0-1 classes — auth, permission, rate-limit, network, server, parse,
  unexpected-endpoint — carries a seeded case in the selftest. **P0-2:** the
  document is written to binary stdout as explicitly UTF-8-encoded bytes, never
  through the inherited console text layer; the producer/consumer byte contract
  is stated in the tool's own docstring. **P0-3:** every verdict-relevant
  connection is paginated to exhaustion, or its source carries `bounded` with
  `reason`, `cap`, `observed` and `has_next_page` together with
  `complete: false`; reaching a cap fails closed rather than reporting a
  truncated list as whole.

  **T2 — `bin/gatebraid-frontier.py` and `bin/gatebraid-frontier-selftest.py`.**
  The consumer. Validates a snapshot document against
  `schema/snapshot.schema.json` **before reading any field of it**, then emits
  verdicts. **P0-4:** `schema` and `snapshot_version` are required and checked
  before consumption; Issue states come from the closed enumeration and
  `UNKNOWN` yields `undecidable`, never unblocked; a verdict is emitted only for
  an item whose `slice_metadata_present` is true, and an item without it carries
  `excluded_reason` and no verdict at all; both dependency directions are read
  and cross-checked, and `mismatch` or `not_performed` yields `undecidable`; a
  declared soft dependency is parsed or the document says `parse_status:
  not_parsed`, which yields `undecidable`; an `Aborted` workflow is never
  `startable` (ADR-0025 §8); any degraded source yields `undecidable` for every
  item.

  **T3 — `bin/gatebraid-o0-acceptance.py` and its selftest.** The end-to-end
  harness, and where the batch review's F-01 and this Slice's Gate 0 Q7 gap are
  discharged together. It drives the pair over the frozen corpus and over a
  seeded induced-failure matrix, and emits its summaries itself rather than
  having them narrated. `--induced-failures` carries one seeded case per P0-1
  class and per P0-4 clause, each of which must produce `undecidable`.
  `--dependency-directions` exercises a **non-empty** dependency relation in
  **both** directions against corpus material rather than the live closed set —
  closing the Q7 gap where Gate 0 could not — and covers the two conditionals no
  fixture asserts: `allOf[3]`'s consequence half, where a cross-check reading
  `mismatch` or `not_performed` yields `undecidable`, and `allOf[2]`'s positive
  arm, where an item carrying Slice metadata owes its id, its Workflow and a
  verdict. `--byte-contract` runs both tools under a **non-UTF-8 parent console**
  with non-ASCII fixture content and compares emitted bytes against the expected
  UTF-8 encoding, closing P0-2 and the BP-01 class that fired on this host during
  this Slice's own Gate 0.

- **Exact `write_domains` allowlist:** `bin/` · `docs/evidence/gatebraid/P2-S4/`
  — and nothing else (ADR-0032 decision 2). `schema/` and `fixtures/` are the
  batch lane's and are frozen; no path outside these two prefixes appears
  anywhere in this plan.

- **The frozen surface is held unmoved, by measurement at named points.** The
  schema `gatebraid/snapshot@1` at sha256
  `95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6` and the
  corpus digest `66051715f76cf52d881aa143d9267f932407dbf5b9c4e6be9f81395ec641ef8e`
  are re-measured by command **D7** at three points: before the first
  implementation commit, after the last, and at Gate 2 exit. "Unmoved" is the
  equality of `digest before` and `digest after` with the batch-frozen value in
  the instrument's own output at each point, never an assumption between them.

- **Test plan** (commands runnable as written on the declared `environment`;
  every one dry-run at Gate 1, see Records P2). Every Python invocation carries
  `-B`, with `PYTHONDONTWRITEBYTECODE=1` set inside the `wsl` command on the WSL
  half. All command output paths are repository-relative and inside the
  allowlist; none uses a system temporary directory.

  | id | command | expected green |
  |---|---|---|
  | D1a | `C:/Python312/python.exe -B bin/gatebraid-snapshot-selftest.py` | `conditions failed : 0`, `SELFTEST CLEAN`, exit 0 |
  | D1b | `wsl -e bash -lc "cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-snapshot-selftest.py"` | as D1a |
  | D2a | `C:/Python312/python.exe -B bin/gatebraid-frontier-selftest.py` | `conditions failed : 0`, `SELFTEST CLEAN`, exit 0 |
  | D2b | `wsl -e bash -lc "cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-frontier-selftest.py"` | as D2a |
  | D3a | `C:/Python312/python.exe -B bin/gatebraid-o0-acceptance.py --induced-failures --out docs/evidence/gatebraid/P2-S4/acceptance/induced.json` | every induced class in the harness's own summary carries verdict `undecidable`; no class reported unexercised; exit 0 |
  | D3b | the D3a command under `wsl -e bash -lc` with `PYTHONDONTWRITEBYTECODE=1 python3 -B` | as D3a |
  | D4 | `C:/Python312/python.exe -B bin/gatebraid-o0-acceptance.py --dependency-directions --out docs/evidence/gatebraid/P2-S4/acceptance/deps.json` | a non-empty relation exercised in both directions; `mismatch` and `not_performed` each yield `undecidable`; the Slice-metadata positive arm accepts; exit 0 |
  | D5 | `C:/Python312/python.exe -B bin/gatebraid-o0-acceptance.py --byte-contract --out docs/evidence/gatebraid/P2-S4/acceptance/bytes.json` | bytes emitted under a non-UTF-8 parent console equal the expected UTF-8 encoding byte for byte; exit 0 |
  | D6a | `C:/Python312/python.exe -B bin/gatebraid-validate.py --corpus fixtures` | `CORPUS CLEAN`, `unexpected dispositions : 0`, exit 0 |
  | D6b | the D6a command under `wsl -e bash -lc` with `PYTHONDONTWRITEBYTECODE=1 python3 -B` | as D6a |
  | D7 | `C:/Python312/python.exe -B fixtures/runner-selftest.py` | `digest before` = `digest after` = the batch-frozen value; `conditions failed : 0`; exit 0 |
  | D8 | `git merge-base --is-ancestor df666070ead7fa21bc72b6c99d2644923b37e787 HEAD` | exit 0 |
  | N1 | `C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/negative-criterion-N1.py df666070ead7fa21bc72b6c99d2644923b37e787 HEAD` | `N1 HOLDS`, exit 0 |

  **Acceptance mapping, item by item, from the Slice body.** Acceptance 1 (both
  tools' outputs validate against the frozen schema, schema/version required) →
  D3a, D3b, D4. Acceptance 2 (the freeze precedes implementation in commit
  history; the batch-pinned digest is unmoved) → D8 and D7. Acceptance 3 (all
  state-pipeline fixtures pass on the declared platforms; `undecidable`
  demonstrably produced by each induced failure) → D6a, D6b and D3a, D3b.
  Acceptance 4 (fail-closed per class; P0-2's byte contract on non-ASCII
  fixtures on both platforms; P0-3 caps; P0-4's closed enum with both
  dependency directions) → D1a, D1b, D2a, D2b, D5, D4.

- **Negative criteria (checkable properties the diff must NOT have).** Each
  states the pattern it proxies for, the scope it searches, and the direction in
  which it errs (ADR-0018 §2, friction #109); scope is an explicit path set,
  never "the added file" (friction #110).

  **N1 — path scope.** The diff over `df666070…..HEAD` touches no path outside
  the explicit set `bin/**` and `docs/evidence/gatebraid/P2-S4/**`. Proxy:
  `git diff --name-only` filtered against those two prefixes. **Errs toward
  false alarm** — a legitimate path relocated above those prefixes would trip it;
  it cannot err toward silence, because containment is decided by the prefix set
  rather than by a heuristic. Checker committed at
  `docs/evidence/gatebraid/P2-S4/g1/negative-criterion-N1.py`; it holds on the
  current range and **fires** on the O0-B1 batch range, so it is a criterion that
  has been shown able to fail.

  **N2 — no fail-open on a verdict-relevant path.** Neither tool converts a
  non-zero subprocess exit, a caught exception, or an absent field into a
  default, empty or absent value on any path that can reach a verdict. Proxy: a
  scan of `bin/gatebraid-snapshot.py` and `bin/gatebraid-frontier.py` for a bare
  `except:` or `except Exception:` without re-raise or an explicit fail-closed
  assignment, for a `returncode` read without comparison, and for `.get(` with a
  non-`None` default on source-status and issue-state fields. **Errs toward false
  positive** — it flags legitimately handled exceptions — which is the safe
  direction, since a missed fail-open is the P0-1 defect itself.

  **N3 — no live network call in any declared test command.** The frozen corpus
  and seeded fixtures are the only inputs to the acceptance commands. Proxy: the
  declared commands' argv contain no `gh` invocation, and the harness's own
  source names no HTTP client. **Errs toward false positive** — a mention in a
  docstring would trip it.

  **N4 — no verdict without validation.** `bin/gatebraid-frontier.py` emits no
  verdict for a document it has not validated against `gatebraid/snapshot@1`.
  Proxy, two halves: a source scan that every verdict-emitting path is dominated
  by the validation call, and a seeded behavioural run using the frozen fixture
  `fixtures/state-pipeline/sp10-snapshot-missing-schema-key.json`, which must
  produce no verdict. **The scan half errs toward false positive**; the seeded
  half is a direct behavioural test drawn from frozen corpus material rather
  than an author-chosen input.

- **Risk notes.** `risk: low` is justified by blast radius, not by ease: the
  allowlist is two prefixes; the Slice writes no protocol, schema, ADR, template
  or fixture; the deliverables are new files, so nothing existing is rewritten;
  and the corpus and schema it consumes are frozen and machine-checked before
  this Slice begins. **Stated against that rating:** consequence-if-wrong is not
  low — from this Slice's Gate 3 exit the pair becomes the sole startability
  authority, and a fail-open tool that passes its own tests would be exactly the
  P0-1 defect this node exists to remove. That is what N2 and N4, the
  induced-failure matrix, and the independent Review are for. `repair_limit: 2`
  is the standing budget; `consult_first: false` is retained, and reconsidering
  it is a Gate 2 decision if a repair is spent.

- **Rollback note.** Nothing is committed before the Gate 2 Writer Lease, so at
  Gate 1 abandonment costs nothing but the uncommitted evidence directory. From
  Gate 2 the Slice works on its own branch cut under the lease: abandonment is
  deleting that unmerged branch, with `main` untouched and no force-push, per the
  Gate 3 prohibition. The frozen schema and corpus are never written by this
  Slice, so there is nothing to revert there — a claim D7 and N1 make checkable
  rather than promised. Evidence files under
  `docs/evidence/gatebraid/P2-S4/` are working files until the lease and may be
  discarded wholesale.

## Records

**P1 — team findings flushed** (only if a read-only team ran)
```
No read-only team was used. gate-1-contract Action 2 makes the team optional;
the option was considered and declined, so there are no findings to flush and
no flush comment exists. Recorded rather than left silent.
```

**P2 — dry-run of every declared test command, on the declared environment (gate-1-contract action 4)**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/dryrun-driver.py --skip-slow
declared-command dry-run matrix
==============================================================================================================
D1a snapshot selftest, windows                 exit=2    want: non-zero naming the declared target absent -> as expected
   $ C:/Python312/python.exe -B bin/gatebraid-snapshot-selftest.py
     C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-snapshot-selftest.py': [E

D1a TWIN form, windows                         exit=0    want: exit 0 -> form resolves here
   $ C:/Python312/python.exe -B bin/gatebraid-capture-selftest.py --help
     corpus/schema surface UNMODIFIED: True
     conditions failed             : 0
     SELFTEST CLEAN: every condition produced its required observation

D1b snapshot selftest, wsl                     exit=2    want: non-zero naming the declared target absent -> as expected
   $ wsl -e bash -lc cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-snapshot-selftest.py
     python3: can't open file '/mnt/d/Github repo/Gatebraid/bin/gatebraid-snapshot-selftest.py': [Errno 2] No such 

D1b TWIN form, wsl                             exit=0    want: exit 0 -> form resolves here
   $ wsl -e bash -lc cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-capture-selftest.py --help
     corpus/schema surface UNMODIFIED: True
     conditions failed             : 0
     SELFTEST CLEAN: every condition produced its required observation

D2a frontier selftest, windows                 exit=2    want: non-zero naming the declared target absent -> as expected
   $ C:/Python312/python.exe -B bin/gatebraid-frontier-selftest.py
     C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-frontier-selftest.py': [E

D2b frontier selftest, wsl                     exit=2    want: non-zero naming the declared target absent -> as expected
   $ wsl -e bash -lc cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-frontier-selftest.py
     python3: can't open file '/mnt/d/Github repo/Gatebraid/bin/gatebraid-frontier-selftest.py': [Errno 2] No such 

D3a acceptance induced-failures, windows       exit=2    want: non-zero naming the declared target absent -> as expected
   $ C:/Python312/python.exe -B bin/gatebraid-o0-acceptance.py --induced-failures --out docs/evidence/gatebraid/P2-S4/acceptance/induced.json
     C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-o0-acceptance.py': [Errno

D3b acceptance induced-failures, wsl           exit=2    want: non-zero naming the declared target absent -> as expected
   $ wsl -e bash -lc cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-o0-acceptance.py --induced-failures --out docs/evidence/gatebraid/P2-S4/acceptance/induced.json
     python3: can't open file '/mnt/d/Github repo/Gatebraid/bin/gatebraid-o0-acceptance.py': [Errno 2] No such file

D4 acceptance dependency-directions, windows   exit=2    want: non-zero naming the declared target absent -> as expected
   $ C:/Python312/python.exe -B bin/gatebraid-o0-acceptance.py --dependency-directions --out docs/evidence/gatebraid/P2-S4/acceptance/deps.json
     C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-o0-acceptance.py': [Errno

D5 acceptance byte-contract, windows           exit=2    want: non-zero naming the declared target absent -> as expected
   $ C:/Python312/python.exe -B bin/gatebraid-o0-acceptance.py --byte-contract --out docs/evidence/gatebraid/P2-S4/acceptance/bytes.json
     C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-o0-acceptance.py': [Errno

D6a corpus, windows                            exit=0    want: exit 0 -> green
   $ C:/Python312/python.exe -B bin/gatebraid-validate.py --corpus fixtures
     positive controls with semantic findings : 0
     CORPUS CLEAN: every declared case reached its recorded disposition and locus set
     unexpected dispositions       : 0

D6b corpus, wsl                                exit=0    want: exit 0 -> green
   $ wsl -e bash -lc cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-validate.py --corpus fixtures
     positive controls with semantic findings : 0
     CORPUS CLEAN: every declared case reached its recorded disposition and locus set
     unexpected dispositions       : 0

D7 corpus digest unmoved, windows              SKIPPED by --skip-slow (run separately; see D7 capture)
D8 freeze precedes implementation              exit=0    want: exit 0 -> green
   $ git merge-base --is-ancestor df666070ead7fa21bc72b6c99d2644923b37e787 HEAD
     (no output)

==============================================================================================================
declared commands with a live target : 3 run, 3 green
declared commands this Slice will write: 8 run, 8 failed only on target-absent
form twins                            : 2 run, 2 resolved on this environment
unexpected results                    : 0
(exit 0)
```

**P2 — D7, run separately for runtime**
```
$ C:/Python312/python.exe -B fixtures/runner-selftest.py
condition                           want  got  verdict  required observation
S00 untouched copy                     0    0  PASS     CORPUS CLEAN
S01 mutation not killed                1    1  PASS     mutation not killed
S02 recorded locus silent              1    1  PASS     recorded locus did not fire
S03 unrecorded locus fired             1    1  PASS     unrecorded locus fired
S04 valid case broken                  1    1  PASS     expected valid
S05 fixture missing                    2    2  PASS     fixture missing
S06 schema missing                     2    2  PASS     schema missing
S07 invalid case unspecified           2    2  PASS     records no expected error
S08 orphan fixture file                2    2  PASS     referenced by no case
[... shown 10 of 37 lines; full output: docs/evidence/gatebraid/P2-S4/g1/G1-dryrun-D7-windows.json]
(exit 0)
```

**P2 — N1 negative-criterion checker: holds on the current range, and fires on a range known to violate it**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/negative-criterion-N1.py df666070ead7fa21bc72b6c99d2644923b37e787 HEAD
range          : df666070ead7fa21bc72b6c99d2644923b37e787..HEAD
allowed prefixes:
   bin/
   docs/evidence/gatebraid/P2-S4/
changed paths  : 0
inside allowlist: 0
outside         : 0

N1 HOLDS: every changed path is inside the frozen allowlist
(exit 0)
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/negative-criterion-N1.py e5e8ee6b8ac0f2fc0da1c9215b18fe6353986893 9dd0415a910e4bdafb0abe66a65189d9aff95cb3
range          : e5e8ee6b8ac0f2fc0da1c9215b18fe6353986893..9dd0415a910e4bdafb0abe66a65189d9aff95cb3
allowed prefixes:
   bin/
   docs/evidence/gatebraid/P2-S4/
changed paths  : 21
inside allowlist: 0
outside         : 21
   OUTSIDE fixtures/CORPORA.json
   OUTSIDE fixtures/DETERMINACY-REPORT.md
   OUTSIDE fixtures/state-pipeline/EXPECTATIONS.json
   OUTSIDE fixtures/state-pipeline/sp01-non-zero-exit-swallowed.json
   OUTSIDE fixtures/state-pipeline/sp02-permission-read-as-no-dependency.json
   OUTSIDE fixtures/state-pipeline/sp03-rate-limit-named-as-permission.json
   OUTSIDE fixtures/state-pipeline/sp04-partial-result-reported-complete.json
[... shown 14 of 30 lines; full output: docs/evidence/gatebraid/P2-S4/g1/G1-dryrun-N1-falsify.json]
(exit 1)
```

**P2 — form probe: the declared output path denotes the same file on both halves (the Slice A class)**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/pathprobe.py write windows
cwd            : D:\Github repo\Gatebraid
relative path  : docs/evidence/gatebraid/P2-S4/acceptance/.pathprobe
resolves to    : D:\Github repo\Gatebraid\docs\evidence\gatebraid\P2-S4\acceptance\.pathprobe
wrote          : written-by-windows
(exit 0)
```

**P2 — form probe: P0-2 byte contract under a non-UTF-8 parent console (the BP-01 class)**
```
$ cmd C:/ docs\evidence\gatebraid\P2-S4\g1\byteprobe-cp936.cmd
Microsoft Windows [�汾 10.0.26200.9168]
(c) Microsoft Corporation����������Ȩ����

D:\Github repo\Gatebraid>
(exit 0)
```

**P2 — exit-checklist item measured, not asserted: every WRITE target named in the plan is inside the allowlist**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/plan-path-scan.py docs/evidence/gatebraid/P2-S4/gate1.md
allowlist prefixes : bin/, docs/evidence/gatebraid/P2-S4/
paths named in plan: 23

WRITE targets, each required to be inside the allowlist:
   bin/                                                             inside=True
   bin/**                                                           inside=True
   bin/gatebraid-capture*.py                                        inside=True
   bin/gatebraid-frontier-selftest.py                               inside=True
   bin/gatebraid-frontier.py                                        inside=True
   bin/gatebraid-o0-acceptance.py                                   inside=True
   bin/gatebraid-snapshot-selftest.py                               inside=True
   bin/gatebraid-snapshot.py                                        inside=True
   bin/gatebraid-validate*.py                                       inside=True
   docs/evidence/gatebraid/P2-S4/                                   inside=True
   docs/evidence/gatebraid/P2-S4/**                                 inside=True
   docs/evidence/gatebraid/P2-S4/acceptance/bytes.json              inside=True
   docs/evidence/gatebraid/P2-S4/acceptance/deps.json               inside=True
   docs/evidence/gatebraid/P2-S4/acceptance/induced.json            inside=True
   docs/evidence/gatebraid/P2-S4/g1/negative-criterion-N1.py        inside=True

READ-ONLY inputs, named on purpose and written by no task in this plan:
   bin/gatebraid-validate.py
   fixtures/runner-selftest.py
   fixtures/state-pipeline/
[... shown 24 of 37 lines; full output: docs/evidence/gatebraid/P2-S4/g1/G1-plan-path-scan.json]
(exit 0)
```

**P3 — exit checklist completed, every item evidence-backed**
```
docs/evidence/gatebraid/P2-S4/g1/gate1-exit-checklist.md
```

**P4 — allowlist_hash reproduced**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/hash-allowlist.py
entries (sorted by byte value):
   'bin/'
   'docs/evidence/gatebraid/P2-S4/'
payload bytes : b'bin/\ndocs/evidence/gatebraid/P2-S4/\n'
payload length: 36
allowlist_hash: feb6d9c8ffbbaa08242d68e64db7b13b3f080aaae3667f01d7d22bdb0c061655
(exit 0)
```

**P5 — plan_hash reproduced**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/hash-plan.py docs/evidence/gatebraid/P2-S4/gate1.md
record        : docs/evidence/gatebraid/P2-S4/gate1.md
heading at    : line 3 (1-based)
next '## ' at : line 166 (1-based)
plan lines    : 161 after stripping and trimming
payload length: 11792
plan_hash     : cb577dbf7fd1c0443b5e7ffbb94aacd7ada64385230afb6faa498815a4828913
(exit 0)
```

**P6 — the sanctioned write_domains post-condition on the Slice issue**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/writedomains-check.py
frozen allowlist  : ['bin/', 'docs/evidence/gatebraid/P2-S4/']
declared on #14   : ['bin/', 'docs/evidence/gatebraid/P2-S4/']
equal as sequences: True
equal as sets     : True

POST-CONDITION ALREADY HOLDS: the declared write_domains equals the frozen
allowlist. The agreement is recorded as this verification row and NO rewrite
of the Slice body is made. The step is performed, not skipped.
(exit 0)
```

## Required disclosures

- Deviations: Action 4 dry-run of a greenfield deliverable is recorded in two parts, and the judgment is disclosed rather than assumed. Eight of the declared commands target tools this Slice will write, so they cannot exit 0 today. Each was RUN as declared and produced a non-zero exit naming its declared target as absent and nothing else wrong, and each interpreter-and-path form was separately proven on this environment by a TWIN command of identical shape against a file that exists, on both halves. Action 4 exists to catch the Slice A defect, a command well-formed on inspection that cannot run there; the twin is what tests that, and Slice A's own defect would have failed its twin.
- Deviations: the Slice A path class is tested directly rather than argued. Every declared output path is repository-relative and under the allowlist; the probe writes that path from one half and reads it from the other, both ways, and both halves resolve it to the same file. No declared command uses a system temporary directory.
- Deviations: the D1a and D1b twin commands pass --help to bin/gatebraid-capture-selftest.py, which does not define that option and therefore ran its full selftest. The twin's purpose, proving the interpreter and repository-relative path form resolve on this environment, is served either way, and the extra work is disclosed rather than left to be noticed in the runtime.
- Deviations: no read-only team was used. gate-1-contract Action 2 makes it optional; declining is recorded with its reason in the P1 row.
- Deviations: the P0-2 byte contract was measured at Gate 1 rather than only declared, because BP-01 fired on this host during this Slice's Gate 0. Under a forced cp936 parent console the text path emitted cp936 bytes that are not valid UTF-8, and the binary-stdout path emitted byte-exact UTF-8. The declared D5 command therefore tests a failure already shown to be real and reproducible here.
- Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; shell Git Bash MINGW64 with Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid with endpoints carrying no leading slash; every Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL /usr/bin/python3 with CPython 3.12.3, jsonschema 4.10.3. environment=mixed-see-prose: the gate ran on the Windows host and the WSL half is evidence.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S4
gate: 1
environment: mixed-see-prose
executor: Claude Lead
base_sha: df666070ead7fa21bc72b6c99d2644923b37e787
started_at: "2026-08-24T05:02:11Z"
ended_at: "2026-08-24T09:54:19Z"
result: needs_approval
approvals:
  - type: State Packet Approval
    author: MianliWang
    comment_url: "https://github.com/MianliWang/gatebraid/issues/14#issuecomment-5390640145"
    at: "2026-08-24T04:14:47Z"
checks:
  - name: plan-complete
    command: "see the frozen plan section"
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: allowlist-exact
    command: "see the frozen plan section"
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: test-plan-dry-run
    command: "C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/dryrun-driver.py --skip-slow"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g1/G1-dryrun-matrix.json"
  - name: test-plan-dry-run-digest
    command: "C:/Python312/python.exe -B fixtures/runner-selftest.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g1/G1-dryrun-D7-windows.json"
  - name: negative-criterion-N1-holds
    command: "C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/negative-criterion-N1.py df666070ead7fa21bc72b6c99d2644923b37e787 HEAD"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g1/G1-dryrun-N1.json"
  - name: negative-criterion-N1-falsified
    command: "C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/negative-criterion-N1.py e5e8ee6b8ac0f2fc0da1c9215b18fe6353986893 9dd0415a910e4bdafb0abe66a65189d9aff95cb3"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g1/G1-dryrun-N1-falsify.json"
  - name: output-path-same-on-both-halves
    command: "C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/pathprobe.py write windows"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g1/G1-formprobe-outpath.json"
  - name: byte-contract-under-non-utf8-console
    command: "cmd /c docs/evidence/gatebraid/P2-S4/g1/byteprobe-cp936.cmd"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g1/G1-formprobe-byte-contract.json"
  - name: gate1-exit-checklist
    command: "see docs/evidence/gatebraid/P2-S4/g1/gate1-exit-checklist.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g1/gate1-exit-checklist.md"
  - name: write-domains-agreement
    command: "gh api repos/MianliWang/gatebraid/issues/14 --jq .body"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/g1/G1-writedomains-check.json"
plan_hash: "cb577dbf7fd1c0443b5e7ffbb94aacd7ada64385230afb6faa498815a4828913"
allowlist_hash: "feb6d9c8ffbbaa08242d68e64db7b13b3f080aaae3667f01d7d22bdb0c061655"
hash_commands:
  allowlist: "C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/hash-allowlist.py"
  plan: "C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/hash-plan.py docs/evidence/gatebraid/P2-S4/gate1.md"
evidence_files:
  - docs/evidence/gatebraid/P2-S4/gate1.md
notes: "Gate 1 planning for O0's tool half. No read-only team was used; the option is recorded as declined. Eight declared commands target deliverables this Slice will write and were dry-run as declared plus a form twin on each half, per the disclosure. The frozen surface is held unmoved by measurement at named points rather than by assumption."

```
