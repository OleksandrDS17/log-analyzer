from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
from .patterns import DEFAULT_PATTERNS

@dataclass
class Match:
    line_no: int
    tag: str
    line: str

def analyze_lines(lines: Iterable[str], patterns=DEFAULT_PATTERNS) -> list[Match]:
    results: list[Match] = []
    for i, line in enumerate(lines, start=1):
        for tag, rx in patterns.items():
            if rx.search(line):
                results.append(Match(i, tag, line.rstrip("\n")))
    return results

def summary(matches: list[Match]) -> dict[str, int]:
    out: dict[str, int] = {}
    for m in matches:
        out[m.tag] = out.get(m.tag, 0) + 1
    return out
