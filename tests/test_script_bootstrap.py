import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATHS = [
    "scripts/generate_site.py",
    "scripts/validate_registry.py",
    "scripts/run_skill_linter.py",
    "scripts/generate_catalog.py",
    "scripts/check_versions.py",
    "scripts/discover_skills.py",
]
POISON_SENTINEL = "poisoned registry_contracts import"


class ScriptBootstrapTests(unittest.TestCase):
    def test_scripts_prefer_repo_root_over_poisoned_pythonpath(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            poison_root = Path(temp_dir)
            poison_scripts = poison_root / "scripts"
            poison_scripts.mkdir()
            (poison_scripts / "__init__.py").write_text("")
            (poison_scripts / "registry_contracts.py").write_text(
                f'raise RuntimeError("{POISON_SENTINEL}")\n'
            )

            env = os.environ.copy()
            env["PYTHONPATH"] = os.pathsep.join([str(poison_root), str(REPO_ROOT)])

            for script_path in SCRIPT_PATHS:
                with self.subTest(script=script_path):
                    result = subprocess.run(
                        [sys.executable, script_path, "--help"],
                        cwd=REPO_ROOT,
                        env=env,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(
                        result.returncode,
                        0,
                        msg=f"{script_path} failed with stderr:\n{result.stderr}",
                    )
                    self.assertNotIn(POISON_SENTINEL, result.stderr)


if __name__ == "__main__":
    unittest.main()
