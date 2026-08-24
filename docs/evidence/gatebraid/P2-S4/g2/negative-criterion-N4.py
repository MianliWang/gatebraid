#!/usr/bin/env python3
"""N4 - no verdict without validation.

THE PROPERTY.  `bin/gatebraid-frontier.py` emits no verdict for a document it
has not validated against `gatebraid/snapshot@1`.

TWO HALVES, as the frozen plan declares them.

  N4a  A SOURCE SCAN that every verdict-emitting path is dominated by the
       validation call.  The scan does not look for a call ordering, which is
       not decidable by search; it checks the STRUCTURE the tool uses to make
       the ordering unforgeable:
         1. `ValidatedSnapshot` is constructed in exactly ONE place;
         2. that place is lexically inside `def validate(`;
         3. the constructor refuses a wrong token, so no other site can build
            one;
         4. `consume(` - the only verdict emitter - takes that object.
       ERRS TOWARD FALSE POSITIVE: a refactor that renamed the type or split
       `validate` would trip this while remaining correct.  That is the safe
       direction, because the failure it guards against is a verdict emitted
       from an unvalidated document.

  N4b  A SEEDED BEHAVIOURAL RUN on frozen corpus material -
       `fixtures/state-pipeline/sp10-snapshot-missing-schema-key.json`, the
       fixture the frozen plan names - which must produce NO verdict: no report
       file, nothing on stdout, and exit 1.  This half is a direct behavioural
       test drawn from the corpus rather than an author-chosen input.

Every match is PRINTED beside its count.  A bare zero states what it searched
(friction #87).

Exit codes: 0 both halves hold - 1 either half fails - 2 the check could not run.
"""

import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SLICE_DIR = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(SLICE_DIR))))

FRONTIER = os.path.join(REPO, "bin", "gatebraid-frontier.py")
SP10 = os.path.join(REPO, "fixtures", "state-pipeline",
                    "sp10-snapshot-missing-schema-key.json")


def main():
    for required in (FRONTIER, SP10):
        if not os.path.isfile(required):
            print("N4 CANNOT RUN: required input not found at %s" % required)
            return 2

    with open(FRONTIER, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    findings = []

    # ---- N4a, the structural half ------------------------------------------
    construction_sites = [i for i, line in enumerate(lines)
                          if re.search(r"(?<![A-Za-z0-9_])ValidatedSnapshot\s*\(", line)
                          and not line.strip().startswith("class ")]
    # Which enclosing `def` each construction site sits in.
    def enclosing_def(index):
        for j in range(index, -1, -1):
            m = re.match(r"^def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", lines[j])
            if m:
                return m.group(1)
        return None

    enclosing = [enclosing_def(i) for i in construction_sites]
    if len(construction_sites) != 1:
        findings.append(("N4a", "construction sites",
                         "ValidatedSnapshot is constructed in %d place(s); the "
                         "guarantee needs exactly one"
                         % len(construction_sites),
                         "; ".join("line %d" % (i + 1) for i in construction_sites)))
    elif enclosing[0] != "validate":
        findings.append(("N4a", "line %d" % (construction_sites[0] + 1),
                         "the only construction site is inside %r, not "
                         "`validate`" % enclosing[0],
                         lines[construction_sites[0]].strip()))

    guarded = any("token is not _VALIDATION_TOKEN" in line for line in lines)
    if not guarded:
        findings.append(("N4a", "ValidatedSnapshot.__init__",
                         "the constructor does not refuse a wrong token, so the "
                         "type can be forged from anywhere", ""))

    consume_sig = [i for i, line in enumerate(lines)
                   if re.match(r"^def\s+consume\s*\(\s*snapshot\s*\)", line)]
    if not consume_sig:
        findings.append(("N4a", "consume()",
                         "the verdict emitter does not take a snapshot object "
                         "as its only argument", ""))

    # ---- N4b, the behavioural half on frozen corpus material ---------------
    tmp = tempfile.mkdtemp(prefix="n4-")
    out_path = os.path.join(tmp, "must-not-exist.json")
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([sys.executable, "-B", FRONTIER, SP10, "--out", out_path],
                          cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          env=env)
    wrote_file = os.path.isfile(out_path)
    wrote_stdout = len(proc.stdout) > 0
    if proc.returncode != 1:
        findings.append(("N4b", os.path.relpath(SP10, REPO).replace(os.sep, "/"),
                         "the consumer exited %d where a refusal is 1"
                         % proc.returncode, ""))
    if wrote_file:
        findings.append(("N4b", out_path, "a report file was written for a "
                                          "document that was never validated", ""))
    if wrote_stdout:
        findings.append(("N4b", "stdout", "%d byte(s) reached stdout for a "
                                          "document that was never validated"
                         % len(proc.stdout), ""))
    try:
        os.remove(out_path)
    except OSError:
        pass
    os.rmdir(tmp)

    print("criterion      : N4 - no verdict without validation")
    print("pattern proxied: a verdict emitted for a document that was never "
          "validated against gatebraid/snapshot@1")
    print("errs toward    : FALSE POSITIVE (a rename or a split of validate() "
          "trips the structural half)")
    print("scope          :")
    print("   bin/gatebraid-frontier.py                 (N4a, structural)")
    print("   fixtures/state-pipeline/sp10-snapshot-missing-schema-key.json "
          "(N4b, behavioural)")
    print()
    print("N4a measured:")
    print("   ValidatedSnapshot construction sites : %d" % len(construction_sites))
    for i, site in enumerate(construction_sites):
        print("      line %-5d inside %s()" % (site + 1, enclosing[i]))
    print("   constructor refuses a wrong token    : %s" % guarded)
    print("   consume() takes the validated object : %s" % bool(consume_sig))
    print()
    print("N4b measured on %s:"
          % os.path.relpath(SP10, REPO).replace(os.sep, "/"))
    print("   exit status                          : %d (a refusal is 1)"
          % proc.returncode)
    print("   report file written                  : %s" % wrote_file)
    print("   bytes reaching stdout                : %d" % len(proc.stdout))
    print()
    print("matches        : %d" % len(findings))
    for shape, where, why, text in findings:
        print("   %-4s %s  %s" % (shape, where, why))
        if text:
            print("        %s" % text)
    print()
    if findings:
        print("N4 DOES NOT HOLD: %d match(es) stand and each needs adjudication "
              "in the record" % len(findings))
        return 1
    print("N4 HOLDS: the validated type is unforgeable and constructed only in "
          "validate(), and the corpus fixture the plan names produces no verdict")
    return 0


if __name__ == "__main__":
    sys.exit(main())
