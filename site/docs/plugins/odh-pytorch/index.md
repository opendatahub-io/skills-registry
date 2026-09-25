---
title: odh-pytorch
---

<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# odh-pytorch

PyTorch cross-language analysis with TorchTalk

!!! info "Plugin Details"

    - **Version**: 0.1.0
    - **Author**: opendatahub-io
    - **License**: Apache-2.0
    - **Scope**: Generic
    - **Category**: [Development Tools](../../categories/development-tools.md)
    - **Tags**: <span class="tag-pill">pytorch</span> <span class="tag-pill">torchtalk</span> <span class="tag-pill">mcp</span>

## Skills

| Skill | Description | Invocable |
|-------|-------------|-----------|
| [`/torchtalk-analyzer`](torchtalk-analyzer.md) | Analyze PyTorch internals across Python, C++, and CUDA layers using the TorchTalk MCP server. Use when asked about how PyTorch operators work internally, where functions are implemented, what would break if code is modified, or finding tests for PyTorch operators. | :material-check: |
| [`/torchtalk-setup`](torchtalk-setup.md) | Install and configure TorchTalk MCP server for PyTorch cross-language analysis | :material-check: |
| [`/torchtalk-trace`](torchtalk-trace.md) | Trace a PyTorch function's cross-language binding chain (Python -> C++ -> CUDA) | :material-check: |

## Installation

**Claude Code**

```bash
/plugin install odh-pytorch@opendatahub-skills
```

**OpenAI Codex** — add the marketplace, then enable `odh-pytorch` from the `/plugins` browser:

```bash
codex plugin marketplace add opendatahub-io/skills-registry
```
