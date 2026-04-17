# opendatahub-io Skills Registry

[![Validate Registry](https://github.com/opendatahub-io/skills-registry/actions/workflows/validate.yml/badge.svg)](https://github.com/opendatahub-io/skills-registry/actions/workflows/validate.yml)

Central registry for AI skills and plugins developed across the opendatahub-io organization.

This registry serves as a **Claude Code marketplace** with native plugin management, and as a **skill catalog** for discovering plugins to use with other agent harnesses.

## Installation

### Claude Code

This registry integrates natively as a Claude Code marketplace:

```bash
# Add the marketplace
claude plugin marketplace add opendatahub-io/skills-registry

# Browse available plugins
/plugin

# Install a plugin
/plugin install rfe-creator@opendatahub-skills

# Update plugins
/plugin update
```

#### Team Setup

Add to your project's `.claude/settings.json` to auto-enable for all developers:

```json
{
  "extraKnownMarketplaces": {
    "opendatahub-skills": {
      "source": { "source": "github", "repo": "opendatahub-io/skills-registry" }
    }
  },
  "enabledPlugins": {
    "rfe-creator@opendatahub-skills": true
  }
}
```

### Other Agent Harnesses

Other platforms (Cursor, Gemini CLI, Codex, OpenCode) do not have a marketplace aggregation mechanism. Install plugins directly from their source repositories instead:

#### Gemini CLI

```bash
gemini extensions install https://github.com/n1hility/assess-rfe
```

#### Codex

```bash
git clone https://github.com/n1hility/assess-rfe ~/.codex/assess-rfe
mkdir -p ~/.agents/skills
ln -s ~/.codex/assess-rfe/skills ~/.agents/skills/assess-rfe
```

#### OpenCode

Add to your `opencode.json`:

```json
{
  "plugin": ["assess-rfe@git+https://github.com/n1hility/assess-rfe.git"]
}
```

#### Cursor

```
/add-plugin https://github.com/n1hility/assess-rfe
```

Replace the repo URL with the plugin you want to install. See [catalog.md](catalog.md) for the full list of plugins and their source repositories.

> **Note:** Multi-harness support depends on each plugin repo having the appropriate configuration files (`.codex/`, `.opencode/`, `gemini-extension.json`, `.cursor-plugin/`). Not all plugins may support all platforms. Check the plugin's repository for platform-specific instructions.

## Available Plugins

See [catalog.md](catalog.md) for the full list of plugins, skills, and install commands.

## Structure

| File | Purpose |
|------|---------|
| `registry.yaml` | Source of truth for all plugins and skills |
| `.claude-plugin/marketplace.json` | Generated Claude Code marketplace manifest |
| `catalog.md` | Auto-generated human-readable catalog |
| `schema/registry.schema.json` | JSON Schema for validation |
| `scripts/` | Sync, validation, and automation scripts |
| `ARCHITECTURE.md` | Architecture and design documentation |

## Adding a Plugin

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on adding your plugin to this registry.

## License

Apache License 2.0 — see [LICENSE](LICENSE).
