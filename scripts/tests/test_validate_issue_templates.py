import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_issue_templates import (  # noqa: E402
    ROUTINE_TEMPLATE,
    load_form,
    validate_routine_intake,
)


class DuplicateKeyRejectionTests(unittest.TestCase):
    """Hostile fixture: a duplicate mapping key must fail closed, not silently
    resolve to the last value. This is the exact class of trust-boundary bug
    CodeRabbit flagged: yaml.safe_load() previously accepted repeated
    ``labels:`` keys, which could let a hidden second block smuggle a
    forbidden status/authority label past a reviewer skimming the diff."""

    def _write(self, tmp_path: Path, text: str) -> Path:
        target = tmp_path / "hostile.yml"
        target.write_text(text, encoding="utf-8")
        return target

    def test_duplicate_top_level_key_is_rejected(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(
                Path(tmp),
                "name: Task\n"
                "labels: [status:intake]\n"
                "labels: [status:intake, authority:A]\n",
            )
            with self.assertRaisesRegex(ValueError, "duplicate mapping key"):
                load_form(path)

    def test_non_duplicate_form_still_loads(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(
                Path(tmp), "name: Task\nlabels: [status:intake]\n"
            )
            form = load_form(path)
            self.assertEqual(form["labels"], ["status:intake"])

    def test_checked_in_forms_have_no_duplicate_keys(self):
        # Regression guard: every real template in the repo must still load
        # cleanly under the stricter loader (no false positives).
        template_dir = ROUTINE_TEMPLATE.parent
        for path in sorted(template_dir.glob("*.yml")):
            with self.subTest(path=path.name):
                load_form(path)


class RoutineIntakeTests(unittest.TestCase):
    def setUp(self):
        self.form = load_form(ROUTINE_TEMPLATE)

    def test_checked_in_form_is_proposal_only(self):
        validate_routine_intake(self.form)

    def test_rejects_any_additional_status_label(self):
        for hostile_status in ("status:ready", "status:executing", "status:review"):
            with self.subTest(hostile_status=hostile_status):
                form = copy.deepcopy(self.form)
                form["labels"].append(hostile_status)
                with self.assertRaisesRegex(ValueError, "forbidden automatic labels"):
                    validate_routine_intake(form)

    def test_rejects_duplicate_or_missing_intake_status(self):
        for labels in ([], ["status:intake", "status:intake"]):
            with self.subTest(labels=labels):
                form = copy.deepcopy(self.form)
                form["labels"] = labels
                with self.assertRaisesRegex(ValueError, "exactly one status:intake"):
                    validate_routine_intake(form)

    def test_rejects_any_authority_label(self):
        form = copy.deepcopy(self.form)
        form["labels"].append("authority:A")
        with self.assertRaisesRegex(ValueError, "forbidden automatic labels"):
            validate_routine_intake(form)


if __name__ == "__main__":
    unittest.main()
