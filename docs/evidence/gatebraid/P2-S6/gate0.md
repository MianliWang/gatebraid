# Gate 0 evidence - P2-S6

## Records

**A1 - repository identity and remote**
```
$ git remote -v
origin	https://github.com/MianliWang/gatebraid.git (fetch)
origin	https://github.com/MianliWang/gatebraid.git (push)
(exit 0)
```

**A1 - ref namespace; any ref outside refs heads, refs remotes, refs tags is reported, not adopted**
```
$ git for-each-ref '--format=%(refname) %(objecttype) %(objectname)'
refs/codex/turn-diffs/checkpoints/6568734db6429e0860cf0954b19afffaadb93c9960d666efb23d1018f152be37/7f8d802c118042d20382a16a250ea1c5fb0bd87efd6e2a2ee3221558ade9c8f3/1785489900931/c0da4005-1ff6-434a-b1a5-9ad1a2af1b0e tree 8c7df84d62a5d70d4a9ed2f05edf2661bbf5bd43
refs/heads/batch/o0-b1 commit 9dd0415a910e4bdafb0abe66a65189d9aff95cb3
refs/heads/batch/o1-b1 commit 01f1ff43a9f4cbfe43c673035ac3a6af9b65f8a0
refs/heads/m1-control-plane commit 823502b4f5eba9e8c60c6056816817980bfea685
refs/heads/m3/n0-ratification commit 4ff3f7b1f49f6853b584f255a61cb6b99797acb4
refs/heads/main commit 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
refs/heads/slice/P2-S1 commit f4186342037870c33c50bb5b64a31430b462ac3e
refs/heads/slice/P2-S2 commit 8c710ca0506e300653779d432fd7e56ae58c4212
refs/heads/slice/P2-S3 commit 97567579644e74bb955d5e642ba2c96e33c99316
refs/heads/slice/P2-S4 commit d45020c455549f244be9c8533de07d94a168cce2
refs/remotes/origin/HEAD commit 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
refs/remotes/origin/batch/o0-b1 commit 9dd0415a910e4bdafb0abe66a65189d9aff95cb3
refs/remotes/origin/batch/o1-b1 commit 01f1ff43a9f4cbfe43c673035ac3a6af9b65f8a0
refs/remotes/origin/m1-control-plane commit 823502b4f5eba9e8c60c6056816817980bfea685
refs/remotes/origin/m3/n0-ratification commit 4ff3f7b1f49f6853b584f255a61cb6b99797acb4
refs/remotes/origin/main commit 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
refs/remotes/origin/slice/P2-S1 commit f4186342037870c33c50bb5b64a31430b462ac3e
refs/remotes/origin/slice/P2-S2 commit 8c710ca0506e300653779d432fd7e56ae58c4212
refs/remotes/origin/slice/P2-S3 commit 97567579644e74bb955d5e642ba2c96e33c99316
refs/remotes/origin/slice/P2-S4 commit d45020c455549f244be9c8533de07d94a168cce2
(exit 0)
```

**A2 - plan baseline: head of the base branch now (recorded here only; the Base SHA field is set at Gate 2 from the head re-read under lease - ADR-0011 section 9)**
```
$ git rev-parse main
3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
(exit 0)
```

