"""SEEDED TRANSITIVE TARGET - not the landed producer, and never invoked.

N5's transitive limb exists because a file-local check alone is unsound: the
default --snapshot-command target is a grandchild process, and a mutation there
is a mutation the composer caused. This seeded stand-in carries one so the limb
can be shown able to fire.

N6 also reads this file, because the composer's own codes must sit outside the
PRODUCER's declared space as well as the consumer's. The paragraph below
therefore declares the same four codes the landed producer declares, so the
seeded collision is a collision with a real space and not with an invented one.

Exit codes: 0 snapshot emitted, every source `ok` and complete - 1 no document
could be produced (self-validation failed) - 2 usage or input error - 3
snapshot emitted and DEGRADED.
"""

QUERY = "query { node(id: \"x\") { id } }"

# N5 transitive: a GraphQL document that opens a mutation, in the file the
# default --snapshot-command names.
MUTATE = "mutation SetField { updateProjectV2ItemFieldValue(input: {}) { __typename } }"
