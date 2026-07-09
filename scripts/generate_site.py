#!/usr/bin/env python3
"""Generate site content from registry.yaml.

Creates MkDocs-compatible markdown pages for the documentation website,
including the landing page, plugin pages, skill pages, and category pages.
Also generates mkdocs.yml with a dynamic navigation section.

Usage:
    python3 scripts/generate_site.py [--registry registry.yaml] [--output-dir site]
"""

import argparse
import html
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
    source_browse_url,
    source_display_name,
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
    source = plugin.get("source", {})
    source_type = source.get("type", "")
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
    if source_type in ("github", "git"):
        display = source_display_name(source)
        browse = source_browse_url(source)
        meta.append(f"    - **Repository**: [{display}]({browse})")
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


# ─── Contract card helpers ───────────────────────────────────────────
# The contract renders as a bespoke "spec-sheet" HTML card (§01–§04)
# with per-section left-spine accents. Templates + CSS live together;
# markup is emitted here, styles in site/docs/assets/stylesheets/extra.css
# under the `.skill-contract` block.


def _esc(value) -> str:
    """HTML-escape a value for safe inclusion in generated markup."""
    return html.escape("" if value is None else str(value), quote=True)


def _parse_contract_ref_url(ref: str | None) -> str | None:
    """Parse `owner/repo@sha:path` into a GitHub blob URL, or None if malformed."""
    if not isinstance(ref, str):
        return None
    ref = ref.strip()
    if "@" not in ref or ":" not in ref:
        return None
    try:
        repo, rest = ref.split("@", 1)
        sha, path = rest.split(":", 1)
    except ValueError:
        return None
    if "/" not in repo or not sha or not path:
        return None
    return f"https://github.com/{repo}/blob/{sha}/{path}"


def _short_contract_ref_label(ref: str | None) -> str:
    """Compact `filename @ abc1234` label from `owner/repo@sha:path/to/file`."""
    if not isinstance(ref, str):
        return ""
    ref = ref.strip()
    if "@" not in ref:
        return ref
    _repo, rest = ref.split("@", 1)
    if ":" in rest:
        sha, path = rest.split(":", 1)
        filename = path.rsplit("/", 1)[-1] or path
        return f"{filename} @ {sha[:7]}"
    return f"@ {rest[:7]}"


