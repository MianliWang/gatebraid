# Gate 0 evidence — P2-S4

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
refs/heads/main commit df666070ead7fa21bc72b6c99d2644923b37e787
refs/heads/slice/P2-S1 commit f4186342037870c33c50bb5b64a31430b462ac3e
refs/heads/slice/P2-S2 commit 8c710ca0506e300653779d432fd7e56ae58c4212
refs/heads/slice/P2-S3 commit 97567579644e74bb955d5e642ba2c96e33c99316
refs/remotes/origin/HEAD commit df666070ead7fa21bc72b6c99d2644923b37e787
refs/remotes/origin/batch/o0-b1 commit 9dd0415a910e4bdafb0abe66a65189d9aff95cb3
refs/remotes/origin/m1-control-plane commit 823502b4f5eba9e8c60c6056816817980bfea685
refs/remotes/origin/m3/n0-ratification commit 4ff3f7b1f49f6853b584f255a61cb6b99797acb4
refs/remotes/origin/main commit df666070ead7fa21bc72b6c99d2644923b37e787
refs/remotes/origin/slice/P2-S1 commit f4186342037870c33c50bb5b64a31430b462ac3e
refs/remotes/origin/slice/P2-S2 commit 8c710ca0506e300653779d432fd7e56ae58c4212
refs/remotes/origin/slice/P2-S3 commit 97567579644e74bb955d5e642ba2c96e33c99316
(exit 0)
```

**A2 — plan baseline: head of the base branch now (recorded here only; the Base SHA field is set at Gate 2 from the head re-read under lease — ADR-0011 §9)**
```
$ git rev-parse main
df666070ead7fa21bc72b6c99d2644923b37e787
(exit 0)
```

**A3 — working tree clean AND at the base branch (one predicate, friction #84)**
```
$ git status --porcelain -- . :(exclude)docs/evidence/gatebraid/P2-S4/
(exit 0)
$ bash -c 'git status --porcelain --untracked-files=all | grep -cv '\''docs/evidence/gatebraid/P2-S4/'\'' || true' --form shell --shell-exe bash --pipefail false --exit-code-source pipeline_last
0
(exit 0)
$ git rev-parse HEAD
df666070ead7fa21bc72b6c99d2644923b37e787
(exit 0)
$ git rev-parse main
df666070ead7fa21bc72b6c99d2644923b37e787
(exit 0)
```

**A3 — unfiltered porcelain, so the baseline row's exclusion is auditable**
```
$ git status --porcelain --untracked-files=all
?? docs/evidence/gatebraid/P2-S4/captures/G0-Q1-falsify-badfield.json
?? docs/evidence/gatebraid/P2-S4/captures/G0-Q1-falsify-noauth.json
?? docs/evidence/gatebraid/P2-S4/captures/G0-Q1-identity.json
?? docs/evidence/gatebraid/P2-S4/captures/G0-Q2-approval.json
?? docs/evidence/gatebraid/P2-S4/captures/G0-Q2-falsify.json
?? docs/evidence/gatebraid/P2-S4/captures/G0-Q3-falsify.json
?? docs/evidence/gatebraid/P2-S4/captures/G0-Q3-issue.json
?? docs/evidence/gatebraid/P2-S4/captures/G0-Q4-project.json
[... shown 8 of 23 lines; full output: docs/evidence/gatebraid/P2-S4/captures/G0-porcelain-full.json]
(exit 0)
```

**A4 — Project Environment field vs actual host**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query{node(id:"PVTI_lAHOBRofUs4Beum7zg3ogLM"){... on ProjectV2Item{ fieldValues(first:50){ nodes{ ... on ProjectV2ItemFieldSingleSelectValue{ name optionId field{ ... on ProjectV2FieldCommon{ name } } } } } }}}'
{"data":{"node":{"fieldValues":{"nodes":[{},{},{"name":"Todo","optionId":"f75ad846","field":{"name":"Status"}},{"name":"Backlog","optionId":"d921911c","field":{"name":"Workflow"}},{"name":"—","optionId":"39696bb5","field":{"name":"Gate"}},{"name":"—","optionId":"450ee130","field":{"name":"Next Approval"}},{"name":"mixed-see-prose","optionId":"1e43ec85","field":{"name":"Environment"}},{"name":"Claude Lead","optionId":"ce859c7d","field":{"name":"Executor"}},{"name":"low","optionId":"e291249c","field":{"name":"Risk"}},{},{},{},{}]}}}}
(exit 0)
$ C:/Python312/python.exe -B -c 'import platform,sys,os;print('\''system      :'\'',platform.system());print('\''release     :'\'',platform.release());print('\''version     :'\'',platform.version());print('\''machine     :'\'',platform.machine());print('\''node        :'\'',platform.node());print('\''interpreter :'\'',sys.executable);print('\''py_version  :'\'',sys.version.split()[0])'
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
$ C:/Python312/python.exe -B -c 'import sys,importlib.metadata as m;print('\''CPython'\'',sys.version.split()[0]);print('\''executable'\'',sys.executable);print('\''jsonschema'\'',m.version('\''jsonschema'\''))'
CPython 3.12.2
executable C:\Python312\python.exe
jsonschema 4.23.0
(exit 0)
$ wsl -e bash -lc 'PYTHONDONTWRITEBYTECODE=1 python3 -B -c "import sys,importlib.metadata as m;print('\''CPython'\'',sys.version.split()[0]);print('\''executable'\'',sys.executable);print('\''jsonschema'\'',m.version('\''jsonschema'\''))"'
CPython 3.12.3
executable /usr/bin/python3
jsonschema 4.10.3
(exit 0)
```

