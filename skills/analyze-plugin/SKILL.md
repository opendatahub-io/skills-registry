---
name: analyze-plugin
description: Analyze a plugin's source repository and generate enriched documentation content with diagrams for the skills-registry documentation site.
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

```bash
TMPDIR=$(mktemp -d)
git clone --depth 1 --branch <ref> https://github.com/<repo>.git "$TMPDIR"
```

### 3. Read all SKILL.md files

For each skill listed in the plugin's registry entry, read the corresponding SKILL.md file
from the cloned repo at `<skills_dir>/<skill-name>/SKILL.md`.

Extract from each SKILL.md:
- **Frontmatter** fields (description, allowed-tools, user-invocable, etc.)
- **Detailed description** — the full markdown content beyond the frontmatter
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
  <skill-name>:
    description: |
      Detailed description from the SKILL.md content.
    usage: |
      Example invocation and usage patterns.
  # ... repeat for each skill
```

The description should be richer than the one-line registry description — it should
explain what the plugin does, why, and how. Keep it concise but informative (2-4 paragraphs).

### 5. Generate pipeline diagram

Invoke the diagram-skills plugin to create a pipeline diagram showing all skills in the plugin:

```
/skill-diagram --skill <path1> --skill <path2> ... --detail low --layout --output site/docs/plugins/<plugin-name>/pipeline
```

This produces a pipeline-mode diagram where each skill is a single node.
After layout, export to SVG:
```
/diagram-layout --input <d2-file> --output site/docs/plugins/<plugin-name>/pipeline.drawio --format svg
```

Move or rename the exported SVG to `site/docs/plugins/<plugin-name>/pipeline.svg`.

### 6. Generate individual skill diagrams

For each skill that has a non-trivial SKILL.md (more than a few lines of instructions),
invoke diagram-skills to create a detailed architecture diagram:

```
/skill-diagram --skill <skill-path> --layout --output site/docs/plugins/<plugin-name>/<skill-name>
```

Export to SVG and place at `site/docs/plugins/<plugin-name>/<skill-name>.svg`.

Skip diagram generation for simple skills with minimal SKILL.md content (< 20 lines of instructions).

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

### Cleanup

Remove the temporary clone directory:
```bash
rm -rf "$TMPDIR"
```
