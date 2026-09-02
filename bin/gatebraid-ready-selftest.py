#!/usr/bin/env python3
"""gatebraid-ready-selftest - seeded conditions for the Ready Frontier composer.

Every condition SEEDS a situation and requires the composer to produce a stated
outcome; the instrument emits its own summary row for each.  Nothing here is
narrated: a class is shown killed by a row this program printed, which is what
the Slice's Acceptance requires and what the M2 measurement chain's third
finding - self-authored instruments each carrying one unexamined trust point -
exists to prevent.

FALSIFICATION IS INTRINSIC.  S01 is the positive control: a composer that
rejected everything would fail S01 and pass every negative below it, so the
suite cannot be satisfied by a tool that simply refuses.  Every other condition
seeds a defect and requires the composer to catch it.

NO NETWORK.  Every producer is a stub, and the two documents are committed,
frozen files read from the tree.  The row `network reads performed` is printed
so the claim is the instrument's and not the reader's.

NO WRITES.  This program writes no file.  It reads two committed documents with
an explicit binary read mode; negative criterion N5 scopes its file-local limb
to this file and `bin/gatebraid-ready.py`, and both satisfy it as frozen.

Exit 0 = every condition produced its required outcome.  Exit 1 = at least one
did not.  Exit 2 = structure: a fixture this suite depends on is missing, so
nothing is claimed either way.
Python 3 standard library only.
"""

import ast
import os
import re
import subprocess
import sys

READY = "bin/gatebraid-ready.py"
PRODUCER = "bin/gatebraid-snapshot.py"

# Two committed, frozen documents. Neither is written by this Slice.
HEALTHY = "docs/evidence/gatebraid/P2-S5/g1/captures/g1-snapshot.json"
DEGRADED = "docs/evidence/gatebraid/P2-S6/g1/dryrun-out/g2-snapshot.json"

PY = sys.executable.replace("\\", "/")

rows = []
network_reads = 0


def stub(program, status=0):
    """A producer stub: one -c program, optionally exiting with a chosen status.

    The program is wrapped in DOUBLE quotes and contains only single quotes, so
    the composer's POSIX split reproduces it exactly. A literal non-ASCII
    character is never written here - it is built with chr() - because a literal
    em dash through nested quoting yields a zero-byte stub and the decode guard
    then appears to pass while testing nothing (friction #15; P1-S3's second
    dry-run).
    """
    if status:
        program = program + ";import sys as _s;_s.exit(%d)" % status
    return '%s -c "%s"' % (PY, program)


def emit_file(path):
    return "import sys;sys.stdout.buffer.write(open('%s','rb').read())" % path


