"""Run pinned skill-linter checks for registry skills touched in git diffs.

Requires Node.js 22+ for skill-linter. Use --staged (pre-commit) or --diff-base
(e.g. CI) for diff-aware selection; see CONTRIBUTING.md.
"""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent
_REPO_ROOT_STR = str(_REPO_ROOT)
sys.path[:] = [entry for entry in sys.path if entry != _REPO_ROOT_STR]
sys.path.insert(0, _REPO_ROOT_STR)

from scripts.registry_contracts import (  # noqa: E402
    GIT_CLONE_TYPES,
    SKILL_LINTER_VERSION,
    SkillKey,
    detect_touched_skills,
    iter_plugins,
    iter_skills,
    load_registry,
    load_registry_from_ref,
    load_staged_registry,
    normalize_git_ref,
    redact_url,
    shallow_clone,
    source_clone_url,
    source_display_name,
)

CACHE_ROOT = Path(".cache/skills-registry/repos")
CONFIG_PATH = Path("config/skill-linter-registry.json")
GIT_COMMAND_TIMEOUT_SECONDS = 120
SKILL_LINTER_TIMEOUT_SECONDS = 300


def run_captured_command(command: list[str], *, cwd: str | None = None,
                         timeout_seconds: int = GIT_COMMAND_TIMEOUT_SECONDS
                         ) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        rendered = shlex.join(command)
        raise RuntimeError(
            f"command timed out after {timeout_seconds}s: {rendered}"
        ) from exc


def build_skill_linter_command(skill_path: Path, config_path: Path) -> list[str]:
    return [
        "npx",
        "--yes",
        "--package",
        f"skill-linter@{SKILL_LINTER_VERSION}",
        "skill-linter",
        "check",
        str(skill_path),
        "--format",
        "json",
        "--config",
        str(config_path.resolve()),
    ]


def _resolve_repo_file(repo_root: Path, relative_path: str) -> Path:
    root = repo_root.resolve()
    rel_path = Path(relative_path)
    if rel_path.is_absolute():
        raise FileNotFoundError(relative_path)

    current = root
    for part in rel_path.parts:
        current = current / part
        if current.is_symlink():
            raise FileNotFoundError(relative_path)

    resolved = (root / rel_path).resolve()
    if not resolved.is_file() or not resolved.is_relative_to(root):
        raise FileNotFoundError(relative_path)
    return resolved


def validate_source_assertions(repo_root: Path, skill_path: str, supporting_paths: list[str]) -> None:
    _resolve_repo_file(repo_root, skill_path)
    for relative_path in supporting_paths:
        _resolve_repo_file(repo_root, relative_path)


def parse_skill_linter_output(stdout: str) -> dict:
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise ValueError("skill-linter returned invalid JSON") from exc
    if not isinstance(payload, dict):
        raise ValueError("skill-linter output must be a JSON object")
    return payload


def skill_linter_dir_from_contract_skill_path(repo_root: Path, skill_path_relative: str) -> Path:
    """Return the skill directory skill-linter should check.

    ``contract.source_assertions.skill_path`` must point at a ``SKILL.md`` file inside
    the plugin repository; linting targets that file's parent directory.
    """
    stripped = skill_path_relative.strip()
    rel_path = Path(stripped)
    if rel_path.name != "SKILL.md":
        raise ValueError(f"skill_path must end with SKILL.md (got path ending in {rel_path.name!r})")

    artifact = _resolve_repo_file(repo_root, stripped)
    return artifact.parent


def interpret_skill_linter_success_stdout(stdout: str) -> tuple[bool, str | None]:
    """Interpret stdout when skill-linter exits 0. Fail-closed when non-empty and not JSON object."""
    trimmed = stdout.strip()
    if not trimmed:
        return True, None

    try:
        report = parse_skill_linter_output(trimmed)
    except ValueError as exc:
        return False, str(exc)

    error_count_raw = report.get("errorCount", 0)
    try:
        error_count = int(error_count_raw)
    except (TypeError, ValueError):
        return False, f"skill-linter output has non-numeric errorCount: {error_count_raw!r}"

    if error_count > 0 or report.get("errors"):
        return False, json.dumps(report, indent=2)
    return True, None


def _select_touched_skill_keys(registry_path: str, staged: bool, diff_base: str | None,
                               current_registry: dict) -> tuple[set[SkillKey], list[str]]:
    if staged:
        try:
            before = load_registry_from_ref("HEAD", path=registry_path)
            after = load_staged_registry(path=registry_path)
        except (subprocess.CalledProcessError, RuntimeError, ValueError):
            return set(), [
                "  Could not read registry.yaml from git (HEAD or staged copy). "
                "Use --staged from a git repository with the registry file staged."
            ]
        return set(detect_touched_skills(before, after)), []

    if diff_base is not None:
        try:
            before = load_registry_from_ref(diff_base, path=registry_path)
        except (subprocess.CalledProcessError, RuntimeError, ValueError):
            return set(), [
                f"  Could not load {registry_path} from git ref {diff_base!r} "
                "(missing ref or path not present at that revision)."
            ]
        return set(detect_touched_skills(before, current_registry)), []

    return set(), []


