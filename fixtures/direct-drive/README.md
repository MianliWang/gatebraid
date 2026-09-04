# fixtures/direct-drive — seeds for the dispatcher (`gatebraid/dispatch-fixture@1`)

These fixtures precede `bin/gatebraid-dispatch.py` (M3-PLAN §2:
fixtures-first) and are the contract's §4 decision table made executable.
Each file is one seed: a manifest, the inbox files it names (inline bodies),
the STOP and RUNNING states, and the expected decision. The dispatcher's
print-only mode `--fixture <path>` materialises the seed in a temporary
inbox, evaluates it, and prints one line: `<id> expected <decision>/<code>
got <decision>/<code> -> MATCH | MISMATCH`, exit 0 only when every seed
matches. Stage 0 of the trial (ADR-0034 decision 9) is that exit 0, with each
seed's run record retained.

| id | class | expected |
|---|---|---|
| DD-P1 | valid read-only dispatch | allow |
| DD-01 | sha256 mismatch | refuse DD-R02 |
| DD-02 | inbox file not in the manifest | refuse DD-R02 |
| DD-03 | repository identity outside the closed set in the text | refuse DD-R05 |
| DD-04 | STOP present | halt DD-R00 |
| DD-05 | write kind under the readonly profile | refuse DD-R03 |
| DD-06 | RUNNING present | refuse DD-R06 |
| DD-07 | handoff-block schema token in the text | refuse DD-R05 |
| DD-08 | manifest repository outside the closed set | refuse DD-R04 |
| DD-09 | CR byte and out-of-set code point in the text | refuse DD-R05 |
| DD-10 | manifest schema key wrong | refuse DD-R01 |
| DD-11 | closing keyword immediately before an issue reference | refuse DD-R05 |
| DD-12 | kind outside the enumeration | refuse DD-R03 |

Two seeds (DD-07, DD-11) test patterns that must never appear in a committed
file, so they carry the pattern in parts (`token_parts`, or the substitution
rule in `note`) and the runner assembles it at evaluation time, recomputing the
entry's `sha256` and `bytes` afterwards. The committed bytes of every file in
this directory are LF-only ASCII, and the closed-set seeds name a
non-existent repository rather than any real one outside the set.

Missing on purpose, owed to R-min: seeds for the `write` profile's deny list
(push from a `gate2` job; a path outside the frozen allowlist). They are
written when R-min defines that profile, before stage 3 runs.