**A3 - working tree clean AND at the base branch (one predicate, friction #84), evaluated over the baseline excluding this gate's own write domain**
```
$ git status --porcelain --untracked-files=all -- . :(exclude)docs/evidence/gatebraid/P2-S6/
?? docs/evidence/gatebraid/P2-S5/captures/G0-baseline-main.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation-pass1.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation-pass2.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-falsify-pass1.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-falsify.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-pass1.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-env-field.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-frontier-run.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-head.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-host-probe.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-porcelain-baseline.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-porcelain-full.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-record-sweep.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-record-validation-pass2.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-record-validation-rejected-pass1.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-record-validation.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-ref-namespace.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-remote.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-render-record-pass1.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-render-record-pass2.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-render-record.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-slice-body.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-slice-metadata-loader.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-slice-metadata-selftest.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-slice-metadata-validation.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-snapshot-run.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-tools-claude.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-tools-codex.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-tools-gh.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-tools-git.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-tools-python-windows.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-tools-python-wsl.json
?? docs/evidence/gatebraid/P2-S5/captures/g0-frontier-report.json
?? docs/evidence/gatebraid/P2-S5/captures/g0-snapshot.json
?? docs/evidence/gatebraid/P2-S5/captures/slice-body-17.md
?? docs/evidence/gatebraid/P2-S5/checks-g0-closed-set-sweep.py
?? docs/evidence/gatebraid/P2-S5/checks-g0-slice-metadata.py
?? docs/evidence/gatebraid/P2-S5/checks-g0-verify-captures.py
?? docs/evidence/gatebraid/P2-S5/falsification/SEED-out-of-set.json
?? docs/evidence/gatebraid/P2-S5/gate0.md
?? docs/evidence/gatebraid/P2-S5/render-gate0.py
(exit 0)
$ git rev-parse HEAD
3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
(exit 0)
$ git rev-parse main
3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
(exit 0)
```

**A3 - tracked changes with no exclusion of any kind: zero**
```
$ git status --porcelain --untracked-files=no
(exit 0)
```

**A3 - unfiltered porcelain, so the baseline row's exclusion is auditable**
```
$ git status --porcelain --untracked-files=all
?? docs/evidence/gatebraid/P2-S5/captures/G0-baseline-main.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation-pass1.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation-pass2.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-falsify-pass1.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-falsify.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-pass1.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep.json
[... shown 8 of 50 lines; full output: docs/evidence/gatebraid/P2-S6/captures/G0-porcelain-full.json]
(exit 0)
```

**A3 - Dirty Baseline Acceptance re-measurement (Ruling 2): the sorted relative-path-list digest, re-derived by the construction shown on the invocation line**
```
$ 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'find docs/evidence/gatebraid/P2-S5 -type f | sort | tr -d '\''\r'\'' | sha256sum'
83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f *-
(exit 0)
```

**A4 - Project Environment field vs actual host**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query{node(id:"PVTI_lAHOBRofUs4Beum7zg4gxqQ"){... on ProjectV2Item{fieldValues(first:50){nodes{... on ProjectV2ItemFieldSingleSelectValue{optionId name field{... on ProjectV2FieldCommon{name}}}}}}}}'
{"data":{"node":{"fieldValues":{"nodes":[{},{},{"optionId":"f75ad846","name":"Todo","field":{"name":"Status"}},{"optionId":"036a9fdc","name":"Gate 0 — Verifying","field":{"name":"Workflow"}},{"optionId":"39696bb5","name":"—","field":{"name":"Gate"}},{"optionId":"450ee130","name":"—","field":{"name":"Next Approval"}},{"optionId":"1e43ec85","name":"mixed-see-prose","field":{"name":"Environment"}},{"optionId":"ce859c7d","name":"Claude Lead","field":{"name":"Executor"}},{"optionId":"e291249c","name":"low","field":{"name":"Risk"}},{},{},{},{}]}}}}
(exit 0)
$ C:/Python312/python.exe -B -c 'import platform,sys;print('\''os'\'',platform.system());print('\''release'\'',platform.platform());print('\''machine'\'',platform.machine());print('\''node'\'',platform.node());print('\''interpreter'\'',sys.version)'
os Windows
release Windows-11-10.0.26200-SP0
machine AMD64
node RoughEgoist
interpreter 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)]
(exit 0)
```

**A5 - tool versions**
```
$ claude.cmd --version
2.1.220 (Claude Code)
(exit 0)
$ git --version
git version 2.51.0.windows.1
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh --version
gh version 2.96.0 (2026-07-02)
https://github.com/cli/cli/releases/tag/v2.96.0
(exit 0)
$ codex.cmd --version
codex-cli 0.144.5
(exit 0)
$ C:/Python312/python.exe -B -c 'import sys,yaml,jsonschema;print('\''CPython'\'',sys.version.split()[0]);print('\''PyYAML'\'',yaml.__version__);print('\''jsonschema'\'',jsonschema.__version__);print('\''exe'\'',sys.executable)'
CPython 3.12.2
PyYAML 6.0.2
jsonschema 4.23.0
exe C:\Python312\python.exe

