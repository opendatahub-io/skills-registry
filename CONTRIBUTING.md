# Contributing to the Skills Registry

## Adding a New Plugin

### 1. Prepare Your Repository

Your plugin repo needs at minimum:

**Option A — Full plugin (recommended):**
```text
your-repo/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
└── skills/                  # Or .claude/skills/
    └── your-skill/
        └── SKILL.md         # Skill definition
```

The `plugin.json` needs at least:
```json
{
  "name": "your-plugin",
  "description": "What your plugin does",
  "version": "1.0.0"
}
```

**Option B — Skills-only repo (no plugin.json):**

If your repo only has `.claude/skills/` and you can't add a `plugin.json`, you can use `strict: false` in the registry entry (see step 2).

### 2. Add Your Entry to registry.yaml

Open a PR adding your plugin to the `plugins` list in `registry.yaml`:

```yaml
plugins:
  # ... existing plugins ...

  - name: your-plugin
    description: What your plugin does (one paragraph)
    version: "1.0.0"
    category: evaluation          # Must match a key in 'categories'
    scope: sdlc                   # generic | sdlc | team (default: sdlc) — see "Plugin scope"
    tags: [tag1, tag2]
    author:
      name: your-name
    license: Apache-2.0
    source:
      type: github
      repo: opendatahub-io/your-repo
      ref: main
    skills:
      - name: your-skill
        description: What this skill does
        user-invocable: true
    harnesses:
      claude-code:
        install: "/plugin install your-plugin@opendatahub-skills"
      generic:
        skill_format: markdown
        skill_dir: skills/
        entry_point: "skills/{skill_name}/SKILL.md"
    depends_on: []
```

For repos without `plugin.json`, add `strict: false` and `skills_dir`:
```yaml
    strict: false
    skills_dir: .claude/skills
```

For plugins hosted on non-GitHub forges (GitLab, Gitea, etc.), use `type: git` with an explicit `url`:
```yaml
    source:
      type: git
      url: https://gitlab.corp.example.com/team/your-repo.git
      ref: main
```

