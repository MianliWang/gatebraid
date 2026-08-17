#!/usr/bin/env python3
"""Falsify run-corpus.py before its zero is trusted (spec §4, ADR-0028 §1).

Why this file is COMMITTED rather than a table in a document
------------------------------------------------------------
The first form of this batch's falsification was seven rows of prose asserting
exit codes and message fragments, with no re-runnable command and no recorded
hash. That collides with ADR-0028 §1 ("the demonstration is recorded beside its
first use"), M3-PLAN §5.3 ("never hand-narrated") and convergence-metrics-v2 §4
("a claimed value names the command that establishes it"). So the demonstration
is this program.

Amended at M3 batch N1C
-----------------------
* **Digest scope (D4, friction #128).** The digest previously covered
  `Path(__file__).parents[1]` — the staging directory while staged, and the
  WHOLE REPOSITORY including `.git` once committed, which is why one function
  returned a different value every time anyone ran it. It now covers the
  SEED-REACHABLE SURFACE: the declared corpora, `CORPORA.json`, `schema/`, and
  the `fixtures/` directory listing. Scoping it to the declared corpora alone
  was the first attempt and was too narrow — S06 deletes a file under `schema/`
  and S09 creates a sibling directory under `fixtures/`, so a seeding bug
  escaping into the real tree by either route would have gone unnoticed. The
  property asserted is "no seeded run mutated anything a seed can reach".
* **N1D (R3, D9, and three new seeds).** The digest scope gains
  `fixtures/run-corpus.py` and `fixtures/runner-selftest.py` — S16 rewrites the
  runner in a throwaway tree and the digest did not cover it, so an escape into
  the real file would have left "surface UNMODIFIED" green (external review R3);
  S21/S22 assert directly that the digest moves when either script's bytes move.
  Digest inputs are now sorted by the NORMALIZED RELATIVE-PATH STRING rather
  than by `Path` object, because `sorted()` over `Path` collates
  case-insensitively on Windows and case-sensitively elsewhere — the digest was
  location-independent but not platform-portable (D9). It is now intended to be
  both, and a cross-platform comparison is what §7 item 7 will eventually need.
* **Second-working-directory falsification (D4).** The runner resolves its root
  from `__file__`, so cwd should not matter. That is a claim, so it is tested:
  the suite runs the real corpus from a different working directory and requires
  an identical exit status and verdict.
* **Three new seeded conditions (A3)** proving the `required`-property narrowing
  fails when it is wrong: a recorded property that does not match, a `required`
  expectation missing its property, and a `property` recorded on a keyword where
  it is meaningless.
* **S16, the counter-case to S15.** S15 asserts that the runner's verdict does
  not depend on the working directory. On its own that is a pass from a
  never-falsified check, which ADR-0028 §1 refuses, so S16 breaks the property
  on a copy — rewriting the runner's root to resolve from the cwd — and requires
  S15's comparison to fail. S00, S11 and S15 assert rather than seed; the column
  header says "condition", not "seeded condition", for that reason.

Amended at M3 batch N1E — the two frozen-surface repairs, each falsified here
-----------------------------------------------------------------------------
* **`__pycache__` immunity (S27, S28).** Importing either instrument as a module
  writes `fixtures/__pycache__/`, which the runner then reported as an undeclared
  corpus (exit 2) and which moved this digest — a read-only measurement broken by
  the act of taking it. `sys.dont_write_bytecode` is set below and is NOT the
  fix: MEASURED at N1E, the flag set in a module's own body cannot suppress that
  module's own cache, because the loader writes the cache before the body runs.
  The fix is excluding the name from the discovery walk and from this digest, and
  S27/S28 are what stop that exclusion from being a comment nobody checked.
* **The environment exit code (S25, S26).** An uncaught exception exits 1, and 1
  is the runner's code for "an expectation failed" — so a jsonschema release that
  could not resolve the committed schemas' relative `$id` reported a surviving
  mutation. Exit 3 now means "this host could not evaluate the corpus". S25 seeds
  a reference the validator cannot resolve; S26 seeds the library away entirely.
  Both must produce 3, and the point of asserting 3 rather than merely non-zero
  is that the defect was a WRONG non-zero code, not a missing one.

  Run:   <python> fixtures/runner-selftest.py
  Exits: 0 = every seeded condition produced its required status
         1 = at least one did not, or a seeded run mutated the real corpus
         2 = the selftest could not run
"""

