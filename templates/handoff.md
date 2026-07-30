<!-- Template: structured handoff comment (gatebraid/handoff@1), posted on the
     Slice issue at every gate completion / checkpoint. This is the mandatory
     trailer: report-10 shape (changed_files, verification with owners,
     residual_risk) plus decisions. Verification shows evidence, not assertion.
     A fresh session resumes from this comment + Project fields + committed
     evidence + Git state alone (ADR-0001). -->

**Handoff — <P_nn-S_nn> · Gate <N> · <short outcome>**

<One short human paragraph: where this Slice now stands.>

```yaml
schema: gatebraid/handoff@1
slice_id: P<nn>-S<nn>
gate: <0|1|2|3>
workflow_to: "<the Workflow option this transitions into>"
changed_files: []            # empty for read-only gates
verification:
  - command: "<check command>"
    owner: Claude Lead       # Human | Claude Lead | Claude Read-Only Team | Codex Consultant | CI
    result: pass             # pass | fail | skipped | not_run
    evidence_ref: "<evidence file anchor / CI url>"
residual_risk:
  - "<concrete remaining risk>"   # empty array = explicitly claiming none
decisions:
  - "<decision taken, with rationale or link (incl. consult ACCEPT/PARTIAL/REJECT)>"
done:
  - "<completed item>"
next:
  - "<next action>"
open_questions: []
```
