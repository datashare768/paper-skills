"""Extract the References section from parsed paper text files
(papers/<slug>/text.md) and output a deduplicated JSON list of raw
reference strings ready for BibTeX lookup.

Usage:
    python extract_references.py <papers_dir> --out raw_refs.json [--min-year 2015]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from difflib import SequenceMatcher


# Patterns that mark the start of a References section
_REF_HEADER = re.compile(
    r"^\s*(?:references?|bibliography|works cited)\s*$",
    re.IGNORECASE,
)

# Numbered reference: "[1] Smith, J. ..." or "1. Smith, J. ..."
_NUM_ENTRY = re.compile(r"^\s*[\[\(]?\d{1,3}[\]\).]?\s+\S")

# Author-year inline: "Smith, J. (2023). Title. Venue."
_AUTHOR_YEAR = re.compile(r"^[A-Z][a-z]+,?\s+[A-Z].*?\(\d{4}\)")

# Year range filter
_YEAR_RE = re.compile(r"\b(19[89]\d|20\d{2})\b")


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def extract_from_file(path: str, min_year: int) -> list[str]:
    with open(path, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    # Find last occurrence of a References header (papers often have
    # "References" mid-text for inline section headers too)
    ref_start = -1
    for i in range(len(lines) - 1, -1, -1):
        if _REF_HEADER.match(lines[i].strip()):
            ref_start = i + 1
            break

    if ref_start == -1:
        # Fallback: look for a dense block of year-containing lines in the last 25%
        tail = lines[int(len(lines) * 0.75):]
        ref_start = int(len(lines) * 0.75)
        lines = tail

    ref_lines = lines[ref_start:]

    # Collect entries: group consecutive non-blank lines into one entry
    entries: list[str] = []
    current: list[str] = []
    for line in ref_lines:
        stripped = line.strip()
        if not stripped:
            if current:
                entries.append(" ".join(current).strip())
                current = []
        else:
            # New numbered entry resets the current buffer
            if current and (_NUM_ENTRY.match(stripped) or _AUTHOR_YEAR.match(stripped)):
                entries.append(" ".join(current).strip())
                current = []
            current.append(stripped)
    if current:
        entries.append(" ".join(current).strip())

    # Filter: must contain a 4-digit year >= min_year and be long enough
    filtered: list[str] = []
    for e in entries:
        years = [int(y) for y in _YEAR_RE.findall(e)]
        if years and max(years) >= min_year and len(e) > 30:
            filtered.append(e)

    return filtered


def deduplicate(entries: list[str]) -> list[str]:
    unique: list[str] = []
    for e in entries:
        if not any(similarity(e, u) > 0.80 for u in unique):
            unique.append(e)
    return unique


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("papers_dir")
    parser.add_argument("--out", default="raw_refs.json")
    parser.add_argument("--min-year", type=int, default=2015,
                        help="Exclude references older than this year")
    args = parser.parse_args()

    all_entries: list[str] = []
    for entry in sorted(os.listdir(args.papers_dir)):
        text_path = os.path.join(args.papers_dir, entry, "text.md")
        if not os.path.isfile(text_path):
            continue
        refs = extract_from_file(text_path, args.min_year)
        print(f"  {entry}: {len(refs)} references found", file=sys.stderr)
        all_entries.extend(refs)

    unique = deduplicate(all_entries)
    print(f"\nTotal after dedup: {len(unique)}", file=sys.stderr)

    out = [{"raw": r, "title": "", "authors": "", "year": ""} for r in unique]
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Written to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
