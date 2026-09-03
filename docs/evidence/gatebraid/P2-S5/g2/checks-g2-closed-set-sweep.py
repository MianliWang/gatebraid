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

GATE 2 COPY. This file is a copy of the Gate 1 instrument
docs/evidence/gatebraid/P2-S5/g1/checks-g1-closed-set-sweep.py (sha256
467790e297c0a89df354455a17a255cdf6fab357b40fd141ebae9a548aef89f8), which Gate
1's captures pin by hash and which therefore rides onto the branch
byte-identical and is NOT edited. The Gate 0 and Gate 0 re-run copies are
likewise untouched.

THIS HEADER DESCRIBES ONLY WHAT THIS FILE'S BYTES CARRY. The Gate 1 copy's
header named a PROSE_PAIRS addition its bytes did not carry; the approval noted
it, left that copy as it stands because its capture pins it, and required this
one to describe itself accurately. Every item below is present in the code.

FOUR groups differ from the Gate 1 copy, all of them DOMAIN FACTS, none of them
a rule. No classification rule, no regex and no residue criterion changed;
`classify_repo` is untouched and the criterion is still
`sys.exit(1 if residue else 0)`.

  G2-a. CAPDIR's default names this gate's captures directory, and the
        self-exclusion prefix is G2-, matching this gate's capture ids.
  G2-b. FS_PREFIX gains "repo", "g1", "properties" and "ndocs", TRANSCRIBED
        VERBATIM from the merged P2-S6 Gate 1 copy together with its own stated
        reasons, and "g2", this gate's own evidence subdirectory, which is
        exactly the class that copy named "g1" for.
  G2-c. PROSE_PAIRS gains "15/15", "incomplete/bounded" and "Gate-1/Gate-2",
        transcribed from the same merged copy, and EIGHTEEN new entries. Every
        new entry is a pair of DOCUMENT FIELD NAMES joined by a slash, printed
        as an instance or schema locus by the N3 validator, by the corpus
        runner, or by the capture tool's own guard, and quoted into this gate's
        record, plus this Slice's own branch name, which is owner/repo-shaped
        and is not a refs/ path. None is a repository identifier. They are EXACT STRINGS, never
        leading-segment rules, and the near-miss seed requires that they do not
        act as prefixes.
  G2-d. The mention class is UNCHANGED from the Gate 1 copy.

ONE RESIDUE IS LEFT DELIBERATELY UNEXPLAINED, and it is not an oversight. The
frozen corpus runner prints a case label carrying an issue-shaped token that is
a FRICTION citation written without the word `friction`, which the FRICTION
regex requires. No existing explicit set fits it honestly: the mention class
means "issues of the permitted repository this Slice's evidence names", which it
is not, and putting it there would assert something false and weaken a live
check. Admitting it would need a new classification branch, which is a rule
change. It stays residue and the gate record discloses it.

FALSIFIED BEFORE TRUST, in two runs, both captured. The two retained seeds must
still fire the repository, node and issue limbs. A NEW seed carries, for every
fact added above, a token shaped like it but outside it - one character
different - and every one of those must remain residue. A fact that admitted
its own near-miss would be a blindfold rather than a domain fact.

