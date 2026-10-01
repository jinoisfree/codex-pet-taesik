#!/usr/bin/env python3
"""Build repository previews from the distributable Codex Pet atlas."""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ATLAS_PATH = ROOT / "pet" / "spritesheet.webp"
PREVIEW_DIR = ROOT / "preview"
CELL_WIDTH = 192
CELL_HEIGHT = 208


def frames_for_row(atlas: Image.Image, row: int, count: int) -> list[Image.Image]:
    return [
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


def save_gif(frames: list[Image.Image], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    converted = [frame.convert("RGBA") for frame in frames]
    converted[0].save(
        output,
        save_all=True,
        append_images=converted[1:],
        duration=150,
        loop=0,
        disposal=2,
        transparency=0,
    )


def main() -> None:
    with Image.open(ATLAS_PATH) as source:
        atlas = source.convert("RGBA")

    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    atlas.save(PREVIEW_DIR / "contact-sheet.png", format="PNG", optimize=True)
    atlas.crop((0, 9 * CELL_HEIGHT, atlas.width, 11 * CELL_HEIGHT)).save(
        PREVIEW_DIR / "look-directions.png", format="PNG", optimize=True
    )

    save_gif(frames_for_row(atlas, 6, 6), PREVIEW_DIR / "animations" / "waiting.gif")
    save_gif(frames_for_row(atlas, 7, 6), PREVIEW_DIR / "animations" / "running.gif")
    save_gif(frames_for_row(atlas, 8, 6), PREVIEW_DIR / "animations" / "review.gif")


if __name__ == "__main__":
    main()
