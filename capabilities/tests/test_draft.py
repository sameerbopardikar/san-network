import copy
import importlib.util
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]
CAPABILITY_ROOT = ROOT / "capabilities"
SCHEMA_PATH = ROOT / "kernel" / "schemas" / "capability-manifest.schema.json"
MANIFEST_PATH = (
    CAPABILITY_ROOT / "skills" / "bootstrap-agent-from-kernel" / "manifest.draft.json"
)
SCRIPT = CAPABILITY_ROOT / "scripts" / "validate_manifests.py"
SPEC = importlib.util.spec_from_file_location("validate_manifests", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
SEMANTIC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SEMANTIC)


class DraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text())
        cls.manifest = json.loads(MANIFEST_PATH.read_text())
        cls.validator = Draft202012Validator(
            cls.schema,
            format_checker=FormatChecker(),
        )

    def errors(self, data):
        return list(self.validator.iter_errors(data))

    def assert_error_mentions(self, data, *needles: str):
        messages = " | ".join(error.message for error in self.errors(data)).lower()
        self.assertTrue(self.errors(data), msg="expected schema errors")
        for needle in needles:
            self.assertIn(needle.lower(), messages)

    def test_checked_in_draft_matches_schema(self):
        self.assertEqual(self.errors(self.manifest), [])
        self.assertEqual(self.manifest["status"], "planned-not-released")
        self.assertIn("not adopted", self.manifest["explicit_non_claims"])

    def test_latest_kernel_pin_is_rejected(self):
        data = copy.deepcopy(self.manifest)
        # valid pin kind; floating value "latest" must fail value pattern
        data["kernel_pin"] = {"kind": "git-commit", "value": "latest"}
        self.assert_error_mentions(data, "does not match")

    def test_released_manifest_requires_artifacts(self):
        data = copy.deepcopy(self.manifest)
        data["status"] = "released"
        data.pop("artifacts", None)
        messages = " | ".join(error.message for error in self.errors(data)).lower()
        self.assertTrue(
            "artifacts" in messages or "required" in messages,
            msg=messages,
        )

    def test_released_manifest_rejects_missing_kernel_and_forged_maturity(self):
        data = copy.deepcopy(self.manifest)
        data["status"] = "released"
        data["kernel_pin"] = {"kind": "none", "value": "none"}
        data["evidence_maturity"] = "outcome-calibrated"
        data["artifacts"] = [{"path": "payload.txt", "sha256": "0" * 64}]
        data["evidence"] = []
        # forged maturity + missing kernel pin produce concrete schema messages
        self.assert_error_mentions(data, "git-commit", "non-empty")

    def test_evidence_maturity_requires_matching_evidence_kind(self):
        data = copy.deepcopy(self.manifest)
        data["evidence_maturity"] = "task-proven"
        data["evidence"] = [
            {
                "kind": "installed",
                "uri": "receipts/install.json",
                "sha256": "1" * 64,
                "actor": "agent:expert",
                "timestamp": "2026-07-21T10:00:00Z",
                "environment_digest": "2" * 64,
                "verdict": "pass",
            }
        ]
        # mismatched evidence kind is rejected by contains-items schema
        self.assert_error_mentions(data, "does not contain items matching")

    def test_evidence_maturity_requires_every_prior_tier(self):
        data = copy.deepcopy(self.manifest)
        data["evidence_maturity"] = "outcome-calibrated"
        data["evidence"] = [
            {
                "kind": "outcome-calibrated",
                "uri": "receipts/outcome.json",
                "sha256": "1" * 64,
                "actor": "agent:expert",
                "timestamp": "2026-07-21T10:00:00Z",
                "environment_digest": "2" * 64,
                "verdict": "pass",
            }
        ]
        self.assert_error_mentions(data, "does not contain items matching")

    def test_deprecated_manifest_requires_verified_rollback(self):
        data = copy.deepcopy(self.manifest)
        data["status"] = "deprecated"
        data["rollback"]["verified"] = False
        self.assert_error_mentions(data, "true")

    def test_released_manifest_requires_verified_non_none_rollback(self):
        data = copy.deepcopy(self.manifest)
        data["status"] = "released"
        data["artifacts"] = [{"path": "payload.txt", "sha256": "0" * 64}]
        data["evidence"] = [{
            "kind": "installed",
            "uri": "capabilities/fixtures/evidence/installed.json",
            "sha256": "0" * 64,
            "actor": "agent:expert",
            "timestamp": "2026-07-21T10:00:00Z",
            "environment_digest": "2" * 64,
            "verdict": "pass",
        }]
        self.assert_error_mentions(data, "true", "none")

    def test_forged_outcome_calibrated_evidence_is_semantically_rejected(self):
        data = copy.deepcopy(self.manifest)
        data["evidence_maturity"] = "outcome-calibrated"
        data["evidence"] = [
            {
                "kind": kind,
                "uri": "README.md",
                "sha256": "0" * 64,
                "actor": "agent:invented-reviewer",
                "timestamp": "2026-07-21T10:00:00Z",
                "environment_digest": "2" * 64,
                "verdict": "pass",
            }
            for kind in ("installed", "sandbox-tested", "task-proven", "monitored", "outcome-calibrated")
        ]
        errors = SEMANTIC.capability_manifest_errors(data)
        self.assertTrue(any("verified actor" in e for e in errors))
        self.assertTrue(any("dedicated evidence root" in e for e in errors))

    def test_capability_evidence_rejects_query_and_fragment(self):
        data = copy.deepcopy(self.manifest)
        data["evidence_maturity"] = "installed"
        for suffix in ("?x=1", "#x"):
            data["evidence"] = [{
                "kind": "installed",
                "uri": "capabilities/fixtures/evidence/installed.json" + suffix,
                "sha256": "0" * 64,
                "actor": "agent:expert",
                "timestamp": "2026-07-21T10:00:00Z",
                "environment_digest": "2" * 64,
                "verdict": "pass",
            }]
            self.assertTrue(any("query or fragment" in e for e in SEMANTIC.capability_manifest_errors(data, fixture_evidence=True)))

    def test_evidence_requires_environment_digest(self):
        data = copy.deepcopy(self.manifest)
        data["evidence_maturity"] = "sandbox-tested"
        data["evidence"] = [
            {
                "kind": "sandbox-tested",
                "uri": "receipts/sandbox.json",
                "sha256": "3" * 64,
                "actor": "agent:expert",
                "timestamp": "2026-07-21T10:00:00Z",
                "verdict": "pass",
            }
        ]
        self.assert_error_mentions(data, "environment_digest")

    def test_cross_plane_artifact_path_is_rejected(self):
        data = copy.deepcopy(self.manifest)
        data["status"] = "released"
        data["artifacts"] = [
            {
                "path": "../../kernel/README.md",
                "sha256": "0" * 64,
            }
        ]
        # Ensure the failure targets the artifact path, not only released-status noise.
        path_errors = [
            err for err in self.errors(data)
            if "path" in (err.json_path or "")
            or "path" in err.message.lower()
            or any("path" in str(p).lower() for p in (err.path or ()))
        ]
        self.assertTrue(
            path_errors,
            msg="expected path-targeted rejection for cross-plane artifact path",
        )

    def test_released_manifest_requires_no_raw_owner_memory_constraint(self):
        data = copy.deepcopy(self.manifest)
        data["status"] = "released"
        data["artifacts"] = [{"path": "payload.txt", "sha256": "0" * 64}]
        data["handling_constraints"] = [
            c for c in data.get("handling_constraints", []) if c != "no-raw-owner-memory"
        ]
        self.assertIn(
            "no-raw-owner-memory",
            self.schema["properties"]["handling_constraints"]["items"]["enum"],
        )
        self.assertNotIn("no-raw-owner-memory", data["handling_constraints"])
        self.assertTrue(
            self.errors(data),
            msg="released manifest without no-raw-owner-memory must be rejected",
        )


if __name__ == "__main__":
    unittest.main()
