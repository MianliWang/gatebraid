# Gate 1 evidence - P2-S5

## Plan (frozen at exit)

- **Approach.** Deliver the M2 slice-C frozen scope on the M3 stack: one program,
  `bin/gatebraid-ready.py`, a Python 3 standard-library composer that runs the
  O0-hardened producer as a subprocess, feeds its document to the O0-hardened
  consumer as a second subprocess, and passes the consumer's verdict through on
  stdout. Diagnostics go to stderr; stdout is always exactly one JSON document
  or nothing. It consumes both published tools and modifies neither. Beside it,
  `bin/gatebraid-ready-selftest.py`, the instrument that emits its own seeded-run
  summaries — the shape every one of the five landed tools already ships in, and
  the only way this Slice's Acceptance can be met, since that Acceptance forbids
  showing a class killed by narration.

  **The scope is read, not remembered.** It was read at this gate from the M2
  slice-C historical record in `MianliWang/gatebraid-scratch` at commit
  `dcd8e851bb508a2e17a6949434fc7c10354506c1`, and every document read is pinned
  by sha256 in the record row that produced it. All three historical attempts
  declare the identical scope: one file `bin/gatebraid-ready.py`; flags
  `--strict` and `--snapshot-command`; stdout one JSON document or nothing;
  producer failure and producer-output-undecodable as two distinct, loudly named
  exits; the consumer's own codes reused rather than renumbered; an allowlist of
  `bin/` plus the Slice's own evidence directory.

  **Four deltas between that frozen scope and the tools it now composes.** Each
  is resolved by applying the frozen rule to the tools as they are, never by
  re-deciding the scope, and each is stated so the Plan Approval can amend it.
  The fourth was not foreseen: it was found by running the dry-run, which is
  what action 4 exists for.

  **D-1, the consumer's code space moved.** The frozen rule is that the
  consumer's own codes are reused rather than renumbered, so a caller already
  reading them is not surprised, and that `10` and `11` sit outside the
  consumer's declared code space so they cannot be confused with a verdict. The
  M2 consumer declared `{0, 2, 3}`. The O0-hardened consumer declares four codes,
  read from its own module docstring rather than remembered: `0` report emitted
  from a healthy snapshot, `1` the snapshot was REFUSED and no verdict was
  emitted, `2` usage or input error, `3` report emitted and every verdict is
  `undecidable` because the snapshot was degraded. Applying the frozen rule
  unchanged: `ready` passes `0`, `1`, `2` and `3` through untouched and keeps
  `10` and `11` outside that set. The rule did not change; the set it ranges over
  is the consumer's, and it is read from the consumer. A code `ready` needs for
  itself — a usage error in its own arguments — takes `12`, the next value
  outside the consumer's space, rather than reusing the consumer's `2`: `ready`
  never declares a code the consumer owns, because for those it does not choose
  a value at all, it passes the child's status through. N6 checks both halves of
  that, and it reads the consumer's space from the consumer's own docstring.

  **D-2, `--strict` has no forwardee.** The frozen scope declares `--strict`
  forwarded to the consumer. The O0-hardened consumer accepts no such flag:
  every verdict being `undecidable` is exit `3` unconditionally, so what
  `--strict` used to select is now the consumer's only behaviour. `ready`
  therefore accepts `--strict`, forwards nothing, and says exactly that in its
  own `--help`. Forwarding it would make the consumer exit `2` on every
  invocation carrying it; rejecting it would break the frozen surface for a
  caller written against it. Retaining it as an accepted flag whose semantics the
  consumer now applies unconditionally is the only option that keeps both.

  **D-3, the default `--snapshot-command` cannot name `python`.** The frozen
  default is `python bin/gatebraid-snapshot.py`. On the Windows half of the
  declared environment `python` is the MSYS build, which carries no `jsonschema`,
  and the hardened producer validates its own output against the frozen schema
  before emitting. The default becomes the interpreter running `ready` itself,
  `sys.executable`, with `-B`, against `bin/gatebraid-snapshot.py` — the same
  resolution on both declared platforms, naming no host-specific absolute path.

  **D-4, the producer's exit status is interpreted, not tested against zero.**
  The frozen scope says a producer that exits non-zero is exit `10`. That was
  sound against the M2 producer, whose only non-zero exits meant no document.
  The O0-hardened producer declares four codes in its own module docstring: `0`
  snapshot emitted with every source `ok` and complete, `1` no document could be
  produced, `2` usage or input error, and **`3` snapshot emitted and DEGRADED**.
  Exit `3` carries a real, well-formed document that the consumer is built to
  classify — every item `undecidable` — and a composer that read any non-zero
  status as failure would discard it and hide the degradation from the only tool
  that can type it. The rule therefore becomes: **a producer status that means a
  document exists (`0` or `3`) passes the document to the consumer; a status that
  means no document exists (`1`, `2`, or anything undeclared) is exit `10`.**
  This delta was not predicted. It was found by running the D6 dry-run as
  written: `--project 999` against the real producer returned **exit 3 with four
  sources `network_error` and a degraded document**, not the no-document failure
  the frozen wording assumed. D6's declared command is therefore an input error
  that genuinely produces no document, and the degraded path is a selftest
  condition of its own. N6 reads BOTH tools' declared spaces for this reason.

  **One consequence worth stating rather than leaving to be noticed.** Friction
  #60 — the defect the whole exit-`11` guard exists to name — is closed at the
  root by O0's byte contract: producer and consumer now both write and read
  explicit UTF-8 through the binary layer. The guard can therefore no longer be
  provoked by the default producer. That is not a reason to drop it; it is
  precisely why the frozen scope carries `--snapshot-command`, whose stated
  reason is that without it the producer-failure and decode-guard paths cannot be
  run, only asserted. The guard is retained and exercised by a seeded stub
  emitting the same two bytes the M2 producer emitted.

- **Exact `write_domains` allowlist:**
  - `bin/`
  - `docs/evidence/gatebraid/P2-S5/`

- **What Gate 2 commits under `docs/evidence/gatebraid/P2-S5/`, proposed for the
  Plan Approval to ratify or amend.** Ruling 2 of the Gate 0 opening comment gave
  this Slice a per-gate layout, and this Slice is the first whose Gate 2 has to
  say what that layout means at commit time. The proposal, in four parts.
  *One.* Each gate keeps its own subdirectory: the retained record of the
  accepted stop keeps the top level, the Gate 0 re-run has
  `docs/evidence/gatebraid/P2-S5/g0r/`, this gate has
  `docs/evidence/gatebraid/P2-S5/g1/`, and Gate 2 writes
  `docs/evidence/gatebraid/P2-S5/g2/` including `g2/gate2.md`. No gate writes
  another gate's subdirectory, and no gate writes the top level.
  *Two.* The retained record and the re-run subdirectory **ride onto the Slice
  branch byte-identical**. They exist only in the working tree today; they are
  the evidence of a gate that closed, and leaving them uncommitted would publish
  a Slice whose Gate 0 has no committed record. They are committed unchanged,
  and `git diff` against the base for those paths is therefore an addition and
  never a modification.
  *Three.* The identity of what rides on is verified at Gate 2, not asserted: the
  retained-set path-list digest must still read
  `83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f`,
  `docs/evidence/gatebraid/P2-S5/gate0.md` must still read
  `be7c338896b1015923671988166d55af3bd59e028660ce89dfd3b69bc7251513`, and
  `docs/evidence/gatebraid/P2-S5/g0r/gate0.md` must still read
  `95ff39111b4a8b8aa43c022e877c98af5f868b054f4ac2c116ae5c67327bc4e6`. That is
  negative criterion N3's content limb, and it runs at Gate 2 as it ran here.
  *Four.* The Gate 2 baseline re-read treats those two subtrees as **untracked
  files that the Slice adds and does not author**. They are inside
  `write_domains` by prefix, so N1 admits them; N3's content limb is what
  actually holds them fixed. A baseline re-read that reported them as drift would
  be reporting the Gate 0 record's existence as a defect.
  **Nothing in this bullet is decided by this gate.** It is a proposal, it
  commits nothing, and Gate 2 does not open on it.

- **Tasks — three, independently verifiable.**
  - **T1 — the producer boundary and its encoding contract.** Run the producer as
    a subprocess; capture stdout as bytes; interpret the producer's status
    against its own declared space per D-4; decode explicitly as UTF-8. A
    producer status meaning no document, and a producer whose bytes do not
    decode, are two distinct, loudly named failures with distinct exits, `10` and
    `11`; a producer status meaning a degraded document is neither, and the
    document travels on. The program never guesses an encoding: a consumer that
    guesses converts a loud failure into silent corruption. Verified by D6, D7
    and the D3 degraded-producer condition.
  - **T2 — the composition and its exit algebra.** Feed the decoded document to
    the consumer as a subprocess, write the consumer's stdout through unchanged
    as bytes, and pass the consumer's own exit code through. Byte passthrough is
    load-bearing on this host today, not future-proofing: re-emitting decoded
    text through a text-mode stdout translates each embedded newline again.
    Verified by D5 and D8.
  - **T3 — the selftest.** One seeded condition per historical ready-failure
    class, each emitting its own summary row, plus a positive control that a tool
    rejecting everything would fail. Verified by D3 and D4.

