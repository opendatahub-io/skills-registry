#!/usr/bin/env python3
"""Generate site content from registry.yaml.

Creates MkDocs-compatible markdown pages for the documentation website,
including the landing page, plugin pages, skill pages, and category pages.
Also generates mkdocs.yml with a dynamic navigation section.

Usage:
    python3 scripts/generate_site.py [--registry registry.yaml] [--output-dir site]
"""

import argparse
import os
import shutil
from pathlib import Path

import yaml


MKDOCS_CONFIG_TEMPLATE = """\
site_name: OpenDataHub Skills Registry
site_url: https://opendatahub-io.github.io/skills-registry

theme:
  name: material
  font:
    text: JetBrains Mono
    code: JetBrains Mono
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: blue
      accent: light blue
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: blue
      accent: light blue
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.indexes
    - search.suggest
    - content.code.copy
    - toc.follow

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - pymdownx.superfences
  - pymdownx.details
  - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
  - tables
  - toc:
      permalink: true

extra_css:
  - assets/stylesheets/extra.css
  - assets/stylesheets/drawio.css

extra_javascript:
  - assets/javascripts/drawio.js

"""

GENERATED_MARKER = "<!-- Auto-generated from registry.yaml. Do not edit directly. -->\n\n"


def load_registry(path: str = "registry.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def clean_generated(output_dir: Path):
    """Remove generated .md files, preserving SVGs, enrichment YAMLs, and drawio files."""
    docs = output_dir / "docs"
    for d in ["plugins", "categories"]:
        target = docs / d
        if not target.exists():
            continue
        for md_file in target.rglob("*.md"):
            md_file.unlink()
    index = docs / "index.md"
    if index.exists():
        index.unlink()


def build_category_plugins(registry: dict) -> dict[str, list]:
    """Group plugins by category key."""
    categories = registry.get("categories", {})
    by_cat: dict[str, list] = {k: [] for k in categories}
    for plugin in registry.get("plugins", []):
        cat = plugin.get("category")
        if cat and cat in by_cat:
            by_cat[cat].append(plugin)
    return by_cat


def generate_landing_page(registry: dict, cat_plugins: dict[str, list]) -> str:
    categories = registry.get("categories", {})
    plugins = registry.get("plugins", [])
    lines = ["---"]
    lines.append("hide:")
    lines.append("  - navigation")
    lines.append("  - toc")
    lines.append("---")
    lines.append("")
    lines.append(GENERATED_MARKER)
    lines.append("")
    title = registry.get('description', registry['name']).strip()
    title = title.split(',')[0].rstrip('.')
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"{len(plugins)} plugins | "
                 f"{sum(len(p.get('skills', [])) for p in plugins)} skills | "
                 f"{len([k for k, v in cat_plugins.items() if v])} categories")
    lines.append("")
    lines.append('[Getting Started](getting-started.md){ .md-button .md-button--primary }')
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Plugins")
    lines.append("")
    lines.append('<div class="grid cards" markdown>')
    lines.append("")

    for plugin in plugins:
        name = plugin["name"]
        desc = plugin["description"].strip().split("\n")[0]
        if len(desc) > 120:
            desc = desc[:117] + "..."
        skill_count = len(plugin.get("skills", []))
        cat_key = plugin.get("category", "")
        cat_name = categories.get(cat_key, {}).get("name", cat_key)
        version = plugin.get("version", "")

        lines.append(f"-   **[{name}](plugins/{name}/index.md)**")
        lines.append("")
        lines.append(f"    ---")
        lines.append("")
        lines.append(f"    {desc}")
        lines.append("")
        lines.append(f"    **{skill_count} skills** · {cat_name} · v{version}")
        lines.append("")

    lines.append("</div>")
    lines.append("")

    lines.append("## Categories")
    lines.append("")
    for cat_key, cat_meta in categories.items():
        cat_list = cat_plugins.get(cat_key, [])
        if not cat_list:
            continue
        count = len(cat_list)
        lines.append(f"- [{cat_meta['name']}](categories/{cat_key}.md) "
                     f"— {cat_meta.get('description', '')} ({count} plugin{'s' if count != 1 else ''})")
    lines.append("")

    return "\n".join(lines)


