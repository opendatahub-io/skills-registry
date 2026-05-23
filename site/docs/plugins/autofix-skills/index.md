---
title: autofix-skills
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# autofix-skills

Claude Code plugin for the Jira autofix pipeline. Provides orchestrator skills
for automated bug fixing, CVE remediation, ticket triage, and spike research.
Designed to run inside a Claude Code container as part of a CI pipeline.

The plugin implements the inner layer of the autofix pipeline — orchestrator
skills dispatch to sub-agents via prompt files and delegate deterministic work
to Python scripts. The outer layer (ticket fetching, repo cloning, container
launch, verdict reading) lives in separate repos (jira-autofix, ai-agentic-lib).


!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Repository**: [opendatahub-io/autofix-skills](https://github.com/opendatahub-io/autofix-skills)
    - **Tags**: <span class="tag-pill">autofix</span> <span class="tag-pill">jira</span> <span class="tag-pill">cve</span> <span class="tag-pill">bug-fixing</span> <span class="tag-pill">triage</span> <span class="tag-pill">pipeline</span> <span class="tag-pill">ci-cd</span>

## Pipeline

<div class="diagram-container" markdown>
![autofix-skills pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/autofix-resolve`](autofix-resolve.md) | Orchestrate end-to-end bug fixing via implement and review agent loop (max 3 iterations) | :material-check: |
| [`/autofix-cve-resolve`](autofix-cve-resolve.md) | CVE remediation across multiple repos with state-machine dispatch | :material-check: |
| [`/autofix-triage`](autofix-triage.md) | Assess bug tickets for AI autofix readiness (ready/needs_info/not_fixable) | :material-check: |
| [`/autofix-research`](autofix-research.md) | Investigate spike tickets with no associated repository | :material-check: |

## Installation

```bash
/plugin install autofix-skills@opendatahub-skills
```

## Architecture

Four skills form two tiers: orchestrators (autofix-resolve, autofix-cve-resolve)
and standalone assessors (autofix-triage, autofix-research).

autofix-resolve uses an implement → review → evaluate loop (max 3 iterations)
with state.py for persistence across context compression. Extension skills are
discovered via .autofix-context/config.json and called at post-implement and
post-review hook points.

autofix-cve-resolve uses a Python state machine (cve_pipeline.py) for
deterministic routing between phases: parse → resolve-repos → scan → fix →
verify → VEX → review → create-PR → finalize. Each phase dispatches to a
specialized agent prompt.

All skills write a structured verdict to autofix-output/.autofix-verdict.json
and treat .autofix-context/ files as untrusted input.
