#!/usr/bin/env python3
"""Gate 3 record renderer — P2-S3.

Emits docs/evidence/gatebraid/P2-S3/gate3.md in the templates/gate3-evidence.md
shape, with every recorded output GENERATED from the pinned capture files rather
than transcribed (ADR-0026; friction #96).

The row writer carries repair 1's lesson forward: a row that shows less than its
capture states `shown/total` and the committed path of the full output, per
stream. It also renders stderr when stderr is where the output actually is —
Review 1's observation F(1) on the Gate 2 record noted a row whose capture
carried stderr the row did not show; the publication push and the CI read are
both such rows, so this renderer shows both streams rather than repeat that gap.

Usage: g3_render_record.py <captures-dir> <out-path> <started_at> <ended_at>
"""
import sys, os, json, base64, hashlib

CAP, OUT, STARTED_AT, ENDED_AT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]

SLICE = "P2-S3"
EV = "docs/evidence/gatebraid/P2-S3"
BASE_SHA = "63c8401f5df6ba446cf002232fcb280673c28e00"

# The Gate 2 handoff fingerprint — this gate's drift comparand (ADR-0011 §2 as
# amended by ADR-0016 §1). Both ends are named by full sha; no row names a state
# the act of recording it will move (ADR-0028 §4).
G2_TREE = "3012c2a70b053721f61f99bb5e2e1c41cdbc7408"
G2_HEAD = "28d5dfcd83b83b7541a3d8f73732fb833a3d119c"

# The amendment this gate publishes, and the record it carries.
AMEND2 = "870a0ca026959014bf5bf0a14eaafefc104e6026"
AMEND2_TREE = "804bdf1c000b3a0326116b0ae33a81ada57ce1a7"
AMEND1 = "78b2cdfa7340c898b156335415649d6a29b1ffae"
GATE2_SHA = "c16a49b688df3b16f87295ee5b0cce890a3ea8ff89bd8ddf58c565f46b08eebd"
GATE2_BYTES = 42529

PR_NUM = 13
PR_URL = "https://github.com/MianliWang/gatebraid/pull/13"
PR_HEAD_AT_OPEN = "870a0ca026959014bf5bf0a14eaafefc104e6026"

APPROVAL = "https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5381788134"
APPROVAL_AT = "2026-08-22T17:54:08Z"
REASSIGN = "https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5384146247"
REASSIGN_ID = "5384146247"
REASSIGN_AT = "2026-08-23T04:10:45Z"

LEASE_OLD = "RoughEgoist:p2s3-gate2-claude-lead:2026-08-22T05:08:51Z"
LEASE_NEW = "RoughEgoist:p2s3-gate3-claude-writer:2026-08-23T04:17:31Z"


def load(cid):
    p = os.path.join(CAP, cid + ".json")
    if not os.path.exists(p):
        print("MISSING CAPTURE: " + cid); sys.exit(3)
    return json.load(open(p, encoding="utf-8"))


def stream(cid, which="stdout"):
    d = load(cid)
    return base64.b64decode(d["streams"][which]["data"]).decode("utf-8") \
        .replace("\r\n", "\n").rstrip("\n")


def rc(cid):
    return load(cid)["exit_code"]


def cmdline(cid):
    d = load(cid)
    inv = d["invocation"]
    env = inv.get("environment") or {}
    prefix = " ".join("%s=%s" % (k, v) for k, v in sorted(env.items())
                      if k != "PYTHONDONTWRITEBYTECODE")
    parts = ["'%s'" % a if (" " in a or "\n" in a) else a for a in inv["argv"]]
    line = " ".join(parts)
    if "\n" in line:
        line = " ".join(line.split())
    return (prefix + " " + line).strip() if prefix else line


def emit(w, cid, which, n):
    """One stream of one capture, with an explicit marker on any elision."""
    lines = stream(cid, which).splitlines()
    total = len(lines)
    keep = lines[max(0, total - n):]
    if len(keep) < total:
        w("[elided: %d of %d %s lines shown; the full output is committed at"
          % (len(keep), total, which))
        w("%s/captures/%s.json]" % (EV, cid))
    for line in keep:
        w(line)
    return total


