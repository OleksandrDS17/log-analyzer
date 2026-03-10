from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Match:
    line_no: int
    tag: str
    line: str


@dataclass(slots=True)
class AnalysisResult:
    total_lines: int
    matches: list[Match]
