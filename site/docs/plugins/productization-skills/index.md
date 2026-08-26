---
title: productization-skills
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# productization-skills

Claude Code plugin with specialized skills for DevOps and cloud-native development workflows. Provides skills for GitLab CI/CD analysis, AWS CloudWatch Logs troubleshooting, Slack integration, GitLab branch management, Jira utilities, Konflux ITS analysis, cloud infrastructure provisioning via mapt, and Google Workspace integration.

!!! info "Plugin Details"

    - **Version**: 0.8.1
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Scope**: Team-specific
    - **Category**: [DevOps & CI/CD](../../categories/devops.md)
    - **Repository**: [opendatahub-io/productization-skills](https://github.com/opendatahub-io/productization-skills)
    - **Tags**: <span class="tag-pill">gitlab</span> <span class="tag-pill">aws</span> <span class="tag-pill">slack</span> <span class="tag-pill">jira</span> <span class="tag-pill">konflux</span> <span class="tag-pill">mapt</span> <span class="tag-pill">devops</span> <span class="tag-pill">ci-cd</span> <span class="tag-pill">cloud</span> <span class="tag-pill">provisioning</span> <span class="tag-pill">google-workspace</span> <span class="tag-pill">reporting</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/gitlab-job-analyzer`](gitlab-job-analyzer.md) | Analyze GitLab CI/CD job failures with structured scripts and error pattern recognition | :material-check: |
| [`/aws-log-analyzer`](aws-log-analyzer.md) | Troubleshoot and analyze AWS CloudWatch Logs for debugging and monitoring | :material-check: |
| [`/slack-utilities`](slack-utilities.md) | Search messages, post updates, and interact with Slack workspaces | :material-check: |
| [`/gitlab-branch-manager`](gitlab-branch-manager.md) | Create and protect GitLab branches with configurable protection rules | :material-check: |
| [`/jira-utilities`](jira-utilities.md) | Manage Jira issues with JQL search, create/update issues, link issues, and sprint info | :material-check: |
| [`/jira-cve-tracker`](jira-cve-tracker.md) | CVE deduplication and release-date clustering for Jira issues | :material-check: |
| [`/jira-release-setup`](jira-release-setup.md) | Set up Jira release versions and manage release workflows | :material-check: |
| [`/jira-sprint-manager`](jira-sprint-manager.md) | Create sprints and assign issues to sprints on Jira boards | :material-check: |
| [`/jira-gap-audit`](jira-gap-audit.md) | Audit Jira releases for gaps in issue coverage | :material-check: |
| [`/mapt-provisioner`](mapt-provisioner.md) | Provision and manage cloud VMs on AWS and Azure using mapt | :material-check: |
| [`/konflux-its-analyzer`](konflux-its-analyzer.md) | Analyze Konflux integration test scenario failures | :material-check: |
| [`/gitlab-code-review`](gitlab-code-review.md) | Structured GitLab merge request code review | :material-check: |
| [`/slack-webhook`](slack-webhook.md) | Post messages to Slack channels via incoming webhooks | :material-check: |
| [`/weekly-status`](weekly-status.md) | Generate weekly status reports from project activity | :material-check: |
| [`/gws-calendar-reader`](gws-calendar-reader.md) | Read Google Calendar events and check free/busy status | :material-check: |
| [`/gws-doc-action-extractor`](gws-doc-action-extractor.md) | Extract action items from Google Docs | :material-check: |
| [`/gws-drive-reader`](gws-drive-reader.md) | List, search, and read files from Google Drive | :material-check: |
| [`/gws-slides-analyzer`](gws-slides-analyzer.md) | Read, search, and create Google Slides presentations | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install productization-skills@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `productization-skills` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
