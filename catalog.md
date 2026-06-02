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

v1.0.0 | [opendatahub-io/assess-rfe](https://github.com/opendatahub-io/assess-rfe)

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

v1.0.0 | [opendatahub-io/odh-test-gen](https://github.com/opendatahub-io/odh-test-gen)

Tags: test-plan, test-cases, quality, strategy, review, scoring, automation, playwright, ui-testing

| Skill | Description |
|-------|-------------|
| `/test-plan-create` | Generate a test plan from a strategy |
| `/test-plan-create-cases` | Generate test case files from a test plan |
| `/test-plan-update` | Update test plan with new docs (ADR, API specs), re-analyze, bump version |
| `/test-plan-case-implement` | Generate executable test automation code from TC specifications with intelligent placement |
| `/test-plan-ui-verify` | Verify UI test cases from a PR against a live ODH/RHOAI cluster via Playwright; supports upgrade testing workflow |
| `/test-plan-publish` | Publish test plan artifacts to GitHub with PR creation |
| `/test-plan-resolve-feedback` | Assess and resolve PR review comments on test plans |
| `/test-plan-score` | Score test plan quality using rubric without auto-revision |

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
| `/historical-bug-coverage` | Analyzes historical blocking and critical bugs from Jira, determines what test coverage exists today with deep test inspection and confidence scoring, and generates standalone HTML reports |
| `/risk-assessment` | Analyze PR for risk, test coverage, architecture impact, and cross-repo intelligence |

```bash
/plugin install quality-tooling@opendatahub-skills
```

### agent-eval-harness

Generic agentic evaluation for skills and agents. Provides end-to-end skills to analyze, test, score, review, and iteratively improve agent skills with MLflow support for experiment tracking, tracing, and reporting. Schema-driven evaluation via eval.yaml with support for inline, LLM-based, and external judges.

v1.4.0 | Generic | [opendatahub-io/agent-eval-harness](https://github.com/opendatahub-io/agent-eval-harness)

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

## Code Quality

Code review, linting, and quality enforcement

### code-review-skills

AI-powered code review for GitLab merge requests. Reviews all commits since the base branch, produces structured JSON feedback with inline comments, and posts results to the GitLab MR (in CI) or displays them locally for preview. Supports chill mode filtering and comment deduplication.

v0.1.0 | Apache-2.0 | [opendatahub-io/code-review-skills](https://github.com/opendatahub-io/code-review-skills)

Tags: code-review, gitlab, ci, merge-request

| Skill | Description |
|-------|-------------|
| `/gitlab-code-review` | Perform AI code review on a GitLab merge request with structured JSON feedback and inline comments |

```bash
/plugin install code-review-skills@opendatahub-skills
```

## Documentation

Skills for generating and maintaining documentation

### knowledge-skills

Autonomous knowledge management skills for keeping AI context files (CLAUDE.md, AGENTS.md) up to date. Scans merged PRs, extracts relevant knowledge using parallel agents, and proposes updates as a git-apply-able patch for human review. Supports GitHub and GitLab.

v0.1.0 | Apache-2.0 | [opendatahub-io/knowledge-skills](https://github.com/opendatahub-io/knowledge-skills)

Tags: knowledge, context, claude-md, agents-md, pr-analysis, automation

| Skill | Description |
|-------|-------------|
| `/knowledge.repo` | Scan merged PRs and propose updates to AI context files (CLAUDE.md, AGENTS.md) as a git-apply-able patch |

```bash
/plugin install knowledge-skills@opendatahub-skills
```

## DevOps & CI/CD

Skills for deployment, CI/CD, and infrastructure

### disconnected-readiness-scorer

Score a repository's readiness for disconnected / air-gapped OpenShift deployments. Scans for image manifest completeness, digest enforcement, runtime egress, and Python dependency validation. Supports automatic detection of image management patterns (env var vs static CSV) and cross-references against the opendatahub-operator manifest.

v0.1.0 | Apache-2.0 | [opendatahub-io/disconnected-readiness-scorer](https://github.com/opendatahub-io/disconnected-readiness-scorer)

Tags: disconnected, air-gap, openshift, image-mirroring, readiness, scoring

| Skill | Description |
|-------|-------------|
| `/disconnected-score` | Score a repository's readiness for disconnected / air-gapped OpenShift deployments |

```bash
/plugin install disconnected-readiness-scorer@opendatahub-skills
```

### aiops-skills

DevOps and TestOps automation skills for ODH/RHOAI — component onboarding, Konflux CI/CD, release management, delivery pipelines, and operational tooling.

v0.1.0 | Apache-2.0 | [opendatahub-io/aiops-infra](https://github.com/opendatahub-io/aiops-infra)

Tags: devops, testops, odh, rhoai, konflux, onboarding, ci-cd, release, automation

| Skill | Description |
|-------|-------------|
| `/create-component-onboarding-jira` | Interactively collect component onboarding parameters and create/update a Jira ticket |
| `/validate-component-onboarding-jira` | Pre-flight validation for ODH component onboarding — fetches Jira, downloads YAML, validates against schema |

```bash
/plugin install aiops-skills@opendatahub-skills
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

v0.1.0 | Generic | Apache-2.0 | [opendatahub-io/ai-helpers](https://github.com/opendatahub-io/ai-helpers)

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

### autofix-skills

Claude Code plugin for the Jira autofix pipeline. Provides orchestrator skills, agent prompt files, and deterministic Python scripts for automated bug fixing, CVE remediation, and ticket triage. Designed to run inside a Claude Code container as part of a CI pipeline.

v0.1.0 | Apache-2.0 | [opendatahub-io/autofix-skills](https://github.com/opendatahub-io/autofix-skills)

Tags: autofix, jira, cve, bug-fixing, triage, pipeline, ci-cd

| Skill | Description |
|-------|-------------|
| `/autofix-resolve` | Orchestrate end-to-end bug fixing via implement and review agent loop (max 3 iterations) |
| `/autofix-cve-resolve` | CVE remediation across multiple repos with state-machine dispatch |
| `/autofix-triage` | Assess bug tickets for AI autofix readiness (ready/needs_info/not_fixable) |
| `/autofix-research` | Investigate spike tickets with no associated repository |

```bash
/plugin install autofix-skills@opendatahub-skills
```

## Product Planning

Skills for requirements, RFEs, and product strategy

### rfe-creator

Claude Code skills for creating, reviewing, and submitting RFEs to the RHAIRFE Jira project. Provides an automated pipeline from initial creation through review, splitting, and submission, plus strategy refinement skills.

**Requires:** `assess-rfe`

v0.1.0 | [opendatahub-io/rfe-creator](https://github.com/opendatahub-io/rfe-creator)

Tags: rfe, jira, review, strategy, pipeline

| Skill | Description |
|-------|-------------|
| `/rfe.create` | Generate new RFEs from problem statements |
| `/rfe.review` | Score and improve RFEs with auto-revision |
| `/rfe.split` | Decompose oversized RFEs into appropriately-scoped pieces |
| `/rfe.submit` | Push RFEs to Jira |
| `/rfe.speedrun` | Execute the full RFE pipeline end-to-end |
| `/rfe.auto-fix` | Batch review, revise, and split operations |
| `/rfe-creator.update-deps` | Update vendored dependencies |
| `/architecture-review` | Architecture review skill |
| `/feasibility-review` | Feasibility review skill |
| `/rfe-feasibility-review` | RFE feasibility review |
| `/scope-review` | Scope review skill |
| `/testability-review` | Testability review skill |

```bash
/plugin install rfe-creator@opendatahub-skills
```

### spike-executor

Execute RHOAI SPIKE investigations with human-in-the-loop approval gates. 9-step lifecycle: intake, plan, Jira sync, AI research enrichment with hallucination detection, pytest test suites on OpenShift, rubric-based scoring with security gates, and RFE input generation. Supports both runtime and protocol library assessment.

v0.2.0 | Apache-2.0 | [IKRedHat/SPIKE-executor](https://github.com/IKRedHat/SPIKE-executor)

Tags: spike, assessment, jira, research, scoring, rfe, openshift, rhoai, feasibility

| Skill | Description |
|-------|-------------|
| `/SPIKE-executor` | Execute RHOAI SPIKE investigations with human-in-the-loop approval gates |

```bash
/plugin install spike-executor@opendatahub-skills
```
