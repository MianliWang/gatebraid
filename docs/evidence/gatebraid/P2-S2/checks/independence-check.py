#!/usr/bin/env python3
"""T9 - the mechanised half of this Slice's negative criterion N-B.

The frozen Gate 1 plan states N-B as: "neither landed file reaches N2's
implementation, and neither imports a third-party module at module level."
This is that check, and it reports LOCI, never the offending text (ADR-0028 §3).

SCOPE, as an explicit path set rather than "the added files" (friction #110):
exactly the paths named on the command line, which the plan fixes as
`bin/gatebraid-validate.py` and `bin/gatebraid-validate-selftest.py`.

DIRECTION OF ERROR, declared because a proxy that does not state one cannot be
read (ADR-0018 §2):

  * third-party half - ERRS TOWARD FALSE FAILURE. Only MODULE-LEVEL
    `Import`/`ImportFrom` nodes are inspected, so a guarded optional import
    inside a function or a `try` block is deliberately out of scope and passes;
    that is how the validator reaches its JSON Schema loader. Any module-level
    name outside `sys.stdlib_module_names` fails.

  * N2 half - ALSO ERRS TOWARD FALSE FAILURE. Any occurrence of the generator's
    module name in any string or identifier anywhere in the parse tree is
    flagged, including a path handed to the committed capture tool on a command
    line, which is expressly PERMITTED use. A flagged occurrence is therefore
    read by a human against the criterion's text and never auto-accepted; what
    the check guarantees is that no such occurrence passes unnoticed.

Exit 0 clean · 1 a criterion is violated · 2 the check could not run.
Python 3 standard library only.
"""
import ast
import os
import sys

# The generator's module identity, assembled rather than written whole so this
# detector does not carry a literal copy of the token it exists to find.
_STEM = "gatebraid" + "-" + "capture"
N2_TOKENS = (_STEM, _STEM.replace("-", "_"))
N2_PATHS = (os.path.join("bin", _STEM + ".py"),
            os.path.join("bin", _STEM + "-selftest.py"))


def module_level_imports(tree):
    """Only nodes whose parent is the Module body: the criterion's stated scope."""
    out = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for a in node.names:
                out.append((a.name.split(".")[0], node.lineno))
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                out.append((node.module.split(".")[0], node.lineno))
    return out


def check(path):
    findings = []
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
        tree = ast.parse(raw.decode("utf-8"), filename=path)
    except (OSError, SyntaxError, UnicodeDecodeError) as exc:
        print("HARNESS: cannot parse %s (%s)" % (path, exc))
        return None

    stdlib = getattr(sys, "stdlib_module_names", frozenset())
    for name, lineno in module_level_imports(tree):
        if name not in stdlib:
            findings.append((path, lineno, "module-level-third-party-import"))

    # N2 reachability: any identifier or string anywhere in the tree.
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if any(tok in node.value for tok in N2_TOKENS):
                findings.append((path, getattr(node, "lineno", 0), "n2-token-in-string"))
        elif isinstance(node, ast.Name):
            if any(tok in node.id for tok in N2_TOKENS):
                findings.append((path, getattr(node, "lineno", 0), "n2-token-in-identifier"))
        elif isinstance(node, ast.Attribute):
            if any(tok in node.attr for tok in N2_TOKENS):
                findings.append((path, getattr(node, "lineno", 0), "n2-token-in-attribute"))

    imported = {n for n, _ in module_level_imports(tree)}
    for n2 in N2_PATHS:
        stem = os.path.splitext(os.path.basename(n2))[0].replace("-", "_")
        if stem in imported:
            findings.append((path, 0, "imports-n2-module"))

    print("  %-46s module-level imports: %-3d  findings: %d"
          % (path, len(module_level_imports(tree)), len(findings)))
    for _, lineno, rule in findings:
        print("      line %-6s %s" % (lineno, rule))
    return findings


def main(argv):
    targets = argv[1:]
    if not targets:
        print(__doc__)
        return 2
    print("N-B scope, as an explicit path set:")
    for t in targets:
        print("   %s" % t)
    print()
    total = []
    for t in targets:
        if not os.path.isfile(t):
            print("HARNESS: %s does not exist" % t)
            return 2
        res = check(t)
        if res is None:
            return 2
        total += res
    print()
    print("stdlib names available        : %d" % len(getattr(sys, "stdlib_module_names", ())))
    print("interpreter                   : %s" % sys.executable)
    print("criterion violations          : %d" % len(total))
    if not total:
        print("INDEPENDENCE CLEAN: no module-level third-party import, and no path "
              "from either file to the generator's implementation")
    else:
        print("INDEPENDENCE NOT CLEAN: each locus above is read against N-B's text; "
              "the check errs toward false failure in both halves")
    return 0 if not total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
