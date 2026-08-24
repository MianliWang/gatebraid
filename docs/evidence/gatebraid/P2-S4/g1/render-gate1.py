"""Render docs/evidence/gatebraid/P2-S4/gate1.md.

Record-row outputs are GENERATED from the Gate 1 captures, never transcribed
(friction #96). The frozen-plan section is the one prose class ADR-0026 admits,
and it is the artefact plan_hash covers; the heading "## Plan (frozen at exit)"
is load-bearing byte-for-byte.

Usage: render-gate1.py <ended_at> <plan_hash|PENDING> <allowlist_hash|PENDING>
"""
import base64, json, os, sys

CAP = "docs/evidence/gatebraid/P2-S4/g1"
OUT = "docs/evidence/gatebraid/P2-S4/gate1.md"
STARTED = "2026-08-24T05:02:11Z"
ENDED, PLAN_HASH, ALLOW_HASH = sys.argv[1], sys.argv[2], sys.argv[3]

ALLOWLIST = ["bin/", "docs/evidence/gatebraid/P2-S4/"]

PLAN = """
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
"""

L = []
def w(s=""):
    L.append(s)

def cap(cid):
    return json.load(open(os.path.join(CAP, cid + ".json"), encoding="utf-8"))

def argv_line(d):
    inv = d["invocation"]
    env = inv.get("environment") or {}
    prefix = " ".join("%s=%s" % (k, env[k]) for k in sorted(env)) if isinstance(env, dict) else ""
    body = " ".join(
        (a if (a and not any(c in a for c in " \t\n\"'")) else "'" + a.replace("'", "'\\''") + "'")
        for a in inv.get("argv", []))
    return ("%s %s" % (prefix, body)).strip()

def stream(d, name):
    s = d.get("streams", {}).get(name, {})
    return base64.b64decode(s["data"]).decode("utf-8", "replace") if s.get("data") else ""

def row(label, cids, limit=None):
    w("**%s**" % label)
    w("```")
    for cid in cids:
        if not os.path.exists(os.path.join(CAP, cid + ".json")):
            # Intermediate pass only: the hash and post-condition captures are
            # taken against the rendered file, so they cannot exist until it is.
            # The final pass has every capture present.
            w("[capture %s pending -- rendered in the final pass]" % cid)
            continue
        d = cap(cid)
        w("$ " + argv_line(d))
        combined = stream(d, "stdout") + (("\n" + stream(d, "stderr")) if stream(d, "stderr").strip() else "")
        lines = combined.splitlines()
        if limit is not None and len(lines) > limit:
            for l in lines[:limit]:
                w(l)
            w("[... shown %d of %d lines; full output: %s/%s.json]" % (limit, len(lines), CAP, cid))
        else:
            for l in lines:
                w(l)
        w("(exit %d)" % d["exit_code"])
    w("```")
    w()

w("# Gate 1 evidence — P2-S4")
w()
w("## Plan (frozen at exit)")
w(PLAN.strip())
w()
w("## Records")
w()
w("**P1 — team findings flushed** (only if a read-only team ran)")
w("```")
w("No read-only team was used. gate-1-contract Action 2 makes the team optional;")
w("the option was considered and declined, so there are no findings to flush and")
w("no flush comment exists. Recorded rather than left silent.")
w("```")
w()
row("P2 — dry-run of every declared test command, on the declared environment (gate-1-contract action 4)",
    ["G1-dryrun-matrix"], limit=90)
row("P2 — D7, run separately for runtime", ["G1-dryrun-D7-windows"], limit=10)
row("P2 — N1 negative-criterion checker: holds on the current range, and fires on a range known to violate it",
    ["G1-dryrun-N1", "G1-dryrun-N1-falsify"], limit=14)
row("P2 — form probe: the declared output path denotes the same file on both halves (the Slice A class)",
    ["G1-formprobe-outpath"], limit=8)
row("P2 — form probe: P0-2 byte contract under a non-UTF-8 parent console (the BP-01 class)",
    ["G1-formprobe-byte-contract"], limit=12)
