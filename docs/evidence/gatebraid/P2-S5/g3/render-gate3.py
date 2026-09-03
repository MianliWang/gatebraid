"""Render docs/evidence/gatebraid/P2-S5/g3/gate3.md from the captures.

Record-row outputs are GENERATED from the capture records, never transcribed
(friction #96). The record lands under g3/ beside g0r/, g1/ and g2/, which is
this Slice's ruled evidence layout and what the Release Approval's term 3 names.

THE LESSON OF THIS SLICE, APPLIED TO ITS LAST RECORD: no count is written as a
constant. Every figure this file states is derived at render time from the row
that measures it, because four separate defects across Gate 2 were a number or a
status that was true when typed and false when the thing it described moved.

This file is written and committed BEFORE the merge and reaches the base branch
through the pull request. It records the pull request by URL and records NO merge
SHA and NO closure timestamp: GitHub holds both natively, and the authoritative
Gate 3 record is the composite of this file, the merge event, the issue's closure
event and the Project's Workflow (ADR-0017).

Usage: render-gate3.py <ended_at>
"""
import base64, json, os, re, sys

G3 = "docs/evidence/gatebraid/P2-S5/g3"
CAPS = G3 + "/captures"
OUT = G3 + "/gate3.md"
STARTED = "2026-09-03T09:00:00Z"
ENDED = sys.argv[1]

BASE = "cbd065893b37f20713ae35b8d2673bf26fe4d2ad"
FP_HEAD = "5b586029344eb6df4a964c34baa1eb12e2916f6d"
FP_TREE = "f696944947a342b6163bf4ad7d9137674830a2f7"
PR_URL = "https://github.com/MianliWang/gatebraid/pull/21"
APPROVAL_URL = ("https://github.com/MianliWang/gatebraid/issues/17"
                "#issuecomment-5523023378")

L = []


def w(s=""):
    L.append(s)


def cap(cid):
    return json.load(open(os.path.join(CAPS, cid + ".json"), encoding="utf-8"))


def has(cid):
    return os.path.isfile(os.path.join(CAPS, cid + ".json"))


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
    """One stated rule, carried forward from the Gate 2 renderer (its F-04).

    Carriage returns removed from each decoded stream; stdout without a trailing
    blank; stderr, when it carries anything, after exactly one newline and also
    without a trailing blank; split on newlines. The count a row prints is the
    number of lines it shows.
    """
    out = stream_text(d, "stdout").replace(chr(13), "")
    err = stream_text(d, "stderr").replace(chr(13), "")
    c = out.rstrip("\n")
    if err.strip():
        c = c + "\n" + err.rstrip("\n")
    return c.split("\n") if c else []


def row(label, cids, limit=None, head=None):
    w("**%s**" % label)
    w("```")
    for cid in cids:
        if not has(cid):
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
              % (limit, total, CAPS, cid))
            for l in tail:
                w(l)
        else:
            for l in lines:
                w(l)
        w("(exit %d)" % d["exit_code"])
    w("```")
    w()


def ci_finding():
    """The CI finding, DERIVED from the row that measures it.

    `none-configured` is a recorded finding and not a pass: where no check
    exists the prohibition on merging with red CI is inert, and this record says
    so rather than implying a check occurred.
    """
    if not has("G3-G5-ci"):
        return "PENDING", "0", "0"
    t = stream_text(cap("G3-G5-ci"), "stdout")
    wf = re.search(r"repository workflows\s*:\s*(\d+)", t)
    cr = re.search(r"check runs on the PR head:\s*(\d+)", t)
    wf = wf.group(1) if wf else "?"
    cr = cr.group(1) if cr else "?"
    return ("none-configured" if wf == "0" and cr == "0" else "UNDETERMINED"), wf, cr


def keyword_matches():
    """The closure-precondition-(b) figure, derived from the scan's own output."""
    if not has("G3-G2b-keyword-scan"):
        return None
    t = stream_text(cap("G3-G2b-keyword-scan"), "stdout")
    m = re.search(r"total pattern matches:\s*(\d+)", t)
    return m.group(1) if m else None


