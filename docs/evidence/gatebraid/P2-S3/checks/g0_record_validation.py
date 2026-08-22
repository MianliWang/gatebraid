#!/usr/bin/env python3
"""Gate 0 — the record's own embedded gatebraid/gate-run@2 block validates.

Extracts the `## gatebraid-metadata` yaml fence from a markdown gate record and
validates it against schema/gate-run-v2.schema.json. Standalone guarded step
whose failure prevents the commit (spec section 4, friction #86); the loader is
named in the output (friction #55).

Usage: g0_record_validation.py <record.md> <schema.json>
Exit 0 = valid; 2 = extraction failure; 3 = schema-invalid.
"""
import sys, re, json, hashlib
import yaml, jsonschema
from jsonschema import Draft202012Validator
import importlib.metadata as _md


def main():
    rec_path, schema_path = sys.argv[1], sys.argv[2]
    raw = open(rec_path, 'rb').read()
    text = raw.decode('utf-8')

    m = re.search(r'^##[ \t]+gatebraid-metadata[ \t]*$', text, re.M)
    if not m:
        print(json.dumps({"error": "no '## gatebraid-metadata' heading"})); sys.exit(2)
    fences = re.findall(r'^```[ \t]*ya?ml[ \t]*\r?\n(.*?)^```[ \t]*$',
                        text[m.end():], re.M | re.S)
    if not fences:
        print(json.dumps({"error": "no fenced yaml block under the heading"})); sys.exit(2)
    data = yaml.safe_load(fences[0])

    schema = json.load(open(schema_path, encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    errs = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path))

    checks = data.get('checks') or []
    out = {
        "loader": "PyYAML %s / jsonschema %s / Draft202012Validator"
                  % (yaml.__version__, _md.version('jsonschema')),
        "interpreter": sys.executable,
        "record": rec_path,
        "record_bytes": len(raw),
        "record_sha256": hashlib.sha256(raw).hexdigest(),
        "crlf_bytes": raw.count(b'\r'),
        "fences_under_heading": len(fences),
        "declared_schema": data.get('schema'),
        "file_id": schema.get('$id'),
        "id_match": data.get('schema') == schema.get('$id'),
        "gate": data.get('gate'),
        "result": data.get('result'),
        "bootstrap_exception_present": 'bootstrap_exception' in data,
        "base_sha_len": len(data.get('base_sha') or ''),
        "checks_total": len(checks),
        "checks_with_output_ref": sum(1 for c in checks if c.get('output_ref')),
        "approvals": [{"type": a.get('type'), "author": a.get('author')}
                      for a in (data.get('approvals') or [])],
        "started_at_is_str": isinstance(data.get('started_at'), str),
        "ended_at_is_str": isinstance(data.get('ended_at'), str),
        "error_count": len(errs),
        "errors": [{"path": list(e.path), "message": e.message} for e in errs][:20],
    }
    print(json.dumps(out))
    sys.exit(3 if errs else 0)


main()
