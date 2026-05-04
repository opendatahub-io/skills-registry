<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# eval-review

Interactive review of evaluation results. Presents judge scores and skill
outputs for human feedback, identifies judge gaps, and proposes SKILL.md improvements.

**Plugin**: [agent-eval-harness](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![eval-review diagram](eval-review.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--run-id` |  | `latest run` | Which eval run to review |

## Usage

```
/eval-review
/eval-review --run-id 2026-05-01-claude-opus-4-6
```