**A6 — slice metadata parses against gatebraid/slice@1**
```
$ C:/Python312/python.exe -B -c 'import sys,yaml,importlib.metadata as m;print('\''interpreter :'\'',sys.executable);print('\''CPython     :'\'',sys.version.split()[0]);print('\''PyYAML      :'\'',yaml.__version__);print('\''jsonschema  :'\'',m.version('\''jsonschema'\''));print('\''validator   : Draft202012Validator'\'')'
interpreter : C:\Python312\python.exe
CPython     : 3.12.2
PyYAML      : 6.0.2
jsonschema  : 4.23.0
validator   : Draft202012Validator
(exit 0)
$ C:/Python312/python.exe -B _handoff/batch-o0/validate-slice-metadata.py --schema schema/slice.schema.json --selftest
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
$ C:/Python312/python.exe -B _handoff/batch-o0/validate-slice-metadata.py --schema schema/slice.schema.json --body docs/evidence/gatebraid/P2-S4/captures/slice-body-14.md
--- extracted block ---
schema: gatebraid/slice@1
slice_id: P2-S4
stage: S2
phase: P2
workflow_profile: classic
environment: mixed-see-prose
risk: low
depends_on: []
write_domains:
  - bin/
  - docs/evidence/gatebraid/P2-S4/
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
[... shown 24 of 36 lines; full output: docs/evidence/gatebraid/P2-S4/captures/G0-slice-metadata-validation.json]
(exit 0)
```

### State-packet queries

**Q1 — identity, run first and alone**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login
mianliwang492-source
(exit 0)
```

**Q1 — falsified: bad field name at exit 0, then unauthenticated store**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .no_such_field

(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/AppData/Local/Temp/claude/d--Github-repo-Gatebraid/34a7c816-9f22-4741-981b-faaeaeda1527/scratchpad/empty-gh-config gh api user --jq .login

To get started with GitHub CLI, please run:  gh auth login
Alternatively, populate the GH_TOKEN environment variable with a GitHub API authentication token.
(exit 4)
```

