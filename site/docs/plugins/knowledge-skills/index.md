---
title: knowledge-skills
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# knowledge-skills

Autonomous knowledge management for keeping AI context files (CLAUDE.md,
AGENTS.md) up to date with recent codebase changes. Scans merged PRs from
the last N days, dispatches parallel extraction agents to identify knowledge
items, synthesizes proposed updates, runs an adversarial review, and produces
a git-apply-able patch for human review.

The skill is forge-agnostic (GitHub via gh CLI, GitLab via glab CLI) and
designed for CI pipeline execution. It produces artifacts (patch file,
run report, extraction data) but never creates PRs/MRs itself — external
tooling handles forge interactions.


!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [Documentation](../../categories/documentation.md)
    - **Repository**: [opendatahub-io/knowledge-skills](https://github.com/opendatahub-io/knowledge-skills)
    - **Tags**: <span class="tag-pill">knowledge</span> <span class="tag-pill">context</span> <span class="tag-pill">claude-md</span> <span class="tag-pill">agents-md</span> <span class="tag-pill">pr-analysis</span> <span class="tag-pill">automation</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/knowledge.repo`](knowledge.repo.md) | Scan merged PRs and propose updates to AI context files (CLAUDE.md, AGENTS.md) as a git-apply-able patch | :material-check: |

## Installation

```bash
/plugin install knowledge-skills@opendatahub-skills
```

## Architecture

A 7-phase pipeline with early-exit gates at each phase:
Setup → Fetch PRs → Extract (parallel haiku agents, waves of 10) →
Synthesize (opus) → Review (opus, context-isolated) → Revise (opus,
conditional) → Artifacts.

Key architectural patterns:
- Separation of concerns: SKILL.md orchestrates, scripts handle
  deterministic work, agent prompts handle judgment
- Adversarial review: review agent is context-isolated from synthesis
  agent (doesn't see rationale, only diff + raw extractions)
- Stateless: no tracking of prior runs. Rejected proposals are handled
  by adding guidance to context files, not by building state
- Per-PR extraction: each PR gets its own agent context to avoid
  overflow, dispatched in parallel waves
