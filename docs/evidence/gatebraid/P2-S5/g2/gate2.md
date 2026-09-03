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
[... shown 14 of 20 lines; full output: docs/evidence/gatebraid/P2-S5/g2/captures/G2-D0F-scope-pin-falsify.json]
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
[... shown 16 of 37 lines; full output: docs/evidence/gatebraid/P2-S5/g2/captures/G2-D1-corpus-digest.json]
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
[... shown 26 of 156 lines; full output: docs/evidence/gatebraid/P2-S5/g2/captures/G2-D2-corpus.json]
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
[... shown 14 of 29 lines; full output: docs/evidence/gatebraid/P2-S5/g2/captures/G2-D4-selftest-wsl.json]
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
[... shown 20 of 195 lines; full output: docs/evidence/gatebraid/P2-S5/g2/captures/G2-D5-live-ready.json]
transport                     : live
sources                       : 4
   project_items    ok                   complete=True  exit=0
   issue_states     ok                   complete=True  exit=0
   dep_blocked_by   ok                   complete=True  exit=0
   dep_blocking     ok                   complete=True  exit=0
items                         : 16
degraded                      : no
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

**V9 D9 - the six negative criteria hold. Pinned to base..fingerprint, which pins the TRACKED half only; this row is EXCLUDED from the deterministic subset and what it asserts is the six verdicts**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g2/negative-criteria.py --base cbd065893b37f20713ae35b8d2673bf26fe4d2ad..5b586029344eb6df4a964c34baa1eb12e2916f6d
changed-path source : git
base                : cbd065893b37f20713ae35b8d2673bf26fe4d2ad..5b586029344eb6df4a964c34baa1eb12e2916f6d
changed paths       : 245
   bin/gatebraid-ready-selftest.py
   bin/gatebraid-ready.py
   docs/evidence/gatebraid/P2-S5/captures/G0-baseline-main.json
[... shown 22 of 32 lines; full output: docs/evidence/gatebraid/P2-S5/g2/captures/G2-D9-negative-pinned.json]
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

**V9b - the live unpinned run, retained beside it as a true record of its own instant, likewise excluded**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g2/negative-criteria.py
changed-path source : git
base                : cbd065893b37f20713ae35b8d2673bf26fe4d2ad
[... shown 16 of 32 lines; full output: docs/evidence/gatebraid/P2-S5/g2/captures/G2-D9-negative.json]
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
[... shown 24 of 49 lines; full output: docs/evidence/gatebraid/P2-S5/g2/captures/G2-D10-negative-falsify.json]
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
  bytes=11878 sha256=7a816de071e54e12eafc7144ad6e23625f4ec8e3d29db2d3d831c45407786cf5 crlf=0 lone_cr=0
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

**V12 - the closed-set sweep over this gate's captures: repository limb CLOSED, 15 residue occurrences, diagnosed by class in the disclosures**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g2/checks-g2-closed-set-sweep.py docs/evidence/gatebraid/P2-S5/g2/captures
captures swept : 65

=== candidate classification (every rule applied explicitly) ===
  E1 permitted repository                                    41
  E3 API-path fragment                                       3
  E4 git ref namespace, not a repository                     4
  E5 filesystem or URL path segment                          539
  E6 schema-id namespace                                     12
  E7 JSON pointer                                            107
  E8 prose slash between ordinary words (named, not matched) 80
  I0 friction citation, not an issue reference               6
  N1 the permitted Project                                   8
  N2 the P2-S5 item                                          17
  N3 field id of the permitted Project                       40
  N4 another item of the permitted Project                   30
  UNEXPLAINED                                                13
