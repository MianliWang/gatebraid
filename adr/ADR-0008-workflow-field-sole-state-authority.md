# ADR-0008 — Workflow field is the sole state authority; `needs-human` is the only mirrored label

**Status:** Accepted · **Final for M1, not provisional** · M1 (2026-07-29) · Product: Gatebraid (ADR-0010)
**Provenance:** report 11 D2 (the field-vs-label trade and the phone-test rule: "decide from the phone test, not from taste"); report 09 §11 (single-homing); the M0 phone probe (report 11 §6 step 6), results recorded verbatim below; operator decision transmitted 2026-07-29 with the M1 execution approval.

## Context

Report 09 originally mapped the 13 workflow states to repository labels partly for GitHub Mobile visibility. The Gatebraid design moves state to a single-select Project field (single authority, no six-repo label sync) and mirrors at most one attention label. Report 11 D2 made the residual mobile-visibility question empirical: run the M0 phone probe, record the results in this ADR, and decide from them.

## M0 phone-probe results (recorded verbatim)

```yaml
github_mobile:
  field_value_visible: false
  label_visible: true
  board_usable: true
  needs_human_notification_sufficient: null
  notes: >
    The Workflow Project field value was not visible directly on the GitHub
    Mobile Issue page. The needs-human label was visible. The Project view was
    usable after the Project link was handed off to GitHub Mobile.
    Safari/Chrome mobile-browser usability was not tested separately.
    Notification sufficiency was not tested.
```

Interpretation against the M0 step-6 placeholders (operator-supplied, 2026-07-29):

- field-on-issue: **no**
- label-on-issue: **yes**
- board-in-mobile-browser: **not tested**

`board_usable: true` refers specifically to the Project view opened through GitHub Mobile after link handoff — not to Safari or Chrome mobile-browser usability, which was not tested separately. This ADR deliberately does not record board-in-mobile-browser as "yes".

## Decision (operator, 2026-07-29)

1. The GitHub Project **`Workflow` field remains the sole complete workflow-state authority.**
2. **`needs-human` remains the only mirrored mobile attention label.**
3. **No second mirrored workflow label is added during M1.**
4. The assignment/@mention **notification-sufficiency test is a non-blocking follow-up before M2** (`needs_human_notification_sufficient` is `null` above until it runs).
5. **This ADR is final for M1**, not provisional.

## Label-coupling rule (normative; from the spec)

The `needs-human` repository label is set **exactly** when `Workflow ∈ {Needs Plan Approval, Human Diagnosis Required, Needs Release Approval}` or `Workflow = Blocked` with a `needs_input`-typed block reason — and removed on exit. In v1 the mirror is maintained by the Lead/human as part of the transition (one-way: field → label; the label is never hand-edited into a state claim of its own).

## Consequences

- The phone attention path is: notification / Needs Me view / `needs-human` label on the issue, then the Project link handoff into GitHub Mobile for board context. Full field visibility on the issue page is not assumed anywhere.
- Folding in the notification-sufficiency result is an M2 entry item; if it fails, the remedy space is bounded by report 11 D2 (at most one additional one-way mirrored label, decided by a new ADR — never hand-synced state).
