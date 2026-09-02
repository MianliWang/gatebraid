# Gate 2 evidence - P2-S5

## Entry records

**E1 - Plan Approval verified: fetched BY ID, author observed, and the executor identity it is compared against**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api repos/MianliWang/gatebraid/issues/comments/5503291709 --jq {id:.id,author:.user.login,author_association:.author_association,created:.created_at,updated:.updated_at,len:(.body|length)}
{"author":"MianliWang","author_association":"OWNER","created":"2026-09-02T02:10:57Z","id":5503291709,"len":5181,"updated":"2026-09-02T02:10:57Z"}
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api user --jq .login
mianliwang492-source
(exit 0)
```

**E1b - the door's fidelity check against the committed source**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid PYTHONDONTWRITEBYTECODE=1 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'T=docs/evidence/gatebraid/P2-S5/g2/dryrun-out/approval-fetched.txt; gh api repos/MianliWang/gatebraid/issues/comments/5503291709 --jq .body > "$T"; echo "source file  : $(sha256sum _handoff/prompts/GH-COMMENT-PLAN-APPROVAL-P2S5.md | cut -d" " -f1)  $(wc -c < _handoff/prompts/GH-COMMENT-PLAN-APPROVAL-P2S5.md) bytes"; echo "fetched body : $(sha256sum "$T" | cut -d" " -f1)  $(wc -c < "$T") bytes"; if cmp -s _handoff/prompts/GH-COMMENT-PLAN-APPROVAL-P2S5.md "$T"; then echo "verdict      : BYTE-IDENTICAL"; else echo "verdict      : DIFFERS"; fi; echo "names plan_hash      : $(grep -c b2cd75f6a49bb056fd16bc3d2f4cfd5cf98ae8515b5761908add2ed5405cc424 "$T")"; echo "names allowlist_hash : $(grep -c 4110b3021bdfc2fcda1f5f90528db01eb87b554177e2176ccfba46ccd6ca3750 "$T")"; echo "is a handoff block   : $(grep -c "gatebraid/handoff@1" "$T")"; echo "strikethrough        : $(grep -c -- "~~" "$T")"; rm -f "$T"'
source file  : fed6bcb9cb3e8dbce0bed06819ce9b0c2907ad3234c3e8ab5016c591f358e46d  5226 bytes
fetched body : fed6bcb9cb3e8dbce0bed06819ce9b0c2907ad3234c3e8ab5016c591f358e46d  5226 bytes
verdict      : BYTE-IDENTICAL
names plan_hash      : 1
names allowlist_hash : 1
is a handoff block   : 0
strikethrough        : 0
(exit 0)
```

**E1c - the door CONSUMED: Next Approval to the bare option, needs-human removed**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f query=mutation($p:ID!,$i:ID!,$f:ID!,$o:String!){updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,value:{singleSelectOptionId:$o}}){projectV2Item{id}}} -f p=PVT_kwHOBRofUs4Beum7 -f i=PVTI_lAHOBRofUs4Beum7zg4E8qs -f f=PVTSSF_lAHOBRofUs4Beum7zhZJcC8 -f o=450ee130
{"data":{"updateProjectV2ItemFieldValue":{"projectV2Item":{"id":"PVTI_lAHOBRofUs4Beum7zg4E8qs"}}}}
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh issue edit 17 --repo MianliWang/gatebraid --remove-label needs-human
https://github.com/MianliWang/gatebraid/issues/17
(exit 0)
```

**E2 - Writer Lease taken, and Workflow moved to the implementing option**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f query=mutation($p:ID!,$i:ID!,$f:ID!,$t:String!){updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,value:{text:$t}}){projectV2Item{id}}} -f p=PVT_kwHOBRofUs4Beum7 -f i=PVTI_lAHOBRofUs4Beum7zg4E8qs -f f=PVTF_lAHOBRofUs4Beum7zhZJcSU -f t=RoughEgoist:p2s5-g2:2026-09-02T02:58:10Z
{"data":{"updateProjectV2ItemFieldValue":{"projectV2Item":{"id":"PVTI_lAHOBRofUs4Beum7zg4E8qs"}}}}
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f query=mutation($p:ID!,$i:ID!,$f:ID!,$o:String!){updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,value:{singleSelectOptionId:$o}}){projectV2Item{id}}} -f p=PVT_kwHOBRofUs4Beum7 -f i=PVTI_lAHOBRofUs4Beum7zg4E8qs -f f=PVTSSF_lAHOBRofUs4Beum7zhZGqt0 -f o=413117f9
{"data":{"updateProjectV2ItemFieldValue":{"projectV2Item":{"id":"PVTI_lAHOBRofUs4Beum7zg4E8qs"}}}}
(exit 0)
```

**E3 - baseline re-read under the lease: X from the re-run record file, Y measured**
```
$ 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'REC=docs/evidence/gatebraid/P2-S5/g0r/gate0.md; X=$(grep -m1 "^base_sha:" "$REC" | awk "{print \$2}"); Y=$(git rev-parse main); echo "record read for X : docs/evidence/gatebraid/P2-S5/g0r/gate0.md"; echo "X (plan baseline) : $X"; echo "Y (measured head) : $Y"; echo "X == Y            : $([ "$X" = "$Y" ] && echo yes || echo no)"; echo "changed paths X..Y:"; git diff --name-only "$X".."$Y" | sed "s/^/   /"; echo "count             : $(git diff --name-only "$X".."$Y" | wc -l)"'
record read for X : docs/evidence/gatebraid/P2-S5/g0r/gate0.md
X (plan baseline) : cbd065893b37f20713ae35b8d2673bf26fe4d2ad
Y (measured head) : cbd065893b37f20713ae35b8d2673bf26fe4d2ad
X == Y            : yes
changed paths X..Y:
count             : 0
(exit 0)
```

- baseline: `unchanged`

**E4 - Active Branch created from Y; Base SHA set to Y; every field read back**
```
$ 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'git rev-parse --abbrev-ref HEAD; git rev-parse HEAD; git log --oneline cbd065893b37f20713ae35b8d2673bf26fe4d2ad..HEAD | cat'
slice/P2-S5
c07d0cb2bd6926352c9e1abc90c7d67129b00ad6
c07d0cb evidence(p2-s5): Gate 2 instruments and the captured declared runs
629e287 feat(o1): gatebraid-ready, the Ready Frontier composer, and its selftest
63c6ea8 evidence(p2-s5): the Gate 0 record, its re-run, and Gate 1 ride onto the branch
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f query=mutation($p:ID!,$i:ID!,$f:ID!,$t:String!){updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,fieldId:$f,value:{text:$t}}){projectV2Item{id}}} -f p=PVT_kwHOBRofUs4Beum7 -f i=PVTI_lAHOBRofUs4Beum7zg4E8qs -f f=PVTF_lAHOBRofUs4Beum7zhZJcPU -f t=cbd065893b37f20713ae35b8d2673bf26fe4d2ad
{"data":{"updateProjectV2ItemFieldValue":{"projectV2Item":{"id":"PVTI_lAHOBRofUs4Beum7zg4E8qs"}}}}
(exit 0)
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid gh api graphql -f 'query=query{node(id:"PVTI_lAHOBRofUs4Beum7zg4E8qs"){... on ProjectV2Item{fieldValues(first:50){nodes{... on ProjectV2ItemFieldSingleSelectValue{optionId name field{... on ProjectV2FieldCommon{name}}} ... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2FieldCommon{name}}}}}}}}'
{"data":{"node":{"fieldValues":{"nodes":[{},{"text":"P2-S5 — O1 gatebraid-ready: the fourth attempt on the frozen scope","field":{"name":"Title"}},{"optionId":"f75ad846","name":"Todo","field":{"name":"Status"}},{"optionId":"413117f9","name":"Gate 2 — Implementing","field":{"name":"Workflow"}},{"optionId":"2a2ff00e","name":"G1 passed","field":{"name":"Gate"}},{"optionId":"450ee130","name":"—","field":{"name":"Next Approval"}},{"optionId":"1e43ec85","name":"mixed-see-prose","field":{"name":"Environment"}},{"optionId":"ce859c7d","name":"Claude Lead","field":{"name":"Executor"}},{"optionId":"e291249c","name":"low","field":{"name":"Risk"}},{"text":"S2","field":{"name":"Stage"}},{"text":"P2","field":{"name":"Phase"}},{"text":"P2-S5","field":{"name":"Slice"}},{"text":"cbd065893b37f20713ae35b8d2673bf26fe4d2ad","field":{"name":"Base SHA"}},{"text":"2026-09-01T22:26Z P2-S5 GATE 1 COMPLETE; plan+allowlist FROZEN; Needs Plan Approval. Scope READ not remembered: 7 docs at scratch dcd8e851, each sha256-pinned, pin FALSIFIED vs the parent commit. 4 deltas vs the landed pair. D-4 found BY the dry-run: the producer returns exit 3 with a DEGRADED DOCUMENT, so its status is INTERPRETED not tested vs zero; the D6 command changed before the freeze. D11 criterion corrected: capture stamps platform.os wsl, not linux. plan_hash b2cd75f6, allowlist_hash 4110b302, gate1.md 78a3f94a, each reproducible. 7 of 8 historical ready-failure classes killed at D2; IN-01 absent from the corpus by its own known_limitation, NOT claimed. 6 negative criteria, all falsified before trust; N3 carries a CONTENT limb. 2 typed fails, disclosed: source limbs report the absent deliverable; the sweep's explanation limb has residue and the instrument was NOT edited. Retained record re-measured UNCHANGED 83b3a273. No commit, push, branch, lease. handoff 5501157052. GATE 2 NOT OPENED.","field":{"name":"Last Checkpoint"}},{"text":"RoughEgoist:p2s5-g2:2026-09-02T02:58:10Z","field":{"name":"Writer Lease"}}]}}}}
(exit 0)
```

