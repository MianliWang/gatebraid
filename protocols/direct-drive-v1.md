# Direct drive v1 — the dispatcher contract (`gatebraid-dispatch`)

**Status:** Proposed with ADR-0034 · lands in batch DD1 · Product: Gatebraid
(ADR-0010). This document is the contract the dispatcher implements and the
fixtures in `fixtures/direct-drive/` test. The fixtures precede the tool
(M3-PLAN §2); a decision this contract does not name is a refusal.

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
- `kind`: one of `gate0`, `gate1`, `review`, `consult-prep` (read-only kinds) and `gate2`, `gate3` (write kinds).
- `repository`: exactly `MianliWang/gatebraid` or `MianliWang/gatebraid-scratch`.
- `cwd`: the clone of that repository; the dispatcher verifies `git -C <cwd> remote get-url origin` names the same repository.
- `profile`: `readonly` for read-only kinds, `write` for write kinds; a mismatch is a refusal.
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
  "head_before": "<40 hex>",
  "head_after": "<40 hex>",
  "porcelain_before_lines": 0,
  "porcelain_after_lines": 0,
  "started_at": "<ISO8601 UTC>",
  "ended_at": "<ISO8601 UTC>",
  "outcome": "completed | refused | halted | timeout | error",
  "refusal": "<DD-Rnn or null>",
  "exit_status": 0,
  "command": ["claude", "-p", "...", "--output-format", "json"],
  "environment": {"GH_CONFIG_DIR": "C:/Users/rough/.gh-gatebraid", "PYTHONDONTWRITEBYTECODE": "1"},
  "stdout_sha256": "<64 hex>",
  "stderr_sha256": "<64 hex>",
  "dispatcher_version": "<sha256 of bin/gatebraid-dispatch.py as run>"
}
```

`head_before`/`head_after` and the porcelain counts are measured by the
dispatcher with `git` in `cwd`; for a read-only kind, `head_after` must
equal `head_before` and `porcelain_after_lines` must equal
`porcelain_before_lines`, else the outcome is `error` with refusal `DD-R08`
recorded after the fact (the run already happened; the record says so).

## 3. Job kinds and profiles

| kind | profile | what the dispatch may direct | what the profile denies |
|---|---|---|---|
| `gate0`, `gate1` | `readonly` | reads, `gh` reads, Python instruments with `-B`, writing under `_handoff/` and under the Slice's own evidence directory as the contract allows | any `git commit`/`push`, any `gh` mutation except the gate's own Exit field writes and handoff comment as the contract names them |
| `review`, `consult-prep` | `readonly` | reads; one report under `_handoff/`; scratch outside every repository | every write inside the repository, every `gh` mutation, any lease |
| `gate2` | `write` | commits on the Slice branch under the lease, field writes the contract names, no push | push; PR creation; any path outside the frozen allowlist (the contract's R1 is the check; the profile is the floor) |
| `gate3` | `write` | push of the Slice branch, PR creation, `gate3.md`, the Exit after the operator's merge | merge; branch deletion; any second branch |

Profiles are Claude Code settings files under the operator's control, named
by absolute path in the run record and hashed there. R-min defines the exact
allow and deny lists; until R-min lands, only the `readonly` profile exists
and only stages 0–1 of the trial run. **No profile ever contains a
permission-bypass setting, and the dispatcher never passes one.**

## 4. The decision procedure (ordered; every failure is a refusal; codes are the fixtures' expected values)

The dispatcher evaluates, in this order, and stops at the first failure:

| code | check | on failure |
|---|---|---|
| `DD-R00` | `_handoff/inbox/STOP` absent | halt the dispatcher; record `halted` |
| `DD-R01` | `MANIFEST.json` parses; `schema` equals `gatebraid/dispatch-manifest@1`; every entry has every required key and no unknown key | refuse the whole manifest |
| `DD-R02` | for the entry: the named file exists; its sha256 and byte count equal the manifest's | refuse the entry |
| `DD-R03` | `kind` is a member of the enumeration; `profile` matches the kind's class | refuse the entry |
| `DD-R04` | `repository` is in the closed set; `cwd`'s `origin` names it | refuse the entry |
| `DD-R05` | the dispatch file's bytes pass the standing scans: no `owner/name` identity outside the closed set; no handoff-block schema token; no closing keyword immediately before an issue reference; no CR byte; no non-ASCII code point outside {U+00A7, U+00B7, U+2013, U+2014, U+2026, U+2192} | refuse the entry |
| `DD-R06` | `_handoff/inbox/RUNNING` absent | refuse the entry (a job is running) |
| `DD-R07` | the profile file exists and hashes; the `claude` executable resolves; `git` and `gh` resolve | refuse the entry |
| — | **run**: write `RUNNING`; record `head_before` and porcelain; start `claude -p <dispatch bytes as the prompt> --output-format json` with `cwd`, the environment of §2.2, the profile, `--max-turns`; poll output and the STOP file; capture stdout and stderr as bytes | — |
| `DD-R08` | after a read-only kind: `head_after == head_before` and the porcelain count unchanged | outcome `error`; the run record says a read-only job wrote |
| — | remove `RUNNING`; write the run record; move to the next entry only if `outcome` is `completed` and STOP is still absent | — |

An entry refused is not retried by the dispatcher; the coordinator corrects
the file or the manifest and re-lists it. A manifest is processed in entry
order; the coordinator lists at most the entries one session needs.

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
over `fixtures/direct-drive/DD-04-stop-present.json` and, separately, creates
`STOP` while a long-running seeded job is in flight; the run record must show
`halted` in both cases, and the job's process must be gone. Both records are
retained as the batch's evidence.

## 7. Audit

After each run the coordinator stages the run record, the captured streams,
the executor's report and every artefact the report names, reproduces every
self-measured region and pin, and rules — exactly the post-hoc audit Part A
introduced. A run record whose `dispatch_sha256` differs from the coordinator's
own hash of the file it wrote is a stop-the-line event (the bytes that ran are
not the bytes that were sent).

## 8. Trial stages

ADR-0034 decision 9 governs; this section names the evidence each stage
commits: stage 0 — one run record per fixture, all print-only, expected
decision matched; stage 1 — the replay's run record, its report, and a
byte-level comparison table of its verdicts against the recorded review's;
stages 2–3 — the scratch Slice's own gate records, which carry their run
records by `output_ref`.

## 9. Host configuration

The dispatcher's host inputs are: the `claude` executable and its version; the
settings profiles; `git`, `gh`, `python`. Each is recorded by path and, for
files, by sha256 in every run record; R-min's conformance check compares the
profiles against a tracked baseline before any may influence a trusted run.
No host file has normative authority; this contract and the dispatch text
bind.
