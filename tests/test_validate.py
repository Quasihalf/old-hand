import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.validate import validate_repository


class ValidateRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name) / "old-hand"
        shutil.copytree(
            PROJECT_ROOT,
            self.repo,
            ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"),
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def assert_has_error(self, fragment):
        errors = validate_repository(self.repo)
        self.assertTrue(
            any(fragment in error for error in errors),
            "Expected error containing {!r}; got:\n{}".format(
                fragment, "\n".join(errors)
            ),
        )

    def test_accepts_the_repository(self):
        self.assertEqual([], validate_repository(self.repo))

    def test_rejects_missing_routed_reference(self):
        (self.repo / "skills/old-hand/references/debug-protocol.md").unlink()

        self.assert_has_error(
            "routed reference is missing: references/debug-protocol.md"
        )

    def test_rejects_plugin_metadata_with_the_wrong_name(self):
        manifest_path = self.repo / ".codex-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["name"] = "not-old-hand"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        self.assert_has_error("plugin manifest must set name to 'old-hand'")

    def test_rejects_plugin_default_prompt_over_runtime_limit(self):
        manifest_path = self.repo / ".codex-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["interface"]["defaultPrompt"] = "$old-hand " + "x" * 119
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        self.assert_has_error(
            "plugin manifest interface.defaultPrompt must be at most 128 characters"
        )

    def test_rejects_invalid_eval_schema(self):
        eval_path = self.repo / "evals/evals.json"
        payload = json.loads(eval_path.read_text(encoding="utf-8"))
        del payload["cases"][0]["expect"]["behaviors"]
        eval_path.write_text(json.dumps(payload), encoding="utf-8")

        self.assert_has_error(
            "evals/evals.json cases[0].expect.behaviors must be a non-empty array"
        )

    def test_rejects_forbidden_placeholders(self):
        readme_path = self.repo / "README.md"
        readme_path.write_text(
            readme_path.read_text(encoding="utf-8")
            + "\nT" + "ODO: replace this placeholder\n",
            encoding="utf-8",
        )

        self.assert_has_error("README.md contains forbidden placeholder 'TODO'")

    def test_rejects_invalid_skill_frontmatter_name(self):
        skill_path = self.repo / "skills/old-hand/SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "name: old-hand", "name: Old Hand", 1
            ),
            encoding="utf-8",
        )

        self.assert_has_error("SKILL.md frontmatter must set name to 'old-hand'")

    def test_rejects_missing_creation_trigger(self):
        skill_path = self.repo / "skills/old-hand/SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "a skill, plugin, agent, MCP server,\n  automation, reusable workflow",
                "a reusable artifact",
                1,
            ),
            encoding="utf-8",
        )

        self.assert_has_error(
            "SKILL.md description must explicitly trigger for skill, plugin, "
            "agent, MCP, and workflow creation"
        )

    def test_rejects_creation_coload_rule_that_is_not_front_loaded(self):
        skill_path = self.repo / "skills/old-hand/SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "Always use Old Hand together with skill-creator or "
                "plugin-creator before\n  creating or substantially redesigning",
                "Use Old Hand for mature judgment when creating or "
                "substantially redesigning",
                1,
            ),
            encoding="utf-8",
        )

        self.assert_has_error(
            "SKILL.md description must front-load creator-skill co-loading"
        )

    def test_rejects_late_creation_discovery_trigger(self):
        skill_path = self.repo / "skills/old-hand/SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "before finalizing the initial stack,",
                "after finalizing the initial stack,",
                1,
            ),
            encoding="utf-8",
        )

        self.assert_has_error(
            "SKILL.md description must make old-hand discoverable before "
            "creation design decisions"
        )

    def test_rejects_missing_creation_research_gate(self):
        protocol_path = (
            self.repo / "skills/old-hand/references/research-protocol.md"
        )
        protocol_path.write_text(
            protocol_path.read_text(encoding="utf-8").replace(
                "Research before design, scaffolding, or implementation even "
                "when the user did not ask for research.",
                "Research when the user asks for it.",
                1,
            ),
            encoding="utf-8",
        )

        self.assert_has_error(
            "research protocol must require creation research before design "
            "without an explicit research request"
        )

    def test_rejects_creation_design_before_initial_search(self):
        protocol_path = (
            self.repo / "skills/old-hand/references/research-protocol.md"
        )
        protocol_path.write_text(
            protocol_path.read_text(encoding="utf-8").replace(
                "Before the initial search completes, do not finalize an "
                "implementation stack, architecture, feature scope, benchmark, "
                "or scaffold location, and do not begin design or scaffolding.\n",
                "Finalize the implementation direction before searching.\n",
                1,
            ),
            encoding="utf-8",
        )

        self.assert_has_error(
            "research protocol must prevent finalized design or scaffolding "
            "before the initial search"
        )

    def test_rejects_absolute_plugin_skills_path(self):
        manifest_path = self.repo / ".codex-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["skills"] = "/skills"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        self.assert_has_error("plugin manifest skills must be a relative path")

    def test_rejects_plugin_manifest_that_is_not_an_object(self):
        (self.repo / ".codex-plugin/plugin.json").write_text("[]", encoding="utf-8")

        self.assert_has_error("plugin manifest must be an object")

    def test_rejects_malformed_marketplace_entry_without_raising(self):
        marketplace_path = self.repo / ".agents/plugins/marketplace.json"
        marketplace = json.loads(marketplace_path.read_text(encoding="utf-8"))
        marketplace["plugins"] = [None]
        marketplace_path.write_text(json.dumps(marketplace), encoding="utf-8")

        self.assert_has_error("marketplace plugins[0] must be an object")

    def test_rejects_non_object_eval_expect_without_raising(self):
        eval_path = self.repo / "evals/evals.json"
        payload = json.loads(eval_path.read_text(encoding="utf-8"))
        payload["cases"][0]["expect"] = []
        eval_path.write_text(json.dumps(payload), encoding="utf-8")

        self.assert_has_error("evals/evals.json cases[0].expect must be an object")

    def test_rejects_eval_fixture_without_required_version_fields(self):
        eval_path = self.repo / "evals/evals.json"
        payload = json.loads(eval_path.read_text(encoding="utf-8"))
        del payload["version"]
        case = payload["cases"][0]
        del case["route"]
        del case["expect"]["behaviors"]
        del case["expect"]["avoid"]
        eval_path.write_text(json.dumps(payload), encoding="utf-8")

        errors = validate_repository(self.repo)
        for fragment in (
            "evals/evals.json must set version to '0.2.2'",
            "evals/evals.json cases[0].route must be non-empty",
            "evals/evals.json cases[0].expect.behaviors must be a non-empty array",
            "evals/evals.json cases[0].expect.avoid must be a non-empty array",
        ):
            self.assertTrue(any(fragment in error for error in errors), fragment)

    def test_rejects_trigger_fixture_with_duplicate_id_missing_reason_and_version(self):
        trigger_path = self.repo / "evals/trigger-cases.json"
        payload = json.loads(trigger_path.read_text(encoding="utf-8"))
        del payload["version"]
        payload["cases"][1]["id"] = payload["cases"][0]["id"]
        del payload["cases"][0]["reason"]
        trigger_path.write_text(json.dumps(payload), encoding="utf-8")

        errors = validate_repository(self.repo)
        for fragment in (
            "evals/trigger-cases.json must set version to '0.2.2'",
            "evals/trigger-cases.json cases[1].id must be unique and non-empty",
            "evals/trigger-cases.json cases[0].reason must be non-empty",
        ):
            self.assertTrue(any(fragment in error for error in errors), fragment)

    def test_rejects_empty_trigger_id(self):
        trigger_path = self.repo / "evals/trigger-cases.json"
        payload = json.loads(trigger_path.read_text(encoding="utf-8"))
        payload["cases"][0]["id"] = ""
        trigger_path.write_text(json.dumps(payload), encoding="utf-8")

        self.assert_has_error(
            "evals/trigger-cases.json cases[0].id must be unique and non-empty"
        )

    def test_rejects_plugin_skills_directory_that_is_not_canonical(self):
        manifest_path = self.repo / ".codex-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["skills"] = "./"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        self.assert_has_error("plugin manifest skills must equal './skills/'")

    def test_rejects_plugin_bundle_without_old_hand_skill(self):
        (self.repo / "skills/old-hand/SKILL.md").unlink()

        self.assert_has_error(
            "plugin skills bundle must contain skills/old-hand/SKILL.md"
        )

    def test_rejects_invalid_agent_metadata(self):
        metadata_path = self.repo / "skills/old-hand/agents/openai.yaml"
        metadata = metadata_path.read_text(encoding="utf-8")
        metadata = metadata.replace(
            "allow_implicit_invocation: true",
            "allow_implicit_invocation: false",
        )
        metadata = metadata.replace("$old-hand", "old-hand", 1)
        metadata_path.write_text(metadata, encoding="utf-8")

        errors = validate_repository(self.repo)
        for fragment in (
            "openai.yaml policy.allow_implicit_invocation must be true",
            "openai.yaml interface.default_prompt must mention '$old-hand'",
        ):
            self.assertTrue(any(fragment in error for error in errors), fragment)

    def test_rejects_agent_default_prompt_over_runtime_limit(self):
        metadata_path = self.repo / "skills/old-hand/agents/openai.yaml"
        metadata = metadata_path.read_text(encoding="utf-8")
        metadata = metadata.replace(
            "Use $old-hand with creator skills; research comparable projects "
            "before designing or scaffolding a new engineering artifact.",
            "$old-hand " + "x" * 119,
        )
        metadata_path.write_text(metadata, encoding="utf-8")

        self.assert_has_error(
            "openai.yaml interface.default_prompt must be at most 128 characters"
        )


if __name__ == "__main__":
    unittest.main()