from __future__ import annotations

import sys

# Defence in depth, first thing. Measured caveat: this cannot stop THIS file's
# own cache when it is imported as a module — the loader writes that before the
# body runs — which is why `_PYCACHE` is excluded by name below.
sys.dont_write_bytecode = True

import hashlib
import json
import pathlib
import shutil
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
RUNNER_REL = "fixtures/run-corpus.py"

# Excluded by name from every walk below. The interpreter writes it; no human
# added it; it is not part of the corpus and must not be able to move a digest
# whose whole purpose is to say whether a seeded run escaped.
_PYCACHE = "__pycache__"


def declared_corpora(root: pathlib.Path) -> list[pathlib.Path]:
    """The built corpus directories, per CORPORA.json — the digest's scope."""
    decl = json.loads((root / "fixtures/CORPORA.json").read_bytes().decode("utf-8"))
    return [root / "fixtures" / name for name in sorted(decl.get("built", []))]


def digest_scope(root: pathlib.Path) -> list[pathlib.Path]:
    """Exactly what the seeded runs can touch — not the whole tree, and not only
    the corpora. The seeds delete a file under schema/ (S06), create a sibling
    directory under fixtures/ (S09) and edit CORPORA.json's neighbours, so a
    digest covering only the declared corpora would stop noticing three of its
    own cases escaping into the real tree."""
    paths = list(declared_corpora(root))
    paths.append(root / "fixtures/CORPORA.json")
    paths.append(root / "schema")
    # R3 (external review): S16 rewrites fixtures/run-corpus.py in a throwaway
    # tree, and the digest did not cover it — appending a byte to a copied runner
    # left the before/after digest identical, so an S16 path bug touching the REAL
    # runner would have kept the "surface UNMODIFIED" claim green. Both scripts
    # are seed-reachable and both are now in scope.
    paths.append(root / "fixtures/run-corpus.py")
    paths.append(root / "fixtures/runner-selftest.py")
    return paths


def corpora_digest(root: pathlib.Path) -> str:
    """Digest of the seed-reachable surface — NOT the tree the script sits in.

    The `fixtures/` directory LISTING is folded in as well, so a stray corpus
    directory appearing in the real tree changes the digest even though nothing
    inside the declared corpora moved.

    N1E: `__pycache__` is excluded from BOTH the listing and the file walk. It is
    interpreter output, not corpus content, and while it was in scope this digest
    reported "the surface moved" for a directory no seed and no author created."""
    h = hashlib.sha256()
    for entry in sorted(p.name for p in (root / "fixtures").iterdir()
                        if p.name != _PYCACHE):
        h.update(b"listing\0" + entry.encode("utf-8") + b"\0")

    # D9: collect (normalized relative path string, bytes) and sort by the STRING.
    # Sorting Path objects collated case-insensitively on Windows and
    # case-sensitively elsewhere, so the digest was location-independent but not
    # platform-portable — the coordinator reproduced this host's value from Linux
    # only by re-sorting identical bytes under casefolded collation. §7 item 7
    # eventually compares digests across platforms and needs one ordering.
    entries = []
    for target in digest_scope(root):
        if target.is_file():
            files = [target]
        else:
            files = [q for q in target.rglob("*")
                     if q.is_file() and _PYCACHE not in q.parts]
        for q in files:
            entries.append((str(q.relative_to(root)).replace("\\", "/"), q))
    for rel, q in sorted(entries, key=lambda e: e[0]):
        h.update(rel.encode("utf-8"))
        h.update(b"\0")
        h.update(q.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def run_runner(tree: pathlib.Path, extra_args=None, cwd=None):
    """Invoke the real runner. encoding pinned to UTF-8: the runner emits em
    dashes and this host's console default (cp936) raises on them — the corpus's
    own BP-01 class, met here."""
    cmd = [sys.executable, str(tree / RUNNER_REL)] + (extra_args or [])
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace",
                       cwd=str(cwd) if cwd else None)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


