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
    contract_metrics_as_dicts,
    mapping_if_dict,
    sequence_as_list,
    skill_contract_mapping,
)


MKDOCS_CONFIG_TEMPLATE = """\
site_name: OpenDataHub Skills Registry
site_url: https://opendatahub-io.github.io/skills-registry
repo_url: https://github.com/opendatahub-io/skills-registry
repo_name: opendatahub-io/skills-registry

theme:
  name: material
  font: false
  custom_dir: overrides
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


def _string_list(items) -> list[str]:
    if items is None or not isinstance(items, list):
        return []
    return [item.strip() for item in items if isinstance(item, str) and item.strip()]


def _knowledge_input_label(item: dict) -> str:
    kind = item.get("kind")
    privacy = item.get("privacy")
    if kind and privacy:
        return f"`{kind}` ({privacy})"
    if kind:
        return f"`{kind}`"
    return "`unknown`"


def _format_contract_function(value: str) -> str:
    description = CANONICAL_FUNCTION_DOCS.get(value)
    if description:
        return f"`{value}`: {description}"
    return f"`{value}`"


def _append_contract_bullets(
    lines: list[str],
    items: list,
    *,
    format_item=str,
) -> None:
    if items:
        for item in items:
            lines.append(f"    - {format_item(item)}")
    else:
        lines.append("    - —")


def _append_code_block(
    lines: list[str],
    block_lines: list[str],
    *,
    language: str = "bash",
    style: str | None = None,
) -> None:
    rendered_lines: list[str] = []
    for block_line in block_lines:
        rendered_lines.extend(str(block_line).splitlines() or [""])

    normalized_style = (
        style.strip().lower()
        if isinstance(style, str) and style.strip()
        else "fenced"
    )
    if normalized_style == "indented":
        for block_line in rendered_lines:
            lines.append(f"    {block_line}" if block_line else "")
        return
    fence_ticks = "```"
    while any(fence_ticks in block_line for block_line in rendered_lines):
        fence_ticks += "`"
    fence = f"{fence_ticks}{language}" if language else fence_ticks
    lines.append(fence)
    lines.extend(rendered_lines)
    lines.append(fence_ticks)


def _format_contract_metric(metric: dict) -> str:
    metric_id = str(metric["id"])
    header = f"`{metric_id}`"

    measure = metric.get("measure")
    if isinstance(measure, str) and measure.strip():
        header += f" (`{measure.strip()}`)"

    details: list[str] = []
    metadata = CANONICAL_METRIC_DOCS.get(metric_id)
    if metadata:
        details.append(metadata["summary"])
        details.append(f"Guidance: {metadata['measure_guidance']}")

    for key, label in (
        ("target_measure", "Target measure"),
        ("success_mode", "Success mode"),
    ):
        value = metric.get(key)
        if isinstance(value, str) and value.strip():
            details.append(f"{label}: `{value.strip()}`")

    references = []
    for ref_key in ("rubric_ref", "verifier_ref", "calibration_ref"):
        ref_value = metric.get(ref_key)
        if isinstance(ref_value, str) and ref_value.strip():
            references.append(f"{ref_key}=`{ref_value.strip()}`")
    if references:
        details.append("References: " + ", ".join(references))

    trials = metric.get("trials")
    if isinstance(trials, int):
        details.append(f"Trials: `{trials}`")

    if details:
        return f"{header}: " + " ".join(details)
    return header


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
    """Group plugins by category key. Team-scoped plugins are excluded — they
    are surfaced in a dedicated Team-Specific section, not function categories."""
    categories = registry.get("categories", {})
    by_cat: dict[str, list] = {k: [] for k in categories}
    for plugin in registry.get("plugins", []):
        if scope_of(plugin) == "team":
            continue
        cat = plugin.get("category")
        if cat and cat in by_cat:
            by_cat[cat].append(plugin)
    return by_cat


SCOPE_BADGE = {"team": "Team-specific", "generic": "Generic"}
VALID_SCOPES = {"sdlc", "generic", "team"}


def scope_of(plugin: dict) -> str:
    """Normalized scope. Unknown/missing values fall back to the sdlc default
    so a plugin is never silently dropped from a scope-grouped section."""
    scope = plugin.get("scope") or "sdlc"
    return scope if scope in VALID_SCOPES else "sdlc"


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
    title = registry.get("description", registry["name"]).strip()
    title = title.split(",")[0].rstrip(".")
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"{len(plugins)} plugins | "
                 f'{sum(len(p.get("skills", [])) for p in plugins)} skills | '
                 f"{len([k for k, v in cat_plugins.items() if v])} categories")
    lines.append("")
    lines.append("[Getting Started](getting-started.md){ .md-button .md-button--primary }")
    lines.append("")
    lines.append("---")
    lines.append("")
    def render_card(plugin):
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
        lines.append("    ---")
        lines.append("")
        lines.append(f"    {desc}")
        lines.append("")
        lines.append(f"    **{skill_count} skills** - {cat_name} - v{version}")
        lines.append("")

    def render_card_section(title, group):
        if not group:
            return
        lines.append(f"## {title}")
        lines.append("")
        lines.append('<div class="grid cards" markdown>')
        lines.append("")
        for plugin in group:
            render_card(plugin)
        lines.append("</div>")
        lines.append("")

    sdlc_plugins = [p for p in plugins if scope_of(p) == "sdlc"]
    generic_plugins = [p for p in plugins if scope_of(p) == "generic"]
    team_plugins = [p for p in plugins if scope_of(p) == "team"]

    render_card_section("SDLC", sdlc_plugins)
    render_card_section("Generic", generic_plugins)
    render_card_section("Teams", team_plugins)

    lines.append("## Categories")
    lines.append("")
    for cat_key, cat_meta in categories.items():
        cat_list = cat_plugins.get(cat_key, [])
        if not cat_list:
            continue
        count = len(cat_list)
        lines.append(f"- [{cat_meta['name']}](categories/{cat_key}.md) "
                     f"-- {cat_meta.get('description', '')} ({count} plugin{'s' if count != 1 else ''})")
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

    def render_row(plugin):
        name = plugin["name"]
        cat_key = plugin.get("category", "")
        cat_name = categories.get(cat_key, {}).get("name", cat_key)
        skill_count = len(plugin.get("skills", []))
        version = plugin.get("version", "")
        lines.append(f"| [{name}]({name}/index.md) | {cat_name} | {skill_count} | v{version} |")

    # Group into one section per scope: SDLC (default), Generic, Teams
    sections = [
        ("SDLC", [p for p in plugins if scope_of(p) == "sdlc"]),
        ("Generic", [p for p in plugins if scope_of(p) == "generic"]),
        ("Teams", [p for p in plugins if scope_of(p) == "team"]),
    ]
    for title, group in sections:
        if not group:
            continue
        lines.append(f"## {title}")
        lines.append("")
        lines.append("| Plugin | Category | Skills | Version |")
        lines.append("|--------|----------|--------|---------|")
        for plugin in group:
            render_row(plugin)
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
    scope = scope_of(plugin)
    meta = []
    if version:
        meta.append(f"    - **Version**: {version}")
    if author:
        meta.append(f"    - **Author**: {author}")
    if license_str:
        meta.append(f"    - **License**: {license_str}")
    if scope in SCOPE_BADGE:
        meta.append(f"    - **Scope**: {SCOPE_BADGE[scope]}")
    if category:
        meta.append(f"    - **Category**: [{cat_name}](../../categories/{category}.md)")
    if repo:
        meta.append(f"    - **Repository**: [{repo}](https://github.com/{repo})")
    if tags:
        pills = " ".join(f'<span class="tag-pill">{t}</span>' for t in tags)
        meta.append(f"    - **Tags**: {pills}")
    lines.extend(meta)
    lines.append("")

    # Pipeline diagram (only if SVG exists)
    if plugin_dir and (plugin_dir / "pipeline.svg").exists():
        lines.append("## Pipeline")
        lines.append("")
        lines.append('<div class="diagram-container" markdown>')
        lines.append(f"![{name} pipeline](pipeline.svg)")
        lines.append("</div>")
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

    contract_summary = mapping_if_dict(plugin.get("contract_summary"))
    if contract_summary:
        lines.append("## Contract Summary")
        lines.append("")
        lines.append(
            "Headline view only. Individual skill pages carry the detailed measures, "
            "references, success conditions, and invariants."
        )
        lines.append("")
        focus_functions = _string_list(contract_summary.get("focus_functions"))
        lines.append("### Focus Functions")
        lines.append("")
        if focus_functions:
            for value in focus_functions:
                description = CANONICAL_FUNCTION_DOCS.get(value)
                if description:
                    lines.append(f"- `{value}` — {description}")
                else:
                    lines.append(f"- `{value}`")
        else:
            lines.append("- —")
        lines.append("")
        focus_metrics = _string_list(contract_summary.get("focus_metrics"))
        lines.append("### Focus Metrics")
        lines.append("")
        if focus_metrics:
            for value in focus_metrics:
                metadata = CANONICAL_METRIC_DOCS.get(value)
                if metadata:
                    lines.append(
                        f"- `{value}` — {metadata['summary']} "
                        f"({metadata['measure_guidance']})"
                    )
                else:
                    lines.append(f"- `{value}`")
        else:
            lines.append("- —")
        lines.append("")
        notes = contract_summary.get("notes", "")
        if notes is None or isinstance(notes, (dict, list)):
            notes_txt = ""
        else:
            notes_txt = str(notes)
        lines.append("### Notes")
        lines.append("")
        lines.append(notes_txt)
        lines.append("")

    # Install
    lines.append("## Installation")
    lines.append("")
    _append_code_block(lines, [f"/plugin install {name}@{registry_name}"])
    lines.append("")

    # Architecture notes from enrichment (very bottom — deep-dive content)
    if enrichment and enrichment.get("architecture_notes"):
        lines.append("## Architecture")
        lines.append("")
        lines.append(enrichment["architecture_notes"].strip())
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

    contract = skill_contract_mapping(skill)
    if contract:
        lines.append("## Contract")
        lines.append("")
        lines.append('!!! info "Skill Contract"')
        lines.append("")
        version = contract.get("version")
        version_txt = "" if version is None else str(version)
        lines.append(f"    **Version**: `{version_txt}`")
        lines.append("")
        problem_statement = contract.get("problem_statement")
        if isinstance(problem_statement, str) and problem_statement.strip():
            lines.append(f"    **Problem Statement**: {problem_statement.strip()}")
            lines.append("")
        functions = _string_list(contract.get("functions"))
        lines.append("    **Functions:**")
        lines.append("")
        _append_contract_bullets(lines, functions, format_item=_format_contract_function)
        lines.append("")
        lines.append("    **Metrics:**")
        lines.append("")
        metric_entries = contract_metrics_as_dicts(contract.get("metrics"))
        _append_contract_bullets(
            lines, metric_entries, format_item=_format_contract_metric
        )
        lines.append("")
        success_conditions = _string_list(contract.get("success_conditions"))
        lines.append("    **Success Conditions:**")
        lines.append("")
        _append_contract_bullets(lines, success_conditions)
        lines.append("")
        invariants = mapping_if_dict(contract.get("invariants"))
        if invariants:
            lines.append("    **Must Preserve:**")
            lines.append("")
            must_preserve = _string_list(invariants.get("must_preserve"))
            _append_contract_bullets(lines, must_preserve)
            lines.append("")
            fixed_context = mapping_if_dict(invariants.get("fixed_context"))
            if fixed_context:
                lines.append("    **Fixed Context:**")
                lines.append("")
                tools = _string_list(fixed_context.get("tools"))
                cli = _string_list(fixed_context.get("cli"))
                documents = _string_list(fixed_context.get("documents"))
                knowledge_inputs = [
                    _knowledge_input_label(item)
                    for item in sequence_as_list(fixed_context.get("knowledge_inputs"))
                    if isinstance(item, dict)
                ]
                lines.append(
                    "    - **Tools**: "
                    + (", ".join(f"`{value}`" for value in tools) if tools else "—")
                )
                lines.append(
                    "    - **CLI**: "
                    + (", ".join(f"`{value}`" for value in cli) if cli else "—")
                )
                lines.append(
                    "    - **Documents**: "
                    + (", ".join(f"`{value}`" for value in documents) if documents else "—")
                )
                lines.append(
                    "    - **Knowledge Inputs**: "
                    + (", ".join(knowledge_inputs) if knowledge_inputs else "—")
                )
                lines.append("")
        source_assertions = mapping_if_dict(contract.get("source_assertions"))
        if source_assertions:
            lines.append("    **Source Assertions:**")
            lines.append("")
            skill_path = source_assertions.get("skill_path")
            if isinstance(skill_path, str) and skill_path.strip():
                lines.append(f"    - **Skill Path**: `{skill_path.strip()}`")
            else:
                lines.append("    - **Skill Path**: —")
            supporting_paths = _string_list(source_assertions.get("supporting_paths"))
            lines.append(
                "    - **Supporting Paths**: "
                + (", ".join(f"`{value}`" for value in supporting_paths) if supporting_paths else "—")
            )
            lines.append("")

    # Skill diagram (only if SVG exists)
    if plugin_dir and (plugin_dir / f"{sname}.svg").exists():
        lines.append("## Diagram")
        lines.append("")
        lines.append('<div class="diagram-container" markdown>')
        lines.append(f"![{sname} diagram]({sname}.svg)")
        lines.append("</div>")
        lines.append("")

    # Argument hint from enrichment (frontmatter argument-hint)
    argument_hint = enriched_skill.get("argument_hint") if enriched_skill else None
    code_block_style = enriched_skill.get("code_block_style") if enriched_skill else None

    # Arguments from enrichment
    if enriched_skill and enriched_skill.get("arguments"):
        lines.append("## Arguments")
        lines.append("")
        # Show invocation example: from argument_hint or auto-generated from args
        hint = argument_hint
        if not hint:
            parts = []
            for arg in enriched_skill["arguments"]:
                name = arg["name"]
                if name.startswith("--"):
                    parts.append(f"[{name}]")
                elif arg.get("required"):
                    parts.append(f"<{name}>")
                else:
                    parts.append(f"[{name}]")
            hint = " ".join(parts)
        _append_code_block(lines, [f"/{sname} {hint}"], style=code_block_style)
        lines.append("")
        lines.append("| Argument | Required | Default | Description |")
        lines.append("|----------|----------|---------|-------------|")
        for arg in enriched_skill["arguments"]:
            aname = f'`{arg["name"]}`'
            req = ":material-check:" if arg.get("required") else ""
            default = f'`{arg["default"]}`' if arg.get("default") else "-"
            adesc = " ".join(arg.get("description", "").split())
            lines.append(f"| {aname} | {req} | {default} | {adesc} |")
        lines.append("")
    elif argument_hint:
        # No enriched arguments but argument-hint exists — parse it as fallback
        lines.append("## Arguments")
        lines.append("")
        _append_code_block(lines, [f"/{sname} {argument_hint}"], style=code_block_style)
        lines.append("")
        lines.append("| Argument | Required | Description |")
        lines.append("|----------|----------|-------------|")
        for token in argument_hint.split():
            if token.startswith("[") and token.endswith("]"):
                name = token.strip("[]")
                lines.append(f"| `{name}` | | Optional |")
            elif token.startswith("<") and token.endswith(">"):
                name = token.strip("<>")
                lines.append(f"| `{name}` | :material-check: | |")
            elif token.startswith("--"):
                lines.append(f"| `{token}` | | Flag |")
            else:
                lines.append(f"| `{token}` | :material-check: | |")
        lines.append("")

    # Usage examples from enrichment
    if enriched_skill and enriched_skill.get("usage_examples"):
        lines.append("## Usage")
        lines.append("")
        _append_code_block(
            lines,
            [str(ex) for ex in enriched_skill["usage_examples"]],
            style=code_block_style,
        )
        lines.append("")
    elif enriched_skill and enriched_skill.get("usage"):
        lines.append("## Usage")
        lines.append("")
        lines.append(enriched_skill["usage"].strip())
        lines.append("")
    elif not (enriched_skill and enriched_skill.get("arguments")) and not argument_hint:
        # No arguments, no usage examples — show basic invocation
        lines.append("## Usage")
        lines.append("")
        _append_code_block(lines, [f"/{sname}"], style=code_block_style)
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

    def render_plugin_entries(group):
        for plugin in group:
            name = plugin["name"]
            desc = plugin["description"].strip()
            skill_count = len(plugin.get("skills", []))
            version = plugin.get("version", "")
            lines.append(f"### [{name}](../plugins/{name}/index.md)")
            lines.append("")
            lines.append(desc)
            lines.append("")
            lines.append(f"**{skill_count} skills** - v{version}")
            lines.append("")

    # Split into SDLC and Generic subsections (team plugins aren't in categories)
    sdlc_group = [p for p in plugins if scope_of(p) == "sdlc"]
    generic_group = [p for p in plugins if scope_of(p) == "generic"]
    for title, group in (("SDLC", sdlc_group), ("Generic", generic_group)):
        if not group:
            continue
        lines.append(f"## {title}")
        lines.append("")
        render_plugin_entries(group)

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


def generate_llms_txt(registry: dict, site_url: str) -> str:
    """Generate llms.txt index following the llmstxt.org spec."""
    plugins = registry.get("plugins", [])
    lines = ["# OpenDataHub Skills Registry"]
    lines.append("")
    lines.append("> Claude Code skills and plugins marketplace for the "
                 "opendatahub-io organization. Aggregates skills from multiple "
                 "GitHub repositories into a single discoverable marketplace.")
    lines.append("")
    lines.append("## Plugins")
    lines.append("")
    for p in plugins:
        name = p["name"]
        desc = p["description"].strip().split("\n")[0]
        lines.append(f"- [{name}]({site_url}/plugins/{name}/): {desc}")
    lines.append("")
    lines.append("## Skills")
    lines.append("")
    for p in plugins:
        pname = p["name"]
        for s in p.get("skills", []):
            sname = s["name"]
            sdesc = s.get("description", "").strip()
            if s.get("user-invocable", True):
                lines.append(f"- [{sname}]({site_url}/plugins/{pname}/{sname}/): {sdesc}")
    lines.append("")
    lines.append("## Optional")
    lines.append("")
    for p in plugins:
        pname = p["name"]
        for s in p.get("skills", []):
            if not s.get("user-invocable", True):
                sname = s["name"]
                sdesc = s.get("description", "").strip()
                lines.append(f"- [{sname}]({site_url}/plugins/{pname}/{sname}/): {sdesc} (internal)")
    lines.append("")
    return "\n".join(lines)


def generate_llms_full_txt(registry: dict, docs_dir: Path) -> str:
    """Generate llms-full.txt with all skill details inlined."""
    plugins = registry.get("plugins", [])
    lines = ["# OpenDataHub Skills Registry"]
    lines.append("")
    lines.append("> Claude Code skills and plugins marketplace for the "
                 "opendatahub-io organization. Aggregates skills from multiple "
                 "GitHub repositories into a single discoverable marketplace.")
    lines.append("")
    lines.append("---")
    lines.append("")
    for p in plugins:
        name = p["name"]
        desc = p["description"].strip()
        repo = p.get("source", {}).get("repo", "")
        enrichment = load_enrichment(docs_dir / "plugins" / name)
        edesc = enrichment.get("description", desc).strip() if enrichment else desc
        arch = (enrichment.get("architecture_notes", "").strip()
                if enrichment else "")
        lines.append(f"## {name}")
        lines.append("")
        lines.append(edesc)
        lines.append("")
        if repo:
            lines.append(f"**Repository**: https://github.com/{repo}")
            lines.append("")
        if arch:
            lines.append("### Architecture")
            lines.append("")
            lines.append(arch)
            lines.append("")
        lines.append("### Skills")
        lines.append("")
        eskills = enrichment.get("skills", {}) if enrichment else {}
        for s in p.get("skills", []):
            sname = s["name"]
            sdesc = s.get("description", "").strip()
            invocable = s.get("user-invocable", True)
            badge = "" if invocable else " (internal)"
            es = eskills.get(sname, {})
            if es.get("description"):
                sdesc = es["description"].strip()
            hint = es.get("argument_hint", "")
            args = es.get("arguments", [])
            examples = es.get("usage_examples", [])
            lines.append(f"#### /{sname}{badge}")
            lines.append("")
            lines.append(sdesc)
            lines.append("")
            if hint:
                lines.append(f"```\n/{sname} {hint}\n```")
                lines.append("")
            if args:
                lines.append("| Argument | Required | Description |")
                lines.append("|----------|----------|-------------|")
                for arg in args:
                    aname = arg.get("name", "")
                    req = "yes" if arg.get("required") else ""
                    adesc = " ".join(arg.get("description", "").split())
                    lines.append(f"| `{aname}` | {req} | {adesc} |")
                lines.append("")
            if examples:
                lines.append("Examples:")
                lines.append("```")
                for ex in examples:
                    lines.append(ex)
                lines.append("```")
                lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)


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

    # llms.txt protocol files — written to docs/ so MkDocs includes them
    # in the build output (served at /skills-registry/llms.txt)
    site_url = "https://opendatahub-io.github.io/skills-registry"
    (docs / "llms.txt").write_text(generate_llms_txt(registry, site_url))
    (docs / "llms-full.txt").write_text(
        generate_llms_full_txt(registry, docs))



def main() -> None:
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