<string>:1: DeprecationWarning: Accessing jsonschema.__version__ is deprecated and will be removed in a future release. Use importlib.metadata directly to query for jsonschema's version.
(exit 0)
$ wsl.exe -e bash -lc 'PYTHONDONTWRITEBYTECODE=1 python3 -B -c "import sys;print('\''CPython'\'',sys.version.split()[0]);print('\''exe'\'',sys.executable)"'
CPython 3.12.3
exe /usr/bin/python3
(exit 0)
```

**A6 - slice metadata parses against gatebraid slice@1**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/checks-g0-slice-metadata.py --schema schema/slice.schema.json --selftest
selftest pass  positive-control accepted
selftest pass  M1 wrong schema const rejected -> schema: 'gatebraid/slice@1' was expected
selftest pass  M2 slice_id off-pattern rejected -> slice_id: 'P2S4' does not match '^P[0-9]+-S[0-9]+$'
selftest pass  M3 required key removed rejected -> <root>: 'risk' is a required property
selftest pass  M4 undeclared property rejected -> <root>: Additional properties are not allowed ('owner' was unexpected)
selftest pass  M5 environment off-enum rejected -> environment: 'linux' is not one of ['wsl', 'windows', 'macos-authority', 'mixed-see-prose']
selftest pass  M6 repair_limit above max rejected -> repair_limit: 3 is greater than the maximum of 2
selftest pass  M7 workflow_profile renamed rejected -> workflow_profile: 'classic' was expected
selftest pass  M8 parallel_mode off-enum rejected -> parallel_mode: 'isolated' is not one of ['safe-single-writer', 'isolated-write']
selftest pass  M9 stage off-pattern rejected -> stage: '2' does not match '^S[0-9]+$'
selftest pass  M10 write_domains empty string rejected -> write_domains/0: '' should be non-empty
selftest pass  X1 heading absent errored -> no '## gatebraid-metadata' heading
selftest pass  X2 fence absent errored -> no fenced yaml block under the heading
selftest pass  X3 block is a list not a mapping yaml-errored -> ParserError
SELFTEST PASS - checker may be trusted
(exit 0)
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/checks-g0-slice-metadata.py --schema schema/slice.schema.json --body docs/evidence/gatebraid/P2-S6/captures/slice-body-19.md
--- extracted block ---
schema: gatebraid/slice@1
slice_id: P2-S6
stage: S2
phase: P2
workflow_profile: classic
environment: mixed-see-prose
risk: low
depends_on: []
write_domains:
  - bin/
  - docs/evidence/gatebraid/P2-S6/
resource_locks: []
repair_limit: 2
consult_first: false
parallel_mode: safe-single-writer
--- parsed ---
{
  "consult_first": false,
  "depends_on": [],
  "environment": "mixed-see-prose",
  "parallel_mode": "safe-single-writer",
  "phase": "P2",
  "repair_limit": 2,
[... shown 24 of 36 lines; full output: docs/evidence/gatebraid/P2-S6/captures/G0-slice-metadata-validation.json]
(exit 0)
```

### Startability - the hardened pair as sole authority, under the ruled D-2 exception

**S1 - gatebraid-snapshot**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid C:/Python312/python.exe -B bin/gatebraid-snapshot.py --out docs/evidence/gatebraid/P2-S6/captures/g0-snapshot.json --generated-at 2026-08-29T07:34:37Z

generator                     : gatebraid-snapshot 1.0.0
schema                        : D:\Github repo\Gatebraid\schema\snapshot.schema.json sha256=95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6
transport                     : live
sources                       : 4
   project_items    ok                   complete=True  exit=0
   issue_states     unexpected_endpoint  complete=False exit=65  bounded
   dep_blocked_by   unexpected_endpoint  complete=False exit=65  bounded
   dep_blocking     unexpected_endpoint  complete=False exit=65  bounded
items                         : 0
degraded                      : yes
SNAPSHOT DEGRADED: every item carries verdict `undecidable`; exit status 3 so no caller reads this as a healthy read
(exit 3)
```

**S1 - the snapshot document it emitted**
```
$ cat docs/evidence/gatebraid/P2-S6/captures\g0-snapshot.json
(sha256 d8476d262538c859c56704545963a4a7086fcbc5103980ef12eaaf47da2e4ced, 1689 bytes)
{
 "generated_at": "2026-08-29T07:34:37Z",
 "generator": {
  "name": "gatebraid-snapshot",
  "source_sha256": "e27eaad381518ef76d563a59d616f0f5747eaa97a995a602d9972c5a342ef878",
  "version": "1.0.0"
 },
 "items": [],
 "schema": "gatebraid/snapshot@1",
 "snapshot_version": 1,
 "sources": [
  {
   "complete": true,
   "exit_code": 0,
   "query": "live:project_items",
   "source_id": "project_items",
   "status": "ok"
  },
  {
   "bounded": {
    "cap": 10,
    "has_next_page": true,
    "observed": 0,
    "reason": "query_failed"
   },
   "complete": false,
   "exit_code": 65,
   "failure_detail": "the response body is a list where an object was required; the process exited 0 and `exit_code` carries the read-outcome sentinel 65",
   "query": "live:issue_states",
   "source_id": "issue_states",
   "status": "unexpected_endpoint"
  },
  {
   "bounded": {
    "cap": 10,
    "has_next_page": true,
    "observed": 0,
    "reason": "query_failed"
   },
   "complete": false,
   "exit_code": 65,
   "failure_detail": "the response body is a list where an object was required; the process exited 0 and `exit_code` carries the read-outcome sentinel 65",
   "query": "live:dep_blocked_by",
   "source_id": "dep_blocked_by",
   "status": "unexpected_endpoint"
  },
  {
   "bounded": {
    "cap": 10,
    "has_next_page": true,
    "observed": 0,
    "reason": "query_failed"
   },
   "complete": false,
   "exit_code": 65,
   "failure_detail": "the response body is a list where an object was required; the process exited 0 and `exit_code` carries the read-outcome sentinel 65",
   "query": "live:dep_blocking",
   "source_id": "dep_blocking",
   "status": "unexpected_endpoint"
  }
 ]
}
```

**S2 - gatebraid-frontier**
```
$ C:/Python312/python.exe -B bin/gatebraid-frontier.py docs/evidence/gatebraid/P2-S6/captures/g0-snapshot.json --out docs/evidence/gatebraid/P2-S6/captures/g0-frontier-report.json

