import struct
import hashlib

def read_index(path='.git/index'):
    with open(path, 'rb') as f:
        data = f.read()

    header = data[:12]
    signature, version, num_entries = struct.unpack('!4sII', header)

    if signature != b'DIRC':
        raise ValueError("Not a valid Git index file")

    print(f"Index Version: {version}, Entries: {num_entries}")

    offset = 12
    entries = []

    for _ in range(num_entries):
        fields = struct.unpack('!10I20sH', data[offset:offset + 62])
        entry = {
            'ctime': fields[0],
            'mtime': fields[2],
            'dev': fields[4],
            'ino': fields[5],
            'mode': fields[6],
            'uid': fields[7],
            'gid': fields[8],
            'size': fields[9],
            'sha1': fields[10].hex(),
            'flags': fields[11],
        }

        name_len = entry['flags'] & 0x0FFF
        path_end = offset + 62 + name_len
        path = data[offset + 62:path_end].split(b'\x00')[0].decode()
        entry['path'] = path

        entries.append(entry)

        total_entry_len = ((path_end - offset + 8) // 8) * 8  # padding to multiple of 8
        offset += total_entry_len

    for e in entries:
        print(f"{e['mode']:06o} {e['sha1']} {e['size']}\t{e['path']}")

    # Checksum (last 20 bytes)
    index_data = data[:-20]
    actual_checksum = data[-20:]
    expected_checksum = hashlib.sha1(index_data).digest()

    if expected_checksum != actual_checksum:
        print("⚠️  WARNING: Index checksum mismatch!")
    else:
        print("✅ Index checksum verified.")

# 실행
read_index()

