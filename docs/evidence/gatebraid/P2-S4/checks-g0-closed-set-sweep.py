"""Gate 0 closed-set sweep, complement method, over EVERY captured response.

The packet's section 2 makes any identifier outside its table a STOP and a
finding, and its touch-vs-mention ruling makes tool self-describing output a
mention rather than a touch. Extraction is deliberately over-sensitive: every
owner/repo-shaped token, every PVT*-node id, and every bare issue reference,
across each capture's stdout, stderr, recorded invocation and notes.

Every candidate is then classified by an EXPLICIT rule. The sweep passes only
if the unexplained residue is empty. No forbidden name is looked up; the method
needs only the permitted set, which is why it also catches a seventh name.

Pass 1 of this sweep (capture G0-closed-set-sweep-pass1.json) ran with an
incomplete rule set and returned 39 candidates, exit 1. That run is retained
deliberately: it is this instrument's own falsification. A sweep that has only
ever returned empty has never been shown able to fire.
"""
import base64, collections, glob, json, os, re, sys

CAPDIR = "docs/evidence/gatebraid/P2-S4/captures"

PERMITTED_REPOS = {"MianliWang/gatebraid", "MianliWang/gatebraid-scratch"}
PERMITTED_PROJECT = "PVT_kwHOBRofUs4Beum7"
PERMITTED_ITEM = "PVTI_lAHOBRofUs4Beum7zg3ogLM"
SUBJECT_ISSUE = 14
# Packet section 2 names these and marks them mention-class: no query targets them.
MENTION_CLASS_ISSUES = {6, 7, 8, 10, 12, 13, 15}
SEEDED_PROBES = {1, 99, 999999}          # deliberately nonexistent, inside the permitted repo
GH_OWN_RELEASE_HOST = {"cli/cli"}        # gh --version prints its own release URL

REPO = re.compile(r"(?<![A-Za-z0-9_./-])([A-Za-z0-9][A-Za-z0-9_.-]{0,38}/[A-Za-z0-9][A-Za-z0-9_.-]{0,60})")
NODE = re.compile(r"PVT[A-Za-z]*_[A-Za-z0-9_-]+")
ISSUE = re.compile(r"(?<![A-Za-z0-9_])#(\d+)")
FRICTION = re.compile(r"friction\s+#(\d+)", re.I)

REF_NAMESPACE = re.compile(r"^refs/[a-z]+$")
FS_PREFIX = {
    "docs", "fixtures", "schema", "bin", "protocols", "templates", "adr",
    "evidence", "projects", "consults", "captures", "Users", "AppData",
    "Roaming", "npm", "mnt", "usr", "tmp", "Program Files",
}
URL_PREFIX = {"https:", "http:", "api.github.com", "github.com",
              "json-schema.org", "objects.githubusercontent.com"}
SCHEMA_NS = {"gatebraid"}
JSON_POINTER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*/\d+$")     # write_domains/0
PROSE_PAIR = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.\-]*/[A-Za-z0-9][A-Za-z0-9.\-]*$")


def classify_repo(tok, where):
    parts = tok.split("/")
    if tok in PERMITTED_REPOS:
        return "E1 permitted repository", tok
    if tok in GH_OWN_RELEASE_HOST:
        return "E2 gh's own release URL (tool self-describing: mention, not touch)", None
    if parts[0] == "repos":
        # fragment of an API path repos/<owner>/<repo>/...; the real identity is resolved
        return "E3 API-path fragment", None
    if REF_NAMESPACE.match(tok):
        return "E4 git ref namespace, not a repository", None
    if parts[0] in FS_PREFIX or parts[0] in URL_PREFIX:
        return "E5 filesystem or URL path segment", None
    if parts[0] in SCHEMA_NS:
        return "E6 schema-id namespace", None
    if JSON_POINTER.match(tok):
        return "E7 JSON pointer", None
    if PROSE_PAIR.match(tok):
        return "E8 prose slash between ordinary words", None
    return "UNEXPLAINED", None


