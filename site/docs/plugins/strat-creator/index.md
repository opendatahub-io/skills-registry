---
title: strat-creator
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strat-creator

**strat-creator** turns approved RFEs into reviewed, feature-ready **strategies** in
the RHAISTRAT Jira project. Where an RFE captures the *what* and *why*, a strategy adds
the *how* — technical approach, affected components, impacted teams, dependencies, and
non-functional requirements — grounded in the platform's actual architecture.

The plugin implements a two-loop pipeline. The **CI loop** runs unattended: it clones
approved RFEs into RHAISTRAT (`strategy-create`), refines each into a full strategy
(`strategy-refine`), and subjects it to an adversarial quality gate that combines
deterministic rubric scoring with four independent forked reviewers (`strategy-review`).
The gate labels each strategy `strat-creator-rubric-pass` or `strat-creator-needs-attention`.
The **human loop** then lets a staff engineer pull a post-CI strategy into a local
workspace (`strategy-pull`), iterate on it with the same refine/review skills in local
mode, and either push it back for re-evaluation (`strategy-push`) or sign it off as
feature-ready (`strategy-signoff`).

Every skill is designed to be safe and idempotent: a shared set of pipeline label gates
prevents reprocessing already-handled strategies, a `--dry-run` mode skips all external
Jira writes, and strict section ownership guarantees the RFE business need is copied
verbatim and human-authored input is never overwritten. Jira access works through the
Atlassian MCP server when available, falling back to a REST API script driven by
`JIRA_SERVER`/`JIRA_USER`/`JIRA_TOKEN` environment variables.


!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: Eder Ignatowicz
    - **Category**: [Product Planning](../../categories/planning.md)
    - **Repository**: [opendatahub-io/strat-creator](https://github.com/opendatahub-io/strat-creator)
    - **Tags**: <span class="tag-pill">strategy</span> <span class="tag-pill">strat</span> <span class="tag-pill">jira</span> <span class="tag-pill">review</span> <span class="tag-pill">pipeline</span>

## Pipeline

<div class="diagram-container" markdown>
![strat-creator pipeline](pipeline.svg)
</div>

## Dependencies

- [`assess-strat`](../assess-strat/index.md)

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/strategy-create`](strategy-create.md) | Create strategies from approved RFEs by cloning them to RHAISTRAT in Jira | :material-check: |
| [`/strategy-refine`](strategy-refine.md) | Refine a strategy with technical HOW, dependencies, and NFRs | :material-check: |
| [`/strategy-review`](strategy-review.md) | Adversarial review with rubric scoring and independent forked reviewers | :material-check: |
| [`/strategy-pull`](strategy-pull.md) | Pull a post-CI strategy from Jira into local workspace for human review | :material-check: |
| [`/strategy-push`](strategy-push.md) | Push a locally-refined strategy back to Jira and resubmit to CI | :material-check: |
| [`/strategy-signoff`](strategy-signoff.md) | Sign off on a CI-approved strategy with human sign-off label | :material-check: |
| [`/export-rubric`](export-rubric.md) | Export the scoring rubric to artifacts/strat-rubric.md | :material-check: |
| [`/strategy-feasibility-review`](strategy-feasibility-review.md) | Reviews strategy for technical feasibility and effort estimate credibility | :material-close: internal |
| [`/strategy-testability-review`](strategy-testability-review.md) | Reviews strategy for testability and measurable acceptance criteria | :material-close: internal |
| [`/strategy-scope-review`](strategy-scope-review.md) | Reviews strategy for right-sizing and bounded scope | :material-close: internal |
| [`/strategy-architecture-review`](strategy-architecture-review.md) | Reviews strategy for architectural correctness and integration patterns | :material-close: internal |

## Installation

```bash
/plugin install strat-creator@opendatahub-skills
```

## Architecture

**Artifact conventions.** All CI-mode skills read and write under `artifacts/`:
`strat-tasks/` (strategy files with YAML frontmatter), `strat-reviews/` (per-strategy
review files), `strat-originals/` (frozen RFE/STRAT snapshots), and `strat-skipped.md`
(audit trail of gated-out RFEs). The human loop mirrors this structure under `local/`
with `workflow: local` frontmatter. Skills auto-detect local mode by checking for
`local/strat-tasks/` and prefer it when both exist.

**Structured frontmatter.** Task and review files carry validated YAML frontmatter
(strat_id, title, source_rfe, jira_key, priority, status, reviewers.*, recommendation).
Skills never hand-write YAML — they go through `scripts/frontmatter.py` (schema/read/set).
Long-running skills persist progress via `scripts/state.py` so they survive context
compression.

**Section ownership.** Each strategy file has three top-level sections with strict rules:
`## Business Need (from RFE)` is copied character-for-character and never modified;
`## Strategy (AI Generated by Agentic SDLC Pipeline)` is the only section the pipeline
writes and is fully regenerated each run; `## Staff Engineer / SME Input` is human-owned
and read-only for the agent, taking highest priority among refinement inputs.

**Pipeline label gates.** Gate logic (status checks, required-label checks, already-processed
skips) is duplicated across `strategy-create`, `strategy-refine`, and `strategy-review`
so each is independently safe to run. Strategies already carrying `strat-creator-rubric-pass`
or `strat-creator-needs-attention` are skipped by the CI-mode gate; local mode bypasses
the gate because the human is deliberately iterating.

**Review orchestration.** `strategy-review` is the most complex skill: it bootstraps the
`assess-strat` plugin, spawns a background scorer agent against the rubric, runs
deterministic scripts (`parse_results.py`, `apply_scores.py`, `summarize_run.py`) to
compute the verdict with no LLM judgment, then invokes the four reviewer skills
(`strategy-feasibility-review`, `strategy-testability-review`, `strategy-scope-review`,
`strategy-architecture-review`) in parallel via the Skill tool. Each reviewer runs in an
isolated `context: fork` so no reviewer sees another's output, preserving independent
adversarial judgment. Prose reviewer verdicts are informational only — the gate decision
comes solely from the numeric rubric scores.

**Architecture grounding.** Refinement and review fetch opendatahub-io/architecture-context
into `.context/architecture-context/` (via `fetch-architecture-context.sh`). Component
docs, `PLATFORM.md`, and human-authored `overlays/` (recent corrections that supersede
the generated docs) ground technical claims and let reviewers flag outdated assumptions.
