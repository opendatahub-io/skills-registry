---
title: odh-llm-d
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-llm-d

llm-d release orchestration for opendatahub-io

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Scope**: Team-specific
    - **Category**: [DevOps & CI/CD](../../categories/devops.md)
    - **Tags**: <span class="tag-pill">llm-d</span> <span class="tag-pill">release</span> <span class="tag-pill">konflux</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/ai-gateway-operator-manifest-update`](ai-gateway-operator-manifest-update.md) | Update batch-gateway manifests in opendatahub-io/ai-gateway-operator when the pinned llm-d-batch-gateway-operator main commit changes. | :material-check: |
| [`/odh-llm-d-release`](odh-llm-d-release.md) | Orchestrate the opendatahub-io release for all llm-d components in one cycle. Collects upstream(llm-d) versions, auto-discovers the release tracker issue, then spawns parallel sub-agents — one per component (release branch, Konflux onboarder workflow, PR validation, approve+merge, Quay image verify, GitHub draft release) plus one KServe metadata PR sub-agent — and posts the final #Release# tracker comment. Use when the release manager runs on/before ODH code-freeze date for the llm-d team. | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-llm-d@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-llm-d` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
