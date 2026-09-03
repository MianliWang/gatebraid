"""Render docs/evidence/gatebraid/P2-S5/g0r/gate0.md from the g0r captures.

Outputs are GENERATED from the capture records, never transcribed (friction
#96). Every elision prints shown and total plus the committed path of the full
output. The renderer writes the file and asserts nothing about it: the record
is machine-validated separately by bin/gatebraid-validate.py.

This is the RE-RUN's renderer. It is a fresh file under g0r/, not an edit of the
retained docs/evidence/gatebraid/P2-S5/render-gate0.py (sha256
c46487a314c0eae52e3126f9137fc740d279f875b455e94197ed675f63f65238), which is the
permanent record of the accepted stop and is never opened for writing. Its
structure follows the P2-S6 renderer because that is the most recent gate that
recorded a pass.

Two row kinds are emitted. `row` prints a capture's own recorded streams.
`docrow` prints a document this gate produced - the snapshot and the frontier
report - from its bytes on disk, with its measured sha256, because the
startability verdict and its reasons must appear in the record verbatim and
those live in the documents rather than in a stream.
"""
import base64, hashlib, json, os, sys

CAP = "docs/evidence/gatebraid/P2-S5/g0r/captures"
OUT = "docs/evidence/gatebraid/P2-S5/g0r/gate0.md"
STARTED = "2026-08-31T02:43:46Z"
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
    "Deviations: this gate ran WHOLE with no exception of any kind. The D-2 startability-by-reproduced-failure "
    "exception belonged to this Slice's first attempt and to P2-S6 and is spent; the operator's Ruling 1 in the "
    "Gate 0 opening comment on issue 17 states it does not travel. The expected observation was a HEALTHY read "
    "and a healthy read is what was measured: gatebraid-snapshot exited 0 with all four sources ok, complete "
    "true and exit 0, sixteen items and no degradation; gatebraid-frontier exited 0 with snapshot_degraded "
    "false and rendered a verdict for the P2-S5 item. The frontier re-derived every verdict rather than "
    "adopting the producer's declared value, and it discriminated: three aborted P1 slices came back blocked "
    "under ADR-0025 decision 8. Any other outcome, a degraded source or blocked or undecidable or an absent "
    "verdict or a non-zero exit, would have been a stop; none occurred.",

    "Deviations: the closed-set sweep copy was EXTENDED between its first run and its recorded run, under the "
    "operator's Ruling A of 2026-08-31, and the sequence matters. The unextended copy was run first and "
    "reported thirty-two unexplained residue; this window did NOT edit the instrument to clear its own "
    "finding. It stopped, reported, and asked. That failing run is preserved at "
    "captures/G0R-closed-set-sweep-pass1.json, whose internal capture_id remains G0R-closed-set-sweep because "
    "a capture is immutable and renaming its file does not and must not rewrite the record. Ruling A then "
    "authorised exactly three domain facts in the g0r copy only: an N4 class for node ids carrying the "
    "permitted Project's own item-namespace prefix, and FS_PREFIX gaining Files and tags transcribed from the "
    "P2-S6 committed copy together with its own stated reasons. No classification rule, no regex and no "
    "residue criterion changed; N4 is an added branch ordered after the N2 identity test, removing no class "
    "and loosening no criterion.",

    "Deviations: the N4 class was falsified against an OUT-OF-NAMESPACE seed before it was trusted, which is "
    "Ruling A's stated condition and not optional. A class that admits its own Project's items is a domain "
    "fact; a class that admits any item id whatever is a blindfold, and only a foreign-namespace item id "
    "distinguishes the two. The seed at docs/evidence/gatebraid/P2-S5/g0r/falsification/SEED-out-of-namespace-item.json carries four item ids: "
    "the subject item, a genuine sibling row of the permitted Project, an id in a different Project's "
    "namespace, and a near-miss whose namespace differs from the permitted one by a single character. The "
    "extended sweep admitted the first two, classifying them N2 and N4, and left BOTH of the last two as "
    "unexplained residue at exit 1. The pre-existing seed was re-run against the extended copy as well and "
    "its repository, node and issue limbs all still fired at exit 1, so the extension blunted no limb that "
    "already worked. Both falsification runs are recorded rows and both seeds are retained.",

    "Deviations: the capture-set check is typed fail and is not a blocker. Three captures are rejected by the "
    "N3 validator while the capture tool's own guard with re-derivation accepts them, each carrying the single "
    "finding placeholder-survives-its-own-check on a rendered stream-text locus. The cause is the validator's "
    "structural placeholder scan matching faithfully recorded FOREIGN text: an angle-bracket token inside the "
    "metadata checker's own error strings, another inside a Python DeprecationWarning, and an HTML comment "
    "inside the issue body. This is the friction #169 mention class, where the exemption covers command and "
    "citation loci but not captured-stream text. The merged and reviewed P2-S6 Gate 0 records the identical "
    "outcome, the same three capture kinds with the same finding at the same exit code, and discloses it in "
    "its committed gate0.md; the operator's Ruling B of 2026-08-31 carries it here as a disclosure citing that "
    "precedent by name. Its repair is a queued Slice of its own. The check is not one of the contract's "
    "Actions 1 through 6 and does not bear on this gate's disposition.",

    "Deviations: this record was rendered twice. The sweep over the first rendering reported two unexplained "
    "residues of repository kind, both the same token and both introduced by this record's own prose: a "
    "relative path whose leading segment is not a known filesystem prefix. Neither was a repository "
    "identifier. The correction was made in the RECORD, not in the instrument -- the path is now written in "
    "full, which is what this record does with every other path and what ADR-0026 asks for when a committed "
    "path is named. The sweep's rule set is unchanged and still has no class for a bare leading segment of "
    "that shape, so the same token in another document would still be residue; nothing was blinded. Ruling A "
    "authorised three domain facts and exactly three were made; this was not a fourth. The failing first "
    "sweep is preserved at captures/G0R-record-sweep-pass1.json.",

    "Deviations: this gate opened on 2026-08-31 and completed on 2026-09-01 because it stopped mid-gate for "
    "operator adjudication and held. started_at is the first captured action rather than the Workflow field "
    "write that opened the gate, which preceded it and carries no capture of its own; ended_at is measured at "
    "render. The elapsed span is the hold, not execution time, and is stated rather than left to be inferred "
    "from two distant timestamps.",

    "Deviations: bin/gatebraid-frontier.py is byte-identical at the first attempt's baseline and at this one, "
    "sha256 283075b8, and still carries the deferred ADR-0033 defect: the document it emits declares no schema "
    "key and names its interface under a report key instead, which is why the validator classifies it "
    "interface-not-covered rather than rejecting it. This gate therefore ran a repaired producer into an "
    "unrepaired consumer, which is correct under one Slice one tool and affected nothing this gate measured. "
    "The frontier identity-key Slice remains queued. Recorded under the operator's Ruling 5a and not acted on "
    "here.",

    "Deviations: the slice body's gatebraid-metadata block declares four depends_on edges, issues 8, 10, 12 "
    "and 14, while the live dependency graph and this gate's snapshot both carry five, adding issue 19, the "
    "repair Slice. The metadata still validates against gatebraid/slice@1 because the schema does not require "
    "the declared edges to equal the graph's. This is a body edit, out of this gate's scope, recorded under "
    "the operator's Ruling 5b for the Slice's next governed touch of the body and not acted on here.",

    "Deviations: the unfiltered porcelain row is a true measurement of its own moment and is NOT reproducible "
    "later. It recorded fifty-two untracked paths; the count rose as this gate continued writing its own "
    "evidence under the accepted prefix. It belongs to no deterministic subset, and the drift is the gate "
    "working rather than the tree changing underneath it.",

    "Deviations: captures/slice-body-17.md is not itself the product of a captured command. It was written "
    "from the recorded stdout of the G0R-slice-body capture and reproduces that capture's own stream sha256 "
    "1d35bd1269c51732f4aedfffeb513b4c401318059fab682df5d625ce848db03f exactly, so the capture pins the file "
    "rather than the file standing on its own. Same construction P2-S6 used.",

    "Deviations: every byte this gate wrote lies under docs/evidence/gatebraid/P2-S5/g0r/, which is Ruling 2's "
    "layout. No path under docs/evidence/gatebraid/P2-S5/ outside g0r/ was created, modified, moved or "
    "deleted. The forty-three retained files of the accepted stop are untouched and the retained gate0.md "
    "still measures be7c338896b1015923671988166d55af3bd59e028660ce89dfd3b69bc7251513. The Dirty Baseline "
    "Acceptance digest is computed with the re-run subdirectory excluded, so it re-derives equal no matter "
    "what this gate writes beside the retained set.",

    "Deviations: the three instrument copies under g0r/ are copies of the retained originals, verified "
    "byte-identical to them before any edit. checks-g0r-slice-metadata.py is verbatim with zero changes "
    "because it takes its schema and body as arguments. checks-g0r-verify-captures.py differs in one line, "
    "its domain constant. checks-g0r-closed-set-sweep.py differs in six domain facts, three from the layout "
    "and three from Ruling A, each recorded inside the file itself with the retained original's sha256. No "
    "rule of any instrument was changed, and no instrument was edited to accommodate the layout: the sweep "
    "takes its domain as an argument and each domain is named explicitly. --report-id is passed explicitly on "
    "the validation of this record, because the default derives a name from the basename alone and two "
    "gate0.md at different depths would collide.",

    "Deviations: at gate opening Workflow was written to the Gate 0 Verifying option, resolved fresh from the "
    "live field list by exact label with exactly one candidate, id 036a9fdc, its dash measured as U+2014 at "
    "codepoint level rather than by appearance, and read back. The exact labels were carried in a UTF-8 file "
    "and resolved by key, never typed through this host's console, whose codec would mangle the mark. The "
    "same was done for both Exit writes. Executor already read Claude Lead and was not rewritten.",

    "Deviations: this gate wrote no tracked file, made no commit, made no push, created no branch, ran no "
    "fetch and no pull. The evidence files under this Slice's own directory are working files, committed "
    "under the lease at Gate 2, and the Gate 0 contract's Exit clause makes writing them here not a violation. "
    "Base SHA is not re-touched at this gate and still carries the first attempt's baseline.",

    "Deviations: the capture-set check ran before this record was rendered, so the captures written after it, "
    "the render and this record's own machine validation and the sweep over this record, are outside the set "
    "it checked. That boundary is inherent rather than an omission: each new run would itself produce a "
    "capture the run could not have covered, and the regress is stopped by stating where the set ends. The "
    "record itself is independently validated by bin/gatebraid-validate.py in its own row.",

    "Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; Git for Windows "
    "2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh call pins "
    "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every Python "
    "invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL half; "
    "Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL "
    "/usr/bin/python3 with CPython 3.12.3; every captured command was marshalled as an argv list rather than "
    "a shell string, so no quoting layer could alter it. environment=mixed-see-prose: the gate ran on the "
    "Windows host and the WSL half is evidence.",
]