- **Test plan (commands, runnable as written on the declared environment).**
  Every command is repository-relative and was dry-run at this gate; the rows are
  in `## Records`, and each row names the host it ran on. `environment:
  mixed-see-prose` — the tools run on the Windows host and the WSL half is
  evidence, so the transport-independent selftest and the evidence toolchain are
  declared on both halves. No command uses a temporary directory, because the
  shell and the interpreter disagree about what one means here.
  - **D0** `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/scope-pin.py`
    — green: exit 0, `SCOPE PIN HOLDS`, the pinned commit resolving to itself,
    every one of the seven documents re-deriving to its frozen sha256, and each
    scope assertion present in all three attempts.
    Covers: the Slice body's requirement that the frozen scope be read rather
    than remembered, and pinned by hash. Re-run at Gate 2, it is what would
    detect the historical record having moved under the plan.
  - **D0F** the same command with `--commit` naming the pinned commit's parent
    — green: exit 1, `SCOPE PIN STALE`, the commit limb reporting
    `NOT THE PINNED COMMIT`, at least one document `ABSENT AT THIS COMMIT`, and
    the scope assertions dropping below three of three.
    Covers: the pin is falsified before it is trusted. A pin that has only ever
    matched has measured nothing.
  - **D1** `PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B fixtures/runner-selftest.py`
    — green: exit 0, `digest after` equals
    `73c5e059091982ac8cda43d9f59902f3934444b742e7a383ad9422448cd5fdfc`,
    `seed-reachable surface UNMODIFIED: True`, `conditions failed : 0`.
    Covers: this Slice consumes the batch-frozen corpus and authors none of it.
  - **D2** `PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B fixtures/run-corpus.py`
    — green: exit 0, `TOTAL: 133 passed, 0 failed`, `CORPUS CLEAN`, and every
    `BP1` and `IN1` row present and `ok`.
    Covers: Acceptance item 3 for the seven historical ready-failure classes the
    frozen corpus holds — BP-01, BP-02, BP-03, IN-02, IN-03, IN-04 and IN-05 —
    each shown killed by the runner's own emitted summary row naming the locus,
    never by narration. **IN-01 is deliberately absent from the frozen corpus**
    by that corpus's own declared `known_limitation`, so it cannot be shown
    killed from the corpus and is not claimed to be; it is carried by D3 instead.
  - **D3** `PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready-selftest.py`
    — green: exit 0, `conditions failed : 0`, `SELFTEST CLEAN`, `network reads
    performed : 0`, and a present, passing row for each of: the positive control;
    producer non-zero exit yielding `10`; producer bytes that do not decode
    yielding `11`; a decodable but malformed document yielding the consumer's own
    refusal code and no verdict; a healthy replayed document yielding `0` with
    the consumer's report on stdout byte-for-byte; a degraded replayed document
    yielding `3` with the report still on stdout; a producer that exits `3` with
    a DEGRADED but well-formed document having that document passed on rather
    than discarded, the D-4 rule seeded from the producer side; `--strict`
    accepted and changing nothing; and **the IN-01 condition** — a composition
    whose first stage fails and whose second stage would succeed must never
    report success.
    Covers: T1, T3, Acceptance item 3's IN-01 remainder, and the D-1 and D-2
    resolutions.
  - **D4** `wsl.exe -e bash -lc "cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-ready-selftest.py"`
    — green: exit 0, `SELFTEST CLEAN`, `network reads performed : 0`.
    Covers: the WSL half of the declared environment.
  - **D5** `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid C:/Python312/python.exe -B bin/gatebraid-capture.py --out docs/evidence/gatebraid/P2-S5/g2/captures/G2-live-ready.json --capture-id G2-live-ready --env GH_CONFIG_DIR --input bin/gatebraid-ready.py --input bin/gatebraid-snapshot.py --input bin/gatebraid-frontier.py -- C:/Python312/python.exe -B bin/gatebraid-ready.py`
    — green: the captured run exits 0; its recorded stdout parses as exactly one
    JSON document; that document carries a verdict for
    `MianliWang/gatebraid#17`; and the capture's stderr shows the producer's four
    sources each `ok` and `complete=True`.
    Covers: T2 end to end against the real control plane, and Acceptance item 4's
    requirement that control-plane state be read through the O0 outputs alone.
  - **D6** `C:/Python312/python.exe -B bin/gatebraid-ready.py --snapshot-command "C:/Python312/python.exe -B bin/gatebraid-snapshot.py --replay docs/evidence/gatebraid/P2-S5/g1/dryrun-out/no-such-transcript.json"`
    — green: exit **10**, stdout empty, stderr carrying the producer's own
    `USAGE: no transcript at ...` message and its exit status `2`.
    Covers: T1's producer-failure limb against the REAL producer, on a status
    that genuinely means no document. The named transcript is deliberately
    absent; the command needs no network and runs identically on both declared
    platforms. It replaced `--project 999`, which the dry-run showed returns
    exit `3` with a degraded document rather than a no-document failure — the
    D-4 discovery, and the reason this row now names an input error instead.
  - **D7** `C:/Python312/python.exe -B bin/gatebraid-ready.py --snapshot-command "<the cp936 stub>"`, where the stub writes
    `('{' + chr(34) + 'name' + chr(34) + ': ' + chr(34) + 'Gate 0 ' + chr(0x2014) + ' Verifying' + chr(34) + '}').encode('cp936')`
    to the binary stdout layer — green: exit **11**, stdout empty, stderr naming
    the decode failure and the offending byte. Every quote and the em dash are
    built with `chr()`: a literal em dash through nested quoting yields a
    zero-byte stub, and the guard then appears to pass while testing nothing.
    Covers: T1's decode-guard limb, on the same two bytes the M2 producer emitted.
  - **D8** `C:/Python312/python.exe -B bin/gatebraid-ready.py --snapshot-command "<the empty-object stub>"`, where the stub writes
    the two bytes of an empty JSON object to the binary stdout layer — green:
    exit **1**, the consumer's own refusal code passed through unchanged, stdout
    empty, stderr carrying the consumer's own `SNAPSHOT REFUSED` message.
    Covers: T2's passthrough of the consumer's code space, and D-1.
  - **D9** `PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/negative-criteria.py`
    — green: exit 0, `NEGATIVE CRITERIA HOLD: N1, N2, N3, N4, N5, N6`.
    Covers: review item R4 at Gate 2.
  - **D10** `PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/negative-criteria.py --changed-from docs/evidence/gatebraid/P2-S5/g1/SEED-negative-criteria.txt --code-surface-dir docs/evidence/gatebraid/P2-S5/g1/falsification --frozen-root docs/evidence/gatebraid/P2-S5/g1/falsification/frozen-root`
    — green: exit 1, `NEGATIVE CRITERIA FIRED: N1, N2, N3, N4, N5, N6`, and every
    criterion firing on its SUBSTANTIVE limb rather than on an absent file.
    Covers: the criteria are falsified, not merely asserted. A criterion that has
    only ever held has never been shown able to fire. Each override the command
    carries exists for that one reason: they point the SAME instrument at a
    seeded input, never a copy of it at the real one.
  - **D11** `wsl.exe -e bash -lc "cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-capture.py --out docs/evidence/gatebraid/P2-S5/g2/captures/G2-wsl-ready-selftest.json --capture-id G2-wsl-ready-selftest -- python3 -B bin/gatebraid-ready-selftest.py"`
    followed by
    `wsl.exe -e bash -lc "cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S5/g2/gate2.md --report-id cov-P2-S5-g2-gate2-wsl.md"`
    — green: both exit 0; the first writes a capture whose `platform.os` reads
    **`wsl`** and whose `platform.interpreter` names CPython 3.12.3, the second
    prints `verdict : accepted` above a loader line naming that same
    interpreter. The value is `wsl` and not `linux`: it was measured at this
    gate rather than assumed, and an expected-green criterion written from the
    assumption would have failed a correct run.
    Covers: Acceptance item 4's requirement that the evidence toolchain run on the
    declared platforms — generation by the capture tool and validation by the
    validator, each shown running on WSL and not only on Windows.

  **Acceptance criteria of the Slice body, mapped item by item.** Item 1, the
  Gate 3 exit with `R3 first-pass = pass`, is a gate outcome and not a command;
  it is evaluated at Gate 2's review and at Gate 3, and the plan's contribution
  to it is that every record of this Slice is generated by a renderer from
  captures rather than hand-authored, which is the defect that failed R3 four
  times in the M2 chain. Item 2, `evidence-only repairs = 0` and
  `evidence-only aborts = 0`, is likewise a count over the Slice and is measured
  at closeout from the gate records' own repair-attempt blocks; the plan's
  contribution is the same. Item 3 maps to **D2** for the seven classes the
  frozen corpus holds and to **D3** for IN-01, which it does not. Item 4 maps to
  **D5** for the control-plane half and to **D11** for the two-platform half,
  with every capture in this Slice written by `bin/gatebraid-capture.py` and
  every record validated by `bin/gatebraid-validate.py` with `--report-id` passed
  explicitly.

