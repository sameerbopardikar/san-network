import importlib.util
import json
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
    "uri-only-evidence.json": lambda errs: any(
        "structured" in e.lower() or "uri" in e.lower() for e in errs
    ),
    "mismatched-evidence-pin.json": lambda errs: any(
        "subject_pin" in e for e in errs
    ),
}


class ReceiptTests(unittest.TestCase):
    TEST_REGISTRY = {
        "agent:expert": "github:test-executor",
        "agent:gideon": "github:test-reviewer",
        "agent:nemertes": "github:test-verifier",
    }

    def test_valid_fixture_passes(self):
        path = ROOT / "receipts" / "fixtures" / "valid" / "promotion.json"
        self.assertEqual(
            MODULE.validation_errors(
                path, identity_registry=self.TEST_REGISTRY, fixture_evidence=True
            ),
            [],
        )

    def test_checked_in_promotion_is_not_operationally_valid(self):
        path = ROOT / "receipts" / "fixtures" / "valid" / "promotion.json"
        errors = MODULE.validation_errors(path, fixture_evidence=True)
        self.assertTrue(any("verified identity" in error for error in errors))

    def test_pending_and_unbound_roles_cannot_accept_promotion(self):
        path = ROOT / "receipts" / "fixtures" / "valid" / "promotion.json"
        data = json.loads(path.read_text())
        errors = MODULE._semantic_errors(data, fixture_evidence=True)
        self.assertTrue(any("reviewer" in e and "verified identity" in e for e in errors))
        self.assertTrue(any("verifier" in e and "verified identity" in e for e in errors))

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

    def test_structured_evidence_required(self):
        path = ROOT / "receipts" / "fixtures" / "invalid" / "uri-only-evidence.json"
        errors = MODULE.validation_errors(path)
        self.assertTrue(any("structured" in error.lower() or "is not of type" in error for error in errors))

    def test_evidence_subject_pin_must_match_receipt(self):
        path = ROOT / "receipts" / "fixtures" / "invalid" / "mismatched-evidence-pin.json"
        errors = MODULE.validation_errors(path)
        self.assertTrue(any("subject_pin" in error for error in errors))

    def test_failed_benchmark_cannot_promote(self):
        path = ROOT / "receipts" / "fixtures" / "invalid" / "failed-promotion.json"
        errors = MODULE.validation_errors(path)
        self.assertTrue(any("passed benchmark" in error for error in errors))

    def test_unregistered_receipt_role_is_rejected(self):
        path = ROOT / "receipts" / "fixtures" / "valid" / "promotion.json"
        data = json.loads(path.read_text())
        data["reviewer_agent_id"] = "agent:invented-reviewer"
        self.assertTrue(
            any("reviewer must resolve" in error for error in MODULE._semantic_errors(data))
        )

    def test_receipt_evidence_pointer_must_exist_and_match_digest(self):
        path = ROOT / "receipts" / "fixtures" / "valid" / "promotion.json"
        data = json.loads(path.read_text())
        data["evidence"][0]["uri"] = "conversation"
        data["evidence"][0]["sha256"] = "0" * 64
        self.assertTrue(
            any("dedicated evidence root" in error for error in MODULE._semantic_errors(data))
        )

    def test_readme_and_uri_suffixes_cannot_be_evidence(self):
        path = ROOT / "receipts" / "fixtures" / "valid" / "promotion.json"
        base = json.loads(path.read_text())
        for uri in (
            "README.md",
            "receipts/fixtures/evidence/promotion.json?x=1",
            "receipts/fixtures/evidence/promotion.json#x",
        ):
            with self.subTest(uri=uri):
                data = json.loads(json.dumps(base))
                data["evidence"][0]["uri"] = uri
                self.assertTrue(
                    MODULE._semantic_errors(
                        data,
                        identity_registry=self.TEST_REGISTRY,
                        fixture_evidence=True,
                    )
                )

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
