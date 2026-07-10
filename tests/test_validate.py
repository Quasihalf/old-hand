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

    def test_rejects_absolute_plugin_skills_path(self):
        manifest_path = self.repo / ".codex-plugin/plugin.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["skills"] = "/skills"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        self.assert_has_error("plugin manifest skills must be a relative path")


if __name__ == "__main__":
    unittest.main()
