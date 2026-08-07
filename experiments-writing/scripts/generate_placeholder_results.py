"""Generate a scientifically-plausible PLACEHOLDER result row for "our method",
given a CSV of real baseline numbers, for ANY task/metric type (time-series
forecasting error metrics, classification accuracy/F1, ranking metrics, etc.) --
this is not specific to traffic/time-series tasks.

This is ONLY for non-publication practice/simulation projects where the user has
explicitly stated the results are not for real academic submission. The generated
row must always be disclosed in the paper/table caption as a placeholder pending
real experiments -- this script does not, and must not, alter the real baseline
numbers themselves.

Input CSV format:
    model,col1,col2,col3,...
    BaselineA,14.32,24.83,13.91,...
    BaselineB,14.82,25.33,14.70,...
    ...

Each column is independently treated as lower-is-better or higher-is-better; pass
column names (as they appear in the header) to --higher-is-better for metrics like
accuracy/F1/AUC where a bigger number is better. Every other column defaults to
lower-is-better (errors, loss, latency, etc.).

Usage:
    python generate_placeholder_results.py baselines.csv --seed 42 \
        --min-improve 0.05 --max-improve 0.10 --name Ours \
        --higher-is-better accuracy f1

Output: prints the full table (all real baseline rows unchanged, plus the new
placeholder row) as CSV to stdout.
"""
import argparse
import csv
import random
import sys


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--min-improve", type=float, default=0.05)
    parser.add_argument("--max-improve", type=float, default=0.10)
    parser.add_argument("--name", default="Ours")
    parser.add_argument(
        "--higher-is-better",
        nargs="*",
        default=[],
        help="column names (from the CSV header) where a larger value is better",
    )
    args = parser.parse_args()

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    with open(args.csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    metric_cols = header[1:]
    higher_is_better = set(args.higher_is_better)
    unknown = higher_is_better - set(metric_cols)
    if unknown:
        print(f"Warning: --higher-is-better names not found in header: {unknown}", file=sys.stderr)

    n_cols = len(metric_cols)
    values = [[float(cell) for cell in row[1:]] for row in rows]

    rng = random.Random(args.seed)
    ours = []
    for c, col_name in enumerate(metric_cols):
        col_values = [values[r][c] for r in range(len(values))]
        pct = rng.uniform(args.min_improve, args.max_improve)
        if col_name in higher_is_better:
            best = max(col_values)
            ours.append(round(best * (1 + pct), 2))
        else:
            best = min(col_values)
            ours.append(round(best * (1 - pct), 2))

    writer = csv.writer(sys.stdout)
    writer.writerow(header)
    for row in rows:
        writer.writerow(row)
    writer.writerow([args.name] + [f"{v:.2f}" for v in ours])

    print(
        f"\n# seed={args.seed}, improvement range=[{args.min_improve:.0%}, {args.max_improve:.0%}]"
        f" over the per-column best real baseline. Mark this row as a placeholder in the caption.",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
