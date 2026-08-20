#!/usr/bin/env python3
"""gatebraid-capture - the Gatebraid evidence generator (M3 batch N2).

Captures ONE command execution as a `gatebraid/evidence-capture@1` record: the
canonical, machine-readable evidence document. Markdown renderings of a capture
are a DERIVED VIEW and never a second hand-written authority (M3-PLAN.md
section 2, N2).

WHAT THIS INSTRUMENT DOES NOT DO
--------------------------------
It does not define its own output contract. `schema/evidence-capture.schema.json`
is frozen at N1, BEFORE this program was authored, and this program IMPLEMENTS
it. Any interface change returns to an approved N1 correct-course; nothing here
may narrow, widen or reinterpret the contract (M3-PLAN.md section 2, N1).

It is also not the validator. N3 re-derives verdicts from the JSON plus the
frozen schemas alone, independently of this code. The guard below exists so the
generator cannot WRITE a non-conforming record - it is not, and must not be
read as, independent validation of what it wrote.

STDLIB ONLY
-----------
ADR-0009 fixes plugin scripts as "Python 3 stdlib only", so this program does
NOT import `jsonschema`. Consequence, stated rather than left implicit: the
guard in `check_contract()` is a SECOND EXPRESSION of the frozen contract, and
two expressions can disagree. That risk is not argued away, it is measured -
`gatebraid-capture-selftest.py` runs every fixture of the frozen
`evidence-capture-v1` corpus through this guard and requires the verdicts to
equal the corpus's recorded expectations, and, where `jsonschema` happens to be
importable, requires the guard and `Draft202012Validator` to agree fixture by
fixture. A disagreement is a defect in this file, never in the schema.

EXIT STATUS DECIDES, NOT THE PRINTED TEXT (spec section 4)
----------------------------------------------------------
  0  the record was written and re-read clean
  1  the record FAILED ITS OWN GUARD - nothing was written, or --verify-record
     found a violation. "The instrument caught something."
  2  a STRUCTURE or usage error - bad arguments, an input that does not exist,
     an unresolvable cwd, an unlaunchable command, an unreadable file.
     "The instrument could not run." Distinct from 1 on purpose: one non-zero
     code would conflate the two, which is the distinction
     `fixtures/run-corpus.py` already keeps and for the same reason.

THERE IS DELIBERATELY NO EXIT 3, AND THE OMISSION IS THE CLAIM (M3 batch N2-R2)
------------------------------------------------------------------------------
`fixtures/run-corpus.py` reserves 3 for an ENVIRONMENT failure - "this
interpreter could not evaluate the frozen schema at all" - and that failure class
requires a schema loader to have. This program imports none: it is stdlib-only
under ADR-0009, which is precisely what that rule bought. It therefore cannot
reach the condition 3 names, and a code an instrument can never return is a claim
it cannot honour - worse than an absent one, because a reader would take the
reserved code as a hazard this program actually guards. The subset 0/1/2 is
deliberate, not an oversight. `gatebraid-capture-selftest.py` DOES import a
loader, so it does carry exit 3; the two taxonomies differ because the ADR-0009
boundary runs between the two files.

THE EXIT CODE OF THIS PROGRAM IS NOT THE EXIT CODE OF THE CAPTURED COMMAND.
A capture of a failing command is a successful capture. The captured status
lives in the record's `exit_code`, and what that number measures is declared in
`invocation.shell_semantics.exit_code_source` whenever a shell was involved -
the IN-01 class: with `pipefail` off a pipeline's status is its LAST element's,
so a captured 0 proves nothing about an upstream stage.

FINDINGS NEVER QUOTE THE OFFENDING VALUE
----------------------------------------
A checker never quotes what it forbids into a record (ADR-0028 decision 3,
spec section 4). Every finding this program prints is (keyword, instance path)
plus, where the constraint is about multiplicity or a named key, the property
name or a count. No offending value is ever echoed - not a bad base64 string,
not a placeholder digest, not an unexpected key's name.

GUARDED STEPS, IN THE ORDER THEY GATE THE WRITE
-----------------------------------------------
Each is a separate step whose failure PREVENTS the write (spec section 4):
  1. inputs are hashed BEFORE the command runs (pinned-SHA inputs, #108)
  2. the assembled record is checked against the frozen contract (layer A)
  3. and against re-derivation: base64 decodes, sha256 and byte_length
     re-derive from the decoded bytes, `ended_at >= started_at`, timestamps are
     real calendar instants, any rendering re-derives from the bytes (layer B).
     Layer B is where the relations the schema explicitly CANNOT express are
     enforced on the write path.
  4. the serialized bytes are counted for lone CR; a non-zero count REFUSES the
     write (#108). The `zero_lone_cr.count: 0` in the record is therefore a
     measurement of the bytes that were about to land, not a claim added after.
  5. the file is written binary, then RE-READ and re-checked, and the digest of
     what landed is compared with the digest of what was serialized (ADR-0028
     section 4, "assembly verified after writing").

Usage
-----
  gatebraid-capture.py --out REC.json --capture-id ID [options] -- CMD [ARG...]
  gatebraid-capture.py --verify-record REC.json [--rederive]

Runtime output is deliberately ASCII-only. This host's console default is cp936
and it raises on the em dashes the committed prose uses; an instrument that
cannot print its own verdict on the host it runs on is the BP-01 class biting
the checker (friction #60, and `fixtures/runner-selftest.py` pins UTF-8 for
exactly this reason when it drives the corpus runner).
"""

