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

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Execute UI test cases against a prepared live browser session and produce evidence-backed verification reports.</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">verify</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>Records case actions, assertions and screenshots with the session test log.</li>
        <li>Produces Markdown and HTML reports with the documented PASS, BLOCKED, INCOMPLETE and FAIL verdicts.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/fullsend-ai/test-creator/blob/d13995efb9bdc5b88a2c20e7f864a26fdf9ee9a0/skills/test-plan-ui-verify/instructions.md" title="fullsend-ai/test-creator@d13995efb9bdc5b88a2c20e7f864a26fdf9ee9a0:skills/test-plan-ui-verify/instructions.md">instructions.md @ d13995e<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Use verdict precedence FAIL, INCOMPLETE, BLOCKED, PASS; a case without UI steps is BLOCKED.</li>
        <li>Keep inspection mode read-only and separate from official verification results; enforce retry and no-progress limits.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">documents</span><span class="skill-contract__code-val">skills/test-plan-ui-verify/SKILL.md, skills/test-plan-ui-verify/instructions.md</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">task_input<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/fullsend-ai/test-creator/blob/d13995efb9bdc5b88a2c20e7f864a26fdf9ee9a0/skills/test-plan-ui-verify/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/test-plan-ui-verify/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/test-creator/blob/d13995efb9bdc5b88a2c20e7f864a26fdf9ee9a0/skills/test-plan-ui-verify/instructions.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/test-plan-ui-verify/instructions.md</code></a></li>
      </ul>
    </div>
  </section>
</div>

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
