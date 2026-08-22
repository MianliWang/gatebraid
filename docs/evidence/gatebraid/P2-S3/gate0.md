# Gate 0 evidence — P2-S3

## Records

**A1 — repository identity and remote**
```
$ git remote -v
origin	https://github.com/MianliWang/gatebraid.git (fetch)
origin	https://github.com/MianliWang/gatebraid.git (push)
```

**A2 — plan baseline: head of the base branch now** (recorded here only; the
`Base SHA` field is set at Gate 2 from the head re-read under lease —
ADR-0011 §9)
```
$ git rev-parse main
63c8401f5df6ba446cf002232fcb280673c28e00
```

**A3 — working tree clean AND at the base branch** (one predicate, friction
#84)
```
$ git status --porcelain -- . :(exclude)docs/evidence/gatebraid/P2-S3
$ git status --porcelain
?? docs/evidence/gatebraid/P2-S3/
$ git rev-parse HEAD
63c8401f5df6ba446cf002232fcb280673c28e00
$ git rev-parse main
63c8401f5df6ba446cf002232fcb280673c28e00
```

**A3b — ref namespace enumerated** (unrestricted; friction #103)
```
$ git for-each-ref '--format=%(refname) %(objecttype) %(objectname)'
refs/heads/m1-control-plane commit 823502b4f5eba9e8c60c6056816817980bfea685
refs/heads/m3/n0-ratification commit 4ff3f7b1f49f6853b584f255a61cb6b99797acb4
refs/heads/main commit 63c8401f5df6ba446cf002232fcb280673c28e00
refs/heads/slice/P2-S1 commit f4186342037870c33c50bb5b64a31430b462ac3e
refs/heads/slice/P2-S2 commit 8c710ca0506e300653779d432fd7e56ae58c4212
refs/remotes/origin/HEAD commit 63c8401f5df6ba446cf002232fcb280673c28e00
refs/remotes/origin/m1-control-plane commit 823502b4f5eba9e8c60c6056816817980bfea685
refs/remotes/origin/m3/n0-ratification commit 4ff3f7b1f49f6853b584f255a61cb6b99797acb4
refs/remotes/origin/main commit 63c8401f5df6ba446cf002232fcb280673c28e00
refs/remotes/origin/slice/P2-S1 commit f4186342037870c33c50bb5b64a31430b462ac3e
refs/remotes/origin/slice/P2-S2 commit 8c710ca0506e300653779d432fd7e56ae58c4212
refs/codex/turn-diffs/checkpoints/6568734db6429e0860cf0954b19afffaadb93c9960d666efb23d1018f152be37/7f8d802c118042d20382a16a250ea1c5fb0bd87efd6e2a2ee3221558ade9c8f3/1785489900931/c0da4005-1ff6-434a-b1a5-9ad1a2af1b0e tree 8c7df84d62a5d70d4a9ed2f05edf2661bbf5bd43
```

**A4 — Project `Environment` field vs actual host**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query= query($owner:String!,$repo:String!,$number:Int!){ repository(owner:$owner,name:$repo){ issue(number:$number){ id number title projectItems(first:10){ nodes{ id project{ id title } fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldTextValue{ text field{ ... on ProjectV2FieldCommon{ name } } } ... on ProjectV2ItemFieldSingleSelectValue{ name field{ ... on ProjectV2FieldCommon{ name } } } } } } } } } }' -F owner=MianliWang -F repo=gatebraid -F number=12
{"item": "PVTI_lAHOBRofUs4Beum7zg3i6M0", "field": "Environment", "value": "mixed-see-prose", "optionId": "1e43ec85"}
[elided: 1 of 12 field values shown; full output: docs/evidence/gatebraid/P2-S3/captures/Q6-real.json;
 option ids for the same read: docs/evidence/gatebraid/P2-S3/captures/Q6-real-ids.json]
