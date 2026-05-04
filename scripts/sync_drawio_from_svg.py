#!/usr/bin/env python3
"""Extract embedded draw.io XML from SVGs and write matching .drawio files.

When a user edits an SVG in draw.io and submits it via PR, this script
extracts the embedded mxfile data and writes a .drawio file alongside it.
This keeps the .drawio files in sync without requiring users to commit both.

Usage:
    # Sync specific SVGs (e.g., from CI with changed files list)
    python3 scripts/sync_drawio_from_svg.py site/docs/plugins/assess-rfe/assess-rfe.svg

    # Sync all SVGs under a plugin
    python3 scripts/sync_drawio_from_svg.py site/docs/plugins/assess-rfe/*.svg

    # Dry run — show what would change
    python3 scripts/sync_drawio_from_svg.py --dry-run site/docs/plugins/**/*.svg
"""

import base64
import html
import re
import sys
import urllib.parse
import zlib
from pathlib import Path


def _decompress_diagram(compressed: str) -> str:
    """Decompress a base64+deflate+URL-encoded diagram body to XML.

    The draw.io web editor saves diagrams in compressed format:
    XML → URL-encode → deflate → base64. This reverses that.
    """
    try:
        decoded = base64.b64decode(compressed)
        inflated = zlib.decompress(decoded, -15)
        return urllib.parse.unquote(inflated.decode("utf-8"))
    except Exception:
        return compressed


def extract_mxfile_from_svg(svg_content: str) -> str | None:
    """Extract embedded mxfile XML from an SVG, decompressing if needed."""
    match = re.search(r'content="([^"]*)"', svg_content)
    if match:
        mxfile = html.unescape(match.group(1))
        # Decompress any base64-encoded diagram bodies to readable XML
        def _expand(m):
            body = m.group(1).strip()
            if not body.startswith("<"):
                xml = _decompress_diagram(body)
                return f"{m.group(0)[:m.group(0).index('>')]+1}>{xml}</diagram>"
            return m.group(0)
        mxfile = re.sub(r"(<diagram[^>]*>)(.*?)(</diagram>)",
                        lambda m: f"{m.group(1)}{_decompress_diagram(m.group(2).strip()) if not m.group(2).strip().startswith('<') else m.group(2)}{m.group(3)}",
                        mxfile, flags=re.DOTALL)
        return mxfile
    if "mxGraphModel" in svg_content:
        match = re.search(r"(<mxGraphModel.*?</mxGraphModel>)", svg_content, re.DOTALL)
        if match:
            return match.group(1)
    return None


def main():
    dry_run = "--dry-run" in sys.argv
    svg_paths = [p for p in sys.argv[1:] if not p.startswith("--")]

    if not svg_paths:
        print("Usage: sync_drawio_from_svg.py [--dry-run] <svg-files...>")
        sys.exit(1)

    updated = 0
    skipped = 0
    failed = 0

    for svg_path_str in svg_paths:
        svg_path = Path(svg_path_str)
        if not svg_path.exists() or svg_path.suffix != ".svg":
            continue

        drawio_path = svg_path.with_suffix(".drawio")
        svg_content = svg_path.read_text(encoding="utf-8")
        mxfile = extract_mxfile_from_svg(svg_content)

        if not mxfile:
            print(f"  - {svg_path.name}: no embedded mxfile (d2-rendered SVG)")
            skipped += 1
            continue

        if drawio_path.exists():
            existing = drawio_path.read_text(encoding="utf-8")
            if existing.strip() == mxfile.strip():
                skipped += 1
                continue

        if dry_run:
            print(f"  ~ {svg_path.name} → {drawio_path.name} (would update)")
        else:
            drawio_path.write_text(mxfile, encoding="utf-8")
            print(f"  ✓ {svg_path.name} → {drawio_path.name}")
        updated += 1

    print(f"\n{updated} updated, {skipped} skipped, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
