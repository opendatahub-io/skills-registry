<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# security-reviewer

Independent security reviewer that assesses RHOAI strategy documents
against 39 catalog patterns. Runs in isolated forked context as part
of the multi-reviewer consensus process.

**Plugin**: [rhoai-security-reviewer](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![security-reviewer diagram](security-reviewer.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `STRAT_KEY` | :material-check: | — | STRAT key (e.g., RHAISTRAT-400) |
| `--reviewer` | :material-check: | — | Reviewer number (1, 2, or 3) |
| `--threat-surface` | :material-check: | — | Path to threat surface inventory file |
| `--tier` | :material-check: | — | Review depth tier |
