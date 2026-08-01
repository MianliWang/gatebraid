# ADR-0020 — The executor authenticates as a machine account: attribution before enforcement

**Status:** Accepted · M2 (2026-07-31) · Product: Gatebraid (ADR-0010)
**Amends:** nothing — ADR-0015 stands; this ADR begins resolving the condition it
names.
**Provenance:** ADR-0015; CONSULT-M2-01 §Q2 with verifications V1 (GitHub ToS
§B.3) and V2 (ruleset availability on private repositories);
`consults/CONSULT-M2-01/CONSULT-M2-01-decision.md` §Q2, operator ruling of
2026-07-31; RB-M2-E §E0.1; friction #27.
**Amended:** 2026-07-31 (M2 Batch F) — Provenance cites the consult's committed
location instead of an untracked `_handoff` path, per friction #34. Decisions
unchanged.

## Context

ADR-0015 records that the two approval doors rest on executor discipline:
executor and operator are one GitHub actor, so an approval comment's author
distinguishes nothing. CONSULT-M2-01 stated the failure story at its sharpest —
a mistaken or prompt-injected agent writes "APPROVED" under the operator's
identity, reads its own comment back as authorisation, then pushes, merges and
closes; the durable record afterwards is indistinguishable from a real approval.

The consult bundled the remedy into one plan-contingent recommendation. The
correction, drawn from the consult's own verifications: **attribution and
enforcement are separable, and only enforcement is plan-dependent.**

- *Attribution* requires only that the executor be a different actor. GitHub ToS
  §B.3 permits one free personal account plus a machine account (V1). Nothing
  plan-gated is involved.
- *Enforcement* — rulesets, required reviews, stale-approval dismissal, bypass
  restrictions — is available on private repositories only on paid plans (V2).
  Both repositories are private (E0.1); the plan is unknown, and the one
  inference offered about it rests on an untested premise (friction #27).

Blocking the free half on the gated half was the consult's error. The standing
"no API keys, no credential handling" rule was the remaining question, and it
was the operator's to answer, not either agent's.

## Decision

**1. The operator's ruling of 2026-07-31 is recorded.** The no-credential rule
does not forbid the operator authenticating a second GitHub account through the
browser. It continues to forbid any agent creating, copying, storing or exposing
any secret, and forbids an agent handling a token. The ruling is an
interpretation of the standing rule, not a change to it.

**2. The executor becomes a distinct machine account.** A machine account under
ToS §B.3, established by the operator, logged in by the operator personally on
the executor host through the same browser-based `gh auth login` flow the
current identity uses. No agent performs, scripts, or assists any part of
authentication.

**3. Least privilege.** The machine account receives collaborator write on
`MianliWang/gatebraid` and `MianliWang/gatebraid-scratch`, and access to the
"Mianli Engineering" Project sufficient to write its fields — and nothing else.
If the platform cannot grant one of these (user-Project collaboration is the
untested one), that is a blocking observation to report, not to work around.

**4. Attribution semantics.** Once the split is live, an approval comment
authored by the operator's personal account is evidence the executor did not
write it. The gate contracts' approval-validity checks gain an author condition
**in the same change that executes the cutover, not before**: until the split is
live, every legitimate historical approval carries the shared author, and an
author check adopted early would fail them all. This is ADR-0014 §2's rule
generalised — the check and the state it checks change together.

**5. Sequencing.** No identity change executes before this ADR is on `main`.
The cutover is a separately announced, separately approved operation whose
authentication steps are the operator's own acts; the executor's part is
verification and record, never authentication.

**6. The enforcement half stays open.** It waits on the disabled-ruleset probe:
a `403` on the POST means plan-gated on these private repositories — the options
(public repositories, a paid plan, or detection-only) go to the operator as a
decision for a future ADR. A created-then-deleted ruleset means enforcement is
designable and becomes its own later batch. Neither outcome changes decisions
1–5.

## Consequences

- The indistinguishability ADR-0015 names is closed **by detection, not
  prevention**: a forged approval becomes attributable after the fact; nothing
  yet stops it landing. ADR-0015's reopening conditions — no unattended or
  scheduled gate execution, no agent team executing slices — are **not lifted by
  this ADR**; lifting them is a distinct future decision that may cite it.
- Signed commits remain rejected as a remedy: a signature proves key control,
  not human intent at that moment.
- The operator controls both accounts; the threat model here is agent error and
  prompt injection, not operator malice, which no account topology addresses.
- Follow-ups, owned by the cutover batch when the operator schedules it: the
  cutover runbook (operator acts + executor verifications) and the
  author-condition contract edit, together.

## Reopening conditions

- The probe shows enforcement available → design the enforcement half; revisit
  whether any detection-only clause should tighten.
- GitHub's ToS or machine-account policy changes.
- Any observed action by the machine account outside decision 3's grant.
