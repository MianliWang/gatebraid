# Gate 0 evidence — P2-S2

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
11dbac47927bff5aa7c9e86124e85db9ecdbc650
```

**A3 — working tree clean AND at the base branch** (one predicate, friction
#84)
```
$ git status --porcelain -- . :(exclude)docs/evidence/gatebraid/P2-S2
$ git status --porcelain
?? docs/evidence/gatebraid/P2-S2/
$ git rev-parse HEAD
11dbac47927bff5aa7c9e86124e85db9ecdbc650
$ git rev-parse main
11dbac47927bff5aa7c9e86124e85db9ecdbc650
```

**A4 — Project `Environment` field vs actual host**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f "query=query($owner:String!,$repo:String!,$number:Int!){ repository(owner:$owner,name:$repo){ issue(number:$number){ id number title projectItems(first:10){ nodes{ id project{ id title } fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldTextValue{ text field{ ... on ProjectV2FieldCommon{ name id } } } ... on ProjectV2ItemFieldSingleSelectValue{ name optionId field{ ... on ProjectV2FieldCommon{ name id } } } } } } } } } }" -F owner=MianliWang -F repo=gatebraid -F number=10
{"item": "PVTI_lAHOBRofUs4Beum7zg3ZWpw", "field": "Environment", "value": "mixed-see-prose", "optionId": "1e43ec85"}
[elided: 1 of 11 field values shown; full output: docs/evidence/gatebraid/P2-S2/captures/Q6-real.json]
$ C:/Python312/python -c "import sys,json,jsonschema,yaml,importlib.metadata as m;print(json.dumps({'python':sys.version.split()[0],'exe':sys.executable,'platform':sys.platform,'jsonschema':m.version('jsonschema'),'pyyaml':yaml.__version__}))"
{"python": "3.12.2", "exe": "C:\\Python312\\python.exe", "platform": "win32", "jsonschema": "4.23.0", "pyyaml": "6.0.2"}
$ wsl -e python3 -c "import sys,json,jsonschema,yaml,importlib.metadata as m;print(json.dumps({'python':sys.version.split()[0],'exe':sys.executable,'platform':sys.platform,'jsonschema':m.version('jsonschema'),'pyyaml':yaml.__version__}))"
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
$ C:/Python312/python C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/90d70168-51d5-4c54-ad71-63b5f2237ca4/scratchpad/validate-slice.py docs/evidence/gatebraid/P2-S2/captures/G0-slice-body.json schema/slice.schema.json
{"loader": "PyYAML 6.0.2 / jsonschema 4.23.0 / Draft202012Validator", "fences_under_heading": 1, "declared_schema": "gatebraid/slice@1", "file_id": "gatebraid/slice@1", "id_match": true, "error_count": 0, "errors": [], "slice_id": "P2-S2", "environment": "mixed-see-prose", "write_domains": ["bin/", "docs/evidence/gatebraid/P2-S2/"]}
```

## Required disclosures

