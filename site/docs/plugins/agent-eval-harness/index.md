<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# agent-eval-harness

Generic agentic evaluation for skills and agents. Provides end-to-end skills to analyze, test, score, review, and iteratively improve agent skills with MLflow support for experiment tracking, tracing, and reporting. Schema-driven evaluation via eval.yaml with support for inline, LLM-based, and external judges.

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: Antonin Stefanutti
    - **Category**: [Evaluation & Testing](../../categories/evaluation.md)
    - **Repository**: [opendatahub-io/agent-eval-harness](https://github.com/opendatahub-io/agent-eval-harness)
    - **Tags**: evaluation, testing, skills, agents, mlflow, optimization, scoring

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
