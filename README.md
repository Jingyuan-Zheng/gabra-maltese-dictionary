# Ġabra Maltese Dictionary

An offline Maltese dictionary for **iPhone, iPad, Android, Windows, Linux, and macOS**, based on the **Ġabra Maltese Open Lexicon**. Use the **MDX** edition with a dictionary reader, or install the native **macOS Dictionary** edition for integrated lookup on your Mac.

| Format | Entries | Download |
|---|---|---|
| MDX + CSS | 19,831 headwords containing 21,083 records | [MDX download (ZIP)](https://github.com/Jingyuan-Zheng/gabra-maltese-dictionary/releases/download/v1.0/GabraMalteseDict_MDX_v1.0.zip) |
| macOS `.dictionary` | 21,083 entries with approximately 4.5 million searchable word forms | [Releases](https://github.com/Jingyuan-Zheng/gabra-maltese-dictionary/releases) |

The MDX edition supports headword lookup. The native macOS edition also includes inflected word forms.

## Choose an app

**On macOS, we recommend the built-in Dictionary app and the native edition first.** It integrates with macOS Look Up and includes inflected word forms. GoldenDict-ng and MDict are additional options if you prefer using MDX files.

For the other platforms, install a reader below, then [download and import the MDX package](#install-mdx).

| Platform | Recommended app | Notes | Download |
|---|---|---|---|
| iPhone / iPad | **OpenMDict — first choice** | Free and open source; supports MDX/MDD. | [![App Store][app-store-badge]](https://apps.apple.com/app/id6759032057) |
| iPhone / iPad | MDict | An established MDX reader and a useful alternative. | [![App Store][app-store-badge]](https://apps.apple.com/app/id389083586) |
| Android | **DictTango — first choice** | Feature-rich; suited to frequent MDX use. | [![GitHub][github-badge]](https://github.com/Jimex/DictTango-Android/releases) |
| Android | MDict | A traditional, focused MDX reader. | [![Google Play][google-play-badge]](https://play.google.com/store/apps/details?id=cn.mdict) · [![Official download][official-download-badge]](https://www.mdict.cn/wp/?page_id=5227&lang=en) |
| Windows | **GoldenDict-ng — first choice** | Open source, with extensive dictionary-management and lookup features. | [![GitHub][github-badge]](https://github.com/xiaoyifang/goldendict-ng/releases/latest) |
| Windows | DictTango Windows | An alternative for users already familiar with DictTango on Android. | [![GitHub][github-badge]](https://github.com/Jimex/DictTango-Windows/releases) |
| Linux | **GoldenDict-ng — first choice** | Open source; available through Flathub and distribution packages. | [![Install guide][install-badge]](https://xiaoyifang.github.io/goldendict-ng/install/#linux) |
| macOS | **Apple Dictionary — first choice** | Built into macOS; use our native `.dictionary` edition. | [![Native dictionary][native-badge]](https://github.com/Jingyuan-Zheng/gabra-maltese-dictionary/releases/download/v1.0/GabraMalteseDict_v1.0.dmg) |
| macOS | GoldenDict-ng | A feature-rich MDX option for managing a large dictionary collection. | [![GitHub][github-badge]](https://github.com/xiaoyifang/goldendict-ng/releases/latest) |
| macOS | MDict | A simpler MDX option for focused word lookup. | [![App Store][app-store-badge]](https://apps.apple.com/app/id389083586?platform=mac) |

[app-store-badge]: https://img.shields.io/badge/App_Store-0D96F6?style=flat-square&logo=appstore&logoColor=white
[github-badge]: https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white
[google-play-badge]: https://img.shields.io/badge/Google_Play-414141?style=flat-square&logo=googleplay&logoColor=white
[official-download-badge]: https://img.shields.io/badge/Official_download-2563EB?style=flat-square
[install-badge]: https://img.shields.io/badge/Install_guide-2563EB?style=flat-square
[native-badge]: https://img.shields.io/badge/Download_DMG-555555?style=flat-square&logo=apple&logoColor=white

## Install MDX

1. Download [GabraMalteseDict_MDX_v1.0.zip](https://github.com/Jingyuan-Zheng/gabra-maltese-dictionary/releases/download/v1.0/GabraMalteseDict_MDX_v1.0.zip) from [Initial Release - v1.0](https://github.com/Jingyuan-Zheng/gabra-maltese-dictionary/releases/tag/v1.0).
2. Extract the ZIP. It contains `Gabra.mdx` and `Gabra.css`.
3. Keep both files in the same folder. In your chosen reader, use its dictionary import or add-folder option to load them. On a phone or tablet, transfer both files into the reader's dictionary storage.

The individual files are also available in [`dictionaries/mdx/`](dictionaries/mdx/).

The stylesheet follows the reader's light or dark theme. To customize the appearance, edit `Gabra.css`.

## Install on macOS — recommended native edition

1. Download the macOS DMG from [Releases](https://github.com/Jingyuan-Zheng/gabra-maltese-dictionary/releases).
2. Open it and copy `Gabra.dictionary` into `~/Library/Dictionaries`.
3. Enable the dictionary in **Dictionary → Settings**.

After installing it, you can look up Maltese words directly on your Mac without opening a separate website or third-party app. Use it with:

- The built-in **Dictionary** app.
- **Spotlight** dictionary results, where available in your macOS configuration.
- The macOS **Look Up** feature: tap a word with three fingers when that gesture is enabled, or use Force Click or the **Look Up** contextual-menu command in supported apps.

Choose your gesture in **System Settings → Trackpad → Point & Click → Look up & data detectors**. See Apple's guides to [lookup gestures](https://support.apple.com/en-us/102482) and [Spotlight](https://support.apple.com/en-mt/guide/mac-help/mchlp1008/mac).

I built it because I wanted Maltese lookup to feel like the built-in English dictionary on macOS. When reading a webpage or document, you can use the normal macOS lookup gesture on a Maltese word instead of copying it into a browser.

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
