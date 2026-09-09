# fixtures/direct-drive — seeds for the dispatcher (`gatebraid/dispatch-fixture@1`)

These fixtures precede `bin/gatebraid-dispatch.py` (M3-PLAN §2:
fixtures-first) and are the contract's §4 decision table made executable.
Each file is one seed: a manifest, the inbox files it names (inline bodies),
the STOP and RUNNING states, optionally a host stub (`host.profile_present`)
or declared before/after run states (`post_run`), and the expected decision.
Fixture mode (`--fixture <path>`, contract §10) materialises the seed in a
temporary inbox and profile directory, evaluates the contract's §4 against it
without running anything — and, for a seed with `post_run`, the §2.2 post-run
rule over the declared states — and prints one line: `<id> expected
<decision>/<code> got <decision>/<code> -> MATCH | MISMATCH`, exit 0 only
when every seed matches. Stage 0 of the trial (ADR-0034 decision 9) runs
nothing: its evidence is that exit 0, captured once (fixture mode writes no
run record outside its temporary directory; the capture is the record), plus
print-only mode over the trusted seed DD-P1's inbox on the real host, once
with `STOP` present and once without (contract §6 and §8).

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
| DD-13 | evidence kind (`gate0`) whose only change is under its own evidence directory | completed (post-run rule, declared states) |
| DD-14 | evidence kind (`gate0`) that also changed a path outside its evidence directory | error DD-R08 (declared states) |
| DD-15 | read-only kind (`review`) after which HEAD moved | error DD-R08 (declared states) |
| DD-16 | host stub without the profile file | refuse DD-R07 |
| DD-17 | read-only kind carrying a `slice_id` it must not have | refuse DD-R03 |
| DD-18 | one inbox file named by two manifest entries | refuse DD-R02 (manifest) |
| DD-19 | manifest `written_at` is not a string; the refusal must still be recorded | refuse DD-R01 (manifest; record written) |
| DD-20 | every residue class a real dispatch needs (paths with spaces, branches, refs, a ratio, a schema id) | allow — the pass-direction falsifier of `DD-R05`'s whitelist |
| DD-21 | entry value of the wrong type (`kind` is a number) | refuse DD-R01 (manifest) |
| DD-22 | manifest is a JSON array, not an object; the refusal must still be recorded | refuse DD-R01 (manifest; record written) |
| DD-23 | manifest `written_at` is a string of the wrong shape (slashes); the refusal must still be recorded, in the outbox | refuse DD-R01 (manifest; record written) |
| DD-24 | dispatch text carrying two ordinary prose pairs (`I/O`, `before/after`) | allow — the pass-direction falsifier of the exact-string prose-pair allowlist |
| DD-25 | entry name that is one segment plus a trailing newline | refuse DD-R01 (manifest) |
| DD-26 | read-only kind (`review`) whose heads were not measured on either side (both null, declared states) | error DD-R08 — the unmeasured-state clause on the fixture `post_run` path |
| DD-27 | evidence kind (`gate0`) whose porcelain list after the run was not measured (null, declared states) | error DD-R08 — the same clause, the list limb |

One seed (DD-24) carries two prose pairs joined by a slash in its committed
bytes; they are the class the tool's exact-string allowlist admits (contract
§4, `DD-R05`) and the frozen P2-S5 sweep instrument, which is evidence and is
not edited, reports them as residue of that class. Two seeds (DD-07, DD-11)
test patterns that must never appear in a committed
file, so they carry the pattern in parts under `setup.substitutions` (a
placeholder mapped to a list of parts); fixture mode joins the parts,
replaces the placeholder in every inline body, and recomputes the entry's
`sha256` and `bytes` before `DD-R02` (contract §10). The committed bytes of every seed
file (`DD-*.json`) are LF-only ASCII; this README carries a few code points
from the contract's permitted set. The closed-set seeds name a non-existent
repository rather than any real one outside the set.

Every one of the contract's nine codes has a seed. Two cannot be staged as
inbox state and are seeded differently (contract §10): `DD-R07` (the profile
file or a host tool absent) by DD-16, whose host stub omits the profile file;
`DD-R08` (a job that changed what its class forbids) by DD-13, DD-14 and
DD-15, which declare the heads and porcelain lists before and after a run so
the post-run rule is evaluated without running anything — DD-13 is the
positive case an evidence kind must pass, a Gate 0 that wrote only its own
evidence file — and by DD-26 and DD-27, which declare a null head or a null
list: state the dispatcher could not measure is `error`/`DD-R08` for every
kind (contract §2.2, §4), and the two seeds hold that clause on the fixture
`post_run` path, where the function that owns the rule is the one that must
refuse (the stage-0 review's S-2). DD-02 is the manifest-level half of `DD-R02` — an inbox file
no entry names — which §4 evaluates once per manifest before any entry.

Missing on purpose, owed to R-min: seeds for the `write` profile's deny list
(push from a `gate2` job; a path outside the frozen allowlist). They are
written when R-min defines that profile, before stage 3 runs.
