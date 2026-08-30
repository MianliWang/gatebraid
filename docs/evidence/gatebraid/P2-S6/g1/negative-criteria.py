"""P2-S6 negative criteria N1-N5, mechanised. Python 3 standard library only.

Gate 1 freezes these; review item R4 checks them at Gate 2 (gate-1-contract
action 3, ADR-0011 section 5). Each criterion states the pattern it proxies for,
the scope it searches, and THE DIRECTION IN WHICH IT ERRS (ADR-0018 section 2,
friction #109). The scope is an explicit path set or glob, never "the added
file" (friction #110).

Path criteria (N1-N3) read a changed-path set. Source criteria (N4-N5) read the
two files of the declared code surface.

  --changed-from git         the diff of the working tree against the base
  --changed-from <path>      one path per line; the falsification seed uses this
  --base <sha>               base for `git diff --name-only`, default the
                             Slice's frozen base_sha

Exit 0 = every criterion holds. Exit 1 = at least one fired. Exit 2 = structure.
A criterion that has never fired has never been falsified, which is why the
frozen seed at g1/SEED-negative-criteria.txt exists and is run beside the real
set.
"""
import argparse, ast, os, subprocess, sys

BASE_SHA = "3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8"

ALLOWLIST = ("bin/", "docs/evidence/gatebraid/P2-S6/")

CODE_SURFACE = ("bin/gatebraid-snapshot.py", "bin/gatebraid-snapshot-selftest.py")

FROZEN_PREFIXES = ("schema/", "fixtures/", "docs/evidence/gatebraid/P2-S5/",
                   "adr/", "protocols/", "templates/", "projects/")

# Modules that would mean this tool had stopped delegating authentication to
# `gh`. The list is explicit, never a pattern: a pattern over module names is
# the defect the P2-S5 closed-set sweep was repaired for.
NETWORK_MODULES = {"urllib", "urllib.request", "urllib.error", "http",
                   "http.client", "requests", "socket", "ssl", "urllib3",
                   "httpx", "aiohttp"}

STDLIB = set(sys.stdlib_module_names)

# The non-standard-library imports the code surface ALREADY carries, measured on
# the frozen base at Gate 1 and frozen here. N4 tests that the Slice adds no NEW
# runtime dependency; it does not pretend the tool had none. `jsonschema` is
# pre-existing and lawful - the tool validates its output against the frozen
# schema. Falsifying N4 before trusting it is what surfaced this: the first
# mechanisation read "imports nothing outside the standard library" and fired on
# the unmodified source, which is a defect in the criterion, not in the tool.
BASELINE_NONSTDLIB = {
    "bin/gatebraid-snapshot.py": {"jsonschema"},
    "bin/gatebraid-snapshot-selftest.py": set(),
}


