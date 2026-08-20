#!/usr/bin/env python3
"""Falsify gatebraid-capture before its zero is trusted (spec section 4,
ADR-0028 decision 1).

"A pass from a never-falsified check is not evidence." This program is the
demonstration, recorded beside its first use, in the committed form ADR-0028
decision 1 requires - not a table of prose asserting what would have happened.
It is the sibling of `fixtures/runner-selftest.py`, which does the same office
for the corpus runner, and it borrows that file's two hard-won disciplines:
seeds mutate a THROWAWAY COPY, and the real tree's digest is measured before and
after so a seeding bug escaping into it cannot pass unnoticed (friction #128).

FIVE SECTIONS, ALL MEASURED
---------------------------
A. PRODUCTION-PATH POSITIVES. The real script, invoked as a subprocess through
   its real entry point, captures real commands - clean UTF-8, undecodable
   bytes, a wrong-but-clean codec, an unknown codec, a non-zero exit, an empty
   stream, a declared shell, pinned inputs and outputs, a declared environment
   subset, an unresolved cwd. Not a parallel code path (ADR-0028 section 4:
   "self-test exercising the production path, not a parallel one").

B. THE FROZEN CORPUS. Every case of `fixtures/evidence-capture-v1` is put
   through the generator's own guard via `--verify-record`, and the verdict must
   equal the corpus's recorded expectation. This is the measurable form of N2's
   "all applicable N1 mutations are killed": each mutation the corpus records as
   invalid must be REFUSED BY THE CONTRACT LAYER, and each valid case accepted.
   The corpus is read-only here; nothing in this file may repair it.

C. NEGATIVE CASES. One guard property broken per seed, on a COPY of the
   generator, requiring exit 1, NO FILE WRITTEN, and the RIGHT finding - a
   refusal for the wrong reason is not a kill. C00 runs an unseeded copy first,
   so a negative that fails because the throwaway environment is broken cannot
   be read as the guard working.

D. STRUCTURE CASES. Exit 2, never exit 1. "The instrument could not run" and
   "the instrument caught something" are different findings and one non-zero
   code would conflate them.

E. BYTE AND SURFACE DISCIPLINE. Every record produced in section A is counted
   for CRLF and lone CR; the generator's own source is checked for CR bytes,
   which is the property that makes its `source_sha256` the committed source's
   digest under `.gitattributes`' `* text=auto eol=lf`; and the seed-reachable
   surface digest must not move.

  Run:   <python> bin/gatebraid-capture-selftest.py
  Exits: 0 = every condition produced its required observation
         1 = at least one did not, or a seeded run mutated the real tree
         2 = a STRUCTURE or usage error - the selftest could not run
         3 = an ENVIRONMENT failure: this interpreter has no schema loader, so
             the guard-versus-schema cross-check could not run at all

THIS FILE IS 0/1/2/3; THE GENERATOR IS 0/1/2 (M3 batch N2-R2, R3)
-----------------------------------------------------------------
The divergence is not an inconsistency to be tidied away. It is the ADR-0009
boundary made visible. `gatebraid-capture.py` imports no schema loader, so it
structurally CANNOT have the failure class 3 names, and it does not reserve a
code it can never return. THIS file imports `jsonschema`, so it can have that
class - and at M3 batch N2-R it did: a loader present on one platform could not
evaluate the frozen schema, and this program recorded a tolerated GAP and exited
0. A selftest that meets an environment condition and returns zero is the same
conflation N1E spent a batch removing from `fixtures/run-corpus.py`. Both halves
are closed in `section_schema_crosscheck` below.
"""

from __future__ import annotations

import base64
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

GENERATOR_NAME = "gatebraid-capture.py"

# Exit codes. 0/1/2 as before; 3 is new at M3 batch N2-R2 (R3) and belongs to
# this file alone - see the taxonomy note in the module docstring.
CLEAN = 0
FAILED = 1
STRUCTURE = 2
ENVIRONMENT = 3

# The cross-check's three outcomes, kept apart because two of them are green and
# one of those two did not run.
CROSSCHECK_RUN = "run"
CROSSCHECK_FAILED = "failed"
CROSSCHECK_ABSENT = "absent"

# The frozen schemas carry a RELATIVE `$id` (`gatebraid/evidence-capture@1`).
# jsonschema's legacy RefResolver joins a relative base against itself and then
# tries to FETCH the result, so on that release the internal `$ref` cannot be
# resolved at all unless an absolute base is supplied at load. Any absolute base
# works; this one cannot resolve by construction - `.invalid` is reserved by RFC
# 2606 and guaranteed never to be delegated, so even a resolver that tried to
# dereference it could not reach a network.
#
# WRITTEN INDEPENDENTLY of `fixtures/run-corpus.py`'s `load_schema`, and
# deliberately NOT imported from it (M3 batch N2-R2, R1). The guard this file
# cross-checks is a SECOND expression of the frozen contract, and the whole value
# of the cross-check is that two independently authored readings agree; importing
# the other instrument's code would weaken the independence the check is made of.
# A base URI is environment plumbing, not contract expression - replicating it
# costs none of that independence, while refusing to replicate it cost the entire
# cross-check on one of the two platforms M3-PLAN.md section 7 item 7 names.
_SCHEMA_BASE = "https://schemas.invalid/"