- **Risk notes.** `risk: low` is justified by blast radius and reversibility, not
  by ease. The program performs no control-plane mutation of its own; its only
  network effect is whatever the read-only producer already performs. It writes
  no file, holds no credential, and modifies nothing it consumes. Four
  substantive risks, each with the check that fails it.
  *First*, conflating producer failure with an empty or malformed document, which
  would let a broken pipeline read as no slice being startable — the most
  dangerous silent failure a frontier tool has. D6, D7 and D8 separate the three
  causes by exit code, and the IN-01 selftest condition is the same failure in
  its pipeline form.
  *Second*, guessing an encoding when the decode fails, which would turn a loud
  stop into corruption inside a state document; D7 requires exit `11` rather than
  a best-effort decode.
  *Third*, the exit algebra colliding with the consumer's as that consumer
  changes again. This is not hypothetical: it is exactly what D-1 above had to
  resolve, one hardening later. N6 mechanises the invariant against the
  consumer's own declared codes rather than against a remembered list, so the
  collision is caught by a check and not by a reader.
  *Fourth*, `--snapshot-command` executes whatever it is handed, so the claim of
  performing no control-plane mutation is a property of the default producer and
  is stated as such; N5's transitive limb checks that default and says so.
  Two risks are carried rather than mitigated. Friction #60's root repair is
  O0's, already landed, so `ready` inherits it rather than owning it; and
  `bin/gatebraid-frontier.py` still carries the deferred ADR-0033 identity-key
  defect, which means the report `ready` passes through declares no `schema` key
  and is classified interface-not-covered by the validator. This Slice consumes
  that consumer as it stands and repairs nothing in it: one Slice, one tool.
  `consult_first: false` is deliberate. There is no open design question a
  consultation would settle: the scope is frozen and read, the two tools it
  composes are landed and byte-pinned, and the three deltas are each a
  mechanical application of a frozen rule to a surface that was measured rather
  than recalled.

- **Rollback note.** Nothing is committed until Gate 2 under a `Writer Lease`,
  and the whole Slice lives on its own branch cut from the head re-read under
  that lease. To abandon at any point: leave `main` where it is and stop — no
  push has occurred, no other Slice depends on this branch, and both the retained
  P2-S5 Gate 0 record and its re-run subdirectory are untouched by construction,
  which N3 mechanises from the diff side. If a branch already exists it is
  retained as a record and never merged; ADR-0025 section 3 governs. If
  abandonment happens after a push but before a merge, the branch is retained and
  the pull request closed unmerged; no force push is available under any
  circumstance. The deliverable is two new files that nothing else imports, so a
  revert after a merge removes them completely and leaves all five landed tool
  pairs exactly as they were.

- **Negative criteria (checkable).** All six are mechanised in
  `docs/evidence/gatebraid/P2-S5/g1/negative-criteria.py`, each stating the
  pattern it proxies for, the scope it searches, and the direction in which it
  errs. All six are falsified before trust at this gate: each fires against a
  seeded input at D10 and all six hold against the real tree at D9.
  - **N1 — the diff contains no path outside the allowlist.** Scope: every path
    of `git diff --name-only <base_sha>` together with the untracked set. Errs
    toward false alarm: a path lawfully inside but spelled differently is
    reported rather than passed; it never passes a path that is outside.
  - **N2 — under `bin/`, only the ready pair is touched.** Scope: glob `bin/**`;
    the changed set under it must be a subset of the two added files. Errs toward
    false alarm: any other file under `bin/` fires even where a human would call
    it in scope; it never passes an edit to one of the five landed pairs. This is
    the Non-goals list mechanised.
  - **N3 — no frozen input is written.** Two limbs, and the second is not a path
    rule. *Limb (a), scope: the explicit prefix set* `schema/`, `fixtures/`,
    `adr/`, `protocols/`, `templates/`, `projects/`,
    `docs/evidence/gatebraid/P2-S1/`, `docs/evidence/gatebraid/P2-S2/`,
    `docs/evidence/gatebraid/P2-S3/`, `docs/evidence/gatebraid/P2-S4/` and
    `docs/evidence/gatebraid/P2-S6/` — no changed path may lie under one.
    *Limb (b), scope: the content of the retained Gate 0 record* — the file count
    of `docs/evidence/gatebraid/P2-S5/` with the re-run and this gate's own
    subdirectories excluded must be forty-three, its path-list digest must still
    be `83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f`,
    `docs/evidence/gatebraid/P2-S5/gate0.md` must still be
    `be7c338896b1015923671988166d55af3bd59e028660ce89dfd3b69bc7251513`, and
    `docs/evidence/gatebraid/P2-S5/g0r/gate0.md` must still be
    `95ff39111b4a8b8aa43c022e877c98af5f868b054f4ac2c116ae5c67327bc4e6`.
    The second limb exists because no path rule can protect those files: they sit
    under this Slice's own evidence prefix, so a prefix forbidding writes there
    would forbid the Slice writing at all. Content is therefore what is checked.
    Errs toward false alarm on both limbs: any byte change anywhere in the
    retained set moves the digest and fires, including one a human would call
    harmless. It never passes a modified retained record.
  - **N4 — the code surface adds no runtime dependency and constructs no HTTP
    client.** Scope: the import sets of the two added files only, compared
    against a baseline non-stdlib set that is empty, because the frozen scope is
    a standard-library program. Errs toward false alarm: a stdlib module merely
    named like a network client is reported for a human read, and any non-stdlib
    import fires even if benign; it never passes a real network client and never
    passes a new dependency. This is the hard rule that authentication is
    delegated to the command-line client, mechanised.
  - **N5 — no control-plane mutation, and no file written by the tool.** Two
    parts, because either alone is unsound. *File-local, scope: the two added
    files* — zero GraphQL documents whose operation type is a mutation, which is
    not the same as that word occurring in prose, and zero `open(` in a write
    mode. *Transitive, scope: `bin/gatebraid-snapshot.py`, the default
    `--snapshot-command` target* — every GraphQL document it carries opens
    `query(` and none opens a mutation. The HTTP method is deliberately not the
    proxy: a read-only GraphQL query is sent by POST, so a check for
    no-method-other-than-GET reports a violation where there is none. Errs toward
    false alarm on the file-local limb and is exact on the transitive one. It
    never passes a mutation document.
  - **N6 — `ready` declares no exit code inside either composed tool's declared
    code space, and declares both of its own.** Scope: the module-level `EXIT_`
    integer constants of `bin/gatebraid-ready.py`, and the code space parsed from
    the `Exit codes:` paragraph of `bin/gatebraid-frontier.py`'s and
    `bin/gatebraid-snapshot.py`'s own module docstrings — so the invariant is
    checked against those tools as they are rather than against a remembered
    list. Two conditions: the declared set is disjoint from the union of both
    spaces, and it contains `10` and `11`. Codes a composed tool owns are never
    declared by `ready`, because for those `ready` chooses no value at all — it
    passes the child's status through. A code `ready` needs for itself, such as a
    usage error in its own arguments, takes `12`, the next value outside both
    spaces. The producer's space is read as well as the consumer's because of
    D-4: the producer's `3` means a document exists, so the composer must
    interpret that status rather than test it against zero. Errs toward false
    alarm: a docstring the parser cannot read is a failure rather than a pass, so
    an unparseable composed tool stops the check instead of silently vacating it.
    It never passes a `ready` code that collides with a composed tool's code.

## Records

**P1 - Agent Team: NOT used, and the decision recorded rather than left implicit**
```
gate-1-contract action 2 makes the read-only team OPTIONAL. No team was
spawned for this Slice, for two reasons and the second is decisive.
(1) The question this gate had to answer - what the frozen scope IS - is
    answered by reading seven named documents at one named commit and
    hashing them. That is what scope-pin.py does, reproducibly; a teammate
    could not do it more reliably, and a teammate's report of it would be
    narration where a hash is available.
(2) Action 2 requires all findings to be FLUSHED TO THE SLICE ISSUE before
    the team dissolves. That flush is a control-plane mutation, and this
    window holds approval for exactly four writes: the handoff comment, the
    write_domains post-condition, the four field updates, and nothing else.
    Spawning a team would have forced either an unapproved mutation or a
    violated constraint.
There are therefore NO team findings to flush, and the constraint list of
failure-disposition row 2 is vacuously satisfied rather than exercised.
(no command: nothing was spawned)
```

**P2 entry - the control-plane read, through the O0 outputs alone**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid C:/Python312/python.exe -B bin/gatebraid-snapshot.py --out docs/evidence/gatebraid/P2-S5/g1/captures/g1-snapshot.json --generated-at 2026-09-01T21:39:34Z

generator                     : gatebraid-snapshot 1.0.0
schema                        : D:\Github repo\Gatebraid\schema\snapshot.schema.json sha256=95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6
transport                     : live
sources                       : 4
   project_items    ok                   complete=True  exit=0
   issue_states     ok                   complete=True  exit=0
   dep_blocked_by   ok                   complete=True  exit=0
   dep_blocking     ok                   complete=True  exit=0
items                         : 16
degraded                      : no
SNAPSHOT OK: every source read completely with status `ok`
(exit 0)
$ C:/Python312/python.exe -B bin/gatebraid-frontier.py docs/evidence/gatebraid/P2-S5/g1/captures/g1-snapshot.json --out docs/evidence/gatebraid/P2-S5/g1/captures/g1-frontier-report.json

