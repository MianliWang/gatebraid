"""Every prose claim repair 2 touches or creates, re-measured against the tree.

The mandatory lesson of P2-S6's repair 1: the class that fails records is "a
statement the file makes about itself going false". A repair that corrects five
such statements is exactly the place a sixth is born, so this instrument
enumerates the claims and measures each one rather than asserting it.

It is READ-ONLY: it writes no file and mutates nothing. It runs AFTER the record
commit, so the file and the repository it measures are the ones a reviewer will
see. Exit 0 = every claim holds. Exit 1 = at least one does not.
"""
import base64, hashlib, io, json, os, re, subprocess, sys

G2 = "docs/evidence/gatebraid/P2-S5/g2"
CAPS = G2 + "/captures"
RECORD = G2 + "/gate2.md"
TOOL = "bin/gatebraid-ready.py"
PY = sys.executable

FP_HEAD = "5b586029344eb6df4a964c34baa1eb12e2916f6d"
FP_TREE = "f696944947a342b6163bf4ad7d9137674830a2f7"
BASE = "cbd065893b37f20713ae35b8d2673bf26fe4d2ad"

PINS = {
    "docs/evidence/gatebraid/P2-S5/gate0.md":
        "be7c338896b1015923671988166d55af3bd59e028660ce89dfd3b69bc7251513",
    "docs/evidence/gatebraid/P2-S5/g0r/gate0.md":
        "95ff39111b4a8b8aa43c022e877c98af5f868b054f4ac2c116ae5c67327bc4e6",
    "docs/evidence/gatebraid/P2-S5/g1/gate1.md":
        "78a3f94a2a8b23efb1e36b231ce8932b1c693fa79dee5f657ae5968d29943c70",
}
RETAINED_DIGEST = "83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f"

rows = []


def claim(cid, text, want, got):
    rows.append((cid, text, want, got, "HOLDS" if want == got else "FALSE"))


