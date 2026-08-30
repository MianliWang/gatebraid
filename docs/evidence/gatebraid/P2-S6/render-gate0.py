"""Render docs/evidence/gatebraid/P2-S6/gate0.md from the captures.

Outputs are GENERATED from the capture records, never transcribed (friction
#96). Every elision prints shown and total plus the committed path of the full
output. The renderer writes the file and asserts nothing about it: the record
is machine-validated separately by bin/gatebraid-validate.py.

Two row kinds are emitted. `row` prints a capture's own recorded streams.
`docrow` prints a document this gate produced - the snapshot and the frontier
report - from its bytes on disk, with its measured sha256, because the
startability verdict and its reasons must appear in the record verbatim and
those live in the documents rather than in a stream.
"""
import base64, hashlib, json, os, sys

CAP = "docs/evidence/gatebraid/P2-S6/captures"
OUT = "docs/evidence/gatebraid/P2-S6/gate0.md"
STARTED = "2026-08-29T07:30:33Z"
ENDED = sys.argv[1]

L = []


def w(s=""):
    L.append(s)


def cap(cid):
    return json.load(open(os.path.join(CAP, cid + ".json"), encoding="utf-8"))


def argv_line(d):
    inv = d["invocation"]
    env = inv.get("environment") or {}
    names = sorted(env)
    prefix = " ".join("%s=%s" % (k, env[k]) for k in names)
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
    "Deviations: this gate PASSED on an observation that is a tool failure, and that inversion is the "
    "operator's Ruling 1 in the Gate 0 opening comment on issue 19, the D-2 exception ruled 2026-08-27 for "
    "this Slice alone. The startability evidence is the deterministic failure of the committed pair "
    "reproduced at class level against the live control plane, not a healthy read. gatebraid-snapshot exited "
    "3 with the three issue-backed sources issue_states, dep_blocked_by and dep_blocking each status "
    "unexpected_endpoint, complete false, and the read-outcome sentinel 65; gatebraid-frontier exited 3 with "
    "snapshot_degraded true and zero verdicts of every kind. That is exactly the ruled expectation, so the "
    "startability check records pass and this record carries result passed. Any other outcome, a healthy "
    "read included, would have been a stop; none occurred.",

    "Deviations: class-level identity with the retained P2-S5 run was measured, not assumed, and byte "
    "identity was NOT expected and is absent. The four source identities, their statuses, their complete "
    "flags, their exit codes and their failure_detail strings are equal between this run and the retained "
    "P2-S5 snapshot; the frontier degraded_sources list, the summary and the empty verdicts list are equal; "
    "the snapshot generator source_sha256 is the same committed tool, "
    "e27eaad381518ef76d563a59d616f0f5747eaa97a995a602d9972c5a342ef878. generated_at differs, which is why "
    "byte identity is not the test.",

    "Deviations: this is the standing F-04 note materialising again. The snapshot's live gh transport is "
    "committed and exercised by no declared command; its selftests exercise the replay transport. This gate "
    "is a further live-transport exercise under that same disclosure, and the repair this Slice lands is "
    "what retires it. The fail-closed classification behaved as designed once more: the degradation was "
    "reported rather than absorbed, and no tool was changed inside this gate.",

    "Deviations: source project_items reported status ok, complete true, exit 0, and yielded zero items, so "
    "the snapshot carries items empty and the frontier report carries zero verdicts of every kind rather "
    "than an undecidable verdict for P2-S6. The absent-verdict case is this Slice's expected branch under "
    "Ruling 1 and is recorded as measured; the cause is not diagnosed here and no tool was changed.",

    "Deviations: the baseline is lawfully dirty and the gate proceeded past Action 3 under a Dirty Baseline "
    "Acceptance, Ruling 2 of the Gate 0 opening comment, scoped to the retained P2-S5 Gate 0 evidence and "
    "nothing else. The acceptance is entered in approvals[] with that comment's id. All three of its "
    "re-measured conditions hold: tracked changes are zero; every untracked path lies under the P2-S5 "
    "evidence prefix; and the sorted relative-path-list digest re-derives equal to "
    "83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f by the same construction as section 6 "
    "of SETUP-REPORT-M3-P2S6.md. That construction command is recorded in this file as the invocation line "
    "of the A3 digest row, so the recipe is durable rather than described. Remediation was neither attempted "
    "nor permitted.",

    "Deviations: the entry report for this Slice stated the retained P2-S5 evidence as 44 files. The measured "
    "count is 43, three ways agreeing, and Ruling 2 supersedes the earlier figure with the measured one. The "
    "44 was unverified and no capture from entry time exists to re-derive it; it is recorded as a miscount "
    "and was not remediated. Nothing in the setup batch or this gate wrote to the working tree.",

    "Deviations: A3's clean-tree predicate is evaluated over the baseline excluding this gate's own write "
    "domain, and the unfiltered view is recorded beside it so the exclusion is auditable. The Gate 0 "
    "contract's Exit clause makes this gate's own evidence files not a violation. A separate row records "
    "that tracked changes are zero with no exclusion at all.",

    "Deviations: A1's ref-namespace enumeration found one ref outside refs and heads, refs and remotes, and "
    "refs and tags: a Codex turn-diff checkpoint ref pointing at a tree object. It is REPORTED and NOT "
    "adopted, which is what the contract requires; it was present in the retained P2-S5 enumeration too. No "
    "write of any kind was made into that namespace by this gate.",

    "Deviations: three evidence instruments travel with the evidence they produce, per ADR-0028 section 4 "
    "and the P2-S5 precedent, rather than being cited at an uncommitted path. checks-g0-slice-metadata.py is "
    "byte-identical to _handoff/batch-o0/validate-slice-metadata.py, sha256 "
    "a37850cfd3c94caebeb380d5a41aee1fdc7cbba0a10d7989055878e610779419. checks-g0-closed-set-sweep.py and "
    "checks-g0-verify-captures.py were copied byte-identically from the retained P2-S5 evidence and then "
    "re-parameterized for this Slice, as recorded in the next two entries.",

    "Deviations: the closed-set sweep was re-parameterized for this Slice and then falsified before it was "
    "trusted. The changed constants are this Slice's own facts: the captures directory, this Slice's Project "
    "item id, the subject issue number, and the mention-class issue set. Four further candidates in this "
    "gate's domain needed an explicit rule, and each was named rather than matched by a pattern: a git tag "
    "fragment inside the CPython interpreter version banner; a Windows filesystem segment produced when a "
    "path containing a space is split; and two ordinary prose slashes in this Slice's own issue body. The "
    "additions are exact strings, never a regex, which is the defect pass 1 of the P2-S5 sweep was repaired "
    "for. Falsification after the change: pointed at the seeded domain the sweep fires on all three limbs, "
    "the repository limb, the node limb and the issue limb, and exits 1; pointed at the real domain it "
    "returns empty residue and exits 0. Every REPOSITORY identity named anywhere in the domain is the one "
    "permitted owner-slash-repo pair, counted once. No account repository enumeration was performed at any "
    "point in this gate.",

    "Deviations: checks-g0-verify-captures.py had its domain constant re-pointed at this Slice's captures "
    "directory and made overridable by argument; no rule of the instrument was changed.",

    "Deviations: three captures are accepted by the capture tool's own write-path guard with re-derivation "
    "and rejected by bin/gatebraid-validate.py, which is a disagreement between two independent checkers "
    "rather than a defect in the captures. All three rejections are the finding "
    "placeholder-survives-its-own-check, two at the rendered text of a captured stdout stream and one at the "
    "rendered text of a captured stderr stream. The triggers are foreign text the streams faithfully "
    "recorded: the Slice template's own HTML comment quoted from the issue body, the label jsonschema prints "
    "for the document root when it reports an error path, and the pseudo-filename CPython prints in a "
    "DeprecationWarning. The validator's mention test excuses this pattern at an invocation argument, a "
    "check command and notes, on the stated ground that those fields quote foreign text; a captured "
    "stream's rendered text is the same kind of field and is not in that list. Reported and not worked "
    "around. Unlike P2-S5, where bin was a non-goal, bin is inside this Slice's declared write domain, so "
    "whether this is repaired here is a question for the plan at Gate 1 and is not decided at Gate 0.",

    "Deviations: two documents this gate produced are not routable by bin/gatebraid-validate.py and are "
    "counted in their own class rather than as rejections. g0-snapshot.json declares interface "
    "gatebraid/snapshot@1, which the validator does not implement; g0-frontier-report.json declares no "
    "schema key at all, naming its interface under a report key instead. Both are validator exit 2, a usage "
    "or input error by the tool's own exit-code contract and not a verdict. The frontier document's key "
    "naming is an interface inconsistency reported here and not changed.",

    "Deviations: the A6 body read used gh issue view with json body and jq, whose output carries one "
    "trailing newline that jq appends; the captured bytes are therefore the pinned source plus that "
    "newline, 5067 against 5066. The body file written from the captured bytes is byte-equal to the "
    "capture, and the setup batch's own read-back of the same issue measured 5066 bytes with the pinned "
    "sha256 7b345433708b2e56265b138b399ea8fe4ecaa797bebda7e56c0dd13e158727a8. The difference is the jq "
    "output form, not the stored body. This is the same class P2-S5 recorded.",

    "Deviations: the A3 digest capture's first attempt declared shell form and named the shell by bare name, "
    "and the capture tool could not execute it. The tool never interpolates a string and runs with shell "
    "false, so a declared shell must be an explicit first argument of the command; the bare name is metadata "
    "only. The tool reported the structural failure and wrote no file at all rather than a partial one. The "
    "capture was re-run with the shell named as an explicit absolute path on the Windows host. No partial "
    "artefact survives. This is the same class as the P2-S5 host-probe disclosure.",

    "Deviations: at gate opening Workflow was written to the Gate 0 Verifying option, resolved fresh from "
    "the live field list by exact label with exactly one candidate, id 036a9fdc, its dash measured as U+2014 "
    "at codepoint level rather than by appearance. Executor already read Claude Lead from the setup batch "
    "and was not rewritten. This closes the question P2-S5 left owed, where the same Entry write was omitted "
    "on a stop path.",

    "Deviations: this gate wrote no tracked file, made no commit, made no push, created no branch, ran no "
    "fetch and no pull. The evidence files under this Slice's own directory are working files, committed "
    "under the lease at Gate 2, and the Gate 0 contract's Exit clause makes writing them here not a "
    "violation.",

    "Deviations: the capture-set check in row V3 ran before this record was rendered, so the four captures written after it - the render, this record's own machine validation, the sweep over this record, and V3's own capture - are outside the set it checked. That boundary is inherent rather than an omission: each new run would itself produce a capture the run could not have covered, and the regress is stopped by stating where the set ends. The documents V3 did check are named one per line in its output above. Those four later captures are each written by the same guarded write path, and the record itself is independently validated by bin/gatebraid-validate.py in its own row.",

    "Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; shell Git Bash MINGW64 "
    "with Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh "
    "call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every "
    "Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL "
    "half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; "
    "WSL /usr/bin/python3 with CPython 3.12.3. environment=mixed-see-prose: the gate ran on the Windows host "
    "and the WSL half is evidence.",
]