- Deviations: the closed-set complement sweep over this gate's own captures returned ONE repository identity outside its encoded permitted set — `cli/cli`, a single occurrence in the stdout of `gh --version`, the CLI's own release URL (capture `docs/evidence/gatebraid/P2-S2/captures/G0-closed-set-sweep.json`, instrument exit 1). It was not self-adjudicated here; the record was written `needs_approval` and the ruling obtained at https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5364439544 — the closed-set rule governs identifiers this workflow queries, reads, writes or enumerates, and an identifier appearing only in a contract-mandated tool's self-describing output is a **mention, not a touch**; `cli/cli` is a mention and no scope was exceeded, so the row is dispositioned `pass` against a pinned capture that still reads `SET NOT CLOSED`. The touch-versus-mention distinction is not yet in the instrument's encoded set nor in committed text; both are routed to the D16 protocol-amendment batch, together with the `stop_record` enumeration gap this gate proved · the sweep instrument reached this verdict only at rev 6: rev 5 scanned the `evidence-capture@1` envelope rather than its base64 payload and would have reported CLOSED while seeing none of the evidence, and it also read `docs.github.com/rest/issues` and `github.com/users/<login>` as owner/repo pairs — all three defects are reproduced by seeds C12–C15, and 17 seeded conditions now pass before the sweep's output is trusted · Q6's committed falsification names two cases; case two (an issue not on the Project) has no subject inside the packet's closed set and locating one would require the enumeration the packet forbids — case one was run and the project-selection predicate was exercised against the real response instead · Q5 was read before the one authorized field write rather than after it, so the option id written was verified live first (P2-S1 setup precedent) · `git status --porcelain` unrestricted returns one entry, this gate's own evidence directory, which the contract's Exit step permits; the baseline half of A3 excludes that path and is empty · the bare npm shim `claude` is a shell script and argv-form capture fails on it (FileNotFoundError), so the Windows-executable `claude.cmd` was captured instead, keeping the capture argv-form · two captured stdouts (`G0-tools-python-windows`, `G0-slice-metadata-validation`) carry CRLF terminators because Windows CPython translates on text-mode stdout; the raw bytes are preserved in the capture files that `output_ref` points at and that `--verify-record --rederive` re-checks, and the embedded copies in this record are normalised to LF so this file is LF-only.
- Environment: Windows 11 host, Git Bash (MSYS2) shell; `GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid` on every `gh` call (the shared default store the User-scope variable points at resolves to the operator's account and is never an executor surface, ADR-0024 D1); `PYTHONDONTWRITEBYTECODE=1` on every Python invocation; loader host `C:\Python312\python.exe`; every `gh api` endpoint written without a leading slash, because MSYS rewrites leading-slash endpoints into filesystem paths.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S2
gate: 0
environment: mixed-see-prose
executor: Claude Lead
base_sha: 11dbac47927bff5aa7c9e86124e85db9ecdbc650
started_at: '2026-08-21T01:11:45Z'
ended_at: '2026-08-21T01:29:29Z'
result: passed
bootstrap_exception: true
checks:
- name: repo-identity-and-remote
  command: git remote -v
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G0-remote.json
- name: base-sha-recorded
  command: git rev-parse main
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G0-baseline-main.json
- name: working-tree-clean-at-base
  command: git status --porcelain -- . ':(exclude)docs/evidence/gatebraid/P2-S2'; git rev-parse HEAD;
    git rev-parse main
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G0-porcelain-baseline.json
- name: ref-namespace-enumerated
  command: git for-each-ref --format='%(refname) %(objecttype) %(objectname)'
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G0-ref-namespace.json
- name: environment-matches-host
  command: gh api graphql (Q6 per-item field read); python -c platform probe, both platforms
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G0-tools-python-windows.json
- name: tool-versions
  command: claude.cmd --version; git --version; gh --version; codex --version
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G0-tools-claude.json
- name: slice-metadata-parses
  command: C:\Python312\python.exe validate-slice.py G0-slice-body.json schema/slice.schema.json
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G0-slice-metadata-validation.json
- name: state-packet-Q1-identity
  command: gh api user --jq .login
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q1-real.json
- name: state-packet-Q1-falsification
  command: gh api user --jq .loginX
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q1-falsify.json
- name: state-packet-Q2-approval-author
  command: gh api repos/MianliWang/gatebraid/issues/comments/5363954606 --jq '{author,url,created,updated}'
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q2-real.json
- name: state-packet-Q2-falsification
  command: gh api repos/MianliWang/gatebraid/issues/comments/1 --jq '{...}'
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q2-falsify.json
- name: state-packet-Q3-slice-issue
  command: gh issue view 10 --repo MianliWang/gatebraid --json number,state,title,url
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q3-real.json
- name: state-packet-Q3-falsification
  command: gh issue view 99999 --repo MianliWang/gatebraid --json number,state,title,url
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q3-falsify.json
- name: state-packet-Q4-project
  command: gh project view 1 --owner MianliWang --format json
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q4-real.json
- name: state-packet-Q4-falsification
  command: gh project view 1 --owner MianliWang --format json --jq .doesNotExist
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q4-falsify.json
- name: state-packet-Q5-field-ids
  command: gh project field-list 1 --owner MianliWang --format json
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q5-real.json
- name: state-packet-Q5-falsification
  command: gh project field-list 1 --owner MianliWang --format json --jq .doesNotExist
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q5-falsify.json
- name: state-packet-Q6-item-fields
  command: gh api graphql -f query=<committed Q6 form> -F number=10
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q6-real.json
- name: state-packet-Q6-falsification
  command: gh api graphql -f query=<committed Q6 form> -F number=99999
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q6-falsify.json
- name: state-packet-Q7-blocked-by
  command: gh api repos/MianliWang/gatebraid/issues/10/dependencies/blocked_by
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q7-real-blocked-by.json
- name: state-packet-Q7-blocking
  command: gh api repos/MianliWang/gatebraid/issues/10/dependencies/blocking
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q7-real-blocking.json
- name: state-packet-Q7-falsification
  command: gh api repos/MianliWang/gatebraid/issues/99999/dependencies/blocked_by
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/Q7-falsify.json
- name: phase-subissues-exactly-two
  command: gh api repos/MianliWang/gatebraid/issues/7/sub_issues
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G0-subissues-of-7.json
- name: workflow-field-write-readback
  command: gh project item-edit --id PVTI_lAHOBRofUs4Beum7zg3ZWpw --field-id PVTSSF_lAHOBRofUs4Beum7zhZGqt0
    --single-select-option-id 036a9fdc
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G0-workflow-write.json
- name: closed-set-complement-sweep
  command: C:\Python312\python.exe docs/evidence/gatebraid/P2-S2/closed-set-sweep-rev6.py <11 real-output
    captures>
  result: pass
  output_ref: docs/evidence/gatebraid/P2-S2/captures/G0-closed-set-sweep.json
approvals:
- type: State Packet Approval
  comment_url: https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5363954606
  author: MianliWang
  at: '2026-08-21T01:07:41Z'
evidence_files:
- docs/evidence/gatebraid/P2-S2/gate0.md
notes: 'ADJUDICATION. This record was first written with result: needs_approval, carrying one open finding:
  the closed-set complement sweep exited 1 against its encoded permitted set, reporting cli/cli out-of-set
  - one occurrence, in the stdout of `gh --version` (contract action 5), the CLI''s own release URL. The
  operator ruled at https://github.com/MianliWang/gatebraid/issues/10#issuecomment-5364439544 (author
  MianliWang, OWNER, created_at == updated_at, verified by the door-author check captured at G1-Q2-approval):
  the closed-set rule governs identifiers this workflow QUERIES, READS, WRITES or ENUMERATES, and an identifier
  appearing only inside a contract-mandated tool''s self-describing output is a MENTION, not a touch.
  cli/cli is a mention; no scope was exceeded. The closed-set-complement-sweep row is therefore dispositioned
  pass, while the capture its output_ref pins still shows exit 1 and ''SET NOT CLOSED'': the discrepancy
  is the instrument''s encoded permitted set not yet carrying the touch-versus-mention distinction, and
  that distinction is routed to the D16 protocol-amendment batch for committed text. The stop_record enumeration
  gap this gate proved - neither decidable nor error fits a closed-set classification without writes this
  grant did not authorize - is recorded there as the same #157-family finding. Friction ordinals stay
  unclaimed until the next append. result: passed was written last, after this annotation, as the ruling
  directed. Startability read from the operator-approved closed-set state packet (sha256 396c0ecaeeb97969c23151c2d05ea1bbfaa4cd903253cd2dddf70a9eb7f7c580,
  7800 B), not from the snapshot/frontier pair. Every Q row was falsified in-window on seeded bad input
  before its real output was trusted; both members are recorded. Captures written by the landed bin/gatebraid-capture.py,
  blob 43ff5a06c7f7e1e9b0ba5d6f14e956bc8d4c73d0, and each re-verified with --verify-record --rederive,
  exit 0.'
```
