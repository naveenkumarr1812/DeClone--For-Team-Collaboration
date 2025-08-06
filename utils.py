import hashlib

def generate_file_hash(file) -> str:
    hasher = hashlib.sha256()
    for chunk in iter(lambda: file.read(4096), b""):
        hasher.update(chunk)
    file.seek(0)  # Reset the file for re-use
    return hasher.hexdigest()
