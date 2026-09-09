# REVIEW DISPATCH (headless replay, trial stage 1) - Slice P2-S6 Gate 2, items R1-R5, at the recorded FIRST-review state

You are a headless Claude Code run started by `bin/gatebraid-dispatch.py`
(contract `protocols/direct-drive-v1.md`) under the read-only profile, in
the control repository `D:/Github repo/Gatebraid`, for exactly one job:
perform the gate-2 contract's read-only Review - items R1 to R5 - of Slice
P2-S6 as it stood at one recorded instant, reading that state from the
object database, and write one report. This is ADR-0034 decision 9, trial
stage 1: the Slice is closed and its review was performed and recorded by
a pasted session weeks ago; your run is the same review performed without
a human relay. Afterwards the coordinator compares your verdicts with the
recorded ones, byte by byte. You have not seen the recorded review and you
must not look for it (below). You authored nothing under review and will
author nothing.

Read `protocols/gate-2-contract.md`, section Review, fresh from the
committed tree before acting - its R1-R5 definitions govern; this dispatch
adds pins, carried rulings and pre-briefs, never substitutes. Read
`adr/ADR-0026-*.md` and `adr/ADR-0028-*.md` for the classes and the
deterministic-subset rule R3 rests on.

## Mandate (state these rules in your report)

1. Read-only. Your one intended write is your report,
   `_handoff/batch-stage1/REPLAY-A-REPORT.md` (the Write tool, then the
   Edit tool for the self-measure appended at the end). The profile admits
   editing tools under `_handoff/batch-stage1/` only; if the Write is
   refused, put the entire report in your final message instead, beginning
   with the line `REPORT-IN-FINAL-MESSAGE`, and stop. Any other write you
   make, anywhere, is disclosed in the report naming the path.
2. Do not read `_handoff/batch-p2s6/REVIEW-P2S6-G2.md`,
   `_handoff/batch-p2s6/REVIEW-P2S6-G2-REREVIEW.md`,
   `_handoff/batch-p2s6/REVIEW-P2S6-G2-FINAL.md`, `_handoff/friction-log.md`,
   anything under `_handoff/prompts/`, or anything under
   `_handoff/batch-stage1/` other than the report you write - by any tool,
   including `sed`, `grep` and `git show`. The recorded review must not
   inform yours. State in your report that you did not.
3. No checkout, no switch, no stash, no worktree: every historical read is
   `git show <sha>:<path>`, `git diff <sha>..<sha>`, `git log`,
   `git cat-file`, `git ls-files --with-tree` or `git rev-parse`. The
   working tree stays exactly as found; you never change which commit is
   checked out.
4. Scratch, if you need any, only under `D:/gb-scratch-stage1/replay-a/`
   - a directory where `git rev-parse --show-toplevel` fails; create it and
   write there only with `python -B`; list every file you create there in
   the report. Prefer pipes to files: `git show <sha>:<path> | sha256sum`
   compares a blob without writing it.
5. The dispatcher set `GH_CONFIG_DIR` (to `C:/Users/rough/.gh-gatebraid`,
   the dedicated read store) and `PYTHONDONTWRITEBYTECODE=1` in your
   environment: verify both once with
   `python -B -c "import os; print(os.environ.get('GH_CONFIG_DIR'), os.environ.get('PYTHONDONTWRITEBYTECODE'))"`
   and never prefix a command with a variable assignment - a command that
   begins with `NAME=value` does not match the profile's rules and is
   refused. `gh` reads only, through `gh pr view`, `gh issue view` and
   `gh api repos/MianliWang/gatebraid/...` (endpoints without a leading
   slash; `gh pr list` is not admitted - use the `pulls` endpoint of the
   API with query parameters instead). No `gh` mutation of any kind. Closed
   repository set: `MianliWang/gatebraid` and `MianliWang/gatebraid-scratch`.
6. Every Python invocation carries `-B`; no `py_compile`; bytecode that
   appears is disclosed (you cannot remove it: `rm` is denied; say where it
   is).
