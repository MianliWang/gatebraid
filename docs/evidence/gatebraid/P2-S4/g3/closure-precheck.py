#!/usr/bin/env python3
"""Gate 3 closure precondition (b) — the keyword half, tested as a PATTERN.

THE INVARIANT THIS PROTECTS: a Slice is closed **iff** `G3 passed` (spec §2), and
closure is what releases native `blocked_by` dependents (ADR-0007). So the Slice
must not be closable by anything except this gate's explicit exit command.

WHAT IS PROHIBITED, exactly: a **closing keyword immediately preceding an issue
reference** — `keyword #n`, `keyword owner/repo#n`, `keyword <issue-url>`, in any
case — where keyword is one of `close`/`closes`/`closed`, `fix`/`fixes`/`fixed`,
`resolve`/`resolves`/`resolved` (ADR-0012 §1 as amended by ADR-0018 §1).

**TEST THE PATTERN, NOT THE BARE TOKEN.** This is the whole point of the amended
rule. A conventional-commit `fix(scope):` prefix references nothing and is NOT
prohibited; neither is the word `fixtures`, nor prose like "closed by
measurement". A check that flagged those would be one correct work cannot
satisfy, which trains the executor to route around it (ADR-0018 §2). So this
file counts BOTH — the prohibited pattern, and the bare tokens — and prints the
bare-token matches beside their count, so the zero above them states what it
searched (friction #87) and a reader can see the two are different things.

WHY THIS EXISTS SEPARATELY FROM CHECK (a). Measured 2026-07-30: a merged pull
request saying a closing keyword before an issue reference closed its issue one
second later **with `Auto-close issue` disabled throughout**. That is GitHub's own
behaviour, not Project automation, so check (a) cannot see it. Either check
failing stops the gate; `(a) pass` alone is not compliance.

Usage: closure-precheck.py --range <base>..<head>
       closure-precheck.py --file <path>          (e.g. a drafted PR body)
Exit codes: 0 the prohibited pattern is absent · 1 present · 2 usage error.
"""

import os
import re
import subprocess
import sys

KEYWORD = r"(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)"
REFERENCE = (r"(?:#\d+"
             r"|[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+#\d+"
             r"|https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/issues/\d+)")
# "Immediately preceding": the keyword, optional colon, whitespace, the
# reference. Nothing else may sit between them.
PROHIBITED = re.compile(KEYWORD + r"\s*:?\s+" + REFERENCE, re.I)
BARE = re.compile(KEYWORD, re.I)

def out(line=""):
    """Write one line as EXPLICIT UTF-8 BYTES to a binary sink.

    Not `print`. This instrument scans arbitrary text and echoes matched context,
    so its output carries whatever non-ASCII its input carries -- and on this host
    a cp936 console re-encodes a text-layer write, producing bytes that are not
    valid UTF-8. Measured here rather than assumed: the first run of this check
    against the pull-request body emitted a 0xa1 lead byte and its capture
    recorded `decode_result: replaced`. That is BP-01, the exact defect class this
    Slice ships tools to remove, appearing in the Slice's own gate instrument. The
    fix is the one the Slice's own P0-2 requires of its producer.
    """
    sys.stdout.buffer.write((line + chr(10)).encode("utf-8"))


REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

if len(sys.argv) != 3 or sys.argv[1] not in ("--range", "--file"):
    out("USAGE: closure-precheck.py --range <base>..<head> | --file <path>")
    raise SystemExit(2)

mode, target = sys.argv[1], sys.argv[2]

if mode == "--range":
    p = subprocess.run(["git", "log", "--format=%H%n%B%n---COMMIT-END---", target],
                       cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        out("GIT FAILED: %s" % p.stderr.decode("utf-8", "replace").strip())
        raise SystemExit(2)
    text = p.stdout.decode("utf-8", "replace")
    scope = "every commit message in %s (%d commits)" % (
        target, text.count("---COMMIT-END---"))
else:
    if not os.path.isfile(target):
        out("USAGE: no file at %s" % target)
        raise SystemExit(2)
    with open(target, "rb") as fh:
        text = fh.read().decode("utf-8", "replace")
    scope = "the file %s (%d bytes)" % (target, len(text.encode("utf-8")))

hits = list(PROHIBITED.finditer(text))
bare = list(BARE.finditer(text))


def context(m):
    return text[max(0, m.start() - 60):m.start() + 45].replace("\n", " ").strip()


out("check          : Gate 3 closure precondition (b), keyword half")
out("scope          : %s" % scope)
out("pattern        : a closing keyword IMMEDIATELY PRECEDING an issue reference")
out("keywords       : close/closes/closed, fix/fixes/fixed, resolve/resolves/resolved")
out("reference forms: #n | owner/repo#n | https://github.com/owner/repo/issues/n")
out()
out("PROHIBITED PATTERN matches   : %d" % len(hits))
for m in hits:
    out("   %r" % m.group(0))
    out("      %s" % context(m))
out()
out("bare keyword tokens          : %d  (NOT prohibited; printed so the count "
      "above states what it searched)" % len(bare))
for m in bare[:12]:
    out("   %-12r %s" % (m.group(0), context(m)))
if len(bare) > 12:
    out("   [... shown 12 of %d]" % len(bare))
out()
if hits:
    out("CLOSURE PRECONDITION (b) FAILS: the prohibited pattern is present")
    raise SystemExit(1)
out("CLOSURE PRECONDITION (b) HOLDS: no closing keyword immediately precedes "
      "an issue reference in the scope above")
