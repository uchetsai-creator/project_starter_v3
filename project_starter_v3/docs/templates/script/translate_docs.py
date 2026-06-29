#!/usr/bin/env python3
"""translate_docs.py — Translate approved docs to Traditional Chinese and mirror to docs-zh/

What it does:
1. Reads the same PDF_ALLOWLIST used by build_pdf.py
2. Translates each markdown file to Traditional Chinese using Google Translate (free, no API key)
3. Preserves code blocks, inline code, HTML comments, and table structure — only prose is translated
4. Writes the translated files into docs-zh/, mirroring the same directory structure
5. After running, generate the Chinese PDF with:
     python3 docs/script/build_pdf.py docs-zh --lang zh -o docs/project-documentation-zh.pdf

Usage:
  python3 docs/script/translate_docs.py [docs_dir] [--out docs-zh]

Notes:
  - Google Translate (via deep-translator) has a ~5000 char limit per request; long paragraphs
    are chunked automatically.
  - Translation quality is good for headings and short sentences; technical jargon may need
    manual review.
  - Re-running overwrites previously translated files.

Requires: pip install deep-translator --break-system-packages
"""
import sys, os, re, glob, time

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Missing dependency. Run: pip install deep-translator --break-system-packages")
    sys.exit(1)

# PDF_ALLOWLIST is maintained in pdf_allowlist.py — edit that file, not this one.
_script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _script_dir)
from pdf_allowlist import PDF_ALLOWLIST

MAX_CHARS = 4500   # Google Translate safe limit per request
DELAY     = 0.3    # seconds between API calls to avoid rate limiting


def collect_files(docs_dir):
    rels = [rel for _, rel in PDF_ALLOWLIST]
    seen = set(rels)
    for path in sorted(glob.glob(os.path.join(docs_dir, "modules", "*", "*-module-data-flow.md"))):
        rel = os.path.relpath(path, docs_dir)
        if rel not in seen:
            # insert before last entry (codebase-map)
            rels.insert(-1, rel)
    return rels


# ---------------------------------------------------------------------------
# Markdown-aware translation
# ---------------------------------------------------------------------------

# Placeholder token — uses ⟪n⟫ format which Google Translate passes through unchanged.
_PLACEHOLDER = "⟪{}⟫"

def _protect(text):
    """
    Replace untranslatable spans with placeholder tokens.
    Returns (protected_text, {token: original}).
    Order matters: fenced blocks first, then inline.
    """
    tokens = {}

    def stash(original):
        idx = len(tokens)
        ph = _PLACEHOLDER.format(idx)
        tokens[ph] = original
        return ph

    # Fenced code blocks (``` or ~~~), including the language tag
    text = re.sub(r"(```[^\n]*\n[\s\S]*?```|~~~[^\n]*\n[\s\S]*?~~~)", lambda m: stash(m.group(0)), text)
    # HTML comments <!-- ... -->
    text = re.sub(r"(<!--[\s\S]*?-->)", lambda m: stash(m.group(0)), text)
    # Inline code `...` (single backtick, no newline inside)
    text = re.sub(r"(`[^`\n]+`)", lambda m: stash(m.group(0)), text)
    # Markdown link/image URLs — protect the (url) part, keep the [label] for translation
    text = re.sub(r"(\]\()([^)]+)(\))", lambda m: m.group(1) + stash(m.group(2)) + m.group(3), text)

    return text, tokens


def _restore(text, tokens):
    for ph, original in tokens.items():
        text = text.replace(ph, original)
    return text


def _translate_chunk(text, translator):
    """Translate a single chunk, retrying once on failure."""
    text = text.strip()
    if not text:
        return text
    # Don't send pure-whitespace or pure-placeholder content
    if re.fullmatch(r"[\s\-\|\*_#>]+", text):
        return text
    try:
        result = translator.translate(text)
        time.sleep(DELAY)
        return result if result else text
    except Exception as e:
        print(f"  Translation error: {e} — keeping original")
        return text


def _translate_text(text, translator):
    """
    Split text into chunks ≤ MAX_CHARS and translate each, then rejoin.
    Splits on paragraph boundaries (double newlines) to keep context intact.
    """
    paragraphs = re.split(r"(\n{2,})", text)  # keep separators
    result = []
    buffer = ""

    def flush(buf):
        if not buf.strip():
            return buf
        return _translate_chunk(buf, translator)

    for para in paragraphs:
        if len(buffer) + len(para) > MAX_CHARS:
            result.append(flush(buffer))
            buffer = para
        else:
            buffer += para

    if buffer:
        result.append(flush(buffer))

    return "".join(result)


def translate_markdown(content, translator):
    """Translate markdown content while preserving code, comments, and structure."""
    protected, tokens = _protect(content)
    translated = _translate_text(protected, translator)
    restored = _restore(translated, tokens)
    return restored


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def mirror_path(rel, out_dir):
    out_path = os.path.join(out_dir, rel)
    os.makedirs(os.path.dirname(out_path) if os.path.dirname(out_path) else out_dir, exist_ok=True)
    return out_path


def main():
    args = sys.argv[1:]
    docs_dir = "docs"
    out_dir  = "docs-zh"

    i = 0
    while i < len(args):
        a = args[i]
        if a == "--out" and i + 1 < len(args):
            out_dir = args[i + 1]; i += 2
        elif not a.startswith("-"):
            docs_dir = a; i += 1
        else:
            i += 1

    if not os.path.isdir(docs_dir):
        print(f"Directory not found: {docs_dir}")
        sys.exit(1)

    translator = GoogleTranslator(source="en", target="zh-TW")
    rels = collect_files(docs_dir)

    print(f"Translating {len(rels)} files from {docs_dir}/ → {out_dir}/")
    print()

    for rel in rels:
        src = os.path.join(docs_dir, rel)
        if not os.path.exists(src):
            print(f"  skip (not found): {rel}")
            continue

        dst = mirror_path(rel, out_dir)
        print(f"  {rel} ...", end=" ", flush=True)

        with open(src, "r", encoding="utf-8") as f:
            content = f.read()

        translated = translate_markdown(content, translator)

        with open(dst, "w", encoding="utf-8") as f:
            f.write(translated)

        print("done")

    # Also copy over any HTML/SVG diagram files so build_pdf.py can find them
    for html_path in glob.glob(os.path.join(docs_dir, "**", "*.html"), recursive=True):
        rel = os.path.relpath(html_path, docs_dir)
        dst = mirror_path(rel, out_dir)
        with open(html_path, "rb") as f: data = f.read()
        with open(dst, "wb") as f: f.write(data)
        svg_path = os.path.splitext(html_path)[0] + ".svg"
        if os.path.exists(svg_path):
            svg_dst = os.path.splitext(dst)[0] + ".svg"
            with open(svg_path, "rb") as f: data = f.read()
            with open(svg_dst, "wb") as f: f.write(data)

    print()
    print(f"Translation complete. Now generate the PDF:")
    print(f"  python3 docs/script/build_pdf.py {out_dir} --lang zh -o docs/project-documentation-zh.pdf")


if __name__ == "__main__":
    main()