**E4b - the evidence that rides on, measured AFTER its commit**
```
$ 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'echo "retained-set path-list digest:"; find docs/evidence/gatebraid/P2-S5 -type f -not -path "*/g0r/*" -not -path "*/g1/*" -not -path "*/g2/*" | sort | tr -d "\r" | sha256sum; echo "retained file count: $(find docs/evidence/gatebraid/P2-S5 -type f -not -path "*/g0r/*" -not -path "*/g1/*" -not -path "*/g2/*" | wc -l)"; echo; echo "the three pinned records:"; sha256sum docs/evidence/gatebraid/P2-S5/gate0.md docs/evidence/gatebraid/P2-S5/g0r/gate0.md docs/evidence/gatebraid/P2-S5/g1/gate1.md; echo; echo "the evidence commit, additions only:"; git diff --name-status cbd065893b37f20713ae35b8d2673bf26fe4d2ad..63c6ea8678bb04bf0ab238ddc62f2e22be08a410 | awk "{print \$1}" | sort | uniq -c; echo "paths outside docs/evidence/gatebraid/P2-S5/: $(git diff --name-only cbd065893b37f20713ae35b8d2673bf26fe4d2ad..63c6ea8678bb04bf0ab238ddc62f2e22be08a410 | grep -vc "^docs/evidence/gatebraid/P2-S5/")"'
retained-set path-list digest:
83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f *-
retained file count: 43

the three pinned records:
be7c338896b1015923671988166d55af3bd59e028660ce89dfd3b69bc7251513 *docs/evidence/gatebraid/P2-S5/gate0.md
95ff39111b4a8b8aa43c022e877c98af5f868b054f4ac2c116ae5c67327bc4e6 *docs/evidence/gatebraid/P2-S5/g0r/gate0.md
78a3f94a2a8b23efb1e36b231ce8932b1c693fa79dee5f657ae5968d29943c70 *docs/evidence/gatebraid/P2-S5/g1/gate1.md

the evidence commit, additions only:
    158 A
paths outside docs/evidence/gatebraid/P2-S5/: 0
(exit 0)
```

## Verification outputs

**V0 D0 - the frozen scope still re-derives at the pinned commit**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/scope-pin.py
historical record : MianliWang/gatebraid-scratch
pinned commit     : dcd8e851bb508a2e17a6949434fc7c10354506c1
reading at        : dcd8e851bb508a2e17a6949434fc7c10354506c1
resolves to       : dcd8e851bb508a2e17a6949434fc7c10354506c1  MATCH

document                                       bytes    sha256 re-derived
README.md                                      984      e0a5b2689f0e9f08f680077c5cd29f9a1f0f230c78260c39b10542cdf690c730  MATCH
docs/evidence/gatebraid/P1-S3/gate0.md         9000     cc783192e688e677a18d49febedc1cfb1174c8e875056062284d7b7d4e242f81  MATCH
docs/evidence/gatebraid/P1-S3/gate1.md         24576    0966759be9e1b05fea310965e6ac36112244185f6434647bb3f1ec2ed32b21cb  MATCH
docs/evidence/gatebraid/P1-S5/gate0.md         14387    a0fd819614744faf9317f84f4b6532e249fe32c3d35307dabd28160cd356d145  MATCH
docs/evidence/gatebraid/P1-S5/gate1.md         26299    edfc92054015b7190ba79eb94c9da114ce0eec4714acdd3b301628550ee74f33  MATCH
docs/evidence/gatebraid/P1-S6/gate0.md         5996     89af2e287272947f307b2f72d9541e481c508c9e90c6d99cd994061282698c5c  MATCH
docs/evidence/gatebraid/P1-S6/gate1.md         19371    b190299bccaa906548d44477eca18e5579cbb480e4192c52fba5f801bd71920f  MATCH

scope assertions, each required in ALL THREE attempts:
   bin/gatebraid-ready.py   in 3 of 3  ok     the one file the scope delivers
   --snapshot-command       in 3 of 3  ok     the flag whose stated reason is that the guard paths must be runnable, not merely asserted
   --strict                 in 3 of 3  ok     the flag the M2 consumer accepted

SCOPE PIN HOLDS: the commit resolves and every document re-derives to the frozen hash
(exit 0)
```

**V0F D0F - the same instrument at the pinned commit's parent: the pin fires**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/scope-pin.py --commit a8e15e0de2d5df285a79c8a34d1a966fee86e678
historical record : MianliWang/gatebraid-scratch
pinned commit     : dcd8e851bb508a2e17a6949434fc7c10354506c1
reading at        : a8e15e0de2d5df285a79c8a34d1a966fee86e678   (OVERRIDDEN - falsification run)
resolves to       : a8e15e0de2d5df285a79c8a34d1a966fee86e678  *** NOT THE PINNED COMMIT ***
[... shown 14 of 20 lines; full output: docs/evidence/gatebraid/P2-S5/g2\captures/G2-D0F-scope-pin-falsify.json]
docs/evidence/gatebraid/P1-S5/gate1.md         26299    edfc92054015b7190ba79eb94c9da114ce0eec4714acdd3b301628550ee74f33  MATCH
docs/evidence/gatebraid/P1-S6/gate0.md         5996     89af2e287272947f307b2f72d9541e481c508c9e90c6d99cd994061282698c5c  MATCH
docs/evidence/gatebraid/P1-S6/gate1.md         -        *** ABSENT AT THIS COMMIT ***

scope assertions, each required in ALL THREE attempts:
   bin/gatebraid-ready.py   in 2 of 3  FAIL   the one file the scope delivers
   --snapshot-command       in 2 of 3  FAIL   the flag whose stated reason is that the guard paths must be runnable, not merely asserted
   --strict                 in 2 of 3  FAIL   the flag the M2 consumer accepted

SCOPE PIN STALE: 5 item(s) did not re-derive
(exit 1)
```

**V1 D1 - the frozen corpus digest is unmoved by this Slice**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B fixtures/runner-selftest.py
condition                           want  got  verdict  required observation
S00 untouched copy                     0    0  PASS     CORPUS CLEAN
[... shown 16 of 37 lines; full output: docs/evidence/gatebraid/P2-S5/g2\captures/G2-D1-corpus-digest.json]
S27 __pycache__ present                0    0  PASS     CORPUS CLEAN
S11 unexpected argument                2    2  PASS     unexpected argument
S15 cwd-independence holds             0    0  PASS     CORPUS CLEAN from both
S16 cwd-independence falsified       !=0    2  PASS     must NOT be clean from elsewhere
S21 digest sees run-corpus.py       moves  moves  PASS     digest must change when the file changes
S22 digest sees runner-selftest.py  moves  moves  PASS     digest must change when the file changes
S28 __pycache__ moves no digest     same  same  PASS     digest must ignore interpreter output

