"""tmp_hasher.py

Create a tmp directory if it doesn't exist and store files named by the SHA256 hash
of the input string. Exposes a small function and a CLI.
"""

import hashlib
from pathlib import Path


TMP_DIR_NAME = "tmp"


def ensure_tmp_dir(base_path: Path = Path.cwd()) -> Path:
    """Ensure the tmp directory exists under base_path and return its Path."""
    tmp_dir = base_path / TMP_DIR_NAME
    tmp_dir.mkdir(parents=True, exist_ok=True)
    return tmp_dir


def hash_to_filename(s: str, prefix: str = "file_", suffix: str = "") -> str:
    """Return a filename derived from SHA256 of the input string.

    The filename is prefix + first 16 hex chars of the SHA256 digest.
    """
    if not isinstance(s, str):
        raise TypeError("input must be a string")
    h = hashlib.sha256(s.encode("utf-8")).hexdigest()
    return f"{prefix}{h[:16]}{suffix}"


def store_string(
    s: str, base_path: Path = Path.cwd(), prefix: str = "file_", suffix: str = ""
) -> Path:
    """Store the input string into a file named by its hash inside tmp dir.

    Returns the file path and the filename used.
    """
    tmp_dir = ensure_tmp_dir(base_path)
    filename = hash_to_filename(s, prefix=prefix, suffix=suffix)
    file_path = tmp_dir / filename
    # Use atomic write via temporary file then rename
    tmp_file = tmp_dir / (filename + ".tmp")
    with tmp_file.open("w", encoding="utf-8") as f:
        f.write(s)
    tmp_file.replace(file_path)
    return file_path


def read_stored(filename: str, base_path: Path = Path.cwd()) -> str:
    """Read content of a stored file in tmp dir by filename.

    Raises FileNotFoundError if missing.
    """
    file_path = Path(base_path) / TMP_DIR_NAME / filename
    with file_path.open("r", encoding="utf-8") as f:
        return f.read()
