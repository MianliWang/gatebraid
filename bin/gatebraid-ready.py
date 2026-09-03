#!/usr/bin/env python3
"""gatebraid-ready - the Ready Frontier composer (M3 node O1).

Composes the released producer with the released consumer and passes the
consumer's verdict through on stdout.  It consumes both published tools and
MODIFIES NEITHER.  Stdout is always exactly one JSON document or nothing;
every diagnostic goes to stderr.

This is the M2 slice-C frozen scope, delivered on the M3 stack.  Four deltas
separate that scope from the tools it now composes; each applies a frozen rule
to the tools AS MEASURED rather than re-deciding the scope, and all four are
ratified in the Plan Approval on the Slice issue.

D-1  THE CONSUMER'S CODE SPACE MOVED.  The frozen rule is that the consumer's
     own codes are reused rather than renumbered, so a caller already reading
     them is not surprised, and that this tool's own codes sit OUTSIDE that
     space so they cannot be confused with a verdict.  The M2 consumer declared
     {0, 2, 3}.  The hardened consumer declares {0, 1, 2, 3}.  The rule did not
     change; the set it ranges over is the consumer's.

D-2  --strict HAS NO FORWARDEE.  The hardened consumer accepts no such flag:
     every verdict being `undecidable` is exit 3 unconditionally, so what
     --strict used to select is now the consumer's only behaviour.  The flag is
     accepted and forwards nothing.  Rejecting it would break the frozen
     surface for a caller written against it; forwarding it would make the
     consumer exit 2 on every invocation carrying it.

D-3  THE DEFAULT PRODUCER COMMAND CANNOT NAME `python`.  On the Windows half of
     the declared environment `python` is the MSYS build, which carries no
     `jsonschema`, and the producer validates its own output against the frozen
     schema before emitting.  The default is the interpreter running THIS
     program, which is the same resolution on both declared platforms and names
     no host-specific absolute path.

D-4  THE PRODUCER'S STATUS IS INTERPRETED, NOT TESTED AGAINST ZERO.  The
     hardened producer declares 3 for `snapshot emitted and DEGRADED` - a real,
     well-formed document the consumer is built to classify.  A composer that
     read any non-zero status as failure would DISCARD A LAWFUL DOCUMENT and
     hide the degradation from the only tool that can type it.  So: a status
     meaning a document exists passes the document on; a status meaning no
     document exists is EXIT_PRODUCER_FAILED.

THE ENCODING CONTRACT, WHICH IS THE POINT OF THE EXIT-11 GUARD
--------------------------------------------------------------
The producer's stdout is captured as BYTES and decoded as UTF-8 EXPLICITLY and
strictly.  It is never decoded through an inherited console text layer and an
encoding is NEVER guessed: a consumer that guesses turns a loud failure into
silent corruption inside a state document, which is worse than stopping.  A
decode failure is a REFUSAL with its own exit status and its own message.

Friction #60 - the defect this guard was written for - is closed at the root by
the producer's own byte contract, so the guard can no longer be provoked by the
DEFAULT producer.  That is not a reason to drop it.  It is precisely why the
frozen scope carries --snapshot-command, whose stated reason is that without it
the producer-failure and decode-guard paths cannot be run, only asserted.

Exit codes: 0, 1, 2 and 3 are the CONSUMER'S OWN, passed through unchanged - 10
the producer reported no document - 11 the producer's bytes are not valid UTF-8
- 12 usage error in this program's own arguments.  10, 11 and 12 sit outside
both composed tools' declared spaces, which negative criterion N6 checks against
those tools' own docstrings rather than against a remembered list.
Python 3 standard library only.
"""

import argparse
import subprocess
import sys

# This program's OWN exit codes.  Every one sits outside both composed tools'
# declared spaces; N6 is the check, and it reads those spaces from the tools.
EXIT_PRODUCER_FAILED = 10
EXIT_PRODUCER_UNDECODABLE = 11
EXIT_USAGE = 12

# The producer's declared status space, transcribed from its module docstring:
#   0 snapshot emitted, every source `ok` and complete
#   1 no document could be produced (self-validation failed)
#   2 usage or input error
#   3 snapshot emitted and DEGRADED
# The partition below is the D-4 rule.  A selftest condition asserts that the
# union of these two sets equals the space the producer's own docstring
# declares, so this transcription cannot drift from its source unnoticed.
PRODUCER_DOCUMENT_EXISTS = frozenset((0, 3))
PRODUCER_NO_DOCUMENT = frozenset((1, 2))

PRODUCER_PATH = "bin/gatebraid-snapshot.py"
CONSUMER_PATH = "bin/gatebraid-frontier.py"


def default_snapshot_command():
    """D-3: the interpreter running this program, never the bare name `python`.

    The interpreter path is written with forward slashes.  That is not
    cosmetic: the command is split by POSIX rules (see split_command), under
    which a backslash is an escape, and `C:\\Python312\\python.exe` would split
    to `C:Python312python.exe`.  Both interpreters of the declared environment
    accept forward slashes.
    """
    return "%s -B %s" % (sys.executable.replace("\\", "/"), PRODUCER_PATH)


