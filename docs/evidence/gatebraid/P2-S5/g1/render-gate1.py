"""Render docs/evidence/gatebraid/P2-S5/g1/gate1.md from the plan and the captures.

The record lands under g1/ and not beside the retained gate0.md, because Ruling 2
of the Gate 0 opening comment gives this Slice a per-gate layout: the retained
record of the accepted stop keeps the top level, the Gate 0 re-run has g0r/, and
this gate has g1/. Writing the record at the top level would ADD a file to the
retained set and move its path-list digest, which is measured rather than
assumed - negative criterion N3's content limb is exactly that measurement.

Record-row outputs are GENERATED from the capture records, never transcribed
(friction #96) - the second of the three findings the M2 measurement chain
produced, and the one this Slice's own record must not repeat. The frozen plan
is the ONE prose class (ADR-0026 section 1) and is read verbatim from
docs/evidence/gatebraid/P2-S5/g1/plan.md; the heading `## Plan (frozen at exit)`
is load-bearing byte-for-byte because plan_hash covers the lines strictly
between it and the next line beginning with `## `.

Usage: render-gate1.py <ended_at> <plan_hash> <allowlist_hash>
Pass PENDING for either hash on the first pass; compute the hashes from the
rendered file, then re-render with them. The plan section is identical on both
passes, so plan_hash is stable across the re-render - which P5 then verifies by
recomputing it from the final file.
"""
import base64, json, os, sys

G = "docs/evidence/gatebraid/P2-S5/g1"
CAPS = os.path.join(G, "captures")
OUT = "docs/evidence/gatebraid/P2-S5/g1/gate1.md"
STARTED = "2026-09-01T21:39:25Z"
ENDED, PLAN_HASH, ALLOWLIST_HASH = sys.argv[1], sys.argv[2], sys.argv[3]

L = []


def w(s=""):
    L.append(s)


def cap(cid):
    return json.load(open(os.path.join(CAPS, cid + ".json"), encoding="utf-8"))


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


def row(label, cids, limit=None, head=None):
    w("**%s**" % label)
    w("```")
    for cid in cids:
        if not os.path.isfile(os.path.join(CAPS, cid + ".json")):
            # First pass only: this row's capture is produced BY running a
            # command against the rendered file, so it cannot exist before the
            # first render. The second render carries it.
            w("PENDING FIRST RENDER: %s" % cid)
            continue
        d = cap(cid)
        w("$ " + argv_line(d))
        text = stream_text(d, "stdout")
        err = stream_text(d, "stderr")
        combined = text + (("\n" + err) if err.strip() else "")
        lines = combined.splitlines()
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


