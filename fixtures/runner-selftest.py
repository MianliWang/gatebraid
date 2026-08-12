#!/usr/bin/env python3
"""Falsify run-corpus.py before its zero is trusted (spec §4, ADR-0028 §1).

Why this file is COMMITTED rather than a table in a document
------------------------------------------------------------
The first form of this batch's falsification was seven rows of prose asserting
exit codes and message fragments. The seeded inputs were temp copies that no
longer existed, no command was named, and the "corpus unmodified afterwards"
claim recorded no hash. Nobody could re-run a single row. That collides with
ADR-0028 §1 ("the demonstration is recorded beside its first use"), M3-PLAN §5.3
("machine-verifiable evidence ... never hand-narrated") and
convergence-metrics-v2 §4 ("a claimed value names the command that establishes
it ... the reader must be able to re-run what the writer relied on").

So the demonstration is this program. It seeds each condition into a throwaway
copy of the committed corpus, runs the real runner against it, and requires the
recorded exit status. It prints the SHA-256 of the corpus tree before and after
and requires them equal, so "the real corpus was not touched" is measured rather
than promised.

  Run:   <python> fixtures/runner-selftest.py
  Exits: 0 = every seeded condition produced its required status
         1 = at least one did not
         2 = the selftest could not run

Exit-status classes asserted here match run-corpus.py's contract:
  1 = an expectation failed · 2 = a corpus-structure or usage error
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


def tree_sha256(root: pathlib.Path) -> str:
    """Order-independent digest over every file's relative path and bytes."""
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.is_file():
            h.update(str(p.relative_to(root)).replace("\\", "/").encode("utf-8"))
            h.update(b"\0")
            h.update(p.read_bytes())
            h.update(b"\0")
    return h.hexdigest()


def run_runner(tree: pathlib.Path, extra_args: list[str] | None = None):
    """Invoke the real runner inside a seeded tree.

    encoding is pinned to UTF-8 deliberately: the runner emits em dashes, and
    this host's default console codec (cp936) raises UnicodeDecodeError on the
    third byte of one. That is the corpus's own BP-01 class, met here.
    """
    cmd = [sys.executable, str(tree / RUNNER_REL)] + (extra_args or [])
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


# --- seed functions: each mutates a throwaway copy -------------------------

def s_none(d):
    pass


def s_mutation_not_killed(d):
    """Repair an invalid fixture so it validates."""
    p = d / "fixtures/gate-run-v2/short-sha.json"
    doc = json.loads(p.read_text("utf-8"))
    doc["base_sha"] = "9f2c1a7b4e8d0356af91cc2be74d5108a3f6b2d9"
    p.write_text(json.dumps(doc, indent=2), encoding="utf-8")


def s_wrong_locus(d):
    """Point a recorded expectation at a locus that will not fire."""
    p = d / "fixtures/gate-run-v2/EXPECTATIONS.json"
    m = json.loads(p.read_text("utf-8"))
    for c in m["cases"]:
        if c["id"] == "GR2-05":
            c["expect_errors"] = [{"keyword": "required", "path": "notes"}]
    p.write_text(json.dumps(m, indent=2), encoding="utf-8")


def s_over_mutated(d):
    """Add a SECOND defect to a single-locus fixture; the extra must be caught."""
    p = d / "fixtures/gate-run-v2/short-sha.json"
    doc = json.loads(p.read_text("utf-8"))
    doc["gate"] = 9  # outside the enum, on top of the recorded short base_sha
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
    """A fixture file referenced by no case must not be silently ignored."""
    src = d / "fixtures/metrics-v1/valid-batch.json"
    shutil.copyfile(src, d / "fixtures/metrics-v1/unreferenced-extra.json")


def s_undeclared_corpus(d):
    """A corpus directory nobody declared must not pass as absent."""
    new = d / "fixtures/surprise-corpus"
    new.mkdir()
    (new / "EXPECTATIONS.json").write_text("{}", encoding="utf-8")


def s_malformed_manifest(d):
    (d / "fixtures/metrics-v1/EXPECTATIONS.json").write_text("{ not json", encoding="utf-8")


CASES = [
    ("S00 untouched copy",            0, s_none,               "CORPUS CLEAN"),
    ("S01 mutation not killed",       1, s_mutation_not_killed, "mutation not killed"),
    ("S02 recorded locus silent",     1, s_wrong_locus,        "recorded locus did not fire"),
    ("S03 unrecorded locus fired",    1, s_over_mutated,       "unrecorded locus fired"),
    ("S04 valid case broken",         1, s_valid_broken,       "expected valid"),
    ("S05 fixture missing",           2, s_fixture_missing,    "fixture missing"),
    ("S06 schema missing",            2, s_schema_missing,     "schema missing"),
    ("S07 invalid case unspecified",  2, s_unspecified_invalid, "records no expected error"),
    ("S08 orphan fixture file",       2, s_orphan_fixture,     "referenced by no case"),
    ("S09 undeclared corpus dir",     2, s_undeclared_corpus,  "not declared in CORPORA.json"),
    ("S10 malformed manifest",        2, s_malformed_manifest, "not valid JSON"),
]


def main() -> int:
    if not (ROOT / RUNNER_REL).is_file():
        print(f"SELFTEST: runner not found at {RUNNER_REL}")
        return 2

    before = tree_sha256(ROOT)
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

    # S11: usage error, asserted against the real tree (read-only, no seeding).
    rc, out = run_runner(ROOT, ["--unexpected"])
    results.append(("S11 unexpected argument", 2, rc, rc == 2 and "unexpected argument" in out,
                    "unexpected argument"))

    after = tree_sha256(ROOT)

    w = max(len(r[0]) for r in results)
    print(f"{'seeded condition'.ljust(w)}  want  got  verdict  required text")
    for name, want, got, ok, text in results:
        print(f"{name.ljust(w)}  {want:>4}  {got:>3}  {'PASS' if ok else 'FAIL':<7}  {text}")

    failed = sum(1 for r in results if not r[3])
    print()
    print(f"corpus tree sha256 before : {before}")
    print(f"corpus tree sha256 after  : {after}")
    print(f"corpus UNMODIFIED         : {before == after}")
    print(f"conditions failed         : {failed}")

    if before != after:
        print("SELFTEST FAILED: the selftest modified the real corpus")
        return 1
    if failed:
        print("SELFTEST FAILED")
        return 1
    print("SELFTEST CLEAN: every seeded condition produced its required exit status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