def row(w, label, cids, n=200):
    """A record row: each command, and its capture's own output.

    stderr is rendered whenever it is non-empty, labelled, because on some of
    these commands stderr is where the output is. A row that hid it would be
    reporting an empty result for a command that spoke.
    """
    w("**%s**" % label)
    w("")
    w("```")
    for cid in cids:
        w("$ " + cmdline(cid))
        out = emit(w, cid, "stdout", n)
        err_lines = stream(cid, "stderr").splitlines()
        if err_lines:
            w("--- stderr ---")
            emit(w, cid, "stderr", n)
        elif out == 0:
            w("(no output)")
        w("  exit=%d" % rc(cid))
        w("")
    while L and L[-1] == "":
        L.pop()
    w("```")
    w("")


def yaml_str(s):
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"')


L = []
w = L.append

w("# Gate 3 evidence — %s" % SLICE)
w("")
w("## Publication records")
w("")

row(w, "E1 — the writer role transferred: the `Writer Lease` taken by this "
       "session and read back (the reassignment's own requirement — the "
       "superseded value is named, not silently overwritten)",
    ["G3-lease-take", "G3-lease-readback"])
w("- Superseded value: `%s` — the lease the closed writer session held, read "
  "live immediately before the write." % LEASE_OLD)
w("- New value: `%s`, this session's own label in the recorded "
  "`<host>:<session-label>:<ISO8601>` format." % LEASE_NEW)
w("- One writer before, one writer after, never two at once. The prior writer "
  "session is closed and made no write after its lease was superseded.")
w("")

row(w, "G0 — the two granted field writes, by option id, read back by id "
       "(the Release Approval's item 2; both option ids were verified against "
       "the live option set before either write, and neither value string was "
       "re-typed — CLAUDE.md's byte rule)",
    ["G3-write-gate", "G3-write-workflow", "G3-fields-readback"])
w("- Read back **by option id**, not by name: `Gate` = `bd280e21`, `Workflow` "
  "= `fb82cff0` — the two ids the Release Approval names. A name comparison "
  "cannot distinguish U+2014 EM DASH from U+2192 RIGHTWARDS ARROW, which is "
  "why the id is the thing compared.")
w("- The `Writer Lease` is held by this session, the Slice issue is `OPEN`, "
  "and the label set is empty — so the `needs-human` removal this gate's Entry "
  "requires was already in force and **no label operation was performed**, "
  "which the Release Approval also does not authorise.")
w("- `Status = Todo` is written by GitHub's own built-in workflow and is not "
  "Gatebraid state.")
w("")

row(w, "G1 — Release Approval verified, and the reassignment that transfers "
       "it (author must be `MianliWang`, not this session — ADR-0020 §4; "
       "terms cited by rule number, never restated — ADR-0018 §3)",
    ["G3-Q1-release-approval", "G3-Q1-reassignment", "G3-identity"])
w("- The approval states its publication terms and enumerates what is not "
  "authorised; it is not a `gatebraid/handoff@1` block; its author differs "
  "from the executing session's identity above. Valid on all three entry "
  "conditions.")
w("- `created_at` equals `updated_at` on **both** comments, so each was read "
  "as posted: an edited grant cannot pass as an original one (ADR-0017 §4).")
w("- The reassignment supplements the approval and edits none of it. It "
  "transfers the writer role, the lease and the grant to this session; every "
  "term of the approval stands. It is disclosed below and cited by id.")
w("")

row(w, "G2a — closure precondition (a): platform automation (ADR-0012 §2)",
    ["G3-autoclose"])
w("- `Auto-close issue: enabled=false`. All six built-in workflows are read "
  "and printed, so the row is read in context rather than asserted alone, and "
  "it is the only one disabled — the state the manifest §8 and ADR-0011 §6 "
  "record. Were it enabled it would give a Slice a closure path that bypasses "
  "this gate, which is why the gate refuses to publish while it is on.")
w("")

row(w, "G2b — closure precondition (b): the pull request (pattern stated, "
       "matches printed — `keyword #n | keyword owner/repo#n | keyword <url>`, "
       "keyword ∈ close(s|d)/fix(es|ed)/resolve(s|d), any case — ADR-0018 §1)",
    ["G3-commit-keywords", "G3-pr-closing-refs", "G3-pr-body-keywords",
     "G3-issue-state"])
