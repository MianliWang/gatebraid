"""Render docs/evidence/gatebraid/P2-S4/gate0.md from the captures.

Outputs are GENERATED from the capture records, never transcribed (friction
#96). Every elision prints shown/total plus the committed path of the full
output. The renderer writes the file and asserts nothing about it: the record
is machine-validated separately by bin/gatebraid-validate.py.
"""
import base64, json, os, sys

CAP = "docs/evidence/gatebraid/P2-S4/captures"
OUT = "docs/evidence/gatebraid/P2-S4/gate0.md"
STARTED = "2026-08-24T04:19:24Z"
ENDED = sys.argv[1]

DISCLOSURES = [
    "Deviations: the isolation scope changed between windows and is honoured prospectively. The O0 entry "
    "certification recorded that no special source bar applied to this Slice and that the four landed evidence "
    "tools were read-and-execute reference; the State Packet Approval section 3 ratifies a stricter bar, used "
    "never read. Under the earlier permission this window read part of bin/gatebraid-capture-selftest.py during "
    "the independent batch review of 2026-08-23, recorded in that review's section 8 and published as PR 15 "
    "comment 5388974846. No tool contents were read after the grant: the four are identified here by path, blob "
    "id and size via git ls-tree, and used by execution and --help only.",

    "Deviations: Q5's protocol sketch does not emit single-select option ids; the same read with --format json "
    "does. Both forms are recorded. Protocol state-packet-queries-v1 section 0 makes correcting a sketch against "
    "a measured API response verification rather than invention.",

    "Deviations: Q6 adds optionId to the SingleSelect fragment of the protocol sketch, so option ids are read "
    "rather than inferred from labels. Same clause as above.",

    "Deviations: the bare name claude is an extensionless npm shim and is not executable in argv form on this "
    "host; the .cmd wrapper is, and is the form the committed P2-S3 record used. Precedent followed.",

    "Deviations: A6's first attempt placed the capture tool's --form and --shell-exe flags after the argv "
    "separator, so they were consumed as the child's arguments and the read ran through a nested shell whose gh "
    "was unauthenticated. The capture recorded exit 4 and produced a zero-byte body file, on which the metadata "
    "checker errored rather than passing; both fail-closed behaviours fired as designed. The read was re-run in "
    "argv form with the body file written from the captured bytes and proved byte-equal to them. The failed "
    "attempt is retained at captures/G0-slice-body-failed-attempt.json with its checker run at "
    "captures/G0-slice-metadata-validation-on-empty.json.",

    "Deviations: the closed-set sweep's first pass returned 39 candidates under an incomplete rule set and is "
    "retained at captures/G0-closed-set-sweep-pass1.json with exit 1. The rule set was completed and two defects "
    "repaired: the sweep excludes its own reports, a self-reference of the IN-03 class, and reports residue by "
    "kind and location without echoing the token, per ADR-0028 section 3. Pass 1 is kept deliberately as this "
    "instrument's own falsification, since a sweep that has only ever returned empty has never been shown able "
    "to fire.",

    "Deviations: Q7 carries a measured gap. No non-empty dependency sample was taken, because the only "
    "known-related pair lives in the scratch repository, which the packet's closed set names but bars from any "
    "query. The nonexistent-issue seed shows the endpoint discriminates, 404 against 200 with an empty array, so "
    "the empty result is a read rather than a silent default. Reported as a gap per protocol "
    "state-packet-queries-v1 section 3, and not resolved by widening the closed set.",

    "Deviations: A3's predicate is evaluated over the baseline excluding this gate's own write domain. The "
    "unfiltered view is recorded beside it and shows zero entries outside that domain. The Gate 0 contract's "
    "Exit clause makes this gate's own evidence files not a violation.",

    "Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; shell Git Bash MINGW64 "
    "with Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh call "
    "pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every Python "
    "invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL half; Windows "
    "interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL "
    "/usr/bin/python3 with CPython 3.12.3, jsonschema 4.10.3. environment=mixed-see-prose: the gate ran on the "
    "Windows host and the WSL half is evidence.",
]

