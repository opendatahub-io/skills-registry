---
title: disconnected-score
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# disconnected-score

Score a repository's readiness for disconnected / air-gapped OpenShift
deployments. Runs all (or selected) rules from the repo root and produces
an aggregate score with per-rule findings. Supports auto-remediation
(--fix), rule selection (--rules), and multiple output formats (markdown
or JSON). Exits 0 for READY/WARNING, 1 for NOT READY.

**Plugin**: [disconnected-readiness-scorer](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![disconnected-score diagram](disconnected-score.svg)
</div>

## Arguments

```bash
/disconnected-score [--rules <list>] [--fix] [--report <format>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--rules` |  | `all` | Run only specified rules. Aliases: csv, tags, egress, python, manifest. |
| `--fix` |  | - | Attempt auto-remediation where possible (e.g., replace image tags with digests). |
| `--report` |  | `markdown` | Output format for the readiness report. |

## Usage

```bash
/disconnected-score
/disconnected-score --rules csv,tags
/disconnected-score --fix
/disconnected-score --report json
```
