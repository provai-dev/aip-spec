#!/usr/bin/env python3

import json
import sys
from pathlib import Path
import warnings

try:
    import jsonschema
except ImportError as exc:
    raise SystemExit("jsonschema is required. Install with: pip install jsonschema") from exc


ROOT = Path(__file__).resolve().parent.parent

warnings.filterwarnings("ignore", category=DeprecationWarning)

EXAMPLE_SCHEMA_MAP = {
    "approval-envelope.json": "approval-envelope.schema.json",
    "capability-manifest.json": "capability-manifest.schema.json",
    "capability-overlay.json": "capability-overlay.schema.json",
    "credential-token.json": "credential-token.schema.json",
    "endorsement.json": "endorsement.schema.json",
    "engagement-object.json": "engagement-object.schema.json",
    "grant-request.json": "grant-request.schema.json",
    "grant-response.json": "grant-response.schema.json",
    "personal-agent.json": "agent-identity.schema.json",
    "registration-envelope.json": "registration-envelope.schema.json",
    "revocation.json": "revocation-object.schema.json",
    "step-execution-token.json": "credential-token.schema.json",
}

SKIPPED_EXAMPLES = {
    "delegation-chain.json": "No standalone schema file exists for this example.",
    "did-document.json": "Informative DID document example without a repository-local schema file.",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def strip_commentary(value):
    if isinstance(value, dict):
        return {
            key: strip_commentary(inner)
            for key, inner in value.items()
            if not key.startswith("_")
        }
    if isinstance(value, list):
        return [strip_commentary(item) for item in value]
    return value


def schema_instance_for_example(name: str, raw):
    if name in {"credential-token.json", "step-execution-token.json"}:
        return raw["decoded"]["payload"]
    return strip_commentary(raw)


def main() -> int:
    errors = []
    validated = 0

    examples_dir = ROOT / "examples"
    schemas_dir = ROOT / "schemas"
    schema_store = {}

    for schema_path in schemas_dir.glob("*.json"):
        schema = load_json(schema_path)
        schema_store[schema_path.as_uri()] = schema
        schema_id = schema.get("$id")
        if schema_id:
            schema_store[schema_id] = schema

    for example_path in sorted(examples_dir.glob("*.json")):
        if example_path.name in SKIPPED_EXAMPLES:
            print(f"SKIP {example_path.name}: {SKIPPED_EXAMPLES[example_path.name]}")
            continue

        schema_name = EXAMPLE_SCHEMA_MAP.get(example_path.name)
        if not schema_name:
            errors.append(f"{example_path.name}: no schema mapping configured")
            continue

        schema_path = schemas_dir / schema_name
        if not schema_path.exists():
            errors.append(f"{schema_path}: missing schema")
            continue

        try:
            schema = load_json(schema_path)
            instance = schema_instance_for_example(example_path.name, load_json(example_path))
            jsonschema.Draft202012Validator.check_schema(schema)
            resolver = jsonschema.RefResolver.from_schema(schema, store=schema_store)
            jsonschema.validate(instance=instance, schema=schema, resolver=resolver)
            print(f"OK   {example_path.name} -> {schema_name}")
            validated += 1
        except Exception as exc:
            errors.append(f"{example_path.name}: {exc}")

    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1

    print(f"Validated {validated} example files against schemas/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