def split_command(command):
    """Split the producer command with POSIX quoting rules on every platform.

    MEASURED, not assumed.  With `posix=False` - the tempting choice on
    Windows - shlex leaves the quotes attached to the token, so
    `-c "import sys;..."` arrives at the child as a program whose first
    character is a quote.  The child then emits ZERO BYTES and the decode
    guard appears to pass while testing nothing: friction #15's shape, and the
    exact failure P1-S3's second dry-run recorded before this scope was first
    frozen.  POSIX rules split it correctly, at the price of treating a
    backslash as an escape - which is why the default above uses forward
    slashes and why this docstring says so rather than leaving it to be
    rediscovered.
    """
    import shlex
    return shlex.split(command, posix=True)


def _binary_stdout():
    stream = getattr(sys.stdout, "buffer", None)
    if stream is None:
        raise RuntimeError(
            "STRUCTURE: stdout has no binary layer; the byte passthrough this "
            "program's contract rests on cannot be performed")
    return stream


def run_producer(command):
    """Launch the producer and capture its stdout AS BYTES.

    Returns (status, raw_bytes, raw_stderr).  The command is split with the
    platform's own rules so a caller may pass either the default or a stub.
    """
    argv = split_command(command)
    if not argv:
        raise ValueError("the producer command is empty")
    proc = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def run_consumer(document_bytes):
    """Feed the document to the consumer on stdin and return (status, out, err).

    The consumer reads `-` as stdin and decodes UTF-8 explicitly itself, so the
    byte contract holds on both sides of this boundary.
    """
    proc = subprocess.run(
        [sys.executable, "-B", CONSUMER_PATH, "-"],
        input=document_bytes, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout, proc.stderr


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="gatebraid-ready",
        description="Compose the snapshot producer with the frontier consumer "
                    "and emit the Ready Frontier verdict. Stdout carries "
                    "exactly one JSON document or nothing.",
        epilog="Exit codes: 0, 1, 2 and 3 are the CONSUMER'S OWN and are passed "
               "through unchanged; 10 the producer reported no document; 11 the "
               "producer's output is not valid UTF-8; 12 a usage error here.")
    ap.add_argument(
        "--strict", action="store_true",
        help="ACCEPTED AND FORWARDS NOTHING. The consumer no longer takes this "
             "flag: it exits 3 whenever every verdict is `undecidable`, "
             "unconditionally, which is what --strict used to select. The flag "
             "is kept so a caller written against the frozen surface still "
             "runs, and this text says plainly that it changes nothing.")
    ap.add_argument(
        "--snapshot-command", metavar="CMD", default=None,
        help="the producer to run (default: this interpreter against %s). It "
             "exists so the producer-failure and decode-guard paths can be RUN "
             "rather than asserted." % PRODUCER_PATH)

    try:
        args = ap.parse_args(argv)
    except SystemExit as exc:
        # argparse exits 2 on a usage error, which is inside the consumer's
        # declared space and would be indistinguishable from a verdict.
        if exc.code in (0, None):
            raise
        sys.stderr.write("USAGE: bad arguments to gatebraid-ready\n")
        return EXIT_USAGE

    command = args.snapshot_command or default_snapshot_command()

    try:
        status, raw, producer_err = run_producer(command)
    except (OSError, ValueError) as exc:
        sys.stderr.write("USAGE: the producer command could not be run: %s\n"
                         % exc)
        return EXIT_USAGE

    if producer_err:
        sys.stderr.write(producer_err.decode("utf-8", "replace"))

    # D-4: interpret the status, never test it against zero.
    if status not in PRODUCER_DOCUMENT_EXISTS:
        why = ("declared status meaning no document"
               if status in PRODUCER_NO_DOCUMENT
               else "status outside the producer's declared space")
        sys.stderr.write(
            "PRODUCER REPORTED NO DOCUMENT: exit %d (%s); nothing is emitted "
            "and no verdict is invented\n" % (status, why))
        return EXIT_PRODUCER_FAILED

    # The encoding contract.  Decode EXPLICITLY and strictly; never guess.
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        sys.stderr.write(
            "PRODUCER OUTPUT IS NOT VALID UTF-8: %s\n"
            "The offending byte is at position %d. No encoding is guessed: a "
            "best-effort decode would turn this loud failure into corruption "
            "inside a state document.\n" % (exc, exc.start))
        return EXIT_PRODUCER_UNDECODABLE

    # For any input the guard admits, this re-encoding is byte-identical to the
    # bytes captured; the decode is the GUARD and the bytes are the payload.
    document = text.encode("utf-8")
    if document != raw:
        sys.stderr.write(
            "STRUCTURE: the UTF-8 round trip is not byte-identical; refusing "
            "to forward a document this program cannot reproduce\n")
        return EXIT_PRODUCER_UNDECODABLE

    try:
        consumer_status, out, err = run_consumer(document)
    except OSError as exc:
        sys.stderr.write("USAGE: the consumer could not be run: %s\n" % exc)
        return EXIT_USAGE

    if err:
        sys.stderr.write(err.decode("utf-8", "replace"))

    # Byte passthrough.  Re-emitting decoded text through a text-mode stdout
    # would translate each embedded newline again; this is load-bearing on the
    # declared Windows host today, not future-proofing.
    stream = _binary_stdout()
    stream.write(out)
    stream.flush()

    # The consumer's own status, passed through unchanged (D-1).
    return consumer_status


if __name__ == "__main__":
    sys.exit(main())
