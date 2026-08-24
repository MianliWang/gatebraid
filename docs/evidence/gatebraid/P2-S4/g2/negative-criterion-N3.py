#!/usr/bin/env python3
"""N3 - no live network call in any declared test command.

THE PROPERTY.  The frozen corpus and seeded fixtures are the only inputs to the
acceptance commands.  No declared test command reaches the live control plane.

THE PATTERN THIS PROXIES FOR, and where the proxy over-matches (ADR-0018 §2).
The pattern is "a declared test depends on the network", which no token search
decides.  Two syntactic proxies stand in for it:

  N3a  the DECLARED COMMANDS' argv contain no `gh` invocation.  The commands are
       READ OUT OF THE FROZEN PLAN - `docs/evidence/gatebraid/P2-S4/gate1.md` -
       rather than re-typed here, so this check cannot drift from the table it
       is about.
  N3b  the harness's own source names no HTTP client.

IT ERRS TOWARD FALSE POSITIVE.  A mention of `gh` in a docstring or a comment
trips N3a; a module named for a transport that is never used trips N3b.  That is
the safe direction: a declared test that quietly reaches the network would make
every acceptance result depend on a live service and on credentials, which is
what the criterion exists to prevent.  WHERE THE PROXY OVER-MATCHES, THE PATTERN
GOVERNS.

SCOPE is explicit: the declared-command table of the frozen plan, and
`bin/gatebraid-o0-acceptance.py`.  Note deliberately that `bin/gatebraid-snapshot.py`
is NOT in N3b's scope - it carries a live `gh` transport by design, and the
criterion is about the DECLARED COMMANDS never selecting that transport, not
about the transport being absent from the tool.

Every match is PRINTED beside its count.  A bare zero states what it searched
(friction #87).

Exit codes: 0 the criterion holds - 1 at least one match stands - 2 the check
could not run.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLICE_DIR = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SLICE_DIR))))

FROZEN_PLAN = os.path.join(SLICE_DIR, "gate1.md")
HARNESS = os.path.join(REPO, "bin", "gatebraid-o0-acceptance.py")

# Names that would indicate a transport being constructed in the harness.
HTTP_CLIENTS = ("requests", "httpx", "aiohttp", "urllib", "urlopen",
                "http.client", "HTTPConnection", "socket")

ROW = re.compile(r"^\|\s*(D\d+[ab]?|N\d+)\s*\|\s*(.+?)\s*\|")


def declared_commands():
    """Read the declared test-plan commands out of the FROZEN plan."""
    if not os.path.isfile(FROZEN_PLAN):
        raise SystemExit("N3 CANNOT RUN: the frozen plan is not at %s" % FROZEN_PLAN)
    rows = []
    with open(FROZEN_PLAN, "r", encoding="utf-8") as fh:
        for line in fh:
            m = ROW.match(line.strip())
            if m:
                rows.append((m.group(1), m.group(2).strip()))
    if not rows:
        raise SystemExit("N3 CANNOT RUN: no declared-command rows were found in "
                         "the frozen plan; a check that searched nothing must "
                         "not report a pass")
    return rows


def main():
    rows = declared_commands()
    findings = []

    for cid, command in rows:
        # `gh` as an invoked program: at a word boundary and not part of a
        # longer identifier such as `github`.
        for m in re.finditer(r"(?<![A-Za-z0-9_.-])gh(?![A-Za-z0-9_-])", command):
            findings.append(("N3a", "frozen plan row %s" % cid, command,
                             "the declared command's text contains a `gh` "
                             "invocation at offset %d" % m.start()))

    if not os.path.isfile(HARNESS):
        raise SystemExit("N3 CANNOT RUN: the harness is not at %s" % HARNESS)
    with open(HARNESS, "r", encoding="utf-8") as fh:
        harness_lines = fh.read().splitlines()
    for i, line in enumerate(harness_lines):
        for name in HTTP_CLIENTS:
            if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(name), line):
                findings.append(("N3b", "bin/gatebraid-o0-acceptance.py:%d" % (i + 1),
                                 line.strip(),
                                 "the harness source names the HTTP client %r" % name))

    print("criterion      : N3 - no live network call in any declared test command")
    print("pattern proxied: a declared test depending on the live control plane")
    print("errs toward    : FALSE POSITIVE (a mention in prose trips it)")
    print("scope          :")
    print("   the declared-command table of %s"
          % os.path.relpath(FROZEN_PLAN, REPO).replace(os.sep, "/"))
    print("   bin/gatebraid-o0-acceptance.py")
    print("   NOT in scope: bin/gatebraid-snapshot.py, which carries a live gh "
          "transport by design")
    print("shapes searched:")
    print("   N3a  a `gh` invocation in a declared command's argv")
    print("   N3b  an HTTP client named in the harness source: %s"
          % ", ".join(HTTP_CLIENTS))
    print()
    print("declared commands read from the frozen plan : %d" % len(rows))
    for cid, command in rows:
        print("   %-4s %s" % (cid, command[:118]))
    print()
    print("matches        : %d" % len(findings))
    for shape, where, text, why in findings:
        print("   %-4s %s  %s" % (shape, where, why))
        print("        %s" % text[:150])
    print()
    if findings:
        print("N3 DOES NOT HOLD: %d match(es) stand and each needs adjudication "
              "in the record" % len(findings))
        return 1
    print("N3 HOLDS: no declared command invokes `gh` and the harness source "
          "names no HTTP client")
    return 0


if __name__ == "__main__":
    sys.exit(main())
