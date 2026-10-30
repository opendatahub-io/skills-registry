---
title: rfe.speedrun
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.speedrun

Compatibility alias for `/rfe-speedrun`, kept so existing `/rfe.speedrun`
invocations keep working. It runs the layout bootstrap once, then reads its
generic sibling's SKILL.md and follows it from Step 0 with the same
arguments. Prefer `/rfe-speedrun` (Initiatives: `/rfe-speedrun --type
initiative`).

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Run the full RFE pipeline end-to-end — create, auto-fix, and submit — from an idea, Jira key(s), or a batch file.</p>
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
        <li>Runs create, auto-fix, and submit in sequence, persisting IDs and config between phases.</li>
        <li>Verifies completeness and retries missing IDs before submitting.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/fullsend-ai/rfe-creator/blob/c6eb99de1e6c474fbabc9bbcf98d03734dfbefd2/.claude/skills/rfe.speedrun/SKILL.md" title="fullsend-ai/rfe-creator@c6eb99de1e6c474fbabc9bbcf98d03734dfbefd2:.claude/skills/rfe.speedrun/SKILL.md">SKILL.md @ c6eb99d<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Always pass an explicit batch size to auto-fix for reproducibility.</li>
        <li>Never emit a text-only response during pipeline execution, which terminates the CI process.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, Skill</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/c6eb99de1e6c474fbabc9bbcf98d03734dfbefd2/.claude/skills/rfe.speedrun/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe.speedrun/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Usage

```bash
/rfe.speedrun Users need to verify model signatures at serving time
```
