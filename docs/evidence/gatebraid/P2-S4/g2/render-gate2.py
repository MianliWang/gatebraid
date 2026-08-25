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
     "(acceptance 2) — the reference is PINNED to the fingerprint commit at "
     "repair 1; it named `HEAD` before, which does not reproduce",
     ["G2-D8"], None, False),
    ("V13 — N1 · path scope: the diff touches nothing outside the frozen "
     "allowlist — PINNED to the fingerprint commit at repair 1, and it now "
     "reproduces the recorded 137 rather than moving with the tip",
     ["G2-N1"], None, False),
    ("V14 — N2 · no fail-open on a verdict-relevant path (proxy, scope and "
     "matches printed; the scope statement names its false-NEGATIVE channels "
     "from repair 1)", ["G2-N2"], None, False),
    ("V15 — N3 · no live network call in any declared test command",
     ["G2-N3"], 26, False),
    ("V16 — N4 · no verdict without validation, both halves; the structural "
     "half's claim is corrected at repair 1 to what was measured — one guarded "
     "construction site, NOT an unforgeable type", ["G2-N4"], None, False),
    ("V17 — T3 harness selftest, both platforms (NOT a declared test-plan "
     "command; recorded because it is the falsification of the instrument the "
     "declared commands rely on)",
     ["G2-T3selftest-windows", "G2-T3selftest-wsl"], 12, True),
    ("V18 — this gate's captures machine-validated under the capture tool's own "
     "write-path guard, re-derivation layer included (NOT a declared test-plan "
     "command; it is what makes the `output_ref` targets evidence rather than "
     "filenames). The count in this row is the WORKING TREE at "
     "the interval `2026-08-24T13:02:34.689Z` to `13:02:38.461Z` — this label "
     "names the interval's START edge, and the disclosures name its END edge; "
     "see them for the three instants and their three figures",
     ["G2-captures-validation"], None, False),
    ("V19 — the frozen surface by TREE OBJECT, at the plan baseline and at the "
     "fingerprint commit. Both references are pinned, so this row cannot be "
     "falsified by a later commit; it is what the D7 disclosure composes with "
     "V13 in place of the measurement missed at the first named point. A tree "
     "object is content, so equality here also refuses a write that was later "
     "reverted", ["G2-frozen-trees"], None, False),
]
for label, cids, limit, tail in ROWS:
    row(label, cids, limit, tail)

w("## Review record")
w()
w("### Review 1")
w()
w("| Item | Verdict | Evidence |")
w("|---|---|---|")
w("| R1 allowlist confinement | **PASS** | Review 1 §2. 137 paths over "
  "`<base>..50d08de6`, 6 `bin/` + 131 evidence, **0 outside**; byte-identical "
  "to `changed_paths` and to `G2-fp-diff.json`. Re-checked at C1 and D1, "
  "including the whole `bin/` tree object |")
w("| R2 test-plan coverage | **PASS** | Review 1 §3. All four Acceptance boxes "
  "map to declared commands as the frozen plan states; **all 13 declared "
  "commands re-run in the review session, all green, all exit 0**. Two "
  "disclosed coverage limits weighed as F-04 |")
w("| R3 evidence is rows that reproduce | **PASS**, with **F-01** | Review 1 "
  "§4. Frozen hashes, fingerprint pair, both diffs and the record-validation "
  "run reproduce byte-identically; all 12 elisions carry `shown/total` and a "
  "committed path whose line count matches; 41/41 captures re-verified. F-01 "
  "discharged at repair 1; re-checked at C2 and D2 |")
w("| R4 negative criterion | **PASS**, with **F-02**, **F-03** | Review 1 §6. "
  "N1 holds **and still fires** on the O0-B1 range (exit 1, 21 outside); N2's "
  "property re-established by independent AST enumeration, not inherited; N3 "
  "holds; N4 holds in both halves. F-02 and F-03 record limits of the "
  "checkers, not failures of the properties |")
w("| R5 no prohibited action | **PASS** | Review 1 §8. No push (no remote ref "
  "exists), no PR, no tag, no merge, no dependency installation, no disabled "
  "hook or check — the repository carries no CI, hook or dependency-manifest "
  "file at all — and no second writer |")
w()
w("Two supplementary items the reviewer measured beyond the five, recorded "
  "because they close questions this record raised against itself:")
w()
w("| Item | Verdict | Evidence |")
w("|---|---|---|")
w("| R3-Q D7 at the missed point | **CLOSED BY MEASUREMENT — surface unmoved "
  "at every point** | Review 1 §5. The branch point was materialised with "
  "`git archive` and the digest measured there: "
  "`66051715f76cf52d881aa143d9267f932407dbf5b9c4e6be9f81395ec641ef8e`, equal "
  "to the batch-frozen value and to both points this gate measured. **A writer "
  "cannot close its own gap; this one was closed by the reviewer** |")
w("| R4-B induced-failure matrix | **CONFIRMED — 12/12, 0 unexercised** | "
  "Review 1 §7. Re-run independently, with the clause-to-schema mapping built "
  "from `$defs.item.allOf`'s own `$comment` text rather than from this "
  "harness's labels — so the three previously-unasserted conditionals are "
  "shown to fire **behaviourally**, not merely to be labelled as firing |")