w("- `closingIssuesReferences` is empty: GitHub's own view is that this pull "
  "request would close nothing.")
w("- The commit-message scan ran **before the push**, because contract row 2b "
  "makes a closing keyword in a commit message an uncorrectable error — "
  "amending history is a force-push, which this gate prohibits. Seven commit "
  "messages searched, zero matches.")
w("- The body scan ran over the body **as GitHub holds it**, not over the "
  "draft that was submitted, so what is checked is what the platform will act "
  "on. The draft was also scanned before the pull request was opened.")
w("- The checker is **P2-S2's committed instrument, reused** — the direction "
  "ADR-0028 §4 sets for evidence tooling — and it was falsified in-window "
  "before this run was trusted: on seeded input carrying all three reference "
  "forms it returned three matches and `VERDICT: FAIL` at exit 1, and it "
  "correctly did **not** match a conventional-commit `fix(scope):` prefix. "
  "The seed was written to a scratch path outside every repository.")
w("- A match would be printed **defused**, with the keyword-to-reference "
  "adjacency broken: a checker never quotes what it forbids into a record in "
  "live form, and this record is itself committed (ADR-0028 §4). There were "
  "none.")
w("- The Slice issue is linked by the plain reference `Refs #12` in the "
  "pull-request body and by no other form. `Refs` is not a closing keyword.")
w("- The Slice issue is still `open`. Closure is this gate's exit by explicit "
  "command and is **not authorised on this grant**.")
w("")

row(w, "G3 — drift check against the Gate 2 fingerprint (ADR-0011 §2 as "
       "amended by ADR-0016 §1) — pinned at both ends, so no row names a state "
       "the act of recording it would move (ADR-0028 §4)",
    ["G3-drift-diff", "G3-drift-complement", "G3-drift-commits",
     "G3-porcelain-complement", "G3-porcelain-full", "G3-porcelain-final",
     "G3-refns"])
w("- Six changed paths past the fingerprint tree `%s`, every one inside this "
  "slice's evidence directory; the **complement is empty**, over the diff to "
  "commit `%s`. The reviewed work — the two `bin/` instruments — is "
  "byte-unchanged since it was reviewed, which is the question the drift check "
  "exists to answer." % (G2_TREE, AMEND2))
w("- No commit between the fingerprint's `active_branch_head` `%s` and `%s` "
  "touches anything outside that directory." % (G2_HEAD, AMEND2))
w("- **The unrestricted `git status --porcelain` is not empty, and is recorded "
  "as measured rather than only in the form that passes.** Every entry is this "
  "gate's own evidence — its capture files and this record's renderer — "
  "committed together with this file. The contract's criterion is met on the "
  "complement: nothing outside this slice's evidence directory is modified or "
  "untracked, and that restricted row is the substantive one, because it is "
  "what distinguishes drift in the reviewed work from a gate writing its own "
  "evidence. Disclosed below as a deviation rather than smoothed away.")
w("- **That row lists 14 entries and the commit carries more, which is a "
  "boundary and not a discrepancy.** The porcelain was read at "
  "`2026-08-23T04:27:28Z`; the captures for the push, the pull request, the CI "
  "read and this record's own renderer did not exist yet, because the commands "
  "they record had not run. A sweep cannot capture its own later output — the "
  "same inherent boundary this Slice's Gate 2 record names for T8. The "
  "complement row is unaffected: every path added after the read is inside the "
  "evidence directory the complement excludes, and the final pre-commit "
  "porcelain was re-read and carries nothing outside it.")
w("- **One ref outside `refs/heads/`, `refs/remotes/` and `refs/tags/` is "
  "reported and not adopted** (gate-3-contract Action 1, friction #103). It is "
  "a `refs/codex/` turn-diff checkpoint pointing at a **tree**, not a commit, "
  "left by the read-only consultant; its embedded timestamp decodes to "
  "`2026-07-31T09:25:00.931Z`, more than three weeks before this slice opened, "
  "so the slice did not introduce it. It is the same ref P2-S1's and P2-S2's "
  "Gate 3 reported. It is local-only and unreachable by the publication: the "
  "push names one ref explicitly, and `push.default`, `push.followTags`, "
  "`remote.origin.push`, `remote.origin.mirror` and `push.autoSetupRemote` are "
  "all unset, verified before the push.")
w("")

