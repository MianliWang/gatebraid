"""The frozen-scope pin, re-derivable. Python 3 standard library only.

The Slice body says the scope is READ at Gate 1 from the M2 slice-C historical
record and NEVER re-derived from memory, and that the plan pins it by hash. A
pin nobody can recompute is decoration, so this instrument is the pin: it reads
each document from the historical repository at a NAMED COMMIT and prints the
sha256 of the bytes it received, beside the value frozen here.

It is READ-ONLY. It performs no write of any kind, and every read is addressed
to one named repository inside the permitted closed set - it enumerates nothing.

Exit 0 = the commit and every document hash re-derive equal. Exit 1 = at least
one differs or is absent, which means the pin does not describe what is there.
Exit 2 = structure: the named commit could not be resolved at all, so nothing is
claimed either way.

  --commit <sha>   read at this commit instead of the frozen one

That override exists for ONE reason: so the SAME instrument - not a copy of it -
can be pointed at a commit the pin does NOT describe and be shown able to fire.
A pin that has only ever matched has never been falsified (spec section 4,
friction #111). An ABSENT document is a FINDING and not a crash, because a
document missing at the pinned commit is exactly what a stale pin looks like.
"""
import argparse, hashlib, subprocess, sys

REPO = "MianliWang/gatebraid-scratch"

# The commit the scope was read at. Named, not "the tip": a pin to a moving ref
# is not a pin (spec section 4, ADR-0028 section 2).
COMMIT = "dcd8e851bb508a2e17a6949434fc7c10354506c1"

# Every document read at this gate, with the sha256 of the bytes received.
# P1-S3, P1-S5 and P1-S6 are the three M2 slice-C attempts; each carries the
# gate0 record that entered it and the gate1 record that froze its plan.
DOCUMENTS = [
    ("README.md",
     "e0a5b2689f0e9f08f680077c5cd29f9a1f0f230c78260c39b10542cdf690c730"),
    ("docs/evidence/gatebraid/P1-S3/gate0.md",
     "cc783192e688e677a18d49febedc1cfb1174c8e875056062284d7b7d4e242f81"),
    ("docs/evidence/gatebraid/P1-S3/gate1.md",
     "0966759be9e1b05fea310965e6ac36112244185f6434647bb3f1ec2ed32b21cb"),
    ("docs/evidence/gatebraid/P1-S5/gate0.md",
     "a0fd819614744faf9317f84f4b6532e249fe32c3d35307dabd28160cd356d145"),
    ("docs/evidence/gatebraid/P1-S5/gate1.md",
     "edfc92054015b7190ba79eb94c9da114ce0eec4714acdd3b301628550ee74f33"),
    ("docs/evidence/gatebraid/P1-S6/gate0.md",
     "89af2e287272947f307b2f72d9541e481c508c9e90c6d99cd994061282698c5c"),
    ("docs/evidence/gatebraid/P1-S6/gate1.md",
     "b190299bccaa906548d44477eca18e5579cbb480e4192c52fba5f801bd71920f"),
]

# The two facts of the frozen scope that the plan's D-1 and D-2 deltas turn on,
# asserted against the bytes rather than against a reading of them. Both are
# present in ALL THREE attempts, which is what makes the scope one scope.
SCOPE_ASSERTIONS = [
    ("bin/gatebraid-ready.py", "the one file the scope delivers"),
    ("--snapshot-command", "the flag whose stated reason is that the guard "
                           "paths must be runnable, not merely asserted"),
    ("--strict", "the flag the M2 consumer accepted"),
]
SCOPE_DOCS = ["docs/evidence/gatebraid/P1-S3/gate1.md",
              "docs/evidence/gatebraid/P1-S5/gate1.md",
              "docs/evidence/gatebraid/P1-S6/gate1.md"]


def read(path, ref):
    r = subprocess.run(
        ["gh", "api", "-H", "Accept: application/vnd.github.raw",
         "repos/%s/contents/%s?ref=%s" % (REPO, path, ref)],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        return None
    return r.stdout


def resolved_commit(ref):
    r = subprocess.run(
        ["gh", "api", "repos/%s/commits/%s" % (REPO, ref), "--jq", ".sha"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r.returncode != 0:
        raise SystemExit("STRUCTURE: the named commit could not be resolved "
                         "(exit %d)" % r.returncode)
    return r.stdout.decode("utf-8").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", default=COMMIT)
    args = ap.parse_args()
    ref = args.commit

    print("historical record : %s" % REPO)
    print("pinned commit     : %s" % COMMIT)
    print("reading at        : %s%s"
          % (ref, "" if ref == COMMIT else "   (OVERRIDDEN - falsification run)"))
    got = resolved_commit(ref)
    ok_commit = (got == COMMIT)
    print("resolves to       : %s  %s"
          % (got, "MATCH" if ok_commit else "*** NOT THE PINNED COMMIT ***"))
    print()

    bodies = {}
    bad = []
    print("%-46s %-8s %s" % ("document", "bytes", "sha256 re-derived"))
    for path, want in DOCUMENTS:
        raw = read(path, ref)
        if raw is None:
            print("%-46s %-8s %s" % (path, "-", "*** ABSENT AT THIS COMMIT ***"))
            bad.append(path)
            continue
        bodies[path] = raw
        got = hashlib.sha256(raw).hexdigest()
        mark = "MATCH" if got == want else "*** DIFFERS ***"
        print("%-46s %-8d %s  %s" % (path, len(raw), got, mark))
        if got != want:
            bad.append(path)
    print()

    print("scope assertions, each required in ALL THREE attempts:")
    for token, why in SCOPE_ASSERTIONS:
        present = [d for d in SCOPE_DOCS
                   if token.encode("utf-8") in bodies.get(d, b"")]
        ok = len(present) == len(SCOPE_DOCS)
        print("   %-24s in %d of %d  %-5s  %s"
              % (token, len(present), len(SCOPE_DOCS),
                 "ok" if ok else "FAIL", why))
        if not ok:
            bad.append("scope assertion %s" % token)
    print()

    if not ok_commit or bad:
        print("SCOPE PIN STALE: %d item(s) did not re-derive"
              % (len(bad) + (0 if ok_commit else 1)))
        return 1
    print("SCOPE PIN HOLDS: the commit resolves and every document re-derives "
          "to the frozen hash")
    return 0


if __name__ == "__main__":
    sys.exit(main())