**Q2 — State Packet Approval provenance**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5390640145 --jq '{author: .user.login, url: .html_url, created_at: .created_at, updated_at: .updated_at, association: .author_association}'
{"association":"OWNER","author":"MianliWang","created_at":"2026-08-24T04:14:47Z","updated_at":"2026-08-24T04:14:47Z","url":"https://github.com/MianliWang/gatebraid/issues/14#issuecomment-5390640145"}
(exit 0)
```

**Q2 — falsified**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/1 --jq '{author: .user.login}'
{"message":"Not Found","documentation_url":"https://docs.github.com/rest/issues/comments#get-an-issue-comment","status":"404"}
gh: Not Found (HTTP 404)
(exit 1)
```

**Q3 — the Slice issue**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh issue view 14 --repo MianliWang/gatebraid --json number,state,title,url
{"number":14,"state":"OPEN","title":"P2-S4 — O0 snapshot/frontier hardening: the fail-closed pair","url":"https://github.com/MianliWang/gatebraid/issues/14"}
(exit 0)
```

**Q3 — falsified**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh issue view 999999 --repo MianliWang/gatebraid --json number,state,title,url

GraphQL: Could not resolve to an issue or pull request with the number of 999999. (repository.issue)
(exit 1)
```

**Q4 — the Project**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project view 1 --owner MianliWang

  # Title                                                                                                             
                                                                                                                      
  Mianli Engineering                                                                                                  
                                                                                                                      
  ## Description                                                                                                      
[... shown 6 of 81 lines; full output: docs/evidence/gatebraid/P2-S4/captures/G0-Q4-project.json]
(exit 0)
```

**Q5 — field and option ids, read fresh**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project field-list 1 --owner MianliWang
Title	ProjectV2Field	PVTF_lAHOBRofUs4Beum7zhZGppo
Assignees	ProjectV2Field	PVTF_lAHOBRofUs4Beum7zhZGpps
Status	ProjectV2SingleSelectField	PVTSSF_lAHOBRofUs4Beum7zhZGppw
Labels	ProjectV2Field	PVTF_lAHOBRofUs4Beum7zhZGpp0
Linked pull requests	ProjectV2Field	PVTF_lAHOBRofUs4Beum7zhZGpp4
Milestone	ProjectV2Field	PVTF_lAHOBRofUs4Beum7zhZGpp8
Repository	ProjectV2Field	PVTF_lAHOBRofUs4Beum7zhZGpqA
Reviewers	ProjectV2Field	PVTF_lAHOBRofUs4Beum7zhZGpqE
Parent issue	ProjectV2Field	PVTF_lAHOBRofUs4Beum7zhZGpqI
Sub-issues progress	ProjectV2Field	PVTF_lAHOBRofUs4Beum7zhZGpqM
[... shown 10 of 27 lines; full output: docs/evidence/gatebraid/P2-S4/captures/G0-Q5-field-list.json]
(exit 0)
```