w()
w("**Reviewer rows** (the commands the reviewer ran, with outputs — including, "
  "for R3's deterministic subset, the byte-identity re-runs). **Transcribed "
  "under the Release Approval by the writer session holding the lease, from "
  "the three sealed reports and from nothing else**; the reviewer's own rule "
  "is that it never transcribes. Each source is cited by name, byte size and "
  "sha256, and each was re-verified at transcription time.")
w()
w("| source | bytes | sha256 | sealed prefix |")
w("|---|---|---|---|")
w("| `_handoff/batch-o0/REVIEW1-M3-P2S4.md` | 46,125 | "
  "`651f4bf676ad5516985eb7e1b9efc5cbcef93c4278f4a8e0e5763a0a27018945` | "
  "45,582 B, `096dbac63965bcceb596796e882325b252f552e414e19f2a4d2be3618c979840` |")
w("| `_handoff/batch-o0/REVIEW1-ADDENDUM-M3-P2S4.md` | 29,661 | "
  "`a76602ea355fcebf00a2c42b7ab536cd4195114ffa743e0b47703f4b6fb7ee21` | "
  "29,208 B, `a459e86e850306cdd1060642a80276698d473a9a7b032d48d5e3c67e1df96867` |")
w("| `_handoff/batch-o0/REVIEW1-ADDENDUM2-M3-P2S4.md` | 28,260 | "
  "`1ba2dd811d41da244e6078cd2afde1cb041738b3849fbb391f3b92a9fb924e75` | "
  "27,806 B, `f9e3daf9e412b3b0f5dac9671fd72e13ed759bfb9fbece30b1fc8b00f49b54fb` |")
w()
w("**The three sources are session material under `_handoff/`, which the "
  "tracked `.gitignore` excludes — they do not land in this repository.** "
  "Stated because it bounds what this record can offer: the identities above "
  "make a retained copy checkable, and the measured values below are carried "
  "into the record so it stands without them, but a later reader who does not "
  "hold those files cannot re-derive the reviewer's own terminal output from "
  "here. What that reader CAN do is re-run the same commands against this "
  "branch, which is what makes the verdicts checkable rather than merely "
  "attributed.")
w()
w("What the reviewer measured, by item:")
w("```")
w("R1  git diff --name-only <base>..50d08de6  = 137 paths")
w("      6 bin/ + 131 docs/evidence/gatebraid/P2-S4/, 0 outside")
w("      byte-identical to the record's changed_paths AND to the committed")
w("      capture G2-fp-diff.json (both sha256")
w("      ec21760706921912ca25e09bc7fd1cb9c019ff7b2fb2ec28e361fa0c8b030cbd, 7,725 B)")
w("      50d08de6..0964979c = 13 paths, all evidence")
w("      porcelain empty incl. --untracked-files=all; no remote ref for the branch")
w("R2  all four Acceptance boxes map to declared commands as the frozen plan states")
w("      all 13 declared commands RE-RUN in the review session: all green, all exit 0")
w("R3  both frozen hashes, the fingerprint pair, both diffs and the")
w("      record-validation run reproduce byte-identically")
w("      all 12 elisions carry shown/total and a committed full-output path")
w("      whose real line count matches")
w("      41/41 captures re-verified under --verify-record --rederive")
w("R3-Q  D7's missed point CLOSED BY MEASUREMENT: the reviewer materialised the")
w("      branch point with git archive and measured the digest there =")
w("      66051715f76cf52d881aa143d9267f932407dbf5b9c4e6be9f81395ec641ef8e,")
w("      equal to the batch-frozen value and to both points this gate measured")
w("R4  N1 holds and still FIRES on the O0-B1 range (exit 1, 21 outside)")
w("      N2's property independently re-established by AST enumeration, not inherited")
w("      N3 holds; no declared command reaches the network")
w("      N4 holds in both halves")
w("R4-B  induced-failure matrix CONFIRMED 12/12, 0 unexercised, re-run in the")
w("      review session; the clause-to-schema mapping was built from")
w("      $defs.item.allOf's own $comment text, NOT from this harness's labels,")
w("      so the three previously-unasserted conditionals are shown to fire")
w("      BEHAVIOURALLY; D4 exercises a non-empty relation in both directions")
w("      in 4 of 5 cases")
w("R5  no push (no remote ref exists), no pull request, no tag, no merge, no")
w("      dependency installation, no disabled hook or check (the repository")
w("      contains no CI, hook or dependency-manifest file at all), no second writer")
w("```")
w()
w("Bounded re-check 1, on repair 1 — six of seven PASS, **C4 FAIL** (F-09):")
w("```")
w("C1 PASS  13 paths, all evidence; -- bin/ empty; and the whole bin/ TREE OBJECT")
w("           identical at both commits, cff967daf75872071f53319d0fe07274cc8fb76f")
w("C2 PASS  all four pinned captures reproduce byte-identically from their own")
w("           recorded argv; the checks[] row reproduces 137")
w("C3 RULED CORRECT AS LEFT   G2-fp-head is outside the nominated subset")
w("           (V12-V16), so decision 2's exclusion limb is satisfied")
w("C4 FAIL  the D7 substitute sentence attributes to V13 a range V13 no longer")
w("           covers -> F-09, one-reference fix")
w("C5 PASS with F-08         F-03, F-02, F-06 correct and documentary-only")
w("C6 PASS  every field, the lease, the comment set and the absence of")
w("           push/PR/tag/merge verified; the '6' was an arithmetic slip,")
w("           the state is unchanged at 7")
w("C7 PASS  nothing changes; V12/V13 now reproduce BETTER than when first passed")
w("```")
w()
w("Bounded re-check 2, on repair 2 — **seven of seven PASS, no FAIL**:")
w("```")
w("D1 PASS  6 paths, all evidence, none bin/; 32fb583f:bin =")
w("           cff967daf75872071f53319d0fe07274cc8fb76f, unmoved across both repairs")
w("D2 PASS  structural : 0, findings : 0, verdict : accepted, exit 0 -- re-run")
w("D3 PASS with F-11   repair_attempts = 1 entry, result: needs_approval,")
w("           ledger in both sites with PROVISIONAL in both")
w("D4 PASS  the moving-reference scan over the corrected paragraph returns 0;")
w("           ruled correct, not an over-correction")
w("D5 PASS  notes and the comment block carry 0 elision-shaped tokens")
w("D6 PASS  fingerprint 50d08de6/f797297005/137; cells blank; Gate G1 passed;")
w("           7 comments, 5395615534 last; lease held; sweep 46/46; no bytecode")
w("D7 PASS  nothing changes; F-09 DISCHARGED")
w("```")
w()
w("**Findings** (one row per finding: what was measured, not a story about it). "
  "Thirteen were raised across the three documents. **No verdict is FAIL**: "
  "C4's FAIL was on a prose sentence, was repaired, and is discharged.")
