# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Skills and Claude Code plugins marketplace for the opendatahub-io organization. `registry.yaml` is the single source of truth — all other files are generated from it.

## Common Commands

```bash
# Install Python dependencies (needed for all scripts)
pip install pyyaml jsonschema

# Validate registry.yaml against schema
python3 scripts/validate_registry.py

# Regenerate marketplace.json from registry.yaml
python3 scripts/sync_marketplace.py

# Regenerate catalog.md from registry.yaml
python3 scripts/generate_catalog.py

# Regenerate site content from registry.yaml
python3 scripts/generate_site.py

# Check plugin repo versions against registry
python3 scripts/check_versions.py --dry-run

# Validate and also clone/check new plugin repos
python3 scripts/validate_registry.py --diff origin/main --validate-remote-plugins
```

**Before committing any change to `registry.yaml`**, run all four generators (validate, sync marketplace, generate catalog, generate site). CI checks that every generated file matches -- it does not auto-commit.

## Architecture

- `registry.yaml` — source of truth, edited by humans
- `.claude-plugin/marketplace.json` — generated, Claude Code reads this
- `catalog.md` — generated, human-readable listing
- `schema/registry.schema.json` — JSON Schema for validation
- `site/` — MkDocs Material documentation site (generated + static)
- `scripts/` — automation (sync, validate, generate, version check)

See @ARCHITECTURE.md for detailed diagrams and design documentation.

## Key Rules

### strict: false and skills_dir

Plugins without `.claude-plugin/plugin.json` in their repo **must** set `strict: false` and `skills_dir` in their registry entry. Without these, Claude Code cannot discover skills when the plugin is installed via the marketplace. Auto-discovery of `.claude/skills/` only works locally, not for marketplace installs.

- `strict: true` (default): repo has `plugin.json`, Claude Code reads it
- `strict: false`: marketplace defines everything, `skills_dir` required

The schema enforces `skills_dir` requires `strict` to be present (`dependentRequired`), and the validation script checks `skills_dir` is only used with `strict: false`.

### Marketplace JSON format

The `source` field in marketplace.json uses `"source": "github"` (not `"type"`). The `skills` field must be an array (e.g., `["./.claude/skills"]`), not a string. The sync script handles both correctly.

### Agents and MCP servers

Plugins can include agents (defined in `agents/` directories) alongside skills. Agents run in isolated context windows and are auto-delegated by Claude or selected via `/agents`. The `agents_dir` field works like `skills_dir` — only valid with `strict: false`.

Plugins can also provide MCP servers. List them in `mcp_servers: [{name, description}]` so the catalog/site show what the plugin offers (useful for an MCP-only plugin that has no skills, e.g. `pf-mcp`). `mcp_servers` is catalog-only — Claude Code reads the real server config from the source `plugin.json` `mcpServers`, so it is not propagated to `marketplace.json`. Both `agents` and `mcp_servers` render as their own table on the plugin page.

### Meta-plugins (bundles) and skill_count

A plugin with a non-empty `includes: [names...]` is a **meta-plugin** (bundle) that installs those member plugins together. Each member **must** also be registered as its own entry in `registry.yaml` (with a matching name), because Claude Code resolves a plugin's dependencies within the marketplace it was installed from — otherwise the bundle installs zero skills. The bundle's skill count is derived from its members (don't give it its own `skills`/`skill_count`). Members (typically `git-subdir` sub-plugins) **list their own skills** (name + description) so they show on the member page — no `contract` block is required because the canonical-contract requirement applies only to `github`/`git` (`GIT_CLONE_TYPES`) sources; `git-subdir`/`npm`/`local` are exempt (same boundary as skill-linter and skill-name-drift). A member may instead set `skill_count: N` for a count-only display. These fields are catalog-only (not in `marketplace.json`); `check_bundles` in `validate_registry.py` enforces the bundle rules. See @ARCHITECTURE.md and @CONTRIBUTING.md.

## Adding a Plugin

See @CONTRIBUTING.md for the full process. Quick checklist:

1. Add entry to `registry.yaml` with correct `strict`/`skills_dir` settings
2. Run `python3 scripts/validate_registry.py`
3. Run `python3 scripts/sync_marketplace.py`
4. Run `python3 scripts/generate_catalog.py`
5. Run `python3 scripts/generate_site.py`
6. Commit all changed files and open a PR

## Testing a Marketplace Branch

To test changes before merging, install the marketplace from a branch:

```bash
claude plugin marketplace add opendatahub-io/skills-registry#branch-name
```

To update after already adding:

```bash
claude plugin marketplace remove opendatahub-skills
claude plugin marketplace add opendatahub-io/skills-registry#branch-name
```

## References

- [Claude Code skills](https://code.claude.com/docs/en/skills) — SKILL.md frontmatter spec (`user-invocable`, `disable-model-invocation`, `allowed-tools`, etc.)
- [Claude Code sub-agents](https://code.claude.com/docs/en/sub-agents) — agent frontmatter spec
- [Claude Code plugins](https://code.claude.com/docs/en/plugins) — plugin manifest and marketplace format
- [Agent Skills specification](https://agentskills.io/specification) — open standard that Claude Code skills conform to
