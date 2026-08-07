"""Split a wide demo_main_results.csv (columns "<Dataset>_<horizon>_<metric>")
produced by generate_demo_results.py into one CSV per dataset, with columns
"<horizon>_<metric>", ready for build_latex_table.py.

Usage:
    python split_by_dataset.py demo_main_results.csv --datasets PEMS03 PEMS04 ... --out-dir results/
"""
import argparse
import csv
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("--datasets", nargs="+", required=True)
    parser.add_argument("--out-dir", default=".")
    parser.add_argument("--prefix", default="demo_")
    args = parser.parse_args()

    with open(args.csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    os.makedirs(args.out_dir, exist_ok=True)
    for ds in args.datasets:
        ds_prefix = f"{ds}_"
        cols = [c for c in rows[0].keys() if c.startswith(ds_prefix)]
        out_path = os.path.join(args.out_dir, f"{args.prefix}{ds.replace('-', '')}.csv")
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["model"] + [c[len(ds_prefix):] for c in cols])
            for r in rows:
                writer.writerow([r["model"]] + [r[c] for c in cols])
        print(f"-> {out_path}")


if __name__ == "__main__":
    main()
