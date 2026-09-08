# ADR-0035 — The coordinator may start the dispatcher: the operator stops being the starter for read-only runs

**Status:** Proposed · M3 (drafted 2026-09-08 by the coordinator on the
operator's word of the same day — "I agree that you change the ADR" — after
the stage-1 package of ADR-0034 decision 9 had been delivered with three
PowerShell blocks for the operator to run; admitted by an independent
read-only review and ratified by the operator's Batch Approval and merge,
both recorded in this Status line by the batch that lands it) · Product:
Gatebraid (ADR-0010)
**Amends:** ADR-0034 decision 4 (*"a foreground process in the operator's
own host session, started and ended by the operator"*), decision 7 (*"the
coordinator holds no credential and no host process"*) and decision 8
(*"the dispatcher runs only while the operator has started it in a session
they are present for"*), and the contract's §1 (*"never runs anything on
the host"*) — each in the one respect stated in decisions 1–3 below, for
read-only job kinds only; ADR-0034's reopening condition *"any proposal … to run it while
the operator is not present — a distinct decision"* is NOT invoked: the
operator stays present in the sense decision 3 defines. ADR-0015's first
reopening condition (*"discipline is a sufficient control only while a human
is watching the session that holds the credential"*) is revisited a second
time, as narrowly as ADR-0034 decision 8 revisited it, and decision 4 says
what is and is not lifted. Nothing in ADR-0003, ADR-0004, ADR-0020, ADR-0024
or ADR-0025 changes; every door remains an operator act authored in the
browser and located by fidelity; Approval mode Manual is unchanged.
**Provenance:** the stage-1 package (`_handoff/batch-stage1/`, delivered
2026-09-08) and its operator's-runs file, which put three terminal sessions
and a timed kill-switch act on the operator; the operator's question of the
same day — that this work should be done by the coordinator calling Claude
Code itself — and the coordinator's answer that three rules stood in the
way (this project's standing instruction that the coordinator's shell is
remote; ADR-0034 decisions 4, 7 and 8 with contract §1; ADR-0015's
condition), none of which a conversation can override; the measured relay
cost of ADR-0034's provenance, which this decision reduces once more.

## Context

ADR-0034 removed the operator from the transport of a run: the coordinator
writes the dispatch file and the manifest, a committed dispatcher validates
and starts the headless run, and the operator's part shrank to starting the
dispatcher, posting the doors and merging. Stage 0 of its trial showed the
dispatcher refusing and printing on the real host. The stage-1 package —
the first real runs — showed what "starting the dispatcher" costs when the
operator must do it: three PowerShell blocks, one with a 45-second timer to
create the kill-switch file while a job runs, and a HOLD in the build window
that only the operator's `runs done` can release. Every one of those acts is
mechanical; none is a door; each is a relay the operator wanted gone.

The coordinator's session reaches the operator's host through the desktop
bridge: a file bridge (read, write, list) used since M1, and — connected by
the operator on the same host — process tools that can start a program in
the operator's own Windows session and read its output. The capability
exists; what forbade its use was policy, written when the coordinator's
only host reach was files. This decision changes the policy in the one
respect the relay cost justifies, keeps the human watching the session that
holds the credential, and keeps every run inside the dispatcher's record.

## Decision

**1. Who may start the dispatcher.** The coordinator may start
`bin/gatebraid-dispatch.py` on the executor host — in any of its three
modes (fixture, print-only, the run form) — through a host-process tool of
the desktop bridge, in the operator's own host session, for a manifest whose
every entry is a read-only kind (`review`, `consult-prep`; contract §3). The
operator may still start it exactly as ADR-0034 decision 4 says. Evidence and
write kinds remain operator-started until the trial stage that authorises
them (ADR-0034 decision 9, stages 2–3, under R-min's profiles) says
otherwise in its own approval.

**2. What the coordinator's host reach is, and is not.** Through the
host-process tool the coordinator runs exactly four classes of command, each
announced in the conversation before it runs: (a) the dispatcher in one of
its three modes, with `-B` and the two environment variables the contract
names; (b) creating or removing the kill-switch file `STOP` in an inbox it
delivered; (c) read-only measurements the file bridge cannot make and the
audit needs — a hash, a listing, a process count, a version, the reading of
a headless run's transcript — never a mutation; (d) creating a scratch
directory outside every repository. It never starts `claude -p` directly
(a run without a dispatcher record is a run this ADR forbids); never runs
`git` or `gh` in any form; never edits, moves or removes a file outside the
ignored `_handoff/` lane, the profile file included; never installs,
configures or updates anything; never reads or copies a credential or the
dedicated store; never automates a window, a browser or a keyboard; never
starts anything on a schedule, a timer or a trigger — a start is an act in
a conversation turn, on the operator's word for that batch (decision 3).
Everything else on the host stays Claude Code's, by paste, as before.

**3. Presence, redefined so it can be measured.** The operator is present for
a coordinator-started session when all of the following hold: the batch's
brief, delivered through the file bridge, binds by sha256 every manifest the
coordinator may start in that batch; the operator has given the word for the
batch in the conversation after the brief was delivered; the coordinator
announces each start in the conversation with the manifest's sha256 and each
end with the dispatcher's `exit <n>` line; and the operator retains two ways
to end any run that do not pass through the coordinator — the kill-switch
file, created from their own machine, and ending the process in their own
session. A session the operator has said they are leaving is not started;
a session already running when they leave is left to the kill switch they
hold. No coordinator-started session outlives the batch it belongs to.

**4. ADR-0015, revisited a second time and no further.** ADR-0034 decision 8
lifted ADR-0015's condition in one sense — a run may proceed without a human
paste. This decision lifts it in one more — a run may be started without a
human keystroke — and only for job kinds that write nothing inside the
repository (the contract's `DD-R08` records the fact after every run) and
make no `gh` mutation (the read-only profile denies them; the dedicated
store's identity posts no door). The human still watches the session that
holds the credential: the session is theirs, the start is announced to
them, the kill switch is theirs. Scheduled, timed or unattended starts
remain prohibited and would need their own ADR, as ADR-0034 said.

**5. The record.** Every coordinator-started session leaves what an
operator-started one leaves — the run records, the streams, the reports —
and one thing more: a session log on the batch's lane
(`_handoff/batch-<name>/host/coordinator-sessions.txt`, written by the
coordinator through the file bridge), one line per command of decision 2 —
the instant, the class letter, the command as run, the exit status or the
`exit <n>` line — appended before the next command runs. The independent
review compares the log with the records and with the conversation's
announcements; a command in the records that the log does not carry, or in
the log that was not announced, is a finding against the coordinator and
stops the coordinator's host reach until the batch that repairs it.

**6. First use is a demonstration.** Before any trusted coordinator-started
run: (a) a channel probe — the four classes of decision 2 exercised once
each in their harmless form (the dispatcher's `--help`, which exits `2`; a
`STOP` created and removed in an empty inbox; `python -B --version`,
`claude --version` and a process count; a scratch directory created), each
captured (`gatebraid/evidence-capture@1`) and committed as the batch's
evidence; (b) the kill switch against a coordinator-started dispatcher — the
stage-1 acts A and B of ADR-0034 decision 9, started by the coordinator and
halted by a `STOP` the coordinator creates (act B), then once more by a
`STOP` the OPERATOR creates from their own machine at any moment they
choose while a second rehearsal job runs (act B2: one empty file, no
timing) — so that both hands on the switch are on record. The stage-1
package is re-issued with the coordinator as the starter; its success and
stop conditions do not change.

**7. Landing.** This ADR and the contract's amended §1, §5 and §10 land
together as one batch under the standing protocol (dedicated branch, draft
pull request, independent read-only review, the operator's Batch Approval,
the operator's merge; the branch retained). The project's standing
instruction to the coordinator — that host-local work is deferred to Claude
Code on the host — is the operator's to edit, in the same words as decision
2, and this ADR is not in force until both the merge and that edit are on
record; the coordinator states which of the two it has seen before its
first host command.

## Consequences

- The operator's involvement per read-only batch drops to: the word for the
  batch, the pastes that land it (a build window cannot yet be dispatched:
  commit, push and pull-request creation are write kinds), the review paste,
  the approval, the merge. The dispatcher's sessions, the kill-switch acts
  and the post-run measurements are the coordinator's.
- A second party can now create the kill-switch file; the file's meaning is
  unchanged (presence is the signal) and the operator's own hand on it is
  demonstrated once by decision 6(b) and remains available always.
- The coordinator's host reach is wider than files and is bounded by
  decision 2, announced by decision 3 and logged by decision 5 — discipline,
  not access control, as ADR-0015 chose for the operator's own identity; the
  review is what checks it.
- What does not change: Approval mode Manual; every door an operator act;
  one writer; no worktrees; Codex read-only; no credential handling by any
  agent; the closed repository set; the six protected repositories
  untouched; no scheduled execution.

## Reopening conditions

- Any coordinator host command outside decision 2's four classes, or any
  command the session log does not carry — the reach closes until repaired.
- Any proposal to let the coordinator start evidence or write kinds — that
  is ADR-0034 decision 9's stages 2–3 and R-min's profiles, with their own
  approvals, not an amendment here.
- Any proposal for a start without the operator's word for the batch, a
  start the operator is not told of, or a scheduled start — a distinct
  decision, as ADR-0034 already said.
- A host-process tool that cannot be told from the file bridge in the
  record, or one that runs outside the operator's own session — decision 3's
  presence definition would no longer hold.
