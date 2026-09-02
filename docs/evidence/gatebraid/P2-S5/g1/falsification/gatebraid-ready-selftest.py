"""SEEDED CODE SURFACE - not the deliverable, and never imported by anything.

The second half of the seeded surface. It carries ONE defect, so that N4 is
shown firing on a file that is otherwise ordinary: a criterion that only ever
fires on a file stuffed with every defect at once has not been shown to
discriminate.
"""
import urllib.request     # N4: a stdlib network client, reported for a human read


def fetch(url):
    return urllib.request.urlopen(url).read()
