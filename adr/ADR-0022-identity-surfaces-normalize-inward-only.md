# ADR-0022 — The executor's identity surfaces are enumerated, and normalization is inward-only

**Status:** Accepted · M2 (2026-08-01) · Product: Gatebraid (ADR-0010)
**Amends:** ADR-0020 §5, which described the cutover as an authentication change
and named only one of its two surfaces. ADR-0020 otherwise stands, §2 untouched.
**Provenance:** friction #39 (the no-agent-selects-identity norm detecting a
benign anomaly), #41 (`gh auth switch` changes who pushes, not who authors);
RB-M2-G2 §2 and §5; the operator's 2026-08-01 request for self-serve
normalization; `_handoff/batch-n/enforcement-recon.md` §3.3.

## Context

Two incidents in one day located two distinct identity surfaces on the executor
host. At G-2's R0.2 the **gh active account** had drifted back to the operator's
— benign (the operator's own daily use), and detectable *only because* the
standing norm said no agent selects which identity it wields. At G-2's R3 the
**git commit identity** turned out to be a separate setting that `gh auth
switch` never touches; one config short, the cutover's first commit would have
carried the operator's authorship.

The host is shared: the operator's daily GitHub use and the executor's working
identity coexist in one per-user credential store with one active slot. Drift
toward the operator's identity is therefore *routine*, not anomalous — and a
norm that requires the operator to hand-correct routine drift spends their
attention without buying detection.

The resolution keeps what the norm was for and discards what it cost:
**direction** is the load-bearing property. An agent switching *into its own*
identity strengthens attribution; an agent selecting a *human* identity is the
hazard. The two were bundled; this ADR unbundles them.

## Decision

**1. The executor's identity surfaces are exactly two:** (a) the gh active
account; (b) the git author/committer identity, per clone. A newly discovered
surface is a friction entry and an amendment here — not an improvisation.

**2. ADR-0020 §5's cutover is complete only when every surface points at the
machine account.** As of `cf81cf2`'s batch this holds: gh active =
`mianliwang492-source`; both clones' repo-local git identity =
`mianliwang492-source <311670679+mianliwang492-source@users.noreply.github.com>`.

**3. Normalization is inward-only and self-serve.** At batch start, and before
any commit or push, the executor verifies each surface. A surface pointing
elsewhere is **recorded verbatim first** (the observed login — that record is
the diagnostic datum the old norm existed to produce), then normalized into the
machine account: `gh auth switch` to `mianliwang492-source`; repo-local git
config re-checked. **The executor never switches to, logs into, configures, or
acts under any other identity.** That direction remains the operator's act
alone, and an executor doing it is a violation, not a convenience.

**4. Drift after normalization is a stop.** If any surface reads as another
identity mid-batch after H0-time normalization, the executor stops and reports
rather than re-normalizing — repeated drift means something else is writing
identity state, and normalizing over it would erase the evidence.

**5. Selection is not authentication.** Switching among credentials already in
the keyring and setting a repo-local config touch no secret; ADR-0020 §2's bar
on agents performing, scripting or assisting authentication is unchanged and
unreached.

## Consequences

- The operator's daily gh use needs no coordination with Gatebraid batches;
  the batch-start record of "observed active account" replaces the who-switched
  round trip.
- The anomaly signal survives: an unexplained value in the batch-start record,
  or any post-normalization drift (decision 4), is exactly as visible as
  before — more, since it is now always written down.
- Surface (b) is guarded by convention plus this ADR's check; the platform-side
  option (`COMMITTER_EMAIL_PATTERN`, enforcement-recon §3.3) is a candidate for
  the enforcement design, not adopted here.

## Reopening conditions

- A third identity surface is discovered.
- Platform enforcement of surface (b) lands, making decision 3's git-config
  check redundant.
- Any observed instance of outward selection — that is not reopening, that is
  a violation; it reopens ADR-0015's whole question.
