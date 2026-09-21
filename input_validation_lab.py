"""Demonstrate unsafe form handling and a server-side validation patch."""

from __future__ import annotations

from datetime import date
import re
from typing import Any


EXPECTED_FIELDS = {"name", "date_of_birth", "email"}
MAX_NAME_LENGTH = 100
MAX_DATE_LENGTH = 10
MAX_EMAIL_LENGTH = 254
EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
)


def vulnerable_process_form(form: dict[str, Any]) -> dict[str, Any]:
    """Unsafe example: treats every submitted value as trusted data."""
    return {
        "name": form.get("name"),
        "date_of_birth": form.get("date_of_birth"),
        "email": form.get("email"),
        "accepted": True,
    }


def _valid_name(name: str) -> bool:
    if not 1 <= len(name) <= MAX_NAME_LENGTH:
        return False
    return all(character.isalpha() or character in " '-" for character in name)


def _valid_email(email: str) -> bool:
    if len(email) > MAX_EMAIL_LENGTH or email.count("@") != 1:
        return False
    return bool(EMAIL_PATTERN.fullmatch(email))


def validate_form(form: Any) -> tuple[dict[str, str], dict[str, str]]:
    """Validate and normalize a form without echoing rejected input."""
    errors: dict[str, str] = {}
    cleaned: dict[str, str] = {}

    if not isinstance(form, dict):
        return {}, {"form": "Expected an object with name, date_of_birth, and email."}

    missing_fields = EXPECTED_FIELDS - form.keys()
    unknown_fields = form.keys() - EXPECTED_FIELDS
    if missing_fields:
        errors["form"] = "Required fields are missing."
    if unknown_fields:
        errors["form"] = "Unexpected fields are not allowed."
    if errors:
        return {}, errors

    for field in EXPECTED_FIELDS:
        value = form[field]
        if not isinstance(value, str):
            errors[field] = "Expected a text value."
            continue
        cleaned[field] = value.strip()
        if not cleaned[field]:
            errors[field] = "Value cannot be empty."

    if errors:
        return {}, errors

    name = cleaned["name"]
    if not _valid_name(name):
        errors["name"] = "Name contains unsupported characters or is too long."

    date_of_birth = cleaned["date_of_birth"]
    if len(date_of_birth) != MAX_DATE_LENGTH:
        errors["date_of_birth"] = "Date must use YYYY-MM-DD format."
    else:
        try:
            parsed_date = date.fromisoformat(date_of_birth)
        except ValueError:
            errors["date_of_birth"] = "Date is not valid."
        else:
            if parsed_date > date.today():
                errors["date_of_birth"] = "Date cannot be in the future."

    email = cleaned["email"]
    if not _valid_email(email):
        errors["email"] = "Email address is not valid."

    if errors:
        return {}, errors

    cleaned["email"] = email.lower()
    return cleaned, {}


def _check_examples() -> None:
    valid_form = {
        "name": "Zoë O'Neil-Smith",
        "date_of_birth": "2024-02-29",
        "email": "  ZoE@example.COM ",
    }
    cleaned, errors = validate_form(valid_form)
    assert not errors
    assert cleaned == {
        "name": "Zoë O'Neil-Smith",
        "date_of_birth": "2024-02-29",
        "email": "zoe@example.com",
    }

    invalid_forms = [
        {"name": "<script>alert(1)</script>", "date_of_birth": "2026-02-31", "email": "not-an-email"},
        {"name": "Alex", "date_of_birth": "2999-01-01", "email": "alex@example.com"},
        {"name": "Alex", "date_of_birth": "2000-01-01", "email": "alex@@example.com"},
        {"name": None, "date_of_birth": "2000-01-01", "email": "alex@example.com"},
        {"name": "Alex", "date_of_birth": "2000-01-01", "email": "alex@example.com", "role": "admin"},
    ]
    for form in invalid_forms:
        _, errors = validate_form(form)
        assert errors


def main() -> None:
    _check_examples()

    examples = [
        {
            "name": "<script>alert(1)</script>",
            "date_of_birth": "2026-02-31",
            "email": "not-an-email",
        },
        {
            "name": " Zoë O'Neil-Smith ",
            "date_of_birth": "2000-02-29",
            "email": " ZoE@example.COM ",
        },
    ]

    for form in examples:
        print("Submitted:", form)
        print("Vulnerable result:", vulnerable_process_form(form))
        cleaned, errors = validate_form(form)
        print("Patched result:", cleaned if not errors else {"errors": errors})
        print()

    print("Checks passed: vulnerable input is accepted, patched input is validated.")


if __name__ == "__main__":
    main()
