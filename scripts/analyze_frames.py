#!/usr/bin/env python3
"""Report adjacent-frame differences for the distributable atlas."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]
CELL_WIDTH = 192
CELL_HEIGHT = 208
USED_COLUMNS = (7, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8)


def changed_pixels(first: Image.Image, second: Image.Image) -> int:
    difference = ImageChops.difference(first, second)
    pixels = (
        difference.get_flattened_data()
        if hasattr(difference, "get_flattened_data")
        else difference.getdata()
    )
    return sum(pixel != (0, 0, 0, 0) for pixel in pixels)


def main() -> None:
    with Image.open(ROOT / "pet" / "spritesheet.webp") as source:
        atlas = source.convert("RGBA")

    rows = []
    for row, count in enumerate(USED_COLUMNS):
        frames = [
            atlas.crop(
                (
                    column * CELL_WIDTH,
                    row * CELL_HEIGHT,
                    (column + 1) * CELL_WIDTH,
                    (row + 1) * CELL_HEIGHT,
                )
            )
            for column in range(count)
        ]
        differences = [
            changed_pixels(frames[index], frames[index + 1])
            for index in range(len(frames) - 1)
        ]
        rows.append(
            {
                "row": row,
                "frames": count,
                "minAdjacentDiffPixels": min(differences),
                "maxAdjacentDiffPixels": max(differences),
                "allAdjacentFramesDistinct": all(value > 0 for value in differences),
            }
        )

    print(json.dumps({"ok": all(row["allAdjacentFramesDistinct"] for row in rows), "rows": rows}, indent=2))


if __name__ == "__main__":
    main()
