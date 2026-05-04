#!/usr/bin/env python3
"""Extract before/after diagram pairs from a PR into eval dataset cases.

Given SVG files modified in a PR, extracts the embedded draw.io XML from
both the base and head versions, creating eval dataset cases compatible
with agent-eval-harness.

Usage:
    python3 scripts/extract_diagram_feedback.py --base-ref <sha> --svgs <svg1> [svg2 ...]
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import yaml


CASES_DIR = Path("eval/diagram-feedback/cases")


def extract_mxfile_from_svg(svg_content: str) -> str | None:
    """Extract embedded mxfile XML from an SVG file's content."""
    match = re.search(r'content="([^"]*)"', svg_content)
    if match:
        import html
        return html.unescape(match.group(1))

    if "mxGraphModel" in svg_content:
        match = re.search(r'(<mxGraphModel.*?</mxGraphModel>)', svg_content, re.DOTALL)
        if match:
            return match.group(1)

    return None


def get_file_at_ref(ref: str, path: str) -> str | None:
    """Get file content at a specific git ref."""
    try:
        result = subprocess.run(
            ["git", "show", f"{ref}:{path}"],
            capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return None


def derive_skill_info(svg_path: str) -> dict:
    """Extract plugin and skill name from the SVG path."""
    parts = Path(svg_path).parts
    plugin_idx = parts.index("plugins") + 1 if "plugins" in parts else -1
    if plugin_idx >= 0 and plugin_idx < len(parts):
        plugin = parts[plugin_idx]
        skill = Path(svg_path).stem
        return {"plugin": plugin, "skill": skill}
    return {"plugin": "unknown", "skill": Path(svg_path).stem}


def create_case(svg_path: str, base_ref: str, case_num: int) -> Path | None:
    """Create an eval dataset case from a before/after SVG pair."""
    info = derive_skill_info(svg_path)

    before_content = get_file_at_ref(base_ref, svg_path)
    if not before_content:
        print(f"  Skipping {svg_path}: no base version (new file)")
        return None

    after_content = Path(svg_path).read_text()

    before_xml = extract_mxfile_from_svg(before_content)
    after_xml = extract_mxfile_from_svg(after_content)

    if not before_xml:
        print(f"  Skipping {svg_path}: base SVG has no embedded diagram data")
        return None
    if not after_xml:
        print(f"  Skipping {svg_path}: head SVG has no embedded diagram data")
        return None

    if before_xml == after_xml:
        print(f"  Skipping {svg_path}: diagram XML unchanged (cosmetic SVG diff)")
        return None

    slug = info["skill"].replace(".", "-")
    case_dir = CASES_DIR / f"case-{case_num:03d}-{slug}"
    case_dir.mkdir(parents=True, exist_ok=True)

    (case_dir / "before.drawio").write_text(before_xml)
    (case_dir / "after.drawio").write_text(after_xml)

    d2_path = svg_path.replace(".svg", ".d2")
    input_data = {
        "plugin": info["plugin"],
        "skill": info["skill"],
        "svg_path": svg_path,
        "d2_path": d2_path if Path(d2_path).exists() else None,
    }
    with open(case_dir / "input.yaml", "w") as f:
        yaml.dump(input_data, f, default_flow_style=False)

    annotations = {
        "source": "human-edit-pr",
        "extracted_at": datetime.now().isoformat(),
        "base_ref": base_ref,
    }
    with open(case_dir / "annotations.yaml", "w") as f:
        yaml.dump(annotations, f, default_flow_style=False)

    print(f"  Created {case_dir}")
    return case_dir


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--svgs", nargs="+", required=True)
    args = parser.parse_args()

    CASES_DIR.mkdir(parents=True, exist_ok=True)

    existing = list(CASES_DIR.glob("case-*"))
    next_num = max((int(d.name.split("-")[1]) for d in existing), default=0) + 1

    created = 0
    for svg in args.svgs:
        case = create_case(svg, args.base_ref, next_num)
        if case:
            next_num += 1
            created += 1

    print(f"\nExtracted {created} feedback case(s) from {len(args.svgs)} modified SVG(s)")


if __name__ == "__main__":
    main()
