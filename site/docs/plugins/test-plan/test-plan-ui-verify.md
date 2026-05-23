---
title: test-plan-ui-verify
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-ui-verify

Browser-based UI test execution against live ODH/RHOAI clusters. Uses a two-step
flow: ui_prepare.py (deterministic setup in terminal) followed by Claude Code
execution. Loads TC-*.md files from a GitHub PR or repo folder, executes each via
a persistent Playwright CDP browser, and produces a visual HTML report with
PASS/FAIL/BLOCKED/INCOMPLETE verdicts and highlighted screenshots. Supports upgrade
testing workflow with pre/post phase comparison and regression detection.

**Plugin**: [test-plan](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![test-plan-ui-verify diagram](test-plan-ui-verify.svg)
</div>

## Usage

```bash
python3 scripts/ui_prepare.py --test-plan-pr https://github.com/org/repo/pull/5
python3 scripts/ui_prepare.py --test-plan-pr <url> --tc TC-UI --priority P0
python3 scripts/ui_prepare.py --test-plan-pr <url> --upgrade-phase pre
/test-plan-ui-verify
```
