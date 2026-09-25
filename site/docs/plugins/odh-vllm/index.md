---
title: odh-vllm
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-vllm

vLLM backport triage, cherry-pick automation, and requirements comparison

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [DevOps & CI/CD](../../categories/devops.md)
    - **Tags**: <span class="tag-pill">vllm</span> <span class="tag-pill">backport</span> <span class="tag-pill">release</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/vllm-backport-check-backported`](vllm-backport-check-backported.md) | Check which candidate PRs have already been cherry-picked into the downstream branch. Use after classify-and-filter to mark already_backported on each PR. Fully deterministic — compares merge SHAs and PR titles. | :material-check: |
| [`/vllm-backport-cherry-pick`](vllm-backport-cherry-pick.md) | Auto cherry-pick backport candidates and create a draft PR on the downstream repo. Use after scoring to attempt clean cherry-picks for ai-fixable candidates. The agent must still do semantic validation on the result. | :material-check: |
| [`/vllm-backport-classify`](vllm-backport-classify.md) | Classify bugfix PRs by type (runtime_bug, platform_specific, unclear, not_bugfix) and filter by file existence at a release tag. Use after fetching raw PRs to produce a filtered candidate list. PRs marked "unclear" need agent review. | :material-check: |
| [`/vllm-backport-fetch-prs`](vllm-backport-fetch-prs.md) | Fetch merged bugfix PRs from vllm-project/vllm within a date window. Use when starting a backport triage run to get raw PR data from GitHub. Outputs a JSON array of PR objects with labels, authors, and merge commits. | :material-check: |
| [`/vllm-backport-push-report`](vllm-backport-push-report.md) | Push a triage report to GitHub under a timestamped directory in reports/. Use after the agent writes the report markdown and has ranked.json ready. Outputs the report URL to stdout. | :material-check: |
| [`/vllm-backport-score-rank`](vllm-backport-score-rank.md) | Score and rank backport candidates using a composite formula based on verdict, severity, scope, risk, and self-containedness. Use after the agent completes semantic analysis to produce a prioritized ranked list. | :material-check: |
| [`/vllm-compare-reqs`](vllm-compare-reqs.md) | Use this skill to compare vllm requirements files between versions | :material-check: |
| [`/vllm-slack-summary`](vllm-slack-summary.md) | Use this skill to generate slack summaries of vLLM CI SIG Slack channel activity for the RHAIIS midstream release team | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-vllm@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-vllm` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
