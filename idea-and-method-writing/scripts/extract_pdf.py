"""Extract text (per page, as markdown) and embedded images from a PDF.

Usage:
    python extract_pdf.py <input.pdf> <output_dir>

Output:
    <output_dir>/text.md            - full text, split by page headers
    <output_dir>/figures/pageN_imgM.<ext>  - every embedded raster image
"""
import sys
import os
import fitz  # PyMuPDF


def extract(pdf_path: str, out_dir: str) -> None:
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(pdf_path)

    figures_dir = os.path.join(out_dir, "figures")
    os.makedirs(figures_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    text_chunks = []
    image_count = 0

    for page_index, page in enumerate(doc, start=1):
        text_chunks.append(f"\n\n## Page {page_index}\n\n")
        text_chunks.append(page.get_text("text"))

        for img_index, img in enumerate(page.get_images(full=True), start=1):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
            except Exception as exc:  # noqa: BLE001
                print(f"  [warn] page {page_index} image {img_index}: {exc}")
                continue
            ext = base_image.get("ext", "png")
            image_bytes = base_image["image"]
            filename = f"page{page_index}_img{img_index}.{ext}"
            with open(os.path.join(figures_dir, filename), "wb") as f:
                f.write(image_bytes)
            image_count += 1

    text_path = os.path.join(out_dir, "text.md")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write("".join(text_chunks))

    print(f"Pages: {len(doc)}  Images: {image_count}")
    print(f"Text  -> {text_path}")
    print(f"Images -> {figures_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    extract(sys.argv[1], sys.argv[2])