METADATA = """schema: gatebraid/gate-run@2
slice_id: P2-S4
gate: 0
environment: mixed-see-prose
executor: Claude Lead
base_sha: df666070ead7fa21bc72b6c99d2644923b37e787
started_at: "%s"
ended_at: "%s"
result: passed
approvals:
  - type: State Packet Approval
    author: MianliWang
    comment_url: "https://github.com/MianliWang/gatebraid/issues/14#issuecomment-5390640145"
    at: "2026-08-24T04:14:47Z"
checks:
  - name: repo-identity-and-remote
    command: "git remote -v"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-remote.json"
  - name: ref-namespace-enumerated
    command: "git for-each-ref"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-ref-namespace.json"
  - name: base-sha-recorded
    command: "git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-baseline-main.json"
  - name: working-tree-clean-at-base
    command: "git status --porcelain (baseline, excluding this gate's write domain); git rev-parse HEAD; git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-porcelain-baseline.json"
  - name: working-tree-unfiltered-audit
    command: "git status --porcelain --untracked-files=all"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-porcelain-full.json"
  - name: environment-matches-host
    command: "gh api graphql (Environment field read); python host probe"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-env-field.json"
  - name: tool-versions
    command: "claude.cmd --version; git --version; gh --version; codex --version; python version probe on both halves"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-tools-git.json"
  - name: slice-metadata-checker-falsified
    command: "validate-slice-metadata.py --schema schema/slice.schema.json --selftest"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-slice-metadata-selftest.json"
  - name: slice-metadata-parses
    command: "validate-slice-metadata.py --schema schema/slice.schema.json --body captures/slice-body-14.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-slice-metadata-validation.json"
  - name: packet-Q1-identity
    command: "gh api user --jq .login"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q1-identity.json"
  - name: packet-Q1-falsified
    command: "gh api user --jq .no_such_field; gh api user --jq .login against an empty store"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q1-falsify-badfield.json"
  - name: packet-Q2-approval-provenance
    command: "gh api repos/MianliWang/gatebraid/issues/comments/5390640145"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q2-approval.json"
  - name: packet-Q2-falsified
    command: "gh api repos/MianliWang/gatebraid/issues/comments/1"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q2-falsify.json"
  - name: packet-Q3-slice-issue
    command: "gh issue view 14 --repo MianliWang/gatebraid --json number,state,title,url"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q3-issue.json"
  - name: packet-Q3-falsified
    command: "gh issue view 999999 --repo MianliWang/gatebraid --json number,state,title,url"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q3-falsify.json"
  - name: packet-Q4-project
    command: "gh project view 1 --owner MianliWang"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q4-project.json"
  - name: packet-Q5-field-and-option-ids
    command: "gh project field-list 1 --owner MianliWang; the same read with --format json"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q5-field-list-json.json"
  - name: packet-Q5-falsified
    command: "gh project field-list 99 --owner MianliWang --format json"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q5-falsify.json"
  - name: packet-Q6-item-field-read
    command: "gh api graphql, protocol form with optionId, owner=MianliWang repo=gatebraid number=14"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q6-item-fields.json"
  - name: packet-Q6-falsified
    command: "the same form at number=999999; the same form with a field absent from the GraphQL schema; the project-selection step against a seeded wrong project id"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q6-falsify-selector.json"
  - name: packet-Q7-dependencies-both-directions
    command: "gh api repos/MianliWang/gatebraid/issues/14/dependencies/blocked_by ; gh api repos/MianliWang/gatebraid/issues/14/dependencies/blocking"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q7-blocked-by.json"
  - name: packet-Q7-falsified
    command: "gh api repos/MianliWang/gatebraid/issues/999999/dependencies/blocked_by"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q7-falsify.json"
  - name: capture-set-validated
    command: "C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/checks-g0-verify-captures.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-captures-validation.json"
  - name: closed-set-sweep
    command: "C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/checks-g0-closed-set-sweep.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-closed-set-sweep.json"
evidence_files:
  - docs/evidence/gatebraid/P2-S4/gate0.md
notes: "Startability read from the operator-approved closed-set state packet under its own State Packet Approval: the Gate 0 contract Entry's explicit third case, and the packet mechanism's final enumerated use. No bootstrap_exception, because N2 and N3 exist and this record carries full validation. The Base SHA Project field reads the setup-time value e5e8ee6b and is written at Gate 2 when Active Branch is cut under the lease, per contract Action 2."
""" % (STARTED, ENDED)

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


