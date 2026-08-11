<!-- Template: Codex consult file (ADR-0004, ADR-0021).

     PATH FOLLOWS SCOPE (friction #99 — a fixed path collided with every
     frozen allowlist a slice can have):
       - slice-scoped consult → docs/evidence/<product>/<slice_id>/<consult_id>.md
         in the working repo — inside the slice's own write_domains by
         construction, for any failure-triggered artifact.
       - milestone-level consult → consults/<consult_id>/ in the control repo.

     ID FOLLOWS SCOPE, AND IS VALIDATED BEFORE IT IS USED (friction #93):
     CONSULT-<issue#>-<seq> for slice-scoped, CONSULT-M<n>-<seq> for
     milestone-level (ADR-0021 §3). Before the id first appears in any
     filename, comment or reference, validate this file's completed metadata
     block against gatebraid/consult@1 with the real validator, loader named
     (friction #55) — the schema's root conditional binds the id form to the
     trigger's scope; run it, do not reason about it.

     THE CONSULTANT'S ACTUAL CONSTRAINTS, restated from measurement (friction
     #95, #103 and its CORRECTION; ADR-0028 §6). `--sandbox read-only`
     constrains the MODEL'S COMMANDS: it permits execution and forbids writes,
     and the Consultant has NO NETWORK. It does not constrain the CLI itself,
     which maintains session state: a `refs/codex/*` checkpoint ref has been
     observed in a governed repository, written from an interactive session
     into the repository named by `-C`. One measured run under the contract
     invocation form below produced ZERO such refs. Embed all evidence because
     the request must be a durable record and nothing may depend on a live
     service. GIVE the Consultant `-C` so it can check this packet's excerpting
     against the tree — that check is precisely the failure class it has caught
     (friction #96) — but STANDING RULE, precaution under uncertainty: `-C`
     points at a DISPOSABLE FULL COPY of the working repository, created
     outside every governed repository and deleted after the response is
     captured, so any ref the CLI writes lands in the copy. Invocation is
     hermetic: `codex exec --ephemeral --sandbox read-only
     --ignore-user-config` (a host config carries state, including a
     repository-directory trust table — friction #91), no bypass, snapshot
     disabled, response captured to a file by `--output-schema`/`-o`, never
     transcribed.

     The response is saved verbatim as <consult_id>-response.<ext>
     (sanitization disclosed if applied) and committed beside this file;
     linking follows scope (ADR-0021 §4) — from the Slice issue when
     slice-scoped, otherwise by citation from the documents that adopt its
     outcome. Recording in gate-run@1: an in-sequence consult →
     repair_attempts[].consult_ref; an HDR-directed consult → top-level
     consults[] only (friction #94). -->

# <consult_id> — <one-line problem title>

## Problem statement

<Precise statement of the failing behavior / decision needed.>

## Constraints and forbidden operations

<From the project's prohibited-operations overlay + slice metadata. The
Consultant must respect these in its recommendation.>

## Files in scope

- `<path>` — <why>

## Hypotheses already tried

| # | Hypothesis | Outcome |
|---|---|---|
| 1 | <…> | <…> |

## Embedded evidence

<Command outputs, test logs, stack traces, diffs — pasted in full or
committed-log referenced; every elision marked shown/total. This section,
plus the tree reached via -C, is the Consultant's ground truth.>

## Questions

1. <Explicit question 1>

## Required response schema

Respond in exactly this structure (gatebraid/consult@1 `response`):
`findings` · `root_cause_hypotheses` (ranked, each with file-path evidence) ·
`recommended_change` (patch sketch as suggestion text — do not apply anything) ·
`risks` · `verification_steps` · `confidence` (low|medium|high).

## gatebraid-metadata

```yaml
schema: gatebraid/consult@1
consult_id: CONSULT-<issue#>-<seq>   # milestone-level: CONSULT-M<n>-<seq>
slice_id: P<nn>-S<nn>   # slice-scoped triggers only — omit the key entirely otherwise
trigger: repair-sequence   # see consult.schema.json for the trigger list and which are slice-scoped
fingerprint_before: "<semantic git fingerprint>"
request:
  problem: "<one sentence>"
  constraints: ["<…>"]
  files_in_scope: ["<path>"]
  hypotheses_tried:
    - hypothesis: "<…>"
      outcome: "<…>"
  embedded_evidence: ["#embedded-evidence"]
  questions: ["<…>"]
```

<!-- After the response: the Lead independently verifies (reproduce reasoning,
     run verification steps) — NEVER blind-apply — then records the decision
     footer on the response file and completes the yaml with:
       response: {...}   decision: {verdict: ACCEPT|PARTIAL|REJECT, reasons, independently_verified, rebuttal_rounds}
       fingerprint_after: "<...>"
     Maximum one structured rebuttal round each; persistent disagreement →
     decision memo + minimal discriminating experiment → Human Diagnosis Required. -->
