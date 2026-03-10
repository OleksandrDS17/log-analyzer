from __future__ import annotations

import re
from collections.abc import Iterable

from log_analyzer.models import AnalysisResult, Match

PatternMap = dict[str, re.Pattern[str]]


def analyze_lines(
    lines: Iterable[str],
    patterns: PatternMap,
) -> AnalysisResult:
    matches: list[Match] = []
    total_lines = 0

    for line_no, line in enumerate(lines, start=1):
        total_lines += 1

        for tag, regex in patterns.items():
            if regex.search(line):
                matches.append(Match(line_no=line_no, tag=tag, line=line))
                break

    return AnalysisResult(total_lines=total_lines, matches=matches)