row(w, "G4 — publication commands, exactly as approved, in contract order",
    ["G3-lsremote-before", "G3-push-dryrun", "G3-push", "G3-lsremote-after",
     "G3-pr-create"])
w("- Exactly one ref reached the remote, by name, with no force and no tags; "
  "the repository carries no tags at all. `refs/heads/main` is unmoved at `%s`, "
  "its value before the push: no write reached the base branch except through "
  "the pull request (ADR-0017 §3)." % BASE_SHA)
w("- Every remote ref is accounted for: `main`; `m1-control-plane`, kept "
  "because the M1 manifest cites it; `m3/n0-ratification`, retained at its "
  "recorded head; `slice/P2-S1` and `slice/P2-S2`, retained per ADR-0025 §3; "
  "this slice's new ref; and four `refs/pull/<n>/head` refs GitHub maintains "
  "for pull requests 1, 5, 9 and 11. The set is closed and every member is "
  "explained.")
w("- Pull request **#%d**, head `%s` at open, base `main`. Committing this "
  "file necessarily moves the head past the value this file records — the same "
  "boundary the contract names when it says exact head equality \"was not "
  "strict but unsatisfiable\". The live head is the pull request's own Commits "
  "tab." % (PR_NUM, PR_HEAD_AT_OPEN))
w("- The pull-request body was submitted from a file pinned by sha256 as a "
  "capture input, hashed before the command ran. The title carries U+2014 EM "
  "DASH, written from explicit UTF-8 bytes and verified at codepoint level "
  "both before submission and in the stored value GitHub returned.")
w("")

row(w, "G5 — CI status (`none-configured` is a recorded finding, not a pass — "
       "ADR-0011 §7, ADR-0019 §1)",
    ["G3-ci"])
w("- `ci: none-configured`. **A finding, not a pass.** No workflow exists in "
  "this repository, so the prohibition on merging with red CI is inert here, "
  "and this record says so rather than implying a check occurred. The non-zero "
  "exit is the tool reporting an empty check set, not a failing check.")
w("")

row(w, "G6 — the Gate 2 amendment re-validates (the Release Approval's "
       "item 1: `gate-run@2` 0 errors with the loader named, and the repaired "
       "validator's own markdown mode accepting the amended record)",
    ["G3-revalidate-structural", "G3-revalidate-markdown"])
w("- Structural: `error_count` 0, `result: passed`, 20 checks and 20 with an "
  "`output_ref`, loader named in the output rather than assumed. The amended "
  "record is sha256 `%s`, %d bytes." % (GATE2_SHA, GATE2_BYTES))
w("- The repaired validator's **markdown mode** reads and accepts the amended "
  "`gate2.md`: 1 document, 0 rejected or errored, exit 0. That is this Slice's "
  "own subject instrument reading this Slice's own record — reported as such, "
  "not offered as independent validation.")
w("- The structural check is deliberately **not** this Slice's validator. It "
  "reaches `jsonschema` directly and names its loader, so the two rows are "
  "independent of each other.")
w("")
w("- Pull request: %s — referenced, not duplicated (ADR-0017 §2)" % PR_URL)
w("")

w("## Required disclosures")
w("")
w("- Deviations: **(1) The writer role was reassigned mid-Slice.** The "
  "original writer session — the one that took the lease `%s` and made the six "
  "commits ending `%s` — is closed. The operator transferred the writer role, "
  "the `Writer Lease` and the Release Approval's grant to this fresh session "
  "by the comment at %s (id `%s`, %s), which supplements the approval and "
  "edits none of it. This session certified it held no prior role on this "
  "Slice: it is not the closed writer session and it is not the Review-1 "
  "session, whose independence is untouched. The lease's superseded value is "
  "named at E1 above. Single-writer is preserved: one writer before, one "
  "after, never two."
  % (LEASE_OLD, AMEND1, REASSIGN, REASSIGN_ID, REASSIGN_AT))
w("  **(2)** The unrestricted `git status --porcelain` at the drift check is "
  "**not empty**, and is recorded in full at G3. Its entries are this gate's "
  "own evidence — the capture files and this record's renderer, committed with "
  "this file. The contract's criterion is met on the complement of this "
  "slice's evidence directory, which is the row that answers the question the "
  "drift check asks. Reported, not smoothed away; the same deviation P2-S2's "
  "Gate 3 recorded, for the same reason.")
