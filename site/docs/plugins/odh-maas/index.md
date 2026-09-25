---
title: odh-maas
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-maas

MaaS nightly QE impact analysis

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Scope**: Team-specific
    - **Category**: [DevOps & CI/CD](../../categories/devops.md)
    - **Tags**: <span class="tag-pill">maas</span> <span class="tag-pill">qe</span> <span class="tag-pill">autofix</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/maas-nightly-qe-impact`](maas-nightly-qe-impact.md) | Assess whether a Models-as-a-Service autofix change requires follow-up in opendatahub-tests or ods-ci nightly QE pipelines. Runs as a Jira autofix post_review extension for the Model as a Service component. Appends a Nightly QE Impact section to the PR description and writes informational findings. Use when autofix completes a fix in models-as-a-service. | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-maas@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-maas` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
