---
name: generate-site
description: >
  Orchestrate full documentation site generation for the skills-registry — structural
  pages from registry.yaml plus AI-enriched content and presentation-quality SVG diagrams
  for all plugins. Use when the user wants to rebuild the docs, update the website,
  regenerate pages after changing registry.yaml, add diagrams for a new plugin, or says
  things like "rebuild the site", "update the docs", "regenerate the website", or
  "I just added a plugin, update the site".
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
  - Skill
  - Glob
---

# generate-site

Generate the complete documentation site for the skills-registry. Produces structural
pages from `registry.yaml` and optionally enriches each plugin with detailed content
and SVG diagrams via `/analyze-plugin`.

## Arguments

- `--structure-only` — Only generate structural pages (no enrichment or diagrams).
  Equivalent to running `python3 scripts/generate_site.py` directly.
- `--enrich` — Also run `/analyze-plugin` for each plugin to generate enrichment
  and diagrams. This is slower but produces richer content.
- `--plugin <name>` — Only enrich a specific plugin. Implies `--enrich` — you don't
  need to pass both.

If no arguments are provided, defaults to `--structure-only`.

## Instructions

### 1. Generate structural pages

```bash
python3 scripts/generate_site.py
```

This reads `registry.yaml` and generates all markdown pages and the `mkdocs.yml`
navigation under `site/`. It preserves non-markdown files (SVGs, drawio, enrichment
YAMLs) — only `.md` files are regenerated.

Report the counts: plugins, skills, categories.

### 2. Enrich plugins (if --enrich or --plugin)

If `--enrich` or `--plugin` is specified, invoke `/analyze-plugin` for each plugin
in the registry (or just the specified `--plugin`).

For efficiency, use sub-agents to analyze plugins **in parallel** (up to 6-8 at a time).
Each agent clones the plugin repo, reads SKILL.md files, generates enrichment YAML,
and produces pipeline + individual skill diagrams via `/skill-diagram --layout`.

```
Agent({
  description: "Analyze <plugin-name>",
  prompt: "/analyze-plugin <plugin-name>",
  run_in_background: true
})
```

Launch all plugin agents at once (or in batches of 6-8 for plugins with many skills).
Wait for all to complete before proceeding.

#### Permissions

Sub-agents need these permissions to work in the background without interactive approval.
Verify these are in `.claude/settings.local.json` before launching:

```json
{
  "permissions": {
    "allow": [
      "Read(.tmp/skill-repos/**)",
      "Write(site/docs/plugins/**)",
      "Edit(site/docs/plugins/**)",
      "Bash(python3:*)",
      "Bash(d2:*)",
      "Bash(open:*)"
    ]
  }
}
```

If permissions are missing, warn the user and suggest adding them before proceeding —
otherwise every sub-agent will be denied and the enrichment pass will fail silently.

### 3. Clean up after enrichment

After all enrichment agents complete, clean up stray files produced by the
diagram-layout pipeline:

```bash
# Rename .drawio.svg → .svg (draw.io export naming convention)
find site/docs/plugins -name "*.drawio.svg" -exec sh -c 'mv "$1" "${1%.drawio.svg}.svg"' _ {} \;

# Remove temporary files
find site/docs/plugins -name "*.drawio.png" -delete
find site/docs/plugins -name "layout-plan.json" -delete
```

### 4. Regenerate with enrichments

After cleanup, run the generation script again to merge enrichment data into pages:

```bash
python3 scripts/generate_site.py
```

This picks up `_enriched.yaml` files and conditionally includes SVG diagram references
in pages where the SVG exists.

### 5. Build and verify

Stop any running dev server first (it holds a file lock):

```bash
lsof -ti:8000 | xargs kill 2>/dev/null
```

Build the site to verify everything works:

```bash
mkdocs build --config-file site/mkdocs.yml --site-dir /tmp/skills-site-verify-$$
```

Check the build output for warnings or errors. Zero warnings is the target — any
"unrecognized relative link" or "target not found" warnings indicate broken references.

### 6. Report

Report:
- Total pages generated
- Plugins enriched (if --enrich)
- Diagrams generated (if --enrich) — pipeline + individual count
- Build status (success/warnings/errors)
- Any skipped skills or failed diagram exports

Suggest next steps:
- **Preview**: `mkdocs serve --config-file site/mkdocs.yml` (note: new SVG files
  require a server restart — MkDocs doesn't hot-reload non-markdown assets)
- **Deploy**: push to main to trigger the GitHub Pages workflow
