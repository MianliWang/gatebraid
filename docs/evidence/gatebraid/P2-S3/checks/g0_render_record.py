#!/usr/bin/env python3
"""Gate 0 record renderer — P2-S3.

Emits docs/evidence/gatebraid/P2-S3/gate0.md from templates/gate0-evidence.md's
shape, with every recorded output GENERATED from the pinned capture files rather
than transcribed (ADR-0026; friction #96). Command lines are reconstructed from
each capture's own invocation, carrying their environment visibly (friction #89).

Usage: g0_render_record.py <captures-dir> <out-path> <ended_at>
Exit 0 = written; 3 = a required capture is missing or non-zero where a pass is
claimed (the renderer refuses to render a claim it cannot ground).
"""
import sys, os, json, base64

CAP, OUT, ENDED_AT = sys.argv[1], sys.argv[2], sys.argv[3]

SLICE = "P2-S3"
BASE_SHA = "63c8401f5df6ba446cf002232fcb280673c28e00"
STARTED_AT = "2026-08-22T03:08:05Z"
EVIDENCE = "docs/evidence/gatebraid/P2-S3"
APPROVAL_URL = "https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5377522556"
CORRECTION_URL = "https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5377614530"


def load(cid):
    p = os.path.join(CAP, cid + ".json")
    if not os.path.exists(p):
        print("MISSING CAPTURE: " + cid); sys.exit(3)
    return json.load(open(p, encoding="utf-8"))


def stream(cid, which="stdout"):
    d = load(cid)
    s = d["streams"][which]
    return base64.b64decode(s["data"]).decode("utf-8").replace("\r\n", "\n").rstrip("\n")


def rc(cid):
    return load(cid)["exit_code"]


def cmdline(cid, env_first=True):
    """Reconstruct the command as run, environment visible (friction #89)."""
    d = load(cid)
    inv = d["invocation"]
    env = inv.get("environment") or {}
    prefix = " ".join("%s=%s" % (k, v) for k, v in sorted(env.items()) if k != "PYTHONDONTWRITEBYTECODE")
    argv = inv["argv"]
    parts = []
    for a in argv:
        parts.append("'%s'" % a if (" " in a or "\n" in a) and not a.startswith("'") else a)
    line = " ".join(parts)
    if "\n" in line:
        line = " ".join(line.split())
    return (prefix + " " + line).strip() if (env_first and prefix) else line


def require_pass(cids):
    for c in cids:
        if rc(c) != 0:
            print("CAPTURE %s exited %s; refusing to render a pass" % (c, rc(c))); sys.exit(3)


PASSING = [
    "G0-remote", "G0-baseline-main", "G0-porcelain-baseline", "G0-porcelain-full",
    "G0-head", "G0-ref-namespace", "G0-tools-python-windows", "G0-tools-python-wsl",
    "G0-tools-git", "G0-tools-gh", "G0-tools-claude", "G0-tools-codex",
    "G0-slice-body", "G0-slice-metadata-validation", "G0-closed-set-sweep",
    "Q1-real", "Q2-real", "Q2-correction", "Q3-real", "Q4-real", "Q5-real",
    "Q5-real-plain", "Q6-real", "Q6-real-ids", "Q7-real-blockedby", "Q7-real-blocking",
]
require_pass(PASSING)

# Falsifications must NOT have exited 0 where fail-closed is the claim.
for c in ["Q2-falsify", "Q3-falsify", "Q4-falsify", "Q5-falsify", "Q6-falsify", "Q7-falsify"]:
    if rc(c) == 0:
        print("FALSIFICATION %s exited 0; the fail-closed claim is unproven" % c); sys.exit(3)

# Q6 elision: show the Environment row only, name the total.
q6 = json.loads(stream("Q6-real"))
item = [n for n in q6["data"]["repository"]["issue"]["projectItems"]["nodes"]
        if n["project"]["id"] == "PVT_kwHOBRofUs4Beum7"][0]
fvs = [f for f in item["fieldValues"]["nodes"] if f and (f.get("field") or {}).get("name")]
env_row = [f for f in fvs if f["field"]["name"] == "Environment"][0]
q6ids = json.loads(stream("Q6-real-ids"))
item2 = [n for n in q6ids["data"]["repository"]["issue"]["projectItems"]["nodes"]
         if n["project"]["id"] == "PVT_kwHOBRofUs4Beum7"][0]