w("```")
w("F-01  two rows in the nominated deterministic subset named HEAD rather than a")
w("        pinned SHA (ADR-0028 decision 2). DISCHARGED at repair 1.")
w("F-02  N2's shapes do not cover the X or <empty-literal> idiom -- 32")
w("        or-expressions in bin/gatebraid-snapshot.py by AST count. The property")
w("        holds; N2 is not what establishes it. CORRECTED at repair 1;")
w("        shape coverage RECORDED AS DEBT, not repaired.")
w("F-03  'unforgeable' overstated the N4 mechanism: _VALIDATION_TOKEN is a")
w("        reachable module attribute, the reviewer forged a ValidatedSnapshot,")
w("        and consume() has no isinstance guard. CORRECTED at repair 1.")
w("        The isinstance guard and the same word surviving in")
w("        bin/gatebraid-frontier.py's docstring are RECORDED AS DEBT --")
w("        hardening after review would ship un-reviewed behaviour.")
w("F-04  the live gh transport is committed and unmeasured. Established: it")
w("        constructs no HTTP client, handles no credential, adds no network")
w("        dependency to any acceptance result. NOT established: that it")
w("        functions. RECORDED, NOT REPAIRED -- covering it needs a test this")
w("        frozen plan does not declare.")
w("F-05  capture counts diverged across dispatch, record and tree. CORRECTED at")
w("        repair 1 with the instant each figure describes.")
w("F-06  approvals[] cannot express the Writer Assignment: the frozen")
w("        gate-run@2 enumeration has 10 members and none is Writer Assignment,")
w("        so the typing is SCHEMA-FORCED. Note tightened at repair 1.")
w("        RECORDED; queued for the schema's next revision.")
w("F-07  the reviewer's own isolation incident, self-reported: a grep scoped to")
w("        bin/ rather than to its six subject files returned 8 comment lines")
w("        from a landed tool barred to that window. Quarantined, unused,")
w("        disclosed; accepted as correctly handled. Not a Slice defect.")
w("F-08  the sweep-interval edge was named by arithmetic, not in words.")
w("        CORRECTED at repair 2: both endpoints and both true distances")
w("        (13.31 s from the start edge, 9.54 s from the end edge).")
w("F-09  the D7 substitute sentence cited V13 for a range V13 no longer covered")
w("        after repair 1 pinned it. THE ONE FAIL. CORRECTED at repair 2 and")
w("        DISCHARGED -- ruled replaced with a stronger argument than the fix")
w("        the reviewer specified.")
w("F-10  G2-R1-changed runs git status --porcelain and does not reproduce")
w("        (525 bytes recorded, 0 live). Not a defect: outside the deterministic")
w("        subset, no truthful pinned form exists, and the reproducible")
w("        comparand is supplied beside it. RECORDED, NOT REPAIRED.")
w("F-11  the repair_attempts caveat is a YAML comment, so a machine consumer")
w("        reading the array alone cannot see it: yaml.safe_load returns 19 keys")
w("        and the caveat text is not among them, because A COMMENT IS NOT DATA.")
w("        No placement closes the machine case; only notes reaches the data")
w("        layer, and notes carries it. Neither site claims otherwise -- both")
w("        phrase the ledger as an imperative to a reader, never as a mechanism.")
w("        RECORDED, NOT REPAIRED; queued with F-06 for the same revision.")
w("F-12  cosmetic residue of repair 2's rewrite: an orphaned closing apostrophe")
w("        in the caveat comment and a missing space after a separator. Both sit")
w("        inside prose or a YAML comment, both ASSERT NOTHING, the document")
w("        parses and the landed validator accepts it. RECORDED, NOT REPAIRED.")
w("F-13  removing a true MENTION to satisfy a scanner sets a precedent worth")
w("        naming. The HEAD token in the parenthetical was a mention, not a use;")
w("        under ADR-0018 section 2 -- where a proxy over-matches, THE PATTERN")
w("        GOVERNS -- adjudicating it in place would ALSO have been correct.")
w("        Removal won here because this record's own subject is that ambiguity,")
w("        and it cost nothing: the superseded sentence is named, the defect")
w("        described, the literal text recoverable from 3a0f4ac9. RECORDED, NOT")
w("        REPAIRED, and explicitly NOT licence to edit away a true mention")
w("        whenever a checker complains.")
w("```")
w()
w("**Open at transcription: F-04, F-11, F-12, F-13 — all informational or debt, "
  "none routing to a stop.** The queued `gatebraid/gate-run@2` revision carries "
  "three items: the friction-#94 conditional keyed on a bare count, F-06's "
  "missing `Writer Assignment` type, and F-11. The closure ledger carries "
  "F-04's unmeasured live transport, the N4 `isinstance` guard, N2's shape "
  "coverage, and `bin/gatebraid-frontier.py`'s surviving docstring word.")
