"""Render docs/evidence/gatebraid/P2-S5/g2/gate2.md from the captures.

Record-row outputs are GENERATED from the capture records, never transcribed
(friction #96). The record lands under g2/ and not beside the retained gate0.md:
ruling 2 of the Gate 0 opening comment and the Plan Approval both give this
Slice a per-gate layout, and writing at the top level would ADD a file to the
retained set and move its path-list digest.

The Review record is left for the reviewer to append. Verdicts are written by
the reviewer, last; the implementer never pre-fills them, and this renderer has
no code that could.

Usage: render-gate2.py <ended_at>
"""
import base64, json, os, sys

G = "docs/evidence/gatebraid/P2-S5/g2"
CAPS = os.path.join(G, "captures")
OUT = os.path.join(G, "gate2.md")
STARTED = "2026-09-02T02:52:00Z"
ENDED = sys.argv[1]

BASE = "cbd065893b37f20713ae35b8d2673bf26fe4d2ad"
FP_HEAD = "629e287faab01a84935a93a2dc265d369a6a5c33"
FP_TREE = "cda51687a326d41c2b98d6b2ae49a48526bd366e"

L = []


def w(s=""):
    L.append(s)


def cap(cid):
    return json.load(open(os.path.join(CAPS, cid + ".json"), encoding="utf-8"))


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
        p = os.path.join(CAPS, cid + ".json")
        if not os.path.isfile(p):
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
              % (limit, total, CAPS, cid))
            for l in tail:
                w(l)
        else:
            for l in lines:
                w(l)
        w("(exit %d)" % d["exit_code"])
    w("```")
    w()


