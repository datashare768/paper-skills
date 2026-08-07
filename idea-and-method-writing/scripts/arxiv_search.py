"""Search arXiv via its public API.

Usage:
    python arxiv_search.py "<query>" [--max-results 30] [--category cs.CL]

Prints one result per block: arXiv ID, title, published date, abstract URL, pdf URL.
arXiv metadata does not include venue/conference name -- cross-check top-venue
publication (ACL/NeurIPS/ICLR/ICML/AAAI/WWW/ACMMM, etc.) separately, e.g. via web
search for "<title> site:aclanthology.org" or "<title> openreview".
"""
import argparse
import sys
import urllib.parse
import xml.etree.ElementTree as ET

import requests

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
API_URL = "http://export.arxiv.org/api/query"


def search(query: str, max_results: int = 30, category: str | None = None):
    search_query = f"all:{query}"
    if category:
        search_query = f"cat:{category} AND {search_query}"

    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    resp = requests.get(API_URL, params=params, timeout=30)
    resp.raise_for_status()

    root = ET.fromstring(resp.text)
    entries = root.findall("atom:entry", ATOM_NS)
    if not entries:
        print("No results.")
        return

    for entry in entries:
        arxiv_url = entry.find("atom:id", ATOM_NS).text.strip()
        arxiv_id = arxiv_url.rstrip("/").split("/")[-1]
        title = entry.find("atom:title", ATOM_NS).text.strip().replace("\n", " ")
        published = entry.find("atom:published", ATOM_NS).text.strip()[:10]
        summary = entry.find("atom:summary", ATOM_NS).text.strip().replace("\n", " ")
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"

        print(f"[{arxiv_id}] {title}  ({published})")
        print(f"  abs: {arxiv_url}")
        print(f"  pdf: {pdf_url}")
        print(f"  abstract: {summary[:300]}{'...' if len(summary) > 300 else ''}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--max-results", type=int, default=30)
    parser.add_argument("--category", default=None, help="e.g. cs.CL, cs.CV, cs.LG")
    args = parser.parse_args()

    try:
        search(args.query, args.max_results, args.category)
    except requests.RequestException as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        sys.exit(1)
