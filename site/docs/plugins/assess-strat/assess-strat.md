---
title: assess-strat
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# assess-strat

Assess strategies against quality criteria using a structured rubric

**Plugin**: [assess-strat](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Score a strategy against the published rubric and explain the result.</p>
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
        <li>Produces a complete rubric-based assessment for the supplied strategy input.</li>
        <li>Includes evidence-backed scoring rationale for each criterion.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/assess-strat/blob/ae449845b2c8bde238ba7cd6ecd536b2c83f4a8b/skills/assess-strat/SKILL.md" title="opendatahub-io/assess-strat@ae449845b2c8bde238ba7cd6ecd536b2c83f4a8b:skills/assess-strat/SKILL.md">SKILL.md @ ae44984<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>
      </div>
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">evidence_completeness</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/assess-strat/blob/ae449845b2c8bde238ba7cd6ecd536b2c83f4a8b/skills/assess-strat/SKILL.md" title="opendatahub-io/assess-strat@ae449845b2c8bde238ba7cd6ecd536b2c83f4a8b:skills/assess-strat/SKILL.md">SKILL.md @ ae44984<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>
      </div>
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">output_quality</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/assess-strat/blob/ae449845b2c8bde238ba7cd6ecd536b2c83f4a8b/skills/assess-strat/SKILL.md" title="opendatahub-io/assess-strat@ae449845b2c8bde238ba7cd6ecd536b2c83f4a8b:skills/assess-strat/SKILL.md">SKILL.md @ ae44984<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Not</span>
      <ul class="skill-contract__list">
        <li>Do not skip rubric criteria or invent unsupported evidence.</li>
        <li>Do not change the accepted input modes declared by the skill.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Write, Edit, Glob, Grep, Bash, Agent, TaskGet, mcp__atlassian__getJiraIssue, mcp__atlassian__searchJiraIssuesUsingJql</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/assess-strat/blob/main/skills/assess-strat/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/assess-strat/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Usage

```bash
/assess-strat
```