w("  **(3)** This gate records captures where the template's rows are inline "
  "command-and-output; the rows above are generated from those capture "
  "records, so each is pinned by a `gatebraid/evidence-capture@1` document as "
  "well as printed here. The template's `output_ref: \"#publication-records\"` "
  "is kept, and the capture paths are named by the elision markers wherever a "
  "row shows less than its capture.")
w("  **(4)** Three rows beyond the template's fixed set are added — **E1**, "
  "the lease transfer, which the reassignment requires be read back and which "
  "is otherwise recorded nowhere; **G0**, the two granted field writes read "
  "back by id, following P2-S2; and **G6**, the item-1 re-validation. The "
  "headings are new and the choice is disclosed rather than made silently.")
w("  **(5)** `ci: none-configured` is recorded as a finding, not a pass.")
w("  **(6)** One `refs/codex/` tree ref is reported under G3 and not adopted; "
  "it predates the slice by more than three weeks and cannot reach the remote.")
w("  **(7)** **This gate stops at the pull request.** The merge is not "
  "authorised here and is never the executor's: the operator merges in the "
  "browser. Exit steps 2 through 6 of the Gate 3 contract — the merge, "
  "`Gate → G3 passed`, `Workflow → Done`, explicit closure of the Slice issue, "
  "lease release, `Next Approval` back to the bare option, the friction append "
  "with its ordinals assigned from the measured end, and the record-keeping "
  "updates — are therefore **not performed here, and are reported rather than "
  "skipped silently**. They run under the closure batch's own posted approval.")
w("  **(8)** Commit messages carry a `Co-Authored-By` trailer, which prior "
  "commits in this repository outside this Slice do not; it is added per the "
  "executing harness's standing instruction and is noted so the change in "
  "convention is not mistaken for drift. No commit message on this branch "
  "carries any issue reference; the Slice issue is linked by the plain "
  "`Refs #12` in the pull-request body alone.")
w("  **(9)** **Two Python invocations early in this session did not carry "
  "`PYTHONDONTWRITEBYTECODE=1`** — read-only analysis of the schema and the "
  "review report during establishment, before this gate's own work began. "
  "Measured consequence: none. Both read their program from stdin, so no "
  "source file existed beside which a cache could be written, and the tree was "
  "checked immediately afterwards — no `__pycache__` and no `.pyc` anywhere "
  "outside `.git/`, and `--untracked-files=all` porcelain empty. The rule is "
  "nevertheless *every* invocation, so the lapse is disclosed rather than "
  "excused by its null result; every invocation after it carried both the "
  "environment variable and `-B`. This is the over-disclosure direction "
  "(friction #107).")
w("  **(10)** The renderer's pin on the review report was moved from the "
  "report as first reviewed to the **full current file**, per the "
  "coordinator's ruling, because the re-review addendum changed the bytes and "
  "the stale pin failed closed by design. The value the Gate 2 record *cites* "
  "is the addendum's own boundary-2 measurement, which is what the Release "
  "Approval cites. Both are verified at render time, not carried.")
w("- Environment: Windows 11 (10.0.26200), Git Bash over Git for Windows "
  "2.51.0 with the system `core.autocrlf=true` read from "
  "`D:/Program Files/Git/etc/gitconfig` and in-tree `.gitattributes` "
  "`* text=auto eol=lf`; `C:/Python312/python.exe` CPython 3.12.2 (jsonschema "
  "4.23.0, PyYAML 6.0.2); declared `environment: mixed-see-prose`, the second "
  "platform being WSL Ubuntu `/usr/bin/python3` CPython 3.12.3 (jsonschema "
  "4.10.3, PyYAML 6.0.1), exercised at Gate 2 and not re-entered here; "
  "`GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` set on every `gh` invocation, "
  "with the identity check run first and alone; every `gh api` endpoint "
  "written without a leading slash, because MSYS rewrites leading-slash "
  "endpoints into filesystem paths (friction #33); `PYTHONDONTWRITEBYTECODE=1` "
  "and `-B` on every Python invocation of this gate, with the two "
  "establishment-phase exceptions disclosed above; all seeded and scratch "
  "files written to a scratch path outside every repository.")
w("")

