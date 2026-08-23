#!/usr/bin/env python3
"""Gate 2 record renderer — P2-S3.

Emits docs/evidence/gatebraid/P2-S3/gate2.md in the templates/gate2-evidence.md
shape, with every recorded output GENERATED from the pinned capture files rather
than transcribed (ADR-0026; friction #96).

Review 1 has run. Its verdict table and finding summaries are GENERATED from the
reviewer's own report rather than retyped: the report is pinned by sha256 and
this renderer refuses to write when it does not match, so the verdict column is
a byte-faithful transcription by construction (ADR-0026; friction #96).

Repair 1 addresses the review's F-1. Every row that shows less than its capture
now carries `shown/total` and the committed path of the full output, and the
lines F-1 named as missing are restored FROM THE CAPTURE BYTES, never retyped.

Usage: g2_render_record.py <captures-dir> <out-path> <ended_at>
"""
import sys, os, json, base64, hashlib, re, subprocess

CAP, OUT, ENDED_AT = sys.argv[1], sys.argv[2], sys.argv[3]

SLICE = "P2-S3"
BASE_SHA = "63c8401f5df6ba446cf002232fcb280673c28e00"
HEAD = "28d5dfcd83b83b7541a3d8f73732fb833a3d119c"
TREE = "3012c2a70b053721f61f99bb5e2e1c41cdbc7408"
STARTED_AT = "2026-08-22T05:07:00Z"
EV = "docs/evidence/gatebraid/P2-S3"
APPROVAL = "https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5378088991"
PLAN_HASH = "eb89d3eaedc2690babb3086e3be7529f62fa03e7195746b3b8106ad85a626b18"
ALLOW_HASH = "81a0bb015ffbc5f3f6a27abfaec0a089c2b5522aa69e5ee30d5d7a01ecd404c0"

# Review 1's report — the sole findings source. Pinned: a mismatch means the
# transcription below would be of something other than what the reviewer wrote,
# so this renderer fails closed rather than emitting an unpinned verdict.
REPORT = "_handoff/batch-p2s3/REVIEW1-M3-P2S3.md"
REPORT_SHA = "ca7586d8e7c741b5abab318cb3363574b155e0ee116eb2b54c1aff5dbc26f3a9"
REPORT_BYTES = 56244

# The re-review addendum is self-measured to its own named boundary, because a
# hash cannot cover the bytes that state it. The READ GATE above is the full
# current file; the value this record CITES is the boundary-2 one, which is what
# the Release Approval cites. Both are verified rather than declared: the prefix
# is re-hashed at render time and a mismatch is fatal, exactly as the full-file
# pin is.
ADDENDUM_SHA = "1439acf8857f39b5be16e324aebfcf9fbeefac6886f8701283928bdf1566b596"
ADDENDUM_BYTES = 55053

# Repair 1's measure-before-grade comparand (ADR-0027 §1): the tree of the state
# the review failed. Named by full sha, never by HEAD (ADR-0028 §4).
PREV_HEAD = "43022db1721940bfdcd0abcc9c55b150b77fa89d"
PREV_TREE = "3d934d46c18e7c68bad01974bd4a0ac8e0ebbef0"
SELF = "%s/checks/g2_render_record.py" % EV


def report_text():
    raw = open(REPORT, "rb").read()
    got = hashlib.sha256(raw).hexdigest()
    if got != REPORT_SHA or len(raw) != REPORT_BYTES:
        print("REVIEW REPORT NOT AT ITS PINNED VALUE: %s, %d bytes (expected %s, %d)"
              % (got, len(raw), REPORT_SHA, REPORT_BYTES))
        sys.exit(3)
    pre = hashlib.sha256(raw[:ADDENDUM_BYTES]).hexdigest()
    if pre != ADDENDUM_SHA:
        print("ADDENDUM BOUNDARY 2 NOT AT ITS PINNED VALUE: %s over %d bytes "
              "(expected %s)" % (pre, ADDENDUM_BYTES, ADDENDUM_SHA))
        sys.exit(3)
    return raw.decode("utf-8")


RPT = report_text()


def verdict_rows():
    """The reviewer's five table rows, taken verbatim from the report."""
    rows = [l for l in RPT.split("\n") if re.match(r"^\| R[1-5] ", l)]
    if len(rows) != 5:
        print("expected 5 verdict rows in the report, found %d" % len(rows)); sys.exit(3)
    return rows


