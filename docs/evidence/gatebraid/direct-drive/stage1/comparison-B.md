# Verdict comparison - replay B against the recorded FINAL review

Trial stage 1, act C entry 2. The headless reviewer re-performed the Slice
P2-S6 Gate 2 review from the object database at the recorded CLOSING head
`73e489f1976f4b360858b27e4ef1fdaf5501b8f7`, under the read-only profile
`2812c249644a4241fee431f6f654347330dba031f79406ccd90364dcc28792ca`, and wrote
its own report. This file compares words. It rules on nothing: the coordinator
rules on every `DIFFERS` from the cause the replay's report states.

## What is compared

| side | source | measured |
|---|---|---|
| recorded | `_handoff/batch-p2s6/REVIEW-P2S6-G2-FINAL.md`, the five-row table at lines 21 to 25 | sha256 `2cf44ec8656d568573d3aa342185ac5ac4725b62e4af229a1538b7686d94bb68`, 20,795 B |
| replay | `_handoff/batch-stage1/REPLAY-B-REPORT.md`, the five-row table at lines 34 to 38 | sha256 `32f0aec3a057f4d6e0add2b8481fa3600a2d2bd71ed9b48474c71c58cae16e14`, 55,662 B |

The run record is `_handoff/outbox-c/REVIEW-DISPATCH-P2S6-G2-REPLAY-B.md.run.json`
(sha256 `4445a9b714959b56db66d15724591333044052c68cc3e2967dfca5a242228b06`,
18,070 B): outcome `completed`, `exit_status` 0, `head_before` equal to
`head_after` equal to `c0c737d36fd1d3303e3c7562273add804eca812c`, both
porcelain lists empty, so the post-run rule passed.

## The comparison

| item | recorded verdict | replay verdict | comparison |
|---|---|---|---|
| R1 | PASS | PASS | EQUAL |
| R2 | PASS | PASS | EQUAL |
| R3 | PASS | FAIL | DIFFERS |
| R4 | PASS | PASS | EQUAL |
| R5 | PASS | PASS | EQUAL |

Four rows equal, one differs.

## The recorded rows, quoted

    line 21  | **R1** allowlist confinement | **PASS** |
    line 22  | **R2** test-plan coverage | **PASS** |
    line 23  | **R3** evidence is rows that reproduce | **PASS** |
    line 24  | **R4** the negative criteria | **PASS** |
    line 25  | **R5** no prohibited action | **PASS** |

## The replay rows, quoted

    line 34  | R1 | PASS |
    line 35  | R2 | PASS |
    line 36  | R3 | FAIL |
    line 37  | R4 | PASS |
    line 38  | R5 | PASS |

## The one row that differs, and the cause the report states

The replay's report gives four grounds for R3, of which the first two are the
moved world the brief anticipated. Stated in the report's own terms:

1. Row E4's first command names `HEAD`, is nominated inside the record's own
   deterministic subset as reproducing byte-identically, and is neither pinned
   to a commit nor excluded. It returned the branch this batch works on where
   the record had the Slice branch.
2. Row E3's first command names the mutable remote-tracking main ref, also
   in-subset and unpinned. It returned the merge this milestone landed where
   the record had the head of its own day.
3. Rows E2, V5 and V6 read live control-plane state, in-subset with a
   byte-identity claim, neither pinned nor excluded.
4. One disclosure is prose about the file's own revision history.

Grounds 1 and 2 are measured consequences of reading a mutable ref at a later
instant. Grounds 3 and 4 are not. The coordinator rules on all four.

The replay records that everything else in R3 holds: nine pins verified, both
hashes recomputed exactly, five elisions each carrying a shown count, a total
and a resolvable committed path, and row V7 reproducing byte-identically.

## Provenance of this file

Written by the stage-1 audit window from the two sources named above, both
hash-verified at the instant of writing. No file on either side was edited.
The replay's report and its stdout stream carry closed-set residue and stay on
the ignored lane, named with their sha256 in the audit report; this comparison
and the run record are the committed carriers of the five words.
