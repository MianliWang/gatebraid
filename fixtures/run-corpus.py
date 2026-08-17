#!/usr/bin/env python3
"""Run the Gatebraid fixture corpora and assert every recorded expectation.

This is the corpus RUNNER, not an evidence instrument: it neither generates nor
validates gate evidence, and it is neither N2 nor N3. Its only job is to make the
corpus's expected-failure assertions executable, so that "fixtures exist" and
"fixtures assert what they claim" are the same statement (M3-PLAN.md §2 N1).

Contract
--------
Reads fixtures/CORPORA.json, then each corpus's EXPECTATIONS.json, validates each
fixture against its declared schema, and requires the recorded outcome exactly:

  expect: valid    -> zero validation errors
  expect: invalid  -> the observed loci EQUAL the recorded set

Equality, not containment, in both directions:
  * a recorded locus that does not fire  -> rejected for the wrong reason
  * a locus that fires but was not recorded -> the fixture is over-mutated, and a
    corpus that absorbed it would be measuring rejections rather than kills

Structure is asserted too: every declared corpus exists and carries a manifest,
every discovered corpus is declared, and every fixture file in a corpus
directory is referenced by a case. Discovery alone cannot detect what was never
added.

A LOCUS IS (keyword, path, schema_path, property, extra_count)
--------------------------------------------------------------
Amended at N1C (A3) and again at N1D (D6, R1).

N1C added `property`: three fixtures removing three different top-level keys all
recorded `required@(root)`, so a validator rejecting one for another's reason
still passed.

N1D adds `schema_path` — the error's `absolute_schema_path` — because an
instance path cannot say WHICH branch of a conditional fired. Two fixtures
exercising the two arms of one `if/then` produced identical loci; the schema path
separates them, and it was available on every error object all along. Three of
the four collision pairs disclosed at N1C are separated by it. The fourth,
EC1-28/EC1-29, is two values failing the SAME constraint and no locus can
separate them — echoing the values would (spec §4 bars it), so it stays
documented.

N1D also adds `extra_count` for `additionalProperties` (R1, external review):
one unexpected property and two unexpected properties produced the same locus
AND the same schema path, so an over-mutated fixture passed a manifest recording
one. The count is a multiplicity, never the offending names or values — a
checker does not quote what it forbids into a record (ADR-0028 §3).

Per keyword the manifest MUST record, and must not record otherwise:
  every locus  -> keyword, path, schema_path
  required     -> property
  additionalProperties -> extra_count
Each is a structure error in both directions. A key the runner ignores would
read as coverage it does not enforce, which is the failure these amendments
remove rather than relocate.

Findings are reported by keyword, path and property, never by echoing the
offending value into the output (spec §4: a checker never quotes what it forbids
into a record).

AMENDED AT M3 BATCH N1E — two repairs to the frozen surface
-----------------------------------------------------------
**1. An ENVIRONMENT failure is exit 3, and can no longer read as exit 1.**
Measured on WSL (jsonschema 4.10.3): every committed schema carries a RELATIVE
`$id` (`gatebraid/evidence-capture@1`), and that release's `RefResolver` joins it
against itself and tries to fetch `gatebraid/gatebraid/evidence-capture@1`,
raising `RefResolutionError`. Nothing caught it, so it escaped `main()`, and
**Python's own exit status for an uncaught exception is 1** — which this file
defines as "an EXPECTATION failed". A runner whose exit codes exist precisely to
keep "the corpus is broken" apart from "the corpus caught something" was
reporting a missing library feature as a mutation surviving. That is the defect,
and it is in this file rather than in WSL.

Two changes close it, and they are independent on purpose:
  * `ENVIRONMENT = 3` — a distinct code and message for "this interpreter could
    not evaluate the corpus at all". Every path out of `main()` is now covered,
    including the previously uncaught one; a `StructureError` still exits 2 and
    is re-raised ahead of the environment handler so the two never merge. The
    `jsonschema` import failure moves from 2 to 3 as well: a library that is not
    installed is an environment fact, not a malformed corpus, and it was the one
    place this file already conflated the two.
  * A BASE URI IS SUPPLIED AT LOAD (`load_schema`). A relative `$id` is rewritten
    IN THE IN-MEMORY COPY ONLY to an absolute URI under an RFC 2606 reserved
    `.invalid` authority, which is guaranteed never to resolve. The committed
    schema bytes are untouched — `schema/` is inside the selftest's digest scope
    and would fail loudly otherwise. Every `$ref` in the ten committed schemas is
    a pure `#/$defs/...` fragment resolved inside its own document, so no
    resolution leaves the document and no network access is possible or
    attempted. Measured: identical loci on jsonschema 4.10.3 and 4.23.0.

**2. `__pycache__` cannot move the measurement.** Importing either instrument as
a module writes `fixtures/__pycache__/`, and `fixtures/` is exactly where this
runner discovers corpora — so the directory listing gained an undeclared name and
the runner exited 2 on a corpus nobody had changed. A read-only measurement was
broken by the act of measuring it (friction #114 is the same event one round
earlier). `sys.dont_write_bytecode` below is defence in depth and is NOT the fix:
measured, the flag set in a module's own body cannot suppress that module's own
cache, because the cache is written when the loader compiles the module, before
its body runs. The fix is the name exclusion in the discovery walk.

Exit status decides, not the printed text (spec §4).
  0 = every expectation held
  1 = an EXPECTATION failed (a mutation not killed, a valid case broken, wrong,
      missing or extra loci)
  2 = a CORPUS-STRUCTURE or usage error (missing/malformed manifest, fixture or
      schema; undeclared or unreferenced file; a malformed expectation). Distinct
      from 1 on purpose: "the corpus is broken" and "the corpus caught something"
      are different findings and one non-zero code would conflate them.
  3 = an ENVIRONMENT failure: this interpreter could not evaluate the corpus.
      The validator library is missing, or it raised while resolving or applying
      a schema. Distinct from 2 for the same reason 2 is distinct from 1 — "the
      corpus is broken" and "this host cannot read it" are different findings.
"""