digest scope                  : bytes-platform, evidence-capture-v1, gate-run-v2, instruments, live-shapes, metrics-v1, state-pipeline, CORPORA.json, schema, run-corpus.py, runner-selftest.py, fixtures/ listing
digest before                 : 73c5e059091982ac8cda43d9f59902f3934444b742e7a383ad9422448cd5fdfc
digest after                  : 73c5e059091982ac8cda43d9f59902f3934444b742e7a383ad9422448cd5fdfc
seed-reachable surface UNMODIFIED: True
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required exit status
(exit 0)
```

**V2 D2 - the historical ready-failure classes the frozen corpus holds, each killed on a named locus**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B fixtures/run-corpus.py
corpus bytes-platform (v1.1)  <- fixtures\bytes-platform\EXPECTATIONS.json
  loader recorded: CPython 3.12.2 (C:/Python312/python.exe), jsonschema 4.23.0, Draft202012Validator; re-measured identical under CPython 3.12.3 / jsonschema 4.10.3 on WSL
  ok   BP1-01  valid as recorded  [positive control �� one report, one platform, honestly claimed]
  ok   BP1-02  valid as recorded  [positive control �� the only legitimate way to claim both platforms]
  ok   BP1-03  killed on required@properties/1/replay:rederived_sha256 [properties/properties/items/properties/replay/required]  [BP-01 blocked remainder �� sha256 over raw bytes fails to re-derive]
  ok   BP1-04  killed on pattern@properties/1/replay/rederived_sha256 [properties/properties/items/properties/replay/properties/rederived_sha256/pattern]  [BP-02 blocked remainder �� byte_length mismatch caught]
  ok   BP1-05  killed on minItems@dual_platform_claim/reports [properties/dual_platform_claim/properties/reports/minItems]  [BP-03 �� one platform's capture presented as covering both]
  ok   BP1-06  killed on uniqueItems@dual_platform_claim/reports [properties/dual_platform_claim/properties/reports/uniqueItems]  [BP-03 �� the item verbatim: the same capture cited for both platforms]
  ok   BP1-07  killed on type@platform [properties/platform/type]  [BP-03 �� one report presenting ITSELF as covering both]
  ok   BP1-08  killed on required@properties/1:replay [properties/properties/items/allOf/0/then/required]  [BP-01 / BP-02 claim discipline �� a replayed claim with nothing behind it]

corpus evidence-capture-v1 (v1.1)  <- fixtures\evidence-capture-v1\EXPECTATIONS.json
[... shown 26 of 156 lines; full output: docs/evidence/gatebraid/P2-S5/g2\captures/G2-D2-corpus.json]
  ok   SP1-07  killed on const@sources/0/status [properties/sources/items/allOf/2/then/properties/status/const]  [SP-03 rate limit]
  ok   SP1-08  killed on const@sources/0/complete [properties/sources/items/allOf/3/then/properties/complete/const]  [SP-04 network / server error]
  ok   SP1-09  killed on const@items/0/verdict [allOf/0/then/properties/items/items/properties/verdict/const]  [SP-05 malformed GitHub response]
  ok   SP1-10  killed on required@sources/0:bounded [properties/sources/items/allOf/4/then/required]  [SP-06 missing dependency page]
  ok   SP1-11  killed on const@sources/0/complete [properties/sources/items/allOf/5/then/properties/complete/const]  [SP-07 truncated connections]
  ok   SP1-12  killed on const@items/0/verdict [properties/items/items/allOf/0/then/properties/verdict/const]  [SP-08 unknown Issue state]
  ok   SP1-13  killed on not@items/0 [properties/items/items/allOf/1/then/not], required@items/0:excluded_reason [properties/items/items/allOf/1/then/required]  [SP-09 non-Slice Project item]
  ok   SP1-14  killed on required@(root):schema [required]  [SP-10 missing snapshot schema / version]
  ok   SP1-15  killed on required@items/0/dependencies:blocking [properties/items/items/properties/dependencies/required]  [SP-11 one-direction dependency loss]
  ok   SP1-16  killed on required@items/0/soft_dependencies:parse_status [properties/items/items/properties/soft_dependencies/required]  [SP-12 soft Gate-1/Gate-2 dependency unsatisfied]
  ok   SP1-17  killed on not@items/0/verdict [properties/items/items/allOf/5/then/properties/verdict/not]  [SP-13 aborted item presented as ready]

TOTAL: 133 passed, 0 failed
CORPUS CLEAN
(exit 0)
```

**V3 D3 - the ready selftest, Windows half: twenty seeded conditions, each emitting its own row**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready-selftest.py
id     condition                                                        want         got          verdict required observation
S01    a healthy document composes and exits 0                          0            0            PASS    a composer that rejected everything would fail HERE and pass every negative below
S01b   the consumer's report is passed through BYTE-FOR-BYTE            <5127 bytes> <5127 bytes> PASS    byte passthrough, not text: re-emitting decoded text through a text-mode stdout would translate every embedded newline again
S02    producer status 1 (declared: no document) is exit 10             10           10           PASS    a status meaning no document must never reach the consumer
S02b   and stdout stays empty                                           <0 bytes>    <0 bytes>    PASS    stdout carries exactly one JSON document or nothing
S03    producer status 2 (declared: no document) is exit 10             10           10           PASS    a status meaning no document must never reach the consumer
S03b   and stdout stays empty                                           <0 bytes>    <0 bytes>    PASS    stdout carries exactly one JSON document or nothing
S04    producer status 3 (declared: emitted and DEGRADED) passes the do 3            3            PASS    D-4: reading any non-zero status as failure would DISCARD a lawful document and hide the degradation from the only tool that types it
S04b   and the report is still on stdout                                <844 bytes>  <844 bytes>  PASS    --strict changed the exit code and never the output; the consumer now applies that unconditionally
S05    an undeclared producer status is exit 10                         10           10           PASS    an unknown status is treated as no-document, never as success
S06    producer bytes that are not valid UTF-8 are exit 11              11           11           PASS    the same two bytes that broke the M2 pipeline; no encoding is guessed
S06b   and stdout stays empty                                           <0 bytes>    <0 bytes>    PASS    a best-effort decode would turn a loud failure into corruption inside a state document
S06c   and the refusal names the offending byte and its position        True         True         PASS    a guard that fires without naming what it caught is not evidence
S07    a decodable but malformed document returns the consumer's own re 1            1            PASS    the consumer's codes are reused rather than renumbered (D-1)
S07b   and no verdict is emitted                                        <0 bytes>    <0 bytes>    PASS    no verdict is invented for a document the consumer refused
S08    --strict is accepted and changes the exit status not at all      0            0            PASS    D-2: the flag is kept so a caller written against the frozen surface still runs; rejecting it would break that surface
S08b   and changes the output not at all                                <5127 bytes> <5127 bytes> PASS    a flag that silently altered the document would be worse than one that errored
S09    a composition whose FIRST stage fails and whose second would suc 10           10           PASS    IN-01, the class the frozen corpus does not hold: the stub emits a VALID document and exits 1, so a composer testing only the document would return 0
S09b   and the valid document is not forwarded                          <0 bytes>    <0 bytes>    PASS    the producer's status governs, not the shape of what it wrote
S10    the D-4 partition covers exactly the producer's declared space   [0, 1, 2, 3] [0, 1, 2, 3] PASS    the partition is transcribed from the producer's docstring, so it is checked against that docstring rather than trusted
S11    every condition was served by a stub or a committed document     0            0            PASS    a selftest that reached the control plane would be measuring the network, not the composer

tool under test               : D:\Github repo\Gatebraid\bin\gatebraid-ready.py
interpreter                   : C:\Python312\python.exe
documents (committed, frozen) : docs/evidence/gatebraid/P2-S5/g1/captures/g1-snapshot.json, docs/evidence/gatebraid/P2-S6/g1/dryrun-out/g2-snapshot.json
files written by this suite   : 0
network reads performed       : 0 (every producer is a stub)
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required outcome
(exit 0)
```

**V4 D4 - the same selftest, WSL half**
```
$ wsl.exe -e bash -lc 'cd '\''/mnt/d/Github repo/Gatebraid'\'' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-ready-selftest.py'
id     condition                                                        want         got          verdict required observation
S01    a healthy document composes and exits 0                          0            0            PASS    a composer that rejected everything would fail HERE and pass every negative below
S01b   the consumer's report is passed through BYTE-FOR-BYTE            <5127 bytes> <5127 bytes> PASS    byte passthrough, not text: re-emitting decoded text through a text-mode stdout would translate every embedded newline again
S02    producer status 1 (declared: no document) is exit 10             10           10           PASS    a status meaning no document must never reach the consumer
[... shown 14 of 29 lines; full output: docs/evidence/gatebraid/P2-S5/g2\captures/G2-D4-selftest-wsl.json]
S10    the D-4 partition covers exactly the producer's declared space   [0, 1, 2, 3] [0, 1, 2, 3] PASS    the partition is transcribed from the producer's docstring, so it is checked against that docstring rather than trusted
S11    every condition was served by a stub or a committed document     0            0            PASS    a selftest that reached the control plane would be measuring the network, not the composer

