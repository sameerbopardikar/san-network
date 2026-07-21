#!/usr/bin/env python3
import json
from pathlib import Path
try:
    from jsonschema import Draft202012Validator
except ImportError as exc:
    raise SystemExit("Install development requirements: pip install -r requirements-dev.txt") from exc
root=Path(__file__).resolve().parents[1]
failed=False
for path in sorted((root/'schemas').glob('*.schema.json')):
    data=json.loads(path.read_text())
    Draft202012Validator.check_schema(data)
    print(f"valid schema: {path.relative_to(root)}")
raise SystemExit(1 if failed else 0)
