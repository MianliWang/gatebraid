import json,re,subprocess,hashlib,sys
import yaml, importlib.metadata as md
from jsonschema import Draft202012Validator
body=subprocess.run(["gh","api","repos/MianliWang/gatebraid/issues/10","--jq",".body"],
                    capture_output=True,text=True,encoding="utf-8").stdout
m=re.search(r'^## gatebraid-metadata\s*$',body,re.M)
meta=yaml.safe_load(re.findall(r'```yaml\n(.*?)```',body[m.end():],re.S)[0])
schema=json.load(open('schema/slice.schema.json',encoding='utf-8'))
errs=list(Draft202012Validator(schema).iter_errors(meta))
h=hashlib.sha256(('\n'.join(sorted(x.strip() for x in meta['write_domains']))+'\n').encode('utf-8')).hexdigest()
print("loader                     : PyYAML %s / jsonschema %s / Draft202012Validator"%(yaml.__version__,md.version('jsonschema')))
print("live write_domains         : %s"%meta['write_domains'])
print("slice@1 validation errors  : %d"%len(errs))
print("allowlist_hash from the issue: %s"%h)
print("frozen allowlist_hash        : 0c0090ec87b5a47838edfe8bad7d8350a79d50fc642c3e1d10b1582a09223d86")
print("BYTE-EQUAL TO THE FROZEN ALLOWLIST: %s"%(h=="0c0090ec87b5a47838edfe8bad7d8350a79d50fc642c3e1d10b1582a09223d86"))