# --- seed functions: each mutates a throwaway copy -------------------------

def s_none(d):
    pass


def s_mutation_not_killed(d):
    p = d / "fixtures/gate-run-v2/short-sha.json"
    doc = json.loads(p.read_text("utf-8"))
    doc["base_sha"] = "9f2c1a7b4e8d0356af91cc2be74d5108a3f6b2d9"
    p.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def s_wrong_locus(d):
    p = d / "fixtures/gate-run-v2/EXPECTATIONS.json"
    m = json.loads(p.read_text("utf-8"))
    for c in m["cases"]:
        if c["id"] == "GR2-05":
            # schema_path is mandatory since D6; without it this seed would trip
            # the STRUCTURE check (exit 2) instead of the locus-mismatch check it
            # exists to exercise (exit 1). S20 covers the missing-schema_path case.
            c["expect_errors"] = [{"keyword": "required", "path": "notes",
                                   "schema_path": "properties/notes/required",
                                   "property": "nope"}]
    p.write_text(json.dumps(m, indent=2), encoding="utf-8")


def s_over_mutated(d):
    p = d / "fixtures/gate-run-v2/short-sha.json"
    doc = json.loads(p.read_text("utf-8"))
    doc["gate"] = 9
    p.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def s_valid_broken(d):
    p = d / "fixtures/gate-run-v2/valid-at2-record.json"
    doc = json.loads(p.read_text("utf-8"))
    doc["gate"] = 9
    p.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def s_fixture_missing(d):
    (d / "fixtures/gate-run-v2/missing-approval-author.json").unlink()


def s_schema_missing(d):
    (d / "schema/gate-run.schema.json").unlink()


def s_unspecified_invalid(d):
    p = d / "fixtures/metrics-v1/EXPECTATIONS.json"
    m = json.loads(p.read_text("utf-8"))
    for c in m["cases"]:
        if c["id"] == "MT1-05":
            c["expect_errors"] = []
    p.write_text(json.dumps(m, indent=2), encoding="utf-8")


def s_orphan_fixture(d):
    src = d / "fixtures/metrics-v1/valid-batch.json"
    shutil.copyfile(src, d / "fixtures/metrics-v1/unreferenced-extra.json")


def s_undeclared_corpus(d):
    new = d / "fixtures/surprise-corpus"
    new.mkdir()
    (new / "EXPECTATIONS.json").write_text("{}", encoding="utf-8")


def s_malformed_manifest(d):
    (d / "fixtures/metrics-v1/EXPECTATIONS.json").write_text("{ not json", encoding="utf-8")


# --- A3: the required-property narrowing must fail when it is wrong --------

def _ec_manifest(d):
    return d / "fixtures/evidence-capture-v1/EXPECTATIONS.json"


def s_wrong_required_property(d):
    """The right path, the WRONG missing property — must not count as a kill."""
    p = _ec_manifest(d)
    m = json.loads(p.read_text("utf-8"))
    for c in m["cases"]:
        if c["id"] == "EC1-33":          # missing-platform.json
            for e in c["expect_errors"]:
                if e["keyword"] == "required":
                    e["property"] = "inputs"   # the neighbouring case's property
    p.write_text(json.dumps(m, indent=2), encoding="utf-8")


def s_required_without_property(d):
    """A `required` expectation that does not say which property — structure error."""
    p = _ec_manifest(d)
    m = json.loads(p.read_text("utf-8"))
    for c in m["cases"]:
        if c["id"] == "EC1-32":
            for e in c["expect_errors"]:
                e.pop("property", None)
    p.write_text(json.dumps(m, indent=2), encoding="utf-8")