consumer                      : gatebraid-frontier 1.0.0
validated against             : D:\Github repo\Gatebraid\schema\snapshot.schema.json sha256=95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6
items excluded (no verdict)   : 4
startable                     : 9
blocked                       : 3
undecidable                   : 0
FRONTIER OK: the snapshot validated and every verdict was re-derived from it
(exit 0)
```

**P2 entry - Gate = G0 passed, read by node key because the snapshot carries no Gate field**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query{node(id:"PVTI_lAHOBRofUs4Beum7zg4E8qs"){... on ProjectV2Item{fieldValues(first:50){nodes{... on ProjectV2ItemFieldSingleSelectValue{optionId name field{... on ProjectV2FieldCommon{name}}} ... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2FieldCommon{name}}}}}}}}'
{"data":{"node":{"fieldValues":{"nodes":[{},{"text":"P2-S5 — O1 gatebraid-ready: the fourth attempt on the frozen scope","field":{"name":"Title"}},{"optionId":"f75ad846","name":"Todo","field":{"name":"Status"}},{"optionId":"f6b57153","name":"Gate 1 — Planning","field":{"name":"Workflow"}},{"optionId":"6922003a","name":"G0 passed","field":{"name":"Gate"}},{"optionId":"450ee130","name":"—","field":{"name":"Next Approval"}},{"optionId":"1e43ec85","name":"mixed-see-prose","field":{"name":"Environment"}},{"optionId":"ce859c7d","name":"Claude Lead","field":{"name":"Executor"}},{"optionId":"e291249c","name":"low","field":{"name":"Risk"}},{"text":"S2","field":{"name":"Stage"}},{"text":"P2","field":{"name":"Phase"}},{"text":"P2-S5","field":{"name":"Slice"}},{"text":"7ff1f848661aac20b3921ae47fe140394a5d2587","field":{"name":"Base SHA"}},{"text":"2026-09-01T20:39:35Z P2-S5 GATE 0 RE-RUN PASSED on a HEALTHY read; Ruling 1 retired D-2. snapshot exit 0, 4/4 sources ok+complete, 16 items, not degraded; frontier exit 0, snapshot_degraded false, P2-S5 verdict startable RE-DERIVED; blocked_by 8/10/12/14/19 all CLOSED, cross_check consistent. Actions 1-6 pass. base_sha cbd06589 untouched at G0; tracked ZERO; retained digest 83b3a273 EQUAL, g0r excluded. Opening comment 5472973466 MianliWang verified. Gate 6922003a; Workflow f6b57153; Next Approval 450ee130 unchanged; read back MATCH. Evidence UNCOMMITTED at P2-S5/g0r/; gate0.md 95ff3911 ACCEPTED 0 findings, --report-id explicit; record sweep residue 0. RETAINED record be7c3388 UNTOUCHED. STOPPED ONCE on unextended sweep residue; Rulings A+B 2026-08-31 gave 3 domain facts, g0r copy only, no rule changed; N4 falsified out-of-namespace. capture-set fail = known placeholder defect, as merged P2-S6. 5a ADR-0033, 5b body 4-vs-5 edges disclosed. handoff 5500114756. No lease/commit/push. GATE 1 NOT OPENED.","field":{"name":"Last Checkpoint"}}]}}}}
(exit 0)
```

**P2 D0 - the frozen scope, read at a named commit and pinned by hash**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/scope-pin.py
historical record : MianliWang/gatebraid-scratch
pinned commit     : dcd8e851bb508a2e17a6949434fc7c10354506c1
reading at        : dcd8e851bb508a2e17a6949434fc7c10354506c1
resolves to       : dcd8e851bb508a2e17a6949434fc7c10354506c1  MATCH

document                                       bytes    sha256 re-derived
README.md                                      984      e0a5b2689f0e9f08f680077c5cd29f9a1f0f230c78260c39b10542cdf690c730  MATCH
docs/evidence/gatebraid/P1-S3/gate0.md         9000     cc783192e688e677a18d49febedc1cfb1174c8e875056062284d7b7d4e242f81  MATCH
docs/evidence/gatebraid/P1-S3/gate1.md         24576    0966759be9e1b05fea310965e6ac36112244185f6434647bb3f1ec2ed32b21cb  MATCH
docs/evidence/gatebraid/P1-S5/gate0.md         14387    a0fd819614744faf9317f84f4b6532e249fe32c3d35307dabd28160cd356d145  MATCH
docs/evidence/gatebraid/P1-S5/gate1.md         26299    edfc92054015b7190ba79eb94c9da114ce0eec4714acdd3b301628550ee74f33  MATCH
docs/evidence/gatebraid/P1-S6/gate0.md         5996     89af2e287272947f307b2f72d9541e481c508c9e90c6d99cd994061282698c5c  MATCH
docs/evidence/gatebraid/P1-S6/gate1.md         19371    b190299bccaa906548d44477eca18e5579cbb480e4192c52fba5f801bd71920f  MATCH

scope assertions, each required in ALL THREE attempts:
   bin/gatebraid-ready.py   in 3 of 3  ok     the one file the scope delivers
   --snapshot-command       in 3 of 3  ok     the flag whose stated reason is that the guard paths must be runnable, not merely asserted
   --strict                 in 3 of 3  ok     the flag the M2 consumer accepted

SCOPE PIN HOLDS: the commit resolves and every document re-derives to the frozen hash
(exit 0)
```

**P2 D0F - the same instrument at the pinned commit's parent: the pin fires**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/scope-pin.py --commit a8e15e0de2d5df285a79c8a34d1a966fee86e678
historical record : MianliWang/gatebraid-scratch
pinned commit     : dcd8e851bb508a2e17a6949434fc7c10354506c1
reading at        : a8e15e0de2d5df285a79c8a34d1a966fee86e678   (OVERRIDDEN - falsification run)
resolves to       : a8e15e0de2d5df285a79c8a34d1a966fee86e678  *** NOT THE PINNED COMMIT ***
[... shown 14 of 20 lines; full output: docs/evidence/gatebraid/P2-S5/g1\captures/G1-dryrun-D0F-scope-pin-falsify.json]
docs/evidence/gatebraid/P1-S5/gate1.md         26299    edfc92054015b7190ba79eb94c9da114ce0eec4714acdd3b301628550ee74f33  MATCH
docs/evidence/gatebraid/P1-S6/gate0.md         5996     89af2e287272947f307b2f72d9541e481c508c9e90c6d99cd994061282698c5c  MATCH
docs/evidence/gatebraid/P1-S6/gate1.md         -        *** ABSENT AT THIS COMMIT ***

scope assertions, each required in ALL THREE attempts:
   bin/gatebraid-ready.py   in 2 of 3  FAIL   the one file the scope delivers
   --snapshot-command       in 2 of 3  FAIL   the flag whose stated reason is that the guard paths must be runnable, not merely asserted
   --strict                 in 2 of 3  FAIL   the flag the M2 consumer accepted

SCOPE PIN STALE: 5 item(s) did not re-derive
(exit 1)
```

**P2 D1 - the frozen corpus digest is unmoved by this Slice**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B fixtures/runner-selftest.py
condition                           want  got  verdict  required observation
S00 untouched copy                     0    0  PASS     CORPUS CLEAN
[... shown 16 of 37 lines; full output: docs/evidence/gatebraid/P2-S5/g1\captures/G1-dryrun-D1-corpus-digest.json]
S27 __pycache__ present                0    0  PASS     CORPUS CLEAN
S11 unexpected argument                2    2  PASS     unexpected argument
S15 cwd-independence holds             0    0  PASS     CORPUS CLEAN from both
S16 cwd-independence falsified       !=0    2  PASS     must NOT be clean from elsewhere
S21 digest sees run-corpus.py       moves  moves  PASS     digest must change when the file changes
S22 digest sees runner-selftest.py  moves  moves  PASS     digest must change when the file changes
S28 __pycache__ moves no digest     same  same  PASS     digest must ignore interpreter output

digest scope                  : bytes-platform, evidence-capture-v1, gate-run-v2, instruments, live-shapes, metrics-v1, state-pipeline, CORPORA.json, schema, run-corpus.py, runner-selftest.py, fixtures/ listing
digest before                 : 73c5e059091982ac8cda43d9f59902f3934444b742e7a383ad9422448cd5fdfc
digest after                  : 73c5e059091982ac8cda43d9f59902f3934444b742e7a383ad9422448cd5fdfc
seed-reachable surface UNMODIFIED: True
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
(exit 0)
```

**P2 D2 - the historical ready-failure classes the frozen corpus holds, each killed on a named locus**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B fixtures/run-corpus.py
corpus bytes-platform (v1.1)  <- fixtures\bytes-platform\EXPECTATIONS.json
  loader recorded: CPython 3.12.2 (C:/Python312/python.exe), jsonschema 4.23.0, Draft202012Validator; re-measured identical under CPython 3.12.3 / jsonschema 4.10.3 on WSL
  ok   BP1-01  valid as recorded  [positive control �� one report, one platform, honestly claimed]
  ok   BP1-02  valid as recorded  [positive control �� the only legitimate way to claim both platforms]
  ok   BP1-03  killed on required@properties/1/replay:rederived_sha256 [properties/properties/items/properties/replay/required]  [BP-01 blocked remainder �� sha256 over raw bytes fails to re-derive]
  ok   BP1-04  killed on pattern@properties/1/replay/rederived_sha256 [properties/properties/items/properties/replay/properties/rederived_sha256/pattern]  [BP-02 blocked remainder �� byte_length mismatch caught]
  ok   BP1-05  killed on minItems@dual_platform_claim/reports [properties/dual_platform_claim/properties/reports/minItems]  [BP-03 �� one platform's capture presented as covering both]
  ok   BP1-06  killed on uniqueItems@dual_platform_claim/reports [properties/dual_platform_claim/properties/reports/uniqueItems]  [BP-03 �� the item verbatim: the same capture cited for both platforms]
  ok   BP1-07  killed on type@platform [properties/platform/type]  [BP-03 �� one report presenting ITSELF as covering both]
  ok   BP1-08  killed on required@properties/1:replay [properties/properties/items/allOf/0/then/required]  [BP-01 / BP-02 claim discipline �� a replayed claim with nothing behind it]
[... shown 24 of 156 lines; full output: docs/evidence/gatebraid/P2-S5/g1\captures/G1-dryrun-D2-corpus.json]
  ok   SP1-07  killed on const@sources/0/status [properties/sources/items/allOf/2/then/properties/status/const]  [SP-03 rate limit]
  ok   SP1-08  killed on const@sources/0/complete [properties/sources/items/allOf/3/then/properties/complete/const]  [SP-04 network / server error]
  ok   SP1-09  killed on const@items/0/verdict [allOf/0/then/properties/items/items/properties/verdict/const]  [SP-05 malformed GitHub response]
  ok   SP1-10  killed on required@sources/0:bounded [properties/sources/items/allOf/4/then/required]  [SP-06 missing dependency page]
  ok   SP1-11  killed on const@sources/0/complete [properties/sources/items/allOf/5/then/properties/complete/const]  [SP-07 truncated connections]
  ok   SP1-12  killed on const@items/0/verdict [properties/items/items/allOf/0/then/properties/verdict/const]  [SP-08 unknown Issue state]
  ok   SP1-13  killed on not@items/0 [properties/items/items/allOf/1/then/not], required@items/0:excluded_reason [properties/items/items/allOf/1/then/required]  [SP-09 non-Slice Project item]
  ok   SP1-14  killed on required@(root):schema [required]  [SP-10 missing snapshot schema / version]
  ok   SP1-15  killed on required@items/0/dependencies:blocking [properties/items/items/properties/dependencies/required]  [SP-11 one-direction dependency loss]
  ok   SP1-16  killed on required@items/0/soft_dependencies:parse_status [properties/items/items/properties/soft_dependencies/required]  [SP-12 soft Gate-1/Gate-2 dependency unsatisfied]
  ok   SP1-17  killed on not@items/0/verdict [properties/items/items/allOf/5/then/properties/verdict/not]  [SP-13 aborted item presented as ready]

TOTAL: 133 passed, 0 failed
CORPUS CLEAN
(exit 0)
```

