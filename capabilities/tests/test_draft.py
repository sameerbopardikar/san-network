import copy
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


class DraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text())
        cls.manifest = json.loads(MANIFEST_PATH.read_text())
        cls.validator = Draft202012Validator(
            cls.schema,
            format_checker=FormatChecker(),
        )

    def errors(self, data):
        return list(self.validator.iter_errors(data))

    def test_checked_in_draft_matches_schema(self):
        self.assertEqual(self.errors(self.manifest), [])
        self.assertEqual(self.manifest["status"], "planned-not-released")
        self.assertIn("not adopted", self.manifest["explicit_non_claims"])

    def test_latest_kernel_pin_is_rejected(self):
        data = copy.deepcopy(self.manifest)
        data["kernel_pin"] = {"kind": "release", "value": "latest"}
        self.assertTrue(self.errors(data))

    def test_released_manifest_requires_artifacts(self):
        data = copy.deepcopy(self.manifest)
        data["status"] = "released"
        data.pop("artifacts", None)
        self.assertTrue(self.errors(data))

    def test_released_manifest_rejects_missing_kernel_and_forged_maturity(self):
        data = copy.deepcopy(self.manifest)
        data["status"] = "released"
        data["kernel_pin"] = {"kind": "none", "value": "none"}
        data["evidence_maturity"] = "outcome-calibrated"
        data["artifacts"] = [{"path": "payload.txt", "sha256": "0" * 64}]
        data["evidence"] = []
        self.assertTrue(self.errors(data))

    def test_evidence_maturity_requires_matching_evidence_kind(self):
        data = copy.deepcopy(self.manifest)
        data["evidence_maturity"] = "task-proven"
        data["evidence"] = [
            {
                "kind": "installed",
                "uri": "receipts/install.json",
                "sha256": "1" * 64,
            }
        ]
        self.assertTrue(self.errors(data))

    def test_cross_plane_artifact_path_is_rejected(self):
        data = copy.deepcopy(self.manifest)
        data["status"] = "released"
        data["artifacts"] = [
            {
                "path": "../../kernel/README.md",
                "sha256": "0" * 64,
            }
        ]
        self.assertTrue(self.errors(data))


if __name__ == "__main__":
    unittest.main()