**Q5 — the same read with --format json, for the option ids**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project field-list 1 --owner MianliWang --format json
{"fields":[{"id":"PVTF_lAHOBRofUs4Beum7zhZGppo","name":"Title","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZGpps","name":"Assignees","type":"ProjectV2Field"},{"id":"PVTSSF_lAHOBRofUs4Beum7zhZGppw","name":"Status","options":[{"id":"f75ad846","name":"Todo"},{"id":"47fc9ee4","name":"In Progress"},{"id":"98236657","name":"Done"}],"type":"ProjectV2SingleSelectField"},{"id":"PVTF_lAHOBRofUs4Beum7zhZGpp0","name":"Labels","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZGpp4","name":"Linked pull requests","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZGpp8","name":"Milestone","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZGpqA","name":"Repository","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZGpqE","name":"Reviewers","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZGpqI","name":"Parent issue","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZGpqM","name":"Sub-issues progress","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZGpqQ","name":"Created","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZGpqU","name":"Updated","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZGpqY","name":"Closed","type":"ProjectV2Field"},{"id":"PVTSSF_lAHOBRofUs4Beum7zhZGqt0","name":"Workflow","options":[{"id":"d921911c","name":"Backlog"},{"id":"036a9fdc","name":"Gate 0 — Verifying"},{"id":"f6b57153","name":"Gate 1 — Planning"},{"id":"2ad6af85","name":"Needs Plan Approval"},{"id":"413117f9","name":"Gate 2 — Implementing"},{"id":"9b8a5a62","name":"Needs Review"},{"id":"460a6e5b","name":"Repair Required"},{"id":"21b06e61","name":"Codex Consultation"},{"id":"2d3c4966","name":"Human Diagnosis Required"},{"id":"d2746737","name":"Blocked"},{"id":"ee48415b","name":"Needs Release Approval"},{"id":"fb82cff0","name":"Gate 3 — Releasing"},{"id":"54406fe3","name":"Done"},{"id":"9bb48144","name":"Aborted"}],"type":"ProjectV2SingleSelectField"},{"id":"PVTSSF_lAHOBRofUs4Beum7zhZJbxQ","name":"Gate","options":[{"id":"39696bb5","name":"—"},{"id":"6922003a","name":"G0 passed"},{"id":"2a2ff00e","name":"G1 passed"},{"id":"bd280e21","name":"G2 passed"},{"id":"32d8cac7","name":"G3 passed"}],"type":"ProjectV2SingleSelectField"},{"id":"PVTSSF_lAHOBRofUs4Beum7zhZJcBI","name":"Executor","options":[{"id":"02bd5534","name":"Human"},{"id":"ce859c7d","name":"Claude Lead"},{"id":"f542c3a3","name":"Claude Read-Only Team"},{"id":"5fe71e56","name":"Codex Consultant"},{"id":"01c6f861","name":"Cowork Coordinator"}],"type":"ProjectV2SingleSelectField"},{"id":"PVTSSF_lAHOBRofUs4Beum7zhZJcC8","name":"Next Approval","options":[{"id":"450ee130","name":"—"},{"id":"e45b9ae5","name":"Plan Approval (G1→G2)"},{"id":"1684d5fd","name":"Release Approval (G2→G3)"},{"id":"17102bff","name":"Dirty Baseline Acceptance"},{"id":"6512cd4c","name":"Scope / Allowlist Change"},{"id":"067af845","name":"Environment Change"},{"id":"502b6080","name":"Session Persistence"},{"id":"cacf4f16","name":"Worktree Exception"},{"id":"07e57052","name":"Human Diagnosis"}],"type":"ProjectV2SingleSelectField"},{"id":"PVTSSF_lAHOBRofUs4Beum7zhZJcD0","name":"Environment","options":[{"id":"833d6b16","name":"wsl"},{"id":"b9bddbb2","name":"windows"},{"id":"74d75f0e","name":"macos-authority"},{"id":"1e43ec85","name":"mixed-see-prose"}],"type":"ProjectV2SingleSelectField"},{"id":"PVTSSF_lAHOBRofUs4Beum7zhZJcD4","name":"Risk","options":[{"id":"e291249c","name":"low"},{"id":"18c0a5f4","name":"medium"},{"id":"86949a76","name":"high"}],"type":"ProjectV2SingleSelectField"},{"id":"PVTF_lAHOBRofUs4Beum7zhZJcJM","name":"Stage","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZJcKE","name":"Phase","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZJcOM","name":"Slice","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZJcPU","name":"Base SHA","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZJcQM","name":"Active Branch","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZJcQo","name":"Parallel Group","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZJcSU","name":"Writer Lease","type":"ProjectV2Field"},{"id":"PVTF_lAHOBRofUs4Beum7zhZJcTM","name":"Last Checkpoint","type":"ProjectV2Field"}],"totalCount":27}
(exit 0)
```

**Q5 — falsified**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh project field-list 99 --owner MianliWang --format json

GraphQL: Could not resolve to a ProjectV2 with the number 99. (user.projectV2)
(exit 1)
```

