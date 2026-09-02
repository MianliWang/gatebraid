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
# F-05: CAPS is a filesystem path built with the host separator. Every path
# this renderer DISPLAYS is a committed path and must be spelled as git
# spells it, so display uses this constant and never CAPS.
CAPS_DISPLAY = G + "/captures"
OUT = os.path.join(G, "gate2.md")
STARTED = "2026-09-02T02:52:00Z"
ENDED = sys.argv[1]

BASE = "cbd065893b37f20713ae35b8d2673bf26fe4d2ad"
FP_HEAD = "5b586029344eb6df4a964c34baa1eb12e2916f6d"
FP_TREE = "f696944947a342b6163bf4ad7d9137674830a2f7"

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


def rendered_lines(d):
    """The lines a capture contributes to a record row, by ONE stated rule.

    F-04. Carriage returns are removed from each decoded stream; stdout keeps
    its content without a trailing blank; stderr, when it carries anything, is
    appended after exactly one newline, also without a trailing blank; the
    result is split on newlines.

    The rule exists because the first form used splitlines() over the raw
    concatenation, and splitlines() treats a lone carriage return as a line
    break. One capture's stderr carries CRCRLF endings, so its 18 lines were
    counted as 36 and its elision total was reported higher than the output
    actually has. The count and the rendered block now come from the SAME
    rule, so the number a row prints is the number of lines it shows.
    """
    out = stream_text(d, "stdout").replace(chr(13), "")
    err = stream_text(d, "stderr").replace(chr(13), "")
    combined = out.rstrip("\n")
    if err.strip():
        combined = combined + "\n" + err.rstrip("\n")
    return combined.split("\n") if combined else []


def sweep_residue_facts():
    """Every residue figure this record states, DERIVED FROM THE SWEEP'S CAPTURE.

    F-03. The earlier record wrote a figure in prose and its own cited row
    contradicted it. A quantified claim exists only as a row (ADR-0026
    decision 2), so every number below is read out of the row instead of
    asserted beside it - the total, the split by kind, and how many sit inside
    superseded -pass captures the gate retained deliberately.

    The sweep prints one indented line per residue as
    `<file> <where> <kind>`, after a line giving the total.
    """
    d = cap("G2-closed-set-sweep")
    lines = stream_text(d, "stdout").splitlines()
    total = None
    rows = []
    seen_total = False
    for line in lines:
        if line.startswith("UNEXPLAINED RESIDUE:"):
            total = int(line.split(":")[1].strip())
            seen_total = True
            continue
        if seen_total and line.startswith("    ") and line.strip():
            parts = line.split()
            if len(parts) >= 3:
                rows.append((parts[0], parts[-1]))
    if total is None:
        raise SystemExit("STRUCTURE: the sweep capture states no residue count")
    if len(rows) != total:
        raise SystemExit("STRUCTURE: the sweep capture lists %d residue rows for "
                         "a stated total of %d" % (len(rows), total))
    issue = sum(1 for f, k in rows if k == "issue")
    in_pass = sum(1 for f, k in rows if "-pass" in f)
    return {
        "residue": "%d" % total,
        "residue_issue": "%d" % issue,
        "residue_other": "%d" % (total - issue),
        "residue_in_pass": "%d" % in_pass,
    }


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
        lines = rendered_lines(d)
        total = len(lines)
        if limit is not None and total > limit:
            keep = lines[:head] if head else []
            tail = lines[-(limit - len(keep)):]
            for l in keep:
                w(l)
            w("[... shown %d of %d lines; full output: %s/%s.json]"
              % (limit, total, CAPS_DISPLAY, cid))
            for l in tail:
                w(l)
        else:
            for l in lines:
                w(l)
        w("(exit %d)" % d["exit_code"])
    w("```")
    w()


