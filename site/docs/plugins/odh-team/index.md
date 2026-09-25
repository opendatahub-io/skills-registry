---
title: odh-team
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-team

Team weekly reports, engineer activity snapshots, and delivery postmortems

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Tags**: <span class="tag-pill">reporting</span> <span class="tag-pill">postmortem</span> <span class="tag-pill">jira</span> <span class="tag-pill">github</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/create-delivery-postmortem`](create-delivery-postmortem.md) | Use when a release delay, missed deadline, or delivery incident needs a structured post-mortem. Facilitates context gathering, timeline synthesis, and interactive Five Whys root cause analysis. Produces an executive-ready document in HTML or Markdown. | :material-check: |
| [`/engineer-snapshot`](engineer-snapshot.md) | Generate an engineer activity snapshot showing active JIRA issues with days open, blocked work, upstream PRs awaiting review, recently merged PRs, and open action items from 1:1 notes. Requires a team config YAML file. Use when the user asks to review an engineer's status, check someone's workload, or prepare for a 1:1. | :material-check: |
| [`/team-weekly-report`](team-weekly-report.md) | Generate a weekly team status report combining JIRA and GitHub data. Fetches closed, open, stale, and blocked issues plus PR activity for each team member. Requires a team config YAML file with JIRA project, GitHub repos, and team member mappings. Use when the user asks for a weekly report, team status, or team update. | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-team@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-team` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