def finding_summaries():
    """The report's own one-line finding headings, whitespace-collapsed."""
    out = [" ".join(m.group(1).split())
           for m in re.finditer(r"\*\*(F-\d .*?)\*\*", RPT, re.S)]
    if len(out) != 6:
        print("expected 6 findings in the report, found %d" % len(out)); sys.exit(3)
    return out


def rereview_ruling():
    """Section H's ruling, taken verbatim from the addendum.

    The re-review is Review 1's own window re-checking R3 and nothing else. Its
    verdict is transcribed the same way the first-pass table is — read out of
    the report, never retyped — so this record cannot drift from what the
    reviewer wrote, and a change in the report's wording stops the render rather
    than passing silently.
    """
    sec = re.search(r"^### H\. Ruling\n(.*?)\n<!-- fingerprint boundary 2",
                    RPT, re.S | re.M)
    if not sec:
        print("re-review ruling section not found in the report"); sys.exit(3)
    body = sec.group(1)
    verdict = re.search(r"^\*\*(R3 on re-review: .*?)\*\*$", body, re.M)
    # The scope paragraph closes the section, so it runs to the section end —
    # which the boundary-2 comment already pins, as the file's sha256 pins the
    # whole. No terminator of its own is needed or invented.
    scope = re.search(r"^(R1, R2, R4 and R5 are unchanged at PASS\..*)",
                      body, re.S | re.M)
    if not verdict or not scope:
        print("re-review ruling not in the expected form"); sys.exit(3)
    return verdict.group(1), " ".join(scope.group(1).split())


def git(*args):
    return subprocess.run(("git",) + args, capture_output=True).stdout.decode("utf-8").strip()


def load(cid):
    p = os.path.join(CAP, cid + ".json")
    if not os.path.exists(p):
        print("MISSING CAPTURE: " + cid); sys.exit(3)
    return json.load(open(p, encoding="utf-8"))


def stream(cid, which="stdout"):
    d = load(cid)
    return base64.b64decode(d["streams"][which]["data"]).decode("utf-8").replace("\r\n", "\n").rstrip("\n")


def rc(cid):
    return load(cid)["exit_code"]


def cmdline(cid):
    d = load(cid)
    inv = d["invocation"]
    env = inv.get("environment") or {}
    prefix = " ".join("%s=%s" % (k, v) for k, v in sorted(env.items())
                      if k != "PYTHONDONTWRITEBYTECODE")
    parts = ["'%s'" % a if (" " in a or "*" in a or "\n" in a) else a for a in inv["argv"]]
    line = " ".join(parts)
    if "\n" in line:
        line = " ".join(line.split())
    return (prefix + " " + line).strip() if prefix else line


def tail(cid, n):
    return "\n".join(stream(cid).splitlines()[-n:])


def row(w, label, cid, n, head=0):
    """One record row: the command, and a window onto the capture's own output.

    When the window is smaller than the capture, the row carries `shown/total`
    and the committed path of the full output — the form V16 already used, and
    the form ADR-0026 §1(b), gate-2-contract R3 and templates/gate2-evidence.md
    require of EVERY elision. Review 1's F-1 was that nine rows elided without
    it. `head` keeps the capture's opening lines when the row must show them
    (friction #55: a schema-validation row names its loader); the markers carry
    no ellipsis, so an elision can never be mistaken for a placeholder.
    """
    lines = stream(cid).splitlines()
    total = len(lines)
    keep = sorted(set(range(min(head, total))) | set(range(max(0, total - n), total)))
    shown = len(keep)
    w("*%s*" % label)
    w("```")
    w("$ " + cmdline(cid))
    if shown < total:
        w("[elided: %d of %d output lines shown; the full output is committed at"
          % (shown, total))
        w("%s/captures/%s.json]" % (EV, cid))
    if total == 0:
        w("")
    else:
        prev = None
        for i in keep:
            if prev is not None and i != prev + 1:
                w("[%d further lines elided here]" % (i - prev - 1))
            w(lines[i])
            prev = i
    w("  exit=%d" % rc(cid))
    w("```")
    w("")


def yaml_str(s):
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"')


changed = [l for l in stream("G2-changed-paths").splitlines() if l.strip()]

