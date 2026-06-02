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

    # Group plugins by category. Team-scoped plugins are pulled out into a
    # dedicated section at the end rather than mixed into function categories.
    categories = registry.get("categories", {})
    plugins = registry.get("plugins", [])
    by_category: dict[str, list] = {}
    uncategorized = []
    team_plugins = []

    for plugin in plugins:
        if plugin.get("scope") == "team":
            team_plugins.append(plugin)
            continue
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

    # Team-specific plugins (scope: team) — listed separately at the end
    if team_plugins:
        lines.append("## Team-Specific")
        lines.append("")
        lines.append(
            "Plugins hardcoded to a specific team's setup. Not generally reusable "
            "by other teams without modification."
        )
        lines.append("")
        for plugin in team_plugins:
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
    scope = plugin.get("scope", "sdlc")

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
    if scope == "generic":
        meta_parts.append("Generic")
    elif scope == "team":
        meta_parts.append("Team-Specific")
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

    # Skills table (only user-invocable skills; internal ones are hidden)
    skills = [s for s in plugin.get("skills", []) if s.get("user-invocable", True)]
    if skills:
        lines.append("| Skill | Description |")
        lines.append("|-------|-------------|")
        for skill in skills:
            sname = skill["name"]
            sdesc = skill.get("description", "")
            lines.append(f"| `/{sname}` | {sdesc} |")
        lines.append("")

    # Agents table
    agents = plugin.get("agents", [])
    if agents:
        lines.append("| Agent | Description |")
        lines.append("|-------|-------------|")
        for agent in agents:
            aname = agent["name"]
            adesc = agent.get("description", "")
            lines.append(f"| {aname} | {adesc} |")
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
