"""SEEDED CODE SURFACE - not the deliverable, and never imported by anything.

Hand-written so that criteria N4, N5 and N6 can be shown ABLE TO FIRE against
the SAME instrument rather than against a copy of it. A criterion that has only
ever held has never been falsified (spec section 4, friction #111).

Each defect below is deliberate and is the exact shape its criterion proxies for:

  N4  a non-stdlib network client is imported.
  N5  a GraphQL document opens a mutation, and a file is opened for writing.
  N6  an exit constant is declared INSIDE the consumer's declared code space,
      and one of the frozen scope's own two codes is missing.
"""
import json
import requests            # N4: a real network client, outside the stdlib

# N6: 2 collides with the consumer's declared space, and 11 is absent, so both
# halves of the criterion have something to find.
EXIT_OK = 0
EXIT_PRODUCER_FAILED = 10
EXIT_WRONG = 2

MUTATE = "mutation { updateProjectV2ItemFieldValue(input: {}) { clientMutationId } }"


def sneaky_write(path, payload):
    # N5 file-local: an open() in a write mode inside the tool itself.
    fh = open(path, "w", encoding="utf-8")
    fh.write(json.dumps(payload))
    fh.close()


def sneaky_mutate(token):
    # N5 file-local: the document above actually leaves the process.
    return requests.post("https://api.github.com/graphql",
                         json={"query": MUTATE},
                         headers={"Authorization": "bearer " + token})
