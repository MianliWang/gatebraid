"""Render docs/evidence/gatebraid/P2-S5/gate0.md from the captures.

Outputs are GENERATED from the capture records, never transcribed (friction
#96). Every elision prints shown/total plus the committed path of the full
output. The renderer writes the file and asserts nothing about it: the record
is machine-validated separately by bin/gatebraid-validate.py.

Two row kinds are emitted. `row` prints a capture's own recorded streams.
`docrow` prints a document this gate produced — the snapshot and the frontier
report — from its bytes on disk, with its measured sha256, because the
startability verdict and its reasons must appear in the record verbatim and
those live in the documents rather than in a stream.
"""
import base64, hashlib, json, os, sys

CAP = "docs/evidence/gatebraid/P2-S5/captures"
OUT = "docs/evidence/gatebraid/P2-S5/gate0.md"
STARTED = "2026-08-26T19:39:21Z"
ENDED = sys.argv[1]

L = []


def w(s=""):
    L.append(s)


def cap(cid):
    return json.load(open(os.path.join(CAP, cid + ".json"), encoding="utf-8"))


def argv_line(d):
    inv = d["invocation"]
    env = inv.get("environment") or {}
    names = sorted(env) if isinstance(env, dict) else sorted(env)
    prefix = " ".join("%s=%s" % (k, (env[k] if isinstance(env, dict) else "")) for k in names)
    body = " ".join(
        (a if (a and not any(c in a for c in " \t\n\"'")) else "'" + a.replace("'", "'\\''") + "'")
        for a in inv.get("argv", []))
    return ("%s %s" % (prefix, body)).strip()


def stream_text(d, name):
    s = d.get("streams", {}).get(name, {})
    if not s.get("data"):
        return ""
    return base64.b64decode(s["data"]).decode("utf-8", "replace")


def row(label, cids, limit=None):
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
            for l in lines[:limit]:
                w(l)
            w("[... shown %d of %d lines; full output: %s/%s.json]" % (limit, total, CAP, cid))
        else:
            for l in lines:
                w(l)
        w("(exit %d)" % d["exit_code"])
    w("```")
    w()


def docrow(label, name, limit=None):
    path = os.path.join(CAP, name)
    raw = open(path, "rb").read()
    w("**%s**" % label)
    w("```")
    w("$ cat %s" % path)
    w("(sha256 %s, %d bytes)" % (hashlib.sha256(raw).hexdigest(), len(raw)))
    lines = raw.decode("utf-8", "replace").splitlines()
    total = len(lines)
    if limit is not None and total > limit:
        for l in lines[:limit]:
            w(l)
        w("[... shown %d of %d lines; full document: %s]" % (limit, total, path))
    else:
        for l in lines:
            w(l)
    w("```")
    w()