7. Measure, never declare - every verdict cites the command and its output.
   Cite, never restate. A bare zero states what it searched. Full 40-hex
   SHAs. Friction ordinals stay unclaimed. ASCII only in the report, plus at
   most the code points U+00A7, U+00B7, U+2013, U+2014, U+2026, U+2192.
8. No subagent: the profile admits none, and you do not ask. Work alone,
   in order, and budget your turns: the dispatcher ends you at
   800 turns or 10,800 seconds. If you cannot finish, write
   the report with what you have, the line `INCOMPLETE` and the item you
   stopped at; a partial report with true rows is worth more than none.
9. On any uncertainty about a rule, do the conservative thing, record it
   as a finding, and continue; there is no one to ask.

## The moved world (read this before measuring anything)

The Slice is closed: after the recorded instant its branch was pushed,
its pull request was opened and merged, and `main` has moved on several
times since. So: the reviewed head is an ANCESTOR of today's `HEAD`, not
`HEAD`; `slice/P2-S6` exists on origin today although it did not at the
recorded instant; the working tree today is not the working tree then;
the live Project fields are not the fields then. Every item below says
which of its measurements are read from immutable objects (a commit, a
blob at a commit, a comment by id) and which are live. A live measurement
whose value today differs from what the recorded state implies is entered
in the report's MOVED-WORLD REGISTER with the cause you measured (a
timestamp, a later commit, a merge), and the item's verdict is ruled on
the recorded state, with that cause stated. A difference with no stated
measured cause is a finding, never a shrug.

## The recorded state (verify every pin before using it)

- Base `3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8` (`main` at the recorded
  instant). Reviewed head `44906edc4d49cc090673a2220d3b66246b187bca` (state its tree from `git rev-parse 44906edc4d49cc090673a2220d3b66246b187bca^{tree}`).
  Verify `git merge-base --is-ancestor 44906edc4d49cc090673a2220d3b66246b187bca HEAD` (exit 0) and print
  `git rev-parse HEAD` so the report states today's head.
- Recorded instant: `2026-08-30T04:50:27Z` (the coordinator measured it from the
  recorded report's own modification time; use it for every ordering
  question below).
- Record under review: `docs/evidence/gatebraid/P2-S6/gate2.md` AT the
  reviewed head - `git show 44906edc4d49cc090673a2220d3b66246b187bca:docs/evidence/gatebraid/P2-S6/gate2.md`
  - sha256 `8f23326e1f9087327cedf84840a087d9a8afec9aa62ff37f814d16b6fecf7211`, 28,726 bytes. Measure it by piping to
  `sha256sum` and `wc -c`. Never review the working-tree copy: it is a
  later state.
- Frozen at Gate 1 (`docs/evidence/gatebraid/P2-S6/gate1.md`, sha256
  `47b5bc56c350d71829909aec881f51e5e215dad9dcf59c2ff1e4128ca38fc6b3`,
  39,830 bytes): `plan_hash`
  `4435c71eaf08bf0605815e5960c8093c4698babf99ae8a7030d05ebe445671d0`,
  `allowlist_hash`
  `8938efcce4b8b863b14f7a503c808d7c2c67d2975aad180fd153fd45cc6da291`,
  `write_domains` = `bin/` and `docs/evidence/gatebraid/P2-S6/`. Gate 0
  record `gate0.md` sha256
  `8f9e13a136b7e0836254535138694e5913214c7ffee58f11e36e71c68d97732f`,
  39,514 bytes. Both records at the reviewed head must carry those values.
- Plan Approval comment `5466316139` on issue `#19` (author `MianliWang`;
  names both hashes - fetch it by id and check).
- The build window's lease at the recorded instant:
  `RoughEgoist:claude-p2s6-executor:2026-08-30T02:58:49Z`. The live
  `Writer Lease` field is a moved-world value; the lease string inside the
  branch's write domains at the reviewed head is not.
