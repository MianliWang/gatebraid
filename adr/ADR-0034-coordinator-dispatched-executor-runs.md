# ADR-0034 — Coordinator-dispatched executor runs: the operator stops being the transport

**Status:** Proposed · M3 (drafted 2026-09-03 by the coordinator; corrected
twice on 2026-09-04 on the findings of the batch's two independent read-only
reviews — untracked working files under `_handoff/batch-dd1/`, identified by
their self-measured regions `ab65eea47f4781d2962186ca7125527e5fe901c839a14278ed6892f6e4b71db2`
and `22b0117257667880e13c743226218a1dff17bcefdf4e79dea8da4004f2d13c0a`, whose
findings this text now carries; ratified only by the operator's
Batch Approval for DD1 after an independent read-only review of the
corrected text) · Product: Gatebraid (ADR-0010)
**Amends:** ADR-0015's reopening condition *"before any unattended or scheduled
execution"* is executed here, narrowly, for the first time — see decision 8;
ADR-0015 decisions 1–4 stand unchanged. ADR-0020's Consequences anticipate a
*"distinct future decision that may cite it"*; this is that decision. Nothing
in ADR-0003 (single writer), ADR-0004 (Codex read-only), ADR-0020/0024
(executor identity held in the dedicated store; no agent handles a credential)
or ADR-0025 (terminal is an operator act, reached only from
`Human Diagnosis Required`) is changed for any Slice outside
`MianliWang/gatebraid-scratch`; decision 9 adds one entry route to
`Human Diagnosis Required` for the trial's stage 3, confined to trial Slices
on that repository and stated there as a typed exception — an edge the
spec's §1 transition list does not carry. The spec's own text is edited in
the batch that lands stage 3, the batch that authorises the route (as
ADR-0025 edited spec §1 in the batch that added `9→14`); until then the list
is unchanged for every Slice, and the edge exists only as this ADR's
announced exception.
**Provenance:** `claude/proposal-fewer-relays-chaining-and-direct-drive.md`
Part B (coordinator workspace, 2026-09-02; the operator's word to draft this
ADR was given 2026-09-03); the measured relay cost on P2-S5 — fourteen pastes
and four URL returns before the Human Diagnosis route, then a further eleven
relays across two Human Diagnosis rounds, of which two arrived at the wrong
window (both refused with zero writes: the misdelivered routing paste, and a
review dispatch pasted before the remediation it named existed); friction
#201 (addressing by self-measurable properties); friction #100/#116 (evidence
is never transported by hand between windows); M3-PLAN §5.1 (an ADR is
justified by a changed permission boundary), §5.2 (two standing doors; every
extra human round trip carries a typed exception), §5.3, §8; the harness
survey `claude/research-harness-2026-09-borrowable-designs.md` (Codex's
headless `exec` with a fixed approval policy; Hermes's exact-bytes input
hashing for unattended jobs; OpenClaw's external policy guard whose every
failure is a block).

## Context

Today an executor run begins only when the operator pastes an instruction into
a Claude Code window on the host, and ends when the operator carries its report
back to the coordinator. Between the two standing doors, almost every relay
moves a stop report one way and a "continue" the other; it carries no decision.
Part A of the proposal (chained pastes, in force since 2026-09-02) cut the
count by bundling phases into one paste with one-word triggers. It did not
change who originates a run, so the operator remains the transport, and the
transport is where the two misdeliveries happened.

The permission boundary is the point. Under the contracts as written, a
coordinator-written file cannot start an executor run; only the operator's
paste can. Changing that is exactly what M3-PLAN §5.1 reserves an ADR for. Two
other things make it decidable now rather than later. ADR-0020/0024 gave the
executor an identity distinct from the operator's, held in a dedicated
credential store, so a forged approval is attributable after the fact — the
detection half ADR-0015 lacked when it wrote its reopening condition. And the
evidence discipline now measures rather than trusts: reports self-measure their
regions, doors are located by fidelity against a committed source, and a fresh
context is addressed by properties it can verify about itself. A headless run is
a fresh context; the addressing discipline was built for exactly that.

