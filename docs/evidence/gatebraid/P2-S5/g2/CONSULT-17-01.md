# CONSULT-17-01 — repair 2 of Gate 2: restore the frozen tool surface, and correct five record defects without creating a sixth of the same class

## Problem statement

An independent read-only review of Slice P2-S5's Gate 2 returned **R1, R2, R4,
R5 PASS and R3 FAIL on two grounds**, plus one HIGH finding outside R3's letter.
Repair 1 of the gate's unified repair sequence is already spent. This consult
precedes **repair 2, which is the last attempt**: if anything is still red after
it, the gate routes to `Human Diagnosis Required`.

Six defects must be repaired in one attempt:

- **F-01 (HIGH)** — the delivered tool declares two flags beyond the frozen
  scope, and one of them breaks the frozen scope's own stdout/exit invariant.
- **F-02 (HIGH)** — a record row is nominated into the byte-reproducible subset
  that cannot reproduce, by construction.
- **F-03 (MEDIUM)** — a disclosure states "ONE RESIDUE" where its own cited
  capture measures 14.
- **F-04, F-05, F-06 (LOW)** — an inflated elision total, eleven elision paths
  that are not committed-path spellings, and ten deviation bullets carrying no
  citation.

The danger this consult exists to avoid is the one that failed the record the
first time: **a statement the file makes about itself going false.** Repair 1 of
the sibling Slice P2-S6 introduced three fresh defects of exactly that class
while repairing three others.

## Constraints and forbidden operations

- **Scope**: not one byte outside `bin/gatebraid-ready.py` and
  `docs/evidence/gatebraid/P2-S5/g2/`. No `schema/` byte, no `fixtures/` byte,
  no edit to any other landed tool, no edit to the retained Gate 0 record, to
  `g0r/`, or to `g1/`.
- The frozen plan and its two hashes are **binding and unchanged**; any change
  to plan or allowlist voids the Plan Approval and returns the Slice to Gate 1.
- No Project field write (`Workflow` stays `Needs Review`), no label change,
  nothing pushed, no pull request, no merge.
- **The consultant is read-only and authors nothing in the tree.**
- ADR-0026 content classes only: metadata block, record rows, required
  disclosures, template-fixed headings.
- ADR-0028 decision 2: a mutable reference is pinned to a SHA **or** excluded
  from the deterministic subset **and said so**.
- ADR-0028 decision 3: a checker never quotes what it forbids into a record.
- The closed-set sweep's rules, regexes and residue criterion may **not** change
  (Plan Approval ruling 2); only explicit domain facts may be added, and F-08 is
  already ruled: the `fail`-typed sweep check **stays** `fail`.

## Files in scope

- `bin/gatebraid-ready.py` — declares the two out-of-scope flags (F-01).
- `docs/evidence/gatebraid/P2-S5/g2/gate2.md` — carries F-02 … F-06.
- `docs/evidence/gatebraid/P2-S5/g2/render-gate2.py` — generates that record;
  every prose defect above is a renderer edit, never a hand edit of the record.
- `docs/evidence/gatebraid/P2-S5/g1/plan.md` — the frozen scope (read-only).
- `docs/evidence/gatebraid/P2-S5/g1/negative-criteria.py` — the instrument whose
  union-of-untracked behaviour causes F-02 (read-only; frozen at Gate 1).

## Hypotheses already tried

| # | Hypothesis | Outcome |
|---|---|---|
| 1 | (repair 1, spent) N3's content limb fired because the Gate 1 mechanisation hard-codes two per-gate subdirectories where the frozen plan says "this gate's own subdirectories" | **Green.** A `g2/` copy naming three was made, falsified, and all six criteria hold. Not related to the six defects above. |

## Embedded evidence

### E-1 · The frozen scope sentence (`g1/plan.md`, the scope-is-read paragraph)

> All three historical attempts declare the identical scope: one file
> `bin/gatebraid-ready.py`; flags `--strict` and `--snapshot-command`; stdout one
> JSON document or nothing; producer failure and producer-output-undecodable as
> two distinct, loudly named exits; the consumer's own codes reused rather than
> renumbered; an allowlist of `bin/` plus the Slice's own evidence directory.

### E-2 · F-01, quoted verbatim from the review report

