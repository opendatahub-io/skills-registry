---
title: rfe-speedrun
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# rfe-speedrun

Runs the whole pipeline end to end — create, auto-fix, submit — from a single
idea, a Jira key, or a YAML batch file, with as little interaction as
possible.

Step 0 resolves the type, cleans `tmp/`, and pins every flag (notably
`batch_size`, which must be a concrete integer) into
`tmp/{STATE_PREFIX}speedrun-config.yaml` so the run is reproducible and
survives compression. It then picks a mode: **A** a `--input` batch YAML,
**B** an existing Jira key (skip create), or **C** a single free-text idea.

Mode A validates the batch with `--strict` before spending any agent budget,
pre-allocates every ID, then fans out one `/rfe-create` agent per entry —
passing each entry's `clarifying_context` verbatim inside a delimited block
as data, never as instructions. Completion is a blocking barrier on the task
files, not agent notifications: the same IDs pending across three exit-3
results means those agents are dead and get relaunched. Phase 2 hands off to
`/rfe-auto-fix` via the Skill tool (Agent would background it and end the
session) and verifies with `check_autofix_complete.py`, retrying the missing
IDs up to three times. Phase 3 submits only the IDs
`collect_recommendations.py` reports as passing.

**Plugin**: [rfe-creator](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Run the full pipeline for the resolved type end-to-end — create, auto-fix, and submit — from an idea, Jira key(s), or a batch file.</p>
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
        <a class="skill-contract__ref" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/.claude/skills/rfe-speedrun/SKILL.md" title="fullsend-ai/rfe-creator@43ee4ae3c982ffe927aeaebbdb6723a668c08072:.claude/skills/rfe-speedrun/SKILL.md">SKILL.md @ 43ee4ae<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
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
        <li>Forward the resolved type to every phase it launches.</li>
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
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/fullsend-ai/rfe-creator/blob/43ee4ae3c982ffe927aeaebbdb6723a668c08072/.claude/skills/rfe-speedrun/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/rfe-speedrun/SKILL.md</code></a></div>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![rfe-speedrun diagram](rfe-speedrun.svg)
</div>

## Arguments

```bash
/rfe-speedrun [--type <t>] [--input <path>] [--headless] [--announce-complete] [--dry-run] [--batch-size N] <idea | Jira key>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `idea or Jira key` |  | - | A free-text idea or objective (mode C), or a single Jira key to process an existing item (mode B). Omit when using --input. |
| `--type` |  | `rfe` | Work-item type for the run. An explicit --type always wins. |
| `--input` |  | - | YAML file of batch entries (prompt, priority, labels, clarifying_context) — mode A. May also be a mapping with type and items keys. |
| `--headless` |  | - | Suppress questions and confirmations, for CI and eval runs. |
| `--announce-complete` |  | - | Print a completion marker when done, for CI and eval harnesses. |
| `--dry-run` |  | - | Skip the Jira writes in the submit phase. |
| `--batch-size` |  | `5` | Batch size forwarded to auto-fix. Always passed explicitly so runs stay reproducible. |

## Usage

```bash
/rfe-speedrun Users need to verify model signatures at serving time
/rfe-speedrun --input batch.yaml --headless --announce-complete
/rfe-speedrun --type initiative --dry-run RHAISTRAT-12345
```
