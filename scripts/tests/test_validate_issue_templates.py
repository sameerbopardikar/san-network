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