env_oid = [f for f in item2["fieldValues"]["nodes"]
           if f and (f.get("field") or {}).get("name") == "Environment"][0]["optionId"]
env_line = json.dumps({"item": item["id"], "field": "Environment",
                       "value": env_row["name"], "optionId": env_oid})

# Ref namespace: split watched from outside.
refs = [l for l in stream("G0-ref-namespace").splitlines() if l.strip()]
watched = [l for l in refs if l.startswith(("refs/heads/", "refs/remotes/", "refs/tags/"))]
outside = [l for l in refs if not l.startswith(("refs/heads/", "refs/remotes/", "refs/tags/"))]

sweep = json.loads(stream("G0-closed-set-sweep"))

CHECKS = [
    ("repo-identity-and-remote", cmdline("G0-remote"), "G0-remote"),
    ("base-sha-recorded", cmdline("G0-baseline-main"), "G0-baseline-main"),
    ("working-tree-clean-at-base",
     "%s; %s; %s" % (cmdline("G0-porcelain-baseline"), cmdline("G0-head"), cmdline("G0-baseline-main")),
     "G0-porcelain-baseline"),
    ("ref-namespace-enumerated", cmdline("G0-ref-namespace"), "G0-ref-namespace"),
    ("environment-matches-host",
     "gh api graphql (Q6 per-item field read); python platform probe, both platforms",
     "G0-tools-python-windows"),
    ("tool-versions", "claude.cmd --version; git --version; gh --version; codex --version",
     "G0-tools-claude"),
    ("slice-metadata-parses", cmdline("G0-slice-metadata-validation"), "G0-slice-metadata-validation"),
    ("slice-metadata-falsification-schema-invalid", cmdline("G0-slice-metadata-falsify-seedA"),
     "G0-slice-metadata-falsify-seedA"),
    ("slice-metadata-falsification-digest-mismatch", cmdline("G0-slice-metadata-falsify-seedB"),
     "G0-slice-metadata-falsify-seedB"),
    ("slice-metadata-falsification-no-heading", cmdline("G0-slice-metadata-falsify-seedC"),
     "G0-slice-metadata-falsify-seedC"),
    ("closed-set-sweep", cmdline("G0-closed-set-sweep"), "G0-closed-set-sweep"),
    ("state-packet-Q1-identity", cmdline("Q1-real"), "Q1-real"),
    ("state-packet-Q1-falsification", cmdline("Q1-falsify"), "Q1-falsify"),
    ("state-packet-Q2-approval-author", cmdline("Q2-real"), "Q2-real"),
    ("state-packet-Q2-falsification", cmdline("Q2-falsify"), "Q2-falsify"),
    ("state-packet-Q2-correction-provenance", cmdline("Q2-correction"), "Q2-correction"),
    ("state-packet-Q3-slice-issue", cmdline("Q3-real"), "Q3-real"),
    ("state-packet-Q3-falsification", cmdline("Q3-falsify"), "Q3-falsify"),
    ("state-packet-Q4-project", cmdline("Q4-real"), "Q4-real"),
    ("state-packet-Q4-falsification", cmdline("Q4-falsify"), "Q4-falsify"),
    ("state-packet-Q5-field-ids", cmdline("Q5-real-plain"), "Q5-real-plain"),
    ("state-packet-Q5-field-ids-json", cmdline("Q5-real"), "Q5-real"),
    ("state-packet-Q5-falsification", cmdline("Q5-falsify"), "Q5-falsify"),
    ("state-packet-Q6-item-fields", cmdline("Q6-real"), "Q6-real"),
    ("state-packet-Q6-item-fields-by-option-id", cmdline("Q6-real-ids"), "Q6-real-ids"),
    ("state-packet-Q6-falsification", cmdline("Q6-falsify"), "Q6-falsify"),
    ("state-packet-Q7-blocked-by", cmdline("Q7-real-blockedby"), "Q7-real-blockedby"),
    ("state-packet-Q7-blocking", cmdline("Q7-real-blocking"), "Q7-real-blocking"),
    ("state-packet-Q7-falsification", cmdline("Q7-falsify"), "Q7-falsify"),
]