def generate_plugins_index(registry: dict) -> str:
    plugins = registry.get("plugins", [])
    categories = registry.get("categories", {})
    lines = ["---\ntitle: Plugins\n---\n"]
    lines.append(GENERATED_MARKER)
    lines.append("# Plugins")
    lines.append("")
    lines.append(f"{len(plugins)} plugins registered in the marketplace.")
    lines.append("")
    lines.append("| Plugin | Category | Skills | Version |")
    lines.append("|--------|----------|--------|---------|")
    for plugin in plugins:
        name = plugin["name"]
        cat_key = plugin.get("category", "")
        cat_name = categories.get(cat_key, {}).get("name", cat_key)
        skill_count = len(plugin.get("skills", []))
        version = plugin.get("version", "")
        lines.append(f"| [{name}]({name}/index.md) | {cat_name} | {skill_count} | v{version} |")
    lines.append("")
    return "\n".join(lines)


def generate_plugin_page(plugin: dict, registry: dict, enrichment: dict | None,
                         plugin_dir: Path | None = None) -> str:
    name = plugin["name"]
    desc = plugin["description"].strip()
    version = plugin.get("version", "")
    author = plugin.get("author", {}).get("name", "")
    license_str = plugin.get("license", "")
    category = plugin.get("category", "")
    tags = plugin.get("tags", [])
    repo = plugin.get("source", {}).get("repo", "")
    deps = plugin.get("depends_on", [])
    skills = plugin.get("skills", [])
    agents = plugin.get("agents", [])
    registry_name = registry["name"]
    categories = registry.get("categories", {})
    cat_name = categories.get(category, {}).get("name", category)

    if enrichment:
        desc = enrichment.get("description", desc)

    lines = [f"---\ntitle: {name}\n---\n"]
    lines.append(GENERATED_MARKER)
    lines.append(f"# {name}")
    lines.append("")
    lines.append(desc)
    lines.append("")

    # Metadata
    lines.append('!!! info "Plugin Details"')
    lines.append("")
    meta = []
    if version:
        meta.append(f"    - **Version**: {version}")
    if author:
        meta.append(f"    - **Author**: {author}")
    if license_str:
        meta.append(f"    - **License**: {license_str}")
    if category:
        meta.append(f"    - **Category**: [{cat_name}](../../categories/{category}.md)")
    if repo:
        meta.append(f"    - **Repository**: [{repo}](https://github.com/{repo})")
    if tags:
        pills = " ".join(f'<span class="tag-pill">{t}</span>' for t in tags)
        meta.append(f"    - **Tags**: {pills}")
    lines.extend(meta)
    lines.append("")

    # Architecture notes from enrichment
    if enrichment and enrichment.get("architecture_notes"):
        lines.append("## Architecture")
        lines.append("")
        lines.append(enrichment["architecture_notes"].strip())
        lines.append("")

    # Pipeline diagram (only if SVG exists)
    if plugin_dir and (plugin_dir / "pipeline.svg").exists():
        lines.append("## Pipeline")
        lines.append("")
        lines.append(f'<div class="diagram-container" markdown>')
        lines.append(f"![{name} pipeline](pipeline.svg)")
        lines.append(f"</div>")
        lines.append("")

    # Dependencies
    if deps:
        lines.append("## Dependencies")
        lines.append("")
        for d in deps:
            lines.append(f"- [`{d}`](../{d}/index.md)")
        lines.append("")

    # Skills table
    if skills:
        lines.append("## Skills")
        lines.append("")
        lines.append("| Skill | Description | Invocable |")
        lines.append("|-------|-------------|-----------|")
        for skill in skills:
            sname = skill["name"]
            sdesc = " ".join(skill.get("description", "").split())
            invocable = skill.get("user-invocable", True)
            badge = ":material-check:" if invocable else ":material-close: internal"
            lines.append(f"| [`/{sname}`]({sname}.md) | {sdesc} | {badge} |")
        lines.append("")

    # Agents table
    if agents:
        lines.append("## Agents")
        lines.append("")
        lines.append("| Agent | Description |")
        lines.append("|-------|-------------|")
        for agent in agents:
            aname = agent["name"]
            adesc = agent.get("description", "")
            lines.append(f"| {aname} | {adesc} |")
        lines.append("")

    # Install
    lines.append("## Installation")
    lines.append("")
    lines.append("```bash")
    lines.append(f"/plugin install {name}@{registry_name}")
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


