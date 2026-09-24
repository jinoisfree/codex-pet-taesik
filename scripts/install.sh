#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
CODEX_DATA_DIR=${CODEX_HOME:-"$HOME/.codex"}
TARGET_DIR="$CODEX_DATA_DIR/pets/phone-cat"

if [ -f "$TARGET_DIR/pet.json" ] || [ -f "$TARGET_DIR/spritesheet.webp" ]; then
  BACKUP_DIR="$TARGET_DIR/backups/$(date -u +%Y%m%dT%H%M%SZ)"
  mkdir -p "$BACKUP_DIR"
  [ ! -f "$TARGET_DIR/pet.json" ] || cp "$TARGET_DIR/pet.json" "$BACKUP_DIR/pet.json"
  [ ! -f "$TARGET_DIR/spritesheet.webp" ] || cp "$TARGET_DIR/spritesheet.webp" "$BACKUP_DIR/spritesheet.webp"
fi

mkdir -p "$TARGET_DIR"
cp "$REPO_DIR/pet/pet.json" "$TARGET_DIR/pet.json"
cp "$REPO_DIR/pet/spritesheet.webp" "$TARGET_DIR/spritesheet.webp"

echo "Installed Taesik to $TARGET_DIR"
