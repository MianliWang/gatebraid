# Gate 0 evidence — P2-S5

## Records

**A1 — repository identity and remote**
```
$ git remote -v
origin	https://github.com/MianliWang/gatebraid.git (fetch)
origin	https://github.com/MianliWang/gatebraid.git (push)
(exit 0)
```

**A1 — ref namespace; any ref outside refs/heads/, refs/remotes/, refs/tags/ is reported, not adopted**
```
$ git for-each-ref '--format=%(refname) %(objecttype) %(objectname)'
refs/codex/turn-diffs/checkpoints/6568734db6429e0860cf0954b19afffaadb93c9960d666efb23d1018f152be37/7f8d802c118042d20382a16a250ea1c5fb0bd87efd6e2a2ee3221558ade9c8f3/1785489900931/c0da4005-1ff6-434a-b1a5-9ad1a2af1b0e tree 8c7df84d62a5d70d4a9ed2f05edf2661bbf5bd43
refs/heads/batch/o0-b1 commit 9dd0415a910e4bdafb0abe66a65189d9aff95cb3
refs/heads/m1-control-plane commit 823502b4f5eba9e8c60c6056816817980bfea685
refs/heads/m3/n0-ratification commit 4ff3f7b1f49f6853b584f255a61cb6b99797acb4
refs/heads/main commit 7ff1f848661aac20b3921ae47fe140394a5d2587
refs/heads/slice/P2-S1 commit f4186342037870c33c50bb5b64a31430b462ac3e
refs/heads/slice/P2-S2 commit 8c710ca0506e300653779d432fd7e56ae58c4212
refs/heads/slice/P2-S3 commit 97567579644e74bb955d5e642ba2c96e33c99316
refs/heads/slice/P2-S4 commit d45020c455549f244be9c8533de07d94a168cce2
refs/remotes/origin/HEAD commit 7ff1f848661aac20b3921ae47fe140394a5d2587
refs/remotes/origin/batch/o0-b1 commit 9dd0415a910e4bdafb0abe66a65189d9aff95cb3
refs/remotes/origin/m1-control-plane commit 823502b4f5eba9e8c60c6056816817980bfea685
refs/remotes/origin/m3/n0-ratification commit 4ff3f7b1f49f6853b584f255a61cb6b99797acb4
refs/remotes/origin/main commit 7ff1f848661aac20b3921ae47fe140394a5d2587
refs/remotes/origin/slice/P2-S1 commit f4186342037870c33c50bb5b64a31430b462ac3e
refs/remotes/origin/slice/P2-S2 commit 8c710ca0506e300653779d432fd7e56ae58c4212
refs/remotes/origin/slice/P2-S3 commit 97567579644e74bb955d5e642ba2c96e33c99316
refs/remotes/origin/slice/P2-S4 commit d45020c455549f244be9c8533de07d94a168cce2
(exit 0)
```

**A2 — plan baseline: head of the base branch now (recorded here only; the Base SHA field is set at Gate 2 from the head re-read under lease — ADR-0011 §9)**
```
$ git rev-parse main
7ff1f848661aac20b3921ae47fe140394a5d2587
(exit 0)
```