from __future__ import annotations

import argparse
import base64
import binascii
import datetime as dt
import hashlib
import json
import os
import pathlib
import platform as platform_mod
import re
import subprocess
import sys

NAME = "gatebraid-capture"
VERSION = "1.0.0"
SCHEMA_ID = "gatebraid/evidence-capture@1"

OK = 0
NONCONFORMANT = 1
STRUCTURE = 2

ENV_MAX_PROPERTIES = 32          # schema: invocation.environment.maxProperties

# The frozen schema's patterns, transcribed. Two deliberate substitutions, both
# to preserve the schema's OWN stated semantics under Python's `re`:
#   * `$` becomes `\Z`. ECMA-262 - which JSON Schema specifies - anchors `$` at
#     end of input, while Python's `$` also matches before a final newline. `\Z`
#     is the ECMA `$`. Without this, a digest or base64 string with a trailing
#     newline would pass here and fail a conforming validator.
#   * the timestamp pattern already ends in `(?![\s\S])` and is copied verbatim;
#     the schema chose that form for this exact reason and says so.
RE_TIMESTAMP = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:\d{2})(?![\s\S])"
)
RE_SHA256 = re.compile(r"^[0-9a-f]{64}\Z")
RE_BASE64 = re.compile(r"^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?\Z")

FORM_VALUES = ("argv", "shell")
RESOLUTION_VALUES = ("absolute-verified", "as-supplied")
EXIT_CODE_SOURCE_VALUES = ("process", "pipeline_last", "pipeline_any_failure")
OS_VALUES = ("windows", "wsl", "linux", "macos")
DECODE_RESULT_VALUES = ("ok", "replaced", "failed")

RECORD_PROPERTIES = (
    "schema", "capture_id", "generator", "invocation", "exit_code", "streams",
    "started_at", "ended_at", "inputs", "outputs", "platform",
    "self_assertions", "notes",
)
RECORD_REQUIRED = (
    "schema", "capture_id", "generator", "invocation", "exit_code", "streams",
    "started_at", "ended_at", "platform", "inputs", "outputs",
    "self_assertions",
)


class StructureError(Exception):
    """The instrument could not run. Exit 2, never 1."""


# --------------------------------------------------------------------------
# findings
# --------------------------------------------------------------------------

class Findings:
    """(keyword, path[, property][, count]) tuples. Never a value.

    The shape follows `fixtures/run-corpus.py`'s locus tuple so a reader
    comparing this instrument's output with the corpus runner's is comparing
    like with like: `keyword@path`, `:property` for `required`, `xN` for
    `additionalProperties` multiplicity.
    """

    def __init__(self):
        self.items = []

    def add(self, keyword, path="", prop=None, count=None):
        self.items.append((keyword, path or "(root)", prop, count))

    def __bool__(self):
        return bool(self.items)

    def __len__(self):
        return len(self.items)

    def format(self):
        out = []
        for keyword, path, prop, count in sorted(
            self.items, key=lambda t: tuple(str(x) for x in t)
        ):
            text = "%s@%s" % (keyword, path)
            if prop is not None:
                text += ":%s" % prop
            if count is not None:
                text += "x%d" % count
            out.append(text)
        return ", ".join(out)


def _join(path, key):
    return "%s/%s" % (path, key) if path else str(key)


def _is_integer(value):
    """JSON Schema `integer`: a number with zero fractional part. `true` is not
    a number in JSON Schema even though Python makes bool a subclass of int."""
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return True
    return isinstance(value, float) and value.is_integer()


def _json_equal(left, right):
    """JSON equality for `const`, which Python's `==` does not give: `false ==
    0` and `true == 1` hold in Python and do NOT hold in JSON, where a boolean
    and a number are different types. L1 review finding - without this,
    `count: false` escaped the `const: 0` locus (it was still refused, by the
    `type` locus, so the verdict never moved; the finding is faithfulness to
    the frozen contract, not a missed rejection)."""
    if isinstance(left, bool) != isinstance(right, bool):
        return False
    return left == right


# --------------------------------------------------------------------------
# layer A - conformance with the frozen contract
# --------------------------------------------------------------------------

