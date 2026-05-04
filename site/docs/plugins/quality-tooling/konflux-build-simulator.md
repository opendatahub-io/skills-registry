<!-- Auto-generated from registry.yaml. Do not edit directly. -->


# konflux-build-simulator

Simulates Konflux build environment on PRs to catch build failures before
production. Generates GitHub Actions workflows for hermetic build validation,
Docker checks, FIPS compliance, and operator integration testing.

**Plugin**: [quality-tooling](index.md) | **:material-check: User-invocable**

## Diagram

<div class="diagram-container" markdown>
![konflux-build-simulator diagram](konflux-build-simulator.svg)
</div>

## Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `repository-url` | :material-check: | — | GitHub repository URL to simulate builds for |

## Usage

```
/konflux-build-simulator https://github.com/opendatahub-io/odh-dashboard
/konflux-build-simulator https://github.com/opendatahub-io/kserve
```
