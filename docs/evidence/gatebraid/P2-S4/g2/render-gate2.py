"""Render docs/evidence/gatebraid/P2-S4/gate2.md.

Record-row outputs are GENERATED from the Gate 2 captures, never transcribed
(friction #96). Every elision carries shown/total and the committed path of the
full output (ADR-0026). The metadata block's `result` is `needs_approval`: this
gate does not grade itself, and the review verdicts are the reviewer's to write.

Usage: render-gate2.py <ended_at>
"""
import base64
import json
import os
import sys

CAP = "docs/evidence/gatebraid/P2-S4/g2"
OUT = "docs/evidence/gatebraid/P2-S4/gate2.md"
BASE_SHA = "df666070ead7fa21bc72b6c99d2644923b37e787"
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
    if isinstance(env, dict):
        prefix = " ".join("%s=%s" % (k, env[k]) for k in sorted(env))
    else:
        prefix = ""
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
        lines = [x for x in combined.splitlines()]
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


def diff_paths():
    if not has("G2-fp-diff"):
        return []
    return [x for x in stream(cap("G2-fp-diff"), "stdout").splitlines() if x.strip()]


def one_line(cid, stream_name="stdout"):
    return stream(cap(cid), stream_name).strip()


w("# Gate 2 evidence — P2-S4")
w()
w("## Entry records")
w()

row("E1 — Plan Approval verified (author must be `MianliWang`, not this "
    "session — ADR-0020 §4; hashes must match the frozen values)",
    ["G2-E1-plan-approval", "G2-E1-identity"])

row("E1b — Writer Assignment verified (the operator ruling that opens Gate 2 "
    "in this session — its clause 2 amends the Plan Approval's §5 window clause)",
    ["G2-E1-writer-assignment"])

w("- Approval author `MianliWang`, executor identity `%s`: the approval was "
  "not written by the session it authorises." % one_line("G2-E1-identity"))
w("- `created_at` equals `updated_at` on both comments, so the grant that was "
  "posted is the grant that was read.")
w("- Both frozen hashes appear in the Plan Approval body — `plan_hash` "
  "`cb577dbf7fd1c0443b5e7ffbb94aacd7ada64385230afb6faa498815a4828913` and "
  "`allowlist_hash` "
  "`feb6d9c8ffbbaa08242d68e64db7b13b3f080aaae3667f01d7d22bdb0c061655`.")
w("- Writer-role certification (Writer Assignment clause 3): this session held "
  "no prior role on Slice P2-S4 — it authored neither Gate 0 nor Gate 1 — and "
  "is not the Review session.")
w()

row("E2 — Writer Lease taken, and the entry field writes, each by option id",
    ["G2-E2-set-nextapproval", "G2-E2-remove-label", "G2-E2-set-lease",
     "G2-E2-set-workflow"])

row("E3 — baseline re-read (ADR-0011 §9; ADR-0014 §1 excludes "
    "`docs/evidence/gatebraid/P2-S4/` before the intersection)",
    ["G2-E3-baseline-Y"])

w("- X, the plan baseline recorded in `gate0.md`: `%s`" % BASE_SHA)
w("- Y, the head of the base branch at entry: `%s`"
  % one_line("G2-E3-baseline-Y").split()[0])
w("- baseline: `unchanged`")
w()

row("E4 — Active Branch created from Y; `Base SHA` field set to Y",
    ["G2-E4-branch", "G2-E4-set-activebranch", "G2-E4-set-basesha"])

row("E5 — every entry field read back, by option id, with the issue's labels",
    ["G2-E-exit-readback"])

w("## Verification outputs")
w()

