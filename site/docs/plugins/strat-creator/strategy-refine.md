---
title: strategy-refine
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-refine

Refines exactly one strategy per invocation — adding the technical approach, affected
components, impacted teams, high-level requirements, dependencies, non-functional
requirements, out-of-scope, acceptance criteria, effort estimate, risks, assumptions,
and open questions using the unified `strat-template.md`. It grounds the *how* in the
platform's architecture context and follows a strict priority chain of HOW inputs:
Staff Engineer / SME Input > architecture-context overlays > removed RFE implementation
context (from source-RFE comments) > generated architecture docs. In revision mode
(a prior review exists) it addresses each reviewer's concerns rather than regenerating
from scratch. It only ever writes the `## Strategy` section, updates frontmatter to
`Refined`, and (outside dry-run) pushes the section to Jira with a provenance label.

**Plugin**: [strat-creator](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Refine a strategy stub into a complete strategy with technical approach, dependencies, impacted teams, and NFRs.</p>
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
        <li>Produces a refined strategy with HOW, dependencies, and NFRs grounded in platform architecture.</li>
        <li>Updates the local strategy artifact with complete frontmatter and structured sections.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/strat-creator/blob/0e102d4d1c4a2747895c267b637cf8a33d5f93fc/.claude/skills/strategy-refine/SKILL.md" title="opendatahub-io/strat-creator@0e102d4d1c4a2747895c267b637cf8a33d5f93fc:.claude/skills/strategy-refine/SKILL.md">SKILL.md @ 0e102d4<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Not</span>
      <ul class="skill-contract__list">
        <li>Do not alter the original RFE scope or acceptance criteria.</li>
        <li>Do not fabricate component names or dependencies not present in the architecture context.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Write, Edit, Glob, Grep, Bash</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/strat-creator/blob/main/.claude/skills/strategy-refine/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>.claude/skills/strategy-refine/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/strat-creator/blob/main/.claude/skills/strategy-refine/strat-template.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>.claude/skills/strategy-refine/strat-template.md</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![strategy-refine diagram](strategy-refine.svg)
</div>

## Arguments

```bash
/strategy-refine <RHAISTRAT-NNNN> [--dry-run] [--architecture-context <path>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `RHAISTRAT-NNNN` | :material-check: | - | The strategy key to refine (e.g. RHAISTRAT-1531 or STRAT-001). Exactly one per invocation; the skill errors without it. |
| `--architecture-context` |  | - | Local path to an architecture-context checkout to link instead of fetching from remote — useful for testing overlay changes locally. |
| `--dry-run` |  | - | Skip all Jira writes (no push, no labels). Reads and local artifact updates still happen. |

## Usage

```bash
/strategy-refine RHAISTRAT-1531
/strategy-refine RHAISTRAT-1531 --dry-run
/strategy-refine RHAISTRAT-1531 --architecture-context ../architecture-context
```
