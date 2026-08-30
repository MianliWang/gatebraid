"""Render docs/evidence/gatebraid/P2-S6/gate1.md from the plan and the captures.

Record-row outputs are GENERATED from the capture records, never transcribed
(friction #96). The frozen plan is the ONE prose class (ADR-0026 section 1) and
is read verbatim from g1/plan.md; the heading `## Plan (frozen at exit)` is
load-bearing byte-for-byte because plan_hash covers the lines strictly between
it and the next line beginning with `## `.

Usage: render-gate1.py <ended_at> <plan_hash> <allowlist_hash>
Pass PENDING for either hash on the first pass; compute the hashes from the
rendered file, then re-render with them. The plan section is identical on both
passes, so plan_hash is stable across the re-render - which P5 then verifies by
recomputing it from the final file.
"""
import base64, json, os, sys

G = "docs/evidence/gatebraid/P2-S6/g1"
OUT = "docs/evidence/gatebraid/P2-S6/gate1.md"
STARTED = "2026-08-29T08:22:58Z"
ENDED, PLAN_HASH, ALLOWLIST_HASH = sys.argv[1], sys.argv[2], sys.argv[3]

L = []


def w(s=""):
    L.append(s)


def cap(cid):
    return json.load(open(os.path.join(G, cid + ".json"), encoding="utf-8"))


def argv_line(d):
    inv = d["invocation"]
    env = inv.get("environment") or {}
    prefix = " ".join("%s=%s" % (k, env[k]) for k in sorted(env))
    body = " ".join(
        (a if (a and not any(c in a for c in " \t\n\"'")) else "'" + a.replace("'", "'\\''") + "'")
        for a in inv.get("argv", []))
    return ("%s %s" % (prefix, body)).strip()


def stream_text(d, name):
    s = d.get("streams", {}).get(name, {})
    if not s.get("data"):
        return ""
    return base64.b64decode(s["data"]).decode("utf-8", "replace")


def row(label, cids, limit=None, head=None):
    w("**%s**" % label)
    w("```")
    for cid in cids:
        if not os.path.isfile(os.path.join(G, cid + ".json")):
            # First pass only: this row's capture is produced BY running a
            # command against the rendered file, so it cannot exist before the
            # first render. The second render carries it.
            w("PENDING FIRST RENDER: %s" % cid)
            continue
        d = cap(cid)
        w("$ " + argv_line(d))
        text = stream_text(d, "stdout")
        err = stream_text(d, "stderr")
        combined = text + (("\n" + err) if err.strip() else "")
        lines = combined.splitlines()
        total = len(lines)
        if limit is not None and total > limit:
            keep = lines[:head] if head else []
            tail = lines[-(limit - len(keep)):]
            for l in keep:
                w(l)
            w("[... shown %d of %d lines; full output: %s/%s.json]"
              % (limit, total, G, cid))
            for l in tail:
                w(l)
        else:
            for l in lines:
                w(l)
        w("(exit %d)" % d["exit_code"])
    w("```")
    w()