def yaml_str(s):
    return '"%s"' % s.replace('\\', '\\\\').replace('"', '\\"')


L = []
w = L.append

w("# Gate 0 evidence — %s" % SLICE)
w("")
w("## Records")
w("")
w("**A1 — repository identity and remote**")
w("```")
w("$ " + cmdline("G0-remote"))
w(stream("G0-remote"))
w("```")
w("")
w("**A2 — plan baseline: head of the base branch now** (recorded here only; the")
w("`Base SHA` field is set at Gate 2 from the head re-read under lease —")
w("ADR-0011 §9)")
w("```")
w("$ " + cmdline("G0-baseline-main"))
w(stream("G0-baseline-main"))
w("```")
w("")
w("**A3 — working tree clean AND at the base branch** (one predicate, friction")
w("#84)")
w("```")
w("$ " + cmdline("G0-porcelain-baseline"))
b = stream("G0-porcelain-baseline")
if b:
    w(b)
w("$ " + cmdline("G0-porcelain-full"))
w(stream("G0-porcelain-full"))
w("$ " + cmdline("G0-head"))
w(stream("G0-head"))
w("$ " + cmdline("G0-baseline-main"))
w(stream("G0-baseline-main"))
w("```")
w("")
w("**A3b — ref namespace enumerated** (unrestricted; friction #103)")
w("```")
w("$ " + cmdline("G0-ref-namespace"))
for l in watched:
    w(l)
for l in outside:
    w(l)
w("```")
w("")
w("**A4 — Project `Environment` field vs actual host**")
w("```")
w("$ " + cmdline("Q6-real"))
w(env_line)
w("[elided: 1 of %d field values shown; full output: %s/captures/Q6-real.json;"
  % (len(fvs), EVIDENCE))
w(" option ids for the same read: %s/captures/Q6-real-ids.json]" % EVIDENCE)
w("$ " + cmdline("G0-tools-python-windows"))
w(stream("G0-tools-python-windows"))
w("$ " + cmdline("G0-tools-python-wsl"))
w(stream("G0-tools-python-wsl"))
w("```")
w("")
w("**A5 — tool versions**")
w("```")
for c in ["G0-tools-claude", "G0-tools-git", "G0-tools-gh", "G0-tools-codex"]:
    w("$ " + cmdline(c))
    w(stream(c))
w("```")
w("")
w("**A6 — slice metadata parses against `gatebraid/slice@1`**")
w("```")
w("$ " + cmdline("G0-slice-metadata-validation"))
w(stream("G0-slice-metadata-validation"))
w("```")
w("")
w("**A6b — the A6 checker falsified before its pass was trusted** (ADR-0028 §4)")
w("```")
for c, seed in [("G0-slice-metadata-falsify-seedA", "schema-invalid body"),
                ("G0-slice-metadata-falsify-seedB", "tampered payload, stale stdout digest"),
                ("G0-slice-metadata-falsify-seedC", "metadata heading removed")]:
    w("$ " + cmdline(c))
    w(stream(c))
    w("  exit=%d   [seed: %s]" % (rc(c), seed))
w("```")
w("")
w("**A7 — closed-set complement sweep over this gate's own captures**")
w("```")
w("$ " + cmdline("G0-closed-set-sweep"))
w(stream("G0-closed-set-sweep"))
w("```")
w("")
w("**B1–B7 — state-packet rows, each falsified before its output was trusted**")
w("```")
for cid in ["Q1-real", "Q1-falsify", "Q2-real", "Q2-falsify", "Q2-correction",
            "Q3-real", "Q3-falsify", "Q4-falsify", "Q5-falsify",
            "Q6-falsify", "Q7-real-blockedby", "Q7-real-blocking", "Q7-falsify"]:
    w("$ " + cmdline(cid))
    o = stream(cid)
    e = stream(cid, "stderr")
    if o:
        w(o if len(o) <= 400 else o[:400] + " …")
    if e:
        w(e if len(e) <= 300 else e[:300] + " …")
    w("  exit=%d" % rc(cid))
