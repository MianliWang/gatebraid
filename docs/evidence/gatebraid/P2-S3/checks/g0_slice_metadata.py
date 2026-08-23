#!/usr/bin/env python3
"""Gate 0 A6 — the Slice issue body's `## gatebraid-metadata` block parses
against schema/slice.schema.json (gatebraid/slice@1).

Reads the gatebraid/evidence-capture@1 record produced for the body read,
decodes its stdout payload from base64 (never the envelope's rendering),
extracts the first fenced yaml block under the heading per the schema's own
stated rule, and validates. Loader is named in the output (friction #55).

Usage: g0_slice_metadata.py <capture.json> <schema.json>
Exit 0 = valid; 2 = extraction failure; 3 = schema-invalid; 4 = capture unusable.
"""
import sys, re, json, base64, hashlib
import yaml, jsonschema
from jsonschema import Draft202012Validator


def main():
    cap_path, schema_path = sys.argv[1], sys.argv[2]
    cap = json.load(open(cap_path, encoding='utf-8'))
    if cap.get('schema') != 'gatebraid/evidence-capture@1':
        print(json.dumps({"error": "not an evidence-capture@1 record"})); sys.exit(4)
    if cap.get('exit_code') != 0:
        print(json.dumps({"error": "captured command exited non-zero",
                          "exit_code": cap.get('exit_code')})); sys.exit(4)

    raw = base64.b64decode(cap['streams']['stdout']['data'])
    if hashlib.sha256(raw).hexdigest() != cap['streams']['stdout']['sha256']:
        print(json.dumps({"error": "stdout digest mismatch"})); sys.exit(4)

    payload = json.loads(raw.decode('utf-8'))
    body = payload['body']

    m = re.search(r'^##[ \t]+gatebraid-metadata[ \t]*$', body, re.M)
    if not m:
        print(json.dumps({"error": "no '## gatebraid-metadata' heading"})); sys.exit(2)
    rest = body[m.end():]
    fences = re.findall(r'^```[ \t]*ya?ml[ \t]*\r?\n(.*?)^```[ \t]*$', rest, re.M | re.S)
    if not fences:
        print(json.dumps({"error": "no fenced yaml block under the heading"})); sys.exit(2)
    data = yaml.safe_load(fences[0])

    schema = json.load(open(schema_path, encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    errs = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path))

    out = {
        "loader": "PyYAML %s / jsonschema %s / Draft202012Validator"
                  % (yaml.__version__, jsonschema.metadata.version('jsonschema')
                     if hasattr(jsonschema, 'metadata') else __import__('importlib.metadata', fromlist=['version']).version('jsonschema')),
        "interpreter": sys.executable,
        "body_sha256": hashlib.sha256(body.encode('utf-8')).hexdigest(),
        "body_bytes": len(body.encode('utf-8')),
        "fences_under_heading": len(fences),
        "declared_schema": data.get('schema'),
        "file_id": schema.get('$id'),
        "id_match": data.get('schema') == schema.get('$id'),
        "error_count": len(errs),
        "errors": [{"path": list(e.path), "message": e.message} for e in errs],
        "slice_id": data.get('slice_id'),
        "environment": data.get('environment'),
        "write_domains": data.get('write_domains'),
    }
    print(json.dumps(out))
    sys.exit(3 if errs else 0)


main()
