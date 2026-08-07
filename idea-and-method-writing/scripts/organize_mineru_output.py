"""
Post-process a MinerU extraction result for one paper.

Input : the MinerU "auto" output folder of a single PDF, i.e. the folder
        containing  <name>.md, <name>_content_list.json, images/ ...
Output (written into the SAME auto folder, unless --out-dir is given):
    tables/   Table<N>_<slug>.md      one markdown file per table, named
                                        after the table's own caption/number
    figures/  Fig<N>_<slug>.png       one composed image per real, captioned
                                        figure, named after the paper's own
                                        figure number/caption. Multi-panel
                                        figures (a)/(b)/(c)... are re-assembled
                                        into a single image based on their
                                        original layout (bbox positions).

Formulas are intentionally NOT extracted as separate images: MinerU already
inlines them as LaTeX ($$ ... $$) inside <name>.md, which is exactly what we
want to keep for downstream writing (method.tex generation etc).

Uncaptioned / decorative images (logos, stray crops, chart panels whose
group never resolves to a real "Figure N" caption) are dropped on purpose,
per the "不需要无关紧要的图" requirement.

Usage:
    python organize_mineru_output.py <auto_dir> [--out-dir OUT_DIR]

Example:
    python organize_mineru_output.py \
        D:/PHD/Traffic_flow/mineru_test_output/10549-AAAI24.KongW/auto
"""

import argparse
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    from fix_ligatures import fix_ligatures
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from fix_ligatures import fix_ligatures


FIG_RE = re.compile(r"Fig(?:ure)?\.?\s*(\d+)\s*[:.]?\s*(.*)", re.IGNORECASE)
TABLE_RE = re.compile(r"^\s*Table\s*(\d+)\s*[:.]?\s*(.*)", re.IGNORECASE)
# Many IEEE-style papers number tables with Roman numerals, e.g. "TABLE III".
TABLE_ROMAN_RE = re.compile(
    r"^\s*Table\s+([IVXLCDM]+)\b\.?\s*[:.]?\s*(.*)", re.IGNORECASE
)

_ROMAN_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(s: str):
    s = s.upper()
    if not s or any(ch not in _ROMAN_VALUES for ch in s):
        return None
    total = 0
    prev = 0
    for ch in reversed(s):
        val = _ROMAN_VALUES[ch]
        total += val if val >= prev else -val
        prev = val
    return total if total > 0 else None


def slugify(text: str, maxlen: int = 50) -> str:
    text = re.sub(r"[^\w\u4e00-\u9fff]+", "_", text or "").strip("_")
    return text[:maxlen].strip("_")


def find_content_list(auto_dir: Path) -> Path:
    candidates = sorted(auto_dir.glob("*_content_list.json"))
    if not candidates:
        raise FileNotFoundError(f"No *_content_list.json found in {auto_dir}")
    return candidates[0]


def html_table_to_markdown(html: str) -> str:
    if not html:
        return ""
    if pd is not None:
        try:
            dfs = pd.read_html(io.StringIO(html))
            if dfs:
                df = dfs[0]
                df = df.fillna("")
                return df.to_markdown(index=False)
        except Exception:
            pass
    return html


def process_tables(items, out_dir: Path):
    tables_dir = out_dir / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    written = []
    anon_count = 0
    for item in items:
        if item.get("type") != "table":
            continue
        captions = item.get("table_caption") or []
        full_caption = fix_ligatures(" ".join(c.strip() for c in captions).strip())
        m = TABLE_RE.match(full_caption) if full_caption else None
        if m:
            num, title = m.group(1), m.group(2).strip()
        else:
            m_roman = TABLE_ROMAN_RE.match(full_caption) if full_caption else None
            roman_val = roman_to_int(m_roman.group(1)) if m_roman else None
            if m_roman and roman_val is not None:
                num, title = str(roman_val), m_roman.group(2).strip()
            else:
                anon_count += 1
                num, title = f"x{anon_count}", full_caption

        slug = slugify(title)
        fname = f"Table{num}" + (f"_{slug}" if slug else "") + ".md"
        fname = fname[:120]

        md_table = fix_ligatures(html_table_to_markdown(item.get("table_body", "")))
        footnotes = [fix_ligatures(f) for f in (item.get("table_footnote") or [])]

        content_lines = [f"# {full_caption or ('Table ' + str(num))}", ""]
        content_lines.append(md_table if md_table else "(table body could not be parsed)")
        if footnotes:
            content_lines.append("")
            content_lines.extend(footnotes)

        (tables_dir / fname).write_text("\n".join(content_lines) + "\n", encoding="utf-8")
        written.append(fname)
    return written