**Q6 — per-item Project field read**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=
query($owner:String!,$repo:String!,$number:Int!){
  repository(owner:$owner,name:$repo){
    issue(number:$number){
      id number title
      projectItems(first:10){
        nodes{
          id
          project{ id title }
          fieldValues(first:50){
            nodes{
              ... on ProjectV2ItemFieldTextValue{ text  field{ ... on ProjectV2FieldCommon{ name } } }
              ... on ProjectV2ItemFieldSingleSelectValue{ name optionId field{ ... on ProjectV2FieldCommon{ name } } }
            }
          }
        }
      }
    }
  }
}' -F owner=MianliWang -F repo=gatebraid -F number=14
{"data":{"repository":{"issue":{"id":"I_kwDOTmww988AAAABN3wEOA","number":14,"title":"P2-S4 — O0 snapshot/frontier hardening: the fail-closed pair","projectItems":{"nodes":[{"id":"PVTI_lAHOBRofUs4Beum7zg3ogLM","project":{"id":"PVT_kwHOBRofUs4Beum7","title":"Mianli Engineering"},"fieldValues":{"nodes":[{},{"text":"P2-S4 — O0 snapshot/frontier hardening: the fail-closed pair","field":{"name":"Title"}},{"name":"Todo","optionId":"f75ad846","field":{"name":"Status"}},{"name":"Backlog","optionId":"d921911c","field":{"name":"Workflow"}},{"name":"—","optionId":"39696bb5","field":{"name":"Gate"}},{"name":"—","optionId":"450ee130","field":{"name":"Next Approval"}},{"name":"mixed-see-prose","optionId":"1e43ec85","field":{"name":"Environment"}},{"name":"Claude Lead","optionId":"ce859c7d","field":{"name":"Executor"}},{"name":"low","optionId":"e291249c","field":{"name":"Risk"}},{"text":"S2","field":{"name":"Stage"}},{"text":"P2","field":{"name":"Phase"}},{"text":"P2-S4","field":{"name":"Slice"}},{"text":"e5e8ee6b8ac0f2fc0da1c9215b18fe6353986893","field":{"name":"Base SHA"}}]}}]}}}}}
(exit 0)
```

**Q6 — falsified: nonexistent issue, bad GraphQL field, and the project-selection step**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=
query($owner:String!,$repo:String!,$number:Int!){
  repository(owner:$owner,name:$repo){
    issue(number:$number){
      id number title
      projectItems(first:10){
        nodes{
          id
          project{ id title }
          fieldValues(first:50){
            nodes{
              ... on ProjectV2ItemFieldTextValue{ text  field{ ... on ProjectV2FieldCommon{ name } } }
              ... on ProjectV2ItemFieldSingleSelectValue{ name optionId field{ ... on ProjectV2FieldCommon{ name } } }
            }
          }
        }
      }
    }
  }
}' -F owner=MianliWang -F repo=gatebraid -F number=999999
{"data":{"repository":{"issue":null}},"errors":[{"type":"NOT_FOUND","path":["repository","issue"],"locations":[{"line":4,"column":5}],"message":"Could not resolve to an Issue with the number of 999999."}]}
gh: Could not resolve to an Issue with the number of 999999.
(exit 1)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query($owner:String!,$repo:String!,$number:Int!){ repository(owner:$owner,name:$repo){ issue(number:$number){ id noSuchFieldOnIssue } } }' -F owner=MianliWang -F repo=gatebraid -F number=14
{"errors":[{"path":["query","repository","issue","noSuchFieldOnIssue"],"extensions":{"code":"undefinedField","typeName":"Issue","fieldName":"noSuchFieldOnIssue"},"locations":[{"line":1,"column":114}],"message":"Field 'noSuchFieldOnIssue' doesn't exist on type 'Issue'"}]}
gh: Field 'noSuchFieldOnIssue' doesn't exist on type 'Issue'
(exit 1)
$ C:/Python312/python.exe -B -c '
import json,base64,sys
cap="docs/evidence/gatebraid/P2-S4/captures/G0-Q6-item-fields.json"
r=json.loads(base64.b64decode(json.load(open(cap,encoding="utf-8"))["streams"]["stdout"]["data"]).decode("utf-8"))
nodes=r["data"]["repository"]["issue"]["projectItems"]["nodes"]
REAL="PVT_kwHOBRofUs4Beum7"
WRONG="PVT_kwHOBRofUs4Beum7_SEEDED_WRONG"
for label,pid in (("real project id",REAL),("SEEDED wrong project id",WRONG)):
    sel=[n for n in nodes if n["project"]["id"]==pid]
    print("%-26s -> %d item(s) selected" % (label,len(sel)))
print()
print("selector falsified: a wrong project id selects ZERO, so the equality test is load-bearing")
print("and an item on a different project could not be read as this project state.")
sys.exit(0)
'
real project id            -> 1 item(s) selected
SEEDED wrong project id    -> 0 item(s) selected

selector falsified: a wrong project id selects ZERO, so the equality test is load-bearing
and an item on a different project could not be read as this project state.
(exit 0)
```

