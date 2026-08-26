import unittest

import scripts.generate_site as generate_site

from tests.registry_contract_fixtures import build_registry_with_contract


class SiteContractRenderingTests(unittest.TestCase):
    def test_skill_page_renders_contract_section(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        skill = plugin["skills"][0]

        page = generate_site.generate_skill_page(skill, plugin, enrichment=None, plugin_dir=None)

        for marker in (
            "## Contract",
            'class="skill-contract"',
            "canonical-skill-v1",
            "Review the artifact.",  # problem_statement rendered as the lede
            'data-section="01"',
            'data-section="02"',
            'data-section="03"',
            'data-section="04"',
            "task_success",
            ">review<",  # function chip
            "skill-contract__measure--judge",
            "example-org/example-plugin@main:docs/review-rubric.md",  # title attr on ref
            "review-rubric.md @ main",  # short ref label
            "Must Preserve",  # invariants.must_preserve label
            "Traceability",
            "skills/example-skill/SKILL.md",
        ):
            self.assertIn(marker, page)
        # Old admonition/bullet markers should not appear
        for old_marker in (
            '!!! info "Skill Contract"',
            "**Problem Statement**",
            "**Success Conditions:**",
            "**Metrics:**",
            "**Must Preserve:**",
            "**Source Assertions:**",
        ):
            self.assertNotIn(old_marker, page)
        idx_contract = page.index("## Contract")
        idx_review = page.index(">review<", idx_contract)
        self.assertGreater(idx_review, idx_contract)

    def test_skill_page_omits_contract_when_contract_is_not_mapping(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        skill = plugin["skills"][0]
        skill["contract"] = None
        page = generate_site.generate_skill_page(skill, plugin, enrichment=None, plugin_dir=None)
        self.assertNotIn("## Contract", page)

        skill["contract"] = ["oops"]
        page = generate_site.generate_skill_page(skill, plugin, enrichment=None, plugin_dir=None)
        self.assertNotIn("## Contract", page)

    def test_plugin_page_renders_contract_summary(self):
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

    def test_plugin_page_skips_non_mapping_contract_summary(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        plugin["contract_summary"] = None
        page = generate_site.generate_plugin_page(plugin, registry, enrichment=None, plugin_dir=None)
        self.assertNotIn("## Contract Summary", page)

        plugin["contract_summary"] = "invalid"
        page = generate_site.generate_plugin_page(plugin, registry, enrichment=None, plugin_dir=None)
        self.assertNotIn("## Contract Summary", page)

    def test_skill_page_can_render_indented_command_examples(self):
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

    def test_append_code_block_indents_all_physical_lines(self):
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

    def test_plugin_page_renders_git_source_link(self):
        registry = build_registry_with_contract()
        plugin = registry["plugins"][0]
        plugin["source"] = {
            "type": "git",
            "url": "https://gitlab.example.com/team/plugin.git",
        }

        page = generate_site.generate_plugin_page(plugin, registry, enrichment=None, plugin_dir=None)

        self.assertIn("gitlab.example.com/team/plugin", page)
        self.assertIn("https://gitlab.example.com/team/plugin", page)
        self.assertNotIn("https://github.com/", page)

    def test_append_code_block_uses_longer_fence_when_needed(self):
        lines = []

        generate_site._append_code_block(  # pylint: disable=protected-access
            lines,
            ["/example-skill ok", "```embedded"],
        )

        self.assertEqual(lines[0], "````bash")
        self.assertEqual(lines[1:3], ["/example-skill ok", "```embedded"])
        self.assertEqual(lines[3], "````")


class SkillCountTests(unittest.TestCase):
    def _registry(self):
        return {
            "plugins": [
                {"name": "bundle", "includes": ["leaf-a", "leaf-b"]},
                {"name": "leaf-a", "skill_count": 10},
                {"name": "leaf-b", "skill_count": 5},
                {"name": "listed", "skills": [{"name": "x"}, {"name": "y"}]},
            ]
        }

    def test_get_skill_count_leaf_uses_skill_count_or_listed(self):
        by_name = generate_site.build_plugin_index(self._registry())
        self.assertEqual(10, generate_site.get_skill_count(by_name["leaf-a"], by_name))
        self.assertEqual(2, generate_site.get_skill_count(by_name["listed"], by_name))

    def test_get_skill_count_bundle_aggregates_members(self):
        by_name = generate_site.build_plugin_index(self._registry())
        self.assertEqual(15, generate_site.get_skill_count(by_name["bundle"], by_name))

    def test_total_skill_count_excludes_bundles(self):
        # 10 (leaf-a) + 5 (leaf-b) + 2 (listed) = 17; the bundle's 15 is NOT added.
        self.assertEqual(17, generate_site.total_skill_count(self._registry()))

    def test_get_skill_count_survives_member_cycle(self):
        # A malformed mutual cycle must not recurse forever (check_bundles
        # rejects it separately); get_skill_count returns 0 for the cycle.
        registry = {"plugins": [
            {"name": "a", "includes": ["b"]},
            {"name": "b", "includes": ["a"]},
        ]}
        by_name = generate_site.build_plugin_index(registry)
        self.assertEqual(0, generate_site.get_skill_count(by_name["a"], by_name))

    def test_get_skill_count_handles_diamond_without_dropping_members(self):
        # A bundles B and C; both bundle the same leaf D. The per-path visited
        # set must not treat the second D as a cycle.
        registry = {"plugins": [
            {"name": "a", "includes": ["b", "c"]},
            {"name": "b", "includes": ["d"]},
            {"name": "c", "includes": ["d"]},
            {"name": "d", "skill_count": 4},
        ]}
        by_name = generate_site.build_plugin_index(registry)
        self.assertEqual(8, generate_site.get_skill_count(by_name["a"], by_name))

    def test_plugin_page_renders_includes_for_bundle(self):
        plugin = {
            "name": "bundle", "description": "A bundle plugin", "version": "0.1.0",
            "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "p"},
            "includes": ["leaf-a", "leaf-b"],
        }
        registry = {"name": "opendatahub-skills", "plugins": [plugin], "categories": {}}
        page = generate_site.generate_plugin_page(
            plugin, registry, enrichment=None, plugin_dir=None)
        self.assertIn("## Includes", page)
        self.assertIn("[`leaf-a`](../leaf-a/index.md)", page)
        self.assertIn("[`leaf-b`](../leaf-b/index.md)", page)

    def test_plugin_page_renders_mcp_servers(self):
        plugin = {
            "name": "pf-mcp", "description": "An MCP plugin", "version": "0.1.0",
            "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "p"},
            "skill_count": 0,
            "mcp_servers": [
                {"name": "patternfly", "description": "Component docs via MCP"},
            ],
        }
        registry = {"name": "opendatahub-skills", "plugins": [plugin], "categories": {}}
        page = generate_site.generate_plugin_page(
            plugin, registry, enrichment=None, plugin_dir=None)
        self.assertIn("## MCP Servers", page)
        self.assertIn("| patternfly | Component docs via MCP |", page)

    def test_llms_txt_and_full_surface_mcp_servers(self):
        import tempfile
        from pathlib import Path
        registry = {
            "name": "opendatahub-skills",
            "categories": {},
            "plugins": [
                {"name": "pf-mcp", "description": "MCP plugin", "version": "0.1.0",
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "p"},
                 "skill_count": 0,
                 "mcp_servers": [{"name": "patternfly", "description": "Docs via MCP"}]},
            ],
        }
        llms = generate_site.generate_llms_txt(registry, "https://example.test")
        self.assertIn("## MCP Servers", llms)
        self.assertIn("[patternfly](https://example.test/plugins/pf-mcp/): Docs via MCP", llms)
        with tempfile.TemporaryDirectory() as d:
            full = generate_site.generate_llms_full_txt(registry, Path(d))
        self.assertIn("### MCP Servers", full)
        self.assertIn("#### patternfly", full)


class VisiblePluginsTests(unittest.TestCase):
    def _registry(self):
        return {
            "name": "opendatahub-skills",
            "categories": {"dev": {"name": "Dev", "description": "d"}},
            "plugins": [
                {"name": "bundle", "description": "A bundle", "version": "0.1.0",
                 "category": "dev", "scope": "generic",
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "p"},
                 "includes": ["m1", "m2"]},
                {"name": "m1", "description": "Member one", "version": "0.1.0",
                 "category": "dev", "scope": "generic", "skill_count": 3,
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "p/m1"}},
                {"name": "m2", "description": "Member two", "version": "0.1.0",
                 "category": "dev", "scope": "generic", "skill_count": 2,
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "p/m2"}},
                {"name": "solo", "description": "Standalone", "version": "0.1.0",
                 "category": "dev", "scope": "generic",
                 "source": {"type": "github", "repo": "o/solo"},
                 "skills": [{"name": "s1"}]},
            ],
        }

    def test_bundle_member_names(self):
        self.assertEqual({"m1", "m2"},
                         generate_site.bundle_member_names(self._registry()))

    def test_visible_plugins_excludes_members(self):
        names = [p["name"] for p in generate_site.visible_plugins(self._registry())]
        self.assertEqual(["bundle", "solo"], names)

    def test_plugins_index_hides_members_shows_bundle(self):
        page = generate_site.generate_plugins_index(self._registry())
        self.assertIn("[bundle](bundle/index.md)", page)
        self.assertIn("2 plugins.", page)
        self.assertNotIn("[m1](m1/index.md)", page)
        self.assertNotIn("[m2](m2/index.md)", page)

    def test_category_page_excludes_members(self):
        by_cat = generate_site.build_category_plugins(self._registry())
        names = [p["name"] for p in by_cat["dev"]]
        self.assertNotIn("m1", names)
        self.assertNotIn("m2", names)
        self.assertIn("bundle", names)

    def test_mkdocs_nav_nests_members_under_bundle(self):
        reg = self._registry()
        yml = generate_site.generate_mkdocs_yml(reg, reg["categories"],
                                                generate_site.build_category_plugins(reg))
        # members are nested under the bundle, not top-level nav entries
        self.assertIn("      - m1: plugins/m1/index.md", yml)
        self.assertIn("    - bundle:", yml)      # bundle IS a top-level group
        self.assertNotIn("    - m1:\n", yml)     # m1 is NOT a top-level group

    def test_mkdocs_nav_nests_member_skill_pages(self):
        # A member that lists its own skills must have those skill pages nested
        # under it, or they would be orphaned from the nav.
        reg = {
            "name": "opendatahub-skills",
            "categories": {"dev": {"name": "Dev", "description": "d"}},
            "plugins": [
                {"name": "bundle", "description": "b", "version": "0.1.0",
                 "category": "dev", "scope": "generic",
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "p"},
                 "includes": ["m1"]},
                {"name": "m1", "description": "m", "version": "0.1.0",
                 "category": "dev", "scope": "generic",
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "p/m1"},
                 "skills": [{"name": "sk1"}]},
            ],
        }
        yml = generate_site.generate_mkdocs_yml(
            reg, reg["categories"], generate_site.build_category_plugins(reg))
        self.assertIn("      - m1:", yml)
        self.assertIn("        - sk1: plugins/m1/sk1.md", yml)

    def test_plugin_page_category_link_guarded_when_no_page(self):
        # A member whose category has no surfaced plugins must not link to a
        # category page that is never generated (would 404); it shows plain text.
        reg = {
            "name": "opendatahub-skills",
            "categories": {"dev": {"name": "Dev", "description": "d"},
                           "lonely": {"name": "Lonely", "description": "d"}},
            "plugins": [
                {"name": "bundle", "description": "b", "version": "0.1.0",
                 "category": "dev", "scope": "generic",
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "p"},
                 "includes": ["m1"]},
                {"name": "m1", "description": "m", "version": "0.1.0",
                 "category": "lonely", "scope": "generic", "skill_count": 1,
                 "source": {"type": "git-subdir", "url": "https://x/y.git", "path": "p/m1"}},
            ],
        }
        m1 = reg["plugins"][1]
        page = generate_site.generate_plugin_page(m1, reg, enrichment=None, plugin_dir=None)
        self.assertIn("**Category**: Lonely", page)
        self.assertNotIn("../../categories/lonely.md", page)