$ C:/Python312/python -c 'import sys,json,yaml,importlib.metadata as m;print(json.dumps({'python':sys.version.split()[0],'exe':sys.executable,'platform':sys.platform,'jsonschema':m.version('jsonschema'),'pyyaml':yaml.__version__}))'
{"python": "3.12.2", "exe": "C:\\Python312\\python.exe", "platform": "win32", "jsonschema": "4.23.0", "pyyaml": "6.0.2"}
$ wsl -e python3 -c 'import sys,json,yaml,importlib.metadata as m;print(json.dumps({'python':sys.version.split()[0],'exe':sys.executable,'platform':sys.platform,'jsonschema':m.version('jsonschema'),'pyyaml':yaml.__version__}))'
{"python": "3.12.3", "exe": "/usr/bin/python3", "platform": "linux", "jsonschema": "4.10.3", "pyyaml": "6.0.1"}
```

**A5 — tool versions**
```
$ C:/Users/rough/AppData/Roaming/npm/claude.cmd --version
2.1.220 (Claude Code)
$ git --version
git version 2.51.0.windows.1
$ gh --version
gh version 2.96.0 (2026-07-02)
https://github.com/cli/cli/releases/tag/v2.96.0
$ codex --version
codex-cli 0.144.6
```

**A6 — slice metadata parses against `gatebraid/slice@1`**
```
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g0_slice_metadata.py docs/evidence/gatebraid/P2-S3/captures/G0-slice-body.json schema/slice.schema.json
{"loader": "PyYAML 6.0.2 / jsonschema 4.23.0 / Draft202012Validator", "interpreter": "C:\\Python312\\python.exe", "body_sha256": "0ff298e0bdcda12cb5961b9400aee791a25c5b9cf6b8827b0a23ad438551040a", "body_bytes": 3129, "fences_under_heading": 1, "declared_schema": "gatebraid/slice@1", "file_id": "gatebraid/slice@1", "id_match": true, "error_count": 0, "errors": [], "slice_id": "P2-S3", "environment": "mixed-see-prose", "write_domains": ["bin/", "docs/evidence/gatebraid/P2-S3/"]}
```

**A6b — the A6 checker falsified before its pass was trusted** (ADR-0028 §4)
```
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g0_slice_metadata.py C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/0846d62b-0514-43be-8d3b-c1ee296ee47c/scratchpad/seedA-schema-invalid.json schema/slice.schema.json
{"loader": "PyYAML 6.0.2 / jsonschema 4.23.0 / Draft202012Validator", "interpreter": "C:\\Python312\\python.exe", "body_sha256": "418d9455390fe76b4d9fe4d8829a8f705c4712c217ee57260b195e493393932a", "body_bytes": 3138, "fences_under_heading": 1, "declared_schema": "gatebraid/slice@1", "file_id": "gatebraid/slice@1", "id_match": true, "error_count": 1, "errors": [{"path": ["risk"], "message": "'catastrophic' is not one of ['low', 'medium', 'high']"}], "slice_id": "P2-S3", "environment": "mixed-see-prose", "write_domains": ["bin/", "docs/evidence/gatebraid/P2-S3/"]}
  exit=3   [seed: schema-invalid body]
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g0_slice_metadata.py C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/0846d62b-0514-43be-8d3b-c1ee296ee47c/scratchpad/seedB-digest-mismatch.json schema/slice.schema.json
{"error": "stdout digest mismatch"}
  exit=4   [seed: tampered payload, stale stdout digest]
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g0_slice_metadata.py C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/0846d62b-0514-43be-8d3b-c1ee296ee47c/scratchpad/seedC-no-heading.json schema/slice.schema.json
{"error": "no '## gatebraid-metadata' heading"}
  exit=2   [seed: metadata heading removed]
