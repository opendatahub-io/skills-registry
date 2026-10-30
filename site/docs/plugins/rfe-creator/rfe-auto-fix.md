---
title: rfe-auto-fix
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe-auto-fix

Reviews, revises and splits batches of work items non-interactively. It
takes explicit IDs or a JQL query and makes every decision autonomously.

Where `/rfe-review` hand-rolls its polling, auto-fix delegates control to
`scripts/pipeline_state.py` — a 31-phase state machine running `BATCH_START`
→ `FETCH` → `SETUP` → `ASSESS` → `REVIEW` → `REVISE` → `FIXUP`, the
`REASSESS_*` block, `COLLECT`, the `SPLIT_*` block, `BATCH_DONE`,
`ERROR_COLLECT`, `REPORT`, `DONE`. The skill loops on `next-action` and
executes what it returns: `run_script` runs a phase, `launch_wave` launches
the listed background agents with pre-rendered variables, and every wave is
followed by the blocking `wait-for-wave` barrier (exit 3 means re-run it).

In JQL mode `snapshot_fetch.py` fetches only what is new or changed since
the last run, so an idle re-run legitimately processes zero IDs and goes
straight to `done`. The loop must reach `DONE` on its own — the skill body
explicitly tells the model to ignore any impulse to stop early for budget,
and a `Stop` hook re-enters the loop if a turn ends first.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Review, revise, and split batches of work items of the resolved type non-interactively through a pipeline state machine.</p>
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
        <li>Processes every ID through assess, review dimensions, review, revise, re-assess, and split phases until DONE.</li>
        <li>Emits a run report and a counts summary.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/fullsend-ai/rfe-creator/blob/c6eb99de1e6c474fbabc9bbcf98d03734dfbefd2/.claude/skills/rfe-auto-fix/SKILL.md" title="fullsend-ai/rfe-creator@c6eb99de1e6c474fbabc9bbcf98d03734dfbefd2:.claude/skills/rfe-auto-fix/SKILL.md">SKILL.md @ c6eb99d<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>Run the dispatch loop to completion — never exit early or skip batches.</li>
        <li>After launching a wave of agents, the next call must be wait-for-wave.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Glob, Bash, Agent</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/c6eb99de1e6c474fbabc9bbcf98d03734dfbefd2/.claude/skills/rfe-auto-fix/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe-auto-fix/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![rfe-auto-fix diagram](rfe-auto-fix.svg)
</div>

## Arguments

```bash
/rfe-auto-fix [--type <t>] [--jql "<query>"] [--limit N] [--batch-size N] [--data-dir <path>] [--headless] [--announce-complete] [--reprocess] [--random N] [ID ...]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `ID` |  | - | Explicit item IDs to process. Omit when using --jql or --reprocess. |
| `--type` |  | `rfe` | Work-item type to process. An explicit --type always wins; a headless run with no type and no IDs resolves to rfe. |
| `--jql` |  | - | Fetch the batch from Jira by JQL. The query's project is cross-checked against the resolved type's binding. |
| `--limit` |  | - | Cap the number of issues the JQL fetch returns. |
| `--batch-size` |  | `50` | Number of IDs processed per batch. |
| `--data-dir` |  | - | Alternate data directory for the snapshot fetch. |
| `--headless` |  | - | Non-interactive run (the default posture for this skill). |
| `--announce-complete` |  | - | Print a completion marker when the pipeline reaches DONE. |
| `--reprocess` |  | - | Reprocess already-seen issues instead of only new or changed ones. Works with or without --jql. |
| `--random` |  | - | Sample N issues at random from the fetch result. |

## Usage

```bash
/rfe-auto-fix RHAIRFE-1595 RHAIRFE-1602
/rfe-auto-fix --jql "project = RHAIRFE AND status = New" --limit 20
/rfe-auto-fix --type initiative --reprocess --batch-size 10
```
