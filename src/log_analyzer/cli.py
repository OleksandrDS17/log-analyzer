import argparse
from pathlib import Path
from .analyzer import analyze_lines, summary

def main():
    p = argparse.ArgumentParser(prog="log-analyzer", description="Analyze log files for common patterns.")
    p.add_argument("path", help="Path to log file")
    p.add_argument("--show", type=int, default=20, help="Show first N matches")
    p.add_argument("--summary", action="store_true", help="Print summary counts")
    args = p.parse_args()

    path = Path(args.path)
    with path.open("r", errors="ignore") as f:
        matches = analyze_lines(f)

    if args.summary:
        s = summary(matches)
        for k, v in sorted(s.items(), key=lambda x: (-x[1], x[0])):
            print(f"{k}: {v}")

    for m in matches[: args.show]:
        print(f"{m.line_no:>6} [{m.tag}] {m.line}")
