import hashlib
from pathlib import Path

def generate_sha256(file_path: str) -> str:
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()

def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()