**A3 — working tree clean AND at the base branch (one predicate, friction #84)**
```
$ git status --porcelain -- . :(exclude)docs/evidence/gatebraid/P2-S5/
(exit 0)
$ git rev-parse HEAD
7ff1f848661aac20b3921ae47fe140394a5d2587
(exit 0)
$ git rev-parse main
7ff1f848661aac20b3921ae47fe140394a5d2587
(exit 0)
```

**A3 — unfiltered porcelain, so the baseline row's exclusion is auditable**
```
$ git status --porcelain --untracked-files=all
?? docs/evidence/gatebraid/P2-S5/captures/G0-baseline-main.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-head.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-porcelain-baseline.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-ref-namespace.json
?? docs/evidence/gatebraid/P2-S5/captures/G0-remote.json
(exit 0)
```

**A4 — Project Environment field vs actual host**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query{node(id:"PVTI_lAHOBRofUs4Beum7zg4E8qs"){... on ProjectV2Item{ fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldSingleSelectValue{ name optionId field{ ... on ProjectV2FieldCommon{ name } } } } } }}}'
{"data":{"node":{"fieldValues":{"nodes":[{},{},{"name":"Todo","optionId":"f75ad846","field":{"name":"Status"}},{"name":"Backlog","optionId":"d921911c","field":{"name":"Workflow"}},{"name":"—","optionId":"39696bb5","field":{"name":"Gate"}},{"name":"—","optionId":"450ee130","field":{"name":"Next Approval"}},{"name":"mixed-see-prose","optionId":"1e43ec85","field":{"name":"Environment"}},{"name":"Claude Lead","optionId":"ce859c7d","field":{"name":"Executor"}},{"name":"low","optionId":"e291249c","field":{"name":"Risk"}},{},{},{},{}]}}}}
(exit 0)
$ C:/Python312/python.exe -B -c 'import platform,sys;print("system      :",platform.system());print("release     :",platform.release());print("version     :",platform.version());print("machine     :",platform.machine());print("node        :",platform.node());print("interpreter :",sys.executable);print("py_version  :",sys.version.split()[0])'
system      : Windows
release     : 11
version     : 10.0.26200
machine     : AMD64
node        : RoughEgoist
interpreter : C:\Python312\python.exe
py_version  : 3.12.2
(exit 0)
```

**A5 — tool versions**
```
$ C:/Users/rough/AppData/Roaming/npm/claude.cmd --version
2.1.220 (Claude Code)
(exit 0)
$ git --version
git version 2.51.0.windows.1
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh --version
gh version 2.96.0 (2026-07-02)
https://github.com/cli/cli/releases/tag/v2.96.0
(exit 0)
$ codex --version
codex-cli 0.144.6
(exit 0)
$ C:/Python312/python.exe -B -c 'import sys,yaml,importlib.metadata as m;print("CPython    ",sys.version.split()[0]);print("executable ",sys.executable);print("PyYAML     ",yaml.__version__);print("jsonschema ",m.version("jsonschema"))'
CPython     3.12.2
executable  C:\Python312\python.exe
PyYAML      6.0.2
jsonschema  4.23.0
(exit 0)
$ wsl -e bash -lc 'PYTHONDONTWRITEBYTECODE=1 python3 -B -c "import sys,importlib.metadata as m;print(\"CPython    \",sys.version.split()[0]);print(\"executable \",sys.executable);print(\"jsonschema \",m.version(\"jsonschema\"))"'
CPython     3.12.3
executable  /usr/bin/python3
jsonschema  4.10.3
(exit 0)
```

**A6 — slice metadata parses against gatebraid/slice@1**
```
$ C:/Python312/python.exe -B -c 'import sys,yaml,importlib.metadata as m;print("interpreter :",sys.executable);print("CPython     :",sys.version.split()[0]);print("PyYAML      :",yaml.__version__);print("jsonschema  :",m.version("jsonschema"));print("validator   : Draft202012Validator")'
interpreter : C:\Python312\python.exe
CPython     : 3.12.2
PyYAML      : 6.0.2
jsonschema  : 4.23.0
validator   : Draft202012Validator
(exit 0)
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/checks-g0-slice-metadata.py --schema schema/slice.schema.json --selftest
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
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/checks-g0-slice-metadata.py --schema schema/slice.schema.json --body docs/evidence/gatebraid/P2-S5/captures/slice-body-17.md
--- extracted block ---
schema: gatebraid/slice@1
slice_id: P2-S5
stage: S2
phase: P2
workflow_profile: classic
environment: mixed-see-prose
risk: low
depends_on:
  - issue: MianliWang/gatebraid#8
    requires_gate: 3
    reason: "N2 evidence generator (P2-S1) landed at Gate 3; O1's evidence is generated by it"
  - issue: MianliWang/gatebraid#10
    requires_gate: 3
    reason: "N3 evidence validator (P2-S2) landed at Gate 3; O1's evidence is validated by it"
  - issue: MianliWang/gatebraid#12
    requires_gate: 3
    reason: "P2-S3 completed N3's arc: validator repair plus the owed N2 re-validation to completion"
  - issue: MianliWang/gatebraid#14
    requires_gate: 3
    reason: "O0 hardened snapshot/frontier pair (P2-S4) is the startability authority and state source for O1"
