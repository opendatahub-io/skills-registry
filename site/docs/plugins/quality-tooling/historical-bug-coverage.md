---
title: historical-bug-coverage
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# historical-bug-coverage

Analyzes historical blocking and critical bugs from Jira and determines
what test coverage exists today through deep test inspection with confidence
scoring. Reads matched test files, extracts actual assertions, and calculates
0-100% confidence scores based on entity matches and scenario validation.

Coverage thresholds are strict: COVERED requires 80%+ confidence that a test
explicitly validates the failure scenario, PARTIALLY COVERED is 60-80%, and
GAP is below 60%. Supports granular test levels (unit, mock, component,
integration, E2E upstream/downstream, contract) and auto-categorizes bugs
by type (upgrade, platform-specific, FIPS, performance, security, disconnected).

Generates a standalone HTML report with sortable/filterable tables, SVG charts,
color-coded confidence badges, E2E breakdown by category, and prioritized
recommendations for test gaps. Supports external test repositories for
cross-repo coverage analysis.

**Plugin**: [quality-tooling](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![historical-bug-coverage diagram](historical-bug-coverage.svg)
</div>

## Arguments

```bash
/historical-bug-coverage --jql JQL_QUERY --repo REPO_PATH [--external-tests PATH] [--filter FILTER_ID] [--output PATH]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--jql` | :material-check: | - | JQL query string to fetch bugs from Jira (mutually exclusive with --filter) |
| `--repo` | :material-check: | - | Path to the target repository to analyze for test coverage |
| `--external-tests` |  | - | Path to an external test repository for cross-repo coverage analysis |
| `--filter` |  | - | Saved Jira filter ID (alternative to --jql) |
| `--output` |  | - | Output HTML file path (defaults to {repo-name}-bug-coverage.html) |

## Usage

```bash
/historical-bug-coverage --jql "project = MYPROJECT AND priority in (Blocker, Critical)" --repo /path/to/repo
/historical-bug-coverage --jql "project = MYPROJECT AND component = 'Dashboard'" --repo /path/to/repo --external-tests /path/to/e2e-tests
/historical-bug-coverage --jql "project = MYPROJECT AND created >= -90d" --repo /path/to/repo
```
