#!/usr/bin/env python3
"""Validate gate evidence records against the frozen gatebraid/gate-run@2 schema.

Deliberately INDEPENDENT of `bin/gatebraid-validate.py`, this Slice's own
delivered validator. A record marked `bootstrap_exception: true` claims NO N3
independent validation -- N2's and N3's own gate landings are re-validated with
the landed validator only AFTER N3's Gate 3 -- so using N3's validator to bless
N3's own gate records would be exactly the circularity the exception exists to
name. This checker reaches the schema through `jsonschema` directly and names
its loader in the output.

For each file it reports: the declared schema id, the gate number, the result,
the number of `checks[]` rows, any row lacking an `output_ref`, any `output_ref`
naming a repository path that does not exist, and the schema error count with
every message printed.

Exit 0 = every record conforms and every anchor resolves. Exit 1 = otherwise.
"""
import io
import json
import os
import sys

import yaml
import jsonschema
from jsonschema import Draft202012Validator

SCHEMA = "schema/gate-run-v2.schema.json"
FENCE = "`" * 3


def extract_block(path):
    """The fenced yaml block under the `## gatebraid-metadata` heading."""
    text = io.open(path, encoding="utf-8").read()
    if path.endswith(".json"):
        return json.loads(text)
    tail = text.split("## gatebraid-metadata")[1]
    return yaml.safe_load(tail.split(FENCE + "yaml")[1].split(FENCE)[0])


def main(paths):
    import importlib.metadata as md
    loader = "PyYAML %s / jsonschema %s / Draft202012Validator" % (yaml.__version__, md.version("jsonschema"))
    schema = json.load(io.open(SCHEMA, encoding="utf-8"))
    validator = Draft202012Validator(schema)

    print("schema: %s" % SCHEMA)
    print("loader: %s" % loader)
    bad = 0
    for p in paths:
        doc = extract_block(p)
        errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
        no_ref = [c["name"] for c in doc.get("checks", []) if not c.get("output_ref")]
        missing = [c["output_ref"] for c in doc.get("checks", [])
                   if str(c.get("output_ref", "")).startswith("docs/") and not os.path.exists(c["output_ref"])]
        ok = not errors and not no_ref and not missing
        bad += 0 if ok else 1
        print("%-46s schema=%-22s gate=%s result=%-14s checks=%-3s %s"
              % (p, doc.get("schema"), doc.get("gate"), doc.get("result"),
                 len(doc.get("checks", [])), "conforms" if ok else "NON-CONFORMING"))
        for e in errors:
            print("    schema error: %s" % e.message)
        for n in no_ref:
            print("    checks[] row without output_ref: %s" % n)
        for m in missing:
            print("    output_ref names a path that does not exist: %s" % m)
    print("records validated: %d  non-conforming: %d" % (len(paths), bad))
    return 1 if bad else 0


# Emit LF, not the platform line ending: this output is transcribed into a gate
# record that is committed under .gitattributes `* text=auto eol=lf`, and Windows
# newline translation would put CRLF into evidence bytes that are hashed.
try:
    sys.stdout.reconfigure(newline=chr(10))
except AttributeError:  # pragma: no cover - Python < 3.7
    pass


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
