# Direct drive v1 — the dispatcher contract (`gatebraid-dispatch`)

**Status:** Frozen with ADR-0034 by the merge of batch DD1
(`6062a21105e890e614ed7a45f589341943c88d6f`, 2026-09-04) · amended by batch
DD2 (the third review's M-1 and M-3 clauses; §4's `slice_id` clause; §10's
`substitutions`, command line and exit statuses; two seeds added; the
whole-manifest record's portable name and the profile file name, found by
the build window) · Product:
Gatebraid (ADR-0010). This document is the contract the dispatcher
implements and the fixtures in `fixtures/direct-drive/` test. The fixtures
precede the tool (M3-PLAN §2); a decision this contract does not name is a
refusal.

## 1. Parties and roles

- **Coordinator** — writes dispatch files and the manifest through the device
  bridge; never runs anything on the host; audits every run from its record.
- **Operator** — starts and ends the dispatcher in their own host session;
  posts every door; merges; may halt the dispatcher at any time with the STOP
  file. The operator is present for every session in which the dispatcher
  runs (ADR-0034 decision 8).
- **Dispatcher** — `bin/gatebraid-dispatch.py`, Python 3 standard library
  only, committed to the control repository. It validates, starts headless
  Claude Code, records, and refuses. It never posts a comment, never touches
  a Project field, never takes or releases a lease, never runs two jobs at
  once, never runs on a schedule.
- **Executor** — the headless Claude Code run the dispatcher starts. It is a
  fresh context, addressed by self-measurable properties, bound by the gate
  contracts and the dispatch text exactly as a pasted window is.

## 2. Files and directories (all under the ignored `_handoff/` lane)

```
_handoff/inbox/MANIFEST.json      the manifest; schema gatebraid/dispatch-manifest@1
_handoff/inbox/<name>.md          a dispatch file listed in the manifest
_handoff/inbox/STOP               the kill switch (presence is the signal; content ignored)
_handoff/inbox/RUNNING            the single-job lock, written by the dispatcher, removed at job end
_handoff/outbox/<name>.run.json   the run record; schema gatebraid/dispatch-run@1
_handoff/outbox/<name>.stdout     the run's captured stdout (bytes, as emitted)
_handoff/outbox/<name>.stderr     the run's captured stderr (bytes, as emitted)
```

The executor's own report goes wherever the dispatch text directs (today
`_handoff/batch-<slice>/<REPORT>.md`); the dispatcher does not read or judge it.

### 2.1 `gatebraid/dispatch-manifest@1`

```json
{
  "schema": "gatebraid/dispatch-manifest@1",
  "written_at": "<ISO8601 UTC>",
  "entries": [
    {
      "name": "REVIEW-DISPATCH-P2S6-G2-REPLAY.md",
      "sha256": "<64 hex>",
      "bytes": 6086,
      "kind": "review",
      "repository": "MianliWang/gatebraid",
      "cwd": "D:/Github repo/Gatebraid",
      "profile": "readonly",
      "max_turns": 200,
      "timeout_seconds": 3600
    }
  ]
}
```

