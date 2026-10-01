#!/usr/bin/env python3
"""Normalize a generated Taesik redesign into a Codex Pet v2 atlas."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


TARGET_SIZE = (1536, 2288)
CELL_WIDTH = 192
CELL_HEIGHT = 208
USED_COLUMNS = (7, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8)
LOW_ALPHA_CUTOFF = 32
PALETTE_COLORS = 48


def normalize(source_path: Path, output_path: Path) -> None:
    with Image.open(source_path) as source:
        atlas = source.convert("RGBA").resize(TARGET_SIZE, Image.Resampling.LANCZOS)

    alpha = atlas.getchannel("A")
    colors = atlas.convert("RGB").quantize(
        colors=PALETTE_COLORS,
        method=Image.Quantize.MEDIANCUT,
        dither=Image.Dither.NONE,
    )
    atlas = colors.convert("RGBA")
    atlas.putalpha(alpha)

    pixels = atlas.load()
    for y in range(atlas.height):
        for x in range(atlas.width):
            red, green, blue, alpha = pixels[x, y]
            if alpha < LOW_ALPHA_CUTOFF:
                pixels[x, y] = (0, 0, 0, 0)
            elif alpha == 0 and (red or green or blue):
                pixels[x, y] = (0, 0, 0, 0)

    transparent = Image.new("RGBA", (CELL_WIDTH, CELL_HEIGHT), (0, 0, 0, 0))
    for row, used_count in enumerate(USED_COLUMNS):
        for column in range(used_count, 8):
            atlas.paste(transparent, (column * CELL_WIDTH, row * CELL_HEIGHT))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(output_path, format="WEBP", lossless=True, method=6, exact=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    normalize(args.source, args.output)


if __name__ == "__main__":
    main()
