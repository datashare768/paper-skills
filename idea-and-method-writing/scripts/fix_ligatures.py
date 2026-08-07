"""
Fix a common PDF text-extraction artifact: some academic PDFs embed the
"ff"/"ffi"/"ffl" ligature as a single glyph whose ToUnicode mapping is
broken, so text extractors (MinerU/pdftotext/PyMuPDF alike) silently drop
one 'f', turning "traffic" into "trafic", "efficient" into "eficient", etc.

This is purely a font/encoding issue in the SOURCE pdf, not something a
better OCR model can reliably "guess" back, so we fix it with a curated
whole-word dictionary of the academic-writing terms most commonly affected.
Case (lower / Title / UPPER) is preserved.

Usage:
    python fix_ligatures.py <file.md> [more_files.md ...]   # edits in place
    from fix_ligatures import fix_ligatures
    fixed_text = fix_ligatures(text)
"""

import re
import sys

# broken -> correct (lowercase form; matching is case-insensitive, whole word)
_LIGATURE_FIXES = {
    "trafic": "traffic",
    "trafics": "traffics",
    "eficient": "efficient",
    "eficiently": "efficiently",
    "eficiency": "efficiency",
    "ineficient": "inefficient",
    "ineficiency": "inefficiency",
    "suficient": "sufficient",
    "suficiently": "sufficiently",
    "insuficient": "insufficient",
    "insuficiently": "insufficiently",
    "coeficient": "coefficient",
    "coeficients": "coefficients",
    "diferent": "different",
    "diferently": "differently",
    "diference": "difference",
    "diferences": "differences",
    "diferentiate": "differentiate",
    "diferentiation": "differentiation",
    "difuse": "diffuse",
    "difusion": "diffusion",
    "efect": "effect",
    "efects": "effects",
    "efective": "effective",
    "efectively": "effectively",
    "efectiveness": "effectiveness",
    "afect": "affect",
    "afects": "affects",
    "afected": "affected",
    "afecting": "affecting",
    "oface": "office",
    "ofices": "offices",
    "ofer": "offer",
    "ofers": "offers",
    "ofered": "offered",
    "ofset": "offset",
    "ofline": "offline",
    "staf": "staff",
    "bufer": "buffer",
    "bufers": "buffers",
    "sufer": "suffer",
    "sufers": "suffers",
    "sufering": "suffering",
    "dificulty": "difficulty",
    "dificult": "difficult",
    "dificulties": "difficulties",
    "shufle": "shuffle",
    "shufling": "shuffling",
    "flufy": "fluffy",
}

_WORD_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in _LIGATURE_FIXES) + r")\b",
    re.IGNORECASE,
)


def _match_case(replacement: str, original: str) -> str:
    if original.isupper():
        return replacement.upper()
    if original[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def fix_ligatures(text: str) -> str:
    def _sub(m):
        original = m.group(0)
        correct = _LIGATURE_FIXES[original.lower()]
        return _match_case(correct, original)

    return _WORD_RE.sub(_sub, text)


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_ligatures.py <file1> [file2 ...]")
        sys.exit(1)
    for path in sys.argv[1:]:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        fixed = fix_ligatures(text)
        n_changes = sum(1 for _ in _WORD_RE.finditer(text))
        if fixed != text:
            with open(path, "w", encoding="utf-8") as f:
                f.write(fixed)
            print(f"[fixed] {path}  ({n_changes} occurrence(s))")
        else:
            print(f"[ok]    {path}  (no ligature artifacts found)")


if __name__ == "__main__":
    main()
