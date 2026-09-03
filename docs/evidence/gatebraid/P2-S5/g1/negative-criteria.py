"""P2-S5 negative criteria N1-N6, mechanised. Python 3 standard library only.

Gate 1 freezes these; review item R4 checks them at Gate 2 (gate-1-contract
action 3, ADR-0011 section 5). Each criterion states the pattern it proxies for,
the scope it searches, and THE DIRECTION IN WHICH IT ERRS (ADR-0018 section 2,
friction #109). The scope is an explicit path set or glob, never "the added
file" (friction #110).

Path criteria (N1, N2) read a changed-path set: the tracked diff against the
frozen base UNION the untracked set, because a Slice whose deliverable is two
new files and a directory of evidence writes almost nothing a tracked diff can
see until it is staged.

N3 is TWO limbs and the second is not a path rule. The retained P2-S5 Gate 0
record and its re-run subdirectory live under this Slice's OWN evidence prefix,
so a prefix rule forbidding writes there would forbid the Slice writing at all.
The limb that protects them therefore measures CONTENT: the retained-set
path-list digest and the two gate0.md hashes, each frozen below at the value the
Gate 0 exit recorded.

N4 and N5 read source. N6 reads two sources and compares one against the other's
own declared code space rather than against a remembered list.

  --changed-from git         tracked diff against --base, union the untracked set
  --changed-from <path>      one path per line; the falsification seed uses this
  --base <sha>               base for `git diff --name-only`
  --code-surface-dir <dir>   read the code surface from here instead
  --transitive-target <path> the default --snapshot-command target N5 checks
  --frozen-root <dir>        the retained-record root N3's content limb measures
  --consumer <path>          the consumer whose code space N6 reads

Exit 0 = every criterion holds. Exit 1 = at least one fired. Exit 2 = structure.
A criterion that has never fired has never been falsified, which is why the
frozen seed beside this file exists and is run against this same instrument.
"""
import argparse, ast, hashlib, os, re, subprocess, sys

BASE_SHA = "cbd065893b37f20713ae35b8d2673bf26fe4d2ad"

ALLOWLIST = ("bin/", "docs/evidence/gatebraid/P2-S5/")

CODE_SURFACE = ("bin/gatebraid-ready.py", "bin/gatebraid-ready-selftest.py")

TRANSITIVE_TARGET = "bin/gatebraid-snapshot.py"
CONSUMER = "bin/gatebraid-frontier.py"
FROZEN_ROOT = "docs/evidence/gatebraid/P2-S5"

FROZEN_PREFIXES = ("schema/", "fixtures/", "adr/", "protocols/", "templates/",
                   "projects/",
                   "docs/evidence/gatebraid/P2-S1/",
                   "docs/evidence/gatebraid/P2-S2/",
                   "docs/evidence/gatebraid/P2-S3/",
                   "docs/evidence/gatebraid/P2-S4/",
                   "docs/evidence/gatebraid/P2-S6/")

# The three values the Gate 0 exit recorded and re-measured. They are frozen
# here so N3's content limb compares against a written constant rather than
# against whatever the tree happens to hold when it runs.
RETAINED_PATHLIST_DIGEST = \
    "83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f"
RETAINED_GATE0_SHA256 = \
    "be7c338896b1015923671988166d55af3bd59e028660ce89dfd3b69bc7251513"
G0R_GATE0_SHA256 = \
    "95ff39111b4a8b8aa43c022e877c98af5f868b054f4ac2c116ae5c67327bc4e6"
RETAINED_FILE_COUNT = 43

# Modules that would mean this tool had stopped delegating authentication to the
# command-line client. The list is EXPLICIT, never a pattern: a pattern over
# module names is the defect the P2-S5 closed-set sweep was repaired for.
NETWORK_MODULES = {"urllib", "urllib.request", "urllib.error", "http",
                   "http.client", "requests", "socket", "ssl", "urllib3",
                   "httpx", "aiohttp"}

