import copy
import importlib.util
import json
import subprocess
import tempfile
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
RELEASE = ROOT / "agentic-engineering" / "releases" / "v0.1.0"
SCRIPT = ROOT / "scripts" / "verify_release.py"
SPEC = importlib.util.spec_from_file_location("verify_release", SCRIPT)
assert SPEC is not None
assert SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((RELEASE / "manifest.json").read_text())
        cls.schema = json.loads(
            (REPO_ROOT / "kernel" / "schemas" / "corpus-release.schema.json").read_text()
        )

    def schema_errors(self, data):
        validator = Draft202012Validator(self.schema)
        return list(validator.iter_errors(data))

    def test_agentic_engineering_v010(self):
        with tempfile.TemporaryDirectory() as cwd:
            subprocess.run([sys.executable, str(SCRIPT)], cwd=cwd, check=True)

    def test_missing_artifact_rights_is_rejected(self):
        data = copy.deepcopy(self.manifest)
        del data["artifacts"][0]["rights_basis"]
        self.assertTrue(self.schema_errors(data))

    def test_latest_release_version_is_rejected(self):
        data = copy.deepcopy(self.manifest)
        data["version"] = "latest"
        self.assertTrue(self.schema_errors(data))

    def test_path_traversal_is_rejected(self):
        data = copy.deepcopy(self.manifest)
        data["artifacts"][0]["path"] = "../../kernel/README.md"
        self.assertTrue(self.schema_errors(data))

    def test_unknown_source_id_is_rejected(self):
        data = copy.deepcopy(self.manifest)
        data["artifacts"][0]["source_ids"] = ["unknown-source"]
        sources = MODULE.load_provenance(RELEASE / "provenance.ndjson")
        with self.assertRaisesRegex(ValueError, "unknown source IDs"):
            MODULE.validate_source_bindings(data, sources)

    def test_duplicate_artifact_path_is_rejected(self):
        data = copy.deepcopy(self.manifest)
        data["artifacts"].append(copy.deepcopy(data["artifacts"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate artifact paths"):
            MODULE.validate_manifest(data, self.schema)


    def test_unresolved_relation_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            release = Path(tmp) / "rel"
            # minimal md with bad relation
            release.mkdir()
            md = release / "concepts"
            md.mkdir()
            body = "---\nrelations:\n  - type: related\n    target: concepts/does-not-exist\n---\n\n# X\n"
            (md / "x.md").write_text(body)
            with self.assertRaisesRegex(ValueError, "unresolved relation target"):
                MODULE.validate_links(release, {"concepts/x.md"})

    def test_source_card_metadata_mismatch_is_rejected(self):
        data = copy.deepcopy(self.manifest)
        sources = MODULE.load_provenance(RELEASE / "provenance.ndjson")
        sid = data["artifacts"][0]["source_ids"][0]
        card = dict(sources[sid])
        card["url"] = "https://example.invalid/drift"
        data["artifacts"][0]["source_cards"] = [card]
        with self.assertRaisesRegex(ValueError, "source card metadata mismatch"):
            MODULE.validate_source_bindings(data, sources)

    def test_relation_parent_traversal_is_rejected(self):
        self.assertFalse(
            MODULE._resolve_relation_target("../provenance.ndjson", {"provenance.ndjson"})
        )
        self.assertFalse(
            MODULE._resolve_relation_target(
                "concepts/../sources/x.md", {"sources/x.md", "concepts/x.md"}
            )
        )

    def test_source_card_must_be_in_artifact_source_ids(self):
        data = copy.deepcopy(self.manifest)
        sources = MODULE.load_provenance(RELEASE / "provenance.ndjson")
        # force a known source off the artifact's declared list, then attach its card
        declared = list(data["artifacts"][0]["source_ids"])
        self.assertGreaterEqual(len(declared), 1)
        other = declared[-1]
        data["artifacts"][0]["source_ids"] = declared[:-1] or declared[:0]
        if not data["artifacts"][0]["source_ids"]:
            # keep schema/path valid: leave one declared id, use another source as card
            data["artifacts"][0]["source_ids"] = declared[:1]
            other = next(sid for sid in sources if sid != declared[0])
        card = dict(sources[other])
        data["artifacts"][0]["source_cards"] = [card]
        with self.assertRaisesRegex(ValueError, "not declared in artifact source_ids"):
            MODULE.validate_source_bindings(data, sources)

    def test_source_card_revision_url_mismatch_is_rejected(self):
        data = copy.deepcopy(self.manifest)
        sources = MODULE.load_provenance(RELEASE / "provenance.ndjson")
        sid = data["artifacts"][0]["source_ids"][0]
        card = dict(sources[sid])
        card["revision_url"] = "https://example.invalid/wrong-revision"
        data["artifacts"][0]["source_cards"] = [card]
        with self.assertRaisesRegex(ValueError, "source card metadata mismatch"):
            MODULE.validate_source_bindings(data, sources)

    def test_released_at_offset_comparison_uses_instants(self):
        # 05:00-01:00 == 06:00Z; must not sort as strings
        earlier = MODULE._parse_iso_utc("2026-07-21T05:00:00-01:00")
        later = MODULE._parse_iso_utc("2026-07-21T06:00:00Z")
        self.assertEqual(earlier, later)
        self.assertLess(
            MODULE._parse_iso_utc("2026-07-21T05:59:59Z"),
            MODULE._parse_iso_utc("2026-07-21T06:00:00+00:00"),
        )

    def test_latest_retrieval_selects_by_utc_instant_not_lexical(self):
        # Lexically 05:00:00-01:00 < 05:30:00Z, but as UTC instants 06:00Z > 05:30Z.
        candidates = [
            ("a", MODULE._parse_iso_utc("2026-07-21T05:30:00Z")),
            ("b", MODULE._parse_iso_utc("2026-07-21T05:00:00-01:00")),
        ]
        latest_id, _ = max(candidates, key=lambda item: item[1])
        self.assertEqual(latest_id, "b")
        lexical = max(
            ["2026-07-21T05:30:00Z", "2026-07-21T05:00:00-01:00"]
        )
        self.assertEqual(lexical, "2026-07-21T05:30:00Z")


if __name__ == "__main__":
    unittest.main()
