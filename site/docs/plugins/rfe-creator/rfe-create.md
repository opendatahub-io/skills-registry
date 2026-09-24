---
title: rfe-create
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe-create

Write a new work item of any registered type — an RFE from a problem statement, idea, or need (business needs, WHAT/WHY), or an Initiative from an objective or strategic goal (/rfe-create --type initiative ...). Asks clarifying questions, then produces well-formed items. Use when starting from scratch.


**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Turn a problem statement, idea or objective into a well-formed work item of the resolved type — an RFE describing business needs (WHAT and WHY) by default, an Initiative with --type initiative — sized and ready for review.</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">generate</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>Produces a well-formed item of the resolved type, sized by the type&#x27;s rules (S/M/L/XL from acceptance-criteria count for RFEs).</li>
        <li>Writes the type&#x27;s task file (artifacts/rfe-tasks/RFE-NNN.md, artifacts/initiatives/INIT-NNN.md) with valid frontmatter and rebuilds the index when the type keeps one.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/.claude/skills/rfe-create/SKILL.md" title="opendatahub-io/rfe-creator@3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588:.claude/skills/rfe-create/SKILL.md">SKILL.md @ 3242eb2<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Describe needs and outcomes (WHAT and WHY) only — never prescribe architecture or implementation.</li>
        <li>Use Jira priority values (Blocker/Critical/Major/Normal/Minor), never High/Medium/Low.</li>
        <li>Take every typed literal (template, guidance, dirs, id prefix) from the type registry&#x27;s launch block — never hand-write a typed path.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/.claude/skills/rfe-create/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe-create/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/types/rfe/template.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/rfe/template.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/types/rfe/prompts/create-guidance.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/rfe/prompts/create-guidance.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/types/initiative/template.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/initiative/template.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/3242eb2d1b3bfb76c4683de2f3e7a6f5d670f588/types/initiative/prompts/create-guidance.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/initiative/prompts/create-guidance.md</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Usage

```bash
/rfe-create
```