**P2 D3 - ready selftest, Windows half: RUN AS DECLARED; names the absent deliverable and nothing else**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready-selftest.py

C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-ready-selftest.py': [Errno 2] No such file or directory
(exit 2)
```

**P2 D4 - ready selftest, WSL half: RUN AS DECLARED; the same absence on the other declared platform**
```
$ wsl.exe -e bash -lc 'cd '\''/mnt/d/Github repo/Gatebraid'\'' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-ready-selftest.py'

python3: can't open file '/mnt/d/Github repo/Gatebraid/bin/gatebraid-ready-selftest.py': [Errno 2] No such file or directory
(exit 2)
```

**P2 D5 - live end-to-end: RUN AS DECLARED, output directory substituted**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready.py

C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-ready.py': [Errno 2] No such file or directory
(exit 2)
```

**P2 D6 - producer failure: RUN AS DECLARED, and the companion probe carrying the real producer status**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready.py --snapshot-command 'C:/Python312/python.exe -B bin/gatebraid-snapshot.py --replay docs/evidence/gatebraid/P2-S5/g1/dryrun-out/no-such-transcript.json'

C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-ready.py': [Errno 2] No such file or directory
(exit 2)
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-snapshot.py --replay docs/evidence/gatebraid/P2-S5/g1/dryrun-out/no-such-transcript.json

USAGE: no transcript at docs/evidence/gatebraid/P2-S5/g1/dryrun-out/no-such-transcript.json
(exit 2)
```

**P2 D6 probe - the D-4 discovery: --project 999 returns a DEGRADED DOCUMENT, not a producer failure**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-snapshot.py --project 999
{
 "generated_at": "2026-01-01T00:00:00Z",
[... shown 14 of 81 lines; full output: docs/evidence/gatebraid/P2-S5/g1\captures/G1-probe-D6-producer-failure.json]

generator                     : gatebraid-snapshot 1.0.0
schema                        : D:\Github repo\Gatebraid\schema\snapshot.schema.json sha256=95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6
transport                     : live
sources                       : 4
   project_items    network_error        complete=False exit=1  bounded
   issue_states     network_error        complete=False exit=65  bounded
   dep_blocked_by   network_error        complete=False exit=65  bounded
   dep_blocking     network_error        complete=False exit=65  bounded
items                         : 0
degraded                      : yes
SNAPSHOT DEGRADED: every item carries verdict `undecidable`; exit status 3 so no caller reads this as a healthy read
(exit 3)
```

**P2 D7 - decode guard: RUN AS DECLARED, and the stub whose bytes are the pair that broke the M2 pipeline**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready.py --snapshot-command 'C:/Python312/python.exe -c import sys;q=chr(34);s='\''{'\''+q+'\''name'\''+q+'\'': '\''+q+'\''Gate 0 '\''+chr(0x2014)+'\'' Verifying'\''+q+'\''}'\'';sys.stdout.buffer.write(s.encode('\''cp936'\''))'

C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-ready.py': [Errno 2] No such file or directory
(exit 2)
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -c 'import sys;q=chr(34);s='\''{'\''+q+'\''name'\''+q+'\'': '\''+q+'\''Gate 0 '\''+chr(0x2014)+'\'' Verifying'\''+q+'\''}'\'';sys.stdout.buffer.write(s.encode('\''cp936'\''))'
{"name": "Gate 0 �� Verifying"}
(exit 0)
```

**P2 D8 - consumer refusal: RUN AS DECLARED, and the companion probe over a real stdin composition with pipefail declared**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready.py --snapshot-command 'C:/Python312/python.exe -c import sys;sys.stdout.buffer.write(chr(123).encode()+chr(125).encode())'

C:/Python312/python.exe: can't open file 'D:\\Github repo\\Gatebraid\\bin\\gatebraid-ready.py': [Errno 2] No such file or directory
(exit 2)
$ PYTHONDONTWRITEBYTECODE=1 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'C:/Python312/python.exe -c "import sys;sys.stdout.buffer.write(chr(123).encode()+chr(125).encode())" | C:/Python312/python.exe -B bin/gatebraid-frontier.py -'

SNAPSHOT REFUSED: the document does not say what it is: `schema` is absent, so it cannot be consumed as if current
verdicts emitted             : 0 (no verdict is emitted for a document this tool could not validate)
(exit 1)
```

**P2 probe - the T1 producer boundary measured on this host, without the program under test**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/probe-producer-boundary.py
probe: the T1 producer boundary, without the program under test
producer            : bin/gatebraid-snapshot.py
interpreter         : C:\Python312\python.exe

--- R1 real producer, input error (the declared D6 producer)
    producer exit status : 2
    D-4 reading          : no document exists; the composer exits 10
    stdout bytes captured: 0
    strict UTF-8 decode  : ok

--- R2 real producer, degraded live read (the D-4 case)
    producer exit status : 3
    D-4 reading          : a document exists; the composer passes it on
    stdout bytes captured: 1825
    first 48 bytes       : b'{\n "generated_at": "2026-01-01T00:00:00Z",\n "gen'
    strict UTF-8 decode  : ok

--- R3 cp936 stub, the bytes that broke the M2 pipeline (the declared D7 producer)
    producer exit status : 0
    D-4 reading          : a document exists; the composer passes it on
    stdout bytes captured: 31
    first 48 bytes       : b'{"name": "Gate 0 \xa1\xaa Verifying"}'
    strict UTF-8 decode  : REFUSED - 'utf-8' codec can't decode byte 0xa1 in position 17: invalid start byte
    the composer exits 11 and never guesses an encoding

boundary steps not as declared: 0

PROBE CLEAN: every declared boundary step ran here and behaved as the plan declares
(exit 0)
```

**P2 D9 - negative criteria against the real tree: the three path limbs hold, the three source limbs report the absent deliverable**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/negative-criteria.py
changed-path source : git
base                : cbd065893b37f20713ae35b8d2673bf26fe4d2ad
changed paths       : 109
   docs/evidence/gatebraid/P2-S5/captures/G0-baseline-main.json
[... shown 20 of 36 lines; full output: docs/evidence/gatebraid/P2-S5/g1\captures/G1-dryrun-D9-negative.json]
frozen root         : docs/evidence/gatebraid/P2-S5

N1 every changed path inside the allowlist         : holds
N2 under bin/, only the ready pair is touched      : holds
N3 no frozen input is written                      : holds
N4 no runtime dependency, no HTTP client           : FIRED
      bin/gatebraid-ready.py: ABSENT (the declared code surface is missing)
      bin/gatebraid-ready-selftest.py: ABSENT (the declared code surface is missing)
N5 no control-plane mutation, no file written      : FIRED
      bin/gatebraid-ready.py:0 [ABSENT] the declared code surface is missing
      bin/gatebraid-ready-selftest.py:0 [ABSENT] the declared code surface is missing
N6 ready's codes sit outside the consumer's space  : FIRED
      consumer declared code space, read from its docstring: 0, 1, 2, 3
      [ready] bin/gatebraid-ready.py: the declared code surface is missing

NEGATIVE CRITERIA FIRED: N4, N5, N6
(exit 1)
```

**P2 D10 - negative criteria falsified: all six fire, each on its substantive limb**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/negative-criteria.py --changed-from docs/evidence/gatebraid/P2-S5/g1/SEED-negative-criteria.txt --code-surface-dir docs/evidence/gatebraid/P2-S5/g1/falsification --frozen-root docs/evidence/gatebraid/P2-S5/g1/falsification/frozen-root
changed-path source : docs/evidence/gatebraid/P2-S5/g1/SEED-negative-criteria.txt
base                : cbd065893b37f20713ae35b8d2673bf26fe4d2ad
changed paths       : 9
   bin/gatebraid-ready.py
   bin/gatebraid-ready-selftest.py
   bin/gatebraid-frontier.py
