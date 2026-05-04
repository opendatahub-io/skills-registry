---
title: rfe.create
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.create

Generate new RFEs from problem statements. Asks clarifying questions
(unless --headless), then produces well-formed RFEs with YAML frontmatter.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rfe.create diagram](rfe.create.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--headless` |  | — | Skip clarifying questions, generate directly from input |
| `--priority` |  | `Normal` | Override default priority |
| `--labels` |  | — | Labels to apply to created RFEs |
| `--rfe-id` |  | — | Pre-assigned RFE ID (placeholder file must exist) |

## Usage

```
/rfe.create Users need better error messages
/rfe.create --headless --priority Critical Fix dashboard latency
```