DISCLOSURES = [
    "Deviations: this gate STOPPED at the startability read. gatebraid-snapshot exited 3 (DEGRADED) with three "
    "of four sources failing closed, and gatebraid-frontier exited 3 with every item undecidable and no verdict "
    "for P2-S5. Both failing runs are retained as evidence. No remediation of any kind was attempted and no "
    "re-run was made: the Gate 0 Opening comment clause 2 types exit 3 as result stopped with no remediation and "
    "no retry-until-green, and a re-run happens only on the operator's word.",

    "Deviations: stop_record.next_approval reads Human Diagnosis, and that value is the coordinator's reading "
    "awaiting the operator's ratification, not an operator ruling. The Gate 0 Opening comment clause 2 types "
    "exit 3 as result stopped, which is the contract's decidable branch, and gate-run@2 enforces that a decidable "
    "stop carry a next_approval and no workflow. No member of that enumeration names a startability stop: the "
    "members are the two gate transitions, Dirty Baseline Acceptance, Scope / Allowlist Change, Environment "
    "Change, Session Persistence, Worktree Exception and Human Diagnosis. Human Diagnosis is the only member "
    "whose plain meaning covers a stop where an instrument functioned, fail-closed, and left a human to decide. "
    "It was written here because the frozen schema admits no decidable stop without it. The Project Next Approval "
    "field was NOT written: no field mutation is authorised on the stop path, the row reaches the operator "
    "through this report instead, and the value stands or falls on the operator's word. Named as a candidate "
    "item for the owed gate-run@2 revision batch beside the approvals[].type gap.",

    "Deviations: this is the disclosed F-04 limit materialising on its first trusted use. The snapshot's live gh "
    "transport is committed and exercised by no declared command; its selftests exercise the replay transport. "
    "The first live use failed on three of four sources with the same recorded failure_detail, the response body "
    "is a list where an object was required, and the read-outcome sentinel 65. The fail-closed classification "
    "behaved as designed: the degradation was reported rather than absorbed.",

    "Deviations: source project_items reported status ok, complete true, exit 0, and yielded zero items, so the "
    "snapshot carries items empty and the frontier report carries zero verdicts of every kind rather than an "
    "undecidable verdict for P2-S5. The stop is therefore an absence of any verdict for this Slice, not an "
    "adverse verdict about it. Recorded as measured; the cause is not diagnosed here and no tool was changed.",

    "Deviations: the slice-metadata checker was copied byte-identically from the P2-S4-era working file at "
    "_handoff/batch-o0/validate-slice-metadata.py, sha256 "
    "a37850cfd3c94caebeb380d5a41aee1fdc7cbba0a10d7989055878e610779419, into this Slice's own evidence directory "
    "as checks-g0-slice-metadata.py, and is invoked there. P2-S4 cited the uncommitted _handoff path. ADR-0028 "
    "section 4 requires evidence instruments to be committed, and this Slice's write domain already contains the "
    "path, so the instrument now travels with the evidence it produces. The change from precedent is the "
    "location only; the bytes are identical.",

    "Deviations: the closed-set sweep was falsified before it was trusted, and the falsification found a defect "
    "in the sweep itself. Pass 1 carried the P2-S4 original's PROSE_PAIR regex, which matches essentially every "
    "token of the owner-slash-repo shape, so a seeded out-of-set REPOSITORY identifier was classified E8 and "
    "never reached the residue: the repository limb could not fire at all, while the node and issue limbs did. "
    "The rule was replaced by an explicit allowlist naming the prose pairs actually present. Pass 2 fires on all "
    "three limbs against the seed and returns empty residue against the real domain. Pass 1 is retained at "
    "captures/G0-closed-set-sweep-pass1.json with its seeded run at "
    "captures/G0-closed-set-sweep-falsify-pass1.json.",

    "Deviations: the sweep's domain in the P2-S4 original is the captures directory only, so a gate's own record "
    "— the document that would be committed — was never swept by it. The instrument here accepts a file as well "
    "as a directory and is run a second time over gate0.md, after rendering, at "
    "captures/G0-record-sweep.json. That second run is the reason this disclosure's own prose says "
    "owner-slash-repo rather than the slashed form: with E8 narrowed to a named allowlist, an ordinary prose "
    "slash now surfaces as residue instead of being swallowed, which is the intended trade and is what the "
    "first run over gate0.md found.",

    "Deviations: two captures are accepted by the capture tool's own write-path guard with re-derivation and "
    "rejected by bin/gatebraid-validate.py, which is a disagreement between two independent checkers rather than "
    "a defect in the captures. Both rejections are the finding placeholder-survives-its-own-check at "
    "/streams/stdout/rendered/text. The triggers are the Slice template's own HTML comment quoted from the issue "
    "body, and the string <root> printed by jsonschema as an error path label. The validator's mention test "
    "excuses this pattern at /invocation/argv/N, /checks/N/command and /notes, on the stated ground that those "
    "fields quote foreign text; a captured stream's rendered text is the same kind of field and is not in that "
    "list. Reported, not worked around: bin/ is a non-goal for writes in this Slice.",

    "Deviations: two documents this gate produced are not routable by bin/gatebraid-validate.py and are counted "
    "in their own class rather than as rejections. g0-snapshot.json declares interface gatebraid/snapshot@1, "
    "which the validator does not implement; g0-frontier-report.json declares no schema key at all, naming its "
    "interface under report instead. Both are validator exit 2, a usage or input error by the tool's own "
    "exit-code contract and not a verdict. The frontier document's key naming is an interface inconsistency "
    "reported here and not changed.",

    "Deviations: the A6 body read used gh issue view --json body --jq .body, whose output carries one trailing "
    "newline that jq appends; the captured bytes are therefore the pinned source plus that newline, 4187 against "
    "4186. The body file written from the captured bytes is byte-equal to the capture, and the entry phase's "
    "--json body read of the same issue measured 4186 bytes with the pinned sha256. The difference is the jq "
    "output form, not the stored body.",

    "Deviations: the A4 host probe's first attempt named the interpreter by its MSYS path and could not be "
    "executed by the capture tool, which runs on the Windows host. The tool recorded the structural failure and "
    "wrote no file at all rather than a partial one. The probe was re-run with the Windows interpreter path, the "
    "form the committed P2-S4 record used. No partial artefact survives.",

    "Deviations: the Gate 0 contract's Entry names two field states, Executor = Claude Lead and Workflow to "
    "Gate 0 — Verifying. Executor already read Claude Lead from the entry batch and was not rewritten. Workflow "
    "was NOT set to Gate 0 — Verifying and still reads Backlog. The Gate 0 Opening comment's clause 5 enumerates "
    "this gate's moves and does not include that write, and it authorises field writes only at Exit, on the pass "
    "path. The omission is recorded rather than repaired: the gate stopped, so writing Gate 0 — Verifying now "
    "would assert a gate in progress that is not, and no field mutation is authorised on the stop path. The "
    "operator's ruling is owed on whether the Entry write should have preceded the actions.",

    "Deviations: no field write, no handoff comment and no Last Checkpoint update was made at this gate. Those "
    "are the contract's Exit steps and clause 5's stop condition for a gate that passes; this gate stopped "
    "before Exit. The Slice item still reads Workflow Backlog, Gate the bare option and Next Approval the bare "
    "option, unchanged from the entry batch, and the only comment on the Slice issue is the operator's own "
    "opening comment. Nothing was committed and nothing was pushed: evidence files are working files, committed "
    "under the lease at Gate 2.",

    "Deviations: A3's predicate is evaluated over the baseline excluding this gate's own write domain. The "
    "unfiltered view is recorded beside it. The Gate 0 contract's Exit clause makes this gate's own evidence "
    "files not a violation.",

    "Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; shell Git Bash MINGW64 "
    "with Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh call "
    "pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every Python "
    "invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL half; Windows "
    "interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL "
    "/usr/bin/python3 with CPython 3.12.3, jsonschema 4.10.3. environment=mixed-see-prose: the gate ran on the "
    "Windows host and the WSL half is evidence.",
]