def _schema_with_absolute_base(schema):
    """A COPY of `schema` whose `$id` is absolute; the input is never mutated.

    A relative reference is exactly one with no scheme (RFC 3986 section 4.2).
    The committed file on disk is not touched and must not be: `schema/` sits
    inside this program's own surface digest, so an attempt to touch it would
    fail loudly at the before/after comparison rather than quietly."""
    if not isinstance(schema, dict):
        return schema
    sid = schema.get("$id")
    if isinstance(sid, str) and not urllib.parse.urlsplit(sid).scheme:
        schema = dict(schema)
        schema["$id"] = _SCHEMA_BASE + sid.lstrip("/")
    return schema


def find_root(start):
    """Ascend to the repository root, identified by the artifacts this test
    reads rather than by a fixed number of `..` steps.

    Friction #128 is the reason: a digest labelled "corpus tree" was really a
    digest of whatever directory its script happened to sit two levels below.
    A hard-coded `parents[1]` is the same latent bug - it is correct in `bin/`
    and silently wrong while the file is staged elsewhere for review, which is
    exactly where this file lives before it lands."""
    for candidate in [start] + list(start.parents):
        if (candidate / "fixtures/CORPORA.json").is_file() and \
                (candidate / "schema/evidence-capture.schema.json").is_file():
            return candidate
    return None


HERE = pathlib.Path(__file__).resolve().parent
GENERATOR = HERE / GENERATOR_NAME
ROOT = find_root(HERE)
CORPUS_DIR = None if ROOT is None else ROOT / "fixtures/evidence-capture-v1"

PY = sys.executable
results = []


def record(name, want, got, ok, observation):
    results.append((name, want, got, ok, observation))


