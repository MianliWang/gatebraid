# ADR-0026 — Evidence states measurements, not narratives

**Status:** Accepted · M2 (2026-08-09) · Product: Gatebraid (ADR-0010)
**Amends:** the four `templates/gate[0-3]-evidence.md` (rewritten under this
ADR in the same batch) and gate-2-contract R3's subject. ADR-0018 §2/§2a
stand and are satisfied structurally by this design. ADR-0017 (the composite
record) and ADR-0019 (expressibility) are the parents this ADR applies at
the evidence layer.
**Provenance:** the P1-S3 and P1-S5 measurement — implementation green in
every review of both attempts and untouched by every repair, while R3 failed
eight consecutive times across four repairs, two directed rewrites and one
independent consult, every failure in prose self-description; friction #70
(three reviews, three R3 failures, all in prose about the file itself), #87,
#88, #96 (the defect class reproduces inside its own remedy — three measured
instances); #96's byte-mismatch caught only by regeneration; the
convergence-metrics §5 divergence signature firing with all defect mass
localized to the narrative layer (RB-M2-J); CONSULT-14-01; independent
convergence in an external harness survey — "skills compute state, never
paste state" (the survey's durable record is ADR-0027).

## Context

Two attempts at one slice produced a controlled experiment. The work was
correct both times. What failed, every time, was the evidence file's prose
about its own process — and each layer of remedy (repair, directed rewrite,
consult-verified rewrite) produced fresh instances of the defect class it was
correcting. A divergence signature whose entire defect mass sits in one
content class is not a call for more clauses governing that class; it is a
call to remove the class. The current templates invite narrative — approach
recaps, remediation stories, self-assessments — and narrative written by the
executing party about its own conduct has now been measured as unwritable at
this standard, independent of effort, discipline, or prediction.

## Decision

**1. An evidence file consists of exactly these content classes, and nothing
else.**

- **(a) The metadata block** — the gate-run@1 yaml, unchanged in role.
- **(b) Record rows.** Each row is a one-line label, a `$ command` line, and
  that command's output. The command line carries its environment visibly
  (friction #89). The output is **generated from the command, never
  transcribed** (friction #96); for the deterministic subset (`git diff`,
  `git rev-parse`, `grep`/`rg` over committed content, hash computations)
  the file's own generation records a byte-identity assertion, and R3
  re-runs it. Long outputs may live at a committed path, referenced from the
  row; every elision carries `shown/total` and that path.
- **(c) Required disclosures**, enumerated by the template and nowhere
  else: deviations (one line each, citing the friction entry or ruling),
  reviewer write disclosure, environment statement.
- **(d) Template-fixed headings and the rows' one-line labels.**
- **(e) At Gate 1 only: the frozen-plan section** — approach, exact
  allowlist, test plan, risk notes, rollback note, negative criterion. It is
  the design artifact the plan hash covers, not a record of conduct, and it
  is the one class where prose is expected. After the freeze it is cited,
  never re-described.

**No narrative sections. No statements about the file's own revision history
or prior reviews — the per-review recorded rows are the only record. No
explanatory prose.** Rationale lives where it already has durable homes:
commit messages, handoff comments, the friction log, consult records.
Template comments are authoring instructions and are **deleted at
instantiation**; a comment surviving into an instantiated file is content
outside the classes.

**2. Quantified and universal claims exist only as rows.** ADR-0018 §2a is
thereby satisfied by construction rather than by vigilance.

**3. Attribution is machine-derivable or absent.** A statement attributing a
decision, finding or recommendation to any party carries the citation a
machine can check — comment id, response line — or is not written. (Four
measured instances of right-disposition-wrong-stated-reason on one slice.)

**4. R3's subject is redefined to match** (gate-2-contract amendment, same
batch): R3 passes iff every row's output reproduces — byte-identical for the
deterministic subset — and the file contains no content outside classes
(a)–(d), plus (e) where the gate defines it. R3 becomes predominantly
mechanical, which is the point: the surface on which prose could be false is
removed rather than policed.

**5. One review heuristic becomes normative:** the fix for X is the first
place to look for a fresh X (#87, #88, #96 — three instances). Reviewers
check the remedy's own section against the defect class it remedies, first.

## Consequences

- The four evidence templates are rewritten to this shape in this batch; the
  diff is subtractive in total normative surface, which is the response
  §5's divergence signature calls for.
- A slice's evidence becomes regenerable and byte-checkable end to end;
  reviews get faster and their verdicts get harder.
- What evidence loses in readability, handoffs and reports retain — those
  are written for readers and remain prose, outside R3's subject.

## Reopening conditions

- A content class genuinely needed by a gate that (a)–(e) cannot carry.
- The deterministic-subset byte check meeting a command class that matters
  and cannot be made deterministic — that is a design change here, not a
  silent exemption.
- Any measured return of narrative through the disclosure class — one-line
  disclosures growing paragraphs is this ADR failing slowly.