The `user-invocable` field mirrors the [native Claude Code SKILL.md frontmatter field](https://code.claude.com/docs/en/skills#frontmatter-reference). Set it to `false` for internal skills that are called only by other skills/agents in the background — they will be hidden from the generated catalog. The registry value is catalog-only, so to actually hide the skill from the `/` menu in Claude Code you must also set `user-invocable: false` in the SKILL.md frontmatter in your source repo.

### Plugin scope

The optional `scope` field declares how reusable the plugin is. It is catalog-only metadata — it is **not** propagated to `marketplace.json` and does not affect installation (every plugin remains installable by anyone via `/plugin install`). It only controls how the plugin is labeled and organized in the catalog and docs site.

| Scope | Meaning | Example |
|-------|---------|---------|
| `generic` | Works anywhere, for any user or project | `agent-eval-harness` |
| `sdlc` (default) | RHOAI/ODH-wide, reusable across teams | `rfe-creator`, `assess-rfe` |
| `team` | Hardcoded to one team's setup (project keys, custom fields, labels) — not usable by others without modification | a team's JIRA-hygiene skill |

**Prefer making skills reusable.** If a skill only hardcodes team-specific values (project key, team ID, component, custom-field IDs) out of convenience, consider externalizing those into config or env vars so it can be `sdlc`-scoped and shared. Mark `scope: team` only when the skill genuinely serves a single team.

`generic` and `team` plugins are labeled on the site; `team` plugins are listed in a dedicated "Team-Specific" section rather than mixed into function categories. Always use a **function-based** `category` (what the skill does) regardless of scope — do not create team-named categories. Team identity belongs in `tags` and `scope`.

### Delegated sub-plugins: listing skills vs `skill_count`

A sub-plugin whose skills live in its own repo (typically a `git-subdir` source) delegates discovery to its `plugin.json`. Because such sources are exempt from the contract requirement (see [Choosing Canonical Contracts](#choosing-canonical-contracts)), **the preferred approach is to list its skills** (name + description, no contract) so they render on the plugin's catalog/site page:

```yaml
    source:
      type: git-subdir
      url: https://github.com/rh-uxd/ai-helpers.git
      path: plugins/patternfly/pf-react
      ref: main
    skills:
      - name: pf-test-gen
        description: Generate a unit test file for a React component using Testing Library.
        user-invocable: true
      # ... name + description only; no contract needed for git-subdir sources
```

Alternatively, when you only want a count and not a list, set `skill_count: N` instead of a `skills` array — catalog-only metadata (not propagated to `marketplace.json`). A plugin sets `skill_count` **or** lists `skills`, never both. Either way it is hand-maintained; keep it in sync when the upstream plugin adds or removes skills.

### Meta-plugins (bundles)

A **meta-plugin** installs several other plugins in one step. List its members with `includes` (the names of other registry plugins):

```yaml
  - name: patternfly            # the bundle
    description: Everything you need for PatternFly development
    version: "0.1.0"
    category: development-tools
    scope: generic
    source:
      type: git-subdir
      url: https://github.com/rh-uxd/ai-helpers.git
      path: plugins/patternfly
      ref: main
    includes: [pf-react, pf-design-guide, pf-design-audit, pf-a11y, pf-migration, pf-code-review, pf-mcp]
    depends_on: []
```

Rules for bundles:

- **Register every member as its own top-level entry** in `registry.yaml`, with `name` matching the bundle's upstream `plugin.json` `dependencies`. Claude Code resolves a plugin's dependencies within the marketplace it was installed *from*, so if the members are not in this registry, installing the bundle resolves nothing (`dependency-unsatisfied`) and no skills load. (Members are normal entries — typically `git-subdir` sub-plugins that list their own skills, name + description, without contract blocks.)
- **Do not give the bundle its own `skills` or `skill_count`.** Its displayed count is derived by summing its members' counts, and bundles are excluded from registry-wide totals so each skill is counted once.
- `includes` is different from `depends_on`. `depends_on` records a peer plugin this one *requires*; `includes` records the plugins this one *installs together*, and renders as an "Includes" section in the catalog and site. Neither reaches `marketplace.json`.
- `validate_registry.py` rejects a bundle that references an undefined member, lists itself, forms a cycle, or carries its own `skills`/`skill_count`.

### Agents and MCP servers

A plugin can provide **agents** and **MCP servers** alongside (or instead of) skills. Both are surfaced as their own table on the plugin's catalog and site page:

```yaml
    agents:
      - name: python-packaging-investigator
        description: Investigates Python package repositories and packaging complexity
    mcp_servers:
      - name: patternfly
        description: Component documentation, design token lookup, and accessibility guidance via MCP
```

- **`agents`** lists the agents the plugin ships (matching the agent file names). For a `strict: false` plugin, also set `agents_dir` so the marketplace entry points Claude Code at them; for a `strict: true` plugin, the `plugin.json` is authoritative and `agents` is catalog-only display metadata.
- **`mcp_servers`** lists the MCP servers the plugin provides (matching the keys in the plugin's `plugin.json` `mcpServers`). It is **catalog-only** display metadata — Claude Code reads the actual server config from the source `plugin.json`, so `mcp_servers` is never propagated to `marketplace.json`. Use it so an MCP-only plugin (e.g. `pf-mcp`) advertises what it offers instead of appearing as "0 skills".

### 3. Regenerate Artifacts

After editing `registry.yaml`, validate and regenerate artifacts so CI stays in sync (same sequence as `CLAUDE.md`):

```bash
pip install pyyaml jsonschema  # once, if dependencies are missing
python3 scripts/validate_registry.py
python3 scripts/sync_marketplace.py
python3 scripts/generate_catalog.py
python3 scripts/generate_site.py
```

Commit generated updates under `.claude-plugin/marketplace.json`, `catalog.md`, and `site/` with your PR.

### Local Hooks

Install the same contract and `skill-linter` checks used in CI:

```bash
python3 -m pip install pre-commit
pre-commit install
```

The hooks validate staged `registry.yaml` changes and run pinned `skill-linter` checks against the referenced source skills. You also need Node.js 22 or newer available locally because `skill-linter` requires Node 22.

`config/skill-linter-registry.json` may downgrade an occasionally noisy rule to warning when permission-documentation text would otherwise false-positive, so you can still see warning-level linter output while the hook passes.

When you add a skill or change an existing skill's registry entry (compared against `HEAD` for pre-commit or the configured base ref in CI), include a canonical `contract` block on that skill plus accurate `contract.source_assertions` paths into the upstream repository; CI and hooks enforce this for touched skills.

The contract requirement applies **only to skills whose plugin `source.type` is `github` or `git`** — whole-repo sources whose in-repo skills carry resolvable `source_assertions`, the same sources `skill-linter` verifies. Skills on `git-subdir`, `npm`, or `local` sources are **exempt from the contract requirement**: `npm`/`local` cannot be cloned at all, and a `git-subdir` sub-plugin delegates skill discovery to its own `plugin.json` rather than to `source_assertions`, so a contract on it would be unverifiable metadata. This lets a delegated sub-plugin (e.g. a bundle member) list its skills (name + description) for display without a contract block.

Note that the **clone-based upstream sweeps are broader** than the contract requirement. `git-subdir` *is* cloneable (clone the repo, then resolve its `path`), so skill-name drift, `--check-sources`, and the Codex-manifest check (`GIT_CLONEABLE_TYPES` = `github`/`git`/`git-subdir`) all cover it — only the contract requirement stays scoped to `github`/`git`.

### Choosing Canonical Contracts

Treat the `contract` block as a contributor-facing optimization spec, not a bag of tags. Keep it deliberate and minimal.

Use the generated canonical reference in [`catalog.md`](catalog.md#canonical-contract-system) for the full glossary of functions, metrics, and measures. In `CONTRIBUTING.md`, focus on these decision rules:

- Pick 1-2 `functions` that describe the published job-to-be-done, not an internal implementation step.
- Pick the smallest metric set that captures what a downstream optimizer should improve without changing the skill's purpose.
- Declare `measure` explicitly for every metric. Prefer `deterministic`, then `verifier_backed`, and use `judge` only when rubric-based evaluation is genuinely necessary.
- When `measure: judge`, include a stable `rubric_ref`. When `measure: verifier_backed`, include `verifier_ref`.
- Use `success_conditions`, `invariants`, and `source_assertions` to document what must remain fixed while the skill is optimized.
- Reserve `output_quality` for genuinely judge-only artifact quality; it always needs a rubric, and `calibration_ref`, `trials`, and `success_mode` become important once the metric is used for repeatable optimization rather than one-off review.

### 4. CI Validation

CI runs on pull requests and pushes to `main`. It automatically:
- Validates `registry.yaml` against the JSON Schema and touched-skill contract rules (diff-aware vs the PR base branch or prior push commit).
- Runs pinned `skill-linter` on skills you changed when they declare GitHub `source` and `contract.source_assertions`.
- Checks that referenced GitHub repos are reachable and that expected manifests or paths resolve as validated by `scripts/validate_registry.py`.
- Clones the plugins you touched and checks each registry skill `name` against the upstream `SKILL.md` frontmatter.

### Skill name drift

A registry skill `name` must match the `name` in that skill's upstream `SKILL.md` frontmatter — that is the value Claude Code registers as the slash command. If they disagree, the catalog and site publish a command that resolves to nothing.

`scripts/validate_registry.py --check-skill-names` clones each plugin's source and compares. Run it yourself with `--diff-base origin/main` to check only the plugins you touched:

```bash
python3 scripts/validate_registry.py --diff-base origin/main --check-skill-names
```

It **fails** when a registry skill has no upstream `SKILL.md` declaring that name. It **warns**, without failing, when:

- the registry and the upstream frontmatter disagree on `user-invocable` (remember the registry value is catalog-only — the source `SKILL.md` is what controls the `/` menu);
- a `strict: false` plugin has upstream skills missing from `registry.yaml`. Those install anyway, since the whole `skills_dir` is loaded, so they are live but undocumented commands. For `strict: true` plugins the registry list is a curated subset by design and is not flagged.

Most drift starts upstream, where no registry PR is involved, so the same sweep runs weekly across every plugin (github / git / git-subdir) via the `Upstream Plugin Checks` workflow, which also reports plugins missing a `.codex-plugin/plugin.json` (see below).

### Codex-manifest readiness

Codex discovers a plugin's skills from that plugin's own `.codex-plugin/plugin.json` `skills` path. A skill-bearing plugin whose source repo ships no such manifest installs with **zero skills under Codex**. Because that is an upstream repo property the registry can't fix, `scripts/validate_registry.py --check-codex-manifests` only **warns** (never fails) — it clones each plugin and lists those lacking a `.codex-plugin/plugin.json`. It runs weekly alongside skill-name drift in the `Upstream Plugin Checks` workflow. To fix a warned plugin, add a `.codex-plugin/plugin.json` (with a `skills` path) to its source repo — use `.codex-plugin/` rather than `.claude-plugin/plugin.json`, which would conflict with a `strict: false` entry's Claude install.

### 5. Review and Merge

Once CI passes and the PR is reviewed, it will be merged and the plugin will be available to all users who have added this marketplace.

## Updating a Plugin Version

Plugin versions are checked automatically every week. If you bump the `version` field in your repo's `plugin.json`, a PR will be auto-created to update `registry.yaml`.

You can also manually update the `version` field in `registry.yaml` and submit a PR.

## Adding a New Category

Add the category to the `categories` map in `registry.yaml`:

```yaml
categories:
  your-category:
    name: Your Category Name
    description: What plugins in this category do
```