METADATA = """schema: gatebraid/gate-run@2
slice_id: P2-S5
gate: 0
environment: mixed-see-prose
executor: Claude Lead
base_sha: cbd065893b37f20713ae35b8d2673bf26fe4d2ad
started_at: "%s"
ended_at: "%s"
result: passed
approvals:
  - type: Dirty Baseline Acceptance
    author: MianliWang
    comment_url: "https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5472973466"
checks:
  - name: repo-identity-and-remote
    command: "git remote -v"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-remote.json"
  - name: ref-namespace-enumerated
    command: "git for-each-ref (one ref outside the three watched namespaces: reported, not adopted)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-ref-namespace.json"
  - name: base-sha-recorded
    command: "git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-baseline-main.json"
  - name: working-tree-clean-at-base
    command: "git status --porcelain --untracked-files=all (baseline, excluding this Slice's evidence prefix); git rev-parse HEAD; git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-porcelain-baseline.json"
  - name: working-tree-tracked-changes-zero
    command: "git status --porcelain --untracked-files=no (no exclusion of any kind)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-porcelain-tracked.json"
  - name: working-tree-unfiltered-audit
    command: "git status --porcelain --untracked-files=all"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-porcelain-full.json"
  - name: dirty-baseline-acceptance-digest-rederived
    command: "find docs/evidence/gatebraid/P2-S5 -type f -not -path g0r | sort | tr -d CR | sha256sum (Ruling 3 construction; the exact recipe is the invocation line of the A3 digest row)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-p2s5-pathlist-digest.json"
  - name: environment-matches-host
    command: "gh api graphql (Environment field read); python host probe"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-env-field.json"
  - name: tool-versions
    command: "claude.cmd --version; git --version; gh --version; codex.cmd --version; python version probe on both halves"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-tools-git.json"
  - name: slice-metadata-checker-falsified
    command: "checks-g0r-slice-metadata.py --schema schema/slice.schema.json --selftest"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-slice-metadata-selftest.json"
  - name: slice-metadata-parses
    command: "checks-g0r-slice-metadata.py --schema schema/slice.schema.json --body captures/slice-body-17.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-slice-metadata-validation.json"
  - name: startability-snapshot-healthy
    command: "gatebraid-snapshot.py --out captures/g0r-snapshot.json --generated-at (measured); exit 0, all four sources ok and complete, items include P2-S5"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-snapshot-run.json"
  - name: startability-frontier-verdict-startable
    command: "gatebraid-frontier.py captures/g0r-snapshot.json --out captures/g0r-frontier-report.json; exit 0, snapshot_degraded false, the P2-S5 verdict re-derived as startable"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-frontier-run.json"
  - name: closed-set-sweep-falsified
    command: "checks-g0r-closed-set-sweep.py (original seeded domain; must fire on the repository, node and issue limbs after the Ruling A extension)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-closed-set-sweep-falsify.json"
  - name: closed-set-sweep-n4-falsified-out-of-namespace
    command: "checks-g0r-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g0r/falsification/SEED-out-of-namespace-item.json (Ruling A's condition: N4 must admit the permitted Project's own items and still fire on a foreign namespace and on a single-character near-miss)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-closed-set-sweep-falsify-n4.json"
  - name: closed-set-sweep
    command: "checks-g0r-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g0r/captures"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-closed-set-sweep.json"
  - name: closed-set-sweep-over-record
    command: "checks-g0r-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g0r/gate0.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-record-sweep.json"
  - name: capture-set-validated
    command: "checks-g0r-verify-captures.py (capture-tool guard with re-derivation, and bin/gatebraid-validate.py, over every document)"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-captures-validation.json"
evidence_files:
  - docs/evidence/gatebraid/P2-S5/g0r/gate0.md
notes: "Startability read from the hardened gatebraid-snapshot and gatebraid-frontier pair as sole authority, the Gate 0 contract Entry's After-O0 clause, with the pair now the REPAIRED one landed by P2-S6. This gate ran whole with no exception: the operator's Ruling 1 retired the D-2 exception, the expected observation was a healthy read, and a healthy read is what was measured, so result passed rests on the contract's own pass condition rather than on any inversion. Gate 0 opening comment: id 5472973466, author MianliWang observed at verification time, https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5472973466 ; fetched from the API by id and compared byte for byte against the pinned source before use, identical except one trailing newline, which is the known storage class, zero CR bytes and no ruling struck. Per that comment's record-typing clause this record carries NO approvals[] entry for the opening comment itself: the frozen gate-run@2 approvals[].type enumeration still has no member for a Gate 0 Opening, and that missing member remains a candidate item for the already-owed gate-run@2 revision batch. The one approvals[] entry present is Ruling 3's Dirty Baseline Acceptance, which IS a member, carrying the same comment id and scoped to the forty-three retained files of the accepted stop. Ruling 3's digest construction is recorded as the invocation line of the A3 digest row so the recipe is reproducible rather than described, and it excludes the g0r subdirectory so the retained set stays verifiable at every later gate. This gate stopped once, mid-run, when the unextended closed-set sweep reported residue it could only clear by editing itself; the window reported and held, and Rulings A and B of 2026-08-31 resolved both open items. The capture-set check is typed fail because two independent checkers disagree about three captures over faithfully recorded foreign text; it is not one of the contract's Actions 1 through 6, it does not bear on this gate's disposition, and it matches merged P2-S6's committed record in kind and outcome. Base SHA is not re-touched at this gate."
"""

