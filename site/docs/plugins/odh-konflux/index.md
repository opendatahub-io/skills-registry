---
title: odh-konflux
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-konflux

Konflux application and component management

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [DevOps & CI/CD](../../categories/devops.md)
    - **Tags**: <span class="tag-pill">konflux</span> <span class="tag-pill">ci</span> <span class="tag-pill">onboarding</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/konflux-application`](konflux-application.md) | Manage Konflux application | :material-check: |
| [`/konflux-component`](konflux-component.md) | Manage Konflux component | :material-check: |
| [`/konflux-sandbox-onboarding`](konflux-sandbox-onboarding.md) | Guide AIPCC engineers through obtaining access to the shared Konflux sandbox, onboarding a user-selected GitHub repository or dummy project, and verifying pull-request and push pipelines. Use when an engineer wants a hands-on Konflux staging experiment; exclude production tenants and release configuration. | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-konflux@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-konflux` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