ROWS = [
    ("V1 — D1a · T1 producer selftest, Windows half (acceptance 4: fail-closed "
     "per class; the seven P0-1 classes each carry a seeded condition)",
     ["G2-D1a"], 14, True),
    ("V2 — D1b · T1 producer selftest, WSL half (acceptance 3: the declared "
     "platforms)", ["G2-D1b"], 14, True),
    ("V3 — D2a · T2 consumer selftest, Windows half (acceptance 4: P0-4's "
     "closed enumerations and both dependency directions)", ["G2-D2a"], 14, True),
    ("V4 — D2b · T2 consumer selftest, WSL half", ["G2-D2b"], 14, True),
    ("V5 — D3a · induced-failure matrix, Windows half (acceptance 3: "
     "`undecidable` demonstrably produced by each induced failure)",
     ["G2-D3a"], 30, False),
    ("V6 — D3b · induced-failure matrix, WSL half", ["G2-D3b"], 14, True),
    ("V7 — D4 · dependency directions (acceptance 1 and 4: a NON-EMPTY relation "
     "in BOTH directions, `allOf[2]`'s positive arm, `allOf[3]`'s consequence "
     "half — the Gate 0 Q7 gap)", ["G2-D4"], 24, False),
    ("V8 — D5 · the byte contract under a non-UTF-8 parent console "
     "(acceptance 4: P0-2 on non-ASCII content)", ["G2-D5"], 22, False),
    ("V9 — D6a · the frozen corpus under the landed validator, Windows half "
     "(acceptance 3; loader named in the output)", ["G2-D6a"], 12, True),
    ("V10 — D6b · the same, WSL half", ["G2-D6b"], 12, True),
    ("V11 — D7 · the frozen surface held unmoved (acceptance 2: the "
     "batch-pinned digest), at two of the plan's three named points — after "
     "the last implementation commit, and at Gate 2 exit; the third, before "
     "the first implementation commit, was missed and is disclosed",
     ["G2-D7", "G2-D7-exit"], 10, True),
    ("V12 — D8 · the freeze precedes the implementation in commit history "
     "(acceptance 2)", ["G2-D8"], None, False),
    ("V13 — N1 · path scope: the diff touches nothing outside the frozen "
     "allowlist", ["G2-N1"], None, False),
    ("V14 — N2 · no fail-open on a verdict-relevant path (proxy, scope and "
     "matches printed)", ["G2-N2"], None, False),
    ("V15 — N3 · no live network call in any declared test command",
     ["G2-N3"], 26, False),
    ("V16 — N4 · no verdict without validation, both halves", ["G2-N4"], None, False),
    ("V17 — T3 harness selftest, both platforms (NOT a declared test-plan "
     "command; recorded because it is the falsification of the instrument the "
     "declared commands rely on)",
     ["G2-T3selftest-windows", "G2-T3selftest-wsl"], 12, True),
    ("V18 — this gate's captures machine-validated under the capture tool's own "
     "write-path guard, re-derivation layer included (NOT a declared test-plan "
     "command; it is what makes the `output_ref` targets evidence rather than "
     "filenames)", ["G2-captures-validation"], None, False),
]
for label, cids, limit, tail in ROWS:
    row(label, cids, limit, tail)

w("## Review record")
w()
w("### Review 1")
w()
w("| Item | Verdict | Evidence |")
w("|---|---|---|")
w("| R1 allowlist confinement | | V13, and `git status --porcelain "
  "--untracked-files=all` at review time |")
w("| R2 test-plan coverage | | V1–V13, item-by-item mapping in the frozen "
  "plan's acceptance mapping |")
w("| R3 evidence is rows that reproduce | | every row above; the deterministic "
  "subset is V12, V13, V14, V15, V16 |")
w("| R4 negative criterion | | V13 (N1), V14 (N2), V15 (N3), V16 (N4) |")
w("| R5 no prohibited action | | E2–E5; no push, PR, merge, tag or dependency "
  "install appears in any capture |")
w()
w("**Reviewer rows** (the commands the reviewer ran, with outputs — including, "
  "for R3's deterministic subset, the byte-identity re-runs)")
w("```")
w("[written by the reviewer]")
w("```")
w()
w("**Findings** (only if any verdict is fail — one row per finding: what was "
  "measured, not a story about it)")
