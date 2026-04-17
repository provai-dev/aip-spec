#!/usr/bin/env python3

import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent


def current_draft_name() -> str:
    tree = ET.parse(ROOT / "draft.xml")
    return tree.getroot().attrib["docName"]


def main() -> int:
    errors = []
    draft_name = current_draft_name()

    if not re.match(r"^draft-[a-z0-9-]+-\d{2}$", draft_name):
        errors.append(f"Invalid draft name format: {draft_name}")

    index_path = ROOT / "drafts" / "index.json"
    if not index_path.exists():
        errors.append("drafts/index.json is missing")
    else:
        with index_path.open("r", encoding="utf-8") as handle:
            index = json.load(handle)
        if index.get("current_working_draft") != draft_name:
            errors.append(
                f"drafts/index.json current_working_draft does not match draft.xml: {draft_name}"
            )

        latest_minted = index.get("latest_minted_draft")
        snapshot_paths = {entry.get("draft"): entry.get("path") for entry in index.get("snapshots", [])}
        snapshot_path = snapshot_paths.get(draft_name)
        if snapshot_path and not (ROOT / snapshot_path).exists():
            errors.append(f"Current draft snapshot path is missing: {snapshot_path}")
        if latest_minted:
            latest_path = snapshot_paths.get(latest_minted)
            if not latest_path:
                errors.append(f"latest_minted_draft missing from drafts/index.json snapshots: {latest_minted}")
            elif not (ROOT / latest_path).exists():
                errors.append(f"latest_minted_draft path is missing: {latest_path}")

    for required_dir in ["schemas", "examples", "drafts"]:
        if not (ROOT / required_dir).exists():
            errors.append(f"{required_dir}/ directory is missing")

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Draft consistency checks passed for {draft_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