w("# Gate 0 evidence - P2-S5 (re-run under the repaired startability pair)")
w()
w("## Records")
w()

row("A1 - repository identity and remote", ["G0R-remote"])
row("A1 - ref namespace; any ref outside refs heads, refs remotes, refs tags is reported, not adopted",
    ["G0R-ref-namespace"], limit=23)
row("A2 - plan baseline: head of the base branch now (recorded here only; the Base SHA field is set at Gate 2 from the head re-read under lease - ADR-0011 section 9)",
    ["G0R-baseline-main"])
row("A3 - working tree clean AND at the base branch (one predicate, friction #84), evaluated over the baseline excluding this Slice's own evidence prefix",
    ["G0R-porcelain-baseline", "G0R-head", "G0R-baseline-main"])
row("A3 - tracked changes with no exclusion of any kind: zero", ["G0R-porcelain-tracked"])
row("A3 - unfiltered porcelain, so the baseline row's exclusion is auditable",
    ["G0R-porcelain-full"], limit=8)
row("A3 - Dirty Baseline Acceptance re-measurement (Ruling 3): the sorted relative-path-list digest, re-derived by the construction shown on the invocation line, with the re-run subdirectory excluded",
    ["G0R-p2s5-pathlist-digest"])
row("A4 - Project Environment field vs actual host", ["G0R-env-field", "G0R-host-probe"], limit=14)
row("A5 - tool versions",
    ["G0R-tools-claude", "G0R-tools-git", "G0R-tools-gh", "G0R-tools-codex",
     "G0R-tools-python-windows", "G0R-tools-python-wsl"])
