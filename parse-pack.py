import struct
import zlib
import sys

def read_object_header(data, offset):
    """Git 객체의 타입과 사이즈를 해석하는 함수"""
    c = data[offset]
    offset += 1

    type_id = (c >> 4) & 0x07
    size = c & 0x0F
    shift = 4

    while c & 0x80:
        c = data[offset]
        offset += 1
        size |= (c & 0x7F) << shift
        shift += 7

    return type_id, size, offset

def get_type_name(type_id):
    return {
        1: "commit",
        2: "tree",
        3: "blob",
        4: "tag",
        6: "ofs_delta",
        7: "ref_delta"
    }.get(type_id, f"unknown({type_id})")

def parse_packfile(filename):
    with open(filename, "rb") as f:
        data = f.read()

    offset = 0

    # 헤더 검증
    if data[offset:offset+4] != b"PACK":
        raise Exception("Not a valid Git pack file.")
    offset += 4

    version = struct.unpack(">I", data[offset:offset+4])[0]
    offset += 4

    num_objects = struct.unpack(">I", data[offset:offset+4])[0]
    offset += 4

    print(f"PACK version: {version}, objects: {num_objects}")
    print()

    for i in range(num_objects):
        obj_offset = offset
        type_id, size, offset = read_object_header(data, offset)
        type_name = get_type_name(type_id)

        if type_name in ("ofs_delta", "ref_delta"):
            print(f"[{i+1}] Skipping delta object at offset {obj_offset}")
            # delta는 헤더 이후에 delta-specific 데이터가 있음 (건너뜀)
            if type_name == "ofs_delta":
                # read offset encoding
                while True:
                    b = data[offset]
                    offset += 1
                    if not (b & 0x80):
                        break
            else:
                offset += 20  # SHA-1

        # 압축된 데이터 추출
        decompress = zlib.decompressobj()
        try:
            decompressed = decompress.decompress(data[offset:])
            print(decompressed)
            consumed = len(data[offset:]) - len(decompress.unused_data)
            offset += consumed
        except Exception as e:
            print(f"[{i+1}] Error decompressing object at {obj_offset}: {e}")
            break

        print(f"[{i+1}] Type: {type_name:<10} Size: {size} Offset: {obj_offset}")

    # 마지막 SHA-1 체크섬
    trailer = data[-20:]
    print("\nPackfile SHA-1 trailer:", trailer.hex())

# 사용 예시
# parse_packfile(".git/objects/pack/pack-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.pack")


# 예시 실행
parse_packfile(sys.argv[1])