def _render_contract_card(contract: dict, plugin: dict) -> list[str]:
    """Return HTML lines for the skill contract card (spec-sheet aesthetic)."""

    lines: list[str] = []

    version = _esc(str(contract.get("version") or "").strip())
    problem = str(contract.get("problem_statement") or "").strip()

    source = plugin.get("source") or {}
    base_url: str | None = None
    ref_name = "main"
    if isinstance(source, dict) and source.get("type") in ("github", "git"):
        try:
            base_url = source_browse_url(source)
            ref_name = source.get("ref") or "main"
        except (KeyError, ValueError):
            base_url = None

    lines.append('<div class="skill-contract">')
    lines.append('  <header class="skill-contract__header">')
    lines.append('    <span class="skill-contract__eyebrow">Skill Contract</span>')
    if version:
        lines.append(f'    <span class="skill-contract__version">{version}</span>')
    lines.append('  </header>')
    if problem:
        lines.append(
            f'  <p class="skill-contract__lede">{_esc(problem)}</p>'
        )

    # §01 IDENTITY — functions + success conditions
    functions = _string_list(contract.get("functions"))
    success = _string_list(contract.get("success_conditions"))
    if functions or success:
        lines.append('  <section class="skill-contract__section" data-section="01">')
        lines.append(
            '    <h3 class="skill-contract__section-title">'
            '<span class="skill-contract__section-name">Identity</span>'
            '</h3>'
        )
        if functions:
            lines.append('    <div class="skill-contract__row">')
            lines.append('      <span class="skill-contract__field">Functions</span>')
            lines.append('      <div class="skill-contract__inline">')
            for fn in functions:
                lines.append(
                    f'        <span class="skill-contract__chip skill-contract__chip--function">{_esc(fn)}</span>'
                )
            lines.append('      </div>')
            lines.append('    </div>')
        if success:
            lines.append('    <div class="skill-contract__row">')
            lines.append('      <span class="skill-contract__field">Success</span>')
            lines.append('      <ul class="skill-contract__list">')
            for cond in success:
                lines.append(f'        <li>{_esc(cond)}</li>')
            lines.append('      </ul>')
            lines.append('    </div>')
        lines.append('  </section>')

    # §02 OPTIMIZATION TARGETS — metrics as compact spec rows
    metrics = contract_metrics_as_dicts(contract.get("metrics"))
    if metrics:
        lines.append('  <section class="skill-contract__section" data-section="02">')
        lines.append(
            '    <h3 class="skill-contract__section-title">'
            '<span class="skill-contract__section-name">Optimization Targets</span>'
            '</h3>'
        )
        lines.append('    <div class="skill-contract__metrics">')
        for m in metrics:
            metric_id = _esc(m.get("id", ""))
            measure = str(m.get("measure") or "").strip()
            ref_val = m.get("rubric_ref") or m.get("verifier_ref")
            lines.append('      <div class="skill-contract__metric">')
            lines.append(f'        <code class="skill-contract__metric-id">{metric_id}</code>')
            if measure:
                lines.append(
                    f'        <span class="skill-contract__measure skill-contract__measure--{_esc(measure)}">{_esc(measure)}</span>'
                )
            else:
                lines.append('        <span class="skill-contract__measure-placeholder"></span>')
            if ref_val:
                url = _parse_contract_ref_url(ref_val)
                label = _short_contract_ref_label(ref_val)
                title_attr = _esc(str(ref_val))
                if url:
                    lines.append(
                        f'        <a class="skill-contract__ref" href="{_esc(url)}" title="{title_attr}">'
                        f'{_esc(label)}<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>'
                    )
                else:
                    lines.append(
                        f'        <span class="skill-contract__ref" title="{title_attr}">{_esc(label)}</span>'
                    )
            else:
                lines.append('        <span class="skill-contract__ref-placeholder"></span>')
            lines.append('      </div>')
        lines.append('    </div>')
        lines.append('  </section>')

    # §03 INVARIANTS — must_preserve + fixed_context
    invariants = mapping_if_dict(contract.get("invariants"))
    if invariants:
        must = _string_list(invariants.get("must_preserve"))
        fixed = mapping_if_dict(invariants.get("fixed_context")) or {}
        tools = _string_list(fixed.get("tools"))
        cli = _string_list(fixed.get("cli"))
        documents = _string_list(fixed.get("documents"))
        kinputs = [
            item for item in sequence_as_list(fixed.get("knowledge_inputs"))
            if isinstance(item, dict)
        ]

        if must or tools or cli or documents or kinputs:
            lines.append('  <section class="skill-contract__section" data-section="03">')
            lines.append(
                '    <h3 class="skill-contract__section-title">'
                '<span class="skill-contract__section-name">Invariants</span>'
                '</h3>'
            )
            if must:
                lines.append('    <div class="skill-contract__row">')
                lines.append('      <span class="skill-contract__field">Must Not</span>')
                lines.append('      <ul class="skill-contract__list">')
                for item in must:
                    lines.append(f'        <li>{_esc(item)}</li>')
                lines.append('      </ul>')
                lines.append('    </div>')

            # Fixed context — tools / cli / documents / knowledge rendered as
            # one recessed code block (config-style), so the literal identifier
            # lists read as a single contained surface instead of loose tokens.
            def _code_line(key: str, value_html: str) -> str:
                return (
                    '      <div class="skill-contract__code-line">'
                    f'<span class="skill-contract__code-key">{_esc(key)}</span>'
                    f'<span class="skill-contract__code-val">{value_html}</span>'
                    '</div>'
                )

            code_lines: list[str] = []
            if tools:
                code_lines.append(_code_line("tools", ", ".join(_esc(t) for t in tools)))
            if cli:
                code_lines.append(_code_line("cli", ", ".join(_esc(c) for c in cli)))
            if documents:
                code_lines.append(_code_line("documents", ", ".join(_esc(d) for d in documents)))
            if kinputs:
                parts = []
                for ki in kinputs:
                    kind = _esc(ki.get("kind", "unknown"))
                    privacy = str(ki.get("privacy") or "unknown").strip() or "unknown"
                    parts.append(
                        f'{kind}<span class="skill-contract__privacy">{_esc(privacy)}</span>'
                    )
                code_lines.append(_code_line("knowledge", ", ".join(parts)))

            if code_lines:
                lines.append('    <div class="skill-contract__row">')
                lines.append('      <span class="skill-contract__field">Fixed Context</span>')
                lines.append('      <div class="skill-contract__code">')
                lines.extend(code_lines)
                lines.append('      </div>')
                lines.append('    </div>')

            lines.append('  </section>')

    # §04 TRACEABILITY — source_assertions
    source_assertions = mapping_if_dict(contract.get("source_assertions"))
    if source_assertions:
        skill_path_val = str(source_assertions.get("skill_path") or "").strip()
        supp = _string_list(source_assertions.get("supporting_paths"))
        if skill_path_val or supp:
            lines.append('  <section class="skill-contract__section" data-section="04">')
            lines.append(
                '    <h3 class="skill-contract__section-title">'
                '<span class="skill-contract__section-name">Traceability</span>'
                '</h3>'
            )

            def _path_markup(path: str) -> str:
                path_esc = _esc(path)
                if base_url:
                    href = f"{_esc(base_url)}/blob/{_esc(ref_name)}/{path_esc}"
                    return (
                        f'<a class="skill-contract__path" href="{href}">'
                        '<span class="skill-contract__ref-arrow" aria-hidden="true">↗</span>'
                        f'<code>{path_esc}</code></a>'
                    )
                return f'<code class="skill-contract__mono">{path_esc}</code>'

            if skill_path_val:
                lines.append('    <div class="skill-contract__row">')
                lines.append('      <span class="skill-contract__field">Skill</span>')
                lines.append(f'      <div class="skill-contract__inline">{_path_markup(skill_path_val)}</div>')
                lines.append('    </div>')
            if supp:
                lines.append('    <div class="skill-contract__row">')
                lines.append('      <span class="skill-contract__field">Supporting</span>')
                lines.append('      <ul class="skill-contract__paths">')
                for path in supp:
                    lines.append(f'        <li>{_path_markup(path)}</li>')
                lines.append('      </ul>')
                lines.append('    </div>')
            lines.append('  </section>')

    lines.append('</div>')
    return lines


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
        lines.extend(_render_contract_card(contract, plugin))
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
        source = p.get("source", {})
        source_type = source.get("type", "")
        enrichment = load_enrichment(docs_dir / "plugins" / name)
        edesc = enrichment.get("description", desc).strip() if enrichment else desc
        arch = (enrichment.get("architecture_notes", "").strip()
                if enrichment else "")
        lines.append(f"## {name}")
        lines.append("")
        lines.append(edesc)
        lines.append("")
        if source_type in ("github", "git"):
            lines.append(f"**Repository**: {source_browse_url(source)}")
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
