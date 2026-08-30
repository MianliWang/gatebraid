"""Closure precondition (b): a closing keyword immediately preceding an issue
reference, in the pull-request body or in ANY commit message the PR carries.

ADR-0018 section 1 and gate-3-contract: TEST THE PATTERN, NOT THE BARE TOKEN.
A conventional-commit `fix(scope):` prefix references nothing and is not
prohibited; this scan therefore reports the bare-token count BESIDE the pattern
count so a zero is not mistaken for "the word does not appear", and prints every
pattern match rather than asserting there are none (ADR-0018 section 2,
friction #87).

Keywords: close/closes/closed, fix/fixes/fixed, resolve/resolves/resolved, any
case. References: `#n`, `owner/repo#n`, a GitHub issue URL.

Exit 0 = no pattern match anywhere. Exit 1 = at least one. Exit 2 = structure.
Python 3 standard library only.
"""
import argparse, json, re, subprocess, sys

KEYWORD = r"(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)"
REFERENCE = (r"(?:#\d+"
             r"|[A-Za-z0-9._-]+/[A-Za-z0-9._-]+#\d+"
             r"|https?://github\.com/\S+/issues/\d+)")
PATTERN = re.compile(KEYWORD + r"\s*:?\s+" + REFERENCE, re.I)
BARE = re.compile(KEYWORD, re.I)


def run(argv):
    p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="MianliWang/gatebraid")
    ap.add_argument("--pr", type=int, required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--head", default="HEAD")
    ap.add_argument("--body-from", default=None,
                    help="read the PR body from a file instead of the API "
                         "(used only to point the SAME scan at a seeded body)")
    args = ap.parse_args()

    print("keyword pattern    : %s" % PATTERN.pattern)
    print("scope              : the pull-request body and every commit message "
          "in %s..%s" % (args.base[:12], args.head))
    print()

    hits = []

    if args.body_from:
        body = open(args.body_from, encoding="utf-8").read()
        src = "file:%s" % args.body_from
    else:
        rc, out = run(["gh", "pr", "view", str(args.pr), "--repo", args.repo,
                       "--json", "body"])
        if rc != 0:
            print("STRUCTURE: could not read the pull-request body")
            return 2
        body = json.loads(out)["body"]
        src = "pr#%d" % args.pr
    m = PATTERN.findall(body)
    print("PR body (%s)" % src)
    print("   pattern matches : %d  %s" % (len(m), m if m else ""))
    print("   bare tokens     : %d  (a conventional-commit prefix references "
          "nothing and is not prohibited)" % len(BARE.findall(body)))
    hits += [("body", x) for x in m]

    rc, out = run(["git", "rev-list", "%s..%s" % (args.base, args.head), "--reverse"])
    if rc != 0:
        print("STRUCTURE: could not list the commits")
        return 2
    commits = out.split()
    print()
    print("commit messages the pull request carries: %d" % len(commits))
    for c in commits:
        rc, msg = run(["git", "log", "-1", "--format=%B", c])
        cm = PATTERN.findall(msg)
        subject = msg.strip().splitlines()[0][:48] if msg.strip() else ""
        print("   %s  pattern=%-2d bare=%-2d  %s"
              % (c[:12], len(cm), len(BARE.findall(msg)), subject))
        if cm:
            print("        MATCHES: %s" % cm)
        hits += [(c, x) for x in cm]

    print()
    print("total pattern matches: %d" % len(hits))
    for where, x in hits:
        print("   %s  %r" % (where, x))
    if hits:
        print("CLOSING-KEYWORD SCAN: FOUND - closure precondition (b) FAILS")
        return 1
    print("CLOSING-KEYWORD SCAN: CLEAN - no closing keyword precedes any issue "
          "reference")
    return 0


if __name__ == "__main__":
    sys.exit(main())
