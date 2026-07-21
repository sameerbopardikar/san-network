import json, unittest
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
class SchemaTests(unittest.TestCase):
    def test_all_schemas_are_valid(self):
        paths=list((ROOT/'schemas').glob('*.schema.json'))
        self.assertGreaterEqual(len(paths),4)
        for path in paths:
            Draft202012Validator.check_schema(json.loads(path.read_text()))
if __name__ == '__main__': unittest.main()
