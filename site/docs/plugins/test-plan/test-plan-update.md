---
title: test-plan-update
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# test-plan-update

Update an existing test plan with new documentation (ADR, API specs, design docs).
Re-runs the 3 parallel analyzers with original + new material, uses the merge
sub-agent to intelligently integrate findings while preserving user edits, resolves
gaps, re-runs quality review, and optionally regenerates test cases. Bumps the
version number automatically.

**Plugin**: [test-plan](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Incorporate new design documents into an existing test plan while retaining human edits and tracking unresolved gaps.</p>
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
        <li>Re-analyzes the new documents, merges findings and updates gap accounting and plan version.</li>
        <li>Re-reviews the updated plan and offers test-case regeneration when needed.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/fullsend-ai/test-creator/blob/d13995efb9bdc5b88a2c20e7f864a26fdf9ee9a0/skills/test-plan-update/SKILL.md" title="fullsend-ai/test-creator@d13995efb9bdc5b88a2c20e7f864a26fdf9ee9a0:skills/test-plan-update/SKILL.md">SKILL.md @ d13995e<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Preserve valid user edits when merging new findings.</li>
        <li>Account for remaining gaps as original minus resolved plus new, without inventing resolutions.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">documents</span><span class="skill-contract__code-val">skills/test-plan-update/SKILL.md</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">task_input<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/fullsend-ai/test-creator/blob/d13995efb9bdc5b88a2c20e7f864a26fdf9ee9a0/skills/test-plan-update/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>skills/test-plan-update/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![test-plan-update diagram](test-plan-update.svg)
</div>

## Arguments

```bash
/test-plan-update <SOURCE> <NEW_DOC_PATH> [<NEW_DOC_PATH>...]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `SOURCE` | :material-check: | - | Test plan location: local directory path, GitHub branch URL, or GitHub PR URL |
| `NEW_DOC_PATH` | :material-check: | - | One or more paths to new documentation files (ADR, API spec, design doc) |

## Usage

```bash
/test-plan-update ~/Code/collection-tests/mcp_catalog adr.pdf
/test-plan-update https://github.com/org/repo/pull/42 api-spec.md design.md
```
