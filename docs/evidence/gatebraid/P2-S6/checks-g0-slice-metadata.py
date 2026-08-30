#!/usr/bin/env python3
"""Entry-phase check: does an issue body's `## gatebraid-metadata` block
validate against schema/slice.schema.json (gatebraid/slice@1)?

Session working instrument (uncommitted, _handoff/). Per ADR-0028 §4 it is
falsified before it is trusted: --selftest runs seeded mutants that a correct
checker MUST reject, and a positive control it MUST accept. A run that does not
kill every mutant exits non-zero and the check is not trusted.

Extraction rule is the schema's own: the '## gatebraid-metadata' heading
followed by the FIRST fenced yaml block under it.
"""
import argparse
import copy
import json
import re
import sys

import yaml
from jsonschema import Draft202012Validator

HEADING = re.compile(r'^##[ \t]+gatebraid-metadata[ \t]*$', re.MULTILINE)
FENCE = re.compile(r'^```[ \t]*(?:yaml|yml)[ \t]*\n(.*?)^```[ \t]*$',
                   re.MULTILINE | re.DOTALL)


class ExtractError(Exception):
    pass


def extract(text):
    m = HEADING.search(text)
    if m is None:
        raise ExtractError("no '## gatebraid-metadata' heading")
    rest = text[m.end():]
    f = FENCE.search(rest)
    if f is None:
        raise ExtractError("no fenced yaml block under the heading")
    return f.group(1)


def parse_and_validate(text, schema):
    block = extract(text)
    doc = yaml.safe_load(block)
    if not isinstance(doc, dict):
        raise ExtractError("yaml block is not a mapping")
    errs = sorted(Draft202012Validator(schema).iter_errors(doc),
                  key=lambda e: list(e.path))
    return doc, block, errs


def fmt(errs):
    return [f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}"
            for e in errs]


BODY = """# Title

## gatebraid-metadata

```yaml
schema: gatebraid/slice@1
slice_id: P2-S4
stage: S2
phase: P2
workflow_profile: classic
environment: mixed-see-prose
risk: low
depends_on: []
write_domains:
  - bin/
resource_locks: []
repair_limit: 2
consult_first: false
parallel_mode: safe-single-writer
```
"""


def selftest(schema):
    """Seeded mutants a correct checker MUST reject + one positive control."""
    ok = True

    # Positive control: the checker must ACCEPT a well-formed block.
    try:
        _, _, errs = parse_and_validate(BODY, schema)
    except ExtractError as exc:
        print(f"SELFTEST FAIL  positive-control: extractor errored: {exc}")
        return False
    if errs:
        print(f"SELFTEST FAIL  positive-control rejected: {fmt(errs)}")
        ok = False
    else:
        print("selftest pass  positive-control accepted")

    base = yaml.safe_load(extract(BODY))

    mutants = [
        ("M1 wrong schema const", lambda d: d.update({"schema": "gatebraid/slice@2"})),
        ("M2 slice_id off-pattern", lambda d: d.update({"slice_id": "P2S4"})),
        ("M3 required key removed", lambda d: d.pop("risk")),
        ("M4 undeclared property", lambda d: d.update({"owner": "claude"})),
        ("M5 environment off-enum", lambda d: d.update({"environment": "linux"})),
        ("M6 repair_limit above max", lambda d: d.update({"repair_limit": 3})),
        ("M7 workflow_profile renamed", lambda d: d.update({"workflow_profile": "gatebraid-classic"})),
        ("M8 parallel_mode off-enum", lambda d: d.update({"parallel_mode": "isolated"})),
        ("M9 stage off-pattern", lambda d: d.update({"stage": "2"})),
        ("M10 write_domains empty string", lambda d: d.update({"write_domains": [""]})),
    ]
    for name, mutate in mutants:
        d = copy.deepcopy(base)
        mutate(d)
        errs = list(Draft202012Validator(schema).iter_errors(d))
        if errs:
            print(f"selftest pass  {name} rejected -> {fmt(sorted(errs, key=lambda e: list(e.path)))[0]}")
        else:
            print(f"SELFTEST FAIL  {name} SURVIVED (checker does not detect it)")
            ok = False

    # Extractor mutants: the checker MUST error, never silently pass.
    extractor_mutants = [
        ("X1 heading absent", BODY.replace("## gatebraid-metadata", "## metadata")),
        ("X2 fence absent", re.sub(r'```[ \t]*yaml\n.*?```', '(removed)', BODY, flags=re.DOTALL)),
        ("X3 block is a list not a mapping",
         BODY.replace("schema: gatebraid/slice@1", "- schema: gatebraid/slice@1")
             .replace("slice_id:", "  slice_id:")),
    ]
    for name, text in extractor_mutants:
        try:
            _, _, errs = parse_and_validate(text, schema)
        except ExtractError as exc:
            print(f"selftest pass  {name} errored -> {exc}")
            continue
        except yaml.YAMLError as exc:
            print(f"selftest pass  {name} yaml-errored -> {type(exc).__name__}")
            continue
        if errs:
            print(f"selftest pass  {name} rejected -> {fmt(errs)[0]}")
        else:
            print(f"SELFTEST FAIL  {name} SURVIVED")
            ok = False

    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", required=True)
    ap.add_argument("--body")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    with open(a.schema, "rb") as fh:
        schema = json.loads(fh.read().decode("utf-8"))

    if a.selftest:
        ok = selftest(schema)
        print("SELFTEST " + ("PASS - checker may be trusted" if ok
                             else "FAIL - checker NOT trusted"))
        return 0 if ok else 1

    if not a.body:
        print("usage error: --body required without --selftest", file=sys.stderr)
        return 2

    with open(a.body, "rb") as fh:
        text = fh.read().decode("utf-8")

    try:
        doc, block, errs = parse_and_validate(text, schema)
    except ExtractError as exc:
        print(f"EXTRACT ERROR: {exc}")
        return 1

    print("--- extracted block ---")
    sys.stdout.write(block)
    print("--- parsed ---")
    print(json.dumps(doc, indent=2, ensure_ascii=False, sort_keys=True))
    if errs:
        print(f"REJECTED against {schema.get('$id')}:")
        for line in fmt(errs):
            print("  " + line)
        return 1
    print(f"VALID against {schema.get('$id')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
