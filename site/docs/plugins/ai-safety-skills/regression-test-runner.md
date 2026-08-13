---
title: regression-test-runner
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# regression-test-runner

End-to-end regression testing workflow for TrustyAI/AI Safety components — patches images, runs pytest as on-cluster Jobs, analyzes failures, creates fix PRs, and updates Jira

**Plugin**: [ai-safety-skills](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Run a component&#x27;s regression suite as sequential on-cluster Jobs across pytest tiers, classify failures (product bug / test bug / infra / flaky / environment), optionally fix and PR test bugs, and report structured results to Jira.</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">orchestrate</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>Every tier that has matching tests is run, and results are aggregated across all tiers even when some fail.</li>
        <li>Fix PRs for test bugs are never created without an explicit user checkpoint, and always go through code review before merge.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/sheltoncyril/sheltons-toolkit/blob/cec313e2f38d493acf8c8ad65bddb110903fb70a/skills/regression-test-runner/SKILL.md" title="sheltoncyril/sheltons-toolkit@cec313e2f38d493acf8c8ad65bddb110903fb70a:skills/regression-test-runner/SKILL.md">SKILL.md @ cec313e<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Never auto-transition the Jira ticket to Resolved if any product_bug failures were found.</li>
        <li>Never read the full pytest log into the main agent context — always delegate that to a subagent.</li>
        <li>If more failures exist than the analysis cap, report how many were skipped rather than dropping them silently.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Bash, Read, Write, Grep, Glob, Agent, AskUserQuestion, Skill</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">oc, git, gh, python3, uv</span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/sheltoncyril/sheltons-toolkit/blob/cec313e2f38d493acf8c8ad65bddb110903fb70a/skills/regression-test-runner/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/regression-test-runner/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/sheltoncyril/sheltons-toolkit/blob/cec313e2f38d493acf8c8ad65bddb110903fb70a/skills/regression-test-runner/resources/component-test-map.json"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/regression-test-runner/resources/component-test-map.json</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Usage

```bash
/regression-test-runner
```
