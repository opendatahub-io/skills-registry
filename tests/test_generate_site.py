import unittest

import scripts.generate_site as generate_site

from tests.registry_contract_fixtures import build_registry_with_contract


class SiteContractRenderingTests(unittest.TestCase):
    def test_skill_page_renders(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        skill = plugin["skills"][0]

        page = generate_site.generate_skill_page(skill, plugin, enrichment=None, plugin_dir=None)

        for marker in (
            "## Contract",
            '!!! info "Skill Contract"',
            "canonical-skill-v1",
            "task_success",
            "`review`",
            "**Problem Statement**",
            "**Success Conditions:**",
            "**Metrics:**",
            "`judge`",
            "example-org/example-plugin@main:docs/review-rubric.md",
            "**Must Preserve:**",
            "**Source Assertions:**",
            "skills/example-skill/SKILL.md",
        ):
            self.assertIn(marker, page)
        for old_heading in ("### Problem Statement", "### Metrics"):
            self.assertNotIn(old_heading, page)
        idx_contract = page.index("## Contract")
        idx_review = page.index("`review`", idx_contract)
        self.assertGreater(idx_review, idx_contract)

    def test_skill_page_omits_contract_when_contract_is(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        skill = plugin["skills"][0]
        skill["contract"] = None
        page = generate_site.generate_skill_page(skill, plugin, enrichment=None, plugin_dir=None)
        self.assertNotIn("## Contract", page)

        skill["contract"] = ["oops"]
        page = generate_site.generate_skill_page(skill, plugin, enrichment=None, plugin_dir=None)
        self.assertNotIn("## Contract", page)

    def test_plugin_page_renders(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        plugin["contract_summary"] = {
            "focus_functions": ["review"],
            "focus_metrics": ["task_success"],
            "notes": "Example summary",
        }

        page = generate_site.generate_plugin_page(plugin, registry, enrichment=None, plugin_dir=None)

        self.assertIn("## Contract Summary", page)
        self.assertIn("Example summary", page)

    def test_plugin_page_skips_non_mapping(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        plugin["contract_summary"] = None
        page = generate_site.generate_plugin_page(plugin, registry, enrichment=None, plugin_dir=None)
        self.assertNotIn("## Contract Summary", page)

        plugin["contract_summary"] = "invalid"
        page = generate_site.generate_plugin_page(plugin, registry, enrichment=None, plugin_dir=None)
        self.assertNotIn("## Contract Summary", page)

    def test_skill_page_can_render_indented(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        skill = plugin["skills"][0]
        enrichment = {
            "skills": {
                "example-skill": {
                    "code_block_style": "indented",
                    "arguments": [
                        {
                            "name": "input",
                            "required": True,
                            "description": "Input to review.",
                        }
                    ],
                    "usage_examples": [
                        "/example-skill foo",
                        "/example-skill bar",
                    ],
                }
            }
        }

        page = generate_site.generate_skill_page(
            skill, plugin, enrichment=enrichment, plugin_dir=None
        )

        self.assertIn("## Arguments", page)
        self.assertIn("    /example-skill <input>", page)
        self.assertIn("## Usage", page)
        self.assertIn("    /example-skill foo", page)
        self.assertIn("    /example-skill bar", page)
        self.assertNotIn("```bash", page)

    def test_append_code_block_indents_all(self):
        lines = []

        generate_site._append_code_block(  # pylint: disable=protected-access
            lines,
            ["/example-skill ok\n<script>alert(1)</script>"],
            style="indented",
        )

        self.assertEqual(
            lines,
            [
                "    /example-skill ok",
                "    <script>alert(1)</script>",
            ],
        )

    def test_append_code_block_uses_longer_fence(self):
        lines = []

        generate_site._append_code_block(  # pylint: disable=protected-access
            lines,
            ["/example-skill ok", "```embedded"],
        )

        self.assertEqual(lines[0], "````bash")
        self.assertEqual(lines[1:3], ["/example-skill ok", "```embedded"])
        self.assertEqual(lines[3], "````")
