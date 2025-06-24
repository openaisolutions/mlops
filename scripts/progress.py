from __future__ import annotations

import json
from pathlib import Path

import yaml

TOC_PATH = Path("book/_toc.yml")
BADGE_PATH = Path("badges/progress.json")


def iter_sections(toc: dict) -> list[str]:
    files: list[str] = []
    for part in toc.get("parts", []):
        for chap in part.get("chapters", []):
            for sec in chap.get("sections", []):
                files.append(sec["file"])
    return files


def count_filled(paths: list[str]) -> int:
    count = 0
    for p in paths:
        f = Path("book") / f"{p}.md"
        if not f.exists():
            f = Path("book") / f
        if f.exists() and f.stat().st_size > 1024:
            count += 1
    return count


def main() -> None:
    toc = yaml.safe_load(TOC_PATH.read_text())
    section_files = iter_sections(toc)
    total = len(section_files)
    filled = count_filled(section_files)
    percent = int((filled / total) * 100) if total else 0
    BADGE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BADGE_PATH.write_text(
        json.dumps({"label": "book", "message": f"{percent}%", "color": "blue"})
    )


if __name__ == "__main__":
    main()
