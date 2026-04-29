# Skills and plugins for AI-assisted software engineering workflows, developed by the opendatahub-io team.


Auto-generated from `registry.yaml`. Do not edit directly.

## Quick Start

```bash
# Add this marketplace to Claude Code
claude plugin marketplace add opendatahub-io/skills-registry

# Browse available plugins
/plugin
```

## Evaluation & Testing

Skills for evaluating and testing AI agent skills

### assess-rfe

Assess RFEs against quality criteria using a structured rubric.

v1.0.0 | [n1hility/assess-rfe](https://github.com/n1hility/assess-rfe)

Tags: rfe, rubric, quality, assessment

| Skill | Description |
|-------|-------------|
| `/assess-rfe` | Assess RFEs against quality criteria using a structured rubric |
| `/export-rubric` | Export the assessment rubric |

```bash
/plugin install assess-rfe@opendatahub-skills
```

### test-plan

End-to-end test planning workflow for RHOAI: generate test plans from strategies, create test cases, implement executable automation code, verify UI tests against live clusters via Playwright, publish to GitHub with PR creation, resolve review feedback, and score quality with automated rubrics using parallel sub-agent analysis.

v0.2.0 | [fege/test-plan](https://github.com/fege/test-plan)

Tags: test-plan, test-cases, quality, strategy, review, scoring, automation, playwright, ui-testing

| Skill | Description |
|-------|-------------|
| `/test-plan.create` | Generate a test plan from a strategy |
| `/test-plan.create-cases` | Generate test case files from a test plan |
| `/test-plan.update` | Update test plan with new docs (ADR, API specs), re-analyze, bump version |
| `/test-plan.case-implement` | Generate executable test automation code from TC specifications with intelligent placement |
| `/test-plan.ui-verify` | Verify UI test cases from a PR against a live ODH/RHOAI cluster via Playwright; supports upgrade testing workflow |
| `/test-plan.publish` | Publish test plan artifacts to GitHub with PR creation |
| `/test-plan.resolve-feedback` | Assess and resolve PR review comments on test plans |
| `/test-plan.score` | Score test plan quality using rubric without auto-revision |

```bash
/plugin install test-plan@opendatahub-skills
```

### quality-tooling

Quality tooling and automation for RHOAI component development. Includes automated repository analysis, build validation, and test pattern extraction.

v1.0.0 | [antowaddle/Red-Hat-Quality-Tiger-Team](https://github.com/antowaddle/Red-Hat-Quality-Tiger-Team)

Tags: quality, testing, ci-cd, build-validation, analysis

| Skill | Description |
|-------|-------------|
| `/quality-repo-analysis` | Automated analysis tool that evaluates CI/CD, testing, security, and best practices against gold standards |
| `/konflux-build-simulator` | Generate GitHub Actions workflows that simulate Konflux builds at PR time to catch failures before merge |
| `/test-rules-generator` | Extract test patterns from existing tests and generate .claude/rules/ documentation for consistency |

```bash
/plugin install quality-tooling@opendatahub-skills
```

### agent-eval-harness

Generic agentic evaluation for skills and agents. Provides end-to-end skills to analyze, test, score, review, and iteratively improve agent skills with MLflow support for experiment tracking, tracing, and reporting. Schema-driven evaluation via eval.yaml with support for inline, LLM-based, and external judges.

v0.1.0 | [opendatahub-io/agent-eval-harness](https://github.com/opendatahub-io/agent-eval-harness)

Tags: evaluation, testing, skills, agents, mlflow, optimization, scoring

| Skill | Description |
|-------|-------------|
| `/eval-setup` | One-time environment setup for evaluation (dependencies, MLflow, API keys) |
| `/eval-analyze` | Deep-read a target skill and generate eval.yaml configuration with dataset schemas and judges |
| `/eval-dataset` | Generate realistic test cases from eval.yaml schema (bootstrap, expand, from-traces) |
| `/eval-run` | Execute skill against test cases, collect artifacts, run judges, and detect regressions |
| `/eval-review` | Human-in-the-loop review of scores and outputs with qualitative feedback collection |
| `/eval-mlflow` | Bidirectional MLflow sync for results, datasets, and feedback |
| `/eval-optimize` | Automated improvement loop that identifies failures, edits SKILL.md, and re-runs with regression checks |

```bash
/plugin install agent-eval-harness@opendatahub-skills
```

## Security Review

Security analysis, threat modeling, and compliance review

### rhoai-security-reviewer

Consensus-based security review for RHOAI strategy documents (STRATs). An orchestrator spawns three independent reviewers to identify security risks, then synthesizes findings with confidence tagging based on cross-reviewer agreement. Covers 39 catalog patterns across auth, data protection, cryptographic compliance, network security, supply chain, and infrastructure.

v0.1.0 | [jctanner/ai-first-pipeline](https://github.com/jctanner/ai-first-pipeline)

Tags: security, review, strat, threat-modeling, fips, compliance, consensus

| Skill | Description |
|-------|-------------|
| `/strat-security-review` | Multi-reviewer consensus orchestrator for security review of STRAT documents. Extracts threat surfaces, spawns three independent security-reviewer instances, synthesizes findings with confidence levels, and produces a final verdict (PASS/CONCERNS/FAIL).
 |
| `/security-reviewer` | Individual security reviewer that assesses RHOAI strategy documents against 39 catalog patterns covering authentication, data protection, cryptographic compliance, network security, supply chain, and infrastructure. Uses a two-phase discovery-then-filter approach with severity classification.
 |

```bash
/plugin install rhoai-security-reviewer@opendatahub-skills
```

## Development Tools

Developer productivity tools for packaging, CI/CD debugging, and workflow automation

### odh-ai-helpers

Developer productivity tools for Python packaging, CI/CD debugging, and workflow automation. Includes skills for analyzing package build complexity, resolving dependencies, finding licenses, debugging GitLab pipelines, reviewing ADRs, and more.

v0.1.0 | Apache-2.0 | [opendatahub-io/ai-helpers](https://github.com/opendatahub-io/ai-helpers)

Tags: python-packaging, licensing, dependencies, gitlab, jira, adr, git, automation

| Skill | Description |
|-------|-------------|
| `/adr-review` | Review an Architectural Decision Record (ADR) using a team of specialist reviewer subagents and produce a consolidated report |
| `/gitlab-pipeline-debugger` | Debug and monitor GitLab CI/CD pipelines for merge requests, check pipeline status, view job logs, and troubleshoot CI failures |
| `/git-shallow-clone` | Perform a shallow clone of a Git repository to a temporary location |
| `/jira-upload-chat-log` | Export and upload the current chat conversation as a markdown file attachment to a Jira ticket |
| `/python-full-deps` | Resolve the full install-time dependency tree for a Python package with environment markers |
| `/python-packaging-bug-finder` | Find known packaging bugs, fixes, and workarounds for Python projects by searching GitHub issues |
| `/python-packaging-complexity` | Analyze Python package build complexity by inspecting PyPI metadata, compilation requirements, and distribution types |
| `/python-packaging-env-finder` | Investigate environment variables that can be set when building Python wheels for a given project |
| `/python-packaging-license-checker` | Check whether a Python package license is compatible with redistribution in Red Hat products |
| `/python-packaging-license-finder` | Deterministically find license information for Python packages by checking PyPI metadata and Git repository LICENSE files |
| `/python-packaging-source-finder` | Locate source code repositories for Python packages by analyzing PyPI metadata and project URLs |
| `/vllm-backport-fetch-prs` | Fetch merged bugfix PRs from upstream vLLM within a configurable date window using GitHub CLI |
| `/vllm-backport-classify` | Classify PRs by backport relevance using labels, title patterns, and file-existence heuristics |
| `/vllm-backport-check-backported` | Check if PRs are already cherry-picked in a downstream release branch via SHA and title matching |
| `/vllm-backport-score-rank` | Score and rank backport candidates by severity, scope, and risk using a deterministic composite score |
| `/vllm-backport-push-report` | Push triage report to a GitHub repository with timestamped directory structure |
| `/vllm-backport-cherry-pick` | Attempt automatic cherry-pick of clean backport candidates to a downstream release branch |
| `/vllm-compare-reqs` | Compare Python requirements between upstream vLLM and a downstream fork to identify version mismatches and missing packages |
| `/vllm-slack-summary` | Generate a concise Slack-formatted summary of vLLM backport triage results |

| Agent | Description |
|-------|-------------|
| python-packaging-investigator | Investigates Python package repositories to analyze build systems, dependencies, and packaging complexity |

```bash
/plugin install odh-ai-helpers@opendatahub-skills
```

## Product Planning

Skills for requirements, RFEs, and product strategy

### rfe-creator

Claude Code skills for creating, reviewing, and submitting RFEs to the RHAIRFE Jira project. Provides an automated pipeline from initial creation through review, splitting, and submission, plus strategy refinement skills.

**Requires:** `assess-rfe`

v0.1.0 | [jwforres/rfe-creator](https://github.com/jwforres/rfe-creator)

Tags: rfe, jira, review, strategy, pipeline

| Skill | Description |
|-------|-------------|
| `/rfe.create` | Generate new RFEs from problem statements |
| `/rfe.review` | Score and improve RFEs with auto-revision |
| `/rfe.split` | Decompose oversized RFEs into appropriately-scoped pieces |
| `/rfe.submit` | Push RFEs to Jira |
| `/rfe.speedrun` | Execute the full RFE pipeline end-to-end |
| `/rfe.auto-fix` | Batch review, revise, and split operations |
| `/strat.create` | Create strategy documents |
| `/strat.refine` | Refine strategy documents |
| `/strat.review` | Review strategy documents |
| `/strat.prioritize` | Prioritize strategy items |
| `/rfe-creator.update-deps` | Update vendored dependencies |
| `/architecture-review` | Architecture review skill |
| `/feasibility-review` | Feasibility review skill |
| `/rfe-feasibility-review` | RFE feasibility review |
| `/scope-review` | Scope review skill |
| `/testability-review` | Testability review skill |

```bash
/plugin install rfe-creator@opendatahub-skills
```

### meeting-quality-skills

Pre-meeting skills for improving meeting quality by checking shared update docs, identifying missing async updates, and helping organizers focus meetings on items that actually need discussion.

v0.1.0 | Apache-2.0 | [ahinek/meeting-quality-skills](https://github.com/ahinek/meeting-quality-skills)

Tags: meeting, google-workspace, agenda, async-updates, productivity

| Skill | Description |
|-------|-------------|
| `/meeting-async-update-check` | Check a shared update doc and identify attendees missing async updates before a status meeting |
| `/meeting-risk-agenda` | Analyze pre-meeting updates and generate a risk-focused agenda by identifying blocked and at-risk items |

```bash
/plugin install meeting-quality-skills@opendatahub-skills
```
