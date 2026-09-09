#!/usr/bin/env python3
"""Stage-1 channel probe, class (c) measurements (ADR-0035 decision 6a).

Read-only. Prints, one per line:
  which <tool> <path or None>          for python, claude, git, gh (shutil.which)
  version <tool> <text>                for python (sys.version) and claude (--version)
  processes claude <count>             image name claude.exe, from tasklist
  scratch <dir> outside-every-repo <bool>   no .git in the dir or any parent
  cwd <path>
  env GH_CONFIG_DIR <value>  env PYTHONDONTWRITEBYTECODE <value>
Spawns exactly two subprocesses: `<claude> --version` (the version query
contract section 9 requires) and `tasklist` (a listing). Writes nothing.
Never runs git or gh.
"""
import os
import pathlib
import shutil
import subprocess
import sys


def main(argv):
    scratch = argv[1] if len(argv) > 1 else "D:/gb-scratch-stage1"
    for tool in ("python", "claude", "git", "gh"):
        print("which %s %s" % (tool, shutil.which(tool)))
    print("version python %s" % sys.version.replace("\n", " "))
    claude = shutil.which("claude")
    if claude:
        done = subprocess.run([claude, "--version"], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        print("version claude %s (exit %d)" % (
            done.stdout.decode("utf-8", "replace").strip(), done.returncode))
    else:
        print("version claude None")
    try:
        done = subprocess.run(["tasklist", "/FI", "IMAGENAME eq claude.exe", "/NH"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        lines = [l for l in done.stdout.decode("utf-8", "replace").splitlines()
                 if l.strip().lower().startswith("claude.exe")]
        print("processes claude %d" % len(lines))
    except OSError as exc:
        print("processes claude unmeasured (%s)" % exc.__class__.__name__)
    p = pathlib.Path(scratch)
    chain = [p] + list(p.parents)
    repos = [str(q) for q in chain if (q / ".git").exists()]
    print("scratch %s outside-every-repo %s%s" % (
        scratch, "True" if not repos else "False",
        "" if not repos else " (.git at: %s)" % ", ".join(repos)))
    print("cwd %s" % os.getcwd())
    print("env GH_CONFIG_DIR %s" % os.environ.get("GH_CONFIG_DIR"))
    print("env PYTHONDONTWRITEBYTECODE %s" % os.environ.get("PYTHONDONTWRITEBYTECODE"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
