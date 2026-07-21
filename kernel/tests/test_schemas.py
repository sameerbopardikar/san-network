import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from scripts.validate import work_object_errors

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
AGENT_DIR = ROOT / "agents"
WORK_FIXTURE_DIR = ROOT / "fixtures" / "work-object"


class SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schemas = {
            path.name: json.loads(path.read_text())
            for path in SCHEMA_DIR.glob("*.schema.json")
        }
        cls.agent_schema = cls.schemas["agent-card.schema.json"]
        cls.agent_validator = Draft202012Validator(
            cls.agent_schema,
            format_checker=FormatChecker(),
        )
        cls.work_validator = Draft202012Validator(
            cls.schemas["work-object.schema.json"],
            format_checker=FormatChecker(),
        )

    def test_all_schemas_are_valid(self):
        self.assertGreaterEqual(len(self.schemas), 5)
        for schema in self.schemas.values():
            Draft202012Validator.check_schema(schema)

    def test_all_agent_cards_are_valid_and_unique(self):
        ids = []
        for path in sorted(AGENT_DIR.glob("*.json")):
            data = json.loads(path.read_text())
            self.assertEqual(list(self.agent_validator.iter_errors(data)), [])
            ids.append(data["agent_id"])
        self.assertEqual(len(ids), 4)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("agent:nemertes", ids)

    def test_verified_runtime_cannot_use_latest(self):
        data = json.loads((AGENT_DIR / "expert.json").read_text())
        data = copy.deepcopy(data)
        data["runtime"]["version"] = "latest"
        self.assertTrue(list(self.agent_validator.iter_errors(data)))

    def test_bound_runtime_cannot_use_unbound_sentinel(self):
        data = copy.deepcopy(json.loads((AGENT_DIR / "expert.json").read_text()))
        data["runtime"]["version"] = "unbound"
        self.assertTrue(list(self.agent_validator.iter_errors(data)))

    def test_pending_github_binding_requires_login(self):
        data = json.loads((AGENT_DIR / "gideon.json").read_text())
        data = copy.deepcopy(data)
        data["github_identity"]["login"] = None
        self.assertTrue(list(self.agent_validator.iter_errors(data)))

    def test_bound_github_identity_cannot_use_unbound_binding_type(self):
        data = copy.deepcopy(json.loads((AGENT_DIR / "gideon.json").read_text()))
        data["github_identity"]["binding_type"] = "unbound"
        self.assertTrue(list(self.agent_validator.iter_errors(data)))

    def test_valid_work_object_passes_cross_field_validation(self):
        data = json.loads((WORK_FIXTURE_DIR / "valid.json").read_text())
        self.assertEqual(work_object_errors(data, self.work_validator), [])

    def test_same_role_work_object_is_rejected(self):
        data = json.loads((WORK_FIXTURE_DIR / "invalid-same-role.json").read_text())
        self.assertIn(
            "executor, reviewer, and verifier must be pairwise distinct",
            work_object_errors(data, self.work_validator),
        )


    def test_self_merge_is_rejected(self):
        data = json.loads((WORK_FIXTURE_DIR / "invalid-self-merge.json").read_text())
        self.assertIn(
            "merger must not resolve to the executor identity",
            work_object_errors(data, self.work_validator),
        )

    def test_stale_head_evidence_is_rejected(self):
        data = json.loads(
            (WORK_FIXTURE_DIR / "invalid-stale-evidence.json").read_text()
        )
        self.assertIn(
            "all evidence must bind the current subject_sha",
            work_object_errors(data, self.work_validator),
        )

    def test_maturity_cannot_advance_without_required_evidence(self):
        data = json.loads((WORK_FIXTURE_DIR / "valid.json").read_text())
        data = copy.deepcopy(data)
        data["evidence"] = [
            item for item in data["evidence"] if item["kind"] != "independent-review"
        ]
        errors = work_object_errors(data, self.work_validator)
        self.assertTrue(any("missing evidence kinds" in error for error in errors))

    def test_semantic_adversarial_work_objects_are_rejected(self):
        for path in sorted(WORK_FIXTURE_DIR.glob("invalid-*.json")):
            with self.subTest(path=path.name):
                data = json.loads(path.read_text())
                self.assertTrue(work_object_errors(data, self.work_validator))


    def test_adoption_roles_must_be_pairwise_distinct(self):
        from scripts.validate import adoption_receipt_errors

        schema = self.schemas["adoption-receipt.schema.json"]
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        pin = {"kind": "git-commit", "value": "a" * 40}
        base = {
            "schema_version": 1,
            "receipt_id": "receipt:test-adopt",
            "event_type": "adopt",
            "subject_id": "bootstrap-agent-from-kernel",
            "subject_pin": pin,
            "destination_agent_id": "agent:gideon",
            "executor_agent_id": "agent:expert",
            "reviewer_agent_id": "agent:expert",
            "verifier_agent_id": "agent:nemertes",
            "benchmark_id": "bench-a",
            "benchmark_version": "1.0.0",
            "benchmark_result": "passed",
            "threshold": "all green",
            "observed_result": "all green",
            "previous_baseline_pin": {"kind": "none", "value": "none"},
            "candidate_pin": pin,
            "resulting_baseline_pin": pin,
            "rollback_target_pin": {"kind": "none", "value": "none"},
            "result": "accepted",
            "tested_at": "2026-07-21T10:00:00Z",
            "evidence": [{
                "uri": "receipts/example.json",
                "sha256": "7f227db1653b6b723b07c8f2f6eb488f1f09e2f083ca7a3f5e02bbb274f5ff2e",
                "subject_pin": pin,
            }],
            "evidence_maturity": "sandbox-tested",
            "rollback_verified": True,
            "claims": ["installed"],
            "deviations": [],
        }
        errors = adoption_receipt_errors(base, validator)
        self.assertIn(
            "executor, reviewer, and verifier must be pairwise distinct",
            errors,
        )

    def test_demote_allows_explicit_none_baseline(self):
        schema = self.schemas["adoption-receipt.schema.json"]
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        pin = {"kind": "git-commit", "value": "b" * 40}
        data = {
            "schema_version": 1,
            "receipt_id": "receipt:test-demote",
            "event_type": "demote",
            "subject_id": "bootstrap-agent-from-kernel",
            "subject_pin": pin,
            "destination_agent_id": "agent:gideon",
            "executor_agent_id": "agent:expert",
            "reviewer_agent_id": "agent:gideon",
            "verifier_agent_id": "agent:nemertes",
            "benchmark_id": "bench-a",
            "benchmark_version": "1.0.0",
            "benchmark_result": "failed",
            "threshold": "all green",
            "observed_result": "regressed",
            "previous_baseline_pin": pin,
            "candidate_pin": pin,
            "resulting_baseline_pin": {"kind": "none", "value": "none"},
            "rollback_target_pin": {"kind": "none", "value": "none"},
            "result": "rolled-back",
            "tested_at": "2026-07-21T10:00:00Z",
            "evidence": [{
                "uri": "receipts/example.json",
                "sha256": "7f227db1653b6b723b07c8f2f6eb488f1f09e2f083ca7a3f5e02bbb274f5ff2e",
                "subject_pin": pin,
            }],
            "evidence_maturity": "monitored",
            "rollback_verified": False,
            "claims": [],
            "deviations": [],
            "demotion_reason": "monitored evidence invalidated required claim",
        }
        self.assertEqual(list(validator.iter_errors(data)), [])


if __name__ == "__main__":
    unittest.main()