[... shown 22 of 41 lines; full output: docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep.json]
    G2-E1-approval-fidelity-pass1.json           invocation   repo
    G2-E1-approval-fidelity-pass1.json           invocation   repo
    G2-E3-baseline-pass1.json                    stdout       repo
    G2-E3-baseline-pass1.json                    invocation   repo
    G2-X-checkpoint.json                         invocation   repo
    G2-X-exit-readback.json                      stdout       repo
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
[... shown 26 of 27 lines; full output: docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep-falsify-near-miss.json]

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
$ git rev-parse 5b586029344eb6df4a964c34baa1eb12e2916f6d^{tree}
f696944947a342b6163bf4ad7d9137674830a2f7
$ git diff --name-only cbd065893b37f20713ae35b8d2673bf26fe4d2ad..5b586029344eb6df4a964c34baa1eb12e2916f6d | sort | wc -l
219
$ git diff --name-only cbd065893b37f20713ae35b8d2673bf26fe4d2ad..5b586029344eb6df4a964c34baa1eb12e2916f6d | sort | grep -c '^docs/evidence/gatebraid/P2-S5/'
217
$ git diff --name-only cbd065893b37f20713ae35b8d2673bf26fe4d2ad..5b586029344eb6df4a964c34baa1eb12e2916f6d | sort | grep '^bin/'
bin/gatebraid-ready-selftest.py
bin/gatebraid-ready.py
```

## Review record

### Review 1

Independent read-only reviewer, `Executor = Claude Read-Only Team`, at head `8fde380b26e44caba7754dacd0611f3d5ff026a8`. Report `REVIEW-P2S5-G2.md`, measured region bytes 1..46,375, sha256 `f9b932e36892a9254512d05a0a79adeba333c79478c11dbef0a91b5a609d3228`.

| Item | Verdict | Evidence |
|---|---|---|
| R1 allowlist confinement | **pass** | 160 paths base..fingerprint, 0 outside the frozen write_domains, all additions; porcelain 0; the four ride-on pins unmoved. |
| R2 test-plan coverage | **pass** | every Acceptance item mapped to a declared command item by item; the re-captured D-rows reproduce. |
| R3 evidence is rows that reproduce | **fail** | two grounds. F-02: V9 was nominated into the byte-reproducible subset but cannot reproduce, because the instrument unions the tracked diff with the untracked set. F-03: the V12 disclosure said ONE residue where its own cited capture measured more. |
| R4 negative criterion | **pass** | D9 exit 0 with all six holding; D10 exit 1 with all six firing. |
| R5 no prohibited action | **pass** | no push, no pull request, no dependency change, no disabled hook, one lease. |

Also raised, outside R3's letter: **F-01 (HIGH)** - the delivered tool declared `--consumer` and `--version` beyond the frozen scope, and `--version` put non-JSON on stdout at exit 0. **F-04, F-05, F-06 (LOW)** - an inflated elision total, elision paths that were not committed-path spellings, and deviation bullets without citations. **F-07** the reviewer declined to fail anything over; **F-08** typed this record's `fail` check as the operator's to rule.

- Reviewer write disclosure: `none`
- Rules given to the reviewer: the standing hard-rules block and spec section 4, verbatim in its mandate; its report states which it was given.

### Review 2 - bounded re-check after repair 2

The same independent reviewer, at head `622d79a9f2f21b7b2fabe850c8a3ba0bdd8a473b`. Report `REVIEW-P2S5-G2-RECHECK.md`, measured region bytes 1..28,369, sha256 `c11cd5e40024a48f96da33340cafdad16f7c903b5e68799cea10790e9703d152`.

| Item | Verdict | Evidence |
|---|---|---|
| R1 allowlist confinement | **pass** | 249 paths base..tip, 0 outside, all additions; porcelain 0; the four ride-on pins unmoved. |
| R2 test-plan coverage and F-01's resolution | **pass** | the surface is exactly the frozen two flags plus `--help`; the removed flags exit 12 with empty stdout; `--help` verified grounded as test-plan command 1 of all three M2 attempts. |
| R3 evidence is rows that reproduce | **fail** | three findings. **G-01** the metadata `notes` field contradicted `repair_attempts` and the V12 row. **G-02** the V12 row label understated its own table and capture. **G-03** the claim re-check instrument stated a universal over a domain that excluded metadata fields - the IN-05 class - which is why G-01 reached the tip. |
| R4 negative criteria at the new fingerprint | **pass** | D9 pinned to `base..5b586029` exit 0, six holding; D10 exit 1, six firing. |
| R5 no prohibited action | **pass** | 0 remote rows, 0 pull requests, 0 non-sample hooks, one lease, clean reflog. |

Verified remedied by that re-check: F-01 removed cleanly, and F-02, F-04, F-05 and F-06 each re-measured rather than read.

- Reviewer write disclosure: `none`
- Rules given to the reviewer: as above, verbatim in its mandate.

### Human Diagnosis disposition

`repair_limit = 2` was spent with R3 still red, so the gate routed to `Human Diagnosis Required` and the operator authored the disposition this record carries in `approvals[]`: comment `5518637712`, author `MianliWang`, verified byte-equal to its committed source under the single-trailing-newline tolerance. It directs **remediation under stated rules followed by ONE FULL re-review**, and states in terms that the terminal disposition is NOT directed. The remediation it names is G-01, G-02 and G-03 and nothing else; it is recorded in the Remediation record below and is not a repair attempt, so `repair_attempts` stays at two.

### Review 3 - full re-review of R1 through R5

The same independent reviewer, at head `541f6a25ba11638d845a67a0e6a9cbd670339750`, after the first Human Diagnosis remediation. Report `REVIEW-P2S5-G2-FULL.md`, measured region bytes 1..26,320, sha256 `68a0dbc0af3a04fceb53392718d7eb8e1dbb2674d4d94e64e1c3432a36aafd71`. Its verdict line reads `VERDICTS: R1=PASS R2=PASS R3=FAIL R4=PASS R5=PASS`, and its verdict table agrees with that line.

| Item | Verdict | Evidence |
|---|---|---|
| R1 allowlist confinement | **pass** | all three remediation commits confined to `g2/`; 0 paths outside it in `622d79a9..tip`; 257 paths base..tip, 0 outside `write_domains`, all additions; porcelain 0; four ride-on pins unmoved; `bin/` untouched. |
| R2 test-plan coverage | **pass** | mapping unchanged; F-01's resolution stands - the parser declares exactly `--strict` and `--snapshot-command`, the removed flags exit 12 with empty stdout, `--help` grounded as test-plan command 1 of all three M2 attempts. |
| R3 evidence is rows that reproduce | **fail** | **H-01**: the required `Reviewer write disclosure` stated that no review had run while the Review record in the same file recorded two completed reviews, each disclosing `none`. The line was byte-unchanged from before the first remediation; that remediation's directed Review-record fill is what made it false. |
| R4 negative criteria | **pass** | the instrument byte-unchanged; D9 pinned to `base..5b586029` exit 0, six holding over 219 paths; D10 exit 1, six firing. |
| R5 no prohibited action | **pass** | 0 remote rows; 0 pull requests; 0 non-sample hooks; one lease string; reflog clean across all eleven commits; `refs/codex` a single unchanged ref. |

Informational findings, none of which fails anything: **H-02** the `Remediation record` heading the template has no home for, queued with F-07 for the pending ADR-0026 clarification; **H-03** a sentence of the builder's remediation report that overreached in claiming a class closed while an instance of it survived, recorded for the closeout ledger and not a record claim; **H-04** the per-review disclosure `none` compressing a repository-scoped answer, ruled to stand; **H-05** a cross-check the reviewer initially misread and resolved in the record's favour.

- Reviewer write disclosure: `none`
- Rules given to the reviewer: as above, verbatim in its mandate.

### Second Human Diagnosis disposition

Under rule 7 of the first disposition, R3's FAIL returned the Slice to `Human Diagnosis Required` a second time. The operator authored the second disposition this record carries in `approvals[]`: comment `5520728930`, author `MianliWang`, verified byte-equal to its own committed source under the single-trailing-newline tolerance - a DIFFERENT source from the first disposition's, which matches only its own. It directs **remediation followed by ONE FULL re-review** and states in terms that the terminal disposition is NOT directed. The remediation it names is H-01 and nothing else, and it directs that the correction be made STRUCTURAL: the mirror is derived from the per-review entries rather than written as a literal. It is recorded in the Remediation record below and is not a repair attempt, so `repair_attempts` stays at two.

### Review 4 - the next full re-review

Not yet run. The second disposition directs ONE FULL re-review of R1 through R5. Its five verdicts are recorded here at the Exit, by the reviewer's values, last; this record carries no verdict written by its implementer.

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
[... shown 14 of 34 lines; full output: docs/evidence/gatebraid/P2-S5/g2/captures/G2-R-n3-g1-instrument-fired.json]
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

### Repair 2

- Hypothesis (new): the independent review's R3 FAIL and its HIGH finding share one cause - a claim the record or the tool makes that its own measurement contradicts - so the repair restores the frozen two-flag surface and re-derives every contradicted figure from the row that measures it, rather than restating it in prose.

**Novelty measured - the tree moved from the reviewed failing state, so the attempt is a repair and not a consumed one (ADR-0027 section 1)**
```
$ 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'echo "tree at the reviewed failing state 8fde380b: $(git rev-parse 8fde380b26e44caba7754dacd0611f3d5ff026a8^{tree})"; echo "tree after repair 2 implementation  : $(git rev-parse 5b586029344eb6df4a964c34baa1eb12e2916f6d^{tree})"; echo "unchanged tree                      : $([ "$(git rev-parse 8fde380b26e44caba7754dacd0611f3d5ff026a8^{tree})" = "$(git rev-parse 5b586029344eb6df4a964c34baa1eb12e2916f6d^{tree})" ] && echo yes || echo no)"; echo; echo "changed by the repair-2 implementation commit:"; git diff --name-status 8fde380b26e44caba7754dacd0611f3d5ff026a8..5b586029344eb6df4a964c34baa1eb12e2916f6d | sed "s/^/   /"'
tree at the reviewed failing state 8fde380b: 74de097bb05023cb955cc59fa1c7338e4524f229
tree after repair 2 implementation  : f696944947a342b6163bf4ad7d9137674830a2f7
unchanged tree                      : no

