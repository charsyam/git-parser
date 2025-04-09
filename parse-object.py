import zlib
import sys

def read_git_object(file_path):
    """Read and decompress a Git object from the given file path."""
    with open(file_path, 'rb') as f:
        compressed_data = f.read()
    
    # Decompress the data
#    import pdb; pdb.set_trace()
    decompressed_data = zlib.decompress(compressed_data)
    
    # Split header and content
    header, content = decompressed_data.split(b'\x00', 1)
    
    # Extract type and size from the header
    obj_type, obj_size = header.split(b' ', 1)
    
    return obj_type.decode('utf-8'), int(obj_size.decode('utf-8')), content

def print_blob_content(content):
    """Print the content of a blob object."""
    try:
        print("\nBlob Content:\n")
        print(content.decode('utf-8'))
    except UnicodeDecodeError:
        print("\nBinary Content (not displayable as text)\n")

def print_commit_content(content):
    """Print the content of a commit object."""
    print("\nCommit Content:\n")
    print(content.decode('utf-8'))

def print_tree_content(content):
    """Print the content of a tree object."""
    print("\nTree Content:\n")
    index = 0
    while index < len(content):
        mode_end = content.find(b' ', index)
        mode = content[index:mode_end].decode('utf-8')
        
        name_end = content.find(b'\x00', mode_end)
        name = content[mode_end + 1:name_end].decode('utf-8')
        
        sha1 = content[name_end + 1:name_end + 21]  # SHA-1 is 20 bytes
        sha1_hex = sha1.hex()
        
        print(f"{mode} {name} {sha1_hex}")
        index = name_end + 21

def print_tag_content(content):
    """Print the content of a tag object."""
    print("\nTag Content:\n")
    print(content.decode('utf-8'))

def main(file_path):
    obj_type, obj_size, content = read_git_object(file_path)
    print(f"Object Type: {obj_type}")
    print(f"Object Size: {obj_size} bytes")

    if obj_type == 'blob':
        print_blob_content(content)
    elif obj_type == 'commit':
        print_commit_content(content)
    elif obj_type == 'tree':
        print_tree_content(content)
    elif obj_type == 'tag':
        print_tag_content(content)
    else:
        print("\nUnknown Git object type.")

# Example usage
# Replace 'path_to_git_object' with your actual .git/objects path
main(sys.argv[1])
