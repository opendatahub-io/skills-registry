# Getting Started

## What is the Skills Registry?

The OpenDataHub Skills Registry is a centralized marketplace that aggregates
Claude Code plugins from multiple repositories into a single discoverable catalog.
Each plugin provides AI-powered skills for software engineering workflows — from
RFE creation and strategy review to security analysis and test planning.

## Add the Marketplace

```bash
claude plugin marketplace add opendatahub-io/skills-registry
```

This gives Claude Code access to all plugins in the registry. You can then
browse and install individual plugins.

## Browse Plugins

Once the marketplace is added, use the `/plugin` command to see available plugins:

```bash
/plugin
```

## Install a Plugin

Install a specific plugin by name:

```bash
/plugin install rfe-creator@opendatahub-skills
```

After installation, the plugin's skills become available as slash commands
(e.g., `/rfe.create`, `/rfe.review`).

## Test from a Branch

To test marketplace changes before they're merged:

```bash
claude plugin marketplace add opendatahub-io/skills-registry#branch-name
```

## Contributing

See the [Contributing Guide](https://github.com/opendatahub-io/skills-registry/blob/main/CONTRIBUTING.md)
for how to add your own plugins to the registry.
