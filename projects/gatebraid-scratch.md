# Project registration — gatebraid-scratch

Registration record (`gatebraid/project@1`) for the scratch repository used by
M1's sample hierarchy and by M2/M3 rehearsal and validation. Registration is
metadata only (schema/project.schema.json); it confers no access.

The four workflow-orthogonal labels (`needs-human`, `strict-gate`,
`security-sensitive`, `scientific-evidence`) are created **only** in this
repository during M1 — it is the label template for later, separately
authorized rollouts.

## gatebraid-metadata

```yaml
schema: gatebraid/project@1
project_id: gatebraid-scratch
repo: MianliWang/gatebraid-scratch
environment: wsl
strict_gate: false
risk_default: low
default_branch: main
notes: >
  Scratch/rehearsal repository. Reused authoritative repository identity:
  GitHub repository ID 1315376699 (renamed per ADR-0010 if it bore a former
  name; redirects preserved; never duplicated). Sample Slices A–D live here
  as cross-repo sub-issues of Phase P1 in MianliWang/gatebraid.
```
