"""Render docs/evidence/gatebraid/P2-S6/gate2.md from the captures.

Record-row outputs are GENERATED from the capture records, never transcribed
(friction #96). The Review record section is left EMPTY on purpose: review
verdicts are written by the reviewer, last, and the implementer never pre-fills
them (gate-2-contract; templates/gate2-evidence.md).

Usage: render-gate2.py <ended_at>
"""
import base64, json, os, sys

G = "docs/evidence/gatebraid/P2-S6/g2/captures"
OUT = "docs/evidence/gatebraid/P2-S6/gate2.md"
STARTED = "2026-08-30T02:58:49Z"
ENDED = sys.argv[1]

BASE = "3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8"
FP_HEAD = "5386ce382bac5b4bc1c76a38bcbe86717adf9c1c"
FP_TREE = "3f88cc11fd11292d7225cb1c914dc860b8956646"

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
        if not lines:
            w("(no output)")
        w("(exit %d)" % d["exit_code"])
    w("```")
    w()


DISCLOSURES = [
    "Deviations: THE REVIEW RECORD SECTION OF THIS FILE IS DELIBERATELY EMPTY. The five review items are "
    "not this session's to answer: it built this tree, and R3's independence is exactly what a self-review "
    "destroys. No verdict is pre-filled, the `review-five-items` check is typed `not_run` rather than "
    "guessed, and `Gate` was NOT set to `G2 passed`. The reviewer appends its block, writes the verdicts, "
    "and the record's `result` is re-affirmed then.",

    "Deviations: `result: needs_approval` records the disposition this gate run actually reached - the build "
    "is complete, every declared command is green, and what stands between here and Gate 3 is human: a "
    "review and then a Release Approval. It is NOT a claim that the review passed. gate-run@2's enumeration "
    "carries no `needs_review` member, and the nearest true member is used rather than a member that would "
    "assert more than was measured.",

    "Deviations: the two behavioural criteria that could not be shown at Gate 1 are now shown, and the "
    "difference is worth naming precisely. At Gate 1 the declared commands D5 and D6 ran as declared and "
    "exited 3, reproducing the defect. At this gate the same two commands exit 0: all four sources `ok` and "
    "complete, sixteen items, and a frontier report carrying a verdict for P2-S5. The repair is measured by "
    "the same commands that measured its absence.",

    "Deviations: the item-list envelope carries NO pagination key of any kind, so a short read is detectable "
    "only by arithmetic. `connection_truncated` was used for it - already a member of the frozen "
    "bounded-reason enumeration and exactly this case. NO `schema/` byte was written and none was needed; "
    "the Non-goals hold.",

    "Deviations: the live surface spells issue state in lower case and the frozen schema's enumeration is "
    "upper case. The map is explicit and one-directional - `open` and `closed` only - and any other value "
    "passes through unchanged so `closed()` turns it into `UNKNOWN`. Upper-casing whatever arrived would "
    "coerce an unrecognised value toward a member, which is the one direction this tool must never move in; "
    "it is written as a named map rather than a case transform for that reason.",

    "Deviations: `slice_metadata_present` is derived from the presence of a non-empty Project `Slice` field "
    "on the row. That is the control plane's own declaration that a row is a Slice, and it matches the "
    "measured data exactly - eleven of the fifteen frozen elements carry `slice` and `workflow`, and the "
    "four that carry neither are the Stage and Phase container rows, which by design carry no Workflow. The "
    "reading is stated here so it can be disputed rather than applied silently.",

    "Deviations: B-3's frozen seed is described in the Acceptance as C-3's six-key element, and a six-key "
    "element is a CONTAINER row - it carries no Slice field, so it is excluded and never reaches a verdict "
    "at all. The behavioural property B-3 asserts is about a row that DOES reach a verdict, so LB-3 seeds "
    "the frozen envelope with the `workflow` key removed from the P2-S5 row and asserts the end-to-end "
    "result: `workflow` UNKNOWN, verdict `undecidable`, no KeyError. The container case is asserted "
    "separately at LS-01b. The substitution is named rather than left to be noticed.",

    "Deviations: the selftest reaches the live half by importing the tool in-process and replacing only the "
    "process-execution boundary (`_run`) with the frozen O1-B1 bodies. Endpoint construction, body "
    "normalisation, classification, pagination, assembly and verdicts are the tool's own and unmodified. "
    "This is what pays down the F-04 debt P2-S4 recorded: the live path was committed and exercised by no "
    "declared command. `network reads performed : 0` still holds.",

    "Deviations: `--page-cap` no longer governs the three issue-backed sources, because a per-issue fan-out "
    "is bounded by construction rather than being an open-ended connection; the transport DECLARES its read "
    "count and the loop honours it. The cap still governs any transport that declares nothing, which is "
    "every replay seed - which is why all pre-existing conditions travel exactly the path they did before "
    "and stay green. Had the cap been left applying, a fifteen-issue fan-out under the default cap of ten "
    "would have reported a complete read as bounded.",

    "Deviations: P2-S5 reads `blocked` in the live smoke read, not `startable`, because `#19` - this Slice - "
    "is open and blocks it. That is the setup batch's operational unblock edge working exactly as intended "
    "and is not a defect. The Acceptance asks that `items` include P2-S5 and that the frontier consume the "
    "snapshot with exit 0; both hold, and the verdict's reason is carried verbatim in the frontier report.",

    "Deviations: the handoff fingerprint is measured at the last IMPLEMENTATION commit, before this record "
    "and the rest of this Slice's evidence are committed, which is what the fingerprint's definition "
    "requires and what makes it Gate 3's comparand. Every commit after it is record-only and confined to "
    "docs/evidence/gatebraid/P2-S6/, which is inside the frozen allowlist.",

    "Deviations: this Slice's Gate 0 and Gate 1 evidence was uncommitted working material until this gate. "
    "It is committed here under the lease, per the recorded procedure those gates' records state. The "
    "retained P2-S5 evidence is NOT committed and NOT touched - it is outside the allowlist and negative "
    "criterion N3 fires on it, as its falsification run shows.",

    "Deviations: no repair sequence ran. Every declared command was green on its first run at this gate, so "
    "`repair_attempts` is empty and `repair_limit` is unspent. No Codex consult was needed or made.",

    "Deviations: THE NOMINATED DETERMINISTIC SUBSET of this record, stated explicitly because ADR-0028 decision 2 admits exactly two lawful treatments for a mutable reference - pin it, or exclude it and SAY SO. IN the subset, and reproducing byte-identically: E1, E2, E3, E4's first command, E4b, V1 through V6, V7 (pinned at repair 1), V8, V9, and the novelty row of repair 1. OUTSIDE the subset, by the exclusion limb, TWO rows. First, V7b, the retained unpinned run: its instrument reads the WORKING TREE, so it recorded 2 changed paths at its instant and returns more after every later commit - it is kept as a true record of that instant and this record makes NO claim that it reproduces. Second, E4's second command, `git rev-parse HEAD`, and the committed capture G2-fp-head.json that carries the same command. Its recorded value 5386ce382bac5b4bc1c76a38bcbe86717adf9c1c was the branch head at the implementation-complete commit and is true of that instant; it now returns the record-only commit that followed. It has NO truthful pinned form - rewriting it as `git rev-parse 5386ce38...` would echo its own argument and establish nothing - so exclusion is the treatment, exactly as P2-S4's merged record reasoned. What the row carries is PROVENANCE, how this writer arrived at that commit, not specification; everything the fingerprint must SPECIFY is carried by rows that do reproduce: E4b names the commit as a SHA, V9 derives its tree and its changed-path set from pinned arguments.",

    "Deviations: REPAIR 1, F-02 - what was pinned, and the one line that changed. Row V7 recorded the negative-criteria instrument run with an unpinned base, so its changed-path set was read against the WORKING TREE and moved when this Slice's 92 record-only files were committed: 673 bytes and 2 changed paths recorded, 6,622 bytes and 94 live. The row is now the same instrument - byte-identical, sha256 72a4fc5bd8b14c9873f0c75e04f1413019f78c604e79c8bc89be57ef04fe97a9 across every run at both gates, NOT edited - invoked with --base <base>..<fingerprint-commit>. The pinned stdout is 715 bytes against the unpinned 673, and the difference is EXACTLY 42 bytes on one line: the two dots and the forty hex characters of the pinned end-point, echoed by the command as its own argument. Every other line is identical, including all five verdicts and both changed paths, and two consecutive pinned runs are byte-identical to each other. The unpinned run is RETAINED beside it as V7b rather than deleted: it is a true record of its own instant, and removing it would hide the defect this repair fixes.",

    "Deviations: REPAIR 1, F-03 - the Repair record's form. It carried two sentences of prose in none of ADR-0026's content classes. It is now a `### Repair 1` block of the template's shape, carrying this attempt. The fact those sentences asserted - that no repair had been attempted - was true when written and is superseded by this attempt rather than deleted as wrong.",

    "Deviations: REPAIR 1, the ADR-0027 novelty measurement and the one boundary it has. The tree at the previous failed state is 4f2a6130bd2dd93f63380ffa220dd09c43ee153f, measured by a command PINNED to commit 44906edc4d49cc090673a2220d3b66246b187bca so the row reproduces. This repair's own tree cannot appear inside the file the repair commits - a record cannot contain the hash of the commit that contains it - so it is measured after the commit and carried in _handoff/batch-p2s6/G2-REPAIR1-REPORT-M3-P2S6.md. The trees necessarily differ, because this file's own bytes changed; an unchanged tree would not be a repair, and the report is where that comparison is shown rather than asserted here.",

    "Deviations: REPAIR 1 changed NOT ONE `bin/` BYTE, and no `schema/` or `fixtures/` byte. The repair scope ruled by the operator is the record alone. The negative-criteria instrument was RE-RUN, never edited; its hash is unchanged and is cited above. No Project field was written, no label touched, nothing pushed.",

    "Deviations: F-04 is RECORDED, NOT REPAIRED, by operator ruling: it is follow-up-Slice material and no code changes in this Slice. The finding: a dependency answer that is a JSON OBJECT on a source whose expected kind is a list, returned with exit 0, is read as healthy and can reach `startable`, because `classify`'s kind guard rejects only a non-dict payload while `LIVE_EXPECTED_KIND` expects a list, and `build_items` then treats the source as read. The Acceptance's actual criterion B-2 - a bulk issue LIST offered as a dependency answer - is correctly fail-closed and is what LB-2 tests. Two statements in this Slice are overstated by it and travel to that Slice with the fix: the `_normalise` comment saying a wrong-kind body `fails the source closed`, and the frozen plan's `rejected as the wrong surface rather than parsed`. Both are true of the list case and false of the dict-on-list-source case.",

    "Deviations: F-05 is RECORDED, NOT REPAIRED, by the same ruling. LB-3's `undecidable` leg is inert in the frozen harness because every Slice row is already undecidable before the mutation, so the condition does not isolate the property it names. Its `workflow == UNKNOWN` leg does discriminate and does pass. No in-Slice strengthening was made; strengthening a test after its gate's review would ship un-reviewed behaviour.",

    "Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; shell Git Bash MINGW64 "
    "with Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh "
    "call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every "
    "Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL "
    "half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; "
    "WSL /usr/bin/python3 with CPython 3.12.3. The selftest writes its seeds to a temporary directory "
    "OUTSIDE every repository (tempfile.mkdtemp), which gate-2-contract permits explicitly and which this "
    "row names. environment=mixed-see-prose: the tool runs on the Windows host and the WSL half is evidence.",
]

