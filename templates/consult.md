<!-- Template: Codex consult file (ADR-0004). The Lead writes this file at
     docs/consults/CONSULT-<issue#>-<seq>.md (cross-project: in
     MianliWang/gatebraid/evidence/). The Consultant is READ-ONLY
     (--ephemeral --sandbox read-only, no bypass, snapshot disabled):
     ALL evidence must be embedded here — it cannot execute anything.
     The response is saved verbatim as CONSULT-<...>-response.md (sanitization
     disclosed if applied), committed, linked from the Slice issue. -->

# CONSULT-<issue#>-<seq> — <one-line problem title>

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
committed-log referenced. This section is the Consultant's only ground truth.>

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
consult_id: CONSULT-<issue#>-<seq>
slice_id: P<nn>-S<nn>
trigger: repair-sequence   # see consult.schema.json for the trigger list
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
