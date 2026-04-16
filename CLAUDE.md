# Skills Registry

Skills and Claude Code plugins marketplace for the opendatahub-io organization. `registry.yaml` is the single source of truth — all other files are generated from it.

## Common Commands

```bash
# Validate registry.yaml against schema
python3 scripts/validate_registry.py

# Regenerate marketplace.json from registry.yaml
python3 scripts/sync_marketplace.py

# Regenerate catalog.md from registry.yaml
python3 scripts/generate_catalog.py

# Check plugin repo versions against registry
python3 scripts/check_versions.py --dry-run
```

Always run all three (validate, sync, generate) before committing changes to registry.yaml. CI will fail if generated files are out of sync.

## Architecture

- `registry.yaml` — source of truth, edited by humans
- `.claude-plugin/marketplace.json` — generated, Claude Code reads this
- `catalog.md` — generated, human-readable listing
- `schema/registry.schema.json` — JSON Schema for validation
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

### Agents

Plugins can include agents (defined in `agents/` directories) alongside skills. Agents run in isolated context windows and are auto-delegated by Claude or selected via `/agents`. The `agents_dir` field works like `skills_dir` — only valid with `strict: false`.

## Adding a Plugin

See @CONTRIBUTING.md for the full process. Quick checklist:

1. Add entry to `registry.yaml` with correct `strict`/`skills_dir` settings
2. Run `python3 scripts/validate_registry.py`
3. Run `python3 scripts/sync_marketplace.py`
4. Run `python3 scripts/generate_catalog.py`
5. Commit all changed files and open a PR

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