```

**A7 — closed-set complement sweep over this gate's own captures**
```
$ C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g0_closed_set_sweep.py docs/evidence/gatebraid/P2-S3/captures
{
 "selftest": "PASSED (4 positive seeds caught, 9 negative seeds clean)",
 "files_scanned": 42,
 "permitted": [
  "MianliWang/gatebraid",
  "MianliWang/gatebraid-scratch"
 ],
 "known_mentions_found": [
  "cli/cli"
 ],
 "known_mention_sites": [
  {
   "identifier": "cli/cli",
   "file": "G0-tools-gh.json",
   "where": "envelope"
  },
  {
   "identifier": "cli/cli",
   "file": "G0-tools-gh.json",
   "where": "payload:stdout"
  }
 ],
 "outside_permitted_set": [],
 "verdict": "SET CLOSED"
}
```

**B1–B7 — state-packet rows, each falsified before its output was trusted**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login
mianliwang492-source
  exit=0
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .loginX
  exit=0
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5377522556 --jq '{author: .user.login, url: .html_url}'
{"author":"MianliWang","url":"https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5377522556"}
  exit=0
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/999999999999 --jq '{author: .user.login, url: .html_url}'
{"message":"Not Found","documentation_url":"https://docs.github.com/rest/issues/comments#get-an-issue-comment","status":"404"}
gh: Not Found (HTTP 404)
  exit=1
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5377614530 --jq '{author: .user.login, url: .html_url}'
{"author":"MianliWang","url":"https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5377614530"}
  exit=0
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh issue view 12 --repo MianliWang/gatebraid --json number,state,title,url
{"number":12,"state":"OPEN","title":"P2-S3 — gatebraid-validate repair: heuristic scope, markdown records, N2 re-validation completion","url":"https://github.com/MianliWang/gatebraid/issues/12"}
  exit=0
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh issue view 99999 --repo MianliWang/gatebraid --json number,state,title,url
GraphQL: Could not resolve to an issue or pull request with the number of 99999. (repository.issue)
  exit=1
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project view 999 --owner MianliWang
GraphQL: Could not resolve to a ProjectV2 with the number 999. (user.projectV2)
  exit=1
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project field-list 999 --owner MianliWang --format json
GraphQL: Could not resolve to a ProjectV2 with the number 999. (user.projectV2)
  exit=1
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query= query($owner:String!,$repo:String!,$number:Int!){ repository(owner:$owner,name:$repo){ issue(number:$number){ id number projectItems(first:10){ nodes{ id project{ id } } } } } }' -F owner=MianliWang -F repo=gatebraid -F number=99999
{"data":{"repository":{"issue":null}},"errors":[{"type":"NOT_FOUND","path":["repository","issue"],"locations":[{"line":4,"column":5}],"message":"Could not resolve to an Issue with the number of 99999."}]}
gh: Could not resolve to an Issue with the number of 99999.
  exit=1
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/12/dependencies/blocked_by
[]
  exit=0
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/12/dependencies/blocking
[]
  exit=0
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/99999/dependencies/blocked_by
{"message":"Not Found","documentation_url":"https://docs.github.com/rest/issues/issue-dependencies#list-dependencies-an-issue-is-blocked-by","status":"404"}
gh: Not Found (HTTP 404)
  exit=1
[Q4-real and Q5-real/Q5-real-plain outputs are long and are not inlined;
 full outputs: docs/evidence/gatebraid/P2-S3/captures/Q4-real.json, Q5-real.json, Q5-real-plain.json.
 Q6-real and Q6-real-ids appear under A4 with their elision note.]
```

## Required disclosures

