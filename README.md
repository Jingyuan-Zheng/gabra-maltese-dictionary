# Ġabra Maltese Dictionary for macOS

A native macOS Dictionary for the [Ġabra Maltese Open Lexicon](https://mlrs.research.um.edu.mt/resources/gabra-api/), with 21,083 entries and 4.5 million searchable word forms.

## Install (recommended)

You do **not** need Xcode, Python, or this repository to use the dictionary.

1. Download the latest `GabraMalteseDict_*.dmg` from [Releases](https://github.com/Jingyuan-Zheng/gabra-maltese-macos-dictionary/releases/latest).
2. Double-click the downloaded DMG to open it.
3. Drag `Gabra.dictionary` into the `Dictionaries` folder shown in the DMG window.
4. Open the macOS **Dictionary** app and choose **Dictionary > Settings…**.
5. Find and enable **Ġabra Maltese Dictionary**.

The dictionary is then available in Dictionary and through macOS Look Up.

### If macOS blocks the installer

If macOS reports that the DMG cannot be opened, Control-click the file in Finder, choose **Open**, then confirm **Open** again.

## Build from source

This section is only for contributors or anyone who wants to generate a new dictionary from the Ġabra source data.

### Requirements

- macOS
- [Dictionary Development Kit](https://developer.apple.com/library/archive/documentation/UserExperience/Conceptual/DictionaryServicesProgGuide/Introduction/Introduction.html), installed at `/Applications/Dictionary Development Kit`
- Python 3

### Steps

1. Visit the [Ġabra download page](https://mlrs.research.um.edu.mt/resources/gabra-api/p/download) and download the latest `.tar.gz` data archive.
2. Create a `data/` folder in this project, if needed, and place the archive inside it.
3. In Terminal, from the project folder, run:

   ```bash
   chmod +x update.sh
   ./update.sh
   ```

The script extracts the data, generates the dictionary XML, builds the dictionary, and installs it in `~/Library/Dictionaries`.

## Project files

- `generate_gabra_xml.py` — converts Ġabra BSON data to Apple Dictionary XML.
- `update.sh` — automates generation, building, and installation.
- `Makefile`, `MyInfo.plist`, `MyDict.css` — Dictionary Development Kit configuration and styling.

## Credits

Dictionary data is provided by the [Ġabra project](https://mlrs.research.um.edu.mt/resources/gabra-api/) at the University of Malta.
