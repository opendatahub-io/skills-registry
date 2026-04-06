# opendatahub-io Skills Registry

Central registry for AI skills and plugins developed across the opendatahub-io organization.
Works as both a **Claude Code marketplace** (native integration) and a **universal skill catalog** for other agent harnesses.

## Quick Start

### Claude Code

```bash
# Add this marketplace
claude plugin marketplace add opendatahub-io/skills-registry

# Browse and install plugins
/plugin
```

Or install a specific plugin:

```bash
/plugin install agent-eval-harness@opendatahub-skills
```

### Team Setup

Add to your project's `.claude/settings.json` to auto-enable for all developers:

```json
{
  "extraKnownMarketplaces": {
    "opendatahub-skills": {
      "source": { "source": "github", "repo": "opendatahub-io/skills-registry" }
    }
  },
  "enabledPlugins": {
    "agent-eval-harness@opendatahub-skills": true
  }
}
```

### Other Agent Harnesses

Fetch `registry.yaml` directly and parse it — it contains all metadata including per-harness install instructions, skill lists, and source references.

## Structure

| File | Purpose |
|------|---------|
| `registry.yaml` | Source of truth for all plugins and skills |
| `.claude-plugin/marketplace.json` | Generated Claude Code marketplace manifest |
| `catalog.md` | Auto-generated human-readable catalog |
| `schema/registry.schema.json` | JSON Schema for validation |
| `scripts/` | Sync, validation, and automation scripts |

## Available Plugins

See [catalog.md](catalog.md) for the full list of plugins and skills.

## Adding a Plugin

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on adding your plugin to this registry.