METADATA = """schema: gatebraid/gate-run@2
slice_id: P2-S5
gate: 0
environment: mixed-see-prose
executor: Claude Lead
base_sha: 7ff1f848661aac20b3921ae47fe140394a5d2587
started_at: "%s"
ended_at: "%s"
result: stopped
stop_record:
  stopped_at: "startability read (Gate 0 Opening comment clause 2; ENTRY-M3-O1 section 6)"
  disposition: decidable
  observed: "gatebraid-snapshot exit 3 DEGRADED, 3 of 4 sources status unexpected_endpoint with read-outcome sentinel 65 and failure_detail 'the response body is a list where an object was required'; project_items ok and complete with 0 items; gatebraid-frontier exit 3, snapshot_degraded true, verdicts [] and summary startable 0 / blocked 0 / undecidable 0 / excluded 0, so no verdict exists for P2-S5"
  expected: "frontier exit 0 with verdict `startable` for the P2-S5 item, per the Gate 0 Opening comment clause 2"
  next_approval: Human Diagnosis
  remediation_attempted: none
checks:
  - name: repo-identity-and-remote
    command: "git remote -v"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-remote.json"
  - name: ref-namespace-enumerated
    command: "git for-each-ref"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-ref-namespace.json"
  - name: base-sha-recorded
    command: "git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-baseline-main.json"
  - name: working-tree-clean-at-base
    command: "git status --porcelain (baseline, excluding this gate's write domain); git rev-parse HEAD; git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-porcelain-baseline.json"
  - name: working-tree-unfiltered-audit
    command: "git status --porcelain --untracked-files=all"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-porcelain-full.json"
  - name: environment-matches-host
    command: "gh api graphql (Environment field read); python host probe"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-env-field.json"
  - name: tool-versions
    command: "claude.cmd --version; git --version; gh --version; codex --version; python version probe on both halves"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-tools-git.json"
  - name: slice-metadata-checker-falsified
    command: "checks-g0-slice-metadata.py --schema schema/slice.schema.json --selftest"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-slice-metadata-selftest.json"
  - name: slice-metadata-parses
    command: "checks-g0-slice-metadata.py --schema schema/slice.schema.json --body captures/slice-body-17.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-slice-metadata-validation.json"
  - name: startability-snapshot
    command: "gatebraid-snapshot.py --out captures/g0-snapshot.json --generated-at (measured)"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-snapshot-run.json"
  - name: startability-frontier
    command: "gatebraid-frontier.py captures/g0-snapshot.json --out captures/g0-frontier-report.json"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-frontier-run.json"
  - name: closed-set-sweep-falsified
    command: "checks-g0-closed-set-sweep.py (seeded domain; must fire on repo, node and issue limbs)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-falsify.json"
  - name: closed-set-sweep
    command: "checks-g0-closed-set-sweep.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep.json"
  - name: closed-set-sweep-over-record
    command: "checks-g0-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/gate0.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-record-sweep.json"
  - name: capture-set-validated
    command: "checks-g0-verify-captures.py (capture-tool guard with re-derivation, and bin/gatebraid-validate.py, over every document)"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation.json"
evidence_files:
  - docs/evidence/gatebraid/P2-S5/gate0.md
notes: "Startability read from the hardened gatebraid-snapshot / gatebraid-frontier pair as sole authority: the Gate 0 contract Entry's After-O0 clause, first exercise. No state packet exists for this or any later Slice. Gate 0 Opening comment: id 5430107363, author MianliWang, https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5430107363 ; verified against the committed source before use, byte-identical except one trailing newline, no clause struck. Per that comment's clause 3 this record carries NO approvals[] entry for it: the frozen gate-run@2 approvals[].type enumeration has no member for an Entry Ratification and Gate 0 Opening, and State Packet Approval would be false here because no packet exists. The missing member is named here as a candidate item for the already-owed gate-run@2 revision batch. A second gap of the same kind is recorded by this stop: stop_record.next_approval has no enum member for a startability stop, its members being Dirty Baseline Acceptance, Scope / Allowlist Change, Environment Change, Session Persistence, Worktree Exception, Human Diagnosis and the two gate transitions, so the optional field is omitted rather than mistyped, and this too is a candidate item for that revision batch. Base SHA is not re-touched at this gate."
"""

