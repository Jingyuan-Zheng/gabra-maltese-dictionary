"""Check MDX lookup order, not merely sequential decompression."""
from bisect import bisect_left
from pathlib import Path
import re
import string
import sys
from mdict_utils.base.readmdict import MDX


def lookup_key(value):
    return re.sub('[' + re.escape(string.punctuation) + ' ]+', '', value.lower())


def check(path, required_words=('badbad', 'bagħbas', 'aħwa')):
    reader = MDX(str(path))
    words = [key.decode('utf-8') for _, key in reader._key_list]
    normalized = [lookup_key(word) for word in words]
    inversions = sum(a > b for a, b in zip(normalized, normalized[1:]))
    assert inversions == 0, f'{inversions} index order violations'
    for word in words:
        key = lookup_key(word)
        index = bisect_left(normalized, key)
        assert index < len(words) and normalized[index] == key, word
    records = dict(reader.items())
    for word in required_words:
        assert word.encode() in records, word
        index = bisect_left(normalized, lookup_key(word))
        assert normalized[index] == lookup_key(word)
    print(f'PASS: {len(words)} keys searchable by normalized binary lookup; representative records present.')


if __name__ == '__main__':
    check(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'dictionaries/mdx/Gabra.mdx')
