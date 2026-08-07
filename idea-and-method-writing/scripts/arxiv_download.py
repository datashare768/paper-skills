"""Download a paper from arXiv by ID: either the PDF, or the LaTeX source
e-print (tar.gz), auto-extracted.

Usage:
    python arxiv_download.py <arxiv_id> --dest <dir> --pdf
    python arxiv_download.py <arxiv_id> --dest <dir> --source

<arxiv_id> examples: 2305.12345 or 2305.12345v2
"""
import argparse
import os
import tarfile
import gzip
import shutil
import io

import requests


def download_pdf(arxiv_id: str, dest: str) -> str:
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    os.makedirs(dest, exist_ok=True)
    path = os.path.join(dest, f"{arxiv_id}.pdf")
    with open(path, "wb") as f:
        f.write(resp.content)
    print(f"PDF saved -> {path}")
    return path


def download_source(arxiv_id: str, dest: str) -> str:
    url = f"https://arxiv.org/e-print/{arxiv_id}"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()

    extract_dir = os.path.join(dest, arxiv_id.replace("/", "_"))
    os.makedirs(extract_dir, exist_ok=True)
    raw = io.BytesIO(resp.content)

    try:
        with tarfile.open(fileobj=raw, mode="r:*") as tar:
            tar.extractall(extract_dir)
        print(f"Source tarball extracted -> {extract_dir}")
    except tarfile.ReadError:
        # Some e-prints are a single gzipped .tex file, not a tar archive.
        raw.seek(0)
        try:
            with gzip.GzipFile(fileobj=raw) as gz:
                data = gz.read()
            single_path = os.path.join(extract_dir, f"{arxiv_id}.tex")
            with open(single_path, "wb") as f:
                f.write(data)
            print(f"Single gzipped source saved -> {single_path}")
        except OSError:
            # Not gzip either: save raw bytes as-is for manual inspection.
            raw_path = os.path.join(extract_dir, f"{arxiv_id}.raw")
            with open(raw_path, "wb") as f:
                f.write(resp.content)
            print(f"Unknown format, saved raw -> {raw_path}")

    return extract_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("arxiv_id")
    parser.add_argument("--dest", default=".")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pdf", action="store_true", help="download PDF only")
    group.add_argument("--source", action="store_true", help="download and extract LaTeX source")
    args = parser.parse_args()

    if args.pdf:
        download_pdf(args.arxiv_id, args.dest)
    else:
        download_source(args.arxiv_id, args.dest)
