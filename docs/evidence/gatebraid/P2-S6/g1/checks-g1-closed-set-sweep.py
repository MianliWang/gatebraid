"""Gate 0 closed-set sweep, complement method, over EVERY captured response.

The standing rule makes any owner/repo identifier outside the permitted set a
STOP and a finding. Extraction is deliberately over-sensitive: every
owner/repo-shaped token, every PVT*-node id, and every bare issue reference,
across each capture's stdout, stderr, recorded invocation and notes.

Every candidate is then classified by an EXPLICIT rule. The sweep passes only
if the unexplained residue is empty. No forbidden name is looked up; the method
needs only the permitted set, which is why it also catches a seventh name.

Two differences from the P2-S4 original, both widening the domain rather than
narrowing it:

  1. Documents in the captures directory that are not evidence-capture@1 — the
     snapshot and frontier documents this gate produced — are swept over their
     raw text. The original's reader yielded only capture-shaped fields, so a
     non-capture document would have been swept as an empty invocation and
     passed vacuously. A sweep that cannot see a file it is pointed at is not a
     sweep over that file.
  2. The subject issue is 17 and the mention class carries 14 and 16, which
     were subject and PR of the preceding Slice.

Residue is reported by kind and location, never by echoing the token
(ADR-0028 section 3). The sweep excludes its own reports, a self-reference of
the IN-03 class.
"""
import base64, collections, glob, json, os, re, sys

# The domain defaults to this gate's captures. It is overridable ONLY so the
# same instrument — not a copy of it — can be pointed at a seeded domain and
# shown able to fire. A sweep that has only ever returned empty has never been
# falsified. The seeded run is retained beside the real one.
CAPDIR = sys.argv[1] if len(sys.argv) > 1 else "docs/evidence/gatebraid/P2-S6/g1"

PERMITTED_REPOS = {"MianliWang/gatebraid", "MianliWang/gatebraid-scratch"}
PERMITTED_PROJECT = "PVT_kwHOBRofUs4Beum7"
PERMITTED_ITEM = "PVTI_lAHOBRofUs4Beum7zg4gxqQ"
SUBJECT_ISSUE = 19
# Issues and PRs of the permitted repository that this Slice's own body and
# evidence name but no query in this gate targets.
MENTION_CLASS_ISSUES = {6, 7, 8, 10, 12, 13, 14, 15, 16, 17, 18}
SEEDED_PROBES = set()                    # this gate ran no nonexistent-issue seed
GH_OWN_RELEASE_HOST = {"cli/cli"}        # gh --version prints its own release URL

REPO = re.compile(r"(?<![A-Za-z0-9_./-])([A-Za-z0-9][A-Za-z0-9_.-]{0,38}/[A-Za-z0-9][A-Za-z0-9_.-]{0,60})")
NODE = re.compile(r"PVT[A-Za-z]*_[A-Za-z0-9_-]+")
ISSUE = re.compile(r"(?<![A-Za-z0-9_])#(\d+)")
FRICTION = re.compile(r"friction\s+#(\d+)", re.I)

REF_NAMESPACE = re.compile(r"^refs/[a-z]+$")
FS_PREFIX = {
    "docs", "fixtures", "schema", "bin", "protocols", "templates", "adr",
    "evidence", "projects", "consults", "captures", "Users", "AppData",
    "Roaming", "npm", "mnt", "usr", "tmp", "Program Files", "_handoff",
    "Python312", "Github repo", "lib", "etc", "var",
    "Files",      # "D:/Program Files/Git/..." splits at the space, so the
                  # token is Files/Git: a filesystem segment, never an owner
    "repo",       # "D:\Github repo\Gatebraid" splits at its space the same
                  # way, giving repo/Gatebraid: the same class as Files/Git
    "g1",         # this Slice's own Gate 1 evidence subdirectory
    "properties", # a JSON Schema pointer segment printed by the corpus runner,
                  # e.g. properties/items/items/properties/workflow/type
    "ndocs",      # a Python bytes repr renders a newline as a backslash-n
                  # immediately before a path, so the payload-bytes line of
                  # the allowlist hash yields ndocs joined to evidence
    "tags",       # CPython banner "3.12.2 (tags/v3.12.2:...)": a git tag ref
                  # fragment inside an interpreter version string
}
URL_PREFIX = {"https:", "http:", "api.github.com", "github.com",
              "json-schema.org", "objects.githubusercontent.com"}