DISCLOSURES = [
    "Deviations: the handoff fingerprint is measured at the last IMPLEMENTATION commit, "
    "629e287faab01a84935a93a2dc265d369a6a5c33, before this record and the rest of this gate's "
    "evidence are committed. That is what the fingerprint's definition requires and what makes it "
    "Gate 3's comparand. Every commit after it is record-only and confined to "
    "docs/evidence/gatebraid/P2-S5/g2/, which is inside the frozen allowlist.",

    "Deviations: REPAIR 1, and what it did and did not touch. The FIRST run of the declared D9 "
    "command at this gate returned exit 1: negative criterion N3's content limb fired, reporting 62 "
    "files where 43 were expected. The cause was not a changed retained record - both pinned gate0.md "
    "hashes were unchanged throughout and the digest re-derives - but the Gate 1 MECHANISATION of "
    "the limb, whose exclusion set is hard-coded to `g0r` and `g1`, the two per-gate subdirectories "
    "that existed when it was written. The frozen plan states the property as `the file count of "
    "docs/evidence/gatebraid/P2-S5/ with the re-run and THIS GATE'S OWN SUBDIRECTORIES excluded "
    "must be forty-three`; at Gate 2 that is three names, not two. The Gate 1 file was NOT edited - "
    "Gate 1's captures pin it and it rides on byte-identical - and the failing run is retained at "
    "docs/evidence/gatebraid/P2-S5/g2/captures/G2-R-n3-g1-instrument-fired.json. The repair is a g2 "
    "copy differing in exactly one line. It LOOSENS NOTHING: the expected count is still 43, the "
    "expected digest still 83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f, both "
    "pinned gate0.md hashes unchanged, and the exclusion set is an explicit tuple of names rather than a "
    "pattern. It was falsified against the Gate 1 seeds before it was trusted, and all six criteria "
    "fired.",

    "Deviations: whether repair 1 counts toward the Slice's `evidence-only repairs = 0` acceptance "
    "item is stated rather than assumed, because the classification is arguable and the record "
    "should let a reader decide. Its subject is neither the deliverable nor this record's prose - "
    "the two things the M2 measurement chain's evidence-only repairs were - but a CHECK "
    "INSTRUMENT'S DOMAIN CONSTANT. This writer's reading is that it is not an evidence-only repair "
    "under that definition. The reviewer and the operator may read it otherwise; everything needed "
    "to reclassify it is in the Repair record and in the retained failing run.",

    "Deviations: the D9 row is recorded TWICE and the reason is the defect P2-S6's own repair 1 "
    "found. The instrument's changed-path set is the tracked diff UNION the untracked set. Run "
    "unpinned it reads the working tree, so it moves after every later commit and does not "
    "reproduce. V9 is therefore the run PINNED to base..fingerprint, which is the row that "
    "reproduces; V9b is the live unpinned run, retained beside it as a true record of its own "
    "instant. The untracked half is working-tree-relative even when pinned and can only SHRINK as "
    "this Slice's own files are committed; every path it can contain is inside the allowlist by "
    "construction, so the six verdicts are stable under that shrinkage even though the listing is "
    "not.",

    "Deviations: THE NOMINATED DETERMINISTIC SUBSET of this record. IN the subset, and required to "
    "reproduce byte-identically: E1's three rows, E3, E4b, V0, V0F, V1, V2, V3, V4, V6, V7, V8, V9 "
    "(pinned), V10, and the repair's novelty row. OUTSIDE the "
    "subset, by ADR-0028 decision 2's exclusion limb, and named here rather than left to be "
    "discovered: V5, the live composition, whose report is re-derived from the control plane at "
    "each run and whose `workflow` value for this Slice changes as this very gate writes fields; "
    "V9b, the unpinned criteria run, for the reason above; V12 and its two falsification runs, whose domain is the captures directory AS IT STOOD when they ran and which grows as this gate writes the captures that follow them; E2 and E4, whose recorded values include "
    "a lease timestamp and a branch head that later commits move; and V11's second half, which "
    "validates this record and therefore reads bytes that this render produced.",

    "Deviations: two of this gate's declared commands name paths that a read-only gate could not "
    "have created, and both now run against artefacts that exist. D5 writes its capture into "
    "docs/evidence/gatebraid/P2-S5/g2/captures/, the directory the frozen plan names. D11's second "
    "half validates docs/evidence/gatebraid/P2-S5/g2/gate2.md, so it runs AFTER this record is "
    "authored and its outcome enters the record as the record's own last row - which is why that "
    "row is outside the deterministic subset.",

    "Deviations: the closed-set sweep's g2 copy carries domain facts under ruling 2 of the Plan "
    "Approval, and ONE RESIDUE IS LEFT DELIBERATELY UNEXPLAINED. The hard-rule limb is satisfied "
    "and shown: exactly two repository identities anywhere in the domain, MianliWang/gatebraid and "
    "MianliWang/gatebraid-scratch, both PERMITTED, nothing outside the set, and no mention-class "
    "issue targeted by any query. The remaining token is an issue-shaped citation printed by the "
    "FROZEN corpus runner inside a case label, which is a friction reference written without the "
    "word `friction` that the FRICTION regex requires. No existing explicit set fits it honestly: "
    "the mention class means `issues of the permitted repository this Slice's evidence names`, "
    "which it is not, and putting it there would assert something false and weaken a live check. "
    "Admitting it would need a new classification branch, which is a rule change the approval "
    "forbids. It stays residue and is disclosed here. THE SWEEP OVER THIS RECORD ITSELF returns "
    "UNEXPLAINED RESIDUE 0 at exit 0: every candidate token in these bytes is explained by an "
    "explicit rule, and the four residues an earlier render carried were removed AT SOURCE rather "
    "than by widening anything - a bare relative path in a row's own echo label written out in "
    "full, a host temporary path moved inside this gate's evidence directory, and three near-miss "
    "tokens this record had been quoting into itself, which is the IN-03 class and was the record "
    "sweep catching a defect in its own file.",

    "Deviations: the sweep copy was falsified in TWO runs before any weight was put on it, which is "
    "the approval's stated condition. The two retained seeds still fire the repository, node and "
    "issue limbs, so the added facts blunted no limb that already worked. A new seed carries, for "
    "every fact the copy adds, a token shaped like it but OUTSIDE it by one appended or "
    "substituted character, and all fifteen of those tokens remained residue. The seed is retained at docs/evidence/gatebraid/P2-S5/g2/falsification/SEED-near-miss-new-classes.json and the tokens are NOT echoed here: a checker does not quote what it forbids into a record (ADR-0028 decision 3, the IN-03 class), and this disclosure quoting three of them is a defect the record sweep caught in this very file. A fact that admitted its own near-miss would be a blindfold rather than a domain fact.",

    "Deviations: the composer's argument-splitting rule was settled by MEASUREMENT during "
    "authoring, and it is recorded because it is the exact failure this scope was first frozen "
    "around. The producer command must be split by POSIX rules on every platform. With posix=False "
    "- the tempting choice on Windows - shlex leaves the quotes attached to the token, the stub "
    "arrives at the child as a program whose first character is a quote, the child emits ZERO "
    "BYTES, and the decode guard appears to pass while testing nothing. That is friction #15's "
    "shape and precisely what P1-S3's second dry-run caught before this scope was frozen. It was "
    "caught here the same way, by running rather than reading. The default producer command is "
    "written with forward slashes because POSIX rules treat a backslash as an escape.",

    "Deviations: THIS RECORD'S FIRST RENDER WAS REJECTED BY ITS OWN MACHINE VALIDATION, and the "
    "correction is recorded rather than quietly folded in. The metadata's `approvals[0].type` was "
    "written with an ASCII arrow, `Plan Approval (G1->G2)`, and the frozen schema's enum requires "
    "the label carrying U+2192 RIGHTWARDS ARROW. D11's validation half returned `verdict: rejected` "
    "with one structural finding at `approvals/0/type`, and that failing run is retained at "
    "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D11-wsl-toolchain-pass1.json. The renderer now "
    "RESOLVES the label from the schema's own enum by prefix rather than writing it at all, which "
    "is the standing never-re-type rule applied to a record field instead of to a control-plane "
    "write. This is recorded as an AUTHORING correction and not as a repair attempt: it was caught "
    "by this writer's own pre-submission validation, before the record was committed and before any "
    "reviewer saw it, which is the discipline ADR-0028 mandates rather than a round trip it "
    "measures. A reviewer who reads it otherwise has the failing capture and this disclosure to "
    "reclassify from.",

    "Deviations: the selftest's S06c assertion was corrected during authoring, and the correction "
    "was to the ASSERTION and never to the composer. Its first writing matched the phrase `not "
    "valid UTF-8` in lower case against a refusal the composer writes in capitals, so a correct "
    "guard was reported failing. The row now matches case-insensitively and on three substantive "
    "tokens - the byte, its position, and the refusal phrase. The composer's message was not "
    "changed to suit a check.",

    "Deviations: two files under docs/evidence/gatebraid/P2-S5/g1/dryrun-out/ and two under "
    "docs/evidence/gatebraid/P2-S5/g2/dryrun-out/ carry CRLF in the working copy and are stored LF "
    "under the tree's `* text=auto eol=lf` attribute. They are unreferenced probe stderr, named by "
    "no capture and covered by no pin. The four pinned measurements are byte-identical either way, "
    "before and after the evidence commit.",

    "Deviations: this gate took the Writer Lease and held it throughout; no second writer of any "
    "kind ran. Nothing was pushed, no pull request was opened, no merge was performed, no "
    "dependency was installed, no hook or check was disabled, and no git reset, clean or checkout "
    "was run against baseline state. The one checkout performed was `git checkout slice/P2-S5` "
    "onto the branch this gate created from Y, which is the Entry step the contract names.",

    "Deviations: scratch paths outside every repository were relied on and are named here, as the "
    "Prohibited clause requires. Every commit message was passed through a file under the session "
    "scratchpad outside this repository, never as a shell argument. The approval-fidelity row "
    "writes and removes one file, and it writes it INSIDE this gate's own evidence directory "
    "rather than outside the repository: its first form used a host temporary path whose leading "
    "segment the closed-set sweep has no class for, and the record sweep caught that in this very "
    "file. The superseded capture is retained at "
    "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E1-approval-fidelity-pass1.json.",

    "Deviations: the record's FINAL bytes are validated by a run cited by output_ref and not "
    "inlined as a row, because a document that quoted its own verification would change the bytes "
    "that verification read. V11's second half validated this record at its own instant on the WSL "
    "half and returned accepted; the Windows-half run against the final bytes is "
    "docs/evidence/gatebraid/P2-S5/g2/captures/G2-record-validation.json, and the sweep over those "
    "same final bytes is G2-record-sweep.json in the same directory. Both are captured, both are "
    "named in checks, and neither is inlined.",

    "Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; Git for "
    "Windows 2.51.0.windows.1 whose SYSTEM configuration carries core.autocrlf=true, verified in "
    "this window, and the same binary resolves for a Windows-Python subprocess; every gh call pins "
    "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every "
    "Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for "
    "the WSL half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, "
    "jsonschema 4.23.0; WSL /usr/bin/python3 with CPython 3.12.3, jsonschema 4.10.3, whose captures "
    "stamp platform.os `wsl`. The `python` on PATH is the MSYS 3.14.3 build and carries neither, "
    "which is why no declared command names it and why delta D-3 exists. Captures are argv-form "
    "unless the row declares shell semantics, in which case the shell, pipefail and the exit-code "
    "source are all recorded. environment=mixed-see-prose.",
]

