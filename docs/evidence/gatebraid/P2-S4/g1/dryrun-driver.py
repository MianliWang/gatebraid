"""Gate 1 Action 4 -- dry-run every declared test command on the declared environment.

`environment: mixed-see-prose` means the gate runs on the Windows host with the
WSL half as evidence, so a command declared for both halves is run on both.

THE GREENFIELD PROBLEM, STATED RATHER THAN GLOSSED. Three of this Slice's four
tasks deliver tools that do not exist yet, so a declared command against them
cannot exit 0 today. Action 4 exists to catch the Slice A defect -- a command
well-formed on inspection that cannot run *there* -- so each such command is
dry-run in two parts:

  RUN   the command exactly as declared. Expected today: a non-zero exit whose
        message names the declared target as absent, and nothing else wrong.
  TWIN  the same interpreter, the same repository-relative path form, the same
        shell, against a file that DOES exist. Expected: exit 0.

A twin that passes while the run reports only "target absent" shows the
invocation form resolves on this environment; the sole remaining unknown is the
file this Slice will write. Slice A's defect would fail the twin, because its
path form was wrong for the platform rather than merely unpopulated.

Commands whose targets exist today are run once, plainly, with no twin needed.
"""
import subprocess, sys

WINPY = "C:/Python312/python.exe"
ROOT_WSL = "/mnt/d/Github repo/Gatebraid"


def win(args):
    return [WINPY, "-B"] + args


def wsl(argstr):
    return ["wsl", "-e", "bash", "-lc",
            "cd '%s' && PYTHONDONTWRITEBYTECODE=1 python3 -B %s" % (ROOT_WSL, argstr)]


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def show(tag, cmd, rc, out, want):
    lines = [l for l in out.splitlines() if l.strip()]
    keep = lines[-3:] if lines else ["(no output)"]
    print("%-46s exit=%-4d %s" % (tag, rc, want))
    print("   $ %s" % " ".join(cmd))
    for l in keep:
        print("     %s" % l[:110])


# (tag, command, kind) -- kind: "live" runs today; "absent" is a declared
# command whose target this Slice will write; "twin" is its form probe.
CASES = [
    ("D1a snapshot selftest, windows", win(["bin/gatebraid-snapshot-selftest.py"]), "absent"),
    ("D1a TWIN form, windows", win(["bin/gatebraid-capture-selftest.py", "--help"]), "twin"),
    ("D1b snapshot selftest, wsl", wsl("bin/gatebraid-snapshot-selftest.py"), "absent"),
    ("D1b TWIN form, wsl", wsl("bin/gatebraid-capture-selftest.py --help"), "twin"),
    ("D2a frontier selftest, windows", win(["bin/gatebraid-frontier-selftest.py"]), "absent"),
    ("D2b frontier selftest, wsl", wsl("bin/gatebraid-frontier-selftest.py"), "absent"),
    ("D3a acceptance induced-failures, windows",
     win(["bin/gatebraid-o0-acceptance.py", "--induced-failures",
          "--out", "docs/evidence/gatebraid/P2-S4/acceptance/induced.json"]), "absent"),
    ("D3b acceptance induced-failures, wsl",
     wsl("bin/gatebraid-o0-acceptance.py --induced-failures "
         "--out docs/evidence/gatebraid/P2-S4/acceptance/induced.json"), "absent"),
    ("D4 acceptance dependency-directions, windows",
     win(["bin/gatebraid-o0-acceptance.py", "--dependency-directions",
          "--out", "docs/evidence/gatebraid/P2-S4/acceptance/deps.json"]), "absent"),
    ("D5 acceptance byte-contract, windows",
     win(["bin/gatebraid-o0-acceptance.py", "--byte-contract",
          "--out", "docs/evidence/gatebraid/P2-S4/acceptance/bytes.json"]), "absent"),
    ("D6a corpus, windows", win(["bin/gatebraid-validate.py", "--corpus", "fixtures"]), "live"),
    ("D6b corpus, wsl", wsl("bin/gatebraid-validate.py --corpus fixtures"), "live"),
    ("D7 corpus digest unmoved, windows", win(["fixtures/runner-selftest.py"]), "live-slow"),
    ("D8 freeze precedes implementation",
     ["git", "merge-base", "--is-ancestor",
      "df666070ead7fa21bc72b6c99d2644923b37e787", "HEAD"], "live"),
]

SKIP_SLOW = "--skip-slow" in sys.argv

print("declared-command dry-run matrix")
print("=" * 110)
absent_ok = twin_ok = live_ok = 0
absent_n = twin_n = live_n = 0
bad = []
for tag, cmd, kind in CASES:
    if kind == "live-slow" and SKIP_SLOW:
        print("%-46s SKIPPED by --skip-slow (run separately; see D7 capture)" % tag)
        continue
    rc, out = run(cmd)
    if kind == "absent":
        absent_n += 1
        names_target = ("No such file" in out or "can't open file" in out
                        or "cannot find" in out.lower())
        good = rc != 0 and names_target
        absent_ok += good
        show(tag, cmd, rc, out, "want: non-zero naming the declared target absent -> %s"
             % ("as expected" if good else "*** UNEXPECTED ***"))
        if not good:
            bad.append(tag)
    elif kind == "twin":
        twin_n += 1
        good = rc == 0
        twin_ok += good
        show(tag, cmd, rc, out, "want: exit 0 -> %s" % ("form resolves here" if good else "*** FORM BROKEN ***"))
        if not good:
            bad.append(tag)
    else:
        live_n += 1
        good = rc == 0
        live_ok += good
        show(tag, cmd, rc, out, "want: exit 0 -> %s" % ("green" if good else "*** FAILED ***"))
        if not good:
            bad.append(tag)
    print()

print("=" * 110)
print("declared commands with a live target : %d run, %d green" % (live_n, live_ok))
print("declared commands this Slice will write: %d run, %d failed only on target-absent" % (absent_n, absent_ok))
print("form twins                            : %d run, %d resolved on this environment" % (twin_n, twin_ok))
print("unexpected results                    : %d" % len(bad))
for b in bad:
    print("   ", b)
sys.exit(1 if bad else 0)