changed by the repair-2 implementation commit:
   M	bin/gatebraid-ready.py
(exit 0)
```

**The frozen tool surface, restored and verified (F-01)**
```
$ 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'echo "declared option surface:"; PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready.py --help | sed -n "1,2p" | sed "s/^/   /"; echo; echo "add_argument declarations in the source:"; grep -o -- "\"--[a-z-]*\"" bin/gatebraid-ready.py | sort -u | sed "s/^/   /"; echo; for f in --version --consumer; do PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B bin/gatebraid-ready.py $f > docs/evidence/gatebraid/P2-S5/g2/dryrun-out/rm.out 2>/dev/null; st=$?; echo "$f -> exit $st, stdout $(wc -c < docs/evidence/gatebraid/P2-S5/g2/dryrun-out/rm.out) bytes"; done; rm -f docs/evidence/gatebraid/P2-S5/g2/dryrun-out/rm.out; echo; echo "residual references to the removed flags in the source: $(grep -c -- "VERSION\|args.consumer\|consumer_path" bin/gatebraid-ready.py || true)"'
declared option surface:
   usage: gatebraid-ready [-h] [--strict] [--snapshot-command CMD]
   

add_argument declarations in the source:
   "--snapshot-command"
   "--strict"

--version -> exit 12, stdout 0 bytes
--consumer -> exit 12, stdout 0 bytes