DISCLOSURES = [
    "Deviations: no read-only Agent Team was used, and the decision is recorded here rather than left "
    "implicit. gate-1-contract action 2 makes the team OPTIONAL. Two reasons, and the second is the "
    "decisive one. First, the question this gate had to answer - what the frozen scope IS - is answered by "
    "reading seven named documents at one named commit and hashing them, which a teammate could not do more "
    "reliably than the pin instrument does. Second, action 2 requires all findings to be FLUSHED TO THE "
    "SLICE ISSUE before the team dissolves, and that flush is a control-plane mutation this window has no "
    "approval for: the operator's release of this gate sanctions the handoff comment, the write_domains "
    "post-condition and the four field writes, and nothing else. Spawning a team would have forced either "
    "an unapproved mutation or a violated constraint. Consequently there are NO team findings to flush, and "
    "failure-disposition row 2 is vacuously satisfied rather than exercised.",

    "Deviations: action 4's dry-run of a not-yet-written deliverable is recorded honestly and in three "
    "classes, not two. SIX declared commands ran to their full green criterion today: D0, D0F, D1, D2, D10 "
    "and the D9 path limbs. FIVE - D3, D4, D5, D6, D7, D8 and D11 - name `bin/gatebraid-ready.py` or "
    "`bin/gatebraid-ready-selftest.py`, which Gate 1 is forbidden to create, and each was RUN AS DECLARED on "
    "the declared platform and produced an interpreter error naming exactly the absent file and nothing else "
    "wrong. That establishes what action 4 exists to establish - the command reaches the interpreter on THAT "
    "host, rather than being well-formed on inspection - and no more. The third class is the one that makes "
    "the difference: for every such command a COMPANION PROBE ran the same boundary against the real tools, "
    "so the parts other than the program under test are measured and not assumed.",

    "Deviations: the dry-run CHANGED THE PLAN, twice, before the freeze, which is the whole purpose of the "
    "requirement. D6 was declared as `--project 999` on the reasoning that a bad project number is a "
    "producer failure. Run against the real producer it returns EXIT 3 WITH A DEGRADED DOCUMENT, not a "
    "no-document failure - the O0-hardened producer fails closed and reports degradation rather than "
    "crashing. That is delta D-4, it was not foreseen, and it changes the composer's central rule from `the "
    "producer exited non-zero` to `the producer's status says whether a document exists`. D6 now names an "
    "input error that genuinely produces none. Separately, D11's expected-green criterion was written as "
    "`platform.os reads linux`; the capture tool running on WSL stamps `wsl`, so the criterion as first "
    "written would have failed a correct run. Both corrections are in the frozen plan, and both were found "
    "by running rather than by reading.",

    "Deviations: a landed tool defect was found by running a declared command as written, and this Slice "
    "does not repair it. `bin/gatebraid-validate.py --record <absent path>` raises an uncaught "
    "FileNotFoundError from validate_document rather than reporting a typed usage error, so a caller reading "
    "the exit status sees 1 - the same status a REJECTED record produces - with a traceback instead of a "
    "finding. It is recorded here as a queued defect: the validator is one of the five landed pairs this "
    "Slice's Non-goals put out of scope, and repairing it here would be the widening that ADR-0032's lane "
    "structure exists to prevent. One Slice, one tool.",

    "Deviations: the closed-set sweep over this gate's captures reports UNEXPLAINED RESIDUE and the "
    "instrument was NOT edited to clear its own finding. The hard rule the sweep enforces is SATISFIED and "
    "shown: exactly two repository identities are named anywhere in the domain, `MianliWang/gatebraid` and "
    "`MianliWang/gatebraid-scratch`, both PERMITTED, nothing outside the set, and no mention-class issue is "
    "targeted by any query. What is unresolved is the sweep's ability to EXPLAIN every candidate token by "
    "rule, and every residue token was identified with its source before anything was done. Exactly one was "
    "this window's own prose - a slash joining two field names in a capture note - and it was removed AT "
    "SOURCE by rewording, with the superseded read retained beside it. Every other residue is text this gate "
    "cannot alter and must not: JSON Schema pointer segments printed by the corpus runner and the validator "
    "whose leading segment is not `properties`; two ratios, a relative path and a slashed word pair inside "
    "the `Last Checkpoint` value the CLOSED Gate 0 exit wrote; an issue-shaped friction citation inside a "
    "frozen corpus case label; a Windows path split at its space; and a newline rendered by a Python bytes "
    "repr immediately before a path. Four of those classes are already named with stated reasons in the "
    "MERGED P2-S6 Gate 1 copy; the rest are new and no committed copy names them. Adding them is a domain "
    "fact this window will not make on its own authority, exactly as the Gate 0 re-run stopped rather than "
    "extend this same instrument, and the ruling is requested in the exit report. The sweep is typed `fail` "
    "here and is not one of the contract's Actions 1 through 6.",

    "Deviations: the sweep was falsified before any weight was put on it. The SAME instrument, pointed at "
    "the two retained seeds, fired on the repository, node and issue limbs at exit 1, and left BOTH "
    "out-of-namespace item ids as residue including the near-miss that differs from the permitted namespace "
    "by a single character. A sweep that has only ever returned empty has measured nothing.",

    "Deviations: the contract's Entry condition `Gate = G0 passed` CANNOT be established from the O0 outputs "
    "alone, and that gap is recorded rather than papered over. The snapshot document carries `workflow` for "
    "every item and no `Gate` field at all, so the Slice's acceptance clause `control-plane state read "
    "exclusively through O0 outputs` does not reach the field this gate's Entry turns on. Every dependency, "
    "verdict and workflow reading in this record comes from the snapshot and the frontier; the `Gate`, "
    "`Next Approval` and `Last Checkpoint` readings come from the same by-key node read the Gate 0 Exit used "
    "for its own read-backs, captured, and resolved by option id rather than by typing a label through this "
    "host's console. The gap is a finding about the acceptance clause, not a licence to query freely.",

    "Deviations: the frozen corpus holds SEVEN of the eight catalogued historical ready-failure classes, not "
    "eight, and the Slice's Acceptance is read against what the corpus actually contains. BP-01, BP-02, "
    "BP-03, IN-02, IN-03, IN-04 and IN-05 are each shown killed at D2 by the runner's own summary rows "
    "naming the locus. IN-01, the pipeline exit code, is DELIBERATELY ABSENT from the corpus by that "
    "corpus's own declared known_limitation, so it cannot be shown killed from the corpus and this record "
    "does not claim it is. It is carried instead as a declared selftest condition of the deliverable, and "
    "its shape was exercised at this gate by the D8 companion probe, which ran the composition under a shell "
    "with pipefail declared and the exit-code source named.",

    "Deviations: the D5 row's declared command writes into the Gate 2 captures directory, and creating a "
    "Gate 2 directory at Gate 1 would assert a gate that has not opened. The dry-run substituted the output "
    "directory only; interpreter, flags, repository-relative path form and allowlist prefix are identical, "
    "and both paths lie under `docs/evidence/gatebraid/P2-S5/`, which N1 covers. Its `--input` list was also "
    "reduced to the tools that exist, because the capture tool hashes declared inputs BEFORE running and "
    "would otherwise refuse on the absent deliverable - which is the outcome the row reports anyway.",

    "Deviations: one Gate 1 instrument writes nothing and is not the deliverable, and is named so it is not "
    "mistaken for one. `docs/evidence/gatebraid/P2-S5/g1/probe-producer-boundary.py` has no command line, "
    "composes nothing with the consumer and implements no exit algebra; it crosses the T1 boundary three "
    "times against real producers and reports what each crossing produced. It exists because action 4 asks "
    "whether the declared commands run HERE, and Slice A's frozen plan is the case where that question was "
    "answered by reading and the answer was wrong.",

    "Deviations: three Gate 1 instruments were copied from earlier evidence and re-parameterised to this "
    "Slice's constants only. `hash-plan.py` is BYTE-IDENTICAL to the P2-S4 and P2-S6 file, sha256 "
    "17649cdb5535f4cc09e114ca135e23750aabfa35b69de1d8cd0263d690ed0ada, because it takes its target as an "
    "argument and needed no change. `plan-path-scan.py` and `writedomains-check.py` differ only in this "
    "Slice's allowlist, its read-only input set, its excluded lanes and the issue read. "
    "`checks-g1-closed-set-sweep.py` is a copy of the Gate 0 re-run instrument, sha256 "
    "d2b501555a223e5d69720fed3cf8640e56233d2f4d81549a87ca02788ad3bff1, differing in three DOMAIN FACTS - the "
    "captures directory, the self-exclusion prefix, and four mention-class issue numbers the historical "
    "record necessarily names - and in no rule, regex or residue criterion. A closed gate's instruments are "
    "not editable by a later gate, and the Gate 0 copies were not touched.",

    "Deviations: this record was FIRST WRITTEN TO THE WRONG PATH and the correction is recorded rather than "
    "quietly folded in, because the mistake is exactly the one negative criterion N3's content limb exists "
    "to catch. The contract's Exit names `docs/evidence/gatebraid/<slice_id>/gate1.md`, and the first two "
    "render passes took it literally and wrote `docs/evidence/gatebraid/P2-S5/gate1.md` - beside the "
    "retained gate0.md, at the top level. Ruling 2 of the Gate 0 opening comment gives this Slice a per-gate "
    "layout instead, and the operator's release of this gate names "
    "`docs/evidence/gatebraid/P2-S5/g1/gate1.md` explicitly. The consequence was measured, not reasoned "
    "about: with the misplaced file present the retained-set path-list digest read "
    "1177e325f02fd660b9de2edfdbecff1fe30627c4e37d2789592fc58522ddf571 instead of "
    "83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f. NO RETAINED FILE WAS EVER MODIFIED - "
    "the perturbation was an ADDED path in the file list, and both gate0.md hashes were unchanged throughout. "
    "Removing the file restored the digest to the frozen value exactly, re-measured before the Exit and again "
    "after it. The renderer, the record path, the validator target, the plan-path scan target, the "
    "`hash_commands` and `evidence_files` entries were all corrected together, and the superseded captures "
    "are retained as `-pass1` files rather than deleted.",

    "Deviations: this record's own machine validation and the sweep over it necessarily run against the byte "
    "state produced by the final render, and their captures are cited by output_ref rather than inlined as "
    "record rows - a document that quoted its own verification would change the bytes that verification "
    "read. The plan section, which is what plan_hash covers and what a Plan Approval binds, is byte-identical "
    "across every render pass; only the Records rows and the metadata block moved. plan_hash was recomputed "
    "from the FINAL file after the last render and equals the embedded value.",

    "Deviations: this gate wrote no tracked file, made no commit, made no push, created no branch, ran no "
    "fetch and no pull, and took no Writer Lease. Every byte it wrote lies under "
    "`docs/evidence/gatebraid/P2-S5/g1/`. The forty-three retained files of the accepted Gate 0 stop and "
    "every file under `docs/evidence/gatebraid/P2-S5/g0r/` are untouched, which negative criterion N3's "
    "content limb measures rather than asserts. Base SHA is not touched at this gate; ADR-0011 section 9 "
    "sets it at Gate 2 from the head re-read under lease, and the Project field still carries the O0 merge "
    "commit while this record's base_sha is the current head of main, the tree the plan is made against.",

    "Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; Git for Windows "
    "2.51.0.windows.1 whose SYSTEM configuration carries core.autocrlf=true, verified in this window; every "
    "gh call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every "
    "Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL "
    "half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; "
    "WSL /usr/bin/python3 with CPython 3.12.3, jsonschema 4.10.3, whose captures stamp platform.os `wsl`. "
    "The `python` on PATH is the MSYS 3.14.3 build and carries neither, which is why no declared command "
    "names it and why delta D-3 exists. Every captured command was marshalled as an argv list rather than a "
    "shell string except the one row that declares shell semantics explicitly, so no quoting layer could "
    "alter it. environment=mixed-see-prose: the tools run on the Windows host and the WSL half is evidence, "
    "and the selftest and both halves of the evidence toolchain are declared and dry-run on both.",
]

