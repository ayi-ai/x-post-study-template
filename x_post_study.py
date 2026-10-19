import argparse
import csv
import sys
from pathlib import Path

import numpy as np

METRICS = [
    ("Likes", "点赞"),
    ("Bookmarks", "收藏"),
    ("New follows", "新增关注"),
    ("Profile visits", "主页访问"),
]
REQUIRED = ["content_type", "Impressions", *[col for col, _ in METRICS]]
MIN_N = 20


def load_rows(path):
    with Path(path).open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [col for col in REQUIRED if col not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(f"{path}: missing columns: {', '.join(missing)}")
        return list(reader)


def summarize(rows):
    lines = ["content_type,指标,n,每千次曝光中位数,恰好为0的比例"]
    groups = {}
    for row in rows:
        groups.setdefault(row["content_type"], []).append(row)
    for ctype in sorted(groups):
        group = groups[ctype]
        n = len(group)
        imp = np.array([float(row["Impressions"]) for row in group], dtype=np.float64)
        for col, label in METRICS:
            values = np.array([float(row[col]) for row in group], dtype=np.float64)
            zeros = int((values == 0).sum())
            prop = zeros / n
            if n < MIN_N:
                med = ""
            else:
                safe = imp > 0
                rates = np.divide(values, imp, out=np.zeros(n), where=safe) * 1000.0
                med = float(np.median(rates))
            lines.append(f"{ctype},{label},{n},{med},{prop}")
    return lines


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_paths", nargs="+")
    parser.add_argument("--output-prefix", required=True)
    args = parser.parse_args()

    rows = []
    for path in args.csv_paths:
        rows.extend(load_rows(path))
    out = Path(f"{args.output_prefix}-study-metrics.csv")
    out.write_text("\n".join(summarize(rows)) + "\n", encoding="utf-8")
    print(out.resolve())
    return 0


if __name__ == "__main__":
    sys.exit(main())