from __future__ import annotations

import sys

# Defence in depth, and deliberately the FIRST statement after the import that
# makes it reachable. It stops caches for anything this module goes on to import.
# It does NOT stop this module's own cache when this file is itself imported —
# that is measured, not assumed (N1E), and it is why `_PYCACHE` below exists.
sys.dont_write_bytecode = True

import json
import pathlib
import re
import urllib.parse

EXPECT_FAIL = 1
STRUCTURE = 2
ENVIRONMENT = 3

# The one directory name the interpreter creates by itself inside a tree it is
# only supposed to be reading. Excluded BY NAME rather than by a pattern, so a
# corpus legitimately called e.g. `cache` is unaffected.
_PYCACHE = "__pycache__"

# Any absolute base works; this one cannot resolve by construction. `.invalid` is
# reserved by RFC 2606 and guaranteed never to be delegated, so even a resolver
# that tried to dereference it could not reach a network. Chosen over dropping
# `$id` entirely because supplying a base preserves what `$id` is FOR, and over a
# real hostname because a schema base that could resolve is a schema base that
# might one day be fetched.
_SCHEMA_BASE = "https://schemas.invalid/"

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("ENVIRONMENT: jsonschema is not importable by this interpreter.")
    print("             On this host use C:/Python312/python.exe (jsonschema 4.23.0).")
    sys.exit(ENVIRONMENT)

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"

# jsonschema's required-error message names the one property this error is about.
# The instance-vs-required set difference cannot be used: it yields every missing
# property on every one of the per-property errors.
# Either quote style: repr() switches to double quotes when the property name
# itself contains a single quote, and a missed match must be a STRUCTURE error
# (the loader's wording changed) rather than an expectation failure.
_REQUIRED_MSG = re.compile(
    r"^(?P<q>['\"])(?P<prop>.+?)(?P=q) is a required property$"
)


class StructureError(Exception):
    pass


class EnvironmentFailure(Exception):
    """This interpreter could not evaluate the corpus. Never an expectation
    failure, never a corpus defect — exit 3, and it is kept a separate class from
    StructureError so the two cannot collapse into one code by accident."""


def _reject_nonfinite(token: str):
    """R2 (external review): Python's json accepts NaN/Infinity/-Infinity, which
    RFC 8259 does not. A fixture carrying one is not JSON, and a measured metrics
    value of NaN would otherwise validate as a number. Structure error, exit 2."""
    raise StructureError(
        f"non-JSON numeric constant {token!r}; RFC 8259 admits no such literal"
    )


def load_json(path: pathlib.Path, what: str):
    try:
        return json.loads(path.read_bytes().decode("utf-8"),
                          parse_constant=_reject_nonfinite)
    except FileNotFoundError:
        raise StructureError(f"{what} missing: {path.relative_to(ROOT)}")
    except UnicodeDecodeError as e:
        raise StructureError(f"{what} is not UTF-8: {path.relative_to(ROOT)} ({e})")
    except json.JSONDecodeError as e:
        raise StructureError(f"{what} is not valid JSON: {path.relative_to(ROOT)} ({e})")


