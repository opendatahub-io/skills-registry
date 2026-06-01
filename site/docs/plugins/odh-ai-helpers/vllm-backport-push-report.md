---
title: vllm-backport-push-report
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# vllm-backport-push-report

Push a triage report to a GitHub repository under a timestamped
directory in reports/. Copies the report markdown and candidates JSON,
commits, pushes, and prints the GitHub URL to stdout.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![vllm-backport-push-report diagram](vllm-backport-push-report.svg)
</div>

## Arguments

```bash
/vllm-backport-push-report [--report] [--candidates] [--version]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--report` | :material-check: | - | Path to report markdown file |
| `--candidates` | :material-check: | - | Path to ranked.json |
| `--version` | :material-check: | - | Release version (e.g., v0.13.0) |

## Usage

```bash
/vllm-backport-push-report --report artifacts/report.md --candidates artifacts/ranked.json --version v0.13.0
```
