# ADR-0013 — Every Gate 0 verification has a defined failure disposition

**Status:** Accepted · M2 (2026-07-31) · Product: Gatebraid (ADR-0010)
**Provenance:** M2 Batch B, the first execution of Gate 0 against a real slice
(Slice A `P1-S1`, 2026-07-30). ADR-0011 §4 (a check with no defined failure mode
carries no information); `protocols/gatebraid-control-plane-spec-v1.md` §1
(Workflow options and the `needs-human` coupling) and §2 (`Next Approval`
options).

## Context

Gate 0 has six read-only actions. Exactly one of them — action 3, working-tree
cleanliness — states what happens when it fails: `result: stopped`,
`Next Approval = Dirty Baseline Acceptance`, and no remediation of any kind,
ever. The other five say only "verify".

The first real execution of Gate 0 walked straight into that gap. Action 4
verifies that the Project's `Environment` field matches the actual host. The
field said `wsl`; the host was Windows — `MINGW64_NT`, `git 2.51.0.windows.1`,
a working tree on `D:/`, no `/proc/version` anywhere. The check failed
correctly, and then there was nowhere to go: no Workflow state the contract
sanctioned, no `Next Approval` value, and an evidence template offering only
`environment-matches-host: pass`.

The executor stopped and asked, which is right, and explicitly declined three
available workarounds: writing the field to `windows` (an unapproved correction
of an M1 record), editing the slice metadata (forbidden by that batch), and
recording a pass on the argument that the field means the *target* environment
rather than the host (the contract says host). It also declined to write a
`gate0.md` claiming a gate that had not passed. Every one of those refusals was
correct, and each was only necessary because the contract left a hole.

**The mismatch itself is a real defect, not a false alarm.** M1 set
`environment: wsl` on all four sample slices — inherited from the example value
in `templates/slice.md` — while every session since has run on Windows-side Git
Bash. Gate 0 is simply the first thing that ever compared the record with
reality. That is the gate doing its job.

## Decision

**1. Every Gate 0 action states its failure disposition, and the dispositions
come in exactly two kinds.**

- **Decidable by a human** — the state is defensible and the operator may accept
  it. `result: stopped`; set the matching `Next Approval`; the row reaches the
  human through `Next Approval`, and the `needs-human` label is *not* set here
  (spec §1 governs the label, and this is not one of its states). No
  remediation, ever.
- **An error** — nothing for a human to accept, something is simply wrong.
  `Workflow = Blocked` with a typed `needs_input` reason in a comment, which is
  the one case where spec §1 does set `needs-human`. Stop and report.

**2. The dispositions, per action:**

| Action | Failure | Disposition |
|---|---|---|
| 1 — repository identity and remote | wrong repository or remote | **error** → `Blocked` + `needs_input` |
| 2 — record the plan baseline | cannot read the base branch head | **error** → `Blocked` + `needs_input` |
| 3 — working tree clean | dirty tree | **decidable** → `Next Approval = Dirty Baseline Acceptance` *(unchanged)* |
| 4 — `Environment` matches the host | mismatch | **decidable** → `Next Approval = Environment Change` |
| 5 — tool versions | a required tool is missing or non-functional | **error** → `Blocked` + `needs_input` |
| 5 — tool versions | present but a different version than recorded | **record only**; it blocks nothing unless the plan depends on the version, in which case Gate 1 declares that dependency |
| 6 — metadata parses against `gatebraid/slice@1` | fails validation | **error** → `Blocked` + `needs_input` |

**No new `Next Approval` option is created.** `Environment Change` already
exists in the nine (spec §2) — the machinery was there; only the contract's
wiring to it was missing.

**3. `templates/gate0-evidence.md` gains a `result: stopped` shape** so an
evidence file can record a failed gate honestly. A gate that stopped must be
writable as stopped; the previous template could only express a pass, which is
what made "write nothing" the only honest option.

**4. Two template corrections, both of which caused this.**

- `templates/gate0-evidence.md` still ended with
  `notes: "<straight to Needs Plan Approval only for trivial pre-planned
  slices — record why>"`, advertising the shortcut ADR-0011 §8 removed from the
  contract. A template that invites a transition the contract forbids is worse
  than no template. Removed.
- `templates/slice.md` carried `environment: wsl` as its example value. That
  default propagated to all four M1 sample slices and is what action 4 caught.
  The example now shows the value this installation actually runs on, and the
  comment says the field must equal the host Gate 0 will verify against — it is
  not a preference or a target.

## Consequences

**Data correction, recorded here so it is not mistaken for drift:** the four
sample slices `P1-S1`…`P1-S4` have `environment` corrected from `wsl` to
`windows`, in both the Project field and the issue metadata block. This is a
correction of an M1 drafting default, not a change of plan — nothing about these
slices ever needed WSL, and the repositories, tooling and working trees have
been on Windows throughout. It is applied under this ADR in an announced batch,
not silently by an executor mid-gate.

The `environment` value is not covered by `plan_hash` or `allowlist_hash`
(ADR-0011 §3), so correcting it before Gate 1 costs nothing and invalidates no
freeze.

Gate 0 can now fail in five distinct ways and record each one. The
milestone-level consequence is that a stopped Gate 0 is a normal, expressible
outcome rather than a dead end — which is what the design always intended, since
action 3 was written that way from the start.

## Reopening conditions

- If a slice is ever genuinely intended to execute somewhere other than the host
  running Gate 0 — a remote runner, a container, a second machine — then
  `Environment` is being asked to mean two things and needs splitting into
  *where this executes* and *where this targets*, rather than a wider enum.
- If action 5's "record only" branch ever lets a version drift cause a Gate 2
  failure, the branch is too permissive and version pinning belongs in the Gate 1
  plan as a declared dependency.
- If Gate 1, 2 or 3 turn out to have verifications with no stated failure
  disposition — this ADR only audited Gate 0 — the same treatment applies and
  should be done in one pass rather than one gate at a time.
