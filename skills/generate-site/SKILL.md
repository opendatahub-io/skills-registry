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

Generate the complete documentation site for the skills-registry. Enriches each plugin
with detailed content extracted from SKILL.md files, generates presentation-quality SVG
diagrams, and produces structural pages from `registry.yaml`.

## Arguments

- `--plugin <name>` — Only process a specific plugin. Without this, all plugins are processed.
- `--no-diagrams` — Skip diagram generation (enrichment only). Useful for refreshing
  descriptions, arguments, and argument hints without the slow diagram pipeline.

## Instructions

### 1. Enrich plugins

Invoke `/analyze-plugin` for each plugin in the registry (or just the `--plugin` if specified).

If `--no-diagrams` is set, pass it through to `/analyze-plugin` so it skips Steps 5-6
(pipeline and individual skill diagrams) and only generates the enrichment YAML.

For efficiency, use sub-agents to analyze plugins **in parallel** (up to 6-8 at a time).

```
Agent({
  description: "Analyze <plugin-name>",
  prompt: "/analyze-plugin <plugin-name> [--no-diagrams]",
  run_in_background: true
})
```

Launch all plugin agents at once (or in batches of 6-8 for plugins with many skills).
Wait for all to complete before proceeding.

#### Permissions

Sub-agents need these permissions to work in the background without interactive approval.
Verify these are in `.claude/settings.json` before launching:

```json
{
  "permissions": {
    "allow": [
      "Read(.tmp/skill-repos/**)",
      "Write(site/docs/plugins/**)",
      "Edit(site/docs/plugins/**)",
      "Bash(python3 *)",
      "Bash(d2 *)",
      "Bash(mkdir *)",
      "Bash(mv *)",
      "Bash(find *)",
      "Bash(rm *)",
      "Bash(git clone *)",
      "Bash(git pull *)",
      "Bash(open *)",
      "Bash(ls *)",
      "Skill(diagram-skills:skill-diagram:*)",
      "Skill(diagram-skills:diagram-layout:*)"
    ]
  }
}
```

If permissions are missing, warn the user and suggest adding them before proceeding —
otherwise every sub-agent will be denied and the enrichment pass will fail silently.

### 2. Clean up after enrichment

After all enrichment agents complete, clean up stray files produced by the
diagram-layout pipeline:

```bash
# Rename .drawio.svg → .svg (draw.io export naming convention)
find site/docs/plugins -name "*.drawio.svg" -exec sh -c 'mv "$1" "${1%.drawio.svg}.svg"' _ {} \;

# Remove temporary files
find site/docs/plugins -name "*.drawio.png" -delete
find site/docs/plugins -name "layout-plan.json" -delete
```

### 3. Generate pages

After cleanup, run the generation script again to merge enrichment data into pages:

```bash
python3 scripts/generate_site.py
```

This picks up `_enriched.yaml` files (including `argument_hint` and `arguments`) and
conditionally includes SVG diagram references in pages where the SVG exists.

### 4. Build and verify

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

### 5. Report

Report:
- Total pages generated
- Plugins enriched
- Diagrams generated (if not `--no-diagrams`) — pipeline + individual count
- Build status (success/warnings/errors)
- Any skipped skills or failed diagram exports

Suggest next steps:
- **Preview**: `mkdocs serve --config-file site/mkdocs.yml` (note: new SVG files
  require a server restart — MkDocs doesn't hot-reload non-markdown assets)
- **Deploy**: push to main to trigger the GitHub Pages workflow
