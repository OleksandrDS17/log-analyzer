from __future__ import annotations

import argparse
from pathlib import Path

from log_analyzer.core import DEFAULT_PATTERNS, analyze_lines, read_lines, summarize_matches


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="log-analyzer",
        description="Analyze log files for common patterns.",
    )
    parser.add_argument("path", help="Path to log file")
    parser.add_argument("--show", type=int, default=20, help="Show first N matches")
    parser.add_argument("--summary", action="store_true", help="Print summary counts")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    path = Path(args.path)

    if not path.exists():
        parser.error(f"File not found: {path}")

    if not path.is_file():
        parser.error(f"Not a file: {path}")

    lines = read_lines(path)
    result = analyze_lines(lines, DEFAULT_PATTERNS)

    if args.summary:
        summary = summarize_matches(result.matches)
        for tag, count in sorted(summary.items(), key=lambda item: (-item[1], item[0])):
            print(f"{tag}: {count}")

    for match in result.matches[: args.show]:
        print(f"{match.line_no:>6} [{match.tag}] {match.line}")
