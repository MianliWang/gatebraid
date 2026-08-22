#!/usr/bin/env python3
"""Gate 0 closed-set sweep — complement method (CLAUDE.md).

Enumerates every REPOSITORY identifier appearing in this gate's captures and
reports any outside the permitted set. Scans the DECODED base64 stdout/stderr
payloads as well as the envelope (the P2-S2 rev-5 defect was scanning the
envelope only, seeing none of the evidence).

A repository identifier is recognised only in a context that actually names a
repository -- not any slash-separated token. Three contexts:
  1. github.com/<owner>/<repo>            (web URL; /users/ and /orgs/ excluded)
  2. api.github.com/repos/<owner>/<repo>  (REST)
  3. <owner>/<repo>#<number>              (cross-repo issue reference)
Bare `a/b` text is NOT treated as a repository: on this host it matches file
paths, ref names and schema ids in overwhelming volume, and an instrument that
reports those as findings reports noise, not a closed-set breach.

Exit 0 = set closed; 1 = an identifier outside the permitted set was found;
2 = a self-test seed failed (the instrument is not trustworthy).
"""
import sys, os, json, base64, re, glob

PERMITTED = {"MianliWang/gatebraid", "MianliWang/gatebraid-scratch"}
# Known mentions with a settled ruling: a contract-mandated tool's own
# self-describing output is a mention, not a touch (ruling at issue 10,
# comment 5364439544).
KNOWN_MENTIONS = {"cli/cli"}

NAME = r'[A-Za-z0-9][A-Za-z0-9_.-]*'
PATTERNS = [
    re.compile(r'(?<![A-Za-z0-9.-])api\.github\.com/repos/(%s)/(%s)' % (NAME, NAME)),
    re.compile(r'(?<![A-Za-z0-9.-])github\.com/(?!users/|orgs/|sponsors/)(%s)/(%s)' % (NAME, NAME)),
    re.compile(r'(?<![A-Za-z0-9_./-])(%s)/(%s)#[0-9]+' % (NAME, NAME)),
]
STRIP = re.compile(r'\.git$')


def idents_in(text):
    found = set()
    for pat in PATTERNS:
        for m in pat.finditer(text):
            owner, repo = m.group(1), STRIP.sub('', m.group(2))
            if repo in ('releases', 'tag', 'tree', 'blob', 'commit', 'compare'):
                continue
            found.add('%s/%s' % (owner, repo))
    return found


def texts_from(path):
    raw = open(path, 'rb').read()
    yield 'envelope', raw.decode('utf-8', 'replace')
    try:
        d = json.loads(raw.decode('utf-8'))
    except Exception:
        return
    for stream in ('stdout', 'stderr'):
        s = (d.get('streams') or {}).get(stream) or {}
        if s.get('data'):
            try:
                yield 'payload:' + stream, base64.b64decode(s['data']).decode('utf-8', 'replace')
            except Exception:
                pass


def selftest():
    """Falsify before trust: seeded positives must be caught, negatives must not."""
    must_catch = {
        "https://github.com/SomeOwner/secret-repo": "SomeOwner/secret-repo",
        "https://api.github.com/repos/Other/thing/issues/3": "Other/thing",
        "see Other/thing#12 for context": "Other/thing",
        "origin\thttps://github.com/MianliWang/other-repo.git (fetch)": "MianliWang/other-repo",
    }
    must_not_catch = [
        "C:/Python312/python.exe", "refs/heads/main", "schema/slice.schema.json",
        "AppData/Local/Temp", "gatebraid/evidence-capture@1", "usr/bin/python3",
        "https://github.com/users/MianliWang/projects/1",
        "https://docs.github.com/rest/issues/comments#get-an-issue-comment",
        "https://docs.github.com/rest/issues/issue-dependencies#list-dependencies",
    ]
    for text, expected in must_catch.items():
        if expected not in idents_in(text):
            return "seed NOT caught: %r (expected %s)" % (text, expected)
    for text in must_not_catch:
        if idents_in(text):
            return "false positive on: %r -> %s" % (text, idents_in(text))
    return None


def main():
    fail = selftest()
    if fail:
        print(json.dumps({"selftest": "FAILED", "detail": fail})); sys.exit(2)

    root = sys.argv[1]
    files = sorted(glob.glob(os.path.join(root, '*.json')))
    findings, mentions = [], []
    for f in files:
        for label, text in texts_from(f):
            for ident in idents_in(text):
                if ident in PERMITTED:
                    continue
                rec = {"identifier": ident, "file": os.path.basename(f), "where": label}
                (mentions if ident in KNOWN_MENTIONS else findings).append(rec)

    def uniq(rs):
        seen, out = set(), []
        for r in rs:
            k = (r['identifier'], r['file'], r['where'])
            if k not in seen:
                seen.add(k); out.append(r)
        return out

    findings, mentions = uniq(findings), uniq(mentions)
    print(json.dumps({
        "selftest": "PASSED (4 positive seeds caught, 9 negative seeds clean)",
        "files_scanned": len(files),
        "permitted": sorted(PERMITTED),
        "known_mentions_found": sorted({m['identifier'] for m in mentions}),
        "known_mention_sites": mentions,
        "outside_permitted_set": findings,
        "verdict": "SET CLOSED" if not findings else "SET NOT CLOSED",
    }, indent=1))
    sys.exit(1 if findings else 0)


main()