> The delivered tool declares **four** flags — `--strict`, `--snapshot-command`,
> `--consumer` (default `bin/gatebraid-frontier.py`), and `--version`.
>
> | Token | Occurrences across the six frozen documents |
> |---|---|
> | `--strict` | 28 |
> | `--snapshot-command` | 26 |
> | **`--consumer`** | **0** |
> | `--version` | 21 — **all of them `gh --version` / `python --version` probes**; none refers to the deliverable |
>
> The sharp edge is `--version`, and I ran it rather than reasoning about it:
>
> ```
> $ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready.py --version
> stdout: gatebraid-ready 1.0.0        <- not JSON
> exit  : 0
> ```
>
> That violates **two clauses of the frozen sentence at once**: stdout carries
> something that is neither one JSON document nor nothing, and it exits **0**, a
> code the tool's own epilog declares to be *"the CONSUMER'S OWN … passed through
> unchanged"* — that is, a verdict. A caller written against the frozen surface
> cannot distinguish `--version` from a successful ready verdict by exit status.
> The argparse `version` action bypasses the tool's own `SystemExit` guard, which
> deliberately re-raises on code 0.
>
> `--consumer` is the lesser half, but not nothing: it lets a caller substitute an
> arbitrary path that is then executed as a subprocess, widening an exec surface
> with **no declared test**.
>
> Why no instrument caught this: the scope pin asserts **presence** of the file and
> the two flags across all three historical attempts (`in 3 of 3 ok`). It is not a
> closure check, so an added flag cannot fire it.

**Operator's disposition on F-01: REMOVE.** Both flags leave the tool, together
with any code that exists only to serve them. The frozen surface is restored.

### E-3 · The `bin/gatebraid-ready.py` passages F-01 names

Module-level constants:

```python
VERSION = "1.0.0"
...
PRODUCER_PATH = "bin/gatebraid-snapshot.py"
CONSUMER_PATH = "bin/gatebraid-frontier.py"
```

The consumer runner, whose second parameter is the substitution point:

```python
def run_consumer(document_bytes, consumer_path):
    """Feed the document to the consumer on stdin and return (status, out, err).
    ...
    """
    proc = subprocess.run(
        [sys.executable, "-B", consumer_path, "-"],
        input=document_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr
```

The two declarations to be removed, and the `SystemExit` guard immediately after
them:

```python
    ap.add_argument(
        "--consumer", metavar="PATH", default=CONSUMER_PATH,
        help="the consumer to feed (default: %s)" % CONSUMER_PATH)
    ap.add_argument("--version", action="version",
                    version="gatebraid-ready %s" % VERSION)

    try:
        args = ap.parse_args(argv)
    except SystemExit as exc:
        # argparse exits 2 on a usage error, which is inside the consumer's
        # declared space and would be indistinguishable from a verdict.
        if exc.code in (0, None):
            raise
        sys.stderr.write("USAGE: bad arguments to gatebraid-ready\n")
        return EXIT_USAGE
```

The single call site of the removed `--consumer` value:

```python
        consumer_status, out, err = run_consumer(document, args.consumer)
```

**A fact bearing on the guard.** `--help` is **not** out of scope: the M2 frozen
record's own test-plan command 1 is
`python bin/gatebraid-ready.py --help` — *green: exit 0 and usage text naming
both `--strict` and `--snapshot-command`*. So `--help` remains, it still exits 0
through argparse, and the `if exc.code in (0, None): raise` clause is what lets
it. Removing `--version` does not make that clause dead.

### E-4 · F-02, quoted verbatim

> `V9` appears in the record's own sentence: *"IN the subset, and required to
> reproduce byte-identically: … V9 (pinned) …"*. It does not reproduce:
>
> ```
> stored:  changed paths       : 197     …  [... 185 more …]
> mine:    changed paths       : 160     …  [... 148 more …]
> ```
>
> Pinning `--base A..B` pins only the tracked half. When the builder ran it, 37 of
> this Slice's own files were still untracked; they are now committed, so the
> untracked half is empty and the count can only shrink. **The row can never
> reproduce again**, by construction.
>
> The record predicts this precisely, in the very disclosure that nominates it …
> That sentence and the nomination contradict each other, and the sentence is the
> true one. **The defect is the nomination**, not the measurement and not the
> criteria. … The natural repair is to move V9 beside V9b with its property
> stated, or to give the instrument a tracked-only mode so the pinned row
> genuinely reproduces.

### E-5 · F-03, quoted verbatim, and the record text it indicts

