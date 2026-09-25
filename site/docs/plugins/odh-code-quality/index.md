---
title: odh-code-quality
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-code-quality

CodeRabbit review triage and project-conformant unit test generation

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Scope**: Generic
    - **Category**: [Code Quality](../../categories/code-quality.md)
    - **Tags**: <span class="tag-pill">code-review</span> <span class="tag-pill">coderabbit</span> <span class="tag-pill">unit-tests</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/coderabbit-review`](coderabbit-review.md) | Use when you need to evaluate CodeRabbit PR comments and fix or reply | :material-check: |
| [`/unit-test-project-conformant`](unit-test-project-conformant.md) | Use this skill to write unit tests that strictly conform to the project's existing testing structure, patterns, and style by learning from similar tests before writing anything new. | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-code-quality@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-code-quality` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
