#!/usr/bin/env python3
"""Gatebraid direct-drive dispatcher - validate, record, refuse; start nothing unchecked.

CONTRACT. This file implements `protocols/direct-drive-v1.md` ("Direct drive
v1 - the dispatcher contract"), frozen with ADR-0034 by the merge
`6062a21105e890e614ed7a45f589341943c88d6f` and amended by batch DD2. Section 2
gives the file layout and the manifest schema, section 2.2 the run record and
the post-run rule, section 4 the ordered decision procedure `DD-R00`..`DD-R08`,
section 5 what the dispatcher never does, section 6 the kill switch, section 10
fixture mode, print-only mode, the command line, the exit statuses and the
prohibitions this source obeys. Nothing outside that document is authority. A
decision the contract does not name is a refusal: manifest-shape problems are
`DD-R01`, entry-shape problems are `DD-R03`.

DOMAIN. Two repositories, held below as a WHITELIST (`PERMITTED_REPOSITORIES`)
and never matched by pattern. Every other identity is refused without being
named here, which is why this file cannot leak a protected one: it does not
contain one and never learns one.

THE SCANS OF `DD-R05`, over the dispatch file's decoded bytes, in this order.

  (a) Closed set. Owner/name-shaped tokens are extracted with the same pattern
      class the committed sweep
      `docs/evidence/gatebraid/P2-S5/g2/checks-g2-closed-set-sweep.py` uses:

          (?<![A-Za-z0-9_./-])([A-Za-z0-9][A-Za-z0-9_.-]{0,38}/[A-Za-z0-9][A-Za-z0-9_.-]{0,60})

      A token passes only if it is a member of `PERMITTED_REPOSITORIES` or
      falls in one of the residue classes below - each an explicit RULE, none
      of which names a repository outside the set:
        * a leading segment in `PATH_PREFIXES` or `URL_PREFIXES` (a filesystem
          or URL path segment);
        * `repos/...`, an API path fragment;
        * `refs/<lowercase>`, a git ref namespace, `REF_NAMESPACE`;
        * a leading segment in `SCHEMA_NAMESPACE`, a schema id such as this
          contract's own manifest and run schemas;
        * a JSON pointer, `JSON_POINTER` = ^[A-Za-z_][A-Za-z0-9_]*/[0-9]+$;
        * a document citation naming two numbers, `DOC_CITATION` =
          ^ADR-[0-9]{4}/[0-9]{4}$;
        * the literal metasyntax in `METASYNTAX`.
      Anything else is residue and the entry is refused. This is a whitelist
      with named exceptions, not a blacklist.

  (b) The handoff-block schema token, held in `HANDOFF_BLOCK_TOKEN` and
      ASSEMBLED FROM PARTS at import time so the token itself is not among
      this file's bytes - the same device the seeds use through
      `setup.substitutions` (contract section 10).

  (c) A closing keyword immediately preceding an issue reference, as a regular
      expression and never as an example. The precedent instrument is
      `docs/evidence/gatebraid/P2-S2/checks/closing-keyword-scan.py`, whose
      two patterns are carried here unchanged in `CLOSING_KEYWORD` and
      `REFERENCE`: the bare token is not matched, so a conventional-commit
      scope prefix, which references nothing, is correctly not a match.

  (d) CR bytes, counted on the raw bytes before decoding.

  (e) Code points outside `ALLOWED_NON_ASCII`.

  A checker never quotes what it forbids into a record (ADR-0028 section 3):
  every refusal line gives the class, the count and the first line number, and
  never the token, the match or the identity that caused it.

THE POST-RUN RULE (`DD-R08`, contract section 2.2). Porcelain lines are
compared as SETS after normalisation: the two status columns are stripped for
the path comparison, a rename's two sides are both taken, a git-quoted path is
unquoted, and separators are made forward slashes. A read-only kind must leave
`head_after == head_before` and the two lists equal as sets. An evidence kind
must leave HEAD unmoved and every after-line that is not in the before set must
name paths under `docs/evidence/gatebraid/<slice_id>/`. Write kinds are not
checked here; their contracts govern.

HOST FACTS, measured on this host and recorded because the run form depends on
them (contract section 9). The installed executable is Claude Code 2.1.220.

  * `--settings <file-or-json>` - "Path to a settings JSON file or a JSON
    string to load additional settings from". This is the settings-file flag a
    profile is passed with; it is listed in `claude --help`.
  * `--max-turns <turns>` - "Maximum number of agentic turns in non-interactive
    mode. This will early exit the conversation after the specified number of
    turns." Present in the installed executable but NOT listed in
    `claude --help` at this version; the contract names it, so it is passed.
  * A run whose turn budget was exhausted reports the result subtype
    `error_max_turns`, which is how section 2.2's `timeout` outcome is reached
    for the turn limb; the wall-clock limb is `timeout_seconds`, measured here.

PROFILE FILE CONVENTION. The contract names profiles by class and holds their
contents to R-min, which has not landed. This dispatcher resolves the settings
file for a class as `<profiles>/<class>.settings.json` and records its absolute
path and sha256 in every run record. The convention is declared here because
the contract does not fix a filename; the reviewer should read it as such.

WHAT THIS SOURCE DOES NOT CONTAIN (contract section 10): the handoff-block
schema token in literal form; a closing keyword adjacent to an issue reference;
any repository identity outside the closed set; any credential, or any read of
one - `GH_CONFIG_DIR` is a configuration DIRECTORY path passed through from the
operator's environment, not a secret; any permission-bypass flag or any
permission-mode flag; any scheduling. The one `time.sleep` call is the STOP
poll of section 4's run row, which the kill switch of section 6 requires, and
is not a scheduler: this tool runs when the operator starts it and never
otherwise.

MODES (contract section 10). `--fixture <path> [...]` materialises each seed in
a temporary directory, evaluates `DD-R00`..`DD-R07` against it plus the
post-run rule over any declared states, runs nothing, and prints one line per
seed. `--print-only` evaluates a real inbox and prints the command each
admitted entry would run, writing nothing. The bare run form starts the
executor. Exit status is `0`, `1` or `2` as section 10 writes, printed as the
last line in the form `exit <n>`.

Python 3 standard library only. Run it with `-B`.
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

CONTRACT_PATH = "protocols/direct-drive-v1.md"
MANIFEST_SCHEMA = "gatebraid/dispatch-manifest@1"
RUN_SCHEMA = "gatebraid/dispatch-run@1"
FIXTURE_SCHEMA = "gatebraid/dispatch-fixture@1"

# The closed set, as a whitelist. Contract section 5: an identity outside it is
# refused without appearing anywhere in this tool.
PERMITTED_REPOSITORIES = frozenset((
    "MianliWang/gatebraid",
    "MianliWang/gatebraid-scratch",
))

READ_ONLY_KINDS = frozenset(("review", "consult-prep"))
EVIDENCE_KINDS = frozenset(("entry", "gate0", "gate1"))
WRITE_KINDS = frozenset(("gate2", "gate3"))
ALL_KINDS = READ_ONLY_KINDS | EVIDENCE_KINDS | WRITE_KINDS
PROFILE_CLASSES = ("readonly", "evidence", "write")

MANIFEST_KEYS = ("schema", "written_at", "entries")
ENTRY_KEYS_REQUIRED = (
    "name", "sha256", "bytes", "kind", "repository", "cwd", "profile",
    "max_turns", "timeout_seconds",
)
ENTRY_KEYS_OPTIONAL = ("slice_id",)
ENTRY_KEYS = frozenset(ENTRY_KEYS_REQUIRED + ENTRY_KEYS_OPTIONAL)

NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}\.md$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SLICE_ID_RE = re.compile(r"^P[0-9]+-S[0-9]+$")

EVIDENCE_ROOT = "docs/evidence/gatebraid/"

ALLOWED_NON_ASCII = frozenset((0x00A7, 0x00B7, 0x2013, 0x2014, 0x2026, 0x2192))

REPO_TOKEN = re.compile(
    r"(?<![A-Za-z0-9_./-])([A-Za-z0-9][A-Za-z0-9_.-]{0,38}/[A-Za-z0-9][A-Za-z0-9_.-]{0,60})")

# Assembled from parts: the token is not among this file's bytes.
HANDOFF_BLOCK_TOKEN = "".join(("gatebraid/hand", "off@1"))

# Carried unchanged from the P2-S2 instrument named in the docstring.
CLOSING_KEYWORD = r"(?:clos(?:e|es|ed)|fix(?:|es|ed)|resolve(?:|s|d))"
REFERENCE = (r"(?:\#[0-9]+|[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\#[0-9]+"
             r"|https?://[^\s]*issues/[0-9]+)")
CLOSING_BEFORE_REFERENCE = re.compile(
    CLOSING_KEYWORD + r"\s+" + REFERENCE, re.IGNORECASE)

REF_NAMESPACE = re.compile(r"^refs/[a-z]+$")
JSON_POINTER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*/[0-9]+$")
DOC_CITATION = re.compile(r"^ADR-[0-9]{4}/[0-9]{4}$")
METASYNTAX = frozenset(("owner/name", "owner/repo"))
SCHEMA_NAMESPACE = frozenset(("gatebraid",))
PATH_PREFIXES = frozenset((
    "adr", "bin", "captures", "consults", "docs", "evidence", "fixtures",
    "projects", "protocols", "schema", "templates", "_handoff",
    "AppData", "Users", "Program Files", "Github repo", "etc", "lib", "mnt",
    "npm", "tmp", "usr", "var",
))
URL_PREFIXES = frozenset((
    "http:", "https:", "api.github.com", "github.com", "json-schema.org",
))
UNEXPLAINED = "UNEXPLAINED"

# Section 2.2's environment. GH_CONFIG_DIR is a directory path the operator
# provisioned (ADR-0024 section 5); it is passed through, never read for
# content and never copied.
DEFAULT_GH_CONFIG_DIR = "C:/Users/rough/.gh-gatebraid"
DEFAULT_INBOX = "_handoff/inbox"
DEFAULT_OUTBOX = "_handoff/outbox"
DEFAULT_PROFILES = os.path.join(os.path.expanduser("~"), ".gatebraid", "profiles")

# The STOP poll of section 4's run row. Not a scheduler: see the docstring.
STOP_POLL_SECONDS = 0.5
TERMINATE_GRACE_SECONDS = 5.0

EXIT_OK = 0
EXIT_REFUSED = 1
EXIT_USAGE = 2

ALLOW = "allow"


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------

def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def line_of(text, index):
    return text.count("\n", 0, index) + 1


def say(line):
    print(line, flush=True)


class Decision(object):
    """One outcome of the section 4 procedure."""

    def __init__(self, decision, code=None, reason="", scope="entry"):
        self.decision = decision
        self.code = code
        self.reason = reason
        self.scope = scope

    def announce(self):
        """ADR-0028 section 3: never quote what is forbidden into a record."""
        if self.decision == "refuse":
            say("refused %s %s" % (self.code, self.reason))
        elif self.decision == "halt":
            say("halted %s %s" % (self.code, self.reason))
        elif self.decision == "error":
            say("error %s %s" % (self.code, self.reason))


# --------------------------------------------------------------------------
# DD-R05: the scans
# --------------------------------------------------------------------------

def classify_repo_token(token):
    head = token.split("/")[0]
    if token in PERMITTED_REPOSITORIES:
        return "permitted repository"
    if head == "repos":
        return "API path fragment"
    if REF_NAMESPACE.match(token):
        return "git ref namespace"
    if head in PATH_PREFIXES or head in URL_PREFIXES:
        return "filesystem or URL path segment"
    if head in SCHEMA_NAMESPACE:
        return "schema-id namespace"
    if JSON_POINTER.match(token):
        return "JSON pointer"
    if DOC_CITATION.match(token):
        return "document citation naming two numbers"
    if token in METASYNTAX:
        return "literal metasyntax"
    return UNEXPLAINED


def scan_dispatch(raw):
    """Return a list of defused findings. Empty means DD-R05 passes."""
    findings = []
    if b"\r" in raw:
        findings.append("carries %d CR byte(s), first at offset %d"
                        % (raw.count(b"\r"), raw.index(b"\r")))
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        findings.append("is not valid UTF-8 (first bad byte at offset %d)" % exc.start)
        return findings

    residue = [m for m in REPO_TOKEN.finditer(text)
               if classify_repo_token(m.group(1)) == UNEXPLAINED]
    if residue:
        findings.append(
            "names %d owner/name token(s) outside the closed set, first at line %d "
            "(not quoted)" % (len(residue), line_of(text, residue[0].start())))

    if HANDOFF_BLOCK_TOKEN in text:
        findings.append(
            "carries the handoff-block schema token, %d occurrence(s), first at line %d"
            % (text.count(HANDOFF_BLOCK_TOKEN),
               line_of(text, text.index(HANDOFF_BLOCK_TOKEN))))

    closing = list(CLOSING_BEFORE_REFERENCE.finditer(text))
    if closing:
        findings.append(
            "carries a closing keyword immediately before an issue reference, "
            "%d match(es), first at line %d (not quoted)"
            % (len(closing), line_of(text, closing[0].start())))

    outside = [(i, ord(c)) for i, c in enumerate(text)
               if ord(c) > 127 and ord(c) not in ALLOWED_NON_ASCII]
    if outside:
        findings.append(
            "carries %d code point(s) outside the permitted set, first U+%04X at line %d"
            % (len(outside), outside[0][1], line_of(text, outside[0][0])))
    return findings


# --------------------------------------------------------------------------
# DD-R01: manifest and entry shape
# --------------------------------------------------------------------------

def positive_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def non_negative_int(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def check_entry_shape(entry, position):
    where = "entry %d" % position
    if not isinstance(entry, dict):
        return "%s is not a JSON object" % where
    for key in ENTRY_KEYS_REQUIRED:
        if key not in entry:
            return "%s lacks the required key %s" % (where, key)
    extra = sorted(set(entry) - ENTRY_KEYS)
    if extra:
        return "%s carries %d key(s) outside the schema: %s" % (
            where, len(extra), ", ".join(extra))
    for key in ("name", "kind", "repository", "cwd", "profile"):
        if not isinstance(entry[key], str) or not entry[key]:
            return "%s: %s is not a non-empty string" % (where, key)
    if "slice_id" in entry and not isinstance(entry["slice_id"], str):
        return "%s: slice_id is not a string" % where
    if not NAME_RE.match(entry["name"]):
        return "%s: name is not one path segment matching the schema pattern" % where
    if not isinstance(entry["sha256"], str) or not SHA256_RE.match(entry["sha256"]):
        return "%s: sha256 is not 64 lowercase hex characters" % where
    if not non_negative_int(entry["bytes"]):
        return "%s: bytes is not a non-negative integer" % where
    if not positive_int(entry["max_turns"]):
        return "%s: max_turns is not a positive integer" % where
    if not positive_int(entry["timeout_seconds"]):
        return "%s: timeout_seconds is not a positive integer" % where
    return None


def check_manifest_shape(manifest):
    """DD-R01. Returns a reason string, or None when the shape is sound."""
    if not isinstance(manifest, dict):
        return "the manifest is not a JSON object"
    for key in MANIFEST_KEYS:
        if key not in manifest:
            return "the manifest lacks the required key %s" % key
    extra = sorted(set(manifest) - set(MANIFEST_KEYS))
    if extra:
        return "the manifest carries %d key(s) outside the schema: %s" % (
            len(extra), ", ".join(extra))
    if manifest["schema"] != MANIFEST_SCHEMA:
        return "the manifest schema key is not %s" % MANIFEST_SCHEMA
    if not isinstance(manifest["written_at"], str) or not manifest["written_at"]:
        return "written_at is not a non-empty string"
    if not isinstance(manifest["entries"], list):
        return "entries is not a list"
    for position, entry in enumerate(manifest["entries"], 1):
        reason = check_entry_shape(entry, position)
        if reason:
            return reason
    return None


# --------------------------------------------------------------------------
# DD-R04: the repository of a clone
# --------------------------------------------------------------------------

def repository_from_remote_url(url):
    """Reduce a remote URL to owner/name, or None."""
    text = (url or "").strip().replace("\\", "/")
    if text.endswith(".git"):
        text = text[:-4]
    text = text.rstrip("/")
    if "://" in text:
        text = text.split("://", 1)[1]
    head = text.split("/")[0]
    if "@" in head:
        text = text.split("@", 1)[1]
        head = text.split("/")[0]
    if ":" in head:
        text = text.split(":", 1)[1]
    elif "." in head or head == "localhost":
        text = "/".join(text.split("/")[1:])
    segments = [s for s in text.split("/") if s]
    if len(segments) < 2:
        return None
    return "/".join(segments[-2:])


def git_origin(cwd):
    try:
        done = subprocess.run(
            ["git", "-C", str(cwd), "remote", "get-url", "origin"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError as exc:
        return None, "git could not be started (%s)" % exc.__class__.__name__
    if done.returncode != 0:
        return None, "git could not read origin in the entry's cwd"
    return done.stdout.decode("utf-8", "replace").strip(), None


# --------------------------------------------------------------------------
# DD-R08: the post-run rule
# --------------------------------------------------------------------------

def porcelain_paths(line):
    """Strip the two status columns; a rename yields both sides."""
    body = line[3:] if len(line) > 3 else ""
    sides = body.split(" -> ") if " -> " in body else [body]
    paths = []
    for side in sides:
        side = side.strip()
        if len(side) >= 2 and side[0] == '"' and side[-1] == '"':
            side = side[1:-1]
        side = side.replace("\\", "/")
        if side:
            paths.append(side)
    return paths


def porcelain_key(line):
    return (line[:2], tuple(porcelain_paths(line)))


def apply_post_run_rule(kind, slice_id, states):
    head_before = states.get("head_before")
    head_after = states.get("head_after")
    before = list(states.get("porcelain_before") or [])
    after = list(states.get("porcelain_after") or [])

    if kind in WRITE_KINDS:
        return Decision("completed")

    if head_after != head_before:
        return Decision("error", "DD-R08",
                        "HEAD moved during a %s job (head_before != head_after)"
                        % ("read-only" if kind in READ_ONLY_KINDS else "evidence"))

    if kind in READ_ONLY_KINDS:
        before_keys = set(map(porcelain_key, before))
        after_keys = set(map(porcelain_key, after))
        if before_keys != after_keys:
            return Decision("error", "DD-R08",
                            "the working tree changed during a read-only job "
                            "(%d porcelain line(s) differ)"
                            % len(before_keys ^ after_keys))
        return Decision("completed")

    evidence_dir = EVIDENCE_ROOT + slice_id + "/"
    before_keys = set(map(porcelain_key, before))
    offending = []
    for line in after:
        if porcelain_key(line) in before_keys:
            continue
        for path in porcelain_paths(line):
            if not path.startswith(evidence_dir):
                offending.append(path)
    if offending:
        return Decision("error", "DD-R08",
                        "an evidence job changed %d path(s) outside %s: %s"
                        % (len(offending), evidence_dir,
                           ", ".join(sorted(set(offending)))))
    return Decision("completed")


# --------------------------------------------------------------------------
# host resolution (DD-R07)
# --------------------------------------------------------------------------

def resolve_tools():
    """Return (paths, missing). Section 2.2's tool_paths."""
    paths = {}
    missing = []
    for tool in ("claude", "git", "gh", "python"):
        found = shutil.which(tool)
        paths[tool] = found
        if not found:
            missing.append(tool)
    return paths, missing


