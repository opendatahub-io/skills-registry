---
title: docs-skills
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# docs-skills

A comprehensive toolkit for technical documentation work on AsciiDoc and
Markdown content, built around Red Hat and IBM style conventions. It combines
an orchestrated, multi-stage documentation pipeline with a large library of
standalone review, authoring, and integration skills — everything from turning
a JIRA ticket into a reviewed, merge-ready documentation PR to auditing a single
file for style guide compliance, PII, or technical accuracy.

The centerpiece is the `docs-orchestrator`, a pipeline that runs a JIRA ticket
through requirements analysis, source-code learning, evidence-based scope
auditing, optional PR analysis, planning, writing, and a battery of reviews
(technical, style, security, and an LLM quality gate) before committing and
opening a merge request. Each stage is its own `docs-workflow-*` step skill that
reads inputs from the previous stage's output folder and writes a lightweight
`step-result.json` sidecar, so the orchestrator can manage progress, resume,
and iterate without holding heavy content in context. Specialized subagents
(planner, writer, reviewers, analysts, classifiers) do the heavy lifting in
isolated context windows.

Around the pipeline sits a set of reusable building blocks. Codebase
understanding is provided by `learn-code` (parallel module analysis producing an
ONBOARDING.md), `query-code`, and `understand-pull-request`. Platform
integration comes from `git-pr-reader` (a unified GitHub/GitLab interface),
`jira-reader`/`jira-writer`, and web/content tools (`article-extractor`,
`redhat-docs-toc`, `docs-convert-gdoc-md`). Content ingestion, linting
(`lint-with-vale`), and release-notes auditing (`rn-known-issues`) round out the
authoring surface.

Style and quality enforcement is factored into a granular catalog of review
skills: eight IBM Style Guide checkers (`ibm-sg-*`), eight Red Hat Supplementary
Style Guide checkers (`rh-ssg-*`), plus modular-docs, content-quality, and
security/PII reviews. These are composed by the higher-level `docs-review-style`
and `docs-review-technical` skills (multi-agent, confidence-scored, with
optional inline PR/MR comment posting) and by `action-comments`, which fetches
and actions reviewer comments on a PR/MR.


!!! info "Plugin Details"

    - **Version**: 0.3.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [Documentation](../../categories/documentation.md)
    - **Repository**: [opendatahub-io/docs-skills](https://github.com/opendatahub-io/docs-skills)
    - **Tags**: <span class="tag-pill">documentation</span> <span class="tag-pill">asciidoc</span> <span class="tag-pill">mkdocs</span> <span class="tag-pill">workflow</span> <span class="tag-pill">review</span> <span class="tag-pill">style-guide</span> <span class="tag-pill">jira</span> <span class="tag-pill">onboarding</span> <span class="tag-pill">code-analysis</span>

## Pipeline

<div class="diagram-container" markdown>
![docs-skills pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/docs-orchestrator`](docs-orchestrator.md) | Documentation workflow orchestrator. Reads the step list from .agent_workspace/docs-workflow.yaml (or the plugin default). Runs steps sequentially, manages progress state, handles iteration and confirmation gates. Claude is the orchestrator — the YAML is a step list, not a workflow engine. | :material-check: |

## Installation

```bash
/plugin install docs-skills@opendatahub-skills
```

## Architecture

The plugin has three layers: the orchestrator, the workflow step skills, and a
library of reusable tool/review skills — with a pool of subagents underneath.

**Orchestrator layer.** `docs-orchestrator` is the brain. It reads an ordered
step list from `.agent_workspace/docs-workflow.yaml` (or a plugin default),
resolves the source repository via `resolve_source.py`, then runs each step
sequentially. It owns all iteration and gating logic: a technical-review loop
(up to 3 passes to reach acceptable confidence), a quality-gate loop (up to 2
passes to reach intent alignment), `when` conditions (`has_source_repo`,
`has_pr`, `has_many_requirements`, `create_merge_request`), and a commit
confirmation gate. State lives in a progress JSON that is re-read from disk after
every step so the workflow survives context compaction and can resume.
`docs-workflow-start` is the interactive front door (AskUserQuestion-driven
setup that builds CLI flags and hands off to the orchestrator);
`docs-workflow-jira-ready` is the automation front door (a check-and-return gate
for cron/CI that lists tickets ready for processing).

**Workflow step layer.** Each `docs-workflow-*` step follows the same contract —
parse args, do work (often by dispatching a subagent or wrapping a tool skill),
and write a `step-result.json` sidecar. Steps communicate only through files in
`.agent_workspace/<ticket>/<step>/`, never by returning large payloads to the
orchestrator. Several steps use a fan-out pattern for context isolation:
`requirements` runs a two-pass discovery-then-per-requirement fanout;
`scope-req-audit` dispatches one classifier per requirement; `quality-gate`
runs per-AC coverage agents plus two parallel Opus judges; `tech-review`
validates documentation claims via batched `code-questioner` agents. Wrapper
steps (`code-analysis`, `pr-analysis`) run heavy skills (`learn-code`,
`understand-pull-request`) inside a subagent to keep the orchestrator context
lean, and merge agents assemble large markdown outputs off the main thread.

**Tool and review layer.** `learn-code` is a standalone five-stage pipeline
(detect → registry → parallel module analysis → relationships → synthesis) that
fans out `module-analyzer` and `relationship-analyzer` agents in batches of 10.
`git-pr-reader` is the shared platform abstraction (GitHub/GitLab auto-detect)
used by nearly every PR/MR-touching skill for reading, extracting line numbers,
posting, and replying. `jira-reader`/`jira-writer` wrap the Atlassian REST API.
The style-guide review skills (`ibm-sg-*`, `rh-ssg-*`, `docs-review-*`) are
atomic, checklist-driven reviewers with no CLI surface of their own — they are
composed by `docs-review-style`/`docs-review-technical` (multi-agent, extract
changed line ranges, review in parallel, validate, filter by confidence
threshold, optionally post inline comments) and by the `docs-writer`/
`docs-reviewer` subagents inside the pipeline. Scripts are invoked with
`${CLAUDE_SKILL_DIR}` / `${CLAUDE_PLUGIN_ROOT}` substitution and PEP 723
(`uv run --script`) for scripts with external dependencies.
