---
title: pf-design-audit
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# pf-design-audit

Design audit -- validate existing code and designs against PatternFly standards

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: UXD Team
    - **License**: MIT
    - **Scope**: Generic
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Tags**: <span class="tag-pill">patternfly</span> <span class="tag-pill">design</span> <span class="tag-pill">audit</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/pf-ai-audit`](pf-ai-audit.md) | Audit AI-powered features against Red Hat's AI design language — transparency notices, iconography, chatbot patterns, color and gradient rules. Use when reviewing chatbots, AI assistants, or generation UIs for brand compliance. | :material-check: |
| [`/pf-color-scan`](pf-color-scan.md) | Find raw color values (hex, rgb, hsl) in code and suggest PatternFly design token replacements. Use when auditing stylesheets for hardcoded colors or enforcing token compliance. | :material-check: |
| [`/pf-css-token-check`](pf-css-token-check.md) | Detect hardcoded color, spacing, typography, border radius and shadow values that have PF token equivalents and suggest the correct design token replacements. Works on CSS, SCSS, CSS-in-JS, and inline styles. Use when auditing stylesheets for hardcoded values, enforcing design token compliance, or refactoring styles to use PatternFly tokens. | :material-check: |
| [`/pf-figma-check`](pf-figma-check.md) | Check Figma designs against PatternFly v6 standards for colors, typography, spacing, and component usage. Use when validating a design before handoff, auditing existing mockups for compliance, or reviewing design token usage. Requires Figma MCP. | :material-check: |
| [`/pf-figma-token-check`](pf-figma-token-check.md) | Audit designs against the PatternFly 6 token architecture and bridge Figma styles to PF semantic tokens. Use when validating token usage, mapping Figma variables to PF tokens, or checking designs for token compliance. | :material-check: |
| [`/pf-icon-finder`](pf-icon-finder.md) | Identify PatternFly icons in design mockups and provide the correct React import statements. Use when implementing a design, verifying icon usage in a prototype, or finding the correct icon imports for React components. | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install pf-design-audit@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `pf-design-audit` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