def claude_version(executable):
    try:
        done = subprocess.run([executable, "--version"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        return None
    if done.returncode != 0:
        return None
    return done.stdout.decode("utf-8", "replace").strip() or None


def profile_file(profiles_dir, profile_class):
    return Path(profiles_dir) / ("%s.settings.json" % profile_class)


def profile_class_for(kind):
    if kind in READ_ONLY_KINDS:
        return "readonly"
    if kind in EVIDENCE_KINDS:
        return "evidence"
    return "write"


# --------------------------------------------------------------------------
# the ordered procedure of section 4
# --------------------------------------------------------------------------

def evaluate_manifest_level(inbox):
    """DD-R00, DD-R01 and the manifest-level half of DD-R02, in that order."""
    inbox = Path(inbox)
    if (inbox / "STOP").exists():
        return Decision("halt", "DD-R00",
                        "the STOP file is present in the inbox",
                        scope="manifest"), None

    manifest_path = inbox / "MANIFEST.json"
    if not manifest_path.is_file():
        return Decision("refuse", "DD-R01",
                        "MANIFEST.json is absent from the inbox",
                        scope="manifest"), None
    raw = manifest_path.read_bytes()
    try:
        manifest = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return Decision("refuse", "DD-R01",
                        "MANIFEST.json does not parse as UTF-8 JSON",
                        scope="manifest"), None

    reason = check_manifest_shape(manifest)
    if reason:
        return Decision("refuse", "DD-R01", reason, scope="manifest"), manifest

    # DD-R02, manifest-level half: once per manifest, before any entry.
    present = sorted(p.name for p in inbox.iterdir()
                     if p.is_file()
                     and p.name not in ("MANIFEST.json", "STOP", "RUNNING"))
    counts = {}
    for entry in manifest["entries"]:
        counts[entry["name"]] = counts.get(entry["name"], 0) + 1
    for name in present:
        seen = counts.get(name, 0)
        if seen == 0:
            return Decision("refuse", "DD-R02",
                            "an inbox file is named by no entry: %s" % name,
                            scope="manifest"), manifest
        if seen > 1:
            return Decision("refuse", "DD-R02",
                            "an inbox file is named by %d entries: %s" % (seen, name),
                            scope="manifest"), manifest
    return None, manifest


def evaluate_entry(entry, position, inbox, profiles_dir, host):
    """DD-R02 (entry half) through DD-R07, stopping at the first failure."""
    inbox = Path(inbox)
    where = "entry %d" % position

    # DD-R02, entry half.
    path = inbox / entry["name"]
    if not path.is_file():
        return Decision("refuse", "DD-R02",
                        "%s: the named file is absent from the inbox: %s"
                        % (where, entry["name"])), None
    raw = path.read_bytes()
    if len(raw) != entry["bytes"]:
        return Decision("refuse", "DD-R02",
                        "%s: the file's byte count differs from the manifest "
                        "(%d on disk, %d declared)"
                        % (where, len(raw), entry["bytes"])), None
    if sha256_hex(raw) != entry["sha256"]:
        return Decision("refuse", "DD-R02",
                        "%s: the file's sha256 differs from the manifest" % where), None

    # DD-R03.
    kind = entry["kind"]
    if kind not in ALL_KINDS:
        return Decision("refuse", "DD-R03",
                        "%s: kind is outside the enumeration" % where), None
    expected_profile = profile_class_for(kind)
    if entry["profile"] != expected_profile:
        return Decision("refuse", "DD-R03",
                        "%s: profile does not match the kind's class "
                        "(the class requires %s)" % (where, expected_profile)), None
    needs_slice = kind in EVIDENCE_KINDS or kind in WRITE_KINDS
    has_slice = "slice_id" in entry
    if needs_slice and not has_slice:
        return Decision("refuse", "DD-R03",
                        "%s: slice_id is absent for a kind that requires it"
                        % where), None
    if has_slice and not needs_slice:
        return Decision("refuse", "DD-R03",
                        "%s: slice_id is present for a read-only kind" % where), None
    if has_slice and not SLICE_ID_RE.match(entry["slice_id"]):
        return Decision("refuse", "DD-R03",
                        "%s: slice_id does not match its pattern" % where), None

    # DD-R04.
    if entry["repository"] not in PERMITTED_REPOSITORIES:
        return Decision("refuse", "DD-R04",
                        "%s: the entry's repository is outside the closed set "
                        "(the identifier is not quoted)" % where), None
    url, failure = git_origin(entry["cwd"])
    if failure:
        return Decision("refuse", "DD-R04", "%s: %s" % (where, failure)), None
    if repository_from_remote_url(url) != entry["repository"]:
        return Decision("refuse", "DD-R04",
                        "%s: the cwd's origin does not name the entry's repository"
                        % where), None

    # DD-R05.
    findings = scan_dispatch(raw)
    if findings:
        return Decision("refuse", "DD-R05",
                        "%s: the dispatch text %s"
                        % (where, "; ".join(findings))), None

    # DD-R06.
    if (inbox / "RUNNING").exists():
        return Decision("refuse", "DD-R06",
                        "%s: a job is running (the RUNNING lock is present)"
                        % where), None

    # DD-R07.
    settings = profile_file(profiles_dir, entry["profile"])
    if not settings.is_file():
        return Decision("refuse", "DD-R07",
                        "%s: the settings profile for the entry's class is absent: %s"
                        % (where, settings.name)), None
    profile_bytes = settings.read_bytes()
    if host["missing"]:
        return Decision("refuse", "DD-R07",
                        "%s: %d host tool(s) do not resolve: %s"
                        % (where, len(host["missing"]),
                           ", ".join(host["missing"]))), None
    if not host["claude_version"]:
        return Decision("refuse", "DD-R07",
                        "%s: the claude executable does not report a version"
                        % where), None

    admitted = {
        "raw": raw,
        "profile_path": str(settings.resolve()),
        "profile_sha256": sha256_hex(profile_bytes),
    }
    return Decision(ALLOW), admitted


# --------------------------------------------------------------------------
# fixture mode
# --------------------------------------------------------------------------

def materialise_seed(seed, root):
    """Build the temporary inbox and profile directory the seed declares."""
    root = Path(root)
    inbox = root / "inbox"
    profiles = root / "profiles"
    inbox.mkdir(parents=True)
    profiles.mkdir(parents=True)

    setup = seed.get("setup") or {}
    manifest = json.loads(json.dumps(setup.get("manifest")))
    files = dict(setup.get("files") or {})

    # Section 10: join the parts, replace the placeholder in every inline body,
    # and recompute each AFFECTED entry's sha256 and bytes BEFORE DD-R02.
    changed = set()
    for placeholder, parts in (setup.get("substitutions") or {}).items():
        joined = "".join(parts)
        for name in list(files):
            if placeholder in files[name]:
                files[name] = files[name].replace(placeholder, joined)
                changed.add(name)
    if changed and isinstance(manifest, dict) and isinstance(manifest.get("entries"), list):
        for entry in manifest["entries"]:
            if isinstance(entry, dict) and entry.get("name") in changed:
                body = files[entry["name"]].encode("utf-8")
                entry["sha256"] = sha256_hex(body)
                entry["bytes"] = len(body)

    for name, body in files.items():
        (inbox / name).write_bytes(body.encode("utf-8"))
    (inbox / "MANIFEST.json").write_bytes(
        (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    if setup.get("stop_present"):
        (inbox / "STOP").write_bytes(b"")
    if setup.get("running_present"):
        (inbox / "RUNNING").write_bytes(b"")

    host_stub = setup.get("host") or {}
    if host_stub.get("profile_present", True):
        for profile_class in PROFILE_CLASSES:
            profile_file(profiles, profile_class).write_bytes(
                b'{"gatebraid_fixture_profile_stub": true}\n')
    return inbox, profiles


def evaluate_seed(seed, host):
    """Return the Decision fixture mode reaches for one seed."""
    root = tempfile.mkdtemp(prefix="gatebraid-dispatch-fixture-")
    try:
        inbox, profiles = materialise_seed(seed, root)
        decision, manifest = evaluate_manifest_level(inbox)
        if decision is not None:
            return decision
        admitted_entry = None
        for position, entry in enumerate(manifest["entries"], 1):
            decision, _admitted = evaluate_entry(entry, position, inbox, profiles, host)
            if decision.decision != ALLOW:
                return decision
            if admitted_entry is None:
                admitted_entry = entry
        post_run = (seed.get("setup") or {}).get("post_run")
        if post_run and admitted_entry is not None:
            return apply_post_run_rule(admitted_entry["kind"],
                                       admitted_entry.get("slice_id"), post_run)
        return Decision(ALLOW)
    finally:
        shutil.rmtree(root, ignore_errors=True)


def render(decision, code):
    return "%s/%s" % (decision, code if code else "null")


def fixture_mode(paths, host):
    mismatches = 0
    for raw_path in paths:
        path = Path(raw_path)
        try:
            seed = json.loads(path.read_bytes().decode("utf-8"))
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            say("cannot read seed %s (%s)" % (raw_path, exc.__class__.__name__))
            return EXIT_USAGE
        if not isinstance(seed, dict) or seed.get("schema") != FIXTURE_SCHEMA:
            say("seed %s is not %s" % (raw_path, FIXTURE_SCHEMA))
            return EXIT_USAGE
        seed_id = seed.get("id") or path.stem
        expected = seed.get("expected") or {}
        got = evaluate_seed(seed, host)
        got.announce()
        matched = (got.decision == expected.get("decision")
                   and (got.code or None) == (expected.get("code") or None))
        if not matched:
            mismatches += 1
        say("%s expected %s got %s -> %s"
            % (seed_id,
               render(expected.get("decision"), expected.get("code")),
               render(got.decision, got.code),
               "MATCH" if matched else "MISMATCH"))
    return EXIT_OK if mismatches == 0 else EXIT_REFUSED


# --------------------------------------------------------------------------
# the run form and print-only mode
# --------------------------------------------------------------------------

def build_command(entry, prompt, profile_path):
    """Section 4's run row and section 2.2's command field."""
    return [
        "claude", "-p", prompt,
        "--output-format", "json",
        "--max-turns", str(entry["max_turns"]),
        "--settings", profile_path,
    ]


def run_environment():
    env = os.environ.copy()
    env["GH_CONFIG_DIR"] = os.environ.get("GH_CONFIG_DIR", DEFAULT_GH_CONFIG_DIR)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def declared_environment(env):
    return {"GH_CONFIG_DIR": env["GH_CONFIG_DIR"],
            "PYTHONDONTWRITEBYTECODE": env["PYTHONDONTWRITEBYTECODE"]}


def git_head(cwd):
    try:
        done = subprocess.run(["git", "-C", str(cwd), "rev-parse", "HEAD"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        return None
    if done.returncode != 0:
        return None
    return done.stdout.decode("utf-8", "replace").strip()


def git_porcelain(cwd):
    try:
        done = subprocess.run(
            ["git", "-C", str(cwd), "status", "--porcelain", "--untracked-files=all"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        return None
    if done.returncode != 0:
        return None
    text = done.stdout.decode("utf-8", "replace")
    return [line for line in text.split("\n") if line]


def stop_the_job(process):
    """Section 6: after a halt the job's process must be gone."""
    try:
        process.terminate()
        process.wait(timeout=TERMINATE_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        process.kill()
        try:
            process.wait(timeout=TERMINATE_GRACE_SECONDS)
        except subprocess.TimeoutExpired:
            pass
    except OSError:
        pass


def outcome_from_output(stdout_bytes, exit_status):
    """Section 2.2: a turn budget exhausted is recorded as timeout."""
    if exit_status == 0:
        return "completed"
    try:
        payload = json.loads(stdout_bytes.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return "error"
    if isinstance(payload, dict) and payload.get("subtype") == "error_max_turns":
        return "timeout"
    return "error"


def dispatcher_version():
    try:
        return sha256_hex(Path(__file__).read_bytes())
    except OSError:
        return None


def run_record(name, entry, manifest_sha, admitted, started_at, ended_at,
               outcome, refusal, extras):
    """Section 2.2's gatebraid/dispatch-run@1."""
    entry = entry or {}
    kind = entry.get("kind")
    slice_id = entry.get("slice_id")
    evidence_dir = None
    if kind in EVIDENCE_KINDS and slice_id:
        evidence_dir = EVIDENCE_ROOT + slice_id + "/"
    record = {
        "schema": RUN_SCHEMA,
        "name": name,
        "dispatch_sha256": sha256_hex(admitted["raw"]) if admitted else None,
        "manifest_sha256": manifest_sha,
        "profile_path": admitted["profile_path"] if admitted else None,
        "profile_sha256": admitted["profile_sha256"] if admitted else None,
        "kind": kind,
        "repository": entry.get("repository"),
        "cwd": entry.get("cwd"),
        "slice_id": slice_id if kind in (EVIDENCE_KINDS | WRITE_KINDS) else None,
        "evidence_dir": evidence_dir,
        "head_before": None,
        "head_after": None,
        "porcelain_before": None,
        "porcelain_after": None,
        "started_at": started_at,
        "ended_at": ended_at,
        "outcome": outcome,
        "refusal": refusal,
        "exit_status": None,
        "command": None,
        "environment": None,
        "stdout_sha256": None,
        "stderr_sha256": None,
        "claude_version": None,
        "tool_paths": None,
        "dispatcher_version": dispatcher_version(),
    }
    record.update(extras or {})
    return record


def write_record(outbox, filename, record):
    outbox = Path(outbox)
    outbox.mkdir(parents=True, exist_ok=True)
    target = outbox / filename
    payload = (json.dumps(record, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    target.write_bytes(payload)
    return target


def execute_entry(entry, inbox, outbox, admitted, manifest_sha, host):
    """Section 4's run row, then DD-R08, then the record. RUNNING brackets it."""
    running = Path(inbox) / "RUNNING"
    prompt = admitted["raw"].decode("utf-8")
    command = build_command(entry, prompt, admitted["profile_path"])
    env = run_environment()
    started_at = utc_now()
    Path(outbox).mkdir(parents=True, exist_ok=True)
    stdout_path = Path(outbox) / ("%s.stdout" % entry["name"])
    stderr_path = Path(outbox) / ("%s.stderr" % entry["name"])
    running.write_bytes(("%s %s\n" % (started_at, entry["name"])).encode("utf-8"))

    head_before = git_head(entry["cwd"])
    porcelain_before = git_porcelain(entry["cwd"])
    outcome = "completed"
    refusal = None
    exit_status = None
    stdout_bytes = b""
    stderr_bytes = b""
    try:
        # The streams are captured to files as bytes, unmodified; the loop below
        # is section 4's poll of the STOP file and the wall clock between reads.
        with open(stdout_path, "wb") as out_handle, open(stderr_path, "wb") as err_handle:
            process = subprocess.Popen(command, cwd=entry["cwd"], env=env,
                                       stdout=out_handle, stderr=err_handle)
            deadline = time.monotonic() + entry["timeout_seconds"]
            while True:
                exit_status = process.poll()
                if exit_status is not None:
                    break
                if (Path(inbox) / "STOP").exists():
                    stop_the_job(process)
                    outcome, refusal = "halted", "DD-R00"
                    exit_status = process.poll()
                    break
                if time.monotonic() > deadline:
                    stop_the_job(process)
                    outcome = "timeout"
                    exit_status = process.poll()
                    break
                time.sleep(STOP_POLL_SECONDS)
        stdout_bytes = stdout_path.read_bytes()
        stderr_bytes = stderr_path.read_bytes()
        if outcome == "completed":
            outcome = outcome_from_output(stdout_bytes, exit_status)
        head_after = git_head(entry["cwd"])
        porcelain_after = git_porcelain(entry["cwd"])
        if outcome == "completed":
            verdict = apply_post_run_rule(
                entry["kind"], entry.get("slice_id"),
                {"head_before": head_before, "head_after": head_after,
                 "porcelain_before": porcelain_before or [],
                 "porcelain_after": porcelain_after or []})
            if verdict.decision == "error":
                outcome, refusal = "error", verdict.code
                verdict.announce()
    finally:
        if running.exists():
            running.unlink()

    record = run_record(
        entry["name"], entry, manifest_sha, admitted, started_at, utc_now(),
        outcome, refusal,
        {"head_before": head_before, "head_after": head_after,
         "porcelain_before": porcelain_before, "porcelain_after": porcelain_after,
         "exit_status": exit_status, "command": command,
         "environment": declared_environment(env),
         "stdout_sha256": sha256_hex(stdout_bytes),
         "stderr_sha256": sha256_hex(stderr_bytes),
         "claude_version": host["claude_version"], "tool_paths": host["paths"]})
    write_record(outbox, "%s.run.json" % entry["name"], record)
    say("%s outcome %s" % (entry["name"], outcome))
    return outcome


def real_inbox_mode(args, host, print_only):
    inbox, profiles, outbox = args.inbox, args.profiles, args.outbox
    if not Path(inbox).is_dir():
        say("the inbox directory does not exist: %s" % inbox)
        return EXIT_USAGE

    manifest_path = Path(inbox) / "MANIFEST.json"
    manifest_sha = (sha256_hex(manifest_path.read_bytes())
                    if manifest_path.is_file() else None)
    started_at = utc_now()
    decision, manifest = evaluate_manifest_level(inbox)
    if decision is not None:
        decision.announce()
        if not print_only:
            written_at = (manifest or {}).get("written_at") or started_at
            record = run_record("MANIFEST.json", None, manifest_sha, None,
                                started_at, utc_now(),
                                "halted" if decision.decision == "halt" else "refused",
                                decision.code, {})
            filename = "MANIFEST.%s.run.json" % written_at
            try:
                write_record(outbox, filename, record)
            except OSError as exc:
                say("the whole-manifest record section 2.2 names could not be "
                    "written as %s (%s); no substitute name is invented for it"
                    % (filename, exc.__class__.__name__))
                return EXIT_USAGE
        return EXIT_REFUSED

    status = EXIT_OK
    for position, entry in enumerate(manifest["entries"], 1):
        verdict, admitted = evaluate_entry(entry, position, inbox, profiles, host)
        if verdict.decision != ALLOW:
            verdict.announce()
            status = EXIT_REFUSED
            if not print_only:
                record = run_record(entry["name"], entry, manifest_sha, None,
                                    utc_now(), utc_now(), "refused", verdict.code, {})
                write_record(outbox, "%s.run.json" % entry["name"], record)
            break
        if print_only:
            say(json.dumps(build_command(entry, admitted["raw"].decode("utf-8"),
                                         admitted["profile_path"])))
            continue
        outcome = execute_entry(entry, inbox, outbox, admitted, manifest_sha, host)
        if outcome != "completed":
            status = EXIT_REFUSED
            break
        if (Path(inbox) / "STOP").exists():
            say("halted DD-R00 the STOP file appeared between entries")
            status = EXIT_REFUSED
            break
    return status


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="gatebraid-dispatch",
        description="Gatebraid direct-drive dispatcher (%s)." % CONTRACT_PATH)
    parser.add_argument("--fixture", nargs="+", metavar="PATH",
                        help="evaluate seeds in a temporary directory and run nothing")
    parser.add_argument("--print-only", action="store_true", dest="print_only",
                        help="evaluate the real inbox and print commands; write nothing")
    parser.add_argument("--inbox", default=DEFAULT_INBOX)
    parser.add_argument("--outbox", default=DEFAULT_OUTBOX)
    parser.add_argument("--profiles", default=DEFAULT_PROFILES)
    return parser


def main(argv):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.fixture and args.print_only:
        say("fixture mode and print-only mode are exclusive")
        return EXIT_USAGE

    paths, missing = resolve_tools()
    host = {"paths": paths, "missing": missing,
            "claude_version": claude_version(paths["claude"]) if paths["claude"] else None}

    if args.fixture:
        return fixture_mode(args.fixture, host)
    return real_inbox_mode(args, host, args.print_only)


# Emit LF, not the platform line ending: this output is captured and hashed as
# evidence, and Windows newline translation would put CRLF into those bytes.
try:
    sys.stdout.reconfigure(newline=chr(10))
except AttributeError:  # pragma: no cover - Python < 3.7
    pass

if __name__ == "__main__":
    try:
        STATUS = main(sys.argv[1:])
    except OSError as error:
        say("an I/O failure stopped the dispatcher (%s)" % error.__class__.__name__)
        STATUS = EXIT_USAGE
    say("exit %d" % STATUS)
    sys.exit(STATUS)