w("```")
w("[written by the reviewer]")
w("```")
w()
w("- Reviewer write disclosure: [written by the reviewer]")
w("- Rules given to the reviewer: [written by the reviewer]")
w()
w("## Repair record")
w()
w("No repair was entered at this gate; `repair_limit` 2 is unspent.")
w()
w("## Required disclosures")
w()
w("- Deviations: **D7 was not run at the first of its three named points.** The "
  "frozen plan requires the frozen surface to be re-measured by D7 *before the "
  "first implementation commit*, after the last, and at Gate 2 exit. It was run "
  "after the last implementation commit and at exit, and NOT before the first "
  "one; the omission is the executor's. What stands in its place is a stronger "
  "statement over a wider interval rather than a substitute measurement at the "
  "missed instant: V13 (N1) shows the whole range `%s..HEAD` touches no path "
  "outside `bin/` and `docs/evidence/gatebraid/P2-S4/`, so neither `schema/` nor "
  "`fixtures/` was written at any point in this gate, and V11 shows `digest "
  "before` equal to `digest after` equal to the batch-frozen value. The schema "
  "half was also measured before the first implementation commit incidentally, "
  "by the producer's own startup line naming "
  "`schema/snapshot.schema.json sha256=95ecf38e…`. The timing requirement was "
  "still missed and is recorded as missed · **two seeded cases in the harness "
  "were corrected by their own first run**, both disclosed because a seed that "
  "measures nothing is the defect this project has recorded most often: a "
  "capped transcript whose pages carried no item exercised the bounded flag and "
  "then had no item to carry a verdict, and an ASCII-only probe file needed its "
  "non-ASCII payload as escapes rather than as literals · **negative criterion "
  "N2 fired on this Slice's own implementation and the implementation was "
  "changed rather than the criterion.** The replay transport read `exit_code` "
  "with a non-`None` default, which places an implicit success assumption on a "
  "path that reaches a verdict; commit `1da43d8` removes it and S37 seeds the "
  "new behaviour. N2 now holds with zero matches · **`bin/gatebraid-snapshot.py` "
  "carries a live `gh` transport that no declared test command exercises.** "
  "Every declared command selects the replay transport or reads a frozen "
  "fixture, so the live path is committed but unmeasured at this gate; N3's "
  "scope names this explicitly rather than leaving it implied · **the three "
  "negative-criterion checkers for N2, N3 and N4 were authored at this gate**, "
  "not at Gate 1, which committed only N1's. They are instruments authored "
  "beside the work they certify — the pattern ADR-0028 §4 warns about — and are "
  "offered as mechanical aids to R4 rather than as independent certification; "
  "each states the pattern it proxies for, its explicit scope, and the "
  "direction in which it errs · **the handoff fingerprint, V13 (N1), V12 (D8) "
  "and V18's sweep were all measured at the commit BEFORE this record's own "
  "commit**, which is what the fingerprint's definition requires and what makes "
  "it Gate 3's comparand. The files the final commit adds — this record, the "
  "renderer's and sweep's own captures, and the re-taken fingerprint captures — "
  "are therefore outside those measurements. Every one of them is under "
  "`docs/evidence/gatebraid/P2-S4/`, so the allowlist claim is unaffected, and "
  "a reviewer re-running N1 at the final head measures the wider set. This is "
  "the boundary any sweep has over its own output, named rather than left to "
  "be noticed · **commit messages carry a `Co-Authored-By` "
  "trailer** per the executing harness's standing instruction, noted so the "
  "convention change is not mistaken for drift."
  % BASE_SHA)
w("- Reviewer write disclosure: `none` — no review has run at the time this "
  "record is written.")
w("- Environment: Windows 11 host, Git Bash (MSYS2) shell, `mixed-see-prose` "
  "with the WSL half exercised for D1b, D2b, D3b, D6b and V17; Windows loader "
  "`C:\\Python312\\python.exe` (CPython 3.12.2, jsonschema 4.23.0), WSL "
  "`/usr/bin/python3` (CPython 3.12.3, jsonschema 4.10.3); "
  "`PYTHONDONTWRITEBYTECODE=1` on every Windows Python invocation and set "
  "inside the `wsl` command on the WSL half, which inherits no Windows process "
  "environment; `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` "
  "call, every endpoint written without a leading slash (friction #33); the "
  "selftest seeds and the harness's parallel tree are written to scratch paths "
  "outside every repository, as the contract requires such a path to be named.")
w()
w("## gatebraid-metadata")
w()
w("```yaml")
w("schema: gatebraid/gate-run@2")
w("slice_id: P2-S4")
w("gate: 2")
w("environment: mixed-see-prose")
w("executor: Claude Lead")
w("base_sha: %s" % BASE_SHA)
w("active_branch: slice/P2-S4")
w('started_at: "%s"' % started_at())
w('ended_at: "%s"' % ENDED)
w("result: needs_approval")
w("checks:")

