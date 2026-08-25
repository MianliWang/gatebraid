"""Render docs/evidence/gatebraid/P2-S4/gate3.md.

Record-row outputs are GENERATED from the Gate 3 captures, never transcribed
(friction #96). Every elision carries shown/total and the committed path of the
full output (ADR-0026). This file records NO merge SHA and NO closure timestamp:
GitHub holds both natively and the authoritative Gate 3 record is the composite
(ADR-0017 §1/§2).

Usage: render-gate3.py <ended_at>
"""
import base64
import json
import os
import sys

CAP = "docs/evidence/gatebraid/P2-S4/g3"
OUT = "docs/evidence/gatebraid/P2-S4/gate3.md"
BASE_SHA = "df666070ead7fa21bc72b6c99d2644923b37e787"
TREE_SHA = "f797297005d35d150799af300ecc22daef35dac9"
ABH = "50d08de65158faf23f1ae86aeebcde39e929c359"
PR_URL = "https://github.com/MianliWang/gatebraid/pull/16"
APPROVAL_URL = ("https://github.com/MianliWang/gatebraid/issues/14"
                "#issuecomment-5415966794")
ENDED = sys.argv[1]

L = []


def w(s=""):
    L.append(s)


def cap(cid):
    return json.load(open(os.path.join(CAP, cid + ".json"), encoding="utf-8"))


def has(cid):
    return os.path.exists(os.path.join(CAP, cid + ".json"))


def argv_line(d):
    inv = d["invocation"]
    env = inv.get("environment") or {}
    prefix = " ".join("%s=%s" % (k, env[k]) for k in sorted(env)) \
        if isinstance(env, dict) else ""
    body = " ".join(
        (a if (a and not any(c in a for c in " \t\n\"'")) else
         "'" + a.replace("'", "'\\''") + "'")
        for a in inv.get("argv", []))
    return ("%s %s" % (prefix, body)).strip()


def stream(d, name):
    s = d.get("streams", {}).get(name, {})
    if not s.get("data"):
        return ""
    return base64.b64decode(s["data"]).decode("utf-8", "replace")


def row(label, cids, limit=None, tail=False):
    w("**%s**" % label)
    w("```")
    for cid in cids:
        if not has(cid):
            w("[capture %s absent]" % cid)
            continue
        d = cap(cid)
        w("$ " + argv_line(d))
        out = stream(d, "stdout")
        err = stream(d, "stderr")
        combined = out + (("\n" + err) if err.strip() else "")
        lines = combined.splitlines()
        if limit is not None and len(lines) > limit:
            window = lines[-limit:] if tail else lines[:limit]
            for x in window:
                w(x)
            w("[... shown %d of %d lines (%s); full output: %s/%s.json]"
              % (limit, len(lines), "tail" if tail else "head", CAP, cid))
        else:
            for x in lines:
                w(x)
        w("(exit %d)" % d["exit_code"])
    w("```")
    w()


def started_at():
    stamps = []
    for name in sorted(os.listdir(CAP)):
        if not name.endswith(".json"):
            continue
        try:
            d = json.load(open(os.path.join(CAP, name), encoding="utf-8"))
        except ValueError:
            continue
        if d.get("started_at"):
            stamps.append(d["started_at"])
    return min(stamps) if stamps else ENDED


w("# Gate 3 evidence — P2-S4")
w()
w("## Publication records")
w()

row("G1 — Release Approval verified (author must be `MianliWang`, not this "
    "session — ADR-0020 §4; terms cited by rule number, never restated — "
    "ADR-0018 §3)",
    ["G3-entry-approval", "G3-entry-identity"])

w("- Approval author `MianliWang`, `author_association` `OWNER`; executor "
  "identity `mianliwang492-source`. The approval was not written by the "
  "session it authorises.")
w("- `created_at` equals `updated_at`, so the grant that was posted is the "
  "grant that was read.")
w("- Entry conditions (a), (b), (c) of the Gate 3 contract are met: the "
  "comment is not a `gatebraid/handoff@1` block, it states the publication "
  "terms in its clause 2, and it is authored by the operator's personal "
  "account. **Its clause 2 is cited, not restated** — the terms bind from the "
  "comment, and a copy here would be a second thing to keep true.")
w()

row("G2a — closure precondition (a): platform automation (ADR-0012 §2)",
    ["G3-closure-a-workflows"])

w("- `Auto-close issue` is **disabled**, `updatedAt 2026-07-30T21:45:57Z`. Of "
  "the five enabled built-in workflows none closes an issue: the chain that "
  "would — `Pull request merged` writing `Status` to `Done`, then "
  "`Auto-close issue` closing on that write — is **broken at exactly the "
  "disabled link**.")
w()

row("G2b — closure precondition (b): the pull request (pattern stated, matches "
    "printed — `keyword #n | keyword owner/repo#n | keyword <url>`, keyword ∈ "
    "close(s|d)/fix(es|ed)/resolve(s|d), any case — ADR-0018 §1)",
    ["G3-closure-b-refs"])

