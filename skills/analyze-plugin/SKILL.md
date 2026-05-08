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
- `--no-diagrams` — Skip diagram generation (Steps 5-6). Only clone, read SKILL.md files,
  and generate the enrichment YAML. Useful for refreshing descriptions, arguments, and
  argument hints without the slow diagram pipeline.

## Instructions

### 1. Find the plugin in the registry

Read `registry.yaml` and locate the plugin entry matching the provided name.
Extract: `source.repo`, `source.ref`, `skills_dir` (or default `.claude/skills`),
`skills[]`, `agents[]`, and all metadata.

If the plugin name is not found, list available plugins and exit.

### 2. Clone the source repository

Clone into `.tmp/skill-repos/<plugin-name>` inside the project directory (not a system
temp dir — sub-agents need read access and can't access paths outside the project).

If the directory already exists, check that it points to the correct repo:

```bash
if [ -d .tmp/skill-repos/<plugin-name> ]; then
  remote=$(cd .tmp/skill-repos/<plugin-name> && git remote get-url origin 2>/dev/null)
  if [ "$remote" != "https://github.com/<repo>.git" ]; then
    echo "Repo URL changed ($remote → <repo>), re-cloning"
    rm -rf .tmp/skill-repos/<plugin-name>
  fi
fi
```

If the directory doesn't exist (or was just deleted), clone fresh:

```bash
mkdir -p .tmp/skill-repos
git clone --depth 1 --branch <ref> https://github.com/<repo>.git .tmp/skill-repos/<plugin-name>
```

If the directory exists and the remote matches, pull latest:

```bash
cd .tmp/skill-repos/<plugin-name> && git pull --ff-only
```

The `.tmp/` directory is already in `.gitignore`.

### 2.5. Clean up stale files

Compare existing site files against the current registry skill names. Remove files
from previous runs that no longer correspond to registered skills (e.g., after a
skill rename from `test-plan.create` to `test-plan-create`).

```bash
# Build the set of expected file stems
expected_stems="pipeline index _enriched"
for skill in <registered skill names>; do
  expected_stems="$expected_stems $skill"
done

# Remove orphaned diagram/page files
for file in site/docs/plugins/<plugin-name>/*; do
  stem=$(basename "$file" | sed 's/\.[^.]*$//')  # strip last extension
  # Skip _enriched.yaml, index.md, pipeline.*, artifacts/
  if echo "$expected_stems" | grep -qw "$stem"; then continue; fi
  if [ -d "$file" ]; then continue; fi  # skip directories like artifacts/
  echo "Removing stale file: $file"
  rm -f "$file"
done
```

This handles:
- Skill renames (e.g., `test-plan.create` → `test-plan-create`)
- Removed skills (skill deleted from registry but files remain)
- Repo moves (old diagrams from previous repo version)

### 3. Read all SKILL.md files

For each skill listed in the plugin's registry entry, read the corresponding SKILL.md file
from the cloned repo at `<skills_dir>/<skill-name>/SKILL.md`.

If a skill's SKILL.md is not found at the expected path, try common name transformations:
- Replace `-` with `.` (dashes to dots): `test-plan-create` → `test-plan.create`
- Replace `.` with `-` (dots to dashes): `test-plan.create` → `test-plan-create`

Report any name mapping used so the user knows.

If a skill listed in `registry.yaml` is not found in the repo after trying transformations,
skip it and add it to the "skipped" list in the report. Do not fail — continue with the
remaining skills.

Extract from each SKILL.md:
- **Frontmatter** fields (description, allowed-tools, user-invocable, argument-hint, etc.)
- **Detailed description** — the full markdown content beyond the frontmatter
- **argument-hint** — if present in frontmatter, store it as `argument_hint` in the
  enrichment. Then use it as the starting point for building the arguments list:
  parse each token (`<NAME>` = required, `[NAME]` = optional, `--flag` = flag),
  then search the SKILL.md body for descriptions of each argument name. Look for
  the argument name in headings, table rows, bullet lists, or prose near "Parse
  Arguments", "Inputs", "Arguments", or "Usage" sections.
- **Arguments** — look for "Parse Arguments", "Arguments", "Usage", "Inputs" sections.
  Extract from markdown tables, bullet lists, or usage code blocks. Capture: name,
  type/format, required/optional, default value, description. If `argument-hint`
  was already parsed, merge — the hint provides names and required/optional status,
  the body provides descriptions and types.
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
    argument_hint: "<REQUIRED_ARG> [OPTIONAL_ARG] --flag"
    arguments:
      - name: "REQUIRED_ARG"
        required: true
        description: "Description inferred from SKILL.md body"
      - name: "OPTIONAL_ARG"
        required: false
        description: "Description inferred from SKILL.md body"
      - name: "--flag"
        type: "(value type)"
        required: false
        default: "default-value"
        description: "What this argument does"
    usage_examples:
      - "/skill-name <REQUIRED_ARG> [OPTIONAL_ARG]"
      - "/skill-name --flag value"
  # ... repeat for each skill
```

The description should be richer than the one-line registry description — it should
explain what the plugin does, why, and how. Keep it concise but informative (2-4 paragraphs).

### 5. Generate pipeline diagram

**Skip this step if `--no-diagrams` is set.**

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

**Skip this step if `--no-diagrams` is set.**

For each skill, invoke `/skill-diagram` to create a detailed architecture diagram.
Use sub-agents with `run_in_background: true` to generate diagrams **in parallel** —
sequential execution is too slow for plugins with many skills.

```
Agent({
  description: "diagram <skill-name>",
  prompt: "/skill-diagram --skill .tmp/skill-repos/<plugin-name>/<skills_dir>/<dir-name> --output site/docs/plugins/<plugin-name>/<skill-name> --layout",
  run_in_background: true
})
```

Use `<dir-name>` from the name mapping in Step 3 (the actual directory name in the repo).
Use `<skill-name>` from the registry for the output path (so site files match registry names).

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