def _check_object(value, path, required, properties, f):
    """`type: object` + `additionalProperties: false` + `required`.

    Returns False when the value is not an object, so the caller stops: in JSON
    Schema a failed `type` does not evaluate the subschemas beneath it, and a
    guard that kept going would report loci a conforming validator never emits.
    """
    if not isinstance(value, dict):
        f.add("type", path)
        return False
    extra = [k for k in value if k not in properties]
    if extra:
        f.add("additionalProperties", path, count=len(extra))
    for key in required:
        if key not in value:
            f.add("required", path, prop=key)
    return True


def _check_string(value, path, f, min_length=None, pattern=None, enum=None,
                  const=None):
    if not isinstance(value, str):
        f.add("type", path)
        return False
    if const is not None and value != const:
        f.add("const", path)
    if enum is not None and value not in enum:
        f.add("enum", path)
    if min_length is not None and len(value) < min_length:
        f.add("minLength", path)
    if pattern is not None and not pattern.search(value):
        f.add("pattern", path)
    return True


def _check_integer(value, path, f, minimum=None):
    if not _is_integer(value):
        f.add("type", path)
        return False
    if minimum is not None and value < minimum:
        f.add("minimum", path)
    return True


def _check_byte_stream(stream, path, f):
    """$defs/byteStream - THE BYTE CONTRACT (the P0-2 remedy)."""
    properties = ("encoding", "byte_length", "sha256", "data", "rendered")
    required = ("encoding", "byte_length", "sha256", "data")
    if not _check_object(stream, path, required, properties, f):
        return
    if "encoding" in stream:
        _check_string(stream["encoding"], _join(path, "encoding"), f,
                      const="base64")
    if "byte_length" in stream:
        _check_integer(stream["byte_length"], _join(path, "byte_length"), f,
                       minimum=0)
    if "sha256" in stream:
        _check_string(stream["sha256"], _join(path, "sha256"), f,
                      pattern=RE_SHA256)
    if "data" in stream:
        _check_string(stream["data"], _join(path, "data"), f,
                      pattern=RE_BASE64)
    if "rendered" in stream:
        _check_rendered(stream["rendered"], _join(path, "rendered"), f)


def _check_rendered(rendered, path, f):
    """The DERIVED VIEW. Never authoritative, and never what a verdict reads."""
    properties = ("decode_codec", "decode_result", "decode_error", "text")
    required = ("decode_codec", "decode_result")
    if not _check_object(rendered, path, required, properties, f):
        return
    if "decode_codec" in rendered:
        _check_string(rendered["decode_codec"], _join(path, "decode_codec"), f,
                      min_length=1)
    if "decode_error" in rendered:
        _check_string(rendered["decode_error"], _join(path, "decode_error"), f,
                      min_length=1)
    if "text" in rendered:
        _check_string(rendered["text"], _join(path, "text"), f)
    if "decode_result" not in rendered:
        return
    result = rendered["decode_result"]
    if not _check_string(result, _join(path, "decode_result"), f,
                         enum=DECODE_RESULT_VALUES):
        return

    # The four conditionals, in the schema's own allOf order so that a reader
    # can put them side by side with it.
    if result in ("replaced", "failed") and "decode_error" not in rendered:
        f.add("required", path, prop="decode_error")          # allOf/0
    if result == "failed" and "text" in rendered:
        f.add("not", path)                                    # allOf/1
    if result == "replaced" and "text" not in rendered:
        f.add("required", path, prop="text")                  # allOf/2
    if result == "ok":
        if "text" not in rendered:
            f.add("required", path, prop="text")              # allOf/3 then
        if "decode_error" in rendered:
            f.add("not", path)                                # allOf/3 not


