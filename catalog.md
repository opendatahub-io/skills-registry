# Skills and plugins for AI-assisted software engineering workflows, developed by the opendatahub-io team.


Auto-generated from `registry.yaml`. Do not edit directly.

## Quick Start

```bash
# Add this marketplace to Claude Code
claude plugin marketplace add opendatahub-io/skills-registry

# Browse available plugins
/plugin
```

## Evaluation & Testing

Skills for evaluating and testing AI agent skills

### assess-rfe

Assess RFEs against quality criteria using a structured rubric.

v1.0.0 | [n1hility/assess-rfe](https://github.com/n1hility/assess-rfe)

Tags: rfe, rubric, quality, assessment

| Skill | Description |
|-------|-------------|
| `/assess-rfe` | Assess RFEs against quality criteria using a structured rubric |
| `/export-rubric` | Export the assessment rubric |

```bash
/plugin install assess-rfe@opendatahub-skills
```

### test-plan

Generate test plans and test cases from RHOAI strategies using parallel sub-agent analysis and automated review.

v0.1.0 | [fege/test-plan](https://github.com/fege/test-plan)

Tags: test-plan, test-cases, quality, strategy

| Skill | Description |
|-------|-------------|
| `/test-plan.create` | Generate a test plan from a strategy |
| `/test-plan.create-cases` | Generate test case files from a test plan |
| test-plan.analyze.endpoints | Extract scope and API endpoints |
| test-plan.analyze.risks | Determine test levels, priorities, and risks |
| test-plan.analyze.infra | Identify environment and infrastructure needs |
| test-plan.review | Review test plan for completeness |

```bash
/plugin install test-plan@opendatahub-skills
```

## Security Review

Security analysis, threat modeling, and compliance review

### rhoai-security-reviewer

Consensus-based security review for RHOAI strategy documents (STRATs). An orchestrator spawns three independent reviewers to identify security risks, then synthesizes findings with confidence tagging based on cross-reviewer agreement. Covers 39 catalog patterns across auth, data protection, cryptographic compliance, network security, supply chain, and infrastructure.

v0.1.0 | [jctanner/ai-first-pipeline](https://github.com/jctanner/ai-first-pipeline)

Tags: security, review, strat, threat-modeling, fips, compliance, consensus

| Skill | Description |
|-------|-------------|
| `/strat-security-review` | Multi-reviewer consensus orchestrator for security review of STRAT documents. Extracts threat surfaces, spawns three independent security-reviewer instances, synthesizes findings with confidence levels, and produces a final verdict (PASS/CONCERNS/FAIL).
 |
| `/security-reviewer` | Individual security reviewer that assesses RHOAI strategy documents against 39 catalog patterns covering authentication, data protection, cryptographic compliance, network security, supply chain, and infrastructure. Uses a two-phase discovery-then-filter approach with severity classification.
 |

```bash
/plugin install rhoai-security-reviewer@opendatahub-skills
```

## Product Planning

Skills for requirements, RFEs, and product strategy

### rfe-creator

Claude Code skills for creating, reviewing, and submitting RFEs to the RHAIRFE Jira project. Provides an automated pipeline from initial creation through review, splitting, and submission, plus strategy refinement skills.

**Requires:** `assess-rfe`

v0.1.0 | [jwforres/rfe-creator](https://github.com/jwforres/rfe-creator)

Tags: rfe, jira, review, strategy, pipeline

| Skill | Description |
|-------|-------------|
| `/rfe.create` | Generate new RFEs from problem statements |
| `/rfe.review` | Score and improve RFEs with auto-revision |
| `/rfe.split` | Decompose oversized RFEs into appropriately-scoped pieces |
| `/rfe.submit` | Push RFEs to Jira |
| `/rfe.speedrun` | Execute the full RFE pipeline end-to-end |
| `/rfe.auto-fix` | Batch review, revise, and split operations |
| `/strat.create` | Create strategy documents |
| `/strat.refine` | Refine strategy documents |
| `/strat.review` | Review strategy documents |
| `/strat.prioritize` | Prioritize strategy items |
| `/rfe-creator.update-deps` | Update vendored dependencies |
| `/architecture-review` | Architecture review skill |
| `/feasibility-review` | Feasibility review skill |
| `/rfe-feasibility-review` | RFE feasibility review |
| `/scope-review` | Scope review skill |
| `/testability-review` | Testability review skill |

```bash
/plugin install rfe-creator@opendatahub-skills
```
