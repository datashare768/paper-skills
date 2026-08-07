"""Query CrossRef API to find proper BibTeX entries for extracted raw references.

Input : JSON produced by extract_references.py  (list of {raw, title, ...})
Output: .bib file with @article / @inproceedings / @misc entries.
        Entries that could not be confidently matched are marked with % VERIFY.

Usage:
    python fetch_bibtex.py raw_refs.json --out references.bib --target 45

Requirements: pip install requests thefuzz python-Levenshtein
(thefuzz is optional; falls back to difflib if not installed)
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
from difflib import SequenceMatcher
from typing import Any, Optional

import requests

try:
    from thefuzz import fuzz  # type: ignore
    _FUZZY = True
except ImportError:
    _FUZZY = False

CROSSREF_URL = "https://api.crossref.org/works"
HEADERS = {"User-Agent": "paper-skills-bib-fetcher/1.0 (mailto:noreply@example.com)"}
_YEAR_RE = re.compile(r"\b(19[89]\d|20\d{2})\b")
_NONALPHA = re.compile(r"[^a-z0-9\s]")


def _normalize(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return _NONALPHA.sub(" ", s.lower()).strip()


def _title_similarity(a: str, b: str) -> float:
    na, nb = _normalize(a), _normalize(b)
    if _FUZZY:
        return fuzz.token_sort_ratio(na, nb) / 100.0
    return SequenceMatcher(None, na, nb).ratio()


def _extract_title_from_raw(raw: str) -> str:
    """Best-effort title extraction from a raw reference string."""
    # Remove leading [N] or "N." numbering
    raw = re.sub(r"^[\[\(]?\d{1,3}[\]\).]?\s*", "", raw).strip()
    # Remove leading author block up to first ". " or ". \u201c" or year
    # Heuristic: title often starts after "Year." or after first sentence
    m = re.search(r"\(?\d{4}\)?[.,]?\s+(.+?)(?:\.|$)", raw)
    if m:
        candidate = m.group(1).strip()
        # Stop at venue indicators: "In ", "Proceedings", "arXiv", journal name
        candidate = re.split(r"\.\s+(?:In |Proceedings|arXiv|Journal)", candidate)[0]
        if len(candidate) > 15:
            return candidate
    # Fallback: take the middle 40% of the string
    words = raw.split()
    start = max(0, len(words) // 5)
    end = min(len(words), 4 * len(words) // 5)
    return " ".join(words[start:end])


def _crossref_query(title: str) -> Optional[dict[str, Any]]:
    try:
        r = requests.get(
            CROSSREF_URL,
            params={"query.title": title, "rows": 3, "select": "DOI,title,author,published,type,container-title,publisher"},
            headers=HEADERS,
            timeout=15,
        )
        r.raise_for_status()
        items = r.json().get("message", {}).get("items", [])
        for item in items:
            cr_title = " ".join(item.get("title", [""]))
            sim = _title_similarity(title, cr_title)
            if sim > 0.78:
                return item
        return None
    except Exception as exc:  # noqa: BLE001
        print(f"    CrossRef error: {exc}", file=sys.stderr)
        return None


def _make_key(authors: list[dict], year: int, title: str) -> str:
    first_author = authors[0].get("family", "Unknown") if authors else "Unknown"
    first_word = re.sub(r"[^a-zA-Z]", "", title.split()[0]) if title.split() else "paper"
    return f"{first_author}{year}{first_word}"


def _format_authors(authors: list[dict]) -> str:
    parts = []
    for a in authors[:6]:
        family = a.get("family", "")
        given = a.get("given", "")
        parts.append(f"{family}, {given}" if given else family)
    if len(authors) > 6:
        parts.append("others")
    return " and ".join(parts)


def _item_to_bibtex(item: dict, key: str, verified: bool) -> str:
    title = " ".join(item.get("title", ["Unknown Title"]))
    authors = item.get("author", [])
    author_str = _format_authors(authors)
    pub = item.get("published", {}).get("date-parts", [[0]])[0]
    year = pub[0] if pub else 0
    doi = item.get("DOI", "")
    item_type = item.get("type", "journal-article")
    container = " ".join(item.get("container-title", []))

    if item_type in ("proceedings-article", "paper-conference"):
        entry_type = "inproceedings"
        venue_field = f"  booktitle = {{{container}}},"
    else:
        entry_type = "article"
        venue_field = f"  journal   = {{{container}}},"

    verify_note = "" if verified else "  % VERIFY: low confidence match -- please check manually\n"
    doi_field = f"  doi       = {{{doi}}}," if doi else ""

    return (
        f"@{entry_type}{{{key},\n"
        f"{verify_note}"
        f"  author    = {{{author_str}}},\n"
        f"  title     = {{{{{title}}}}},\n"
        f"  year      = {{{year}}},\n"
        f"{venue_field}\n"
        f"{doi_field}\n"
        f"}}\n"
    )


def _raw_to_misc(raw: str, idx: int) -> str:
    years = _YEAR_RE.findall(raw)
    year = years[0] if years else "0000"
    key = f"ref{idx}_{year}"
    return (
        f"@misc{{{key},\n"
        f"  % VERIFY: could not match via CrossRef -- fill in manually\n"
        f"  note      = {{{raw[:200]}}},\n"
        f"  year      = {{{year}}},\n"
        f"}}\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_path")
    parser.add_argument("--out", default="references.bib")
    parser.add_argument("--target", type=int, default=45,
                        help="Target number of BibTeX entries in the output")
    parser.add_argument("--max-query", type=int, default=80,
                        help="Maximum number of CrossRef queries to make")
    parser.add_argument("--delay", type=float, default=0.5,
                        help="Seconds between CrossRef requests (be polite)")
    args = parser.parse_args()

    with open(args.json_path, encoding="utf-8") as f:
        raw_refs: list[dict] = json.load(f)

    entries: list[str] = []
    seen_keys: set[str] = set()
    seen_dois: set[str] = set()
    queried = 0

    print(f"Fetching BibTeX for up to {min(args.max_query, len(raw_refs))} references...",
          file=sys.stderr)

    for i, ref in enumerate(raw_refs[:args.max_query]):
        if len(entries) >= args.target:
            break
        raw = ref.get("raw", "")
        title_guess = _extract_title_from_raw(raw)
        if len(title_guess) < 10:
            entries.append(_raw_to_misc(raw, i))
            continue

        print(f"  [{i+1}] Querying: {title_guess[:60]}...", file=sys.stderr)
        item = _crossref_query(title_guess)
        queried += 1
        time.sleep(args.delay)

        if item is None:
            entries.append(_raw_to_misc(raw, i))
            continue

        doi = item.get("DOI", "")
        if doi and doi in seen_dois:
            print(f"    (duplicate DOI, skipping)", file=sys.stderr)
            continue
        if doi:
            seen_dois.add(doi)

        authors = item.get("author", [])
        pub = item.get("published", {}).get("date-parts", [[0]])[0]
        year = pub[0] if pub else 0
        title = " ".join(item.get("title", [""]))
        key = _make_key(authors, year, title)
        base_key = key
        suffix = 2
        while key in seen_keys:
            key = f"{base_key}{suffix}"
            suffix += 1
        seen_keys.add(key)

        cr_title = " ".join(item.get("title", [""]))
        verified = _title_similarity(title_guess, cr_title) > 0.88
        entries.append(_item_to_bibtex(item, key, verified))

    # Pad with @misc for remaining raw refs if still below target
    misc_idx = queried
    for ref in raw_refs[args.max_query:]:
        if len(entries) >= args.target:
            break
        entries.append(_raw_to_misc(ref.get("raw", ""), misc_idx))
        misc_idx += 1

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(f"% Generated by fetch_bibtex.py -- {len(entries)} entries\n")
        f.write("% Entries marked with % VERIFY must be checked manually.\n\n")
        f.writelines(e + "\n" for e in entries)

    verify_count = sum(1 for e in entries if "% VERIFY" in e)
    print(f"\nWrote {len(entries)} entries to {args.out}", file=sys.stderr)
    print(f"  {verify_count} entries need manual verification (% VERIFY)", file=sys.stderr)


if __name__ == "__main__":
    main()