def _check_invocation(inv, f):
    path = "invocation"
    properties = ("form", "argv", "shell_semantics", "cwd", "environment")
    required = ("form", "argv", "cwd")
    if not _check_object(inv, path, required, properties, f):
        return
    if "form" in inv:
        _check_string(inv["form"], _join(path, "form"), f, enum=FORM_VALUES)
    if "argv" in inv:
        argv = inv["argv"]
        if not isinstance(argv, list):
            f.add("type", _join(path, "argv"))
        else:
            if len(argv) < 1:
                f.add("minItems", _join(path, "argv"))
            for index, item in enumerate(argv):
                if not isinstance(item, str):
                    f.add("type", _join(_join(path, "argv"), index))
    if "cwd" in inv:
        cwd_path = _join(path, "cwd")
        if _check_object(inv["cwd"], cwd_path, ("path", "resolution"),
                         ("path", "resolution"), f):
            if "path" in inv["cwd"]:
                _check_string(inv["cwd"]["path"], _join(cwd_path, "path"), f,
                              min_length=1)
            if "resolution" in inv["cwd"]:
                _check_string(inv["cwd"]["resolution"],
                              _join(cwd_path, "resolution"), f,
                              enum=RESOLUTION_VALUES)
    if "environment" in inv:
        env_path = _join(path, "environment")
        env = inv["environment"]
        if not isinstance(env, dict):
            f.add("type", env_path)
        else:
            if len(env) > ENV_MAX_PROPERTIES:
                f.add("maxProperties", env_path)
            for key, value in env.items():
                if not isinstance(value, str):
                    f.add("type", _join(env_path, key))
    if "shell_semantics" in inv:
        sem_path = _join(path, "shell_semantics")
        keys = ("shell", "pipefail", "exit_code_source")
        if _check_object(inv["shell_semantics"], sem_path, keys, keys, f):
            sem = inv["shell_semantics"]
            if "shell" in sem:
                _check_string(sem["shell"], _join(sem_path, "shell"), f,
                              min_length=1)
            if "pipefail" in sem and not isinstance(sem["pipefail"], bool):
                f.add("type", _join(sem_path, "pipefail"))
            if "exit_code_source" in sem:
                _check_string(sem["exit_code_source"],
                              _join(sem_path, "exit_code_source"), f,
                              enum=EXIT_CODE_SOURCE_VALUES)

    # allOf/0 - a shell invocation without declared semantics is an exit code
    # nobody can interpret. allOf/1 - and `argv` means no shell was involved,
    # so it cannot describe the shell's exit-code semantics (F6).
    form = inv.get("form")
    if form == "shell" and "shell_semantics" not in inv:
        f.add("required", path, prop="shell_semantics")
    if form == "argv" and "shell_semantics" in inv:
        f.add("not", path)


def _check_self_assertions(block, f):
    path = "self_assertions"
    keys = ("zero_lone_cr", "binary_mode_write")
    if not _check_object(block, path, keys, keys, f):
        return
    if "binary_mode_write" in block and block["binary_mode_write"] is not True:
        f.add("const", _join(path, "binary_mode_write"))
    if "zero_lone_cr" not in block:
        return
    cr_path = _join(path, "zero_lone_cr")
    cr_keys = ("asserted", "count")
    if not _check_object(block["zero_lone_cr"], cr_path, cr_keys, cr_keys, f):
        return
    cr = block["zero_lone_cr"]
    if "asserted" in cr and cr["asserted"] is not True:
        f.add("const", _join(cr_path, "asserted"))
    if "count" in cr:
        _check_integer(cr["count"], _join(cr_path, "count"), f, minimum=0)
    # The record exists, so the write happened. `asserted: true` with a
    # non-zero count therefore describes a state the guard is defined to make
    # impossible.
    if cr.get("asserted") is True and "count" in cr and \
            not _json_equal(cr["count"], 0):
        f.add("const", _join(cr_path, "count"))


def _check_file_list(items, path, f, with_byte_length):
    if not isinstance(items, list):
        f.add("type", path)
        return
    keys = ("path", "sha256", "byte_length") if with_byte_length \
        else ("path", "sha256")
    for index, entry in enumerate(items):
        entry_path = _join(path, index)
        if not _check_object(entry, entry_path, keys, keys, f):
            continue
        if "path" in entry:
            _check_string(entry["path"], _join(entry_path, "path"), f,
                          min_length=1)
        if "sha256" in entry:
            _check_string(entry["sha256"], _join(entry_path, "sha256"), f,
                          pattern=RE_SHA256)
        if with_byte_length and "byte_length" in entry:
            _check_integer(entry["byte_length"],
                           _join(entry_path, "byte_length"), f, minimum=0)