METADATA = """schema: gatebraid/gate-run@2
slice_id: P2-S5
gate: 1
environment: mixed-see-prose
executor: Claude Lead
base_sha: cbd065893b37f20713ae35b8d2673bf26fe4d2ad
started_at: "%(started)s"
ended_at: "%(ended)s"
result: needs_approval
checks:
  - name: gate1-entry-g0-passed
    command: "by-key node read of the Gate and Workflow single-select values with their option ids"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-entry-fields.json"
  - name: control-plane-read-through-o0-outputs
    command: "bin/gatebraid-snapshot.py then bin/gatebraid-frontier.py; four sources ok and complete, sixteen items, snapshot_degraded false"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-entry-frontier.json"
  - name: frozen-scope-pinned-by-hash
    command: "docs/evidence/gatebraid/P2-S5/g1/scope-pin.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D0-scope-pin.json"
  - name: frozen-scope-pin-falsified
    command: "the same instrument with --commit naming the pinned commit's parent; must report SCOPE PIN STALE"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D0F-scope-pin-falsify.json"
  - name: plan-complete
    command: "approach, write_domains, three tasks, test plan, risk notes, rollback note, six negative criteria"
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: allowlist-exact
    command: "docs/evidence/gatebraid/P2-S5/g1/hash-allowlist.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-allowlist-hash.json"
  - name: plan-paths-inside-allowlist
    command: "docs/evidence/gatebraid/P2-S5/g1/plan-path-scan.py docs/evidence/gatebraid/P2-S5/g1/gate1.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-plan-path-scan.json"
  - name: corpus-digest-unmoved
    command: "fixtures/runner-selftest.py; digest after equals the O1-B1 freeze value"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D1-corpus-digest.json"
  - name: historical-ready-failure-classes-killed
    command: "fixtures/run-corpus.py; BP-01, BP-02, BP-03, IN-02, IN-03, IN-04 and IN-05 each killed on a named locus. IN-01 is absent from the corpus by its own known_limitation and is not claimed"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D2-corpus.json"
  - name: test-plan-dry-run
    command: "D0, D0F, D1, D2, D9, D10 to full green; D3, D4, D5, D6, D7, D8, D11 run as declared on the declared platform, each naming the absent deliverable and nothing else"
    result: pass
    output_ref: "#records"
  - name: producer-boundary-runnable-here
    command: "docs/evidence/gatebraid/P2-S5/g1/probe-producer-boundary.py; three boundary crossings against real producers"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-probe-boundary.json"
  - name: evidence-toolchain-runs-on-wsl
    command: "bin/gatebraid-capture.py and bin/gatebraid-validate.py, each run on the WSL half; the capture stamps platform.os wsl, the validator returns accepted"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-probe-D11-wsl-validate.json"
  - name: negative-criteria-falsified
    command: "negative-criteria.py against the seeded changed-path list, code surface and frozen root; all six must fire on their substantive limbs"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D10-negative-falsify.json"
  - name: negative-criteria-path-limbs-hold
    command: "negative-criteria.py against the real tree; N1, N2 and N3 including the retained-record content limb"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D9-negative.json"
  - name: negative-criteria-source-limbs-absent
    command: "the same run; N4, N5 and N6 report bin/gatebraid-ready.py absent, which is what a read-only gate must report about a file it may not create"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D9-negative.json"
  - name: closed-set-sweep-falsified
    command: "the same instrument over the two retained seeds; must fire on the repository, node and issue limbs"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-closed-set-sweep-falsify.json"
  - name: closed-set-repository-limb-closed
    command: "checks-g1-closed-set-sweep.py over the captures domain; exactly two repository identities named, both permitted, no mention-class issue targeted by a query"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-closed-set-sweep.json"
  - name: closed-set-sweep-explains-every-candidate
    command: "the same run; residue remains and the instrument was NOT edited to clear its own finding. Every token identified with its source; a ruling is requested"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-closed-set-sweep.json"
  - name: gate1-exit-checklist
    command: "templates/gatebraid-gate1-exit-checklist.md, every item evidence-backed"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/gate1-exit-checklist.md"
  - name: gate1-record-machine-validated
    command: "bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S5/g1/gate1.md --report-id cov-P2-S5-g1-gate1.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-record-validation.json"
  - name: write-domains-agreement
    command: "docs/evidence/gatebraid/P2-S5/g1/writedomains-check.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-writedomains-check.json"
plan_hash: "%(plan_hash)s"
allowlist_hash: "%(allowlist_hash)s"
hash_commands:
  allowlist: "PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/hash-allowlist.py"
  plan: "PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/hash-plan.py docs/evidence/gatebraid/P2-S5/g1/gate1.md"
evidence_files:
  - docs/evidence/gatebraid/P2-S5/g1/gate1.md
notes: "Planning for the fourth gatebraid-ready attempt on the M2 slice-C frozen scope. The scope was READ, not remembered: seven documents at one named commit of the historical working repository, each pinned by the sha256 of the bytes received, re-derivable by the instrument that produced the pin and falsified against the pinned commit's parent. All three historical attempts declare one identical scope; four deltas separate it from the tools it must now compose, and the fourth was found by running the dry-run rather than by reading it. The Gate 0 re-run opening comment 5472973466 and its rulings belong to the Gate 0 record and are not re-entered here; this gate opened no approval and carries no approvals[] entry. Two checks are typed fail and both are disclosed in full: the source limbs of the negative criteria, which report a deliverable a read-only gate may not create, and the closed-set sweep's explanation limb, whose residue was identified token by token and whose instrument was NOT edited to clear its own finding. The sweep's hard-rule limb - the repository identity set - is closed. A recorded human approval comment is the only door to Gate 2."
"""

