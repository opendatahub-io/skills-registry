---
title: odh-ai-helpers
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-ai-helpers

A comprehensive suite of developer productivity tools for Python packaging,
CI/CD debugging, upstream maintenance, and workflow automation. The plugin
spans three functional domains: (1) a Python packaging toolchain that can
analyze build complexity, resolve full dependency trees, locate source repos,
find and check licenses against Red Hat redistribution policy, discover build
environment variables, and surface known packaging bugs; (2) a vLLM backport
triage pipeline that fetches upstream bugfix PRs, classifies them, checks
for existing cherry-picks, scores and ranks candidates, auto-cherry-picks
clean fixes, pushes reports, compares requirements across versions, and
summarizes Slack channel activity; and (3) general-purpose skills for ADR
review panels, GitLab CI debugging, Jira chat-log uploads, and Git
shallow-cloning.

The Python packaging skills are designed to work both independently and as a
coordinated pipeline through the python-packaging-investigator agent, which
orchestrates all packaging skills in parallel and produces a standardized
build analysis report. The vLLM backport skills form a linear pipeline from
PR fetching through classification, deduplication, scoring, and cherry-picking,
with each stage producing JSON artifacts consumed by the next.


!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Scope**: Generic
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Repository**: [opendatahub-io/ai-helpers](https://github.com/opendatahub-io/ai-helpers)
    - **Tags**: <span class="tag-pill">python-packaging</span> <span class="tag-pill">licensing</span> <span class="tag-pill">dependencies</span> <span class="tag-pill">gitlab</span> <span class="tag-pill">jira</span> <span class="tag-pill">adr</span> <span class="tag-pill">git</span> <span class="tag-pill">automation</span>

## Pipeline

<div class="diagram-container" markdown>
![odh-ai-helpers pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/adr-review`](adr-review.md) | Review an Architectural Decision Record (ADR) using a team of specialist reviewer subagents and produce a consolidated report | :material-check: |
| [`/gitlab-pipeline-debugger`](gitlab-pipeline-debugger.md) | Debug and monitor GitLab CI/CD pipelines for merge requests, check pipeline status, view job logs, and troubleshoot CI failures | :material-check: |
| [`/git-shallow-clone`](git-shallow-clone.md) | Perform a shallow clone of a Git repository to a temporary location | :material-check: |
| [`/jira-upload-chat-log`](jira-upload-chat-log.md) | Export and upload the current chat conversation as a markdown file attachment to a Jira ticket | :material-check: |
| [`/python-full-deps`](python-full-deps.md) | Resolve the full install-time dependency tree for a Python package with environment markers | :material-check: |
| [`/python-packaging-bug-finder`](python-packaging-bug-finder.md) | Find known packaging bugs, fixes, and workarounds for Python projects by searching GitHub issues | :material-check: |
| [`/python-packaging-complexity`](python-packaging-complexity.md) | Analyze Python package build complexity by inspecting PyPI metadata, compilation requirements, and distribution types | :material-check: |
| [`/python-packaging-env-finder`](python-packaging-env-finder.md) | Investigate environment variables that can be set when building Python wheels for a given project | :material-check: |
| [`/python-packaging-license-checker`](python-packaging-license-checker.md) | Check whether a Python package license is compatible with redistribution in Red Hat products | :material-check: |
| [`/python-packaging-license-finder`](python-packaging-license-finder.md) | Deterministically find license information for Python packages by checking PyPI metadata and Git repository LICENSE files | :material-check: |
| [`/python-packaging-source-finder`](python-packaging-source-finder.md) | Locate source code repositories for Python packages by analyzing PyPI metadata and project URLs | :material-check: |
| [`/vllm-backport-fetch-prs`](vllm-backport-fetch-prs.md) | Fetch merged bugfix PRs from upstream vLLM within a configurable date window using GitHub CLI | :material-check: |
| [`/vllm-backport-classify`](vllm-backport-classify.md) | Classify PRs by backport relevance using labels, title patterns, and file-existence heuristics | :material-check: |
| [`/vllm-backport-check-backported`](vllm-backport-check-backported.md) | Check if PRs are already cherry-picked in a downstream release branch via SHA and title matching | :material-check: |
| [`/vllm-backport-score-rank`](vllm-backport-score-rank.md) | Score and rank backport candidates by severity, scope, and risk using a deterministic composite score | :material-check: |
| [`/vllm-backport-push-report`](vllm-backport-push-report.md) | Push triage report to a GitHub repository with timestamped directory structure | :material-check: |
| [`/vllm-backport-cherry-pick`](vllm-backport-cherry-pick.md) | Attempt automatic cherry-pick of clean backport candidates to a downstream release branch | :material-check: |
| [`/vllm-compare-reqs`](vllm-compare-reqs.md) | Compare Python requirements between upstream vLLM and a downstream fork to identify version mismatches and missing packages | :material-check: |
| [`/vllm-slack-summary`](vllm-slack-summary.md) | Generate a concise Slack-formatted summary of vLLM backport triage results | :material-check: |

## Agents

| Agent | Description |
|-------|-------------|
| python-packaging-investigator | Investigates Python package repositories to analyze build systems, dependencies, and packaging complexity |

## Installation

```bash
/plugin install odh-ai-helpers@opendatahub-skills
```

## Architecture

The plugin follows a modular architecture with three distinct skill families:

**Python Packaging Toolchain** -- Seven skills that share a common pattern of
wrapping helper scripts (Python/Bash) and chaining through skill invocations.
The source-finder locates repositories, the shallow-clone skill provides local
access, and downstream skills (complexity, license-finder, license-checker,
env-finder, bug-finder) analyze different facets. The investigator agent
orchestrates all of them in parallel sub-agents.

**vLLM Backport Pipeline** -- Eight skills forming a linear data pipeline.
Each produces a JSON artifact (raw-prs.json -> filtered.json -> candidates.json
-> analyzed.json -> ranked.json -> cherry-pick-result.json) consumed by the
next stage. The pipeline combines deterministic script-based steps with
agent-driven semantic analysis for unclear classifications.

**Utility Skills** -- Standalone skills (adr-review, gitlab-pipeline-debugger,
jira-upload-chat-log, git-shallow-clone) that operate independently with no
inter-skill dependencies. The adr-review skill uses six parallel reviewer
sub-agents with human-in-the-loop correction before synthesis.
