#!/usr/bin/env python3
"""K2b — every gate record validates against the committed gatebraid/gate-run@2.

Discharges the second conjunct of plan task K2. Nothing in the Gate 2 record
discharged it: the landed generator's contract is `gatebraid/evidence-capture@1`
and it has no gate-run mode, so it could not have produced this row. This
script is that row's generator.

The loader is NAMED in the output rather than assumed, because "validated"
without a validator is the mute class ADR-0028 exists against: a run that
never performed the check must not be able to report itself clean.

`gate0.json` is a JSON record. `gate1.md` and `gate2.md` carry their record in
the fenced YAML block under `## gatebraid-metadata`; that block is extracted
and validated as the record it is.

Usage:  python3 k2b_gate_records.py <record> [<record> ...]
Exit 0 when every record conforms, 1 otherwise, 3 when no loader is present
(never 0 -- an absent validator is not a pass).
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

SCHEMA = Path("schema/gate-run-v2.schema.json")
BLOCK = re.compile(r"^## gatebraid-metadata\s*\n+```yaml\n(.*?)\n```", re.S | re.M)


def load_record(path: Path):
    if path.suffix == ".json":
        return json.load(io.open(path, encoding="utf-8"))
    text = io.open(path, encoding="utf-8").read()
    m = BLOCK.search(text)
    if not m:
        raise ValueError("no gatebraid-metadata yaml block in %s" % path.as_posix())
    import yaml  # guarded: only markdown records need it
    return yaml.safe_load(m.group(1))


def main(argv: list[str]) -> int:
    records = [Path(a) for a in argv[1:]]
    if not records:
        print("usage: k2b_gate_records.py <record> [<record> ...]", file=sys.stderr)
        return 2

    try:
        import jsonschema
        from jsonschema import Draft202012Validator as Validator
    except ImportError:
        # exit 3, never 0: a run that could not check must not look clean.
        print("schema validation: ABSENT -- no jsonschema loader present")
        return 3

    from importlib.metadata import version
    schema = json.load(io.open(SCHEMA, encoding="utf-8"))
    print("schema: %s" % SCHEMA.as_posix())
    print("loader: jsonschema %s, %s" % (version("jsonschema"), Validator.__name__))

    failures = 0
    for path in records:
        doc = load_record(path)
        errors = sorted(Validator(schema).iter_errors(doc), key=lambda e: list(e.path))
        verdict = "conforms" if not errors else "%d error(s)" % len(errors)
        print("%-52s schema=%-22s gate=%s result=%-14s %s"
              % (path.as_posix(), doc.get("schema"), doc.get("gate"),
                 doc.get("result"), verdict))
        for e in errors[:6]:
            print("      at %s: %s" % (list(e.path), e.message[:160]))
            failures += 1
        if errors:
            failures += 1

    print("records validated: %d  non-conforming: %d" % (len(records), failures))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