> The disclosure reads *"ONE RESIDUE IS LEFT DELIBERATELY UNEXPLAINED"* … The
> capture it cites reports:
>
> ```
> UNEXPLAINED RESIDUE: 14
> ```
>
> My own re-run over the current domain also reports **14**. … Exactly one is the
> disclosed friction citation inside the frozen corpus output. The other thirteen
> are **benign shape collisions** — two path fragments and a count ratio, one a
> `<word>/<word>` filename and one an `N/N` figure — and **eleven of the thirteen
> sit inside superseded `-pass1` captures** the gate retained deliberately. None
> is a repository identity. … the safety-critical claim is **true and
> independently verified** … What is wrong is the number in the prose.

The record's own two statements, which must both change:

- disclosure: `… and ONE RESIDUE IS LEFT DELIBERATELY UNEXPLAINED.`
- `checks[]`: `command: "the same run; one residue remains, an issue-shaped
  friction citation inside a frozen corpus case label, disclosed and not
  admitted by a rule change"`

**Operator's ruling F-08: ACCEPTED.** The check stays typed `fail`, with F-03's
count corrected and the diagnosis stated; a repair would need a rule change the
Plan Approval forbids. That ruling is the citation this deviation must carry.

### E-6 · F-04, and my own re-measurement of it

Review: *"The D5 elision reads 'shown 20 of 214 lines'. The capture's stdout is
**177** lines … The 214 is exactly reproducible as
`len(stdout.split("\n")) + len(stderr.splitlines())` = `178 + 36`, where the
stderr text carries **36 carriage returns for 18 lines** — `\r\r\n` endings, so
`splitlines()` counts each line twice. The honest combined total is **195**."*

I re-measured rather than adopting it:

```
stdout: newlines=177  splitlines=177  split("\n")=178
stderr: CR=36  splitlines=36  split("\n")=19
renderer combined splitlines = 214
```

The renderer's current rule is
`combined = stdout + ("\n" + stderr if stderr.strip() else "")` then
`combined.splitlines()`. I propose ONE stated replacement rule — *carriage
returns removed; exactly one newline between stdout and stderr; no trailing
blank* — and measured its effect on **every** capture in the directory:

```
PROPOSED RULE total for D5 = 195     (agrees with the review's honest total)
captures whose rendered line count moves under the rule:
  G2-D5-live-ready.json          214 -> 195
  G2-D6-producer-failure.json      4 -> 3
  G2-D8-consumer-refusal.json      5 -> 3
```

D6 and D8 are un-elided rows, so no `total` figure of theirs is printed; their
rendered blocks lose the doubled blank lines.

### E-7 · F-05 and F-06, quoted verbatim

> Every one reads `docs/evidence/gatebraid/P2-S5/g2\captures/…` — a backslash
> before `captures`. As written, **none** of the 11 is a tracked path (`git
> ls-tree` match 0/11); normalised to forward slashes, **all 11** are tracked
> (11/11).

> Measured: 15 deviation bullets; **5** cite something (`friction #15`,
> `ruling 2`, `ADR-0028` ×3); **10** cite neither a friction entry nor a ruling.

The backslash's origin is `CAPS = os.path.join(G, "captures")` in the renderer,
interpolated into the elision line.

### E-8 · F-07 — explicitly NOT repaired

The reviewer records a real gap in ADR-0026 (no sanctioned home for a
pre-submission correction the executor must still be honest about), declines to
fail anything over it, and queues it for an ADR clarification. **The operator
directs that those disclosures stand as they are.** Do not propose removing them.

### E-9 · My proposed fixes, for you to attack

1. **F-01** — delete the `--consumer` and `--version` `add_argument` calls;
   delete `VERSION`; change `run_consumer(document, args.consumer)` to use the
   module constant, and drop the now-unused parameter. Keep `CONSUMER_PATH`,
   keep the `SystemExit` guard (E-3 explains why), keep `--help`.
2. **F-02** — move `V9` out of the deterministic subset and into the exclusion
   list, with the reason the record already states: the six verdicts are stable;
   the listing is not. Do **not** modify the frozen Gate 1 instrument.
3. **F-03** — replace "ONE RESIDUE" with the measured count and a
   class-by-class diagnosis; correct the `checks[]` command string; cite the
   F-08 ruling. The hard-rule limb's claim is unchanged and stays.
4. **F-04** — adopt the E-6 rule in the renderer.
5. **F-05** — build the elision path with forward slashes.
6. **F-06** — give every deviation bullet a citation.

## Questions

1. **F-01 completeness.** Is deleting the two `add_argument` calls, the
   `VERSION` constant, and the `consumer_path` parameter the **complete and
   minimal** change, or does anything else in `bin/gatebraid-ready.py` exist
   only to serve the two removed flags? Check the file through `-C` rather than
   trusting my excerpt.