- `name`: exactly one path segment matching `^[A-Za-z0-9][A-Za-z0-9._-]{0,127}\.md$`; must exist under `_handoff/inbox/`.
- `sha256`, `bytes`: the file's whole-file values; both must equal the file as read.
- `kind`: one of three classes — **read-only kinds** `review`, `consult-prep` (nothing inside the repository changes); **evidence kinds** `entry`, `gate0`, `gate1` (the working tree may change only under the Slice's own evidence directory, `docs/evidence/gatebraid/<slice_id>/`, and nothing is committed — the Gate 0 and Gate 1 contracts write their evidence file at Exit and, as their Exits direct and as M3 practice does, commit nothing (their Prohibited sections permit the commit without requiring it; this profile denies it), the record riding onto the Slice branch under the Gate 2 lease, and the Entry paste writes Project fields and at most files under that same directory); **write kinds** `gate2`, `gate3`.
- `repository`: exactly `MianliWang/gatebraid` or `MianliWang/gatebraid-scratch`.
- `cwd`: the clone of that repository; the dispatcher verifies `git -C <cwd> remote get-url origin` names the same repository.
- `profile`: `readonly` for read-only kinds, `evidence` for evidence kinds, `write` for write kinds; a mismatch is a refusal.
- `slice_id`: required for evidence and write kinds and absent for read-only kinds; matches `^P[0-9]+-S[0-9]+$`; names the Slice whose evidence directory the post-run rule (§2.2) admits.
- `max_turns`, `timeout_seconds`: positive integers; the run is ended and recorded as `timeout` when either is exceeded.

### 2.2 `gatebraid/dispatch-run@1`

```json
{
  "schema": "gatebraid/dispatch-run@1",
  "name": "<entry name>",
  "dispatch_sha256": "<64 hex>",
  "manifest_sha256": "<64 hex of MANIFEST.json as read>",
  "profile_path": "<absolute path of the settings profile used>",
  "profile_sha256": "<64 hex>",
  "kind": "review",
  "repository": "MianliWang/gatebraid",
  "cwd": "D:/Github repo/Gatebraid",
  "slice_id": "<P<n>-S<m> for evidence and write kinds, else null>",
  "evidence_dir": "<docs/evidence/gatebraid/<slice_id>/ for evidence kinds, else null>",
  "head_before": "<40 hex>",
  "head_after": "<40 hex>",
  "porcelain_before": ["<each line of git status --porcelain --untracked-files=all, as read>"],
  "porcelain_after": ["<the same, after the run>"],
  "started_at": "<ISO8601 UTC>",
  "ended_at": "<ISO8601 UTC>",
  "outcome": "completed | refused | halted | timeout | error",
  "refusal": "<DD-Rnn or null>",
  "exit_status": 0,
  "command": ["claude", "-p", "...", "--output-format", "json"],
  "environment": {"GH_CONFIG_DIR": "C:/Users/rough/.gh-gatebraid", "PYTHONDONTWRITEBYTECODE": "1"},
  "stdout_sha256": "<64 hex>",
  "stderr_sha256": "<64 hex>",
  "claude_version": "<the executable's reported version>",
  "tool_paths": {"claude": "<path>", "git": "<path>", "gh": "<path>", "python": "<path>"},
  "dispatcher_version": "<sha256 of bin/gatebraid-dispatch.py as run>"
}
```

`head_before`/`head_after` and the two porcelain lists are measured by the
dispatcher with `git` in `cwd` immediately before and after the run. **The
post-run rule (`DD-R08`):** for a read-only kind, `head_after` must equal
`head_before` and the two porcelain lists must be equal as sets; for an
evidence kind, `head_after` must equal `head_before` and every porcelain line
present after the run and not before (or present in both with a different
status) must name a path under `evidence_dir` — the same exclusion of the
Slice's own evidence directory that ADR-0014 §1 applies to the baseline
re-read; a write kind has no post-run rule here (the Gate 2 contract's R1
and the Gate 3 contract govern what it may change). A failure is the outcome
`error` with refusal `DD-R08`, recorded after the fact (the run already
happened; the record says so). A whole-manifest refusal (`DD-R01`, or
`DD-R02`'s manifest-level half) is recorded too: `name` is `MANIFEST.json`,
`kind`, `slice_id`, `evidence_dir`, the heads and the lists are null, the
outcome is `refused` with the code, and the file is
`_handoff/outbox/MANIFEST.<stamp>.run.json`, where `<stamp>` is the
manifest's `written_at` with its colons removed (`2026-09-03T00:00:00Z` →
`2026-09-03T000000Z`; an ISO 8601 instant is not a portable filename, and
the executor host refuses colons). The record's own `written_at` field, when
present, keeps the original form.

## 3. Job kinds and profiles

| kind | profile | what the dispatch may direct | what the profile denies |
|---|---|---|---|
| `entry`, `gate0`, `gate1` | `evidence` | reads, `gh` reads, Python instruments with `-B`, writing under `_handoff/` and under the Slice's own evidence directory as the gate contract allows | any `git commit`/`push`, any write inside the repository outside the Slice's own evidence directory, any `gh` mutation except the acts the gate's own Exit names: its field writes, its handoff comment, and — for Gate 1 — the `needs-human` label and the one sanctioned rewrite of the Slice issue's metadata block (`protocols/gate-1-contract.md`, Exit) |
| `review`, `consult-prep` | `readonly` | reads; one report under `_handoff/`; scratch outside every repository | every write inside the repository, every `gh` mutation, any lease |
| `gate2` | `write` | commits on the Slice branch under the lease, field writes the contract names, no push | push; PR creation; any path outside the frozen allowlist (the contract's R1 is the check; the profile is the floor) |
| `gate3` | `write` | push of the Slice branch, PR creation, `gate3.md`, then HOLD at the merge door; the Exit after the operator's merge is a second `gate3` entry the coordinator lists once the merge is on record — no job spans a door | merge; branch deletion; any second branch |

Profiles are Claude Code settings files under the operator's control, one
per class, named `<class>.settings.json` (`readonly.settings.json`,
`evidence.settings.json`, `write.settings.json`) under the profiles
directory the operator provisioned, and named by absolute path in the run
record and hashed there. R-min defines the exact
allow and deny lists of all three; until R-min lands, only the `readonly`
profile exists, so stages 2–3 of the trial follow R-min or run as its first
live exercise under R-min's own approval (ADR-0034 decision 9 governs the
sequencing; this sentence repeats it and adds nothing). **No profile ever
contains a permission-bypass setting, and the dispatcher never passes one.**

## 4. The decision procedure (ordered; every failure is a refusal; codes are the fixtures' expected values)

The dispatcher evaluates, in this order, and stops at the first failure:

| code | check | on failure |
|---|---|---|
| `DD-R00` | `_handoff/inbox/STOP` absent | halt the dispatcher; record `halted` |
| `DD-R01` | `MANIFEST.json` parses; `schema` equals `gatebraid/dispatch-manifest@1`; every entry has every required key and no key outside the schema (`slice_id` is a schema key; whether it must be present is `DD-R03`'s rule) | refuse the whole manifest |
| `DD-R02` | first, once per manifest: every file in `_handoff/inbox/` other than `MANIFEST.json`, `STOP` and `RUNNING` is named by exactly one entry (ADR-0034 decision 1: anything not in the manifest is refused); then, for the entry: the named file exists; its sha256 and byte count equal the manifest's | an unlisted file, or a file named by two entries: refuse the whole manifest, naming the file; a mismatch: refuse the entry |
| `DD-R03` | `kind` is a member of the enumeration; `profile` matches the kind's class; `slice_id` is present exactly when the kind is an evidence or write kind, and matches its pattern | refuse the entry |
| `DD-R04` | `repository` is in the closed set; `cwd`'s `origin` names it | refuse the entry |
| `DD-R05` | the dispatch file's bytes pass the standing scans: no `owner/name` identity outside the closed set; no handoff-block schema token; no closing keyword immediately before an issue reference; no CR byte; no non-ASCII code point outside {U+00A7, U+00B7, U+2013, U+2014, U+2026, U+2192} | refuse the entry |
| `DD-R06` | `_handoff/inbox/RUNNING` absent | refuse the entry (a job is running) |
| `DD-R07` | the profile file for the entry's class exists and hashes; the `claude` executable resolves and reports a version; `git`, `gh` and `python` resolve | refuse the entry |
| — | **run**: write `RUNNING`; record `head_before` and `porcelain_before`; start `claude -p <dispatch bytes as the prompt> --output-format json` with `cwd`, the environment of §2.2, the profile, `--max-turns`; poll output and the STOP file; capture stdout and stderr as bytes | — |
| `DD-R08` | the post-run rule of §2.2: a read-only kind changed nothing (`head_after == head_before`, porcelain lists equal as sets); an evidence kind changed nothing outside `docs/evidence/gatebraid/<slice_id>/` and committed nothing; write kinds are not checked here | outcome `error`; the run record says which paths, or which head, moved |
| — | remove `RUNNING`; write the run record; move to the next entry only if `outcome` is `completed` and STOP is still absent | — |

An entry refused is not retried by the dispatcher; the coordinator corrects
the file or the manifest and re-lists it. A manifest is processed in entry
order; the coordinator lists at most the entries one session needs.

Every code has at least one seed in `fixtures/direct-drive/` (§10 says how the
two that cannot be staged as inbox state are seeded): `DD-R07` by a seed whose
host stub omits the profile file (DD-16); `DD-R08` by seeds that declare the
heads and porcelain lists before and after a run (DD-13, DD-14, DD-15), over
which fixture mode evaluates the post-run rule without running anything. In
addition, `DD-R07` is demonstrated once on the real host at stage 1 of the
trial by an entry naming a profile that does not exist — a refusal before any
run, with no write — and that run record is bound by stage 1's approval (§8).
`DD-R08` is not provoked on the real host: a job that writes under a profile
meant to deny it is not something the trial runs on purpose.

## 5. What the dispatcher never does

- Posts, edits or deletes any GitHub comment; writes any Project field;
  applies any label. Doors are operator acts; handoff comments are the
  executor's under its contract.
- Merges, deletes a branch, force-pushes, or pushes outside a `gate3` job.
- Runs two jobs at once, or any job while `RUNNING` or `STOP` exists.
- Passes a permission-bypass flag or a permission mode other than the
  profile's declared allowlist.
- Names, matches or enumerates any repository outside the closed set; the
  closed-set check is a whitelist, so the protected business repositories are
  refused without appearing anywhere in the tool.
- Runs on a schedule, a timer, or a trigger other than the operator starting
  it. A future scheduled mode is a new ADR.
- Reads a credential, sets one, or copies the dedicated store. It sets
  `GH_CONFIG_DIR` to the path the operator provisioned and nothing more
  (ADR-0024 §5).

## 6. The kill switch, demonstrated

Before first trusted use the operator runs the dispatcher in print-only mode
over `fixtures/direct-drive/DD-04.json` (the STOP-present seed) and,
separately, creates `STOP` while a long-running seeded job is in flight; the
run record must show `halted` in both cases, and the job's process must be
gone. Both records are retained as the batch's evidence.

## 7. Audit

After each run the coordinator stages the run record, the captured streams,
the executor's report and every artefact the report names, reproduces every
self-measured region and pin, and rules — exactly the post-hoc audit Part A
introduced. A run record whose `dispatch_sha256` differs from the coordinator's
own hash of the file it wrote is a stop-the-line event (the bytes that ran are
not the bytes that were sent).

## 8. Trial stages

ADR-0034 decision 9 governs; this section names the evidence each stage
commits: stage 0 — one run record per fixture (nineteen), all in fixture
mode, expected decision matched, nothing run; stage 1 — the replay's run
record, its report, a byte-level comparison table of its verdicts against the
recorded review's, and the `DD-R07` host seed's run record (a refusal before
any run; the stage's "zero writes" criterion is a property of the replay and
is not touched by it); stages 2–3 — the scratch Slice's own gate records,
which carry their run records by `output_ref`.

## 9. Host configuration

The dispatcher's host inputs are: the `claude` executable and its version; the
settings profiles; `git`, `gh`, `python`. Each is recorded in every run record
(`claude_version`, `tool_paths`, `profile_path`, `profile_sha256`); the batch
approval for each trial stage pins the profile sha256 values it expects, and a
run record carrying another value is a stop-the-line event at audit (§7), of
the same shape as the `dispatch_sha256` mismatch. No host file has normative
authority; this contract and the dispatch text bind.

## 10. Fixture mode, print-only mode, and the command line (`gatebraid/dispatch-fixture@1`)

**Fixture mode.** `bin/gatebraid-dispatch.py --fixture <path> [<path> ...]`
materialises each seed in a temporary directory — an inbox with the seed's
manifest, its inline files and its `STOP`/`RUNNING` state, and a profile
directory holding a stub file per profile class unless the seed's
`host.profile_present` is `false` — evaluates §4 from `DD-R00` through
`DD-R07` against it with `cwd` and the closed set measured on the real host,
runs nothing, and prints one line per seed:
`<id> expected <decision>/<code> got <decision>/<code> -> MATCH | MISMATCH`.
A seed carrying `setup.post_run` (`head_before`, `head_after`,
`porcelain_before`, `porcelain_after`, as the run record would hold them) is
evaluated one step further: after `DD-R07` passes, the post-run rule of §2.2
is applied to the declared states and the decision is `completed` (code
null) or `error` (`DD-R08`). A seed may carry `setup.substitutions`: a map
from a placeholder of the form `{NAME}` to a list of string parts; fixture
mode joins the parts, replaces every occurrence of the placeholder in every
inline body, and recomputes each affected entry's `sha256` and `bytes`
**before** `DD-R02` — this is how DD-07 and DD-11 carry a pattern no
committed file may hold, and a runner that skips the recomputation returns
the wrong code for both. A seed's `expected.decision` is one of `allow`,
`refuse`, `halt`, `completed`, `error`; `expected.code` is the §4 code or
null. The temporary directory is removed when the seed's line has been
printed; nothing under `_handoff/` or the repository is touched.

**Print-only mode.** `--print-only --inbox <dir> --profiles <dir> --outbox
<dir>` evaluates the real inbox exactly as fixture mode evaluates a seed,
without `post_run`, prints the command each admitted entry would run, and
writes nothing — not even a run record.

**The run form.** `--inbox <dir> --profiles <dir> --outbox <dir>` is the
form the operator starts for a trusted run; it is refused before the first
entry when `STOP` is present and behaves as §4 writes. `--inbox` defaults to
`_handoff/inbox`, `--outbox` to `_handoff/outbox`, `--profiles` to the path
the operator provisioned (never a repository path). No flag enables a
permission bypass, and the tool passes none to the executable it starts.

**Exit status, all modes.** `0`: every seed matched (fixture mode), or every
admitted entry reached `completed` (run form), or the print-only evaluation
finished; `1`: any `MISMATCH` (fixture mode), or any refusal, halt, timeout or
error (run form); `2`: a usage error, an unreadable input, or an I/O failure
before any evaluation. The status is printed as the last line of output in
the form `exit <n>` so a transcript states it.

**What the source may not contain.** The dispatcher is one file of Python 3
standard library (ADR-0028: committed, falsified on its seeds, reused). Its
source carries no handoff-block schema token (the pattern is assembled from
parts, as the seeds do), no closing keyword immediately before an issue
reference (the pattern is a regular expression, not an example), no
repository identity outside the closed set (the closed-set check is a
whitelist), no credential, no permission-bypass flag, and no scheduling.