w("## gatebraid-metadata")
w("")
w("```yaml")
w("schema: gatebraid/gate-run@2")
w("slice_id: %s" % SLICE)
w("gate: 3")
w("environment: mixed-see-prose")
w("executor: Claude Lead")
w("base_sha: %s" % BASE_SHA)
w("active_branch: slice/%s" % SLICE)
w("started_at: %s" % yaml_str(STARTED_AT))
w("ended_at: %s" % yaml_str(ENDED_AT))
w("result: passed")
w("checks:")
CHECKS = [
    ("writer-lease-transferred-readback",
     "gh api graphql updateProjectV2ItemFieldValue (Writer Lease) + read-back",
     "pass", "#publication-records"),
    ("granted-field-writes-readback",
     "gh project item-edit x2 by option id, then one read-back by item id",
     "pass", "#publication-records"),
    ("release-approval-verified",
     "gh api repos/MianliWang/gatebraid/issues/comments/5381788134 --jq {author,url,created,updated}",
     "pass", "#publication-records"),
    ("closure-precondition-automation",
     "gh api graphql -f query=query($p:ID!){ node(id:$p){ ... on ProjectV2 { workflows(first:20){ nodes{ name enabled } } } } } -F p=PVT_kwHOBRofUs4Beum7",
     "pass", "#publication-records"),
    ("closure-precondition-pull-request",
     "gh pr view 13 --json closingIssuesReferences; closing-keyword-scan.py run twice - over every commit message before the push, and over the pull-request body as GitHub holds it",
     "pass", "#publication-records"),
    ("staged-set-matches-gate2-handoff",
     "git diff --name-only %s %s" % (G2_TREE, AMEND2),
     "pass", "#publication-records"),
    ("ref-namespace-clean",
     "git for-each-ref --format=%(refname) %(objecttype)",
     "pass", "#publication-records"),
    ("publication-push-one-ref",
     "git push origin slice/P2-S3, with git ls-remote origin before and after",
     "pass", "#publication-records"),
    ("pull-request-opened",
     "gh pr create --repo MianliWang/gatebraid --base main --head slice/P2-S3",
     "pass", "#publication-records"),
    ("ci-status", "gh pr checks 13 --repo MianliWang/gatebraid",
     "none_configured", "#publication-records"),
    ("gate2-amendment-revalidates",
     "checks/g0_record_validation.py gate2.md schema/gate-run-v2.schema.json; checks/g1_sweep.py over gate2.md",
     "pass", "#publication-records"),
]
for name, cmd, result, ref in CHECKS:
    w("  - name: %s" % name)
    w("    command: %s" % yaml_str(cmd))
    w("    result: %s" % result)
    w("    output_ref: %s" % yaml_str(ref))
w("consults: []")
w("approvals:")
w('  - type: "Release Approval (G2→G3)"')
w("    comment_url: %s" % yaml_str(APPROVAL))
w('    author: "MianliWang"')
w("    at: %s" % yaml_str(APPROVAL_AT))
w("evidence_files:")
w("  - %s/gate3.md" % EV)
w("notes: %s" % yaml_str(
    "PR %s, head %s at open. No merge SHA and no closure timestamp are "
    "recorded here - GitHub holds both natively (ADR-0017 2). The merge and "
    "the closure batch are not authorized on this grant and are not performed: "
    "the operator merges in the browser. The writer role was reassigned "
    "mid-Slice to this session by comment %s, which supplements the Release "
    "Approval and edits none of it; the superseded lease value is recorded at "
    "E1. This gate published the amendment commit %s, tree %s, whose parent is "
    "exactly %s - two paths, both inside the frozen allowlist, carrying the "
    "re-review transcription that turned R3 and the result: passed the Release "
    "Approval granted."
    % (PR_URL, PR_HEAD_AT_OPEN, REASSIGN_ID, AMEND2, AMEND2_TREE, AMEND1)))
w("```")

data = ("\n".join(L) + "\n").encode("utf-8")
if b"\r" in data:
    print("CR byte in rendered record; refusing to write"); sys.exit(3)
open(OUT, "wb").write(data)
print(json.dumps({"written": OUT, "bytes": len(data),
                  "sha256": hashlib.sha256(data).hexdigest(),
                  "checks": len(CHECKS)}))
