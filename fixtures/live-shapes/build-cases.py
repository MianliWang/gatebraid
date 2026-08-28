"""Derive every live-shapes case file from the committed provenance records.

Run from the repository root:

    python -B fixtures/live-shapes/build-cases.py [--check]

`--check` rebuilds into memory and compares against what is on disk, changing
nothing; without it the case files are written. Either way the derivation is
reproducible FROM THE COMMITTED TREE ALONE: this script reads
`fixtures/live-shapes/provenance/`, never the executor's working directory, so a
reviewer can re-derive every case without any uncommitted input.

THE VERIFICATION THAT MATTERS runs before any body is used. Each provenance file
is a self-sealed `gatebraid/evidence-capture@1` record carrying its captured
stdout as base64 together with that stream's own `sha256` and `byte_length`. The
body is decoded, re-hashed, and compared against the record's recorded values;
a mismatch aborts rather than writing anything. The corpus therefore cannot
contain a body that its own provenance does not vouch for.

Seven cases are the captured bodies VERBATIM — the exact bytes GitHub returned,
not a re-serialisation. Two are MUTATIONS, and those necessarily pass through
parse/serialise because they are transformations; each is asserted here to equal
its base with exactly the named change applied and nothing else, so the
re-serialisation cannot smuggle a second difference in.

Two cases carry no file of their own: LS-M1 and LS-M4 reuse the bulk-list body
UNCHANGED and differ from LS-04 only in which schema they are declared against.
That is the assertion — the same bytes are lawful as an issue list and unlawful
as an item-list envelope or a dependency list — so giving them private copies
would weaken it into three documents that merely resemble each other.
"""
import base64
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROV = os.path.join(HERE, "provenance")

# capture id -> (case file for its verbatim body, or None if unused directly)
VERBATIM = [
    ("LIVE-item-list-full", "ls01-item-list-full.json"),
    ("LIVE-item-list-limit2", "ls02-item-list-short-read.json"),
    ("LIVE-issue-17-object", "ls03-issue-object.json"),
    ("LIVE-issues-bulk", "ls04-issue-list-bulk.json"),
    ("LIVE-dep-17-blocked-by", "ls05-dependency-list-four-edges.json"),
    ("LIVE-dep-17-blocking", "ls06-dependency-list-empty.json"),
    ("LIVE-dep-14-blocking", "ls07-dependency-list-one-edge.json"),
]

CHECK = "--check" in sys.argv[1:]


def fail(msg):
    print("ABORT: %s" % msg)
    sys.exit(2)


def body_of(capture_id):
    """Return the captured stdout bytes, verified against the record's own seal."""
    path = os.path.join(PROV, capture_id + ".json")
    if not os.path.exists(path):
        fail("provenance record missing: %s" % path)
    rec = json.loads(open(path, "rb").read().decode("utf-8"))
    if rec.get("schema") != "gatebraid/evidence-capture@1":
        fail("%s is not a gatebraid/evidence-capture@1 record" % capture_id)
    stream = rec["streams"]["stdout"]
    raw = base64.b64decode(stream["data"])
    got = hashlib.sha256(raw).hexdigest()
    if got != stream["sha256"]:
        fail("%s stdout sha256 mismatch: recorded %s, re-derived %s"
             % (capture_id, stream["sha256"], got))
    if len(raw) != stream["byte_length"]:
        fail("%s stdout byte_length mismatch: recorded %d, measured %d"
             % (capture_id, stream["byte_length"], len(raw)))
    try:
        raw.decode("utf-8")
    except UnicodeDecodeError as e:
        fail("%s stdout is not strict UTF-8: %s" % (capture_id, e))
    return raw


def emit(name, data: bytes):
    path = os.path.join(HERE, name)
    if CHECK:
        if not os.path.exists(path):
            fail("case file absent: %s" % name)
        on_disk = open(path, "rb").read()
        status = "MATCHES" if on_disk == data else "DIFFERS"
        print("  %-44s %s" % (name, status))
        return on_disk == data
    open(path, "wb").write(data)
    print("  %-44s %d bytes  sha256 %s"
          % (name, len(data), hashlib.sha256(data).hexdigest()))
    return True


def serialise(obj) -> bytes:
    return (json.dumps(obj, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


print("provenance : %s" % PROV.replace("\\", "/"))
print("mode       : %s" % ("check (writes nothing)" if CHECK else "build"))
print()

ok = True

print("verbatim bodies (the exact bytes GitHub returned):")
bodies = {}
for capture_id, case_file in VERBATIM:
    raw = body_of(capture_id)
    bodies[capture_id] = raw
    ok = emit(case_file, raw) and ok

print()
print("mutations (each = its base with exactly the named change):")

# LS-M2 - the item-list envelope with `totalCount` deleted.
base = json.loads(bodies["LIVE-item-list-full"].decode("utf-8"))
m2 = json.loads(bodies["LIVE-item-list-full"].decode("utf-8"))
del m2["totalCount"]
if set(base) - set(m2) != {"totalCount"} or m2["items"] != base["items"]:
    fail("LS-M2 transformation changed something other than removing totalCount")
ok = emit("lsm2-item-list-totalcount-deleted.json", serialise(m2)) and ok

# LS-M3 - the first element carrying `workflow`, with that value retyped to a
# number. The index is derived, not chosen, so the mutation is reproducible.
m3 = json.loads(bodies["LIVE-item-list-full"].decode("utf-8"))
idx = next((i for i, e in enumerate(m3["items"]) if "workflow" in e), None)
if idx is None:
    fail("LS-M3 cannot be built: no element carries `workflow`")
m3["items"][idx]["workflow"] = 0
diffs = [i for i, (a, b) in enumerate(zip(base["items"], m3["items"])) if a != b]
if diffs != [idx] or m3["totalCount"] != base["totalCount"]:
    fail("LS-M3 transformation touched more than one element")
print("  (LS-M3 target element index %d, derived as the first carrying `workflow`)"
      % idx)
ok = emit("lsm3-item-list-workflow-retyped.json", serialise(m3)) and ok

print()
if not ok:
    print("CASES DIFFER FROM THE COMMITTED FILES")
    sys.exit(1)
print("CASES OK: every body verified against its provenance record's own seal")
