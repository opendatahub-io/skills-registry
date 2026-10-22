---
title: rfe.split
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.split

Compatibility alias for `/rfe-split`, kept so existing `/rfe.split`
invocations keep working. It runs the layout bootstrap once, then reads its
generic sibling's SKILL.md and follows it from Step 0 with the same
arguments. Prefer `/rfe-split` (Initiatives: `/rfe-split --type
initiative`).

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Decompose an oversized RFE into appropriately right-sized child RFEs that together cover the original scope.</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">transform</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>Decomposes an oversized RFE into right-sized children that cover all of the original scope.</li>
        <li>Reviews the children through rfe.review and archives the parent RFE.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/.claude/skills/rfe.split/SKILL.md" title="fullsend-ai/rfe-creator@43ee4ae3c982ffe927aeaebbdb6723a668c08072:.claude/skills/rfe.split/SKILL.md">SKILL.md @ 43ee4ae<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Preserve full coverage of the original RFE scope across the children.</li>
        <li>Limit right-sizing self-correction to one cycle, and re-split only for right-sizing.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Glob, Bash, Agent, Skill, AskUserQuestion</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/.claude/skills/rfe.split/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe.split/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Usage

```bash
/rfe.split RHAIRFE-1234
```
