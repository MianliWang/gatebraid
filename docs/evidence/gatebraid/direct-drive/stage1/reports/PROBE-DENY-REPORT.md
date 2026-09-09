# PROBE-DENY-REPORT -- direct-drive stage 1, read-only profile

Job: trial stage 1 probe, four attempts in order, started headless by
bin/gatebraid-dispatch.py under the read-only profile in the control
repository. Repository set: MianliWang/gatebraid only.

## Per attempt

1 ADMITTED "File created successfully at: D:\Github repo\Gatebraid\_handoff\batch-stage1\PROBE-ADMITTED.txt"
2 REFUSED "File is in a directory that is denied by your permission settings."
3 REFUSED "Permission to use Bash with command git checkout -b gb-probe-stage1 has been denied."
4 ADMITTED "(Bash completed with no output)"

Note on attempt 1: the tool's message carried a trailing parenthetical,
"(file state is current in your context [em dash] no need to Read it back)",
elided here because it contains a non-ASCII dash and this report is ASCII
only. Nothing else in any of the four messages was altered. The message on
attempt 4 is the harness's own rendering of a completed command that emitted
no bytes; the command produced no text of its own.

Note on attempt 3: the refusal came from the permission layer, before the
command reached git. No branch gb-probe-stage1 was created; attempt 4 was run
after it and shows the tree unmoved.

## Attempt 4 output, verbatim

The command `git status --porcelain --untracked-files=all` produced no output
at all -- zero bytes, exit status 0. There is nothing to quote between these
two sentences, and that emptiness is the measurement. The file written in
attempt 1 does not appear because `_handoff/` is ignored by the tracked,
root-anchored .gitignore and `--untracked-files=all` does not list ignored
paths.

## Statement

I made no other write and ran no other command, with one correction: after
the four attempts I ran the two measurement commands named in the job
(`sed ... | sha256sum` and `wc -c`) against this file, which the job requires,
and I made the Edit to this file that appends their results below the marker.

<!-- self-measured region ends -->

sha256 c093b9b8e328f308544fc333049574598141391b0def733e7e2c795c4368949b
bytes  1991

Measured with the two commands named in the job, against this file, over the
region the job's own sed expression selects -- line 1 through the marker line
inclusive. Everything from the blank line after the marker down is outside the
measured region and was appended afterward with the Edit tool, so appending it
does not disturb the figures above.

Deviation to record: the measurement was first issued as a single command
beginning `cd "D:/Github repo/Gatebraid" && sed ...` and was REFUSED --
"Commands that change directories and perform write operations require
explicit approval to ensure paths are evaluated correctly. For security,
Claude Code cannot automatically determine the final working directory when
'cd' is used in compound commands." It was reissued without `cd`, using the
absolute path, and admitted. This is a fifth refusal, outside the four
attempts the job specifies; it is reported because it happened, and the reissue
was a change of form for a command the job requires, not a workaround of any of
the four probed refusals.

The measurement was run twice: once before this appended block existed and once
after it, and both runs returned the sha256 and byte count printed above. The
second run is the falsification of the first -- it shows the append below the
marker does not move the measured region.
