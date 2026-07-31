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

### 5. Set up diagram generation

**Skip Steps 5-6 if `--no-diagrams` is set.**

Diagrams are authored by parallel sub-agents that each follow the durable recipe at
`references/diagram-agent-instructions.md` (next to this SKILL.md). Set up once:

1. **Locate diagram-skills.** Find the local `diagram-skills` checkout (the
   `skill-diagram` + `diagram-layout` skills live there; commonly
   `~/Development/diagram-skills`). Call its path `<DIAGRAM_SKILLS>`. Sub-agents read
   its scripts/prompts, so it must be in `permissions.additionalDirectories`.
2. **Grant sub-agent permissions.** Sub-agents CANNOT get interactive approval — any
   tool call not on the allow-list is auto-denied and the agent hangs. Ensure
   `.claude/settings.local.json` allows `Write(.tmp/diagram-work/**)`,
   `Write(site/docs/plugins/**)`, `Read(.tmp/**)`, the Bash forms
   (`mkdir`/`mv`/`rm`/`cd`), and `additionalDirectories: [<DIAGRAM_SKILLS>]`. Adding
   permission rules needs explicit user consent (the self-modification guard blocks
   silent widening) — ask first. Then run ONE cheap smoke-test agent (Write to
   `.tmp/diagram-work/` and `site/docs/plugins/`, `python3 --version`) to confirm the
   perms are live before the expensive batch.
3. **Back up + clean-slate.** Copy any existing `*.d2`/`*.drawio`/`*.svg` in
   `site/docs/plugins/<plugin-name>/` to `.tmp/diagram-backup/<plugin-name>/`, then
   delete them from the output dir (so no agent mistakes stale output for "done").
   Clear stale scratch, including the SHARED `.tmp/diagram-work/pipeline/` dir — its
   name collides across plugins, and a stale `layout-plan.json` there will render the
   WRONG plugin's pipeline.
4. **Derive per-skill flows.** From the SKILL.md files read in Step 3 (and a skim of
   each skill's `scripts/`), write a brief node/edge **suggested flow** per skill and
   for the pipeline: ordered nodes with roles pre-assigned (entry / processing /
   decision / llm / external / output / callout), the expected llm-node count, the
   **primary output artifact to call out**, and any per-skill reserved-id traps.
   These outlines are the main quality lever — derive them yourself so agents refine
   rather than re-derive, and so callouts land on the right artifact.

### 6. Generate the diagrams (parallel agents), export, verify

**Skip this step if `--no-diagrams` is set.**

#### Detail requirements (non-negotiable — this is where diagrams silently regress)

Every individual skill diagram MUST clear skill-diagram's **Detail Floor**
(see `skill-diagram/prompts/analysis-guide.md` — read it, not just `d2-conventions.md`,
which is only the *style* guide). The floor:

- **≥1 callout detail box** per non-trivial skill — above all the skill's **primary
  output artifact's structure** (its schema/fields), plus any central file tree or
  config snippet. Read the actual script that writes it (e.g. `workspace.py`, the
  config template) to get the *real* structure — do not approximate.
- **Data-flow edge labels**: name the artifact that flows between steps
  (`summary.yaml`, `collection.json`) on the edges, not just conditions.
- **Containers for composite subsystems** (e.g. a scoring system's judge types),
  nested where a member is itself multi-step — never flatten into one node.
- **Decision branches and back-edges** preserved (mode branches, retry loops,
  cache/fast-path short-circuits).
- **~10-16 boxes** for a rich skill with 2-5 concrete bullets each (real
  script/flag/file names). A lean 5-9-node outline is the regression signature.

This means each diagram agent must **read the skill's `scripts/` and `references/`**
(not only its SKILL.md) to source callout content — SKILL.md gives the flow, the
scripts give the concrete artifacts. Author the `.d2` accordingly, then verify:

```bash
python3 <diagram-skills>/skills/skill-diagram/scripts/validate_d2.py <output>.d2
```

and clear the `detail_warnings` (missing callout / no data-flow labels / too few
nodes) before accepting the diagram.

The reliable path is to have each agent **author its `.d2` directly following the
recipe** (`references/diagram-agent-instructions.md`), then run the layout pipeline —
agents that call `/skill-diagram` as a nested Skill tend to shortcut.

For each skill AND the pipeline overview, spawn ONE `general-purpose` sub-agent that
reads the recipe and follows it, passing the inputs the recipe expects:

```
Agent({
  subagent_type: "general-purpose",
  run_in_background: false,   // barrier: put all calls of a batch in ONE message
  description: "diagram <skill-name>",
  prompt: `Read <abs>/.claude/skills/analyze-plugin/references/diagram-agent-instructions.md and follow it EXACTLY.
    name: <skill-name>
    OUT_DIR: <abs>/site/docs/plugins/<plugin-name>
    SCRATCH: <abs>/.tmp/diagram-work/<skill-name>/artifacts
    SKILL_MD: <abs>/.tmp/skill-repos/<plugin-name>/<skills_dir>/<dir-name>/SKILL.md
    DIAGRAM_SKILLS: <DIAGRAM_SKILLS>
    Suggested flow: <the per-skill outline from Step 5.4 — roles + llm count>
    Callout target: <the skill's primary output artifact to ground a callout>
    Reserved-id traps: <per-skill, e.g. mlflow: push->push-fb; check: filter->filter-classify>`
})
```

Use `<dir-name>` from the Step 3 name mapping; `<skill-name>` from the registry for
output paths (so site files match registry names). Launch in **barrier batches of ~6**
(all Agent calls in a single message, then wait for the batch). For the pipeline, pass
`name: pipeline` and a whole-plugin flow (one node per skill, fan-out + feedback
edges); the per-skill callout floor is relaxed for that overview.

Agents produce only `<name>.d2` + `<name>.drawio` (no SVG). **You (main thread) then
export SVGs sequentially** — do NOT let agents export (draw.io desktop contention):

```bash
for name in pipeline <skill-1> <skill-2> ...; do
  python3 <DIAGRAM_SKILLS>/skills/diagram-layout/scripts/export_diagram.py \
    site/docs/plugins/<plugin-name>/$name.drawio site/docs/plugins/<plugin-name>/$name.svg
done
find site/docs/plugins/<plugin-name> -name '*.drawio.bkp' -delete
find . -maxdepth 2 -name '.*.drawio.bkp' -delete
```

**Verify every diagram clears the Detail Floor:** `<mxCell` count > 2, `value=""` == 0,
≥1 callout (`grep -c 'JetBrains Mono' <name>.drawio` ≥ 1), `double=1` count == the
designed llm-node count and == the `strokeWidth=3` count (no thick-vs-double drift),
and SVG size in a healthy range (~150k–1.3M). Re-author or fix any diagram that misses
the floor — an under-detailed diagram is not done.

**Recovery for transient failures.** At this fan-out, agents occasionally die on
`Stream idle timeout` / `Connection closed mid-response` (not a task problem). If an
agent wrote a fresh `layout-plan.json`, finish it in the main thread
(`fix_layout.py → validate_layout.py → render_drawio.py`); if it wrote nothing,
relaunch it. If the skill's SKILL.md is unchanged vs the backed-up baseline and that
backup already clears the Detail Floor, restore the backup `.d2`/`.drawio` and just
re-export its SVG.

Skip diagram generation for placeholder skills with no real workflow (e.g., "not yet
implemented"). Reserved-id note: draw.io export fails (silently or hard) on cell ids
`filter`, `push`, `output`, `find` — the recipe handles renaming; surface any per-skill
occurrence in the agent's task prompt.

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
