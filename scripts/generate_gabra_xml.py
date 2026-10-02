import argparse
from pathlib import Path
import struct
import os
import xml.sax.saxutils as saxutils

def parse_bson_doc(f):
    header = f.read(4)
    if not header:
        return None
    doc_len = struct.unpack('<I', header)[0]
    data = header + f.read(doc_len - 4)
    
    def parse_doc(data, pos):
        doc_len = struct.unpack('<I', data[pos:pos+4])[0]
        end_pos = pos + doc_len
        pos += 4
        doc = {}
        while pos < end_pos - 1:
            element_type = data[pos]
            pos += 1
            name_end = data.find(b'\x00', pos)
            name = data[pos:name_end].decode('utf-8', errors='ignore')
            pos = name_end + 1
            
            if element_type == 0x01: # Double
                value = struct.unpack('<d', data[pos:pos+8])[0]
                pos += 8
            elif element_type == 0x02: # String
                str_len = struct.unpack('<I', data[pos:pos+4])[0]
                pos += 4
                value = data[pos:pos+str_len-1].decode('utf-8', errors='ignore')
                pos += str_len
            elif element_type == 0x03: # Document
                value, pos = parse_doc(data, pos)
            elif element_type == 0x04: # Array
                value_doc, pos = parse_doc(data, pos)
                value = [value_doc[str(i)] for i in range(len(value_doc))]
            elif element_type == 0x05: # Binary
                bin_len = struct.unpack('<I', data[pos:pos+4])[0]
                pos += 5
                value = data[pos:pos+bin_len]
                pos += bin_len
            elif element_type == 0x07: # ObjectId
                value = data[pos:pos+12].hex()
                pos += 12
            elif element_type == 0x08: # Boolean
                value = data[pos] == 0x01
                pos += 1
            elif element_type == 0x09: # UTC datetime
                value = struct.unpack('<q', data[pos:pos+8])[0]
                pos += 8
            elif element_type == 0x0A: # Null
                value = None
            elif element_type == 0x10: # Int32
                value = struct.unpack('<i', data[pos:pos+4])[0]
                pos += 4
            elif element_type == 0x12: # Int64
                value = struct.unpack('<q', data[pos:pos+8])[0]
                pos += 8
            else:
                break
            doc[name] = value
        return doc, end_pos

    doc, _ = parse_doc(data, 0)
    return doc

def generate_dict(data_dir, xml_output_path):
    script_dir = str(data_dir)
    lexemes_path = os.path.join(script_dir, 'lexemes.bson')
    wordforms_path = os.path.join(script_dir, 'wordforms.bson')
    Path(xml_output_path).parent.mkdir(parents=True, exist_ok=True)
    
    lexemes = {}
    print(f"Reading lexemes from {lexemes_path}...")
    if not os.path.exists(lexemes_path):
        print(f"Error: {lexemes_path} not found.")
        raise FileNotFoundError("Required BSON input is missing")
        
    with open(lexemes_path, 'rb') as f:
        while True:
            doc = parse_bson_doc(f)
            if doc is None:
                break
            lexemes[doc['_id']] = {
                'lemma': doc.get('lemma', ''),
                'pos': doc.get('pos', ''),
                'glosses': doc.get('glosses', []),
                'phonetic': doc.get('phonetic', ''),
                'root': doc.get('root', {}).get('radicals', ''),
                'forms': set()
            }
    
    print(f"Loaded {len(lexemes)} lexemes.")
    
    print(f"Reading wordforms from {wordforms_path} (this may take a while)...")
    if not os.path.exists(wordforms_path):
        print(f"Error: {wordforms_path} not found.")
        raise FileNotFoundError("Required BSON input is missing")

    count = 0
    with open(wordforms_path, 'rb') as f:
        while True:
            doc = parse_bson_doc(f)
            if doc is None:
                break
            lid = doc.get('lexeme_id')
            form = doc.get('surface_form')
            if lid in lexemes and form:
                lexemes[lid]['forms'].add(form)
            count += 1
            if count % 100000 == 0:
                print(f"Processed {count} wordforms...")

    print(f"Writing XML to {xml_output_path}...")
    with open(xml_output_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">\n')
        
        for lid, data in lexemes.items():
            lemma = data['lemma']
            if not lemma: continue
            
            f.write(f'<d:entry id="{lid}" d:title={saxutils.quoteattr(lemma)}>\n')
            f.write(f'  <d:index d:value={saxutils.quoteattr(lemma)}/>\n')
            for form in data['forms']:
                if form != lemma:
                    f.write(f'  <d:index d:value={saxutils.quoteattr(form)}/>\n')
            
            f.write(f'  <h1>{saxutils.escape(lemma)}</h1>\n')
            if data['pos']:
                f.write(f'  <span class="pos">{saxutils.escape(data["pos"])}</span>\n')
            if data['phonetic']:
                f.write(f'  <span class="phonetic">/{saxutils.escape(data["phonetic"])}/</span>\n')
            if data['root']:
                f.write(f'  <div class="root">Root: {saxutils.escape(data["root"])}</div>\n')
            
            f.write('  <ol>\n')
            for g in data['glosses']:
                gloss = g.get('gloss', '')
                if gloss:
                    f.write(f'    <li>{saxutils.escape(gloss)}</li>\n')
            f.write('  </ol>\n')
            f.write('</d:entry>\n')
            
        f.write('</d:dictionary>\n')
    print("Done!")

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description='Convert upstream Gabra BSON to Apple Dictionary XML')
    parser.add_argument('--data-dir', type=Path, default=root / 'data/gabra')
    parser.add_argument('--output', type=Path, default=root / 'macos/Gabra.xml')
    args = parser.parse_args()
    generate_dict(args.data_dir, args.output)