def load_schema(path: pathlib.Path, what: str):
    """Load a schema and SUPPLY ITS BASE URI (N1E).

    Every committed schema's `$id` is a relative reference, which jsonschema
    4.10.3 resolves by joining it against itself and then attempting to fetch the
    result. The rewrite happens on a COPY held in memory; the committed bytes are
    never touched, and `schema/` sits inside the selftest's digest scope so any
    attempt to touch them would fail loudly rather than quietly."""
    schema = load_json(path, what)
    if isinstance(schema, dict):
        sid = schema.get("$id")
        # A relative reference is exactly one with no scheme (RFC 3986 §4.2).
        if isinstance(sid, str) and not urllib.parse.urlsplit(sid).scheme:
            schema = dict(schema)
            schema["$id"] = _SCHEMA_BASE + sid.lstrip("/")
    return schema


def locus(err):
    path = "/".join(str(p) for p in err.absolute_path) or "(root)"
    schema_path = "/".join(str(p) for p in err.absolute_schema_path)
    prop = None
    extra = None
    if err.validator == "additionalProperties":
        # R1: multiplicity only. Never the names — the offending keys are exactly
        # what a checker must not quote into a record (ADR-0028 §3).
        # This reproduces jsonschema's find_additional_properties WITHOUT its
        # patternProperties term. Valid only while no schema in scope uses
        # patternProperties — verified true of all ten committed schemas at N1D,
        # and re-verified across all eleven at N1E. A schema adding one would make
        # this over-count, and the count is asserted in both directions, so it
        # would fail loudly rather than silently.
        declared = set(err.schema.get("properties", {}))
        extra = len(set(err.instance) - declared)
    if err.validator == "required":
        m = _REQUIRED_MSG.match(err.message)
        if m is None:
            # The loader's message wording changed. That is the corpus being
            # unreadable, not an expectation failing, so it must exit 2 — an
            # earlier form returned a marker and reached exit 1, conflating the
            # two classes at the one point this code exists to keep apart.
            raise StructureError(
                "cannot determine which property a 'required' error names; the "
                "validator's message wording is not the one this runner parses"
            )
        prop = m.group("prop")
    return (err.validator, path, schema_path, prop, extra)


def loci(errors):
    return {locus(e) for e in errors}


def observe(schema, doc, cid: str):
    """Validate, converting any failure of the validation MACHINERY into an
    environment failure (N1E).

    StructureError is re-raised first and deliberately: `locus()` raises it when
    the loader's message wording has moved, and that is a corpus-readability
    finding at exit 2, not an environment one. Everything else reaching here —
    ref resolution, an unsupported draft, a library defect — is this host being
    unable to evaluate the corpus."""
    try:
        return loci(Draft202012Validator(schema).iter_errors(doc))
    except StructureError:
        raise
    except Exception as e:
        raise EnvironmentFailure(
            f"{cid}: the validator could not evaluate this case: "
            f"{type(e).__name__}: {e}"
        )


def fmt(items) -> str:
    out = []
    for k, p, sp, prop, extra in sorted(items, key=lambda t: tuple(str(x) for x in t)):
        s = f"{k}@{p}"
        if prop is not None:
            s += f":{prop}"
        if extra is not None:
            s += f"x{extra}"
        out.append(f"{s} [{sp}]")
    return ", ".join(out)


def expected_locus(case_id: str, e: dict):
    for key in ("keyword", "path", "schema_path"):
        if key not in e:
            raise StructureError(f"{case_id}: expectation missing {key!r}")
    kw = e["keyword"]
    has_prop = "property" in e
    has_extra = "extra_count" in e
    if kw == "required" and not has_prop:
        raise StructureError(
            f"{case_id}: a 'required' expectation must record which property is "
            f"missing (path {e['path']!r})"
        )
    if kw != "required" and has_prop:
        raise StructureError(
            f"{case_id}: 'property' is only meaningful on a 'required' "
            f"expectation, not on {kw!r}"
        )
    if kw == "additionalProperties" and not has_extra:
        raise StructureError(
            f"{case_id}: an 'additionalProperties' expectation must record "
            f"extra_count (path {e['path']!r})"
        )
    if kw != "additionalProperties" and has_extra:
        raise StructureError(
            f"{case_id}: 'extra_count' is only meaningful on an "
            f"'additionalProperties' expectation, not on {kw!r}"
        )
    return (kw, e["path"], e["schema_path"], e.get("property"), e.get("extra_count"))


