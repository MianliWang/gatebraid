# ADR-0024 — Executor identity is held, not checked: the dedicated credential store

**Status:** Accepted · M2 (2026-08-07) · Product: Gatebraid (ADR-0010)
**Amends:** ADR-0022 §1's definition of surface (a) and §3's normalization
procedure. ADR-0022 §4 (drift after normalization is a stop) and §5 (selection
is not authentication) stand, re-scoped to the store this ADR defines.
ADR-0020 §2 (no agent performs, scripts or assists authentication) is
untouched and load-bearing here.
**Provenance:** friction #61 (one push under the operator's identity; a check
that printed instead of stopping), #63 (second drift; the executor's own
formulation, verbatim — *on this host the executor cannot hold its own
identity, only check it, and checking is a race it happens to keep winning*), #64 (the isolation as delivered resolved
to the operator's account — active, sole, `project` scope absent — caught by
verification before first use), #71 (the reverse channel: a Human Diagnosis
authored by the machine account), #74 (a file this project did not write,
inside the control repository working tree; author undeterminable); hosts.yml mtimes `04:11:50Z` and
`17:06:46Z` (2026-08-06), each falling between correct executor operations;
RB-M2-I.

## Context

Batch I measured, three times, what ADR-0022 §3's check-based discipline could
not provide. The gh credential store it relied on has one active slot shared
by every process on the host. Two mid-batch flips were recorded by the store's
own mtime; one push left under the operator's identity because the identity
check was chained into the command it should have gated; a premise that the
concurrent writer "was stopped" was falsified by the next flip. The remedy
that held was structural: a **dedicated credential store** that no other
process points at. Separately, #71 demonstrated the same disease in the other
direction — the operator, browser still authenticated as the machine account
from provisioning, posted a Human Diagnosis that ADR-0020 §4 correctly
rejected. Attribution is a property of the **pair** of parties, not of the
executor alone. And #74 showed that foreign writes reach even the control
repository's working tree: a file this project did not write appeared there,
carrying a false claim about its own git-exclusion status — author
undeterminable, with an agent-harness convention file as the leading
candidate and not a conclusion.

## Decision

**1. Surface (a) is the dedicated store.** The executor's gh identity surface
is the credential store at `GH_CONFIG_DIR = %USERPROFILE%\.gh-gatebraid`,
provisioned by the operator in person (browser login of
`mianliwang492-source`, scopes including `project` — an operator act, per the
2026-07-31 ruling and ADR-0020 §2). Every executor `gh` and `git` command runs
in an environment with `GH_CONFIG_DIR` set to it. The machine-shared default
store **ceases to be an executor identity surface**: the executor does not
read it, write it, or normalize it, and its state is of no consequence to
Gatebraid work.

**2. The write-before guard is normative, not decorative.** The dedicated
store was delivered resolving to `MianliWang` — active, the only account
present, without `project` scope — and verification-before-use caught it as a
real alarm, not a latent risk (#64): unchecked, the next Project write would
have left under the wrong identity. After the operator's login the entry
remains, dormant; removing it was rejected because the keyring is
machine-shared and a logout there would deauthenticate the operator
machine-wide. Isolation therefore narrows
the flip surface without closing it. Before every push or mutating call, the
executor verifies the dedicated store's active login as a **standalone
blocking step** — a command whose failure prevents the action, never a log
line in the same chain (#61's lesson, in force since its remedy). A wrong
value in the dedicated store is an ADR-0022 §4 stop and a real alarm: nothing
else legitimately points at that directory.

**3. Co-resident agents are barred from Gatebraid's surfaces.** The measured
writer classes of shared host state are: the operator's own use, co-resident
agents, and unknown. Standing bar, operator-maintained: the two Gatebraid
repositories and the dedicated store's directory are excluded from every
other agent's workspace and write scope, **permanently — not merely during
batches**. #74 is the incident that makes the working-tree half load-bearing.
The executor's standing countermeasures remain: `git add` by explicit path
only, never `-A` or `.`; `git status --porcelain` before any control-repo
commit, stopping on unexplained entries; foreign files preserved as evidence,
never adopted, deleted or edited.

**4. The reverse channel is the operator's half.** ADR-0020's attribution
guarantee holds only if the operator's outbound surfaces also point at the
operator. Normative operator practice: door and approval comments are posted
after confirming the browser session's account; the operator does not work in
a shell that has `GH_CONFIG_DIR` pointed at the executor store. The executor's
§4-style verification of door-comment authors (ADR-0020 §4) is unchanged —
#71 is the proof it works — and remains the enforcement of last resort.

**5. Provisioning and repair of the dedicated store are operator acts.**
Login, scope refresh, and any future re-provisioning happen in the operator's
own terminal and browser. The executor's permitted identity acts are exactly:
setting `GH_CONFIG_DIR` to the operator-provisioned path, reading the active
login from it, and verifying repo-local git identity per ADR-0022. Nothing
here touches a secret.

## Consequences

- ADR-0022's Consequence is restored in stronger form: the operator's daily gh
  use and other agents' credential churn need no coordination with Gatebraid
  at any time.
- The batch-start identity record simplifies to: dedicated-store active login;
  repo-local git identity in both clones. The shared store's value is no
  longer recorded.
- The enforcement-design queue item (ADR-0020 §6) gains a measured input: two
  flips in thirteen hours on the shared store; on the dedicated store, no
  unexplained active-account change since provisioning — its two hosts.yml
  rewrites (`22:14:38Z` login, `01:58:41Z` scope refresh) are both operator
  acts, recorded as such.

## Reopening conditions

- Any observed flip of the dedicated store — handled as a §4 stop first, then
  reopened here, because it would mean the isolation premise failed.
- A second executor host, or platform-side per-repository credentials
  (deploy keys, GitHub App installation) becoming available for this design —
  either changes what "holding" an identity can mean.
- Any recurrence of a foreign write inside a Gatebraid repository after the
  scope bar is in place (#74's class) — that is not drift, that is the bar
  failing, and it escalates to the operator before any further batch work.