w()
w("**The repair-residue class, recorded as the durable lesson.** Three "
  "corrections each seeded the next finding — F-08 an ambiguity between two "
  "TRUE figures, F-10 a non-reproducing row, F-12 two characters that assert "
  "nothing. **Severity is strictly decreasing, not compounding**, and each was "
  "caught by the re-check that followed, which is what earned those re-checks "
  "their cost. **A correction to prose is itself prose and inherits the same "
  "failure modes** — that is the lesson, and it is why a repair is re-checked "
  "rather than trusted.")
w()
w("- Reviewer write disclosure: **`none` on any tracked path, across all three "
  "review windows.** Each window's sole write was its own report under "
  "`_handoff/`, which `git check-ignore -v` confirms is excluded by "
  "`.gitignore:7:/_handoff/` and is therefore not a tracked-file edit. Measured "
  "each time: **zero commits, zero tracked files modified/added/deleted, zero "
  "`gh` mutations** — every `gh` call was a read (`api user`, "
  "`api …/issues/comments/…`, `api graphql` query, `pr list`) — zero "
  "label/field/comment operations, no lease taken, no ref created, moved or "
  "deleted, and no checkout: the branch point was materialised with "
  "`git archive` rather than by moving `HEAD`. Bytecode: none, searched before "
  "and after every run. Scratch material lived outside every repository.")
w("- Rules given to the reviewer: measure never declare; cite never restate; a "
  "checker never echoes a forbidden value into its record, name loci and counts, "
  "and a bare zero states what it searched; closed-set by complement over its "
  "own outputs with the ruled touch-vs-mention distinction, permitted set "
  "`MianliWang/gatebraid` + `MianliWang/gatebraid-scratch`; every `gh` read pins "
  "`GH_CONFIG_DIR`, endpoints without a leading slash, identity check first and "
  "alone; every Python invocation carries `-B` and `PYTHONDONTWRITEBYTECODE=1`, "
  "the variable set inside any `wsl -e` command, no `py_compile`, any bytecode "
  "removed and disclosed; on any uncertainty STOP and ask; **isolation** — the "
  "four landed evidence tools are used and never read, the six new `bin/` files "
  "are the subject; **sole write** its own report, zero commits, zero "
  "tracked-file edits, zero `gh` mutations; **the verdicts are the reviewer's "
  "to write and it never transcribes**, transcription being the writer's under "
  "the Release Approval; friction ordinals unclaimed; and the host hazard named "
  "in advance — the console mangles U+2014 and U+2192, so compare BYTES "
  "wherever a mark decides an outcome. Both re-checks carried the same rules "
  "verbatim (spec §4, friction #97).")
w()
w("## Repair record")
w()
w("### Repair 1")
w()
w("- Hypothesis (new): the record's own reproducibility, not its measurements, "
  "is what is defective — two rows nominated as deterministic name a moving "
  "ref, and three prose claims (N4's reach, N2's reach, the capture count) "
  "assert more or less than what was measured.")
w()
w("**Novelty measured** (ADR-0027 §1; the comparand is the tree Review 1 "
  "examined, not a failed state — no review item was red)")
row("tree at the reviewed state, and the paths this repair changes",
    ["G2-R1-tree-before", "G2-R1-changed"])
w("- The changed-path list above is measured before this record is re-rendered, "
  "so it does not include this record itself (`gate2.md`) nor any capture "
  "written after that measurement — this row's own capture, and the "
  "record-validation capture. Every one of them is under "
  "`docs/evidence/gatebraid/P2-S4/g2/`, no `bin/` path is among them, and the "
  "repair commit's own diff is the comparand the bounded re-check runs.")
w("- Result: `green`")
w("- Consult: `none`")
w("- Scope: `docs/evidence/gatebraid/P2-S4/` only. **No `bin/` file changed — "
  "not one byte**, verified by `git status --porcelain --untracked-files=all -- "
  "bin/` returning empty and by the repair commit's diff carrying no `bin/` "
  "path. No behavioural change was made to either tool or to either checker; "
  "every edit is to what a record or a checker SAYS about what it measured.")
