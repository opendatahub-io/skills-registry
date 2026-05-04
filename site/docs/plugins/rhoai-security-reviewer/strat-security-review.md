<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strat-security-review

Security review orchestrator for STRAT documents. Extracts threat surface,
determines review tier, spawns 3 independent reviewers, synthesizes
consensus findings, and produces a final verdict with confidence tagging.

**Plugin**: [rhoai-security-reviewer](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![strat-security-review diagram](strat-security-review.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `RHAISTRAT_KEY` | :material-check: | — | RHAISTRAT Jira key (e.g., RHAISTRAT-400) |
| `--force` |  | — | Regenerate review even if one already exists |

## Usage

```
/strat-security-review RHAISTRAT-400
/strat-security-review RHAISTRAT-400 --force
```
