#!/usr/bin/env python3
"""Closed-set complement sweep, rev 4 (session-local instrument, P2-S2 setup).

Rev 4 = rev 3 + the fix the P2-S1 setup recorded as owed: JSON string values are
DECODED before matching, so an escape sequence like \\n inside a body string can
no longer fabricate a token such as `npass/fail`. Raw-text scanning is retained
only for non-JSON inputs.

Two tiers, per the P2-S1 precedent:
  TIER 1 - repository identities: owner/repo in an identity-bearing context
           (github.com/<o>/<r>, api path repos/<o>/<r>, full_name field).
           Any identity outside the permitted set is a STOP.
  TIER 2 - every other `a/b` token, SURFACED not dropped, for human
           classification. Tier 2 is not a failure channel.
"""
import base64, json, re, sys, os

PERMITTED = {"MianliWang/gatebraid", "MianliWang/gatebraid-scratch"}

SEG = r"[A-Za-z0-9._-]+"

# Rev 5 repair. Rev 4 treated ANY `github.com/<a>/<b>` as a repository identity,
# which promoted `api.github.com/users/<login>`, `api.github.com/licenses/<id>`
# and the `repos` path segment itself into tier 1 as false identities, and left a
# `.git` clone suffix unnormalized so one repository appeared as two. Both are the
# #146/#147 family - the check mis-reading a non-identity as an identity - and
# neither was probed by rev 4's seeds, which is why the seeds were extended below.
# An identity is now recognised only in a context that actually names a repository.
RE_IDENTITY = re.compile(
    r"(?:"
    r"api\.github\.com/repos/"                      # api: only /repos/ names a repo
    r"|(?<![A-Za-z0-9.-])github\.com[:/]"           # BARE host only - not api., not docs.
    r"|(?<![A-Za-z0-9._-])repos/"                   # bare `gh api repos/<o>/<r>`
    r")(" + SEG + r")/(" + SEG + r")"
)

# Rev 6. On the bare web host these first segments are GitHub's own routes, never
# repository owners: github.com/users/<login> is a profile, not a repo. Rev 5 read
# them as owners because its only host discrimination was `api.` - which also let
# docs.github.com/rest/issues through as an owner/repo pair.
RESERVED_FIRST_SEGMENT = {
    "users", "orgs", "settings", "apps", "marketplace", "sponsors", "topics",
    "collections", "notifications", "explore", "features", "about", "pricing",
    "login", "join", "search", "new", "codespaces", "enterprise", "site",
}
RE_FULLNAME = re.compile(r'"full_name"\s*:\s*"(' + SEG + r")/(" + SEG + r')"')
RE_AB = re.compile(r"(?<![A-Za-z0-9._/-])(" + SEG + r")/(" + SEG + r")(?![A-Za-z0-9._/-])")


def normalize(owner, repo):
    """A clone URL's `.git` suffix names the same repository, not another one.

    Returns None when the pair is not a repository identity at all.
    """
    if owner.lower() in RESERVED_FIRST_SEGMENT:
        return None
    if repo.endswith(".git"):
        repo = repo[:-4]
    return "%s/%s" % (owner, repo)


def decode_capture_streams(obj, out):
    """gatebraid/evidence-capture@1 carries its payload base64-encoded.

    A text sweep over such a record measures the ENVELOPE, not the evidence: the
    real API responses sit inside `streams.<name>.data` as one opaque base64 token,
    so every identity they contain is invisible while the base64 blob itself is
    surfaced as a junk token. Decoding the payloads here is what makes the sweep
    a measurement of the evidence rather than of its wrapper.
    """
    if not isinstance(obj, dict):
        return
    streams = obj.get("streams")
    if isinstance(streams, dict):
        for st in streams.values():
            if isinstance(st, dict) and st.get("encoding") == "base64" and st.get("data"):
                try:
                    out.append(base64.b64decode(st["data"]).decode("utf-8", errors="replace"))
                except Exception:
                    pass