w("# Gate 0 evidence — P2-S5")
w()
w("## Records")
w()

row("A1 — repository identity and remote", ["G0-remote"])
row("A1 — ref namespace; any ref outside refs/heads/, refs/remotes/, refs/tags/ is reported, not adopted",
    ["G0-ref-namespace"], limit=19)
row("A2 — plan baseline: head of the base branch now (recorded here only; the Base SHA field is set at Gate 2 from the head re-read under lease — ADR-0011 §9)",
    ["G0-baseline-main"])
row("A3 — working tree clean AND at the base branch (one predicate, friction #84)",
    ["G0-porcelain-baseline", "G0-head", "G0-baseline-main"])
row("A3 — unfiltered porcelain, so the baseline row's exclusion is auditable",
    ["G0-porcelain-full"], limit=8)
row("A4 — Project Environment field vs actual host", ["G0-env-field", "G0-host-probe"], limit=14)
row("A5 — tool versions",
    ["G0-tools-claude", "G0-tools-git", "G0-tools-gh", "G0-tools-codex",
     "G0-tools-python-windows", "G0-tools-python-wsl"])
row("A6 — slice metadata parses against gatebraid/slice@1",
    ["G0-slice-metadata-loader", "G0-slice-metadata-selftest", "G0-slice-metadata-validation"], limit=24)

w("### Startability — the hardened pair as sole authority (After-O0 clause, first exercise)")
w()
row("S1 — gatebraid-snapshot", ["G0-snapshot-run"])
docrow("S1 — the snapshot document it emitted", "g0-snapshot.json")
row("S2 — gatebraid-frontier", ["G0-frontier-run"])
docrow("S2 — the frontier report it emitted: the verdict and its reasons, verbatim", "g0-frontier-report.json")

w("### Evidence verification")
w()
row("V1 — closed-set sweep, falsified against a seeded domain: it must fire on the repository, node and issue limbs",
    ["G0-closed-set-sweep-falsify"], limit=14)
row("V1 — pass 1 of the same falsification, retained: the repository limb did NOT fire",
    ["G0-closed-set-sweep-falsify-pass1"], limit=14)
row("V2 — closed-set sweep over every captured response", ["G0-closed-set-sweep"], limit=30)
w("**V2b — the same sweep over this record itself, run after it was rendered; its output is at "
  "captures/G0-record-sweep.json and is not inlined here, because a document that quoted its own "
  "sweep would change the text the sweep just read**")
w()
row("V3 — every document checked by the capture tool's own guard with re-derivation and by bin/gatebraid-validate.py",
    ["G0-captures-validation"], limit=40)

w("## Required disclosures")
w()
for d in DISCLOSURES:
    w("- " + d)
w()
w("## gatebraid-metadata")
w()
w("```yaml")
w((METADATA % (STARTED, ENDED)).rstrip())
w("```")

open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("WROTE %s" % OUT)
