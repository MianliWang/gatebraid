# Gate 0 evidence - P2-S5 (re-run under the repaired startability pair)

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
refs/heads/main commit cbd065893b37f20713ae35b8d2673bf26fe4d2ad
refs/heads/slice/P2-S1 commit f4186342037870c33c50bb5b64a31430b462ac3e
refs/heads/slice/P2-S2 commit 8c710ca0506e300653779d432fd7e56ae58c4212
refs/heads/slice/P2-S3 commit 97567579644e74bb955d5e642ba2c96e33c99316
refs/heads/slice/P2-S4 commit d45020c455549f244be9c8533de07d94a168cce2
refs/heads/slice/P2-S6 commit a8f34507b8628819d3995137c60131b78e715063
refs/remotes/origin/HEAD commit cbd065893b37f20713ae35b8d2673bf26fe4d2ad
refs/remotes/origin/batch/o0-b1 commit 9dd0415a910e4bdafb0abe66a65189d9aff95cb3
refs/remotes/origin/batch/o1-b1 commit 01f1ff43a9f4cbfe43c673035ac3a6af9b65f8a0
refs/remotes/origin/m1-control-plane commit 823502b4f5eba9e8c60c6056816817980bfea685
refs/remotes/origin/m3/n0-ratification commit 4ff3f7b1f49f6853b584f255a61cb6b99797acb4
refs/remotes/origin/main commit cbd065893b37f20713ae35b8d2673bf26fe4d2ad
refs/remotes/origin/slice/P2-S1 commit f4186342037870c33c50bb5b64a31430b462ac3e
refs/remotes/origin/slice/P2-S2 commit 8c710ca0506e300653779d432fd7e56ae58c4212
refs/remotes/origin/slice/P2-S3 commit 97567579644e74bb955d5e642ba2c96e33c99316
refs/remotes/origin/slice/P2-S4 commit d45020c455549f244be9c8533de07d94a168cce2
refs/remotes/origin/slice/P2-S6 commit a8f34507b8628819d3995137c60131b78e715063
(exit 0)
```

**A2 - plan baseline: head of the base branch now (recorded here only; the Base SHA field is set at Gate 2 from the head re-read under lease - ADR-0011 section 9)**
```
$ git rev-parse main
cbd065893b37f20713ae35b8d2673bf26fe4d2ad
(exit 0)
```

**A3 - working tree clean AND at the base branch (one predicate, friction #84), evaluated over the baseline excluding this Slice's own evidence prefix**
```
$ git status --porcelain --untracked-files=all -- . :(exclude)docs/evidence/gatebraid/P2-S5/
(exit 0)
$ git rev-parse HEAD
cbd065893b37f20713ae35b8d2673bf26fe4d2ad
(exit 0)
$ git rev-parse main
cbd065893b37f20713ae35b8d2673bf26fe4d2ad
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
[... shown 8 of 52 lines; full output: docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-porcelain-full.json]
(exit 0)
```

**A3 - Dirty Baseline Acceptance re-measurement (Ruling 3): the sorted relative-path-list digest, re-derived by the construction shown on the invocation line, with the re-run subdirectory excluded**
```
$ 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'find docs/evidence/gatebraid/P2-S5 -type f -not -path '\''*/g0r/*'\'' | sort | tr -d '\''\r'\'' | sha256sum'
83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f *-
(exit 0)
```

**A4 - Project Environment field vs actual host**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query{node(id:"PVTI_lAHOBRofUs4Beum7zg4E8qs"){... on ProjectV2Item{fieldValues(first:50){nodes{... on ProjectV2ItemFieldSingleSelectValue{optionId name field{... on ProjectV2FieldCommon{name}}}}}}}}'
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

**A6 - slice metadata parses against gatebraid slice@1, the checker falsified first**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g0r/checks-g0r-slice-metadata.py --schema schema/slice.schema.json --selftest
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
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g0r/checks-g0r-slice-metadata.py --schema schema/slice.schema.json --body docs/evidence/gatebraid/P2-S5/g0r/captures/slice-body-17.md
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
resource_locks: []
repair_limit: 2
[... shown 26 of 69 lines; full output: docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-slice-metadata-validation.json]
(exit 0)
```

### Startability - the repaired hardened pair as sole authority

**S1 - gatebraid-snapshot**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid C:/Python312/python.exe -B bin/gatebraid-snapshot.py --out docs/evidence/gatebraid/P2-S5/g0r/captures/g0r-snapshot.json --generated-at 2026-08-31T02:46:12Z

generator                     : gatebraid-snapshot 1.0.0
schema                        : D:\Github repo\Gatebraid\schema\snapshot.schema.json sha256=95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6
transport                     : live
sources                       : 4
   project_items    ok                   complete=True  exit=0
   issue_states     ok                   complete=True  exit=0
   dep_blocked_by   ok                   complete=True  exit=0
   dep_blocking     ok                   complete=True  exit=0
items                         : 16
degraded                      : no
SNAPSHOT OK: every source read completely with status `ok`
(exit 0)
```

**S1 - the snapshot document it emitted**
```
$ cat docs/evidence/gatebraid/P2-S5/g0r/captures\g0r-snapshot.json
(sha256 fd975bcc917e07217afeb73137e3eca68fffd1180c783bceab4e6f6a37a94c07, 9271 bytes)
{
 "generated_at": "2026-08-31T02:46:12Z",
 "generator": {
  "name": "gatebraid-snapshot",
  "source_sha256": "d064e512af603ccda4d8a3f6c3c2b281fa7b0e0932d23e8d5e22cead0ac97d4c",
  "version": "1.0.0"
 },
 "items": [
  {
   "dependencies": {
    "blocked_by": [],
    "blocking": [],
    "cross_check": "consistent"
   },
   "excluded_reason": "the Project row carries no Slice field; container rows are not Slices",
   "issue": "MianliWang/gatebraid#2",
   "issue_state": "CLOSED",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg0oafU",
   "slice_metadata_present": false,
   "soft_dependencies": {
    "declared": false,
    "entries": [],
    "parse_status": "parsed"
   }
  },
  {
   "dependencies": {
    "blocked_by": [],
    "blocking": [],
    "cross_check": "consistent"
   },
   "excluded_reason": "the Project row carries no Slice field; container rows are not Slices",
   "issue": "MianliWang/gatebraid#3",
   "issue_state": "CLOSED",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg0oahM",
   "slice_metadata_present": false,
   "soft_dependencies": {
    "declared": false,
    "entries": [],
    "parse_status": "parsed"
   }
  },
  {
   "dependencies": {
    "blocked_by": [],
    "blocking": [
     {
      "issue": "MianliWang/gatebraid-scratch#4",
      "state": "OPEN"
     },
     {
      "issue": "MianliWang/gatebraid-scratch#14",
      "state": "OPEN"
     },
     {
      "issue": "MianliWang/gatebraid-scratch#15",
      "state": "OPEN"
     }
    ],
    "cross_check": "consistent"
[... shown 60 of 412 lines; full document: docs/evidence/gatebraid/P2-S5/g0r/captures\g0r-snapshot.json]
```

**S2 - gatebraid-frontier**
```
$ C:/Python312/python.exe -B bin/gatebraid-frontier.py docs/evidence/gatebraid/P2-S5/g0r/captures/g0r-snapshot.json --out docs/evidence/gatebraid/P2-S5/g0r/captures/g0r-frontier-report.json

consumer                      : gatebraid-frontier 1.0.0
validated against             : D:\Github repo\Gatebraid\schema\snapshot.schema.json sha256=95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6
items excluded (no verdict)   : 4
startable                     : 9
blocked                       : 3
undecidable                   : 0
FRONTIER OK: the snapshot validated and every verdict was re-derived from it
(exit 0)
```

**S2 - the frontier report it emitted: the verdict and its reasons, verbatim**
```
$ cat docs/evidence/gatebraid/P2-S5/g0r/captures\g0r-frontier-report.json
(sha256 a52f974b727345730b332d85c081817d7fa796d816cd618eadac737c293dff85, 5128 bytes)
{
 "consumer": {
  "name": "gatebraid-frontier",
  "version": "1.0.0"
 },
 "degraded_sources": [],
 "excluded": [
  {
   "excluded_reason": "the Project row carries no Slice field; container rows are not Slices",
   "issue": "MianliWang/gatebraid#2",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg0oafU"
  },
  {
   "excluded_reason": "the Project row carries no Slice field; container rows are not Slices",
   "issue": "MianliWang/gatebraid#3",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg0oahM"
  },
  {
   "excluded_reason": "the Project row carries no Slice field; container rows are not Slices",
   "issue": "MianliWang/gatebraid#6",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg3Dr2w"
  },
  {
   "excluded_reason": "the Project row carries no Slice field; container rows are not Slices",
   "issue": "MianliWang/gatebraid#7",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg3Dr30"
  }
 ],
 "report": "gatebraid/frontier-report@1",
 "snapshot": {
  "generated_at": "2026-08-31T02:46:12Z",
  "schema_sha256": "95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6",
  "snapshot_version": 1,
  "validated_against": "D:\\Github repo\\Gatebraid\\schema\\snapshot.schema.json"
 },
 "snapshot_degraded": false,
 "summary": {
  "blocked": 3,
  "excluded": 4,
  "startable": 9,
  "undecidable": 0
 },
 "verdicts": [
  {
   "declared_verdict": "startable",
   "issue": "MianliWang/gatebraid-scratch#2",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg0oahY",
   "reasons": [
    "every dependency is closed, both directions agree, and the sources read completely"
   ],
   "slice_id": "P1-S1",
   "verdict": "startable",
   "workflow": "Done"
  },
  {
   "declared_verdict": "startable",
   "issue": "MianliWang/gatebraid-scratch#3",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg0oahc",
   "reasons": [
    "every dependency is closed, both directions agree, and the sources read completely"
   ],
   "slice_id": "P1-S2",
   "verdict": "startable",
   "workflow": "Done"
  },
  {
   "declared_verdict": "blocked",
   "issue": "MianliWang/gatebraid-scratch#4",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg0oahg",
   "reasons": [
    "an Aborted slice is never a candidate (ADR-0025 decision 8), whatever its edges say"
   ],
   "slice_id": "P1-S3",
   "verdict": "blocked",
   "workflow": "Aborted"
  },
  {
   "declared_verdict": "startable",
   "issue": "MianliWang/gatebraid-scratch#5",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg0oahk",
   "reasons": [
    "every dependency is closed, both directions agree, and the sources read completely"
   ],
   "slice_id": "P1-S4",
   "verdict": "startable",
   "workflow": "Backlog"
  },
  {
   "declared_verdict": "blocked",
   "issue": "MianliWang/gatebraid-scratch#14",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg1wWEI",
   "reasons": [
    "an Aborted slice is never a candidate (ADR-0025 decision 8), whatever its edges say"
   ],
   "slice_id": "P1-S5",
   "verdict": "blocked",
   "workflow": "Aborted"
  },
  {
   "declared_verdict": "blocked",
   "issue": "MianliWang/gatebraid-scratch#15",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg14FYg",
   "reasons": [
    "an Aborted slice is never a candidate (ADR-0025 decision 8), whatever its edges say"
   ],
   "slice_id": "P1-S6",
   "verdict": "blocked",
   "workflow": "Aborted"
  },
  {
   "declared_verdict": "startable",
   "issue": "MianliWang/gatebraid#8",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg3Dr5A",
   "reasons": [
    "every dependency is closed, both directions agree, and the sources read completely"
   ],
   "slice_id": "P2-S1",
   "verdict": "startable",
   "workflow": "Done"
  },
  {
   "declared_verdict": "startable",
   "issue": "MianliWang/gatebraid#10",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg3ZWpw",
   "reasons": [
    "every dependency is closed, both directions agree, and the sources read completely"
   ],
   "slice_id": "P2-S2",
   "verdict": "startable",
   "workflow": "Done"
  },
  {
   "declared_verdict": "startable",
   "issue": "MianliWang/gatebraid#12",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg3i6M0",
   "reasons": [
    "every dependency is closed, both directions agree, and the sources read completely"
   ],
   "slice_id": "P2-S3",
   "verdict": "startable",
   "workflow": "Done"
  },
  {
   "declared_verdict": "startable",
   "issue": "MianliWang/gatebraid#14",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg3ogLM",
   "reasons": [
    "every dependency is closed, both directions agree, and the sources read completely"
   ],
   "slice_id": "P2-S4",
   "verdict": "startable",
   "workflow": "Done"
  },
  {
   "declared_verdict": "startable",
   "issue": "MianliWang/gatebraid#17",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg4E8qs",
   "reasons": [
    "every dependency is closed, both directions agree, and the sources read completely"
   ],
   "slice_id": "P2-S5",
   "verdict": "startable",
   "workflow": "Gate 0 — Verifying"
  },
  {
   "declared_verdict": "startable",
   "issue": "MianliWang/gatebraid#19",
   "item_id": "PVTI_lAHOBRofUs4Beum7zg4gxqQ",
   "reasons": [
    "every dependency is closed, both directions agree, and the sources read completely"
   ],
   "slice_id": "P2-S6",
   "verdict": "startable",
   "workflow": "Done"
  }
 ]
}
```

### Evidence verification

**V1 - closed-set sweep, the original seeded domain re-run against the Ruling A extended copy: every limb that already worked must still fire**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g0r/checks-g0r-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g0r/falsification/SEED-out-of-set.json
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
    SEED-out-of-set.json                         stdout       issue
(exit 1)
```

**V1b - closed-set sweep, N4 falsified against an OUT-OF-NAMESPACE seed (Ruling A's condition): the permitted Project's own items admitted, a foreign namespace and a single-character near-miss both left as residue**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g0r/checks-g0r-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g0r/falsification/SEED-out-of-namespace-item.json
captures swept : 1

=== candidate classification (every rule applied explicitly) ===
  N2 the P2-S5 item                                          1
  N4 another item of the permitted Project                   1

=== every REPOSITORY identity named anywhere ===

=== mention-class check: a mention must never appear in an INVOCATION ===
  mention-class issues targeted by a query: 0 (0 required)

domain      : 1 documents (0 of this sweep's own reports excluded)
UNEXPLAINED RESIDUE: 2
    SEED-out-of-namespace-item.json              stdout       node
    SEED-out-of-namespace-item.json              stdout       node
(exit 1)
```

**V2 - closed-set sweep over every captured response**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g0r/checks-g0r-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g0r/captures
captures swept : 24

=== candidate classification (every rule applied explicitly) ===
  E1 permitted repository                                    63
  E4 git ref namespace, not a repository                     25
  E5 filesystem or URL path segment                          82
  E6 schema-id namespace                                     8
  E7 JSON pointer                                            1
  E8 prose slash between ordinary words (named, not matched) 4
  I0 friction citation, not an issue reference               1
  I3 mention-class                                           11
  N2 the P2-S5 item                                          3
  N4 another item of the permitted Project                   30

=== every REPOSITORY identity named anywhere ===
  MianliWang/gatebraid           x43   PERMITTED
  MianliWang/gatebraid-scratch   x20   PERMITTED

=== mention-class check: a mention must never appear in an INVOCATION ===
  #7      seen in stdout                       targeted by a query: False
  #8      seen in stdout                       targeted by a query: False
  #10     seen in stdout                       targeted by a query: False
  #12     seen in stdout                       targeted by a query: False
  #14     seen in stdout                       targeted by a query: False
  #16     seen in stdout                       targeted by a query: False
  mention-class issues targeted by a query: 0 (0 required)

domain      : 24 documents (3 of this sweep's own reports excluded)
UNEXPLAINED RESIDUE: 0
(exit 0)
```

**V2b - the same sweep over this record itself, run after it was rendered; its output is at captures/G0R-record-sweep.json and is not inlined here, because a document that quoted its own sweep would change the text the sweep just read**

**V3 - every document checked by the capture tool's own guard with re-derivation and by bin/gatebraid-validate.py**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g0r/checks-g0r-verify-captures.py
G0R-baseline-main.json                 guard+rederive,validate  L1=0 L2=0  accepted
G0R-captures-validation.json           guard+rederive,validate  L1=0 L2=0  accepted
G0R-closed-set-sweep-falsify-n4.json   guard+rederive,validate  L1=0 L2=0  accepted
G0R-closed-set-sweep-falsify.json      guard+rederive,validate  L1=0 L2=0  accepted
G0R-closed-set-sweep-pass1.json        guard+rederive,validate  L1=0 L2=0  accepted
G0R-closed-set-sweep.json              guard+rederive,validate  L1=0 L2=0  accepted
G0R-env-field.json                     guard+rederive,validate  L1=0 L2=0  accepted
G0R-frontier-run.json                  guard+rederive,validate  L1=0 L2=0  accepted
G0R-head.json                          guard+rederive,validate  L1=0 L2=0  accepted
G0R-host-probe.json                    guard+rederive,validate  L1=0 L2=0  accepted
G0R-p2s5-pathlist-digest.json          guard+rederive,validate  L1=0 L2=0  accepted
G0R-porcelain-baseline.json            guard+rederive,validate  L1=0 L2=0  accepted
G0R-porcelain-full.json                guard+rederive,validate  L1=0 L2=0  accepted
G0R-porcelain-tracked.json             guard+rederive,validate  L1=0 L2=0  accepted
G0R-ref-namespace.json                 guard+rederive,validate  L1=0 L2=0  accepted
G0R-remote.json                        guard+rederive,validate  L1=0 L2=0  accepted
G0R-slice-body.json                    guard+rederive,validate  L1=0 L2=1  REJECTED
G0R-slice-metadata-selftest.json       guard+rederive,validate  L1=0 L2=1  REJECTED
G0R-slice-metadata-validation.json     guard+rederive,validate  L1=0 L2=0  accepted
G0R-snapshot-run.json                  guard+rederive,validate  L1=0 L2=0  accepted
G0R-tools-claude.json                  guard+rederive,validate  L1=0 L2=0  accepted
G0R-tools-codex.json                   guard+rederive,validate  L1=0 L2=0  accepted
G0R-tools-gh.json                      guard+rederive,validate  L1=0 L2=0  accepted
G0R-tools-git.json                     guard+rederive,validate  L1=0 L2=0  accepted
G0R-tools-python-windows.json          guard+rederive,validate  L1=0 L2=1  REJECTED
G0R-tools-python-wsl.json              guard+rederive,validate  L1=0 L2=0  accepted
g0r-frontier-report.json               validate                 L1=0 L2=2  NOT-COVERED
g0r-snapshot.json                      validate                 L1=0 L2=2  NOT-COVERED

documents checked        : 28
accepted by both layers  : 23
rejected                 : 3
interface not covered    : 2
   NOT-COVERED g0r-frontier-report.json       STRUCTURE: docs/evidence/gatebraid/P2-S5/g0r/captures\g0r-frontier-report.json declares no
   NOT-COVERED g0r-snapshot.json              STRUCTURE: docs/evidence/gatebraid/P2-S5/g0r/captures\g0r-snapshot.json declares unknown i
   REJECTED G0R-slice-body.json
      layer1 exit=0 bytes=11621 crlf=0 lone_cr=0
      layer2 exit=1 verdict       : rejected
   REJECTED G0R-slice-metadata-selftest.json
      layer1 exit=0 bytes=5459 crlf=0 lone_cr=0
      layer2 exit=1 verdict       : rejected
   REJECTED G0R-tools-python-windows.json
[... shown 42 of 44 lines; full output: docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-captures-validation.json]
(exit 1)
```

## Required disclosures

- Deviations: this gate ran WHOLE with no exception of any kind. The D-2 startability-by-reproduced-failure exception belonged to this Slice's first attempt and to P2-S6 and is spent; the operator's Ruling 1 in the Gate 0 opening comment on issue 17 states it does not travel. The expected observation was a HEALTHY read and a healthy read is what was measured: gatebraid-snapshot exited 0 with all four sources ok, complete true and exit 0, sixteen items and no degradation; gatebraid-frontier exited 0 with snapshot_degraded false and rendered a verdict for the P2-S5 item. The frontier re-derived every verdict rather than adopting the producer's declared value, and it discriminated: three aborted P1 slices came back blocked under ADR-0025 decision 8. Any other outcome, a degraded source or blocked or undecidable or an absent verdict or a non-zero exit, would have been a stop; none occurred.
- Deviations: the closed-set sweep copy was EXTENDED between its first run and its recorded run, under the operator's Ruling A of 2026-08-31, and the sequence matters. The unextended copy was run first and reported thirty-two unexplained residue; this window did NOT edit the instrument to clear its own finding. It stopped, reported, and asked. That failing run is preserved at captures/G0R-closed-set-sweep-pass1.json, whose internal capture_id remains G0R-closed-set-sweep because a capture is immutable and renaming its file does not and must not rewrite the record. Ruling A then authorised exactly three domain facts in the g0r copy only: an N4 class for node ids carrying the permitted Project's own item-namespace prefix, and FS_PREFIX gaining Files and tags transcribed from the P2-S6 committed copy together with its own stated reasons. No classification rule, no regex and no residue criterion changed; N4 is an added branch ordered after the N2 identity test, removing no class and loosening no criterion.
- Deviations: the N4 class was falsified against an OUT-OF-NAMESPACE seed before it was trusted, which is Ruling A's stated condition and not optional. A class that admits its own Project's items is a domain fact; a class that admits any item id whatever is a blindfold, and only a foreign-namespace item id distinguishes the two. The seed at docs/evidence/gatebraid/P2-S5/g0r/falsification/SEED-out-of-namespace-item.json carries four item ids: the subject item, a genuine sibling row of the permitted Project, an id in a different Project's namespace, and a near-miss whose namespace differs from the permitted one by a single character. The extended sweep admitted the first two, classifying them N2 and N4, and left BOTH of the last two as unexplained residue at exit 1. The pre-existing seed was re-run against the extended copy as well and its repository, node and issue limbs all still fired at exit 1, so the extension blunted no limb that already worked. Both falsification runs are recorded rows and both seeds are retained.
- Deviations: the capture-set check is typed fail and is not a blocker. Three captures are rejected by the N3 validator while the capture tool's own guard with re-derivation accepts them, each carrying the single finding placeholder-survives-its-own-check on a rendered stream-text locus. The cause is the validator's structural placeholder scan matching faithfully recorded FOREIGN text: an angle-bracket token inside the metadata checker's own error strings, another inside a Python DeprecationWarning, and an HTML comment inside the issue body. This is the friction #169 mention class, where the exemption covers command and citation loci but not captured-stream text. The merged and reviewed P2-S6 Gate 0 records the identical outcome, the same three capture kinds with the same finding at the same exit code, and discloses it in its committed gate0.md; the operator's Ruling B of 2026-08-31 carries it here as a disclosure citing that precedent by name. Its repair is a queued Slice of its own. The check is not one of the contract's Actions 1 through 6 and does not bear on this gate's disposition.
- Deviations: this record was rendered twice. The sweep over the first rendering reported two unexplained residues of repository kind, both the same token and both introduced by this record's own prose: a relative path whose leading segment is not a known filesystem prefix. Neither was a repository identifier. The correction was made in the RECORD, not in the instrument -- the path is now written in full, which is what this record does with every other path and what ADR-0026 asks for when a committed path is named. The sweep's rule set is unchanged and still has no class for a bare leading segment of that shape, so the same token in another document would still be residue; nothing was blinded. Ruling A authorised three domain facts and exactly three were made; this was not a fourth. The failing first sweep is preserved at captures/G0R-record-sweep-pass1.json.
- Deviations: this gate opened on 2026-08-31 and completed on 2026-09-01 because it stopped mid-gate for operator adjudication and held. started_at is the first captured action rather than the Workflow field write that opened the gate, which preceded it and carries no capture of its own; ended_at is measured at render. The elapsed span is the hold, not execution time, and is stated rather than left to be inferred from two distant timestamps.
- Deviations: bin/gatebraid-frontier.py is byte-identical at the first attempt's baseline and at this one, sha256 283075b8, and still carries the deferred ADR-0033 defect: the document it emits declares no schema key and names its interface under a report key instead, which is why the validator classifies it interface-not-covered rather than rejecting it. This gate therefore ran a repaired producer into an unrepaired consumer, which is correct under one Slice one tool and affected nothing this gate measured. The frontier identity-key Slice remains queued. Recorded under the operator's Ruling 5a and not acted on here.
- Deviations: the slice body's gatebraid-metadata block declares four depends_on edges, issues 8, 10, 12 and 14, while the live dependency graph and this gate's snapshot both carry five, adding issue 19, the repair Slice. The metadata still validates against gatebraid/slice@1 because the schema does not require the declared edges to equal the graph's. This is a body edit, out of this gate's scope, recorded under the operator's Ruling 5b for the Slice's next governed touch of the body and not acted on here.
- Deviations: the unfiltered porcelain row is a true measurement of its own moment and is NOT reproducible later. It recorded fifty-two untracked paths; the count rose as this gate continued writing its own evidence under the accepted prefix. It belongs to no deterministic subset, and the drift is the gate working rather than the tree changing underneath it.
- Deviations: captures/slice-body-17.md is not itself the product of a captured command. It was written from the recorded stdout of the G0R-slice-body capture and reproduces that capture's own stream sha256 1d35bd1269c51732f4aedfffeb513b4c401318059fab682df5d625ce848db03f exactly, so the capture pins the file rather than the file standing on its own. Same construction P2-S6 used.
- Deviations: every byte this gate wrote lies under docs/evidence/gatebraid/P2-S5/g0r/, which is Ruling 2's layout. No path under docs/evidence/gatebraid/P2-S5/ outside g0r/ was created, modified, moved or deleted. The forty-three retained files of the accepted stop are untouched and the retained gate0.md still measures be7c338896b1015923671988166d55af3bd59e028660ce89dfd3b69bc7251513. The Dirty Baseline Acceptance digest is computed with the re-run subdirectory excluded, so it re-derives equal no matter what this gate writes beside the retained set.
- Deviations: the three instrument copies under g0r/ are copies of the retained originals, verified byte-identical to them before any edit. checks-g0r-slice-metadata.py is verbatim with zero changes because it takes its schema and body as arguments. checks-g0r-verify-captures.py differs in one line, its domain constant. checks-g0r-closed-set-sweep.py differs in six domain facts, three from the layout and three from Ruling A, each recorded inside the file itself with the retained original's sha256. No rule of any instrument was changed, and no instrument was edited to accommodate the layout: the sweep takes its domain as an argument and each domain is named explicitly. --report-id is passed explicitly on the validation of this record, because the default derives a name from the basename alone and two gate0.md at different depths would collide.
- Deviations: at gate opening Workflow was written to the Gate 0 Verifying option, resolved fresh from the live field list by exact label with exactly one candidate, id 036a9fdc, its dash measured as U+2014 at codepoint level rather than by appearance, and read back. The exact labels were carried in a UTF-8 file and resolved by key, never typed through this host's console, whose codec would mangle the mark. The same was done for both Exit writes. Executor already read Claude Lead and was not rewritten.
- Deviations: this gate wrote no tracked file, made no commit, made no push, created no branch, ran no fetch and no pull. The evidence files under this Slice's own directory are working files, committed under the lease at Gate 2, and the Gate 0 contract's Exit clause makes writing them here not a violation. Base SHA is not re-touched at this gate and still carries the first attempt's baseline.
- Deviations: the capture-set check ran before this record was rendered, so the captures written after it, the render and this record's own machine validation and the sweep over this record, are outside the set it checked. That boundary is inherent rather than an omission: each new run would itself produce a capture the run could not have covered, and the regress is stopped by stating where the set ends. The record itself is independently validated by bin/gatebraid-validate.py in its own row.
- Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL /usr/bin/python3 with CPython 3.12.3; every captured command was marshalled as an argv list rather than a shell string, so no quoting layer could alter it. environment=mixed-see-prose: the gate ran on the Windows host and the WSL half is evidence.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S5
gate: 0
environment: mixed-see-prose
executor: Claude Lead
base_sha: cbd065893b37f20713ae35b8d2673bf26fe4d2ad
started_at: "2026-08-31T02:43:46Z"
ended_at: "2026-09-01T20:37:05Z"
result: passed
approvals:
  - type: Dirty Baseline Acceptance
    author: MianliWang
    comment_url: "https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5472973466"
checks:
  - name: repo-identity-and-remote
    command: "git remote -v"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-remote.json"
  - name: ref-namespace-enumerated
    command: "git for-each-ref (one ref outside the three watched namespaces: reported, not adopted)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-ref-namespace.json"
  - name: base-sha-recorded
    command: "git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-baseline-main.json"
  - name: working-tree-clean-at-base
    command: "git status --porcelain --untracked-files=all (baseline, excluding this Slice's evidence prefix); git rev-parse HEAD; git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-porcelain-baseline.json"
  - name: working-tree-tracked-changes-zero
    command: "git status --porcelain --untracked-files=no (no exclusion of any kind)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-porcelain-tracked.json"
  - name: working-tree-unfiltered-audit
    command: "git status --porcelain --untracked-files=all"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-porcelain-full.json"
  - name: dirty-baseline-acceptance-digest-rederived
    command: "find docs/evidence/gatebraid/P2-S5 -type f -not -path g0r | sort | tr -d CR | sha256sum (Ruling 3 construction; the exact recipe is the invocation line of the A3 digest row)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-p2s5-pathlist-digest.json"
  - name: environment-matches-host
    command: "gh api graphql (Environment field read); python host probe"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-env-field.json"
  - name: tool-versions
    command: "claude.cmd --version; git --version; gh --version; codex.cmd --version; python version probe on both halves"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-tools-git.json"
  - name: slice-metadata-checker-falsified
    command: "checks-g0r-slice-metadata.py --schema schema/slice.schema.json --selftest"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-slice-metadata-selftest.json"
  - name: slice-metadata-parses
    command: "checks-g0r-slice-metadata.py --schema schema/slice.schema.json --body captures/slice-body-17.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-slice-metadata-validation.json"
  - name: startability-snapshot-healthy
    command: "gatebraid-snapshot.py --out captures/g0r-snapshot.json --generated-at (measured); exit 0, all four sources ok and complete, items include P2-S5"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-snapshot-run.json"
  - name: startability-frontier-verdict-startable
    command: "gatebraid-frontier.py captures/g0r-snapshot.json --out captures/g0r-frontier-report.json; exit 0, snapshot_degraded false, the P2-S5 verdict re-derived as startable"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-frontier-run.json"
  - name: closed-set-sweep-falsified
    command: "checks-g0r-closed-set-sweep.py (original seeded domain; must fire on the repository, node and issue limbs after the Ruling A extension)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-closed-set-sweep-falsify.json"
  - name: closed-set-sweep-n4-falsified-out-of-namespace
    command: "checks-g0r-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g0r/falsification/SEED-out-of-namespace-item.json (Ruling A's condition: N4 must admit the permitted Project's own items and still fire on a foreign namespace and on a single-character near-miss)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-closed-set-sweep-falsify-n4.json"
  - name: closed-set-sweep
    command: "checks-g0r-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g0r/captures"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-closed-set-sweep.json"
  - name: closed-set-sweep-over-record
    command: "checks-g0r-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g0r/gate0.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-record-sweep.json"
  - name: capture-set-validated
    command: "checks-g0r-verify-captures.py (capture-tool guard with re-derivation, and bin/gatebraid-validate.py, over every document)"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-captures-validation.json"
evidence_files:
  - docs/evidence/gatebraid/P2-S5/g0r/gate0.md
notes: "Startability read from the hardened gatebraid-snapshot and gatebraid-frontier pair as sole authority, the Gate 0 contract Entry's After-O0 clause, with the pair now the REPAIRED one landed by P2-S6. This gate ran whole with no exception: the operator's Ruling 1 retired the D-2 exception, the expected observation was a healthy read, and a healthy read is what was measured, so result passed rests on the contract's own pass condition rather than on any inversion. Gate 0 opening comment: id 5472973466, author MianliWang observed at verification time, https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5472973466 ; fetched from the API by id and compared byte for byte against the pinned source before use, identical except one trailing newline, which is the known storage class, zero CR bytes and no ruling struck. Per that comment's record-typing clause this record carries NO approvals[] entry for the opening comment itself: the frozen gate-run@2 approvals[].type enumeration still has no member for a Gate 0 Opening, and that missing member remains a candidate item for the already-owed gate-run@2 revision batch. The one approvals[] entry present is Ruling 3's Dirty Baseline Acceptance, which IS a member, carrying the same comment id and scoped to the forty-three retained files of the accepted stop. Ruling 3's digest construction is recorded as the invocation line of the A3 digest row so the recipe is reproducible rather than described, and it excludes the g0r subdirectory so the retained set stays verifiable at every later gate. This gate stopped once, mid-run, when the unextended closed-set sweep reported residue it could only clear by editing itself; the window reported and held, and Rulings A and B of 2026-08-31 resolved both open items. The capture-set check is typed fail because two independent checkers disagree about three captures over faithfully recorded foreign text; it is not one of the contract's Actions 1 through 6, it does not bear on this gate's disposition, and it matches merged P2-S6's committed record in kind and outcome. Base SHA is not re-touched at this gate."
```
