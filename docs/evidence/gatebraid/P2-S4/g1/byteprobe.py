"""P0-2 / BP-01 probe: what a non-UTF-8 parent console does to a child's output.

BP-01 fired on this host during this Slice's Gate 0: a child Python inheriting
the cp936 console codec mangled U+2014 into bytes that were not valid UTF-8.
P0-2 requires explicit UTF-8 binary stdout with the producer/consumer byte
contract stated and tested on non-ASCII fixtures, and this probe is what that
requirement looks like as a measurement rather than a sentence.

Two children are compared under the SAME parent console:

  text    print() through the inherited text layer -- the defect path
  bytes   sys.stdout.buffer.write(... .encode("utf-8")) -- the contract path

The probe reports the parent's codec and the exact bytes each path produced, so
"the byte contract holds" is a comparison of byte strings and not an assertion.
"""
import sys

PAYLOAD = "em dash — CJK 中文 end"

mode = sys.argv[1] if len(sys.argv) > 1 else "report"

if mode == "text":
    # The defect path: whatever codec the console handed us.
    print(PAYLOAD)
elif mode == "bytes":
    # The contract path: explicit UTF-8 bytes on binary stdout.
    sys.stdout.buffer.write(PAYLOAD.encode("utf-8") + b"\n")
    sys.stdout.buffer.flush()
else:
    print("stdout.encoding :", sys.stdout.encoding)
    print("payload         :", repr(PAYLOAD))
    print("utf-8 bytes     :", PAYLOAD.encode("utf-8").hex())