# ADR-0027 §1: novelty is MEASURED before the result is graded. An unchanged
# tree is not a repair. The comparand is the state Review 1 failed, named by
# full sha rather than by HEAD (ADR-0028 §4). This renderer refuses to grade a
# repair green when the instrument it repairs has not moved.
OLD_BLOB = git("rev-parse", "%s:%s" % (PREV_HEAD, SELF))
NEW_BLOB = git("hash-object", SELF)
if not OLD_BLOB or not NEW_BLOB:
    print("NOVELTY UNMEASURABLE: git did not return a blob id"); sys.exit(3)
if OLD_BLOB == NEW_BLOB:
    print("NOVELTY FAILED: %s is unchanged at %s; an unchanged tree is not a repair"
          % (SELF, OLD_BLOB))
    sys.exit(3)

L = []
w = L.append

w("# Gate 2 evidence — %s" % SLICE)
w("")
w("## Entry records")
w("")
w("**E1 — Plan Approval verified** (author must be `MianliWang`, not this")
w("session — ADR-0020 §4; hashes must match the frozen values)")
w("```")
w("$ " + cmdline("G2-approval-provenance"))
w(stream("G2-approval-provenance"))
w("$ " + cmdline("G2-executor-identity"))
w(stream("G2-executor-identity"))
w("```")
w("The author `MianliWang` is not the executor `mianliwang492-source`, so the")
w("approval was not written by the session it authorises. `created_at` equals")
w("`updated_at`, so the grant that was posted is the grant that was read: an")
w("approval edited after posting is not the approval that was given. Both frozen")
w("hashes appear in the approval body — `plan_hash` `%s`" % PLAN_HASH)
w("and `allowlist_hash` `%s`." % ALLOW_HASH)
w("")
w("**E2 — Writer Lease taken, read back**")
w("```")
w("$ " + cmdline("G2-lease-take"))
w(tail("G2-lease-take", 2))
w("$ " + cmdline("G2-entry-readback"))
w(json.dumps(next(
    ({"Writer Lease": fv.get("text")} for fv in
     json.loads(stream("G2-entry-readback"))["data"]["node"]["fieldValues"]["nodes"]
     if (fv.get("field") or {}).get("name") == "Writer Lease"), {})))
w("```")
w("")
w("**E3 — baseline re-read** (ADR-0011 §9; ADR-0014 §1 excludes")
w("`docs/evidence/gatebraid/P2-S3/` before the intersection)")
w("```")
w("$ " + cmdline("G2-baseline-reread"))
w(stream("G2-baseline-reread"))
w("```")
w("- X, the plan baseline recorded in `gate0.md`: `%s`" % BASE_SHA)
w("- Y, the head of the base branch now: `%s`" % stream("G2-baseline-reread").split()[0])
w("- baseline: `unchanged`")
w("")
w("`X == Y`, so the plan's assumptions are intact and no changed-path set exists")
w("to intersect with the frozen allowlist. The outcome is recorded here because")
w("the contract requires it in every case, including no change. The `Base SHA`")
w("field already carried this value from setup, and its agreement with `Y` was")
w("confirmed before the branch was cut.")
w("")
w("**E4 — Active Branch created from Y; `Base SHA` field set to Y**")
w("```")
w("$ " + cmdline("G2-branch-create"))
w(tail("G2-branch-create", 2))
w("```")
w("`Active Branch` = `slice/P2-S3`, `Base SHA` = `%s` — both read back at E-exit." % BASE_SHA)
w("")
w("## Verification outputs")
w("")
# tuple: (label, capture id, tail lines, head lines)
# head > 0 on V3 and V6 so the validator's `loader :` line stays in the row
# (friction #55); V8's window starts at S23 so Task A's positive-direction pair
# is in the row a reader checks acceptance box 1 against. Both are Review 1's
# F-1; both are taken from the capture bytes by `row`, never retyped.
for label, cid, n, head in [
    ("V1 — T1 Windows: the heuristic accepts what it wrongly rejected "
     "(acceptance box 1, positive direction)", "G2-T1-windows", 3, 0),
    ("V2 — T1 WSL: the same, on the second declared platform", "G2-T1-wsl", 3, 0),
    ("V3 — T2: a genuine elision still rejects (acceptance box 1, negative "
     "direction; negative criterion N2)", "G2-T2-windows", 14, 3),
    ("V4 — T3 Windows: the markdown mode reads what it could not read "
     "(acceptance box 2)", "G2-T3-windows", 5, 0),
    ("V5 — T3 WSL", "G2-T3-wsl", 5, 0),
    ("V6 — T4 seed 1: an invalid embedded record is rejected, not merely read",
     "G2-T4-invalid", 5, 3),
    ("V7 — T4 seed 2: a file that is not a record stays an input error "
     "(the pre-existing broken-input condition does not regress)",
     "G2-T4-notarecord", 2, 0),
    ("V8 — T5 Windows: the selftest, carrying both repairs in both directions "
     "(acceptance box 4)", "G2-T5-windows", 14, 0),
    ("V9 — T5 WSL", "G2-T5-wsl", 6, 0),
    ("V10 — T6: the frozen corpus is unmoved (acceptance box 4; friction #165 "
     "budget case, 420,000 ms, measured 147,993 ms)", "G2-T6-windows", 7, 0),
    ("V11 — T7 Windows: the corpus mutation suite still passes", "G2-T7-windows", 5, 0),
    ("V12 — T7 WSL", "G2-T7-wsl", 5, 0),
    ("V13 — T9 Windows — Task C: the N2 re-validation run to completion "
     "(acceptance boxes 2 and 3)", "G2-T9-windows", 14, 0),
    ("V14 — T9 WSL: Task C on the second declared platform", "G2-T9-wsl", 14, 0),
    ("V15 — T8: the self-validation point — the repaired validator over this "
     "Slice's own evidence, discharging the state packet §5 disclosed limit",
     "G2-T8-windows", 16, 0),
]:
    row(w, label, cid, n, head)

