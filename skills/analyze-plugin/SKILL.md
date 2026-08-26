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
Extract `source`, `skills[]`, `agents[]`, `mcp_servers[]`, `includes[]`, and all
metadata. The `source` comes in three shapes — note which one this plugin uses,
because it changes how you clone (Step 2) and where SKILL.md files live (Step 3):

| `source.type` | Fields | Repo to clone | Plugin lives at | Skills at |
|---------------|--------|---------------|-----------------|-----------|
| `github` | `repo` (`owner/name`), `ref`, `skills_dir?` | `https://github.com/<repo>.git` | repo root | `<skills_dir or .claude/skills>/<name>/SKILL.md` |
| `git` | `url`, `ref`, `skills_dir?` | `<url>` | repo root | `<skills_dir or .claude/skills>/<name>/SKILL.md` |
| `git-subdir` | `url`, `path`, `ref` | `<url>` | `<path>/` inside the repo | `<path>/skills/<name>/SKILL.md` |

Call the plugin's directory inside the clone `<SUBDIR>` — it is `.` for `github`/`git`
and `<source.path>` for `git-subdir`. Agents live at `<SUBDIR>/agents/`.

**Meta-plugins (bundles).** If the entry has a non-empty `includes: [members...]`, it is a
bundle — it installs those member plugins and has **no skills of its own**. Skip the
skill-reading and per-skill diagram steps for it; instead follow *Bundle handling* below.
The members are their own top-level registry entries (usually `git-subdir`) and are
analyzed on their own runs.

If the plugin name is not found, list available plugins and exit.

#### Bundle handling (plugins with `includes`)

For a bundle, produce an enrichment that describes the toolkit rather than skills it
does not have:

- Write `_enriched.yaml` with a synthesized `description` (what the bundle installs and
  why) and an `architecture_notes` that lists the member plugins from `includes` and, if
  useful, reads each member entry's `description` from `registry.yaml`. Do **not** emit a
  `skills:` map.
- For diagrams (unless `--no-diagrams`), generate only a **pipeline** overview whose nodes
  are the member plugins (one node per member, the bundle as entry). Skip per-skill
  diagrams — the bundle has none.
- You may still clone the bundle's `<SUBDIR>` to read its `plugin.json`/`README.md` for
  the overview, but there are no `<SUBDIR>/skills/` to iterate.

### 2. Clone the source repository

