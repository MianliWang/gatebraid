# Gate 0 state-packet queries — v1

Normative for the closed-set state packet `M3-PLAN.md` §2 names as Gate 0's
startability authority during the N2/N3 bootstrap boundary. Coordinator-drafted
under the operator's ruling of 2026-08-17 (N2 approval item A5), because the two
reads below had **no form recorded in any committed file** and a session
inventing one is the prohibition this file removes.

## 0. What this file is, and is not

It **is** the contract each read must satisfy, the closed set it may touch, the
failure semantics, and the falsification each must pass before its output is
trusted. It **is not** a claim that the invocation sketches in §3 are correct as
written: the GitHub API surface is outside this repository's control and moves.
**The executor verifies each invocation read-only, records the exact form that
worked verbatim in the gate evidence, and — if the working form differs from the
sketch — records the difference and proceeds.** Correcting a sketch against a
measured API response is verification, not invention; composing a filter
expression from imagination is invention and remains prohibited.

## 1. Closed set — the only identities any query may name

- Repositories: `MianliWang/gatebraid` and `MianliWang/gatebraid-scratch`. No
  others, ever.
- Project: the private user Project "Mianli Engineering", id
  `PVT_kwHOBRofUs4Beum7`.
- Items: named by issue number or node id, enumerated in the packet before the
  first query runs.

**Never** list account repositories, never enumerate the Project's items to
discover what exists, never widen a query to "find" a missing item. A required
item that is absent is a **stop**, and its creation is a proposal to the
operator, never an action.

## 2. Failure semantics — identical for every query

1. **Fail closed on every non-zero exit**, on any HTTP status other than 200,
   on any response carrying an `errors` array, on any missing required field,
   and on any timeout. A failed query yields `undecidable`, never a default and
   never an inferred value.
2. **No retry that could mask a partial answer.** One attempt; a transport
   failure is reported as a transport failure.
3. **Every query's exact invocation, exit status, and raw response digest are
   recorded** in the gate record's evidence by `checks[].output_ref` pointer to
   a committed capture file (ADR-0028 §2: pin, never name a moving ref).
4. **Pagination:** if a response is or could be paginated, either every page is
   fetched or the read fails closed with a bounded-snapshot flag. A truncated
   list silently treated as complete is the P0-3 class.

## 3. The two reads

### Q6 — per-item Project field read

**Contract.** Given one issue (repository + number), return that issue's
Project item field values for exactly: `Workflow`, `Gate`, `Next Approval`,
`Environment`, `Status`. Absent field ⇒ report absent; do not substitute empty
string. Item not on the Project ⇒ fail closed.

**Candidate invocation** (`gh api graphql`, verify and correct against the live
shape):

```
gh api graphql -f query='
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
              ... on ProjectV2ItemFieldSingleSelectValue{ name  field{ ... on ProjectV2FieldCommon{ name } } }
            }
          }
        }
      }
    }
  }
}' -F owner=MianliWang -F repo=<repo> -F number=<n>
```

Then select the item whose `project.id` equals `PVT_kwHOBRofUs4Beum7` — **an
item on a different project is not this project's state** — and read the five
field names. If the item appears on more than one project, that is a finding,
not a tie to break.

**Falsification before first trusted use** (ADR-0028 decision 1): run it once
against an issue number that does not exist and once against an issue that is
not on the Project; both must fail closed with a non-zero disposition, and both
demonstrations are recorded beside the first real use.

### Q7 — dependency / blocked-by read

**Contract.** Given one issue, return the issues it is **blocked by** and the
issues it **blocks**, as `owner/repo#number` identities, complete or failed.
Both directions are required: `M3-PLAN.md` §2 O0's P0-4 names "both dependency
directions cross-checked" as a hardening requirement, and a one-directional read
that reports as complete is the defect that requirement exists to remove.

**Candidate invocation.** GitHub exposes issue dependencies and sub-issues
through evolving REST and GraphQL surfaces; the executor determines the current
form by reading GitHub's own documentation and verifying read-only against a
known pair in `MianliWang/gatebraid-scratch` whose relationship is already known
from the M1 sample hierarchy. **The verified form, and only the verified form,
is what the packet records.** Where a native dependency read is unavailable for
one direction, that direction is reported as a **measured gap** and the packet's
startability verdict becomes `undecidable` — never a silent one-directional
answer.

**Falsification before first trusted use:** run it against an issue with no
dependencies (must return empty, not error) and against a non-existent issue
(must fail closed). Both recorded.

## 4. What these queries do not do

They do not write. They do not create, label, assign, close, or move anything.
They do not read any repository or project outside §1. They do not decide
anything: they supply the values the Gate 0 contract evaluates, and if any value
is unavailable the honest outcome is a stop.

## 5. Amendment

A change to either contract is a change to Gate 0's authority and lands only
through an approved batch, never by a session's improvisation at gate time. A
change to an *invocation* that a measurement showed to be wrong is recorded in
the batch report and lands with the next batch that touches this file.