w("# Gate 1 evidence - P2-S5")
w()
w("## Plan (frozen at exit)")
w()
plan = open(os.path.join(G, "plan.md"), encoding="utf-8").read().rstrip("\n")
for line in plan.split("\n"):
    if line.startswith("## "):
        raise SystemExit("STRUCTURE: the plan contains a '## ' line, which would "
                         "truncate plan_hash's payload: %r" % line)
    w(line)
w()
w("## Records")
w()

w("**P1 - Agent Team: NOT used, and the decision recorded rather than left implicit**")
w("```")
w("gate-1-contract action 2 makes the read-only team OPTIONAL. No team was")
w("spawned for this Slice, for two reasons and the second is decisive.")
w("(1) The question this gate had to answer - what the frozen scope IS - is")
w("    answered by reading seven named documents at one named commit and")
w("    hashing them. That is what scope-pin.py does, reproducibly; a teammate")
w("    could not do it more reliably, and a teammate's report of it would be")
w("    narration where a hash is available.")
w("(2) Action 2 requires all findings to be FLUSHED TO THE SLICE ISSUE before")
w("    the team dissolves. That flush is a control-plane mutation, and this")
w("    window holds approval for exactly four writes: the handoff comment, the")
w("    write_domains post-condition, the four field updates, and nothing else.")
w("    Spawning a team would have forced either an unapproved mutation or a")
w("    violated constraint.")
w("There are therefore NO team findings to flush, and the constraint list of")
w("failure-disposition row 2 is vacuously satisfied rather than exercised.")
w("(no command: nothing was spawned)")
w("```")
w()