w("**V16 — the handoff fingerprint, both ends pinned**")
w("```")
w("$ " + cmdline("G2-fingerprint"))
w(stream("G2-fingerprint"))
w("$ " + cmdline("G2-changed-paths"))
w("[elided: %d of %d changed paths shown; the full sorted set is the"
  % (6, len(changed)))
w(" `changed_paths` array of the metadata block below, and the full output is")
w(" committed at %s/captures/G2-changed-paths.json]" % EV)
for p in changed[:6]:
    w(p)
w("```")
w("")
w("## Review record")
w("")
w("### Review 1")
w("")
w("| Item | Verdict | Evidence |")
w("|---|---|---|")
for _r in verdict_rows():
    w(_r)
w("")
w("**Findings** — Review 1's own one-line summaries, read from the report:")
w("")
for _f in finding_summaries():
    w("- %s" % _f)
w("")
w("- Reviewer: `Claude Read-Only Team`, a fresh read-only window under its own "
  "dispatch. Source: `%s`, measured to its `fingerprint boundary 2` — sha256 "
  "`%s`, %d bytes. Every row of the table above and every summary above is "
  "generated from that file, not retyped."
  % (REPORT, ADDENDUM_SHA, ADDENDUM_BYTES))
w("- Reviewer write disclosure: one write, `%s`, on the ignored `_handoff/` "
  "path — no commit, no tracked-file edit, no `gh` mutation, no label, field or "
  "comment operation, no lease taken. The five WSL halves it re-ran in recorded "
  "form wrote no bytecode, verified after each run and by an empty "
  "`--untracked-files=all` porcelain at the end." % REPORT)
w("- Rules given to the reviewer: the spec §4 conduct rules, enumerated in full "
  "at the report's own `## Conduct rules this review was given` — measure never "
  "declare; cite never restate; never echo a forbidden value into the record, "
  "name loci and counts; a bare zero states what it searched; closed-set by "
  "complement with the ruled touch-vs-mention distinction; the capture pair "
  "never read, only executed; `GH_CONFIG_DIR` pinned per call and identity "
  "checked first and alone; `PYTHONDONTWRITEBYTECODE=1` with the measured "
  "caveat that it does not cross `wsl -e`; dash and arrow marks never retyped; "
  "business repositories untouchable; single writer; STOP and ask on any "
  "uncertainty.")
