---
title: rfe-creator
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe-creator

A comprehensive Claude Code skill suite for the full lifecycle of Requests for
Enhancement (RFEs) in the RHAIRFE Jira project. Covers creation from problem
statements, multi-phase rubric-based review with technical feasibility checks
and auto-revision, intelligent splitting of oversized RFEs, batch auto-fix at
scale, and deterministic submission to Jira. A speedrun skill chains the whole
pipeline end-to-end (create → auto-fix → submit) for a single idea, a set of
existing Jira keys, or a YAML batch of ideas.

The plugin uses a shared artifact convention -- all skills read from and write
to an `artifacts/` directory, with YAML frontmatter (managed exclusively via
`scripts/frontmatter.py`) carrying structured metadata on every task and review
file. Jira write operations go through deterministic Python scripts (REST API +
Basic Auth) rather than LLM tool-calling, so the exact sequence of API calls is
reproducible; read operations prefer the Atlassian MCP server and fall back to
the REST API. Long-running orchestrators persist state to `tmp/` via
`scripts/state.py` so they survive context-compression boundaries. A dependency
on the `assess-rfe` plugin provides the scoring rubric, bootstrapped
automatically on first use.


!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: jwforres
    - **Category**: [Product Planning](../../categories/planning.md)
    - **Repository**: [opendatahub-io/rfe-creator](https://github.com/opendatahub-io/rfe-creator)
    - **Tags**: <span class="tag-pill">rfe</span> <span class="tag-pill">initiative</span> <span class="tag-pill">jira</span> <span class="tag-pill">review</span> <span class="tag-pill">pipeline</span>

## Pipeline

<div class="diagram-container" markdown>
![rfe-creator pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/rfe-create`](rfe-create.md) | Write a new work item of any registered type — an RFE from a problem statement, idea, or need (business needs, WHAT/WHY), or an Initiative from an objective or strategic goal (/rfe-create --type initiative ...). Asks clarifying questions, then produces well-formed items. Use when starting from scratch. | :material-check: |
| [`/rfe-review`](rfe-review.md) | Review and improve work items of any registered type — RFEs (RHAIRFE) and Initiatives (RHOAIENG, /rfe-review --type initiative). Accepts one or more Jira keys to fetch and review existing items, or reviews local artifacts from /rfe-create. Runs rubric scoring and the type's review dimensions (technical feasibility, strategic alignment), then auto- revises the issues it finds. | :material-check: |
| [`/rfe-split`](rfe-split.md) | Split oversized work items of any registered type — RFEs and Initiatives — into smaller, right-sized ones. Accepts one or more IDs (e.g., /rfe-split RHAIRFE-1234 RHAIRFE-5678, /rfe-split --type initiative INIT-001). Runs non-interactively — decomposes, generates new items, reviews them, self-corrects, and checks coverage. | :material-check: |
| [`/rfe-submit`](rfe-submit.md) | Submit or update work items of any registered type in Jira — new RHAIRFE tickets for new RFEs, RHOAIENG Initiative tickets for Initiatives (/rfe-submit --type initiative), or updates to existing tickets fetched from Jira. Use after /rfe-review. | :material-check: |
| [`/rfe-speedrun`](rfe-speedrun.md) | End-to-end pipeline for work items of any registered type — RFEs by default, Initiatives with --type initiative. Accepts a single idea, Jira key(s), or a YAML batch file. Creates, reviews, auto-fixes (with splits), and submits. Supports --headless, --announce-complete, and --dry-run for CI. | :material-check: |
| [`/rfe-auto-fix`](rfe-auto-fix.md) | Review and fix batches of work items automatically — RFEs by default, any registered type with --type (e.g. --type initiative). Accepts explicit IDs or a JQL query. Reviews, auto- revises, and splits oversized items. Non-interactive. | :material-check: |
| [`/rfe.create`](rfe.create.md) | Compatibility alias for /rfe-create, kept so existing /rfe.create invocations keep working. Write a new RFE: prefer /rfe-create (Initiatives: /rfe-create --type initiative). | :material-check: |
| [`/rfe.review`](rfe.review.md) | Compatibility alias for /rfe-review, kept so existing /rfe.review invocations keep working. Review, improve and auto-revise RFEs: prefer /rfe-review (Initiatives: /rfe- review --type initiative). | :material-check: |
| [`/rfe.split`](rfe.split.md) | Compatibility alias for /rfe-split, kept so existing /rfe.split invocations keep working. Split oversized RFEs: prefer /rfe-split (Initiatives: /rfe-split --type initiative). | :material-check: |
| [`/rfe.submit`](rfe.submit.md) | Compatibility alias for /rfe-submit, kept so existing /rfe.submit invocations keep working. Submit or update RFEs in Jira: prefer /rfe-submit (Initiatives: /rfe-submit --type initiative). | :material-check: |
| [`/rfe.speedrun`](rfe.speedrun.md) | Compatibility alias for /rfe-speedrun, kept so existing /rfe.speedrun invocations keep working. End-to-end RFE pipeline: prefer /rfe-speedrun (Initiatives: /rfe-speedrun --type initiative). | :material-check: |
| [`/rfe.auto-fix`](rfe.auto-fix.md) | Compatibility alias for /rfe-auto-fix, kept so existing /rfe.auto-fix invocations keep working. Batch review, revision and split of RFEs: prefer /rfe-auto-fix (Initiatives: /rfe-auto-fix --type initiative). | :material-check: |
| [`/rfe-creator.update-deps`](rfe-creator.update-deps.md) | Update vendored dependencies | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install rfe-creator@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `rfe-creator` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```

## Architecture

The RFE skills (rfe.*) form the requirements pipeline. `rfe.speedrun` is the
top-level orchestrator: it invokes `rfe.create`, `rfe.auto-fix`, and
`rfe.submit` as sub-skills and never duplicates their work, persisting the ID
list and flags between phases so the run is resumable.

`rfe.review` is the central review orchestrator and is deliberately
content-blind -- it never reads RFE bodies into its own context. Instead it
launches parallel waves of sub-agents (fetch, assess, feasibility, review,
revise), reads only YAML frontmatter via `scripts/frontmatter.py`, checks file
existence via Glob, and polls for wave completion with
`scripts/check_review_progress.py` (sleeping for the reported `NEXT_POLL`
interval). Rubric assessment is delegated to the `assess-rfe` plugin (a
dedicated `rfe-scorer` subagent), and per-RFE technical feasibility is delegated
to the `rfe-feasibility-review` sub-agent. Failing RFEs are auto-revised and
re-assessed for up to two cycles.

`rfe.auto-fix` wraps the same building blocks into a non-interactive pipeline
state machine (`scripts/pipeline_state.py`) with phased dispatch (fetch →
bootstrap → assess → feasibility → review → revise → re-assess → split). It
drives a strict `next-action` / `launch_wave` / `wait-for-wave` loop, processes
IDs in configurable batches, and supports snapshot-based incremental fetch
(`scripts/snapshot_fetch.py`) for resume and reprocessing. `rfe.split`
decomposes oversized RFEs via parallel split agents, re-reviews the children
through `rfe.review`, and runs a one-cycle right-sizing self-correction loop.

Review artifacts follow a fixed layout under `artifacts/` (`rfe-tasks/`,
`rfe-originals/`, `rfe-reviews/`), and `scripts/frontmatter.py rebuild-index`
regenerates `rfes.md`. Architecture context is fetched from
opendatahub-io/architecture-context into `.context/architecture-context/` and
used by the feasibility fork to ground assessments in real platform components
and APIs; human-authored overlays under `overlays/` take precedence over the
generated docs. Note that `architecture-review`, `feasibility-review`,
`scope-review`, and `testability-review` are forked strategy reviewers (they
read `artifacts/strat-tasks/` and assess refined strategy features) shared with
the strategy workflow; `rfe-feasibility-review` is the RFE-specific reviewer
wired into `rfe.review`.
