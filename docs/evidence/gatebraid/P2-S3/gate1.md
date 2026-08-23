# Gate 1 evidence — P2-S3

## Plan (frozen at exit)

- **Approach.** Two defects in the landed `gatebraid-validate`, repaired in the
  order they were found, plus the re-validation their repair unblocks.

  **Task A — scope the placeholder heuristic (friction #169).** The heuristic
  `PLACEHOLDER` at `bin/gatebraid-validate.py` today matches `...` anywhere in
  any string of any document. Measured at this gate, that single rule produces
  every placeholder rejection across three Slices' evidence, at three loci:
  `/invocation/argv/N`, `/checks/N/command` and `/notes`. The repair does not
  weaken the rule; it adds a **mention test** that fires only where a document
  legitimately quotes foreign text, and only for two named quoting forms:

  1. a **GraphQL inline-fragment spread** — `...` followed by whitespace, `on`,
     whitespace and a type name;
  2. an **intra-token identifier abbreviation** — `...` bounded by identifier
     characters rather than standing alone as a token (an abbreviated node id or
     object name).

  A hit is reclassified as a mention **only when both** hold: its locus is one of
  `/invocation/argv/N`, `/checks/N/command`, `/notes` (the command and citation
  fields), **and** the hit matches one of the two named forms. Everything else
  stays a finding. The mention is recorded as a labelled property, not silently
  dropped: a suppressed hit that leaves no trace is the shape ADR-0026 exists
  against.

  This discriminates by measurement rather than by locus alone, and the
  distinction is not theoretical — it is what separates the two populations that
  share the `/checks/N/command` locus. P2-S1's `gate0.json` carries nine
  citations of the form `gh api graphql ... -F number=99999` and
  `gh project item-edit --id ... --text S2`, where `...` stands alone in place of
  omitted command text, plus one `<...>` stand-in; those are the #171-class
  findings the Slice is explicitly forbidden to repair and which must survive.
  This Slice's own `gate0.md` carries `... on ProjectV2ItemFieldTextValue` at the
  same locus, which is GraphQL syntax quoted verbatim. A locus-only exemption
  would suppress both; the two named forms suppress only the second.

  **Task B — markdown gate-record mode (friction #170).** `validate_document`
  reads its input with `json.loads` and raises `InputError` on anything else, so
  three of any Slice's four gate records — every ADR-0026 markdown record — are
  outside the validator's reach. The repair adds a second front end: when the
  input does not parse as JSON, look for a `## gatebraid-metadata` heading and
  take the first fenced yaml block under it (the extraction rule the schemas
  themselves state), parse it, and hand the resulting document to the existing
  schema and semantic path unchanged. The YAML loader is imported **inside the
  function, guarded**, exactly as `load_schema_validator` imports the JSON Schema
  loader: the module level stays standard-library only, which is a property this
  file's own docstring asserts and which must not be broken to fix a defect.
  An input that is neither JSON nor a markdown document carrying that heading
  remains an input error at exit 2 — the existing selftest condition covering a
  broken input must stay green, and is one of the two directions Task B is
  seeded in.

  **Task C — complete the N2 re-validation.** Run the repaired validator over
  N2's evidence to completion and record the results in this Slice's evidence,
  discharging the remainder the P2-S2 closure left owed. Task C reads; it does
  not repair. Any finding it surfaces in a merged historical record is recorded,
  never fixed.

  The three tasks are independently verifiable: A by its seeded pair, B by its
  seeded pair, C by its recorded output.

- **Exact `write_domains` allowlist:** `bin/gatebraid-validate.py` ·
  `bin/gatebraid-validate-selftest.py` · `docs/evidence/gatebraid/P2-S3/`
  — the two subject files by their ratified names and this Slice's evidence
  prefix, and nothing else. `bin/gatebraid-capture.py` and
  `bin/gatebraid-capture-selftest.py` appear in no allowlist entry and must
  appear in no diff.

- **Test plan (commands, runnable as written on the declared environment).**
  `environment` is `mixed-see-prose`; each command names its own interpreter and
  the platform half it is assigned to. Every command below was dry-run at this
  gate on its assigned half and its output recorded in `## Records` P2. Expected
  results are stated as properties of the instruments' own emitted summaries,
  never as counts carried from any document.

  **T1 — the heuristic accepts what it wrongly rejected (positive direction).**
  Assigned: **both halves.**
  `windows:  C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py C:/Python312/python 'docs/evidence/gatebraid/P2-S1/captures/*.json'`
  `wsl:      python3 docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py python3 'docs/evidence/gatebraid/P2-S1/captures/*.json'`
  Expected green: the sweep prints `SWEEP COMPLETE` and exits 0 — no document in
  P2-S1's capture set is rejected, on either half. Pre-repair both halves reject
  the same set, which is recorded as this gate's baseline.

  **T2 — a genuine elision still rejects (negative direction).**
  Assigned: **Windows.**
  `C:/Python312/python bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S1/gate0.json`
  Expected green: exit 1, and the emitted findings are exactly the record's own
  `/checks/N/command` citations — the #171 class — reproduced, not suppressed.
  This is the paired half of T1 and the criterion the Slice is judged on: if the
  repair makes this record clean, the repair is wrong.

  **T3 — the markdown mode reads what it could not read.**
  Assigned: **both halves.**
  `windows:  C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py C:/Python312/python 'docs/evidence/gatebraid/P2-S1/gate1.md' 'docs/evidence/gatebraid/P2-S1/gate2.md' 'docs/evidence/gatebraid/P2-S1/gate3.md'`
  `wsl:      python3 docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py python3 'docs/evidence/gatebraid/P2-S1/gate1.md' 'docs/evidence/gatebraid/P2-S1/gate2.md' 'docs/evidence/gatebraid/P2-S1/gate3.md'`
  Expected green: every one is READ — no document exits 2. `gate1.md` and
  `gate2.md` are expected to be accepted; `gate3.md` is expected to be REJECTED
  on its own two `/checks/N/command` elisions, which is the record's finding and
  not the tool's, and is reported rather than repaired.

  **T4 — the markdown mode refuses what it should refuse.**
  Assigned: **Windows.** Two seeds, both constructed in a scratch directory
  outside every repository, run through
  `C:/Python312/python bin/gatebraid-validate.py --record <seed>`:
  a markdown document whose embedded block is schema-invalid must exit 1; a file
  that is neither JSON nor carries a `## gatebraid-metadata` heading must exit 2.
  Expected green: 1 and 2 respectively. The second seed is the existing
  broken-input condition and must not regress.

  **T5 — the selftest covers both repairs and is green on both halves.**
  Assigned: **both halves.**
  `windows:  C:/Python312/python bin/gatebraid-validate-selftest.py`
  `wsl:      python3 bin/gatebraid-validate-selftest.py`
  Expected green: `SELFTEST CLEAN` and exit 0 on both, with the suite carrying
  new conditions for both directions of Task A and both directions of Task B.

  **T6 — the frozen corpus is unmoved.**
  Assigned: **Windows** (see the budget note; the assignment is measured, not
  assumed).
  `C:/Python312/python fixtures/runner-selftest.py`
  Expected green: `SELFTEST CLEAN`, `conditions failed : 0`, and `digest before`
  equal to `digest after` equal to
  `f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686`, the value
  measured at this gate before any repair. The digest's own declared scope
  covers the corpora, `CORPORA.json`, `schema/`, `run-corpus.py` and
  `runner-selftest.py` — it does not cover `bin/`, so this Slice's allowlist
  cannot move it, and a moved digest means something outside the allowlist was
  touched.

  **T7 — the corpus mutation suite still passes.**
  Assigned: **both halves.**
  `windows:  C:/Python312/python bin/gatebraid-validate.py --corpus fixtures`
  `wsl:      python3 bin/gatebraid-validate.py --corpus fixtures`
  Expected green: `CORPUS CLEAN` and exit 0 — every declared case still reaches
  its recorded disposition and locus set after the repair.

  **T8 — the self-validation point** (the step the approval requires this plan
  to name). Assigned: **Windows**, after Task A and Task B have landed under the
  lease at Gate 2.
  `C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py C:/Python312/python 'docs/evidence/gatebraid/P2-S3/captures/*.json' 'docs/evidence/gatebraid/P2-S3/gate0.md' 'docs/evidence/gatebraid/P2-S3/gate1.md'`
  This is where the **repaired** validator machine-validates this gate's own
  evidence and the Gate 0 record through the markdown mode, discharging the
  disclosed limit the state packet recorded at §5. Its result lands in this
  Slice's evidence.
  Expected green, stated honestly rather than optimistically: every document is
  READ (none exits 2), and the only rejections that remain are at
  `/streams/stdout/rendered/text`, a locus this Slice does **not** exempt — see
  the risk note. A clean sweep here is **not** expected and must not be
  engineered by widening the exemption.

  **T9 — the N2 re-validation, run to completion and recorded** (Task C).
  Assigned: **both halves.**
  `windows:  C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py C:/Python312/python 'docs/evidence/gatebraid/P2-S1/captures/*.json' 'docs/evidence/gatebraid/P2-S1/gate0.json' 'docs/evidence/gatebraid/P2-S1/gate1.md' 'docs/evidence/gatebraid/P2-S1/gate2.md' 'docs/evidence/gatebraid/P2-S1/gate3.md'`
  `wsl:      python3 docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py python3 'docs/evidence/gatebraid/P2-S1/captures/*.json' 'docs/evidence/gatebraid/P2-S1/gate0.json' 'docs/evidence/gatebraid/P2-S1/gate1.md' 'docs/evidence/gatebraid/P2-S1/gate2.md' 'docs/evidence/gatebraid/P2-S1/gate3.md'`
  Expected green: all four gate records and every capture are READ; the surviving
  findings are exactly the historical records' own — `gate0.json`'s citations and
  `gate3.md`'s two — and the run's output is written into this Slice's evidence
  as the discharge of the owed remainder.

- **Command budgets (friction #165).** Measured at this gate, not estimated.
  Each command that approaches the two-minute default carries its own budget;
  the rest are recorded so the absence of a budget is a measurement too.

  | command | measured at this gate | budget |
  |---|---|---|
  | T6 `fixtures/runner-selftest.py` (Windows) | **147,993 ms** | **420,000 ms** — the only command over the default; it must be run with an explicit extended budget or it dies at 120 s and takes its queue with it |
  | T1 / T9 sweeps (Windows) | 25,187 ms over P2-S1's captures | 240,000 ms |
  | T1 sweep (WSL) | comparable; both halves rejected the same set | 240,000 ms |
  | T5 selftest | 9,180 ms Windows · 6,506 ms WSL | default |
  | T7 corpus mode | 613 ms Windows · 1,478 ms WSL | default |
  | T8 self-validation sweep | 3,323 ms-class, this Slice's set | 240,000 ms |

  T6 is assigned to Windows for a measured reason: the same command was started
  on the WSL half at this gate and had not completed after thirteen minutes,
  against 147,993 ms on Windows. Cross-platform filesystem access is the
  plausible cause and is not investigated here. The digest is a content hash over
  repository bytes and its own seed set asserts it ignores interpreter output, so
  one half establishes the unmoved claim; the dual-platform obligation attaches
  to T5 and T7, which run on both.

- **Risk notes.** `risk: low` is justified by scope: two functions in one file,
  no interface change, no schema/contract/ADR/template/corpus text touched, and
  a frozen corpus that the allowlist provably cannot reach. The risks that remain
  are named rather than rated away.

  1. **The exemption could be widened to buy a clean sweep.** T8 will still show
     rejections at `/streams/stdout/rendered/text`, and the tempting repair is to
     add that locus to the mention set. Measured at this gate, `rendered.text` is
     **not** re-derived from `data` anywhere in the validator — `check_capture`
     re-derives `byte_length` and `sha256` over the decoded payload but never
     compares the rendering against it. Exempting that locus would therefore
     remove the only check that field has, and would be a coverage regression
     bought to make a number look better. It is out of scope here and routed, not
     taken.
  2. **The two named quoting forms are proxies and can be wrong in both
     directions.** Their error directions are stated below, under the negative
     criterion.
  3. **The markdown front end could swallow a broken input.** If extraction is
     attempted too eagerly, a corrupt file could be read as a record instead of
     refused. T4's second seed exists for exactly this and is the direction the
     design is guarded in.
  4. **A YAML dependency at module level would break a property this file
     asserts about itself.** The guarded in-function import is a requirement of
     the plan, not an implementation preference.

- **Rollback note.** Every change lands in two files under `bin/` plus this
  Slice's evidence prefix, on a Slice branch, with no commit before the lease is
  held at Gate 2. Abandoning at any point before the Gate 3 merge costs nothing
  durable: the branch is left unmerged as a record (ADR-0025 §3), `main` is
  untouched at `63c8401f5df6ba446cf002232fcb280673c28e00`, the frozen corpus is
  provably unmoved by T6, and the landed validator continues to behave exactly as
  it does today — the defects are pre-existing and their persistence is the
  status quo, not a regression introduced by abandonment. No migration, no data
  change, no external state.

- **Negative criterion (checkable).** Three, each with an explicit path set and
  each stating the direction its mechanised proxy errs.

  **N1 — the diff touches nothing outside the frozen allowlist.**
  Scope, as an explicit path set: every path in
  `git diff --name-only <base_sha>..<head>`. The property: every such path is
  `bin/gatebraid-validate.py`, `bin/gatebraid-validate-selftest.py`, or begins
  `docs/evidence/gatebraid/P2-S3/`. In particular `bin/gatebraid-capture.py` and
  `bin/gatebraid-capture-selftest.py` appear nowhere in it.
  *Direction the proxy errs:* toward **false accusation**. It compares whole path
  strings and cannot recognise a legitimate path it was not told about, so a new
  in-scope directory would be reported as a violation rather than missed. It
  never errs toward silence.

  **N2 — the nine #171-class citations in `docs/evidence/gatebraid/P2-S1/gate0.json`
  are not suppressed.**
  Scope, as an explicit path set: the single file
  `docs/evidence/gatebraid/P2-S1/gate0.json`. The property: the repaired
  validator still rejects it, and the findings it emits are still at
  `/checks/N/command`. This is the criterion that makes the repair falsifiable —
  a change that merely stops rejecting things passes T1 and fails here.
  *Direction the proxy errs:* toward **false accusation**. It asserts the
  findings survive at their locus; if a future edit to that historical record
  legitimately removed a citation, this criterion would fail even though nothing
  is wrong. It cannot pass while the findings are silently suppressed, which is
  the failure it exists to catch.

  **N3 — the validator adds no module-level third-party import.**
  Scope, as an explicit path set: `bin/gatebraid-validate.py` and
  `bin/gatebraid-validate-selftest.py`. The property: every `import` statement at
  module indentation level resolves to the Python standard library; any
  third-party loader is imported inside a function and guarded.
  *Direction the proxy errs:* toward **false accusation**. A textual scan of
  module-level imports cannot know that a name is a vendored stdlib shim, so it
  would flag a legitimate one; it will not miss a genuine module-level
  third-party import, which is the regression it guards.

- **Acceptance mapping** (issue `#12`'s four boxes → declared commands, stated
  as properties of the instruments' own summaries, count-free).
  Box 1, the both-way heuristic seeds → **T1** (accepts) and **T2** (a genuine
  elision still rejects), with **T5** carrying the seeded pair inside the suite.
  Box 2, all four P2-S1 gate records read with `gate0.json`'s own findings
  reproducing → **T3** and **T9**, with **T2** as the named guard.
  Box 3, the full N2 re-validation run to completion and recorded in this
  Slice's evidence → **T9**, and **T8** for this Slice's own records.
  Box 4, the selftest green on both platforms with the corpus digest unmoved →
  **T5**, **T6** and **T7**.

## Records

**P1 — team findings flushed** (only if a read-only team ran)
```
No read-only team was spawned for this Slice: the planning surface is two
functions in one file whose defects were already measured and reproduced at
this gate. Contract action 2 is optional; nothing was delegated, so there are
no team findings to flush and no teammate constraint was engaged.
```

**P2 — dry-run of every declared test command, on the declared environment**
(gate-1-contract action 4 — one row per declared command)

*T1, Windows half*
```
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py C:/Python312/python 'docs/evidence/gatebraid/P2-S1/captures/*.json'
   F001     /invocation/argv/4                             placeholder-survives-its-own-check
   F002     /notes                                         placeholder-survives-its-own-check
SWEEP COMPLETE rejected_or_errored=11
  exit=1
```

*T1, WSL half*
```
$ wsl -e python3 docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py python3 'docs/evidence/gatebraid/P2-S1/captures/*.json'
   F002     /notes                                         placeholder-survives-its-own-check
SWEEP COMPLETE rejected_or_errored=11
  exit=1
```

*T3 surface (all four P2-S1 gate records + this Slice's gate0.md), Windows*
```
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py C:/Python312/python docs/evidence/gatebraid/P2-S1/gate0.json docs/evidence/gatebraid/P2-S1/gate1.md docs/evidence/gatebraid/P2-S1/gate2.md docs/evidence/gatebraid/P2-S1/gate3.md docs/evidence/gatebraid/P2-S3/gate0.md
   
gate3.md rc=2
   
gate0.md rc=2
   
SWEEP COMPLETE rejected_or_errored=5
  exit=1
```

*T5, Windows half*
```
$ C:/Python312/python bin/gatebraid-validate-selftest.py
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
  exit=0
```

*T5, WSL half*
```
$ wsl -e python3 bin/gatebraid-validate-selftest.py
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
  exit=0
```

*T7, Windows half*
```
$ C:/Python312/python bin/gatebraid-validate.py --corpus fixtures

CORPUS CLEAN: every declared case reached its recorded disposition and locus set
unexpected dispositions       : 0
  exit=0
```

*T7, WSL half*
```
$ wsl -e python3 bin/gatebraid-validate.py --corpus fixtures

CORPUS CLEAN: every declared case reached its recorded disposition and locus set
unexpected dispositions       : 0
  exit=0
```

*T8 surface, Windows half*
```
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py C:/Python312/python 'docs/evidence/gatebraid/P2-S3/captures/*.json' docs/evidence/gatebraid/P2-S3/gate0.md
gate0.md rc=2
   
SWEEP COMPLETE rejected_or_errored=5
  exit=1
```

*T6 corpus digest, Windows half*
```
$ C:/Python312/python fixtures/runner-selftest.py
digest scope                  : bytes-platform, evidence-capture-v1, gate-run-v2, instruments, metrics-v1, CORPORA.json, schema, run-corpus.py, runner-selftest.py, fixtures/ listing
digest before                 : f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686
digest after                  : f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686
seed-reachable surface UNMODIFIED: True
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
  exit=0
```

**P3 — exit checklist completed, every item evidence-backed**
```
docs/evidence/gatebraid/P2-S3/gate1-exit-checklist.md
```

**P4 — allowlist_hash reproduced**
```
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_hashes.py allowlist bin/gatebraid-validate.py bin/gatebraid-validate-selftest.py docs/evidence/gatebraid/P2-S3/
algorithm     : entries stripped, sorted by byte value, joined with LF, one trailing LF
entry         : bin/gatebraid-validate-selftest.py
entry         : bin/gatebraid-validate.py
entry         : docs/evidence/gatebraid/P2-S3/
bytes         : 92
allowlist_hash: 81a0bb015ffbc5f3f6a27abfaec0a089c2b5522aa69e5ee30d5d7a01ecd404c0
```

**P5 — plan_hash reproduced**
```
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_hashes.py plan docs/evidence/gatebraid/P2-S3/gate1.md
algorithm     : lines strictly between '## Plan (frozen at exit)' and the next '## ' line,
                each rstripped, leading/trailing blank lines dropped,
                joined with LF, one trailing LF
source        : docs/evidence/gatebraid/P2-S3/gate1.md
plan lines    : 261
bytes         : 17059
plan_hash     : eb89d3eaedc2690babb3086e3be7529f62fa03e7195746b3b8106ad85a626b18
```

**P6 — the sanctioned `write_domains` write-back to the Slice issue**
(gate-1-contract Exit; byte-identical re-emission apart from that field)
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api --method PATCH repos/MianliWang/gatebraid/issues/12 --input _handoff/batch-p2s3/G1-body-patch.json
{"url":"https://api.github.com/repos/MianliWang/gatebraid/issues/12","repository_url":"https://api.github.com/repos/MianliWang/gatebraid","labels_url":"https://api.github.com/repos/MianliWang/gatebraid/issues/12/labels{/name}","comments_url":"https://api.github.com/repos/MianliWang/gatebraid/issues/12/comments","events_url":"https://api.github.com/repos/MianliWang/gatebraid/issues/12/events","html_url":"https://github.com/MianliWang/gatebraid/issues/12","id":5219654398,"node_id":"I_kwDOTmww988AAAABNx2a_g","number":12,"title":"P2-S3 — gatebraid-validate repair: heuristic scope, markdown records, N2 re-validation completion","user":{"login":"mianliwang492-source","id":311670679,"node_id":"U_kgDOEpO3lw","avatar_url":"https://avatars.githubusercontent.com/u/311670679?v=4","gravatar_id":"","url":"https://api.github.com/users/mianliwang492-source","html_url":"https://github.com/mianliwang492-source","followers_url":"https://api.github.com/users/mianliwang492-source/followers","following_url":"https://api.github.com/users/mianliwang492-source/following{/other_user}","gists_url":"https://api.github.com/users/mianliwang492-source/gists{/gist_id}","starred_url":"https://api.github.com/users/mianliwang492-source/starred{/owner}{/repo}","subscriptions_url":"https://api.github.com/users/mianliwang492-source/subscriptions","organizations_url":"https://api.github.com/users/mianliwang492-source/orgs","repos_url":"https://api.github.com/users/mianliwang492-source/repos","events_url":"https://api.github.com/users/mianliwang492-source/events{/privacy}","received_events_url":"https://api.github.com/users/mianliwang492-source/received_events","type":"User","user_view_type":"public","site_admin":false},"labels":[],"state":"open","locked":false,"assignees":[],"milestone":null,"comments":4,"created_at":"2026-08-22T02:27:17Z","updated_at":"2026-08-22T04:40:06Z","closed_at":null,"assignee":null,"author_association":"COLLABORATOR","active_lock_reason":null,"sub_issues_summary":{"total":0,"completed":0,"percent_completed":0},"parent_issue_url":"https://api.github.com/repos/MianliWang/gatebraid/issues/7","issue_dependencies_summary":{"blocked_by":0,"total_blocked_by":0,"blocking":0,"total_blocking":0},"body":"# P2-S3 — gatebraid-validate repair: heuristic scope, markdown records, N2 re-validation completion\n\n## Goal\n\nRepair the two instrument defects `gatebraid-validate`'s first production\nrun exposed (friction #169, #170) and complete the N2 re-validation that\nrun left bounded: scope the placeholder heuristic to command and citation\nfields so GraphQL inline-fragment spreads and notes-field id\nabbreviations are classified as mentions, not elisions; add a\nmarkdown-gate-record mode (`## gatebraid-metadata` extraction, the\nADR-0026 form) so all four gate records of any Slice are within the\nvalidator's reach; then re-run the full N2 re-validation to completion\nand record it — discharging the remainder the P2-S2 closure named as\nowed. Files under repair: `bin/gatebraid-validate.py` and\n`bin/gatebraid-validate-selftest.py` (the ratified names; no new tool,\nno new name).\n\n## Context\n\n- Why now: the P2-S2 closure's bounded discharge (issue #10, the Closure\n  Resume's verbatim passage) leaves the full mechanical re-validation of\n  N2's four gate records owed until this Slice lands; O1 will rely on\n  the validator over real records, so the over-match is repaired before\n  the toolchain is leaned on.\n- Both repairs carry their falsifications: the heuristic fix is seeded\n  in both directions (a genuine elision must still reject — the\n  P2-S2-closure falsification pair is the model); the markdown mode is\n  seeded with a valid and an invalid embedded record.\n- Non-goals: no change to `bin/gatebraid-capture*.py` (never read, only\n  executed); no contract, schema, ADR, template or corpus text; no edit\n  to any merged historical gate record — `gate0.json`'s nine #171-class\n  citations stay recorded, not repaired.\n- Related: Phase P2 `#7` · P2-S1 `#8` · P2-S2 `#10` · PR `#11` ·\n  friction #169/#170/#171 · the P2-S2 Closure Resume rulings (a)–(c).\n\n## Acceptance\n\n- [ ] The 11 P2-S1 captures rejected at the P2-S2 closure validate\n      `accepted` with the repaired heuristic, AND a genuinely elided\n      capture still rejects — both shown by seeded runs, summaries\n      emitted by the instrument itself.\n- [ ] All four P2-S1 gate records (`gate0.json`, `gate1.md`, `gate2.md`,\n      `gate3.md`) are read and verdicts emitted by the validator's own\n      record mode; `gate0.json`'s nine genuine findings reproduce\n      (they are the record's, not the tool's).\n- [ ] The full N2 re-validation re-runs to completion on the declared\n      platforms and its results are recorded in this Slice's evidence —\n      the P2-S2 closure's owed remainder, discharged.\n- [ ] The selftest covers both repairs and is green on both platforms;\n      the frozen corpus digest is unmoved before and after.\n\n## Gate evidence\n\n<!-- Filled as gates complete: docs/evidence/gatebraid/P2-S3/ -->\n\n## gatebraid-metadata\n\n```yaml\nschema: gatebraid/slice@1\nslice_id: P2-S3\nstage: S2\nphase: P2\nworkflow_profile: classic\nenvironment: mixed-see-prose\nrisk: low\ndepends_on: []\nwrite_domains:\n  - bin/gatebraid-validate.py\n  - bin/gatebraid-validate-selftest.py\n  - docs/evidence/gatebraid/P2-S3/\nresource_locks: []\nrepair_limit: 2\nconsult_first: false\nparallel_mode: safe-single-writer\n```\n","closed_by":null,"reactions":{"url":"https://api.github.com/repos/MianliWang/gatebraid/issues/12/reactions","total_count":0,"+1":0,"-1":0,"laugh":0,"hooray":0,"confused":0,"heart":0,"rocket":0,"eyes":0},"timeline_url":"https://api.github.com/repos/MianliWang/gatebraid/issues/12/timeline","performed_via_github_app":null,"state_reason":null,"pinned_comment":null}
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh issue view 12 --repo MianliWang/gatebraid --json body
{"body":"# P2-S3 — gatebraid-validate repair: heuristic scope, markdown records, N2 re-validation completion\n\n## Goal\n\nRepair the two instrument defects `gatebraid-validate`'s first production\nrun exposed (friction #169, #170) and complete the N2 re-validation that\nrun left bounded: scope the placeholder heuristic to command and citation\nfields so GraphQL inline-fragment spreads and notes-field id\nabbreviations are classified as mentions, not elisions; add a\nmarkdown-gate-record mode (`## gatebraid-metadata` extraction, the\nADR-0026 form) so all four gate records of any Slice are within the\nvalidator's reach; then re-run the full N2 re-validation to completion\nand record it — discharging the remainder the P2-S2 closure named as\nowed. Files under repair: `bin/gatebraid-validate.py` and\n`bin/gatebraid-validate-selftest.py` (the ratified names; no new tool,\nno new name).\n\n## Context\n\n- Why now: the P2-S2 closure's bounded discharge (issue #10, the Closure\n  Resume's verbatim passage) leaves the full mechanical re-validation of\n  N2's four gate records owed until this Slice lands; O1 will rely on\n  the validator over real records, so the over-match is repaired before\n  the toolchain is leaned on.\n- Both repairs carry their falsifications: the heuristic fix is seeded\n  in both directions (a genuine elision must still reject — the\n  P2-S2-closure falsification pair is the model); the markdown mode is\n  seeded with a valid and an invalid embedded record.\n- Non-goals: no change to `bin/gatebraid-capture*.py` (never read, only\n  executed); no contract, schema, ADR, template or corpus text; no edit\n  to any merged historical gate record — `gate0.json`'s nine #171-class\n  citations stay recorded, not repaired.\n- Related: Phase P2 `#7` · P2-S1 `#8` · P2-S2 `#10` · PR `#11` ·\n  friction #169/#170/#171 · the P2-S2 Closure Resume rulings (a)–(c).\n\n## Acceptance\n\n- [ ] The 11 P2-S1 captures rejected at the P2-S2 closure validate\n      `accepted` with the repaired heuristic, AND a genuinely elided\n      capture still rejects — both shown by seeded runs, summaries\n      emitted by the instrument itself.\n- [ ] All four P2-S1 gate records (`gate0.json`, `gate1.md`, `gate2.md`,\n      `gate3.md`) are read and verdicts emitted by the validator's own\n      record mode; `gate0.json`'s nine genuine findings reproduce\n      (they are the record's, not the tool's).\n- [ ] The full N2 re-validation re-runs to completion on the declared\n      platforms and its results are recorded in this Slice's evidence —\n      the P2-S2 closure's owed remainder, discharged.\n- [ ] The selftest covers both repairs and is green on both platforms;\n      the frozen corpus digest is unmoved before and after.\n\n## Gate evidence\n\n<!-- Filled as gates complete: docs/evidence/gatebraid/P2-S3/ -->\n\n## gatebraid-metadata\n\n```yaml\nschema: gatebraid/slice@1\nslice_id: P2-S3\nstage: S2\nphase: P2\nworkflow_profile: classic\nenvironment: mixed-see-prose\nrisk: low\ndepends_on: []\nwrite_domains:\n  - bin/gatebraid-validate.py\n  - bin/gatebraid-validate-selftest.py\n  - docs/evidence/gatebraid/P2-S3/\nresource_locks: []\nrepair_limit: 2\nconsult_first: false\nparallel_mode: safe-single-writer\n```\n"}
```

## Required disclosures

- Deviations: the declared sweep commands invoke `docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py`, verification tooling written at this gate inside the frozen allowlist's evidence prefix, so that each declared command is short enough to freeze and dry-runnable exactly as written; it is not Slice implementation, which is confined to the two `bin/` files · the capture tool's `--form shell` was attempted twice for the sweep dry-runs and returned `STRUCTURE: the command could not be executed (FileNotFoundError)` on this host, once with a bare shell name and once with the resolved Windows path; the argv form was used instead and every dry-run capture is argv-form, and the shell-form behaviour was **not** investigated further because inspecting the capture tool's behaviour beyond its documented interface is a STOP-and-ask under the ratified isolation rule, not a licence to read — recorded here as a measured limitation and routed · T6 is assigned to the Windows half on a measured basis. The frozen plan states that the WSL half of the same command had not completed after thirteen minutes, which was true when the plan was frozen; that run has since COMPLETED and is superseded HERE rather than in the frozen text: WSL rc=0, elapsed 1,016,719 ms (16m57s) against 147,993 ms on Windows, a factor of 6.9, with `digest before` and `digest after` both f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686 — identical to the Windows half. The completed measurement CONFIRMS the assignment rather than changing it, and upgrades the plan's platform-independence claim for the digest from an argument to a measurement. The plan section is deliberately NOT edited: it is frozen under plan_hash, its statement was accurate at freeze time, and a later measurement belongs in the record rather than in a silently rewritten plan — a re-freeze would require the correct-course path and refrozen: true · this gate did not repair anything and did not edit any `bin/` file: the pre-repair outputs recorded above are the baseline the frozen plan is measured against, and every expected-green criterion in the plan describes the post-repair state that Gate 2 must produce · `git status --porcelain` reports this Slice's evidence directory as untracked, which the read-only gates permit; nothing is committed and no lease is held.
- Environment: Windows 11 host, Git Bash (MSYS2) shell, with the WSL half of `mixed-see-prose` exercised for T1, T5 and T7; `PYTHONDONTWRITEBYTECODE=1` on every Python invocation; Windows loader `C:\Python312\python.exe` (CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0) and WSL `/usr/bin/python3` (3.12.3, PyYAML 6.0.1, jsonschema 4.10.3); `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` call; every `gh api` endpoint written without a leading slash (friction #33).

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S3
gate: 1
environment: mixed-see-prose
executor: Claude Lead
base_sha: 63c8401f5df6ba446cf002232fcb280673c28e00
started_at: "2026-08-22T04:10:00Z"
ended_at: "2026-08-22T04:55:00Z"
result: needs_approval
approvals:
  - type: State Packet Approval
    comment_url: "https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5377522556"
    author: MianliWang
    at: "2026-08-22T03:04:46Z"
checks:
  - name: plan-complete
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: allowlist-exact
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: negative-criteria-declared-with-error-direction
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: acceptance-mapped-count-free
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: self-validation-point-named
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: command-budgets-declared
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: test-plan-dry-run-T1-windows
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T1-windows.json"
  - name: test-plan-dry-run-T1-wsl
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T1-wsl.json"
  - name: test-plan-dry-run-T3-surface
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T2-windows.json"
  - name: test-plan-dry-run-T5-windows
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T3-windows.json"
  - name: test-plan-dry-run-T5-wsl
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T3-wsl.json"
  - name: test-plan-dry-run-T7-windows
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T7-windows.json"
  - name: test-plan-dry-run-T7-wsl
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T7-wsl.json"
  - name: test-plan-dry-run-T8-surface
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T5-windows.json"
  - name: test-plan-dry-run-T6-corpus-digest
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G1-dryrun-T6-windows.json"
  - name: gate1-exit-checklist
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/gate1-exit-checklist.md"
  - name: allowlist-hash-reproduced
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G1-allowlist-hash.json"
  - name: plan-hash-reproduced
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G1-plan-hash.json"
  - name: write-domains-agreement
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G1-writedomains-readback.json"
  - name: exit-fields-readback
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G1-exit-fields-readback.json"
plan_hash: "eb89d3eaedc2690babb3086e3be7529f62fa03e7195746b3b8106ad85a626b18"
allowlist_hash: "81a0bb015ffbc5f3f6a27abfaec0a089c2b5522aa69e5ee30d5d7a01ecd404c0"
hash_commands:
  allowlist: "C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_hashes.py allowlist bin/gatebraid-validate.py bin/gatebraid-validate-selftest.py docs/evidence/gatebraid/P2-S3/"
  plan: "C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g1_hashes.py plan docs/evidence/gatebraid/P2-S3/gate1.md"
evidence_files:
  - docs/evidence/gatebraid/P2-S3/gate1.md
  - docs/evidence/gatebraid/P2-S3/gate1-exit-checklist.md
notes: "Gate 1 planning only; nothing repaired, no bin/ file edited, no lease, no branch, no commit. The dry-run outputs recorded here are the PRE-repair baseline and establish that each declared command runs as written on its assigned platform half; the plan's expected-green criteria describe the post-repair state Gate 2 must produce. bootstrap_exception is absent: the bounded evidence bootstrap expired at N2+N3 Gate 3 and this record claims none of it. Startability for the Slice was read from the operator-approved closed-set state packet under ruling R-a at Gate 0. The Gate 1 window was granted at https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5377794416 (author MianliWang, Q2-form read back, capture G1-Q2-approval); that grant is cited here and the approvals[] entry remains the State Packet Approval, matching the Gate 0 record's treatment of the record-container correction."
```
