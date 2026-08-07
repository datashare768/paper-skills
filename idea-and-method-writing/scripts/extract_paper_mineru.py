"""
Structured extraction for PUBLISHED ACADEMIC PDFs, using MinerU.

This is the PRIMARY extraction path for paper-shaped PDFs (double-column
layout, equations, figures with captions, complex tables, long reference
lists). It restores reading order and paper structure, which the generic
PyMuPDF-based `extract_pdf.py` cannot do reliably on multi-column PDFs.

Pipeline:
    1. Copy the source PDF into a short-named temp file (Windows MAX_PATH
       is easily exceeded by the long, descriptive filenames typical of
       downloaded papers combined with MinerU's own nested temp dirs).
    2. Run `mineru -p <pdf> -o <out_dir> -b pipeline` (CPU/GPU auto).
    3. Post-process the result with organize_mineru_output.py:
         - fix common ligature-OCR artifacts (traffic/trafic, etc.)
         - split tables into individual named markdown files
         - reassemble multi-panel figures into individual named images
         - drop uncaptioned / irrelevant image crops

Output layout (under <out_dir>/<paper_slug>/auto/):
    <paper_slug>.md                 full text, reading order restored,
                                     equations inline as LaTeX
    <paper_slug>_content_list.json  structured items (type/bbox/page/caption)
    images/                         all raw cropped images (MinerU original)
    tables/Table<N>_<slug>.md       one file per table
    figures/Fig<N>_<slug>.png       one file per figure (multi-panel merged)

Requirements (one-time setup, see SKILL.md "MinerU 环境搭建"):
    conda create -n mineru_env python=3.11
    conda activate mineru_env
    pip install -U "mineru[pipeline]" six pandas tabulate lxml beautifulsoup4 pillow
    setx MINERU_MODEL_SOURCE modelscope   # or: $env:MINERU_MODEL_SOURCE="modelscope"

Usage:
    python extract_paper_mineru.py <input.pdf> <output_dir> [--slug my_paper]
"""

import argparse
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent


def run_mineru(pdf_path: Path, out_dir: Path, backend: str = "pipeline") -> Path:
    """Copy pdf to a short temp name, run mineru, return the produced auto/ dir."""
    out_dir.mkdir(parents=True, exist_ok=True)
    short_name = "p" + uuid.uuid4().hex[:8]
    tmp_pdf = out_dir / f"{short_name}.pdf"
    shutil.copyfile(pdf_path, tmp_pdf)

    try:
        cmd = ["mineru", "-p", str(tmp_pdf), "-o", str(out_dir), "-b", backend]
        print("[run]", " ".join(cmd))
        subprocess.run(cmd, check=True)
    finally:
        tmp_pdf.unlink(missing_ok=True)

    auto_dir = out_dir / short_name / "auto"
    if not auto_dir.exists():
        raise RuntimeError(f"MinerU did not produce expected output at {auto_dir}")
    return auto_dir, short_name


def rename_outputs(auto_dir: Path, short_name: str, slug: str) -> Path:
    """Rename the mineru-generated <short_name>.* files to <slug>.* for readability."""
    parent = auto_dir.parent  # out_dir/<short_name>/
    for f in auto_dir.iterdir():
        if f.is_file() and f.stem.startswith(short_name):
            new_name = f.name.replace(short_name, slug, 1)
            f.rename(auto_dir / new_name)

    final_dir = parent.parent / slug
    if final_dir.exists():
        shutil.rmtree(final_dir)
    parent.rename(final_dir)
    return final_dir / "auto"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdf_path")
    parser.add_argument("output_dir")
    parser.add_argument("--slug", default=None, help="Friendly name for output files (default: sanitized pdf stem)")
    parser.add_argument("--backend", default="pipeline", help="mineru backend (default: pipeline = CPU/GPU auto)")
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path).resolve()
    out_dir = Path(args.output_dir).resolve()
    if not pdf_path.is_file():
        print(f"[error] not found: {pdf_path}")
        sys.exit(1)

    slug = args.slug or "".join(c if c.isalnum() else "_" for c in pdf_path.stem)[:60].strip("_") or "paper"

    auto_dir, short_name = run_mineru(pdf_path, out_dir, backend=args.backend)
    auto_dir = rename_outputs(auto_dir, short_name, slug)

    print(f"[extracted] -> {auto_dir}")

    subprocess.run(
        [sys.executable, str(SCRIPT_DIR / "organize_mineru_output.py"), str(auto_dir)],
        check=True,
    )


if __name__ == "__main__":
    main()