METADATA = """schema: gatebraid/gate-run@2
slice_id: P2-S5
gate: 2
environment: mixed-see-prose
executor: Claude Lead
base_sha: cbd065893b37f20713ae35b8d2673bf26fe4d2ad
active_branch: slice/P2-S5
started_at: "%(started)s"
ended_at: "%(ended)s"
result: needs_approval
checks:
  - name: plan-approval-verified
    command: "gh api repos/MianliWang/gatebraid/issues/comments/5503291709 by id; author observed MianliWang, compared against gh api user = mianliwang492-source; body byte-identical to the committed source"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E1-approval-fidelity.json"
  - name: door-consumed
    command: "Next Approval to the bare option 450ee130; needs-human removed"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E4-entry-readback.json"
  - name: writer-lease-taken
    command: "Writer Lease field write and read-back"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E2-lease.json"
  - name: baseline-reread
    command: "X read from docs/evidence/gatebraid/P2-S5/g0r/gate0.md; Y = git rev-parse main; git diff --name-only X..Y"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E3-baseline.json"
  - name: active-branch-created-from-Y
    command: "git rev-parse --abbrev-ref HEAD; git rev-parse HEAD"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E4-branch.json"
  - name: evidence-rides-on-byte-identical
    command: "retained-set digest, three pinned records, and the commit shown additions-only, measured AFTER the commit"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E4b-evidence-commit.json"
  - name: D0-frozen-scope-pin-holds
    command: "docs/evidence/gatebraid/P2-S5/g1/scope-pin.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D0-scope-pin.json"
  - name: D0F-frozen-scope-pin-falsified
    command: "the same instrument with --commit naming the pinned commit's parent"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D0F-scope-pin-falsify.json"
  - name: D1-corpus-digest-unmoved
    command: "fixtures/runner-selftest.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D1-corpus-digest.json"
  - name: D2-historical-ready-failure-classes-killed
    command: "fixtures/run-corpus.py; BP-01, BP-02, BP-03, IN-02, IN-03, IN-04 and IN-05 each killed on a named locus. IN-01 is absent from the corpus by its own known_limitation and is carried by D3 instead"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D2-corpus.json"
  - name: D3-ready-selftest-windows
    command: "bin/gatebraid-ready-selftest.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D3-selftest-windows.json"
  - name: D4-ready-selftest-wsl
    command: "wsl.exe -e bash -lc \\"cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-ready-selftest.py\\""
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D4-selftest-wsl.json"
  - name: D5-live-end-to-end
    command: "bin/gatebraid-ready.py against the real control plane; four sources ok and complete, a verdict for the Slice issue"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D5-live-ready.json"
  - name: D6-producer-reported-no-document
    command: "bin/gatebraid-ready.py --snapshot-command (producer on an absent transcript); expect exit 10"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D6-producer-failure.json"
  - name: D7-decode-guard
    command: "bin/gatebraid-ready.py --snapshot-command (cp936 stub); expect exit 11 and empty stdout"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D7-decode-guard.json"
  - name: D8-consumer-refusal-passed-through
    command: "bin/gatebraid-ready.py --snapshot-command (empty-object stub); expect the consumer's own exit 1"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D8-consumer-refusal.json"
  - name: D9-negative-criteria-hold
    command: "g2/negative-criteria.py --base cbd06589..629e287f (pinned so the diff half reproduces)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D9-negative-pinned.json"
  - name: D10-negative-criteria-falsified
    command: "g2/negative-criteria.py against the Gate 1 seeds; all six must fire"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D10-negative-falsify.json"
  - name: D11-evidence-toolchain-on-wsl
    command: "bin/gatebraid-capture.py and bin/gatebraid-validate.py, both run on the WSL half"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D11-wsl-toolchain.json"
  - name: closed-set-repository-limb-closed
    command: "g2/checks-g2-closed-set-sweep.py over the captures domain; exactly two repository identities, both permitted, no mention-class issue targeted by a query"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep.json"
  - name: closed-set-sweep-falsified-two-ways
    command: "the two retained seeds, and a new seed carrying a near-miss for every fact the copy adds"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep-falsify-near-miss.json"
  - name: closed-set-sweep-explains-every-candidate
    command: "the same run; one residue remains, an issue-shaped friction citation inside a frozen corpus case label, disclosed and not admitted by a rule change"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep.json"
  - name: gate2-record-machine-validated
    command: "bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S5/g2/gate2.md --report-id cov-P2-S5-g2-gate2.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-record-validation.json"
  - name: review-five-items
    command: "R1 through R5, by an independent read-only reviewer in a separate session"
    result: not_run
    output_ref: "#review-record"
handoff_fingerprint:
  active_branch_head: "%(fp_head)s"
  tree_sha: "%(fp_tree)s"
  changed_paths:
%(paths)s
consults: []
repair_attempts:
  - number: 1
    hypothesis: "N3's content limb fired on a retained record that did not change; the Gate 1 mechanisation hard-codes the two per-gate subdirectories that existed when it was written, and the frozen plan says `this gate's own subdirectories`, which at Gate 2 is three"
    result: green
approvals:
  - type: "%(approval_type)s"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5503291709"
    author: "MianliWang"
plan_hash: "b2cd75f6a49bb056fd16bc3d2f4cfd5cf98ae8515b5761908add2ed5405cc424"
allowlist_hash: "4110b3021bdfc2fcda1f5f90528db01eb87b554177e2176ccfba46ccd6ca3750"
evidence_files:
  - docs/evidence/gatebraid/P2-S5/g2/gate2.md
notes: "The fourth gatebraid-ready attempt on the M2 slice-C frozen scope, built on the M3 stack. The deliverable is the ready pair alone; it composes the landed producer and consumer and modifies neither. The four ratified deltas are implemented as the approval states them, and D-4 - the producer's status is interpreted against its own declared space rather than tested against zero - is the one that keeps a degraded-but-emitted document from being discarded. Twenty selftest conditions each emit their own summary row; S09 carries IN-01, the class the frozen corpus does not hold, and S10 parses the producer's docstring so the D-4 partition cannot drift from its source unnoticed. One repair was taken and it changed a check instrument's domain constant, not the deliverable and not this record's prose. One check is typed fail and is disclosed in full: the sweep's explanation limb leaves a single residue that no existing explicit set fits honestly. The review is NOT this session's: R1 through R5 belong to an independent reviewer dispatched after adjudication, and Gate = G2 passed is not set here."
"""