row("P2 entry - the control-plane read, through the O0 outputs alone",
    ["G1-entry-snapshot", "G1-entry-frontier"], limit=14, head=2)
row("P2 entry - Gate = G0 passed, read by node key because the snapshot carries no Gate field",
    ["G1-entry-fields"], limit=10, head=4)
row("P2 D0 - the frozen scope, read at a named commit and pinned by hash",
    ["G1-dryrun-D0-scope-pin"])
row("P2 D0F - the same instrument at the pinned commit's parent: the pin fires",
    ["G1-dryrun-D0F-scope-pin-falsify"], limit=14, head=4)
row("P2 D1 - the frozen corpus digest is unmoved by this Slice",
    ["G1-dryrun-D1-corpus-digest"], limit=16, head=2)
row("P2 D2 - the historical ready-failure classes the frozen corpus holds, each killed on a named locus",
    ["G1-dryrun-D2-corpus"], limit=24, head=10)
row("P2 D3 - ready selftest, Windows half: RUN AS DECLARED; names the absent deliverable and nothing else",
    ["G1-dryrun-D3-selftest-windows"])
row("P2 D4 - ready selftest, WSL half: RUN AS DECLARED; the same absence on the other declared platform",
    ["G1-dryrun-D4-selftest-wsl"])
row("P2 D5 - live end-to-end: RUN AS DECLARED, output directory substituted",
    ["G1-dryrun-D5-live-ready"])
