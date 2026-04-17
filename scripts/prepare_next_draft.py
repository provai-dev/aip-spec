#!/usr/bin/env python3

import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "drafts" / "index.json"


def bump_name(name: str) -> str:
    match = re.match(r"^(.*-)(\d{2})$", name)
    if not match:
        raise SystemExit(f"Unrecognized draft name format: {name}")
    prefix, number = match.groups()
    return f"{prefix}{int(number) + 1:02d}"


def load_index() -> dict:
    with INDEX_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_index(index: dict) -> None:
    with INDEX_PATH.open("w", encoding="utf-8") as handle:
        json.dump(index, handle, indent=2)
        handle.write("\n")


def main() -> int:
    draft_xml = ROOT / "draft.xml"
    tree = ET.parse(draft_xml)
    root = tree.getroot()
    current = root.attrib["docName"]
    next_name = bump_name(current)

    if not (ROOT / "drafts" / current).exists():
        raise SystemExit(
            f"Current draft snapshot drafts/{current} does not exist. Archive the current draft before bumping."
        )

    root.attrib["docName"] = next_name
    for series in root.findall("./front/seriesInfo"):
        if series.attrib.get("name") == "Internet-Draft":
            series.attrib["value"] = next_name

    tree.write(draft_xml, encoding="utf-8", xml_declaration=True)

    index = load_index()
    index["current_working_draft"] = next_name
    write_index(index)

    print(f"Bumped draft.xml from {current} to {next_name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
