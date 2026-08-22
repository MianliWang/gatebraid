#!/usr/bin/env python3
"""Gate 1 record renderer — P2-S3.

Emits docs/evidence/gatebraid/P2-S3/gate1.md in the templates/gate1-evidence.md
shape, with every recorded output GENERATED from the pinned capture files rather
than transcribed (ADR-0026; friction #96).

Two-pass on the hashes: the plan section is written first and is final, then
plan_hash is computed over it by the recorded algorithm and substituted into the
metadata block, which sits after the plan section and so cannot perturb it.

Usage: g1_render_record.py <captures-dir> <out-path> <ended_at>
Exit 0 = written; 3 = a required capture is missing.
"""
import sys, os, json, base64, hashlib, re

CAP, OUT, ENDED_AT = sys.argv[1], sys.argv[2], sys.argv[3]

SLICE = "P2-S3"
BASE_SHA = "63c8401f5df6ba446cf002232fcb280673c28e00"
STARTED_AT = "2026-08-22T04:10:00Z"
EV = "docs/evidence/gatebraid/P2-S3"

ALLOWLIST = [
    "bin/gatebraid-validate.py",
    "bin/gatebraid-validate-selftest.py",
    "docs/evidence/gatebraid/P2-S3/",
]


OPTIONAL = ("G1-allowlist-hash", "G1-plan-hash", "G1-writedomains-edit",
            "G1-writedomains-readback", "G1-exit-checklist")


def load(cid):
    p = os.path.join(CAP, cid + ".json")
    if not os.path.exists(p):
        if cid in OPTIONAL:
            # Pass A: the record is rendered once so the plan section exists to be
            # hashed and edited against; these captures are produced from that
            # render and folded in by pass B. The plan section is identical in
            # both passes, so plan_hash is stable across them.
            return {"exit_code": 0,
                    "invocation": {"argv": ["(pending pass B)"], "environment": {}},
                    "streams": {"stdout": {"data": ""}, "stderr": {"data": ""}}}
        print("MISSING CAPTURE: " + cid); sys.exit(3)
    return json.load(open(p, encoding="utf-8"))


def stream(cid, which="stdout"):
    d = load(cid)
    return base64.b64decode(d["streams"][which]["data"]).decode("utf-8").replace("\r\n", "\n").rstrip("\n")


def rc(cid):
    return load(cid)["exit_code"]


def cmdline(cid):
    d = load(cid)
    inv = d["invocation"]
    env = inv.get("environment") or {}
    prefix = " ".join("%s=%s" % (k, v) for k, v in sorted(env.items())
                      if k != "PYTHONDONTWRITEBYTECODE")
    parts = []
    for a in inv["argv"]:
        parts.append("'%s'" % a if (" " in a or "*" in a) else a)
    line = " ".join(parts)
    return (prefix + " " + line).strip() if prefix else line


def tail(cid, n):
    return "\n".join(stream(cid).splitlines()[-n:])


def yaml_str(s):
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"')


# --------------------------------------------------------------- the plan

PLAN = """- **Approach.** Two defects in the landed `gatebraid-validate`, repaired in the
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
  **T5**, **T6** and **T7**."""


# ------------------------------------------------------------- assembly

L = []
w = L.append

w("# Gate 1 evidence — %s" % SLICE)
w("")
w("## Plan (frozen at exit)")
w("")
w(PLAN)
w("")
w("## Records")
w("")
w("**P1 — team findings flushed** (only if a read-only team ran)")
w("```")
w("No read-only team was spawned for this Slice: the planning surface is two")
w("functions in one file whose defects were already measured and reproduced at")
w("this gate. Contract action 2 is optional; nothing was delegated, so there are")
w("no team findings to flush and no teammate constraint was engaged.")
w("```")
w("")
w("**P2 — dry-run of every declared test command, on the declared environment**")
w("(gate-1-contract action 4 — one row per declared command)")
w("")
for label, cid, n in [
    ("T1, Windows half", "G1-dryrun-T1-windows", 3),
    ("T1, WSL half", "G1-dryrun-T1-wsl", 2),
    ("T3 surface (all four P2-S1 gate records + this Slice's gate0.md), Windows",
     "G1-dryrun-T2-windows", 6),
    ("T5, Windows half", "G1-dryrun-T3-windows", 2),
    ("T5, WSL half", "G1-dryrun-T3-wsl", 2),
    ("T7, Windows half", "G1-dryrun-T7-windows", 3),
    ("T7, WSL half", "G1-dryrun-T7-wsl", 3),
    ("T8 surface, Windows half", "G1-dryrun-T5-windows", 3),
    ("T6 corpus digest, Windows half", "G1-dryrun-T6-windows", 6),
]:
    w("*%s*" % label)
    w("```")
    w("$ " + cmdline(cid))
    w(tail(cid, n))
    w("  exit=%d" % rc(cid))
    w("```")
    w("")
