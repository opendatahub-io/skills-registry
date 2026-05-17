import unittest

from scripts.registry_contracts import SkillKey, detect_touched_skills


def build_registry():
    return {
        "name": "example-registry",
        "owner": {"name": "example-org"},
        "plugins": [
            {
                "name": "example-plugin",
                "description": "Example plugin",
                "version": "1.0.0",
                "source": {"type": "github", "repo": "example-org/example-plugin", "ref": "main"},
                "skills": [
                    {
                        "name": "example-skill",
                        "description": "Example skill",
                    },
                    {
                        "name": "example-skill-two",
                        "description": "Second skill",
                    },
                ],
            }
        ],
    }


class TouchDetectionTests(unittest.TestCase):
    def test_detects_skill_change(self):
        before = build_registry()
        after = build_registry()
        after["plugins"][0]["skills"][0]["description"] = "Updated description"

        self.assertEqual(
            [SkillKey("example-plugin", "example-skill")],
            detect_touched_skills(before, after),
        )

    def test_no_touch_when_strict_omitted_vs_explicit_true(self):
        before = build_registry()
        after = build_registry()
        after["plugins"][0]["strict"] = True

        self.assertEqual([], detect_touched_skills(before, after))

    def test_detects_plugin_source_ref_change_for_all_skills(self):
        before = build_registry()
        after = build_registry()
        after["plugins"][0]["source"]["ref"] = "stable"

        self.assertEqual(
            [
                SkillKey("example-plugin", "example-skill"),
                SkillKey("example-plugin", "example-skill-two"),
            ],
            detect_touched_skills(before, after),
        )


if __name__ == "__main__":
    unittest.main()
