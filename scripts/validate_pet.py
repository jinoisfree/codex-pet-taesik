#!/usr/bin/env python3
"""Validate the distributable Taesik Codex pet without modifying it."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
PET_DIR = ROOT / "pet"
MANIFEST_PATH = PET_DIR / "pet.json"
SPRITESHEET_PATH = PET_DIR / "spritesheet.webp"
CELL_WIDTH = 192
CELL_HEIGHT = 208
EXPECTED_SIZE = (1536, 2288)
USED_COLUMNS = (7, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8)


def fail(message: str) -> None:
    raise ValueError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pixel_data(image: Image.Image):
    if hasattr(image, "get_flattened_data"):
        return image.get_flattened_data()
    return image.getdata()


def visible_pixels(image: Image.Image) -> int:
    alpha = image.getchannel("A")
    return sum(1 for value in pixel_data(alpha) if value > 0)


def validate() -> dict[str, object]:
    if not MANIFEST_PATH.is_file():
        fail(f"missing manifest: {MANIFEST_PATH}")
    if not SPRITESHEET_PATH.is_file():
        fail(f"missing spritesheet: {SPRITESHEET_PATH}")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("id") != "phone-cat":
        fail("pet id must be phone-cat")
    if manifest.get("spriteVersionNumber") != 2:
        fail("spriteVersionNumber must be 2")
    if manifest.get("spritesheetPath") != "spritesheet.webp":
        fail("spritesheetPath must be spritesheet.webp")

    with Image.open(SPRITESHEET_PATH) as source:
        if source.size != EXPECTED_SIZE:
            fail(f"spritesheet size must be {EXPECTED_SIZE}, got {source.size}")
        atlas = source.convert("RGBA")

    transparent_rgb_residue = 0
    used_cells = 0
    unused_cells = 0

    for row, used_count in enumerate(USED_COLUMNS):
        for column in range(8):
            cell = atlas.crop(
                (
                    column * CELL_WIDTH,
                    row * CELL_HEIGHT,
                    (column + 1) * CELL_WIDTH,
                    (row + 1) * CELL_HEIGHT,
                )
            )
            count = visible_pixels(cell)
            if column < used_count:
                used_cells += 1
                if count == 0:
                    fail(f"used cell r{row}c{column} is empty")
            else:
                unused_cells += 1
                if count != 0:
                    fail(f"unused cell r{row}c{column} is not transparent")

            transparent_rgb_residue += sum(
                1
                for red, green, blue, alpha in pixel_data(cell)
                if alpha == 0 and (red != 0 or green != 0 or blue != 0)
            )

    if transparent_rgb_residue:
        fail(f"found {transparent_rgb_residue} hidden RGB pixels under alpha 0")

    waiting = atlas.crop((0, 6 * CELL_HEIGHT, 1536, 7 * CELL_HEIGHT))
    running = atlas.crop((0, 7 * CELL_HEIGHT, 1536, 8 * CELL_HEIGHT))
    if ImageChops.difference(waiting, running).getbbox() is None:
        fail("waiting and running rows must be visually distinct")

    return {
        "ok": True,
        "id": manifest["id"],
        "displayName": manifest["displayName"],
        "spriteVersionNumber": manifest["spriteVersionNumber"],
        "dimensions": list(EXPECTED_SIZE),
        "usedCells": used_cells,
        "unusedCells": unused_cells,
        "transparentRgbResiduePixels": transparent_rgb_residue,
        "spritesheetSha256": sha256(SPRITESHEET_PATH),
        "manifestSha256": sha256(MANIFEST_PATH),
    }


def main() -> int:
    try:
        result = validate()
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
