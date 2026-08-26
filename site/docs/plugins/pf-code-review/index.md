---
title: pf-code-review
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# pf-code-review

Code review and quality -- adversarial review, security patterns

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: UXD Team
    - **License**: MIT
    - **Scope**: Generic
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Tags**: <span class="tag-pill">patternfly</span> <span class="tag-pill">code-review</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/pf-review`](pf-review.md) | Run all PatternFly compliance checks on a project — imports, components, colors, legacy CSS, and security. Use when auditing PF code, before merging PRs, or for comprehensive compliance review. | :material-check: |
| [`/pf-security-scan`](pf-security-scan.md) | Scan PatternFly React code for security anti-patterns — XSS via dangerouslySetInnerHTML, unsanitized user input in tooltips/labels, and insecure href patterns. Use when reviewing PF code for security vulnerabilities or auditing user-controlled content in PF components. | :material-check: |

## Installation

```bash
/plugin install pf-code-review@opendatahub-skills
```
