# Skills and plugins for AI-assisted software engineering workflows, developed by the opendatahub-io team.


Auto-generated from `registry.yaml`. Do not edit directly.

## Quick Start

Add this marketplace to your agent harness, then browse the plugins.

**Claude Code**

```bash
claude plugin marketplace add opendatahub-io/skills-registry
/plugin
```

**OpenAI Codex**

```bash
codex plugin marketplace add opendatahub-io/skills-registry
/plugins
```

## Canonical Contract System

Contracts are contributor-facing optimization specs: functions describe the published job-to-be-done, metrics describe what should improve, and measures state how each metric is scored today.

### Functions

| Function | Meaning |
|----------|---------|
| `plan` | Choose an approach, sequence, or strategy before execution. |
| `retrieve` | Locate and return source material, facts, or artifacts needed for later work. |
| `analyze` | Interpret inputs to extract structure, meaning, or implications. |
| `review` | Assess an artifact against expectations and identify issues, risks, or fit. |
| `generate` | Produce a new artifact for the user or another tool to consume. |
| `transform` | Rewrite or convert existing input into a different form while preserving intent. |
| `verify` | Check whether a claim, artifact, or result satisfies explicit criteria. |
| `execute` | Carry out a bounded operational task in tools, CLIs, or external systems. |
| `orchestrate` | Coordinate multiple steps, tools, or subagents into a larger workflow. |

### Metrics

| Metric | What It Optimizes | Measurement Guidance |
|--------|-------------------|----------------------|
| `task_success` | Whether the skill completes the intended job correctly for the task. | Prefer deterministic or verifier-backed checks; use judge only as a fallback. |
| `tool_correctness` | Whether chosen tools and tool calls are valid and appropriate. | Usually deterministic or verifier-backed from tool traces and outcomes. |
| `argument_correctness` | Whether tool inputs, flags, and parameters are correct. | Usually deterministic or verifier-backed from arguments and downstream results. |
| `evidence_completeness` | Whether claims and verdicts are backed by enough concrete evidence. | Use verifier-backed checks when evidence can be counted; otherwise use a rubric-backed judge. |
| `step_efficiency` | Whether the workflow uses a reasonable number of steps for the task. | Deterministic only; count steps against an explicit budget or baseline. |
| `latency` | How quickly the skill produces the final usable result. | Deterministic only; measure elapsed wall-clock time for the user-visible outcome. |
| `token_efficiency` | How economically the skill uses model tokens. | Deterministic only; measure prompt/completion token consumption. |
| `context_footprint` | How much context the skill requires to do the job reliably. | Deterministic only; measure required files, tokens, or supporting artifacts. |
| `output_quality` | Human-judged quality of the final artifact when deterministic checks are insufficient. | Judge only; always pair it with a stable rubric_ref and, when available, calibration data. |

### Measures

| Measure | When To Use |
|---------|-------------|
| `deterministic` | Use when a direct oracle or exact check can score the metric consistently. |
| `verifier_backed` | Use when a programmatic verifier can judge success, but not by simple exact match. |
| `judge` | Use rubric-based human or LLM evaluation only when deterministic checks are insufficient. |

Skill tables below show metric ids with the current measure in parentheses.

## Evaluation & Testing

Skills for evaluating and testing AI agent skills

### assess-rfe

Assess RFEs against quality criteria using a structured rubric.

