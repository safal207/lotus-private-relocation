# Static intake prototype

This directory contains a browser-only prototype for the first-stage Lotus Private Relocation discovery brief.

## Privacy model

- no backend;
- no analytics;
- no cookies;
- no remote form action;
- no network transport in `app.js`;
- no document upload;
- no passport, banking, tax-return, exact-wealth, source-of-funds, child-document, password, token, or credential fields;
- output remains in the browser until the user explicitly downloads the JSON file.

The downloaded JSON may contain the contact reference entered by the user. It must be handled as confidential data and must never be committed to this public repository.

## Local preview

From the repository root:

```bash
python3 -m http.server 8080 --directory site
```

Then open `http://localhost:8080`.

The page also works when `site/index.html` is opened directly, although running a local HTTP server gives a more realistic browser environment.

## Validation

Install the development dependency and run the repository validator:

```bash
python3 -m pip install --requirement requirements-dev.txt
python3 scripts/validate_schemas.py
```

The validator checks:

- JSON Schema validity;
- synthetic client and partner fixtures;
- public-example privacy key guardrails;
- `.invalid` email use in public examples;
- presence of the static form assets;
- absence of a remote form action;
- absence of common browser network-transport APIs in `app.js`;
- required privacy-warning copy.

## Before production use

Do not connect this form to a backend until the following are defined and reviewed:

- legal entity and controller identity;
- privacy notice and lawful basis;
- consent evidence;
- data storage location;
- encryption and access controls;
- retention and deletion rules;
- incident response;
- processor and partner agreements;
- authentication and anti-abuse controls;
- jurisdiction-specific legal review.