residual references to the removed flags in the source: 0
(exit 0)
```

**The consult's metadata validated against gatebraid/consult@1 before the id was relied on, loader named**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B -c '
import io,re,sys,json,yaml
from jsonschema import Draft202012Validator, FormatChecker
import jsonschema, platform
body=io.open('\''docs/evidence/gatebraid/P2-S5/g2/CONSULT-17-01.md'\'',encoding='\''utf-8'\'').read()
m=re.search(r'\''^```yaml\s*\n(.*?)^```\s*$'\'', body, re.M|re.S)
doc=yaml.safe_load(m.group(1))
schema=json.load(io.open('\''schema/consult.schema.json'\'',encoding='\''utf-8'\''))
v=Draft202012Validator(schema, format_checker=FormatChecker())
errs=sorted(v.iter_errors(doc), key=lambda e: list(e.path))
print('\''loader: %s %s - PyYAML %s - jsonschema %s (format_checker enabled)'\'' % (sys.executable, platform.python_version(), yaml.__version__, jsonschema.__version__))
print('\''schema: gatebraid/consult@1'\'')
print('\''consult_id: %s   slice_id: %s   trigger: %s'\'' % (doc['\''consult_id'\''], doc.get('\''slice_id'\''), doc['\''trigger'\'']))
print('\''result: %s'\'' % ('\''VALID'\'' if not errs else '\''INVALID'\''))
for e in errs[:8]: print('\''   '\'', list(e.path), e.message[:180])
sys.exit(1 if errs else 0)
'
loader: C:\Python312\python.exe 3.12.2 - PyYAML 6.0.2 - jsonschema 4.23.0 (format_checker enabled)
schema: gatebraid/consult@1
consult_id: CONSULT-17-01   slice_id: P2-S5   trigger: repair-sequence
result: VALID
<string>:11: DeprecationWarning: Accessing jsonschema.__version__ is deprecated and will be removed in a future release. Use importlib.metadata directly to query for jsonschema's version.
(exit 0)
```

**The friction #103 precaution, verified rather than assumed: no ref was written by the consult**
```
$ 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'echo "today UTC          : $(date -u +%Y-%m-%d)"; echo "total refs         : $(git for-each-ref --format="%(refname)" | wc -l)"; echo "codex refs         : $(git for-each-ref --format="%(refname)" | grep -ci codex)"; echo; echo "the codex ref and its object:"; git for-each-ref --format="   %(refname) -> %(objecttype) %(objectname)" | grep -i codex; echo; echo "leaf ref file, with its timestamp:"; find .git/refs/codex -type f | while read f; do ls -la --time-style=long-iso "$f" | sed "s/^/   /"; done'
today UTC          : 2026-09-02
total refs         : 23
codex refs         : 1

the codex ref and its object:
   refs/codex/turn-diffs/checkpoints/6568734db6429e0860cf0954b19afffaadb93c9960d666efb23d1018f152be37/7f8d802c118042d20382a16a250ea1c5fb0bd87efd6e2a2ee3221558ade9c8f3/1785489900931/c0da4005-1ff6-434a-b1a5-9ad1a2af1b0e -> tree 8c7df84d62a5d70d4a9ed2f05edf2661bbf5bd43

leaf ref file, with its timestamp:
   -rw-r--r-- 1 rough 197609 41 2026-07-31 05:25 .git/refs/codex/turn-diffs/checkpoints/6568734db6429e0860cf0954b19afffaadb93c9960d666efb23d1018f152be37/7f8d802c118042d20382a16a250ea1c5fb0bd87efd6e2a2ee3221558ade9c8f3/1785489900931/c0da4005-1ff6-434a-b1a5-9ad1a2af1b0e
(exit 0)
```

**The Gate 1 instrument's own run at this gate, retained - the finding repair 1 answered**
```
$ PYTHONDONTWRITEBYTECODE=1 C:/Python312/python.exe -B docs/evidence/gatebraid/P2-S5/g1/negative-criteria.py
changed-path source : git
base                : cbd065893b37f20713ae35b8d2673bf26fe4d2ad
changed paths       : 179
   bin/gatebraid-ready-selftest.py
[... shown 14 of 34 lines; full output: docs/evidence/gatebraid/P2-S5/g2/captures/G2-R-n3-g1-instrument-fired.json]
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
- Consult: `CONSULT-17-01` (in sequence - also on `repair_attempts[1].consult_ref`; friction #94). Verdict **PARTIAL**, independently verified before application: every claim in the response was re-measured against the tree before any byte changed. Accepted in full on the completeness of the F-01 removal, on excluding V9 rather than modifying the frozen Gate 1 instrument, on the elision-line rule, on the twelve-item post-repair claim set, and on the three further statements the V9 fix had to change. Declined on one point, for scope and not disagreement: the consult recommended narrowing the module docstring's stdout sentence to exempt `--help`, and the operator's repair-2 instruction permits no other `bin/` byte change; the residual is disclosed instead.

## Remediation record

Directed by the operator's Human Diagnosis disposition, comment `5518637712`. It is NOT a repair attempt: `repair_limit` was already spent when the disposition was authored, `repair_attempts` stays at two, and the sequence's budget is not drawn on again. Record-only - not one byte under `bin/`, in the retained record, in `g0r/`, in `g1/`, in `schema/` or in `fixtures/` - and the handoff fingerprint is unchanged.

- What it corrects, exactly the bounded re-check's three surviving findings: **G-01** the metadata `notes` field, rewritten so every statement agrees with `repair_attempts`, the V12 row and the review history, and every figure in it DERIVED from the row that measures it rather than typed beside it; **G-02** the V12 row label, which now carries that same derived figure; **G-03** the claim re-check instrument, extended to the metadata block, every heading and every bolded row label, its docstring now naming the domain its universal ranges over.

**Novelty measured against the tree at the state the bounded re-check reviewed (ADR-0027 section 1), recorded for a remediation rather than for a repair attempt**
```
$ 'D:/Program Files/Git/bin/bash.exe' -o pipefail -c 'echo "tree at the re-checked state 622d79a9 : $(git rev-parse 622d79a9f2f21b7b2fabe850c8a3ba0bdd8a473b^{tree})"; echo "tree after the remediation commit    : $(git rev-parse 0a7e2c62349209fc4bbf56b82f576197806ca051^{tree})"; echo "unchanged tree                       : $([ "$(git rev-parse 622d79a9f2f21b7b2fabe850c8a3ba0bdd8a473b^{tree})" = "$(git rev-parse 0a7e2c62349209fc4bbf56b82f576197806ca051^{tree})" ] && echo yes || echo no)"; echo; echo "changed by the remediation commit:"; git diff --name-status 622d79a9f2f21b7b2fabe850c8a3ba0bdd8a473b..0a7e2c62349209fc4bbf56b82f576197806ca051 | sed "s/^/   /"; echo; echo "bytes outside docs/evidence/gatebraid/P2-S5/g2/ : $(git diff --name-only 622d79a9f2f21b7b2fabe850c8a3ba0bdd8a473b..0a7e2c62349209fc4bbf56b82f576197806ca051 | grep -vc "^docs/evidence/gatebraid/P2-S5/g2/")"'
tree at the re-checked state 622d79a9 : 4ed35acc2a254454e21905c502a61de54be0f2d7
tree after the remediation commit    : 7bd10149c6e865262c8e639a55e6fd7dab4fa2ea
unchanged tree                       : no