DISCLOSURES = [
    "Deviations: no read-only Agent Team was used. gate-1-contract action 2 makes it optional; the decision "
    "and its reason are recorded in the P1 row rather than left implicit. Nothing was flushed because nothing "
    "was spawned, and the constraint list of failure-disposition row 2 is therefore vacuously satisfied "
    "rather than tested.",

    "Deviations: action 4's dry-run of a not-yet-written deliverable is recorded honestly and in two classes. "
    "Six of the eight declared commands ran to their full green criterion today: D1, D2, D3, D4, D7 and D8. "
    "Two, D5 and D6, target the repaired live transport and cannot be green before it exists; each was RUN AS "
    "DECLARED on this environment and produced exit 3 naming exactly the defect this Slice repairs and "
    "nothing else wrong. Their command form is additionally corroborated by this Slice's own Gate 0, where "
    "the identical snapshot and frontier invocations ran and were captured. Action 4 exists to catch a "
    "command well-formed on inspection that cannot run there; these run there.",

    "Deviations: the D5 and D6 dry-runs wrote their outputs into g1/dryrun-out/ rather than the g2 captures "
    "directory the frozen commands name, because creating a Gate 2 directory at Gate 1 would assert a gate "
    "that has not opened. The substitution is the output directory only; interpreter, flags, repository-"
    "relative path form and allowlist prefix are identical, and both declared paths lie under "
    "docs/evidence/gatebraid/P2-S6/, which N1 covers.",

    "Deviations: the negative criteria were falsified before they were trusted, and the falsification found a "
    "defect in criterion N4 itself. Its first mechanisation read `imports nothing outside the standard "
    "library` and FIRED on the unmodified source, because bin/gatebraid-snapshot.py already imports "
    "jsonschema to validate its own output against the frozen schema. That is a defect in the criterion, not "
    "in the tool: the criterion says the Slice adds no runtime dependency, not that the tool had none. N4 now "
    "compares against BASELINE_NONSTDLIB, the non-stdlib import set measured on the frozen base and frozen "
    "beside it. Recorded rather than quietly corrected.",

    "Deviations: N4 and N5 read a source surface, so falsifying them required pointing the SAME instrument - "
    "not a copy - at a seeded surface, which is why negative-criteria.py carries --code-surface-dir. The "
    "seeded files under g1/falsification/ are hand-written and are not part of the code surface; they exist "
    "so that a criterion which has only ever held can be shown able to fire. All five criteria fired at D8 "
    "and all five hold at D7.",

    "Deviations: D1 takes materially longer than the other declared commands - it re-derives the corpus "
    "digest across all seven corpora - and was captured as a background run for that reason. The runtime is "
    "recorded here so that a Gate 2 executor budgets for it rather than reading a slow command as a hung one.",

    "Deviations: the frozen corpus digest is unmoved by this Slice BY CONSTRUCTION, not by hope. The digest "
    "scope, printed by the instrument itself, is the seven corpora plus CORPORA.json, schema, run-corpus.py, "
    "runner-selftest.py and the fixtures listing. This Slice's allowlist is bin/ and its own evidence "
    "directory, and neither intersects that scope; N3 mechanises the same guarantee from the diff side. D1 "
    "measures it rather than relying on the argument.",

    "Deviations: the selftest of the code surface takes no arguments, so no falsification flag was invented "
    "for it. Its falsification is intrinsic and is stated in the plan: S01 is the positive control that a "
    "tool rejecting everything would fail, and every other condition seeds a mutation and requires the tool "
    "to catch it. Inventing a --falsify flag to make the test plan look symmetrical would have been a "
    "fabricated interface.",

    "Deviations: three Gate 1 instruments were copied byte-identically from the P2-S4 Gate 1 evidence and "
    "re-parameterized to this Slice's constants only - hash-allowlist.py (its write-domain list), "
    "plan-path-scan.py (its allowlist prefixes) and writedomains-check.py (its allowlist and the issue it "
    "reads). hash-plan.py was copied and is BYTE-IDENTICAL to the P2-S4 file, sha256 "
    "17649cdb5535f4cc09e114ca135e23750aabfa35b69de1d8cd0263d690ed0ada, because it takes its target as an "
    "argument and needed no change. No rule of any instrument was altered.",

    "Deviations: a Gate 0 instrument was edited at Gate 1 and the edit was REVERTED rather than kept. Extending the closed-set sweep for this gate's prose, I first modified docs/evidence/gatebraid/P2-S6/checks-g0-closed-set-sweep.py in place - the file three Gate 0 captures name as an input and pin by sha256. That would have left the CLOSED Gate 0 record citing an instrument whose bytes no longer existed. The file was restored and re-measured to df7b756a500c682133f7ab4935b0ffdbdff41d1bf0213223781c37f5e58b9cd6, the exact hash all three Gate 0 captures recorded, so the Gate 0 record is reproducible again; the Gate 1 additions live in a separate copy, g1/checks-g1-closed-set-sweep.py, which was falsified on all three limbs after the change. A closed gate's instruments are not editable by a later gate, and this is recorded rather than quietly reverted.",

    "Deviations: eight sweep residues in an earlier draft of this record were my own row labels, written with a slash joining the row group to the ordinal, P2 then D1 through D8. They were removed AT SOURCE by renaming the labels rather than by widening the sweep's allowlist: a checker should not be taught to ignore something the record need not have said. The remaining classes are genuinely unavoidable and are named explicitly in the Gate 1 copy - JSON Schema pointer segments printed by the corpus runner, two Windows path segments produced when a path containing a space is split, this Slice's own g1 directory, a backslash-n rendered inside a Python bytes repr, and one prose pair from a frozen corpus case name. Exact strings only, never a regex.",

    "Deviations: this record's own machine validation and closed-set sweep necessarily ran against the byte-state produced by the final render, and their captures are cited by output_ref rather than inlined as record rows - a document that quoted its own verification would change the bytes that verification read. The plan section, which is what plan_hash covers and what a Plan Approval binds, is byte-identical across every render pass; only the Records rows and the metadata block moved. plan_hash was recomputed from the FINAL file after the last render and equals the embedded value.",

    "Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; shell Git Bash MINGW64 "
    "with Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh "
    "call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every "
    "Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL "
    "half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; "
    "WSL /usr/bin/python3 with CPython 3.12.3. environment=mixed-see-prose: the tool runs on the Windows host "
    "and the WSL half is evidence, and the transport-independent selftest is declared and dry-run on both.",
]

