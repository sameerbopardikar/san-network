import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "receipts" / "scripts" / "validate_receipts.py"
SPEC = importlib.util.spec_from_file_location("validate_receipts", SCRIPT)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReceiptTests(unittest.TestCase):
    def test_valid_fixture_passes(self):
        path = ROOT / "receipts" / "fixtures" / "valid" / "promotion.json"
        self.assertEqual(MODULE.validation_errors(path), [])

    def test_same_role_fixture_fails(self):
        path = ROOT / "receipts" / "fixtures" / "invalid" / "same-role.json"
        errors = MODULE.validation_errors(path)
        self.assertIn(
            "executor, reviewer, and verifier must be pairwise distinct",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
