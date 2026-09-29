---
title: SPIKE-executor
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# SPIKE-executor

Execute RHOAI SPIKE investigations through a 9-step human-in-the-loop
lifecycle. Each step produces artifacts in the artifacts/ directory and
pauses at a breakpoint for explicit user approval before continuing.
Steps: (1) intake, (2) plan generation, (3) Jira preview, (4) Jira
creation, (5) AI research enrichment with hallucination validation,
(6) test plan + pytest suite generation, (7) test execution + rubric
scoring, (8) RFE generation + approval, (9) completion summary. Supports
--skip-tests (no OpenShift) and --skip-jira (no Jira credentials).

**Plugin**: [spike-executor](index.md) | **:material-check: User-invocable**

## Contract

<div class="skill-contract">
  <header class="skill-contract__header">
    <span class="skill-contract__eyebrow">Skill Contract</span>
    <span class="skill-contract__version">canonical-skill-v1</span>
  </header>
  <p class="skill-contract__lede">Guide an engineer through the nine-step RHOAI SPIKE lifecycle for a named project (plan, Jira structure and sync, AI research enrichment and validation, test plan and pytest suite, cluster test run and feasibility scoring, RFE generation, final summary) by running the spike-executor CLI at each step and stopping at each of the skill&#x27;s six breakpoints for human review.</p>
  <section class="skill-contract__section" data-section="01">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Identity</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Functions</span>
      <div class="skill-contract__inline">
        <span class="skill-contract__chip skill-contract__chip--function">orchestrate</span>
        <span class="skill-contract__chip skill-contract__chip--function">generate</span>
      </div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Success</span>
      <ul class="skill-contract__list">
        <li>Each step writes the artifact the skill names for it under artifacts/ (SPIKE-Plan-&lt;project&gt;.md, SPIKE-Jira-Preview-&lt;project&gt;.md, SPIKE-Jira-Tickets-&lt;project&gt;.md and Jira-Links-&lt;project&gt;-spike.md, Research-Findings-&lt;project&gt;.yaml and .md, Research-Prompt-&lt;project&gt;.md, Research-Validation-&lt;project&gt;.md, Dockerfile.ubi-&lt;project&gt;, Test-Plan-&lt;project&gt;.md, test_suite_&lt;project&gt;.py, Test-Results-&lt;project&gt;.yaml, Feasibility-Report-&lt;project&gt;.yaml and .md, RFE-Input-&lt;project&gt;.md, SPIKE-Summary-&lt;project&gt;.md).</li>
        <li>At each of the six breakpoints (plan, Jira structure, research, test plan, test execution, RFE) the artifacts generated for that gate are shown in full and the workflow advances only on the engineer&#x27;s approval phrase; Step 4 (ticket creation) displays the created-tickets table and continues without a gate.</li>
        <li>With cluster tests run, the feasibility decision (GO, PIVOT or NO-GO) follows the computed score and the security gate, and RFE generation is offered only for GO or PIVOT; with --skip-tests, Steps 6 and 7 are skipped, the RFE step runs without a score, and the skipped stages are reported upfront rather than silently omitted.</li>
      </ul>
    </div>
  </section>
  <section class="skill-contract__section" data-section="02">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Optimization Targets</span></h3>
    <div class="skill-contract__metrics">
      <div class="skill-contract__metric">
        <code class="skill-contract__metric-id">task_success</code>
        <span class="skill-contract__measure skill-contract__measure--judge">judge</span>
        <a class="skill-contract__ref" href="https://github.com/IKRedHat/SPIKE-executor/blob/924ec480198b89d42ceb82275938a7859dbf92ff/.claude/skills/SPIKE-executor/SKILL.md" title="IKRedHat/SPIKE-executor@924ec480198b89d42ceb82275938a7859dbf92ff:.claude/skills/SPIKE-executor/SKILL.md">SKILL.md @ 924ec48<span class="skill-contract__ref-arrow" aria-hidden="true">&#x2192;</span></a>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="03">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Invariants</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Must Preserve</span>
      <ul class="skill-contract__list">
        <li>At every breakpoint, display each generated .md artifact&#x27;s complete content with the Read tool, never a summary, an excerpt or a path alone.</li>
        <li>Never proceed past a breakpoint without the engineer&#x27;s explicit approval phrase.</li>
        <li>Report missing Jira credentials or OpenShift access before starting and continue with the steps that remain possible instead of blocking.</li>
        <li>When tests run, any security check scoring 0 blocks GO, and a NO-GO result never offers RFE generation.</li>
      </ul>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Fixed Context</span>
      <div class="skill-contract__code">
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">tools</span><span class="skill-contract__code-val">Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, WebSearch, WebFetch</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">cli</span><span class="skill-contract__code-val">spike-executor, oc</span></div>
      <div class="skill-contract__code-line"><span class="skill-contract__code-key">knowledge</span><span class="skill-contract__code-val">repository_content<span class="skill-contract__privacy">public</span>, task_input<span class="skill-contract__privacy">task_private</span>, tool_output<span class="skill-contract__privacy">task_private</span></span></div>
      </div>
    </div>
  </section>
  <section class="skill-contract__section" data-section="04">
    <h3 class="skill-contract__section-title"><span class="skill-contract__section-name">Traceability</span></h3>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Skill</span>
      <div class="skill-contract__inline"><a class="skill-contract__path" href="https://github.com/IKRedHat/SPIKE-executor/blob/924ec480198b89d42ceb82275938a7859dbf92ff/.claude/skills/SPIKE-executor/SKILL.md"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>.claude/skills/SPIKE-executor/SKILL.md</code></a></div>
    </div>
    <div class="skill-contract__row">
      <span class="skill-contract__field">Supporting</span>
      <ul class="skill-contract__paths">
        <li><a class="skill-contract__path" href="https://github.com/IKRedHat/SPIKE-executor/blob/924ec480198b89d42ceb82275938a7859dbf92ff/templates/spike_plan.md.j2"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>templates/spike_plan.md.j2</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/IKRedHat/SPIKE-executor/blob/924ec480198b89d42ceb82275938a7859dbf92ff/templates/research_findings.md.j2"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>templates/research_findings.md.j2</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/IKRedHat/SPIKE-executor/blob/924ec480198b89d42ceb82275938a7859dbf92ff/templates/test_suites.md.j2"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>templates/test_suites.md.j2</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/IKRedHat/SPIKE-executor/blob/924ec480198b89d42ceb82275938a7859dbf92ff/templates/feasibility_report.md.j2"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>templates/feasibility_report.md.j2</code></a></li>
        <li><a class="skill-contract__path" href="https://github.com/IKRedHat/SPIKE-executor/blob/924ec480198b89d42ceb82275938a7859dbf92ff/templates/rfe_document.md.j2"><span class="skill-contract__ref-arrow" aria-hidden="true">&#x2197;</span><code>templates/rfe_document.md.j2</code></a></li>
      </ul>
    </div>
  </section>
</div>

## Diagram

<div class="diagram-container" markdown>
![SPIKE-executor diagram](SPIKE-executor.svg)
</div>

## Arguments

```bash
/SPIKE-executor <project> [--skip-tests] [--skip-jira]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `project` | :material-check: | - | Name of the project/technology being investigated (e.g., AutoGluon, gRPC). Used as the suffix for all artifact filenames. |
| `--skip-tests` |  | - | Skip cluster tests and scoring (Steps 6-7). For environments without OpenShift access. |
| `--skip-jira` |  | - | Skip Jira sync steps (Steps 3-4, 5b). For testing without Jira credentials. |

## Usage

```bash
/SPIKE-executor AutoGluon
/SPIKE-executor gRPC --skip-tests
/SPIKE-executor my-project --skip-jira
```