def approval_type():
    """The approval label, READ FROM THE FROZEN SCHEMA'S OWN ENUM.

    It carries U+2192 RIGHTWARDS ARROW, not a dash and not an ASCII arrow. The
    first render of this record typed `->` and the record's own machine
    validation rejected it on the enum - which is why the value is now resolved
    from the schema by prefix rather than written here at all. The standing rule
    is that these marks are never re-typed; this is that rule applied to a
    record field instead of to a control-plane write.
    """
    import json as _json
    schema = _json.load(open("schema/gate-run-v2.schema.json", encoding="utf-8"))
    enum = schema["properties"]["approvals"]["items"]["properties"]["type"]["enum"]
    hits = [e for e in enum if e.startswith("Plan Approval")]
    if len(hits) != 1:
        raise SystemExit("STRUCTURE: %d Plan Approval members in the enum, want 1"
                         % len(hits))
    return hits[0]


def main():
    changed = [l for l in os.popen(
        "git diff --name-only %s..%s" % (BASE, FP_HEAD)).read().splitlines() if l]
    changed.sort()
    paths = "\n".join('    - "%s"' % p for p in changed)

    w("# Gate 2 evidence - P2-S5")
    w()
    w("## Entry records")
    w()
    row("E1 - Plan Approval verified: fetched BY ID, author observed, and the "
        "executor identity it is compared against",
        ["G2-E1-approval", "G2-E1-executor-identity"])
    row("E1b - the door's fidelity check against the committed source",
        ["G2-E1-approval-fidelity"])
    row("E1c - the door CONSUMED: Next Approval to the bare option, needs-human removed",
        ["G2-E1-consume-next-approval", "G2-E1-remove-needs-human"])
    row("E2 - Writer Lease taken, and Workflow moved to the implementing option",
        ["G2-E2-lease", "G2-E2-workflow"])
    row("E3 - baseline re-read under the lease: X from the re-run record file, Y measured",
        ["G2-E3-baseline"])
    w("- baseline: `unchanged`")
    w()
    row("E4 - Active Branch created from Y; Base SHA set to Y; every field read back",
        ["G2-E4-branch", "G2-E4-base-sha", "G2-E4-entry-readback"], limit=26, head=8)
    row("E4b - the evidence that rides on, measured AFTER its commit",
        ["G2-E4b-evidence-commit"])

    w("## Verification outputs")
    w()
    row("V0 D0 - the frozen scope still re-derives at the pinned commit",
        ["G2-D0-scope-pin"])
    row("V0F D0F - the same instrument at the pinned commit's parent: the pin fires",
        ["G2-D0F-scope-pin-falsify"], limit=14, head=4)
    row("V1 D1 - the frozen corpus digest is unmoved by this Slice",
        ["G2-D1-corpus-digest"], limit=16, head=2)
    row("V2 D2 - the historical ready-failure classes the frozen corpus holds, each killed on a named locus",
        ["G2-D2-corpus"], limit=26, head=12)
    row("V3 D3 - the ready selftest, Windows half: twenty seeded conditions, each emitting its own row",
        ["G2-D3-selftest-windows"], limit=32, head=24)
    row("V4 D4 - the same selftest, WSL half",
        ["G2-D4-selftest-wsl"], limit=14, head=4)
    row("V5 D5 - the live end-to-end composition against the real control plane",
        ["G2-D5-live-ready"], limit=20, head=4)
    row("V6 D6 - a producer status meaning NO DOCUMENT is exit 10",
        ["G2-D6-producer-failure"])
    row("V7 D7 - producer bytes that are not valid UTF-8 are exit 11, and stdout stays empty",
        ["G2-D7-decode-guard"])
    row("V8 D8 - a decodable but malformed document returns the consumer's OWN refusal code",
        ["G2-D8-consumer-refusal"])
    row("V9 D9 - the six negative criteria hold, PINNED to base..fingerprint so the row reproduces",
        ["G2-D9-negative-pinned"], limit=22, head=6)
    row("V9b - the live unpinned run, retained as a true record of its own instant and OUTSIDE the deterministic subset",
        ["G2-D9-negative"], limit=16, head=2)
    row("V10 D10 - the six negative criteria falsified: all six fire on their substantive limbs",
        ["G2-D10-negative-falsify"], limit=24, head=6)
    row("V11 D11 - the evidence toolchain on the WSL half, both tools",
        ["G2-D11-wsl-toolchain"], limit=20, head=4)
    row("V12 - the closed-set sweep over this gate's captures: repository limb CLOSED, one residue disclosed",
        ["G2-closed-set-sweep"], limit=22, head=16)
    row("V12a - falsification 1: the two retained seeds still fire the repository, node and issue limbs",
        ["G2-closed-set-sweep-falsify-retained"])
    row("V12b - falsification 2: a near-miss for every fact the copy adds; all fifteen remain residue",
        ["G2-closed-set-sweep-falsify-near-miss"], limit=26, head=8)

    w("**V13 - handoff fingerprint: the tree and the changed-path set at the "
      "implementation-complete commit**")
    w("```")
    w("$ git rev-parse %s^{tree}" % FP_HEAD)
    w(FP_TREE)
    w("$ git diff --name-only %s..%s | sort | wc -l" % (BASE, FP_HEAD))
    w(str(len(changed)))
    w("$ git diff --name-only %s..%s | sort | grep -c '^docs/evidence/gatebraid/P2-S5/'"
      % (BASE, FP_HEAD))
    w(str(sum(1 for p in changed if p.startswith("docs/evidence/gatebraid/P2-S5/"))))
    w("$ git diff --name-only %s..%s | sort | grep '^bin/'" % (BASE, FP_HEAD))
    for p in changed:
        if p.startswith("bin/"):
            w(p)
    w("```")
    w()

    w("## Review record")
    w()
    w("No review has run. R1 through R5 are the independent reviewer's to write, "
      "last, in a session that did not build this tree; this record carries no "
      "verdict written by its implementer.")
    w()

    w("## Repair record")
    w()
    w("### Repair 1")
    w()
    w("- Hypothesis (new): N3's content limb fired on a retained record that did "
      "not change; the Gate 1 mechanisation hard-codes the two per-gate "
      "subdirectories that existed when it was written, and the frozen plan says "
      "`this gate's own subdirectories`, which at Gate 2 is three.")
    w()
    row("Novelty measured - the tree moved, so the attempt is a repair and not a "
        "consumed one (ADR-0027 section 1)", ["G2-R1-novelty"])
    row("The failing run, retained", ["G2-R-n3-g1-instrument-fired"], limit=14, head=4)
    w("- Result: `green`")
    w("- Consult: `none` - the sequence stopped at repair 1 because the check "
      "returned green; no consult was reached and none was run.")
    w()

    w("## Required disclosures")
    w()
    for d in DISCLOSURES:
        w("- " + d)
    w("- Reviewer write disclosure: `not applicable - no review has run`")
    w()
    w("## gatebraid-metadata")
    w()
    w("```yaml")
    w((METADATA % {"started": STARTED, "ended": ENDED, "fp_head": FP_HEAD,
                   "fp_tree": FP_TREE, "paths": paths,
                   "approval_type": approval_type()}).rstrip())
    w("```")

    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print("WROTE %s" % OUT)


main()