METADATA = """schema: gatebraid/gate-run@2
slice_id: P2-S6
gate: 1
environment: mixed-see-prose
executor: Claude Lead
base_sha: 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
started_at: "%(started)s"
ended_at: "%(ended)s"
result: needs_approval
checks:
  - name: plan-complete
    command: "approach, write_domains, test plan, risk notes, rollback note, five negative criteria"
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: allowlist-exact
    command: "docs/evidence/gatebraid/P2-S6/g1/hash-allowlist.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g1/G1-allowlist-hash.json"
  - name: plan-paths-inside-allowlist
    command: "docs/evidence/gatebraid/P2-S6/g1/plan-path-scan.py docs/evidence/gatebraid/P2-S6/gate1.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g1/G1-plan-path-scan.json"
  - name: test-plan-dry-run
    command: "D1 through D8, each run on the declared environment; D5 and D6 run as declared and exit 3 naming the unrepaired defect"
    result: pass
    output_ref: "#records"
  - name: negative-criteria-falsified
    command: "negative-criteria.py --changed-from SEED-negative-criteria.txt --code-surface-dir g1/falsification (all five must fire)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g1/G1-dryrun-D8-negative-falsify.json"
  - name: negative-criteria-hold
    command: "negative-criteria.py (real diff against the frozen base)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g1/G1-dryrun-D7-negative.json"
  - name: corpus-digest-unmoved
    command: "fixtures/runner-selftest.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g1/G1-dryrun-D1-corpus-digest.json"
  - name: frozen-corpus-passes-unchanged
    command: "fixtures/run-corpus.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g1/G1-dryrun-D2-corpus.json"
  - name: gate1-exit-checklist
    command: "templates/gatebraid-gate1-exit-checklist.md, every item evidence-backed"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g1/gate1-exit-checklist.md"
  - name: closed-set-sweep-falsified
    command: "g1/checks-g1-closed-set-sweep.py (seeded domain; must fire on the repository, node and issue limbs)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g1/G1-closed-set-sweep-falsify.json"
  - name: closed-set-sweep-over-gate1-record
    command: "g1/checks-g1-closed-set-sweep.py docs/evidence/gatebraid/P2-S6/gate1.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g1/G1-record-sweep.json"
  - name: gate1-record-machine-validated
    command: "bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S6/gate1.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g1/G1-record-validation.json"
  - name: write-domains-agreement
    command: "docs/evidence/gatebraid/P2-S6/g1/writedomains-check.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g1/G1-writedomains-check.json"
plan_hash: "%(plan_hash)s"
allowlist_hash: "%(allowlist_hash)s"
hash_commands:
  allowlist: "PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/g1/hash-allowlist.py"
  plan: "PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/g1/hash-plan.py docs/evidence/gatebraid/P2-S6/gate1.md"
evidence_files:
  - docs/evidence/gatebraid/P2-S6/gate1.md
notes: "Planning for the snapshot live-transport repair. The two defects are the ones the P2-S5 Gate 0 stop diagnosed byte-exactly and this Slice's own Gate 0 reproduced at class level: D-A, three issue-backed sources served from one bulk endpoint with page_index structurally unused; D-B, live pages parsed with the replay transcript's key shape. The plan repairs them in two layers and leaves the classifier, the assembly and the whole replay path untouched, so every pre-existing selftest condition staying green is the regression evidence. Gate 0 opening comment 5461039588 and the Dirty Baseline Acceptance it carried belong to the Gate 0 record and are not re-entered here; this gate opened no approval and carries no approvals[] entry. Base SHA is not re-touched at this gate. A recorded human approval comment is the only door to Gate 2."
"""

