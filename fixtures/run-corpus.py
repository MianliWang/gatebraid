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

A LOCUS IS (keyword, path, property)
------------------------------------
Amended at M3 batch N1C (A3). Previously a locus was (keyword, path), which
could not say WHICH required property was missing: three fixtures removing three
different top-level keys all recorded `required@(root)`, so a validator that
rejected one of them for another's reason still passed. `jsonschema` emits one
error per missing property and names it in the message, so `required` loci now
carry that property and are checked in both directions like any other.

The manifest must therefore record `property` on every `required` expectation
and must NOT record it on any other keyword — both are structure errors. A key
the runner ignores would read as coverage it does not enforce, which is the
failure this amendment exists to remove, not to relocate.

Findings are reported by keyword, path and property, never by echoing the
offending value into the output (spec §4: a checker never quotes what it forbids
into a record).

Exit status decides, not the printed text (spec §4).
  0 = every expectation held
  1 = an EXPECTATION failed (a mutation not killed, a valid case broken, wrong,
      missing or extra loci)
  2 = a CORPUS-STRUCTURE or usage error (missing/malformed manifest, fixture or
      schema; undeclared or unreferenced file; a malformed expectation). Distinct
      from 1 on purpose: "the corpus is broken" and "the corpus caught something"
      are different findings and one non-zero code would conflate them.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("STRUCTURE: jsonschema is not importable by this interpreter.")
    print("           On this host use C:/Python312/python.exe (jsonschema 4.23.0).")
    sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"

EXPECT_FAIL = 1
STRUCTURE = 2

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


def load_json(path: pathlib.Path, what: str):
    try:
        return json.loads(path.read_bytes().decode("utf-8"))
    except FileNotFoundError:
        raise StructureError(f"{what} missing: {path.relative_to(ROOT)}")
    except UnicodeDecodeError as e:
        raise StructureError(f"{what} is not UTF-8: {path.relative_to(ROOT)} ({e})")
    except json.JSONDecodeError as e:
        raise StructureError(f"{what} is not valid JSON: {path.relative_to(ROOT)} ({e})")


def locus(err) -> tuple[str, str, str | None]:
    path = "/".join(str(p) for p in err.absolute_path) or "(root)"
    prop = None
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
    return (err.validator, path, prop)


def loci(errors) -> set[tuple[str, str, str | None]]:
    return {locus(e) for e in errors}


def fmt(triples) -> str:
    out = []
    for k, p, prop in sorted(triples, key=lambda t: (t[0], t[1], t[2] or "")):
        out.append(f"{k}@{p}:{prop}" if prop is not None else f"{k}@{p}")
    return ", ".join(out)


def expected_locus(case_id: str, e: dict) -> tuple[str, str, str | None]:
    for key in ("keyword", "path"):
        if key not in e:
            raise StructureError(f"{case_id}: expectation missing {key!r}")
    kw = e["keyword"]
    has_prop = "property" in e
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
    return (kw, e["path"], e.get("property"))


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
        schema = load_json(ROOT / case["schema"], f"{cid} schema")
        observed = loci(Draft202012Validator(schema).iter_errors(doc))

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

        discovered = {p.name for p in FIXTURES.iterdir() if p.is_dir()}
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

    print(f"TOTAL: {total_pass} passed, {total_fail} failed")
    if total_fail:
        print("CORPUS FAILED")
        return EXPECT_FAIL
    print("CORPUS CLEAN")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
