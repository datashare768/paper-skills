"""Generate a complete synthetic / Demo result table for ALL baselines + Ours.

Used in Demo mode (personal practice / pipeline simulation, NOT for real
academic publication). Numbers are plausible but NOT from real experiments.

Input JSON files
----------------
datasets.json  -- list of dataset descriptors
baselines.json -- list of baseline descriptors

See --help for format details and examples.

Usage
-----
python generate_demo_results.py \\
    --seed 42 \\
    --datasets datasets.json \\
    --baselines baselines.json \\
    --metrics MAE RMSE MAPE \\
    --lower-is-better MAE RMSE MAPE \\
    --horizons 15min 30min 60min \\
    --ours "Ours" \\
    --out results/demo_main_results.csv

The generated CSV can then be passed to build_latex_table.py.

JSON format examples
--------------------
datasets.json:
[
  {"name": "PEMS03", "difficulty": 0.55},
  {"name": "PEMS04", "difficulty": 0.50},
  {"name": "PEMS07", "difficulty": 0.60},
  {"name": "PEMS08", "difficulty": 0.45}
]
  "difficulty" in [0, 1]: higher = harder = larger absolute error values.

baselines.json:
[
  {"name": "GWNet",   "strength": 0.75},
  {"name": "AGCRN",   "strength": 0.70},
  {"name": "MTGNN",   "strength": 0.72},
  {"name": "DGCRN",   "strength": 0.76},
  {"name": "STPGNN",  "strength": 0.74},
  {"name": "HimNet",  "strength": 0.80},
  {"name": "M3Net",   "strength": 0.79},
  {"name": "STADNN",  "strength": 0.85}
]
  "strength" in [0, 1]: higher = stronger method = lower error / higher accuracy.
  Ours is always generated with strength 0.90 (slightly above the best baseline).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import sys
from typing import Any


# ── Plausible base error ranges per metric (lower-is-better), indexed by
# difficulty = 0 (easy) to 1 (hard). These ranges represent typical values
# seen in traffic/time-series literature; tweak for other tasks.
BASE_RANGES: dict[str, tuple[float, float]] = {
    "MAE":  (10.0, 25.0),
    "RMSE": (18.0, 45.0),
    "MAPE": (7.0,  22.0),
    "MSE":  (50.0, 200.0),
    # Higher-is-better defaults
    "ACC":      (0.70, 0.95),
    "ACCURACY": (0.70, 0.95),
    "F1":       (0.65, 0.92),
    "AUC":      (0.75, 0.97),
    "NDCG":     (0.30, 0.65),
    "HR":       (0.35, 0.75),
    "RECALL":   (0.30, 0.70),
}


def is_higher_better(metric: str, hib_set: set[str]) -> bool:
    return metric.upper() in hib_set


def base_value(metric: str, difficulty: float, hib_set: set[str], rng: random.Random,
               override_ranges: dict[str, tuple[float, float]] | None = None) -> float:
    key = metric.upper()
    if override_ranges and key in override_ranges:
        lo, hi = override_ranges[key]
    else:
        lo, hi = BASE_RANGES.get(key, (0.5, 5.0))
    if is_higher_better(metric, hib_set):
        # harder dataset → lower accuracy
        v = hi - difficulty * (hi - lo) + rng.uniform(-0.005, 0.005) * (hi - lo)
    else:
        # harder dataset → higher error
        v = lo + difficulty * (hi - lo) + rng.uniform(-0.02, 0.02) * (hi - lo)
    return max(lo * 0.5, v)


def strength_factor(strength: float, higher: bool) -> float:
    """Convert strength [0,1] to a multiplicative adjustment.
    stronger method → lower error (lower-is-better) / higher score (higher-is-better).
    """
    # deviation > 0 when strength > 0.85 (ref baseline), < 0 when weaker
    deviation = (strength - 0.85) * 0.20
    if higher:
        return 1.0 + deviation   # stronger → larger value
    else:
        return 1.0 - deviation   # stronger → smaller error


def horizon_factor(h_idx: int, n_horizons: int, higher: bool, rng: random.Random) -> float:
    """Later horizons are harder: higher error / lower accuracy."""
    base = 1.0 + h_idx * rng.uniform(0.06, 0.12)
    if higher:
        return 1.0 / base
    return base


def metric_consistency(metric: str, row: dict[str, Any], rng: random.Random) -> float:
    """Ensure RMSE >= MAE when both present (add a small positive margin)."""
    m = metric.upper()
    if m == "RMSE" and "MAE" in row:
        mae_v = row["MAE"]
        # RMSE must be at least MAE
        return max(row.get("RMSE_raw", 0.0), mae_v * rng.uniform(1.05, 1.50))
    return row.get(f"{metric}_raw", 0.0)


def generate(
    datasets: list[dict],
    baselines: list[dict],
    metrics: list[str],
    horizons: list[str],
    ours_name: str,
    hib_set: set[str],
    seed: int,
) -> list[dict]:
    rng = random.Random(seed)
    rows: list[dict] = []

    # Ours is slightly stronger than the best baseline
    best_strength = max(b["strength"] for b in baselines)
    ours_strength = min(1.0, best_strength + rng.uniform(0.04, 0.09))

    all_methods = baselines + [{"name": ours_name, "strength": ours_strength}]

    for method in all_methods:
        row: dict[str, Any] = {"model": method["name"]}
        for ds in datasets:
            for h_idx, horizon in enumerate(horizons):
                metric_vals: dict[str, float] = {}
                ds_override = None
                if ds.get("base_ranges"):
                    ds_override = {k.upper(): tuple(v) for k, v in ds["base_ranges"].items()}
                for metric in metrics:
                    higher = is_higher_better(metric, hib_set)
                    bv = base_value(metric, ds["difficulty"], hib_set, rng, ds_override)
                    sf = strength_factor(method["strength"], higher)
                    hf = horizon_factor(h_idx, len(horizons), higher, rng)
                    noise = rng.uniform(-0.015, 0.015)
                    if higher:
                        v = bv * sf / hf * (1 + noise)
                        v = min(v, 0.9999)
                    else:
                        v = bv * sf * hf * (1 + noise)
                        v = max(v, 0.01)
                    metric_vals[metric] = v

                # enforce RMSE >= MAE
                if "MAE" in metric_vals and "RMSE" in metric_vals:
                    if metric_vals["RMSE"] < metric_vals["MAE"]:
                        metric_vals["RMSE"] = metric_vals["MAE"] * rng.uniform(1.08, 1.45)

                for metric, v in metric_vals.items():
                    col = f"{ds['name']}_{horizon}_{metric}"
                    row[col] = round(v, 2)
        rows.append(row)

    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--datasets", required=True,
                        help="JSON file with list of {name, difficulty} dicts")
    parser.add_argument("--baselines", required=True,
                        help="JSON file with list of {name, strength} dicts")
    parser.add_argument("--metrics", nargs="+", default=["MAE", "RMSE", "MAPE"],
                        help="Metric names in the order they appear per horizon")
    parser.add_argument("--lower-is-better", nargs="*", default=None,
                        help="Metric names that are lower-is-better (default: all)")
    parser.add_argument("--horizons", nargs="+", default=["15min", "30min", "60min"])
    parser.add_argument("--ours", default="Ours")
    parser.add_argument("--out", default="demo_main_results.csv")
    args = parser.parse_args()

    with open(args.datasets, encoding="utf-8") as f:
        datasets = json.load(f)
    with open(args.baselines, encoding="utf-8") as f:
        baselines = json.load(f)

    # Determine higher-is-better set
    if args.lower_is_better is not None:
        lib = {m.upper() for m in args.lower_is_better}
        hib_set = {m.upper() for m in args.metrics if m.upper() not in lib}
    else:
        # default: assume all metrics not in BASE_RANGES higher-is-better keys are lower
        hib_defaults = {"ACC", "ACCURACY", "F1", "AUC", "NDCG", "HR", "RECALL"}
        hib_set = {m.upper() for m in args.metrics if m.upper() in hib_defaults}

    rows = generate(
        datasets=datasets,
        baselines=baselines,
        metrics=args.metrics,
        horizons=args.horizons,
        ours_name=args.ours,
        hib_set=hib_set,
        seed=args.seed,
    )

    os.makedirs(os.path.dirname(args.out) if os.path.dirname(args.out) else ".", exist_ok=True)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    fieldnames = list(rows[0].keys())
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Written {len(rows)} rows to {args.out}", file=sys.stderr)
    print(f"Seed={args.seed}. All values are SYNTHETIC DEMO PLACEHOLDERS.", file=sys.stderr)


if __name__ == "__main__":
    main()