w("")
w("### Re-review after repair 1")
w("")
_verdict, _scope = rereview_ruling()
w("The R3 row in the table above is Review 1's FIRST-PASS verdict, recorded as it")
w("was returned. Repair 1 — recorded in full at `## Repair record` below — was")
w("built against it, and the same read-only window that failed R3 re-checked it.")
w("Its ruling, read from the report and not retyped:")
w("")
w("> **%s**" % _verdict)
w("")
w("> %s" % _scope)
w("")
w("- Re-review source: the same report, its `## Re-review after repair 1` "
  "addendum, measured to `fingerprint boundary 2` — sha256 `%s`, %d bytes. "
  "This renderer re-hashes that prefix on every run and refuses to write when "
  "it does not match, so the citation is measured here, not carried."
  % (ADDENDUM_SHA, ADDENDUM_BYTES))
w("- Scope of the re-review: **R3 only**. R1, R2, R4 and R5 were not reopened "
  "and are unchanged at PASS. The reviewer graded and stopped; disposition is "
  "the Release Approval's.")
w("- `review-five-items` is therefore recorded `pass`: that is the truthful "
  "final state of the COMPLETED sequence — R1 pass, R2 pass, R3 fail then "
  "repair 1 then pass on re-review, R4 pass, R5 pass. The intermediate FAIL is "
  "not erased; it stands in the table above and in the repair record below, "
  "which is what makes the final value auditable rather than merely asserted.")
