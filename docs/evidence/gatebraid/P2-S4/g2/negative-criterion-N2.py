#!/usr/bin/env python3
"""N2 - no fail-open on a verdict-relevant path.

THE PROPERTY.  Neither tool converts a non-zero subprocess exit, a caught
exception, or an absent field into a default, empty or absent value on any path
that can reach a verdict.

THE PATTERN THIS PROXIES FOR, and where the proxy over-matches (ADR-0018 §2).
The pattern is semantic - "a failure silently becomes a benign value" - and no
token search decides it.  This check searches three syntactic shapes that the
pattern reliably takes:

  N2a  a bare `except:` or an `except Exception:` whose handler neither
       re-raises nor makes an explicit fail-closed assignment;
  N2b  a `returncode` read that is not compared against anything;
  N2c  a `.get(` with a NON-None default on a verdict-relevant field name.

IT ERRS TOWARD FALSE POSITIVE, deliberately.  A legitimately handled exception
trips N2a; a `.get(` with a harmless default on a verdict-relevant name trips
N2c.  That is the safe direction: a missed fail-open IS the P0-1 defect, so the
check is built to over-report and be adjudicated rather than to under-report and
be trusted.  WHERE THE PROXY OVER-MATCHES, THE PATTERN GOVERNS - a match is a
question to answer in the record, not an automatic failure of the Slice.

SCOPE is an explicit path set, never "the added file" (friction #110):
`bin/gatebraid-snapshot.py` and `bin/gatebraid-frontier.py` - the two tools that
can reach a verdict.  The harness and the selftests are deliberately OUT of
scope: they emit no verdict, and including them would drown the signal in test
scaffolding.

Every match is PRINTED beside its count. A bare zero states what it searched
(friction #87).

Exit codes: 0 the criterion holds (no unadjudicated match) - 1 at least one
match stands - 2 the check could not run.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(HERE)))))

SCOPE = [
    os.path.join("bin", "gatebraid-snapshot.py"),
    os.path.join("bin", "gatebraid-frontier.py"),
]

# Field names whose value can reach a verdict. A default on any of these is the
# shape the criterion is about.
VERDICT_RELEVANT = (
    "status", "complete", "exit_code", "issue_state", "verdict", "workflow",
    "cross_check", "parse_status", "slice_metadata_present", "blocked_by",
    "blocking", "sources", "items",
)

BARE_EXCEPT = re.compile(r"^\s*except\s*:\s*$")
BROAD_EXCEPT = re.compile(r"^\s*except\s+Exception\b")
RETURNCODE = re.compile(r"\breturncode\b")
GET_DEFAULT = re.compile(r"\.get\(\s*[\"']([A-Za-z_]+)[\"']\s*,\s*([^)]+)\)")


def handler_body(lines, start):
    """The indented block belonging to the `except` at `start` (0-based)."""
    indent = len(lines[start]) - len(lines[start].lstrip())
    body = []
    for line in lines[start + 1:]:
        if not line.strip():
            body.append(line)
            continue
        if (len(line) - len(line.lstrip())) <= indent:
            break
        body.append(line)
    return body


def check_file(rel, findings):
    path = os.path.join(REPO, rel)
    if not os.path.isfile(path):
        raise SystemExit("N2 CANNOT RUN: %s is not present" % rel)
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    for i, line in enumerate(lines):
        if BARE_EXCEPT.match(line) or BROAD_EXCEPT.match(line):
            body = handler_body(lines, i)
            text = "\n".join(body)
            fail_closed = ("raise" in text) or ("return fail(" in text) \
                or ("SnapshotRefused" in text) or ("InputError" in text)
            if not fail_closed:
                findings.append(("N2a", rel, i + 1, line.strip(),
                                 "a broad handler that neither re-raises nor "
                                 "fails closed"))

        if RETURNCODE.search(line):
            compared = any(op in line for op in ("==", "!=", "<", ">", "if "))
            assigned_through = "exit_code=" in line or "exit_code =" in line
            if not (compared or assigned_through):
                findings.append(("N2b", rel, i + 1, line.strip(),
                                 "a returncode read that is neither compared "
                                 "nor carried into exit_code"))

        for match in GET_DEFAULT.finditer(line):
            field, default = match.group(1), match.group(2).strip()
            if field not in VERDICT_RELEVANT:
                continue
            if default in ("None",):
                continue
            findings.append(("N2c", rel, i + 1, line.strip(),
                             "a non-None default on the verdict-relevant field "
                             "%r" % field))


def main():
    findings = []
    for rel in SCOPE:
        check_file(rel, findings)

    print("criterion      : N2 - no fail-open on a verdict-relevant path")
    print("pattern proxied: a failure silently becoming a default, empty or "
          "absent value")
    print("errs toward    : FALSE POSITIVE (a missed fail-open is the defect "
          "itself)")
    print("scope          : an explicit path set, %d file(s)" % len(SCOPE))
    for rel in SCOPE:
        print("   %s" % rel.replace(os.sep, "/"))
    print("shapes searched:")
    print("   N2a  bare `except:` / `except Exception:` with no re-raise and no "
          "fail-closed assignment")
    print("   N2b  a `returncode` read that is not compared and not carried "
          "into exit_code")
    print("   N2c  `.get(` with a non-None default on a verdict-relevant field")
    print("verdict-relevant fields : %s" % ", ".join(VERDICT_RELEVANT))
    print()
    print("matches        : %d" % len(findings))
    for shape, rel, line_no, text, why in findings:
        print("   %-4s %s:%d  %s" % (shape, rel.replace(os.sep, "/"), line_no, why))
        print("        %s" % text)
    print()
    if findings:
        print("N2 DOES NOT HOLD: %d match(es) stand and each needs adjudication "
              "in the record" % len(findings))
        return 1
    print("N2 HOLDS: no fail-open shape found on any verdict-relevant path in "
          "the scope above")
    return 0


if __name__ == "__main__":
    sys.exit(main())