def check_contract(doc):
    """LAYER A. Exactly the constraints of `gatebraid/evidence-capture@1`.

    Nothing stronger belongs here: this function's verdicts are measured
    against the frozen corpus for EQUALITY, so an extra check would show up as
    a disagreement with the schema and would be indistinguishable from a bug.
    Everything the schema cannot express lives in `check_coherence()`.
    """
    f = Findings()
    if not _check_object(doc, "", RECORD_REQUIRED, RECORD_PROPERTIES, f):
        return f

    if "schema" in doc:
        _check_string(doc["schema"], "schema", f, const=SCHEMA_ID)
    if "capture_id" in doc:
        _check_string(doc["capture_id"], "capture_id", f, min_length=1)
    if "notes" in doc:
        _check_string(doc["notes"], "notes", f)
    if "exit_code" in doc:
        _check_integer(doc["exit_code"], "exit_code", f)
    for field in ("started_at", "ended_at"):
        if field in doc:
            _check_string(doc[field], field, f, pattern=RE_TIMESTAMP)

    if "generator" in doc:
        keys = ("name", "version", "source_sha256")
        if _check_object(doc["generator"], "generator", keys, keys, f):
            gen = doc["generator"]
            for field in ("name", "version"):
                if field in gen:
                    _check_string(gen[field], _join("generator", field), f,
                                  min_length=1)
            if "source_sha256" in gen:
                _check_string(gen["source_sha256"],
                              "generator/source_sha256", f, pattern=RE_SHA256)

    if "invocation" in doc:
        _check_invocation(doc["invocation"], f)

    if "streams" in doc:
        keys = ("stdout", "stderr")
        if _check_object(doc["streams"], "streams", keys, keys, f):
            for key in keys:
                if key in doc["streams"]:
                    _check_byte_stream(doc["streams"][key],
                                       _join("streams", key), f)

    if "inputs" in doc:
        _check_file_list(doc["inputs"], "inputs", f, with_byte_length=False)
    if "outputs" in doc:
        _check_file_list(doc["outputs"], "outputs", f, with_byte_length=True)

    if "platform" in doc:
        keys = ("os", "os_release", "interpreter")
        if _check_object(doc["platform"], "platform", keys, keys, f):
            plat = doc["platform"]
            if "os" in plat:
                _check_string(plat["os"], "platform/os", f, enum=OS_VALUES)
            for field in ("os_release", "interpreter"):
                if field in plat:
                    _check_string(plat[field], _join("platform", field), f,
                                  min_length=1)

    if "self_assertions" in doc:
        _check_self_assertions(doc["self_assertions"], f)

    return f


# --------------------------------------------------------------------------
# layer B - the relations the schema states it cannot express
# --------------------------------------------------------------------------

