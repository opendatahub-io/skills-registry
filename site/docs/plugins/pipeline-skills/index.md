---
title: pipeline-skills
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# pipeline-skills

Pipeline failure analysis skills for AIPCC (AI Platform Compute Cluster)
CI/CD pipelines. This plugin is the **inner layer** of a larger failure
analysis system — the two skills that run inside a Claude Code container
and do the actual reasoning. The **outer layer** (Python orchestration,
GitLab CI wiring, per-group report assembly, and Jira/Slack notification)
lives in [pipeline-failure-analyzer](https://github.com/opendatahub-io/pipeline-failure-analyzer)
and the generic [agentic-ci](https://github.com/opendatahub-io/agentic-ci)
framework.

Analysis runs in two stages. First, **pipeline-grouping** reads the
preprocessed error output of every failed job and clusters jobs by shared
root cause — merging jobs with the same underlying error even when they
span different collections or pipeline actions, and deduplicating against
open Jira tickets to avoid filing repeats. Then, for each resulting group,
**pipeline-rca** investigates trace logs, source code, and build artifacts
to diagnose *why* the failure happened, emitting structured narrative
sections and a machine-readable finding with a confidence-rated diagnosis.

Both skills are **orchestrator-invoked** (`user-invocable: false`): they
take no command-line arguments. Instead they operate against a workspace
contract at `/workspace/` that the orchestrator populates with context
JSON, job trace logs, preprocessed error files, and shallow repository
clones. Every input is treated strictly as evidence-to-analyze, never as
instructions — a deliberate prompt-injection boundary given that the skills
process untrusted CI log content. Outputs are deterministic, schema-validated
files (`grouping.json`, `finding.json`, section markdown) that the outer
orchestrator assembles and routes downstream.


!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Category**: [DevOps & CI/CD](../../categories/devops.md)
    - **Repository**: [opendatahub-io/pipeline-skills](https://github.com/opendatahub-io/pipeline-skills)
    - **Tags**: <span class="tag-pill">pipeline</span> <span class="tag-pill">ci-cd</span> <span class="tag-pill">failure-analysis</span> <span class="tag-pill">grouping</span> <span class="tag-pill">root-cause</span> <span class="tag-pill">gitlab</span>

## Pipeline

<div class="diagram-container" markdown>
![pipeline-skills pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/pipeline-grouping`](pipeline-grouping.md) | Group failed CI/CD pipeline jobs by error similarity using log analysis and Jira ticket deduplication | :material-close: internal |
| [`/pipeline-rca`](pipeline-rca.md) | Root cause analysis for a pipeline failure error group with structured findings and section files | :material-close: internal |

## Installation

```bash
/plugin install pipeline-skills@opendatahub-skills
```

## Architecture

The two skills form a fan-out pipeline: one grouping pass produces N error
groups, and one root-cause-analysis task runs per group. Each skill is
self-contained — its prompt, scripts, and reference templates live together
under `skills/<name>/` and reference themselves via `${CLAUDE_SKILL_DIR}`.

**pipeline-grouping** builds `grouping.json` incrementally through a CLI
tool (`scripts/grouper.py`) rather than emitting JSON directly. The skill
reads `/workspace/_context/grouping-context.json` (job manifest, expected
job IDs, Jira URL) plus every `jobs/<id>-<name>/errors.txt`, then drives the
grouper via four subcommands operating on a `grouping.work.json` work file:
`add-group` (one call per root cause, with jobs and unique error messages),
`add-job` (straggler corrections), `status` (inspect groups and unassigned
jobs), and `finalize` (validate completeness against the expected job set,
then write `grouping.json` with sequential slug IDs). The grouper enforces
invariants deterministically — no duplicate job across groups, no unknown
IDs, no empty summaries, and every expected job assigned exactly once — so
the agent must fix and retry on non-zero exit. After grouping, it optionally
reads `recent-tickets.json` and writes `dedup-results.json` marking groups
that match an existing Jira ticket (high/medium confidence) to suppress
duplicate filings.

**pipeline-rca** runs once per error group. It reads
`/workspace/_context/rca-context.json` (group metadata, pipeline SHA/ref,
affected-jobs and file-paths tables, dependency versions, repo clone path)
and investigates using local git first (`git show <sha>:<path>` against the
shallow clone) with a GitLab API fallback via `glab` for history beyond the
clone depth. It cleans oversized trace logs through the shared
`log_cleaner.py` with AIPCC error patterns, verifies its diagnosis against a
cheap distinguishing check before committing, and writes content-fragment
section files — `error-overview.md` (the symptom, with quoted errors),
`root-cause.md` (the diagnosis and failure chain), and optionally
`resolution.md` and `feedback.md`. It finishes with `finding.json`, validated
against `references/finding.schema.json`, carrying classification metadata
(collections, actions, cascade flag, group consistency), a confidence level
under a high/medium/low rubric, the target repository for the fix, and the
full list of files consulted. Credentials in quoted log lines are redacted.
