<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.speedrun

Execute the full RFE pipeline end-to-end: create, review, auto-fix,
and submit. Supports single ideas, Jira keys, or batch YAML input.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rfe.speedrun diagram](rfe.speedrun.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` |  | — | Path to YAML file with batch entries |
| `--headless` |  | — | Non-interactive mode for CI/eval |
| `--dry-run` |  | — | Skip Jira writes in submit phase |
| `--batch-size` |  | `5` | Override batch size for auto-fix |
| `--announce-complete` |  | — | Print completion marker when done |

## Usage

```
/rfe.speedrun Better dashboard for ML models
/rfe.speedrun --input batch.yaml --headless --dry-run
```