**Q7 — dependencies, both directions**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/14/dependencies/blocked_by
[]
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/14/dependencies/blocking
[]
(exit 0)
```

**Q7 — falsified**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/999999/dependencies/blocked_by
{"message":"Not Found","documentation_url":"https://docs.github.com/rest/issues/issue-dependencies#list-dependencies-an-issue-is-blocked-by","status":"404"}
gh: Not Found (HTTP 404)
(exit 1)
```

**Every capture verified with the capture tool's own write-path guard, re-derivation included**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/checks-g0-verify-captures.py
G0-Q1-falsify-badfield.json                    exit=0  bytes=1764 crlf=0 lone_cr=0
G0-Q1-falsify-noauth.json                      exit=0  bytes=2168 crlf=0 lone_cr=0
G0-Q1-identity.json                            exit=0  bytes=1633 crlf=0 lone_cr=0
G0-Q2-approval.json                            exit=0  bytes=2237 crlf=0 lone_cr=0
G0-Q2-falsify.json                             exit=0  bytes=2215 crlf=0 lone_cr=0
G0-Q3-falsify.json                             exit=0  bytes=2111 crlf=0 lone_cr=0
[... shown 6 of 48 lines; full output: docs/evidence/gatebraid/P2-S4/captures/G0-captures-validation.json]
(exit 0)
```

**Closed-set sweep over every captured response**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/checks-g0-closed-set-sweep.py
captures swept : 39

=== candidate classification (every rule applied explicitly) ===
  E1 permitted repository                                    3
  E3 API-path fragment                                       7
  E4 git ref namespace, not a repository                     16
  E5 filesystem or URL path segment                          43
  E6 schema-id namespace                                     5
  E7 JSON pointer                                            1
  E8 prose slash between ordinary words                      8
  I0 friction citation, not an issue reference               1
  I1 the subject issue                                       1
  I3 mention-class (packet section 2)                        9
  N1 the permitted Project                                   2
  N2 the P2-S4 item                                          2
  N3 field id of the permitted Project                       54
  N4 seeded-invalid probe string (selector falsification)    1

=== every REPOSITORY identity named anywhere ===
  MianliWang/gatebraid           x2    PERMITTED
  MianliWang/gatebraid-scratch   x1    PERMITTED

=== mention-class check: a mention must never appear in an INVOCATION ===
  #7      seen in stdout                       targeted by a query: False
  #8      seen in stdout                       targeted by a query: False
  #10     seen in stdout                       targeted by a query: False
  #12     seen in stdout                       targeted by a query: False
  #13     seen in stdout                       targeted by a query: False
  mention-class issues targeted by a query: 0 (0 required)

domain      : 39 captures (2 of this sweep's own reports excluded)
UNEXPLAINED RESIDUE: 0
(exit 0)
```