METADATA = """schema: gatebraid/gate-run@2
slice_id: P2-S6
gate: 2
environment: mixed-see-prose
executor: Claude Lead
base_sha: %(base)s
active_branch: slice/P2-S6
started_at: "%(started)s"
ended_at: "%(ended)s"
result: needs_approval
checks:
  - name: plan-approval-verified
    command: "gh api repos/MianliWang/gatebraid/issues/comments/5466316139 (author observed, compared against gh api user)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-E1-approval.json"
  - name: writer-lease-taken
    command: "Writer Lease field write and read-back"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-E2-lease.json"
  - name: baseline-reread
    command: "git rev-parse refs/remotes/origin/main; git diff --name-only X..Y"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-E3-baseline-Y.json"
  - name: active-branch-created-from-Y
    command: "git rev-parse --abbrev-ref HEAD"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-E4-branch.json"
  - name: D1-corpus-digest-unmoved
    command: "fixtures/runner-selftest.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-D1-corpus-digest.json"
  - name: D2-frozen-corpus-passes-unchanged
    command: "fixtures/run-corpus.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-D2-corpus.json"
  - name: D3-snapshot-selftest-windows
    command: "bin/gatebraid-snapshot-selftest.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-D3-selftest-windows.json"
  - name: D4-snapshot-selftest-wsl
    command: "wsl.exe -e bash -lc \\"cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-snapshot-selftest.py\\""
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-D4-selftest-wsl.json"
  - name: D5-live-smoke-snapshot
    command: "gatebraid-capture.py -- gatebraid-snapshot.py --out g2-snapshot.json --generated-at (measured)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-live-smoke-snapshot.json"
  - name: D6-live-smoke-frontier
    command: "gatebraid-capture.py -- gatebraid-frontier.py g2-snapshot.json --out g2-frontier-report.json"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-live-smoke-frontier.json"
  - name: D7-negative-criteria-hold
    command: "g1/negative-criteria.py --base 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8..5386ce382bac5b4bc1c76a38bcbe86717adf9c1c (pinned at repair 1; instrument unmodified)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-D7-negative-pinned.json"
  - name: D8-negative-criteria-falsified
    command: "g1/negative-criteria.py --changed-from SEED --code-surface-dir g1/falsification (all five must fire)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-D8-negative-falsify.json"
  - name: allowlist-respected
    command: "git diff --name-only %(base)s..%(fp_head)s"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-fp-diff.json"
  - name: closed-set-sweep-falsified
    command: "g2/checks-g2-closed-set-sweep.py (seeded domain; must fire on the repository, node and issue limbs)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-closed-set-sweep-falsify.json"
  - name: closed-set-sweep-over-captures
    command: "g2/checks-g2-closed-set-sweep.py docs/evidence/gatebraid/P2-S6/g2/captures"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-closed-set-sweep.json"
  - name: gate2-record-machine-validated
    command: "bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S6/gate2.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/g2/captures/G2-record-validation.json"
  - name: review-five-items
    command: "R1-R5, by an independent read-only reviewer; NOT run by the implementing session"
    result: not_run
    output_ref: "#review-record"
handoff_fingerprint:
  active_branch_head: "%(fp_head)s"
  tree_sha: "%(fp_tree)s"
  changed_paths:
    - bin/gatebraid-snapshot-selftest.py
    - bin/gatebraid-snapshot.py
consults: []
repair_attempts:
  - number: 1
    hypothesis: "the record lacks ADR-0028 decision 2's treatment for head-mutable rows and carries an unpinned diff base, so two rows inside R3's deterministic subset do not reproduce and the record says nothing about it"
    result: green
approvals:
  - type: "Plan Approval (G1\u2192G2)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/19#issuecomment-5466316139"
    author: "MianliWang"
plan_hash: "4435c71eaf08bf0605815e5960c8093c4698babf99ae8a7030d05ebe445671d0"
allowlist_hash: "8938efcce4b8b863b14f7a503c808d7c2c67d2975aad180fd153fd45cc6da291"
evidence_files:
  - docs/evidence/gatebraid/P2-S6/gate2.md
notes: "Implementation of the frozen plan's T1, T2 and T3. The plan and allowlist are UNCHANGED - no correct-course, no re-freeze - so both hashes carry their Gate 1 values. The two defects are repaired in the two layers the plan named, and the classifier, the assembly and the whole replay transport are untouched: every pre-existing selftest condition stays green, which is the regression evidence the plan nominated. The Plan Approval was targeted BY COMMENT ID, never by matching words or hashes, because Gate 1's own handoff comment carries both hashes and the phrase `Plan Approval` and an id-anchored fetch cannot read the gate's own exit as consent. Review verdicts are absent by design and belong to an independent reviewer."
"""