def run_generator(args, generator=None, cwd=None):
    proc = subprocess.run(
        [PY, str(generator or GENERATOR)] + [str(a) for a in args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(cwd) if cwd else None)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def expected_os():
    """The platform value this host must produce, derived INDEPENDENTLY of the
    generator's own detection so the check is evidence rather than a tautology:
    the generator reads `platform.uname().release`, this reads `/proc/version`.

    BP-03's schema-inexpressible half. `evidence-capture@1` can check that a
    capture names A platform from the enum; it cannot check that the name is
    the platform the capture ran on, and a dual-platform claim is read from two
    captures. A generator quietly writing `linux` under WSL would make the two
    captures of a dual-platform claim indistinguishable from one host's."""
    if sys.platform == "win32":
        return "windows"
    if sys.platform == "darwin":
        return "macos"
    if sys.platform.startswith("linux"):
        try:
            marker = pathlib.Path("/proc/version").read_bytes().lower()
        except OSError:
            marker = b""
        return "wsl" if b"microsoft" in marker else "linux"
    return None


def emit_bytes_argv(raw):
    """A child that writes exact bytes, so a capture's input is not at the mercy
    of the child's own text-mode encoding."""
    return [PY, "-c",
            "import sys;sys.stdout.buffer.write(%r)" % (raw,)]


# --------------------------------------------------------------------------
# A. production-path positives
# --------------------------------------------------------------------------

EM_DASH_UTF8 = b"before\xe2\x80\x94after"
UNDECODABLE_UTF8 = b"before\xff\xfeafter"


def section_a(tmp):
    produced = []

    def capture(name, args, checks):
        out = tmp / ("%s.json" % name)
        rc, text = run_generator(["--out", out, "--capture-id", name] + args)
        if rc != 0 or not out.is_file():
            record("A %s" % name, 0, rc, False, "record written and conforming")
            return
        doc = json.loads(out.read_bytes().decode("utf-8"))
        raw = out.read_bytes()
        failures = [label for label, ok in checks(doc) if not ok]
        if raw.count(b"\r\n") or _lone_cr(raw):
            failures.append("bytes carry CR")
        rc2, _ = run_generator(["--verify-record", out, "--rederive"])
        if rc2 != 0:
            failures.append("re-verify")
        record("A %s" % name, 0, rc, not failures,
               "; ".join(failures) if failures else "conforms, re-verifies, no CR")
        produced.append(out)

    capture("A01-argv-clean", ["--"] + emit_bytes_argv(EM_DASH_UTF8), lambda d: [
        ("form", d["invocation"]["form"] == "argv"),
        ("no shell semantics", "shell_semantics" not in d["invocation"]),
        ("decode ok", d["streams"]["stdout"]["rendered"]["decode_result"] == "ok"),
        ("byte length", d["streams"]["stdout"]["byte_length"] == len(EM_DASH_UTF8)),
        ("sha re-derives", d["streams"]["stdout"]["sha256"] ==
            hashlib.sha256(EM_DASH_UTF8).hexdigest()),
        ("base64 re-derives", base64.b64decode(
            d["streams"]["stdout"]["data"]) == EM_DASH_UTF8),
        ("cwd verified", d["invocation"]["cwd"]["resolution"] == "absolute-verified"),
        ("platform named from an independent source",
         d["platform"]["os"] == expected_os()),
    ])

    capture("A02-lossy-render",
            ["--"] + emit_bytes_argv(UNDECODABLE_UTF8), lambda d: [
                ("decode replaced",
                 d["streams"]["stdout"]["rendered"]["decode_result"] == "replaced"),
                ("carries error",
                 len(d["streams"]["stdout"]["rendered"].get("decode_error", "")) > 0),
                ("carries lossy text",
                 "text" in d["streams"]["stdout"]["rendered"]),
                ("bytes unharmed", base64.b64decode(
                    d["streams"]["stdout"]["data"]) == UNDECODABLE_UTF8),
            ])

    capture("A03-wrong-codec-clean",
            ["--render-codec", "cp936", "--"] + emit_bytes_argv(EM_DASH_UTF8),
            lambda d: [
                # cp936 decodes these bytes WITHOUT raising, into different
                # text. The rendering is honest and the bytes are the authority;
                # this case exists so that "decode_result: ok" is never read as
                # "the text is what the producer meant".
                ("decode ok",
                 d["streams"]["stdout"]["rendered"]["decode_result"] == "ok"),
                ("text differs from utf-8 reading",
                 d["streams"]["stdout"]["rendered"]["text"] !=
                 EM_DASH_UTF8.decode("utf-8")),
                ("bytes identical to A01", base64.b64decode(
                    d["streams"]["stdout"]["data"]) == EM_DASH_UTF8),
            ])

    capture("A04-unknown-codec",
            ["--render-codec", "no-such-codec", "--"] + emit_bytes_argv(b"x"),
            lambda d: [
                ("decode failed",
                 d["streams"]["stdout"]["rendered"]["decode_result"] == "failed"),
                ("carries error",
                 len(d["streams"]["stdout"]["rendered"].get("decode_error", "")) > 0),
                ("no text",
                 "text" not in d["streams"]["stdout"]["rendered"]),
            ])

    capture("A05-nonzero-exit",
            ["--", PY, "-c", "import sys;sys.exit(3)"], lambda d: [
                ("captured exit is 3", d["exit_code"] == 3),
                ("empty stdout", d["streams"]["stdout"]["byte_length"] == 0),
                ("empty data field", d["streams"]["stdout"]["data"] == ""),
            ])

    capture("A06-no-render",
            ["--no-render", "--"] + emit_bytes_argv(b"plain"), lambda d: [
                ("no rendering", "rendered" not in d["streams"]["stdout"]),
            ])

    shell_args = ["--form", "shell", "--shell-exe", "declared-shell",
                  "--pipefail", "false", "--exit-code-source", "pipeline_last",
                  "--"] + emit_bytes_argv(b"shell-form")
    capture("A07-shell-declared", shell_args, lambda d: [
        ("form shell", d["invocation"]["form"] == "shell"),
        ("semantics present", "shell_semantics" in d["invocation"]),
        ("pipefail recorded false",
         d["invocation"]["shell_semantics"]["pipefail"] is False),
        ("exit source recorded",
         d["invocation"]["shell_semantics"]["exit_code_source"] == "pipeline_last"),
    ])

    pinned = tmp / "pinned-input.txt"
    pinned.write_bytes(b"pinned bytes\n")
    written = tmp / "declared-output.txt"
    written.write_bytes(b"already here\n")
    capture("A08-inputs-outputs",
            ["--input", pinned, "--output", written, "--"]
            + emit_bytes_argv(b"io"), lambda d: [
                ("one input", len(d["inputs"]) == 1),
                ("input sha pinned", d["inputs"][0]["sha256"] ==
                 hashlib.sha256(b"pinned bytes\n").hexdigest()),
                ("one output", len(d["outputs"]) == 1),
                ("output sha", d["outputs"][0]["sha256"] ==
                 hashlib.sha256(b"already here\n").hexdigest()),
                ("output length", d["outputs"][0]["byte_length"] == 13),
            ])

    capture("A09-declared-env",
            ["--env", "PATH", "--"] + emit_bytes_argv(b"env"), lambda d: [
                ("env is a declared subset",
                 list(d["invocation"].get("environment", {}).keys()) == ["PATH"]),
            ])

    capture("A10-cwd-as-supplied",
            ["--cwd", ".", "--cwd-as-supplied", "--"] + emit_bytes_argv(b"cwd"),
            lambda d: [
                ("resolution as-supplied",
                 d["invocation"]["cwd"]["resolution"] == "as-supplied"),
            ])
    return produced


# --------------------------------------------------------------------------
# B. the frozen corpus
# --------------------------------------------------------------------------

def section_b():
    manifest = json.loads(
        (CORPUS_DIR / "EXPECTATIONS.json").read_bytes().decode("utf-8"))
    cases = manifest["cases"]
    killed = accepted = 0
    disagreements = []
    for case in cases:
        want_valid = case["expect"] == "valid"
        rc, text = run_generator(
            ["--verify-record", CORPUS_DIR / case["fixture"], "--rederive"])
        contract_line = ""
        for line in text.splitlines():
            if line.startswith("contract :"):
                contract_line = line.split(":", 1)[1].strip()
        if want_valid:
            ok = rc == 0 and contract_line == "conforms"
            accepted += 1 if ok else 0
        else:
            # The kill must come from the CONTRACT layer: that is the claim
            # "this generator implements the frozen interface", and a kill by
            # re-derivation alone would not establish it.
            ok = rc == 1 and contract_line != "conforms"
            killed += 1 if ok else 0
        if not ok:
            disagreements.append(case["id"])
    total_invalid = sum(1 for c in cases if c["expect"] == "invalid")
    total_valid = len(cases) - total_invalid
    record("B corpus evidence-capture-v1",
           "%d/%d" % (total_valid, total_invalid),
           "%d/%d" % (accepted, killed),
           not disagreements,
           "accepted/killed; disagreements: "
           + (", ".join(disagreements) if disagreements else "none"))
    return len(cases), total_valid, total_invalid, killed, accepted


# --------------------------------------------------------------------------
# C. negative cases - one broken property per seed, on a copy
# --------------------------------------------------------------------------

WRONG_BUT_WELL_FORMED_SHA = "0" * 63 + "1"

SEEDS = [
    ("C01 lone CR in the written bytes",
     [('    return (text + "\\n").encode("utf-8")',
       '    return (text + "\\r").encode("utf-8")')],
     "lone CR found in the serialized record", []),

    ("C02 binary_mode_write false",
     [('"binary_mode_write": True,', '"binary_mode_write": False,')],
     "const@self_assertions/binary_mode_write", []),

    ("C03 guard reported as not run",
     [('"zero_lone_cr": {"asserted": True, "count": 0},',
       '"zero_lone_cr": {"asserted": False, "count": 0},')],
     "const@self_assertions/zero_lone_cr/asserted", []),

    ("C04 guard run and overridden",
     [('"zero_lone_cr": {"asserted": True, "count": 0},',
       '"zero_lone_cr": {"asserted": True, "count": 7},')],
     "const@self_assertions/zero_lone_cr/count", []),

    ("C05 placeholder where a digest belongs",
     [('"source_sha256": source_sha256()', '"source_sha256": "<sha>"')],
     "pattern@generator/source_sha256", []),

    ("C06 stream digest does not re-derive",
     [('        "sha256": hashlib.sha256(raw).hexdigest(),',
       '        "sha256": "%s",' % WRONG_BUT_WELL_FORMED_SHA)],
     "sha256-mismatch@streams/stdout/sha256", []),

    ("C07 byte_length does not re-derive",
     [('        "byte_length": len(raw),', '        "byte_length": len(raw) + 1,')],
     "byte_length-mismatch@streams/stdout/byte_length", []),

    ("C08 capture ends before it starts",
     [('    ended_at = _now_rfc3339()',
       '    ended_at = "2020-01-01T00:00:00.000000Z"')],
     "ended-before-started@ended_at", []),

    ("C09 RFC3339-shaped but not a calendar instant",
     [('    ended_at = _now_rfc3339()',
       '    ended_at = "2026-02-31T00:00:00.000000Z"')],
     "not-a-calendar-instant@ended_at", []),

    ("C10 argv invocation carrying shell semantics",
     [('    if args.form == "shell":\n        invocation["shell_semantics"] = {',
       '    if True:\n        invocation["shell_semantics"] = {'),
      ('            "shell": args.shell_exe,',
       '            "shell": args.shell_exe or "declared-shell",'),
      ('            "exit_code_source": args.exit_code_source,',
       '            "exit_code_source": args.exit_code_source or "process",')],
     "not@invocation", []),

    ("C11 shell invocation without declared semantics",
     [('    if args.form == "shell":\n        invocation["shell_semantics"] = {',
       '    if False:\n        invocation["shell_semantics"] = {')],
     "required@invocation:shell_semantics",
     ["--form", "shell", "--shell-exe", "sh", "--pipefail", "true",
      "--exit-code-source", "process"]),

    ("C12 undeclared top-level field",
     [('    if args.notes:',
       '    record["undeclared_field"] = "x"\n    if args.notes:')],
     "additionalProperties@(root)x1", []),

    ("C13 environment dump over the cap",
     [('    started_at = _now_rfc3339()',
       '    environment = {("V%02d" % i): "x" for i in range(33)}\n'
       '    started_at = _now_rfc3339()')],
     "maxProperties@invocation/environment", []),

    ("C14 data outside the base64 grammar",
     [('        "data": base64.b64encode(raw).decode("ascii"),',
       '        "data": "A",')],
     "pattern@streams/stdout/data", []),

    ("C15 rendering not derivable from the bytes",
     [('            "text": raw.decode(codec, errors="strict"),',
       '            "text": "not derived from these bytes",')],
     "rendering-not-rederivable@streams/stdout/rendered/text", []),
]


def section_c(tmp):
    source = GENERATOR.read_bytes().decode("utf-8")

    # C00, the positive control. Without it, a negative case that fails because
    # the throwaway copy cannot run at all would be indistinguishable from the
    # guard doing its job.
    control_dir = tmp / "control"
    control_dir.mkdir(parents=True, exist_ok=True)
    control = control_dir / GENERATOR_NAME
    control.write_text(source, encoding="utf-8", newline="\n")
    out = control_dir / "control.json"
    rc, _ = run_generator(["--out", out, "--capture-id", "C00", "--"]
                          + emit_bytes_argv(b"control"), generator=control)
    record("C00 unseeded copy still writes", 0, rc,
           rc == 0 and out.is_file(), "the harness itself is sound")

    for name, replacements, want_text, extra_args in SEEDS:
        work = tmp / name.split()[0]
        work.mkdir(parents=True, exist_ok=True)
        seeded = source
        applied = True
        for old, new in replacements:
            if old not in seeded:
                applied = False
                break
            seeded = seeded.replace(old, new, 1)
        if not applied:
            record(name, 1, "n/a", False,
                   "SEED DID NOT APPLY - the generator's source moved")
            continue
        target = work / GENERATOR_NAME
        target.write_text(seeded, encoding="utf-8", newline="\n")
        out = work / "must-not-exist.json"
        rc, text = run_generator(
            ["--out", out, "--capture-id", name.split()[0]] + extra_args
            + ["--"] + emit_bytes_argv(b"seeded"), generator=target)
        refused = rc == 1
        silent = not out.exists()
        right_reason = want_text in text
        record(name, 1, rc, refused and silent and right_reason,
               "refused=%s no-file=%s right-finding=%s"
               % (refused, silent, right_reason))

    # C16 falsifies A01's platform comparison, which is a claim like any other.
    # It is deliberately NOT shaped like the seeds above: a wrong platform is
    # not refusable by the generator's guard - the record is contract-valid,
    # `macos` is in the enum, and the generator has no second source to
    # contradict itself with. The property is therefore owned by the
    # independent comparison in `expected_os()`, and what must be shown is that
    # the comparison FIRES. Recording which check owns a property, rather than
    # implying the guard owns them all, is the ADR-0028 decision 2 discipline.
    work = tmp / "C16"
    work.mkdir(parents=True, exist_ok=True)
    wrong = "macos" if expected_os() != "macos" else "linux"
    seeded = source.replace('        "os": os_name,',
                            '        "os": "%s",' % wrong, 1)
    if seeded == source:
        record("C16 wrong platform caught by comparison", "caught", "n/a",
               False, "SEED DID NOT APPLY - the generator's source moved")
        return
    target = work / GENERATOR_NAME
    target.write_text(seeded, encoding="utf-8", newline="\n")
    out = work / "wrong-platform.json"
    rc, _ = run_generator(["--out", out, "--capture-id", "C16", "--"]
                          + emit_bytes_argv(b"platform"), generator=target)
    accepted_by_guard = rc == 0 and out.is_file()
    caught = False
    if accepted_by_guard:
        doc = json.loads(out.read_bytes().decode("utf-8"))
        caught = doc["platform"]["os"] != expected_os()
    record("C16 wrong platform caught by comparison", "caught",
           "caught" if caught else "missed", accepted_by_guard and caught,
           "guard accepts it (contract-valid); the independent comparison "
           "is what fires")


# --------------------------------------------------------------------------
# D. structure cases - exit 2, never exit 1
# --------------------------------------------------------------------------

def section_d(tmp):
    junk = tmp / "not-json.txt"
    junk.write_bytes(b"{ not json")
    out = tmp / "structure.json"
    cases = [
        ("D01 no command", ["--out", out, "--capture-id", "D01"],
         "no command given"),
        ("D02 no --out", ["--capture-id", "D02", "--"] + emit_bytes_argv(b"x"),
         "--out is required"),
        ("D03 no --capture-id", ["--out", out, "--"] + emit_bytes_argv(b"x"),
         "--capture-id is required"),
        ("D04 input does not exist",
         ["--out", out, "--capture-id", "D04", "--input",
          tmp / "absent-input.txt", "--"] + emit_bytes_argv(b"x"),
         "declared input is not a readable file"),
        ("D05 cwd does not exist",
         ["--out", out, "--capture-id", "D05", "--cwd", tmp / "absent-dir",
          "--"] + emit_bytes_argv(b"x"),
         "cwd could not be resolved"),
        ("D06 command cannot be executed",
         ["--out", out, "--capture-id", "D06", "--",
          str(tmp / "no-such-executable")], "could not be executed"),
        ("D07 argv form given shell semantics",
         ["--out", out, "--capture-id", "D07", "--shell-exe", "sh", "--"]
         + emit_bytes_argv(b"x"), "cannot carry shell semantics"),
        ("D08 shell form missing its declarations",
         ["--out", out, "--capture-id", "D08", "--form", "shell", "--"]
         + emit_bytes_argv(b"x"), "form=shell requires"),
        ("D09 verify a file that is not JSON",
         ["--verify-record", junk], "not valid JSON"),
        ("D10 verify a file that is not there",
         ["--verify-record", tmp / "absent-record.json"],
         "could not be read"),
        ("D11 declared env var is not set",
         ["--out", out, "--capture-id", "D11", "--env",
          "GATEBRAID_DEFINITELY_UNSET_VARIABLE", "--"] + emit_bytes_argv(b"x"),
         "not set in this environment"),
        ("D12 verify given a command as well",
         ["--verify-record", CORPUS_DIR / "valid-argv-capture.json", "--"]
         + emit_bytes_argv(b"x"),
         "takes no command"),
    ]
    for name, args, want_text in cases:
        rc, text = run_generator(args)
        record(name, 2, rc, rc == 2 and want_text in text,
               "structure error kept distinct from a guard finding")


# --------------------------------------------------------------------------
# E. byte and surface discipline
# --------------------------------------------------------------------------

def _lone_cr(payload):
    count = 0
    for index, byte in enumerate(payload):
        if byte == 0x0D and payload[index + 1:index + 2] != b"\n":
            count += 1
    return count


def surface_digest(root):
    """The surface a run of this selftest could reach in the real tree: the
    frozen corpus, the schemas, and this program's own directory listing.
    Measured before and after, as `fixtures/runner-selftest.py` does."""
    digest = hashlib.sha256()
    entries = []
    for target in (root / "fixtures", root / "schema"):
        for path in sorted(target.rglob("*")):
            if path.is_file():
                entries.append(
                    (str(path.relative_to(root)).replace("\\", "/"), path))
    for rel, path in sorted(entries, key=lambda e: e[0]):
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def section_e(produced):
    source = GENERATOR.read_bytes()
    record("E01 generator source carries no CR byte", 0, source.count(b"\r"),
           source.count(b"\r") == 0,
           "so working-tree bytes are the committed bytes under eol=lf")
    total_crlf = sum(path.read_bytes().count(b"\r\n") for path in produced)
    total_lone = sum(_lone_cr(path.read_bytes()) for path in produced)
    record("E02 records written carry no CRLF", 0, total_crlf, total_crlf == 0,
           "over %d records" % len(produced))
    record("E03 records written carry no lone CR", 0, total_lone,
           total_lone == 0, "over %d records" % len(produced))


def _load_generator_module():
    """Import the generator for the two in-process checks WITHOUT writing a
    bytecode cache beside it.

    Measured at N2, the hard way: importing a committed instrument as a module
    creates a `__pycache__` directory next to it, and under `fixtures/` that
    directory WAS a new entry in the directory listing - which the frozen corpus
    digest folded in, and which `fixtures/run-corpus.py` refused outright as an
    undeclared corpus directory (exit 2). A read-only measurement mutated the
    tree and broke two committed instruments at once.

    CORRECTED AT M3 BATCH N2-R: M3 batch N1E falsified the second half of that
    paragraph. The committed runner and the committed digest now exclude
    `__pycache__` BY NAME (commit 5bc41d7667d1ae019b228d43ed1ef29ea5c0b928,
    `fixtures/run-corpus.py` and `fixtures/runner-selftest.py`). Re-measured
    against that commit with a `__pycache__` seeded under `fixtures/` in a
    throwaway copy: the runner exits 0, NOT 2, and the corpus digest is
    unchanged at f6128a0a...65686. The consequence this docstring asserted no
    longer follows, and a docstring is a claim like any other.

    The suppression STAYS - kept for the reason still load-bearing, not the one
    that lapsed. It is set HERE, before the import, and it suppresses the cache
    of the module being imported. Measured both ways at N2-R: with the flag
    unset the import creates `__pycache__` beside the generator; with it set no
    directory appears. The generator cannot do this for itself, because
    `sys.dont_write_bytecode` in a module BODY cannot suppress that module's own
    cache - the loader writes the cache before the body runs (measured at N1E).
    So the committed name exclusion is the half that keeps the corpus
    instruments honest, and this flag is the half that stops an instrument from
    writing anything at all beside a committed file. Two independent halves, on
    purpose.

    The flag is set here rather than left to the caller's `-B` flag, because a
    discipline that depends on remembering a command-line flag is not a
    discipline."""
    import importlib.util
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        return _import_from_path()
    finally:
        sys.dont_write_bytecode = previous


def _import_from_path():
    import importlib.util
    spec = importlib.util.spec_from_file_location("gatebraid_capture", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def section_g():
    """Guard faithfulness at two points the production path cannot reach.

    The generator always writes `count: 0`, so no capture it can produce
    exercises the JSON-equality rule that `false` is not `0` while `0.0` is.
    These are therefore direct calls on constructed documents - a unit check,
    named as one, beside the subprocess tests rather than instead of them.
    They exist because the L1 review found the guard using Python's `==` for a
    JSON `const`, where `false == 0` silently holds."""
    module = _load_generator_module()
    base = json.loads(
        (CORPUS_DIR / "valid-argv-capture.json").read_bytes().decode("utf-8"))

    doc = json.loads(json.dumps(base))
    doc["self_assertions"]["zero_lone_cr"]["count"] = False
    loci = module.check_contract(doc).format()
    ok = "const@self_assertions/zero_lone_cr/count" in loci and \
         "type@self_assertions/zero_lone_cr/count" in loci
    record("G01 count false is not count 0", "const+type",
           "found" if ok else "missed", ok,
           "a JSON boolean is not a JSON number")

    doc = json.loads(json.dumps(base))
    doc["self_assertions"]["zero_lone_cr"]["count"] = 0.0
    loci = module.check_contract(doc).format()
    record("G02 count 0.0 is count 0", "no locus",
           "clean" if not loci else "locus", not loci,
           "a number with zero fractional part is the integer 0")


def _loader_version():
    try:
        import importlib.metadata
        return importlib.metadata.version("jsonschema")
    except Exception:                                    # noqa: BLE001
        return "unknown"


def section_schema_crosscheck():
    """Require the guard and a real Draft202012Validator to agree case by case,
    on EVERY platform that has a loader.

    AMENDED AT M3 BATCH N2-R2 (R1, R2). Until this revision the check tolerated a
    GAP: where the loader could not evaluate the frozen schema it recorded the
    reason and PASSED. Measured at N2 and again at N2-R, that is exactly what
    happened on Ubuntu under WSL with jsonschema 4.10.3 - and the consequence, in
    this program's own words, was that a green selftest on that platform did not
    mean the cross-check had run. A check that cannot say it did not run is the
    mute class, sitting inside the program written to falsify.

    Two changes close it, and they are independent.

      1. The relative `$id` is rewritten to an absolute base ON AN IN-MEMORY COPY
         before validation. That is the one KNOWN cause of the failure, and it is
         measured rather than argued: on 4.10.3 the same committed schema and the
         same fixture raise RefResolutionError with no base and validate cleanly
         with one, while an invalid fixture still dies on its recorded locus. The
         rewrite is written independently of `fixtures/run-corpus.py` - see
         `_schema_with_absolute_base`.
      2. A loader that is PRESENT and still cannot evaluate the frozen schema is
         now a FAILURE, not a gap. The one known cause is repaired above, so any
         cause remaining is unknown, and an unknown cause that cannot fail is the
         defect this amendment exists to remove.

    The genuinely different environment survives: an interpreter with NO schema
    loader at all cannot run this check and is not defective for it. That case
    returns ABSENT and `main()` turns it into exit 3 - an environment status,
    never a silent zero. Status in the printed text, decision in the exit status.
    """
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        record("F schema cross-check", "agree", "ABSENT", True,
               "no schema loader importable by this interpreter - the "
               "cross-check cannot run here; this run exits %d (environment) "
               "rather than reporting a clean self-test" % ENVIRONMENT)
        return CROSSCHECK_ABSENT
    version = _loader_version()
    schema = _schema_with_absolute_base(json.loads(
        (ROOT / "schema/evidence-capture.schema.json").read_bytes().decode("utf-8")))
    module = _load_generator_module()
    manifest = json.loads(
        (CORPUS_DIR / "EXPECTATIONS.json").read_bytes().decode("utf-8"))
    disagreements = []
    for case in manifest["cases"]:
        doc = json.loads(
            (CORPUS_DIR / case["fixture"]).read_bytes().decode("utf-8"))
        guard_invalid = bool(module.check_contract(doc))
        try:
            schema_invalid = bool(
                list(Draft202012Validator(schema).iter_errors(doc)))
        except Exception as exc:                          # noqa: BLE001
            # R2: the loader is HERE and still could not evaluate the frozen
            # schema. The one known cause is repaired at load, so this is an
            # unknown cause and it must surface as a failure rather than pass as
            # a gap. Reported by class name and case id only - the offending
            # value is never echoed (ADR-0028 decision 3).
            record("F schema cross-check", "agree", "FAILED", False,
                   "loader %s is present and could not evaluate the frozen "
                   "schema at case %s (%s) - a FAILURE, not a tolerated gap"
                   % (version, case["id"], type(exc).__name__))
            return CROSSCHECK_FAILED
        if guard_invalid != schema_invalid:
            disagreements.append(case["id"])
    record("F schema cross-check", "agree",
           "disagree" if disagreements else "agree", not disagreements,
           "guard vs Draft202012Validator %s over %d cases; %s"
           % (version, len(manifest["cases"]),
              ", ".join(disagreements) if disagreements else "no disagreement"))
    return CROSSCHECK_RUN


_CROSSCHECK_SUMMARY = {
    CROSSCHECK_RUN: "run",
    CROSSCHECK_FAILED: "FAILED - loader present and unable; condition F above",
    CROSSCHECK_ABSENT:
        "NOT RUN - no schema loader on this interpreter (exit %d)" % ENVIRONMENT,
}


# --------------------------------------------------------------------------

def main():
    if not GENERATOR.is_file():
        sys.stdout.write("SELFTEST: generator not found beside this file\n")
        return STRUCTURE
    if ROOT is None:
        sys.stdout.write(
            "SELFTEST: repository root not found above this file; the frozen "
            "corpus and schemas are required\n")
        return STRUCTURE

    before = surface_digest(ROOT)
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="gatebraid-capture-selftest-"))
    try:
        produced = section_a(tmp)
        corpus_totals = section_b()
        section_c(tmp)
        section_d(tmp)
        section_e(produced)
        section_g()
        crosscheck = section_schema_crosscheck()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    after = surface_digest(ROOT)

    width = max(len(r[0]) for r in results)
    sys.stdout.write("%s  want  got  verdict  required observation\n"
                     % "condition".ljust(width))
    for name, want, got, ok, observation in results:
        sys.stdout.write("%s  %4s  %3s  %-7s  %s\n"
                         % (name.ljust(width), want, got,
                            "PASS" if ok else "FAIL", observation))

    failed = sum(1 for r in results if not r[3])
    total, valid, invalid, killed, accepted = corpus_totals
    sys.stdout.write("\n")
    sys.stdout.write("generator                     : %s\n" % GENERATOR.as_posix())
    sys.stdout.write("generator source_sha256       : %s\n"
                     % hashlib.sha256(GENERATOR.read_bytes()).hexdigest())
    sys.stdout.write("interpreter                   : %s\n" % PY)
    sys.stdout.write("platform                      : %s\n" % sys.platform)
    sys.stdout.write("corpus cases                  : %d (%d valid, %d invalid)\n"
                     % (total, valid, invalid))
    sys.stdout.write("mutations killed              : %d of %d\n" % (killed, invalid))
    sys.stdout.write("valid cases accepted          : %d of %d\n" % (accepted, valid))
    sys.stdout.write("schema cross-check            : %s\n"
                     % _CROSSCHECK_SUMMARY[crosscheck])
    sys.stdout.write("platform named by the records : %s\n" % expected_os())
    sys.stdout.write("surface digest before         : %s\n" % before)
    sys.stdout.write("surface digest after          : %s\n" % after)
    sys.stdout.write("corpus/schema surface UNMODIFIED: %s\n" % (before == after))
    sys.stdout.write("conditions failed             : %d\n" % failed)

    if before != after:
        sys.stdout.write("SELFTEST FAILED: a seeded run mutated the real tree\n")
        return FAILED
    if failed:
        sys.stdout.write("SELFTEST FAILED\n")
        return FAILED
    if crosscheck == CROSSCHECK_ABSENT:
        # Everything checkable passed, but not everything was checkable. Exit 3
        # says so; exit 0 would have claimed a falsification this run did not
        # perform. Ordered AFTER the failure checks deliberately - a condition
        # that actually failed is the more actionable finding and keeps exit 1,
        # the same precedence `fixtures/run-corpus.py` gives StructureError over
        # its own environment handler.
        sys.stdout.write(
            "SELFTEST ENVIRONMENT: no schema loader importable, so the "
            "guard-versus-schema cross-check could not run on this "
            "interpreter; every other condition passed\n")
        return ENVIRONMENT
    sys.stdout.write(
        "SELFTEST CLEAN: every condition produced its required observation\n")
    return CLEAN


if __name__ == "__main__":
    sys.exit(main())
