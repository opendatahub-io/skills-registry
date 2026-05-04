<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# python-packaging-license-finder

Deterministically find license information for Python packages
by checking PyPI metadata and Git repository LICENSE files.

**Plugin**: [odh-ai-helpers](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![python-packaging-license-finder diagram](python-packaging-license-finder.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `package_name` | :material-check: | — | Python package name |
| `version` |  | `latest` | Specific package version |

## Usage

```
/python-packaging-license-finder requests
/python-packaging-license-finder django 4.2.0
```
