"""Scan parsed reference papers under papers/<slug>/auto/ and build an
inventory of every Table/Figure caption, tagged with a guessed experiment
type, to feed the experiments-enrichment skill's selection step.

Usage
-----
python scan_reference_experiments.py --papers-dir papers --out inventory.json

For each papers/<slug>/auto/<slug>.md this collects:
  - paper title (first "# " heading line)
  - every "Fig./Figure N: ..." caption line found in the markdown body
  - every papers/<slug>/auto/tables/*.md file's first line (table caption)
and assigns a rough type tag via keyword matching (see TAG_RULES below).

Output is a JSON list of {slug, title, kind, ref, caption, tags} records,
sorted by slug, so the agent can quickly cross-reference against the
current project's method.tex / experiments.tex without re-reading full
paper text.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

FIG_CAPTION_RE = re.compile(r"^(Fig(?:ure)?\.?\s*\d+)[:.](.*)$")

# Ordered keyword -> tag rules; first match wins. Extend freely.
TAG_RULES: list[tuple[str, str]] = [
    (r"ablat", "ablation"),
    (r"decompos", "decomposition_analysis"),
    (r"significan|t-test|t test", "statistical_significance"),
    (r"noise|perturbat|robust|missing", "robustness_perturbation"),
    (r"transfer|zero-shot|few-shot|generaliz", "transfer_few_shot"),
    (r"memory|gpu|parameter[s]? and|computation(al)? (cost|efficiency|time)|inference time|training time", "efficiency_memory"),
    (r"sensitivity|hyper-?parameter", "parameter_sensitivity"),
    (r"case study|visuali[sz]ation|qualitative|heatmap|attention", "case_study_visualization"),
    (r"training (process|curve)|validation loss|convergence", "training_curve"),
    (r"framework|architecture|overview", "framework_diagram"),
    (r"main result|performance comparison|result on|comparison of", "main_results"),
    (r"dataset|statistics", "dataset_stats"),
]


def guess_tag(caption: str) -> str:
    low = caption.lower()
    for pattern, tag in TAG_RULES:
        if re.search(pattern, low):
            return tag
    return "other"


def get_title(md_path: str) -> str:
    with open(md_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
    return os.path.basename(md_path)


def scan_paper(slug: str, auto_dir: str) -> list[dict]:
    records: list[dict] = []
    md_path = os.path.join(auto_dir, f"{slug}.md")
    if not os.path.isfile(md_path):
        return records
    title = get_title(md_path)

    with open(md_path, encoding="utf-8") as f:
        for line in f:
            m = FIG_CAPTION_RE.match(line.strip())
            if m:
                caption = m.group(2).strip()
                records.append({
                    "slug": slug, "title": title, "kind": "figure",
                    "ref": m.group(1), "caption": caption,
                    "tag": guess_tag(caption),
                })

    tables_dir = os.path.join(auto_dir, "tables")
    if os.path.isdir(tables_dir):
        for fname in sorted(os.listdir(tables_dir)):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(tables_dir, fname)
            with open(fpath, encoding="utf-8") as f:
                first_line = f.readline().strip().lstrip("#").strip()
            records.append({
                "slug": slug, "title": title, "kind": "table",
                "ref": fname, "caption": first_line,
                "tag": guess_tag(first_line),
            })
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--papers-dir", default="papers")
    parser.add_argument("--out", default="reference_experiment_inventory.json")
    args = parser.parse_args()

    all_records: list[dict] = []
    if not os.path.isdir(args.papers_dir):
        print(f"No such directory: {args.papers_dir}", file=sys.stderr)
        sys.exit(1)

    for slug in sorted(os.listdir(args.papers_dir)):
        auto_dir = os.path.join(args.papers_dir, slug, "auto")
        if os.path.isdir(auto_dir):
            all_records.extend(scan_paper(slug, auto_dir))

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(all_records, f, ensure_ascii=False, indent=2)

    tag_counts: dict[str, int] = {}
    for r in all_records:
        tag_counts[r["tag"]] = tag_counts.get(r["tag"], 0) + 1
    print(f"Scanned {len(set(r['slug'] for r in all_records))} papers, "
          f"{len(all_records)} table/figure captions.", file=sys.stderr)
    print("Tag distribution:", json.dumps(tag_counts, indent=2), file=sys.stderr)


if __name__ == "__main__":
    main()