def cluster_rows(entries, tol_ratio: float = 0.5):
    """entries: list of (bbox, Image). Cluster into visual rows by y-position."""
    heights = [b[3] - b[1] for b, _ in entries]
    tol = (sum(heights) / len(heights)) * tol_ratio if heights else 10
    entries_sorted = sorted(entries, key=lambda t: (t[0][1], t[0][0]))
    rows = []
    current_row = [entries_sorted[0]]
    current_y = entries_sorted[0][0][1]
    for b, im in entries_sorted[1:]:
        if abs(b[1] - current_y) <= tol:
            current_row.append((b, im))
        else:
            rows.append(current_row)
            current_row = [(b, im)]
            current_y = b[1]
    rows.append(current_row)
    for row in rows:
        row.sort(key=lambda t: t[0][0])
    return rows


def compose_grid(entries, pad: int = 12, bg=(255, 255, 255)):
    if len(entries) == 1:
        return entries[0][1]

    rows = cluster_rows(entries)
    row_images = []
    for row in rows:
        h = max(im.height for _, im in row)
        resized = []
        for _, im in row:
            w = max(1, int(im.width * h / im.height))
            resized.append(im.resize((w, h)))
        total_w = sum(im.width for im in resized) + pad * (len(resized) - 1)
        row_canvas = Image.new("RGB", (total_w, h), bg)
        x = 0
        for im in resized:
            row_canvas.paste(im, (x, 0))
            x += im.width + pad
        row_images.append(row_canvas)

    max_w = max(im.width for im in row_images)
    total_h = sum(im.height for im in row_images) + pad * (len(row_images) - 1)
    canvas = Image.new("RGB", (max_w, total_h), bg)
    y = 0
    for im in row_images:
        canvas.paste(im, (0, y))
        y += im.height + pad
    return canvas


def process_figures(items, images_dir: Path, out_dir: Path):
    figs_dir = out_dir / "figures"
    figs_dir.mkdir(parents=True, exist_ok=True)
    written = []
    dropped = 0

    group = []  # list of content_list items pending a "Figure N" caption

    def flush(final_caption_text):
        nonlocal dropped
        if not group:
            return
        m = FIG_RE.search(final_caption_text) if final_caption_text else None
        if not m:
            # Never got a real "Figure N" caption -> irrelevant, drop silently.
            dropped += len(group)
            group.clear()
            return
        num, title = m.group(1), m.group(2).strip()
        slug = slugify(title)
        fname = f"Fig{num}" + (f"_{slug}" if slug else "") + ".png"
        fname = fname[:120]

        entries = []
        for g in group:
            p = images_dir / Path(g["img_path"]).name
            if p.exists():
                try:
                    im = Image.open(p).convert("RGB")
                    entries.append((g["bbox"], im))
                except Exception:
                    continue
        group.clear()
        if not entries:
            return
        composite = compose_grid(entries)
        composite.save(figs_dir / fname)
        written.append(fname)

    for item in items:
        t = item.get("type")
        if t not in ("image", "chart"):
            continue
        cap_key = "image_caption" if t == "image" else "chart_caption"
        captions = item.get(cap_key) or []
        full_text = fix_ligatures(" ".join(c.strip() for c in captions).strip())
        group.append(item)
        m = FIG_RE.search(full_text)
        if m:
            flush(full_text[m.start():])

    # Any leftover group at end of document never resolved -> irrelevant, drop.
    dropped += len(group)

    return written, dropped


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("auto_dir", help="MinerU '<name>/auto' output directory")
    parser.add_argument("--out-dir", default=None, help="Where to write tables/ and figures/ (default: auto_dir)")
    args = parser.parse_args()

    auto_dir = Path(args.auto_dir)
    out_dir = Path(args.out_dir) if args.out_dir else auto_dir
    images_dir = auto_dir / "images"

    content_list_path = find_content_list(auto_dir)
    items = json.loads(content_list_path.read_text(encoding="utf-8"))

    md_files = list(auto_dir.glob("*.md"))
    for md_path in md_files:
        text = md_path.read_text(encoding="utf-8")
        fixed = fix_ligatures(text)
        if fixed != text:
            md_path.write_text(fixed, encoding="utf-8")
            print(f"[ligature-fix] applied to {md_path.name}")

    table_files = process_tables(items, out_dir)
    fig_files, dropped = process_figures(items, images_dir, out_dir)

    print(f"[tables]  {len(table_files)} written -> {out_dir / 'tables'}")
    for f in table_files:
        print("   -", f)
    print(f"[figures] {len(fig_files)} written -> {out_dir / 'figures'}  ({dropped} irrelevant image(s) dropped)")
    for f in fig_files:
        print("   -", f)


if __name__ == "__main__":
    main()
