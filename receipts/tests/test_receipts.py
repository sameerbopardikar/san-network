import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "receipts" / "scripts" / "validate_receipts.py"
SPEC = importlib.util.spec_from_file_location("validate_receipts", SCRIPT)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

# Expected failure predicates for semantic adversarial fixtures.
ADVERSARIAL_EXPECTATIONS = {
    "failed-promotion.json": lambda errs: any("passed benchmark" in e for e in errs),
    "same-role.json": lambda errs: any(
        "pairwise" in e.lower() or "same" in e.lower() or "distinct" in e.lower() or "role" in e.lower()
        for e in errs
    ),
    "malformed-json.json": lambda errs: bool(errs),
    "malformed-array.json": lambda errs: bool(errs),
}


class ReceiptTests(unittest.TestCase):
    def test_valid_fixture_passes(self):
        path = ROOT / "receipts" / "fixtures" / "valid" / "promotion.json"
        self.assertEqual(MODULE.validation_errors(path), [])

    def test_all_adversarial_fixtures_fail(self):
        invalid_dir = ROOT / "receipts" / "fixtures" / "invalid"
        for path in sorted(invalid_dir.glob("*.json")):
            with self.subTest(path=path.name):
                errors = MODULE.validation_errors(path)
                self.assertTrue(errors, msg=f"expected errors for {path.name}")
                pred = ADVERSARIAL_EXPECTATIONS.get(path.name)
                if pred is not None:
                    self.assertTrue(
                        pred(errors),
                        msg=f"{path.name} failed for unexpected reasons: {errors}",
                    )

    def test_failed_benchmark_cannot_promote(self):
        path = ROOT / "receipts" / "fixtures" / "invalid" / "failed-promotion.json"
        errors = MODULE.validation_errors(path)
        self.assertTrue(any("passed benchmark" in error for error in errors))

    def test_non_json_operational_artifact_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            fake_root = Path(td)
            stray = fake_root / "receipts" / "gate1" / "_tmp_fail_closed_probe.md"
            previous_root = MODULE.ROOT
            MODULE.ROOT = fake_root
            try:
                stray.parent.mkdir(parents=True, exist_ok=True)
                stray.write_text("probe\n")
                with self.assertRaises(SystemExit) as ctx:
                    MODULE._operational_receipts()
                self.assertIn("unsupported non-JSON", str(ctx.exception))
            finally:
                MODULE.ROOT = previous_root
                if stray.exists():
                    stray.unlink()


if __name__ == "__main__":
    unittest.main()