What must not move: the two doors are honoured, not optimised away (ADR-0015
§2); the executor never writes its own authorisation (§3); no agent handles a
credential (ADR-0020 §1); one writer per repository (ADR-0003); no scheduled
work into hours when nobody is watching (ADR-0015's consequence, kept as a
prohibition in decision 8); and *Approval mode: Manual* — no Auto, no Skip.

## Decision

**1. Origination.** The coordinator may originate an executor run only by
writing a dispatch file into the inbox `_handoff/inbox/` and listing it in
`_handoff/inbox/MANIFEST.json` (schema `gatebraid/dispatch-manifest@1` — the
key by ADR-0033; the id admitted, like `gatebraid/dispatch-run@1` and
`gatebraid/dispatch-fixture@1`, by this ADR plus the operator's Batch Approval
under ADR-0030) with the file's sha256, its job kind, and its target
repository. Anything in the inbox that no entry names is refused with the
manifest, at the manifest level, before any entry runs. A
host-side dispatcher — `bin/gatebraid-dispatch.py`, committed to the control
repository like every other instrument (ADR-0028, ADR-0032) — validates each
entry against the manifest and the standing scans, and starts a headless Claude
Code run (`claude -p`) with the dispatch file as its instruction, the repository
as its working directory, and the executor's environment (`GH_CONFIG_DIR`
naming the dedicated store, `PYTHONDONTWRITEBYTECODE=1`, `-B` on every Python
invocation the paste directs). Anything not in the manifest, or whose bytes do
not equal the manifest's hash, is refused. The refusal is the product: a
dispatcher that has only ever allowed has not been shown able to refuse, so
`fixtures/direct-drive/` precedes the tool and each refusal is demonstrated on
its seed before first trusted use (spec §4's rule, M3-PLAN §2's fixtures-first).

