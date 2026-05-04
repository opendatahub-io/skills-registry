<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.split

Decompose oversized RFEs into appropriately-scoped pieces. Generates
child RFEs, reviews them, and validates coverage.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rfe.split diagram](rfe.split.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--headless` |  | — | Suppress end-of-run summary |

## Usage

```
/rfe.split RHAIRFE-1234
```