def _normalize_supporting_paths(source_assertions: dict) -> list[str]:
    raw = source_assertions.get("supporting_paths")
    if raw is None:
        return []
    if not isinstance(raw, list):
        return []
    return [p for p in raw if isinstance(p, str)]


def skill_is_skill_linter_candidate(plugin: dict, skill: dict) -> bool:
    """True when this skill could run pinned skill-linter (before clone / FS checks)."""
    contract = skill.get("contract")
    if not isinstance(contract, dict):
        return False
    assertions = contract.get("source_assertions")
    if not isinstance(assertions, dict):
        return False
    skill_path_raw = assertions.get("skill_path")
    if not isinstance(skill_path_raw, str) or not skill_path_raw.strip():
        return False
    if Path(skill_path_raw.strip()).name != "SKILL.md":
        return False

    source = plugin.get("source") or {}
    if not isinstance(source, dict):
        return False
    source_type = source.get("type")
    if source_type not in GIT_CLONE_TYPES:
        return False
    if source_type == "github":
        repo = source.get("repo")
        if not isinstance(repo, str) or not repo.strip():
            return False
    elif source_type == "git":
        url = source.get("url")
        if not isinstance(url, str) or not url.strip():
            return False

    try:
        normalize_git_ref(source.get("ref", "main"))
    except ValueError:
        return False
    return True


def _cache_destination(repo: str, ref: str) -> Path:
    safe_repo = repo.replace("/", "__")
    safe_ref = ref.replace("/", "_")
    return CACHE_ROOT.resolve() / f"{safe_repo}__{safe_ref}"


def _ensure_repo(source: dict) -> Path:
    clone_url = source_clone_url(source)
    display = source_display_name(source)
    ref = normalize_git_ref(source.get("ref", "main"))
    destination = _cache_destination(display, ref)
    destination.parent.mkdir(parents=True, exist_ok=True)

    if not (destination / ".git").exists():
        result = shallow_clone(clone_url, ref, str(destination),
                               timeout=GIT_COMMAND_TIMEOUT_SECONDS)
        if result.returncode != 0:
            raise RuntimeError(
                f"clone failed for {redact_url(clone_url)}: {redact_url(result.stderr)}".strip()
            )
    else:
        fetch = run_captured_command(
            ["git", "-C", str(destination), "fetch", "--depth", "1", "origin", ref],
            timeout_seconds=GIT_COMMAND_TIMEOUT_SECONDS,
        )
        if fetch.returncode == 0:
            chk = run_captured_command(
                ["git", "-C", str(destination), "checkout", "--detach", "FETCH_HEAD"],
                timeout_seconds=GIT_COMMAND_TIMEOUT_SECONDS,
            )
            if chk.returncode != 0:
                raise RuntimeError(f"checkout FETCH_HEAD failed in cached repo {destination}: {chk.stderr}".strip())
        else:
            # Ref may not exist on fetch-by-name — try detached checkout directly.
            chk = run_captured_command(
                ["git", "-C", str(destination), "fetch", "--depth", "1", "origin"],
                timeout_seconds=GIT_COMMAND_TIMEOUT_SECONDS,
            )
            if chk.returncode != 0:
                raise RuntimeError(f"fetch origin failed for {destination}: {chk.stderr}".strip())
            chk_out = run_captured_command(
                ["git", "-C", str(destination), "checkout", "--detach", ref],
                timeout_seconds=GIT_COMMAND_TIMEOUT_SECONDS,
            )
            if chk_out.returncode != 0:
                raise RuntimeError(
                    f"checkout {ref} failed in cached repo {destination}: {chk_out.stderr}".strip()
                )

    return destination


def _lookup_skill(registry: dict, key: SkillKey) -> tuple[dict | None, dict | None]:
    for plugin in iter_plugins(registry):
        if plugin.get("name") != key.plugin_name:
            continue
        for skill in iter_skills(plugin):
            if skill.get("name") == key.skill_name:
                return plugin, skill
    return None, None


