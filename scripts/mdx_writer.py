"""MDX writer with consistent case-insensitive, punctuation-stripped indexing."""
from io import BytesIO
import re
import string
import struct
import zlib
from mdict_utils.base.writemdict import MDictWriter as BaseWriter


class MDictWriter(BaseWriter):
    def _build_offset_table(self, records):
        super()._build_offset_table(records)
        strip = re.compile('[' + re.escape(string.punctuation) + ' ]+')
        self._offset_table.sort(
            key=lambda entry: strip.sub('', entry.key.decode(self._python_encoding).lower()))
        offset = 0
        for entry in self._offset_table:
            entry.offset = offset
            offset += len(entry.record_null)
        self._total_record_len = offset

    def _write_header(self, output):
        buffer = BytesIO()
        super()._write_header(buffer)
        data = buffer.getvalue()
        size = struct.unpack('>I', data[:4])[0]
        header = data[4:4 + size].decode('utf-16le')
        header = header.replace('KeyCaseSensitive="No"',
                                'KeyCaseSensitive="No" StripKey="Yes"')
        encoded = header.encode('utf-16le')
        output.write(struct.pack('>I', len(encoded)))
        output.write(encoded)
        output.write(struct.pack('<I', zlib.adler32(encoded) & 0xffffffff))
