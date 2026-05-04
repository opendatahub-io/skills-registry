<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.auto-fix

Batch review, revise, and split operations across many RFEs.
Supports JQL queries for bulk processing.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![rfe.auto-fix diagram](rfe.auto-fix.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--jql` |  | — | JQL query to fetch RFE IDs from Jira |
| `--limit` |  | — | Max number of results from JQL |
| `--batch-size` |  | `50` | Process IDs in batches of this size |
| `--headless` |  | — | Non-interactive mode |
| `--reprocess` |  | — | Reprocess RFEs that had prior runs |
| `--random` |  | — | Process N random RFEs from the batch |

## Usage

```
/rfe.auto-fix RFE-001 RFE-002
/rfe.auto-fix --jql "project=RHAIRFE AND status=New" --limit 20
```
