import tempfile
import unittest
from pathlib import Path

from validate import MAX_SKILL_LINES, validate

SKILL_MD = "---\nname: demo\ndescription: Demo skill.\n---\n\nSee [format](references/format.md).\n"


class ValidateTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.skill = self.root / "skills" / "demo"
        (self.skill / "references").mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(SKILL_MD)
        (self.skill / "references" / "format.md").write_text("# Format\n")

    def tearDown(self):
        self._tmp.cleanup()

    def test_a_valid_skill_has_no_problems(self):
        self.assertEqual(validate(self.root), [])

    def test_a_repository_without_skills_is_reported(self):
        (self.skill / "SKILL.md").unlink()
        self.assertIn("no skill found", validate(self.root)[0])

    def test_a_skill_md_over_the_line_budget_is_reported(self):
        (self.skill / "SKILL.md").write_text(SKILL_MD + "line\n" * MAX_SKILL_LINES)
        self.assertIn("budget is 500", validate(self.root)[0])

    def test_a_broken_link_is_reported(self):
        (self.skill / "references" / "format.md").unlink()
        self.assertIn("missing file", validate(self.root)[0])

    def test_a_link_leaving_the_skill_directory_is_reported(self):
        (self.root / "outside.md").write_text("# Outside\n")
        (self.skill / "SKILL.md").write_text(SKILL_MD + "[out](../../outside.md)\n")
        self.assertIn("leaves the skill directory", validate(self.root)[0])

    def test_external_links_and_anchors_are_ignored(self):
        (self.skill / "SKILL.md").write_text(SKILL_MD + "[w](https://example.com) [a](#modes)\n")
        self.assertEqual(validate(self.root), [])

    def test_link_syntax_inside_code_is_ignored(self):
        (self.skill / "SKILL.md").write_text(SKILL_MD + "Probe: `alt=[\"'](image|icon)`\n\n```\n[x](missing.md)\n```\n")
        self.assertEqual(validate(self.root), [])


if __name__ == "__main__":
    unittest.main()
