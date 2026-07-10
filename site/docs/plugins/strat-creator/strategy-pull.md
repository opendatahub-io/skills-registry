---
title: strategy-pull
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# strategy-pull

Pulls a post-CI RHAISTRAT strategy from Jira into the `local/` workspace so a human
can review and iterate on it. It validates the issue carries a post-CI label
(`strat-creator-rubric-pass` or `strat-creator-needs-attention`), then fetches the
strategy into `local/strat-tasks/` with `workflow: local` frontmatter, the linked RFE
original and comments into `local/strat-originals/`, and the CI review summary and full
review attachment into `local/strat-reviews/`. It summarizes the title, priority, CI
verdict, review highlights, and source RFE, then advises whether to iterate-and-push
or iterate-and-signoff.

**Plugin**: [strat-creator](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Pull a RHAISTRAT issue from Jira into local/ workspace for human review and iteration.</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">retrieve</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>Writes the strategy content to local/strat-tasks/ with correct frontmatter.</li>
        <li>Pulls associated reviews and RFE originals into local/ subdirectories.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--deterministic">deterministic</span>
        <span class="skill-contract__ref-placeholder"></span>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Not</span>
      <ul class="skill-contract__list">
        <li>Do not modify the Jira issue during pull.</li>
        <li>Do not overwrite local files without user confirmation.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Write, Bash, Glob, Grep</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/strat-creator/blob/main/.claude/skills/strategy-pull/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>.claude/skills/strategy-pull/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![strategy-pull diagram](strategy-pull.svg)
</div>

## Arguments

```bash
/strategy-pull <RHAISTRAT-NNNN>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `RHAISTRAT-NNNN` | :material-check: | - | The strategy key to pull (e.g. RHAISTRAT-1520). If omitted the skill asks for one. Only post-CI strategies (with a rubric-pass or needs-attention label) can be pulled. |

## Usage

```bash
/strategy-pull RHAISTRAT-1520
```
