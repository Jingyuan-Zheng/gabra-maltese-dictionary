# Ġabra Maltese Dictionary for macOS

This project converts the [Ġabra Maltese Open Lexicon](https://mlrs.research.um.edu.mt/resources/gabra-api/) into a native macOS Dictionary application.

## Prerequisites

1.  **macOS**
2.  **Dictionary Development Kit**: Usually included with Xcode or can be downloaded separately. It must be located at `/Applications/Dictionary Development Kit`.
3.  **Python 3**: For parsing the BSON data and generating the dictionary XML.

## How to Build

1.  **Download Data**:
    Go to the [Ġabra Download Page](https://mlrs.research.um.edu.mt/resources/gabra-api/p/download) and download the latest "Latest" version (a `.tar.gz` file).
2.  **Place Data**:
    Put the downloaded `.tar.gz` file into the `data/` directory of this project.
3.  **Run Update Script**:
    Open Terminal and run:
    ```bash
    chmod +x update.sh
    ./update.sh
    ```
    This script will extract the data, generate the dictionary source, compile it, and install it to `~/Library/Dictionaries`.

## Usage

1.  Open the **Dictionary** app on your Mac.
2.  Go to **Settings...** (Cmd + ,).
3.  Scroll to the bottom and check **Ġabra Maltese Dictionary**.
4.  You can now search for Maltese words directly or use system-wide "Look up".

## Project Structure

- `data/`: Place your downloaded `.tar.gz` files here.
- `generate_gabra_xml.py`: Python script to convert BSON to Apple Dictionary XML.
- `update.sh`: Master script to automate the update process.
- `Makefile`, `MyInfo.plist`, `MyDict.css`: Configuration for the Dictionary Development Kit.

## Credits

Data provided by the [Ġabra](https://mlrs.research.um.edu.mt/resources/gabra-api/) project (University of Malta).
