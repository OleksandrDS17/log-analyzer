#!/usr/bin/env python3
"""
Log Analyzer Tool
-----------------
Lightweight Python utility for parsing and analyzing log files.

Features:
- Handles large log files (stream processing)
- Filters by keywords, severity, or regex patterns
- Detects recurring errors
- Generates summary statistics
- Extracts relevant entries

Usage examples:
  python log_analyzer.py app.log
  python log_analyzer.py app.log --keyword ERROR
  python log_analyzer.py app.log --regex "failed login"
  python log_analyzer.py app.log --summary
"""

import argparse
import re
from collections import Counter
from pathlib import Path
from typing import Iterable, Optional


# -----------------------------
# Core processing functions
# -----------------------------

def read_log_lines(file_path: Path) -> Iterable[str]:
    """Stream log file line by line (memory efficient)."""
    with file_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            yield line.rstrip("\n")


def match_line(
    line: str,
    keyword: Optional[str] = None,
    regex: Optional[re.Pattern] = None,
    severity: Optional[str] = None,
) -> bool:
    """Check whether a log line matches given filters."""

    if keyword and keyword.lower() not in line.lower():
        return False

    if severity and severity.lower() not in line.lower():
        return False

    if regex and not regex.search(line):
        return False

    return True


def analyze_logs(
    file_path: Path,
    keyword: Optional[str],
    regex_pattern: Optional[str],
    severity: Optional[str],
    show_summary: bool,
    top_n: int,
) -> None:
    """Main analysis routine."""

    regex = re.compile(regex_pattern, re.IGNORECASE) if regex_pattern else None

    total_lines = 0
    matched_lines = 0
    error_counter: Counter[str] = Counter()

    print("--- Matching log entries ---")

    for line in read_log_lines(file_path):
        total_lines += 1

        if match_line(line, keyword, regex, severity):
            matched_lines += 1
            print(line)

            # crude recurring error detection
            normalized = normalize_error(line)
            if normalized:
                error_counter[normalized] += 1

    print("\n--- Analysis complete ---")
    print(f"Total lines processed: {total_lines}")
    print(f"Matched lines: {matched_lines}")

    if show_summary:
        print_summary(error_counter, top_n)


# -----------------------------
# Helper utilities
# -----------------------------

def normalize_error(line: str) -> Optional[str]:
    """
    Attempt to normalize error messages so recurring ones can be counted.
    Removes numbers and IDs that typically vary.
    """

    if not any(word in line.lower() for word in ("error", "failed", "exception", "warning")):
        return None

    # remove numbers and hex ids
    normalized = re.sub(r"0x[0-9a-fA-F]+", "<HEX>", line)
    normalized = re.sub(r"\b\d+\b", "<NUM>", normalized)

    # collapse whitespace
    normalized = re.sub(r"\s+", " ", normalized).strip()

    return normalized


def print_summary(counter: Counter[str], top_n: int) -> None:
    """Print most common recurring issues."""

    print("\n--- Top recurring issues ---")

    if not counter:
        print("No recurring errors detected.")
        return

    for msg, count in counter.most_common(top_n):
        print(f"[{count}x] {msg}")


# -----------------------------
# CLI
# -----------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Log Analysis Tool")

    parser.add_argument("logfile", type=Path, help="Path to log file")

    parser.add_argument(
        "--keyword",
        help="Filter lines containing keyword (case-insensitive)",
    )

    parser.add_argument(
        "--regex",
        help="Filter using regular expression",
    )

    parser.add_argument(
        "--severity",
        help="Filter by severity (ERROR, WARNING, INFO, etc.)",
    )

    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show recurring error summary",
    )

    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="Number of top recurring issues to display",
    )

    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    if not args.logfile.exists():
        parser.error(f"File not found: {args.logfile}")

    analyze_logs(
        file_path=args.logfile,
        keyword=args.keyword,
        regex_pattern=args.regex,
        severity=args.severity,
        show_summary=args.summary,
        top_n=args.top,
    )


if __name__ == "__main__":
    main()
