---
title: pf-migration
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# pf-migration

PF version migration -- breaking change detection, class scanning, upgrade planning

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: UXD Team
    - **License**: MIT
    - **Scope**: Generic
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Tags**: <span class="tag-pill">patternfly</span> <span class="tag-pill">migration</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/pf-css-migration-scan`](pf-css-migration-scan.md) | Scan code for legacy PatternFly CSS classes and recommend PF6-safe replacements. Use when upgrading from PF4/PF5 or auditing a codebase for deprecated class names. | :material-check: |
| [`/pf-react-migration-scan`](pf-react-migration-scan.md) | Scan code for @patternfly/react-* API breaking changes and produce a markdown report. Use when upgrading PatternFly React versions, auditing component API usage, or checking for removed props, renamed components, or import path changes. | :material-check: |
| [`/pf-release-candidate-update`](pf-release-candidate-update.md) | Update @patternfly/* npm dependencies to the latest release candidate versions. Use when testing the next PF release or bumping to RC packages. | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install pf-migration@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `pf-migration` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