**Closed-set sweep, pass 1 — retained as the sweep's own falsification**
```
$ C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/checks-g0-closed-set-sweep.py
captures swept : 39

=== repository-shaped identifiers ===
  ADR-0014/0016              x1    *** OUTSIDE ***
[... shown 4 of 97 lines; full output: docs/evidence/gatebraid/P2-S4/captures/G0-closed-set-sweep-pass1.json]
(exit 1)
```

## Required disclosures

- Deviations: the isolation scope changed between windows and is honoured prospectively. The O0 entry certification recorded that no special source bar applied to this Slice and that the four landed evidence tools were read-and-execute reference; the State Packet Approval section 3 ratifies a stricter bar, used never read. Under the earlier permission this window read part of bin/gatebraid-capture-selftest.py during the independent batch review of 2026-08-23, recorded in that review's section 8 and published as PR 15 comment 5388974846. No tool contents were read after the grant: the four are identified here by path, blob id and size via git ls-tree, and used by execution and --help only.
- Deviations: Q5's protocol sketch does not emit single-select option ids; the same read with --format json does. Both forms are recorded. Protocol state-packet-queries-v1 section 0 makes correcting a sketch against a measured API response verification rather than invention.
- Deviations: Q6 adds optionId to the SingleSelect fragment of the protocol sketch, so option ids are read rather than inferred from labels. Same clause as above.
- Deviations: the bare name claude is an extensionless npm shim and is not executable in argv form on this host; the .cmd wrapper is, and is the form the committed P2-S3 record used. Precedent followed.
- Deviations: A6's first attempt placed the capture tool's --form and --shell-exe flags after the argv separator, so they were consumed as the child's arguments and the read ran through a nested shell whose gh was unauthenticated. The capture recorded exit 4 and produced a zero-byte body file, on which the metadata checker errored rather than passing; both fail-closed behaviours fired as designed. The read was re-run in argv form with the body file written from the captured bytes and proved byte-equal to them. The failed attempt is retained at captures/G0-slice-body-failed-attempt.json with its checker run at captures/G0-slice-metadata-validation-on-empty.json.
- Deviations: the closed-set sweep's first pass returned 39 candidates under an incomplete rule set and is retained at captures/G0-closed-set-sweep-pass1.json with exit 1. The rule set was completed and two defects repaired: the sweep excludes its own reports, a self-reference of the IN-03 class, and reports residue by kind and location without echoing the token, per ADR-0028 section 3. Pass 1 is kept deliberately as this instrument's own falsification, since a sweep that has only ever returned empty has never been shown able to fire.
- Deviations: Q7 carries a measured gap. No non-empty dependency sample was taken, because the only known-related pair lives in the scratch repository, which the packet's closed set names but bars from any query. The nonexistent-issue seed shows the endpoint discriminates, 404 against 200 with an empty array, so the empty result is a read rather than a silent default. Reported as a gap per protocol state-packet-queries-v1 section 3, and not resolved by widening the closed set.
- Deviations: A3's predicate is evaluated over the baseline excluding this gate's own write domain. The unfiltered view is recorded beside it and shows zero entries outside that domain. The Gate 0 contract's Exit clause makes this gate's own evidence files not a violation.
- Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; shell Git Bash MINGW64 with Git for Windows 2.51.0.windows.1 whose system configuration carries core.autocrlf=true; every gh call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL /usr/bin/python3 with CPython 3.12.3, jsonschema 4.10.3. environment=mixed-see-prose: the gate ran on the Windows host and the WSL half is evidence.

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S4
gate: 0
environment: mixed-see-prose
executor: Claude Lead
base_sha: df666070ead7fa21bc72b6c99d2644923b37e787
started_at: "2026-08-24T04:19:24Z"
ended_at: "2026-08-24T04:39:23Z"
result: passed
approvals:
  - type: State Packet Approval
    author: MianliWang
    comment_url: "https://github.com/MianliWang/gatebraid/issues/14#issuecomment-5390640145"
    at: "2026-08-24T04:14:47Z"