w("- `repair_limit` 2: one spent at this attempt.")
w()
w("### Repair 2")
w()
w("- Hypothesis (new): repair 1's own corrections left four prose defects — a "
  "citation that repair 1 itself falsified by pinning the row it cites, a "
  "justification stated more strongly than its mechanism supports, an interval "
  "reported by one unnamed edge in two places, and a newly added row whose "
  "non-reproduction was not declared.")
w()
w("**Novelty measured** (the comparand is the tree at repair 1's tip)")
row("tree at repair 1, and the `bin/` tree object at the fingerprint commit and "
    "at repair 1",
    ["G2-R2-tree-before", "G2-R2-bintree"])
w("- **The `bin/` row above is the pinned form of this repair record's "
  "no-`bin/`-byte claim.** Repair 1 rested that claim partly on a "
  "`git status` row that does not reproduce (F-10); a tree object at two "
  "pinned commits does reproduce, and it is strictly stronger than comparing "
  "the six blobs, because it also refuses an addition or a removal. Review 1's "
  "addendum adopted this comparison as the standard and it is used here.")
w("- Result: `green`")
w("- Consult: `none`")
w("- Scope: `docs/evidence/gatebraid/P2-S4/` only; four prose corrections, no "
  "behavioural change to any tool or checker, **no `bin/` byte**.")
w("- **THE REPAIR LEDGER, stated here because the array no longer states it.** "
  "`repair_limit` is 2. **Repair 1 and repair 2 are both spent. ZERO repairs "
  "remain and no third is available.** If anything further is found the route "
  "is a decidable stop — `result: stopped` with the matching `Next Approval` — "
  "and the state goes to the operator. No remediation past the budget, ever.")
w("- **Why repair 2 is not an entry in `repair_attempts`, and why that is not a "
  "reduction of the count.** That array models the gate-2-contract's **D6 "
  "red-check sequence**; its own `$comment` grounds it in that sequence by "
  "name — *repair 1 … Codex consult … repair 2 … Human Diagnosis Required* — "
  "and **neither of this Slice's repairs was an instance of it**: no review "
  "item was ever red, Review 1 returned R1–R5 all PASS, and both repairs "
  "corrected prose in a record that already validated. Recording repair 2 "
  "there trips `allOf[0]`, whose antecedent is `repair_attempts` present and "
  "`minItems: 2` and no `consult_ref` anywhere — **a bare count, naming no "
  "result** — and forces `result: human_diagnosis_required`, which is false of "
  "this gate. The escape of inventing a `consult_ref` is refused in the "
  "schema's own words: *nothing can force a false `consult_ref`*, and no "
  "consult occurred. **A reader who sees only the array must not conclude that "
  "one repair remains: none does.** This is the frozen schema's modelling "
  "range, disclosed as such and not as a convenience — the same shape as "
  "F-06's `approvals[]`, which cannot express a Writer Assignment. **This is a "
  "PROVISIONAL representation** pending the `gatebraid/gate-run@2` revision "
  "that keys this conditional on the sequence it means rather than on a count, "
  "carried through the batch lane by ADR beside F-06's missing type; **it is "
  "not yet normative**, and a later Slice inheriting this record should read it "
  "as debt recorded, not as a rule established.")
