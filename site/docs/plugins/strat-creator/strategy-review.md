---
title: strategy-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-review

Adversarially reviews one refined strategy: it produces a review file with numeric
rubric scores and detailed prose. After bootstrapping the `assess-strat` plugin and
fetching architecture context, it spawns a background scorer agent against the rubric,
then runs deterministic scripts to parse results, compute the APPROVE/REVISE/REJECT
verdict (total ≥6 and no zeros → APPROVE; ≥3 and ≤1 zero → REVISE; else REJECT), and
write scores to the review frontmatter with no LLM judgment. It then invokes the four
reviewer skills — feasibility, testability, scope, architecture — in parallel, each in
an isolated `context: fork`, and assembles their prose (plus Agreements/Disagreements)
into the review file. Outside dry-run it posts a summary comment, attaches the full
review, and applies the verdict label to the RHAISTRAT issue.

**Plugin**: [strat-creator](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Score a strategy against the rubric and run independent forked reviewers for detailed adversarial prose.</p>
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
        <li>Produces a review file with numeric scores across all rubric dimensions.</li>
        <li>Runs independent reviewer agents for feasibility, testability, scope, and architecture.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/strat-creator/blob/0e102d4d1c4a2747895c267b637cf8a33d5f93fc/.claude/skills/strategy-review/SKILL.md" title="opendatahub-io/strat-creator@0e102d4d1c4a2747895c267b637cf8a33d5f93fc:.claude/skills/strategy-review/SKILL.md">SKILL.md @ 0e102d4<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>
      </div>
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">output_quality</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/strat-creator/blob/0e102d4d1c4a2747895c267b637cf8a33d5f93fc/.claude/skills/strategy-review/SKILL.md" title="opendatahub-io/strat-creator@0e102d4d1c4a2747895c267b637cf8a33d5f93fc:.claude/skills/strategy-review/SKILL.md">SKILL.md @ 0e102d4<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Not</span>
      <ul class="skill-contract__list">
        <li>Do not skip rubric criteria or invent findings not supported by evidence.</li>
        <li>Do not modify the strategy being reviewed.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Write, Edit, Glob, Grep, Bash, Skill, Agent</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/strat-creator/blob/main/.claude/skills/strategy-review/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>.claude/skills/strategy-review/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![strategy-review diagram](strategy-review.svg)
</div>

## Arguments

```bash
/strategy-review <RHAISTRAT-NNNN> [--dry-run] [--architecture-context <path>]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `RHAISTRAT-NNNN` | :material-check: | - | The strategy key to review (e.g. RHAISTRAT-1531). Exactly one per invocation; the skill errors without it. The strategy must already be refined. |
| `--architecture-context` |  | - | Local path to an architecture-context checkout to use instead of fetching from remote. |
| `--dry-run` |  | - | Skip all Jira writes — save the review comment to a file instead of posting, and skip attachments/labels. |

## Usage

```bash
/strategy-review RHAISTRAT-1531
/strategy-review RHAISTRAT-1531 --dry-run
```
