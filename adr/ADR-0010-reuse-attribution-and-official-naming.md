# ADR-0010 — Reuse, attribution, and official naming

**Status:** Accepted · M1 (2026-07-29) · **Governs all names; overrides former names wherever earlier documents conflict.** The approved M1 ADR set is exactly ADR-0001 through ADR-0010.
**Provenance:** report 12 §2 (license verification of all five source snapshots), §5 (reuse matrix), §19 (vendoring strategy); ADR-0009 (dispositions); operator naming decision 2026-07-28 ("M1 tasking — Gatebraid edition"); operator M1 correction 2026-07-29 (naming content — originally drafted as a standalone eleventh ADR — merged into this ADR before any commit; no eleventh ADR exists).

## Part I — Reuse and attribution

1. **Ports are owned.** Every adopted design from Spec Kit, GSD, CCPM, BMAD, or Superpowers is re-implemented as Gatebraid-owned code, schema, or template — vendored, attributed, re-written. No fork, no dependency, no installation of any source framework (ADR-0009).
2. **Attribution lives in `NOTICE.md`** at the repository root: source project, upstream URL, license (all five are MIT), copyright holder, and what was derived. `NOTICE.md` is updated in the same PR as any new derived artifact.
3. **BMAD trademark rule.** The BMAD name is trademarked and is not reused in any Gatebraid artifact name. BMAD-derived artifacts are renamed `gatebraid-*` (M1: `gatebraid-gate1-exit-checklist`, `gatebraid-correct-course`; later: the Slice body conventions and portfolio-brief template that draw on story-context and sprint-status).
4. **Scope in M1.** M1 derives **templates and specifications only** (no code exists yet to vendor). The M2/M3 ports (frontier algorithm, doctor concept, skill-TDD method, etc.) inherit this ADR's rules and extend `NOTICE.md` when they land.
5. **Sanitized provenance.** Any artifact migrated from prior systems carries a provenance header (origin, original ID, timestamp) per ADR-0001.

## Part II — Official Naming and Superseded-Name Migration Map

### Official names

1. The product is **Gatebraid**; the full system name is the **Gatebraid Delivery System**.
2. The v1 workflow profile is **Gatebraid Classic**, profile id **`classic`** (the profile id is a stable identifier, not a former name — it does not rename).
3. Control repository: **`MianliWang/gatebraid`** (private). Scratch repository: **`MianliWang/gatebraid-scratch`** (private).
4. Schema ids live under **`gatebraid/*@1`**: `gatebraid/slice@1`, `gatebraid/stage@1`, `gatebraid/phase@1`, `gatebraid/project@1`, `gatebraid/gate-run@1`, `gatebraid/consult@1`, `gatebraid/handoff@1`.
5. Issue-body machine-readable block heading: **`## gatebraid-metadata`**.
6. Template names: **`gatebraid-gate1-exit-checklist`**, **`gatebraid-correct-course`** (Part I §3).
7. Future tool names (forward-binding for M2/M3): plugin **`gatebraid`**; scripts **`gatebraid-frontier`**, **`gatebraid-guard`**, **`gatebraid-doctor`**, **`gatebraid-snapshot`**; deferred dispatcher name **`gatebraidctl`**; business-repository evidence path (M2+) **`docs/evidence/gatebraid/<slice_id>/`**; skills/subagents named under the product convention when those milestones are tasked.

### Historical mapping table — former names appear ONLY here

> **Explicitly marked historical record.** The left column exists solely so a
> future reader can connect prior documents to current resources. Former names
> are deprecated for all new resources and appear nowhere else in this
> repository except quoted provenance.

| Former (deprecated; history only) | Official |
|---|---|
| "Mianli Classic Delivery" (product/system) | **Gatebraid** / **Gatebraid Delivery System** |
| `MianliWang/mianli-control` (control repo) | **`MianliWang/gatebraid`** |
| `MianliWang/classic-scratch` (scratch repo) | **`MianliWang/gatebraid-scratch`** |
| `mianli-classic` (plugin) | **`gatebraid`** |
| `classic/*@1` (schema-id namespace) | **`gatebraid/*@1`** |
| `## classic-metadata` (block heading) | **`## gatebraid-metadata`** |
| `classic-gate1-exit-checklist`, `classic-correct-course` | **`gatebraid-gate1-exit-checklist`**, **`gatebraid-correct-course`** |
| `classic-frontier`, `classic-guard`, `classic-doctor`, `classic-snapshot` | **`gatebraid-frontier`**, **`gatebraid-guard`**, **`gatebraid-doctor`**, **`gatebraid-snapshot`** |
| `classicctl` (deferred dispatcher) | **`gatebraidctl`** (still deferred) |
| `docs/evidence/classic/<slice_id>/` (evidence path, M2+) | **`docs/evidence/gatebraid/<slice_id>/`** |
| `Classic-*` (BMAD-derived artifact prefix) | **`gatebraid-*`** |

### Unchanged names (explicitly)

The GitHub portfolio Project remains **"Mianli Engineering"**; the repository
labels remain `needs-human`, `strict-gate`, `security-sensitive`,
`scientific-evidence`; the profile id remains `classic`; prior report and spec
filenames keep their historical titles as evidence.

### Rules

1. **No resource is ever created under a former name.**
2. Where a former-name repository already exists, it is **renamed** (GitHub redirects preserved) — never paralleled by a duplicate.
3. Former names may appear only in this ADR's marked table and in quoted, provenance-headed historical material.
4. Any document, schema, or issue found bearing a former name in a new resource is a defect against this ADR.

## Consequences

- License compliance is a review item on every PR that adds derived material; renames per Part II do not erase attribution — `NOTICE.md` records the derivation chain even where names moved.
- The locked spec is carried in this repository as `protocols/gatebraid-control-plane-spec-v1.md` — the official-naming edition of `classic-control-plane-spec-v1.md` (2026-07-27): names moved per Part II, content otherwise unchanged, with one operator-ratified substitution (2026-07-29): the illustrative `depends_on` example references `gatebraid-scratch`, keeping all committed examples self-contained within Gatebraid resources.