def _run_one_skill(plugin: dict, skill: dict, config_abs: Path) -> int:
    plug_name = plugin.get("name")
    ski_name = skill.get("name")

    contract = skill.get("contract")
    if not isinstance(contract, dict):
        return 0
    source_assertions = contract.get("source_assertions")
    if not isinstance(source_assertions, dict):
        return 0

    skill_path_raw = source_assertions.get("skill_path")
    if not isinstance(skill_path_raw, str) or not skill_path_raw.strip():
        return 0

    source = plugin.get("source") or {}
    if not isinstance(source, dict) or source.get("type") not in GIT_CLONE_TYPES:
        print(
            f"ERROR: Plugin '{plug_name}' skill '{ski_name}' "
            "has contract source_assertions but source type is not cloneable",
            file=sys.stderr,
        )
        return 1

    try:
        source_clone_url(source)
    except (ValueError, KeyError):
        print(
            f"ERROR: Plugin '{plug_name}' has invalid source configuration.",
            file=sys.stderr,
        )
        return 1

    try:
        normalize_git_ref(source.get("ref", "main"))
    except ValueError:
        print(
            f"ERROR: Plugin '{plug_name}' has invalid source.ref.",
            file=sys.stderr,
        )
        return 1

    supporting = _normalize_supporting_paths(source_assertions)

    repo_root = _ensure_repo(source)
    try:
        resolved_skill_dir = skill_linter_dir_from_contract_skill_path(repo_root, skill_path_raw)
    except (ValueError, FileNotFoundError) as exc:
        print(
            f"ERROR: Plugin '{plug_name}' skill '{ski_name}': invalid skill_path: {exc}",
            file=sys.stderr,
        )
        return 1

    validate_source_assertions(
        repo_root,
        skill_path_raw.strip(),
        supporting,
    )

    command = build_skill_linter_command(resolved_skill_dir, config_abs)
    print(f"Running skill-linter for {plug_name}/{ski_name} (source={source_display_name(source)})...")

    proc = run_captured_command(
        command,
        cwd=str(_REPO_ROOT),
        timeout_seconds=SKILL_LINTER_TIMEOUT_SECONDS,
    )

    if proc.returncode != 0:
        err = proc.stderr.strip() or proc.stdout.strip() or "(no output)"
        print(f"skill-linter failed ({proc.returncode}): {err}", file=sys.stderr)
        return 1

    stdout_ok, detail = interpret_skill_linter_success_stdout(proc.stdout)
    if not stdout_ok:
        print(
            "skill-linter exited 0 but the report indicates failure or invalid output:",
            detail,
            sep="\n",
            file=sys.stderr,
        )
        return 1

    print(f"  OK: {plug_name}/{ski_name}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--registry", default="registry.yaml", help="Registry file path")

    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument(
        "--staged",
        action="store_true",
        help="Lint skills touched between HEAD registry and staged registry.yaml",
    )
    scope.add_argument(
        "--diff-base",
        metavar="REF",
        dest="diff_base",
        default=None,
        help="Lint skills touched between REF registry and working-tree registry.yaml",
    )

    args = parser.parse_args()

    registry_path = args.registry
    current = load_registry(registry_path)

    touched, fatal = _select_touched_skill_keys(
        registry_path,
        args.staged,
        args.diff_base,
        current,
    )
    if fatal:
        print("FAIL selecting touched skills:")
        for line in fatal:
            print(line, file=sys.stderr)
        sys.exit(1)

    if not touched:
        print("No touched skills — skipping skill-linter.")
        return

    config_abs = (_REPO_ROOT / CONFIG_PATH).resolve()
    if not config_abs.is_file():
        print(f"ERROR: missing skill-linter config at {config_abs}", file=sys.stderr)
        sys.exit(1)

    lint_jobs: list[tuple[SkillKey, dict, dict]] = []
    for key in sorted(touched):
        plugin, skill = _lookup_skill(current, key)
        if skill is None or plugin is None:
            continue
        if skill_is_skill_linter_candidate(plugin, skill):
            lint_jobs.append((key, plugin, skill))

    if touched and not lint_jobs:
        touched_display = ", ".join(f"{k.plugin_name}/{k.skill_name}" for k in sorted(touched))
        print(
            f"Touched {len(touched)} skill(s): {touched_display}. "
            "None are configured for pinned skill-linter in this workspace "
            "(GitHub plugin source, contract.source_assertions.skill_path to a SKILL.md file, etc.). "
            "Skipping skill-linter runs."
        )
        return

    exit_code = 0
    for key, plugin, skill in lint_jobs:
        try:
            rc = _run_one_skill(plugin, skill, config_abs)
            if rc != 0:
                exit_code = 1
        except (RuntimeError, OSError, FileNotFoundError) as exc:
            print(
                f"ERROR: Plugin '{key.plugin_name}' skill '{key.skill_name}': {exc}",
                file=sys.stderr,
            )
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