consumer                      : gatebraid-frontier 1.0.0
validated against             : D:\Github repo\Gatebraid\schema\snapshot.schema.json sha256=95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6
items excluded (no verdict)   : 0
startable                     : 0
blocked                       : 0
undecidable                   : 0
FRONTIER UNDECIDABLE: the snapshot is degraded in 3 source(s), so every item is undecidable
(exit 3)
```

**S2 - the frontier report it emitted: the verdict and its reasons, verbatim**
```
$ cat docs/evidence/gatebraid/P2-S6/captures\g0-frontier-report.json
(sha256 c840ab95c70abfcc388fb5c1039944341d468d28566461be92bfc088d6310084, 844 bytes)
{
 "consumer": {
  "name": "gatebraid-frontier",
  "version": "1.0.0"
 },
 "degraded_sources": [
  {
   "complete": false,
   "source_id": "issue_states",
   "status": "unexpected_endpoint"
  },
  {
   "complete": false,
   "source_id": "dep_blocked_by",
   "status": "unexpected_endpoint"
  },
  {
   "complete": false,
   "source_id": "dep_blocking",
   "status": "unexpected_endpoint"
  }
 ],
 "excluded": [],
 "report": "gatebraid/frontier-report@1",
 "snapshot": {
  "generated_at": "2026-08-29T07:34:37Z",
  "schema_sha256": "95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6",
  "snapshot_version": 1,
  "validated_against": "D:\\Github repo\\Gatebraid\\schema\\snapshot.schema.json"
 },
 "snapshot_degraded": true,
 "summary": {
  "blocked": 0,
  "excluded": 0,
  "startable": 0,
  "undecidable": 0
 },
 "verdicts": []
}
```

### Evidence verification

**V1 - closed-set sweep, falsified against a seeded domain after re-parameterization: it must fire on the repository, node and issue limbs**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/checks-g0-closed-set-sweep.py docs/evidence/gatebraid/P2-S6/falsification
captures swept : 1

=== candidate classification (every rule applied explicitly) ===
  UNEXPLAINED                                                1

=== every REPOSITORY identity named anywhere ===

=== mention-class check: a mention must never appear in an INVOCATION ===
  mention-class issues targeted by a query: 0 (0 required)

domain      : 1 documents (0 of this sweep's own reports excluded)
UNEXPLAINED RESIDUE: 3
    SEED-out-of-set.json                         stdout       repo
    SEED-out-of-set.json                         stdout       node
[... shown 14 of 15 lines; full output: docs/evidence/gatebraid/P2-S6/captures/G0-closed-set-sweep-falsify.json]
(exit 1)
```

**V2 - closed-set sweep over every captured response**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/checks-g0-closed-set-sweep.py docs/evidence/gatebraid/P2-S6/captures
captures swept : 23

=== candidate classification (every rule applied explicitly) ===
  E1 permitted repository                                    1
  E4 git ref namespace, not a repository                     20
  E5 filesystem or URL path segment                          121
  E6 schema-id namespace                                     8
  E7 JSON pointer                                            1
  E8 prose slash between ordinary words (named, not matched) 2
  I3 mention-class                                           7
  N2 this Slice's own Project item                           1

=== every REPOSITORY identity named anywhere ===
  MianliWang/gatebraid           x1    PERMITTED