w("# Gate 1 evidence - P2-S6")
w()
w("## Plan (frozen at exit)")
w()
plan = open(os.path.join(G, "plan.md"), encoding="utf-8").read().rstrip("\n")
for line in plan.split("\n"):
    if line.startswith("## "):
        raise SystemExit("STRUCTURE: the plan contains a '## ' line, which would "
                         "truncate plan_hash's payload: %r" % line)
    w(line)
w()
w("## Records")
w()

w("**P1 - Agent Team: NOT used, and the decision recorded rather than left implicit**")
w("```")
w("gate-1-contract action 2 makes the read-only team OPTIONAL. No team was")
w("spawned for this Slice. Reason: the two defects were already diagnosed")
w("byte-exactly against the source that ran (the P2-S5 Gate 0 stop), the target")
w("shapes are frozen in the O1-B1 live-shapes corpus, and this Slice's own Gate 0")
w("reproduced the failure at class level - so there was no open question a")
w("read-only teammate could close that reading the frozen corpus did not.")
w("Consequently there are NO team findings to flush, and the flush-before-")
w("dissolution constraint is vacuously satisfied rather than exercised.")
w("(no command: nothing was spawned)")
w("```")
w()

row("P2 D1 - corpus digest unmoved, and the runner's own conditions",
    ["G1-dryrun-D1-corpus-digest"], limit=18, head=2)
row("P2 D2 - the whole frozen corpus passes unchanged; the four live-shapes mutations stay killed",
    ["G1-dryrun-D2-corpus"], limit=16, head=6)
row("P2 D3 - snapshot selftest, Windows half", ["G1-dryrun-D3-selftest-windows"], limit=12, head=2)
row("P2 D4 - snapshot selftest, WSL half", ["G1-dryrun-D4-selftest-wsl"], limit=12, head=2)
row("P2 D5 - live smoke read, snapshot: RUN AS DECLARED; exit 3 names the unrepaired defect and nothing else",
    ["G1-dryrun-D5-live-snapshot"], limit=16, head=2)
row("P2 D6 - live smoke read, frontier: RUN AS DECLARED; exit 3 for the same reason",
    ["G1-dryrun-D6-live-frontier"], limit=12, head=2)
row("P2 D7 - negative criteria against the real diff: all five hold",
    ["G1-dryrun-D7-negative"])
row("P2 D8 - negative criteria falsified against a seeded input: all five fire",
    ["G1-dryrun-D8-negative-falsify"], limit=22, head=10)

w("**P2b - no path outside the frozen allowlist appears as a write anywhere in the plan**")
w("```")
if os.path.isfile(os.path.join(G, "G1-plan-path-scan.json")):
    w("$ " + argv_line(cap("G1-plan-path-scan")))
    for l in stream_text(cap("G1-plan-path-scan"), "stdout").splitlines():
        w(l)
    w("(exit %d)" % cap("G1-plan-path-scan")["exit_code"])
else:
    w("PENDING FIRST RENDER: G1-plan-path-scan")
w("```")
w()

w("**P3 - exit checklist completed, every item evidence-backed**")
w("```")
w("docs/evidence/gatebraid/P2-S6/g1/gate1-exit-checklist.md")
w("```")
w()

row("P4 - allowlist_hash reproduced", ["G1-allowlist-hash"])
row("P5 - plan_hash reproduced, from the rendered record itself", ["G1-plan-hash"])
row("P6 - the sanctioned write_domains post-condition on the Slice issue",
    ["G1-writedomains-check"])

w("## Required disclosures")
w()
for d in DISCLOSURES:
    w("- " + d)
w()
w("## gatebraid-metadata")
w()
w("```yaml")
w((METADATA % {"started": STARTED, "ended": ENDED,
               "plan_hash": PLAN_HASH, "allowlist_hash": ALLOWLIST_HASH}).rstrip())
w("```")

open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("WROTE %s" % OUT)