**2. What the relay becomes.** For every step that is not a door, the
operator's paste-by-paste relay is replaced by the coordinator's post-hoc audit
of the run's outputs: the executor's report where the dispatch text directs
it (today `_handoff/batch-<slice>/`), the dispatcher's run record
(`gatebraid/dispatch-run@1`: the dispatch file's sha256, the settings
profile's sha256, the heads and porcelain lists before and after, start and
end instants, exit status, the captured streams' sha256), and the artefacts
the report names — staged through the
device bridge and re-measured in the coordinator's sandbox exactly as today.
The doors — Plan Approval, Release Approval, Human Diagnosis dispositions — and
the merge remain operator acts, authored in the browser and verified by fidelity
against a committed source. The dispatcher never posts a comment of any kind;
the coordinator pre-checks every door before the operator posts it, as now.

**3. Addressing.** A headless run is a fresh context and is addressed exactly
as a paste is — by properties the run can measure about itself (the files it
can hash, the fields it can read, the branch it is on), never by history only
the sender knows (friction #201). A dispatch that fails its own entry
conditions ends with a typed stop and zero writes; that outcome is a success of
the mechanism, recorded as such, not an error to be retried unchanged.

**4. Kill switch.** The dispatcher checks for `_handoff/inbox/STOP` before every
job and, for a running job, at every output-poll; its presence halts the
dispatcher with a typed record. The dispatcher is a foreground process in the
operator's own host session, started and ended by the operator; the STOP file
is the second, independent way to end it. Both are demonstrated on a seeded
test before first trusted use.

**5. Permissions are declared, never bypassed.** A headless run cannot answer a
permission prompt, so each job kind runs under a declared tool allowlist held
in the host's Claude Code settings profile for that kind's class, whose sha256
the run record carries: read-only kinds (Review, consult preparation) get a
read-only tool set; evidence kinds (Entry, Gate 0, Gate 1) get a set that
writes only under the Slice's own evidence directory and never commits —
the Gate 0 and Gate 1 contracts write their evidence file at Exit and the
record rides onto the Slice branch under the Gate 2 lease; write kinds
(Gate 2 under lease, Gate 3) get the allowlist R-min defines. The dispatcher
measures the head and the porcelain list before and after every run and
records, for a read-only kind, that nothing changed, and for an evidence
kind, that nothing changed outside `docs/evidence/gatebraid/<slice_id>/` and
nothing was committed — the exclusion ADR-0014 §1 applies to the baseline
re-read (the contract's `DD-R08`). A tool the profile does not allow is denied
and the run stops there — that is the fail-closed behaviour, and it is why the trial
below is staged. No permission-bypass flag is ever passed; *Approval mode:
Manual* is unchanged — this ADR changes who starts a run, never who approves
anything.

**6. Single job; single writer; closed set.** The dispatcher runs one job at a
time and refuses a second while one runs. A write-kind job takes and releases
the `Writer Lease` exactly as the gate contracts write it; the dispatcher does
not touch the lease. A review-kind job carries its read-only mandate in the
dispatch text and attests to it in its report, as today. Every dispatch and
every manifest entry is checked against the closed repository set
(`MianliWang/gatebraid`, `MianliWang/gatebraid-scratch`): any other
`owner/name` identity, in either, is refused — the six protected business
repositories are therefore refused without being named anywhere in the tool
or its fixtures.

**7. Identity.** Headless runs use the executor's machine account through the
dedicated store (ADR-0024 §1) inside the operator's host session. The
coordinator holds no credential and no host process; the dispatcher performs
no authentication act; ADR-0024 §2's write-before identity guard is carried by
the paste as now. Nothing here touches a secret.

**8. ADR-0015's reopening condition, executed narrowly.** ADR-0015's first
reopening condition says the operating-rhythm ADR *"must not authorise
unattended gate execution without revisiting this one"*; this ADR revisits it
and lifts the prohibition only in this sense: a run may proceed without a
human paste. It does not lift the rest. No run is scheduled; the dispatcher
runs only while the operator has started it in a session they are present for;
every door is still an operator act, now attributable (ADR-0020 §4); every run
is audited from its record before the next door is drafted; and a business
repository is out of scope until M3-PLAN §7's checklist admits it under its
own approval. Scheduled or cron-driven execution remains prohibited and would
need its own ADR.

**9. Controlled trial, each stage its own batch approval with a measurable
stop.**

| Stage | What runs | Success criterion | Stop if |
|---|---|---|---|
| 0 — dry run | the dispatcher in print-only mode: reads the inbox, validates, prints the command it would run, runs nothing | every fixture in `fixtures/direct-drive/` yields its expected decision; STOP halts it | any seeded refusal fails to fire |
| 1 — read-only replay | a headless run of a closed Slice's review dispatch (P2-S6's R1–R5) under the read-only profile; separately, one entry naming a profile that does not exist, refused before any run (the live `DD-R07` seed, whose record the stage's approval binds) | the headless report's verdicts equal the recorded review's; zero writes inside the repository by the replay; the report's self-measured region reproduces; the seed's record shows `DD-R07` | any write by the replay, or a verdict that differs without a stated measured cause |
| 2 — evidence gates on a scratch Slice | Entry, Gate 0 and Gate 1 on a `gatebraid-scratch` Slice, as `entry`, `gate0` and `gate1` jobs under the `evidence` profile | `plan_hash` and `allowlist_hash` reproduce; every field write read back; each run record shows nothing changed outside the Slice's own evidence directory and nothing committed; the Plan Approval door stops the run | any Gate 2 action without a door; any `DD-R08` |
| 3 — a write gate under lease | Gate 2 on the same scratch Slice under R-min's declared allowlist | R1–R5 pass by an independent reviewer; the lease is taken by the record and still held when the stage's last dispatched job ends with the Slice at `Needs Release Approval`; nothing pushed; afterwards the lease is cleared by the operator's terminal disposition of the scratch Slice (the route below), and the cleared field is read back as the stage's last measurement | any path outside the allowlist; any push |

Stages 0–1 may run before R-min. Stages 2–3 depend on R-min's permission
allowlist and follow it, or run as its first live exercise under R-min's own
approval. Only after stage 3 may a Slice outside `gatebraid-scratch` have its non-door
steps dispatched this way, and the first such Slice is announced as one.

**How stage 3 ends, stated so its success criterion is satisfiable.** Under
the gate contracts a lease is taken at Gate 2 entry and released at Gate 3
exit (ADR-0003 §1; `protocols/gate-3-contract.md` exit step 6), and Gate 3
exit requires the push and merge that stage 3 forbids. The only other release
on record is terminal disposition (ADR-0025 §3 clears `Writer Lease`),
reachable only from `Human Diagnosis Required` (ADR-0025 §2), which spec §1's
transition list enters from the repair sequence (`8→9`), repair exhaustion,
or blocker recurrence — not from `Needs Release Approval`. Stage 3 therefore
ends by a typed exception, confined to trial Slices on
`MianliWang/gatebraid-scratch` and pre-authorised by the stage's own batch
approval: the operator, by a disposition comment on the scratch Slice's issue
(a door — ADR-0015 §2/§3, ADR-0020 §4), routes it from
`Needs Release Approval` to `Human Diagnosis Required` and then to terminal
under ADR-0025 §2–§4 exactly as any terminated Slice: branch retained local
and unpushed, `Writer Lease` cleared, `Workflow` `Aborted`, the issue not
closed; the field writes of both transitions are the executor's, under the
disposition's announced action, as for every disposition on record. No Slice
outside that repository may use this route; the transition list is unchanged
for all of them. The dispatcher plays no part in it.

**10. Landing.** This ADR, `protocols/direct-drive-v1.md`, and
`fixtures/direct-drive/` land together as batch DD1 under M3-PLAN §8's batch
protocol (a pre-adjudicated approval binding to an announcement; blob-hash
bindings for coordinator-delivered files; the two doors live), taking in
addition the heavier shape §8 prescribes for N0 — a dedicated branch, a draft
pull request and an independent read-only review before the operator's merge
— because this ADR changes a permission boundary (M3-PLAN §5.1). The
dispatcher's code lands in a later batch, after the fixtures it must fail on
are frozen by commit SHA. DD1 does not land while a Slice holds an open Gate 2
or Gate 3 on the control repository, so the base under that Slice does not
move; the coordinator names the landing window when it opens.

## Consequences

- The operator's involvement per Slice drops from a relay per step to: start
  the dispatcher, post the doors, merge, stop the dispatcher. M3-PLAN §5.2's
  two standing doors are exactly preserved; the typed exceptions for extra
  round trips become rarer, not more common.
- M3-PLAN §5.3 is strengthened: the run record is generated by a committed
  tool and the report is read from a file, so no evidence is transported by
  hand between windows at all.
- The dispatcher is one more instrument under ADR-0028: committed, falsified
  on its fixtures, reused. Its refusal codes are the fixtures' expected
  decisions, so the two cannot drift without a fixture failing.
- What does not change is listed once so nobody infers otherwise: Approval
  mode Manual; one writer; no worktrees; Codex read-only; no credential
  handling; the closed repository set; the six protected repositories
  untouched; terminal only from Human Diagnosis Required by the operator.

## Reopening conditions

- Any run that starts without a manifest entry, or with a hash mismatch, and is
  not refused — that is the mechanism failing, and it stops all dispatching
  until repaired and re-falsified.
- Any proposal to schedule dispatching, or to run it while the operator is not
  present — a distinct decision, not an amendment here.
- A second executor host, or a host permission model that can enforce the
  read-only profile rather than declare it — either changes what decision 5 can
  promise.
- The first business-repository dispatch, which M3-PLAN §7 gates separately.