row("G2b continued — the pattern search over every commit message the pull "
    "request carries, and over the pull-request body. **The body was checked "
    "BEFORE the pull request was opened**, which is the gate's normal loop for "
    "its own draft rather than a correction after the fact",
    ["G3-closure-b-commits", "G3-closure-b-prbody"], 22, False)

w("- `closingIssuesReferences` `totalCount` **0**, nodes empty.")
w("- Prohibited-pattern matches: **0** in the commit messages, **0** in the "
  "body. Bare keyword tokens are printed beside each zero so the count states "
  "what it searched (friction #87): the branch carries ten — `closed by "
  "measurement`, `fixtures`, `fix(m3):` among them — and **none is "
  "prohibited**. A check that flagged those is one correct work cannot "
  "satisfy (ADR-0018 §2).")
w("- **`(a) pass` alone is not compliance**; both halves are recorded, and "
  "(b) exists because the 2026-07-30 measurement was GitHub's own behaviour, "
  "which (a) cannot see.")
w()

row("G3 — drift check against the Gate 2 fingerprint (ADR-0011 §2 as amended "
    "by ADR-0016 §1). Every revision is PINNED and passed in as an argument: "
    "this Slice's own F-01 lesson applied to its last gate, since `gate3.md`'s "
    "commit moves the branch head immediately after this runs",
    ["G3-drift"], 34, False)

w("- The head this check names is the head at drift-check time, "
  "`e29756c33d93c3432918c53b2e45e51235521c35`, recorded in its own output. "
  "Commits after it are this record and its captures, inside the slice's "
  "evidence directory.")
w()

row("G3-pass1 — the drift check's own falsification, retained (exit 1)",
    ["G3-drift-pass1"], 12, True)

w("- Check **C fired** on the gate's own untracked evidence directory, created "
  "moments earlier to hold this very capture. **A drift check that had only "
  "ever passed would never have been shown able to fire**; pass 2 ran from a "
  "committed tree, where C measures what it is for. The same convention Gate 0 "
  "used for its sweep's first pass.")
w()

row("G4 — publication commands, exactly as approved, in contract order",
    ["G3-pr-open"])

w("- Push, then pull request, per contract Action 2. `slice/P2-S4` and nothing "
  "else was published: no other branch, no tag, **no direct write to `main`**, "
  "and **no force-push at any point**.")
w("- The pull request references the Slice issue by **plain reference only**.")
w()

row("G5 — CI status (`none-configured` is a recorded finding, not a pass — "
    "ADR-0011 §7, ADR-0019 §1)",
    ["G3-ci-status", "G3-ci-none-configured"])

w("- `ci: none-configured`, established by measurement and not by the absence "
  "of a report: the repository has **`total_count` 0 workflows** and the tree "
  "at this head carries **no `.github/` path at all**.")
w("- **Recorded as a finding.** Where no check exists, the prohibition on "
  "merging with red CI is inert; this record says so rather than implying a "
  "check occurred. `gh pr checks` exits 1 with *no checks reported*, which is "
  "the absence of a check and not a failing one.")
w()

w("- Pull request: %s — referenced, not duplicated (ADR-0017 §2)" % PR_URL)
w()

w("## Required disclosures")
w()
w("- Deviations: **BP-01 fired inside this gate's own instrument, and is fixed "
  "by the doctrine this Slice ships.** `closure-precheck.py` echoes matched "
  "context from arbitrary text, so its output carries whatever non-ASCII its "
  "input carries; run against the pull-request body under this host's cp936 "
  "console, `print()` re-encoded it and the capture recorded "
  "`decode_result: replaced` with a `0xa1` lead byte. The verdict was "
  "unaffected — exit 0, 0 prohibited matches — but **a check whose own output "
  "cannot be decoded is not evidence**. Both Gate 3 instruments now write "
  "explicit UTF-8 bytes to a binary sink, which is exactly what this Slice's "
  "P0-2 requires of its producer. The first run is retained at "
  "`g3/G3-closure-b-prbody-pass1.json`. Two defects in that patch were caught "
  "before it ran — a broken string literal, and a local variable that shadowed "
  "the new helper and would have raised at the first commit examined · **one "
  "commit message was rewritten on an unpushed commit.** The first attempt "
  "passed backticks through a shell, which substituted two words away, leaving "
  "*\"a local named  in\"*. The remote did not carry that commit — remote head "
  "was `54eb5afd…` — so the rewrite is a fast-forward and **no force-push was "
  "involved**; the Gate 3 prohibition is untouched. Later commit messages are "
  "passed through a file rather than a shell argument, which is the root fix · "
  "**one ref sits outside the three watched namespaces**, the pre-existing "
  "`refs/codex/turn-diffs/checkpoints/…` tree ref. **Reported, not adopted** "
  "(friction #103). This Slice created exactly one ref, `refs/heads/slice/"
  "P2-S4`, which is inside `refs/heads/` · **`ci: none-configured` is carried "
  "as a finding**, not a pass and not `skipped` · the debt this Slice carries "
  "past its own close is named in `gate2.md` and belongs to the batch lane and "
  "the closure ledger, not to this gate: the `gate-run@2` revision owing three "
  "items, N4's `isinstance` guard, N2's shape coverage, "
  "`bin/gatebraid-frontier.py`'s surviving docstring word, and F-04's "
  "unmeasured live transport.")
