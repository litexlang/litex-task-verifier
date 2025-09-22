"""csv_utils.py

Small CSV helper utilities using stdlib csv and optional pandas helpers.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Optional, Iterable


def export_csv_dicts(
    path: str | Path,
    rows: Iterable[Dict[str, str]],
    fieldnames: Optional[Iterable[str]] = None,
    encoding: str = "utf-8",
    delimiter: str = ",",
    write_mode: str = "w",
) -> None:
    """Write an iterable of dict rows to CSV.

    - `fieldnames`: explicit header order. If None, the header is inferred from the
      first row's keys (iteration will consume one row to infer).
    - `rows`: iterable of dict-like rows (e.g., list[dict] or generator)
    - `write_mode`: 'w' (overwrite) or 'a' (append)
    """
    from typing import Iterable

    path = Path(path)
    # Ensure parent exists
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

    it = iter(rows)
    try:
        first = next(it)
    except StopIteration:
        # nothing to write; create empty file with headers if provided
        with path.open(write_mode, encoding=encoding, newline="") as fh:
            if fieldnames:
                writer = csv.DictWriter(fh, fieldnames=list(fieldnames), delimiter=delimiter)
                writer.writeheader()
        return

    # Determine fieldnames and convert to concrete list for csv.DictWriter
    if fieldnames is None:
        # Preserve insertion order of keys from the first row
        fieldnames = list(first.keys())

    fieldnames_list = list(fieldnames)

    with path.open(write_mode, encoding=encoding, newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames_list, delimiter=delimiter)
        # If overwriting, write header. If appending, only write header if file empty
        if write_mode == "w":
            writer.writeheader()
        else:
            # append mode: write header if file is empty
            try:
                is_empty = path.stat().st_size == 0
            except Exception:
                is_empty = True
            if is_empty:
                writer.writeheader()

        # write the first row and the rest
        writer.writerow(first)
        for row in it:
            writer.writerow(row)


def load_csv_dicts(
    path: str | Path, encoding: str = "utf-8", delimiter: Optional[str] = None
) -> List[Dict[str, str]]:
    """Load a CSV into a list of dicts (uses header row).

    - auto-detects delimiter if `delimiter` is None.
    - returns list of rows as dictionaries: [{header: value, ...}, ...]
    """
    path = Path(path)
    with path.open("r", encoding=encoding, newline="") as fh:
        sample = fh.read(8192)
        fh.seek(0)
        if delimiter is None:
            try:
                dialect = csv.Sniffer().sniff(sample)
                delimiter = dialect.delimiter
            except csv.Error:
                delimiter = ","
        reader = csv.DictReader(fh, delimiter=delimiter)
        return [row for row in reader]
