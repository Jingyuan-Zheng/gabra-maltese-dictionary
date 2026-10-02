# Attribution and licensing

## Lexical data

The dictionary derives from the **Ġabra Maltese Open Lexicon**, a project associated with **MLRS at the University of Malta**, including work by **John J. Camilleri** and its contributors.

- Upstream API and data-download documentation: https://github.com/MLRS/gabra-api
- Upstream web application: https://github.com/MLRS/gabra-web
- Historical project site: https://mlrs.research.um.edu.mt/resources/gabra/
- John J. Camilleri, *A computational grammar and lexicon for Maltese* (2013), Appendix D, printed page 100 / PDF page 113: https://publications.lib.chalmers.se/records/fulltext/185320/185320.pdf

Appendix D states that the lexicon data is covered by CC-BY and links to **Creative Commons Attribution 3.0**: https://creativecommons.org/licenses/by/3.0/ . This is the upstream license evidence used here; the bundled compiled snapshot has no separate license manifest or known BSON snapshot date. Retain this attribution and the upstream license link when redistributing data.

Local adaptations by this project: Apple Dictionary packaging; MDX conversion; duplicate-headword grouping; whitespace trimming in search keys; CSS for reader themes; the explicitly documented `aħwa` correction. The data remains distinct from the source-code license. This project is not an official University of Malta or Ġabra release.

## Project software

The repository already selected GNU GPL v3. Its previously truncated license placeholder has been replaced with the complete, unmodified text from https://www.gnu.org/licenses/gpl-3.0.txt . This does not change the selected license family or version.

## Dependencies and format references

- mdict-utils: https://github.com/liuyug/mdict-utils (installed dependency, not vendored).
- writemdict: https://github.com/zhansliu/writemdict (underlying MDX implementation; its source and license remain with the dependency).
- Apple dictionary block format investigation: https://gist.github.com/josephg/5e134adf70760ee7e49d . The decoder here is limited to the observed Gabra layout.
- Apple Dictionary Development Kit is required only for native macOS builds and is not distributed in this repository.
