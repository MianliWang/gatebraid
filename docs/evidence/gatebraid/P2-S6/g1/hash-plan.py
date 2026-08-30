"""plan_hash, per gate-1-contract action 6, Python 3 standard library only.

Recipe, verbatim: the lines of gate1.md strictly between the
`## Plan (frozen at exit)` heading and the next line beginning with `## `, each
stripped of trailing whitespace, leading and trailing blank lines removed,
joined with "\n", one trailing "\n". SHA-256, lowercase hex, over UTF-8 bytes.
"""
import hashlib, sys

HEADING = "## Plan (frozen at exit)"
path = sys.argv[1]
lines = open(path, encoding="utf-8").read().split("\n")

start = None
for i, l in enumerate(lines):
    if l == HEADING:
        start = i + 1
        break
if start is None:
    print("STRUCTURE: heading not found verbatim: %r" % HEADING)
    sys.exit(2)

end = None
for j in range(start, len(lines)):
    if lines[j].startswith("## "):
        end = j
        break
if end is None:
    print("STRUCTURE: no following '## ' line")
    sys.exit(2)

section = [l.rstrip() for l in lines[start:end]]
while section and not section[0]:
    section.pop(0)
while section and not section[-1]:
    section.pop()
payload = ("\n".join(section) + "\n").encode("utf-8")

print("record        : %s" % path)
print("heading at    : line %d (1-based)" % start)
print("next '## ' at : line %d (1-based)" % (end + 1))
print("plan lines    : %d after stripping and trimming" % len(section))
print("payload length: %d" % len(payload))
print("plan_hash     : %s" % hashlib.sha256(payload).hexdigest())