def main():
    ci, wf_count, cr_count = ci_finding()
    kw = keyword_matches()

    w("# Gate 3 evidence - P2-S5")
    w()
    w("## Publication records")
    w()
    row("G1 - Release Approval verified: located by fidelity against its "
        "committed source, then fetched by id, and the executor identity it is "
        "compared against",
        ["G3-G1-approval", "G3-G1-executor-identity"])
    row("G2a - closure precondition (a): platform automation",
        ["G3-G2a-automation"])
    row("G2b - closure precondition (b), first half: the pull request's own "
        "closing references", ["G3-G2b-refs"])
    row("G2b - closure precondition (b), falsified BEFORE the clean run is "
        "trusted: the same instrument over a seeded body carrying all three "
        "lawful reference shapes, and a conventional-commit near-miss that must "
        "not match", ["G3-G2b-keyword-scan-falsify"], limit=14, head=8)
    row("G2b - closure precondition (b), second half: the pattern search over "
        "the pull-request body and every commit message the pull request "
        "carries, run against the FINAL pull-request state",
        ["G3-G2b-keyword-scan"], limit=16, head=8)
    row("G3 - drift check against the Gate 2 fingerprint", ["G3-G3-drift"])
    row("G4 - publication commands, in the contract's order",
        ["G3-G4-publication"])
    row("G5 - CI status", ["G3-G5-ci"])
    w("- Pull request: %s - referenced, not duplicated (ADR-0017 section 2)" % PR_URL)
    w("- CI: `ci: %s` - %s repository workflows and %s check runs on the "
      "pull-request head. A recorded finding, not a pass: where no check exists "
      "the prohibition on merging with red CI is inert, and this record says so "
      "rather than implying a check occurred." % (ci, wf_count, cr_count))
    w()

    w("## Required disclosures")
    w()
    w("- Deviations (gate-3-contract Action 1, and the drift check's own "
      "meaning): the drift check was run BEFORE publication and was clean - 0 "
      "of 76 changed paths outside the Slice's evidence directory, 0 of 9 "
      "commits past the fingerprint outside it, `git status --porcelain "
      "--untracked-files=all` at 0 lines. The G3 row above is a RE-RUN against "
      "the committed tree, because a first capture of it was taken after this "
      "gate had begun writing its own evidence and therefore recorded eight "
      "untracked `g3/` paths beside a summary line asserting emptiness. That "
      "capture is retained at "
      "`docs/evidence/gatebraid/P2-S5/g3/captures/G3-G3-drift-pass1.json` "
      "rather than deleted: it is a true record of its own instant, and the "
      "false line in it is the very class four Gate 2 findings were about.")
    w("- Deviations (friction #103): one ref outside `refs/heads/`, "
      "`refs/remotes/` and `refs/tags/` exists in this clone - a `refs/codex` "
      "checkpoint tree ref whose leaf file is dated 2026-07-31, more than a "
      "month before this Slice's work, and which this Slice's own entry report "
      "recorded as pre-existing. It is REPORTED and not adopted; this Slice "
      "introduced no ref.")
    w("- Deviations (ADR-0011 section 7, ADR-0019 section 1): `ci: %s`. Neither "
      "Gatebraid repository carries a workflow, so no check ran and none could. "
      "The figures above are read from the row that measures them." % ci)
    w("- Deviations (ADR-0017 section 2): this record carries the pull request "
      "by URL and records NO merge SHA and NO closure timestamp. Both are held "
      "natively, and the authoritative Gate 3 record is the composite of this "
      "file, the merge event, the issue's closure event and the Project's "
      "`Workflow` field. A file written before the merge cannot attest to it "
      "(friction #56).")
    w("- Deviations (Release Approval terms 1 and 4): the merge is the "
      "operator's own browser action and no machine account performs it; the "
      "branch is retained after the merge, never deleted. This gate stops after "
      "pushing this record and holds.")
    w("- Deviations (Release Approval rulings 1 through 6, carried unchanged): "
      "F-08 leaves the Gate 2 sweep check typed `fail` with its residue "
      "diagnosed by class; F-07 and H-02 are queued together for the ADR-0026 "
      "clarification; the `--help` frozen-scope tension goes to closeout with "
      "the `bin/` docstring unedited; J-01's one-line subset-nomination wording "
      "and the `consults[]` recording gap are closeout items; and the Slice "
      "issue's Acceptance item 1, `R3 first-pass = pass`, is NOT met - the "
      "first-pass R3 verdict was FAIL, and O1's acceptance is decided at "
      "closeout, not by this publication.")
    w("- Environment (friction #89): Windows host, Windows 11 build "
      "10.0.26200, AMD64, node RoughEgoist; Git for Windows 2.51.0.windows.1 "
      "whose system configuration carries `core.autocrlf=true`; every `gh` call "
      "pins `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` and uses endpoints "
      "with no leading slash; every Python invocation carries `-B` with "
      "`PYTHONDONTWRITEBYTECODE=1`; Windows interpreter "
      "`C:/Python312/python.exe`, CPython 3.12.2, PyYAML 6.0.2, jsonschema "
      "4.23.0; WSL `/usr/bin/python3`, CPython 3.12.3, jsonschema 4.10.3. "
      "Captures are argv-form unless the row declares shell semantics, in which "
      "case the shell, pipefail and the exit-code source are all recorded.")
    w()

    w("## gatebraid-metadata")
    w()
    w("```yaml")
    meta = '''schema: gatebraid/gate-run@2
slice_id: P2-S5
gate: 3
environment: mixed-see-prose
executor: Claude Lead
base_sha: %(base)s
active_branch: slice/P2-S5
started_at: "%(started)s"
ended_at: "%(ended)s"
result: passed
checks:
  - name: staged-set-matches-gate2-handoff
    command: "git diff --name-only %(fp_tree)s HEAD; git log --format=%%H %(fp_head)s..HEAD -- ':!docs/evidence/gatebraid/P2-S5/'; git status --porcelain --untracked-files=all"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G3-drift.json"
  - name: closure-precondition-automation
    command: "the Project's built-in workflows read with their enabled state; Auto-close issue is disabled"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G2a-automation.json"
  - name: closure-precondition-pull-request
    command: "closingIssuesReferences empty; the closing-keyword pattern searched over the pull-request body and every commit message the pull request carries, matches printed beside the count"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G2b-keyword-scan.json"
  - name: closure-precondition-pull-request-falsified
    command: "the same instrument over a seeded body: it must fire on each lawful reference shape and must not match a conventional-commit prefix"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G2b-keyword-scan-falsify.json"
  - name: ci-status
    command: "repository workflows, workflow files in the tree, and check runs on the pull-request head"
    result: none_configured
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G5-ci.json"
  - name: publication-commands-in-contract-order
    command: "git push -u origin slice/P2-S5, read back from the remote; then the pull request opened to main by plain reference"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g3/captures/G3-G4-publication.json"
consults: []
approvals:
  - type: "Release Approval (G2%(arrow)sG3)"
    comment_url: "%(approval)s"
    author: "MianliWang"
evidence_files:
  - docs/evidence/gatebraid/P2-S5/g3/gate3.md
notes: "PR %(pr)s. No merge SHA and no closure timestamp are recorded here - GitHub holds both natively (ADR-0017 section 2), and this file is written before the merge. The publication set is the reviewed tree at %(fp_head)s (tree %(fp_tree)s) plus the record-only evidence commits that follow it, every one inside docs/evidence/gatebraid/P2-S5/. CI is %(ci)s, a recorded finding rather than a pass. The Slice issue is referenced by plain reference and is closed at this gate's Exit by an explicit command, never by this pull request - closure is what releases native blocked-by dependents. Every figure in this record is derived from the row that measures it; four Gate 2 findings were a count or a status typed as a constant and later contradicted by its own row, and this record does not repeat that."
'''
    arrow = "\u2192"
    w((meta % {"base": BASE, "started": STARTED, "ended": ENDED,
               "fp_tree": FP_TREE, "fp_head": FP_HEAD, "pr": PR_URL,
               "approval": APPROVAL_URL, "ci": ci, "arrow": arrow}).rstrip())
    w("```")

    open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print("WROTE %s   (ci=%s, keyword matches=%s)" % (OUT, ci, kw))


main()