def run_corpus(corpus_dir: pathlib.Path) -> tuple[int, int]:
    exp_path = corpus_dir / "EXPECTATIONS.json"
    manifest = load_json(exp_path, "manifest")
    name = manifest.get("corpus", corpus_dir.name)
    version = manifest.get("corpus_version", "?")
    print(f"corpus {name} ({version})  <- {exp_path.relative_to(ROOT)}")
    print(f"  loader recorded: {manifest.get('loader', '(none recorded)')}")

    cases = manifest.get("cases")
    if not isinstance(cases, list) or not cases:
        raise StructureError(f"manifest has no cases: {exp_path.relative_to(ROOT)}")

    referenced = {c.get("fixture") for c in cases}
    on_disk = {p.name for p in corpus_dir.glob("*.json")} - {"EXPECTATIONS.json"}
    orphans = on_disk - referenced
    if orphans:
        raise StructureError(
            f"{corpus_dir.name}: fixture file(s) present but referenced by no case: "
            + ", ".join(sorted(orphans))
        )

    passed = failed = 0
    for case in cases:
        for key in ("id", "fixture", "schema", "expect", "expect_errors"):
            if key not in case:
                raise StructureError(
                    f"{corpus_dir.name}: case missing {key!r}: {case.get('id', '(no id)')}"
                )
        cid = case["id"]
        doc = load_json(corpus_dir / case["fixture"], f"{cid} fixture")
        schema = load_schema(ROOT / case["schema"], f"{cid} schema")
        observed = observe(schema, doc, cid)

        if case["expect"] == "valid":
            if observed:
                print(f"  FAIL {cid}: expected valid, got {fmt(observed)}")
                failed += 1
            else:
                print(f"  ok   {cid}  valid as recorded  [{case.get('class', '')}]")
                passed += 1
            continue

        if case["expect"] != "invalid":
            raise StructureError(f"{cid}: expect must be 'valid' or 'invalid'")

        required = {expected_locus(cid, e) for e in case["expect_errors"]}
        if not required:
            raise StructureError(f"{cid}: an invalid case records no expected error")
        if not observed:
            print(f"  FAIL {cid}: expected invalid, document VALIDATED — mutation not killed")
            failed += 1
            continue
        missing = required - observed
        extra = observed - required
        if missing or extra:
            if missing:
                print(f"  FAIL {cid}: recorded locus did not fire: {fmt(missing)}")
            if extra:
                print(f"  FAIL {cid}: unrecorded locus fired (over-mutated?): {fmt(extra)}")
            failed += 1
        else:
            print(f"  ok   {cid}  killed on {fmt(required)}  [{case.get('class', '')}]")
            passed += 1

    return passed, failed


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        print(f"STRUCTURE: unexpected argument(s): {' '.join(argv[1:])}")
        print("usage: run-corpus.py   (no arguments; corpora are declared in CORPORA.json)")
        return STRUCTURE

    try:
        declared = load_json(FIXTURES / "CORPORA.json", "corpus declaration")
        built = set(declared.get("built", []))
        planned = set(declared.get("planned", []))

        # N1E: `__pycache__` is excluded BY NAME. The interpreter writes it into
        # fixtures/ whenever either instrument is imported as a module, and
        # without this line the runner reports it as an undeclared corpus — a
        # measurement broken by the act of taking it.
        discovered = {p.name for p in FIXTURES.iterdir()
                      if p.is_dir() and p.name != _PYCACHE}
        undeclared = discovered - built - planned
        if undeclared:
            raise StructureError(
                "corpus director(ies) present but not declared in CORPORA.json: "
                + ", ".join(sorted(undeclared))
            )
        for miss in sorted(built - discovered):
            raise StructureError(f"declared corpus {miss!r} does not exist")
        for p in sorted(planned & discovered):
            raise StructureError(
                f"planned corpus {p!r} now exists: give it an EXPECTATIONS.json "
                "and move it to 'built' in CORPORA.json"
            )

        total_pass = total_fail = 0
        for cname in sorted(built):
            p, f = run_corpus(FIXTURES / cname)
            total_pass += p
            total_fail += f
            print()
    except StructureError as e:
        print(f"STRUCTURE: {e}")
        return STRUCTURE
    except EnvironmentFailure as e:
        print(f"ENVIRONMENT: {e}")
        return ENVIRONMENT
    except Exception as e:
        # N1E: the path that used to escape. An uncaught exception exits 1, which
        # is this file's code for "an expectation failed", so the one accident
        # this runner must never have is the one it had. Nothing reaches the
        # interpreter's own handler now.
        print(f"ENVIRONMENT: unhandled {type(e).__name__}: {e}")
        return ENVIRONMENT

    print(f"TOTAL: {total_pass} passed, {total_fail} failed")
    if total_fail:
        print("CORPUS FAILED")
        return EXPECT_FAIL
    print("CORPUS CLEAN")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