row("P2 — exit-checklist item measured, not asserted: every WRITE target named in the plan is inside the allowlist",
    ["G1-plan-path-scan"], limit=24)
w("**P3 — exit checklist completed, every item evidence-backed**")
w("```")
w("docs/evidence/gatebraid/P2-S4/g1/gate1-exit-checklist.md")
w("```")
w()
row("P4 — allowlist_hash reproduced", ["G1-allowlist-hash"])
row("P5 — plan_hash reproduced", ["G1-plan-hash"])
row("P6 — the sanctioned write_domains post-condition on the Slice issue",
    ["G1-writedomains-check"], limit=20)

w("## Required disclosures")
w()
for d in [
    "Deviations: Action 4 dry-run of a greenfield deliverable is recorded in two parts, and the judgment is "
    "disclosed rather than assumed. Eight of the declared commands target tools this Slice will write, so they "
    "cannot exit 0 today. Each was RUN as declared and produced a non-zero exit naming its declared target as "
    "absent and nothing else wrong, and each interpreter-and-path form was separately proven on this environment "
    "by a TWIN command of identical shape against a file that exists, on both halves. Action 4 exists to catch the "
    "Slice A defect, a command well-formed on inspection that cannot run there; the twin is what tests that, and "
    "Slice A's own defect would have failed its twin.",

    "Deviations: the Slice A path class is tested directly rather than argued. Every declared output path is "
    "repository-relative and under the allowlist; the probe writes that path from one half and reads it from the "
    "other, both ways, and both halves resolve it to the same file. No declared command uses a system temporary "
    "directory.",

    "Deviations: the D1a and D1b twin commands pass --help to bin/gatebraid-capture-selftest.py, which does not "
    "define that option and therefore ran its full selftest. The twin's purpose, proving the interpreter and "
    "repository-relative path form resolve on this environment, is served either way, and the extra work is "
    "disclosed rather than left to be noticed in the runtime.",

    "Deviations: no read-only team was used. gate-1-contract Action 2 makes it optional; declining is recorded "
    "with its reason in the P1 row.",

    "Deviations: the P0-2 byte contract was measured at Gate 1 rather than only declared, because BP-01 fired on "
    "this host during this Slice's Gate 0. Under a forced cp936 parent console the text path emitted cp936 bytes "
    "that are not valid UTF-8, and the binary-stdout path emitted byte-exact UTF-8. The declared D5 command "
    "therefore tests a failure already shown to be real and reproducible here.",

    "Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; shell Git Bash MINGW64 with "
    "Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh call pins "
    "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid with endpoints carrying no leading slash; every Python invocation "
    "carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL half; Windows interpreter "
    "C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL /usr/bin/python3 with "
    "CPython 3.12.3, jsonschema 4.10.3. environment=mixed-see-prose: the gate ran on the Windows host and the WSL "
    "half is evidence.",
]:
    w("- " + d)
w()
w("## gatebraid-metadata")
w()
w("```yaml")
w("""schema: gatebraid/gate-run@2
slice_id: P2-S4
gate: 1
environment: mixed-see-prose
executor: Claude Lead
base_sha: df666070ead7fa21bc72b6c99d2644923b37e787
started_at: "%s"
ended_at: "%s"
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
plan_hash: "%s"
allowlist_hash: "%s"
hash_commands:
  allowlist: "C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/hash-allowlist.py"
  plan: "C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/g1/hash-plan.py docs/evidence/gatebraid/P2-S4/gate1.md"
evidence_files:
  - docs/evidence/gatebraid/P2-S4/gate1.md
notes: "Gate 1 planning for O0's tool half. No read-only team was used; the option is recorded as declined. Eight declared commands target deliverables this Slice will write and were dry-run as declared plus a form twin on each half, per the disclosure. The frozen surface is held unmoved by measurement at named points rather than by assumption."
""" % (STARTED, ENDED, PLAN_HASH, ALLOW_HASH))
w("```")

open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("WROTE %s" % OUT)