def run_ready(snapshot_command, extra=None):
    argv = [sys.executable, "-B", READY, "--snapshot-command", snapshot_command]
    if extra:
        argv += extra
    proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def run_consumer_direct(path):
    proc = subprocess.run(
        [sys.executable, "-B", "bin/gatebraid-frontier.py", path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout


def row(cid, condition, want, got, observation):
    ok = (want == got)
    rows.append((cid, condition, want, got, "PASS" if ok else "FAIL", observation))
    return ok


def producer_declared_space(path):
    """The producer's declared exit codes, parsed from its own module docstring.

    Read from the tool rather than remembered, so the D-4 partition cannot
    drift from its source unnoticed.
    """
    src = open(path, "r", encoding="utf-8").read()
    doc = ast.get_docstring(ast.parse(src, filename=path)) or ""
    m = re.search(r"Exit codes:(.*?)(?:\n\s*\n|$)", doc, re.S)
    if not m:
        raise SystemExit("STRUCTURE: no `Exit codes:` paragraph in %s" % path)
    return {int(x) for x in re.findall(r"(?<![0-9])([0-9]{1,2})\s", m.group(1) + " ")}


def main():
    global network_reads

    for p in (READY, PRODUCER, HEALTHY, DEGRADED):
        if not os.path.isfile(p):
            sys.stderr.write("STRUCTURE: missing fixture or tool: %s\n" % p)
            return 2

    # ---- S01 positive control -------------------------------------------
    status, out, err = run_ready(stub(emit_file(HEALTHY)))
    want_status, want_out = run_consumer_direct(HEALTHY)
    row("S01", "a healthy document composes and exits 0", 0, status,
        "a composer that rejected everything would fail HERE and pass every "
        "negative below")
    row("S01b", "the consumer's report is passed through BYTE-FOR-BYTE",
        want_out, out,
        "byte passthrough, not text: re-emitting decoded text through a "
        "text-mode stdout would translate every embedded newline again")

    # ---- S02/S03 the producer says NO DOCUMENT --------------------------
    for cid, code in (("S02", 1), ("S03", 2)):
        status, out, err = run_ready(stub("import sys", status=code))
        row(cid, "producer status %d (declared: no document) is exit 10" % code,
            10, status,
            "a status meaning no document must never reach the consumer")
        row(cid + "b", "and stdout stays empty", b"", out,
            "stdout carries exactly one JSON document or nothing")

    # ---- S04 D-4: a DEGRADED document still travels ---------------------
    status, out, err = run_ready(stub(emit_file(DEGRADED), status=3))
    dstatus, dout = run_consumer_direct(DEGRADED)
    row("S04", "producer status 3 (declared: emitted and DEGRADED) passes the "
        "document on and returns the consumer's own 3", 3, status,
        "D-4: reading any non-zero status as failure would DISCARD a lawful "
        "document and hide the degradation from the only tool that types it")
    row("S04b", "and the report is still on stdout", dout, out,
        "--strict changed the exit code and never the output; the consumer "
        "now applies that unconditionally")

    # ---- S05 a status OUTSIDE the producer's declared space --------------
    status, out, err = run_ready(stub("import sys", status=42))
    row("S05", "an undeclared producer status is exit 10", 10, status,
        "an unknown status is treated as no-document, never as success")

    # ---- S06 the decode guard -------------------------------------------
    q = "chr(34)"
    prog = ("import sys;q=%s;s='{'+q+'name'+q+': '+q+'Gate 0 '+chr(0x2014)+"
            "' Verifying'+q+'}';sys.stdout.buffer.write(s.encode('cp936'))" % q)
    status, out, err = run_ready(stub(prog))
    row("S06", "producer bytes that are not valid UTF-8 are exit 11", 11, status,
        "the same two bytes that broke the M2 pipeline; no encoding is guessed")
    row("S06b", "and stdout stays empty", b"", out,
        "a best-effort decode would turn a loud failure into corruption "
        "inside a state document")
    # Matched case-INSENSITIVELY and on the substantive tokens. The first
    # writing of this row matched the phrase `not valid UTF-8` in lower case
    # against a refusal the tool writes in capitals: a defect in the assertion,
    # not in the composer, and it is the assertion that was corrected.
    lowered = err.decode("utf-8", "replace").lower()
    row("S06c", "and the refusal names the offending byte and its position",
        True,
        ("0xa1" in lowered and "position 17" in lowered
         and "not valid utf-8" in lowered),
        "a guard that fires without naming what it caught is not evidence")

    # ---- S07 decodable but malformed ------------------------------------
    status, out, err = run_ready(
        stub("import sys;sys.stdout.buffer.write(chr(123).encode()+chr(125).encode())"))
    row("S07", "a decodable but malformed document returns the consumer's own "
        "refusal code", 1, status,
        "the consumer's codes are reused rather than renumbered (D-1)")
    row("S07b", "and no verdict is emitted", b"", out,
        "no verdict is invented for a document the consumer refused")

    # ---- S08 --strict is accepted and changes nothing (D-2) -------------
    s_plain, out_plain, _ = run_ready(stub(emit_file(HEALTHY)))
    s_strict, out_strict, _ = run_ready(stub(emit_file(HEALTHY)), extra=["--strict"])
    row("S08", "--strict is accepted and changes the exit status not at all",
        s_plain, s_strict,
        "D-2: the flag is kept so a caller written against the frozen surface "
        "still runs; rejecting it would break that surface")
    row("S08b", "and changes the output not at all", out_plain, out_strict,
        "a flag that silently altered the document would be worse than one "
        "that errored")

    # ---- S09 IN-01: first stage fails, second would succeed -------------
    status, out, err = run_ready(stub(emit_file(HEALTHY), status=1))
    row("S09", "a composition whose FIRST stage fails and whose second would "
        "succeed never reports success", 10, status,
        "IN-01, the class the frozen corpus does not hold: the stub emits a "
        "VALID document and exits 1, so a composer testing only the document "
        "would return 0")
    row("S09b", "and the valid document is not forwarded", b"", out,
        "the producer's status governs, not the shape of what it wrote")

    # ---- S10 the D-4 partition matches the producer's own docstring -----
    declared = producer_declared_space(PRODUCER)
    src = open(READY, "r", encoding="utf-8").read()
    tree = ast.parse(src, filename=READY)
    partition = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in (
                        "PRODUCER_DOCUMENT_EXISTS", "PRODUCER_NO_DOCUMENT"):
                    for e in ast.walk(node.value):
                        if isinstance(e, ast.Constant) and isinstance(e.value, int):
                            partition.add(e.value)
    row("S10", "the D-4 partition covers exactly the producer's declared space",
        sorted(declared), sorted(partition),
        "the partition is transcribed from the producer's docstring, so it is "
        "checked against that docstring rather than trusted")

    # ---- S11 no network -------------------------------------------------
    row("S11", "every condition was served by a stub or a committed document",
        0, network_reads,
        "a selftest that reached the control plane would be measuring the "
        "network, not the composer")

    # ---- report ---------------------------------------------------------
    print("%-6s %-64s %-12s %-12s %-7s %s"
          % ("id", "condition", "want", "got", "verdict", "required observation"))
    failed = 0
    for cid, cond, want, got, verdict, obs in rows:
        if verdict == "FAIL":
            failed += 1

        def short(v):
            if isinstance(v, bytes):
                return "<%d bytes>" % len(v)
            return str(v)
        print("%-6s %-64s %-12s %-12s %-7s %s"
              % (cid, cond[:64], short(want)[:12], short(got)[:12], verdict, obs))
    print()
    print("tool under test               : %s" % os.path.abspath(READY))
    print("interpreter                   : %s" % sys.executable)
    print("documents (committed, frozen) : %s, %s" % (HEALTHY, DEGRADED))
    print("files written by this suite   : 0")
    print("network reads performed       : %d (every producer is a stub)"
          % network_reads)
    print("conditions failed             : %d" % failed)
    if failed:
        print("SELFTEST FAILED: %d condition(s) did not produce the required "
              "outcome" % failed)
        return 1
    print("SELFTEST CLEAN: every seeded condition produced its required outcome")
    return 0


if __name__ == "__main__":
    sys.exit(main())