def strings_from_json(obj, out):
    """Collect DECODED string values and keys from a parsed JSON document."""
    if isinstance(obj, dict):
        b64 = obj.get("encoding") == "base64"
        for k, v in obj.items():
            out.append(str(k))
            if b64 and k == "data":
                continue  # opaque payload; decoded separately, never scanned as text
            strings_from_json(v, out)
    elif isinstance(obj, list):
        for v in obj:
            strings_from_json(v, out)
    elif isinstance(obj, str):
        out.append(obj)


def scan_text(text, tier1, tier2):
    for rx in (RE_IDENTITY, RE_FULLNAME):
        for m in rx.finditer(text):
            ident = normalize(m.group(1), m.group(2))
            if ident:
                tier1.add(ident)
    for m in RE_AB.finditer(text):
        tok = "%s/%s" % (m.group(1), m.group(2))
        tier2.add(tok)


def sweep_bytes(raw):
    """Returns (tier1, tier2). Decodes JSON string values when the input parses."""
    tier1, tier2 = set(), set()
    text = raw.decode("utf-8", errors="replace")
    parsed = None
    try:
        parsed = json.loads(text)
    except Exception:
        parsed = None
    if parsed is not None:
        vals = []
        strings_from_json(parsed, vals)
        decode_capture_streams(parsed, vals)
        # identity contexts also live in the raw envelope (URLs are string values,
        # so the decoded pass covers them); scan decoded values only.
        for s in vals:
            scan_text(s, tier1, tier2)
    else:
        scan_text(text, tier1, tier2)
    return tier1, tier2


def sweep_files(paths):
    t1, t2 = set(), set()
    for p in paths:
        with open(p, "rb") as f:
            raw = f.read()
        a, b = sweep_bytes(raw)
        t1 |= a
        t2 |= b
    return t1, t2