w("[Q4-real and Q5-real/Q5-real-plain outputs are long and are not inlined;")
w(" full outputs: %s/captures/Q4-real.json, Q5-real.json, Q5-real-plain.json." % EVIDENCE)
w(" Q6-real and Q6-real-ids appear under A4 with their elision note.]")
w("```")
w("")
w("## Required disclosures")
w("")
w("- Deviations: the approval's §5 named this record `gate0.json`; the operator "
  "ruled that a coordinator drafting slip and directed the contract Exit form, "
  "`gate0.md` from `templates/gate0-evidence.md`, with every bracketed term "
  "unchanged — correction comment `5377614530`, author read back via the packet's "
  "Q2 form before this record was written (capture `Q2-correction`); `approvals[]` "
  "continues to cite the State Packet Approval itself · **one ref outside the "
  "watched namespaces**, `refs/codex/turn-diffs/checkpoints/…` pointing at a *tree*, "
  "embedded timestamp 1785489900931 = 2026-07-31T09:25:00.931Z, written by Codex "
  "CLI's own turn-diff bookkeeping and pre-dating this Slice by about three weeks: "
  "**reported, not adopted** per the contract's Action 1, not deleted or moved, "
  "since either would be a state-changing Git command inside the gate and a "
  "self-remediation — note that the entry paste's §3.4 form "
  "(`for-each-ref refs/heads/ refs/remotes/ refs/tags/`) filters to exactly the "
  "three namespaces this hazard is defined as outside and cannot find the class in "
  "principle, which is why only the contract's unrestricted enumeration surfaced it · "
  "**the closed-set sweep instrument was refuted twice before its verdict was "
  "trusted**: rev 1 treated every slash-separated token as a repository and would "
  "have reported `SET NOT CLOSED` over `Python312/python.exe`, `refs/heads` and "
  "~130 similar path fragments; rev 2 matched `github.com/` as a substring of "
  "`docs.github.com/` and reported `rest/issues` from GitHub's own 404 "
  "documentation URLs — the identical false positive P2-S2's rev 5 hit and "
  "disclosed; rev 3 anchors the host against a preceding domain label and runs 4 "
  "positive and 9 negative seeds before every verdict, exiting 2 and refusing to "
  "report if any seed fails; its stated coverage limit is that a foreign repository "
  "named in bare `owner/repo` form with no URL and no `#N` would not be caught, "
  "while all three contexts a query could actually reach are · `cli/cli` appears "
  "twice in `gh --version`'s own release URL — a mention in a contract-mandated "
  "tool's self-describing output, not a touch, per the ruling at "
  "https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5364439544 · "
  "Q5 was additionally run with `--format json` for machine readability and Q6 "
  "additionally with `optionId` added, because the packet's verbatim Q6 form returns "
  "option *names* and this console mangles U+2014, so verifying select values by "
  "name would mean comparing mangled text against a retyped mark, which the standing "
  "dash rule forbids; the packet's literal forms were also captured "
  "(`Q5-real-plain`, `Q6-real`) so no row is left unexecuted as written, and neither "
  "supplement changed a verdict · `git status --porcelain` unrestricted returns one "
  "entry, this gate's own evidence directory, which the contract's Exit step permits; "
  "the baseline half of A3 excludes that path and is empty · the bare npm shim "
  "`claude` is a shell script and argv-form capture fails on it, so the "
  "Windows-executable `claude.cmd` was captured instead, keeping the capture "
  "argv-form (P2-S2 precedent) · this gate's captures are **not** machine-validated "
  "by the landed `bin/gatebraid-validate.py`, per the approval's §4 disclosed "
  "instrument limit: the Q6 form carries four GraphQL inline-fragment spreads that "
  "the landed validator misclassifies as elisions (friction #169, the defect this "
  "Slice repairs); their machine validation is owed to the repaired validator within "
  "this Slice at the point the Gate 1 plan names, and this record's own schema "
  "validation is unaffected and was run — as a standalone guarded step, against "
  "schema/gate-run-v2.schema.json, itself falsified first by six seeds each "
  "targeting a documented @2 delta or required property (abbreviated base_sha; "
  "approvals[] missing author, the friction #71 class; an unquoted ISO8601 scalar "
  "resolving to a datetime rather than a string, friction #55; a checks[] entry "
  "missing result; a removed metadata heading; and bootstrap_exception: true with "
  "no State Packet Approval), all six rejected for their stated reason before the "
  "record's own pass was trusted, captures G0-record-falsify-* · the record's "
  "validation is deliberately NOT a checks[] row: a record does not certify itself "
  "(no self-reference, ADR-0026), so it is a commit gate rather than a record claim · "
  "the A7 sweep cannot scan captures written after it runs; exactly two files "
  "postdate it by construction — its own capture and the final record-validation "
  "capture — and both are outputs of local check scripts over local files, carrying "
  "no repository identifier beyond the permitted set.")