=== mention-class check: a mention must never appear in an INVOCATION ===
  #7      seen in stdout                       targeted by a query: False
  #14     seen in stdout                       targeted by a query: False
  #17     seen in stdout                       targeted by a query: False
  #18     seen in stdout                       targeted by a query: False
  mention-class issues targeted by a query: 0 (0 required)

domain      : 23 documents (1 of this sweep's own reports excluded)
UNEXPLAINED RESIDUE: 0
(exit 0)
```

**V2b - the same sweep over this record itself, run after it was rendered; its output is at captures/G0-record-sweep.json and is not inlined here, because a document that quoted its own sweep would change the text the sweep just read**

**V3 - every document checked by the capture tool's own guard with re-derivation and by bin/gatebraid-validate.py**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S6/checks-g0-verify-captures.py docs/evidence/gatebraid/P2-S6/captures
G0-baseline-main.json                  guard+rederive,validate  L1=0 L2=0  accepted
G0-closed-set-sweep-falsify.json       guard+rederive,validate  L1=0 L2=0  accepted
G0-closed-set-sweep.json               guard+rederive,validate  L1=0 L2=0  accepted
G0-env-field.json                      guard+rederive,validate  L1=0 L2=0  accepted
G0-frontier-run.json                   guard+rederive,validate  L1=0 L2=0  accepted
G0-head.json                           guard+rederive,validate  L1=0 L2=0  accepted
G0-host-probe.json                     guard+rederive,validate  L1=0 L2=0  accepted
G0-p2s5-pathlist-digest.json           guard+rederive,validate  L1=0 L2=0  accepted
G0-porcelain-baseline.json             guard+rederive,validate  L1=0 L2=0  accepted
G0-porcelain-full.json                 guard+rederive,validate  L1=0 L2=0  accepted
G0-porcelain-tracked.json              guard+rederive,validate  L1=0 L2=0  accepted
G0-ref-namespace.json                  guard+rederive,validate  L1=0 L2=0  accepted
G0-remote.json                         guard+rederive,validate  L1=0 L2=0  accepted
G0-slice-body.json                     guard+rederive,validate  L1=0 L2=1  REJECTED
G0-slice-metadata-selftest.json        guard+rederive,validate  L1=0 L2=1  REJECTED
G0-slice-metadata-validation.json      guard+rederive,validate  L1=0 L2=0  accepted
G0-snapshot-run.json                   guard+rederive,validate  L1=0 L2=0  accepted
G0-tools-claude.json                   guard+rederive,validate  L1=0 L2=0  accepted
G0-tools-codex.json                    guard+rederive,validate  L1=0 L2=0  accepted
G0-tools-gh.json                       guard+rederive,validate  L1=0 L2=0  accepted
G0-tools-git.json                      guard+rederive,validate  L1=0 L2=0  accepted
G0-tools-python-windows.json           guard+rederive,validate  L1=0 L2=1  REJECTED
G0-tools-python-wsl.json               guard+rederive,validate  L1=0 L2=0  accepted
g0-frontier-report.json                validate                 L1=0 L2=2  NOT-COVERED
g0-snapshot.json                       validate                 L1=0 L2=2  NOT-COVERED

documents checked        : 25
accepted by both layers  : 20
rejected                 : 3
interface not covered    : 2
   NOT-COVERED g0-frontier-report.json        STRUCTURE: docs/evidence/gatebraid/P2-S6/captures\g0-frontier-report.json declares no `sch
   NOT-COVERED g0-snapshot.json               STRUCTURE: docs/evidence/gatebraid/P2-S6/captures\g0-snapshot.json declares unknown interf
   REJECTED G0-slice-body.json
      layer1 exit=0 bytes=13606 crlf=0 lone_cr=0
      layer2 exit=1 verdict       : rejected
   REJECTED G0-slice-metadata-selftest.json
      layer1 exit=0 bytes=5224 crlf=0 lone_cr=0
      layer2 exit=1 verdict       : rejected
   REJECTED G0-tools-python-windows.json
      layer1 exit=0 bytes=2314 crlf=0 lone_cr=0
[... shown 40 of 41 lines; full output: docs/evidence/gatebraid/P2-S6/captures/G0-captures-validation.json]
(exit 1)
```

## Required disclosures

- Deviations: this gate PASSED on an observation that is a tool failure, and that inversion is the operator's Ruling 1 in the Gate 0 opening comment on issue 19, the D-2 exception ruled 2026-08-27 for this Slice alone. The startability evidence is the deterministic failure of the committed pair reproduced at class level against the live control plane, not a healthy read. gatebraid-snapshot exited 3 with the three issue-backed sources issue_states, dep_blocked_by and dep_blocking each status unexpected_endpoint, complete false, and the read-outcome sentinel 65; gatebraid-frontier exited 3 with snapshot_degraded true and zero verdicts of every kind. That is exactly the ruled expectation, so the startability check records pass and this record carries result passed. Any other outcome, a healthy read included, would have been a stop; none occurred.
- Deviations: class-level identity with the retained P2-S5 run was measured, not assumed, and byte identity was NOT expected and is absent. The four source identities, their statuses, their complete flags, their exit codes and their failure_detail strings are equal between this run and the retained P2-S5 snapshot; the frontier degraded_sources list, the summary and the empty verdicts list are equal; the snapshot generator source_sha256 is the same committed tool, e27eaad381518ef76d563a59d616f0f5747eaa97a995a602d9972c5a342ef878. generated_at differs, which is why byte identity is not the test.
- Deviations: this is the standing F-04 note materialising again. The snapshot's live gh transport is committed and exercised by no declared command; its selftests exercise the replay transport. This gate is a further live-transport exercise under that same disclosure, and the repair this Slice lands is what retires it. The fail-closed classification behaved as designed once more: the degradation was reported rather than absorbed, and no tool was changed inside this gate.
- Deviations: source project_items reported status ok, complete true, exit 0, and yielded zero items, so the snapshot carries items empty and the frontier report carries zero verdicts of every kind rather than an undecidable verdict for P2-S6. The absent-verdict case is this Slice's expected branch under Ruling 1 and is recorded as measured; the cause is not diagnosed here and no tool was changed.
- Deviations: the baseline is lawfully dirty and the gate proceeded past Action 3 under a Dirty Baseline Acceptance, Ruling 2 of the Gate 0 opening comment, scoped to the retained P2-S5 Gate 0 evidence and nothing else. The acceptance is entered in approvals[] with that comment's id. All three of its re-measured conditions hold: tracked changes are zero; every untracked path lies under the P2-S5 evidence prefix; and the sorted relative-path-list digest re-derives equal to 83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f by the same construction as section 6 of SETUP-REPORT-M3-P2S6.md. That construction command is recorded in this file as the invocation line of the A3 digest row, so the recipe is durable rather than described. Remediation was neither attempted nor permitted.
- Deviations: the entry report for this Slice stated the retained P2-S5 evidence as 44 files. The measured count is 43, three ways agreeing, and Ruling 2 supersedes the earlier figure with the measured one. The 44 was unverified and no capture from entry time exists to re-derive it; it is recorded as a miscount and was not remediated. Nothing in the setup batch or this gate wrote to the working tree.
- Deviations: A3's clean-tree predicate is evaluated over the baseline excluding this gate's own write domain, and the unfiltered view is recorded beside it so the exclusion is auditable. The Gate 0 contract's Exit clause makes this gate's own evidence files not a violation. A separate row records that tracked changes are zero with no exclusion at all.
- Deviations: A1's ref-namespace enumeration found one ref outside refs and heads, refs and remotes, and refs and tags: a Codex turn-diff checkpoint ref pointing at a tree object. It is REPORTED and NOT adopted, which is what the contract requires; it was present in the retained P2-S5 enumeration too. No write of any kind was made into that namespace by this gate.
- Deviations: three evidence instruments travel with the evidence they produce, per ADR-0028 section 4 and the P2-S5 precedent, rather than being cited at an uncommitted path. checks-g0-slice-metadata.py is byte-identical to _handoff/batch-o0/validate-slice-metadata.py, sha256 a37850cfd3c94caebeb380d5a41aee1fdc7cbba0a10d7989055878e610779419. checks-g0-closed-set-sweep.py and checks-g0-verify-captures.py were copied byte-identically from the retained P2-S5 evidence and then re-parameterized for this Slice, as recorded in the next two entries.
- Deviations: the closed-set sweep was re-parameterized for this Slice and then falsified before it was trusted. The changed constants are this Slice's own facts: the captures directory, this Slice's Project item id, the subject issue number, and the mention-class issue set. Four further candidates in this gate's domain needed an explicit rule, and each was named rather than matched by a pattern: a git tag fragment inside the CPython interpreter version banner; a Windows filesystem segment produced when a path containing a space is split; and two ordinary prose slashes in this Slice's own issue body. The additions are exact strings, never a regex, which is the defect pass 1 of the P2-S5 sweep was repaired for. Falsification after the change: pointed at the seeded domain the sweep fires on all three limbs, the repository limb, the node limb and the issue limb, and exits 1; pointed at the real domain it returns empty residue and exits 0. Every REPOSITORY identity named anywhere in the domain is the one permitted owner-slash-repo pair, counted once. No account repository enumeration was performed at any point in this gate.
- Deviations: checks-g0-verify-captures.py had its domain constant re-pointed at this Slice's captures directory and made overridable by argument; no rule of the instrument was changed.
- Deviations: three captures are accepted by the capture tool's own write-path guard with re-derivation and rejected by bin/gatebraid-validate.py, which is a disagreement between two independent checkers rather than a defect in the captures. All three rejections are the finding placeholder-survives-its-own-check, two at the rendered text of a captured stdout stream and one at the rendered text of a captured stderr stream. The triggers are foreign text the streams faithfully recorded: the Slice template's own HTML comment quoted from the issue body, the label jsonschema prints for the document root when it reports an error path, and the pseudo-filename CPython prints in a DeprecationWarning. The validator's mention test excuses this pattern at an invocation argument, a check command and notes, on the stated ground that those fields quote foreign text; a captured stream's rendered text is the same kind of field and is not in that list. Reported and not worked around. Unlike P2-S5, where bin was a non-goal, bin is inside this Slice's declared write domain, so whether this is repaired here is a question for the plan at Gate 1 and is not decided at Gate 0.
- Deviations: two documents this gate produced are not routable by bin/gatebraid-validate.py and are counted in their own class rather than as rejections. g0-snapshot.json declares interface gatebraid/snapshot@1, which the validator does not implement; g0-frontier-report.json declares no schema key at all, naming its interface under a report key instead. Both are validator exit 2, a usage or input error by the tool's own exit-code contract and not a verdict. The frontier document's key naming is an interface inconsistency reported here and not changed.
- Deviations: the A6 body read used gh issue view with json body and jq, whose output carries one trailing newline that jq appends; the captured bytes are therefore the pinned source plus that newline, 5067 against 5066. The body file written from the captured bytes is byte-equal to the capture, and the setup batch's own read-back of the same issue measured 5066 bytes with the pinned sha256 7b345433708b2e56265b138b399ea8fe4ecaa797bebda7e56c0dd13e158727a8. The difference is the jq output form, not the stored body. This is the same class P2-S5 recorded.
- Deviations: the A3 digest capture's first attempt declared shell form and named the shell by bare name, and the capture tool could not execute it. The tool never interpolates a string and runs with shell false, so a declared shell must be an explicit first argument of the command; the bare name is metadata only. The tool reported the structural failure and wrote no file at all rather than a partial one. The capture was re-run with the shell named as an explicit absolute path on the Windows host. No partial artefact survives. This is the same class as the P2-S5 host-probe disclosure.
- Deviations: at gate opening Workflow was written to the Gate 0 Verifying option, resolved fresh from the live field list by exact label with exactly one candidate, id 036a9fdc, its dash measured as U+2014 at codepoint level rather than by appearance. Executor already read Claude Lead from the setup batch and was not rewritten. This closes the question P2-S5 left owed, where the same Entry write was omitted on a stop path.
- Deviations: this gate wrote no tracked file, made no commit, made no push, created no branch, ran no fetch and no pull. The evidence files under this Slice's own directory are working files, committed under the lease at Gate 2, and the Gate 0 contract's Exit clause makes writing them here not a violation.
- Deviations: the capture-set check in row V3 ran before this record was rendered, so the four captures written after it - the render, this record's own machine validation, the sweep over this record, and V3's own capture - are outside the set it checked. That boundary is inherent rather than an omission: each new run would itself produce a capture the run could not have covered, and the regress is stopped by stating where the set ends. The documents V3 did check are named one per line in its output above. Those four later captures are each written by the same guarded write path, and the record itself is independently validated by bin/gatebraid-validate.py in its own row.
- Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; shell Git Bash MINGW64 with Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL /usr/bin/python3 with CPython 3.12.3. environment=mixed-see-prose: the gate ran on the Windows host and the WSL half is evidence.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S6
gate: 0
environment: mixed-see-prose
executor: Claude Lead
base_sha: 3d47f8be0b9c999bf80e356f2b1c1cf88e2e5dd8
started_at: "2026-08-29T07:30:33Z"
ended_at: "2026-08-29T07:42:56Z"
result: passed
approvals:
  - type: Dirty Baseline Acceptance
    author: MianliWang
    comment_url: "https://github.com/MianliWang/gatebraid/issues/19#issuecomment-5461039588"
checks:
  - name: repo-identity-and-remote
    command: "git remote -v"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-remote.json"
  - name: ref-namespace-enumerated
    command: "git for-each-ref (one ref outside the three watched namespaces: reported, not adopted)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-ref-namespace.json"
  - name: base-sha-recorded
    command: "git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-baseline-main.json"
  - name: working-tree-clean-at-base
    command: "git status --porcelain --untracked-files=all (baseline, excluding this gate's write domain); git rev-parse HEAD; git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-porcelain-baseline.json"
  - name: working-tree-tracked-changes-zero
    command: "git status --porcelain --untracked-files=no (no exclusion of any kind)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-porcelain-tracked.json"
  - name: working-tree-unfiltered-audit
    command: "git status --porcelain --untracked-files=all"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-porcelain-full.json"
  - name: dirty-baseline-acceptance-digest-rederived
    command: "find docs/evidence/gatebraid/P2-S5 -type f | sort | tr -d CR | sha256sum (Ruling 2 re-measurement; the exact construction is the invocation line of the A3 digest row)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-p2s5-pathlist-digest.json"
  - name: environment-matches-host
    command: "gh api graphql (Environment field read); python host probe"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-env-field.json"
  - name: tool-versions
    command: "claude.cmd --version; git --version; gh --version; codex.cmd --version; python version probe on both halves"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-tools-git.json"
  - name: slice-metadata-checker-falsified
    command: "checks-g0-slice-metadata.py --schema schema/slice.schema.json --selftest"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-slice-metadata-selftest.json"
  - name: slice-metadata-parses
    command: "checks-g0-slice-metadata.py --schema schema/slice.schema.json --body captures/slice-body-19.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-slice-metadata-validation.json"
  - name: startability-snapshot-degraded-as-ruled
    command: "gatebraid-snapshot.py --out captures/g0-snapshot.json --generated-at (measured); exit 3 with the three issue-backed sources unexpected_endpoint and sentinel 65 IS the ruled expectation"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-snapshot-run.json"
  - name: startability-frontier-undecidable-as-ruled
    command: "gatebraid-frontier.py captures/g0-snapshot.json --out captures/g0-frontier-report.json; exit 3 with snapshot_degraded true and zero verdicts IS the ruled expectation"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-frontier-run.json"
  - name: closed-set-sweep-falsified
    command: "checks-g0-closed-set-sweep.py (seeded domain; must fire on the repository, node and issue limbs)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-closed-set-sweep-falsify.json"
  - name: closed-set-sweep
    command: "checks-g0-closed-set-sweep.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-closed-set-sweep.json"
  - name: closed-set-sweep-over-record
    command: "checks-g0-closed-set-sweep.py docs/evidence/gatebraid/P2-S6/gate0.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-record-sweep.json"
  - name: capture-set-validated
    command: "checks-g0-verify-captures.py (capture-tool guard with re-derivation, and bin/gatebraid-validate.py, over every document)"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S6/captures/G0-captures-validation.json"
evidence_files:
  - docs/evidence/gatebraid/P2-S6/gate0.md
notes: "Startability read from the hardened gatebraid-snapshot and gatebraid-frontier pair as sole authority, the Gate 0 contract Entry's After-O0 clause, under the operator's D-2 exception for this Slice alone: the expected observation IS the deterministic failure reproduced at class level, so exit 3 from both tools is the pass condition and not a stop. Gate 0 opening comment: id 5461039588, author MianliWang observed at verification time, https://github.com/MianliWang/gatebraid/issues/19#issuecomment-5461039588 ; fetched from the API and compared against the committed source before use, identical except one trailing newline, which is the known storage class, and no ruling struck. Per that comment's record-typing clause this record carries NO approvals[] entry for the opening comment itself: the frozen gate-run@2 approvals[].type enumeration still has no member for a Gate 0 Opening, and that missing member remains a candidate item for the already-owed gate-run@2 revision batch. The one approvals[] entry present is Ruling 2's Dirty Baseline Acceptance, which IS a member, carrying the same comment id. The Ruling 2 re-measurement construction is recorded as the invocation line of the A3 digest row so the recipe is reproducible rather than described. The capture-set check is typed fail because two independent checkers disagree about three captures; it is not one of the contract's Actions 1 through 6 and does not bear on this gate's disposition, and it is disclosed in full above. Base SHA is not re-touched at this gate."
```
