import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from scripts.validate import adoption_receipt_errors, work_object_errors

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
AGENT_DIR = ROOT / "agents"
WORK_FIXTURE_DIR = ROOT / "fixtures" / "work-object"


class SchemaTests(unittest.TestCase):
    TEST_REGISTRY = {
        "agent:expert": "github:test-executor",
        "agent:gideon": "github:test-reviewer",
        "agent:nemertes": "github:test-verifier",
    }

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
        self.assertEqual(
            work_object_errors(
                data,
                self.work_validator,
                identity_registry=self.TEST_REGISTRY,
                fixture_evidence=True,
            ),
            [],
        )

    def test_pending_and_unbound_roles_are_not_operationally_valid(self):
        data = json.loads((WORK_FIXTURE_DIR / "valid.json").read_text())
        errors = work_object_errors(data, self.work_validator, fixture_evidence=True)
        self.assertTrue(any("reviewer" in e and "verified identity" in e for e in errors))
        self.assertTrue(any("verifier" in e and "verified identity" in e for e in errors))

    def test_same_role_work_object_is_rejected(self):
        data = json.loads((WORK_FIXTURE_DIR / "invalid-same-role.json").read_text())
        errors = work_object_errors(data, self.work_validator)
        self.assertTrue(
            any("must be pairwise distinct" in error for error in errors),
            errors,
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
        data["evidence"] = []
        errors = work_object_errors(data, self.work_validator)
        self.assertTrue(any("missing evidence kinds" in error for error in errors))

    def test_unregistered_roles_cannot_satisfy_work_object(self):
        data = copy.deepcopy(json.loads((WORK_FIXTURE_DIR / "valid.json").read_text()))
        data["roles"]["reviewer"] = "agent:invented-reviewer"
        self.assertTrue(
            any("reviewer must resolve" in error for error in work_object_errors(data, self.work_validator))
        )

    def test_unbound_identity_cannot_author_evidence(self):
        data = copy.deepcopy(json.loads((WORK_FIXTURE_DIR / "valid.json").read_text()))
        data["evidence"][0]["actor"] = "agent:nemertes"
        self.assertTrue(
            any("verified agent identity" in error for error in work_object_errors(data, self.work_validator))
        )

    def test_nonexistent_or_digest_mismatched_evidence_is_rejected(self):
        data = copy.deepcopy(json.loads((WORK_FIXTURE_DIR / "valid.json").read_text()))
        data["evidence"][0]["uri"] = "conversation"
        data["evidence"][0]["sha256"] = "0" * 64
        self.assertTrue(
            any("dedicated evidence root" in error for error in work_object_errors(data, self.work_validator))
        )

    def test_readme_and_uri_suffixes_cannot_be_work_evidence(self):
        base = json.loads((WORK_FIXTURE_DIR / "valid.json").read_text())
        for uri in (
            "README.md",
            "kernel/fixtures/evidence/build.json?x=1",
            "kernel/fixtures/evidence/build.json#x",
        ):
            with self.subTest(uri=uri):
                data = copy.deepcopy(base)
                data["evidence"][0]["uri"] = uri
                self.assertTrue(
                    work_object_errors(
                        data,
                        self.work_validator,
                        identity_registry=self.TEST_REGISTRY,
                        fixture_evidence=True,
                    )
                )

    def test_invalid_git_branch_is_rejected(self):
        base = json.loads((WORK_FIXTURE_DIR / "valid.json").read_text())
        for branch in ("../main", "-bad", "foo.lock", "foo/.bar", "foo/bar.", "foo//bar", "foo..bar"):
            with self.subTest(branch=branch):
                data = copy.deepcopy(base)
                data["branch"] = branch
                self.assertTrue(list(self.work_validator.iter_errors(data)))

    def test_semantic_adversarial_work_objects_are_rejected(self):
        for path in sorted(WORK_FIXTURE_DIR.glob("invalid-*.json")):
            with self.subTest(path=path.name):
                data = json.loads(path.read_text())
                self.assertTrue(work_object_errors(data, self.work_validator))

    def test_case_alias_role_collision_is_rejected(self):
        """BK-15: an uppercase merger alias of the executor's login must not
        bypass the merger/executor separation check."""
        data = json.loads(
            (WORK_FIXTURE_DIR / "invalid-merger-case-alias-self-merge.json").read_text()
        )
        errors = work_object_errors(data, self.work_validator)
        self.assertTrue(errors)

    def test_reviewer_verifier_role_reuse_via_case_is_rejected(self):
        """BK-15: canonicalize before comparing so 'agent:X' vs 'AGENT:X' collides.

        The merger schema pattern allows mixed case, so an uppercase alias of
        the executor's resolved GitHub login is schema-valid but must still be
        rejected once identities are canonicalized -- this is the exact
        case/alias bypass the reviewer reproduced.
        """
        data = json.loads(
            (WORK_FIXTURE_DIR / "invalid-merger-case-alias-self-merge.json").read_text()
        )
        schema_only_errors = list(self.work_validator.iter_errors(data))
        self.assertEqual(schema_only_errors, [])
        errors = work_object_errors(data, self.work_validator)
        self.assertIn("merger must not resolve to the executor identity", errors)

    def test_omitted_role_identity_is_rejected(self):
        """BK-15: all four identities (incl. merger) must be present, not just executor."""
        data = copy.deepcopy(json.loads((WORK_FIXTURE_DIR / "valid.json").read_text()))
        data["roles"]["merger"] = ""
        errors = [e.message for e in self.work_validator.iter_errors(data)]
        # schema requires merger to match a github: pattern; empty string fails schema
        self.assertTrue(errors)

    def test_scope_exclude_traversal_is_rejected(self):
        """BK-16: scope.exclude entries must be normalized, not silently dropped."""
        data = json.loads(
            (WORK_FIXTURE_DIR / "invalid-malformed-excluded-path.json").read_text()
        )
        errors = work_object_errors(data, self.work_validator)
        self.assertTrue(
            any("malformed entry" in error for error in errors), errors
        )

    def test_empty_changed_paths_is_rejected(self):
        """BK-16: changed_paths must be present and non-empty."""
        data = json.loads(
            (WORK_FIXTURE_DIR / "invalid-empty-changed-paths.json").read_text()
        )
        errors = work_object_errors(data, self.work_validator)
        self.assertTrue(errors)

    def test_changed_path_traversal_is_rejected(self):
        """BK-16: a '..' traversal segment in changed_paths must not validate."""
        data = json.loads(
            (WORK_FIXTURE_DIR / "invalid-changed-path-traversal.json").read_text()
        )
        errors = work_object_errors(data, self.work_validator)
        self.assertTrue(errors)

    def test_impossible_branch_ref_is_rejected(self):
        """A Git-impossible branch such as '../main' must fail closed."""
        data = json.loads((WORK_FIXTURE_DIR / "invalid-branch-ref.json").read_text())
        schema_only_errors = list(self.work_validator.iter_errors(data))
        errors = work_object_errors(data, self.work_validator)
        self.assertTrue(errors)
        self.assertTrue(
            schema_only_errors or any("not a valid Git ref" in error for error in errors),
            errors,
        )


    def test_adoption_roles_must_be_pairwise_distinct(self):
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
                "actor": "agent:nemertes",
                "timestamp": "2026-07-21T10:00:00Z",
                "environment_digest": "2" * 64,
                "verdict": "pass",
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
                "actor": "agent:nemertes",
                "timestamp": "2026-07-21T10:00:00Z",
                "environment_digest": "2" * 64,
                "verdict": "pass",
            }],
            "evidence_maturity": "monitored",
            "rollback_verified": False,
            "claims": [],
            "deviations": [],
            "demotion_reason": "monitored evidence invalidated required claim",
        }
        self.assertEqual(list(validator.iter_errors(data)), [])

    def test_adoption_receipt_rejects_unregistered_roles(self):
        validator = Draft202012Validator(
            self.schemas["adoption-receipt.schema.json"], format_checker=FormatChecker()
        )
        data = json.loads(
            (ROOT.parent / "receipts" / "fixtures" / "valid" / "promotion.json").read_text()
        )
        data["reviewer_agent_id"] = "agent:invented-reviewer"
        self.assertTrue(
            any("reviewer must resolve" in error for error in adoption_receipt_errors(data, validator))
        )

    def test_adoption_receipt_evidence_must_resolve_and_match_digest(self):
        validator = Draft202012Validator(
            self.schemas["adoption-receipt.schema.json"], format_checker=FormatChecker()
        )
        data = json.loads(
            (ROOT.parent / "receipts" / "fixtures" / "valid" / "promotion.json").read_text()
        )
        data["evidence"][0]["uri"] = "receipts/fixtures/evidence/missing.json"
        data["evidence"][0]["sha256"] = "0" * 64
        self.assertTrue(
            any(
                "does not exist" in error
                for error in adoption_receipt_errors(
                    data,
                    validator,
                    identity_registry=self.TEST_REGISTRY,
                    fixture_evidence=True,
                )
            )
        )

    def test_rollback_receipt_requires_resulting_target_match(self):
        validator = Draft202012Validator(
            self.schemas["adoption-receipt.schema.json"], format_checker=FormatChecker()
        )
        data = json.loads(
            (ROOT.parent / "receipts" / "fixtures" / "valid" / "promotion.json").read_text()
        )
        data["event_type"] = "rollback"
        data["result"] = "rolled-back"
        data["resulting_baseline_pin"] = data["rollback_target_pin"]
        matching_errors = adoption_receipt_errors(
            data,
            validator,
            identity_registry=self.TEST_REGISTRY,
            fixture_evidence=True,
        )
        self.assertNotIn(
            "resulting_baseline_pin must equal rollback_target_pin for rollback",
            matching_errors,
        )
        data["resulting_baseline_pin"] = data["candidate_pin"]
        self.assertIn(
            "resulting_baseline_pin must equal rollback_target_pin for rollback",
            adoption_receipt_errors(
                data,
                validator,
                identity_registry=self.TEST_REGISTRY,
                fixture_evidence=True,
            ),
        )

    def test_golden_fixture_required_false_needs_only_reason(self):
        data = copy.deepcopy(json.loads((WORK_FIXTURE_DIR / "valid.json").read_text()))
        data["golden_fixture"] = {
            "required": False,
            "inapplicable_reason": "no deterministic golden fixture for this work object class",
        }
        self.assertEqual(list(self.work_validator.iter_errors(data)), [])
        bare = {"required": False}
        self.assertTrue(list(self.work_validator.iter_errors({**data, "golden_fixture": bare})))

    def test_corpus_release_handling_constraints_include_no_raw_owner_memory(self):
        enum = self.schemas["corpus-release.schema.json"]["properties"][
            "handling_constraints"
        ]["items"]["enum"]
        self.assertIn("no-raw-owner-memory", enum)

    def test_work_object_handling_constraints_include_no_raw_owner_memory(self):
        enum = self.schemas["work-object.schema.json"]["properties"][
            "handling_constraints"
        ]["items"]["enum"]
        self.assertIn("no-raw-owner-memory", enum)


if __name__ == "__main__":
    unittest.main()