w("")
w("## Repair record")
w("")
w("### Repair 1")
w("")
w("- Finding addressed: **F-1**, the finding Review 1's R3 fail rests on — nine")
w("  rows showed a window smaller than their capture with no `shown/total` and")
w("  no committed path in the row.")
w("- Hypothesis (new): the rule was broken at RENDER rather than at measurement")
w("  — the row writer emitted a tail window and never a marker, so every row")
w("  whose window was smaller than its capture elided silently.")
w("- Remedy: the row writer now emits `shown/total` and the capture's committed")
w("  path whenever the window is smaller than the capture, and can hold a")
w("  capture's opening lines when the row must carry them. Every restored line")
w("  is read from the capture bytes by the instrument, never retyped.")
w("")
w("**Novelty measured** (ADR-0027 §1: an unchanged tree is not a repair. The")
w("comparand is the state Review 1 failed, named by full sha, never by `HEAD`.)")
w("```")
w("$ git rev-parse %s^{tree}" % PREV_HEAD)
w(PREV_TREE)
w("$ git rev-parse %s:%s" % (PREV_HEAD, SELF))
w(OLD_BLOB)
w("$ git hash-object %s" % SELF)
w(NEW_BLOB)
w("```")
w("The render instrument's blob differs from the one the failed state carried, so")
w("the amended tree cannot equal `%s`." % PREV_TREE)
w("This renderer exits 3 rather than grade a repair green when those two blob ids")
w("are equal.")
w("")
w("- Changed by this repair: `%s/gate2.md` and" % EV)
w("  `%s` — record text and the" % SELF)
w("  instrument that generates it, both inside the frozen allowlist. No `bin/`")
w("  file, no frozen-plan text, no historical record, and no capture: the")
w("  measurements are the ones Review 1 already re-ran and confirmed.")
w("- Result: `green`")
w("- Consult: `none`")
w("")
w("`repair_limit` is 2; this is attempt 1, so one attempt remains unspent.")
w("")
w("## Required disclosures")
w("")
w("- Deviations: **`bin/__pycache__/` was created and removed inside this gate, "
  "and the attribution this record first carried for it is WITHDRAWN (Review 1's "
  "F-3).** The standing rule is `PYTHONDONTWRITEBYTECODE=1` on every Python "
  "invocation; it was set on every Windows invocation and does **not** cross into "
  "WSL, which inherits none of the Windows process environment. That much is "
  "measured, and measured twice — at this gate and again by Review 1: "
  "`wsl -e printenv PYTHONDONTWRITEBYTECODE` returns empty. What is withdrawn is "
  "the sentence that followed it, that the WSL halves of T1, T3, T5, T7 and T9 "
  "wrote the bytecode. Review 1 ran all five in their recorded form and none "
  "wrote any, and the mechanism says why: `g1_sweep.py` and the selftest reach "
  "the validator by `subprocess.run`, so no module under `bin/` is ever imported "
  "and no bytecode can be generated there, while `fixtures/run-corpus.py` "
  "documents that importing the corpus instruments writes `fixtures/__pycache__/` "
  "— a different path, which that runner excludes by name. The claim was an "
  "inference from a true premise, presented as a measurement. What stands: the "
  "directory was observed, it was removed before the first commit, and no `.pyc` "
  "reached the index. What is undetermined: what created it. The error direction "
  "was OVER-disclosure — this record disclosed a write more broadly than it "
  "occurred, which is the safe direction and the opposite of the failure R1 "
  "exists to catch (friction #107). A CANDIDATE mechanism was measured while "
  "repairing this record and is offered as a candidate only, not as a finding of "
  "cause: `python -m py_compile` writes `__pycache__/` beside its target even "
  "with `PYTHONDONTWRITEBYTECODE=1` set, because explicit compilation is not "
  "import-time caching. It was reproduced on a file in a scratch directory "
  "outside every repository. Whether anything of that shape ran against `bin/` "
  "at this gate is not known and is not claimed · **repair 1 itself created and "
  "removed `docs/evidence/gatebraid/P2-S3/checks/__pycache__/`**, by the "
  "`py_compile` syntax check named above, on this record's own render "
  "instrument. It was removed before the amendment commit, no `.pyc` reached the "
  "index, and it is disclosed here for the same reason the first one is: a write "
  "created and removed inside a gate is invisible to the diff. "
  "`__pycache__` is not in this repository's `.gitignore` — a pre-existing gap "
  "outside this Slice's frozen allowlist, reported and not fixed. The corpus "
  "digest is unaffected and V10 confirms it: the runner's own seed set asserts "
  "the digest ignores interpreter output · **a raw GraphQL response was written "
  "into `captures/` with a shell redirect during entry and removed.** It was not "
  "an `evidence-capture@1` record and did not belong in a directory whose "
  "contract is that every file is one; T8 caught it as an exit-2 input error, "
  "which is the sweep doing its job on its own evidence. It was replaced by a "
  "proper capture, `G2-entry-readback`, whose field values are unchanged since "
  "entry; both the creation and the removal are disclosed here · the capture "
  "tool's `--form shell` was not used: it returned `STRUCTURE: the command could "
  "not be executed (FileNotFoundError)` on this host at Gate 1 and the behaviour "
  "was not investigated, because inspecting the capture tool beyond its "
  "documented interface is a STOP-and-ask under the ratified isolation rule; "
  "every capture here is argv form · **T8 does not include the captures written "
  "after it ran** — its own capture, the fingerprint and changed-path captures, "
  "and this record — the same inherent boundary a sweep always has over its own "
  "output · **T8 is not a clean sweep and was not made one.** Six documents are "
  "rejected: five at `/streams/stdout/rendered/text` and one at `/notes`. Both "
  "loci are outside the frozen exemption by design. `rendered.text` is not "
  "re-derived from `data` anywhere in the validator, so exempting it would delete "
  "the only check that field has; the `/notes` case is this gate's own lease "
  "note, which quotes the lease *format* in angle brackets, and angle-bracket "
  "stand-ins never qualify as a mention. The frozen plan predicted this state and "
  "the Plan Approval endorsed the prediction as binding acceptance semantics · "
  "**commit messages carry a `Co-Authored-By` trailer**, which prior commits in "
  "this repository do not; it is added per the executing harness's standing "
  "instruction and is noted so the change in convention is not mistaken for "
  "drift · **the frozen plan's `gate3.md` expectation was wrong when frozen "
  "(Review 1's F-2), and is reconciled HERE rather than in the frozen text.** The "
  "plan states at T3, and again at T9, that "
  "`docs/evidence/gatebraid/P2-S1/gate3.md` is rejected on its own **two** "
  "`/checks/N/command` elisions. Measured, on both declared platforms: **one** "
  "finding, at the single locus `/checks/1/command`. The document does carry two "
  "elisions, but both sit in one string at that one locus, and "
  "`check_placeholders` emits at most one finding per string value — behaviour "
  "that PREDATES this Slice's repair, where the walk was a single search per "
  "string. The mention count for that document is zero, so nothing was "
  "reclassified as a mention: the count is what the instrument emits, not what "
  "the exemption suppressed. The Gate 2 report's `one` is the measured value and "
  "stands. The plan section is deliberately NOT edited: it is frozen under "
  "`plan_hash`, its author had not measured this when it was frozen, and a later "
  "measurement belongs in a record rather than in a silently rewritten plan — the "
  "same treatment this gate already gave the T6 WSL timing · **the frozen plan's "
  "`gate0.json` citation count is off by one (Review 1's F-4), corrected HERE for "
  "the same reason.** Task A's prose reads as nine ellipsis-form citations plus "
  "one angle-bracket stand-in, which is ten. Measured, the population is nine in "
  "total: eight ellipsis-kind, and one angle-bracket-kind at `/checks/5/command`. "
  "The negative criterion N2's own count of nine was exact throughout, and nine "
  "is what every run of T2 and T9 reproduces; only the surrounding prose "
  "over-counted.")