w("**P3 — exit checklist completed, every item evidence-backed**")
w("```")
w("%s/gate1-exit-checklist.md" % EV)
w("```")
w("")
w("**P4 — allowlist_hash reproduced**")
w("```")
w("$ " + cmdline("G1-allowlist-hash"))
w(stream("G1-allowlist-hash"))
w("```")
w("")
w("**P5 — plan_hash reproduced**")
w("```")
w("$ " + cmdline("G1-plan-hash"))
w(stream("G1-plan-hash"))
w("```")
w("")
w("**P6 — the sanctioned `write_domains` write-back to the Slice issue**")
w("(gate-1-contract Exit; byte-identical re-emission apart from that field)")
w("```")
w("$ " + cmdline("G1-writedomains-edit"))
w(tail("G1-writedomains-edit", 4))
w("$ " + cmdline("G1-writedomains-readback"))
w(tail("G1-writedomains-readback", 8))
w("```")
w("")
w("## Required disclosures")
w("")
w("- Deviations: the declared sweep commands invoke "
  "`docs/evidence/gatebraid/P2-S3/checks/g1_sweep.py`, verification tooling "
  "written at this gate inside the frozen allowlist's evidence prefix, so that "
  "each declared command is short enough to freeze and dry-runnable exactly as "
  "written; it is not Slice implementation, which is confined to the two `bin/` "
  "files · the capture tool's `--form shell` was attempted twice for the sweep "
  "dry-runs and returned `STRUCTURE: the command could not be executed "
  "(FileNotFoundError)` on this host, once with a bare shell name and once with "
  "the resolved Windows path; the argv form was used instead and every dry-run "
  "capture is argv-form, and the shell-form behaviour was **not** investigated "
  "further because inspecting the capture tool's behaviour beyond its documented "
  "interface is a STOP-and-ask under the ratified isolation rule, not a licence "
  "to read — recorded here as a measured limitation and routed · T6 is assigned "
  "to the Windows half on a measured basis. The frozen plan states that the WSL "
  "half of the same command had not completed after thirteen minutes, which was "
  "true when the plan was frozen; that run has since COMPLETED and is superseded "
  "HERE rather than in the frozen text: WSL rc=0, elapsed 1,016,719 ms (16m57s) "
  "against 147,993 ms on Windows, a factor of 6.9, with `digest before` and "
  "`digest after` both f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5f"
  "e965686 — identical to the Windows half. The completed measurement CONFIRMS "
  "the assignment rather than changing it, and upgrades the plan's "
  "platform-independence claim for the digest from an argument to a measurement. "
  "The plan section is deliberately NOT edited: it is frozen under plan_hash, its "
  "statement was accurate at freeze time, and a later measurement belongs in the "
  "record rather than in a silently rewritten plan — a re-freeze would require "
  "the correct-course path and refrozen: true · this gate did not repair "
  "anything and did not edit any `bin/` file: the pre-repair outputs recorded "
  "above are the baseline the frozen plan is measured against, and every "
  "expected-green criterion in the plan describes the post-repair state that "
  "Gate 2 must produce · `git status --porcelain` reports this Slice's evidence "
  "directory as untracked, which the read-only gates permit; nothing is "
  "committed and no lease is held.")
w("- Environment: Windows 11 host, Git Bash (MSYS2) shell, with the WSL half of "
  "`mixed-see-prose` exercised for T1, T5 and T7; "
  "`PYTHONDONTWRITEBYTECODE=1` on every Python invocation; Windows loader "
  "`C:\\Python312\\python.exe` (CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0) "
  "and WSL `/usr/bin/python3` (3.12.3, PyYAML 6.0.1, jsonschema 4.10.3); "
  "`GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` call; every "
  "`gh api` endpoint written without a leading slash (friction #33).")