changed by the remediation commit:
   M	docs/evidence/gatebraid/P2-S5/g2/claims-recheck.py
   M	docs/evidence/gatebraid/P2-S5/g2/gate2.md
   M	docs/evidence/gatebraid/P2-S5/g2/render-gate2.py

bytes outside docs/evidence/gatebraid/P2-S5/g2/ : 0
(exit 0)
```

- Result: `green`

### Remediation 2

Directed by the operator's SECOND Human Diagnosis disposition, comment `5520728930`, after the full re-review returned R3 FAIL on H-01. Also not a repair attempt; `repair_attempts` stays at two, and the fingerprint is unchanged.

- What it corrects: **H-01** alone. The `Reviewer write disclosure` line under `Required disclosures` is the template's mirror of the Review record. It was a typed literal - true when first rendered, when no review had run - and the first remediation's directed Review-record fill made it false without touching its bytes. The disposition directs the correction be made STRUCTURAL, and it is: the per-review disclosures are now one list in the renderer, every per-review entry renders from it, and the mirror is DERIVED from the same list - `none` when every recorded review disclosed nothing, otherwise the union of their lists. A mirror that is derived cannot diverge from what it mirrors, and a review that has not run contributes no entry rather than a sentence about itself.

- What the instrument gained, because the instance is not the class: the derivation claim itself; every bullet under `Required disclosures` enumerated and measured; and a WHOLE-RECORD claim - every line outside the Review record that states a review count, a review status, or that a review has or has not run, listed with its measurement against the Review record and `review-five-items`. That last is the general form of H-01, and it is what the earlier extension lacked: it closed the fields it had been shown, not the relation between a section and the sentences elsewhere that depend on it.

**Novelty measured against the tree at the state the full re-review reviewed (ADR-0027 section 1)**
```
PENDING FIRST RENDER: G2-RM2-novelty
```

- Result: `green`

## Required disclosures

- Deviations (review finding F-01, operator disposition REMOVE): the delivered tool declared two flags beyond the frozen scope and both are gone. The frozen sentence names `--strict` and `--snapshot-command`; the tool also declared `--consumer` and `--version`. Measured against the M2 record at the pinned commit with every document digest re-derived first: `--consumer` 0 occurrences, and all 21 hits of `--version` are `gh --version` or `python --version` probes that never refer to the deliverable. `--version` printed non-JSON to stdout and exited 0, breaking both clauses of the frozen sentence at once and making itself indistinguishable by exit status from a verdict. Removed with them: the `VERSION` constant and the `consumer_path` parameter, which existed only to serve them. `--help` is KEPT because it IS grounded in the frozen record as test-plan command 1 of all three M2 attempts, and with it the zero-exit branch of the SystemExit guard that lets it through.
- Deviations (review finding F-01, and a residual the consult raised that this gate does NOT repair): `--help` still writes usage text to stdout and exits 0, so the module docstring's sentence `Stdout is always exactly one JSON document or nothing` remains literally overbroad on that one path. The consult recommended narrowing the docstring. This gate declines, and the reason is scope, not disagreement: the operator's repair-2 instruction says `no other bin/ byte changes unless a selftest condition referenced a removed flag`, and the reviewer measured zero such conditions. The residual is disclosed here instead of edited around, and it is unchanged from before this repair rather than introduced by it.
- Deviations (review finding F-02, R3 ground 1): V9 is no longer nominated into the byte-reproducible subset. The instrument's changed-path set is the tracked diff UNION the untracked set read at execution time; `--base A..B` pins the tracked half only, so the row cannot reproduce in bytes. What the row asserts is the six verdicts, and those held in the retained run and hold now. The earlier record placed it in the wrong bucket while its own neighbouring sentence said why it could not belong there; the nomination was the defect, not the measurement.
- Deviations (review finding F-02, and the consult's answer to question 6): the earlier wording said the untracked half `can only SHRINK` and that every path it can contain is inside the allowlist `by construction`. Both were unsafe: a later untracked file can appear anywhere and can move both the listing and the verdicts. The claim is now bounded to what was measured - in the retained run all six criteria held, and each future run is evaluated on its own current untracked set.
- Deviations (review finding F-03, R3 ground 2, and operator ruling F-08 ACCEPTED): every residue figure in this bullet is READ FROM THE CITED ROW, not asserted beside it, which is what the earlier prose got wrong when it said ONE against a row that measured more. The sweep over this gate's captures reports 15 residue occurrences. 2 of them are the friction-shaped citation printed by the FROZEN corpus runner inside a case label - a friction reference written without the word the FRICTION regex requires. The other 13 are benign shape collisions: an N-of-N ratio and two path fragments. 12 of the 15 sit inside superseded -pass captures this gate retained deliberately rather than deleted. NONE is a repository identity, and the hard-rule limb is independently verified true by the reviewer: exactly two repository identities, both permitted, and no mention-class issue targeted by any query. Under ruling F-08 the check stays typed `fail` with the count corrected and the diagnosis stated, because admitting the remainder would need a rule change the Plan Approval forbids.
- Deviations (review finding F-04): the elision totals are produced by ONE stated rule, given in the renderer's `rendered_lines` docstring. Carriage returns are removed from each decoded stream, stdout keeps its content without a trailing blank, stderr when present is appended after exactly one newline, and the result is split on newlines. The earlier form used `splitlines()` over the raw concatenation, which treats a lone carriage return as a line break; one capture's stderr carries CRCRLF endings, so its lines were counted twice and one elision total was inflated. The count and the rendered block now come from the same rule.
- Deviations (review finding F-05): every elision names the committed path with forward slashes. The earlier spelling carried the host separator because the renderer displayed the same constant it used to open files; display now uses a separate forward-slash constant and the filesystem constant is never printed.
- Deviations (review finding F-06, ADR-0026 class (c)): every bullet in this section cites the finding, ruling or friction entry it rests on. The earlier record left most of them uncited.
- Deviations (gate-2-contract repair sequence, and friction #94): repair 2 was preceded by the Codex consult the unified sequence places before it. CONSULT-17-01 and its verbatim response are committed beside this record; the consult ran read-only and hermetically with `-C` pointed at a disposable full copy of this repository made outside every governed repository and deleted after capture. The verdict is PARTIAL and its reasons are in the Repair record. Recorded as `repair_attempts[1].consult_ref` because it is an in-sequence consult, never in top-level `consults[]`.
- Deviations (friction #103, and its correction): the precaution against the CLI writing a checkpoint ref into a governed repository was verified rather than assumed. The governed repository carries exactly one `refs/codex` ref; its leaf file is dated more than a month before this consult and its object is the same tree this Slice's entry report recorded as pre-existing. No ref was written by this consult.
- Deviations (ADR-0011 section 2, as amended by ADR-0016): the handoff fingerprint is re-measured at the NEW implementation-complete commit, the repair-2 commit that restored the frozen tool surface. Every commit after it is record-only and confined to docs/evidence/gatebraid/P2-S5/g2/, which is inside the frozen allowlist.
- Deviations (ADR-0028 decision 2): THE NOMINATED DETERMINISTIC SUBSET of this record. IN the subset, and required to reproduce byte-identically: E1's three rows, E3, E4b, V0, V0F, V1, V2, V3, V4, V6, V7, V8, V10, and the two repair novelty rows. OUTSIDE the subset, by the exclusion limb, and named here rather than left to be discovered: V5, the live composition, whose report is re-derived from the control plane at each run; V9 and V9b, for F-02's reason; V12 and its two falsification runs, whose domain is the captures directory as it stood when they ran and which grows as this gate writes the captures that follow them; E2 and E4, whose recorded values include a lease timestamp and a branch head that later commits move; and V11's second half, which validates this record and therefore reads bytes that this render produced.
- Deviations (ADR-0027 section 1): repair 1 remains as recorded - a Gate 1 check instrument's exclusion set, not the deliverable and not this record's prose - and repair 2 is the last attempt the sequence allows. Both carry a novelty row comparing the tree against the tree at the previous failed state, measured before the result is graded.
- Deviations (review finding F-07, left standing on the reviewer's own reasoning and the operator's instruction): the disclosures that narrate this record's own authoring history - the rejected first render, the corrected assertion, the corrected split rule - remain. The reviewer records a real gap in ADR-0026, which forbids revision narrative without providing a sanctioned home for a pre-submission correction the executor is simultaneously required to be honest about, and declines to fail anything over it. It is queued for an ADR clarification rather than repaired here.
- Deviations (friction #15, and P1-S3's second dry-run): the composer's argument-splitting rule was settled by measurement during authoring. The producer command must be split by POSIX rules on every platform; with `posix=False` the quotes stay attached, the stub arrives wrapped, the child emits ZERO BYTES, and the decode guard appears to pass while testing nothing. The default producer command is written with forward slashes because POSIX rules treat a backslash as an escape.
- Deviations (ADR-0028 decision 3, the IN-03 class): this record does not echo the near-miss tokens its falsification seed carries. The seed is retained beside the sweep instrument and the tokens live there, not here; an earlier render quoted three of them into this file and the record's own sweep caught it.
- Deviations (full re-review finding H-01, and the second Human Diagnosis disposition's rule 2): the `Reviewer write disclosure` mirror is DERIVED by the renderer from the per-review entries it renders, and is never a typed literal. It read `not applicable - no review has run` while the Review record recorded two completed reviews, each disclosing `none`; the line was true when written and the first remediation's directed Review-record fill made it false without touching its bytes. The structural form is the fix: one list feeds both the per-review entries and the mirror, so the two cannot disagree, and a review that has not run contributes no entry rather than a sentence about itself.
- Deviations (full re-review finding H-03, recorded for the closeout ledger): the previous remediation report of this window said of G-03 that the class was closed and not just its instance. H-01 was a surviving instance of that class, so the sentence overreached. The instrument's own summary and docstring were correctly bounded; the overreach was in the report's prose about it, and it is recorded rather than quietly dropped.
- Deviations (full re-review findings H-02 and H-04, ruled by the second disposition): the `Remediation record` heading stays - it is the structural gap already queued with F-07 for the ADR-0026 clarification, since the template offers a directed non-repair remediation no home and filing it under the Repair record would corrupt `repair_attempts`. The per-review disclosure `none` is the repository-scoped answer the contract's clause asks for; the reviewer's own report on the ignored path and its named scratch files are disclosed in that report and are not listed here, so the derived mirror is `none`.
- Deviations (ADR-0026 decision 1, and the reviewer's F-04 observation): four unreferenced probe-stderr files under this Slice's two dryrun-out directories carry CRLF in the working copy and are stored LF under the tree's text attribute. No pin covers them and no capture names them.
- Deviations (gate-2-contract Prohibited, scratch clause): scratch paths outside every repository were relied on and are named. Every commit message passed through a file in the session scratchpad outside this repository, never as a shell argument; the consult's disposable repository copy lived there and was deleted; the approval-fidelity row writes and removes one file inside this gate's own evidence directory.
- Deviations (ADR-0026 class (b), and friction #96): the record's FINAL bytes are validated and swept by runs cited by output_ref and not inlined, because a document that quoted its own verification would change the bytes that verification read.
- Environment (friction #89): Windows host, Windows 11 build 10.0.26200, AMD64, node RoughEgoist; Git for Windows 2.51.0.windows.1 whose SYSTEM configuration carries core.autocrlf=true; every gh call pins GH_CONFIG_DIR=C:/Users/rough/.gh-gatebraid and uses endpoints with no leading slash; every Python invocation carries -B with PYTHONDONTWRITEBYTECODE=1, set inside the wsl command for the WSL half; Windows interpreter C:/Python312/python.exe with CPython 3.12.2, PyYAML 6.0.2, jsonschema 4.23.0; WSL /usr/bin/python3 with CPython 3.12.3, jsonschema 4.10.3, whose captures stamp platform.os `wsl`; the Codex CLI is codex-cli 0.144.6, invoked `--ephemeral --sandbox read-only --ignore-user-config`. The `python` on PATH is the MSYS 3.14.3 build and carries neither library, which is why no declared command names it and why delta D-3 exists. Captures are argv-form unless the row declares shell semantics, in which case the shell, pipefail and the exit-code source are all recorded. environment=mixed-see-prose.
- Reviewer write disclosure: `none`

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
ended_at: "2026-09-03T07:01:11Z"
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
    command: "the same run; the residue count is the cited capture's own figure, diagnosed by class in the disclosures - one friction-shaped citation printed by the frozen corpus runner, the remainder benign shape collisions, none a repository identity. Typed fail under operator ruling F-08: admitting the remainder would need a rule change the Plan Approval forbids"
    result: fail
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep.json"
  - name: frozen-tool-surface-restored
    command: "bin/gatebraid-ready.py --help declares only --strict and --snapshot-command; --version and --consumer are usage errors with exit 12 and empty stdout"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-R2-surface.json"
  - name: gate2-record-machine-validated
    command: "bin/gatebraid-validate.py --record docs/evidence/gatebraid/P2-S5/g2/gate2.md --report-id cov-P2-S5-g2-gate2.md"
    result: pass
    output_ref: "docs/evidence/gatebraid/P2-S5/g2/captures/G2-record-validation.json"
  - name: review-five-items
    command: "R1 through R5, by an independent read-only reviewer in a separate session"
    result: not_run
    output_ref: "#review-record"
handoff_fingerprint:
  active_branch_head: "5b586029344eb6df4a964c34baa1eb12e2916f6d"
  tree_sha: "f696944947a342b6163bf4ad7d9137674830a2f7"
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
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D0-scope-pin.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D0F-scope-pin-falsify.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D1-corpus-digest.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D10-negative-falsify.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D11-wsl-toolchain-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D11-wsl-toolchain.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D2-corpus.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D3-selftest-windows.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D4-selftest-wsl.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D5-live-ready.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D6-producer-failure.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D7-decode-guard.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D8-consumer-refusal.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D9-negative-pinned.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-D9-negative.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E1-approval-fidelity-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E1-approval-fidelity.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E1-approval.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E1-consume-next-approval.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E1-entry-fields.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E1-executor-identity.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E1-remove-needs-human.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E2-field-options.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E2-lease.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E2-workflow.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E3-baseline-pass1.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E3-baseline.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E4-base-sha.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E4-branch.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E4-entry-readback.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-E4b-evidence-commit.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-R-n3-g1-instrument-fired.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-R1-novelty.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-X-checkpoint.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-X-exit-readback.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-X-workflow-needs-review.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-X-workflow-options.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep-falsify-near-miss.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep-falsify-retained.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-closed-set-sweep.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-record-sweep.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-record-validation.json"
    - "docs/evidence/gatebraid/P2-S5/g2/captures/G2-wsl-ready-selftest.json"
    - "docs/evidence/gatebraid/P2-S5/g2/checks-g2-closed-set-sweep.py"
    - "docs/evidence/gatebraid/P2-S5/g2/dryrun-out/approval-body-raw.txt"
    - "docs/evidence/gatebraid/P2-S5/g2/dryrun-out/checkpoint-g2.txt"
    - "docs/evidence/gatebraid/P2-S5/g2/dryrun-out/lease.txt"
    - "docs/evidence/gatebraid/P2-S5/g2/dryrun-out/s06c.err"
    - "docs/evidence/gatebraid/P2-S5/g2/dryrun-out/t5.err"
    - "docs/evidence/gatebraid/P2-S5/g2/dryrun-out/t5.out"
    - "docs/evidence/gatebraid/P2-S5/g2/dryrun-out/t6.err"
    - "docs/evidence/gatebraid/P2-S5/g2/dryrun-out/t7.err"
    - "docs/evidence/gatebraid/P2-S5/g2/dryrun-out/t7.out"
    - "docs/evidence/gatebraid/P2-S5/g2/dryrun-out/t8.err"
    - "docs/evidence/gatebraid/P2-S5/g2/dryrun-out/t8.out"
    - "docs/evidence/gatebraid/P2-S5/g2/falsification/SEED-near-miss-new-classes.json"
    - "docs/evidence/gatebraid/P2-S5/g2/gate2.md"
    - "docs/evidence/gatebraid/P2-S5/g2/negative-criteria.py"
    - "docs/evidence/gatebraid/P2-S5/g2/render-gate2.py"
    - "docs/evidence/gatebraid/P2-S5/gate0.md"
    - "docs/evidence/gatebraid/P2-S5/render-gate0.py"
consults: []
repair_attempts:
  - number: 1
    hypothesis: "N3's content limb fired on a retained record that did not change; the Gate 1 mechanisation hard-codes the two per-gate subdirectories that existed when it was written, and the frozen plan says `this gate's own subdirectories`, which at Gate 2 is three"
    result: green
  - number: 2
    hypothesis: "The independent review's R3 FAIL and its HIGH finding share one cause - a claim the record or the tool makes that its own measurement contradicts - so the repair restores the frozen two-flag surface and re-derives every contradicted figure from the row that measures it, rather than restating it in prose"
    result: green
    consult_ref: CONSULT-17-01
