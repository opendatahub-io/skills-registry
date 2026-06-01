---
title: spike-executor
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# spike-executor

Execute RHOAI SPIKE investigations with human-in-the-loop approval gates on
OpenShift. Provides a 9-step lifecycle covering intake, plan generation, Jira
ticket creation and sync, AI-powered research enrichment with hallucination
detection, pytest test suite generation and execution on OpenShift clusters,
rubric-based feasibility scoring with a security gate, and RFE document
generation.

The skill orchestrates via a CLI (spike-executor) that handles each step as a
separate command, writing artifacts to an artifacts/ directory with a consistent
<Type>-<project> naming pattern. Workflow state is persisted in
.spike-state-<project>.json for resume support. Supports both runtime evaluations
(e.g., AutoGluon) and protocol library evaluations (e.g., gRPC). Integrates with
Jira for ticket management (create, update, transition) and optionally requires
OpenShift access for cluster test execution.


!!! info "Plugin Details"

    - **Version**: 0.2.0
    - **Author**: IKRedHat
    - **License**: Apache-2.0
    - **Category**: [Product Planning](../../categories/planning.md)
    - **Repository**: [IKRedHat/SPIKE-executor](https://github.com/IKRedHat/SPIKE-executor)
    - **Tags**: <span class="tag-pill">spike</span> <span class="tag-pill">assessment</span> <span class="tag-pill">jira</span> <span class="tag-pill">research</span> <span class="tag-pill">scoring</span> <span class="tag-pill">rfe</span> <span class="tag-pill">openshift</span> <span class="tag-pill">rhoai</span> <span class="tag-pill">feasibility</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/SPIKE-executor`](SPIKE-executor.md) | Execute RHOAI SPIKE investigations with human-in-the-loop approval gates | :material-check: |

## Installation

```bash
/plugin install spike-executor@opendatahub-skills
```

## Architecture

Single-skill plugin with a 9-step CLI-driven workflow. Each step maps to a
spike-executor subcommand that reads/writes from the artifacts/ directory.
Breakpoints after each step pause for human review and approval before
proceeding.

Key modules: plan_generator.py (Jinja2 template rendering), jira_sync.py
(Jira REST API with retry, labels, comments), test_generator.py (Phase 2
plan parser + pytest suite generation), test_executor.py (pytest runner +
JUnit XML parsing), scorer.py (rubric-based 0-3 scoring with domain weights
and security gate), state.py (workflow persistence), cli.py (Typer CLI).

Step 5 (AI Research) is the most complex: generates a research scaffold via
templates, then the LLM performs a comprehensive web research deep dive
covering community health, license, architecture, performance, UBI
feasibility, operator integration, security (CVE, FIPS, rootless, air-gap,
supply chain), and hardware/MLOps. A validation step (validate-research)
checks for hallucination via URL reachability, evidence-backed claims, TBD
audit, and GitHub metrics cross-referencing.

Scoring uses a 4-domain rubric (UBI 25%, Operator 20%, Security 30%,
Hardware 25%) with 14 checks, each scored 0-3. Decision bands: GO >= 80,
PIVOT 55-79, NO-GO < 55. A security critical failure gate blocks GO if
any security check scores 0.

Three hooks handle artifact safety: backup-artifact.sh (PreToolUse on
Write), validate-artifact.sh and auto-validate-research.sh (PostToolUse
on Write).