def generate_skill_page(skill: dict, plugin: dict, enrichment: dict | None,
                        plugin_dir: Path | None = None) -> str:
    sname = skill["name"]
    sdesc = skill.get("description", "")
    invocable = skill.get("user-invocable", True)
    plugin_name = plugin["name"]

    enriched_skill = None
    if enrichment:
        enriched_skill = enrichment.get("skills", {}).get(sname)

    if enriched_skill and enriched_skill.get("description"):
        sdesc = enriched_skill["description"].strip()

    lines = [f"---\ntitle: {sname}\n---\n"]
    lines.append(GENERATED_MARKER)
    lines.append(f"# {sname}")
    lines.append("")
    lines.append(sdesc)
    lines.append("")

    # Metadata
    badge = ":material-check: User-invocable" if invocable else ":material-close: Internal"
    lines.append(f"**Plugin**: [{plugin_name}](index.md) | **{badge}**")
    lines.append("")

    # Skill diagram (only if SVG exists)
    if plugin_dir and (plugin_dir / f"{sname}.svg").exists():
        lines.append("## Diagram")
        lines.append("")
        lines.append(f'<div class="diagram-container" markdown>')
        lines.append(f"![{sname} diagram]({sname}.svg)")
        lines.append(f"</div>")
        lines.append("")

    # Arguments from enrichment
    if enriched_skill and enriched_skill.get("arguments"):
        lines.append("## Arguments")
        lines.append("")
        lines.append("| Argument | Required | Default | Description |")
        lines.append("|----------|----------|---------|-------------|")
        for arg in enriched_skill["arguments"]:
            aname = f'`{arg["name"]}`'
            req = ":material-check:" if arg.get("required") else ""
            default = f'`{arg["default"]}`' if arg.get("default") else "—"
            adesc = arg.get("description", "")
            lines.append(f"| {aname} | {req} | {default} | {adesc} |")
        lines.append("")

    # Usage examples from enrichment
    if enriched_skill and enriched_skill.get("usage_examples"):
        lines.append("## Usage")
        lines.append("")
        lines.append("```")
        for ex in enriched_skill["usage_examples"]:
            lines.append(ex)
        lines.append("```")
        lines.append("")
    elif enriched_skill and enriched_skill.get("usage"):
        lines.append("## Usage")
        lines.append("")
        lines.append(enriched_skill["usage"].strip())
        lines.append("")

    return "\n".join(lines)


def generate_categories_index(registry: dict) -> str:
    categories = registry.get("categories", {})
    by_cat = build_category_plugins(registry)
    lines = ["---\ntitle: Categories\n---\n"]
    lines.append(GENERATED_MARKER)
    lines.append("# Categories")
    lines.append("")
    lines.append(f"{len(categories)} categories in the marketplace.")
    lines.append("")
    lines.append("| Category | Plugins | Description |")
    lines.append("|----------|---------|-------------|")
    for key, meta in categories.items():
        if not by_cat.get(key):
            continue
        name = meta["name"]
        desc = meta.get("description", "").strip().split("\n")[0]
        count = len(by_cat[key])
        lines.append(f"| [{name}]({key}.md) | {count} | {desc} |")
    lines.append("")
    return "\n".join(lines)


def generate_category_page(cat_key: str, cat_meta: dict,
                           plugins: list) -> str:
    lines = [f"---\ntitle: {cat_meta['name']}\n---\n"]
    lines.append(GENERATED_MARKER)
    lines.append(f"# {cat_meta['name']}")
    lines.append("")
    lines.append(cat_meta.get("description", ""))
    lines.append("")

    if plugins:
        lines.append("## Plugins")
        lines.append("")
        for plugin in plugins:
            name = plugin["name"]
            desc = plugin["description"].strip().split("\n")[0]
            if len(desc) > 120:
                desc = desc[:117] + "..."
            skill_count = len(plugin.get("skills", []))
            version = plugin.get("version", "")
            lines.append(f"### [{name}](../plugins/{name}/index.md)")
            lines.append("")
            lines.append(desc)
            lines.append("")
            lines.append(f"**{skill_count} skills** · v{version}")
            lines.append("")

    return "\n".join(lines)