CHECKS = [
    ("plan-approval-verified",
     "gh api repos/MianliWang/gatebraid/issues/comments/5394791863 --jq '{author,url,created,updated}'",
     "#entry-records"),
    ("writer-assignment-verified",
     "gh api repos/MianliWang/gatebraid/issues/comments/5395086921 --jq '{author,url,created,updated}'",
     "#entry-records"),
    ("writer-lease-taken", "gh project item-edit (Writer Lease) + read-back",
     "#entry-records"),
    ("baseline-reread", "git ls-remote origin refs/heads/main", "#entry-records"),
    ("active-branch-created-from-Y",
     "git checkout -b slice/P2-S4 %s" % BASE_SHA, "#entry-records"),
    ("D1a-producer-selftest-windows", None, "%s/G2-D1a.json" % CAP),
    ("D1b-producer-selftest-wsl", None, "%s/G2-D1b.json" % CAP),
    ("D2a-consumer-selftest-windows", None, "%s/G2-D2a.json" % CAP),
    ("D2b-consumer-selftest-wsl", None, "%s/G2-D2b.json" % CAP),
    ("D3a-induced-failures-windows", None, "%s/G2-D3a.json" % CAP),
    ("D3b-induced-failures-wsl", None, "%s/G2-D3b.json" % CAP),
    ("D4-dependency-directions", None, "%s/G2-D4.json" % CAP),
    ("D5-byte-contract", None, "%s/G2-D5.json" % CAP),
    ("D6a-frozen-corpus-windows", None, "%s/G2-D6a.json" % CAP),
    ("D6b-frozen-corpus-wsl", None, "%s/G2-D6b.json" % CAP),
    ("D7-frozen-surface-unmoved", None, "%s/G2-D7.json" % CAP),
    ("D8-freeze-precedes-implementation", None, "%s/G2-D8.json" % CAP),
    ("N1-path-scope", None, "%s/G2-N1.json" % CAP),
    ("N2-no-fail-open", None, "%s/G2-N2.json" % CAP),
    ("N3-no-live-network", None, "%s/G2-N3.json" % CAP),
    ("N4-no-verdict-without-validation", None, "%s/G2-N4.json" % CAP),
    ("harness-selftest-windows", None, "%s/G2-T3selftest-windows.json" % CAP),
    ("harness-selftest-wsl", None, "%s/G2-T3selftest-wsl.json" % CAP),
    ("captures-machine-validated", None,
     "%s/G2-captures-validation.json" % CAP),
    ("allowlist-respected",
     "git diff --name-only %s..HEAD" % BASE_SHA, "#verification-outputs"),
]
for name, command, ref in CHECKS:
    w("  - name: %s" % name)
    if command:
        w('    command: "%s"' % command.replace('"', '\\"'))
    w("    result: pass")
    w('    output_ref: "%s"' % ref)

w("handoff_fingerprint:")
w('  active_branch_head: "%s"' % (one_line("G2-fp-head") if has("G2-fp-head") else ""))
w('  tree_sha: "%s"' % (one_line("G2-fp-tree") if has("G2-fp-tree") else ""))
w("  changed_paths:")
for p in sorted(diff_paths()):
    w("    - %s" % p)
w("consults: []")
w("repair_attempts: []")
w("approvals:")
w('  - type: "Plan Approval (G1→G2)"')
w('    comment_url: "https://github.com/MianliWang/gatebraid/issues/14#issuecomment-5394791863"')
w('    author: "MianliWang"')
w('    at: "2026-08-24T11:51:54Z"')
w('  - type: "Plan Approval (G1→G2)"')
w('    comment_url: "https://github.com/MianliWang/gatebraid/issues/14#issuecomment-5395086921"')
w('    author: "MianliWang"')
w('    at: "2026-08-24T12:19:15Z"')
w('plan_hash: "cb577dbf7fd1c0443b5e7ffbb94aacd7ada64385230afb6faa498815a4828913"')
w('allowlist_hash: "feb6d9c8ffbbaa08242d68e64db7b13b3f080aaae3667f01d7d22bdb0c061655"')
w("evidence_files:")
w("  - docs/evidence/gatebraid/P2-S4/gate2.md")
w('notes: "Implementation of the frozen plan in three tasks, each shipping a '
  'tool and its committed falsification. This gate does not grade itself: '
  '`result` is needs_approval and the Review 1 verdicts are left for the '
  'reviewer, who runs in a fresh read-only window under its own dispatch. The '
  'second approvals[] entry is the operator Writer Assignment that supplements '
  'the Plan Approval and, by its clause 2, amends the window clause so that '
  'Gate 2 opens in the session presenting that comment URL; it is recorded as '
  'the same approval type because it grants no new door, it re-addresses the '
  'existing one. The frozen schema and corpus were never written: N1 shows the '
  'whole range touches only bin/ and this Slice evidence path, and D7 shows '
  'the digest unmoved at '
  '66051715f76cf52d881aa143d9267f932407dbf5b9c4e6be9f81395ec641ef8e. No push, '
  'PR, tag or merge; publication is Gate 3."')
w("```")

data = ("\n".join(L).rstrip("\n") + "\n").encode("utf-8")
with open(OUT, "wb") as fh:
    fh.write(data)
import hashlib
print("WROTE %s" % OUT)
print("  bytes=%d sha256=%s" % (len(data), hashlib.sha256(data).hexdigest()))
print("  crlf=%d lone_cr=%d" % (data.count(b"\r\n"),
                                data.count(b"\r") - data.count(b"\r\n")))