2. **F-01 side effects.** Does removing `--version` change the behaviour of any
   surviving path — in particular, is the `if exc.code in (0, None): raise`
   clause still reachable and still correct once `--help` is the only zero-exit
   argparse path? Is there any remaining way for this tool to put non-JSON on
   stdout and exit a code inside the consumer's declared space `{0,1,2,3}`?
3. **F-02 choice.** Is moving `V9` into the exclusions the correct repair, or
   should the pinned row instead be made genuinely reproducible? Note the
   constraint: the instrument is frozen at Gate 1 and rides on byte-identical,
   and a `g2/` copy already exists for a different domain fact.
4. **F-04 rule.** Is the E-6 rule the right single rule, and does it have any
   effect I have not measured — in particular on rows whose stderr is empty, or
   on the `shown` half of any elision?
5. **The class that fails records.** What is the **complete set of prose claims
   in `gate2.md`** that these six edits touch or create, each of which must be
   re-measured against the file and the repository **as they will exist after
   the commit**? Name each claim and the command that measures it. This is the
   question P2-S6's repair 1 failed to ask.
6. **Fresh self-reference.** Does any fix I propose create a new statement the
   file makes about itself that could go false — and if so, which, and what is
   the safer wording?

## Required response schema

Respond in exactly this structure (gatebraid/consult@1 `response`):
`findings` · `root_cause_hypotheses` (ranked, each with file-path evidence) ·
`recommended_change` (patch sketch as suggestion text — do not apply anything) ·
`risks` · `verification_steps` · `confidence` (low|medium|high).

## gatebraid-metadata

```yaml
schema: gatebraid/consult@1
consult_id: CONSULT-17-01
slice_id: P2-S5
trigger: repair-sequence
fingerprint_before: "slice/P2-S5 head 8fde380b26e44caba7754dacd0611f3d5ff026a8, tree 74de097bb05023cb955cc59fa1c7338e4524f229, base cbd065893b37f20713ae35b8d2673bf26fe4d2ad"
request:
  problem: "Repair 2 is the last attempt: restore the frozen two-flag tool surface and correct five record defects without creating a sixth of the self-reference class."
  constraints:
    - "Not one byte outside bin/gatebraid-ready.py and docs/evidence/gatebraid/P2-S5/g2/."
    - "No schema/ or fixtures/ byte; no edit to any other landed tool; the retained record, g0r/ and g1/ are frozen."
    - "The frozen plan and its two hashes are binding and unchanged."
    - "No Project field write, no label change, nothing pushed."
    - "The consultant is read-only and authors nothing in the tree."
    - "ADR-0026 content classes only; ADR-0028 decision 2 pin-or-exclude; ADR-0028 decision 3 no quoting what is forbidden."
    - "The closed-set sweep's rules, regexes and residue criterion may not change; F-08 is ruled and the check stays typed fail."
  files_in_scope:
    - "bin/gatebraid-ready.py"
    - "docs/evidence/gatebraid/P2-S5/g2/gate2.md"
    - "docs/evidence/gatebraid/P2-S5/g2/render-gate2.py"
    - "docs/evidence/gatebraid/P2-S5/g1/plan.md"
    - "docs/evidence/gatebraid/P2-S5/g1/negative-criteria.py"
  hypotheses_tried:
    - hypothesis: "N3's content limb fired because the Gate 1 mechanisation hard-codes two per-gate subdirectories where the frozen plan says this gate's own subdirectories"
      outcome: "Repair 1, green. A g2/ copy naming three was made and falsified; unrelated to the six defects under repair here."
  embedded_evidence: ["#embedded-evidence"]
  questions:
    - "Is deleting the two add_argument calls, the VERSION constant and the consumer_path parameter the complete and minimal F-01 change, or does other code exist only to serve the removed flags?"
    - "Does removing --version change any surviving path, is the zero-exit SystemExit clause still reachable and correct with --help as the only zero-exit argparse path, and does any way remain to put non-JSON on stdout and exit inside {0,1,2,3}?"
    - "Is moving V9 into the exclusions the correct F-02 repair, or should the pinned row be made genuinely reproducible given the Gate 1 instrument is frozen?"
    - "Is the proposed elision-total rule correct, and does it have effects not measured, on empty-stderr rows or on the shown half?"
    - "What is the complete set of prose claims in gate2.md that these edits touch or create, each of which must be re-measured after the commit, and what command measures each?"
    - "Does any proposed fix create a new statement the file makes about itself that could go false, and what is the safer wording?"
```
