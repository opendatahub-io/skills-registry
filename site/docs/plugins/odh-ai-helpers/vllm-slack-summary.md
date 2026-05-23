---
title: vllm-slack-summary
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# vllm-slack-summary

Generate a summary of the vLLM CI SIG Slack channel activity for the
RHAIIS midstream release team. Uses slackdump to export channel messages,
generates a markdown transcript, then analyzes it for breaking changes,
hardware issues, CI/CD infrastructure changes, dependency updates,
performance regressions, and upstream release stability.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![vllm-slack-summary diagram](vllm-slack-summary.svg)
</div>

## Arguments

```bash
/vllm-slack-summary [--days] [--output-dir]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--days` |  | `7` | Number of days of Slack history to export |
| `--output-dir` |  | `vllm_slack_summary` | Output directory for transcript and summary |

## Usage

```bash
/vllm-slack-summary
/vllm-slack-summary --days 14
```