approvals:
  - type: "Plan Approval (G1→G2)"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5503291709"
    author: "MianliWang"
  - type: "Human Diagnosis"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5518637712"
    author: "MianliWang"
  - type: "Human Diagnosis"
    comment_url: "https://github.com/MianliWang/gatebraid/issues/17#issuecomment-5520728930"
    author: "MianliWang"
plan_hash: "b2cd75f6a49bb056fd16bc3d2f4cfd5cf98ae8515b5761908add2ed5405cc424"
allowlist_hash: "4110b3021bdfc2fcda1f5f90528db01eb87b554177e2176ccfba46ccd6ca3750"
evidence_files:
  - docs/evidence/gatebraid/P2-S5/g2/gate2.md
  - docs/evidence/gatebraid/P2-S5/g2/CONSULT-17-01.md
  - docs/evidence/gatebraid/P2-S5/g2/CONSULT-17-01-response.json
notes: "The fourth gatebraid-ready attempt on the M2 slice-C frozen scope, built on the M3 stack. The deliverable is the ready pair alone; it composes the landed producer and consumer and modifies neither. The four ratified deltas are implemented as the approval states them, and D-4 - the producer's status is interpreted against its own declared space rather than tested against zero - is the one that keeps a degraded-but-emitted document from being discarded. Twenty selftest conditions each emit their own summary row; S09 carries IN-01, the class the frozen corpus does not hold, and S10 parses the producer's docstring so the D-4 partition cannot drift from its source unnoticed. TWO repair attempts were taken and both are listed in repair_attempts. Attempt 1 changed a check instrument's domain constant, touching neither the deliverable nor this record's prose. Attempt 2 changed BOTH: it removed two flags from the deliverable that the frozen scope does not name, and it re-rendered this record. One check is typed fail and is disclosed in full: the sweep's explanation limb leaves 15 residue occurrences - 2 friction-shaped citation(s) printed by the frozen corpus runner and 13 benign shape collisions, 12 of the 15 inside superseded -pass captures - none a repository identity, and admitting the remainder would need a rule change the Plan Approval forbids. Every figure in this field is derived from the row that measures it, which is what the operator's Human Diagnosis disposition directed after the earlier wording of this field contradicted repair_attempts and the V12 row. The review is NOT this session's: R1 through R5 belong to an independent reviewer, and Gate = G2 passed is not set here."
```