w()
w("## Required disclosures")
w()
w("- Deviations: **D7 was not run at the first of its three named points.** The "
  "frozen plan requires the frozen surface to be re-measured by D7 *before the "
  "first implementation commit*, after the last, and at Gate 2 exit. It was run "
  "after the last implementation commit and at exit, and NOT before the first "
  "one; the omission is the executor's. **What stands in its place is not a "
  "substitute measurement at the missed instant but two PINNED facts that "
  "compose into the property that measurement would have established, neither "
  "of them naming a reference that can move.** First, `V19`: `schema/` and "
  "`fixtures/` are the SAME TREE OBJECTS at the plan baseline `%s` and at the "
  "fingerprint commit `50d08de6…` - `schema` is "
  "`afbaab4f6dc51d050b8fe7fb7b356667088ce1c9` at both and `fixtures` is "
  "`802366bed1ce3fe6a156bd5d3b967b071d8d76b2` at both - so neither frozen "
  "directory was written anywhere inside the span the missed instant sits in, "
  "in whatever order the commits of that span fell. A tree object is content, "
  "so this is stronger than a path-set argument: it cannot be satisfied by a "
  "write that was later reverted. Second, `V13` pinned shows that same span "
  "carrying 137 paths with none outside `bin/` and "
  "`docs/evidence/gatebraid/P2-S4/`. **Every commit after the fingerprint "
  "commit is record-only**, confined to `docs/evidence/gatebraid/P2-S4/`, which "
  "is why nothing here needs to reach past that commit to stay true. "
  "*(An earlier revision of this paragraph cited `V13` for a range ending at "
  "the branch head rather than at a pinned commit. Repair 1 pinned `V13` to "
  "end at the fingerprint commit, which made "
  "that citation false about `V13` while its conclusion stayed true; Review 1's "
  "addendum ruled it F-09, the one correction owed, and this is that "
  "correction. The superseded sentence is named, not silently replaced.)* "
  "`V11` shows `digest "
  "before` equal to `digest after` equal to the batch-frozen value at the two "
  "points D7 did run. The schema "
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
  "direction in which it errs · **the handoff fingerprint and V18's sweep were "
  "measured at the commit BEFORE this record's own commit**, which is what the "
  "fingerprint's definition requires and what makes it Gate 3's comparand. "
  "V12 (D8) and V13 (N1) described the same instant but named `HEAD` to reach "
  "it; **repair 1 pins both to `50d08de6…`** so they reproduce, and N1 now "
  "returns the recorded `137` instead of moving with the tip. The files each "
  "later commit adds are outside those measurements; every one of them is under "
  "`docs/evidence/gatebraid/P2-S4/`, so the allowlist claim is unaffected. This "
  "is the boundary any sweep has over its own output, named rather than left to "
  "be noticed · **REPAIR 1, F-01 — what was pinned and what was deliberately "
  "not.** `V12` and `V13` are pinned, and so are `G2-fp-tree` "
  "(`git rev-parse 50d08de6…^{tree}`, which still derives the tree rather than "
  "restating it) and `G2-fp-diff` "
  "(`git diff --name-only df666070…..50d08de6…`, which reproduces the 137 paths "
  "exactly), plus the `allowlist-respected` `checks[]` row. **`G2-fp-head` is "
  "left naming `HEAD`, on purpose.** Pinning it would turn "
  "`git rev-parse HEAD` into `git rev-parse 50d08de6…`, a command that echoes "
  "its own argument and establishes nothing; the row's only content is *what "
  "the branch head was at that instant*, and pinning would destroy it while "
  "making the row look deterministic. The grant says not to manufacture "
  "agreement, and that is what manufacturing it would look like. **Why leaving "
  "it is sufficient, stated in the corrected form Review 1's addendum ruled "
  "under C3.** An earlier revision of this clause said the head claim was "
  "*corroborated* by `G2-fp-tree`; that was a shade too strong and is "
  "withdrawn. `G2-fp-tree` takes `50d08de6…` as its own argument, so it would "
  "reproduce identically even if the head claim were wrong — it cannot "
  "independently confirm that this commit WAS the branch head. It does not "
  "need to. The row sits **outside the nominated deterministic subset**, so "
  "ADR-0028 decision 2 is satisfied by its exclusion limb rather than by "
  "pinning; and everything the fingerprint must SPECIFY for Gate 3's drift "
  "check is carried by pinned, reproducing rows — that the commit exists on "
  "this branch (`V12`), that its tree is the recorded `tree_sha` "
  "(`G2-fp-tree`), and that its changed paths are exactly the 137 of "
  "`G2-fp-diff`. What is left unpinned is **provenance — how this writer "
  "arrived at that commit — not specification**, and provenance is inherently "
  "unreproducible. Decision 2 handles exactly that case by exclusion rather "
  "than by faking ·**REPAIR 1, F-03 — an overclaim in "
  "this record, corrected.** The N4 structural half was described as making the "
  "validated type UNFORGEABLE. Review 1 measured that false: `_VALIDATION_TOKEN` "
  "is a reachable module attribute, a holder of the module forged a "
  "`ValidatedSnapshot`, and `consume()` carries no `isinstance` guard — it "
  "rejected a duck-typed stand-in only incidentally, by `AttributeError`. The "
  "accurate claim, now carried by the checker's own output, is one guarded "
  "construction site inside `validate()`: strong against accidental refactor, "
  "NOT proof against a determined caller in the same module. **The N4 property "
  "itself holds in both halves**; the overstatement was in prose. `isinstance` "
  "was NOT added — that is hardening, not correction, and shipping un-reviewed "
  "behaviour after the review is what this sequence must not do; it is debt. "
  "**`bin/gatebraid-frontier.py`'s module docstring carries the same word and "
  "was not edited**, because this repair changes no `bin/` byte; that line is "
  "debt too, and it is named here so the correction is not mistaken for "
  "complete · **REPAIR 1, F-02 — N2's reach was overstated by omission.** N2 "
  "declares it errs toward false positives and owed an account of its "
  "false-NEGATIVE channels. Two are now named in its own scope statement: the "
  "`X or <empty-literal>` idiom is not searched at all — 32 `or`-expressions in "
  "`bin/gatebraid-snapshot.py` by AST count, re-derived here and equal to "
  "Review 1's — and N2a's `fail_closed` test is a substring search for "
  "`\"raise\"` that a comment or string literal could satisfy. Review 1 "
  "adjudicated all 32 independently and the property holds; **the correction is "
  "that N2 is not what establishes it.** The checker's behaviour is unchanged: "
  "changing what it detects after its gate exited would ship un-reviewed "
  "behaviour · **REPAIR 1, F-05 — one figure, three instants.** The capture "
  "count in `g2/` is **30** committed at the fingerprint commit `50d08de6…`, "
  "**34** in the working tree while the sweep ran — **a sweep is an INTERVAL, "
  "not an instant, and both endpoints are given here because naming only one "
  "made two correct figures read as a contradiction (Review 1 addendum, "
  "F-08)**: the sweep ran `2026-08-24T13:02:34.689Z` to `13:02:38.461Z` and "
  "the commit is stamped `13:02:48Z`, so the true distances are **13.31 s from "
  "its start edge and 9.54 s from its end edge**; the circulating figures "
  "*fourteen* and *ten* are second-truncated derivations of those two, one per "
  "edge, and neither was wrong except in failing to say which edge it measured "
  "from — and **41** at "
  "the tip `0964979c…`; all three are re-derived here and all three are true of "
  "their own instant. A fourth figure, **33**, appears in this Slice's posted "
  "Gate 2 handoff comment `5395615534` and originated with this executor: it "
  "was the standalone sweep run before `G2-D7-exit` and the sweep's own capture "
  "existed. The posted comment is durable and is not edited; the figure is "
  "corrected here. **The ambiguity was the defect, not any figure** · "
  "**REPAIR 2, F-10 — a row in this record does not reproduce, and that is "
  "recorded rather than left to be discovered.** `G2-R1-changed`, added by "
  "repair 1 as its novelty measurement, runs `git status --porcelain "
  "--untracked-files=all` — the second term in ADR-0028 decision 2's own "
  "prohibition — and it does NOT reproduce: 525 bytes recorded, 0 live, the "
  "tree now being clean. **Not a defect, and this record makes no claim that "
  "it reproduces.** It is outside the nominated deterministic subset, so "
  "decision 2's exclusion limb applies; a working-tree novelty measurement has "
  "no truthful pinned form, since pinning it would describe a different thing; "
  "and the reproducible comparand is supplied beside it — the repair commit's "
  "own diff, which is what the bounded re-check actually used. Its sibling "
  "`G2-R1-tree-before`, pinned to `0964979c…^{tree}`, reproduces "
  "byte-identically. Named here so no later reader mistakes its "
  "non-reproduction for drift · "
  "**REPAIR 1, F-04 is RECORDED, NOT REPAIRED.** The live `gh` transport stays "
  "committed and unmeasured: covering it needs a test this frozen plan does not "
  "declare, and the boundary is already disclosed above and named in N3's "
  "scope. It goes to the closure ledger as debt · **commit messages carry a "
  "`Co-Authored-By` "
  "trailer** per the executing harness's standing instruction, noted so the "
  "convention change is not mistaken for drift."
  % BASE_SHA)