SCHEMA_NS = {"gatebraid"}
JSON_POINTER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*/\d+$")     # write_domains/0

# E8 is an EXPLICIT allowlist, not a pattern.
#
# Pass 1 of this sweep carried the P2-S4 original's PROSE_PAIR regex here:
#     ^[A-Za-z0-9][A-Za-z0-9.\-]*/[A-Za-z0-9][A-Za-z0-9.\-]*$
# which matches essentially every `owner/repo` token. Falsification against a
# seeded domain proved the consequence: the seeded out-of-set REPOSITORY
# identifier was classified E8 and never reached the residue, so the sweep's
# repository limb could not fire at all. The node and issue limbs did fire.
# Pass 1 is retained at captures/G0-closed-set-sweep-pass1.json and its seeded
# run at captures/G0-closed-set-sweep-falsify-pass1.json.
#
# The complement method requires every candidate to be explained by an explicit
# rule; a regex that swallows the very shape being hunted is not one. The two
# prose pairs actually present in this gate's domain are named here, and
# anything else of that shape is residue.
PROSE_PAIRS = {
    "ADR-0014/0016",      # an ADR citation naming two numbers
    "snapshot/frontier",  # the O0 tool pair, written as a pair in prose
    "15/15",              # a ratio in the P2-S6 issue body prose
    "incomplete/bounded", # two ordinary words, slashed, in the same body
    "Gate-1/Gate-2",      # prose in a frozen corpus case name, printed by the
                          # corpus runner and quoted into this gate's record
}


def classify_repo(tok, where):
    parts = tok.split("/")
    if tok in PERMITTED_REPOS:
        return "E1 permitted repository", tok
    if tok in GH_OWN_RELEASE_HOST:
        return "E2 gh's own release URL (tool self-describing: mention, not touch)", None
    if parts[0] == "repos":
        return "E3 API-path fragment", None
    if REF_NAMESPACE.match(tok):
        return "E4 git ref namespace, not a repository", None
    if parts[0] in FS_PREFIX or parts[0] in URL_PREFIX:
        return "E5 filesystem or URL path segment", None
    if parts[0] in SCHEMA_NS:
        return "E6 schema-id namespace", None
    if JSON_POINTER.match(tok):
        return "E7 JSON pointer", None
    if tok in PROSE_PAIRS:
        return "E8 prose slash between ordinary words (named, not matched)", None
    return "UNEXPLAINED", None


def texts(path):
    """Yield (where, text) for a document, capture-shaped or not."""
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception:
        yield "raw", open(path, encoding="utf-8", errors="replace").read()
        return
    if d.get("schema") == "gatebraid/evidence-capture@1":
        for stream in ("stdout", "stderr"):
            s = d.get("streams", {}).get(stream, {})
            if s.get("data"):
                yield stream, base64.b64decode(s["data"]).decode("utf-8", "replace")
        yield "invocation", json.dumps(d.get("invocation", {}))
        if d.get("notes"):
            yield "notes", d["notes"]
    else:
        # snapshot / frontier documents: sweep the whole text (difference 1)
        yield "document", json.dumps(d)


buckets = collections.Counter()
repos = collections.Counter()
issue_where = collections.defaultdict(set)
residue = []

if os.path.isfile(CAPDIR):
    # A single document may be swept directly. The gate's own record is the
    # document that would be committed, and the P2-S4 original's domain — the
    # captures directory only — never covered it.
    ALL = [CAPDIR]
else:
    ALL = sorted(glob.glob(os.path.join(CAPDIR, "*.json")))
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
                buckets["N2 this Slice's own Project item"] += 1
            elif n.startswith(("PVTF_", "PVTSSF_")):
                buckets["N3 field id of the permitted Project"] += 1
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
                buckets["I3 mention-class"] += 1
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
print("domain      : %d documents (%d of this sweep's own reports excluded)"
      % (len(files), len(SELF)))
print("UNEXPLAINED RESIDUE: %d" % len(residue))
for base, where, kind, _token in residue:
    print("    %-44s %-12s %s" % (base, where, kind))
sys.exit(1 if residue else 0)