# ---------------------------------------------------------------- falsification
def falsify():
    """Seeded conditions. Each must behave as stated or the instrument is untrusted."""
    cases = []

    # C1 - a foreign repo identity in an identity context MUST be caught in tier 1.
    raw = json.dumps({"url": "https://github.com/SomeOwner/some-private-repo"}).encode()
    t1, _ = sweep_bytes(raw)
    cases.append(("C1 foreign identity caught", "SomeOwner/some-private-repo" in t1))

    # C2 - a permitted identity IS surfaced (so the complement can be computed),
    #      and is inside the permitted set.
    raw = json.dumps({"url": "https://github.com/MianliWang/gatebraid/issues/10"}).encode()
    t1, _ = sweep_bytes(raw)
    cases.append(("C2 permitted identity surfaced", t1 == {"MianliWang/gatebraid"}))

    # C3 - THE REV-4 FIX: an escaped newline must NOT fabricate an a/b token.
    raw = json.dumps({"body": "a real\npass/fail on both platforms"}).encode()
    _, t2 = sweep_bytes(raw)
    cases.append(("C3 no \\n artifact (npass/fail absent)", "npass/fail" not in t2))
    cases.append(("C3b real token still seen (pass/fail)", "pass/fail" in t2))

    # C4 - an api path identity is caught.
    raw = json.dumps({"u": "repos/OtherOwner/otherrepo/issues/1"}).encode()
    t1, _ = sweep_bytes(raw)
    cases.append(("C4 api-path identity caught", "OtherOwner/otherrepo" in t1))

    # C5 - empty / non-JSON input does not crash and reports nothing.
    t1, t2 = sweep_bytes(b"")
    cases.append(("C5 empty input safe", t1 == set() and t2 == set()))

    # C6 - a file path is NOT promoted to a repo identity (tier 2 only).
    raw = json.dumps({"p": "bin/gatebraid-validate.py"}).encode()
    t1, t2 = sweep_bytes(raw)
    cases.append(("C6 file path not an identity", "bin/gatebraid-validate.py" not in t1))

    # ---- seeds added at rev 5, each reproducing a way rev 4 mis-measured ----

    # C7 - an api user path is NOT a repository identity.
    raw = json.dumps({"u": "https://api.github.com/users/MianliWang"}).encode()
    t1, _ = sweep_bytes(raw)
    cases.append(("C7 api users/ path not an identity", t1 == set()))

    # C8 - an api licenses path is NOT a repository identity.
    raw = json.dumps({"u": "https://api.github.com/licenses/apache-2.0"}).encode()
    t1, _ = sweep_bytes(raw)
    cases.append(("C8 api licenses/ path not an identity", t1 == set()))

    # C9 - a clone URL's .git suffix names the SAME repository, not a second one.
    raw = json.dumps({"u": "https://github.com/MianliWang/gatebraid.git"}).encode()
    t1, _ = sweep_bytes(raw)
    cases.append(("C9 .git suffix normalized", t1 == {"MianliWang/gatebraid"}))

    # C10 - an api repos path IS an identity, and `repos` is not itself an owner.
    raw = json.dumps({"u": "https://api.github.com/repos/MianliWang/gatebraid/issues/10"}).encode()
    t1, _ = sweep_bytes(raw)
    cases.append(("C10 api repos/ path is the identity", t1 == {"MianliWang/gatebraid"}))

    # C11 - regression: a FOREIGN repo behind an api repos path is still caught.
    raw = json.dumps({"u": "https://api.github.com/repos/Foreign/secret-repo"}).encode()
    t1, _ = sweep_bytes(raw)
    cases.append(("C11 foreign api repos identity caught", "Foreign/secret-repo" in t1))

    # ---- seeds added at rev 6, each reproducing a way rev 5 mis-measured ----

    # C12 - a docs host is not the repo host. rev 5 excluded only `api.`.
    raw = json.dumps({"u": "https://docs.github.com/rest/issues/issue-dependencies"}).encode()
    t1, _ = sweep_bytes(raw)
    cases.append(("C12 docs.github.com not an identity", t1 == set()))

    # C13 - github.com/users/<login> is a profile route, not owner/repo.
    raw = json.dumps({"u": "https://github.com/users/MianliWang/projects/1"}).encode()
    t1, _ = sweep_bytes(raw)
    cases.append(("C13 web users/ route not an identity", t1 == set()))

    # C14 - THE REV-6 FIX: an evidence-capture@1 payload is base64; the identity it
    #       carries must be FOUND, and the base64 blob must not surface as a token.
    payload = json.dumps({"repository_url": "https://api.github.com/repos/Hidden/inside-base64"})
    raw = json.dumps({
        "schema": "gatebraid/evidence-capture@1",
        "streams": {"stdout": {"encoding": "base64",
                               "data": base64.b64encode(payload.encode()).decode()}},
    }).encode()
    t1, t2 = sweep_bytes(raw)
    cases.append(("C14 identity inside base64 payload found", "Hidden/inside-base64" in t1))
    cases.append(("C14b base64 blob not surfaced as a token",
                  not any(len(tok) > 200 for tok in t2)))

    # C15 - regression: a genuine third-party repo URL is STILL an identity. The
    #       rev 6 host/route narrowing must not blunt the check into silence.
    raw = json.dumps({"u": "https://github.com/cli/cli/releases/tag/v2.96.0"}).encode()
    t1, _ = sweep_bytes(raw)
    cases.append(("C15 real third-party repo still caught", "cli/cli" in t1))

    print("FALSIFICATION (before any trusted use):")
    ok = True
    for name, res in cases:
        print("   %-42s %s" % (name, "PASS" if res else "FAIL"))
        ok = ok and res
    print("   ALL SEEDED CONDITIONS PASS:", ok)
    return ok


if __name__ == "__main__":
    if not falsify():
        print("\nINSTRUMENT UNTRUSTED - refusing to report a sweep.")
        sys.exit(2)
    paths = sorted(sys.argv[1:])
    print("\nSWEEP over %d recorded response files:" % len(paths))
    for p in paths:
        print("   -", os.path.basename(p))
    t1, t2 = sweep_files(paths)
    outside = sorted(t1 - PERMITTED)
    print("\nTIER 1 - repository identities: %d distinct" % len(t1))
    for i in sorted(t1):
        print("   %-32s %s" % (i, "PERMITTED" if i in PERMITTED else "*** OUTSIDE ***"))
    print("   OUTSIDE THE PERMITTED SET: %d" % len(outside))
    print("   VERDICT:", "CLOSED" if not outside else "STOP - SET NOT CLOSED")
    print("\nTIER 2 - %d other a/b tokens, surfaced for classification:" % len(t2))
    for tok in sorted(t2):
        print("   ", tok)
    sys.exit(0 if not outside else 1)
