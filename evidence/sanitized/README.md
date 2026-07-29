# evidence/sanitized/

Cross-project **sanitized** evidence artifacts (consult files and responses,
migrated records, audit excerpts) whose home is the control repository rather
than a working repository (spec §4 common rules).

Rules (ADR-0001, ADR-0010):

1. **Provenance headers are mandatory** — origin, original ID/path, timestamp,
   and what sanitization was applied. Sanitization is disclosed, never silent.
2. **Never enters this directory:** secrets, tokens, keys, credential
   material; sensitive experimental data or specific result values; personal
   data; absolute local paths as functional configuration; unvalidated claims
   phrased as validated.
3. Per-slice gate evidence lives in the working repository at
   `docs/evidence/gatebraid/<slice_id>/` — not here.

M1 note: this directory is intentionally empty except for this README; the
first sanitized artifacts arrive with M2's real Gate 0/1 cycle.