w("# Gate 2 evidence - P2-S6")
w()
w("## Entry records")
w()
row("E1 - Plan Approval verified: the author observed, and the executor identity it is compared against",
    ["G2-E1-approval", "G2-E1-executor-identity"])
row("E2 - Writer Lease taken, read back", ["G2-E2-lease"])
row("E3 - baseline re-read: Y measured, and the changed-path set X..Y",
    ["G2-E3-baseline-Y", "G2-E3-baseline-delta"])
w("- baseline: `unchanged`")
w()
row("E4 - Active Branch created from Y; the Base SHA field set to Y (read back in E2). "
    "The second command names HEAD and is OUTSIDE THE NOMINATED DETERMINISTIC SUBSET: "
    "its recorded value is what the branch head was at the implementation-complete "
    "commit, true at its time and not reproducible later by construction - see the "
    "deterministic-subset disclosure",
    ["G2-E4-branch", "G2-fp-head"])
row("E4b - the same commit named as a SHA rather than reached through HEAD, so the "
    "identity the row asserts is reproducible on its own",
    ["G2-R1-failed-state-head"])

w("## Verification outputs")
w()
row("V1 D1 - the frozen corpus digest is unmoved by this Slice",
    ["G2-D1-corpus-digest"], limit=18, head=2)