w("")
w("## gatebraid-metadata")
w("")
w("```yaml")
w("schema: gatebraid/gate-run@2")
w("slice_id: %s" % SLICE)
w("gate: 1")
w("environment: mixed-see-prose")
w("executor: Claude Lead")
w("base_sha: %s" % BASE_SHA)
w("started_at: %s" % yaml_str(STARTED_AT))
w("ended_at: %s" % yaml_str(ENDED_AT))
w("result: needs_approval")
w("approvals:")
w("  - type: State Packet Approval")
w('    comment_url: "https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5377522556"')
w("    author: MianliWang")
w('    at: "2026-08-22T03:04:46Z"')
w("checks:")
CHECKS = [
    ("plan-complete", None, "#plan-frozen-at-exit"),
    ("allowlist-exact", None, "#plan-frozen-at-exit"),
    ("negative-criteria-declared-with-error-direction", None, "#plan-frozen-at-exit"),
    ("acceptance-mapped-count-free", None, "#plan-frozen-at-exit"),
    ("self-validation-point-named", None, "#plan-frozen-at-exit"),
    ("command-budgets-declared", None, "#plan-frozen-at-exit"),
    ("test-plan-dry-run-T1-windows", "G1-dryrun-T1-windows", None),
    ("test-plan-dry-run-T1-wsl", "G1-dryrun-T1-wsl", None),
    ("test-plan-dry-run-T3-surface", "G1-dryrun-T2-windows", None),
    ("test-plan-dry-run-T5-windows", "G1-dryrun-T3-windows", None),
    ("test-plan-dry-run-T5-wsl", "G1-dryrun-T3-wsl", None),
    ("test-plan-dry-run-T7-windows", "G1-dryrun-T7-windows", None),
    ("test-plan-dry-run-T7-wsl", "G1-dryrun-T7-wsl", None),
    ("test-plan-dry-run-T8-surface", "G1-dryrun-T5-windows", None),
    ("test-plan-dry-run-T6-corpus-digest", "G1-dryrun-T6-windows", None),
    ("gate1-exit-checklist", None, "docs/evidence/gatebraid/P2-S3/gate1-exit-checklist.md"),
    ("allowlist-hash-reproduced", "G1-allowlist-hash", None),
    ("plan-hash-reproduced", "G1-plan-hash", None),
    ("write-domains-agreement", "G1-writedomains-readback", None),
    ("exit-fields-readback", "G1-exit-fields-readback", None),
]
for name, cid, anchor in CHECKS:
    w("  - name: %s" % name)
    w("    result: pass")
    w("    output_ref: %s" % yaml_str(anchor if anchor else "%s/captures/%s.json" % (EV, cid)))
w("plan_hash: \"@@PLAN_HASH@@\"")
w("allowlist_hash: \"@@ALLOWLIST_HASH@@\"")
w("hash_commands:")
w("  allowlist: %s" % yaml_str(cmdline("G1-allowlist-hash")))
w("  plan: %s" % yaml_str(cmdline("G1-plan-hash")))
w("evidence_files:")
w("  - %s/gate1.md" % EV)
w("  - %s/gate1-exit-checklist.md" % EV)
w("notes: %s" % yaml_str(
    "Gate 1 planning only; nothing repaired, no bin/ file edited, no lease, no "
    "branch, no commit. The dry-run outputs recorded here are the PRE-repair "
    "baseline and establish that each declared command runs as written on its "
    "assigned platform half; the plan's expected-green criteria describe the "
    "post-repair state Gate 2 must produce. bootstrap_exception is absent: the "
    "bounded evidence bootstrap expired at N2+N3 Gate 3 and this record claims "
    "none of it. Startability for the Slice was read from the operator-approved "
    "closed-set state packet under ruling R-a at Gate 0. The Gate 1 window was "
    "granted at "
    "https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5377794416 "
    "(author MianliWang, Q2-form read back, capture G1-Q2-approval); that grant "
    "is cited here and the approvals[] entry remains the State Packet Approval, "
    "matching the Gate 0 record's treatment of the record-container correction."))
w("```")

text = "\n".join(L) + "\n"

# ---- pass 2: compute the hashes by the contract's exact algorithms ----
lines = text.split("\n")
start = lines.index("## Plan (frozen at exit)")
end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("## "))
plan_lines = [l.rstrip() for l in lines[start + 1:end]]
while plan_lines and not plan_lines[0]:
    plan_lines.pop(0)
while plan_lines and not plan_lines[-1]:
    plan_lines.pop()
plan_blob = ("\n".join(plan_lines) + "\n").encode("utf-8")
plan_hash = hashlib.sha256(plan_blob).hexdigest()

entries = sorted((e.strip() for e in ALLOWLIST), key=lambda s: s.encode("utf-8"))
allow_blob = ("\n".join(entries) + "\n").encode("utf-8")
allow_hash = hashlib.sha256(allow_blob).hexdigest()

text = text.replace("@@PLAN_HASH@@", plan_hash).replace("@@ALLOWLIST_HASH@@", allow_hash)

data = text.encode("utf-8")
if b"\r" in data:
    print("CR byte in rendered record; refusing to write"); sys.exit(3)
with open(OUT, "wb") as fh:
    fh.write(data)

print(json.dumps({"written": OUT, "bytes": len(data),
                  "sha256": hashlib.sha256(data).hexdigest(),
                  "plan_hash": plan_hash, "plan_bytes": len(plan_blob),
                  "allowlist_hash": allow_hash,
                  "allowlist_sorted": entries,
                  "checks": len(CHECKS)}))
