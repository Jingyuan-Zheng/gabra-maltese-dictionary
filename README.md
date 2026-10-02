# Ġabra Maltese Dictionary

An offline Maltese dictionary based on the **Ġabra Maltese Open Lexicon**, available in **MDX** and native **macOS Dictionary** formats.

| Format | Entries | Download |
|---|---|---|
| MDX + CSS | 19,831 headwords containing 21,083 records | [MDX download (ZIP)](https://github.com/Jingyuan-Zheng/gabra-maltese-dictionary/releases/download/v1.0/GabraMalteseDict_MDX_v1.0.zip) |
| macOS `.dictionary` | 21,083 entries with approximately 4.5 million searchable word forms | [Releases](https://github.com/Jingyuan-Zheng/gabra-maltese-dictionary/releases) |

The MDX edition supports headword lookup. The native macOS edition also includes inflected word forms.

## Install MDX

1. Download [GabraMalteseDict_MDX_v1.0.zip](https://github.com/Jingyuan-Zheng/gabra-maltese-dictionary/releases/download/v1.0/GabraMalteseDict_MDX_v1.0.zip) from [Initial Release - v1.0](https://github.com/Jingyuan-Zheng/gabra-maltese-dictionary/releases/tag/v1.0).
2. Extract the ZIP. It contains `Gabra.mdx` and `Gabra.css`.
3. Keep both files in the same folder and import them into an MDX-compatible dictionary reader.

The individual files are also available in [`dictionaries/mdx/`](dictionaries/mdx/).

The stylesheet follows the reader's light or dark theme. To customize the appearance, edit `Gabra.css`.

## Install on macOS

1. Download the macOS DMG from [Releases](https://github.com/Jingyuan-Zheng/gabra-maltese-dictionary/releases).
2. Open it and copy `Gabra.dictionary` into `~/Library/Dictionaries`.
3. Enable the dictionary in **Dictionary → Settings**.

The dictionary is available in the Dictionary app and macOS Look Up.

## Build MDX

The repository includes the source entry snapshot at [`sources/gabra/Body.data`](sources/gabra/Body.data). This snapshot was extracted from the compiled Gabra macOS dictionary and contains the entry text needed to generate MDX.

**You do not need macOS, the Dictionary app, or an installed `.dictionary` bundle.** Clone or download this repository and run the commands below from its root folder. Python 3.10 or newer is required.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/convert_to_mdx.py sources/gabra/Body.data
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

The output files are:

```text
dictionaries/mdx/Gabra.mdx
dictionaries/mdx/Gabra.css
```

To change the generated dictionary's appearance, edit [`assets/mdx/Gabra.css`](assets/mdx/Gabra.css) before building. Use `--output-dir /path/to/output` to choose a different output folder.

This command rebuilds MDX from the included snapshot; it does not download newer upstream data. To convert another compiled Gabra dictionary, pass its bundle path instead:

```sh
python scripts/convert_to_mdx.py /path/to/Gabra.dictionary --output-dir build/mdx
```

## Build the macOS dictionary

The native build starts from upstream **BSON data**, rather than the MDX snapshot. It requires macOS, Python 3, and Apple's **Dictionary Development Kit** at `/Applications/Dictionary Development Kit`.

1. Obtain a Ġabra BSON archive through the [upstream API project](https://github.com/MLRS/gabra-api).
2. Place one `.tar.gz` archive in `data/`. It should contain `gabra/lexemes.bson` and `gabra/wordforms.bson`.
3. Run:

```sh
bash scripts/update_macos.sh
```

The output is `macos/objects/Gabra.dictionary`. To build and install it, run:

```sh
bash scripts/update_macos.sh --install
```

An existing installed Gabra dictionary is backed up under `build/` before installation.

## Development

Run the tests with:

```sh
python -m unittest discover -s tests -v
```

| Directory | Contents |
|---|---|
| `dictionaries/mdx/` | Ready-to-use MDX and CSS |
| `assets/mdx/` | Stylesheet used during builds |
| `sources/gabra/` | Entry snapshot for rebuilding MDX |
| `scripts/` | Conversion and build tools |
| `macos/` | Native dictionary templates and Makefile |
| `tests/` | Automated tests |
| `docs/` | Technical documentation and attribution |

## Credits and license

Dictionary data comes from **Ġabra / MLRS, University of Malta**, including work by John J. Camilleri and upstream contributors, under **CC BY 3.0**. See [attribution](docs/ATTRIBUTION.md).

Project code is licensed under [GNU GPL v3](LICENSE). MDX conversion uses [mdict-utils](https://github.com/liuyug/mdict-utils) and its underlying [writemdict](https://github.com/zhansliu/writemdict) implementation.