def changed_paths(source, base):
    if source == "git":
        proc = subprocess.run(["git", "diff", "--name-only", base],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            raise SystemExit("STRUCTURE: git diff exited %d: %s"
                             % (proc.returncode,
                                proc.stderr.decode("utf-8", "replace").strip()))
        body = proc.stdout.decode("utf-8", "replace")
    else:
        if not os.path.isfile(source):
            raise SystemExit("STRUCTURE: no such changed-path file: %s" % source)
        body = open(source, encoding="utf-8").read()
    return [l.strip() for l in body.splitlines() if l.strip()]


def n1(paths):
    """Every changed path is inside the frozen allowlist.

    Proxies for: the Slice wrote outside its declared write_domains.
    Scope: every path in the changed set, whole diff.
    ERRS TOWARD FALSE ALARM: a path lawfully inside but spelled differently
    ('./bin/x', 'bin\\x') is reported rather than passed. It never passes a
    path that is outside.
    """
    return [p for p in paths if not p.startswith(ALLOWLIST)]


def n2(paths):
    """Under bin/, only the snapshot pair is touched.

    Proxies for: the Slice edited a tool its Non-goals put out of scope.
    Scope: glob bin/**.
    ERRS TOWARD FALSE ALARM: a rename or a new file inside bin/ fires even if
    a human would call it in scope. It never passes an edit to another tool.
    """
    return [p for p in paths
            if p.startswith("bin/") and p not in CODE_SURFACE]


def n3(paths):
    """No frozen input is written.

    Proxies for: a write to schema/, fixtures/, the retained P2-S5 evidence, or
    any governing document - each frozen and consumed only.
    Scope: the explicit prefix set FROZEN_PREFIXES.
    ERRS TOWARD FALSE ALARM: it fires on any path under those prefixes, without
    asking whether the change was benign. It never passes one.
    """
    return [p for p in paths if p.startswith(FROZEN_PREFIXES)]


def imports_of(path):
    tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.add(a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:
                names.add(node.module)
    return names


def _baseline_for(path):
    """Baseline is keyed by file identity, so a relocated seeded copy of the
    surface inherits the same allowance and the seed tests the rule, not the path."""
    base = os.path.basename(path)
    for k, v in BASELINE_NONSTDLIB.items():
        if os.path.basename(k) == base:
            return v
    return set()


def n4(files):
    """The code surface adds no runtime dependency and constructs no HTTP client.

    Proxies for: the tool began handling credentials or talking to the network
    itself instead of delegating to `gh` (project hard rule; ADR-0009).
    Scope: the two files of CODE_SURFACE, their import set only.
    "Adds no runtime dependency" is measured against BASELINE_NONSTDLIB, the
    non-stdlib import set the surface already carried on the frozen base.
    ERRS TOWARD FALSE ALARM: a stdlib module merely NAMED like a network client
    is reported for a human read rather than silently allowed; and ANY new
    non-stdlib import fires even if a human would call it benign. It never
    passes a real network client, and never passes a new dependency.
    """
    findings = []
    for f in files:
        if not os.path.isfile(f):
            findings.append((f, "ABSENT", "the declared code surface is missing"))
            continue
        for name in sorted(imports_of(f)):
            root = name.split(".")[0]
            if name in NETWORK_MODULES or root in NETWORK_MODULES:
                findings.append((f, name, "network client module"))
            elif root not in STDLIB and root not in _baseline_for(f):
                findings.append((f, name,
                                 "non-stdlib import outside the frozen baseline"))
    return findings


def n5(path):
    """Fail-closed direction: `ok` and `complete: True` are set in one place each.

    Proxies for: a new code path that can report a source healthy without
    travelling the classifier, which is how a degraded read passes through.
    Scope: the single file bin/gatebraid-snapshot.py, its function bodies.
    `member("ok")` may occur only inside classify(); a True-valued "complete"
    key may occur only inside read_source().
    ERRS TOWARD FALSE ALARM: it locates occurrences by enclosing function only,
    so a lawful refactor that moves either into a new helper fires and must be
    re-frozen deliberately. It never passes a second unguarded healthy path.
    """
    if not os.path.isfile(path):
        return [(path, 0, "ABSENT", "the declared code surface is missing")]
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src, filename=path)

    owner = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for n in ast.walk(node):
                for ln in range(getattr(n, "lineno", 0),
                                getattr(n, "end_lineno", 0) + 1):
                    owner.setdefault(ln, node.name)

    findings = []
    for node in ast.walk(tree):
        # member("ok")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "member" and node.args \
                and isinstance(node.args[0], ast.Constant) \
                and node.args[0].value == "ok":
            fn = owner.get(node.lineno, "(module level)")
            if fn != "classify":
                findings.append((path, node.lineno, "member('ok')",
                                 "outside classify(), in %s" % fn))
        # a dict literal setting "complete" to True
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and k.value == "complete" \
                        and isinstance(v, ast.Constant) and v.value is True:
                    fn = owner.get(k.lineno, "(module level)")
                    if fn != "read_source":
                        findings.append((path, k.lineno, '"complete": True',
                                         "outside read_source(), in %s" % fn))
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--changed-from", default="git")
    ap.add_argument("--base", default=BASE_SHA)
    # Overridable ONLY so the SAME instrument - not a copy of it - can be
    # pointed at a seeded surface and shown able to fire. A source criterion
    # that has only ever held has never been falsified.
    ap.add_argument("--code-surface-dir", default=None,
                    help="read the code surface from this directory instead")
    args = ap.parse_args()

    surface = CODE_SURFACE
    if args.code_surface_dir:
        surface = tuple(os.path.join(args.code_surface_dir,
                                     os.path.basename(f)) for f in CODE_SURFACE)

    paths = changed_paths(args.changed_from, args.base)

    print("changed-path source : %s" % args.changed_from)
    print("base                : %s" % args.base)
    print("changed paths       : %d" % len(paths))
    for p in paths:
        print("   %s" % p)
    print("allowlist           : %s" % ", ".join(ALLOWLIST))
    print("code surface        : %s" % ", ".join(surface))
    print()

    fired = []

    r1 = n1(paths)
    print("N1 every changed path inside the allowlist        : %s"
          % ("FIRED" if r1 else "holds"))
    for p in r1:
        print("      outside: %s" % p)
    fired += ["N1"] if r1 else []

    r2 = n2(paths)
    print("N2 under bin/, only the snapshot pair is touched  : %s"
          % ("FIRED" if r2 else "holds"))
    for p in r2:
        print("      not in the code surface: %s" % p)
    fired += ["N2"] if r2 else []

    r3 = n3(paths)
    print("N3 no frozen input is written                     : %s"
          % ("FIRED" if r3 else "holds"))
    for p in r3:
        print("      frozen: %s" % p)
    fired += ["N3"] if r3 else []

    r4 = n4(surface)
    print("N4 no runtime dependency, no HTTP client          : %s"
          % ("FIRED" if r4 else "holds"))
    for f, name, why in r4:
        print("      %s: %s (%s)" % (f, name, why))
    fired += ["N4"] if r4 else []

    r5 = n5(surface[0])
    print("N5 `ok` and `complete: True` each set in one place: %s"
          % ("FIRED" if r5 else "holds"))
    for f, ln, what, why in r5:
        print("      %s:%s %s %s" % (f, ln, what, why))
    fired += ["N5"] if r5 else []

    print()
    if fired:
        print("NEGATIVE CRITERIA FIRED: %s" % ", ".join(fired))
        return 1
    print("NEGATIVE CRITERIA HOLD: N1, N2, N3, N4, N5")
    return 0


if __name__ == "__main__":
    sys.exit(main())
