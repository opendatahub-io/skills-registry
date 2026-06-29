---
title: test-plan
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan

End-to-end test planning and automation workflow for RHOAI (Red Hat OpenShift AI).
Takes a Jira strategy document as input and produces a complete test plan, individual
test case specifications, executable test automation code, and visual UI verification
reports. The pipeline uses parallel sub-agent analysis (endpoints, risks, infrastructure)
to extract testable interfaces, then scores quality with a 5-criteria rubric and
auto-revises up to 2 cycles. Supports the full lifecycle: create, review, publish to
GitHub, resolve PR feedback, update with new documentation, and verify UI test cases
against live clusters via Playwright. Test code generation uses odh-test-context for
repo-specific conventions, Tiger Team pattern guides, and intelligent placement analysis
to decide whether tests belong in the component repo or downstream E2E repo.


!!! info "Plugin Details"

    - **Version**: 1.0.1
    - **Author**: Federico Mosca
    - **Category**: [Evaluation & Testing](../../categories/evaluation.md)
    - **Repository**: [opendatahub-io/odh-test-gen](https://github.com/opendatahub-io/odh-test-gen)
    - **Tags**: <span class="tag-pill">test-plan</span> <span class="tag-pill">test-cases</span> <span class="tag-pill">quality</span> <span class="tag-pill">strategy</span> <span class="tag-pill">review</span> <span class="tag-pill">scoring</span> <span class="tag-pill">automation</span> <span class="tag-pill">playwright</span> <span class="tag-pill">ui-testing</span>

## Pipeline

<div class="diagram-container" markdown>
![test-plan pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/test-plan-create`](test-plan-create.md) | Generate a test plan from a strategy | :material-check: |
| [`/test-plan-create-cases`](test-plan-create-cases.md) | Generate test case files from a test plan | :material-check: |
| [`/test-plan-update`](test-plan-update.md) | Update test plan with new docs (ADR, API specs), re-analyze, bump version | :material-check: |
| [`/test-plan-case-implement`](test-plan-case-implement.md) | Generate executable test automation code from TC specifications with intelligent placement | :material-check: |
| [`/test-plan-ui-verify`](test-plan-ui-verify.md) | Verify UI test cases from a PR against a live ODH/RHOAI cluster via Playwright; supports upgrade testing workflow | :material-check: |
| [`/test-plan-publish`](test-plan-publish.md) | Publish test plan artifacts to GitHub with PR creation | :material-check: |
| [`/test-plan-resolve-feedback`](test-plan-resolve-feedback.md) | Assess and resolve PR review comments on test plans | :material-check: |
| [`/test-plan-score`](test-plan-score.md) | Score test plan quality using rubric without auto-revision | :material-check: |
| [`/test-plan-analyze-endpoints`](test-plan-analyze-endpoints.md) | Extract scope and API endpoints | :material-close: internal |
| [`/test-plan-analyze-risks`](test-plan-analyze-risks.md) | Determine test levels, priorities, NFRs, and risks | :material-close: internal |
| [`/test-plan-analyze-infra`](test-plan-analyze-infra.md) | Identify environment and infrastructure needs | :material-close: internal |
| [`/test-plan-merge`](test-plan-merge.md) | Intelligently merge new analyzer findings into existing test plan | :material-close: internal |
| [`/test-plan-resolve-gaps`](test-plan-resolve-gaps.md) | Cross-reference gaps with new findings to determine what's resolved | :material-close: internal |
| [`/test-plan-analyze-placement`](test-plan-analyze-placement.md) | Analyze test cases and recommend placement (component repo vs downstream) | :material-close: internal |
| [`/test-plan-review`](test-plan-review.md) | Review test plan with 5-criteria rubric and auto-revision | :material-close: internal |
| [`/test-plan-generate-test-file`](test-plan-generate-test-file.md) | Generate complete test file with all functions, quality scoring and auto-revision | :material-close: internal |
| [`/test-plan-score-test-function`](test-plan-score-test-function.md) | Score generated test function code using 5-criteria quality rubric | :material-close: internal |

## Installation

```bash
/plugin install test-plan@opendatahub-skills
```

## Architecture

The plugin is organized as an orchestrated pipeline of 19 skills, split into
user-invocable commands and internal forked sub-agents:

**User-invocable pipeline stages:**
1. test-plan-create -- generates a test plan from a Jira strategy with 3 parallel analyzers
2. test-plan-create-cases -- generates TC-*.md files from the test plan
3. test-plan-update -- re-analyzes with new documents, merges findings, bumps version
4. test-plan-case-implement -- generates executable test code with placement analysis
5. test-plan-ui-verify -- browser-based UI test execution via Playwright CDP
6. test-plan-publish -- creates/updates GitHub PRs with test plan artifacts
7. test-plan-resolve-feedback -- triages and applies PR review comments
8. test-plan-score -- standalone quality rubric assessment (read-only)

**Internal sub-agents (context: fork):**
- test-plan-analyze-endpoints, test-plan-analyze-risks, test-plan-analyze-infra -- parallel analyzers
- test-plan-merge -- intelligent merge of new findings into existing plans
- test-plan-resolve-gaps -- cross-references gaps with new documentation
- test-plan-analyze-placement -- recommends component vs downstream repo placement
- test-plan-review -- quality scoring + auto-revision loop (max 2 cycles)
- test-plan-generate-test-file -- parallel test file generation sub-agent
- test-plan-score-test-function -- quality scoring for generated test functions

Key architectural patterns:
- Parallel forked sub-agents for analysis and code generation (isolated context, clean return)
- Python scripts for deterministic operations (frontmatter, validation, file mapping, repo utilities)
- MCP integration (Atlassian) for fetching Jira strategies
- Persistent Playwright CDP browser for UI verification with screenshot capture
- odh-test-context integration for repository-specific test conventions
