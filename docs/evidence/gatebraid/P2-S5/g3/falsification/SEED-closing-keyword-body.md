Seeded pull-request body for falsification only.

Closes #17 — this line is the thing closure precondition (b) forbids, and it
exists so the scan can be shown able to fire before its clean run is trusted.
Also seeded in other lawful shapes: Fixes MianliWang/gatebraid#17 and
resolves https://github.com/MianliWang/gatebraid/issues/17

And a NEAR-MISS that must NOT match, because a conventional-commit prefix
references nothing: fix(scope): tidy the renderer