def sh(argv):
    p = subprocess.run(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.returncode, p.stdout, p.stderr


def cap(cid):
    return json.load(io.open(os.path.join(CAPS, cid + ".json"), encoding="utf-8"))


def stream(d, name):
    s = d.get("streams", {}).get(name, {})
    return base64.b64decode(s["data"]).decode("utf-8", "replace") if s.get("data") else ""


def rendered_lines(d):
    out = stream(d, "stdout").replace(chr(13), "")
    err = stream(d, "stderr").replace(chr(13), "")
    c = out.rstrip("\n")
    if err.strip():
        c = c + "\n" + err.rstrip("\n")
    return c.split("\n") if c else []


body = io.open(RECORD, encoding="utf-8").read()

# (a) the declared option surface is the frozen two flags
src = io.open(TOOL, encoding="utf-8").read()
flags = sorted(set(re.findall(r'"(--[a-z-]+)"', src)))
claim("a1", "the tool's source declares exactly the two frozen flags",
      ["--snapshot-command", "--strict"], flags)
claim("a2", "no residual reference to the removed flags or their support code",
      0, len(re.findall(r"VERSION|args\.consumer|consumer_path", src)))

# (b) removed flags are usage errors; --help still exits 0
for f in ("--version", "--consumer"):
    st, out, err = sh([PY, "-B", TOOL, f])
    claim("b:%s" % f, "%s is a usage error with exit 12 and empty stdout" % f,
          (12, 0), (st, len(out)))
st, out, err = sh([PY, "-B", TOOL, "--help"])
claim("b:help", "--help exits 0 and prints usage naming both frozen flags",
      (0, True, True),
      (st, b"--strict" in out, b"--snapshot-command" in out))

# (c) the composition paths still behave as declared
for cid, want in (("G2-D3-selftest-windows", 0), ("G2-D4-selftest-wsl", 0),
                  ("G2-D5-live-ready", 0), ("G2-D6-producer-failure", 10),
                  ("G2-D7-decode-guard", 11), ("G2-D8-consumer-refusal", 1)):
    claim("c:%s" % cid, "the row's captured exit is what the plan declares",
          want, cap(cid)["exit_code"])

# (d) V9 is excluded and its six verdicts hold
claim("d1", "V9 is named in the exclusion list, not the subset",
      True, "V9 and V9b, for F-02's reason" in body)
claim("d2", "no sentence still claims V9 reproduces",
      0, len(re.findall(r"V9 \(pinned\)|so the row reproduces", body)))
t = stream(cap("G2-D9-negative-pinned"), "stdout")
claim("d3", "the pinned run's six verdicts hold",
      True, "NEGATIVE CRITERIA HOLD: N1, N2, N3, N4, N5, N6" in t)

# (f)(g) every residue figure in prose equals the cited row's
sw = stream(cap("G2-closed-set-sweep"), "stdout")
total = int([l for l in sw.splitlines() if l.startswith("UNEXPLAINED RESIDUE:")][0].split(":")[1])
rowlines = []
seen = False
for l in sw.splitlines():
    if l.startswith("UNEXPLAINED RESIDUE:"):
        seen = True
        continue
    if seen and l.startswith("    ") and l.strip():
        rowlines.append(l.split())
issue = sum(1 for r in rowlines if r[-1] == "issue")
inpass = sum(1 for r in rowlines if "-pass" in r[0])
m = re.search(r"reports (\d+) residue occurrences\. (\d+) of them are the", body)
claim("f1", "the prose total and issue-kind split equal the cited row's",
      (str(total), str(issue)), (m.group(1), m.group(2)) if m else None)
m2 = re.search(r"The other (\d+) are", body)
claim("f2", "the prose remainder equals the row's", str(total - issue),
      m2.group(1) if m2 else None)
m3 = re.search(r"(\d+) of the (\d+) sit inside superseded", body)
claim("f3", "the prose -pass count equals the row's",
      (str(inpass), str(total)), (m3.group(1), m3.group(2)) if m3 else None)
claim("g1", "the sweep check is still typed fail and cites ruling F-08",
      True, "Typed fail under operator ruling F-08" in body)

# (h) every printed elision total equals the rule applied to its capture
bad = []
for mm in re.finditer(r"\[\.\.\. shown (\d+) of (\d+) lines; full output: ([^\]]+)\]", body):
    shown, tot, path = int(mm.group(1)), int(mm.group(2)), mm.group(3)
    cid = os.path.basename(path)[:-5]
    if len(rendered_lines(cap(cid))) != tot:
        bad.append((cid, tot, len(rendered_lines(cap(cid)))))
claim("h1", "every elision total equals the stated rule over its capture", [], bad)
claim("h2", "the D5 elision reads 20 of 195", True,
      "shown 20 of 195 lines" in body)

# (i) every elision target is a forward-slash committed path
paths = re.findall(r"full output: ([^\]]+)\]", body)
claim("i1", "no elision path carries a backslash", 0,
      sum(1 for p in paths if chr(92) in p))
missing = [p for p in set(paths)
           if subprocess.run(["git", "cat-file", "-e", "HEAD:" + p],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL).returncode != 0]
claim("i2", "every elision path is tracked at HEAD", [], missing)

# (j) every deviation bullet carries a citation
dev = [l for l in body.split("\n") if l.startswith("- Deviations")]
CITE = re.compile(r"friction #\d+|ruling|ADR-\d{4}|finding F-\d\d|Plan Approval|"
                  r"gate-2-contract|P1-S3")
uncited = [l[:70] for l in dev if not CITE.search(l)]
claim("j1", "every deviation bullet cites a finding, ruling or friction entry",
      [], uncited)

# (k)(l) the record's own sweep and validation, over these very bytes
claim("k1", "the record's own closed-set sweep returns residue 0",
      0, cap("G2-record-sweep")["exit_code"])
claim("l1", "the record validates accepted on the Windows half", True,
      "verdict       : accepted" in stream(cap("G2-record-validation"), "stdout"))
claim("l2", "the record validates accepted on the WSL half", True,
      "verdict       : accepted" in stream(cap("G2-D11-wsl-toolchain"), "stdout"))

# the fingerprint trio, and the four ride-on pins
st, out, _ = sh(["git", "rev-parse", FP_HEAD + "^{tree}"])
claim("m1", "the recorded tree_sha is the fingerprint commit's tree",
      FP_TREE, out.decode().strip())
claim("m2", "the record's metadata names that fingerprint head", True,
      FP_HEAD in body and FP_TREE in body)
for p, want in PINS.items():
    claim("p:%s" % os.path.basename(os.path.dirname(p) + "/" + os.path.basename(p)),
          "the ride-on pin %s is unchanged" % p, want,
          hashlib.sha256(io.open(p, "rb").read()).hexdigest())
retained = []
for dirpath, dirnames, filenames in os.walk("docs/evidence/gatebraid/P2-S5"):
    dirnames[:] = [d for d in dirnames if d not in ("g0r", "g1", "g2")]
    for fn in filenames:
        retained.append(os.path.join(dirpath, fn).replace(os.sep, "/"))
retained.sort()
claim("p:digest", "the retained-set path-list digest is unchanged", RETAINED_DIGEST,
      hashlib.sha256(("\n".join(retained) + "\n").encode("utf-8")).hexdigest())

print("%-14s %-62s %-10s %s" % ("claim", "statement", "verdict", "measured"))
failed = 0
for cid, text, want, got, verdict in rows:
    if verdict == "FALSE":
        failed += 1
    shown = got if verdict == "FALSE" else "as stated"
    print("%-14s %-62s %-10s %s" % (cid, text[:62], verdict, str(shown)[:60]))
print()
print("claims measured : %d" % len(rows))
print("claims FALSE    : %d" % failed)
if failed:
    print("CLAIM RECHECK FAILED: the record states something its own tree denies")
    sys.exit(1)
print("CLAIM RECHECK CLEAN: every claim this repair touches or creates holds "
      "against the committed tree")
