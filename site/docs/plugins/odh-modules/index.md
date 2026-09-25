---
title: odh-modules
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-modules

ODH module operator scaffolding, migration, and compliance checks

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Tags**: <span class="tag-pill">operator</span> <span class="tag-pill">modules</span> <span class="tag-pill">scaffolding</span> <span class="tag-pill">compliance</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/module-compliance`](module-compliance.md) | Check an ODH module operator repository for contract violations against the platform onboarding guide. Validates PlatformObject status, CRD structure, Helm chart content, webhook ownership, metadata conventions, and reconciler chain ordering. Use during code review or after scaffolding a new module. | :material-check: |
| [`/module-migrate`](module-migrate.md) | Read existing in-tree ODH operator component code and produce a step-by-step extraction checklist for migrating it to a standalone module. Analyzes controller logic, webhooks, RBAC, embedded manifests, and DSC field mappings. Use when extracting a component from the monolithic operator into its own module repo. | :material-check: |
| [`/module-scaffold`](module-scaffold.md) | Given a component name, generate a complete standalone ODH module operator repository. Produces Go module, CRD types implementing PlatformObject, controller skeleton with reconciler builder pattern, Helm chart, Makefile, CI config, singleton webhook, and AGENTS.md. Use when starting a new module from scratch. | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-modules@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-modules` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
