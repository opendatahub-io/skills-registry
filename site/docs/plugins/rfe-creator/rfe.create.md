---
title: rfe.create
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.create

Generate new RFEs from problem statements or ideas. Loads the assess-rfe
rubric (bootstrapping it if needed), asks 2-5 clarifying questions about
customers, business justification, user problems, scope, and success
criteria, then produces well-formed RFEs using a template. Each RFE
describes WHAT and WHY (business needs), never HOW (implementation).
Supports headless mode for batch/CI use.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rfe.create diagram](rfe.create.svg)
</div>

## Arguments

```bash
/rfe.create <problem-statement> [--headless] [--priority <value>] [--labels <csv>] [--rfe-id <ID>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `problem-statement` | :material-check: | - | The problem statement, idea, or need to turn into RFEs |
| `--headless` |  | - | Skip clarifying questions (Step 2), generate RFEs directly from the input |
| `--priority` |  | `Normal` | Override default priority for created RFEs |
| `--labels` |  | - | Labels to apply to created RFEs |
| `--rfe-id` |  | - | Pre-assigned RFE ID; use this instead of allocating a new one. The placeholder file must already exist. |

## Usage

```bash
/rfe.create Users need better error messages when model serving fails
/rfe.create --headless --priority Critical Fix dashboard latency for large clusters
/rfe.create --headless --rfe-id RFE-003 --labels candidate-3.5 Support GPU sharing
```
