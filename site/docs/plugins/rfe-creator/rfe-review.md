---
title: rfe-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe-review

Scores work items against the type's rubric and auto-revises what fails. It
accepts Jira keys (fetched if not already local) or reviews the local
artifacts `/rfe-create` wrote.

It is an orchestrator: it never reads item bodies into its own context, only
frontmatter. For each ID it launches an assess agent plus one agent per
declared review dimension — technical feasibility for RFEs, feasibility
plus strategic alignment for Initiatives — each with its own blocking and
condition rules.
A review agent then merges those results into
`{REVIEWS_DIR}/<ID>-review.md`, and `filter_for_revision.py` selects which
items a revise agent should rewrite.

Revised items are re-assessed from scratch for at most two cycles. Before
each cycle the review and assess results are deleted so progress detection
works, with `preserve_review_state.py` saving and restoring the cumulative
before-scores and revision history across the teardown. An agent that dies
mid-run leaves no output file, so the ID gets an error stub and drops out of
the batch rather than stalling it.

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
        <a class="skill-contract__ref" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/.claude/skills/rfe-review/SKILL.md" title="fullsend-ai/rfe-creator@43ee4ae3c982ffe927aeaebbdb6723a668c08072:.claude/skills/rfe-review/SKILL.md">SKILL.md @ 43ee4ae<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">output_quality</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/.claude/skills/rfe-review/SKILL.md" title="fullsend-ai/rfe-creator@43ee4ae3c982ffe927aeaebbdb6723a668c08072:.claude/skills/rfe-review/SKILL.md">SKILL.md @ 43ee4ae<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
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
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/.claude/skills/rfe-review/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe-review/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/.claude/skills/rfe-review/prompts/fetch-agent.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe-review/prompts/fetch-agent.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/.claude/skills/rfe-review/prompts/assess-agent.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe-review/prompts/assess-agent.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/.claude/skills/rfe-review/prompts/review-agent.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe-review/prompts/review-agent.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/.claude/skills/rfe-review/prompts/revise-agent.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe-review/prompts/revise-agent.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/types/rfe/prompts/review-rules.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/rfe/prompts/review-rules.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/types/rfe/prompts/review-sections.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/rfe/prompts/review-sections.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/types/rfe/prompts/revise-rules.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/rfe/prompts/revise-rules.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/types/rfe/dimensions/feasibility.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/rfe/dimensions/feasibility.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/types/initiative/prompts/review-rules.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/initiative/prompts/review-rules.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/types/initiative/prompts/review-sections.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/initiative/prompts/review-sections.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/types/initiative/prompts/revise-rules.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/initiative/prompts/revise-rules.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/types/initiative/dimensions/feasibility.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/initiative/dimensions/feasibility.md</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/types/initiative/dimensions/alignment.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>types/initiative/dimensions/alignment.md</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![rfe-review diagram](rfe-review.svg)
</div>

## Arguments

```bash
/rfe-review [--type <t>] [--headless] [--caller <name>] <ID> [ID2 ...]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ID` | :material-check: | - | One or more space-separated item IDs — the type's Jira key form or local id form. A key with no local task file is fetched from Jira first. |
| `--type` |  | `rfe` | Work-item type to review. An explicit --type always wins. |
| `--headless` |  | - | Suppress the end-of-run summary and emit a completion marker instead. |
| `--caller` |  | `none` | Identifies the calling skill so a headless run returns to it. /rfe-split passes --caller split. |

## Usage

```bash
/rfe-review RHAIRFE-1595
/rfe-review RHAIRFE-1595 RHAIRFE-1602 RFE-001
/rfe-review --type initiative INIT-001
```