checks:
  - name: repo-identity-and-remote
    command: "git remote -v"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-remote.json"
  - name: ref-namespace-enumerated
    command: "git for-each-ref"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-ref-namespace.json"
  - name: base-sha-recorded
    command: "git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-baseline-main.json"
  - name: working-tree-clean-at-base
    command: "git status --porcelain (baseline, excluding this gate's write domain); git rev-parse HEAD; git rev-parse main"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-porcelain-baseline.json"
  - name: working-tree-unfiltered-audit
    command: "git status --porcelain --untracked-files=all"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-porcelain-full.json"
  - name: environment-matches-host
    command: "gh api graphql (Environment field read); python host probe"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-env-field.json"
  - name: tool-versions
    command: "claude.cmd --version; git --version; gh --version; codex --version; python version probe on both halves"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-tools-git.json"
  - name: slice-metadata-checker-falsified
    command: "validate-slice-metadata.py --schema schema/slice.schema.json --selftest"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-slice-metadata-selftest.json"
  - name: slice-metadata-parses
    command: "validate-slice-metadata.py --schema schema/slice.schema.json --body captures/slice-body-14.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-slice-metadata-validation.json"
  - name: packet-Q1-identity
    command: "gh api user --jq .login"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q1-identity.json"
  - name: packet-Q1-falsified
    command: "gh api user --jq .no_such_field; gh api user --jq .login against an empty store"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q1-falsify-badfield.json"
  - name: packet-Q2-approval-provenance
    command: "gh api repos/MianliWang/gatebraid/issues/comments/5390640145"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q2-approval.json"
  - name: packet-Q2-falsified
    command: "gh api repos/MianliWang/gatebraid/issues/comments/1"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q2-falsify.json"
  - name: packet-Q3-slice-issue
    command: "gh issue view 14 --repo MianliWang/gatebraid --json number,state,title,url"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q3-issue.json"
  - name: packet-Q3-falsified
    command: "gh issue view 999999 --repo MianliWang/gatebraid --json number,state,title,url"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q3-falsify.json"
  - name: packet-Q4-project
    command: "gh project view 1 --owner MianliWang"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q4-project.json"
  - name: packet-Q5-field-and-option-ids
    command: "gh project field-list 1 --owner MianliWang; the same read with --format json"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q5-field-list-json.json"
  - name: packet-Q5-falsified
    command: "gh project field-list 99 --owner MianliWang --format json"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q5-falsify.json"
  - name: packet-Q6-item-field-read
    command: "gh api graphql, protocol form with optionId, owner=MianliWang repo=gatebraid number=14"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q6-item-fields.json"
  - name: packet-Q6-falsified
    command: "the same form at number=999999; the same form with a field absent from the GraphQL schema; the project-selection step against a seeded wrong project id"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q6-falsify-selector.json"
  - name: packet-Q7-dependencies-both-directions
    command: "gh api repos/MianliWang/gatebraid/issues/14/dependencies/blocked_by ; gh api repos/MianliWang/gatebraid/issues/14/dependencies/blocking"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q7-blocked-by.json"
  - name: packet-Q7-falsified
    command: "gh api repos/MianliWang/gatebraid/issues/999999/dependencies/blocked_by"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-Q7-falsify.json"
  - name: capture-set-validated
    command: "C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/checks-g0-verify-captures.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-captures-validation.json"
  - name: closed-set-sweep
    command: "C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S4/checks-g0-closed-set-sweep.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S4/captures/G0-closed-set-sweep.json"
evidence_files:
  - docs/evidence/gatebraid/P2-S4/gate0.md
notes: "Startability read from the operator-approved closed-set state packet under its own State Packet Approval: the Gate 0 contract Entry's explicit third case, and the packet mechanism's final enumerated use. No bootstrap_exception, because N2 and N3 exist and this record carries full validation. The Base SHA Project field reads the setup-time value e5e8ee6b and is written at Gate 2 when Active Branch is cut under the lease, per contract Action 2."
```
