---
title: security-reviewer
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# security-reviewer

Independent security reviewer that assesses RHOAI strategy documents against
a 39-pattern risk catalog plus creative exploration. Runs in isolated forked
context (context: fork) on the claude-opus-4-6 model as part of the
multi-reviewer consensus process -- not intended for direct user invocation.

Operates in two phases: Phase A (Discovery) checks every catalog pattern
against the threat surface inventory, recording each as APPLICABLE or
NOT-APPLICABLE, then performs creative exploration for cross-component
attack chains, novel attack surfaces, emergent risks, and unvalidated
assumptions. Phase B (Filter and Classify) applies a relevance gate
requiring specific STRAT text citations and checking existing controls
from architecture context, then assigns severity via a decision tree
(Critical > High > Medium > NFR Gap).

The catalog covers 39 patterns across 10 categories: Authentication &
Authorization (AUTH-01 through AUTH-06), Data Protection (DATA-01 through
DATA-04), Cryptographic Compliance (CRYPTO-01 through CRYPTO-04), Network
& API Security (NET-01 through NET-03), Supply Chain (SUPPLY-01 through
SUPPLY-04), Infrastructure (INFRA-01 through INFRA-03), Multi-Tenant
Isolation (TENANT-01 through TENANT-03), Agentic AI Security (AGENT-01
through AGENT-05), MCP Security (MCP-01 through MCP-04), and Upstream
Component Risk (UPSTREAM-01 through UPSTREAM-04). Also checks RHOAI
organizational constraints (FIPS 140-3, TLS profile compliance, auth
patterns, secret management, namespace-scoped RBAC).

**Plugin**: [rhoai-security-reviewer](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![security-reviewer diagram](security-reviewer.svg)
</div>

## Arguments

```bash
/security-reviewer <STRAT_KEY> --reviewer <N> --threat-surface <path> --tier <tier>
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `STRAT_KEY` | :material-check: | - | RHAISTRAT Jira key (e.g., RHAISTRAT-400) |
| `--reviewer` | :material-check: | - | Reviewer number (1, 2, or 3) identifying this instance in the consensus set |
| `--threat-surface` | :material-check: | - | Path to the threat surface inventory file extracted by the orchestrator |
| `--tier` | :material-check: | - | Review depth tier: light (minimal surface), standard (1-2 hints), or deep (3+ hints, auth+crypto, agentic/MCP) |

## Usage

```bash
/security-reviewer RHAISTRAT-400 --reviewer 1 --threat-surface artifacts/security-reviews/RHAISTRAT-400-threat-surface.md --tier standard
/security-reviewer RHAISTRAT-400 --reviewer 2 --threat-surface artifacts/security-reviews/RHAISTRAT-400-threat-surface.md --tier deep
```