w("# Gate 0 evidence — P2-S4")
w()
w("## Records")
w()

row("A1 — repository identity and remote", ["G0-remote"])
row("A1 — ref namespace; any ref outside refs/heads/, refs/remotes/, refs/tags/ is reported, not adopted",
    ["G0-ref-namespace"], limit=17)
row("A2 — plan baseline: head of the base branch now (recorded here only; the Base SHA field is set at Gate 2 from the head re-read under lease — ADR-0011 §9)",
    ["G0-baseline-main"])
row("A3 — working tree clean AND at the base branch (one predicate, friction #84)",
    ["G0-porcelain-baseline", "G0-porcelain-outside-domain", "G0-head", "G0-baseline-main"])
row("A3 — unfiltered porcelain, so the baseline row's exclusion is auditable",
    ["G0-porcelain-full"], limit=8)
row("A4 — Project Environment field vs actual host", ["G0-env-field", "G0-host-probe"], limit=14)
row("A5 — tool versions",
    ["G0-tools-claude", "G0-tools-git", "G0-tools-gh", "G0-tools-codex",
     "G0-tools-python-windows", "G0-tools-python-wsl"])
row("A6 — slice metadata parses against gatebraid/slice@1",
    ["G0-slice-metadata-loader", "G0-slice-metadata-selftest", "G0-slice-metadata-validation"], limit=24)

w("### State-packet queries")
w()
row("Q1 — identity, run first and alone", ["G0-Q1-identity"])
row("Q1 — falsified: bad field name at exit 0, then unauthenticated store",
    ["G0-Q1-falsify-badfield", "G0-Q1-falsify-noauth"])
row("Q2 — State Packet Approval provenance", ["G0-Q2-approval"])
row("Q2 — falsified", ["G0-Q2-falsify"])
row("Q3 — the Slice issue", ["G0-Q3-issue"])
row("Q3 — falsified", ["G0-Q3-falsify"])
row("Q4 — the Project", ["G0-Q4-project"], limit=6)
row("Q5 — field and option ids, read fresh", ["G0-Q5-field-list"], limit=10)
row("Q5 — the same read with --format json, for the option ids", ["G0-Q5-field-list-json"], limit=6)
row("Q5 — falsified", ["G0-Q5-falsify"])
row("Q6 — per-item Project field read", ["G0-Q6-item-fields"], limit=6)
row("Q6 — falsified: nonexistent issue, bad GraphQL field, and the project-selection step",
    ["G0-Q6-falsify-noissue", "G0-Q6-falsify-badfield", "G0-Q6-falsify-selector"])
row("Q7 — dependencies, both directions", ["G0-Q7-blocked-by", "G0-Q7-blocking"])
row("Q7 — falsified", ["G0-Q7-falsify"])
row("Every capture verified with the capture tool's own write-path guard, re-derivation included",
    ["G0-captures-validation"], limit=6)
row("Closed-set sweep over every captured response", ["G0-closed-set-sweep"], limit=32)
row("Closed-set sweep, pass 1 — retained as the sweep's own falsification",
    ["G0-closed-set-sweep-pass1"], limit=4)

w("## Required disclosures")
w()
for d in DISCLOSURES:
    w("- " + d)
w()
w("## gatebraid-metadata")
w()
w("```yaml")
w(METADATA.rstrip())
w("```")

open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("WROTE %s" % OUT)