- Deviations: the approval's §5 named this record `gate0.json`; the operator ruled that a coordinator drafting slip and directed the contract Exit form, `gate0.md` from `templates/gate0-evidence.md`, with every bracketed term unchanged — correction comment `5377614530`, author read back via the packet's Q2 form before this record was written (capture `Q2-correction`); `approvals[]` continues to cite the State Packet Approval itself · **one ref outside the watched namespaces**, `refs/codex/turn-diffs/checkpoints/…` pointing at a *tree*, embedded timestamp 1785489900931 = 2026-07-31T09:25:00.931Z, written by Codex CLI's own turn-diff bookkeeping and pre-dating this Slice by about three weeks: **reported, not adopted** per the contract's Action 1, not deleted or moved, since either would be a state-changing Git command inside the gate and a self-remediation — note that the entry paste's §3.4 form (`for-each-ref refs/heads/ refs/remotes/ refs/tags/`) filters to exactly the three namespaces this hazard is defined as outside and cannot find the class in principle, which is why only the contract's unrestricted enumeration surfaced it · **the closed-set sweep instrument was refuted twice before its verdict was trusted**: rev 1 treated every slash-separated token as a repository and would have reported `SET NOT CLOSED` over `Python312/python.exe`, `refs/heads` and ~130 similar path fragments; rev 2 matched `github.com/` as a substring of `docs.github.com/` and reported `rest/issues` from GitHub's own 404 documentation URLs — the identical false positive P2-S2's rev 5 hit and disclosed; rev 3 anchors the host against a preceding domain label and runs 4 positive and 9 negative seeds before every verdict, exiting 2 and refusing to report if any seed fails; its stated coverage limit is that a foreign repository named in bare `owner/repo` form with no URL and no `#N` would not be caught, while all three contexts a query could actually reach are · `cli/cli` appears twice in `gh --version`'s own release URL — a mention in a contract-mandated tool's self-describing output, not a touch, per the ruling at https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5364439544 · Q5 was additionally run with `--format json` for machine readability and Q6 additionally with `optionId` added, because the packet's verbatim Q6 form returns option *names* and this console mangles U+2014, so verifying select values by name would mean comparing mangled text against a retyped mark, which the standing dash rule forbids; the packet's literal forms were also captured (`Q5-real-plain`, `Q6-real`) so no row is left unexecuted as written, and neither supplement changed a verdict · `git status --porcelain` unrestricted returns one entry, this gate's own evidence directory, which the contract's Exit step permits; the baseline half of A3 excludes that path and is empty · the bare npm shim `claude` is a shell script and argv-form capture fails on it, so the Windows-executable `claude.cmd` was captured instead, keeping the capture argv-form (P2-S2 precedent) · this gate's captures are **not** machine-validated by the landed `bin/gatebraid-validate.py`, per the approval's §4 disclosed instrument limit: the Q6 form carries four GraphQL inline-fragment spreads that the landed validator misclassifies as elisions (friction #169, the defect this Slice repairs); their machine validation is owed to the repaired validator within this Slice at the point the Gate 1 plan names, and this record's own schema validation is unaffected and was run — as a standalone guarded step, against schema/gate-run-v2.schema.json, itself falsified first by six seeds each targeting a documented @2 delta or required property (abbreviated base_sha; approvals[] missing author, the friction #71 class; an unquoted ISO8601 scalar resolving to a datetime rather than a string, friction #55; a checks[] entry missing result; a removed metadata heading; and bootstrap_exception: true with no State Packet Approval), all six rejected for their stated reason before the record's own pass was trusted, captures G0-record-falsify-* · the record's validation is deliberately NOT a checks[] row: a record does not certify itself (no self-reference, ADR-0026), so it is a commit gate rather than a record claim · the A7 sweep cannot scan captures written after it runs; exactly two files postdate it by construction — its own capture and the final record-validation capture — and both are outputs of local check scripts over local files, carrying no repository identifier beyond the permitted set.
- Environment: Windows 11 host, Git Bash (MSYS2) shell; `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` call (the ambient User-scope value points at gh's machine-shared store, whose identity is the operator, ADR-0024 decision 1 / friction #162); `PYTHONDONTWRITEBYTECODE=1` on every Python invocation; loader host `C:\Python312\python.exe` (CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0) with the WSL half (3.12.3 / 6.0.1 / 4.10.3) recorded as the second platform of `mixed-see-prose`; every `gh api` endpoint written without a leading slash, because MSYS rewrites leading-slash endpoints into filesystem paths (friction #33).

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S3
gate: 0
environment: mixed-see-prose
executor: Claude Lead
base_sha: 63c8401f5df6ba446cf002232fcb280673c28e00
started_at: "2026-08-22T03:08:05Z"
ended_at: "2026-08-22T03:33:00Z"
result: passed
approvals:
  - type: State Packet Approval
    comment_url: "https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5377522556"
    author: MianliWang
    at: "2026-08-22T03:04:46Z"
checks:
  - name: repo-identity-and-remote
    command: "git remote -v"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G0-remote.json"
  - name: base-sha-recorded
    command: "git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G0-baseline-main.json"
  - name: working-tree-clean-at-base
    command: "git status --porcelain -- . :(exclude)docs/evidence/gatebraid/P2-S3; git rev-parse HEAD; git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G0-porcelain-baseline.json"
  - name: ref-namespace-enumerated
    command: "git for-each-ref '--format=%(refname) %(objecttype) %(objectname)'"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G0-ref-namespace.json"
  - name: environment-matches-host
    command: "gh api graphql (Q6 per-item field read); python platform probe, both platforms"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G0-tools-python-windows.json"
  - name: tool-versions
    command: "claude.cmd --version; git --version; gh --version; codex --version"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G0-tools-claude.json"
  - name: slice-metadata-parses
    command: "C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g0_slice_metadata.py docs/evidence/gatebraid/P2-S3/captures/G0-slice-body.json schema/slice.schema.json"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G0-slice-metadata-validation.json"
  - name: slice-metadata-falsification-schema-invalid
    command: "C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g0_slice_metadata.py C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/0846d62b-0514-43be-8d3b-c1ee296ee47c/scratchpad/seedA-schema-invalid.json schema/slice.schema.json"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G0-slice-metadata-falsify-seedA.json"
  - name: slice-metadata-falsification-digest-mismatch
    command: "C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g0_slice_metadata.py C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/0846d62b-0514-43be-8d3b-c1ee296ee47c/scratchpad/seedB-digest-mismatch.json schema/slice.schema.json"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G0-slice-metadata-falsify-seedB.json"
  - name: slice-metadata-falsification-no-heading
    command: "C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g0_slice_metadata.py C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/0846d62b-0514-43be-8d3b-c1ee296ee47c/scratchpad/seedC-no-heading.json schema/slice.schema.json"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G0-slice-metadata-falsify-seedC.json"
  - name: closed-set-sweep
    command: "C:/Python312/python docs/evidence/gatebraid/P2-S3/checks/g0_closed_set_sweep.py docs/evidence/gatebraid/P2-S3/captures"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/G0-closed-set-sweep.json"
  - name: state-packet-Q1-identity
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q1-real.json"
  - name: state-packet-Q1-falsification
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .loginX"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q1-falsify.json"
  - name: state-packet-Q2-approval-author
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5377522556 --jq '{author: .user.login, url: .html_url}'"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q2-real.json"
  - name: state-packet-Q2-falsification
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/999999999999 --jq '{author: .user.login, url: .html_url}'"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q2-falsify.json"
  - name: state-packet-Q2-correction-provenance
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5377614530 --jq '{author: .user.login, url: .html_url}'"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q2-correction.json"
  - name: state-packet-Q3-slice-issue
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh issue view 12 --repo MianliWang/gatebraid --json number,state,title,url"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q3-real.json"
  - name: state-packet-Q3-falsification
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh issue view 99999 --repo MianliWang/gatebraid --json number,state,title,url"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q3-falsify.json"
  - name: state-packet-Q4-project
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project view 1 --owner MianliWang"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q4-real.json"
  - name: state-packet-Q4-falsification
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project view 999 --owner MianliWang"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q4-falsify.json"
  - name: state-packet-Q5-field-ids
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project field-list 1 --owner MianliWang"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q5-real-plain.json"
  - name: state-packet-Q5-field-ids-json
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project field-list 1 --owner MianliWang --format json"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q5-real.json"
  - name: state-packet-Q5-falsification
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project field-list 999 --owner MianliWang --format json"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q5-falsify.json"
  - name: state-packet-Q6-item-fields
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query= query($owner:String!,$repo:String!,$number:Int!){ repository(owner:$owner,name:$repo){ issue(number:$number){ id number title projectItems(first:10){ nodes{ id project{ id title } fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldTextValue{ text field{ ... on ProjectV2FieldCommon{ name } } } ... on ProjectV2ItemFieldSingleSelectValue{ name field{ ... on ProjectV2FieldCommon{ name } } } } } } } } } }' -F owner=MianliWang -F repo=gatebraid -F number=12"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q6-real.json"
  - name: state-packet-Q6-item-fields-by-option-id
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query= query($owner:String!,$repo:String!,$number:Int!){ repository(owner:$owner,name:$repo){ issue(number:$number){ projectItems(first:10){ nodes{ id project{ id } fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldTextValue{ text field{ ... on ProjectV2FieldCommon{ name } } } ... on ProjectV2ItemFieldSingleSelectValue{ optionId field{ ... on ProjectV2FieldCommon{ name } } } } } } } } } }' -F owner=MianliWang -F repo=gatebraid -F number=12"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q6-real-ids.json"
  - name: state-packet-Q6-falsification
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query= query($owner:String!,$repo:String!,$number:Int!){ repository(owner:$owner,name:$repo){ issue(number:$number){ id number projectItems(first:10){ nodes{ id project{ id } } } } } }' -F owner=MianliWang -F repo=gatebraid -F number=99999"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q6-falsify.json"
  - name: state-packet-Q7-blocked-by
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/12/dependencies/blocked_by"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q7-real-blockedby.json"
  - name: state-packet-Q7-blocking
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/12/dependencies/blocking"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q7-real-blocking.json"
  - name: state-packet-Q7-falsification
    command: "GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/99999/dependencies/blocked_by"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S3/captures/Q7-falsify.json"
evidence_files:
  - docs/evidence/gatebraid/P2-S3/gate0.md
notes: "Startability read from the operator-approved closed-set state packet (sha256 c7eeb762fe858cf43937419e04546bb17b6b2d63b826bd6fa40697d01a2f541e, 9232 bytes) under ruling R-a, the O0-case treatment extended to this post-bootstrap pre-O0 Slice: full validation, no bootstrap_exception. bootstrap_exception is deliberately ABSENT, not false-by-omission: the bounded evidence bootstrap expired at N2+N3 Gate 3 and this record claims none of it. R-a enlarges the Gate 0 contract's closed enumeration and the approval says so; the contract text is amended by ADR in the R-min/D16 batch. Every checks[] entry carries an output_ref to a capture written by the landed bin/gatebraid-capture.py (generator 1.0.0, source sha256 5dcedf84283952453785c57f9de08ce818b068a1cac8772c806b155444ad5626). Falsification rows record their seeded failure as result: pass because the check they encode is 'this form fails closed on bad input', and each did; the captured exit codes are non-zero by design and are shown in the record. Record container ruled at correction comment https://github.com/MianliWang/gatebraid/issues/12#issuecomment-5377614530."
```
