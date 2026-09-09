# Verdict comparison - replay A against the recorded FIRST review

Trial stage 1, act C entry 3. The headless reviewer re-performed the Slice
P2-S6 Gate 2 review from the object database at the recorded FIRST-review head
`44906edc4d49cc090673a2220d3b66246b187bca`, under the read-only profile
`2812c249644a4241fee431f6f654347330dba031f79406ccd90364dcc28792ca`, and wrote
its own report. The replay text does not say which item the recorded review
failed. This file compares words. It rules on nothing: the coordinator rules on
every `DIFFERS` from the cause the replay's report states.

## What is compared

| side | source | measured |
|---|---|---|
| recorded | `_handoff/batch-p2s6/REVIEW-P2S6-G2.md`, the section 1 verdict table at lines 70 to 74 | sha256 `76ef86a1293755f99351236e0e86301082067ade6ce7ef47db1108bf479225de`, 46,091 B |
| replay | `_handoff/batch-stage1/REPLAY-A-REPORT.md`, the five-row table at lines 36 to 40 | sha256 `49776f06c466b9a862c51d634fbfe4366c4cf201fb18627972d9b4df96b4d1cf`, 57,052 B |

The run record is `_handoff/outbox-c/REVIEW-DISPATCH-P2S6-G2-REPLAY-A.md.run.json`
(sha256 `2d841af7a81fa4049e12f5b0c0ec758a4deb8b749fb52c6695eb562aca943a8a`,
18,062 B): outcome `completed`, `exit_status` 0, `head_before` equal to
`head_after` equal to `c0c737d36fd1d3303e3c7562273add804eca812c`, both
porcelain lists empty, so the post-run rule passed.

## The comparison

| item | recorded verdict | replay verdict | comparison |
|---|---|---|---|
| R1 | PASS | PASS | EQUAL |
| R2 | PASS | PASS | EQUAL |
| R3 | FAIL | FAIL | EQUAL |
| R4 | PASS | PASS | EQUAL |
| R5 | PASS | PASS | EQUAL |

All five rows equal. Nothing differs.

## The recorded rows, quoted

The recorded table carries a third column of evidence prose. The item and
verdict cells are quoted; the evidence cell is elided at the second cell
boundary and is present in full in the cited file at the cited lines.

    line 70  | **R1** allowlist confinement | **PASS** | ...
    line 71  | **R2** test-plan coverage | **PASS** (with F-04, F-05, F-06, F-07) | ...
    line 72  | **R3** evidence is rows that reproduce | **FAIL** | ...
    line 73  | **R4** the negative criteria | **PASS** | ...
    line 74  | **R5** no prohibited action | **PASS** | ...

The recorded review's own disposition line, line 7, reads: `**Disposition:**
**R3 FAILS.** R1, R2, R4, R5 pass.`

## The replay rows, quoted

    line 36  | R1 | PASS |
    line 37  | R2 | PASS |
    line 38  | R3 | FAIL |
    line 39  | R4 | PASS |
    line 40  | R5 | PASS |

## What this run demonstrates

Read beside the companion comparison for replay B, this is the falsification
in the other direction that the brief asked for. The same headless reviewer,
the same profile, the same instrument, at two recorded states of one Slice:
at the first-review state it returns the recorded FAIL, and at the closing
state it returns a verdict of its own rather than echoing the recorded PASS.
The instrument is shown able to fail as well as to pass, and its agreement
here is agreement it could have withheld.

The replay reached its FAIL on four grounds of its own, not by reading the
recorded verdict: the report records that no file under the ignored lane was
read at all, and the transcript audit confirms no input to any tool named the
three recorded reviews, the friction ledger or the prompts directory.

## Provenance of this file

Written by the stage-1 audit window from the two sources named above, both
hash-verified at the instant of writing. No file on either side was edited.
The replay's report and its stdout stream carry closed-set residue, and the
report carries one handoff-block schema token and the stream one code point
outside the permitted set; both stay on the ignored lane, named with their
sha256 in the audit report. This comparison and the run record are the
committed carriers of the five words.
