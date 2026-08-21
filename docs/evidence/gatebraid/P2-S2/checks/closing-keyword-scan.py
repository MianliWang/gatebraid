#!/usr/bin/env python3
"""Closure precondition (b): closing-keyword scan (ADR-0012 §1 as amended by ADR-0018 §1).

Searches text for a CLOSING KEYWORD IMMEDIATELY PRECEDING AN ISSUE REFERENCE --
`keyword #n`, `keyword owner/repo#n`, `keyword <issue-url>`, any case, where
keyword is one of close/closes/closed, fix/fixes/fixed, resolve/resolves/resolved.

It tests the PATTERN, not the bare token, so a conventional-commit `fix(scope):`
prefix -- which references nothing -- is correctly not a match.

Two sources, either or both:
  --range A..B     every commit message (headline AND body) in that git range
  --text-file PATH one text file, e.g. the drafted pull-request body

It also reports PLAIN references (`Refs #n`, `Part of #n`, a bare issue URL),
which are permitted and are how a Slice issue is linked.

DEFUSING. A match is printed with the whitespace between the keyword and the
reference replaced by ` <<KEYWORD-REF>> `. A checker must never quote what it
forbids into a record in live form: this file's output is transcribed into
`gate3.md`, which is itself committed, and a live `keyword #n` reproduced there
would be exactly the string the check exists to keep out of the record set.
The count is authoritative; the defused text shows what was found.

Exit 0 = zero closing-keyword matches. Exit 1 = one or more, and the gate stops.
"""
import argparse
import re
import subprocess
import sys

KEYWORD = r"(?:clos(?:e|es|ed)|fix(?:|es|ed)|resolve(?:|s|d))"
REFERENCE = r"(?:\#[0-9]+|[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\#[0-9]+|https?://[^\s]*issues/[0-9]+)"
CLOSING = re.compile(KEYWORD + r"(\s+)" + REFERENCE, re.IGNORECASE)
PLAIN = re.compile(r"(?:refs|part of)\s+" + REFERENCE, re.IGNORECASE)


def defuse(match_text):
    """Break the keyword->reference adjacency so the record cannot carry a live one."""
    return CLOSING.sub(lambda m: m.group(0).replace(m.group(1), " <<KEYWORD-REF>> ", 1), match_text)


def git_log_messages(rng):
    out = subprocess.run(
        ["git", "log", "--format=%B", rng],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    )
    return out.stdout.decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--range", dest="rng", help="git range A..B; every commit message in it")
    ap.add_argument("--text-file", dest="text_file", help="one text file, e.g. the PR body")
    a = ap.parse_args()
    if not a.rng and not a.text_file:
        ap.error("give --range, --text-file, or both")

    sources, corpus = [], []
    if a.rng:
        text = git_log_messages(a.rng)
        n = len([c for c in subprocess.run(
            ["git", "log", "--format=%H", a.rng],
            stdout=subprocess.PIPE, check=True).stdout.decode().split() if c])
        sources.append("git range %s -- %d commit message(s), headline and body" % (a.rng, n))
        corpus.append(text)
    if a.text_file:
        with open(a.text_file, encoding="utf-8") as fh:
            text = fh.read()
        sources.append("text file %s -- %d byte(s)" % (a.text_file, len(text.encode("utf-8"))))
        corpus.append(text)

    blob = "\n".join(corpus)
    closing = [m.group(0) for m in CLOSING.finditer(blob)]
    plain = [m.group(0) for m in PLAIN.finditer(blob)]

    print("SEARCHED:")
    for s in sources:
        print("  " + s)
    print("PATTERN : keyword-then-reference, keyword in "
          "{close,closes,closed,fix,fixes,fixed,resolve,resolves,resolved}, any case;")
    print("          reference in {#n, owner/repo#n, <url ending issues/n>}.")
    print("          The bare token is NOT matched: a conventional-commit fix(scope): prefix")
    print("          references nothing and is not a match.")
    print("")
    print("CLOSING-KEYWORD MATCHES (defused for the record): %d" % len(closing))
    for m in closing:
        print("  " + defuse(m))
    if not closing:
        print("  (none -- the zero above is over the sources named at the top of this output)")
    print("")
    print("PLAIN REFERENCES (permitted; this is how a Slice issue is linked): %d" % len(plain))
    for m in sorted(set(plain)):
        print("  %d  %s" % (plain.count(m), m))
    if not plain:
        print("  (none)")
    print("")
    print("VERDICT: %s" % ("PASS -- no closing keyword precedes any issue reference"
                           if not closing else "FAIL -- a closing keyword precedes an issue reference"))
    return 1 if closing else 0


# Emit LF, not the platform line ending: this output is transcribed into a gate
# record that is committed under .gitattributes `* text=auto eol=lf`, and Windows
# newline translation would put CRLF into evidence bytes that are hashed.
try:
    sys.stdout.reconfigure(newline=chr(10))
except AttributeError:  # pragma: no cover - Python < 3.7
    pass


if __name__ == "__main__":
    sys.exit(main())
