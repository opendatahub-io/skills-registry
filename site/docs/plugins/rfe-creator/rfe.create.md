---
title: rfe.create
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe.create

Generate new RFEs from a problem statement, idea, or need. Loads the
assess-rfe rubric (bootstrapping it if needed), and unless run headless
asks 2-5 clarifying questions about affected customers, business
justification, the user's problem, size, and success criteria. Produces
well-formed RFEs from a template that describe WHAT and WHY (business
needs), never HOW (implementation) -- it explicitly avoids loading
architecture context so it won't prescribe a solution. Determines each
RFE's t-shirt size from its acceptance-criteria count via the Size Guide
(S: 1-2, M: 3-5, L: 5-8, XL: 8+), allocates IDs atomically (or uses a
pre-assigned `--rfe-id`), writes artifacts with YAML frontmatter via
scripts/frontmatter.py, and rebuilds the index.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Turn a problem statement or idea into well-formed RFEs describing business needs (WHAT and WHY), sized and ready for review.</p>
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
        <li>Produces well-formed RFEs describing business needs, sized S/M/L/XL from acceptance-criteria count.</li>
        <li>Writes artifacts/rfe-tasks/RFE-NNN.md with valid frontmatter and rebuilds the index.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/rfe-creator/blob/c8a2a1edb53654f08bbe67b7aa4382121e22866f/.claude/skills/rfe.create/SKILL.md" title="opendatahub-io/rfe-creator@c8a2a1edb53654f08bbe67b7aa4382121e22866f:.claude/skills/rfe.create/SKILL.md">SKILL.md @ c8a2a1e<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Describe business needs (WHAT and WHY) only — never prescribe architecture or implementation.</li>
        <li>Use Jira priority values (Blocker/Critical/Major/Normal/Minor), never High/Medium/Low.</li>
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
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/c8a2a1edb53654f08bbe67b7aa4382121e22866f/.claude/skills/rfe.create/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe.create/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/rfe-creator/blob/c8a2a1edb53654f08bbe67b7aa4382121e22866f/.claude/skills/rfe.create/rfe-template.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe.create/rfe-template.md</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![rfe.create diagram](rfe.create.svg)
</div>

## Arguments

```bash
/rfe.create <problem-statement> [--headless] [--priority <value>] [--labels <csv>] [--rfe-id <ID>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `problem-statement` | :material-check: | - | The problem statement, idea, or need to turn into RFEs |
| `--headless` |  | - | Skip clarifying questions (Step 2), generate RFEs directly from the input |
| `--priority` |  | `Normal` | Override default priority for created RFEs |
| `--labels` |  | - | Labels to apply to created RFEs |
| `--rfe-id` |  | - | Pre-assigned RFE ID; use this instead of allocating a new one. The placeholder file must already exist. |

## Usage

```bash
/rfe.create Users need better error messages when model serving fails
/rfe.create --headless --priority Critical Fix dashboard latency for large clusters
/rfe.create --headless --rfe-id RFE-003 --labels candidate-3.5 Support GPU sharing
```
