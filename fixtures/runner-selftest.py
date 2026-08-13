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

  Run:   <python> fixtures/runner-selftest.py
  Exits: 0 = every seeded condition produced its required status
         1 = at least one did not, or a seeded run mutated the real corpus
         2 = the selftest could not run
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
RUNNER_REL = "fixtures/run-corpus.py"


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
    return paths


def corpora_digest(root: pathlib.Path) -> str:
    """Digest of the seed-reachable surface — NOT the tree the script sits in.

    The `fixtures/` directory LISTING is folded in as well, so a stray corpus
    directory appearing in the real tree changes the digest even though nothing
    inside the declared corpora moved."""
    h = hashlib.sha256()
    for entry in sorted(p.name for p in (root / "fixtures").iterdir()):
        h.update(b"listing\0" + entry.encode("utf-8") + b"\0")
    for target in digest_scope(root):
        if target.is_file():
            files = [target]
        else:
            files = sorted(q for q in target.rglob("*") if q.is_file())
        for q in files:
            h.update(str(q.relative_to(root)).replace("\\", "/").encode("utf-8"))
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
            c["expect_errors"] = [{"keyword": "required", "path": "notes",
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

    after = corpora_digest(ROOT)

    w = max(len(r[0]) for r in results)
    print(f"{'condition'.ljust(w)}  want  got  verdict  required observation")
    for name, want, got, ok, text in results:
        print(f"{name.ljust(w)}  {str(want):>4}  {got:>3}  {'PASS' if ok else 'FAIL':<7}  {text}")

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