def s_property_on_wrong_keyword(d):
    """`property` where it is meaningless — a key the runner must refuse, not ignore."""
    p = _ec_manifest(d)
    m = json.loads(p.read_text("utf-8"))
    for c in m["cases"]:
        if c["id"] == "EC1-28":          # data-not-valid-base64.json -> pattern
            for e in c["expect_errors"]:
                e["property"] = "data"
    p.write_text(json.dumps(m, indent=2), encoding="utf-8")


def s_two_extra_properties(d):
    """R1: a SECOND unexpected key must not pass a manifest recording one."""
    p = d / "fixtures/evidence-capture-v1/unknown-top-level-field.json"
    doc = json.loads(p.read_text("utf-8"))
    doc["second_unexpected_key"] = "x"
    p.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def s_nonfinite_json(d):
    """R2: a non-RFC numeric literal is not JSON; the corpus is unreadable, exit 2."""
    p = d / "fixtures/metrics-v1/valid-batch.json"
    p.write_text('{"schema": "gatebraid/metrics@1", "value": NaN}', encoding="utf-8")


def s_wrong_schema_path(d):
    """D6: a recorded schema_path that names the other branch must not count."""
    p = d / "fixtures/evidence-capture-v1/EXPECTATIONS.json"
    m = json.loads(p.read_text("utf-8"))
    for c in m["cases"]:
        if c["id"] == "EC1-09":
            for e in c["expect_errors"]:
                e["schema_path"] = e["schema_path"].replace("allOf/2", "allOf/3")
    p.write_text(json.dumps(m, indent=2), encoding="utf-8")


def s_schema_path_missing(d):
    """D6: every expectation must record a schema_path."""
    p = d / "fixtures/metrics-v1/EXPECTATIONS.json"
    m = json.loads(p.read_text("utf-8"))
    for c in m["cases"]:
        if c["id"] == "MT1-06":
            for e in c["expect_errors"]:
                e.pop("schema_path", None)
    p.write_text(json.dumps(m, indent=2), encoding="utf-8")


def s_extra_count_missing(d):
    """R1: an additionalProperties expectation must record extra_count."""
    p = _ec_manifest(d)
    m = json.loads(p.read_text("utf-8"))
    for c in m["cases"]:
        if c["id"] == "EC1-20":
            for e in c["expect_errors"]:
                e.pop("extra_count", None)
    p.write_text(json.dumps(m, indent=2), encoding="utf-8")


def s_extra_count_on_wrong_keyword(d):
    """R1: extra_count is meaningless anywhere else."""
    p = _ec_manifest(d)
    m = json.loads(p.read_text("utf-8"))
    for c in m["cases"]:
        if c["id"] == "EC1-28":
            for e in c["expect_errors"]:
                e["extra_count"] = 1
    p.write_text(json.dumps(m, indent=2), encoding="utf-8")


# --- N1E: the environment class must be 3, never 1 -------------------------

def s_unresolvable_ref(d):
    """The validator MACHINERY raises. On WSL this was RefResolutionError over a
    relative `$id`; here it is a pointer to nowhere, which raises on every
    jsonschema release without touching a network. Either way the runner must say
    ENVIRONMENT and exit 3 — the exact accident being repaired is that an escape
    from this path exits 1, the code for a surviving mutation."""
    p = d / "schema/metrics.schema.json"
    s = json.loads(p.read_text("utf-8"))
    s["properties"]["metrics"] = {"$ref": "#/$defs/thisPointerDoesNotExist"}
    p.write_text(json.dumps(s, indent=2), encoding="utf-8")


def s_validator_absent(d):
    """The library itself is missing. Previously exit 2, which called an absent
    dependency a malformed corpus; it is an environment fact and is now 3."""
    p = d / RUNNER_REL
    src = p.read_text("utf-8")
    broken = src.replace(
        "    from jsonschema import Draft202012Validator",
        "    from jsonschema_absent_by_seed import Draft202012Validator")
    assert broken != src, "validator-absent seed did not apply"
    p.write_text(broken, encoding="utf-8", newline="\n")


# --- N1E: __pycache__ must not be able to move the measurement -------------

