#!/usr/bin/env python3
"""Generate catalog.md from registry.yaml.

Creates a human-readable, browsable catalog of all plugins and skills,
grouped by category.

Usage:
    python3 scripts/generate_catalog.py [--registry registry.yaml] [--output catalog.md]
"""

import argparse
from pathlib import Path

import yaml


def load_registry(path: str = "registry.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def generate_catalog(registry: dict) -> str:
    lines = []
    lines.append(f"# {registry.get('description', registry['name'])}")
    lines.append("")
    lines.append("Auto-generated from `registry.yaml`. Do not edit directly.")
    lines.append("")

    # Quick install
    lines.append("## Quick Start")
    lines.append("")
    lines.append("```bash")
    lines.append("# Add this marketplace to Claude Code")
    owner = registry["owner"]["name"]
    lines.append(f"claude plugin marketplace add {owner}/skills-registry")
    lines.append("")
    lines.append("# Browse available plugins")
    lines.append("/plugin")
    lines.append("```")
    lines.append("")

    # Group plugins by category
    categories = registry.get("categories", {})
    plugins = registry.get("plugins", [])
    by_category: dict[str, list] = {}
    uncategorized = []

    for plugin in plugins:
        cat = plugin.get("category")
        if cat and cat in categories:
            by_category.setdefault(cat, []).append(plugin)
        else:
            uncategorized.append(plugin)

    # Render each category
    for cat_key, cat_meta in categories.items():
        cat_plugins = by_category.get(cat_key, [])
        if not cat_plugins:
            continue

        lines.append(f"## {cat_meta['name']}")
        lines.append("")
        lines.append(cat_meta.get("description", ""))
        lines.append("")

        for plugin in cat_plugins:
            lines.extend(render_plugin(plugin, registry["name"]))

    # Uncategorized
    if uncategorized:
        lines.append("## Other")
        lines.append("")
        for plugin in uncategorized:
            lines.extend(render_plugin(plugin, registry["name"]))

    return "\n".join(lines)


def render_plugin(plugin: dict, registry_name: str) -> list[str]:
    lines = []
    name = plugin["name"]
    desc = plugin["description"].strip()
    version = plugin.get("version", "")
    repo = plugin["source"].get("repo", "")
    license_str = plugin.get("license", "")
    tags = plugin.get("tags", [])

    lines.append(f"### {name}")
    lines.append("")
    lines.append(desc)
    lines.append("")

    # Dependencies
    deps = plugin.get("depends_on", [])
    if deps:
        lines.append(f"**Requires:** {', '.join(f'`{d}`' for d in deps)}")
        lines.append("")

    # Metadata line
    meta_parts = []
    if version:
        meta_parts.append(f"v{version}")
    if license_str:
        meta_parts.append(license_str)
    if repo:
        meta_parts.append(f"[{repo}](https://github.com/{repo})")
    if meta_parts:
        lines.append(" | ".join(meta_parts))
        lines.append("")

    if tags:
        lines.append(f"Tags: {', '.join(tags)}")
        lines.append("")

    # Skills table
    skills = plugin.get("skills", [])
    if skills:
        lines.append("| Skill | Description |")
        lines.append("|-------|-------------|")
        for skill in skills:
            sname = skill["name"]
            sdesc = skill.get("description", "")
            invocable = skill.get("user-invocable", True)
            prefix = f"`/{sname}`" if invocable else sname
            lines.append(f"| {prefix} | {sdesc} |")
        lines.append("")

    # Install command
    lines.append("```bash")
    lines.append(f"/plugin install {name}@{registry_name}")
    lines.append("```")
    lines.append("")

    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--registry", default="registry.yaml")
    parser.add_argument("--output", default="catalog.md")
    args = parser.parse_args()

    registry = load_registry(args.registry)
    catalog = generate_catalog(registry)

    Path(args.output).write_text(catalog)
    plugin_count = len(registry.get("plugins", []))
    print(f"Generated {args.output} with {plugin_count} plugin(s)")


if __name__ == "__main__":
    main()
