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

    def test_all_adversarial_fixtures_fail(self):
        invalid_dir = ROOT / "receipts" / "fixtures" / "invalid"
        for path in sorted(invalid_dir.glob("*.json")):
            with self.subTest(path=path.name):
                self.assertTrue(MODULE.validation_errors(path))

    def test_failed_benchmark_cannot_promote(self):
        path = ROOT / "receipts" / "fixtures" / "invalid" / "failed-promotion.json"
        errors = MODULE.validation_errors(path)
        self.assertTrue(any("passed benchmark" in error for error in errors))



    def test_non_json_operational_artifact_fails_closed(self):
        import tempfile, os, subprocess, sys
        with tempfile.TemporaryDirectory() as td:
            # run validator against a fake tree is hard; instead call helper after monkeypatch
            root = ROOT / "receipts"
            stray = root / "gate1" / "_tmp_fail_closed_probe.md"
            try:
                stray.parent.mkdir(parents=True, exist_ok=True)
                stray.write_text("probe\n")
                with self.assertRaises(SystemExit) as ctx:
                    MODULE._operational_receipts()
                self.assertIn("unsupported non-JSON", str(ctx.exception))
            finally:
                if stray.exists():
                    stray.unlink()

if __name__ == "__main__":
    unittest.main()
