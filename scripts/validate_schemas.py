#!/usr/bin/env python3
"""Validate public JSON Schemas, synthetic fixtures, and privacy guardrails."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
PARTNER_SCHEMA_PATH = ROOT / "schemas" / "partner-record.schema.json"
CONSENT_SCHEMA_PATH = ROOT / "schemas" / "consent-record.schema.json"
HANDOFF_SCHEMA_PATH = ROOT / "schemas" / "handoff-record.schema.json"

SCHEMA_FIXTURES = (
    (
        ROOT / "schemas" / "client-intake.schema.json",
        ROOT / "examples" / "client-intake.synthetic.json",
    ),
    (
        PARTNER_SCHEMA_PATH,
        ROOT / "examples" / "partner-record.synthetic.json",
    ),
    (
        CONSENT_SCHEMA_PATH,
        ROOT / "examples" / "consent-record.synthetic.json",
    ),
    (
        HANDOFF_SCHEMA_PATH,
        ROOT / "examples" / "handoff-record.synthetic.json",
    ),
    (
        HANDOFF_SCHEMA_PATH,
        ROOT / "examples" / "handoff-record.acknowledged.synthetic.json",
    ),
)

NEGATIVE_SCHEMA_FIXTURES = (
    (
        CONSENT_SCHEMA_PATH,
        ROOT / "tests" / "fixtures" / "consent-expired-without-expiry.invalid.json",
    ),
    (
        HANDOFF_SCHEMA_PATH,
        ROOT / "tests" / "fixtures" / "handoff-introduced-due-diligence.invalid.json",
    ),
    (
        HANDOFF_SCHEMA_PATH,
        ROOT / "tests" / "fixtures" / "handoff-introduced-without-consent.invalid.json",
    ),
    (
        HANDOFF_SCHEMA_PATH,
        ROOT / "tests" / "fixtures" / "handoff-introduced-with-blocking-risk.invalid.json",
    ),
)

PARTNER_RECORDS = tuple(sorted((ROOT / "examples").glob("*.partner.json")))
PUBLIC_EXAMPLES = tuple(sorted((ROOT / "examples").glob("*.json")))

FORBIDDEN_KEY_FRAGMENTS = {
    "passport",
    "bank_statement",
    "tax_return",
    "source_of_funds",
    "children_document",
    "child_document",
    "national_id",
    "credit_card",
    "api_key",
    "access_token",
    "password",
    "secret",
}

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot load valid JSON from {path.relative_to(ROOT)}: {exc}") from exc


def iter_items(value: Any, path: str = "$"):
    if isinstance(value, dict):
        for key, item in value.items():
            item_path = f"{path}.{key}"
            yield key, item, item_path
            yield from iter_items(item, item_path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            item_path = f"{path}[{index}]"
            yield None, item, item_path
            yield from iter_items(item, item_path)


def validation_errors(schema_path: Path, fixture_path: Path) -> list[str]:
    schema = load_json(schema_path)
    fixture = load_json(fixture_path)

    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())

    errors: list[str] = []
    for error in sorted(validator.iter_errors(fixture), key=lambda item: list(item.absolute_path)):
        location = "$"
        if error.absolute_path:
            location += "".join(
                f"[{part}]" if isinstance(part, int) else f".{part}"
                for part in error.absolute_path
            )
        errors.append(f"{fixture_path.relative_to(ROOT)} {location}: {error.message}")
    return errors


def validate_schema_and_fixture(schema_path: Path, fixture_path: Path) -> list[str]:
    try:
        return validation_errors(schema_path, fixture_path)
    except Exception as exc:  # jsonschema exposes several schema error subclasses
        return [f"Cannot validate {schema_path.relative_to(ROOT)}: {exc}"]


def validate_expected_invalid(schema_path: Path, fixture_path: Path) -> list[str]:
    try:
        errors = validation_errors(schema_path, fixture_path)
    except Exception as exc:
        return [f"Cannot validate negative fixture {fixture_path.relative_to(ROOT)}: {exc}"]

    if errors:
        return []

    return [
        f"Unsafe negative fixture unexpectedly passed: {fixture_path.relative_to(ROOT)}"
    ]


def validate_public_example_privacy(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path)

    for key, value, location in iter_items(data):
        if key is not None:
            normalised_key = key.lower().replace("-", "_")
            for fragment in FORBIDDEN_KEY_FRAGMENTS:
                if fragment in normalised_key:
                    errors.append(
                        f"{path.relative_to(ROOT)} {location}: forbidden public-example key '{key}'"
                    )

        if isinstance(value, str):
            for email in EMAIL_RE.findall(value):
                if not email.lower().endswith(".invalid"):
                    errors.append(
                        f"{path.relative_to(ROOT)} {location}: public example email must use .invalid"
                    )

    return errors


def validate_static_form() -> list[str]:
    errors: list[str] = []
    index_path = ROOT / "site" / "index.html"
    app_path = ROOT / "site" / "app.js"

    for path in (index_path, app_path, ROOT / "site" / "styles.css"):
        if not path.exists():
            errors.append(f"Missing static form asset: {path.relative_to(ROOT)}")

    if errors:
        return errors

    index_text = index_path.read_text(encoding="utf-8").lower()
    app_text = app_path.read_text(encoding="utf-8").lower()

    if "<form" not in index_text:
        errors.append("site/index.html must contain an intake form")
    if "action=" in index_text:
        errors.append("site/index.html must not submit to a remote form action")

    prohibited_transport_tokens = ("fetch(", "xmlhttprequest", "websocket", "sendbeacon")
    for token in prohibited_transport_tokens:
        if token in app_text:
            errors.append(f"site/app.js contains prohibited network transport token: {token}")

    required_privacy_copy = (
        "does not send your data",
        "do not enter passport",
        "source-of-funds",
    )
    for phrase in required_privacy_copy:
        if phrase not in index_text:
            errors.append(f"site/index.html missing privacy notice phrase: {phrase}")

    return errors


def main() -> int:
    errors: list[str] = []

    for schema_path, fixture_path in SCHEMA_FIXTURES:
        errors.extend(validate_schema_and_fixture(schema_path, fixture_path))

    for schema_path, fixture_path in NEGATIVE_SCHEMA_FIXTURES:
        errors.extend(validate_expected_invalid(schema_path, fixture_path))

    for partner_record_path in PARTNER_RECORDS:
        errors.extend(validate_schema_and_fixture(PARTNER_SCHEMA_PATH, partner_record_path))

    for example_path in PUBLIC_EXAMPLES:
        errors.extend(validate_public_example_privacy(example_path))

    errors.extend(validate_static_form())

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Validation passed: "
        f"{len(SCHEMA_FIXTURES)} positive schema fixtures, "
        f"{len(NEGATIVE_SCHEMA_FIXTURES)} rejected unsafe fixtures, "
        f"{len(PARTNER_RECORDS)} partner records, "
        f"{len(PUBLIC_EXAMPLES)} public examples, and static intake form guardrails."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
