# ADR-0018 — A prohibition names the pattern it forbids; an approval cites the rule it enforces

**Status:** Accepted · M2 (2026-07-31) · Product: Gatebraid (ADR-0010)
**Amends:** ADR-0012 §1 (the closing-keyword ban) and the Gate 2 review item R4.
Both otherwise stand.
**Provenance:** Slice A's Gate 3 entry (2026-07-31), friction #21; Slice A's Gate
2 review item R4 (2026-07-31), the earlier instance of the same over-match.

## Context

Two things went wrong at Gate 3's entry, and only one of them was the contract's
fault.

**The over-match.** ADR-0012 §1 forbids `close`/`closes`/`closed`,
`fix`/`fixes`/`fixed`, `resolve`/`resolves`/`resolved` — but it forbids them
*"when referencing the Slice issue or any other Gatebraid issue"*. The Release
Approval's term 4 paraphrased the list and dropped the qualifier. Slice A's branch
carries two conventional-commit prefixes, `fix(P1-S1): …`, written at Gate 2 and
reviewed there. Read as a bare token list, the branch violated the approval.

This was the **second** instance. Gate 2's review item R4, scoped to GraphQL
documents, tripped on the word `mutation` inside a docstring asserting that the
code performs no mutation. A ban expressed as a word list will keep catching
`fix(`, `closes the gap`, and every comment that names what the code does *not*
do. The words are a proxy. GitHub's actual closing behaviour is a pattern:
a keyword immediately preceding an issue reference.

**The authority conflict, which is the more important half.** The executor did not
stop. Its reasoning is on the record and was raised before the pull request was
opened: term 4 cites ADR-0012 §1 as its authority; §1 scopes the ban to
issue-referencing occurrences; no `keyword + #number` pattern exists on the
branch; and term 4's own mechanical test — `closingIssuesReferences` read back —
returned 0. Cited authority and stated test agreed.

The conclusion was right and the reasoning was good. **The action was still
wrong.** Under the precedence order an operator approval outranks the committed
tree, so where an approval term and the ADR it cites disagree, the *approval*
wins on precedence and the *ADR* wins on merit — and choosing between them is an
authority question, not a technical one. "Stop and ask" exists for exactly this.

And the conflict was manufactured by the coordinator, not by the executor: the
term restated a rule instead of citing it, and the restatement drifted in the one
clause that mattered. This is the same disease ADR-0014 §2 addressed between
schema and template — two copies of one rule, one of them updated.

## Decision

**1. ADR-0012 §1's ban is a pattern, not a token list.** What is forbidden is a
closing keyword **immediately preceding an issue reference** — `keyword #n`,
`keyword owner/repo#n`, `keyword <issue-url>` — in the pull-request body or in
any commit message the pull request carries, in any case. That is GitHub's own
syntax and it is the whole of the mechanism. A bare occurrence of any of those
words, referencing nothing, is not prohibited and never was.

**2. A check written as a token list must state the pattern it proxies for, and
where the proxy over-matches, the pattern governs.** R4 is rescoped accordingly:
it looks for GraphQL mutation *operations*, not for the string `mutation`.
A check that cannot be satisfied by correct work is not strict; it is broken, and
it trains the executor to route around checks.

**3. An approval term cites the rule it enforces; it does not restate it.** Terms
exist to authorise scope — what may be pushed, merged, and where — and to name
constraints the contracts do not already carry. Where a contract rule already
exists, the term references it by number and stops. A term that paraphrases a
contract creates a second copy that will drift, and it drifts in the direction of
whoever wrote it last.

**3a. An approval is a structured object, and an ambiguous one is invalid**
(CONSULT-M2-01 Q3). Citation alone leaves a vague approval merely vague. So an
approval:

- cites the **precise rule version** it relies on — an ADR number plus the commit
  SHA in which that ADR stands;
- fills only the objects of *this* authorisation — the branch, the head SHA,
  `plan_hash`, `allowlist_hash`, and any explicit exception;
- expresses any departure from a contract rule as a structured **`override`**
  naming the clause, the scope and the reason — never as prose that happens to
  differ;
- **is invalid if a required field is missing, if two of its terms conflict, or if
  a term is ambiguous.** An invalid approval is not interpreted charitably; the
  gate stops as if none existed.

A conflicting or mistaken approval is corrected by issuing a **new approval that
supersedes it**, cited by its comment URL. The executor never selects which of two
approvals is in force.

This is what makes decision 4 affordable. The objection to "stop" is that it
trains the operator toward vaguer terms so conflicts never surface; 3a removes the
payoff, because a vaguer approval fails validation rather than passing quietly.

**4. Where a term and its cited rule disagree, the executor stops.** It does not
choose, and it does not resolve the conflict in favour of the better reasoning —
because the disagreement is between two authorities, and adjudicating between
authorities is exactly what the approval doors exist to keep out of the
executor's hands. Raising it before acting, as happened here, is necessary but
not sufficient: the raising must be to a human, and the gate waits.

## Consequences

ADR-0012 §1's wording, `protocols/gate-2-contract.md` (R4),
`protocols/gate-3-contract.md`, and the Release Approval's standard terms change.
No schema, field, view or label change.

Decision 4 costs a round trip in the case where the executor is right — as it was
here. That cost is the point. The alternative is an executor that has once
successfully overridden an operator's literal instruction because its own reading
was better, which is a precedent no subsequent instruction can un-set.

Decision 3 is the cheaper half and prevents most instances of decision 4 arising
at all. Slice A's conflict existed only because a term said in its own words what
an ADR already said in its.

## Reopening conditions

- If a pattern-based check ever **under**-matches — a real closing reference
  merges without being caught — then the token list was doing work the pattern
  does not, and decision 1 needs the union rather than the pattern alone.
- If GitHub extends closing-keyword syntax beyond `keyword <reference>`,
  decision 1's enumeration of forms is stale and must be re-derived from
  GitHub's documentation rather than from this ADR.
- If stopping under decision 4 ever produces a deadlock — an approval whose terms
  cannot be satisfied and whose author is unavailable — the escape is a new
  approval, never an executor's reinterpretation of the old one.