row("P2 D6 - producer failure: RUN AS DECLARED, and the companion probe carrying the real producer status",
    ["G1-dryrun-D6-producer-failure", "G1-probe-D6-no-document"], limit=12, head=2)
row("P2 D6 probe - the D-4 discovery: --project 999 returns a DEGRADED DOCUMENT, not a producer failure",
    ["G1-probe-D6-producer-failure"], limit=14, head=2)
row("P2 D7 - decode guard: RUN AS DECLARED, and the stub whose bytes are the pair that broke the M2 pipeline",
    ["G1-dryrun-D7-decode-guard", "G1-probe-D7-stub"])
row("P2 D8 - consumer refusal: RUN AS DECLARED, and the companion probe over a real stdin composition with pipefail declared",
    ["G1-dryrun-D8-consumer-refusal", "G1-probe-D8-consumer-refusal"], limit=14, head=4)
row("P2 probe - the T1 producer boundary measured on this host, without the program under test",
    ["G1-probe-boundary"])
row("P2 D9 - negative criteria against the real tree: the three path limbs hold, the three source limbs report the absent deliverable",
    ["G1-dryrun-D9-negative"], limit=20, head=4)
row("P2 D10 - negative criteria falsified: all six fire, each on its substantive limb",
    ["G1-dryrun-D10-negative-falsify"], limit=24, head=6)
row("P2 D11 - the evidence toolchain on the WSL half: RUN AS DECLARED, then both tools against artefacts that exist",
    ["G1-dryrun-D11-wsl-toolchain", "G1-probe-D11-wsl-capture", "G1-probe-D11-wsl-validate"],
    limit=18, head=4)
row("P2 sweep - the closed-set sweep, domain named explicitly; repository limb CLOSED, explanation limb typed fail",
    ["G1-closed-set-sweep"], limit=20, head=14)
row("P2 sweep falsified - the same instrument over the two retained seeds",
    ["G1-closed-set-sweep-falsify"])

w("**P2b - no path outside the frozen allowlist appears as a write anywhere in the plan**")
w("```")
if os.path.isfile(os.path.join(CAPS, "G1-plan-path-scan.json")):
    d = cap("G1-plan-path-scan")
    w("$ " + argv_line(d))
    for l in stream_text(d, "stdout").splitlines():
        w(l)
    w("(exit %d)" % d["exit_code"])
else:
    w("PENDING FIRST RENDER: G1-plan-path-scan")
w("```")
w()

w("**P3 - exit checklist completed, every item evidence-backed**")
w("```")
w("docs/evidence/gatebraid/P2-S5/g1/gate1-exit-checklist.md")
w("```")
w()

row("P4 - allowlist_hash reproduced", ["G1-allowlist-hash"])
row("P5 - plan_hash reproduced, from the rendered record itself", ["G1-plan-hash"])
row("P6 - the sanctioned write_domains post-condition on the Slice issue",
    ["G1-writedomains-check"])

w("## Required disclosures")
w()
for d in DISCLOSURES:
    w("- " + d)
w()
w("## gatebraid-metadata")
w()
w("```yaml")
w((METADATA % {"started": STARTED, "ended": ENDED,
               "plan_hash": PLAN_HASH, "allowlist_hash": ALLOWLIST_HASH}).rstrip())
w("```")

open(OUT, "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("WROTE %s" % OUT)