def _parse_rfc3339(text):
    """Real calendar instant, or None. The schema's patterns check LEXICAL FORM
    only and say so: a month of 13, an mday of 45 or 2026-02-31 all match. The
    schema names range validity as a downstream duty; on the write path it is
    enforced here so this generator cannot emit an impossible instant."""
    if not isinstance(text, str):
        return None
    normalized = text.strip()
    if normalized[-1:] in ("z", "Z"):
        normalized = normalized[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(normalized)
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def check_coherence(doc):
    """LAYER B. Everything `evidence-capture@1` explicitly CANNOT check:

      * `data` actually decodes as base64 (the pattern is a grammar, not a
        decoder);
      * `sha256` and `byte_length` RE-DERIVE from the decoded bytes - named in
        the schema's own `data` description as not expressible there;
      * `ended_at >= started_at` - named in `ended_at`'s description as a
        downstream duty, "a capture whose end precedes its start validates
        against this schema and must be rejected";
      * both timestamps are real instants, not merely RFC3339-shaped;
      * a rendering re-derives from the bytes it claims to render.

    Layer A is the schema; this is the part of the byte contract a JSON Schema
    cannot hold. Both gate the write.
    """
    f = Findings()
    if not isinstance(doc, dict):
        return f

    streams = doc.get("streams")
    if isinstance(streams, dict):
        for key in ("stdout", "stderr"):
            stream = streams.get(key)
            if not isinstance(stream, dict):
                continue
            path = _join("streams", key)
            data = stream.get("data")
            if not isinstance(data, str):
                continue
            try:
                raw = base64.b64decode(data, validate=True)
            except (binascii.Error, ValueError):
                f.add("undecodable", _join(path, "data"))
                continue
            if _is_integer(stream.get("byte_length")) and \
                    stream["byte_length"] != len(raw):
                f.add("byte_length-mismatch", _join(path, "byte_length"))
            if isinstance(stream.get("sha256"), str) and \
                    hashlib.sha256(raw).hexdigest() != stream["sha256"]:
                f.add("sha256-mismatch", _join(path, "sha256"))
            rendered = stream.get("rendered")
            if isinstance(rendered, dict):
                _check_rendering_rederives(raw, rendered, _join(path, "rendered"), f)

    started = doc.get("started_at")
    ended = doc.get("ended_at")
    if isinstance(started, str) and _parse_rfc3339(started) is None:
        f.add("not-a-calendar-instant", "started_at")
    if isinstance(ended, str) and _parse_rfc3339(ended) is None:
        f.add("not-a-calendar-instant", "ended_at")
    start_dt = _parse_rfc3339(started)
    end_dt = _parse_rfc3339(ended)
    if start_dt is not None and end_dt is not None and end_dt < start_dt:
        f.add("ended-before-started", "ended_at")
    return f


def _check_rendering_rederives(raw, rendered, path, f):
    """A derived view that cannot be derived from the bytes is not a view of
    them. Cheap to check and it is the whole reason the field is marked
    non-authoritative."""
    codec = rendered.get("decode_codec")
    result = rendered.get("decode_result")
    if not isinstance(codec, str) or not isinstance(result, str):
        return
    if result == "ok":
        try:
            expected = raw.decode(codec, errors="strict")
        except (UnicodeDecodeError, LookupError):
            f.add("rendering-not-rederivable", _join(path, "decode_result"))
            return
        if rendered.get("text") != expected:
            f.add("rendering-not-rederivable", _join(path, "text"))
    elif result == "replaced":
        try:
            expected = raw.decode(codec, errors="replace")
        except LookupError:
            f.add("rendering-not-rederivable", _join(path, "decode_codec"))
            return
        if rendered.get("text") != expected:
            f.add("rendering-not-rederivable", _join(path, "text"))


# --------------------------------------------------------------------------
# capture
# --------------------------------------------------------------------------

def _now_rfc3339():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


def _sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_sha256():
    """The exact instrument, not merely its version string.

    `.gitattributes` pins `* text=auto eol=lf`, so the working-tree bytes of a
    text file are the committed bytes and this digest is the committed source's
    digest. That is a property of the repository's configuration, so the
    selftest measures it rather than trusting this sentence."""
    return _sha256_file(pathlib.Path(__file__).resolve())


def detect_platform():
    if sys.platform == "win32":
        os_name = "windows"
    elif sys.platform == "darwin":
        os_name = "macos"
    elif sys.platform.startswith("linux"):
        release = platform_mod.uname().release.lower()
        os_name = "wsl" if ("microsoft" in release or "wsl" in release) else "linux"
    else:
        # Fail closed. `platform.os` is a closed enum and guessing a value
        # outside it would produce a record that cannot be admitted anyway.
        raise StructureError(
            "platform is outside the closed enum windows|wsl|linux|macos")
    return {
        "os": os_name,
        "os_release": platform_mod.platform(),
        "interpreter": "%s %s (%s)" % (
            platform_mod.python_implementation(),
            platform_mod.python_version(),
            pathlib.Path(sys.executable).as_posix(),
        ),
    }


def build_stream(raw, codec, render):
    stream = {
        "encoding": "base64",
        "byte_length": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "data": base64.b64encode(raw).decode("ascii"),
    }
    if not render:
        return stream
    try:
        stream["rendered"] = {
            "decode_codec": codec,
            "decode_result": "ok",
            "text": raw.decode(codec, errors="strict"),
        }
    except UnicodeDecodeError as exc:
        # CPython's own exception text, with its own reported offset - not a
        # composed sentence. The corpus's EC1-03 was built the same way.
        stream["rendered"] = {
            "decode_codec": codec,
            "decode_result": "replaced",
            "decode_error": str(exc),
            "text": raw.decode(codec, errors="replace"),
        }
    except LookupError as exc:
        stream["rendered"] = {
            "decode_codec": codec,
            "decode_result": "failed",
            "decode_error": str(exc),
        }
    return stream


def count_lone_cr(payload):
    """CR bytes not followed by LF. `#108`'s guard, and the reason it is counted
    over the SERIALIZED BYTES rather than over any string: what lands on disk is
    what matters, and a text-mode write is precisely how a lone CR appears
    without anyone choosing it."""
    return len(re.findall(rb"\r(?!\n)", payload))


def count_crlf(payload):
    return len(re.findall(rb"\r\n", payload))


def serialize(record):
    """UTF-8 bytes. `json.dumps` escapes every control character, so no raw CR,
    LF or NUL from a captured stream is ever embedded directly in a JSON string
    - which is the contract's own sentence, made true by the serializer rather
    than hoped for."""
    text = json.dumps(record, ensure_ascii=False, indent=2, sort_keys=False)
    return (text + "\n").encode("utf-8")


def capture(args):
    resolved_cwd, resolution = _resolve_cwd(args.cwd, args.cwd_as_supplied)

    inputs = []
    for path in args.input:
        candidate = pathlib.Path(path)
        if not candidate.is_file():
            raise StructureError("declared input is not a readable file")
        inputs.append({"path": path, "sha256": _sha256_file(candidate)})

    environment = {}
    for name in args.env:
        # A DECLARED SUBSET, never a dump: the caller names each variable.
        # L1 review finding: an unset name used to be recorded as "", which
        # makes "declared and empty" and "declared and absent" the same
        # document. That is the absent-versus-none_configured conflation
        # ADR-0019 removed at the check level, and the contract gives no way to
        # express absence here - values are strings. So it fails closed: the
        # caller's declaration is wrong and the capture does not paper over it.
        if name not in os.environ:
            raise StructureError(
                "a declared environment variable is not set in this "
                "environment; absence is not expressible in the contract")
        environment[name] = os.environ[name]
    if len(environment) > ENV_MAX_PROPERTIES:
        raise StructureError(
            "declared environment exceeds the contract's cap of %d names"
            % ENV_MAX_PROPERTIES)

    started_at = _now_rfc3339()
    try:
        completed = subprocess.run(
            args.argv,
            cwd=str(resolved_cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,          # the declared shell is an explicit argv[0];
        )                         # this program never interpolates a string
    except OSError as exc:
        raise StructureError("the command could not be executed (%s)"
                             % type(exc).__name__)
    ended_at = _now_rfc3339()

    invocation = {
        "form": args.form,
        "argv": list(args.argv),
        "cwd": {"path": args.cwd if args.cwd_as_supplied else str(resolved_cwd),
                "resolution": resolution},
    }
    if environment:
        invocation["environment"] = environment
    if args.form == "shell":
        invocation["shell_semantics"] = {
            "shell": args.shell_exe,
            "pipefail": args.pipefail == "true",
            "exit_code_source": args.exit_code_source,
        }

    outputs = []
    for path in args.output:
        candidate = pathlib.Path(path)
        if not candidate.is_file():
            raise StructureError("declared output is not a readable file")
        outputs.append({
            "path": path,
            "sha256": _sha256_file(candidate),
            "byte_length": candidate.stat().st_size,
        })

    record = {
        "schema": SCHEMA_ID,
        "capture_id": args.capture_id,
        "generator": {"name": NAME, "version": VERSION,
                      "source_sha256": source_sha256()},
        "invocation": invocation,
        "exit_code": completed.returncode,
        "streams": {
            "stdout": build_stream(completed.stdout or b"", args.render_codec,
                                   not args.no_render),
            "stderr": build_stream(completed.stderr or b"", args.render_codec,
                                   not args.no_render),
        },
        "started_at": started_at,
        "ended_at": ended_at,
        "inputs": inputs,
        "outputs": outputs,
        "platform": detect_platform(),
        "self_assertions": {
            "zero_lone_cr": {"asserted": True, "count": 0},
            "binary_mode_write": True,
        },
    }
    if args.notes:
        record["notes"] = args.notes
    return record


def _resolve_cwd(raw, as_supplied):
    if as_supplied:
        if not raw:
            raise StructureError("--cwd-as-supplied requires --cwd")
        return pathlib.Path(raw), "as-supplied"
    candidate = pathlib.Path(raw) if raw else pathlib.Path.cwd()
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError):
        raise StructureError("cwd could not be resolved to an existing path")
    if not resolved.is_dir():
        raise StructureError("cwd is not a directory")
    return resolved, "absolute-verified"


def write_record(record, out_path, report):
    """Guarded steps 2 through 5. Any failure PREVENTS the write."""
    contract = check_contract(record)
    coherence = check_coherence(record)
    if contract or coherence:
        report("GUARD: the assembled record does not conform; nothing written")
        if contract:
            report("  contract : " + contract.format())
        if coherence:
            report("  coherence: " + coherence.format())
        return NONCONFORMANT

    try:
        payload = serialize(record)
    except (UnicodeEncodeError, ValueError, TypeError) as exc:
        # L1 review finding: a record that cannot be serialized used to crash
        # with a traceback. An instrument that dies instead of refusing has no
        # exit status anyone can read, which is friction #127's class exactly.
        report("GUARD: the record could not be serialized (%s); nothing written"
               % type(exc).__name__)
        return NONCONFORMANT
    lone_cr = count_lone_cr(payload)
    if lone_cr != 0:
        # The record claims count 0; the bytes disagree; the write does not
        # happen. This is the guarded step, not a claim added afterwards.
        report("GUARD: lone CR found in the serialized record; nothing written")
        report("  self_assertions/zero_lone_cr/count would be untrue")
        return NONCONFORMANT

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as handle:      # binary write, always
        handle.write(payload)

    # Assembly verified AFTER writing: re-read, re-parse, re-check, compare
    # digests. A write that silently transformed its bytes would otherwise be
    # invisible, which is exactly how text mode invalidates every digest above.
    landed = out_path.read_bytes()
    if hashlib.sha256(landed).hexdigest() != hashlib.sha256(payload).hexdigest():
        report("GUARD: the bytes on disk are not the bytes that were serialized")
        return NONCONFORMANT
    if count_lone_cr(landed) != 0:
        report("GUARD: lone CR present in the file as it landed")
        return NONCONFORMANT
    try:
        reread = json.loads(landed.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        report("GUARD: the file as it landed is not UTF-8 JSON")
        return NONCONFORMANT
    if check_contract(reread) or check_coherence(reread):
        report("GUARD: the file as it landed does not conform")
        return NONCONFORMANT

    report("WROTE %s" % out_path.as_posix())
    report("  bytes=%d sha256=%s crlf=%d lone_cr=%d"
           % (len(landed), hashlib.sha256(landed).hexdigest(),
              count_crlf(landed), count_lone_cr(landed)))
    return OK


# --------------------------------------------------------------------------
# entry
# --------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="gatebraid-capture", add_help=True,
        description="Capture one command execution as gatebraid/evidence-capture@1.")
    parser.add_argument("--out", metavar="PATH",
                        help="where the record is written (binary)")
    parser.add_argument("--capture-id", metavar="ID",
                        help="stable id a gate record's checks[].output_ref points at")
    parser.add_argument("--cwd", metavar="DIR",
                        help="working directory for the captured command")
    parser.add_argument("--cwd-as-supplied", action="store_true",
                        help="record cwd without resolving it (resolution: as-supplied)")
    parser.add_argument("--input", metavar="PATH", action="append", default=[],
                        help="pinned-SHA input, hashed BEFORE the command runs (repeatable)")
    parser.add_argument("--output", metavar="PATH", action="append", default=[],
                        help="file the command wrote, hashed after (repeatable)")
    parser.add_argument("--env", metavar="NAME", action="append", default=[],
                        help="declare one environment variable by name (repeatable, cap %d)"
                             % ENV_MAX_PROPERTIES)
    parser.add_argument("--render-codec", metavar="CODEC", default="utf-8",
                        help="codec for the DERIVED rendering (default utf-8)")
    parser.add_argument("--no-render", action="store_true",
                        help="omit the derived rendering entirely")
    parser.add_argument("--form", choices=FORM_VALUES, default="argv",
                        help="argv (default) or shell; shell requires the three semantics flags")
    parser.add_argument("--shell-exe", metavar="NAME",
                        help="form=shell: the shell that interpreted the string")
    parser.add_argument("--pipefail", choices=("true", "false"),
                        help="form=shell: whether pipefail was in force")
    parser.add_argument("--exit-code-source", choices=EXIT_CODE_SOURCE_VALUES,
                        help="form=shell: what the recorded exit_code measures")
    parser.add_argument("--notes", metavar="TEXT")
    parser.add_argument("--verify-record", metavar="PATH",
                        help="check an existing record with the SAME guard the write path uses")
    parser.add_argument("--rederive", action="store_true",
                        help="--verify-record: also run layer B (re-derivation)")
    parser.add_argument("argv", nargs=argparse.REMAINDER,
                        help="-- COMMAND [ARG...]")
    return parser


def _report(line):
    sys.stdout.write(line + "\n")


def verify_record(path, rederive, report):
    try:
        raw = pathlib.Path(path).read_bytes()
    except OSError:
        raise StructureError("record could not be read")
    try:
        doc = json.loads(raw.decode("utf-8"))
    except UnicodeDecodeError:
        raise StructureError("record is not UTF-8")
    except ValueError:
        raise StructureError("record is not valid JSON")
    contract = check_contract(doc)
    findings = list(contract.items)
    report("contract : %s" % (contract.format() if contract else "conforms"))
    if rederive:
        coherence = check_coherence(doc)
        findings += list(coherence.items)
        report("coherence: %s" % (coherence.format() if coherence else "conforms"))
    lone_cr = count_lone_cr(raw)
    report("bytes=%d crlf=%d lone_cr=%d" % (len(raw), count_crlf(raw), lone_cr))
    return OK if not findings else NONCONFORMANT


def main(argv):
    parser = build_parser()
    args = parser.parse_args(argv[1:])

    command = list(args.argv)
    if command and command[0] == "--":
        command = command[1:]
    args.argv = command

    try:
        if args.verify_record:
            # L1 review finding: --verify-record used to silently ignore a
            # command and an --out given alongside it, so a caller who meant to
            # capture would get a verification and no capture, with exit 0.
            if command or args.out:
                raise StructureError(
                    "--verify-record takes no command and no --out")
            return verify_record(args.verify_record, args.rederive, _report)

        if not command:
            raise StructureError("no command given; use -- COMMAND [ARG...]")
        if not args.out:
            raise StructureError("--out is required")
        if not args.capture_id:
            raise StructureError("--capture-id is required")
        if args.form == "shell":
            missing = [flag for flag, value in
                       (("--shell-exe", args.shell_exe),
                        ("--pipefail", args.pipefail),
                        ("--exit-code-source", args.exit_code_source))
                       if not value]
            if missing:
                # A shell use that does not declare its semantics is an exit
                # code nobody can interpret, so it is refused here as well as
                # by the contract.
                raise StructureError(
                    "form=shell requires " + ", ".join(missing))
        elif args.shell_exe or args.pipefail or args.exit_code_source:
            raise StructureError(
                "form=argv cannot carry shell semantics; no shell was involved")
        if len(args.env) > ENV_MAX_PROPERTIES:
            raise StructureError(
                "declared environment exceeds the contract's cap of %d names"
                % ENV_MAX_PROPERTIES)

        record = capture(args)
        return write_record(record, pathlib.Path(args.out), _report)
    except StructureError as exc:
        sys.stdout.write("STRUCTURE: %s\n" % exc)
        return STRUCTURE


if __name__ == "__main__":
    sys.exit(main(sys.argv))
