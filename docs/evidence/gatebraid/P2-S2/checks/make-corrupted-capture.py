#!/usr/bin/env python3
"""Build the deliberately corrupted N2 output that T5 requires N3 to reject.

M3-PLAN.md §2 N3's Accept-when includes "a deliberately corrupted N2 output is
rejected".  This script produces that input from a COMMITTED P2-S1 capture,
which is N2's record (data, admissible) and not N2's implementation.

THE CORRUPTION IS CHOSEN SO THE SCHEMA ALONE CANNOT CATCH IT.  One byte of the
decoded stdout payload is changed and the payload re-encoded, while the declared
`sha256` and `byte_length` are left exactly as N2 wrote them.  The result still
satisfies every keyword in `gatebraid/evidence-capture@1` - the base64 grammar,
the digest pattern, the integer minimum - so a validator that only checks shape
accepts it.  It is caught only by re-deriving the digest from the bytes, which is
the duty the schema names as belonging to the independent validator.

The committed original is opened read-only and never written.
Python 3 standard library only.  Usage:
    python make-corrupted-capture.py <source-capture> <output-path>
"""
import base64
import hashlib
import json
import sys


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    src, out = argv[1], argv[2]

    with open(src, "rb") as fh:
        original = fh.read()
    doc = json.loads(original.decode("utf-8"))

    stream = doc["streams"]["stdout"]
    raw = base64.b64decode(stream["data"], validate=True)
    if not raw:
        print("STRUCTURE: the source capture has an empty stdout; choose another")
        return 2

    declared_sha = stream["sha256"]
    declared_len = stream["byte_length"]

    # Flip one byte, preserving length so byte_length still matches and the ONLY
    # broken relation is the digest. A single-locus corruption makes the rejection
    # unambiguous about what it caught.
    mutated = bytearray(raw)
    mutated[0] = (mutated[0] + 1) % 256
    stream["data"] = base64.b64encode(bytes(mutated)).decode("ascii")
    # sha256 and byte_length deliberately left as N2 declared them.
    doc["capture_id"] = doc.get("capture_id", "capture") + "-corrupted"
    doc["notes"] = ("DELIBERATELY CORRUPTED INPUT for M3-PLAN §2 N3's "
                    "corrupted-output rejection item. One byte of the stdout payload "
                    "was changed while the declared sha256 and byte_length were left "
                    "untouched, so the document remains schema-valid and is caught "
                    "only by re-derivation. Not evidence of any real command run.")

    text = json.dumps(doc, ensure_ascii=False, indent=1) + "\n"
    data = text.encode("utf-8")
    if b"\r" in data:
        print("STRUCTURE: refusing to write a record containing CR")
        return 2
    with open(out, "wb") as fh:
        fh.write(data)

    # Prove the corruption is real and that the source was not touched.
    still = open(src, "rb").read()
    print("source            : %s" % src)
    print("source unmodified : %s" % (still == original))
    print("declared sha256   : %s" % declared_sha)
    print("actual  sha256    : %s" % hashlib.sha256(bytes(mutated)).hexdigest())
    print("digest re-derives : %s" % (hashlib.sha256(bytes(mutated)).hexdigest() == declared_sha))
    print("declared length   : %d" % declared_len)
    print("actual  length    : %d" % len(mutated))
    print("length preserved  : %s" % (len(mutated) == declared_len))
    print("wrote             : %s  bytes=%d sha256=%s"
          % (out, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
