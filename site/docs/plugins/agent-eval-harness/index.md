<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# agent-eval-harness

Generic agentic evaluation framework for Claude Code skills. Provides an
end-to-end pipeline to analyze skills, generate test cases, execute evaluations,
review results with human feedback, sync with MLflow, and iteratively optimize
skill quality with regression checks.

The framework is schema-driven via eval.yaml, which defines execution mode,
dataset schemas, output descriptions, judges, models, and thresholds. Supports
inline, LLM-based, and external judges for scoring, with MLflow integration
for experiment tracking and tracing.


!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: Antonin Stefanutti
    - **Category**: [Evaluation & Testing](../../categories/evaluation.md)
    - **Repository**: [opendatahub-io/agent-eval-harness](https://github.com/opendatahub-io/agent-eval-harness)
    - **Tags**: <span class="tag-pill">evaluation</span> <span class="tag-pill">testing</span> <span class="tag-pill">skills</span> <span class="tag-pill">agents</span> <span class="tag-pill">mlflow</span> <span class="tag-pill">optimization</span> <span class="tag-pill">scoring</span>

## Architecture

Seven skills form a linear pipeline with feedback loops: analyze → dataset →
run → review/optimize. eval-run is the hub — it executes skills, runs judges,
and produces summary.yaml consumed by review, optimize, and mlflow. eval-optimize
creates a closed loop by editing SKILL.md and re-running eval-run with regression
checks. eval-mlflow provides bidirectional sync with MLflow for datasets, results,
and feedback.

## Pipeline

<div class="diagram-container" markdown>
![agent-eval-harness pipeline](pipeline.svg)
</div>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/eval-setup`](eval-setup.md) | One-time environment setup for evaluation (dependencies, MLflow, API keys) | :material-check: |
| [`/eval-analyze`](eval-analyze.md) | Deep-read a target skill and generate eval.yaml configuration with dataset schemas and judges | :material-check: |
| [`/eval-dataset`](eval-dataset.md) | Generate realistic test cases from eval.yaml schema (bootstrap, expand, from-traces) | :material-check: |
| [`/eval-run`](eval-run.md) | Execute skill against test cases, collect artifacts, run judges, and detect regressions | :material-check: |
| [`/eval-review`](eval-review.md) | Human-in-the-loop review of scores and outputs with qualitative feedback collection | :material-check: |
| [`/eval-mlflow`](eval-mlflow.md) | Bidirectional MLflow sync for results, datasets, and feedback | :material-check: |
| [`/eval-optimize`](eval-optimize.md) | Automated improvement loop that identifies failures, edits SKILL.md, and re-runs with regression checks | :material-check: |

## Installation

```bash
/plugin install agent-eval-harness@opendatahub-skills
```