STDLIB = set(sys.stdlib_module_names)

# The non-standard-library imports the code surface already carries. Both are
# EMPTY and that is a claim about the frozen scope, not an oversight: all three
# M2 slice-C attempts declare a Python 3 STANDARD-LIBRARY program, so any
# non-stdlib import at all is new. N4 is falsified against a seeded surface
# before it is trusted, which is what distinguishes an empty baseline that was
# measured from one that was assumed.
BASELINE_NONSTDLIB = {
    "bin/gatebraid-ready.py": set(),
    "bin/gatebraid-ready-selftest.py": set(),
}

# The consumer's declared code space is PARSED from its own module docstring,
# not written here. This line is the parser's contract with that docstring.
CONSUMER_CODE_LINE = re.compile(r"Exit codes:(.*?)(?:\n\s*\n|$)", re.S)
CONSUMER_CODE_TOKEN = re.compile(r"(?<![0-9])([0-9]{1,2})\s")

# The codes `ready` adds. The frozen scope's rule is that they sit OUTSIDE the
# consumer's declared space so they cannot be confused with a verdict.
READY_OWN_CODES = {10, 11}


def sha256_file(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def changed_paths(source, base):
    if source != "git":
        if not os.path.isfile(source):
            raise SystemExit("STRUCTURE: no such changed-path file: %s" % source)
        body = open(source, encoding="utf-8").read()
        return [l.strip() for l in body.splitlines() if l.strip()]

    proc = subprocess.run(["git", "diff", "--name-only", base],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise SystemExit("STRUCTURE: git diff exited %d: %s"
                         % (proc.returncode,
                            proc.stderr.decode("utf-8", "replace").strip()))
    tracked = [l.strip() for l in
               proc.stdout.decode("utf-8", "replace").splitlines() if l.strip()]

    # --untracked-files=all, so the set is files and never a bare directory.
    proc = subprocess.run(["git", "status", "--porcelain",
                           "--untracked-files=all"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise SystemExit("STRUCTURE: git status exited %d" % proc.returncode)
    untracked = []
    for line in proc.stdout.decode("utf-8", "replace").splitlines():
        if line.startswith("?? "):
            untracked.append(line[3:].strip().strip('"'))
    return sorted(set(tracked) | set(untracked))


def n1(paths):
    """Every changed path is inside the frozen allowlist.

    Proxies for: the Slice wrote outside its declared write_domains.
    Scope: the tracked diff against the frozen base UNION the untracked set.
    ERRS TOWARD FALSE ALARM: a path lawfully inside but spelled differently is
    reported rather than passed. It never passes a path that is outside.
    """
    return [p for p in paths if not p.startswith(ALLOWLIST)]


def n2(paths):
    """Under bin/, only the ready pair is touched.

    Proxies for: the Slice edited one of the five landed tool pairs, which its
    Non-goals list puts out of scope.
    Scope: glob bin/**.
    ERRS TOWARD FALSE ALARM: any other file appearing under bin/ fires even
    where a human would call it in scope. It never passes an edit to a landed
    pair.
    """
    return [p for p in paths if p.startswith("bin/") and p not in CODE_SURFACE]


def n3_paths(paths):
    """Limb (a): no changed path lies under a frozen prefix.

    Proxies for: a write to a schema, a fixture, a governing document or
    another Slice's committed evidence - each frozen and consumed only.
    Scope: the explicit prefix set FROZEN_PREFIXES.
    ERRS TOWARD FALSE ALARM: it fires on any path under those prefixes without
    asking whether the change was benign. It never passes one.
    """
    return [p for p in paths if p.startswith(FROZEN_PREFIXES)]


def n3_content(root):
    """Limb (b): the retained Gate 0 record still measures what it measured.

    Proxies for: this Slice modified the retained record or its re-run
    subdirectory - which no path rule can catch, because both sit under this
    Slice's own evidence prefix.
    Scope: the file list of <root> with the re-run and this gate's own
    subdirectory excluded, plus the two gate0.md files by content.
    ERRS TOWARD FALSE ALARM: any byte change anywhere in the retained set moves
    the digest and fires, including a change a human would call harmless. It
    never passes a modified retained record.
    """
    findings = []
    retained = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ("g0r", "g1")]
        for fn in filenames:
            p = os.path.join(dirpath, fn).replace(os.sep, "/")
            retained.append(p)
    retained.sort()
    if len(retained) != RETAINED_FILE_COUNT:
        findings.append(("retained file count", str(len(retained)),
                         "expected %d" % RETAINED_FILE_COUNT))
    payload = ("\n".join(retained) + "\n").encode("utf-8")
    got = hashlib.sha256(payload).hexdigest()
    if got != RETAINED_PATHLIST_DIGEST:
        findings.append(("retained-set path-list digest", got,
                         "expected %s" % RETAINED_PATHLIST_DIGEST))
    for rel, want in ((os.path.join(root, "gate0.md"), RETAINED_GATE0_SHA256),
                      (os.path.join(root, "g0r", "gate0.md"), G0R_GATE0_SHA256)):
        if not os.path.isfile(rel):
            findings.append((rel.replace(os.sep, "/"), "ABSENT", "expected %s" % want))
            continue
        got = sha256_file(rel)
        if got != want:
            findings.append((rel.replace(os.sep, "/"), got, "expected %s" % want))
    return findings


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
    """Keyed by file identity, so a relocated seeded copy of the surface
    inherits the same allowance and the seed tests the rule, not the path."""
    base = os.path.basename(path)
    for k, v in BASELINE_NONSTDLIB.items():
        if os.path.basename(k) == base:
            return v
    return set()


def n4(files):
    """The code surface adds no runtime dependency and constructs no HTTP client.

    Proxies for: the tool began handling credentials or talking to the network
    itself instead of delegating to the command-line client (project hard rule;
    ADR-0009).
    Scope: the two files of the code surface, their import set only.
    ERRS TOWARD FALSE ALARM: a stdlib module merely NAMED like a network client
    is reported for a human read rather than silently allowed, and any
    non-stdlib import fires even where a human would call it benign. It never
    passes a real network client and never passes a new dependency.
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


def _graphql_mutations(path):
    """String constants in the file that OPEN a GraphQL mutation document.

    The proxy is the document's operation keyword at the head of the literal,
    NOT the bare word, which occurs in ordinary prose and in this file.
    """
    hits = []
    tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            head = node.value.lstrip()
            if head.startswith("mutation") or head.startswith("query=mutation"):
                hits.append((path, node.lineno, "graphql document opens a mutation"))
    return hits


def n5(files, transitive):
    """No control-plane mutation, and no file written by the tool.

    Two parts, because either alone is unsound.
    File-local, scope: the two added files - zero GraphQL documents opening a
    mutation, and zero open() in a write mode.
    Transitive, scope: the default --snapshot-command target - every GraphQL
    document it carries opens a query and none opens a mutation.
    The HTTP method is deliberately NOT the proxy: a read-only GraphQL query is
    sent by POST, so a no-method-other-than-GET check reports a violation where
    there is none (friction #68). A file-local count of the client's name would
    read zero while the program invokes it on every default run, which is an
    under-matching proxy and not a check at all (friction #67).
    ERRS TOWARD FALSE ALARM on the file-local limb: a read-only open() in a
    variable mode is reported. It never passes a mutation document.
    """
    findings = []
    for f in files:
        if not os.path.isfile(f):
            findings.append((f, 0, "ABSENT", "the declared code surface is missing"))
            continue
        findings += [(p, ln, "file-local", why) for p, ln, why in _graphql_mutations(f)]
        tree = ast.parse(open(f, encoding="utf-8").read(), filename=f)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                    and node.func.id == "open":
                mode = None
                if len(node.args) > 1 and isinstance(node.args[1], ast.Constant):
                    mode = node.args[1].value
                for kw in node.keywords:
                    if kw.arg == "mode" and isinstance(kw.value, ast.Constant):
                        mode = kw.value.value
                if mode is None or any(c in str(mode) for c in ("w", "a", "x", "+")):
                    findings.append((f, node.lineno, "file-local",
                                     "open() not provably read-only (mode %r)" % mode))
    if not os.path.isfile(transitive):
        findings.append((transitive, 0, "transitive",
                         "the declared transitive target is missing"))
    else:
        findings += [(p, ln, "transitive", why)
                     for p, ln, why in _graphql_mutations(transitive)]
    return findings


def consumer_code_space(path):
    """The consumer's declared exit codes, read from its own module docstring.

    Returns a set of ints, or raises. An unreadable docstring is a FAILURE of
    this criterion and never a silent pass: a check that vacates itself when it
    cannot read its input has measured nothing.
    """
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src, filename=path)
    doc = ast.get_docstring(tree) or ""
    m = CONSUMER_CODE_LINE.search(doc)
    if not m:
        raise ValueError("no `Exit codes:` paragraph in the consumer docstring")
    codes = {int(x) for x in CONSUMER_CODE_TOKEN.findall(m.group(1) + " ")}
    if not codes:
        raise ValueError("the `Exit codes:` paragraph declares no code")
    return codes


def ready_declared_codes(path):
    """The exit codes `ready` declares, as module-level int constants whose name
    begins EXIT_. Absent file yields None so the caller can report it."""
    if not os.path.isfile(path):
        return None
    tree = ast.parse(open(path, encoding="utf-8").read(), filename=path)
    codes = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id.startswith("EXIT_") \
                        and isinstance(node.value, ast.Constant) \
                        and isinstance(node.value.value, int):
                    codes.add(node.value.value)
    return codes


def n6(surface_ready, consumer, producer):
    """`ready` declares no exit code inside EITHER composed tool's declared space.

    Proxies for: the composer renumbering into a composed tool's range, so a
    caller reading only the exit status cannot tell a verdict, or a producer
    outcome, from a composition failure. This is the frozen scope's own rule,
    applied to the two tools AS THEY ARE rather than as they were.
    Scope: the module-level EXIT_ integer constants of the ready tool, and the
    `Exit codes:` paragraph of each composed tool's module docstring.
    BOTH spaces are read, not just the consumer's. The producer's matters
    because its exit is INTERPRETED and not merely tested against zero: it
    declares 3 for `snapshot emitted and DEGRADED`, which is a document the
    composer must pass on, and 1 and 2 for outcomes where no document exists at
    all. A composer that read any non-zero producer status as failure would
    discard a lawful degraded document and hide the degradation from the
    consumer that classifies it.
    ERRS TOWARD FALSE ALARM: a docstring the parser cannot read is a failure
    rather than a pass, so an unparseable composed tool stops the check instead
    of silently vacating it. It never passes a colliding code.
    """
    findings = []
    spaces = {}
    for label, path in (("consumer", consumer), ("producer", producer)):
        try:
            spaces[label] = consumer_code_space(path)
        except Exception as exc:
            findings.append((label, path, "code space unreadable: %s" % exc))
    if len(spaces) != 2:
        return findings, spaces
    space = spaces["consumer"] | spaces["producer"]
    declared = ready_declared_codes(surface_ready)
    if declared is None:
        findings.append(("ready", surface_ready,
                         "the declared code surface is missing"))
        return findings, spaces
    for c in sorted(declared & space):
        findings.append(("collision", surface_ready,
                         "exit %d is inside a composed tool's declared space" % c))
    for c in sorted(READY_OWN_CODES - declared):
        findings.append(("missing", surface_ready,
                         "the frozen scope's exit %d is not declared" % c))
    return findings, spaces


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--changed-from", default="git")
    ap.add_argument("--base", default=BASE_SHA)
    # Every override below exists for ONE reason: so the SAME instrument - not a
    # copy of it - can be pointed at a seeded input and shown able to fire.
    ap.add_argument("--code-surface-dir", default=None)
    ap.add_argument("--transitive-target", default=TRANSITIVE_TARGET)
    ap.add_argument("--frozen-root", default=FROZEN_ROOT)
    ap.add_argument("--consumer", default=CONSUMER)
    args = ap.parse_args()

    surface = CODE_SURFACE
    transitive = args.transitive_target
    consumer = args.consumer
    if args.code_surface_dir:
        surface = tuple(os.path.join(args.code_surface_dir, os.path.basename(f))
                        for f in CODE_SURFACE)
        transitive = os.path.join(args.code_surface_dir,
                                  os.path.basename(TRANSITIVE_TARGET))
        consumer = os.path.join(args.code_surface_dir,
                                os.path.basename(CONSUMER))

    paths = changed_paths(args.changed_from, args.base)

    print("changed-path source : %s" % args.changed_from)
    print("base                : %s" % args.base)
    print("changed paths       : %d" % len(paths))
    for p in paths[:12]:
        print("   %s" % p)
    if len(paths) > 12:
        print("   [... %d more; the full set is the scope, not this listing]"
              % (len(paths) - 12))
    print("allowlist           : %s" % ", ".join(ALLOWLIST))
    print("code surface        : %s" % ", ".join(surface))
    print("transitive target   : %s" % transitive)
    print("consumer            : %s" % consumer)
    print("frozen root         : %s" % args.frozen_root)
    print()

    fired = []

    r1 = n1(paths)
    print("N1 every changed path inside the allowlist         : %s"
          % ("FIRED" if r1 else "holds"))
    for p in r1:
        print("      outside: %s" % p)
    fired += ["N1"] if r1 else []

    r2 = n2(paths)
    print("N2 under bin/, only the ready pair is touched      : %s"
          % ("FIRED" if r2 else "holds"))
    for p in r2:
        print("      not in the code surface: %s" % p)
    fired += ["N2"] if r2 else []

    r3a = n3_paths(paths)
    r3b = n3_content(args.frozen_root)
    r3 = r3a or r3b
    print("N3 no frozen input is written                      : %s"
          % ("FIRED" if r3 else "holds"))
    for p in r3a:
        print("      frozen prefix: %s" % p)
    for what, got, want in r3b:
        print("      %s: %s (%s)" % (what, got, want))
    fired += ["N3"] if r3 else []

    r4 = n4(surface)
    print("N4 no runtime dependency, no HTTP client           : %s"
          % ("FIRED" if r4 else "holds"))
    for f, name, why in r4:
        print("      %s: %s (%s)" % (f, name, why))
    fired += ["N4"] if r4 else []

    r5 = n5(surface, transitive)
    print("N5 no control-plane mutation, no file written      : %s"
          % ("FIRED" if r5 else "holds"))
    for f, ln, limb, why in r5:
        print("      %s:%s [%s] %s" % (f, ln, limb, why))
    fired += ["N5"] if r5 else []

    r6, spaces = n6(surface[0], consumer, transitive)
    print("N6 ready's codes sit outside both composed spaces  : %s"
          % ("FIRED" if r6 else "holds"))
    for label in ("consumer", "producer"):
        if label in spaces:
            print("      %s declared code space, read from its docstring: %s"
                  % (label, ", ".join(str(c) for c in sorted(spaces[label]))))
    for kind, where, why in r6:
        print("      [%s] %s: %s" % (kind, where, why))
    fired += ["N6"] if r6 else []

    print()
    if fired:
        print("NEGATIVE CRITERIA FIRED: %s" % ", ".join(fired))
        return 1
    print("NEGATIVE CRITERIA HOLD: N1, N2, N3, N4, N5, N6")
    return 0


if __name__ == "__main__":
    sys.exit(main())
