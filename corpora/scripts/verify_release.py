#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path
release=Path(sys.argv[1] if len(sys.argv)>1 else 'agentic-engineering/releases/v0.1.0').resolve()
data=json.loads((release/'manifest.json').read_text())
expected={x['path']:x['sha256'] for x in data['artifacts']}
actual={}
for p in sorted(release.rglob('*')):
    if p.is_file() and p.name!='manifest.json': actual[str(p.relative_to(release))]=hashlib.sha256(p.read_bytes()).hexdigest()
if actual != expected:
    missing=sorted(set(expected)-set(actual)); extra=sorted(set(actual)-set(expected)); changed=sorted(k for k in set(actual)&set(expected) if actual[k]!=expected[k])
    raise SystemExit(f'release mismatch missing={missing} extra={extra} changed={changed}')
print(f'verified {data["corpus_id"]}@{data["version"]}: {len(actual)} artifacts')