row("A6 - slice metadata parses against gatebraid slice@1, the checker falsified first",
    ["G0R-slice-metadata-selftest", "G0R-slice-metadata-validation"], limit=26)

w("### Startability - the repaired hardened pair as sole authority")
w()
row("S1 - gatebraid-snapshot", ["G0R-snapshot-run"])
docrow("S1 - the snapshot document it emitted", "g0r-snapshot.json", limit=60)
row("S2 - gatebraid-frontier", ["G0R-frontier-run"])
docrow("S2 - the frontier report it emitted: the verdict and its reasons, verbatim",
       "g0r-frontier-report.json")

w("### Evidence verification")
w()
row("V1 - closed-set sweep, the original seeded domain re-run against the Ruling A extended copy: every limb that already worked must still fire",
    ["G0R-closed-set-sweep-falsify"], limit=16)
row("V1b - closed-set sweep, N4 falsified against an OUT-OF-NAMESPACE seed (Ruling A's condition): the permitted Project's own items admitted, a foreign namespace and a single-character near-miss both left as residue",
    ["G0R-closed-set-sweep-falsify-n4"], limit=16)
row("V2 - closed-set sweep over every captured response", ["G0R-closed-set-sweep"], limit=32)
w("**V2b - the same sweep over this record itself, run after it was rendered; its output is at "
  "captures/G0R-record-sweep.json and is not inlined here, because a document that quoted its own "
  "sweep would change the text the sweep just read**")
w()
row("V3 - every document checked by the capture tool's own guard with re-derivation and by bin/gatebraid-validate.py",
    ["G0R-captures-validation"], limit=42)

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
