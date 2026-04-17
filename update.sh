#!/bin/bash

# Update script for Gabra Maltese Dictionary

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DATA_DIR="$SCRIPT_DIR/data"

echo "Checking for new data in $DATA_DIR..."

# Check if there's a .tar.gz file in the data directory
TAR_FILE=$(ls "$DATA_DIR"/*.tar.gz 2>/dev/null | head -n 1)

if [ -z "$TAR_FILE" ]; then
    echo "No .tar.gz file found in $DATA_DIR."
    echo "Please download the latest BSON data from https://mlrs.research.um.edu.mt/resources/gabra-api/p/download"
    echo "and place it in the 'data' directory."
    exit 1
fi

echo "Extracting $TAR_FILE..."
# Remove old gabra directory if exists
rm -rf "$DATA_DIR/gabra"
tar -xzf "$TAR_FILE" -C "$DATA_DIR"

echo "Generating XML..."
python3 "$SCRIPT_DIR/generate_gabra_xml.py"

echo "Building dictionary..."
cd "$SCRIPT_DIR"
make clean
make

echo "Installing dictionary..."
make install

echo "Update complete! Please restart the Dictionary app to see changes."