def s_pycache_present(d):
    """Exactly what importing an instrument produces. The runner must still be
    clean: before the repair this was exit 2, 'not declared in CORPORA.json'."""
    cache = d / "fixtures" / _PYCACHE
    cache.mkdir()
    (cache / "run-corpus.cpython-312.pyc").write_bytes(b"\xcb\x0d\x0d\x0a seeded")


CASES = [
    ("S00 untouched copy",            0, s_none,                    "CORPUS CLEAN"),
    ("S01 mutation not killed",       1, s_mutation_not_killed,     "mutation not killed"),
    ("S02 recorded locus silent",     1, s_wrong_locus,             "recorded locus did not fire"),
    ("S03 unrecorded locus fired",    1, s_over_mutated,            "unrecorded locus fired"),
    ("S04 valid case broken",         1, s_valid_broken,            "expected valid"),
    ("S05 fixture missing",           2, s_fixture_missing,         "fixture missing"),
    ("S06 schema missing",            2, s_schema_missing,          "schema missing"),
    ("S07 invalid case unspecified",  2, s_unspecified_invalid,     "records no expected error"),
    ("S08 orphan fixture file",       2, s_orphan_fixture,          "referenced by no case"),
    ("S09 undeclared corpus dir",     2, s_undeclared_corpus,       "not declared in CORPORA.json"),
    ("S10 malformed manifest",        2, s_malformed_manifest,      "not valid JSON"),
    ("S12 wrong required property",   1, s_wrong_required_property, "recorded locus did not fire"),
    ("S13 required without property", 2, s_required_without_property, "must record which property"),
    ("S14 property on wrong keyword", 2, s_property_on_wrong_keyword, "only meaningful on a 'required'"),
    ("S17 second unexpected property",  1, s_two_extra_properties,  "unrecorded locus fired"),
    ("S18 non-finite JSON literal",     2, s_nonfinite_json,        "non-JSON numeric constant"),
    ("S19 wrong schema_path",           1, s_wrong_schema_path,     "recorded locus did not fire"),
    ("S20 schema_path missing",         2, s_schema_path_missing,   "expectation missing 'schema_path'"),
    ("S23 extra_count missing",         2, s_extra_count_missing,   "must record extra_count"),
    ("S24 extra_count wrong keyword",   2, s_extra_count_on_wrong_keyword,
                                           "only meaningful on an 'additionalProperties'"),
    ("S25 validator cannot resolve",    3, s_unresolvable_ref,      "ENVIRONMENT"),
    ("S26 validator library absent",    3, s_validator_absent,      "not importable"),
    ("S27 __pycache__ present",         0, s_pycache_present,       "CORPUS CLEAN"),
]


