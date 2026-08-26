# Getting Started

## What is the Skills Registry?

The OpenDataHub Skills Registry is a centralized marketplace that aggregates
Claude Code and OpenAI Codex plugins from multiple repositories into a single
discoverable catalog. Each plugin provides AI-powered skills for software
engineering workflows — from RFE creation and strategy review to security
analysis and test planning.

The same `registry.yaml` is projected into a native marketplace for each
harness: `.claude-plugin/marketplace.json` for Claude Code and
`.agents/plugins/marketplace.json` for Codex.

## Claude Code

### Add the Marketplace

```bash
claude plugin marketplace add opendatahub-io/skills-registry
```

This gives Claude Code access to all plugins in the registry. You can then
browse and install individual plugins.

### Browse Plugins

Once the marketplace is added, use the `/plugin` command to see available plugins:

```bash
/plugin
```

### Install a Plugin

Install a specific plugin by name:

```bash
/plugin install rfe-creator@opendatahub-skills
```

After installation, the plugin's skills become available as slash commands
(e.g., `/rfe.create`, `/rfe.review`).

### Test from a Branch

To test marketplace changes before they're merged:

```bash
claude plugin marketplace add opendatahub-io/skills-registry#branch-name
```

## OpenAI Codex

### Add the Marketplace

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```

Codex reads the registry's `.agents/plugins/marketplace.json`. Then open the
plugin browser to enable plugins:

```bash
/plugins
```

To test marketplace changes from a branch before they're merged, pin the ref:

```bash
codex plugin marketplace add opendatahub-io/skills-registry --ref branch-name
```

> **Skill discovery under Codex:** Codex discovers a plugin's skills from that
> plugin's own `.codex-plugin/plugin.json` manifest (its `skills` path) — the
> marketplace entry does not inject a skills path. A plugin that has no
> `.codex-plugin/plugin.json` in its source repo installs with no skills under
> Codex until one is added upstream.

## Contributing

See the [Contributing Guide](https://github.com/opendatahub-io/skills-registry/blob/main/CONTRIBUTING.md)
for how to add your own plugins to the registry.
