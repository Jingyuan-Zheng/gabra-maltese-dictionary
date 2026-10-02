"""Regression checks for conversion, source preservation, and indexed lookup."""
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from mdict_utils.base.readmdict import MDX
from mdict_utils.base.writemdict import MDictWriter as LegacyWriter
from mdx_writer import MDictWriter
from check_mdx_index import check
from convert_to_mdx import convert, read_entries, CORRECTION_ID, ROOT


def source_file(path, entries):
    chunks = []
    for key, entry_id, gloss in entries:
        from xml.sax.saxutils import escape, quoteattr
        xml = (f'<d:entry xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng" '
               f'id="{entry_id}" d:title={quoteattr(key)}><h1>{escape(key)}</h1>'
               f'<span class="pos">NOUN</span><ol><li>{escape(gloss)}</li></ol></d:entry>').encode()
        block = b'\0' * 8 + zlib.compress(xml)
        chunks.append(struct.pack('<I', len(block)) + block)
    data = bytearray(0x60)
    struct.pack_into('<I', data, 0x40, 0x20 + sum(map(len, chunks)))
    path.write_bytes(data + b''.join(chunks))


class ConversionTests(unittest.TestCase):
    def test_legacy_sort_fails_and_new_sort_passes(self):
        records = {k: '<p>'+k+'</p>' for k in ['Zoo', 'badbad', "b'risq", 'bagħbas', 'aħwa', 'Apple']}
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/'test.mdx'
            with path.open('wb') as f:
                LegacyWriter(records, title='Test', description='').write(f)
            with self.assertRaisesRegex(AssertionError, 'order violations'):
                check(path)
            with path.open('wb') as f:
                MDictWriter(records, title='Test', description='').write(f)
            check(path)
            self.assertEqual(MDX(str(path)).header[b'StripKey'], b'Yes')

    def test_grouping_correction_and_source_preservation(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder)/'Body.data'
            source_file(source, [('bagħbas', 'one', 'to touch'), (' bagħbas ', 'two', 'to fondle'),
                                 (' ', CORRECTION_ID, 'brothers')])
            report = convert(source, Path(folder)/'out', ROOT/'assets/mdx/Gabra.css')
            records = dict(MDX(str(Path(folder)/'out/Gabra.mdx')).items())
            self.assertEqual(report['source_entries'], 3)
            self.assertEqual(report['unique_headwords'], 2)
            self.assertIn(b'to touch', records['bagħbas'.encode()])
            self.assertIn(b'to fondle', records['bagħbas'.encode()])
            self.assertIn('<h1>aħwa</h1>'.encode(), records['aħwa'.encode()])
            self.assertEqual(sorted(p.name for p in (Path(folder)/'out').iterdir()), ['Gabra.css', 'Gabra.mdx'])
            convert(source, Path(folder)/'raw', ROOT/'assets/mdx/Gabra.css', apply_correction=False)
            raw = dict(MDX(str(Path(folder)/'raw/Gabra.mdx')).items())
            self.assertNotIn('aħwa'.encode(), raw)

    def test_truncated_source_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder)/'Body.data'
            source_file(source, [('word', 'one', 'definition')])
            source.write_bytes(source.read_bytes()[:-1])
            with self.assertRaises(ValueError):
                list(read_entries(source))

    def test_shipped_dictionary_lookup(self):
        check(ROOT/'dictionaries/mdx/Gabra.mdx')


if __name__ == '__main__':
    unittest.main()
