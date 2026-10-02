# Ġabra Maltese Dictionary

Offline Maltese dictionaries based on the **Ġabra Maltese Open Lexicon**, with ready-to-use **MDX** files and a native **macOS Dictionary** build pipeline.

Previously named `gabra-maltese-macos-dictionary`. The project now covers both formats.

| Format | Where to get it | Search coverage |
|---|---|---|
| MDX + CSS | [`dictionaries/mdx/`](dictionaries/mdx/) | 19,831 lookup keys containing all 21,083 source records |
| macOS `.dictionary` | Existing [macOS release assets](https://github.com/Jingyuan-Zheng/gabra-maltese-dictionary/releases) or build below | Original build includes upstream word-form indexes; the original release describes approximately 4.5 million forms |

**The MDX version indexes headwords, not the macOS word-form index.** The two counts are not interchangeable.

## Use the MDX version

1. Download **both** [`Gabra.mdx`](dictionaries/mdx/Gabra.mdx) and [`Gabra.css`](dictionaries/mdx/Gabra.css) using GitHub's **Download raw file** button, or clone the repository.
2. Keep the files together in the same folder and import the MDX into your reader. If its importer copies dictionaries, also transfer the CSS into the reader's dictionary folder.
3. Enable **Ġabra Maltese Dictionary** and try `badbad`, `bagħbas`, or `aħwa`.

The corrected version has been reported working in **EuDic / 欧路词典**. Other MDX readers may work but have not been tested here. If you imported an older build and entries are missing, remove its dictionary entry and reimport the current files so the reader rebuilds its index.

Entry text inherits the reader's foreground colour and uses a transparent background for light/dark themes. Edit `Gabra.css` to adjust appearance, then reopen the dictionary if the reader caches styles. No ZIP, webpage preview, MDD, or JavaScript is needed.

## Use the macOS version

Download the existing macOS DMG if available under [Releases](https://github.com/Jingyuan-Zheng/gabra-maltese-dictionary/releases), open it, and copy `Gabra.dictionary` into `~/Library/Dictionaries`. Enable it in **Dictionary → Settings**. It is then available in Dictionary and macOS Look Up.

Native installers are release assets, not Git source files. A local checkout may also have them under `releases/macos/` (ignored by Git). The repository rename does not rebuild or reinstall your existing native dictionary.

## Rebuild MDX on any platform

Requires Python 3.10 or newer; the tooling is tested with Python 3.12. macOS and Apple's development tools are **not required** for MDX conversion.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/convert_to_mdx.py sources/gabra/Body.data --report docs/mdx-validation.json
python scripts/check_mdx_index.py dictionaries/mdx/Gabra.mdx
```

On Windows, activate the environment with `.venv\Scripts\activate` instead.

The default output folder contains only `Gabra.mdx` and `Gabra.css`. The canonical stylesheet is [`assets/mdx/Gabra.css`](assets/mdx/Gabra.css); rebuilding copies it to the output. To retain a customized output stylesheet, supply it with `--css dictionaries/mdx/Gabra.css`.

You can also pass a compiled `Gabra.dictionary` bundle or its `Body.data` file:

```sh
python scripts/convert_to_mdx.py /path/to/Gabra.dictionary --output-dir build/mdx
```

The converter supports the **Gabra bundle's block layout**, not every Apple dictionary format. Unsupported/truncated input fails rather than silently dropping entries. See [`sources/gabra/README.md`](sources/gabra/README.md) for snapshot provenance.

## Build the native macOS dictionary

Requires macOS, Python 3, and Apple's **Dictionary Development Kit** at `/Applications/Dictionary Development Kit`.

1. Obtain a Ġabra BSON data archive from the [upstream API project](https://github.com/MLRS/gabra-api). The historical [download page](https://mlrs.research.um.edu.mt/resources/gabra-api/p/download) may redirect or be unavailable.
2. Place exactly one `.tar.gz` in `data/`, containing `gabra/lexemes.bson` and `gabra/wordforms.bson`.
3. Run:

```sh
bash scripts/update_macos.sh
```

The compiled bundle is `macos/objects/Gabra.dictionary`. To build **and install**, use `bash scripts/update_macos.sh --install`; an existing installed Gabra bundle is backed up under `build/` first.

For already-extracted BSON data:

```sh
python3 scripts/generate_gabra_xml.py --data-dir /path/to/gabra --output macos/Gabra.xml
make -C macos
```

The source migration was checked with a small BSON fixture and a build-command dry run; the full native dictionary was not rebuilt for the MDX addition.

## Data quality and validation

Same-headword records are grouped without dropping definitions. Leading/trailing whitespace in lookup keys is trimmed. One blank source headword was changed to **aħwa** by maintainer decision; its `NOUN` / `brothers` content is retained. Use `--no-corrections` for an untitled placeholder instead. This correction has not been verified against an updated upstream record.

Other source anomalies are retained, including `lejliet; acc. to my dictionarues the form is: lejlet`. The ordinary `lejlet` and `lejliet` entries are also present. See [data notes](docs/data-notes.md).

Validation covers source text preservation, all source record counts, exact MDX round-trip decoding, and normalized binary lookup for every key. A regression test rejects the earlier case-sensitive ordering that caused missing lookups. These offline checks cannot guarantee every reader's implementation.

```sh
python -m unittest discover -s tests -v
```

## Repository layout

```text
dictionaries/mdx/   Ready-to-use Gabra.mdx and Gabra.css
assets/mdx/         Canonical editable stylesheet
sources/gabra/     Compiled entry-body snapshot and provenance
scripts/           MDX conversion, index validation, native build tools
macos/             Apple Dictionary templates and Makefile
tests/             Conversion and lookup regression checks
docs/              Data notes, build report, attribution
releases/macos/    Local native release assets (ignored)
data/              Local upstream BSON archives (ignored)
```

## Credits and licensing

Dictionary data: **Ġabra / MLRS, University of Malta**, including work by John J. Camilleri and upstream contributors. See [upstream attribution and data licensing](docs/ATTRIBUTION.md). The data is attributed under the upstream **CC BY 3.0** statement; it is separate from this repository's code license.

Project code: **GNU GPL v3**, retaining the repository's existing license choice; [`LICENSE`](LICENSE) now contains the complete text. MDX tooling uses the separately installed [mdict-utils](https://github.com/liuyug/mdict-utils) package and its [writemdict](https://github.com/zhansliu/writemdict) implementation. No third-party library source is vendored.
