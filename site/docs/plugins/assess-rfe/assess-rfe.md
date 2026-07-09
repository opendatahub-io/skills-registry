---
title: assess-rfe
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# assess-rfe

Assess RFEs against quality criteria using a structured five-criteria
rubric (WHAT, WHY, HOW, Not a Task, Right-Sized) scored 0-2 each for
a total out of 10. Supports single-input mode (Jira issue key via MCP
or REST API, file path, URL, or raw text) and bulk mode (wildcard
pattern like RHAIRFE-*) with up to 30 concurrent parallel scorer
sub-agents. Bulk mode includes phased execution with preflight checks,
Jira project dump, timestamped run directories with resume support,
queue-based batch dispatching, and CSV result aggregation with summary
statistics (pass/fail rates, score distribution, criteria averages,
what-if analysis, and near-miss identification).

**Plugin**: [assess-rfe](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Score an RFE against the published rubric and explain the result.</p>
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
        <li>Produces a complete rubric-based assessment for the supplied RFE input.</li>
        <li>Includes evidence-backed scoring rationale for each criterion.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/assess-rfe/blob/a7674fef9a0de4107e3416f05aba2d0b8c019025/skills/assess-rfe/scripts/agent_prompt.md" title="opendatahub-io/assess-rfe@a7674fef9a0de4107e3416f05aba2d0b8c019025:skills/assess-rfe/scripts/agent_prompt.md">agent_prompt.md @ a7674fe<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>
      </div>
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">evidence_completeness</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/assess-rfe/blob/a7674fef9a0de4107e3416f05aba2d0b8c019025/skills/assess-rfe/scripts/agent_prompt.md" title="opendatahub-io/assess-rfe@a7674fef9a0de4107e3416f05aba2d0b8c019025:skills/assess-rfe/scripts/agent_prompt.md">agent_prompt.md @ a7674fe<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>
      </div>
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">output_quality</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/opendatahub-io/assess-rfe/blob/a7674fef9a0de4107e3416f05aba2d0b8c019025/skills/assess-rfe/scripts/agent_prompt.md" title="opendatahub-io/assess-rfe@a7674fef9a0de4107e3416f05aba2d0b8c019025:skills/assess-rfe/scripts/agent_prompt.md">agent_prompt.md @ a7674fe<span class="skill-contract__ref-arrow" aria-hidden="true">→</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Not</span>
      <ul class="skill-contract__list">
        <li>Do not skip rubric criteria or invent unsupported evidence.</li>
        <li>Do not change the accepted input modes declared by the skill.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Write, Edit, Glob, Grep, Bash, Agent, TaskGet, mcp__atlassian__getJiraIssue, mcp__atlassian__searchJiraIssuesUsingJql</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">python3</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/opendatahub-io/assess-rfe/blob/main/skills/assess-rfe/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/assess-rfe/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/opendatahub-io/assess-rfe/blob/main/skills/assess-rfe/scripts/agent_prompt.md"><span class="skill-contract__ref-arrow" aria-hidden="true">↗</span><code>skills/assess-rfe/scripts/agent_prompt.md</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![assess-rfe diagram](assess-rfe.svg)
</div>

## Arguments

    /assess-rfe <input>

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `input` | :material-check: | - | The RFE to assess. Accepts multiple formats: a Jira issue key (e.g., RHAIRFE-1234), a file path to a document, a URL, raw pasted text, or a wildcard pattern (e.g., RHAIRFE-*) for bulk assessment of an entire Jira project. |

## Usage

    /assess-rfe RHAIRFE-1234
    /assess-rfe PROJ-99
    /assess-rfe /path/to/document.md
    /assess-rfe https://some-url
    /assess-rfe <paste raw text>
    /assess-rfe RHAIRFE-*
