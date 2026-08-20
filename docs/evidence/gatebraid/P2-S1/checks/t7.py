#!/usr/bin/env python3
"""T7/V7 — negative criterion N2: no module-level third-party import.

Reconstruction. The script the Gate 2 V7 row invoked (`_t7.py`) was written at
the repository root, was never committed, and is not recoverable. This file
reproduces that row's check and its output shape, and is committed so the row
is re-runnable as written. It is not the original bytes (gate2.md, Required
disclosures).

Scope, per gate1.md: the named files are parsed with `ast` and every TOP-LEVEL
`Import` / `ImportFrom` node's root module is compared against
`sys.stdlib_module_names`. A guarded optional import inside a function or a
`try` block -- which is how the selftest reaches `jsonschema` -- is
DELIBERATELY out of scope and passes; any module-level third-party import
fails. The criterion errs toward false failure.

Usage:  python3 t7.py <file.py> [<file.py> ...]
Exit 0 when no module-level import is third-party, 1 otherwise.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

RELATIVE = "<relative>"


def module_level_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: list[str] = []
    for node in tree.body:  # top level ONLY -- never ast.walk
        if isinstance(node, ast.Import):
            names += [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                names.append(node.module.split(".")[0])
            else:
                names.append(RELATIVE)
    return names


def main(argv: list[str]) -> int:
    files = [Path(a) for a in argv[1:]]
    if not files:
        print("usage: t7.py <file.py> [<file.py> ...]", file=sys.stderr)
        return 2

    stdlib = sys.stdlib_module_names
    inspected = 0
    offenders: list[tuple[str, list[str]]] = []

    for f in files:
        names = module_level_imports(f)
        inspected += len(names)
        bad = sorted({n for n in names if n != RELATIVE and n not in stdlib})
        if bad:
            offenders.append((f.as_posix(), bad))

    print("module-level imports inspected: %d" % inspected)
    print("third-party at module level: %s"
          % ("NONE" if not offenders else offenders))
    print("scope: exactly the %d named file(s); guarded imports inside try/def "
          "are out of scope by design" % len(files))
    return 1 if offenders else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
