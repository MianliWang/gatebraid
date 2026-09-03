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
