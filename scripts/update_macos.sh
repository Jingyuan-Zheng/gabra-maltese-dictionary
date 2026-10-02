#!/bin/bash
# Generate and build a native dictionary; installation is an explicit opt-in.
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ $# -gt 1 || ( $# -eq 1 && "$1" != '--install' ) ]]; then
    echo 'Usage: scripts/update_macos.sh [--install]' >&2
    exit 2
fi
shopt -s nullglob
archives=("$ROOT_DIR"/data/*.tar.gz)
if [[ ${#archives[@]} -ne 1 ]]; then
    echo 'Place exactly one upstream BSON .tar.gz archive in data/.' >&2
    exit 1
fi
# Preserve existing data. Extract into a disposable build directory.
mkdir -p "$ROOT_DIR/build"
extract_dir="$(mktemp -d "$ROOT_DIR/build/gabra-data.XXXXXX")"
trap 'rm -rf "$extract_dir"' EXIT
tar -xzf "${archives[0]}" -C "$extract_dir"
"${PYTHON:-python3}" "$ROOT_DIR/scripts/generate_gabra_xml.py" --data-dir "$extract_dir/gabra" --output "$ROOT_DIR/macos/Gabra.xml"
make -C "$ROOT_DIR/macos" clean all
if [[ "${1:-}" == '--install' ]]; then
    destination="$HOME/Library/Dictionaries/Gabra.dictionary"
    if [[ -e "$destination" ]]; then
        backup_dir="$(mktemp -d "$ROOT_DIR/build/macos-backup.XXXXXX")"
        cp -R "$destination" "$backup_dir/Gabra.dictionary"
        echo "Previous dictionary backed up to $backup_dir"
    fi
    make -C "$ROOT_DIR/macos" install
fi
