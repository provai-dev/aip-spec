#!/usr/bin/env python3

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "drafts" / "index.json"


def current_draft_name() -> str:
    tree = ET.parse(ROOT / "draft.xml")
    return tree.getroot().attrib["docName"]


def copy_path(src: Path, dst: Path) -> None:
    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)


def load_index() -> dict:
    with INDEX_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_index(index: dict) -> None:
    with INDEX_PATH.open("w", encoding="utf-8") as handle:
        json.dump(index, handle, indent=2)
        handle.write("\n")


def ensure_snapshot_record(index: dict, draft_name: str, archive_dir: Path) -> None:
    snapshots = index.setdefault("snapshots", [])
    for entry in snapshots:
        if entry.get("draft") == draft_name:
            entry["path"] = str(archive_dir.relative_to(ROOT))
            entry["status"] = "minted"
            break
    else:
        snapshots.append(
            {
                "draft": draft_name,
                "path": str(archive_dir.relative_to(ROOT)),
                "status": "minted",
            }
        )
    index["latest_minted_draft"] = draft_name


def main() -> int:
    draft_name = current_draft_name()
    archive_dir = ROOT / "drafts" / draft_name
    created = False

    if not archive_dir.exists():
        created = True
        (archive_dir / "source").mkdir(parents=True)
        (archive_dir / "generated").mkdir(parents=True)

        copy_path(ROOT / "draft.xml", archive_dir / "source" / "draft.xml")
        copy_path(ROOT / "sections", archive_dir / "source" / "sections")
        copy_path(ROOT / "references", archive_dir / "source" / "references")
        copy_path(ROOT / "schemas", archive_dir / "schemas")
        copy_path(ROOT / "examples", archive_dir / "examples")

        for name in [
            "draft-expanded.xml",
            f"{draft_name}.html",
            f"{draft_name}.txt",
        ]:
            src = ROOT / name
            if src.exists():
                copy_path(src, archive_dir / "generated" / name)

        metadata = {
            "draft": draft_name,
            "archived_at": datetime.now(timezone.utc).isoformat(),
            "source_issues": [],
            "approvals": [],
            "notes": "Fill in source issues, approvals, and release notes before finalizing the archival PR.",
        }
        with (archive_dir / "metadata.json").open("w", encoding="utf-8") as handle:
            json.dump(metadata, handle, indent=2)
            handle.write("\n")

    index = load_index()
    ensure_snapshot_record(index, draft_name, archive_dir)
    write_index(index)

    if created:
        print(f"Created archival snapshot at {archive_dir}")
    else:
        print(f"Snapshot already exists at {archive_dir}; refreshed drafts/index.json only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