Clone inside the project directory under `.tmp/skill-repos/` (not a system temp dir —
sub-agents need read access and can't reach paths outside the project).

**Validate inputs first — before building any path or running `rm`/`git clone`.**
`<plugin-name>` and `source.path` come from `registry.yaml` and are interpolated into
`CLONE_DIR`/`WORKDIR` that `rm -rf` and `git clone` then act on, so a traversal value must
be rejected *up front* (the Step 5 sanitize runs too late — after these commands). Confirm
`<plugin-name>` is a plain slug (`^[a-z0-9][a-z0-9._-]*$` — no `/`, no `..`), and confirm
`source.path` (git-subdir) is a safe **relative** path — reject a leading `/` and any `..`
segment, allow `packages/foo`. Abort the run on either (path traversal / unintended
deletion — CWE-22 / CWE-73).

Then pick `CLONE_URL`, `CLONE_DIR`, `WORKDIR`, and `SKILLS_DIR` from the source shape
identified in Step 1:

- **`CLONE_URL`** — `https://github.com/<source.repo>.git` for `github`; `<source.url>`
  for `git` and `git-subdir`.
- **`CLONE_DIR`** — `.tmp/skill-repos/<plugin-name>` for **every** source type (one dir
  per plugin). A `git-subdir` member clones its whole monorepo here and reads only its
  subdir. Keep it per-plugin (not per-repo): `generate-site` fans this skill out in
  parallel, so a shared per-repo dir would let concurrent clones/pulls race and corrupt
  the checkout. The cost is that members of one monorepo each shallow-clone it — redundant
  but safe; a future optimization could clone the shared repo once before the fan-out.
- **`WORKDIR`** — `<CLONE_DIR>/<SUBDIR>` (recall `<SUBDIR>` is `.` for `github`/`git`,
  `<source.path>` for `git-subdir`). All later steps read SKILL.md/agents under `WORKDIR`.
- **`SKILLS_DIR`** — `<skills_dir>` if the entry sets one; else `.claude/skills` for
  `github`/`git`, `skills` for `git-subdir`. Skills resolve at
  `<WORKDIR>/<SKILLS_DIR>/<name>/SKILL.md`; use this **same** value in Step 3 and in the
  Step 6 agent prompt (don't hardcode `skills`, which is wrong for a default github/git plugin).

If the directory already exists, check that it points to the correct repo:

```bash
if [ -d "$CLONE_DIR" ]; then
  remote=$(cd "$CLONE_DIR" && git remote get-url origin 2>/dev/null)
  if [ "$remote" != "$CLONE_URL" ]; then
    echo "Repo URL changed ($remote → $CLONE_URL), re-cloning"
    rm -rf "$CLONE_DIR"
  fi
fi
```

Clone fresh, or (for an existing clone) **fetch and check out the requested `<ref>`** — the
`ref` in `registry.yaml` may have changed since the last run, and this also handles a tag
or SHA checkout cleanly (a plain `git pull --ff-only` fails on a detached/tag checkout and
would silently keep the old branch):

```bash
mkdir -p .tmp/skill-repos
if [ ! -d "$CLONE_DIR" ]; then
  # git-subdir needs the subdir, so a plain shallow clone of the repo is fine here.
  git clone --depth 1 --branch <ref> "$CLONE_URL" "$CLONE_DIR"
else
  git -C "$CLONE_DIR" fetch --depth 1 origin <ref>
  git -C "$CLONE_DIR" checkout -q -f FETCH_HEAD   # switch to the requested ref (branch/tag/SHA)
fi
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
at `<WORKDIR>/<SKILLS_DIR>/<skill-name>/SKILL.md` using the `WORKDIR` and `SKILLS_DIR`
resolved in Step 2. Concretely, a `git-subdir` member resolves to
`<CLONE_DIR>/<source.path>/skills/<skill-name>/SKILL.md`, and a default `github`/`git`
plugin to `<CLONE_DIR>/.claude/skills/<skill-name>/SKILL.md`.

(Skip this step entirely for a bundle — it has no skills; see *Bundle handling* in Step 1.)

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

Also read any agent definitions from `<WORKDIR>/<agents_dir or agents>/<agent-name>.md` if
the plugin has agents. If the plugin declares `mcp_servers` in `registry.yaml`, note them
for the enrichment description — they already render as their own table via
`generate_site.py`, so enrichment only needs to add context, not re-list them.

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

1. **Locate AND verify diagram-skills.** Find the local `diagram-skills` checkout (the
   `skill-diagram` + `diagram-layout` skills live there; commonly
   `~/Development/diagram-skills`). Call its path `<DIAGRAM_SKILLS>`. Sub-agents read
   AND `python3`-execute its scripts, so it is **trusted code** — verify it before use,
   then add it to `permissions.additionalDirectories`:

   ```bash
   git -C <DIAGRAM_SKILLS> remote get-url origin   # must be the known diagram-skills repo
   git -C <DIAGRAM_SKILLS> rev-parse HEAD           # the exact commit whose Python will run
   ```

   **Fail closed:** if `origin` is not the allowlisted diagram-skills repo, or the path is
   not a git checkout you can verify, do NOT spawn the diagram agents (they would execute
   its Python). Otherwise surface the HEAD SHA to the user and proceed only after they
   confirm it (or it matches a previously-approved SHA). Treat an unverified checkout as
   untrusted third-party code (CWE-494 / CWE-829 supply-chain execution).
2. **Grant sub-agents least privilege.** Sub-agents CANNOT get interactive approval — any
   tool call not on the allow-list is auto-denied and the agent hangs. Because each agent
   reads a target plugin's SKILL.md/scripts **cloned from an arbitrary URL in
   `registry.yaml`** (untrusted input — see the recipe's *Trust boundary*), grant them only
   the minimum they need:
   - **Agent-facing minimum:** `Write(.tmp/diagram-work/**)`,
     `Write(site/docs/plugins/<plugin-name>/**)` (scope to THIS run's plugin dir — not all
     of `plugins/**`), `Read(.tmp/skill-repos/**)`, `Read(.tmp/diagram-work/**)`,
     `Bash(python3 *)`, `Bash(mkdir *)`, `Bash(mv *)` (scratch tmp-renames in Step 4 of the
     recipe), `Bash(grep *)` (Step 8 verification), and
     `additionalDirectories: [<DIAGRAM_SKILLS>]`.
   - **Main-thread ONLY (never invoked by sub-agents):** `Bash(rm *)`, `Bash(find *)`,
     `git clone`/`git pull`, `Bash(open *)` — the orchestrator uses these for backup,
     clean-slate, clone, cleanup, and SVG export.

   **Limitation — be honest about it:** `.claude/settings.*.json` permissions are shared by
   the orchestrator and every sub-agent; the Agent tool has no per-agent ACL, so the
   destructive forms cannot be technically withheld from agents while the main thread keeps
   them. The agent restriction is therefore enforced **behaviorally** by the recipe's *Trust
   boundary* (agents are told never to run `rm`/destructive/network/out-of-scope commands),
   plus keeping the committed `.claude/settings.json` minimal (no `Write`/`rm`). Adding
   permission rules needs explicit user consent (the self-modification guard blocks silent
   widening) — ask first. Then run ONE cheap smoke-test agent (Write to `.tmp/diagram-work/`
   and `site/docs/plugins/`, `python3 --version`) to confirm the perms are live before the
   expensive batch.

   **Sanitize the target clone before spawning agents** (it came from an arbitrary
   `registry.yaml` URL): (a) reject symlinks — `find "$CLONE_DIR" -type l` (the clone dir
   from Step 2, `.tmp/skill-repos/<plugin-name>`)
   must return nothing, else abort the run (a symlink like `SKILL.md -> ~/.ssh/id_rsa` would
   let an agent read host files through the allowed read scope); and (b) confirm
   `<plugin-name>` / `<skill-name>` / `<dir-name>` / `<source.path>` are plain slugs (no `..`)
   before
   building any path, so a crafted name cannot escape `.tmp/diagram-work/*` or
   `site/docs/plugins/*`.
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

```text
Agent({
  subagent_type: "general-purpose",
  run_in_background: false,   // barrier: put all calls of a batch in ONE message
  description: "diagram <skill-name>",
  prompt: `Read <abs>/.claude/skills/analyze-plugin/references/diagram-agent-instructions.md and follow it EXACTLY.
    name: <skill-name>
    OUT_DIR: <abs>/site/docs/plugins/<plugin-name>
    SCRATCH: <abs>/.tmp/diagram-work/<skill-name>/artifacts
    SKILL_MD: <abs>/<WORKDIR>/<SKILLS_DIR>/<dir-name>/SKILL.md   # WORKDIR + SKILLS_DIR from Step 2; git-subdir member -> <abs>/.tmp/skill-repos/<plugin-name>/<source.path>/skills/<dir-name>/SKILL.md
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
# Verify + recover FIRST (Detail-Floor check and transient-failure recovery below);
# export only diagrams whose .drawio exists and passed — a missing input would
# otherwise abort the loop mid-way.
for name in pipeline <skill-1> <skill-2> ...; do
  drawio=site/docs/plugins/<plugin-name>/$name.drawio
  [ -f "$drawio" ] || { echo "SKIP $name — no .drawio yet, recover it first"; continue; }
  python3 <DIAGRAM_SKILLS>/skills/diagram-layout/scripts/export_diagram.py \
    "$drawio" site/docs/plugins/<plugin-name>/$name.svg
done
# Clean draw.io backup side-effects, scoped to the plugin output dir (never repo-wide):
find site/docs/plugins/<plugin-name> \( -name '*.drawio.bkp' -o -name '.*.drawio.bkp' \) -delete
```

**Verify every diagram clears the Detail Floor:** `<mxCell` count > 2, `value=""` == 0,
≥1 callout (`grep -c 'JetBrains Mono' <name>.drawio` ≥ 1), `double=1` count == the
designed llm-node count and == the `strokeWidth=3` count (no thick-vs-double drift),
and SVG size in a healthy range (~150k–1.3M). Re-author or fix any diagram that misses
the floor — an under-detailed diagram is not done.

**Verify SEMANTICS, not just density** (the mechanical floor above is necessary but
not sufficient — it catches style/density regressions, not accuracy). Run
`validate_d2.py` (it now also flags one-exit and unlabeled-branch decisions) and clear
its `detail_warnings`, then check each diagram against its SKILL.md for the classes a
linter can't see: (a) each output-artifact callout is anchored to the node that
PRODUCES it, not a downstream consumer; (b) every decision fans out to ≥2
condition-labeled branches; (c) no script-internal flag/behavior absent from the
SKILL.md is shown as user-facing (read the *documented* interface, use scripts only for
artifact structure); (d) each artifact uses one canonical path and callout claims match
the actual commands. For a thorough run, spawn a cheap per-diagram verify agent (or a
workflow adversarial-verify pass) that reads the diagram + its SKILL.md and reports
these — then fix what it finds. This is the class of defect that otherwise surfaces
only in downstream code review.

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

The cloned repo in `.tmp/skill-repos/<plugin-name>` (a `git-subdir` member clones its
whole monorepo here; its subdir is `WORKDIR`) can be left in place for future
re-runs (it's gitignored). To force a fresh clone, delete it before running.
