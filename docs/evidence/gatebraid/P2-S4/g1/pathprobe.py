"""Does the declared output path denote the same file on both platform halves?

Slice A froze `> /tmp/snap.json ... open('/tmp/snap.json')`, correct on Linux and
wrong on `environment: windows`, where the shell and the interpreter disagree
about what `/tmp` means. It passed by reading and could not be repaired at
Gate 2 because the plan was frozen.

Every declared command in this plan writes under
`docs/evidence/gatebraid/P2-S4/acceptance/`, a repository-relative path. This
probe is run once per half: `write` stamps the file with the half's name,
`read` reports what the other half left there. Run write on one half and read
on the other, both ways, and the two halves are shown to agree about what the
path denotes -- measured, not argued.
"""
import pathlib, sys

REL = "docs/evidence/gatebraid/P2-S4/acceptance/.pathprobe"
mode = sys.argv[1]
half = sys.argv[2]
p = pathlib.Path(REL)

print("cwd            :", pathlib.Path.cwd())
print("relative path  :", REL)
print("resolves to    :", p.resolve())

if mode == "write":
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("written-by-" + half + "\n", encoding="utf-8", newline="\n")
    print("wrote          : written-by-" + half)
elif mode == "read":
    if not p.exists():
        print("MISSING        : the other half's write is not visible at this path")
        sys.exit(1)
    print("read back      :", p.read_text(encoding="utf-8").strip())
elif mode == "remove":
    if p.exists():
        p.unlink()
    print("removed        :", not p.exists())
else:
    print("usage: pathprobe.py write|read|remove <half>")
    sys.exit(2)