- What this run is for: the recorded review at this head was the FIRST
  review of the Slice, and it did not pass every item. You are not told
  which item or why. Find what the record supports; if every item passes
  for you, say so with the evidence - a verdict is never adjusted toward
  an expectation.

## Rulings carried into R1 (the operator's, on record - apply, verify, flag)

R1's porcelain half exists to catch writes created inside the gate
(friction #107). At the recorded instant two untracked sets were on record
as lawful: (1) the retained P2-S5 Gate-0 evidence - 43 files, every path
under `docs/evidence/gatebraid/P2-S5/`, sorted relative-path-list digest
`83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f`,
granted `Dirty Baseline Acceptance` in the Gate-0 opening comment
`5461039588`; (2) the Slice's own gate evidence under
`docs/evidence/gatebraid/P2-S6/`, inside `write_domains`. The porcelain of
the working tree at the recorded instant is NOT in the object database;
say so in R1, rule R1's diff half on the objects, and measure today's
porcelain once (`git status --porcelain --untracked-files=all`) for the
moved-world register only. Flag, as the recorded ruling asked, that R1's
letter and parked-Slice evidence interact.

## Pre-briefs, so design is not misread as defect

1. The record's Review section is EMPTY at the reviewed head and
   `review-five-items` is `not_run`; `Gate` reads `G1 passed`, `Workflow`
   `Needs Review` inside the record. Deliberate: the builder must not
   self-review. Not a defect.
2. B-3 seed substitution, disclosed by the builder: the Acceptance's
   parenthetical seed (C-3's frozen six-key element) is claimed to be a
   container row excluded before verdicts, so condition `LB-3` instead
   removes `workflow` from a row that reaches a verdict. Your R2 job:
   MEASURE the exclusion claim from the committed code and fixtures at the
   reviewed head, and rule whether `LB-3` demonstrates B-3's property
   (absent `workflow` gives UNKNOWN gives `undecidable`, never a KeyError,
   never a healthy default).
3. `connection_truncated` is used for bounded short reads - verify it is a
   member of the frozen `schema/snapshot.schema.json` enumeration at the
   reviewed head, and that NO `schema/` or `fixtures/` byte changed between
   the base and the reviewed head.
4. `slice_metadata_present` derives from a non-empty Project `Slice`
   field - stated by the builder so it can be disputed. Re-derive its
   ground from the frozen `live-shapes` provenance at the reviewed head
   (builder's count: 11 of 15 item elements carry `slice` and `workflow`;
   the 4 carrying neither are container rows) and give an explicit verdict
   on the reading.
5. Gate-2 instrument copies exist beside Gate 1's pinned originals - verify
   the G1-pinned originals did not move between Gate 1 and the reviewed
   head (in particular `checks-g0-closed-set-sweep.py`, pinned at
   `df7b756a…` by the G1 record; re-derive every pinned value from
   `gate1.md`'s own rows and compare the blobs at the reviewed head).
6. Among the captures under `docs/evidence/gatebraid/P2-S6/`, three Gate-0
   captures carry validator `fail`-typed placeholder-survives findings on
   faithfully recorded foreign text - a KNOWN defect of the validate tool,
   ruled out of this Slice's scope. The typed `fail` is the honest record,
   not a defect of this branch.

## The items (each verdict PASS or FAIL, with evidence)

**R1 - allowlist confinement.** `git diff --name-only 3d47f8be..44906edc4d49cc090673a2220d3b66246b187bca`
is a subset of the frozen `write_domains`; every commit between base and
the reviewed head named, its own diff confined; the porcelain half as the
carried ruling says.

**R2 - test-plan coverage.** Map every Acceptance checkbox on `#19` to its
declared command D1-D8, item by item, stating each mapping - the frozen
digest to D1; mutations killed and corpus unchanged to D2; transcripts
LS-01 to LS-07 and B-1 to B-4 to D3 (21 new live conditions, zero network
reads - verify the count and the no-network claim from the committed
transcripts and code at the reviewed head); the WSL half to D4; the
captured live smoke read and frontier consumption to D5 and D6; negative
criteria to D7 and D8. Include the B-3 substitution ruling (pre-brief 2).

**R3 - evidence is rows that reproduce.** The record at the reviewed head
contains nothing outside ADR-0026's classes. Every row the record places
in its deterministic subset is re-run and compared in BYTES against the
row's recorded output - re-run FROM THE OBJECT DATABASE: an instrument is
executed as `git show 44906edc4d49cc090673a2220d3b66246b187bca:<instrument> | python -B - <its recorded
arguments>` when it reads nothing else, and from the working tree only
after you have measured that every file it reads is byte-identical between
the working tree and the reviewed head (`git diff --stat 44906edc4d49cc090673a2220d3b66246b187bca HEAD --
<those paths>` empty), stating which you did for each row. A row whose
comparand is mutable - `HEAD`, the working tree, `git status`, `origin` -
is judged by ADR-0028 decision 2 exactly as the record treats it: pinned to
a SHA, or excluded from the deterministic subset and said so; a row that
does neither fails R3, whatever its bytes do today. Non-deterministic rows
are checked against their stated load-bearing property; every elision
carries its shown count, its total, and a committed full-output path; the
remedy section is checked first against the defect class it remedies.

**R4 - the negative criteria.** Re-run D7 (expect exit 0, all five HOLD)
and D8 (expect exit 1, all five FIRED) with the recorded arguments, from
the instrument at the reviewed head; check that each of N1-N5 states the
pattern it proxies for and the direction it errs, and that where a proxy
over-matches, the pattern governs. Where D7's changed-path set is derived
from the working tree, say so and measure the effect (the moved world).

**R5 - no prohibited action, AS OF the recorded instant.** Today
`git ls-remote --heads origin slice/P2-S6` may return the branch and a
pull request for it exists: establish from the pull request's own
timestamps (`gh api "repos/MianliWang/gatebraid/pulls?state=all&head=MianliWang:slice/P2-S6"`
- `created_at`, `merged_at`) and from the Gate 3 record at today's `HEAD`
(`docs/evidence/gatebraid/P2-S6/gate3.md`) when the push happened, and
rule R5 on whether any push, pull request, dependency change, hook change,
second lease, or `reset`/`clean`/`checkout` against the baseline state
existed BEFORE `2026-08-30T04:50:27Z`. Cite `git log -g slice/P2-S6` (the reflog walk)
if the local branch still exists, `.git/hooks/` (count the active hooks
with Glob and Read), and the N4 baseline comparison for dependencies.

**Plus, standing pins:** recompute `plan_hash` and `allowlist_hash` from
`gate1.md` at the reviewed head by its own recorded commands - both
unchanged; byte pins of `gate0.md` and `gate1.md` unmoved between Gate 1
and the reviewed head.

## Report, then stop

Write `_handoff/batch-stage1/REPLAY-A-REPORT.md` with, in this order:
the header (executor `Claude Read-Only Team, headless`; subject head; base;
today's head; the record's measured sha256 and byte count; the recorded
instant); the verdict table - exactly five rows, `| R1 | PASS |` through
`| R5 | FAIL |` in that shape, one verdict word per row, followed by the
evidence citations; the findings, labelled `F-1`, `F-2`, ... in your own
numbering (a mismatch is data, never bent - this dispatch included); the
MOVED-WORLD REGISTER; the mandate rules as given; every write you made
(`none` or the list); every file you created under the scratch directory;
the files under `_handoff/` you read (the list, which must not include the
five forbidden ones); the repository state you leave behind (today's head
unchanged, working tree as found, measured after your last command);
`INCOMPLETE` and the item, if so; then the line
`<!-- self-measured region ends -->` and, appended after it with the Edit
tool, the sha256 and byte count of everything above that line, measured
with `sed -n '1,/^<!-- self-measured region ends -->$/p' <path> | sha256sum`
and the same pipe into `wc -c`. Then stop. Nothing about the Slice is yours
to change: it is closed, and the comparison is the coordinator's.
