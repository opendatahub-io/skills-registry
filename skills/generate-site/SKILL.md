---
name: generate-site
description: Orchestrate full documentation site generation — structural pages from registry.yaml plus AI-enriched content and diagrams for all plugins.
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Agent
  - Skill
---

# generate-site

Generate the complete documentation site for the skills-registry. Produces structural
pages from `registry.yaml` and optionally enriches each plugin with detailed content
and SVG diagrams.

## Arguments

- `--structure-only` — Only generate structural pages (no enrichment or diagrams).
  Equivalent to running `python3 scripts/generate_site.py` directly.
- `--enrich` — Also run `analyze-plugin` for each plugin to generate enrichment
  and diagrams. This is slower but produces richer content.
- `--plugin <name>` — Only enrich a specific plugin (used with `--enrich`).

If no arguments are provided, defaults to `--structure-only`.

## Instructions

### 1. Generate structural pages

```bash
python3 scripts/generate_site.py
```

This reads `registry.yaml` and generates all markdown pages and the `mkdocs.yml`
navigation under `site/`.

Report the counts: plugins, skills, categories.

### 2. Enrich plugins (if --enrich)

If `--enrich` is specified, invoke `/analyze-plugin` for each plugin in the registry
(or just the specified `--plugin` if provided).

For efficiency, use sub-agents to analyze plugins in parallel (up to 3 at a time)
to avoid sequential cloning and analysis:

```
Agent({
  description: "Analyze <plugin-name>",
  prompt: "/analyze-plugin <plugin-name>"
})
```

### 3. Regenerate with enrichments

After all enrichments are complete, run the generation script again to merge
enrichment data into the pages:

```bash
python3 scripts/generate_site.py
```

### 4. Build and verify

Build the site locally to verify everything works:

```bash
mkdocs build --config-file site/mkdocs.yml --site-dir /tmp/skills-site-verify
```

Check the build output for warnings or errors. Report any issues.

### 5. Report

Report:
- Total pages generated
- Plugins enriched (if --enrich)
- Diagrams generated (if --enrich)
- Build status (success/warnings/errors)
- Local preview command: `mkdocs serve --config-file site/mkdocs.yml`