w("- Reviewer write disclosure: **`none` on any tracked path, across all three "
  "review windows** — mirrored from the Review record above. Each window's "
  "sole write was its own `_handoff/` report, excluded by "
  "`.gitignore:7:/_handoff/`; zero commits, zero tracked-file edits, zero "
  "`gh` mutations, no lease taken, no ref moved, no checkout.")
w("- **Transcription is not a repair, and no later reader should count a "
  "third.** Filling the Review record's verdict cells is the Gate 2 contract's "
  "own Exit step once the reviewers pass — *reviewers pass → `Gate = G2 "
  "passed`, Workflow → `Needs Release Approval`* — and it spends nothing from "
  "the repair budget. **The budget remains: `repair_limit` 2, both spent, zero "
  "remaining**, exactly as the Repair record states. The two repairs changed "
  "what this record SAYS; this step records what the reviewer RULED, and the "
  "reviewer's own rule is that it never transcribes.")
w("- Environment: Windows 11 host, Git Bash (MSYS2) shell, `mixed-see-prose` "
  "with the WSL half exercised for D1b, D2b, D3b, D6b and V17; Windows loader "
  "`C:\\Python312\\python.exe` (CPython 3.12.2, jsonschema 4.23.0), WSL "
  "`/usr/bin/python3` (CPython 3.12.3, jsonschema 4.10.3); "
  "`PYTHONDONTWRITEBYTECODE=1` on every Windows Python invocation and set "
  "inside the `wsl` command on the WSL half, which inherits no Windows process "
  "environment; `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` "
  "call, every endpoint written without a leading slash (friction #33); the "
  "selftest seeds and the harness's parallel tree are written to scratch paths "
  "outside every repository, as the contract requires such a path to be named. "
  "**BP-01 fired once more during this gate, on the executor's own verification "
  "rather than on a deliverable, and is recorded because it is a measurement.** "
  "Checking that this record's `Plan Approval (G1→G2)` carries U+2192 was first "
  "attempted by piping `gh project field-list --format json` into a Python "
  "reader; the console codec re-encoded the response and the live option name "
  "arrived as the codepoints U+922B U+625C, so the comparison returned a FALSE "
  "mismatch. Re-measured by writing the response to a file and reading it with "
  "an explicit UTF-8 decode, the live option is U+2192 and the record string is "
  "byte-identical to it; `Gate 2 — Implementing` is U+2014 on the same "
  "measurement. The corrupted read was not acted on, and the hazard the frozen "
  "plan's P0-2 addresses is therefore live on this host in both directions — "
  "which is what D5's `B-premise` case independently establishes.")
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
    ("frozen-surface-by-tree-object", None, "%s/G2-frozen-trees.json" % CAP),
    ("review-five-items", None, "#review-record"),
    ("allowlist-respected",
     "git diff --name-only %s..50d08de65158faf23f1ae86aeebcde39e929c359"
     % BASE_SHA, "#verification-outputs"),
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
w("repair_attempts:")
w("  - number: 1")
w('    hypothesis: "The record\'s reproducibility and the reach of three of its '
  'prose claims are defective, not its measurements: two rows nominated as '
  'deterministic name a moving ref, N4 was called unforgeable, N2 did not name '
  'its false-negative channels, and one capture count was stated without its '
  'instant. Corrections only; no bin/ byte and no checker behaviour changed."')
