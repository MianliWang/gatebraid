# ADR-0027 — Three borrowings from the Prime Agent survey, and one more name on the never-install list

**Status:** Accepted · M2 (2026-08-09) · Product: Gatebraid (ADR-0010)
**Amends:** the Gate 2 repair sequence (gate-2-contract, executed same
batch); `gatebraid/handoff@1` and `templates/handoff.md` (executed same
batch); extends ADR-0009's never-install set by name (ADR-0009 itself is
frozen with the M1 set; this ADR is the durable record of the extension).
**Provenance:** the coordinator's survey of Prime Agent (Prime Intellect;
announced 2026-08-05, MIT), from a read-only depth-1 clone of
`github.com/PrimeIntellect-ai/prime-agent` on 2026-08-08 plus the project's
announcement and RLM posts and arXiv:2605.09998. The survey itself is
session material; the facts this ADR relies on are restated here so the
decision is durable without it (ADR-0001). Friction #86 (a practice applied
to the instance and never generalised to the class); friction #37 (full
values, never prefixes); Batch H's session-loss reconstruction; RB-M2-J.

## Context

Prime Agent is an external coding/research harness whose published results
rest on mechanisms, not model access. Three of those mechanisms solve
problems Gatebraid has now measured on its own record, and the survey found
independent convergence on designs Gatebraid already committed — their
unchanged-failed-gate detection beside the new-hypothesis rule (ADR-0002
§4), their explicit `goal.complete()` transition beside closure-is-explicit
(ADR-0012), their immutable-base-prompt rule beside reference-don't-restate
(ADR-0017), their trajectory-replay recovery beside the ADR-0001 recovery
set. Independent convergence from a performance-driven team is evidence a
design carries weight beyond governance taste — and it is also the reason to
borrow the three mechanisms Gatebraid lacks rather than reinvent them.
Adoption is by this ADR only; the harness itself is never run here.

## Decision

**1. Repair novelty gains a mechanical floor.** Their harness does not rerun
an unchanged failed gate; the attempt count advances instead. Adopted:
before a repair attempt's `result` is recorded, the tree is measured —
`git rev-parse HEAD^{tree}` — against the tree at the previous failed state
(the failing review for repair 1, the prior attempt otherwise). **An
unchanged tree is not a repair:** the attempt is recorded as consumed,
`result: still_red`, hypothesis annotated `(unchanged-tree)`, and the
sequence advances without a re-review. The new-hypothesis rule (ADR-0002 §4)
keeps its semantic force above this floor — a changed tree with a recycled
hypothesis still fails review; an unchanged tree no longer costs one.
Executed in gate-2-contract this batch; a guard-side check joins the
enforcement queue (ADR-0020 §6).

**2. Handoffs carry a `preserve_verbatim` field.** Their compaction pins
operator instructions and exact strings so summarization cannot erode them.
Adopted: `gatebraid/handoff@1` gains optional `preserve_verbatim: []` —
hashes, SHAs, ids, exact commands, door-comment URLs; the items that must
survive any summarization, compaction or relay **byte-exact**. A consumer
carries a listed item mechanically or cites the comment; a paraphrase of a
listed item is a defect. This is friction #37's full-values rule applied at
handoff scale, and it makes the next Batch-H-class reconstruction cheaper
than the last one. Executed in schema + template this batch.

**3. Lessons are local until promoted.** Their harness scopes learned
refinements to the session by default; promotion to global is a separate
explicit act. Adopted as the rule Gatebraid already almost keeps: a lesson —
a friction entry's suggested fix, a working practice adopted mid-batch — is
**working material with no normative force until a batch lands it in a
committed artifact.** The friction log is the queue, never the rule book.
Friction #86 is the measured cost of the alternative: a practice adopted at
the instance (#61's guard) sat five batches beside the unguarded class it
should have covered, precisely because practices do not generalise —
committed text does. Corollary, binding on the coordinator: a queued fix is
re-read from its friction entry when drafted, never from memory.

**4. Prime Agent joins the never-install list by name.** Never installed or
executed in any milestone; specification-level reference only — the
ADR-0009 stance, extended to: Spec Kit, GSD, CCPM, BMAD, Superpowers,
Paperclip, Hermes, **Prime Agent**. Reasons on the record: its installer
pipes curl to sh; its kernel executes model-generated code with user
permissions (its own README disclaims sandboxing); and a resident agent
harness is exactly the co-resident-agent class ADR-0024 §3 bars from
Gatebraid's surfaces. The host standing briefs (`CLAUDE.md`,
`_handoff/M1-STATUS.md`) are updated to carry the name at this batch's
close.

**Recorded as considered and not adopted:** self-applying refinement
(violates Manual approval mode; unreviewed edits to operative text are the
term-4 drift class); heartbeat / autonomous continuation of gate execution
(ADR-0015 bars unattended gates). **Deferred, not rejected:** their
refinement-event record shape and compute-don't-paste skill rule (the
skills batch), their fixed-order budget/limit semantics (the
operating-rhythm work); their subagent topology (design note only,
ADR-0015-gated). Each enters, if ever, by its own approved change.

## Consequences

- The repair sequence acquires its first fully mechanical step; reviewer
  vigilance is spent on semantic novelty only.
- Handoff consumers — fresh sessions, the coordinator, any future
  summarizer — have a machine-checkable list of what must not be
  paraphrased.
- The never-install list's durable home for post-M1 additions is this ADR
  (and successors), since ADR-0009 is frozen.

## Reopening conditions

- Any further survey item proposed for adoption — its own ADR or batch
  approval, never a rider.
- The novelty floor meeting a repair class for which the tree hash is the
  wrong instrument (e.g. a repair legitimately confined to an untracked
  artifact) — that is a design change here, not a silent exemption.
- `preserve_verbatim` growing narrative — the same slow failure ADR-0026's
  disclosure class watches for.
