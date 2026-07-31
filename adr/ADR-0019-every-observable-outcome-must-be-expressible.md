# ADR-0019 — Every outcome a gate can observe must be expressible in the record

**Status:** Accepted · M2 (2026-07-31) · Product: Gatebraid (ADR-0010)
**Extends:** ADR-0014 §2 (schema and template change together) and ADR-0013 §3
(a stopped gate must be writable as stopped). Both stand.
**Provenance:** Slice A's Gate 2 entry and Gate 3 (2026-07-31), friction #14 and
#23; ADR-0012 §4 (the evidence file records the negative).

## Context

Three times now, a gate has observed something true and had no way to write it
down.

- **ADR-0013 §3** — `templates/gate0-evidence.md` could express only a pass, so a
  Gate 0 that stopped could not be recorded at all, and "write nothing" became
  the only honest option.
- **Friction #14** — after ADR-0014 §1, the overwhelmingly common outcome of Gate
  2's baseline re-read is *the base branch changed, but only inside this slice's
  own evidence directory*. The template's enum has no value for it. Every slice
  hits this.
- **Friction #23** — `checks[].result` in `gatebraid/gate-run@1` admits
  `pass | fail | skipped | not_run`. CI was `none-configured`: no workflow, no
  check run, no status, none has ever existed. `pass` is forbidden by the
  template's own comment, `fail` is false, `not_run` implies a check exists that
  was not executed, and `skipped` implies a decision to skip one. The executor
  recorded `skipped` as least-wrong and explained the truth in prose.

In each case the executor did the right thing and the record got worse. The
prose is honest; but a value chosen as *least wrong* is indistinguishable, to
anything reading the record mechanically, from that value chosen because it was
right. ADR-0012 §4 already states the principle for one instance — "a gate that
quietly did not check looks identical to one that checked and passed" — and the
same collapse happens whenever the vocabulary is narrower than reality.

## Decision

**1. `checks[].result` gains `none_configured`.** It means: the thing this check
inspects does not exist in this repository. It is distinct from `skipped` (exists,
deliberately not run) and from `not_run` (exists, did not run). Per ADR-0011 §7 it
remains a **finding, not a pass**, and nothing may treat it as one.

**2. The Gate 2 baseline-re-read outcome gains
`changed-only-in-own-evidence`.** It is the expected outcome under ADR-0014 §1,
not an exception to be explained, and naming it separates *the common case* from
*no change at all* — which are different observations and should not share a
value.

**3. `ci-status` keeps its entry in the Gate 3 check list.** The alternative
considered was dropping the check and letting prose carry the finding. It is
rejected on ADR-0012 §4's grounds: an absent entry cannot be distinguished from a
check that was never performed, and the absence of CI in this repository is a
fact about the repository worth carrying in every slice's machine-readable
record, not a reason to stop recording.

**4. Standing rule.** When a contract defines an observation, the schema and the
template must be able to express **every outcome that observation can produce —
including "the thing being observed does not exist."** An enum narrower than the
observation space forces the executor to record a near-miss and repair it in
prose, and prose is not what a later reader greps.

This is the recording counterpart of ADR-0013 §1, which required every
*verification* to have a defined failure **disposition**. That rule says a gate
must know where to go; this one says it must be able to say what it saw. Both
failures look the same from outside — a gate that stops without a record, or
proceeds with a misleading one.

## Consequences

`schema/gate-run.schema.json`, `templates/gate2-evidence.md` and
`templates/gate3-evidence.md` change **in the same commit**, per ADR-0014 §2. The
enum additions are backward-compatible: no existing evidence file becomes
invalid, and Slice A's `gate3.md` is corrected from `skipped` to
`none_configured` as part of this change, with the correction noted in the file.

Adding vocabulary has a cost — an enum that grows once per incident is a
confession that the contract never specified the observation. Decision 4 is
therefore written as a design obligation at contract-writing time, not as
permission to extend enums reactively; the reopening condition below is the test.

## Reopening conditions

- **If an enum grows by one value per incident rather than one per class**, the
  observation itself is under-specified and the contract — not the enum — is
  what needs rewriting. Two consecutive slices each adding a value is the signal.
- If `none_configured` ever becomes the recorded value for a repository that
  *does* have CI, the check is inspecting the wrong thing and decision 1's
  definition is being used to paper over a lookup failure.
- If a gate ever needs a free-text outcome because no enumerable value fits, the
  observation is not a check and should not be in `checks[]` at all.
