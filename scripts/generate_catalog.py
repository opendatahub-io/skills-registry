#!/usr/bin/env python3
"""Generate catalog.md from registry.yaml.

Creates a human-readable, browsable catalog of all plugins and skills,
grouped by category.

Usage:
    python3 scripts/generate_catalog.py [--registry registry.yaml] [--output catalog.md]
"""

import argparse
import sys
from pathlib import Path

import yaml

_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent
_REPO_ROOT_STR = str(_REPO_ROOT)
sys.path[:] = [entry for entry in sys.path if entry != _REPO_ROOT_STR]
sys.path.insert(0, _REPO_ROOT_STR)

from scripts.registry_contracts import (  # noqa: E402
    CANONICAL_FUNCTION_DOCS,
    CANONICAL_METRIC_DOCS,
    MEASURE_DOCS,
    contract_metrics_as_dicts,
    skill_contract_mapping,
    source_browse_url,
    source_display_name,
)


def load_registry(path: str = "registry.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def format_contract_functions(skill: dict) -> str:
    contract = skill_contract_mapping(skill)
    if contract is None:
        return "—"
    functions = contract.get("functions")
    if not isinstance(functions, list):
        return "—"
    parts = [f"`{value}`" for value in functions]
    return ", ".join(parts) if parts else "—"


def format_metric_assignment(metric: dict) -> str:
    metric_id = metric.get("id")
    if not metric_id:
        return ""
    measure = metric.get("measure")
    if isinstance(measure, str) and measure.strip():
        return f"`{metric_id}` (`{measure.strip()}`)"
    return f"`{metric_id}`"


def format_contract_metrics(skill: dict) -> str:
    contract = skill_contract_mapping(skill)
    if contract is None:
        return "—"
    metric_labels = [
        format_metric_assignment(metric)
        for metric in contract_metrics_as_dicts(contract.get("metrics"))
    ]
    return ", ".join(label for label in metric_labels if label) if metric_labels else "—"


def render_contract_reference() -> list[str]:
    lines = []
    lines.append("## Canonical Contract System")
    lines.append("")
    lines.append(
        "Contracts are contributor-facing optimization specs: functions describe the "
        "published job-to-be-done, metrics describe what should improve, and measures "
        "state how each metric is scored today."
    )
    lines.append("")
    lines.append("### Functions")
    lines.append("")
    lines.append("| Function | Meaning |")
    lines.append("|----------|---------|")
    for function_name, description in CANONICAL_FUNCTION_DOCS.items():
        lines.append(f"| `{function_name}` | {description} |")
    lines.append("")
    lines.append("### Metrics")
    lines.append("")
    lines.append("| Metric | What It Optimizes | Measurement Guidance |")
    lines.append("|--------|-------------------|----------------------|")
    for metric_name, metadata in CANONICAL_METRIC_DOCS.items():
        lines.append(
            f"| `{metric_name}` | {metadata['summary']} | {metadata['measure_guidance']} |"
        )
    lines.append("")
    lines.append("### Measures")
    lines.append("")
    lines.append("| Measure | When To Use |")
    lines.append("|---------|-------------|")
    for measure_name, description in MEASURE_DOCS.items():
        lines.append(f"| `{measure_name}` | {description} |")
    lines.append("")
    lines.append(
        "Skill tables below show metric ids with the current measure in parentheses."
    )
    lines.append("")
    return lines


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
    lines.extend(render_contract_reference())

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
    source = plugin["source"]
    source_type = source.get("type", "")
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
    if source_type in ("github", "git"):
        display = source_display_name(source)
        browse = source_browse_url(source)
        meta_parts.append(f"[{display}]({browse})")
    if meta_parts:
        lines.append(" | ".join(meta_parts))
        lines.append("")

    if tags:
        lines.append(f"Tags: {', '.join(tags)}")
        lines.append("")

    # Skills table (only user-invocable skills; internal ones are hidden)
    skills = [s for s in plugin.get("skills", []) if s.get("user-invocable", True)]
    if skills:
        show_contract_columns = any(skill_contract_mapping(skill) is not None for skill in skills)
        if show_contract_columns:
            lines.append("| Skill | Description | Functions | Metrics |")
            lines.append("|-------|-------------|-----------|---------|")
            for skill in skills:
                sname = skill["name"]
                sdesc = skill.get("description", "")
                lines.append(
                    f"| `/{sname}` | {sdesc} | "
                    f"{format_contract_functions(skill)} | {format_contract_metrics(skill)} |"
                )
        else:
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


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--registry", default="registry.yaml", help="Registry file path")
    parser.add_argument("--output", default="catalog.md", help="Output markdown path")
    args = parser.parse_args()

    registry = load_registry(args.registry)
    catalog = generate_catalog(registry)

    Path(args.output).write_text(catalog)
    plugin_count = len(registry.get("plugins", []))
    print(f"Generated {args.output} with {plugin_count} plugin(s)")


if __name__ == "__main__":
    main()