tool under test               : /mnt/d/Github repo/Gatebraid/bin/gatebraid-ready.py
interpreter                   : /usr/bin/python3
documents (committed, frozen) : docs/evidence/gatebraid/P2-S5/g1/captures/g1-snapshot.json, docs/evidence/gatebraid/P2-S6/g1/dryrun-out/g2-snapshot.json
files written by this suite   : 0
network reads performed       : 0 (every producer is a stub)
conditions failed             : 0
SELFTEST CLEAN: every seeded condition produced its required outcome
(exit 0)
```

**V5 D5 - the live end-to-end composition against the real control plane**
```
$ GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready.py
{
 "consumer": {
  "name": "gatebraid-frontier",
  "version": "1.0.0"
[... shown 20 of 214 lines; full output: docs/evidence/gatebraid/P2-S5/g2\captures/G2-D5-live-ready.json]
SNAPSHOT OK: every source read completely with status `ok`

consumer                      : gatebraid-frontier 1.0.0

validated against             : D:\Github repo\Gatebraid\schema\snapshot.schema.json sha256=95ecf38e927a18e58cace007607caa016d188893c2d92ea3ea748c46453419d6

items excluded (no verdict)   : 4

startable                     : 9

blocked                       : 3

undecidable                   : 0

FRONTIER OK: the snapshot validated and every verdict was re-derived from it

(exit 0)
```

**V6 D6 - a producer status meaning NO DOCUMENT is exit 10**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready.py --snapshot-command 'C:/Python312/python.exe -B bin/gatebraid-snapshot.py --replay docs/evidence/gatebraid/P2-S5/g1/dryrun-out/no-such-transcript.json'

USAGE: no transcript at docs/evidence/gatebraid/P2-S5/g1/dryrun-out/no-such-transcript.json

PRODUCER REPORTED NO DOCUMENT: exit 2 (declared status meaning no document); nothing is emitted and no verdict is invented
(exit 10)
```

**V7 D7 - producer bytes that are not valid UTF-8 are exit 11, and stdout stays empty**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready.py --snapshot-command 'C:/Python312/python.exe -c "import sys;q=chr(34);s='\''{'\''+q+'\''name'\''+q+'\'': '\''+q+'\''Gate 0 '\''+chr(0x2014)+'\'' Verifying'\''+q+'\''}'\'';sys.stdout.buffer.write(s.encode('\''cp936'\''))"'

PRODUCER OUTPUT IS NOT VALID UTF-8: 'utf-8' codec can't decode byte 0xa1 in position 17: invalid start byte
The offending byte is at position 17. No encoding is guessed: a best-effort decode would turn this loud failure into corruption inside a state document.
(exit 11)
```

**V8 D8 - a decodable but malformed document returns the consumer's OWN refusal code**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready.py --snapshot-command 'C:/Python312/python.exe -c "import sys;sys.stdout.buffer.write(chr(123).encode()+chr(125).encode())"'

SNAPSHOT REFUSED: the document does not say what it is: `schema` is absent, so it cannot be consumed as if current

verdicts emitted             : 0 (no verdict is emitted for a document this tool could not validate)

(exit 1)
```

**V9 D9 - the six negative criteria hold, PINNED to base..fingerprint so the row reproduces**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g2/negative-criteria.py --base cbd065893b37f20713ae35b8d2673bf26fe4d2ad..629e287faab01a84935a93a2dc265d369a6a5c33
changed-path source : git
base                : cbd065893b37f20713ae35b8d2673bf26fe4d2ad..629e287faab01a84935a93a2dc265d369a6a5c33
changed paths       : 197
   bin/gatebraid-ready-selftest.py
   bin/gatebraid-ready.py
   docs/evidence/gatebraid/P2-S5/captures/G0-baseline-main.json
[... shown 22 of 32 lines; full output: docs/evidence/gatebraid/P2-S5/g2\captures/G2-D9-negative-pinned.json]
allowlist           : bin/, docs/evidence/gatebraid/P2-S5/
code surface        : bin/gatebraid-ready.py, bin/gatebraid-ready-selftest.py
transitive target   : bin/gatebraid-snapshot.py
consumer            : bin/gatebraid-frontier.py
frozen root         : docs/evidence/gatebraid/P2-S5

N1 every changed path inside the allowlist         : holds
N2 under bin/, only the ready pair is touched      : holds
N3 no frozen input is written                      : holds
N4 no runtime dependency, no HTTP client           : holds
N5 no control-plane mutation, no file written      : holds
N6 ready's codes sit outside both composed spaces  : holds
      consumer declared code space, read from its docstring: 0, 1, 2, 3
      producer declared code space, read from its docstring: 0, 1, 2, 3

NEGATIVE CRITERIA HOLD: N1, N2, N3, N4, N5, N6
(exit 0)
```

**V9b - the live unpinned run, retained as a true record of its own instant and OUTSIDE the deterministic subset**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g2/negative-criteria.py
changed-path source : git
base                : cbd065893b37f20713ae35b8d2673bf26fe4d2ad
[... shown 16 of 32 lines; full output: docs/evidence/gatebraid/P2-S5/g2\captures/G2-D9-negative.json]
transitive target   : bin/gatebraid-snapshot.py
consumer            : bin/gatebraid-frontier.py
frozen root         : docs/evidence/gatebraid/P2-S5

N1 every changed path inside the allowlist         : holds
N2 under bin/, only the ready pair is touched      : holds
N3 no frozen input is written                      : holds
N4 no runtime dependency, no HTTP client           : holds
N5 no control-plane mutation, no file written      : holds
N6 ready's codes sit outside both composed spaces  : holds
      consumer declared code space, read from its docstring: 0, 1, 2, 3
      producer declared code space, read from its docstring: 0, 1, 2, 3

NEGATIVE CRITERIA HOLD: N1, N2, N3, N4, N5, N6
(exit 0)
```

**V10 D10 - the six negative criteria falsified: all six fire on their substantive limbs**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g2/negative-criteria.py --changed-from docs/evidence/gatebraid/P2-S5/g1/SEED-negative-criteria.txt --code-surface-dir docs/evidence/gatebraid/P2-S5/g1/falsification --frozen-root docs/evidence/gatebraid/P2-S5/g1/falsification/frozen-root
changed-path source : docs/evidence/gatebraid/P2-S5/g1/SEED-negative-criteria.txt
base                : cbd065893b37f20713ae35b8d2673bf26fe4d2ad
changed paths       : 9
   bin/gatebraid-ready.py
   bin/gatebraid-ready-selftest.py
   bin/gatebraid-frontier.py
[... shown 24 of 49 lines; full output: docs/evidence/gatebraid/P2-S5/g2\captures/G2-D10-negative-falsify.json]
      retained-set path-list digest: 78b1033539b2e9fb60128927641f8908f9a67b3ff6183e657fba591bc7df853b (expected 83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f)
      docs/evidence/gatebraid/P2-S5/g1/falsification/frozen-root/gate0.md: 9f3760fc458fe6e87b6187bbe787fb5d01e7aeb42281fd5a5bbe699b178de8df (expected be7c338896b1015923671988166d55af3bd59e028660ce89dfd3b69bc7251513)
      docs/evidence/gatebraid/P2-S5/g1/falsification/frozen-root/g0r/gate0.md: fa5bc3f79e5a59986bd97585d41dc34e27b45c1770c2ee20c593934288dd35fc (expected 95ff39111b4a8b8aa43c022e877c98af5f868b054f4ac2c116ae5c67327bc4e6)
N4 no runtime dependency, no HTTP client           : FIRED
      docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready.py: requests (network client module)
      docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready-selftest.py: urllib.request (network client module)
N5 no control-plane mutation, no file written      : FIRED
      docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready.py:23 [file-local] graphql document opens a mutation
      docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready.py:28 [file-local] open() not provably read-only (mode 'w')
      docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-snapshot.py:22 [transitive] graphql document opens a mutation
N6 ready's codes sit outside both composed spaces  : FIRED
      consumer declared code space, read from its docstring: 0, 1, 2, 3
      producer declared code space, read from its docstring: 0, 1, 2, 3
      [collision] docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready.py: exit 0 is inside a composed tool's declared space
      [collision] docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready.py: exit 2 is inside a composed tool's declared space
      [missing] docs/evidence/gatebraid/P2-S5/g1/falsification\gatebraid-ready.py: the frozen scope's exit 11 is not declared

NEGATIVE CRITERIA FIRED: N1, N2, N3, N4, N5, N6
(exit 1)
```

**V11 D11 - the evidence toolchain on the WSL half, both tools**
```
$ wsl.exe -e bash -lc 'cd '\''/mnt/d/Github repo/Gatebraid'\'' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-capture.py --out docs/evidence/gatebraid/P2-S5/g2/captures/G2-wsl-ready-selftest.json --capture-id G2-wsl-ready-selftest -- python3 -B bin/gatebraid-ready-selftest.py && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S5/g2/gate2.md --report-id cov-P2-S5-g2-gate2-wsl.md'
WROTE docs/evidence/gatebraid/P2-S5/g2/captures/G2-wsl-ready-selftest.json
  bytes=11878 sha256=ee68978550743dea5f093c8236588d5b2964fe302feb2a86a05afd5c99e85694 crlf=0 lone_cr=0
target        : docs/evidence/gatebraid/P2-S5/g2/gate2.md
interface     : gatebraid/gate-run@2
loader        : CPython 3.12.3 (/usr/bin/python3), jsonschema 4.10.3, Draft202012Validator
structural    : 0 error locus/loci
properties    : 7 rows
   structural       1
   semantic         6
   replayed         0
   capture-trusted  0
findings      : 0
verdict       : accepted
(exit 0)
```

**V12 - the closed-set sweep over this gate's captures: repository limb CLOSED, one residue disclosed**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g2/checks-g2-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g2/captures
captures swept : 31

=== candidate classification (every rule applied explicitly) ===
  E1 permitted repository                                    19
  E3 API-path fragment                                       2
  E5 filesystem or URL path segment                          264
  E6 schema-id namespace                                     3
  E7 JSON pointer                                            54
  E8 prose slash between ordinary words (named, not matched) 36
  I0 friction citation, not an issue reference               1
  N1 the permitted Project                                   5
  N2 the P2-S5 item                                          11
  N3 field id of the permitted Project                       31
  N4 another item of the permitted Project                   15
  UNEXPLAINED                                                13

[... shown 22 of 39 lines; full output: docs/evidence/gatebraid/P2-S5/g2\captures/G2-closed-set-sweep.json]
    G2-E1-approval-fidelity.json                 invocation   repo
    G2-E1-approval-fidelity.json                 invocation   repo
    G2-E1-approval-fidelity.json                 invocation   repo
    G2-E3-baseline.json                          stdout       repo
    G2-E3-baseline.json                          invocation   repo
    G2-E4-branch.json                            stdout       repo
(exit 1)
```

**V12a - falsification 1: the two retained seeds still fire the repository, node and issue limbs**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g2/checks-g2-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g1/falsification
captures swept : 2

=== candidate classification (every rule applied explicitly) ===
  N2 the P2-S5 item                                          1
  N4 another item of the permitted Project                   1
  UNEXPLAINED                                                1

=== every REPOSITORY identity named anywhere ===

=== mention-class check: a mention must never appear in an INVOCATION ===
  mention-class issues targeted by a query: 0 (0 required)

domain      : 2 documents (0 of this sweep's own reports excluded)
UNEXPLAINED RESIDUE: 5
    SEED-out-of-namespace-item.json              stdout       node
    SEED-out-of-namespace-item.json              stdout       node
    SEED-out-of-set.json                         stdout       repo
    SEED-out-of-set.json                         stdout       node
    SEED-out-of-set.json                         stdout       issue
(exit 1)
```

**V12b - falsification 2: a near-miss for every fact the copy adds; all fifteen remain residue**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g2/checks-g2-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g2/falsification
captures swept : 1

=== candidate classification (every rule applied explicitly) ===
  UNEXPLAINED                                                15

=== every REPOSITORY identity named anywhere ===

=== mention-class check: a mention must never appear in an INVOCATION ===
[... shown 26 of 27 lines; full output: docs/evidence/gatebraid/P2-S5/g2\captures/G2-closed-set-sweep-falsify-near-miss.json]

domain      : 1 documents (0 of this sweep's own reports excluded)
UNEXPLAINED RESIDUE: 15
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
    SEED-near-miss-new-classes.json              document     repo
(exit 1)
```

**V13 - handoff fingerprint: the tree and the changed-path set at the implementation-complete commit**
```
$ git rev-parse 629e287faab01a84935a93a2dc265d369a6a5c33^{tree}
cda51687a326d41c2b98d6b2ae49a48526bd366e
$ git diff --name-only cbd065893b37f20713ae35b8d2673bf26fe4d2ad..629e287faab01a84935a93a2dc265d369a6a5c33 | sort | wc -l
160
$ git diff --name-only cbd065893b37f20713ae35b8d2673bf26fe4d2ad..629e287faab01a84935a93a2dc265d369a6a5c33 | sort | grep -c '^docs/evidence/gatebraid/P2-S5/'
158
$ git diff --name-only cbd065893b37f20713ae35b8d2673bf26fe4d2ad..629e287faab01a84935a93a2dc265d369a6a5c33 | sort | grep '^bin/'
bin/gatebraid-ready-selftest.py
bin/gatebraid-ready.py
```

## Review record

No review has run. R1 through R5 are the independent reviewer's to write, last, in a session that did not build this tree; this record carries no verdict written by its implementer.

## Repair record

### Repair 1

- Hypothesis (new): N3's content limb fired on a retained record that did not change; the Gate 1 mechanisation hard-codes the two per-gate subdirectories that existed when it was written, and the frozen plan says `this gate's own subdirectories`, which at Gate 2 is three.

**Novelty measured - the tree moved, so the attempt is a repair and not a consumed one (ADR-0027 section 1)**
```
$ 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'echo "tree at the previous failed state (629e287f): $(git rev-parse 629e287faab01a84935a93a2dc265d369a6a5c33^{tree})"; echo "tree after the repair          (c07d0cb2): $(git rev-parse c07d0cb2bd6926352c9e1abc90c7d67129b00ad6^{tree})"; echo "unchanged tree                          : $([ "$(git rev-parse 629e287faab01a84935a93a2dc265d369a6a5c33^{tree})" = "$(git rev-parse c07d0cb2bd6926352c9e1abc90c7d67129b00ad6^{tree})" ] && echo yes || echo no)"; echo; echo "changed by this repair:"; git diff --name-only 629e287faab01a84935a93a2dc265d369a6a5c33..c07d0cb2bd6926352c9e1abc90c7d67129b00ad6 | grep -E "negative-criteria|closed-set-sweep" | sed "s/^/   /"'
tree at the previous failed state (629e287f): cda51687a326d41c2b98d6b2ae49a48526bd366e
tree after the repair          (c07d0cb2): b1c146183605d927aa24fb291faac5e969c919d2
unchanged tree                          : no

changed by this repair:
   docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep-falsify-near-miss.json
   docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep-falsify-retained.json
   docs/evidence/gatebraid/P2-S5/g2/checks-g2-closed-set-sweep.py
   docs/evidence/gatebraid/P2-S5/g2/negative-criteria.py
(exit 0)
```

**The failing run, retained**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/negative-criteria.py
changed-path source : git
base                : cbd065893b37f20713ae35b8d2673bf26fe4d2ad
changed paths       : 179
   bin/gatebraid-ready-selftest.py
[... shown 14 of 34 lines; full output: docs/evidence/gatebraid/P2-S5/g2\captures/G2-R-n3-g1-instrument-fired.json]
N3 no frozen input is written                      : FIRED
      retained file count: 62 (expected 43)
      retained-set path-list digest: 4eef9df5e18137b9f427b6efcd4494c7ff1b9a47cbbbe0c39b8f067427f01d56 (expected 83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f)
N4 no runtime dependency, no HTTP client           : holds
N5 no control-plane mutation, no file written      : holds
N6 ready's codes sit outside both composed spaces  : holds
      consumer declared code space, read from its docstring: 0, 1, 2, 3
      producer declared code space, read from its docstring: 0, 1, 2, 3

NEGATIVE CRITERIA FIRED: N3
(exit 1)
```

- Result: `green`
- Consult: `none` - the sequence stopped at repair 1 because the check returned green; no consult was reached and none was run.

## Required disclosures

- Deviations: the handoff fingerprint is measured at the last IMPLEMENTATION commit, 629e287faab01a84935a93a2dc265d369a6a5c33, before this record and the rest of this gate's evidence are committed. That is what the fingerprint's definition requires and what makes it Gate 3's comparand. Every commit after it is record-only and confined to docs/evidence/gatebraid/P2-S5/g2/, which is inside the frozen allowlist.
- Deviations: REPAIR 1, and what it did and did not touch. The FIRST run of the declared D9 command at this gate returned exit 1: negative criterion N3's content limb fired, reporting 62 files where 43 were expected. The cause was not a changed retained record - both pinned gate0.md hashes were unchanged throughout and the digest re-derives - but the Gate 1 MECHANISATION of the limb, whose exclusion set is hard-coded to `g0r` and `g1`, the two per-gate subdirectories that existed when it was written. The frozen plan states the property as `the file count of docs/evidence/gatebraid/P2-S5/ with the re-run and THIS GATE'S OWN SUBDIRECTORIES excluded must be forty-three`; at Gate 2 that is three names, not two. The Gate 1 file was NOT edited - Gate 1's captures pin it and it rides on byte-identical - and the failing run is retained at docs/evidence/gatebraid/P2-S5/g2/captures/G2-R-n3-g1-instrument-fired.json. The repair is a g2 copy differing in exactly one line. It LOOSENS NOTHING: the expected count is still 43, the expected digest still 83b3a273a9bd7da4e9e11469539a5eee0f28b53f5b924c0e6134acd8ba49a70f, both pinned gate0.md hashes unchanged, and the exclusion set is an explicit tuple of names rather than a pattern. It was falsified against the Gate 1 seeds before it was trusted, and all six criteria fired.
- Deviations: whether repair 1 counts toward the Slice's `evidence-only repairs = 0` acceptance item is stated rather than assumed, because the classification is arguable and the record should let a reader decide. Its subject is neither the deliverable nor this record's prose - the two things the M2 measurement chain's evidence-only repairs were - but a CHECK INSTRUMENT'S DOMAIN CONSTANT. This writer's reading is that it is not an evidence-only repair under that definition. The reviewer and the operator may read it otherwise; everything needed to reclassify it is in the Repair record and in the retained failing run.
- Deviations: the D9 row is recorded TWICE and the reason is the defect P2-S6's own repair 1 found. The instrument's changed-path set is the tracked diff UNION the untracked set. Run unpinned it reads the working tree, so it moves after every later commit and does not reproduce. V9 is therefore the run PINNED to base..fingerprint, which is the row that reproduces; V9b is the live unpinned run, retained beside it as a true record of its own instant. The untracked half is working-tree-relative even when pinned and can only SHRINK as this Slice's own files are committed; every path it can contain is inside the allowlist by construction, so the six verdicts are stable under that shrinkage even though the listing is not.
- Deviations: THE NOMINATED DETERMINISTIC SUBSET of this record. IN the subset, and required to reproduce byte-identically: E1's three rows, E3, E4b, V0, V0F, V1, V2, V3, V4, V6, V7, V8, V9 (pinned), V10, and the repair's novelty row. OUTSIDE the subset, by ADR-0028 decision 2's exclusion limb, and named here rather than left to be discovered: V5, the live composition, whose report is re-derived from the control plane at each run and whose `workflow` value for this Slice changes as this very gate writes fields; V9b, the unpinned criteria run, for the reason above; V12 and its two falsification runs, whose domain is the captures directory AS IT STOOD when they ran and which grows as this gate writes the captures that follow them; E2 and E4, whose recorded values include a lease timestamp and a branch head that later commits move; and V11's second half, which validates this record and therefore reads bytes that this render produced.
- Deviations: two of this gate's declared commands name paths that a read-only gate could not have created, and both now run against artefacts that exist. D5 writes its capture into docs/evidence/gatebraid/P2-S5/g2/captures/, the directory the frozen plan names. D11's second half validates docs/evidence/gatebraid/P2-S5/g2/gate2.md, so it runs AFTER this record is authored and its outcome enters the record as the record's own last row - which is why that row is outside the deterministic subset.
- Deviations: the closed-set sweep's g2 copy carries domain facts under ruling 2 of the Plan Approval, and ONE RESIDUE IS LEFT DELIBERATELY UNEXPLAINED. The hard-rule limb is satisfied and shown: exactly two repository identities anywhere in the domain, MianliWang/gatebraid and MianliWang/gatebraid-scratch, both PERMITTED, nothing outside the set, and no mention-class issue targeted by any query. The remaining token is an issue-shaped citation printed by the FROZEN corpus runner inside a case label, which is a friction reference written without the word `friction` that the FRICTION regex requires. No existing explicit set fits it honestly: the mention class means `issues of the permitted repository this Slice's evidence names`, which it is not, and putting it there would assert something false and weaken a live check. Admitting it would need a new classification branch, which is a rule change the approval forbids. It stays residue and is disclosed here. THE SWEEP OVER THIS RECORD ITSELF returns UNEXPLAINED RESIDUE 0 at exit 0: every candidate token in these bytes is explained by an explicit rule, and the four residues an earlier render carried were removed AT SOURCE rather than by widening anything - a bare relative path in a row's own echo label written out in full, a host temporary path moved inside this gate's evidence directory, and three near-miss tokens this record had been quoting into itself, which is the IN-03 class and was the record sweep catching a defect in its own file.
- Deviations: the sweep copy was falsified in TWO runs before any weight was put on it, which is the approval's stated condition. The two retained seeds still fire the repository, node and issue limbs, so the added facts blunted no limb that already worked. A new seed carries, for every fact the copy adds, a token shaped like it but OUTSIDE it by one appended or substituted character, and all fifteen of those tokens remained residue. The seed is retained at docs/evidence/gatebraid/P2-S5/g2/falsification/SEED-near-miss-new-classes.json and the tokens are NOT echoed here: a checker does not quote what it forbids into a record (ADR-0028 decision 3, the IN-03 class), and this disclosure quoting three of them is a defect the record sweep caught in this very file. A fact that admitted its own near-miss would be a blindfold rather than a domain fact.
- Deviations: the composer's argument-splitting rule was settled by MEASUREMENT during authoring, and it is recorded because it is the exact failure this scope was first frozen around. The producer command must be split by POSIX rules on every platform. With posix=False - the tempting choice on Windows - shlex leaves the quotes attached to the token, the stub arrives at the child as a program whose first character is a quote, the child emits ZERO BYTES, and the decode guard appears to pass while testing nothing. That is friction #15's shape and precisely what P1-S3's second dry-run caught before this scope was frozen. It was caught here the same way, by running rather than reading. The default producer command is written with forward slashes because POSIX rules treat a backslash as an escape.
- Deviations: THIS RECORD'S FIRST RENDER WAS REJECTED BY ITS OWN MACHINE VALIDATION, and the correction is recorded rather than quietly folded in. The metadata's `approvals[0].type` was written with an ASCII arrow, `Plan Approval (G1->G2)`, and the frozen schema's enum requires the label carrying U+2192 RIGHTWARDS ARROW. D11's validation half returned `verdict: rejected` with one structural finding at `approvals/0/type`, and that failing run is retained at docs/evidence/gatebraid/P2-S5/g2/captures/G2-D11-wsl-toolchain-pass1.json. The renderer now RESOLVES the label from the schema's own enum by prefix rather than writing it at all, which is the standing never-re-type rule applied to a record field instead of to a control-plane write. This is recorded as an AUTHORING correction and not as a repair attempt: it was caught by this writer's own pre-submission validation, before the record was committed and before any reviewer saw it, which is the discipline ADR-0028 mandates rather than a round trip it measures. A reviewer who reads it otherwise has the failing capture and this disclosure to reclassify from.
- Deviations: the selftest's S06c assertion was corrected during authoring, and the correction was to the ASSERTION and never to the composer. Its first writing matched the phrase `not valid UTF-8` in lower case against a refusal the composer writes in capitals, so a correct guard was reported failing. The row now matches case-insensitively and on three substantive tokens - the byte, its position, and the refusal phrase. The composer's message was not changed to suit a check.
- Deviations: two files under docs/evidence/gatebraid/P2-S5/g1/dryrun-out/ and two under docs/evidence/gatebraid/P2-S5/g2/dryrun-out/ carry CRLF in the working copy and are stored LF under the tree's `* text=auto eol=lf` attribute. They are unreferenced probe stderr, named by no capture and covered by no pin. The four pinned measurements are byte-identical either way, before and after the evidence commit.
- Deviations: this gate took the Writer Lease and held it throughout; no second writer of any kind ran. Nothing was pushed, no pull request was opened, no merge was performed, no dependency was installed, no hook or check was disabled, and no git reset, clean or checkout was run against baseline state. The one checkout performed was `git checkout slice/P2-S5` onto the branch this gate created from Y, which is the Entry step the contract names.
- Deviations: scratch paths outside every repository were relied on and are named here, as the Prohibited clause requires. Every commit message was passed through a file under the session scratchpad outside this repository, never as a shell argument. The approval-fidelity row writes and removes one file, and it writes it INSIDE this gate's own evidence directory rather than outside the repository: its first form used a host temporary path whose leading segment the closed-set sweep has no class for, and the record sweep caught that in this very file. The superseded capture is retained at docs/evidence/gatebraid/P2-S5/g2/captures/G2-E1-approval-fidelity-pass1.json.
- Deviations: the record's FINAL bytes are validated by a run cited by output_ref and not inlined as a row, because a document that quoted its own verification would change the bytes that verification read. V11's second half validated this record at its own instant on the WSL half and returned accepted; the Windows-half run against the final bytes is docs/evidence/gatebraid/P2-S5/g2/captures/G2-record-validation.json, and the sweep over those same final bytes is G2-record-sweep.json in the same directory. Both are captured, both are named in checks, and neither is inlined.
- Environment: Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; Git for Windows 2.51.0.windows.1 whose SYSTEM configuration carries core.autocrlf=true, verified in this window, and the same binary resolves for a Windows-Python subprocess; every gh call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL /usr/bin/python3 with CPython 3.12.3, jsonschema 4.10.3, whose captures stamp platform.os `wsl`. The `python` on PATH is the MSYS 3.14.3 build and carries neither, which is why no declared command names it and why delta D-3 exists. Captures are argv-form unless the row declares shell semantics, in which case the shell, pipefail and the exit-code source are all recorded. environment=mixed-see-prose.
- Reviewer write disclosure: `not applicable - no review has run`

## gatebraid-metadata

```yaml
schema: gatebraid/gate-run@2
slice_id: P2-S5
gate: 2
environment: mixed-see-prose
executor: Claude Lead
base_sha: cbd065893b37f20713ae35b8d2673bf26fe4d2ad
active_branch: slice/P2-S5
started_at: "2026-09-02T02:52:00Z"
ended_at: "2026-09-02T03:26:18Z"
result: needs_approval
checks:
  - name: plan-approval-verified
    command: "gh api repos/MianliWang/gatebraid/issues/comments/5503291709 by id; author observed MianliWang, compared against gh api user = mianliwang492-source; body byte-identical to the committed source"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E1-approval-fidelity.json"
  - name: door-consumed
    command: "Next Approval to the bare option 450ee130; needs-human removed"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E4-entry-readback.json"
  - name: writer-lease-taken
    command: "Writer Lease field write and read-back"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E2-lease.json"
  - name: baseline-reread
    command: "X read from docs/evidence/gatebraid/P2-S5/g0r/gate0.md; Y = git rev-parse main; git diff --name-only X..Y"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E3-baseline.json"
  - name: active-branch-created-from-Y
    command: "git rev-parse --abbrev-ref HEAD; git rev-parse HEAD"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E4-branch.json"
  - name: evidence-rides-on-byte-identical
    command: "retained-set digest, three pinned records, and the commit shown additions-only, measured AFTER the commit"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E4b-evidence-commit.json"
  - name: D0-frozen-scope-pin-holds
    command: "docs/evidence/gatebraid/P2-S5/g1/scope-pin.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D0-scope-pin.json"
  - name: D0F-frozen-scope-pin-falsified
    command: "the same instrument with --commit naming the pinned commit's parent"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D0F-scope-pin-falsify.json"
  - name: D1-corpus-digest-unmoved
    command: "fixtures/runner-selftest.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D1-corpus-digest.json"
  - name: D2-historical-ready-failure-classes-killed
    command: "fixtures/run-corpus.py; BP-01, BP-02, BP-03, IN-02, IN-03, IN-04 and IN-05 each killed on a named locus. IN-01 is absent from the corpus by its own known_limitation and is carried by D3 instead"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D2-corpus.json"
  - name: D3-ready-selftest-windows
    command: "bin/gatebraid-ready-selftest.py"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D3-selftest-windows.json"
  - name: D4-ready-selftest-wsl
    command: "wsl.exe -e bash -lc \"cd '/mnt/d/Github repo/Gatebraid' && PYTHONDONTWRITEBYTECODE=1 python3 -B bin/gatebraid-ready-selftest.py\""
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D4-selftest-wsl.json"
  - name: D5-live-end-to-end
    command: "bin/gatebraid-ready.py against the real control plane; four sources ok and complete, a verdict for the Slice issue"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D5-live-ready.json"
  - name: D6-producer-reported-no-document
    command: "bin/gatebraid-ready.py --snapshot-command (producer on an absent transcript); expect exit 10"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D6-producer-failure.json"
  - name: D7-decode-guard
    command: "bin/gatebraid-ready.py --snapshot-command (cp936 stub); expect exit 11 and empty stdout"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D7-decode-guard.json"
  - name: D8-consumer-refusal-passed-through
    command: "bin/gatebraid-ready.py --snapshot-command (empty-object stub); expect the consumer's own exit 1"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D8-consumer-refusal.json"
  - name: D9-negative-criteria-hold
    command: "g2/negative-criteria.py --base cbd06589..629e287f (pinned so the diff half reproduces)"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D9-negative-pinned.json"
  - name: D10-negative-criteria-falsified
    command: "g2/negative-criteria.py against the Gate 1 seeds; all six must fire"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D10-negative-falsify.json"
  - name: D11-evidence-toolchain-on-wsl
    command: "bin/gatebraid-capture.py and bin/gatebraid-validate.py, both run on the WSL half"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D11-wsl-toolchain.json"
  - name: closed-set-repository-limb-closed
    command: "g2/checks-g2-closed-set-sweep.py over the captures domain; exactly two repository identities, both permitted, no mention-class issue targeted by a query"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep.json"
  - name: closed-set-sweep-falsified-two-ways
    command: "the two retained seeds, and a new seed carrying a near-miss for every fact the copy adds"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep-falsify-near-miss.json"
  - name: closed-set-sweep-explains-every-candidate
    command: "the same run; one residue remains, an issue-shaped friction citation inside a frozen corpus case label, disclosed and not admitted by a rule change"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep.json"
  - name: gate2-record-machine-validated
    command: "bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S5/g2/gate2.md --report-id cov-P2-S5-g2-gate2.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-record-validation.json"
  - name: review-five-items
    command: "R1 through R5, by an independent read-only reviewer in a separate session"
    result: not_run
    output_ref: "#review-record"
handoff_fingerprint:
  active_branch_head: "629e287faab01a84935a93a2dc265d369a6a5c33"
  tree_sha: "cda51687a326d41c2b98d6b2ae49a48526bd366e"
  changed_paths:
    - "bin/gatebraid-ready-selftest.py"
    - "bin/gatebraid-ready.py"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-baseline-main.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation-pass2.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-captures-validation.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-falsify-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-falsify.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-closed-set-sweep.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-env-field.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-frontier-run.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-head.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-host-probe.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-porcelain-baseline.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-porcelain-full.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-record-sweep.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-record-validation-pass2.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-record-validation-rejected-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-record-validation.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-ref-namespace.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-remote.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-render-record-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-render-record-pass2.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-render-record.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-slice-body.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-slice-metadata-loader.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-slice-metadata-selftest.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-slice-metadata-validation.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-snapshot-run.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-tools-claude.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-tools-codex.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-tools-gh.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-tools-git.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-tools-python-windows.json"
    - "docs/evidence/gatebraid/P2-S5/captures/G0-tools-python-wsl.json"
    - "docs/evidence/gatebraid/P2-S5/captures/g0-frontier-report.json"
    - "docs/evidence/gatebraid/P2-S5/captures/g0-snapshot.json"
    - "docs/evidence/gatebraid/P2-S5/captures/slice-body-17.md"
    - "docs/evidence/gatebraid/P2-S5/checks-g0-closed-set-sweep.py"
    - "docs/evidence/gatebraid/P2-S5/checks-g0-slice-metadata.py"
    - "docs/evidence/gatebraid/P2-S5/checks-g0-verify-captures.py"
    - "docs/evidence/gatebraid/P2-S5/falsification/SEED-out-of-set.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-baseline-main.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-captures-validation.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-closed-set-sweep-falsify-n4.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-closed-set-sweep-falsify.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-closed-set-sweep-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-closed-set-sweep.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-env-field.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-frontier-run.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-head.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-host-probe.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-p2s5-pathlist-digest.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-porcelain-baseline.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-porcelain-full.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-porcelain-tracked.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-record-sweep-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-record-sweep.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-record-validation.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-ref-namespace.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-remote.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-render-record.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-slice-body.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-slice-metadata-selftest.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-slice-metadata-validation.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-snapshot-run.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-tools-claude.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-tools-codex.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-tools-gh.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-tools-git.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-tools-python-windows.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/G0R-tools-python-wsl.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/g0r-frontier-report.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/g0r-snapshot.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/captures/slice-body-17.md"
    - "docs/evidence/gatebraid/P2-S5/g0r/checks-g0r-closed-set-sweep.py"
    - "docs/evidence/gatebraid/P2-S5/g0r/checks-g0r-slice-metadata.py"
    - "docs/evidence/gatebraid/P2-S5/g0r/checks-g0r-verify-captures.py"
    - "docs/evidence/gatebraid/P2-S5/g0r/falsification/SEED-out-of-namespace-item.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/falsification/SEED-out-of-set.json"
    - "docs/evidence/gatebraid/P2-S5/g0r/gate0.md"
    - "docs/evidence/gatebraid/P2-S5/g0r/render-gate0.py"
    - "docs/evidence/gatebraid/P2-S5/g1/SEED-negative-criteria.txt"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-allowlist-hash.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-closed-set-sweep-falsify.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-closed-set-sweep.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D0-scope-pin.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D0F-scope-pin-falsify.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D1-corpus-digest.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D10-negative-falsify.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D11-wsl-toolchain.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D2-corpus.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D3-selftest-windows.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D4-selftest-wsl.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D5-live-ready.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D6-producer-failure.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D7-decode-guard.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D8-consumer-refusal.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-dryrun-D9-negative.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-entry-fields-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-entry-fields.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-entry-frontier.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-entry-snapshot.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-exit-field-options.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-exit-handoff-comment.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-exit-label-needs-human.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-exit-readback.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-exit-verify-labels-comment.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-exit-write-checkpoint.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-exit-write-gate.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-exit-write-next-approval.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-exit-write-workflow.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-plan-hash-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-plan-hash.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-plan-path-scan-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-plan-path-scan.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-probe-D11-wsl-capture.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-probe-D11-wsl-validate.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-probe-D6-no-document.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-probe-D6-producer-failure.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-probe-D7-stub.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-probe-D8-consumer-refusal.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-probe-boundary.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-record-sweep-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-record-sweep.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-record-validation-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-record-validation.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/G1-writedomains-check.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/g1-frontier-report.json"
    - "docs/evidence/gatebraid/P2-S5/g1/captures/g1-snapshot.json"
    - "docs/evidence/gatebraid/P2-S5/g1/checks-g1-closed-set-sweep.py"
    - "docs/evidence/gatebraid/P2-S5/g1/dryrun-out/G2-wsl-ready-selftest.json"
    - "docs/evidence/gatebraid/P2-S5/g1/dryrun-out/WSL-inner-probe.json"
    - "docs/evidence/gatebraid/P2-S5/g1/dryrun-out/enc-probe.txt"
    - "docs/evidence/gatebraid/P2-S5/g1/dryrun-out/probe-empty.err"
    - "docs/evidence/gatebraid/P2-S5/g1/dryrun-out/probe-empty.json"
    - "docs/evidence/gatebraid/P2-S5/g1/dryrun-out/probe.err"
    - "docs/evidence/gatebraid/P2-S5/g1/dryrun-out/wsl-frontier-report.json"
    - "docs/evidence/gatebraid/P2-S5/g1/falsification/SEED-out-of-namespace-item.json"
    - "docs/evidence/gatebraid/P2-S5/g1/falsification/SEED-out-of-set.json"
    - "docs/evidence/gatebraid/P2-S5/g1/falsification/frozen-root/g0r/gate0.md"
    - "docs/evidence/gatebraid/P2-S5/g1/falsification/frozen-root/gate0.md"
    - "docs/evidence/gatebraid/P2-S5/g1/falsification/gatebraid-frontier.py"
    - "docs/evidence/gatebraid/P2-S5/g1/falsification/gatebraid-ready-selftest.py"
    - "docs/evidence/gatebraid/P2-S5/g1/falsification/gatebraid-ready.py"
    - "docs/evidence/gatebraid/P2-S5/g1/falsification/gatebraid-snapshot.py"
    - "docs/evidence/gatebraid/P2-S5/g1/gate1-exit-checklist.md"
    - "docs/evidence/gatebraid/P2-S5/g1/gate1.md"
    - "docs/evidence/gatebraid/P2-S5/g1/hash-allowlist.py"
    - "docs/evidence/gatebraid/P2-S5/g1/hash-plan.py"
    - "docs/evidence/gatebraid/P2-S5/g1/negative-criteria.py"
    - "docs/evidence/gatebraid/P2-S5/g1/plan-path-scan.py"
    - "docs/evidence/gatebraid/P2-S5/g1/plan.md"
    - "docs/evidence/gatebraid/P2-S5/g1/probe-producer-boundary.py"
    - "docs/evidence/gatebraid/P2-S5/g1/render-gate1.py"
    - "docs/evidence/gatebraid/P2-S5/g1/scope-pin.py"
    - "docs/evidence/gatebraid/P2-S5/g1/writedomains-check.py"
    - "docs/evidence/gatebraid/P2-S5/gate0.md"
    - "docs/evidence/gatebraid/P2-S5/render-gate0.py"
consults: []
repair_attempts:
  - number: 1
    hypothesis: "N3's content limb fired on a retained record that did not change; the Gate 1 mechanisation hard-codes the two per-gate subdirectories that existed when it was written, and the frozen plan says `this gate's own subdirectories`, which at Gate 2 is three"
    result: green
approvals:
  - type: "Plan Approval (G1→G2)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5503291709"
    author: "MianliWang"
plan_hash: "b2cd75f6a49bb056fd16bc3d2f4cfd5cf98ae8515b5761908add2ed5405cc424"
allowlist_hash: "4110b3021bdfc2fcda1f5f90528db01eb87b554177e2176ccfba46ccd6ca3750"
evidence_files:
  - docs/evidence/gatebraid/P2-S5/g2/gate2.md
notes: "The fourth gatebraid-ready attempt on the M2 slice-C frozen scope, built on the M3 stack. The deliverable is the ready pair alone; it composes the landed producer and consumer and modifies neither. The four ratified deltas are implemented as the approval states them, and D-4 - the producer's status is interpreted against its own declared space rather than tested against zero - is the one that keeps a degraded-but-emitted document from being discarded. Twenty selftest conditions each emit their own summary row; S09 carries IN-01, the class the frozen corpus does not hold, and S10 parses the producer's docstring so the D-4 partition cannot drift from its source unnoticed. One repair was taken and it changed a check instrument's domain constant, not the deliverable and not this record's prose. One check is typed fail and is disclosed in full: the sweep's explanation limb leaves a single residue that no existing explicit set fits honestly. The review is NOT this session's: R1 through R5 belong to an independent reviewer dispatched after adjudication, and Gate = G2 passed is not set here."
```