def main() -> int:
    if not (ROOT / RUNNER_REL).is_file():
        print(f"SELFTEST: runner not found at {RUNNER_REL}")
        return 2

    before = corpora_digest(ROOT)
    results = []

    for name, want_rc, seed, want_text in CASES:
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="gatebraid-selftest-"))
        try:
            work = tmp / "tree"
            shutil.copytree(ROOT, work)
            seed(work)
            rc, out = run_runner(work)
            ok = rc == want_rc and want_text in out
            results.append((name, want_rc, rc, ok, want_text))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # S11: usage error, against the real tree (read-only).
    rc, out = run_runner(ROOT, ["--unexpected"])
    results.append(("S11 unexpected argument", 2, rc,
                    rc == 2 and "unexpected argument" in out, "unexpected argument"))

    # S15 (D4): the runner resolves its root from __file__, so the working
    # directory must not change its verdict. That is a claim; here it is tested.
    other = pathlib.Path(tempfile.mkdtemp(prefix="gatebraid-cwd-"))
    try:
        rc_a, out_a = run_runner(ROOT, cwd=ROOT)
        rc_b, out_b = run_runner(ROOT, cwd=other)
        same = rc_a == rc_b == 0 and ("CORPUS CLEAN" in out_a) and ("CORPUS CLEAN" in out_b)
        results.append(("S15 cwd-independence holds", 0, rc_b, same, "CORPUS CLEAN from both"))
    finally:
        shutil.rmtree(other, ignore_errors=True)

    # S16: S15 asserts a property; on its own that is a pass from a never-falsified
    # check, which ADR-0028 §1 refuses. Here the property is BROKEN on a copy — the
    # runner's root is rewritten to resolve from the working directory instead of
    # __file__ — and S15's comparison is required to fail.
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="gatebraid-cwdneg-"))
    try:
        work = tmp / "tree"
        shutil.copytree(ROOT, work)
        runner = work / RUNNER_REL
        src = runner.read_text("utf-8")
        broken = src.replace(
            "ROOT = pathlib.Path(__file__).resolve().parents[1]",
            "ROOT = pathlib.Path.cwd()")
        assert broken != src, "cwd-negative seed did not apply"
        runner.write_text(broken, encoding="utf-8", newline="\n")
        elsewhere = pathlib.Path(tempfile.mkdtemp(prefix="gatebraid-cwdneg2-"))
        try:
            rc_c, _ = run_runner(work, cwd=work)
            rc_d, out_d = run_runner(work, cwd=elsewhere)
            # With a cwd-derived root the run from `elsewhere` must NOT come back
            # clean; if it did, S15 would be measuring nothing.
            broke = not (rc_d == 0 and "CORPUS CLEAN" in out_d)
            results.append(("S16 cwd-independence falsified", "!=0", rc_d, broke,
                            "must NOT be clean from elsewhere"))
        finally:
            shutil.rmtree(elsewhere, ignore_errors=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # S21/S22 (R3): the digest must actually move when either script's bytes move.
    # A scope that lists a file but never reaches it would pass every seed above.
    for tag, rel in (("S21 digest sees run-corpus.py", "fixtures/run-corpus.py"),
                     ("S22 digest sees runner-selftest.py", "fixtures/runner-selftest.py")):
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="gatebraid-digest-"))
        try:
            work = tmp / "tree"
            shutil.copytree(ROOT, work)
            base_digest = corpora_digest(work)
            target = work / rel
            target.write_bytes(target.read_bytes() + b"\n# digest sensitivity probe\n")
            moved = corpora_digest(work) != base_digest
            results.append((tag, "moves", "moves" if moved else "same", moved,
                            "digest must change when the file changes"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    # S28 (N1E): and the exact converse for __pycache__ — the digest must NOT move
    # for a directory the interpreter wrote. S21/S22 prove the digest is sensitive;
    # without S28 the exclusion could be over-broad and nothing would say so.
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="gatebraid-pycache-"))
    try:
        work = tmp / "tree"
        shutil.copytree(ROOT, work)
        base_digest = corpora_digest(work)
        s_pycache_present(work)
        (work / "schema" / _PYCACHE).mkdir()
        (work / "schema" / _PYCACHE / "x.pyc").write_bytes(b"\xcb\x0d\x0d\x0a seeded")
        held = corpora_digest(work) == base_digest
        results.append(("S28 __pycache__ moves no digest", "same",
                        "same" if held else "moves", held,
                        "digest must ignore interpreter output"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    after = corpora_digest(ROOT)

    w = max(len(r[0]) for r in results)
    print(f"{'condition'.ljust(w)}  want  got  verdict  required observation")
    for name, want, got, ok, text in results:
        print(f"{name.ljust(w)}  {str(want):>4}  {str(got):>3}  {'PASS' if ok else 'FAIL':<7}  {text}")

    failed = sum(1 for r in results if not r[3])
    scope = ", ".join(p.name for p in digest_scope(ROOT)) + ", fixtures/ listing"
    print()
    print(f"digest scope                  : {scope}")
    print(f"digest before                 : {before}")
    print(f"digest after                  : {after}")
    print(f"seed-reachable surface UNMODIFIED: {before == after}")
    print(f"conditions failed             : {failed}")

    if before != after:
        print("SELFTEST FAILED: a seeded run mutated the real corpus")
        return 1
    if failed:
        print("SELFTEST FAILED")
        return 1
    print("SELFTEST CLEAN: every seeded condition produced its required exit status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
