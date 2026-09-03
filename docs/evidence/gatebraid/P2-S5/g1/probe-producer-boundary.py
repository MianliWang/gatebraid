"""Gate 1 dry-run probe: the T1 producer boundary, exercised WITHOUT the deliverable.

This is NOT `bin/gatebraid-ready.py` and is not a draft of it. It has no command
line, composes nothing with the consumer, and implements no exit algebra. It
exists to answer one question action 4 asks and inspection cannot: are the parts
of the declared D6 and D7 commands RUNNABLE ON THIS HOST, or merely well-formed
on the page? Slice A's frozen plan passed by reading and failed at Gate 2, which
is why this is measured instead.

It performs, once each, exactly the three boundary steps T1 declares:

  1. launch the producer as a subprocess and capture its stdout AS BYTES;
  2. read the producer's exit status against the space the producer itself
     declares (the D-4 rule), rather than testing it against zero;
  3. decode those bytes as UTF-8 EXPLICITLY and strictly, never guessing.

and reports what each produced. Three producers are used: the real hardened
producer on an input error, the real hardened producer on a live degraded read,
and the cp936 stub whose bytes are the pair that broke the M2 pipeline.

Read-only: it writes no file and mutates nothing. Exit 0 = every boundary step
behaved as the plan declares. Exit 1 = at least one did not, in which case the
plan is wrong and must be corrected BEFORE the freeze - which is the whole point
of running it now.
"""
import subprocess, sys

PRODUCER = "bin/gatebraid-snapshot.py"

# The producer's own declared space, transcribed from its module docstring and
# checked against it by negative criterion N6 rather than trusted here.
DOCUMENT_EXISTS = {0, 3}          # 0 healthy, 3 emitted and DEGRADED
NO_DOCUMENT = {1, 2}              # 1 nothing could be produced, 2 usage or input

Q = chr(34)
CP936_TEXT = "{" + Q + "name" + Q + ": " + Q + "Gate 0 " + chr(0x2014) + \
             " Verifying" + Q + "}"
CP936_STUB = "import sys;sys.stdout.buffer.write(%r.encode(%r))" \
             % (CP936_TEXT, "cp936")

failures = []


def run(label, argv, expect):
    """One boundary crossing, reported by what it produced."""
    p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    raw = p.stdout
    print("--- %s" % label)
    print("    producer exit status : %d" % p.returncode)
    if p.returncode in DOCUMENT_EXISTS:
        verdict = "a document exists; the composer passes it on"
    elif p.returncode in NO_DOCUMENT:
        verdict = "no document exists; the composer exits 10"
    else:
        verdict = "UNDECLARED status; the composer exits 10"
    print("    D-4 reading          : %s" % verdict)
    print("    stdout bytes captured: %d" % len(raw))
    if raw:
        print("    first 48 bytes       : %r" % raw[:48])
    try:
        raw.decode("utf-8")
        decode = "ok"
        print("    strict UTF-8 decode  : ok")
    except UnicodeDecodeError as exc:
        decode = "refused"
        print("    strict UTF-8 decode  : REFUSED - %s" % exc)
        print("    the composer exits 11 and never guesses an encoding")
    got = (verdict.split(";")[0], decode)
    if got != expect:
        failures.append((label, got, expect))
        print("    NOT AS DECLARED      : got %r, plan declares %r" % (got, expect))
    print()


print("probe: the T1 producer boundary, without the program under test")
print("producer            : %s" % PRODUCER)
print("interpreter         : %s" % sys.executable)
print()

run("R1 real producer, input error (the declared D6 producer)",
    [sys.executable, "-B", PRODUCER, "--replay",
     "docs/evidence/gatebraid/P2-S5/g1/dryrun-out/no-such-transcript.json"],
    ("no document exists", "ok"))

run("R2 real producer, degraded live read (the D-4 case)",
    [sys.executable, "-B", PRODUCER, "--project", "999"],
    ("a document exists", "ok"))

run("R3 cp936 stub, the bytes that broke the M2 pipeline (the declared D7 producer)",
    [sys.executable, "-c", CP936_STUB],
    ("a document exists", "refused"))

print("boundary steps not as declared: %d" % len(failures))
for label, got, expect in failures:
    print("   %s: got %r, plan declares %r" % (label, got, expect))
print()
if failures:
    print("PROBE FAILED: the plan declares behaviour this host does not produce")
    sys.exit(1)
print("PROBE CLEAN: every declared boundary step ran here and behaved as the plan "
      "declares")
