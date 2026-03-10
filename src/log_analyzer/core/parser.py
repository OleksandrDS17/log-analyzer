from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path


def read_lines(path: Path) -> Iterator[str]:
    """Read a log file line by line in a memory-efficient way."""
    with path.open("r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            yield line.rstrip("\n")
