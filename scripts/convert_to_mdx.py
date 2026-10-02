"""Convert a compiled Gabra Apple dictionary into MDX 2.0 and external CSS."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET
import zlib

from mdict_utils.base.readmdict import MDX
from mdx_writer import MDictWriter
from check_mdx_index import check as check_index

ROOT = Path(__file__).resolve().parents[1]
NS = '{http://www.apple.com/DTDs/DictionaryService-1.0.rng}'
CORRECTION_ID = '6357914a7f1ba0e22236b65a'


def find_body(source):
    source = Path(source)
    if source.is_file():
        return source
    for relative in ['Contents/Body.data', 'Contents/Resources/Body.data']:
        candidate = source / relative
        if candidate.is_file():
            return candidate
    raise ValueError(f'No Body.data found in {source}')


def read_entries(path):
    """Read Gabra's length-prefixed zlib blocks, each containing one XML entry.

    This is deliberately not a generic decoder for every Apple dictionary layout.
    Fail on an unsupported/truncated block instead of silently losing entries.
    """
    with Path(path).open('rb') as stream:
        stream.seek(0x40)
        header = stream.read(4)
        if len(header) != 4:
            raise ValueError('Truncated Body.data header')
        limit = 0x40 + struct.unpack('<I', header)[0]
        if limit < 0x60 or limit > Path(path).stat().st_size:
            raise ValueError('Invalid Body.data boundary')
        stream.seek(0x60)
        seen = set()
        while stream.tell() < limit:
            header = stream.read(4)
            if len(header) != 4:
                raise ValueError('Truncated block header')
            size = struct.unpack('<I', header)[0]
            if size < 8 or stream.tell() + size > limit:
                raise ValueError('Invalid block length')
            block = stream.read(size)
            root = ET.fromstring(zlib.decompress(block[8:]).decode('utf-8'))
            if root.tag != NS + 'entry':
                raise ValueError('Unsupported Apple dictionary entry layout')
            entry_id = root.attrib['id']
            if entry_id in seen:
                raise ValueError(f'Duplicate entry ID: {entry_id}')
            seen.add(entry_id)
            yield root


def convert(source, output_dir, css, apply_correction=True):
    source = find_body(source)
    # Read resources before writing any output, including when source==destination.
    css_bytes = Path(css).read_bytes()
    entries = defaultdict(list)
    corrections = []
    untitled = []
    source_count = 0
    for root in read_entries(source):
        key = root.attrib[NS + 'title'].strip()
        entry_id = root.attrib['id']
        if '\x00' in key:
            raise ValueError('NUL in headword')
        if apply_correction and entry_id == CORRECTION_ID:
            title = root.find('h1')
            if key or title is None or (title.text or '').strip():
                raise ValueError('Known correction no longer matches the source; review it')
            key = 'aħwa'
            title.text = key
            corrections.append({'source_id': entry_id, 'headword': key})
        if not key:
            key = f'[Untitled source entry {entry_id}]'
            untitled.append({'source_id': entry_id, 'headword': key})
        before = [' '.join(t.split()) for t in root.itertext() if t.strip()]
        root.tag = 'div'
        root.attrib = {'class': 'gabra-entry', 'id': entry_id}
        body = ET.tostring(root, encoding='unicode', method='html')
        body = re.sub(r'\n[ \t]*\n(?:[ \t]*\n)*', '\n', body).strip()
        if re.search(r'(?:src=|href="(?:x-dictionary|dict):)', body):
            raise ValueError(f'Entry needs resource/link conversion: {key}')
        after = [' '.join(t.split()) for t in ET.fromstring(body).itertext() if t.strip()]
        if before != after:
            raise ValueError(f'Text changed: {key}')
        entries[key].append(body)
        source_count += 1
    if not source_count:
        raise ValueError('No dictionary entries found')
    stylesheet = '<link rel="stylesheet" type="text/css" href="Gabra.css">'
    records = {key: stylesheet + '\n' + '\n'.join(bodies) for key, bodies in entries.items()}
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    mdx_path = output_dir / 'Gabra.mdx'
    with mdx_path.open('wb') as output:
        MDictWriter(records, title='Ġabra Maltese Dictionary',
            description='Based on the Ġabra Maltese Open Lexicon, University of Malta / MLRS. '
                        'Data: CC BY 3.0 (see project attribution). Converted to MDX; '
                        'duplicate headwords grouped. See project documentation for corrections.',
            encoding='utf8', compression_type=2, version='2.0').write(output)
    readback = list(MDX(str(mdx_path)).items())
    recovered = {key.decode('utf-8'): body.decode('utf-8').rstrip('\0') for key, body in readback}
    if len(readback) != len(records) or recovered != records:
        raise ValueError('MDX round-trip mismatch')
    if sum(body.count('<div class="gabra-entry"') for body in recovered.values()) != source_count:
        raise ValueError('Source entry count mismatch')
    check_index(mdx_path, required_words=())
    (output_dir / 'Gabra.css').write_bytes(css_bytes)
    return {'source_entries': source_count, 'unique_headwords': len(records),
            'headwords_with_multiple_entries': sum(len(v) > 1 for v in entries.values()),
            'corrections': corrections, 'untitled_entries': untitled,
            'source_body_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'mdx_sha256': hashlib.sha256(mdx_path.read_bytes()).hexdigest(),
            'css_sha256': hashlib.sha256(css_bytes).hexdigest(),
            'mdx_bytes': mdx_path.stat().st_size,
            'validation': 'All source entries retained; exact HTML round-trip; sorted lookup index.',
            'reader_validation': 'Offline checks do not guarantee behavior in every MDX reader.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path, help='Gabra.dictionary bundle or its Body.data file')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'dictionaries/mdx')
    parser.add_argument('--css', type=Path, default=ROOT / 'assets/mdx/Gabra.css')
    parser.add_argument('--report', type=Path, help='Optional JSON validation report outside deliverables')
    parser.add_argument('--no-corrections', action='store_true', help='Keep the known blank headword untitled')
    args = parser.parse_args()
    report = convert(args.source, args.output_dir, args.css, not args.no_corrections)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