w("- Reviewer write disclosure: one write, `%s`, on the ignored `_handoff/` path "
  "— no commit, no tracked-file edit, no `gh` mutation, no label, field or "
  "comment operation, no lease taken; the five WSL halves Review 1 re-ran wrote "
  "no bytecode. This gate's own writes are disclosed above." % REPORT)
w("- Environment: Windows 11 host, Git Bash (MSYS2) shell, with the WSL half of "
  "`mixed-see-prose` exercised for T1, T3, T5, T7 and T9; Windows loader "
  "`C:\\Python312\\python.exe` (CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0), "
  "WSL `/usr/bin/python3` (3.12.3, PyYAML 6.0.1, jsonschema 4.10.3); "
  "`PYTHONDONTWRITEBYTECODE=1` on every Windows Python invocation and, as "
  "disclosed above, not inherited by WSL; "
  "`GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` call; every "
  "`gh api` endpoint written without a leading slash (friction #33); the T4 seeds "
  "were written to a scratch path outside every repository, as the contract "
  "requires such a path to be named.")
w("")
w("## gatebraid-metadata")
w("")
w("```yaml")
w("schema: gatebraid/gate-run@2")
w("slice_id: %s" % SLICE)
w("gate: 2")
w("environment: mixed-see-prose")
w("executor: Claude Lead")
w("base_sha: %s" % BASE_SHA)
w("active_branch: slice/P2-S3")
w("started_at: %s" % yaml_str(STARTED_AT))
w("ended_at: %s" % yaml_str(ENDED_AT))
w("result: passed")
w("checks:")
CHECKS = [
    ("plan-approval-verified", "gh api repos/MianliWang/gatebraid/issues/comments/5378088991 --jq '{author,url,created,updated}'", "pass", "#entry-records"),
    ("writer-lease-taken", "gh api graphql updateProjectV2ItemFieldValue (Writer Lease) + read-back", "pass", "#entry-records"),
    ("baseline-re-read", "git ls-remote origin refs/heads/main", "pass", "#entry-records"),
    ("active-branch-created-from-Y", "git checkout -b slice/P2-S3 " + BASE_SHA, "pass", "#entry-records"),
    ("T1-heuristic-accepts-windows", None, "pass", "%s/captures/G2-T1-windows.json" % EV),
    ("T1-heuristic-accepts-wsl", None, "pass", "%s/captures/G2-T1-wsl.json" % EV),
    ("T2-genuine-elision-still-rejects", None, "pass", "%s/captures/G2-T2-windows.json" % EV),
    ("T3-markdown-records-read-windows", None, "pass", "%s/captures/G2-T3-windows.json" % EV),
    ("T3-markdown-records-read-wsl", None, "pass", "%s/captures/G2-T3-wsl.json" % EV),
    ("T4-invalid-embedded-record-rejected", None, "pass", "%s/captures/G2-T4-invalid.json" % EV),
    ("T4-non-record-stays-input-error", None, "pass", "%s/captures/G2-T4-notarecord.json" % EV),
    ("T5-selftest-windows", None, "pass", "%s/captures/G2-T5-windows.json" % EV),
    ("T5-selftest-wsl", None, "pass", "%s/captures/G2-T5-wsl.json" % EV),
    ("T6-corpus-digest-unmoved", None, "pass", "%s/captures/G2-T6-windows.json" % EV),
    ("T7-corpus-suite-windows", None, "pass", "%s/captures/G2-T7-windows.json" % EV),
    ("T7-corpus-suite-wsl", None, "pass", "%s/captures/G2-T7-wsl.json" % EV),
    ("T9-n2-revalidation-complete-windows", None, "pass", "%s/captures/G2-T9-windows.json" % EV),
    ("T9-n2-revalidation-complete-wsl", None, "pass", "%s/captures/G2-T9-wsl.json" % EV),
    ("T8-self-validation-point", None, "pass", "%s/captures/G2-T8-windows.json" % EV),
    ("review-five-items", None, "pass", "#review-record"),
]
for name, cmd, result, ref in CHECKS:
    w("  - name: %s" % name)
    if cmd:
        w("    command: %s" % yaml_str(cmd))
    w("    result: %s" % result)
    w("    output_ref: %s" % yaml_str(ref))
