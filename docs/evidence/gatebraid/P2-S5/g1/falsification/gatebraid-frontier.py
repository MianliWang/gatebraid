"""SEEDED CONSUMER - not the landed consumer, and never invoked.

N6 reads the consumer's declared code space from the consumer's OWN module
docstring rather than from a list written into the criterion, so falsifying N6
requires a consumer whose docstring the same parser can read. This stand-in
declares the same four codes the landed consumer declares, so the seeded
collision at exit 2 is a collision with a real space and not with an invented
one.

Exit codes: 0 report emitted from a healthy snapshot - 1 the snapshot was
REFUSED and no verdict was emitted - 2 usage or input error - 3 report emitted
and every verdict is `undecidable` because the snapshot was degraded.
"""
