#!/usr/bin/env python3
"""Validate SAN issue forms and keep routine intake fail-safe."""

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"
ROUTINE_TEMPLATE = TEMPLATE_DIR / "task.yml"
ALLOWED_ROUTINE_STATUS = "status:intake"
PREAUTHORIZED_LABEL_PREFIXES = ("authority:",)


def load_form(path: Path) -> dict:
    """Load one GitHub issue form as a mapping."""
    with path.open(encoding="utf-8") as handle:
        form = yaml.safe_load(handle)
    if not isinstance(form, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a mapping")
    return form


def labels_for(form: dict, path: Path) -> list[str]:
    """Return normalized labels from a GitHub issue form."""
    labels = form.get("labels", [])
    if isinstance(labels, str):
        labels = [labels]
    if not isinstance(labels, list) or not all(isinstance(label, str) for label in labels):
        raise ValueError(f"{path.relative_to(ROOT)} labels must be a string or list of strings")
    return labels


def validate_routine_intake(form: dict) -> None:
    """Require exactly one intake status and reject automatic authority."""
    labels = labels_for(form, ROUTINE_TEMPLATE)
    status_labels = [label for label in labels if label.startswith("status:")]
    forbidden = [
        label
        for label in labels
        if label.startswith(PREAUTHORIZED_LABEL_PREFIXES)
        or (label.startswith("status:") and label != ALLOWED_ROUTINE_STATUS)
    ]
    if forbidden:
        raise ValueError(
            "routine task intake must remain proposal-only; forbidden automatic labels: "
            + ", ".join(forbidden)
        )
    if status_labels != [ALLOWED_ROUTINE_STATUS]:
        raise ValueError(
            f"routine task intake must apply exactly one {ALLOWED_ROUTINE_STATUS} label"
        )


def main() -> int:
    """Parse all forms and enforce the routine-intake trust boundary."""
    forms = {path: load_form(path) for path in sorted(TEMPLATE_DIR.glob("*.yml"))}
    if ROUTINE_TEMPLATE not in forms:
        raise ValueError("routine task template is missing")
    validate_routine_intake(forms[ROUTINE_TEMPLATE])
    print(f"Issue forms valid: {len(forms)}; routine intake is proposal-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