def load_enrichment(plugin_dir: Path) -> dict | None:
    enrichment_file = plugin_dir / "_enriched.yaml"
    if enrichment_file.exists():
        with open(enrichment_file) as f:
            return yaml.safe_load(f)
    return None


def generate_mkdocs_yml(registry: dict, categories: dict,
                        cat_plugins: dict[str, list]) -> str:
    """Generate complete mkdocs.yml with dynamic nav."""
    plugins = registry.get("plugins", [])

    nav_lines = []
    nav_lines.append("nav:")
    nav_lines.append("  - Home: index.md")

    # Plugins section — two-level: plugin > skills
    nav_lines.append("  - Plugins:")
    nav_lines.append("    - plugins/index.md")
    for plugin in plugins:
        name = plugin["name"]
        skills = plugin.get("skills", [])
        nav_lines.append(f"    - {name}:")
        nav_lines.append(f"      - plugins/{name}/index.md")
        for skill in skills:
            sname = skill["name"]
            nav_lines.append(f"      - {sname}: plugins/{name}/{sname}.md")

    # Categories section — with index page
    nav_lines.append("  - Categories:")
    nav_lines.append("    - categories/index.md")
    for cat_key, cat_meta in categories.items():
        if cat_plugins.get(cat_key):
            nav_lines.append(f"    - {cat_meta['name']}: categories/{cat_key}.md")

    nav_lines.append("  - Getting Started: getting-started.md")

    return MKDOCS_CONFIG_TEMPLATE + "\n".join(nav_lines) + "\n"


def generate_site(registry: dict, output_dir: Path):
    docs = output_dir / "docs"
    categories = registry.get("categories", {})
    cat_plugins = build_category_plugins(registry)

    # Clean generated content
    clean_generated(output_dir)

    # Create directories
    (docs / "plugins").mkdir(parents=True, exist_ok=True)
    (docs / "categories").mkdir(parents=True, exist_ok=True)

    # Landing page
    (docs / "index.md").write_text(generate_landing_page(registry, cat_plugins))

    # Plugins index
    (docs / "plugins" / "index.md").write_text(generate_plugins_index(registry))

    # Per-plugin and per-skill pages
    for plugin in registry.get("plugins", []):
        name = plugin["name"]
        plugin_dir = docs / "plugins" / name
        plugin_dir.mkdir(parents=True, exist_ok=True)

        enrichment = load_enrichment(plugin_dir)

        (plugin_dir / "index.md").write_text(
            generate_plugin_page(plugin, registry, enrichment, plugin_dir))

        for skill in plugin.get("skills", []):
            sname = skill["name"]
            (plugin_dir / f"{sname}.md").write_text(
                generate_skill_page(skill, plugin, enrichment, plugin_dir))

    # Category pages
    (docs / "categories").mkdir(parents=True, exist_ok=True)
    (docs / "categories" / "index.md").write_text(
        generate_categories_index(registry))
    for cat_key, cat_meta in categories.items():
        cat_list = cat_plugins.get(cat_key, [])
        if cat_list:
            (docs / "categories" / f"{cat_key}.md").write_text(
                generate_category_page(cat_key, cat_meta, cat_list))

    # mkdocs.yml
    (output_dir / "mkdocs.yml").write_text(
        generate_mkdocs_yml(registry, categories, cat_plugins))


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--registry", default="registry.yaml")
    parser.add_argument("--output-dir", default="site")
    args = parser.parse_args()

    registry = load_registry(args.registry)
    output_dir = Path(args.output_dir)
    generate_site(registry, output_dir)

    plugins = registry.get("plugins", [])
    skills = sum(len(p.get("skills", [])) for p in plugins)
    categories = len([k for k, v in build_category_plugins(registry).items() if v])
    print(f"Generated site: {len(plugins)} plugins, {skills} skills, "
          f"{categories} categories → {output_dir}/")


if __name__ == "__main__":
    main()
