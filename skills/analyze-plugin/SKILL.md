---
name: analyze-plugin
description: >
  Analyze a plugin's source repository and generate enriched documentation content
  with presentation-quality SVG diagrams for the skills-registry documentation site.
  Use when the user wants to document a plugin, generate diagrams for skills, create
  enriched content for the site, or says things like "analyze the rfe-creator plugin",
  "generate diagrams for agent-eval-harness", or "update the docs for test-plan".
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Agent
  - Skill
  - Glob
  - Grep
---

# analyze-plugin

Analyze a plugin's source repository, extract detailed content from its SKILL.md files,
and generate enriched documentation pages with SVG diagrams for the skills-registry site.

## Arguments

- `<plugin-name>` — Name of the plugin as it appears in `registry.yaml` (e.g., `rfe-creator`).
  If omitted, list available plugins and ask the user to choose.

## Instructions

### 1. Find the plugin in the registry

Read `registry.yaml` and locate the plugin entry matching the provided name.
Extract: `source.repo`, `source.ref`, `skills_dir` (or default `.claude/skills`),
`skills[]`, `agents[]`, and all metadata.

If the plugin name is not found, list available plugins and exit.

### 2. Clone the source repository

Clone into `.tmp/skill-repos/<plugin-name>` inside the project directory (not a system
temp dir — sub-agents need read access and can't access paths outside the project).

```bash
mkdir -p .tmp/skill-repos
rm -rf .tmp/skill-repos/<plugin-name>
git clone --depth 1 --branch <ref> https://github.com/<repo>.git .tmp/skill-repos/<plugin-name>
```

The `.tmp/` directory is already in `.gitignore`.

### 3. Read all SKILL.md files

For each skill listed in the plugin's registry entry, read the corresponding SKILL.md file
from the cloned repo at `<skills_dir>/<skill-name>/SKILL.md`.

If a skill listed in `registry.yaml` is not found in the repo (wrong path, renamed, etc.),
skip it and add it to the "skipped" list in the report. Do not fail — continue with the
remaining skills.

Extract from each SKILL.md:
- **Frontmatter** fields (description, allowed-tools, user-invocable, argument-hint, etc.)
- **Detailed description** — the full markdown content beyond the frontmatter
- **Arguments** — look for "Parse Arguments", "Arguments", "Usage" sections. Extract from
  markdown tables, bullet lists, or usage code blocks. Capture: name, type/format,
  required/optional, default value, description. For positional arguments, use descriptive
  names (e.g., "input", "plugin-name"). Also extract usage examples (invocation patterns
  like `/skill-name arg1 arg2`). If the frontmatter has `argument-hint`, use it as a guide.
- **Usage examples** — any example invocations or usage patterns
- **Input/output** — what the skill takes and produces
- **Architecture notes** — how the skill works internally (sub-agents, scripts, prompts)

Also read any agent definitions from `<agents_dir>/<agent-name>.md` if the plugin has agents.

### 4. Generate the enrichment file

Write the extracted content to `site/docs/plugins/<plugin-name>/_enriched.yaml`:

```yaml
description: |
  Multi-paragraph description synthesized from all SKILL.md files
  and the overall plugin structure.
architecture_notes: |
  How the plugin's skills connect and work together.
  Internal architecture patterns (sub-agents, scripts, prompt chains).
skills:
  skill-name:
    description: |
      Detailed description from the SKILL.md content.
    arguments:
      - name: "--flag"
        type: "(value type)"
        required: false
        default: "default-value"
        description: "What this argument does"
    usage_examples:
      - "/skill-name --flag value"
      - "/skill-name positional-arg"
  # ... repeat for each skill
```

The description should be richer than the one-line registry description — it should
explain what the plugin does, why, and how. Keep it concise but informative (2-4 paragraphs).

### 5. Generate pipeline diagram

Invoke `/skill-diagram` to create a pipeline diagram showing all skills in the plugin.
The `--layout` flag chains to `/diagram-layout` automatically — do not invoke diagram-layout
separately.

```
/skill-diagram --skill <path1> --skill <path2> ... --detail low --layout --output site/docs/plugins/<plugin-name>/pipeline
```

This produces a D2 file and a `.drawio` with SVG export. Rename the exported SVG if needed:

```bash
# If exported as pipeline.drawio.svg, rename to pipeline.svg
mv site/docs/plugins/<plugin-name>/pipeline.drawio.svg site/docs/plugins/<plugin-name>/pipeline.svg 2>/dev/null || true
```

### 6. Generate individual skill diagrams

For each skill, invoke `/skill-diagram` to create a detailed architecture diagram.
Use sub-agents with `run_in_background: true` to generate diagrams **in parallel** —
sequential execution is too slow for plugins with many skills.

```
Agent({
  description: "diagram <skill-name>",
  prompt: "/skill-diagram --skill .tmp/skill-repos/<plugin-name>/<skills_dir>/<skill-name> --output site/docs/plugins/<plugin-name>/<skill-name> --layout",
  run_in_background: true
})
```

Launch all skill diagram agents at once (or in batches of 6-8 if there are many).
Wait for all to complete before proceeding.

After all agents complete, rename any `.drawio.svg` files to `.svg`:

```bash
find site/docs/plugins/<plugin-name> -name "*.drawio.svg" -exec sh -c 'mv "$1" "${1%.drawio.svg}.svg"' _ {} \;
```

Also clean up any stray files:

```bash
find site/docs/plugins/<plugin-name> -name "*.drawio.png" -delete
find site/docs/plugins/<plugin-name> -name "layout-plan.json" -delete
```

Skip diagram generation for placeholder skills with no real workflow (e.g., "not yet implemented").

#### Draw.io reserved cell IDs

The draw.io CLI silently fails to export when certain cell IDs are used. Known reserved IDs:
`filter`, `push`, `output`. If diagram export fails with no error message, check for these
IDs in the drawio XML and rename them (e.g., `filter` → `filter-classify`).

### 7. Regenerate site pages

Run the generation script to merge the new enrichment data into the site pages:

```bash
python3 scripts/generate_site.py
```

### 8. Report results

Report:
- Number of skills analyzed
- Enrichment file path
- Number of diagrams generated (pipeline + individual)
- Any skills skipped (not found in repo, too simple for diagrams)
- Any diagram export failures (with suggested fixes)

### Cleanup

The cloned repo in `.tmp/skill-repos/<plugin-name>` can be left in place for future
re-runs (it's gitignored). To force a fresh clone, delete it before running.