def texts(path):
    d = json.load(open(path, encoding="utf-8"))
    for stream in ("stdout", "stderr"):
        s = d.get("streams", {}).get(stream, {})
        if s.get("data"):
            yield stream, base64.b64decode(s["data"]).decode("utf-8", "replace")
    yield "invocation", json.dumps(d.get("invocation", {}))
    if d.get("notes"):
        yield "notes", d["notes"]


buckets = collections.Counter()
repos = collections.Counter()
issue_where = collections.defaultdict(set)
residue = []

ALL = sorted(glob.glob(os.path.join(CAPDIR, "*.json")))
# A checker does not audit its own report, and its report is not a response
# from the closed set. Excluding it also removes a self-reference loop of the
# IN-03 class (a detector re-detecting tokens it printed itself).
SELF = [f for f in ALL if os.path.basename(f).startswith("G0-closed-set-sweep")]
files = [f for f in ALL if f not in SELF]
for f in files:
    base = os.path.basename(f)
    for where, t in texts(f):
        frictions = {int(m.group(1)) for m in FRICTION.finditer(t)}
        for m in REPO.finditer(t):
            tok = m.group(1)
            kind, ident = classify_repo(tok, where)
            buckets[kind] += 1
            if ident:
                repos[ident] += 1
            if kind == "UNEXPLAINED":
                residue.append((base, where, "repo", tok))
        for m in NODE.finditer(t):
            n = m.group(0)
            if n == PERMITTED_PROJECT:
                buckets["N1 the permitted Project"] += 1
            elif n == PERMITTED_ITEM:
                buckets["N2 the P2-S4 item"] += 1
            elif n.startswith(("PVTF_", "PVTSSF_")):
                buckets["N3 field id of the permitted Project"] += 1
            elif n.startswith(PERMITTED_PROJECT + "_SEEDED"):
                buckets["N4 seeded-invalid probe string (selector falsification)"] += 1
            else:
                residue.append((base, where, "node", n))
        for m in ISSUE.finditer(t):
            n = int(m.group(1))
            if n in frictions:
                buckets["I0 friction citation, not an issue reference"] += 1
                continue
            issue_where[n].add(where)
            if n == SUBJECT_ISSUE:
                buckets["I1 the subject issue"] += 1
            elif n in SEEDED_PROBES:
                buckets["I2 seeded-nonexistent probe in the permitted repo"] += 1
            elif n in MENTION_CLASS_ISSUES:
                buckets["I3 mention-class (packet section 2)"] += 1
            else:
                residue.append((base, where, "issue", "#%d" % n))

print("captures swept : %d" % len(files))
print()
print("=== candidate classification (every rule applied explicitly) ===")
for k, v in sorted(buckets.items()):
    print("  %-58s %d" % (k, v))
print()
print("=== every REPOSITORY identity named anywhere ===")
for k, v in sorted(repos.items()):
    print("  %-30s x%-4d %s" % (k, v, "PERMITTED" if k in PERMITTED_REPOS else "*** OUTSIDE ***"))
print()
print("=== mention-class check: a mention must never appear in an INVOCATION ===")
bad_mention = []
for n in sorted(issue_where):
    if n in MENTION_CLASS_ISSUES:
        w = issue_where[n]
        targeted = "invocation" in w
        print("  #%-6d seen in %-28s targeted by a query: %s" % (n, ",".join(sorted(w)), targeted))
        if targeted:
            bad_mention.append(n)
            residue.append(("(mention)", "invocation", "issue", "#%d" % n))
print("  mention-class issues targeted by a query: %d (0 required)" % len(bad_mention))
print()
print("domain      : %d captures (%d of this sweep's own reports excluded)"
      % (len(files), len(SELF)))
print("UNEXPLAINED RESIDUE: %d" % len(residue))
# ADR-0028 section 3: reported by kind and location, never by echoing the token.
for base, where, kind, _token in residue:
    print("    %-44s %-12s %s" % (base, where, kind))
sys.exit(1 if residue else 0)