RE-RUN COPY (Gate 0 re-run, opening comment 5472973466 Ruling 2). This file is
a copy of the retained docs/evidence/gatebraid/P2-S5/checks-g0-closed-set-sweep.py
(sha256 57e015d349587c35b4953c4e8ceb277f606cbb1ec8899235ac8180bcb317f21c), which
retained Gate 0 captures pin by hash and which is therefore frozen. The retained
original is NOT edited. Six things differ, all of them DOMAIN FACTS, none of
them a rule:

  1. CAPDIR's default names this re-run's captures directory. (The domain is
     argv-overridable, so the layout itself needs no edit; the default is moved
     so an argument-less run cannot silently sweep the retained gate's domain
     and report it as this gate's.)
  2. The self-exclusion prefix is G0R-, matching this re-run's capture ids.
  3. The mention class gains 19 and 20 -- the repair Slice and its pull request,
     which this gate's dependency read and baseline necessarily name. They are
     mention-class exactly as 14 and 16 were for the first attempt: named in
     evidence, targeted by no query in this gate. The mention-class invocation
     check still applies to them, so a query that DID target one is still caught.

  4. N4: a node id carrying the permitted Project's own item-namespace prefix
     is classified as another item of that Project. The healthy snapshot this
     gate produced enumerates all 16 live Project rows, so 15 sibling item ids
     entered the domain -- the first time any gate's sweep has seen a
     NON-degraded snapshot document. The retained original has no class for
     them because until this run no document contained one.
  5. FS_PREFIX gains "Files" and "tags", transcribed from the P2-S6 committed
     copy together with its own stated reasons.
  6. PERMITTED_ITEM_NAMESPACE names the prefix N4 tests.

Facts 4-6 were added under the operator's Ruling A of 2026-08-31, AFTER an
unextended run of this copy reported them as residue and the window stopped
rather than edit the instrument on its own authority.

Every classification rule, every regex and the residue criterion are
byte-identical to the retained original. N4 is an added branch in the node
ladder, ordered after the N2 identity test so the subject item still
classifies as N2; it removes no existing class and loosens no criterion.

The copy is re-falsified against a seeded domain before it is trusted; a sweep
that has only ever returned empty has measured nothing. N4 specifically is
falsified against an OUT-OF-NAMESPACE seed: a class that admits its own
Project's items is a domain fact, while a class that admits ANY item id is a
blindfold, and only a foreign-namespace item id distinguishes the two. Both
seeds are retained under falsification/.
"""
import base64, collections, glob, json, os, re, sys

# The domain defaults to this gate's captures. It is overridable ONLY so the
# same instrument — not a copy of it — can be pointed at a seeded domain and
# shown able to fire. A sweep that has only ever returned empty has never been
# falsified. The seeded run is retained beside the real one.
CAPDIR = sys.argv[1] if len(sys.argv) > 1 else "docs/evidence/gatebraid/P2-S5/g2/captures"

PERMITTED_REPOS = {"MianliWang/gatebraid", "MianliWang/gatebraid-scratch"}
PERMITTED_PROJECT = "PVT_kwHOBRofUs4Beum7"
PERMITTED_ITEM = "PVTI_lAHOBRofUs4Beum7zg4E8qs"
# Every item of the permitted Project shares this prefix -- the encoded
# owner+project half of the node id. The subject item above is one of them. A
# node id carrying a DIFFERENT prefix belongs to a different Project and is
# residue; see N4 below and the out-of-namespace falsification seed.
PERMITTED_ITEM_NAMESPACE = "PVTI_lAHOBRofUs4Beum7"
SUBJECT_ISSUE = 17
# Issues and PRs of the permitted repository that this Slice's own body and
# evidence name but no query in this gate targets.
MENTION_CLASS_ISSUES = {2, 3, 4, 5, 6, 7, 8, 10, 12, 13, 14, 15, 16, 19, 20}
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
    "tags",       # CPython banner "3.12.2 (tags/v3.12.2:...)": a git tag ref
                  # fragment inside an interpreter version string
    # --- transcribed VERBATIM from the merged P2-S6 Gate 1 copy, together with
    # --- its own stated reasons (approval ruling 2).
    "repo",       # "D:\Github repo\Gatebraid" splits at its space the same
                  # way, giving repo/Gatebraid: the same class as Files/Git
    "g1",         # this Slice's own Gate 1 evidence subdirectory
    "properties", # a JSON Schema pointer segment printed by the corpus runner,
                  # e.g. properties/items/items/properties/workflow/type
    "ndocs",      # a Python bytes repr renders a newline as a backslash-n
                  # immediately before a path, so the payload-bytes line of
                  # the allowlist hash yields ndocs joined to evidence
    # --- new here, with fresh stated reasons.
    "g2",         # this gate's own evidence subdirectory, exactly the class
                  # the P2-S6 copy named "g1" for
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
    # --- transcribed VERBATIM from the merged P2-S6 Gate 1 copy.
    "15/15",              # a ratio in the P2-S6 issue body prose
    "incomplete/bounded", # two ordinary words, slashed, in the same body
    "Gate-1/Gate-2",      # prose in a frozen corpus case name, printed by the
                          # corpus runner and quoted into this gate's record
    # --- NEW HERE, with fresh stated reasons. Every entry is a pair of
    # --- DOCUMENT FIELD NAMES joined by a slash, printed as an instance or
    # --- schema locus by the N3 validator, by the corpus runner, or by the
    # --- capture tool's own guard, and quoted into this gate's record. None is
    # --- a repository identifier. They are written as EXACT STRINGS and never
    # --- as a leading-segment rule: `streams` as a prefix would admit any
    # --- `streams/<anything>`, and the near-miss seed below requires that it
    # --- does not.
    "streams/stdout",                    # capture record, stream locus
    "items/required",                    # snapshot schema, a required-keyword locus
    "dual_platform_claim/reports",       # coverage report, BP-03's locus
    "invocation/shell_semantics",        # capture record, declared shell semantics
    "self_assertions/zero_lone_cr",      # capture record, the lone-CR guard
    "self_assertions/binary_mode_write", # capture record, the binary-write guard
    "completeness/unexamined",           # coverage report, IN-05's locus
    "findings/0x1",                      # coverage report, a findings multiplicity
    "repair_attempts/0x1",               # gate-run@2, a repair-attempt multiplicity
    "generator/source_sha256",           # capture record, the generator pin
    "validator/source_sha256",           # coverage report, the validator pin
    "invocation/cwd",                    # capture record, working directory
    "invocation/environment",            # capture record, declared variables
    "invocation/form",                   # capture record, argv or shell
    "platform/os",                       # capture record, the platform block
    "stop_record/remediation_attempted", # gate-run@2, the stop-record field
    "locus/loci",                        # the validator's own summary line,
                                         # "structural : N error locus/loci"
    # --- the Slice's own branch name. It is owner/repo-shaped and it is not a
    # --- refs/ path, so REF_NAMESPACE cannot see it; the five prior Slice
    # --- branches share the convention. Named exactly, so another branch would
    # --- still be residue.
    "slice/P2-S5",
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
SELF = [f for f in ALL if os.path.basename(f).startswith("G2-closed-set-sweep")]
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
                buckets["N2 the P2-S5 item"] += 1
            elif n.startswith(("PVTF_", "PVTSSF_")):
                buckets["N3 field id of the permitted Project"] += 1
            elif n.startswith(PERMITTED_ITEM_NAMESPACE):
                buckets["N4 another item of the permitted Project"] += 1
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
