#!/usr/bin/env python3
"""Gate 2 record renderer — P2-S3.

Emits docs/evidence/gatebraid/P2-S3/gate2.md in the templates/gate2-evidence.md
shape, with every recorded output GENERATED from the pinned capture files rather
than transcribed (ADR-0026; friction #96).

The Review record's verdict column is left EMPTY: Review 1 has not run, and a
gate does not transcribe a verdict nobody reached. The `review-five-items` check
is recorded `not_run` for the same reason.

Usage: g2_render_record.py <captures-dir> <out-path> <ended_at>
"""
import sys, os, json, base64, hashlib

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


def row(w, label, cid, n):
    w("*%s*" % label)
    w("```")
    w("$ " + cmdline(cid))
    w(tail(cid, n))
    w("  exit=%d" % rc(cid))
    w("```")
    w("")


def yaml_str(s):
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"')


changed = [l for l in stream("G2-changed-paths").splitlines() if l.strip()]

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
for label, cid, n in [
    ("V1 — T1 Windows: the heuristic accepts what it wrongly rejected "
     "(acceptance box 1, positive direction)", "G2-T1-windows", 3),
    ("V2 — T1 WSL: the same, on the second declared platform", "G2-T1-wsl", 3),
    ("V3 — T2: a genuine elision still rejects (acceptance box 1, negative "
     "direction; negative criterion N2)", "G2-T2-windows", 14),
    ("V4 — T3 Windows: the markdown mode reads what it could not read "
     "(acceptance box 2)", "G2-T3-windows", 5),
    ("V5 — T3 WSL", "G2-T3-wsl", 5),
    ("V6 — T4 seed 1: an invalid embedded record is rejected, not merely read",
     "G2-T4-invalid", 5),
    ("V7 — T4 seed 2: a file that is not a record stays an input error "
     "(the pre-existing broken-input condition does not regress)",
     "G2-T4-notarecord", 2),
    ("V8 — T5 Windows: the selftest, carrying both repairs in both directions "
     "(acceptance box 4)", "G2-T5-windows", 12),
    ("V9 — T5 WSL", "G2-T5-wsl", 6),
    ("V10 — T6: the frozen corpus is unmoved (acceptance box 4; friction #165 "
     "budget case, 420,000 ms, measured 147,993 ms)", "G2-T6-windows", 7),
    ("V11 — T7 Windows: the corpus mutation suite still passes", "G2-T7-windows", 5),
    ("V12 — T7 WSL", "G2-T7-wsl", 5),
    ("V13 — T9 Windows — Task C: the N2 re-validation run to completion "
     "(acceptance boxes 2 and 3)", "G2-T9-windows", 14),
    ("V14 — T9 WSL: Task C on the second declared platform", "G2-T9-wsl", 14),
    ("V15 — T8: the self-validation point — the repaired validator over this "
     "Slice's own evidence, discharging the state packet §5 disclosed limit",
     "G2-T8-windows", 16),
]:
    row(w, label, cid, n)

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
w("| R1 allowlist confinement | | V16 and the `changed_paths` array; "
  "`git status --porcelain --untracked-files=all` at review time |")
w("| R2 test-plan coverage | | V1–V15, mapped item by item in the frozen plan's "
  "acceptance mapping |")
w("| R3 evidence is rows that reproduce | | every row above is a command and its "
  "generated output; the deterministic subset is V16 and the freeze hashes |")
w("| R4 negative criterion | | N1 at V16; N2 at V3; N3 by the module-level "
  "import scan of the two subject files |")
w("| R5 no prohibited action | | no push, PR, tag or merge; no dependency "
  "installed; no second writer; the lease at E2 |")
w("")
w("**The verdict column is deliberately empty.** Review 1 has not run: it is a")
w("fresh read-only window under its own dispatch, and a gate does not transcribe")
w("a verdict nobody reached. `checks[].review-five-items` is recorded `not_run`")
w("rather than `pass` for the same reason — `not_run` means the thing exists and")
w("was not executed, which is exactly the state.")
w("")
w("- Reviewer write disclosure: *(to be recorded by Review 1)*")
w("- Rules given to the reviewer: *(to be recorded by Review 1)*")
w("")
w("## Repair record")
w("")
w("No repair attempt was made. Every declared test command reached its frozen")
w("expected-green state on its first run, so the repair sequence was never")
w("entered and `repair_attempts` is empty. `repair_limit` remains 2, unspent.")
w("")
w("## Required disclosures")
w("")
w("- Deviations: **`bin/__pycache__/` was created and removed inside this gate.** "
  "The standing rule is `PYTHONDONTWRITEBYTECODE=1` on every Python invocation; "
  "it was set on every Windows invocation but does **not** cross into WSL, which "
  "inherits none of the Windows process environment, so the WSL halves of T1, T3, "
  "T5, T7 and T9 wrote bytecode for the two files they executed. Measured, not "
  "inferred: `wsl -e printenv PYTHONDONTWRITEBYTECODE` returns empty. The "
  "directory was removed before the first commit and no `.pyc` reached the index; "
  "it is disclosed here because a write created and removed inside a gate is "
  "invisible to the diff and R1 exists to catch exactly that (friction #107). "
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
  "drift.")
w("- Reviewer write disclosure: *(to be recorded by Review 1)*")
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
w("result: needs_approval")
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
    ("review-five-items", None, "not_run", "#review-record"),
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
w("repair_attempts: []")
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
    "Implementation of the frozen plan; no repair attempt was entered. "
    "result is needs_approval, never passed: passed is the Release Approval's to "
    "grant after Review 1, and this gate does not grade itself. The Review 1 "
    "verdict column is left empty and review-five-items is not_run for the same "
    "reason. Task C, the N2 re-validation, ran to completion on both declared "
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