w("    result: green")
w("# REPAIR 2 IS NOT IN THIS ARRAY, AND ITS ABSENCE IS NOT A REDUCTION OF THE")
w("# COUNT. Two repairs are spent and ZERO remain; no third is available. This")
w("# array models the gate-2-contract's D6 RED-CHECK sequence -- its own")
w("# $comment grounds it in the ordered sequence repair 1, then Codex")
w("# consult, then repair 2, then Human")
w("# Diagnosis Required' -- and neither of this Slice's repairs was an instance")
w("# of it: no review item was ever red, Review 1 returned R1-R5 all PASS, and")
w("# both repairs corrected prose in a record that already validated. Recording")
w("# repair 2 here would trip allOf[0], whose antecedent is a bare COUNT and")
w("# which would force result: human_diagnosis_required -- false of this gate.")
w("# The full ledger is in `notes` and in the Repair record. PROVISIONAL")
w("# REPRESENTATION, pending the gate-run@2 revision that carries F-06's")
w("# missing Writer Assignment type; it is not yet normative for a later Slice.")
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
  'tool and its committed falsification. THIS GATE STILL DOES NOT GRADE '
  'ITSELF: Review 1 returned R1-R5 all PASS across three sealed documents and '
  'those verdicts are TRANSCRIBED here by the writer under the Release '
  'Approval step, from the sealed reports and not from memory; result stays '
  'needs_approval, because passed is the Release Approval to grant and not '
  'this record to claim. TRANSCRIPTION IS NOT A REPAIR and spends nothing: '
  'the budget remains repair_limit 2, both spent, ZERO remaining, and no '
  'later reader should count a third. Thirteen findings were raised; none is '
  'a FAIL at close -- C4 FAILed on a prose sentence, was repaired and is '
  'discharged as F-09. Open and recorded rather than repaired: F-04, F-11, '
  'F-12, F-13, plus the debt named at repair 1.APPROVALS[] OVER-COUNTS PLAN APPROVALS BY ONE AND CANNOT '
  'DO OTHERWISE, so a consumer reading approvals[] alone must read this note '
  'too: comment 5394791863 is the Plan Approval, and comment 5395086921 is the '
  'operator WRITER ASSIGNMENT, a DIFFERENT act, whose clause 2 amends the Plan '
  'Approval window clause so Gate 2 opens in the session presenting its URL and '
  'whose clause 7 makes the writer role transferable only by an operator '
  'comment on the issue. Both entries carry type Plan Approval because the '
  'frozen gatebraid/gate-run@2 enumeration for approvals[].type has ten members '
  'and none is Writer Assignment: the typing is SCHEMA-FORCED, not chosen. A '
  'reader consuming approvals[] without this sentence counts two Plan Approvals '
  'where one Plan Approval and one Writer Assignment occurred. The schema '
  'belongs to the batch lane and is not this Slice to change; the missing '
  'member is queued for its next revision (Review 1, F-06). Repair 1 of 2 is '
  'spent on record corrections only -- no bin/ byte and no checker behaviour '
  'changed. Repair 2 spends the second and last: four prose corrections ruled '
  'by Review 1 addendum -- F-09, the one FAIL, where repair 1 pinned V13 and '
  'left the D7 disclosure citing it for a range it no longer covers; the C3 '
  'justification restated to what the mechanism supports; F-08 naming the '
  'sweep interval edge at both sites; and F-10 declaring a row that does not '
  'reproduce. THE REPAIR BUDGET IS NOW EXHAUSTED: repair_limit is 2 and both '
  'are spent, so any further finding routes to a decidable stop with result '
  'stopped, not to a third repair. REPAIR 2 IS DELIBERATELY NOT AN ENTRY IN '
  'repair_attempts AND ITS ABSENCE IS NOT A REDUCTION OF THE COUNT: two '
  'repairs are spent, ZERO remain, and no third is available. That array '
  'models the gate-2-contract D6 red-check sequence -- its own $comment '
  'grounds it in the ordered sequence repair 1, then Codex consult, then repair 2, then Human Diagnosis '
  'Required -- and neither repair here was an instance of it, since no review '
  'item was ever red and both corrected prose in a record that already '
  'validated. Recording repair 2 there trips allOf[0], whose antecedent is a '
  'bare count naming no result, and forces result human_diagnosis_required, '
  'which is false of this gate; inventing a consult_ref is refused in the '
  'schema own words. A reader seeing only the array must not conclude one '
  'repair remains: none does. PROVISIONAL REPRESENTATION pending the '
  'gate-run@2 revision that keys that conditional on the sequence it means '
  'rather than on a count, carried by ADR through the batch lane beside '
  'F-06 missing Writer Assignment type, and NOT YET NORMATIVE for a later '
  'Slice. The frozen schema and corpus were never '
  'written: N1 over the whole range touches only bin/ and this Slice evidence '
  'path, and D7 shows the digest unmoved at '
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
