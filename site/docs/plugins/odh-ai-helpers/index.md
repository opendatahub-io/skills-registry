---
title: odh-ai-helpers
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-ai-helpers

[DEPRECATED] Backwards-compatibility umbrella for the ODH AI Helpers plugins. Re-exports the skills that existed before the split into the individual odh-* plugins under their original odh-ai-helpers:* names, so existing agents and workflows keep working. Install the odh-* plugins you need, then uninstall this one; it will be removed after the migration window.

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Scope**: Generic
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Repository**: [opendatahub-io/ai-helpers](https://github.com/opendatahub-io/ai-helpers)
    - **Tags**: <span class="tag-pill">deprecated</span>

## Agents

| Agent | Description |
|-------|-------------|
| python-packaging-investigator | Investigates Python package repositories to analyze build systems, dependencies, and packaging complexity |

## Installation

**Claude Code**

```bash
/plugin install odh-ai-helpers@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-ai-helpers` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