w("handoff_fingerprint:")
w("  active_branch_head: %s" % yaml_str(HEAD))
w("  tree_sha: %s" % yaml_str(TREE))
w("  changed_paths:")
for p in changed:
    w("    - %s" % p)
w("consults: []")
w("repair_attempts:")
w("  - number: 1")
w("    hypothesis: %s" % yaml_str(
    "F-1: the elision rule was broken at RENDER rather than at measurement - the "
    "row writer emitted a tail window and never a shown/total marker, so every "
    "row whose window was smaller than its capture elided silently."))
w("    result: green")
w("approvals:")
w('  - type: "Plan Approval (G1→G2)"')
w("    comment_url: %s" % yaml_str(APPROVAL))
w('    author: "MianliWang"')
w('    at: "2026-08-22T05:06:55Z"')
w("plan_hash: %s" % yaml_str(PLAN_HASH))
w("allowlist_hash: %s" % yaml_str(ALLOW_HASH))
w("evidence_files:")
w("  - %s/gate2.md" % EV)
w("notes: %s" % yaml_str(
    "Implementation of the frozen plan, then repair 1 under Review 1, then the "
    "re-review that closed it. This gate never graded itself: it exited "
    "needs_approval and stayed there until the Release Approval "
    "(issue 12 comment 5381788134) granted passed, and this amendment is that "
    "grant being executed, not the gate re-scoring its own work. Review 1 "
    "returned R1 pass, R2 pass, R3 FAIL on finding F-1, R4 pass, R5 pass. "
    "Repair 1 addressed F-1 and the same read-only window re-checked R3 alone "
    "and ruled it PASS on re-review; review-five-items is therefore recorded "
    "pass, the completed sequence's truthful final state, with the intermediate "
    "FAIL carried in the record rather than smoothed. Repair 1 addresses F-1 "
    "and nothing else: every row "
    "whose window is smaller than its capture now carries shown/total and the "
    "committed path of the full output, V3 and V6 keep the loader line friction "
    "#55 requires of a schema-validation row, and V8's window starts at S23 so "
    "Task A's positive-direction pair sits in the row a reader checks acceptance "
    "box 1 against. No measurement changed and no capture was rewritten - the "
    "repair is to how rows are rendered, and every restored line is read from the "
    "capture bytes. R3 was turned by Review 1's own re-review, in its own "
    "window, which is the only thing that could turn it; this record transcribes "
    "that ruling and does not substitute its own. The "
    "review's F-3, F-2 and F-4 are answered in the disclosures: an over-disclosed "
    "write withdrawn, and two frozen-plan counts corrected in the record rather "
    "than in the frozen text. Task C, the N2 re-validation, ran to completion on "
    "both declared "
    "platforms with identical results (V13, V14): every P2-S1 capture accepted "
    "and all four of its gate records READ, with the only surviving findings the "
    "historical records' own - gate0.json's #171-class command citations and "
    "gate3.md's elision - recorded and not repaired, as the grant requires. That "
    "discharges the remainder the P2-S2 closure left owed. The corpus digest is "
    "unmoved at f6128a0a53363162d967cb86e9ea91586455c7b5fb12d55b8a4825e5fe965686 "
    "and the digest's scope does not cover bin/, so this Slice's allowlist could "
    "not have moved it. No push, PR, tag or merge; publication is Gate 3."))
w("```")

data = ("\n".join(L) + "\n").encode("utf-8")
if b"\r" in data:
    print("CR byte in rendered record; refusing to write"); sys.exit(3)
open(OUT, "wb").write(data)
print(json.dumps({"written": OUT, "bytes": len(data),
                  "sha256": hashlib.sha256(data).hexdigest(),
                  "checks": len(CHECKS), "changed_paths": len(changed)}))
