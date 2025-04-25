import hashlib
import sys
import os

def git_hash_object(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()

    # Git은 "blob <size>\0<내용>" 포맷으로 해시
    header = f"blob {len(content)}\0".encode('utf-8')
    store = header + content

    sha1 = hashlib.sha1(store).hexdigest()
    return sha1

# 예시 사용
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python git-hash.py <파일경로>")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"파일이 존재하지 않습니다: {path}")
        sys.exit(1)

    hash_val = git_hash_object(path)
    print(f"Git SHA-1: {hash_val}")