w("- Environment: Windows 11 host, Git Bash (MSYS2) shell; git 2.51.0.windows.1 "
  "with `core.autocrlf=true` from the system gitconfig; Windows loader "
  "`C:\\Python312\\python.exe` (CPython 3.12.2, jsonschema 4.23.0); "
  "`PYTHONDONTWRITEBYTECODE=1` and `-B` on every Python invocation; "
  "`GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` call, every "
  "endpoint written without a leading slash (friction #33). The console codec "
  "is cp936 and mangles U+2014 and U+2192, so every mark that decided an "
  "outcome here was compared by **codepoint**, never by rendered text.")
w()
w("## gatebraid-metadata")
w()
w("```yaml")
w("schema: gatebraid/gate-run@2")
w("slice_id: P2-S4")
w("gate: 3")
w("environment: mixed-see-prose")
w("executor: Claude Lead")
w("base_sha: %s" % BASE_SHA)
w("active_branch: slice/P2-S4")
w('started_at: "%s"' % started_at())
w('ended_at: "%s"' % ENDED)
w("result: passed")
w("checks:")

CHECKS = [
    ("release-approval-verified",
     "gh api repos/MianliWang/gatebraid/issues/comments/5415966794 --jq '{author,url,created,updated}'",
     "pass", "#publication-records"),
    ("staged-set-matches-gate2-handoff",
     "drift-check.py %s %s e29756c33d93c3432918c53b2e45e51235521c35" % (TREE_SHA, ABH),
     "pass", "%s/G3-drift.json" % CAP),
    ("closure-precondition-automation", None, "pass",
     "%s/G3-closure-a-workflows.json" % CAP),
    ("closure-precondition-pull-request", None, "pass",
     "%s/G3-closure-b-refs.json" % CAP),
    ("closure-precondition-keyword-commits", None, "pass",
     "%s/G3-closure-b-commits.json" % CAP),
    ("closure-precondition-keyword-body", None, "pass",
     "%s/G3-closure-b-prbody.json" % CAP),
    ("publication-push-and-pull-request", None, "pass",
     "%s/G3-pr-open.json" % CAP),
    ("ci-status", "gh pr checks 16 --repo MianliWang/gatebraid",
     "none_configured", "%s/G3-ci-none-configured.json" % CAP),
]
for name, command, result, ref in CHECKS:
    w("  - name: %s" % name)
    if command:
        w('    command: "%s"' % command.replace('"', '\\"'))
    w("    result: %s" % result)
    w('    output_ref: "%s"' % ref)

w("# The merge and the closure are post-merge facts. They live in the")
w("# composite record (ADR-0017 section 1) and are not pre-attestable in a")
w("# file written before the merge (friction #56).")
w("consults: []")
w("approvals:")
w('  - type: "Release Approval (G2→G3)"')
w('    comment_url: "%s"' % APPROVAL_URL)
w('    author: "MianliWang"')
w('    at: "2026-08-25T19:57:24Z"')
w("evidence_files:")
w("  - docs/evidence/gatebraid/P2-S4/gate3.md")
w('notes: "PR %s. No merge SHA and no closure timestamp are recorded here -- '
  'GitHub holds both natively (ADR-0017 section 2), and the authoritative Gate '
  '3 record is the COMPOSITE of this file, the pull request merge event, the '
  'issue closure event and the Project Workflow. A consumer reconstructing '
  'state reads the native EVENT SEQUENCE, not the last state: an issue can be '
  'reopened and a comment can be edited. ci is none_configured, carried as a '
  'FINDING and not as a pass -- the repository has zero workflows and the tree '
  'carries no .github path, so the prohibition on merging red is inert here '
  'and this record says so rather than implying a check occurred. The merge is '
  'the operator ACT, made in the browser with Create a merge commit, never '
  'squash and never rebase, because the commit structure is part of what was '
  'reviewed. This file is committed and pushed BEFORE that merge and reaches '
  'main through the pull request like every other change. repair_limit 2, both '
  'spent at Gate 2, zero remaining -- no repair is available at this gate and '
  'a failure here routes per the contract own table."' % PR_URL)
w("```")

data = ("\n".join(L).rstrip("\n") + "\n").encode("utf-8")
with open(OUT, "wb") as fh:
    fh.write(data)
import hashlib
sys.stdout.buffer.write(("WROTE %s\n  bytes=%d sha256=%s\n  crlf=%d lone_cr=%d\n" % (
    OUT, len(data), hashlib.sha256(data).hexdigest(),
    data.count(b"\r\n"), data.count(b"\r") - data.count(b"\r\n"))).encode("utf-8"))