v1.0.0 | [opendatahub-io/assess-rfe](https://github.com/opendatahub-io/assess-rfe)

Tags: rfe, rubric, quality, assessment

| Skill | Description | Functions | Metrics |
|-------|-------------|-----------|---------|
| `/assess-rfe` | Assess RFEs against quality criteria using a structured rubric | `review` | `task_success` (`judge`), `evidence_completeness` (`judge`), `output_quality` (`judge`) |
| `/export-rubric` | Export the assessment rubric | `generate` | `task_success` (`deterministic`), `latency` (`deterministic`) |

```bash
/plugin install assess-rfe@opendatahub-skills
```

### assess-strat

Assess RHAISTRAT strategies against quality criteria using a scored rubric with calibration examples. Scores across four dimensions: feasibility, testability, scope, and architecture.

v1.0.0 | [opendatahub-io/assess-strat](https://github.com/opendatahub-io/assess-strat)

Tags: strategy, strat, rubric, quality, assessment

| Skill | Description | Functions | Metrics |
|-------|-------------|-----------|---------|
| `/assess-strat` | Assess strategies against quality criteria using a structured rubric | `review` | `task_success` (`judge`), `evidence_completeness` (`judge`), `output_quality` (`judge`) |
| `/export-rubric` | Export the assessment rubric | `generate` | `task_success` (`deterministic`), `latency` (`deterministic`) |

```bash
/plugin install assess-strat@opendatahub-skills
```

### test-plan

End-to-end test planning workflow for RHOAI: generate E2E/UI-focused test plans from Jira strategies, create traceable test cases, implement executable automation code, verify UI tests against live clusters via Playwright, publish to GitHub, resolve review feedback, and score plans with deterministic evidence gates and automated rubrics.

v2.0.0 | [opendatahub-io/odh-test-gen](https://github.com/opendatahub-io/odh-test-gen)

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

Generic agentic evaluation for skills and agents. Provides end-to-end skills to analyze, test, score, review, and iteratively improve agent skills, plus compare models/configurations and run Design-of-Experiments (ANOVA) sweeps. MLflow support for experiment tracking, tracing, and reporting. Schema-driven evaluation via eval.yaml with support for inline, LLM-based, and external judges.

v1.30.0 | Generic | [opendatahub-io/agent-eval-harness](https://github.com/opendatahub-io/agent-eval-harness)

Tags: evaluation, testing, skills, agents, mlflow, optimization, scoring, comparison, doe, anova

| Skill | Description | Functions | Metrics |
|-------|-------------|-----------|---------|
| `/eval-setup` | Optional environment configurator that verifies dependencies, API keys, and MLflow tracking for the agent-eval-harness and suggests evaluation modes based on repository contents. | `execute` | `task_success` (`verifier_backed`) |
| `/eval-analyze` | Deep-reads a target skill (or runs a custom analysis prompt) and generates a complete, grounded eval.yaml with dataset schema, outputs, judges, models, and thresholds. | `analyze`, `generate` | `task_success` (`verifier_backed`), `evidence_completeness` (`judge`) |
| `/eval-dataset` | Generates evaluation test cases for an eval.yaml -- from skill analysis, synthetic LLM generation, or MLflow traces -- bootstrapping or augmenting a dataset for /eval-run. | `generate` | `task_success` (`judge`) |
| `/eval-run` | Executes an evaluation against test cases in skill or prompt mode, scores outputs with judges, detects regressions against a baseline, and reports results. | `execute`, `verify` | `task_success` (`verifier_backed`), `evidence_completeness` (`judge`) |
| `/eval-compare` | Discovers a directory of eval run artifacts and generates a self-contained tabbed HTML comparison report with model cards, quality/cost tables, per-case breakdowns, and LLM-written analysis. | `analyze`, `generate` | `task_success` (`judge`), `evidence_completeness` (`judge`) |
| `/eval-anova` | Fan a DoE matrix of agent configs across shared cases, then run repeated-measures/mixed-effects ANOVA (F, p, effect size) plus a cost/quality Pareto. | `orchestrate`, `analyze` | `task_success` (`deterministic`) |
| `/eval-review` | Interactive human-in-the-loop review of eval judge scores and skill outputs that captures qualitative feedback and proposes targeted SKILL.md improvements. | `review` | `task_success` (`judge`), `evidence_completeness` (`judge`) |
| `/eval-mlflow` | Bridges the evaluation harness with MLflow: syncs datasets, logs run params/metrics/traces, and pushes/pulls judge and human feedback bidirectionally. | `execute` | `task_success` (`deterministic`) |
| `/eval-optimize` | Automated skill-improvement loop: runs evals, diagnoses judge failures from traces, edits the SKILL.md, re-runs, and iterates until judges pass without regressions. | `orchestrate`, `transform` | `task_success` (`verifier_backed`) |
| `/eval-check` | Scans a Claude Code harness (skills, commands, CLAUDE.md, hooks) as a system and reports redundancy, trigger overlap, misclassification, and structural issues. | `analyze`, `review` | `task_success` (`judge`), `evidence_completeness` (`judge`) |

```bash
/plugin install agent-eval-harness@opendatahub-skills
```

## Code Quality

Code review, linting, and quality enforcement

### odh-code-quality

CodeRabbit review triage and project-conformant unit test generation

v0.1.0 | Generic | Apache-2.0

Tags: code-review, coderabbit, unit-tests

| Skill | Description |
|-------|-------------|
| `/coderabbit-review` | Use when you need to evaluate CodeRabbit PR comments and fix or reply |
| `/unit-test-project-conformant` | Use this skill to write unit tests that strictly conform to the project's existing testing structure, patterns, and style by learning from similar tests before writing anything new. |

```bash
/plugin install odh-code-quality@opendatahub-skills
```

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

### odh-documentation

AsciiDoc documentation generation, validation, review, and ADR review

v0.1.0 | Apache-2.0

Tags: documentation, asciidoc, adr, review

| Skill | Description |
|-------|-------------|
| `/adr-review` | Review an Architectural Decision Record (ADR) using a team of six specialist reviewer subagents and produce a consolidated report as both PDF and PPTX slide deck. Use this skill whenever the user asks to review, critique, audit, or get feedback on an ADR, architecture decision, design doc, or RFC — whether the input is a Markdown file, a .docx document, or pasted text. Trigger even if the user does not explicitly say "ADR"; phrases like "review this architecture decision", "critique this design doc", or "run the reviewer panel on this" should also invoke this skill. |
| `/doc-gap` | Use this skill to analyze context sufficiency for documentation generation. Reads workspace/context-package.json and produces workspace/gap-report.json with severity-rated gaps and a proceed/gather-more/stop recommendation. |
| `/doc-gather` | Use when you need to gather context for a Jira ticket or PR. Resolves ticket metadata, clones relevant repos, collects candidate files, runs filtering pipeline, and produces workspace/context-package.json. |
| `/doc-generate` | Use when you need to generate AsciiDoc documentation modules from gathered context. Reads context package and gap report, generates content, then self-validates with iterative correction (up to 3 retries). Produces generated files and workspace/generation-report.json. |
| `/doc-pipeline` | Use this skill to orchestrate the full documentation pipeline. Sequences doc-gather, doc-gap, doc-validate, doc-review, and doc-generate skills based on the requested pipeline mode. |
| `/doc-plan` | Use this skill to produce a STRAT-level documentation plan. Traverses a strategic initiative's child epics and stories to identify what documentation is needed, what type, and at what priority. |
| `/doc-post` | Use this skill to post validation and review findings as comments on a GitHub PR or GitLab MR. Reads workspace findings files and formats them as inline or summary comments. |
| `/doc-review` | Use this skill to perform adversarial review of AsciiDoc documentation against context sources. Checks factual accuracy, completeness, consistency, and hallucination. Produces workspace/review-findings.json. |
| `/doc-validate` | Use when you need to validate AsciiDoc documentation for technical accuracy using Extract-Identify-Validate pattern. Runs Vale, asciidoctor, lychee, YAML syntax checks, and LLM-powered cross-reference validation. Produces workspace/validation-findings.json. |

```bash
/plugin install odh-documentation@opendatahub-skills
```

### knowledge-skills

Autonomous knowledge management skills for keeping AI context files (CLAUDE.md, AGENTS.md) up to date. Scans merged PRs, extracts relevant knowledge using parallel agents, and proposes updates as a git-apply-able patch for human review. Supports GitHub and GitLab.

v0.1.0 | Apache-2.0 | [opendatahub-io/knowledge-skills](https://github.com/opendatahub-io/knowledge-skills)

Tags: knowledge, context, claude-md, agents-md, pr-analysis, automation

| Skill | Description | Functions | Metrics |
|-------|-------------|-----------|---------|
| `/knowledge-repo` | Scan merged PRs and propose updates to AI context files (CLAUDE.md, AGENTS.md) and skill files as a git-apply-able patch | `orchestrate`, `generate` | `task_success` (`judge`) |
| `/enrich-reports` | Enrich case study skeletons with error signatures, fix types, lessons, and prevention advice via validated Python script output | `transform` | `task_success` (`judge`) |
| `/knowledge-extraction` | Ingest enriched failure reports into the LLM wiki and maintain an examples catalog of real incidents and fixes | `transform` | `task_success` (`deterministic`) |
| `/wiki-curator` | Merge duplicate wiki pages, drop stale claims, and keep the wiki index and log from growing without bound | `transform` | `task_success` (`deterministic`) |

```bash
/plugin install knowledge-skills@opendatahub-skills
```

### docs-skills

Documentation review, writing, and workflow tools for AsciiDoc and Markdown documentation. Includes an orchestrated multi-step pipeline, standalone review skills, codebase analysis for onboarding, and JIRA/PR integration.

v0.3.15 | Apache-2.0 | [opendatahub-io/docs-skills](https://github.com/opendatahub-io/docs-skills)

Tags: documentation, asciidoc, mkdocs, workflow, review, style-guide, jira, onboarding, code-analysis

| Skill | Description |
|-------|-------------|
| `/docs-orchestrator` | Documentation workflow orchestrator. Reads the step list from .agent_workspace/docs-workflow.yaml (or the plugin default). Runs steps sequentially, manages progress state, handles iteration and confirmation gates. Claude is the orchestrator — the YAML is a step list, not a workflow engine. |

```bash
/plugin install docs-skills@opendatahub-skills
```

## DevOps & CI/CD

Skills for deployment, CI/CD, and infrastructure

### odh-konflux

Konflux application and component management

v0.1.0 | Apache-2.0

Tags: konflux, ci, onboarding

| Skill | Description |
|-------|-------------|
| `/konflux-application` | Manage Konflux application |
| `/konflux-component` | Manage Konflux component |
| `/konflux-sandbox-onboarding` | Guide AIPCC engineers through obtaining access to the shared Konflux sandbox, onboarding a user-selected GitHub repository or dummy project, and verifying pull-request and push pipelines. Use when an engineer wants a hands-on Konflux staging experiment; exclude production tenants and release configuration. |

```bash
/plugin install odh-konflux@opendatahub-skills
```

### odh-rpm

RPM build failure analysis and non-Red Hat RPM detection

v0.1.0 | Apache-2.0

Tags: rpm, containers, compliance

| Skill | Description |
|-------|-------------|
| `/non-redhat-rpms` | Use this skill to identify non-Red Hat RPM packages installed in container images or on the local machine. For containers, pulls images across multiple architectures and release tags; for local scans, inspects the host directly. Extracts RPM signing metadata and reports packages not signed with the Red Hat GPG key as CSV output. Use when auditing compliance, checking supply-chain provenance, or scanning for third-party RPMs in RHOAI component images. |
| `/rpm-examine` | Analyze RPM build.log failures |

```bash
/plugin install odh-rpm@opendatahub-skills
```

### odh-vllm

vLLM backport triage, cherry-pick automation, and requirements comparison

v0.1.0 | Apache-2.0

Tags: vllm, backport, release

| Skill | Description |
|-------|-------------|
| `/vllm-backport-check-backported` | Check which candidate PRs have already been cherry-picked into the downstream branch. Use after classify-and-filter to mark already_backported on each PR. Fully deterministic — compares merge SHAs and PR titles. |
| `/vllm-backport-cherry-pick` | Auto cherry-pick backport candidates and create a draft PR on the downstream repo. Use after scoring to attempt clean cherry-picks for ai-fixable candidates. The agent must still do semantic validation on the result. |
| `/vllm-backport-classify` | Classify bugfix PRs by type (runtime_bug, platform_specific, unclear, not_bugfix) and filter by file existence at a release tag. Use after fetching raw PRs to produce a filtered candidate list. PRs marked "unclear" need agent review. |
| `/vllm-backport-fetch-prs` | Fetch merged bugfix PRs from vllm-project/vllm within a date window. Use when starting a backport triage run to get raw PR data from GitHub. Outputs a JSON array of PR objects with labels, authors, and merge commits. |
| `/vllm-backport-push-report` | Push a triage report to GitHub under a timestamped directory in reports/. Use after the agent writes the report markdown and has ranked.json ready. Outputs the report URL to stdout. |
| `/vllm-backport-score-rank` | Score and rank backport candidates using a composite formula based on verdict, severity, scope, risk, and self-containedness. Use after the agent completes semantic analysis to produce a prioritized ranked list. |
| `/vllm-compare-reqs` | Use this skill to compare vllm requirements files between versions |
| `/vllm-slack-summary` | Use this skill to generate slack summaries of vLLM CI SIG Slack channel activity for the RHAIIS midstream release team |

```bash
/plugin install odh-vllm@opendatahub-skills
```

### ec-cve-check

Inspect Enterprise Contract CVE scan results from Konflux-built container images and test ECP exception removal. Extracts the full Clair REPORTS data from cosign attestations (the same data EC's cve.cve_blockers rule evaluates), supports human-readable and JSON output, and can drive local or cluster-based EC policy validation to check whether a cve.cve_blockers exception is still needed.

v0.1.0 | Apache-2.0 | [jrusz/ec-cve-check](https://github.com/jrusz/ec-cve-check)

Tags: cve, enterprise-contract, konflux, clair, security, release-gating, cosign

| Skill | Description | Functions | Metrics |
|-------|-------------|-----------|---------|
| `/ec-cve-check` | Inspect CVE scan results and test ECP exception removal for Konflux-built images | `analyze` | `task_success` (`deterministic`) |

```bash
/plugin install ec-cve-check@opendatahub-skills
```

### disconnected-readiness-scorer

Score a repository's readiness for disconnected / air-gapped OpenShift deployments. Scans for image manifest completeness, digest enforcement, runtime egress, and Python dependency validation. Supports automatic detection of image management patterns (env var vs static CSV) and cross-references against the opendatahub-operator manifest.

v0.1.0 | Apache-2.0 | [opendatahub-io/disconnected-readiness-scorer](https://github.com/opendatahub-io/disconnected-readiness-scorer)

Tags: disconnected, air-gap, openshift, image-mirroring, readiness, scoring

| Skill | Description | Functions | Metrics |
|-------|-------------|-----------|---------|
| `/disconnected-score` | Score a repository's readiness for disconnected / air-gapped OpenShift deployments | `review` | `task_success` (`deterministic`) |

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

### pipeline-skills

Pipeline failure analysis skills for AIPCC CI/CD pipelines. Groups failed jobs by shared root cause using preprocessed error logs, then performs root cause analysis per group with structured findings, section files, and confidence-rated diagnoses. Designed to run inside a Claude Code container as part of the pipeline-failure-analyzer CI pipeline.

v0.1.0 | Apache-2.0 | [opendatahub-io/pipeline-skills](https://github.com/opendatahub-io/pipeline-skills)

Tags: pipeline, ci-cd, failure-analysis, grouping, root-cause, gitlab

```bash
/plugin install pipeline-skills@opendatahub-skills
```

## Security Review

Security analysis, threat modeling, and compliance review

### rhoai-security-reviewer

Consensus-based security review for RHOAI strategy documents (STRATs). An orchestrator spawns three independent reviewers to identify security risks, then synthesizes findings with confidence tagging based on cross-reviewer agreement. Covers 39 catalog patterns across auth, data protection, cryptographic compliance, network security, supply chain, and infrastructure.

v0.1.0 | [jctanner/ai-first-pipeline](https://github.com/jctanner/ai-first-pipeline)

Tags: security, review, strat, threat-modeling, fips, compliance, consensus

| Skill | Description |
|-------|-------------|
| `/strat-security-review` | Multi-reviewer consensus orchestrator for security review of STRAT documents. Extracts threat surfaces, spawns three independent security-reviewer instances, synthesizes findings with confidence levels, and produces a final verdict (PASS/CONCERNS/FAIL). |
| `/security-reviewer` | Individual security reviewer that assesses RHOAI strategy documents against 39 catalog patterns covering authentication, data protection, cryptographic compliance, network security, supply chain, and infrastructure. Uses a two-phase discovery-then-filter approach with severity classification. |

```bash
/plugin install rhoai-security-reviewer@opendatahub-skills
```

### odh-security

Supply-chain security alerting and OCI image CVE comparison

v0.1.0 | Generic | Apache-2.0

Tags: cve, supply-chain, oci

| Skill | Description |
|-------|-------------|
| `/oci-cve-checker` | Use this skill to compare CVE vulnerabilities between two OCI container images and generate reports showing fixed and new CVEs. |
| `/security-alert` | Use this skill to filter a pre-fetched set of Hacker News stories down to those that report supply-chain security threats relevant to the Red Hat / RHEL ecosystem, Python (PyPI/pip), or JavaScript/TypeScript (npm/yarn/pnpm). Reads stories from stories.json in the workspace, performs semantic analysis (fetching HN threads when the title alone is ambiguous), and writes the stories worth alerting on to findings.json. |

```bash
/plugin install odh-security@opendatahub-skills
```

## Development Tools

Developer productivity tools for packaging, CI/CD debugging, and workflow automation

### odh-ai-helpers

[DEPRECATED] Backwards-compatibility umbrella for the ODH AI Helpers plugins. Re-exports the skills that existed before the split into the individual odh-* plugins under their original odh-ai-helpers:* names, so existing agents and workflows keep working. Install the odh-* plugins you need, then uninstall this one; it will be removed after the migration window.

v0.1.0 | Generic | Apache-2.0 | [opendatahub-io/ai-helpers](https://github.com/opendatahub-io/ai-helpers)

Tags: deprecated

| Agent | Description |
|-------|-------------|
| python-packaging-investigator | Investigates Python package repositories to analyze build systems, dependencies, and packaging complexity |

```bash
/plugin install odh-ai-helpers@opendatahub-skills
```

### odh-general

General-purpose helpers and learning mode

v0.1.0 | Generic | Apache-2.0

Tags: mentoring, learning

| Skill | Description |
|-------|-------------|
| `/learning-mode` | Hands-on mentoring: the agent scaffolds work, then pauses so the engineer writes small, meaningful code (roughly 5–15 lines) for practice. Use when the user enables learning mode, asks for guided mentoring, hands-on practice, collaborative coding, or teaching while building a feature. |

```bash
/plugin install odh-general@opendatahub-skills
```

### odh-git

Git utilities, GitHub/GitLab workflow automation, and CI debugging

v0.1.0 | Generic | Apache-2.0

Tags: git, github, gitlab, ci, gist

| Skill | Description |
|-------|-------------|
| `/aipcc-commit-suggest` | Generate AIPCC Commits style commit messages or summarize existing commits |
| `/gist-upload` | Use this skill to upload a summary or plan from the current conversation as a GitHub Gist using the `gh` CLI. |
| `/git-shallow-clone` | Use this skill to perform a shallow clone of a Git repository to a temporary location. |
| `/github-actions-debugger` | Debug and monitor GitHub Actions workflow runs. Check run status, view failed job logs, and troubleshoot CI failures. Use this when the user needs to investigate GitHub Actions failures, inspect job output, or identify the root cause of a broken workflow run. |
| `/github-sync-upstream` | Sync code from an upstream GitHub repository into a target fork (e.g., opendatahub-io midstream). Detects remotes from the current repo, or clones fresh if run from outside. Fetches upstream, merges into a sync branch, restores protected files, resolves conflicts, and opens a PR to the target GitHub repo. Use when asked to sync upstream, merge upstream changes, or bring a GitHub fork up to date with its upstream source. |
| `/gitlab-pipeline-debugger` | Debug and monitor GitLab CI/CD pipelines for merge requests. Check pipeline status, view job logs, and troubleshoot CI failures. Use this when the user needs to investigate GitLab CI pipeline issues, check job statuses, or view specific job logs. |

```bash
/plugin install odh-git@opendatahub-skills
```

### odh-google-workspace

Gmail, Google Calendar, Docs, and Drive integration

v0.1.0 | Generic | Apache-2.0

Tags: google-workspace, gmail, calendar, drive

| Skill | Description |
|-------|-------------|
| `/email-meeting-summary` | Use when the user wants to summarize a Google Meet meeting and send the summary by email. Reviews a Google Meet transcript for a specific meeting topic, then composes a Gmail draft summarizing decisions and action items for that topic. Prompts for meeting selection if not specified, and for topic selection before drafting. Stops with a message if the transcript is not yet available. |
| `/gmail-draft` | Use this skill to compose a Gmail draft from text content in the conversation. Accepts a body, recipient list, and subject — either from the user or from context — and creates a draft in the user's Gmail Drafts folder via gws. |
| `/google-workspace` | Fetch and query data from Google Workspace using the gws CLI — Gmail, Calendar, Docs, Sheets, Slides, and Drive. Use this skill whenever the user mentions email, inbox, messages, calendar, meetings, schedule, agenda, Google Docs, spreadsheets, presentations, or Drive files. Trigger on phrases like "check my email", "what meetings do I have", "read this doc", "open this spreadsheet", "find files in Drive", or any Google URL (docs.google.com, drive.google.com). |

```bash
/plugin install odh-google-workspace@opendatahub-skills
```

### odh-jira

Jira ticket management, search, triage, and automation

v0.1.0 | Apache-2.0

Tags: jira, acli, triage, automation

| Skill | Description |
|-------|-------------|
| `/acli-setup-check` | Verify acli installation and authentication. Checks if acli is installed, authenticated to Jira, and can query projects. Use when troubleshooting acli issues or setting up acli for the first time. |
| `/ai-bug-fix-triage` | Triage JIRA bugs against repository code to classify AI fixability. Use when reviewing a backlog of bugs to determine which ones an AI agent can fix. |
| `/jira-activity` | Summarize Jira ticket activity, including child tickets, to detect stale tickets in the backlog. Use when user asks to review one or more Jira tickets to determine if they are being worked on. |
| `/jira-aipcc-create` | Create AIPCC-org Jira issues in the RHAI project. Infers summary, description, type, and component from conversation context, confirms with the user before creating. Use when the user wants to file a new AIPCC Jira issue. |
| `/jira-sprint-summary` | Generate comprehensive sprint summaries by analyzing JIRA sprint data, including issue breakdown, progress metrics, and team performance insights. |
| `/jira-upload-chat-log` | Use this skill to export and upload the current chat conversation as a markdown file attachment to a JIRA ticket for later review and documentation. |
| `/jira-workitem-attach` | Upload file attachments to Jira tickets. Verifies file exists and uploads via Jira API. Use when user wants to attach files to tickets. |
| `/jira-workitem-comment` | Add comments to Jira tickets using simple text or Jira markup (ADF JSON). Supports rich formatting with code blocks, lists, mentions, and links. Use when user wants to comment on a ticket. |
| `/jira-workitem-search` | Search Jira tickets using JQL queries. Provides common query templates and flexible output formats. Use when user needs to find or filter tickets. |
| `/jira-workitem-view` | Retrieve and display full details of a Jira ticket. Fetches all fields and formats them for conversation context. Use when user needs ticket information or wants to examine a ticket. |
| `/pr-jira-linker` | Find and link Jira issues to PRs/MRs that are missing Jira references. Supports single PR/MR linking and batch audit of configured repos. Use when the user mentions "link PR to Jira", "scan PRs", "PR audit", "MR missing Jira", "link merge request", or wants to connect code changes to Jira for traceability. |
| `/triage-bug-readiness` | Use when assessing a Jira bug ticket for AI autofix readiness. Produces a structured JSON verdict (ready/needs_info/not_fixable) based on a three-gate rubric. Designed for CI pipeline use with the jira-triage orchestrator. |

```bash
/plugin install odh-jira@opendatahub-skills
```

### odh-modules

ODH module operator scaffolding, migration, and compliance checks

v0.1.0 | Apache-2.0

Tags: operator, modules, scaffolding, compliance

| Skill | Description |
|-------|-------------|
| `/module-compliance` | Check an ODH module operator repository for contract violations against the platform onboarding guide. Validates PlatformObject status, CRD structure, Helm chart content, webhook ownership, metadata conventions, and reconciler chain ordering. Use during code review or after scaffolding a new module. |
| `/module-migrate` | Read existing in-tree ODH operator component code and produce a step-by-step extraction checklist for migrating it to a standalone module. Analyzes controller logic, webhooks, RBAC, embedded manifests, and DSC field mappings. Use when extracting a component from the monolithic operator into its own module repo. |
| `/module-scaffold` | Given a component name, generate a complete standalone ODH module operator repository. Produces Go module, CRD types implementing PlatformObject, controller skeleton with reconciler builder pattern, Helm chart, Makefile, CI config, singleton webhook, and AGENTS.md. Use when starting a new module from scratch. |

```bash
/plugin install odh-modules@opendatahub-skills
```

### odh-python-packaging

Python package analysis, security auditing, and build complexity assessment

**Requires:** `odh-git`

v0.1.0 | Generic | Apache-2.0

Tags: python-packaging, licensing, dependencies, security-audit

| Skill | Description |
|-------|-------------|
| `/python-full-deps` | Resolve the full install-time dependency tree for a Python package. Use when the user needs all transitive dependencies, full dependency list, or install requirements resolved for a specific Python version with environment markers. |
| `/python-packaging-binary-audit` | Scan a Python package repository for compiled/binary files using Fromager-style detection and malcontent YARA analysis, then triage findings with deterministic rules and AI reasoning to produce a structured risk report section. |
| `/python-packaging-bug-finder` | Use when you need to find known packaging bugs, fixes, and workarounds for Python projects by searching GitHub issues and analyzing their resolution status |
| `/python-packaging-complexity` | Use this skill to analyze Python package build complexity by inspecting PyPI metadata. Evaluates compilation requirements, dependencies, distribution types, and provides recommendations for wheel building strategies. |
| `/python-packaging-env-finder` | Use this skill to investigate environment variables that can be set when building Python wheels for a given project. Analyzes setup.py, CMake files, and other build configuration files to discover customizable build environment variables. |
| `/python-packaging-git-audit` | Inspect recent git history of a Python package repository for suspicious commits touching supply-chain-sensitive files, then triage findings with AI reasoning to produce a structured risk report section. |
| `/python-packaging-license-checker` | Use this skill to check whether a Python package license is compatible with redistribution in Red Hat products, using the Fedora License Data as the authoritative policy source. Produces a structured six-field verdict with escalation guidance for non-trivial cases. |
| `/python-packaging-license-finder` | Use this skill to deterministically find license information for Python packages by checking PyPI metadata first, then falling back to Git repository LICENSE files using shallow cloning. |
| `/python-packaging-security-audit` | Use this skill to evaluate the security of a Python package repository by orchestrating static analysis, binary scanning, and git history inspection sub-skills in parallel, then combining their results into a unified security report with a risk rating. |
| `/python-packaging-source-finder` | Use this skill to locate source code repositories for Python packages by analyzing PyPI metadata, project URLs, and code hosting platforms like GitHub, GitLab, and Bitbucket. Provides deterministic results with confidence levels. |
| `/python-packaging-static-audit` | Run hexora static analysis on a Python package repository to detect suspicious code patterns, then triage findings with deterministic rules and AI reasoning to produce a structured risk report section. |

| Agent | Description |
|-------|-------------|
| python-packaging-investigator | Investigates Python package repositories to analyze build systems, dependencies, and packaging complexity. Provides comprehensive guidance on how packages can be built from source using integrated analysis skills. |

```bash
/plugin install odh-python-packaging@opendatahub-skills
```

### odh-pytorch

PyTorch cross-language analysis with TorchTalk

v0.1.0 | Generic | Apache-2.0

Tags: pytorch, torchtalk, mcp

| Skill | Description |
|-------|-------------|
| `/torchtalk-analyzer` | Analyze PyTorch internals across Python, C++, and CUDA layers using the TorchTalk MCP server. Use when asked about how PyTorch operators work internally, where functions are implemented, what would break if code is modified, or finding tests for PyTorch operators. |
| `/torchtalk-setup` | Install and configure TorchTalk MCP server for PyTorch cross-language analysis |
| `/torchtalk-trace` | Trace a PyTorch function's cross-language binding chain (Python -> C++ -> CUDA) |

```bash
/plugin install odh-pytorch@opendatahub-skills
```

### odh-team

Team weekly reports, engineer activity snapshots, and delivery postmortems

v0.1.0 | Apache-2.0

Tags: reporting, postmortem, jira, github

| Skill | Description |
|-------|-------------|
| `/create-delivery-postmortem` | Use when a release delay, missed deadline, or delivery incident needs a structured post-mortem. Facilitates context gathering, timeline synthesis, and interactive Five Whys root cause analysis. Produces an executive-ready document in HTML or Markdown. |
| `/engineer-snapshot` | Generate an engineer activity snapshot showing active JIRA issues with days open, blocked work, upstream PRs awaiting review, recently merged PRs, and open action items from 1:1 notes. Requires a team config YAML file. Use when the user asks to review an engineer's status, check someone's workload, or prepare for a 1:1. |
| `/team-weekly-report` | Generate a weekly team status report combining JIRA and GitHub data. Fetches closed, open, stale, and blocked issues plus PR activity for each team member. Requires a team config YAML file with JIRA project, GitHub repos, and team member mappings. Use when the user asks for a weekly report, team status, or team update. |

```bash
/plugin install odh-team@opendatahub-skills
```

### autofix-skills

Claude Code plugin for the Jira autofix pipeline. Provides orchestrator skills, agent prompt files, and deterministic Python scripts for automated bug fixing, CVE remediation, and ticket triage. Designed to run inside a Claude Code container as part of a CI pipeline.

v0.1.0 | Apache-2.0 | [opendatahub-io/autofix-skills](https://github.com/opendatahub-io/autofix-skills)

Tags: autofix, jira, cve, bug-fixing, triage, pipeline, ci-cd

| Skill | Description | Functions | Metrics |
|-------|-------------|-----------|---------|
| `/autofix-resolve` | Orchestrate end-to-end bug fixing via implement and review agent loop (max 3 iterations) | — | — |
| `/autofix-cve-resolve` | CVE remediation across multiple repos with state-machine dispatch | — | — |
| `/autofix-triage` | Assess bug tickets for AI autofix readiness (ready/needs_info/not_fixable) | — | — |
| `/autofix-repo-resolve` | Disambiguate which repository a Jira ticket targets when it mentions several, and write a verdict with confidence | `analyze` | `task_success` (`verifier_backed`) |

```bash
/plugin install autofix-skills@opendatahub-skills
```

### autoqa-skills

AI skills for AutoQA CI/CD test failure analysis and triage. Covers root cause analysis of test failure logs, matching failures against historical Jira tickets, and classifying failures as known infrastructure false alarms. Designed to run inside a Claude Code container as part of the AutoQA CI pipeline.

v0.1.0 | Apache-2.0 | [opendatahub-io/autoqa-skills](https://github.com/opendatahub-io/autoqa-skills)

Tags: ci, test, failure-analysis, triage, jira, autoqa, false-alarm

```bash
/plugin install autoqa-skills@opendatahub-skills
```

### python-package-skills

AI skills for Python package onboarding into the RHAI distribution pipeline. End-to-end automation covering packaging investigation, license checking, security auditing, build failure analysis, fondue monorepo onboarding, constraint bug descriptions, hardware variant resolution, probe test creation, Jira context summarization, and executive summary generation. Designed to run inside a Claude Code container as part of the package-onboarding CI pipeline.

v0.1.0 | Apache-2.0 | [opendatahub-io/python-package-skills](https://github.com/opendatahub-io/python-package-skills)

Tags: python-packaging, onboarding, fondue, investigation, security, license, testing, constraints, hardware, accelerators

```bash
/plugin install python-package-skills@opendatahub-skills
```

### patternfly

Everything you need for PatternFly development -- React components, design guidance, migration, and MCP docs. Installs all PatternFly sub-plugins in one step.

**Includes:** `pf-react`, `pf-design-guide`, `pf-design-audit`, `pf-a11y`, `pf-migration`, `pf-code-review`, `pf-mcp`

v0.1.0 | Generic | MIT

Tags: patternfly, react, uxd, design, mcp, components, migration

```bash
/plugin install patternfly@opendatahub-skills
```

### pf-react

React component development -- coding standards, testing, and structure

v0.1.0 | Generic | MIT

Tags: patternfly, react

| Skill | Description |
|-------|-------------|
| `/pf-chart-gen` | Generate PatternFly chart components with theming, responsive sizing, and accessibility. Use when building charts, data visualizations, or dashboards with PatternFly. |
| `/pf-component-check` | Audit PatternFly React component nesting, wrapper hierarchies, and layout structure. Use when scanning for hierarchy violations or debugging spacing caused by missing wrapper components. |
| `/pf-component-reuse-check` | Detects custom React components in newly created or modified (uncommitted) code that overlap with PatternFly React components, suggests the PatternFly equivalent, and can replace the custom component then build to verify. Use when creating UI components, reviewing uncommitted React changes, or when the user asks to prefer PatternFly instead of a custom component. |
| `/pf-deploy` | Deploy a PatternFly React project to GitHub Pages using pfcli deploy. Use when publishing a prototype, sharing a demo URL, deploying to GitHub Pages, or when the user mentions pfcli deploy. |
| `/pf-design-comments-setup` | Integrate @patternfly/design-comments into React apps for on-page design feedback, pinned comment threads, GitHub Issues sync, and Jira linking. Use when adding design comments, review overlays, or removing the commenting system from a PatternFly React project. |
| `/pf-form-gen` | Generate PatternFly form components with validation, layout, and accessibility. Use when building forms, adding form fields, or creating validated input workflows. |
| `/pf-import-check` | Audit and fix invalid PatternFly import paths across packages. Use when imports fail, modules are unresolved, or after upgrading PatternFly versions. |
| `/pf-project-gen` | Scaffolds PatternFly React projects with PF6-safe dependencies, imports, and starter layout. Use when creating a new PatternFly app or bootstrapping a migration sandbox. |
| `/pf-table-gen` | Generate PatternFly table components with sorting, filtering, pagination, and expandable rows. Use when building data tables, adding table features, or migrating HTML tables to PatternFly. |
| `/pf-test-gen` | Generate a unit test file for a React component using Testing Library. Use when adding test coverage to new or existing components. |

```bash
/plugin install pf-react@opendatahub-skills
```

### pf-design-guide

Design guide -- component selection, interaction patterns, AI experience patterns

v0.1.0 | Generic | MIT

Tags: patternfly, design

| Skill | Description |
|-------|-------------|
| `/pf-figma-design-mode` | Create and edit Figma design files using PatternFly-approved component libraries. Use when building, updating, or restructuring Figma frames and components. Requires Figma MCP. |
| `/pf-screenshot-mapping` | Maps screenshots and UI mockups (any fidelity) to PatternFly 6 layout and building-block components. Output uses PF Component Mapping (regions, PF6 direction including structure and behavior, doc links) and PF Gaps & Recommendations (structural gaps/stretches and design-system follow-ups). Omits branding and visual styling (logos, colors, typography, border radius, shadows, component shape). Use when the user shares a UI image or asks whether a screen can be built with PatternFly, which PatternFly components to use, or for a PatternFly component pass on a wireframe, lo-fi, or third-party UI reference. |

```bash
/plugin install pf-design-guide@opendatahub-skills
```

### pf-design-audit

Design audit -- validate existing code and designs against PatternFly standards

v0.1.0 | Generic | MIT

Tags: patternfly, design, audit

| Skill | Description |
|-------|-------------|
| `/pf-ai-audit` | Audit AI-powered features against Red Hat's AI design language — transparency notices, iconography, chatbot patterns, color and gradient rules. Use when reviewing chatbots, AI assistants, or generation UIs for brand compliance. |
| `/pf-color-scan` | Find raw color values (hex, rgb, hsl) in code and suggest PatternFly design token replacements. Use when auditing stylesheets for hardcoded colors or enforcing token compliance. |
| `/pf-css-token-check` | Detect hardcoded color, spacing, typography, border radius and shadow values that have PF token equivalents and suggest the correct design token replacements. Works on CSS, SCSS, CSS-in-JS, and inline styles. Use when auditing stylesheets for hardcoded values, enforcing design token compliance, or refactoring styles to use PatternFly tokens. |
| `/pf-figma-check` | Check Figma designs against PatternFly v6 standards for colors, typography, spacing, and component usage. Use when validating a design before handoff, auditing existing mockups for compliance, or reviewing design token usage. Requires Figma MCP. |
| `/pf-figma-token-check` | Audit designs against the PatternFly 6 token architecture and bridge Figma styles to PF semantic tokens. Use when validating token usage, mapping Figma variables to PF tokens, or checking designs for token compliance. |
| `/pf-icon-finder` | Identify PatternFly icons in design mockups and provide the correct React import statements. Use when implementing a design, verifying icon usage in a prototype, or finding the correct icon imports for React components. |

```bash
/plugin install pf-design-audit@opendatahub-skills
```

### pf-a11y

Accessibility auditing, reporting, and documentation

v0.1.0 | Generic | MIT

Tags: patternfly, accessibility, a11y

| Skill | Description |
|-------|-------------|
| `/pf-a11y-audit` | Audit PatternFly components and pages against WCAG and ARIA best practices. Use when reviewing accessibility, fixing screen reader issues, or validating ARIA usage in PatternFly-based applications. |
| `/pf-a11y-keyboard` | Test keyboard accessibility of PatternFly UIs via live browser interaction. Use when validating keyboard navigation, focus management, or interaction patterns in a running application. |

```bash
/plugin install pf-a11y@opendatahub-skills
```

### pf-migration

PF version migration -- breaking change detection, class scanning, upgrade planning

v0.1.0 | Generic | MIT

Tags: patternfly, migration

| Skill | Description |
|-------|-------------|
| `/pf-css-migration-scan` | Scan code for legacy PatternFly CSS classes and recommend PF6-safe replacements. Use when upgrading from PF4/PF5 or auditing a codebase for deprecated class names. |
| `/pf-react-migration-scan` | Scan code for @patternfly/react-* API breaking changes and produce a markdown report. Use when upgrading PatternFly React versions, auditing component API usage, or checking for removed props, renamed components, or import path changes. |
| `/pf-release-candidate-update` | Update @patternfly/* npm dependencies to the latest release candidate versions. Use when testing the next PF release or bumping to RC packages. |

```bash
/plugin install pf-migration@opendatahub-skills
```

### pf-code-review

Code review and quality -- adversarial review, security patterns

v0.1.0 | Generic | MIT

Tags: patternfly, code-review

| Skill | Description |
|-------|-------------|
| `/pf-review` | Run all PatternFly compliance checks on a project — imports, components, colors, legacy CSS, and security. Use when auditing PF code, before merging PRs, or for comprehensive compliance review. |
| `/pf-security-scan` | Scan PatternFly React code for security anti-patterns — XSS via dangerouslySetInnerHTML, unsanitized user input in tooltips/labels, and insecure href patterns. Use when reviewing PF code for security vulnerabilities or auditing user-controlled content in PF components. |

```bash
/plugin install pf-code-review@opendatahub-skills
```

### pf-mcp

PatternFly MCP server -- component documentation, design token lookup, and accessibility guidance via the Model Context Protocol

v0.1.0 | Generic | MIT

Tags: patternfly, mcp

| MCP Server | Description |
|------------|-------------|
| patternfly | PatternFly component documentation, design token lookup, and accessibility guidance via the Model Context Protocol |

```bash
/plugin install pf-mcp@opendatahub-skills
```

## Product Planning

Skills for requirements, RFEs, and product strategy

### rfe-creator

Claude Code skills for creating, reviewing, splitting and submitting work items — RFEs to the RHAIRFE Jira project and Initiatives to RHOAIENG — through one generic pipeline (/rfe-create, /rfe-review, /rfe-split, /rfe-submit, /rfe-auto-fix, /rfe-speedrun; --type initiative for Initiatives). The legacy dotted names (/rfe.create and friends) remain as compatibility aliases.

v0.1.0 | [opendatahub-io/rfe-creator](https://github.com/opendatahub-io/rfe-creator)

Tags: rfe, initiative, jira, review, pipeline

| Skill | Description | Functions | Metrics |
|-------|-------------|-----------|---------|
| `/rfe-create` | Write a new work item of any registered type — an RFE from a problem statement, idea, or need (business needs, WHAT/WHY), or an Initiative from an objective or strategic goal (/rfe-create --type initiative ...). Asks clarifying questions, then produces well-formed items. Use when starting from scratch. | `generate` | `task_success` (`judge`) |
| `/rfe-review` | Review and improve work items of any registered type — RFEs (RHAIRFE) and Initiatives (RHOAIENG, /rfe-review --type initiative). Accepts one or more Jira keys to fetch and review existing items, or reviews local artifacts from /rfe-create. Runs rubric scoring and the type's review dimensions (technical feasibility, strategic alignment), then auto- revises the issues it finds. | `review` | `task_success` (`judge`), `output_quality` (`judge`) |
| `/rfe-split` | Split oversized work items of any registered type — RFEs and Initiatives — into smaller, right-sized ones. Takes one or more IDs of items already in the workspace (fetched by /rfe-review or written by /rfe-create; e.g. /rfe-split RHAIRFE-1234 RHAIRFE-5678, /rfe- split --type initiative INIT-001) and skips an ID with no local task file. Runs non- interactively — decomposes, generates new items, reviews them, self-corrects, and checks coverage. | `transform` | `task_success` (`judge`) |
| `/rfe-submit` | Submit or update work items of any registered type in Jira — new RHAIRFE tickets for new RFEs, RHOAIENG Initiative tickets for Initiatives (/rfe-submit --type initiative), or updates to existing tickets fetched from Jira. Use after /rfe-review. | `execute` | `task_success` (`deterministic`) |
| `/rfe-speedrun` | End-to-end pipeline for work items of any registered type — RFEs by default, Initiatives with --type initiative. Accepts a single idea, Jira key(s), or a YAML batch file. Creates, reviews, auto-fixes (with splits), and submits. Supports --headless, --announce-complete, and --dry-run for CI. | `orchestrate` | `task_success` (`judge`) |
| `/rfe-auto-fix` | Review and fix batches of work items automatically — RFEs by default, any registered type with --type (e.g. --type initiative). Accepts explicit IDs or a JQL query. Reviews, auto- revises, and splits oversized items. Non-interactive. | `orchestrate` | `task_success` (`judge`) |
| `/rfe.create` | Compatibility alias for /rfe-create, kept so existing /rfe.create invocations keep working. Write a new RFE: prefer /rfe-create (Initiatives: /rfe-create --type initiative). | `generate` | `task_success` (`judge`) |
| `/rfe.review` | Compatibility alias for /rfe-review, kept so existing /rfe.review invocations keep working. Review, improve and auto-revise RFEs: prefer /rfe-review (Initiatives: /rfe- review --type initiative). | `review` | `task_success` (`judge`), `output_quality` (`judge`) |
| `/rfe.split` | Compatibility alias for /rfe-split, kept so existing /rfe.split invocations keep working. Split oversized RFEs: prefer /rfe-split (Initiatives: /rfe-split --type initiative). | `transform` | `task_success` (`judge`) |
| `/rfe.submit` | Compatibility alias for /rfe-submit, kept so existing /rfe.submit invocations keep working. Submit or update RFEs in Jira: prefer /rfe-submit (Initiatives: /rfe-submit --type initiative). | `execute` | `task_success` (`deterministic`) |
| `/rfe.speedrun` | Compatibility alias for /rfe-speedrun, kept so existing /rfe.speedrun invocations keep working. End-to-end RFE pipeline: prefer /rfe-speedrun (Initiatives: /rfe-speedrun --type initiative). | `orchestrate` | `task_success` (`judge`) |
| `/rfe.auto-fix` | Compatibility alias for /rfe-auto-fix, kept so existing /rfe.auto-fix invocations keep working. Batch review, revision and split of RFEs: prefer /rfe-auto-fix (Initiatives: /rfe-auto-fix --type initiative). | `orchestrate` | `task_success` (`judge`) |
| `/rfe-creator.update-deps` | Update vendored dependencies | `execute` | `task_success` (`deterministic`) |

```bash
/plugin install rfe-creator@opendatahub-skills
```

### strat-creator

Claude Code skills for creating, reviewing, and submitting strategies to the RHAISTRAT Jira project. Provides an automated pipeline from initial creation through refinement, adversarial review with independent reviewers, and human sign-off workflow with pull/push/signoff gates.

**Requires:** `assess-strat`

v0.1.0 | [opendatahub-io/strat-creator](https://github.com/opendatahub-io/strat-creator)

Tags: strategy, strat, jira, review, pipeline

| Skill | Description | Functions | Metrics |
|-------|-------------|-----------|---------|
| `/strategy-create` | Create strategies from approved RFEs by cloning them to RHAISTRAT in Jira | `execute` | `task_success` (`judge`) |
| `/strategy-refine` | Refine a strategy with technical HOW, dependencies, and NFRs | `transform` | `task_success` (`judge`) |
| `/strategy-review` | Adversarial review with rubric scoring and independent forked reviewers | `review` | `task_success` (`judge`), `output_quality` (`judge`) |
| `/strategy-pull` | Pull a post-CI strategy from Jira into local workspace for human review | `retrieve` | `task_success` (`deterministic`) |
| `/strategy-push` | Push a locally-refined strategy back to Jira and resubmit to CI | `execute` | `task_success` (`deterministic`) |
| `/strategy-signoff` | Sign off on a CI-approved strategy with human sign-off label | `execute` | `task_success` (`deterministic`) |
| `/export-rubric` | Export the scoring rubric to artifacts/strat-rubric.md | `generate` | `task_success` (`deterministic`), `latency` (`deterministic`) |

```bash
/plugin install strat-creator@opendatahub-skills
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

## Team-Specific

Plugins hardcoded to a specific team's setup. Not generally reusable by other teams without modification.

### odh-llm-d

llm-d release orchestration for opendatahub-io

v0.1.0 | Team-Specific | Apache-2.0

Tags: llm-d, release, konflux

| Skill | Description |
|-------|-------------|
| `/ai-gateway-operator-manifest-update` | Update batch-gateway manifests in opendatahub-io/ai-gateway-operator when the pinned llm-d-batch-gateway-operator main commit changes. |
| `/odh-llm-d-release` | Orchestrate the opendatahub-io release for all llm-d components in one cycle. Collects upstream(llm-d) versions, auto-discovers the release tracker issue, then spawns parallel sub-agents — one per component (release branch, Konflux onboarder workflow, PR validation, approve+merge, Quay image verify, GitHub draft release) plus one KServe metadata PR sub-agent — and posts the final #Release# tracker comment. Use when the release manager runs on/before ODH code-freeze date for the llm-d team. |

```bash
/plugin install odh-llm-d@opendatahub-skills
```

### odh-maas

MaaS nightly QE impact analysis

v0.1.0 | Team-Specific | Apache-2.0

Tags: maas, qe, autofix

| Skill | Description |
|-------|-------------|
| `/maas-nightly-qe-impact` | Assess whether a Models-as-a-Service autofix change requires follow-up in opendatahub-tests or ods-ci nightly QE pipelines. Runs as a Jira autofix post_review extension for the Model as a Service component. Appends a Nightly QE Impact section to the PR description and writes informational findings. Use when autofix completes a fix in models-as-a-service. |

```bash
/plugin install odh-maas@opendatahub-skills
```

### productization-skills

Claude Code plugin with specialized skills for DevOps and cloud-native development workflows. Provides skills for GitLab CI/CD analysis, AWS CloudWatch Logs troubleshooting, Slack integration, GitLab branch management, Jira utilities, Konflux ITS analysis, cloud infrastructure provisioning via mapt, and Google Workspace integration.

v0.8.1 | Team-Specific | Apache-2.0 | [opendatahub-io/productization-skills](https://github.com/opendatahub-io/productization-skills)

Tags: gitlab, aws, slack, jira, konflux, mapt, devops, ci-cd, cloud, provisioning, google-workspace, reporting

| Skill | Description | Functions | Metrics |
|-------|-------------|-----------|---------|
| `/gitlab-job-analyzer` | Analyze GitLab CI/CD job failures with structured scripts and error pattern recognition | `analyze` | `task_success` (`judge`) |
| `/aws-log-analyzer` | Troubleshoot and analyze AWS CloudWatch Logs for debugging and monitoring | `analyze` | `task_success` (`judge`) |
| `/slack-utilities` | Search messages, post updates, and interact with Slack workspaces | `retrieve`, `execute` | `task_success` (`judge`) |
| `/gitlab-branch-manager` | Create and protect GitLab branches with configurable protection rules | `execute` | `task_success` (`judge`) |
| `/jira-utilities` | Manage Jira issues with JQL search, create/update issues, link issues, and sprint info | `retrieve`, `execute` | `task_success` (`judge`) |
| `/jira-cve-tracker` | CVE deduplication and release-date clustering for Jira issues | `retrieve`, `analyze` | `task_success` (`judge`) |
| `/jira-release-setup` | Set up Jira release versions and manage release workflows | `execute` | `task_success` (`judge`) |
| `/jira-sprint-manager` | Create sprints and assign issues to sprints on Jira boards | `execute` | `task_success` (`judge`) |
| `/jira-gap-audit` | Audit Jira releases for gaps in issue coverage | `analyze` | `task_success` (`judge`) |
| `/mapt-provisioner` | Provision and manage cloud VMs on AWS and Azure using mapt | `execute` | `task_success` (`judge`) |
| `/konflux-its-analyzer` | Analyze Konflux integration test scenario failures | `analyze` | `task_success` (`judge`) |
| `/gitlab-code-review` | Structured GitLab merge request code review | `review` | `task_success` (`judge`) |
| `/slack-webhook` | Post messages to Slack channels via incoming webhooks | `execute` | `task_success` (`judge`) |
| `/weekly-status` | Generate weekly status reports from project activity | `generate` | `task_success` (`judge`) |
| `/gws-calendar-reader` | Read Google Calendar events and check free/busy status | `retrieve` | `task_success` (`judge`) |
| `/gws-doc-action-extractor` | Extract action items from Google Docs | `retrieve`, `analyze` | `task_success` (`judge`) |
| `/gws-drive-reader` | List, search, and read files from Google Drive | `retrieve` | `task_success` (`judge`) |
| `/gws-slides-analyzer` | Read, search, and create Google Slides presentations | `retrieve`, `generate` | `task_success` (`judge`) |

```bash
/plugin install productization-skills@opendatahub-skills
```
