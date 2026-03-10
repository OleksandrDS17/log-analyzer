from __future__ import annotations

from collections import Counter

from log_analyzer.models import Match


def summarize_matches(matches: list[Match]) -> dict[str, int]:
    counter = Counter(match.tag for match in matches)
    return dict(counter)