write_domains:
  - bin/
  - docs/evidence/gatebraid/P2-S5/
[... shown 24 of 69 lines; full output: docs/evidence/gatebraid/P2-S5/captures/G0-slice-metadata-validation.json]
(exit 0)
```

### Startability — the hardened pair as sole authority (After-O0 clause, first exercise)

**S1 — gatebraid-snapshot**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid C:/Python312/python.exe -B bin/gatebraid-snapshot.py --out docs/evidence/gatebraid/P2-S5/captures/g0-snapshot.json --generated-at 2026-08-26T19:42:38Z

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

**S1 — the snapshot document it emitted**
```
$ cat docs/evidence/gatebraid/P2-S5/captures\g0-snapshot.json
(sha256 401d891cbfe6672dbcc9bc7bcd91b1f1b1f7d04fa10c35205fc52087f6393ef7, 1689 bytes)
{
 "generated_at": "2026-08-26T19:42:38Z",
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

**S2 — gatebraid-frontier**
```
$ C:/Python312/python.exe -B bin/gatebraid-frontier.py docs/evidence/gatebraid/P2-S5/captures/g0-snapshot.json --out docs/evidence/gatebraid/P2-S5/captures/g0-frontier-report.json

consumer                      : gatebraid-frontier 1.0.0
validated against             : D:\Github repo\Gatebraid\schema\snapshot.schema.json sha256=95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6
items excluded (no verdict)   : 0
startable                     : 0
blocked                       : 0
undecidable                   : 0
FRONTIER UNDECIDABLE: the snapshot is degraded in 3 source(s), so every item is undecidable
(exit 3)
```

**S2 — the frontier report it emitted: the verdict and its reasons, verbatim**
```
$ cat docs/evidence/gatebraid/P2-S5/captures\g0-frontier-report.json
(sha256 12302677f807ddb3af43e367f02ccf8f5596842257a89afdd41274f02a2b8ae3, 844 bytes)
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
  "generated_at": "2026-08-26T19:42:38Z",
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

**V1 — closed-set sweep, falsified against a seeded domain: it must fire on the repository, node and issue limbs**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/checks-g0-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/falsification
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
[... shown 14 of 15 lines; full output: docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-falsify.json]
(exit 1)
```

**V1 — pass 1 of the same falsification, retained: the repository limb did NOT fire**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/checks-g0-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/falsification
captures swept : 1

=== candidate classification (every rule applied explicitly) ===
  E8 prose slash between ordinary words                      1

=== every REPOSITORY identity named anywhere ===

=== mention-class check: a mention must never appear in an INVOCATION ===
  mention-class issues targeted by a query: 0 (0 required)

domain      : 1 documents (0 of this sweep's own reports excluded)
UNEXPLAINED RESIDUE: 2
    SEED-out-of-set.json                         stdout       node
    SEED-out-of-set.json                         stdout       issue
(exit 1)
```

**V2 — closed-set sweep over every captured response**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/checks-g0-closed-set-sweep.py
captures swept : 22

=== candidate classification (every rule applied explicitly) ===
  E1 permitted repository                                    15
  E4 git ref namespace, not a repository                     18
  E5 filesystem or URL path segment                          29
  E6 schema-id namespace                                     7
  E7 JSON pointer                                            1
  E8 prose slash between ordinary words (named, not matched) 4
  I3 mention-class                                           11
  N2 the P2-S5 item                                          1

=== every REPOSITORY identity named anywhere ===
  MianliWang/gatebraid           x13   PERMITTED
  MianliWang/gatebraid-scratch   x2    PERMITTED

=== mention-class check: a mention must never appear in an INVOCATION ===
  #7      seen in stdout                       targeted by a query: False
  #8      seen in stdout                       targeted by a query: False
  #10     seen in stdout                       targeted by a query: False
  #12     seen in stdout                       targeted by a query: False
  #14     seen in stdout                       targeted by a query: False
  #16     seen in stdout                       targeted by a query: False
  mention-class issues targeted by a query: 0 (0 required)

domain      : 22 documents (3 of this sweep's own reports excluded)
UNEXPLAINED RESIDUE: 0
(exit 0)
```

**V2b — the same sweep over this record itself, run after it was rendered; its output is at captures/G0-record-sweep.json and is not inlined here, because a document that quoted its own sweep would change the text the sweep just read**

**V3 — every document checked by the capture tool's own guard with re-derivation and by bin/gatebraid-validate.py**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/checks-g0-verify-captures.py
G0-baseline-main.json                  guard+rederive,validate  L1=0 L2=0  accepted
G0-captures-validation-pass1.json      guard+rederive,validate  L1=0 L2=0  accepted
G0-captures-validation-pass2.json      guard+rederive,validate  L1=0 L2=0  accepted
G0-closed-set-sweep-falsify-pass1.json guard+rederive,validate  L1=0 L2=0  accepted
G0-closed-set-sweep-falsify.json       guard+rederive,validate  L1=0 L2=0  accepted
G0-closed-set-sweep-pass1.json         guard+rederive,validate  L1=0 L2=0  accepted
G0-closed-set-sweep.json               guard+rederive,validate  L1=0 L2=0  accepted
G0-env-field.json                      guard+rederive,validate  L1=0 L2=0  accepted
G0-frontier-run.json                   guard+rederive,validate  L1=0 L2=0  accepted
G0-head.json                           guard+rederive,validate  L1=0 L2=0  accepted
G0-host-probe.json                     guard+rederive,validate  L1=0 L2=0  accepted
G0-porcelain-baseline.json             guard+rederive,validate  L1=0 L2=0  accepted
G0-porcelain-full.json                 guard+rederive,validate  L1=0 L2=0  accepted
G0-ref-namespace.json                  guard+rederive,validate  L1=0 L2=0  accepted
G0-remote.json                         guard+rederive,validate  L1=0 L2=0  accepted
G0-slice-body.json                     guard+rederive,validate  L1=0 L2=1  REJECTED
G0-slice-metadata-loader.json          guard+rederive,validate  L1=0 L2=0  accepted
G0-slice-metadata-selftest.json        guard+rederive,validate  L1=0 L2=1  REJECTED
G0-slice-metadata-validation.json      guard+rederive,validate  L1=0 L2=0  accepted
G0-snapshot-run.json                   guard+rederive,validate  L1=0 L2=0  accepted
G0-tools-claude.json                   guard+rederive,validate  L1=0 L2=0  accepted
G0-tools-codex.json                    guard+rederive,validate  L1=0 L2=0  accepted
G0-tools-gh.json                       guard+rederive,validate  L1=0 L2=0  accepted
G0-tools-git.json                      guard+rederive,validate  L1=0 L2=0  accepted
G0-tools-python-windows.json           guard+rederive,validate  L1=0 L2=0  accepted
G0-tools-python-wsl.json               guard+rederive,validate  L1=0 L2=0  accepted
g0-frontier-report.json                validate                 L1=0 L2=2  NOT-COVERED
g0-snapshot.json                       validate                 L1=0 L2=2  NOT-COVERED

documents checked        : 28
accepted by both layers  : 24
rejected                 : 2
interface not covered    : 2
   NOT-COVERED g0-frontier-report.json        STRUCTURE: docs/evidence/gatebraid/P2-S5/captures\g0-frontier-report.json declares no `sch
   NOT-COVERED g0-snapshot.json               STRUCTURE: docs/evidence/gatebraid/P2-S5/captures\g0-snapshot.json declares unknown interf
   REJECTED G0-slice-body.json
      layer1 exit=0 bytes=11552 crlf=0 lone_cr=0
      layer2 exit=1 verdict       : rejected
   REJECTED G0-slice-metadata-selftest.json
      layer1 exit=0 bytes=5224 crlf=0 lone_cr=0
[... shown 40 of 41 lines; full output: docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation.json]
(exit 1)
```

## Required disclosures

- Deviations: this gate STOPPED at the startability read. gatebraid-snapshot exited 3 (DEGRADED) with three of four sources failing closed, and gatebraid-frontier exited 3 with every item undecidable and no verdict for P2-S5. Both failing runs are retained as evidence. No remediation of any kind was attempted and no re-run was made: the Gate 0 Opening comment clause 2 types exit 3 as result stopped with no remediation and no retry-until-green, and a re-run happens only on the operator's word.
- Deviations: stop_record.next_approval reads Human Diagnosis, and that value is the coordinator's reading awaiting the operator's ratification, not an operator ruling. The Gate 0 Opening comment clause 2 types exit 3 as result stopped, which is the contract's decidable branch, and gate-run@2 enforces that a decidable stop carry a next_approval and no workflow. No member of that enumeration names a startability stop: the members are the two gate transitions, Dirty Baseline Acceptance, Scope / Allowlist Change, Environment Change, Session Persistence, Worktree Exception and Human Diagnosis. Human Diagnosis is the only member whose plain meaning covers a stop where an instrument functioned, fail-closed, and left a human to decide. It was written here because the frozen schema admits no decidable stop without it. The Project Next Approval field was NOT written: no field mutation is authorised on the stop path, the row reaches the operator through this report instead, and the value stands or falls on the operator's word. Named as a candidate item for the owed gate-run@2 revision batch beside the approvals[].type gap.
- Deviations: this is the disclosed F-04 limit materialising on its first trusted use. The snapshot's live gh transport is committed and exercised by no declared command; its selftests exercise the replay transport. The first live use failed on three of four sources with the same recorded failure_detail, the response body is a list where an object was required, and the read-outcome sentinel 65. The fail-closed classification behaved as designed: the degradation was reported rather than absorbed.
- Deviations: source project_items reported status ok, complete true, exit 0, and yielded zero items, so the snapshot carries items empty and the frontier report carries zero verdicts of every kind rather than an undecidable verdict for P2-S5. The stop is therefore an absence of any verdict for this Slice, not an adverse verdict about it. Recorded as measured; the cause is not diagnosed here and no tool was changed.
- Deviations: the slice-metadata checker was copied byte-identically from the P2-S4-era working file at _handoff/batch-o0/validate-slice-metadata.py, sha256 a37850cfd3c94caebeb380d5a41aee1fdc7cbba0a10d7989055878e610779419, into this Slice's own evidence directory as checks-g0-slice-metadata.py, and is invoked there. P2-S4 cited the uncommitted _handoff path. ADR-0028 section 4 requires evidence instruments to be committed, and this Slice's write domain already contains the path, so the instrument now travels with the evidence it produces. The change from precedent is the location only; the bytes are identical.
- Deviations: the closed-set sweep was falsified before it was trusted, and the falsification found a defect in the sweep itself. Pass 1 carried the P2-S4 original's PROSE_PAIR regex, which matches essentially every token of the owner-slash-repo shape, so a seeded out-of-set REPOSITORY identifier was classified E8 and never reached the residue: the repository limb could not fire at all, while the node and issue limbs did. The rule was replaced by an explicit allowlist naming the prose pairs actually present. Pass 2 fires on all three limbs against the seed and returns empty residue against the real domain. Pass 1 is retained at captures/G0-closed-set-sweep-pass1.json with its seeded run at captures/G0-closed-set-sweep-falsify-pass1.json.
- Deviations: the sweep's domain in the P2-S4 original is the captures directory only, so a gate's own record — the document that would be committed — was never swept by it. The instrument here accepts a file as well as a directory and is run a second time over gate0.md, after rendering, at captures/G0-record-sweep.json. That second run is the reason this disclosure's own prose says owner-slash-repo rather than the slashed form: with E8 narrowed to a named allowlist, an ordinary prose slash now surfaces as residue instead of being swallowed, which is the intended trade and is what the first run over gate0.md found.
- Deviations: two captures are accepted by the capture tool's own write-path guard with re-derivation and rejected by bin/gatebraid-validate.py, which is a disagreement between two independent checkers rather than a defect in the captures. Both rejections are the finding placeholder-survives-its-own-check at /streams/stdout/rendered/text. The triggers are the Slice template's own HTML comment quoted from the issue body, and the string <root> printed by jsonschema as an error path label. The validator's mention test excuses this pattern at /invocation/argv/N, /checks/N/command and /notes, on the stated ground that those fields quote foreign text; a captured stream's rendered text is the same kind of field and is not in that list. Reported, not worked around: bin/ is a non-goal for writes in this Slice.
- Deviations: two documents this gate produced are not routable by bin/gatebraid-validate.py and are counted in their own class rather than as rejections. g0-snapshot.json declares interface gatebraid/snapshot@1, which the validator does not implement; g0-frontier-report.json declares no schema key at all, naming its interface under report instead. Both are validator exit 2, a usage or input error by the tool's own exit-code contract and not a verdict. The frontier document's key naming is an interface inconsistency reported here and not changed.
- Deviations: the A6 body read used gh issue view --json body --jq .body, whose output carries one trailing newline that jq appends; the captured bytes are therefore the pinned source plus that newline, 4187 against 4186. The body file written from the captured bytes is byte-equal to the capture, and the entry phase's --json body read of the same issue measured 4186 bytes with the pinned sha256. The difference is the jq output form, not the stored body.
- Deviations: the A4 host probe's first attempt named the interpreter by its MSYS path and could not be executed by the capture tool, which runs on the Windows host. The tool recorded the structural failure and wrote no file at all rather than a partial one. The probe was re-run with the Windows interpreter path, the form the committed P2-S4 record used. No partial artefact survives.
- Deviations: the Gate 0 contract's Entry names two field states, Executor = Claude Lead and Workflow to Gate 0 — Verifying. Executor already read Claude Lead from the entry batch and was not rewritten. Workflow was NOT set to Gate 0 — Verifying and still reads Backlog. The Gate 0 Opening comment's clause 5 enumerates this gate's moves and does not include that write, and it authorises field writes only at Exit, on the pass path. The omission is recorded rather than repaired: the gate stopped, so writing Gate 0 — Verifying now would assert a gate in progress that is not, and no field mutation is authorised on the stop path. The operator's ruling is owed on whether the Entry write should have preceded the actions.
- Deviations: no field write, no handoff comment and no Last Checkpoint update was made at this gate. Those are the contract's Exit steps and clause 5's stop condition for a gate that passes; this gate stopped before Exit. The Slice item still reads Workflow Backlog, Gate the bare option and Next Approval the bare option, unchanged from the entry batch, and the only comment on the Slice issue is the operator's own opening comment. Nothing was committed and nothing was pushed: evidence files are working files, committed under the lease at Gate 2.
- Deviations: A3's predicate is evaluated over the baseline excluding this gate's own write domain. The unfiltered view is recorded beside it. The Gate 0 contract's Exit clause makes this gate's own evidence files not a violation.
- Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; shell Git Bash MINGW64 with Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL /usr/bin/python3 with CPython 3.12.3, jsonschema 4.10.3. environment=mixed-see-prose: the gate ran on the Windows host and the WSL half is evidence.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S5
gate: 0
environment: mixed-see-prose
executor: Claude Lead
base_sha: 7ff1f848661aac20b3921ae47fe140394a5d2587
started_at: "2026-08-26T19:39:21Z"
ended_at: "2026-08-26T20:00:41Z"
result: stopped
stop_record:
  stopped_at: "startability read (Gate 0 Opening comment clause 2; ENTRY-M3-O1 section 6)"
  disposition: decidable
  observed: "gatebraid-snapshot exit 3 DEGRADED, 3 of 4 sources status unexpected_endpoint with read-outcome sentinel 65 and failure_detail 'the response body is a list where an object was required'; project_items ok and complete with 0 items; gatebraid-frontier exit 3, snapshot_degraded true, verdicts [] and summary startable 0 / blocked 0 / undecidable 0 / excluded 0, so no verdict exists for P2-S5"
  expected: "frontier exit 0 with verdict `startable` for the P2-S5 item, per the Gate 0 Opening comment clause 2"
  next_approval: Human Diagnosis
  remediation_attempted: none
checks:
  - name: repo-identity-and-remote
    command: "git remote -v"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-remote.json"
  - name: ref-namespace-enumerated
    command: "git for-each-ref"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-ref-namespace.json"
  - name: base-sha-recorded
    command: "git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-baseline-main.json"
  - name: working-tree-clean-at-base
    command: "git status --porcelain (baseline, excluding this gate's write domain); git rev-parse HEAD; git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-porcelain-baseline.json"
  - name: working-tree-unfiltered-audit
    command: "git status --porcelain --untracked-files=all"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-porcelain-full.json"
  - name: environment-matches-host
    command: "gh api graphql (Environment field read); python host probe"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-env-field.json"
  - name: tool-versions
    command: "claude.cmd --version; git --version; gh --version; codex --version; python version probe on both halves"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-tools-git.json"
  - name: slice-metadata-checker-falsified
    command: "checks-g0-slice-metadata.py --schema schema/slice.schema.json --selftest"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-slice-metadata-selftest.json"
  - name: slice-metadata-parses
    command: "checks-g0-slice-metadata.py --schema schema/slice.schema.json --body captures/slice-body-17.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-slice-metadata-validation.json"
  - name: startability-snapshot
    command: "gatebraid-snapshot.py --out captures/g0-snapshot.json --generated-at (measured)"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-snapshot-run.json"
  - name: startability-frontier
    command: "gatebraid-frontier.py captures/g0-snapshot.json --out captures/g0-frontier-report.json"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-frontier-run.json"
  - name: closed-set-sweep-falsified
    command: "checks-g0-closed-set-sweep.py (seeded domain; must fire on repo, node and issue limbs)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-falsify.json"
  - name: closed-set-sweep
    command: "checks-g0-closed-set-sweep.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep.json"
  - name: closed-set-sweep-over-record
    command: "checks-g0-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/gate0.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-record-sweep.json"
  - name: capture-set-validated
    command: "checks-g0-verify-captures.py (capture-tool guard with re-derivation, and bin/gatebraid-validate.py, over every document)"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation.json"
evidence_files:
  - docs/evidence/gatebraid/P2-S5/gate0.md
notes: "Startability read from the hardened gatebraid-snapshot / gatebraid-frontier pair as sole authority: the Gate 0 contract Entry's After-O0 clause, first exercise. No state packet exists for this or any later Slice. Gate 0 Opening comment: id 5430107363, author MianliWang, https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5430107363 ; verified against the committed source before use, byte-identical except one trailing newline, no clause struck. Per that comment's clause 3 this record carries NO approvals[] entry for it: the frozen gate-run@2 approvals[].type enumeration has no member for an Entry Ratification and Gate 0 Opening, and State Packet Approval would be false here because no packet exists. The missing member is named here as a candidate item for the already-owed gate-run@2 revision batch. A second gap of the same kind is recorded by this stop: stop_record.next_approval has no enum member for a startability stop, its members being Dirty Baseline Acceptance, Scope / Allowlist Change, Environment Change, Session Persistence, Worktree Exception, Human Diagnosis and the two gate transitions, so the optional field is omitted rather than mistyped, and this too is a candidate item for that revision batch. Base SHA is not re-touched at this gate."
```
