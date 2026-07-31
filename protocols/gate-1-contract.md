# Gate 1 contract — Planning (read-only; temporary team permitted)

**Normative.** Inherits the common rules of `gatebraid-control-plane-spec-v1.md` §4. Changes only by ADR.

## Entry

- `Gate = G0 passed`. Workflow → `Gate 1 — Planning`.

## Actions (all read-only)

1. Read-only exploration of the repository and its context.
2. **Optional Agent Team** (verified constraints per report 11 D5, written here verbatim as contract terms): ≤3 read-only teammates, spawned from the plugin's subagent definitions; teammates inherit the **lead's** permission mode at spawn, so the lead must never run in any bypass mode; a subagent definition's `skills`/`mcpServers` frontmatter is ignored for teammates — role knowledge lives in the definition body; in-process teammates do not survive `/resume`; one team per session, no nesting, lead fixed; task status can lag and may need a nudge. **All findings are flushed to the Slice issue before the team dissolves.**
3. Produce the plan: approach · exact `write_domains` allowlist · test plan with commands that are **runnable as written on the slice's declared `environment`** · risk notes · rollback note · **at least one negative criterion** — a checkable property the diff must *not* have ("contains no write operation", "adds no runtime dependency", "touches no file outside `bin/`"). It is what review item R4 checks at Gate 2, and it is what keeps a first review from being unfalsifiable (ADR-0011 §5).
4. **Dry-run every declared test command** on the slice's declared `environment`, and record that they ran. "Runnable as written" means runnable *there*, not well-formed on inspection: Slice A froze `> /tmp/snap.json … open('/tmp/snap.json')`, which is correct on Linux and fails on `environment: windows`, where the shell and the interpreter disagree about what `/tmp` means. It was checked by reading, passed, and could not be repaired at Gate 2 because the plan was frozen and its hash bound an approval. A checklist item satisfiable by reading is not evidence-backed.
5. Complete `templates/gatebraid-gate1-exit-checklist.md` — every item evidence-backed.
6. **Freeze** the plan and allowlist; record `plan_hash` and `allowlist_hash` in the evidence file, **with the command that reproduces each one beside its value**.

   Both are SHA-256, lowercase hex, over UTF-8 bytes (ADR-0011 §3):

   - `allowlist_hash` — each `write_domains` entry stripped of surrounding whitespace, sorted by byte value, joined with `\n`, one trailing `\n`.
   - `plan_hash` — the lines of `gate1.md` strictly between the `## Plan (frozen at exit)` heading and the next line beginning with `## `, each stripped of trailing whitespace, leading and trailing blank lines removed, joined with `\n`, one trailing `\n`.

   A hash that cannot be recomputed is decoration: Gate 2 relies on the allowlist being pinned here, and `gatebraid-correct-course.md` relies on new hashes being comparable to old ones. Python 3 standard library only (ADR-0009).

## Prohibited

**Any state-changing Git command against the slice's working tree or branches**; any dependency installation; any teammate with write tools; proceeding to any Gate 2 action before the recorded human approval. Writing and committing this gate's own evidence file is the Exit step and is **not** a violation, for the same reason it is not one at Gate 0.

The one sanctioned rewrite of the Slice issue body is the Gate 1 exit metadata update below. It re-emits the `## gatebraid-metadata` block **byte-identical apart from the fields this exit changes** — `write_domains`, to match the frozen allowlist. Nothing else in the block or the body is touched.

## Exit

- `docs/evidence/gatebraid/<slice_id>/gate1.md` written from `templates/gate1-evidence.md` (`gate: 1`, `result: needs_approval`).
- The Slice issue's `## gatebraid-metadata` block is updated so `write_domains` matches the frozen allowlist — the one sanctioned rewrite, re-emitted byte-identical apart from that field. The frozen plan in `gate1.md` remains authoritative and is what `allowlist_hash` covers; the issue metadata is a declaration of intent brought into agreement with it.
- `Gate = G1 passed`; Workflow → `Needs Plan Approval`; `Next Approval = Plan Approval (G1→G2)`; `needs-human` on.
- **A recorded human approval comment is the only door to Gate 2.**