[... shown 24 of 48 lines; full output: docs/evidence/gatebraid/P2-S5/g1\captures/G1-dryrun-D10-negative-falsify.json]
      retained file count: 1 (expected 43)
      retained-set path-list digest: 78b1033539b2e9fb60128927641f8908f9a67b3ff6183e657fba591bc7df853b (expected 83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f)
      docs/evidence/gatebraid/P2-S5/g1/falsification/frozen-root/gate0.md: 9f3760fc458fe6e87b6187bbe787fb5d01e7aeb42281fd5a5bbe699b178de8df (expected be7c338896b1015923671988166d55af3bd59e028660ce89dfd3b69bc7251513)
      docs/evidence/gatebraid/P2-S5/g1/falsification/frozen-root/g0r/gate0.md: fa5bc3f79e5a59986bd97585d41dc34e27b45c1770c2ee20c593934288dd35fc (expected 95ff39111b4a8b8aa43c022e877c98af5f868b054f4ac2c116ae5c67327bc4e6)
N4 no runtime dependency, no HTTP client           : FIRED
      docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready.py: requests (network client module)
      docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready-selftest.py: urllib.request (network client module)
N5 no control-plane mutation, no file written      : FIRED
      docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready.py:23 [file-local] graphql document opens a mutation
      docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready.py:28 [file-local] open() not provably read-only (mode 'w')
      docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-snapshot.py:13 [transitive] graphql document opens a mutation
N6 ready's codes sit outside the consumer's space  : FIRED
      consumer declared code space, read from its docstring: 0, 1, 2, 3
      [collision] docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready.py: exit 0 is inside the consumer's declared space
      [collision] docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready.py: exit 2 is inside the consumer's declared space
      [missing] docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready.py: the frozen scope's exit 11 is not declared

NEGATIVE CRITERIA FIRED: N1, N2, N3, N4, N5, N6
(exit 1)
```

**P2 D11 - the evidence toolchain on the WSL half: RUN AS DECLARED, then both tools against artefacts that exist**
```
$ wsl.exe -e bash -lc 'cd '\''/mnt/d/Github repo/Gatebraid'\'' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-capture.py --out docs/evidence/gatebraid/P2-S5/g1/dryrun-out/G2-wsl-ready-selftest.json --capture-id G2-wsl-ready-selftest -- python3 -B bin/gatebraid-ready-selftest.py; echo "capture-half exit=$?"; PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S5/gate2.md --report-id cov-P2-S5-gate2-wsl.md; echo "validate-half exit=$?"'
WROTE docs/evidence/gatebraid/P2-S5/g1/dryrun-out/G2-wsl-ready-selftest.json
  bytes=1831 sha256=f2721b0f8c4b6635d9bee6c500ad0b06ee4c295728bf67a1e1357469c8a2d365 crlf=0 lone_cr=0
capture-half exit=0
validate-half exit=1
[... shown 18 of 19 lines; full output: docs/evidence/gatebraid/P2-S5/g1\captures/G1-dryrun-D11-wsl-toolchain.json]
Traceback (most recent call last):
  File "/mnt/d/Github repo/Gatebraid/bin/gatebraid-validate.py", line 898, in <module>
    sys.exit(main())
             ^^^^^^
  File "/mnt/d/Github repo/Gatebraid/bin/gatebraid-validate.py", line 892, in main
    return mode_record(args)
           ^^^^^^^^^^^^^^^^^
  File "/mnt/d/Github repo/Gatebraid/bin/gatebraid-validate.py", line 693, in mode_record
    doc, raw, schema_id, errors, props, findings, loader = validate_document(args.record)
                                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/mnt/d/Github repo/Gatebraid/bin/gatebraid-validate.py", line 651, in validate_document
    with open(path, "rb") as fh:
         ^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'docs/evidence/gatebraid/P2-S5/gate2.md'
(exit 0)
$ wsl.exe -e bash -lc 'cd '\''/mnt/d/Github repo/Gatebraid'\'' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-capture.py --out docs/evidence/gatebraid/P2-S5/g1/dryrun-out/WSL-inner-probe.json --capture-id WSL-inner-probe --notes '\''inner capture written by the WSL half'\'' -- python3 -B bin/gatebraid-frontier.py docs/evidence/gatebraid/P2-S5/g1/captures/g1-snapshot.json --out docs/evidence/gatebraid/P2-S5/g1/dryrun-out/wsl-frontier-report.json'
WROTE docs/evidence/gatebraid/P2-S5/g1/dryrun-out/WSL-inner-probe.json
  bytes=2752 sha256=695845782c101c7fc81cc29c1724796bcd5966b7121449345be7527f651b8e19 crlf=0 lone_cr=0
(exit 0)
$ wsl.exe -e bash -lc 'cd '\''/mnt/d/Github repo/Gatebraid'\'' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S6/gate1.md --report-id cov-P2-S6-gate1-wsl-probe.md'
target        : docs/evidence/gatebraid/P2-S6/gate1.md
interface     : gatebraid/gate-run@2
loader        : CPython 3.12.3 (/usr/bin/python3), jsonschema 4.10.3, Draft202012Validator
structural    : 0 error locus/loci
properties    : 7 rows
   structural       1
   semantic         6
   replayed         0
   capture-trusted  0
findings      : 0
verdict       : accepted
(exit 0)
```

**P2 sweep - the closed-set sweep, domain named explicitly; repository limb CLOSED, explanation limb typed fail**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/checks-g1-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g1/captures
captures swept : 28

=== candidate classification (every rule applied explicitly) ===
  E1 permitted repository                                    50
  E5 filesystem or URL path segment                          122
  E6 schema-id namespace                                     4
  E7 JSON pointer                                            60
  N2 the P2-S5 item                                          4
  N4 another item of the permitted Project                   30
  UNEXPLAINED                                                145

=== every REPOSITORY identity named anywhere ===
  MianliWang/gatebraid           x30   PERMITTED
  MianliWang/gatebraid-scratch   x20   PERMITTED
[... shown 20 of 166 lines; full output: docs/evidence/gatebraid/P2-S5/g1\captures/G1-closed-set-sweep.json]
    G1-entry-fields.json                         stdout       repo
    G1-entry-fields.json                         stdout       repo
    G1-entry-fields.json                         stdout       repo
    G1-probe-D11-wsl-capture.json                invocation   repo
    G1-probe-D11-wsl-validate.json               stdout       repo
    G1-probe-D11-wsl-validate.json               invocation   repo
(exit 1)
```

**P2 sweep falsified - the same instrument over the two retained seeds**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/checks-g1-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g1/falsification
captures swept : 2

=== candidate classification (every rule applied explicitly) ===
  N2 the P2-S5 item                                          1
  N4 another item of the permitted Project                   1
  UNEXPLAINED                                                1

=== every REPOSITORY identity named anywhere ===

=== mention-class check: a mention must never appear in an INVOCATION ===
  mention-class issues targeted by a query: 0 (0 required)