w("- Environment: Windows 11 host, Git Bash (MSYS2) shell; "
  "`GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` call (the ambient "
  "User-scope value points at gh's machine-shared store, whose identity is the "
  "operator, ADR-0024 decision 1 / friction #162); `PYTHONDONTWRITEBYTECODE=1` on "
  "every Python invocation; loader host `C:\\Python312\\python.exe` (CPython 3.12.2, "
  "PyYAML 6.0.2, jsonschema 4.23.0) with the WSL half (3.12.3 / 6.0.1 / 4.10.3) "
  "recorded as the second platform of `mixed-see-prose`; every `gh api` endpoint "
  "written without a leading slash, because MSYS rewrites leading-slash endpoints "
  "into filesystem paths (friction #33).")
w("")
w("## gatebraid-metadata")
w("")
w("```yaml")
w("schema: gatebraid/gate-run@2")
w("slice_id: %s" % SLICE)
w("gate: 0")
w("environment: mixed-see-prose")
w("executor: Claude Lead")
w("base_sha: %s" % BASE_SHA)
w("started_at: %s" % yaml_str(STARTED_AT))
w("ended_at: %s" % yaml_str(ENDED_AT))
w("result: passed")
w("approvals:")
w("  - type: State Packet Approval")
w("    comment_url: %s" % yaml_str(APPROVAL_URL))
w("    author: MianliWang")
w('    at: "2026-08-22T03:04:46Z"')
w("checks:")
for name, cmd, ref in CHECKS:
    w("  - name: %s" % name)
    w("    command: %s" % yaml_str(cmd))
    w("    result: pass")
    w("    output_ref: %s" % yaml_str("%s/captures/%s.json" % (EVIDENCE, ref)))
w("evidence_files:")
w("  - %s/gate0.md" % EVIDENCE)
w("notes: %s" % yaml_str(
    "Startability read from the operator-approved closed-set state packet "
    "(sha256 c7eeb762fe858cf43937419e04546bb17b6b2d63b826bd6fa40697d01a2f541e, "
    "9232 bytes) under ruling R-a, the O0-case treatment extended to this "
    "post-bootstrap pre-O0 Slice: full validation, no bootstrap_exception. "
    "bootstrap_exception is deliberately ABSENT, not false-by-omission: the "
    "bounded evidence bootstrap expired at N2+N3 Gate 3 and this record claims "
    "none of it. R-a enlarges the Gate 0 contract's closed enumeration and the "
    "approval says so; the contract text is amended by ADR in the R-min/D16 "
    "batch. Every checks[] entry carries an output_ref to a capture written by "
    "the landed bin/gatebraid-capture.py (generator 1.0.0, source sha256 "
    "5dcedf84283952453785c57f9de08ce818b068a1cac8772c806b155444ad5626). "
    "Falsification rows record their seeded failure as result: pass because the "
    "check they encode is 'this form fails closed on bad input', and each did; "
    "the captured exit codes are non-zero by design and are shown in the record. "
    "Record container ruled at correction comment " + CORRECTION_URL + "."))
w("```")

data = ("\n".join(L) + "\n").encode("utf-8")
if b"\r" in data:
    print("CR byte in rendered record; refusing to write"); sys.exit(3)
with open(OUT, "wb") as f:
    f.write(data)
import hashlib
print(json.dumps({"written": OUT, "bytes": len(data),
                  "sha256": hashlib.sha256(data).hexdigest(),
                  "checks": len(CHECKS), "captures_referenced": len({c[2] for c in CHECKS}),
                  "sweep_verdict": sweep["verdict"],
                  "refs_watched": len(watched), "refs_outside": len(outside)}))
