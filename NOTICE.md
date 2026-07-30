# NOTICE — Third-party sources and attribution

Gatebraid (this repository) adopts **designs** from the MIT-licensed projects
below as owned, re-written, attributed ports — never as dependencies, forks,
or installations (ADR-0009, ADR-0010). No source framework is installed or
executed in any Gatebraid milestone.

As of M1, the derived artifacts are **templates and specifications only**; the
M2/M3 code ports (frontier, guard, doctor, snapshot, skill acceptance method)
will extend this file in the PRs that add them.

| Source | License · Copyright | Derived in Gatebraid (M1) |
|---|---|---|
| **Spec Kit** — github.com/github/spec-kit | MIT © GitHub, Inc. | Gate/pause-resume semantics and validation-first discipline informing the Gate contracts (design reference only) |
| **GSD (get-shit-done)** — github.com/gsd-build/get-shit-done | MIT © Lex Christopherson | Checkpoint/approval taxonomy mapped into `Next Approval`; wave/frontier grouping and file-overlap serialization specified for `gatebraid-frontier` (M3); 2–3-task slice-sizing heuristic in the slice template |
| **CCPM** — github.com/automazeio/ccpm | MIT © Ran Aroussi | Epic-parent/sub-issue hierarchy shape; `depends_on`/`conflicts_with`-class metadata semantics in `gatebraid/slice@1`; progress-comment handoff convention; "status is a script" principle |
| **BMAD-METHOD** — github.com/bmad-code-org/BMAD-METHOD | MIT © BMad Code, LLC. **Trademark:** the BMAD name is trademarked and is not reused; derived artifacts are renamed `gatebraid-*` | `templates/gatebraid-gate1-exit-checklist.md` (from the implementation-readiness checklist); `templates/gatebraid-correct-course.md` (from correct-course); story-context ideas in `templates/slice.md` |
| **Superpowers** — github.com/obra/superpowers | MIT © Jesse Vincent | Verification-before-completion folded into the handoff contract (`schema/handoff.schema.json`, `templates/handoff.md`); systematic-debugging framing of the "new hypothesis" repair rule; skill-TDD specified as the M2/M3 skill acceptance method |

Additional non-framework provenance: seven operational rules adapted from the
Hermes Agent audit (report 10; recorded in ADR-0006) — respawn guard,
structured handoff metadata, blocker-recurrence escalation, review-required
convention, deterministic failure-loop breaker, managed-scope configuration,
hard deny rules. Hermes itself is excluded (ADR-0006); Hermes Agent is
MIT-licensed by Nous Research; the rules are re-specified here, not copied.

License texts: each upstream's MIT license text is available at its repository
above. Derived-artifact provenance is also noted in each artifact's header
where practical.