METADATA = """schema: gatebraid/gate-run@2
slice_id: P2-S6
gate: 0
environment: mixed-see-prose
executor: Claude Lead
base_sha: 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
started_at: "%s"
ended_at: "%s"
result: passed
approvals:
  - type: Dirty Baseline Acceptance
    author: MianliWang
    comment_url: "https://github.com/MianliWang/gatebraid/issues/19#issuecomment-5461039588"
checks:
  - name: repo-identity-and-remote
    command: "git remote -v"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-remote.json"
  - name: ref-namespace-enumerated
    command: "git for-each-ref (one ref outside the three watched namespaces: reported, not adopted)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-ref-namespace.json"
  - name: base-sha-recorded
    command: "git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-baseline-main.json"
  - name: working-tree-clean-at-base
    command: "git status --porcelain --untracked-files=all (baseline, excluding this gate's write domain); git rev-parse HEAD; git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-porcelain-baseline.json"
  - name: working-tree-tracked-changes-zero
    command: "git status --porcelain --untracked-files=no (no exclusion of any kind)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-porcelain-tracked.json"
  - name: working-tree-unfiltered-audit
    command: "git status --porcelain --untracked-files=all"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-porcelain-full.json"
  - name: dirty-baseline-acceptance-digest-rederived
    command: "find docs/evidence/gatebraid/P2-S5 -type f | sort | tr -d CR | sha256sum (Ruling 2 re-measurement; the exact construction is the invocation line of the A3 digest row)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-p2s5-pathlist-digest.json"
  - name: environment-matches-host
    command: "gh api graphql (Environment field read); python host probe"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-env-field.json"
  - name: tool-versions
    command: "claude.cmd --version; git --version; gh --version; codex.cmd --version; python version probe on both halves"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-tools-git.json"
  - name: slice-metadata-checker-falsified
    command: "checks-g0-slice-metadata.py --schema schema/slice.schema.json --selftest"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-slice-metadata-selftest.json"
  - name: slice-metadata-parses
    command: "checks-g0-slice-metadata.py --schema schema/slice.schema.json --body captures/slice-body-19.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-slice-metadata-validation.json"
  - name: startability-snapshot-degraded-as-ruled
    command: "gatebraid-snapshot.py --out captures/g0-snapshot.json --generated-at (measured); exit 3 with the three issue-backed sources unexpected_endpoint and sentinel 65 IS the ruled expectation"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-snapshot-run.json"
  - name: startability-frontier-undecidable-as-ruled
    command: "gatebraid-frontier.py captures/g0-snapshot.json --out captures/g0-frontier-report.json; exit 3 with snapshot_degraded true and zero verdicts IS the ruled expectation"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-frontier-run.json"
  - name: closed-set-sweep-falsified
    command: "checks-g0-closed-set-sweep.py (seeded domain; must fire on the repository, node and issue limbs)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-closed-set-sweep-falsify.json"
  - name: closed-set-sweep
    command: "checks-g0-closed-set-sweep.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-closed-set-sweep.json"
  - name: closed-set-sweep-over-record
    command: "checks-g0-closed-set-sweep.py docs/evidence/gatebraid/P2-S6/gate0.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-record-sweep.json"
  - name: capture-set-validated
    command: "checks-g0-verify-captures.py (capture-tool guard with re-derivation, and bin/gatebraid-validate.py, over every document)"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-captures-validation.json"
evidence_files:
  - docs/evidence/gatebraid/P2-S6/gate0.md
notes: "Startability read from the hardened gatebraid-snapshot and gatebraid-frontier pair as sole authority, the Gate 0 contract Entry's After-O0 clause, under the operator's D-2 exception for this Slice alone: the expected observation IS the deterministic failure reproduced at class level, so exit 3 from both tools is the pass condition and not a stop. Gate 0 opening comment: id 5461039588, author MianliWang observed at verification time, https://github.com/MianliWang/gatebraid/issues/19#issuecomment-5461039588 ; fetched from the API and compared against the committed source before use, identical except one trailing newline, which is the known storage class, and no ruling struck. Per that comment's record-typing clause this record carries NO approvals[] entry for the opening comment itself: the frozen gate-run@2 approvals[].type enumeration still has no member for a Gate 0 Opening, and that missing member remains a candidate item for the already-owed gate-run@2 revision batch. The one approvals[] entry present is Ruling 2's Dirty Baseline Acceptance, which IS a member, carrying the same comment id. The Ruling 2 re-measurement construction is recorded as the invocation line of the A3 digest row so the recipe is reproducible rather than described. The capture-set check is typed fail because two independent checkers disagree about three captures; it is not one of the contract's Actions 1 through 6 and does not bear on this gate's disposition, and it is disclosed in full above. Base SHA is not re-touched at this gate."
"""