row("V2 D2 - the whole frozen corpus passes unchanged; the four live-shapes mutations stay killed",
    ["G2-D2-corpus"], limit=16, head=6)
row("V3 D3 - snapshot selftest, Windows half: the live shapes and B-1..B-4",
    ["G2-D3-selftest-windows"], limit=34, head=26)
row("V4 D4 - snapshot selftest, WSL half", ["G2-D4-selftest-wsl"], limit=10, head=2)
row("V5 D5 - live smoke read: the snapshot, healthy on all four sources",
    ["G2-live-smoke-snapshot"], limit=16, head=2)
row("V6 D6 - live smoke read: the frontier consumes it, exit 0",
    ["G2-live-smoke-frontier"], limit=12, head=2)
row("V7 D7 - the five negative criteria hold, PINNED to base..fingerprint so the row "
    "reproduces (repair 1, F-02; the instrument is unmodified, sha256 72a4fc5b...)",
    ["G2-D7-negative-pinned"])
row("V7b D7 - the original unpinned run, retained: same instrument, same five verdicts, "
    "a working-tree comparand that has since moved",
    ["G2-D7-negative"])
row("V8 D8 - the same five, falsified against a seeded input: all five fire",
    ["G2-D8-negative-falsify"], limit=22, head=10)
row("V9 - handoff fingerprint: the tree and the changed-path set at the implementation-complete commit",
    ["G2-fp-tree", "G2-fp-diff"])