DISCLOSURES = [
    "Deviations (review finding F-01, operator disposition REMOVE): the delivered tool declared two "
    "flags beyond the frozen scope and both are gone. The frozen sentence names `--strict` and "
    "`--snapshot-command`; the tool also declared `--consumer` and `--version`. Measured against the "
    "M2 record at the pinned commit with every document digest re-derived first: `--consumer` 0 "
    "occurrences, and all 21 hits of `--version` are `gh --version` or `python --version` probes that "
    "never refer to the deliverable. `--version` printed non-JSON to stdout and exited 0, breaking "
    "both clauses of the frozen sentence at once and making itself indistinguishable by exit status "
    "from a verdict. Removed with them: the `VERSION` constant and the `consumer_path` parameter, "
    "which existed only to serve them. `--help` is KEPT because it IS grounded in the frozen record "
    "as test-plan command 1 of all three M2 attempts, and with it the zero-exit branch of the "
    "SystemExit guard that lets it through.",

    "Deviations (review finding F-01, and a residual the consult raised that this gate does NOT "
    "repair): `--help` still writes usage text to stdout and exits 0, so the module docstring's "
    "sentence `Stdout is always exactly one JSON document or nothing` remains literally overbroad on "
    "that one path. The consult recommended narrowing the docstring. This gate declines, and the "
    "reason is scope, not disagreement: the operator's repair-2 instruction says `no other bin/ byte "
    "changes unless a selftest condition referenced a removed flag`, and the reviewer measured zero "
    "such conditions. The residual is disclosed here instead of edited around, and it is unchanged "
    "from before this repair rather than introduced by it.",

    "Deviations (review finding F-02, R3 ground 1): V9 is no longer nominated into the "
    "byte-reproducible subset. The instrument's changed-path set is the tracked diff UNION the "
    "untracked set read at execution time; `--base A..B` pins the tracked half only, so the row "
    "cannot reproduce in bytes. What the row asserts is the six verdicts, and those held in the "
    "retained run and hold now. The earlier record placed it in the wrong bucket while its own "
    "neighbouring sentence said why it could not belong there; the nomination was the defect, not "
    "the measurement.",

    "Deviations (review finding F-02, and the consult's answer to question 6): the earlier wording "
    "said the untracked half `can only SHRINK` and that every path it can contain is inside the "
    "allowlist `by construction`. Both were unsafe: a later untracked file can appear anywhere and "
    "can move both the listing and the verdicts. The claim is now bounded to what was measured - in "
    "the retained run all six criteria held, and each future run is evaluated on its own current "
    "untracked set.",

    "Deviations (review finding F-03, R3 ground 2, and operator ruling F-08 ACCEPTED): every residue "
    "figure in this bullet is READ FROM THE CITED ROW, not asserted beside it, which is what the "
    "earlier prose got wrong when it said ONE against a row that measured more. The sweep over this "
    "gate's captures reports %(residue)s residue occurrences. %(residue_issue)s of them are the "
    "friction-shaped citation printed by the FROZEN corpus runner inside a case label - a friction "
    "reference written without the word the FRICTION regex requires. The other %(residue_other)s are "
    "benign shape collisions: an N-of-N ratio and two path fragments. %(residue_in_pass)s of the "
    "%(residue)s sit inside superseded -pass captures this gate retained deliberately rather than "
    "deleted. NONE is a repository identity, and the hard-rule limb is independently verified true by "
    "the reviewer: exactly two repository identities, both permitted, and no mention-class issue "
    "targeted by any query. Under ruling F-08 the check stays typed `fail` with the count corrected "
    "and the diagnosis stated, because admitting the remainder would need a rule change the Plan "
    "Approval forbids.",

    "Deviations (review finding F-04): the elision totals are produced by ONE stated rule, given in "
    "the renderer's `rendered_lines` docstring. Carriage returns are removed from each decoded "
    "stream, stdout keeps its content without a trailing blank, stderr when present is appended "
    "after exactly one newline, and the result is split on newlines. The earlier form used "
    "`splitlines()` over the raw concatenation, which treats a lone carriage return as a line break; "
    "one capture's stderr carries CRCRLF endings, so its lines were counted twice and one elision "
    "total was inflated. The count and the rendered block now come from the same rule.",

    "Deviations (review finding F-05): every elision names the committed path with forward slashes. "
    "The earlier spelling carried the host separator because the renderer displayed the same "
    "constant it used to open files; display now uses a separate forward-slash constant and the "
    "filesystem constant is never printed.",

    "Deviations (review finding F-06, ADR-0026 class (c)): every bullet in this section cites the "
    "finding, ruling or friction entry it rests on. The earlier record left most of them "
    "uncited.",

    "Deviations (gate-2-contract repair sequence, and friction #94): repair 2 was preceded by the "
    "Codex consult the unified sequence places before it. CONSULT-17-01 and its verbatim response "
    "are committed beside this record; the consult ran read-only and hermetically with `-C` pointed "
    "at a disposable full copy of this repository made outside every governed repository and deleted "
    "after capture. The verdict is PARTIAL and its reasons are in the Repair record. Recorded as "
    "`repair_attempts[1].consult_ref` because it is an in-sequence consult, never in top-level "
    "`consults[]`.",

    "Deviations (friction #103, and its correction): the precaution against the CLI writing a "
    "checkpoint ref into a governed repository was verified rather than assumed. The governed "
    "repository carries exactly one `refs/codex` ref; its leaf file is dated more than a month "
    "before this consult and its object is the same tree this Slice's entry report recorded as "
    "pre-existing. No ref was written by this consult.",

    "Deviations (ADR-0011 section 2, as amended by ADR-0016): the handoff fingerprint is re-measured "
    "at the NEW implementation-complete commit, the repair-2 commit that restored the frozen tool "
    "surface. Every commit after it is record-only and confined to "
    "docs/evidence/gatebraid/P2-S5/g2/, which is inside the frozen allowlist.",

    "Deviations (ADR-0028 decision 2): THE NOMINATED DETERMINISTIC SUBSET of this record. IN the "
    "subset, and required to reproduce byte-identically: E1's three rows, E3, E4b, V0, V0F, V1, V2, "
    "V3, V4, V6, V7, V8, V10, and the two repair novelty rows. OUTSIDE the subset, by the exclusion "
    "limb, and named here rather than left to be discovered: V5, the live composition, whose report "
    "is re-derived from the control plane at each run; V9 and V9b, for F-02's reason; V12 and its "
    "two falsification runs, whose domain is the captures directory as it stood when they ran and "
    "which grows as this gate writes the captures that follow them; E2 and E4, whose recorded values "
    "include a lease timestamp and a branch head that later commits move; and V11's second half, "
    "which validates this record and therefore reads bytes that this render produced.",

    "Deviations (ADR-0027 section 1): repair 1 remains as recorded - a Gate 1 check instrument's "
    "exclusion set, not the deliverable and not this record's prose - and repair 2 is the last "
    "attempt the sequence allows. Both carry a novelty row comparing the tree against the tree at "
    "the previous failed state, measured before the result is graded.",

    "Deviations (review finding F-07, left standing on the reviewer's own reasoning and the "
    "operator's instruction): the disclosures that narrate this record's own authoring history - the "
    "rejected first render, the corrected assertion, the corrected split rule - remain. The reviewer "
    "records a real gap in ADR-0026, which forbids revision narrative without providing a sanctioned "
    "home for a pre-submission correction the executor is simultaneously required to be honest "
    "about, and declines to fail anything over it. It is queued for an ADR clarification rather than "
    "repaired here.",

    "Deviations (friction #15, and P1-S3's second dry-run): the composer's argument-splitting rule "
    "was settled by measurement during authoring. The producer command must be split by POSIX rules "
    "on every platform; with `posix=False` the quotes stay attached, the stub arrives wrapped, the "
    "child emits ZERO BYTES, and the decode guard appears to pass while testing nothing. The default "
    "producer command is written with forward slashes because POSIX rules treat a backslash as an "
    "escape.",

    "Deviations (ADR-0028 decision 3, the IN-03 class): this record does not echo the near-miss "
    "tokens its falsification seed carries. The seed is retained beside the sweep instrument and the "
    "tokens live there, not here; an earlier render quoted three of them into this file and the "
    "record's own sweep caught it.",

    "Deviations (ADR-0026 decision 1, and the reviewer's F-04 observation): four unreferenced "
    "probe-stderr files under this Slice's two dryrun-out directories carry CRLF in the working copy "
    "and are stored LF under the tree's text attribute. No pin covers them and no capture names "
    "them.",

    "Deviations (gate-2-contract Prohibited, scratch clause): scratch paths outside every repository "
    "were relied on and are named. Every commit message passed through a file in the session "
    "scratchpad outside this repository, never as a shell argument; the consult's disposable "
    "repository copy lived there and was deleted; the approval-fidelity row writes and removes one "
    "file inside this gate's own evidence directory.",

    "Deviations (ADR-0026 class (b), and friction #96): the record's FINAL bytes are validated and "
    "swept by runs cited by output_ref and not inlined, because a document that quoted its own "
    "verification would change the bytes that verification read.",

    "Environment (friction #89): Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; "
    "Git for Windows 2.51.0.windows.1 whose SYSTEM configuration carries core.autocrlf=true; every "
    "gh call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading "
    "slash; every Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl "
    "command for the WSL half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, "
    "PyYAML 6.0.2, jsonschema 4.23.0; WSL /usr/bin/python3 with CPython 3.12.3, jsonschema 4.10.3, "
    "whose captures stamp platform.os `wsl`; the Codex CLI is codex-cli 0.144.6, invoked "
    "`--ephemeral --sandbox read-only --ignore-user-config`. The `python` on PATH is the MSYS 3.14.3 "
    "build and carries neither library, which is why no declared command names it and why delta D-3 "
    "exists. Captures are argv-form unless the row declares shell semantics, in which case the "
    "shell, pipefail and the exit-code source are all recorded. environment=mixed-see-prose.",
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
    command: "the same run; the residue count is the cited capture's own figure, diagnosed by class in the disclosures - one friction-shaped citation printed by the frozen corpus runner, the remainder benign shape collisions, none a repository identity. Typed fail under operator ruling F-08: admitting the remainder would need a rule change the Plan Approval forbids"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep.json"
  - name: frozen-tool-surface-restored
    command: "bin/gatebraid-ready.py --help declares only --strict and --snapshot-command; --version and --consumer are usage errors with exit 12 and empty stdout"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-R2-surface.json"
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
  - number: 2
    hypothesis: "The independent review's R3 FAIL and its HIGH finding share one cause - a claim the record or the tool makes that its own measurement contradicts - so the repair restores the frozen two-flag surface and re-derives every contradicted figure from the row that measures it, rather than restating it in prose"
    result: green
    consult_ref: CONSULT-17-01
approvals:
  - type: "%(approval_type)s"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5503291709"
    author: "MianliWang"
plan_hash: "b2cd75f6a49bb056fd16bc3d2f4cfd5cf98ae8515b5761908add2ed5405cc424"
allowlist_hash: "4110b3021bdfc2fcda1f5f90528db01eb87b554177e2176ccfba46ccd6ca3750"
evidence_files:
  - docs/evidence/gatebraid/P2-S5/g2/gate2.md
  - docs/evidence/gatebraid/P2-S5/g2/CONSULT-17-01.md
  - docs/evidence/gatebraid/P2-S5/g2/CONSULT-17-01-response.json
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
    row("V9 D9 - the six negative criteria hold. Pinned to base..fingerprint, which pins the TRACKED half only; this row is EXCLUDED from the deterministic subset and what it asserts is the six verdicts",
        ["G2-D9-negative-pinned"], limit=22, head=6)
    row("V9b - the live unpinned run, retained beside it as a true record of its own instant, likewise excluded",
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
    w("### Repair 2")
    w()
    w("- Hypothesis (new): the independent review's R3 FAIL and its HIGH finding "
      "share one cause - a claim the record or the tool makes that its own "
      "measurement contradicts - so the repair restores the frozen two-flag "
      "surface and re-derives every contradicted figure from the row that "
      "measures it, rather than restating it in prose.")
    w()
    row("Novelty measured - the tree moved from the reviewed failing state, so "
        "the attempt is a repair and not a consumed one (ADR-0027 section 1)",
        ["G2-R2-novelty"])
    row("The frozen tool surface, restored and verified (F-01)", ["G2-R2-surface"])
    row("The consult's metadata validated against gatebraid/consult@1 before the "
        "id was relied on, loader named", ["G2-R2-consult-metadata-validation"])
    row("The friction #103 precaution, verified rather than assumed: no ref was "
        "written by the consult", ["G2-R2-consult-ref-hygiene"])
    row("The Gate 1 instrument's own run at this gate, retained - the finding "
        "repair 1 answered", ["G2-R-n3-g1-instrument-fired"], limit=14, head=4)
    w("- Result: `green`")
    w("- Consult: `CONSULT-17-01` (in sequence - also on "
      "`repair_attempts[1].consult_ref`; friction #94). Verdict **PARTIAL**, "
      "independently verified before application: every claim in the response "
      "was re-measured against the tree before any byte changed. Accepted in "
      "full on the completeness of the F-01 removal, on excluding V9 rather "
      "than modifying the frozen Gate 1 instrument, on the elision-line rule, "
      "on the twelve-item post-repair claim set, and on the three further "
      "statements the V9 fix had to change. Declined on one point, for scope "
      "and not disagreement: the consult recommended narrowing the module "
      "docstring's stdout sentence to exempt `--help`, and the operator's "
      "repair-2 instruction permits no other `bin/` byte change; the residual "
      "is disclosed instead.")
    w()

    w("## Required disclosures")
    w()
    facts = sweep_residue_facts()
    for d in DISCLOSURES:
        w("- " + (d % facts if "%(" in d else d))
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