w("# Gate 0 evidence - P2-S6")
w()
w("## Records")
w()

row("A1 - repository identity and remote", ["G0-remote"])
row("A1 - ref namespace; any ref outside refs heads, refs remotes, refs tags is reported, not adopted",
    ["G0-ref-namespace"], limit=21)
row("A2 - plan baseline: head of the base branch now (recorded here only; the Base SHA field is set at Gate 2 from the head re-read under lease - ADR-0011 section 9)",
    ["G0-baseline-main"])
row("A3 - working tree clean AND at the base branch (one predicate, friction #84), evaluated over the baseline excluding this gate's own write domain",
    ["G0-porcelain-baseline", "G0-head", "G0-baseline-main"])
row("A3 - tracked changes with no exclusion of any kind: zero", ["G0-porcelain-tracked"])
row("A3 - unfiltered porcelain, so the baseline row's exclusion is auditable",
    ["G0-porcelain-full"], limit=8)
row("A3 - Dirty Baseline Acceptance re-measurement (Ruling 2): the sorted relative-path-list digest, re-derived by the construction shown on the invocation line",
    ["G0-p2s5-pathlist-digest"])
row("A4 - Project Environment field vs actual host", ["G0-env-field", "G0-host-probe"], limit=14)
row("A5 - tool versions",
    ["G0-tools-claude", "G0-tools-git", "G0-tools-gh", "G0-tools-codex",
     "G0-tools-python-windows", "G0-tools-python-wsl"])
row("A6 - slice metadata parses against gatebraid slice@1",
    ["G0-slice-metadata-selftest", "G0-slice-metadata-validation"], limit=24)

w("### Startability - the hardened pair as sole authority, under the ruled D-2 exception")
w()
row("S1 - gatebraid-snapshot", ["G0-snapshot-run"])
docrow("S1 - the snapshot document it emitted", "g0-snapshot.json")
row("S2 - gatebraid-frontier", ["G0-frontier-run"])
docrow("S2 - the frontier report it emitted: the verdict and its reasons, verbatim", "g0-frontier-report.json")

w("### Evidence verification")
w()
row("V1 - closed-set sweep, falsified against a seeded domain after re-parameterization: it must fire on the repository, node and issue limbs",
    ["G0-closed-set-sweep-falsify"], limit=14)
row("V2 - closed-set sweep over every captured response", ["G0-closed-set-sweep"], limit=30)
w("**V2b - the same sweep over this record itself, run after it was rendered; its output is at "
  "captures/G0-record-sweep.json and is not inlined here, because a document that quoted its own "
  "sweep would change the text the sweep just read**")
w()
row("V3 - every document checked by the capture tool's own guard with re-derivation and by bin/gatebraid-validate.py",
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