w("## Review record")
w()
w("### Review 1")
w()
w("| Item | Verdict | Evidence |")
w("|---|---|---|")
w("| R1 allowlist confinement | | |")
w("| R2 test-plan coverage | | |")
w("| R3 evidence is rows that reproduce | | |")
w("| R4 negative criterion | | |")
w("| R5 no prohibited action | | |")
w()
w("- Reviewer write disclosure: ")
w("- Rules given to the reviewer: ")
w()

w("## Repair record")
w()
w("### Repair 1")
w()
w("- Hypothesis (new): the record lacks ADR-0028 decision 2's treatment for "
  "head-mutable rows and carries an unpinned diff base, so two rows inside R3's "
  "deterministic subset do not reproduce and the record says nothing about it.")
w()
row("Novelty measured - the tree at the previous failed state, pinned to that commit",
    ["G2-R1-tree-before", "G2-R1-failed-state-head"])
w("- Result: `green`")
w("- Consult: `none`")
w()

w("## Required disclosures")
w()
for d in DISCLOSURES:
    w("- " + d)
w()
w("## gatebraid-metadata")
w()
w("```yaml")
w((METADATA % {"base": BASE, "started": STARTED, "ended": ENDED,
               "fp_head": FP_HEAD, "fp_tree": FP_TREE}).rstrip())
w("```")

open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("WROTE %s" % OUT)
