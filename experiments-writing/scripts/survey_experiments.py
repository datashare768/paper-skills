"""Batch-locate the Datasets / Baselines / Metrics sections inside already
extracted reference paper text files (papers/<slug>/text.md), to speed up the
experiment-setup survey step.

Usage:
    python survey_experiments.py <papers_dir> [--context 6]

<papers_dir> is expected to contain one subdirectory per paper, each holding a
text.md produced by idea-and-method-writing/scripts/extract_pdf.py.
"""
import argparse
import os
import re

KEYWORDS = re.compile(r"Dataset|Baseline|Metric", re.IGNORECASE)


def survey(papers_dir: str, context: int) -> None:
    for entry in sorted(os.listdir(papers_dir)):
        text_path = os.path.join(papers_dir, entry, "text.md")
        if not os.path.isfile(text_path):
            continue

        with open(text_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        print(f"\n=== {entry} ===")
        matched_any = False
        i = 0
        while i < len(lines):
            if KEYWORDS.search(lines[i]):
                matched_any = True
                start = max(0, i - 1)
                end = min(len(lines), i + context)
                for j in range(start, end):
                    marker = ">" if j == i else " "
                    print(f"{marker}{j + 1:5d}| {lines[j].rstrip()}")
                print("  ...")
                i = end
            else:
                i += 1
        if not matched_any:
            print("  (no Dataset/Baseline/Metric keyword found; inspect text.md manually)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("papers_dir")
    parser.add_argument("--context", type=int, default=6)
    args = parser.parse_args()
    survey(args.papers_dir, args.context)
