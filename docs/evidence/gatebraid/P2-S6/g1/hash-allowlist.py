"""allowlist_hash, per gate-1-contract action 6, Python 3 standard library only.

Recipe, verbatim: each `write_domains` entry stripped of surrounding whitespace,
sorted by byte value, joined with "\n", one trailing "\n". SHA-256, lowercase
hex, over UTF-8 bytes (ADR-0011 section 3).
"""
import hashlib

WRITE_DOMAINS = ["bin/", "docs/evidence/gatebraid/P2-S6/"]

entries = [e.strip() for e in WRITE_DOMAINS]
entries.sort(key=lambda s: s.encode("utf-8"))
payload = ("\n".join(entries) + "\n").encode("utf-8")

print("entries (sorted by byte value):")
for e in entries:
    print("   %r" % e)
print("payload bytes : %r" % payload)
print("payload length: %d" % len(payload))
print("allowlist_hash: %s" % hashlib.sha256(payload).hexdigest())