domain      : 2 documents (0 of this sweep's own reports excluded)
UNEXPLAINED RESIDUE: 5
    SEED-out-of-namespace-item.json              stdout       node
    SEED-out-of-namespace-item.json              stdout       node
    SEED-out-of-set.json                         stdout       repo
    SEED-out-of-set.json                         stdout       node
    SEED-out-of-set.json                         stdout       issue
(exit 1)
```

**P2b - no path outside the frozen allowlist appears as a write anywhere in the plan**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/plan-path-scan.py docs/evidence/gatebraid/P2-S5/g1/gate1.md
allowlist prefixes : bin/, docs/evidence/gatebraid/P2-S5/
paths named in plan: 36

WRITE targets, each required to be inside the allowlist:
   bin/                                                                   inside=True
   bin/**                                                                 inside=True
   bin/gatebraid-ready-selftest.py                                        inside=True
   bin/gatebraid-ready.py                                                 inside=True
   docs/evidence/gatebraid/P2-S5/                                         inside=True
   docs/evidence/gatebraid/P2-S5/g0r/                                     inside=True
   docs/evidence/gatebraid/P2-S5/g1/                                      inside=True
   docs/evidence/gatebraid/P2-S5/g1/SEED-negative-criteria.txt            inside=True
   docs/evidence/gatebraid/P2-S5/g1/dryrun-out/no-such-transcript.json    inside=True
   docs/evidence/gatebraid/P2-S5/g1/falsification                         inside=True
   docs/evidence/gatebraid/P2-S5/g1/falsification/frozen-root             inside=True
   docs/evidence/gatebraid/P2-S5/g1/negative-criteria.py                  inside=True
   docs/evidence/gatebraid/P2-S5/g1/scope-pin.py                          inside=True
   docs/evidence/gatebraid/P2-S5/g2/                                      inside=True
   docs/evidence/gatebraid/P2-S5/g2/captures/G2-live-ready.json           inside=True
   docs/evidence/gatebraid/P2-S5/g2/captures/G2-wsl-ready-selftest.json   inside=True
   docs/evidence/gatebraid/P2-S5/g2/gate2.md                              inside=True

READ-ONLY inputs, named on purpose and written by no task in this plan:
   bin/gatebraid-capture.py
   bin/gatebraid-frontier.py
   bin/gatebraid-snapshot.py
   bin/gatebraid-validate.py
   fixtures/run-corpus.py
   fixtures/runner-selftest.py

EXCLUDED LANES the plan names in order to disclaim them:
   adr/
   docs/evidence/gatebraid/P2-S1/
   docs/evidence/gatebraid/P2-S2/
   docs/evidence/gatebraid/P2-S3/
   docs/evidence/gatebraid/P2-S4/
   docs/evidence/gatebraid/P2-S5/g0r/gate0.md
   docs/evidence/gatebraid/P2-S5/gate0.md
   docs/evidence/gatebraid/P2-S6/
   fixtures/
   projects/
   protocols/
   schema/
   templates/

PROSE tokens that are not repository paths:

NEITHER a permitted read-only input nor inside the allowlist: 0

ITEM HOLDS: every write target named in the plan is inside the allowlist
(exit 0)
```

**P3 - exit checklist completed, every item evidence-backed**
```
docs/evidence/gatebraid/P2-S5/g1/gate1-exit-checklist.md
```

**P4 - allowlist_hash reproduced**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/hash-allowlist.py
entries (sorted by byte value):
   'bin/'
   'docs/evidence/gatebraid/P2-S5/'
payload bytes : b'bin/\ndocs/evidence/gatebraid/P2-S5/\n'
payload length: 36
allowlist_hash: 4110b3021bdfc2fcda1f5f90528db01eb87b554177e2176ccfba46ccd6ca3750
(exit 0)
```

**P5 - plan_hash reproduced, from the rendered record itself**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/hash-plan.py docs/evidence/gatebraid/P2-S5/g1/gate1.md
record        : docs/evidence/gatebraid/P2-S5/g1/gate1.md
heading at    : line 3 (1-based)
next '## ' at : line 388 (1-based)
plan lines    : 382 after stripping and trimming
payload length: 28364
plan_hash     : b2cd75f6a49bb056fd16bc3d2f4cfd5cf98ae8515b5761908add2ed5405cc424
(exit 0)
```

**P6 - the sanctioned write_domains post-condition on the Slice issue**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/writedomains-check.py
frozen allowlist  : ['bin/', 'docs/evidence/gatebraid/P2-S5/']
declared on the Slice issue: ['bin/', 'docs/evidence/gatebraid/P2-S5/']
equal as sequences: True
equal as sets     : True

POST-CONDITION ALREADY HOLDS: the declared write_domains equals the frozen
allowlist. The agreement is recorded as this verification row and NO rewrite
of the Slice body is made. The step is performed, not skipped.
(exit 0)
```

## Required disclosures

- Deviations: no read-only Agent Team was used, and the decision is recorded here rather than left implicit. gate-1-contract action 2 makes the team OPTIONAL. Two reasons, and the second is the decisive one. First, the question this gate had to answer - what the frozen scope IS - is answered by reading seven named documents at one named commit and hashing them, which a teammate could not do more reliably than the pin instrument does. Second, action 2 requires all findings to be FLUSHED TO THE SLICE ISSUE before the team dissolves, and that flush is a control-plane mutation this window has no approval for: the operator's release of this gate sanctions the handoff comment, the write_domains post-condition and the four field writes, and nothing else. Spawning a team would have forced either an unapproved mutation or a violated constraint. Consequently there are NO team findings to flush, and failure-disposition row 2 is vacuously satisfied rather than exercised.
- Deviations: action 4's dry-run of a not-yet-written deliverable is recorded honestly and in three classes, not two. SIX declared commands ran to their full green criterion today: D0, D0F, D1, D2, D10 and the D9 path limbs. FIVE - D3, D4, D5, D6, D7, D8 and D11 - name `bin/gatebraid-ready.py` or `bin/gatebraid-ready-selftest.py`, which Gate 1 is forbidden to create, and each was RUN AS DECLARED on the declared platform and produced an interpreter error naming exactly the absent file and nothing else wrong. That establishes what action 4 exists to establish - the command reaches the interpreter on THAT host, rather than being well-formed on inspection - and no more. The third class is the one that makes the difference: for every such command a COMPANION PROBE ran the same boundary against the real tools, so the parts other than the program under test are measured and not assumed.
- Deviations: the dry-run CHANGED THE PLAN, twice, before the freeze, which is the whole purpose of the requirement. D6 was declared as `--project 999` on the reasoning that a bad project number is a producer failure. Run against the real producer it returns EXIT 3 WITH A DEGRADED DOCUMENT, not a no-document failure - the O0-hardened producer fails closed and reports degradation rather than crashing. That is delta D-4, it was not foreseen, and it changes the composer's central rule from `the producer exited non-zero` to `the producer's status says whether a document exists`. D6 now names an input error that genuinely produces none. Separately, D11's expected-green criterion was written as `platform.os reads linux`; the capture tool running on WSL stamps `wsl`, so the criterion as first written would have failed a correct run. Both corrections are in the frozen plan, and both were found by running rather than by reading.
- Deviations: a landed tool defect was found by running a declared command as written, and this Slice does not repair it. `bin/gatebraid-validate.py --record <absent path>` raises an uncaught FileNotFoundError from validate_document rather than reporting a typed usage error, so a caller reading the exit status sees 1 - the same status a REJECTED record produces - with a traceback instead of a finding. It is recorded here as a queued defect: the validator is one of the five landed pairs this Slice's Non-goals put out of scope, and repairing it here would be the widening that ADR-0032's lane structure exists to prevent. One Slice, one tool.
- Deviations: the closed-set sweep over this gate's captures reports UNEXPLAINED RESIDUE and the instrument was NOT edited to clear its own finding. The hard rule the sweep enforces is SATISFIED and shown: exactly two repository identities are named anywhere in the domain, `MianliWang/gatebraid` and `MianliWang/gatebraid-scratch`, both PERMITTED, nothing outside the set, and no mention-class issue is targeted by any query. What is unresolved is the sweep's ability to EXPLAIN every candidate token by rule, and every residue token was identified with its source before anything was done. Exactly one was this window's own prose - a slash joining two field names in a capture note - and it was removed AT SOURCE by rewording, with the superseded read retained beside it. Every other residue is text this gate cannot alter and must not: JSON Schema pointer segments printed by the corpus runner and the validator whose leading segment is not `properties`; two ratios, a relative path and a slashed word pair inside the `Last Checkpoint` value the CLOSED Gate 0 exit wrote; an issue-shaped friction citation inside a frozen corpus case label; a Windows path split at its space; and a newline rendered by a Python bytes repr immediately before a path. Four of those classes are already named with stated reasons in the MERGED P2-S6 Gate 1 copy; the rest are new and no committed copy names them. Adding them is a domain fact this window will not make on its own authority, exactly as the Gate 0 re-run stopped rather than extend this same instrument, and the ruling is requested in the exit report. The sweep is typed `fail` here and is not one of the contract's Actions 1 through 6.
- Deviations: the sweep was falsified before any weight was put on it. The SAME instrument, pointed at the two retained seeds, fired on the repository, node and issue limbs at exit 1, and left BOTH out-of-namespace item ids as residue including the near-miss that differs from the permitted namespace by a single character. A sweep that has only ever returned empty has measured nothing.
- Deviations: the contract's Entry condition `Gate = G0 passed` CANNOT be established from the O0 outputs alone, and that gap is recorded rather than papered over. The snapshot document carries `workflow` for every item and no `Gate` field at all, so the Slice's acceptance clause `control-plane state read exclusively through O0 outputs` does not reach the field this gate's Entry turns on. Every dependency, verdict and workflow reading in this record comes from the snapshot and the frontier; the `Gate`, `Next Approval` and `Last Checkpoint` readings come from the same by-key node read the Gate 0 Exit used for its own read-backs, captured, and resolved by option id rather than by typing a label through this host's console. The gap is a finding about the acceptance clause, not a licence to query freely.
- Deviations: the frozen corpus holds SEVEN of the eight catalogued historical ready-failure classes, not eight, and the Slice's Acceptance is read against what the corpus actually contains. BP-01, BP-02, BP-03, IN-02, IN-03, IN-04 and IN-05 are each shown killed at D2 by the runner's own summary rows naming the locus. IN-01, the pipeline exit code, is DELIBERATELY ABSENT from the corpus by that corpus's own declared known_limitation, so it cannot be shown killed from the corpus and this record does not claim it is. It is carried instead as a declared selftest condition of the deliverable, and its shape was exercised at this gate by the D8 companion probe, which ran the composition under a shell with pipefail declared and the exit-code source named.
- Deviations: the D5 row's declared command writes into the Gate 2 captures directory, and creating a Gate 2 directory at Gate 1 would assert a gate that has not opened. The dry-run substituted the output directory only; interpreter, flags, repository-relative path form and allowlist prefix are identical, and both paths lie under `docs/evidence/gatebraid/P2-S5/`, which N1 covers. Its `--input` list was also reduced to the tools that exist, because the capture tool hashes declared inputs BEFORE running and would otherwise refuse on the absent deliverable - which is the outcome the row reports anyway.
- Deviations: one Gate 1 instrument writes nothing and is not the deliverable, and is named so it is not mistaken for one. `docs/evidence/gatebraid/P2-S5/g1/probe-producer-boundary.py` has no command line, composes nothing with the consumer and implements no exit algebra; it crosses the T1 boundary three times against real producers and reports what each crossing produced. It exists because action 4 asks whether the declared commands run HERE, and Slice A's frozen plan is the case where that question was answered by reading and the answer was wrong.
- Deviations: three Gate 1 instruments were copied from earlier evidence and re-parameterised to this Slice's constants only. `hash-plan.py` is BYTE-IDENTICAL to the P2-S4 and P2-S6 file, sha256 17649cdb5535f4cc09e114ca135e23750aabfa35b69de1d8cd0263d690ed0ada, because it takes its target as an argument and needed no change. `plan-path-scan.py` and `writedomains-check.py` differ only in this Slice's allowlist, its read-only input set, its excluded lanes and the issue read. `checks-g1-closed-set-sweep.py` is a copy of the Gate 0 re-run instrument, sha256 d2b501555a223e5d69720fed3cf8640e56233d2f4d81549a87ca02788ad3bff1, differing in three DOMAIN FACTS - the captures directory, the self-exclusion prefix, and four mention-class issue numbers the historical record necessarily names - and in no rule, regex or residue criterion. A closed gate's instruments are not editable by a later gate, and the Gate 0 copies were not touched.
- Deviations: this record was FIRST WRITTEN TO THE WRONG PATH and the correction is recorded rather than quietly folded in, because the mistake is exactly the one negative criterion N3's content limb exists to catch. The contract's Exit names `docs/evidence/gatebraid/<slice_id>/gate1.md`, and the first two render passes took it literally and wrote `docs/evidence/gatebraid/P2-S5/gate1.md` - beside the retained gate0.md, at the top level. Ruling 2 of the Gate 0 opening comment gives this Slice a per-gate layout instead, and the operator's release of this gate names `docs/evidence/gatebraid/P2-S5/g1/gate1.md` explicitly. The consequence was measured, not reasoned about: with the misplaced file present the retained-set path-list digest read 1177e325f02fd660b9de2edfdbecff1fe30627c4e37d2789592fc58522ddf571 instead of 83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f. NO RETAINED FILE WAS EVER MODIFIED - the perturbation was an ADDED path in the file list, and both gate0.md hashes were unchanged throughout. Removing the file restored the digest to the frozen value exactly, re-measured before the Exit and again after it. The renderer, the record path, the validator target, the plan-path scan target, the `hash_commands` and `evidence_files` entries were all corrected together, and the superseded captures are retained as `-pass1` files rather than deleted.
- Deviations: this record's own machine validation and the sweep over it necessarily run against the byte state produced by the final render, and their captures are cited by output_ref rather than inlined as record rows - a document that quoted its own verification would change the bytes that verification read. The plan section, which is what plan_hash covers and what a Plan Approval binds, is byte-identical across every render pass; only the Records rows and the metadata block moved. plan_hash was recomputed from the FINAL file after the last render and equals the embedded value.
- Deviations: this gate wrote no tracked file, made no commit, made no push, created no branch, ran no fetch and no pull, and took no Writer Lease. Every byte it wrote lies under `docs/evidence/gatebraid/P2-S5/g1/`. The forty-three retained files of the accepted Gate 0 stop and every file under `docs/evidence/gatebraid/P2-S5/g0r/` are untouched, which negative criterion N3's content limb measures rather than asserts. Base SHA is not touched at this gate; ADR-0011 section 9 sets it at Gate 2 from the head re-read under lease, and the Project field still carries the O0 merge commit while this record's base_sha is the current head of main, the tree the plan is made against.
- Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; Git for Windows 2.51.0.windows.1 whose SYSTEM configuration carries core.autocrlf=true, verified in this window; every gh call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL /usr/bin/python3 with CPython 3.12.3, jsonschema 4.10.3, whose captures stamp platform.os `wsl`. The `python` on PATH is the MSYS 3.14.3 build and carries neither, which is why no declared command names it and why delta D-3 exists. Every captured command was marshalled as an argv list rather than a shell string except the one row that declares shell semantics explicitly, so no quoting layer could alter it. environment=mixed-see-prose: the tools run on the Windows host and the WSL half is evidence, and the selftest and both halves of the evidence toolchain are declared and dry-run on both.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S5
gate: 1
environment: mixed-see-prose
executor: Claude Lead
base_sha: cbd065893b37f20713ae35b8d2673bf26fe4d2ad
started_at: "2026-09-01T21:39:25Z"
ended_at: "2026-09-01T22:12:51Z"
result: needs_approval
checks:
  - name: gate1-entry-g0-passed
    command: "by-key node read of the Gate and Workflow single-select values with their option ids"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-entry-fields.json"
  - name: control-plane-read-through-o0-outputs
    command: "bin/gatebraid-snapshot.py then bin/gatebraid-frontier.py; four sources ok and complete, sixteen items, snapshot_degraded false"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-entry-frontier.json"
  - name: frozen-scope-pinned-by-hash
    command: "docs/evidence/gatebraid/P2-S5/g1/scope-pin.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D0-scope-pin.json"
  - name: frozen-scope-pin-falsified
    command: "the same instrument with --commit naming the pinned commit's parent; must report SCOPE PIN STALE"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D0F-scope-pin-falsify.json"
  - name: plan-complete
    command: "approach, write_domains, three tasks, test plan, risk notes, rollback note, six negative criteria"
    result: pass
    output_ref: "#plan-frozen-at-exit"
  - name: allowlist-exact
    command: "docs/evidence/gatebraid/P2-S5/g1/hash-allowlist.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-allowlist-hash.json"
  - name: plan-paths-inside-allowlist
    command: "docs/evidence/gatebraid/P2-S5/g1/plan-path-scan.py docs/evidence/gatebraid/P2-S5/g1/gate1.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-plan-path-scan.json"
  - name: corpus-digest-unmoved
    command: "fixtures/runner-selftest.py; digest after equals the O1-B1 freeze value"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D1-corpus-digest.json"
  - name: historical-ready-failure-classes-killed
    command: "fixtures/run-corpus.py; BP-01, BP-02, BP-03, IN-02, IN-03, IN-04 and IN-05 each killed on a named locus. IN-01 is absent from the corpus by its own known_limitation and is not claimed"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D2-corpus.json"
  - name: test-plan-dry-run
    command: "D0, D0F, D1, D2, D9, D10 to full green; D3, D4, D5, D6, D7, D8, D11 run as declared on the declared platform, each naming the absent deliverable and nothing else"
    result: pass
    output_ref: "#records"
  - name: producer-boundary-runnable-here
    command: "docs/evidence/gatebraid/P2-S5/g1/probe-producer-boundary.py; three boundary crossings against real producers"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-probe-boundary.json"
  - name: evidence-toolchain-runs-on-wsl
    command: "bin/gatebraid-capture.py and bin/gatebraid-validate.py, each run on the WSL half; the capture stamps platform.os wsl, the validator returns accepted"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-probe-D11-wsl-validate.json"
  - name: negative-criteria-falsified
    command: "negative-criteria.py against the seeded changed-path list, code surface and frozen root; all six must fire on their substantive limbs"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D10-negative-falsify.json"
  - name: negative-criteria-path-limbs-hold
    command: "negative-criteria.py against the real tree; N1, N2 and N3 including the retained-record content limb"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D9-negative.json"
  - name: negative-criteria-source-limbs-absent
    command: "the same run; N4, N5 and N6 report bin/gatebraid-ready.py absent, which is what a read-only gate must report about a file it may not create"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D9-negative.json"
  - name: closed-set-sweep-falsified
    command: "the same instrument over the two retained seeds; must fire on the repository, node and issue limbs"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-closed-set-sweep-falsify.json"
  - name: closed-set-repository-limb-closed
    command: "checks-g1-closed-set-sweep.py over the captures domain; exactly two repository identities named, both permitted, no mention-class issue targeted by a query"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-closed-set-sweep.json"
  - name: closed-set-sweep-explains-every-candidate
    command: "the same run; residue remains and the instrument was NOT edited to clear its own finding. Every token identified with its source; a ruling is requested"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-closed-set-sweep.json"
  - name: gate1-exit-checklist
    command: "templates/gatebraid-gate1-exit-checklist.md, every item evidence-backed"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/gate1-exit-checklist.md"
  - name: gate1-record-machine-validated
    command: "bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S5/g1/gate1.md --report-id cov-P2-S5-g1-gate1.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-record-validation.json"
  - name: write-domains-agreement
    command: "docs/evidence/gatebraid/P2-S5/g1/writedomains-check.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g1/captures/G1-writedomains-check.json"
plan_hash: "b2cd75f6a49bb056fd16bc3d2f4cfd5cf98ae8515b5761908add2ed5405cc424"
allowlist_hash: "4110b3021bdfc2fcda1f5f90528db01eb87b554177e2176ccfba46ccd6ca3750"
hash_commands:
  allowlist: "PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/hash-allowlist.py"
  plan: "PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/hash-plan.py docs/evidence/gatebraid/P2-S5/g1/gate1.md"
evidence_files:
  - docs/evidence/gatebraid/P2-S5/g1/gate1.md
notes: "Planning for the fourth gatebraid-ready attempt on the M2 slice-C frozen scope. The scope was READ, not remembered: seven documents at one named commit of the historical working repository, each pinned by the sha256 of the bytes received, re-derivable by the instrument that produced the pin and falsified against the pinned commit's parent. All three historical attempts declare one identical scope; four deltas separate it from the tools it must now compose, and the fourth was found by running the dry-run rather than by reading it. The Gate 0 re-run opening comment 5472973466 and its rulings belong to the Gate 0 record and are not re-entered here; this gate opened no approval and carries no approvals[] entry. Two checks are typed fail and both are disclosed in full: the source limbs of the negative criteria, which report a deliverable a read-only gate may not create, and the closed-set sweep's explanation limb, whose residue was identified token by token and whose instrument was NOT edited to clear its own finding. The sweep's hard-rule limb - the repository identity set - is closed. A recorded human approval comment is the only door to Gate 2."
```
