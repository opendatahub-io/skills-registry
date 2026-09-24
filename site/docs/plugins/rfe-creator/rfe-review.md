---
title: rfe-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe-review

Review and improve work items of any registered type — RFEs (RHAIRFE) and Initiatives (RHOAIENG, /rfe-review --type initiative). Accepts one or more Jira keys to fetch and review existing items, or reviews local artifacts from /rfe-create. Runs rubric scoring and the type's review dimensions (technical feasibility, strategic alignment), then auto- revises the issues it finds.


**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Score work items of the resolved type against the type&#x27;s rubric, run its review dimensions (technical feasibility; strategic alignment for Initiatives), and auto-revise failing items across up to two re-assessment cycles.</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">review</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>Produces a review file per item with rubric scores, a verdict per review dimension, and a recommendation.</li>
        <li>Auto-revises failing items and re-assesses up to 2 cycles; auto_revised stays true only when the content changed.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/.claude/skills/rfe-review/SKILL.md" title="opendatahub-io/rfe-creator@3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588:.claude/skills/rfe-review/SKILL.md">SKILL.md @ 3242eb2<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">output_quality</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/.claude/skills/rfe-review/SKILL.md" title="opendatahub-io/rfe-creator@3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588:.claude/skills/rfe-review/SKILL.md">SKILL.md @ 3242eb2<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Never read item bodies into orchestrator context — delegate to agents and read only frontmatter.</li>
        <li>Do not exceed 2 re-assessment cycles.</li>
        <li>Launch every agent with the type&#x27;s launch block — the review prompts are the shared skeletons under .claude/skills/rfe-review/prompts/ filled from it.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Glob, Bash, Agent, AskUserQuestion</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/.claude/skills/rfe-review/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe-review/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/.claude/skills/rfe-review/prompts/fetch-agent.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe-review/prompts/fetch-agent.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/.claude/skills/rfe-review/prompts/assess-agent.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe-review/prompts/assess-agent.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/.claude/skills/rfe-review/prompts/review-agent.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe-review/prompts/review-agent.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/.claude/skills/rfe-review/prompts/revise-agent.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe-review/prompts/revise-agent.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/types/rfe/prompts/review-rules.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/rfe/prompts/review-rules.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/types/rfe/prompts/review-sections.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/rfe/prompts/review-sections.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/types/rfe/prompts/revise-rules.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/rfe/prompts/revise-rules.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/types/rfe/dimensions/feasibility.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/rfe/dimensions/feasibility.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/types/initiative/prompts/review-rules.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/initiative/prompts/review-rules.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/types/initiative/prompts/review-sections.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/initiative/prompts/review-sections.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/types/initiative/prompts/revise-rules.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/initiative/prompts/revise-rules.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/types/initiative/dimensions/feasibility.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/initiative/dimensions/feasibility.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/types/initiative/dimensions/alignment.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/initiative/dimensions/alignment.md</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Usage

```bash
/rfe-review
```
