import tempfile
import unittest
import zipfile
from pathlib import Path

from bundle import AREAS, BUNDLES, SKILL, build
from generate import NOT_AREAS


class BundleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls._tmp.name)
        cls.sizes = build(cls.out)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def read(self, mode):
        return (self.out / "bundles" / f"ux-expert-{mode}.md").read_text(encoding="utf-8")

    def test_one_bundle_per_mode(self):
        self.assertEqual(sorted(self.sizes), sorted(f"ux-expert-{mode}.md" for mode in BUNDLES))

    def test_each_bundle_starts_with_instructions_and_contains_its_files(self):
        for mode, spec in BUNDLES.items():
            text = self.read(mode)
            self.assertTrue(text.startswith(f"# ux-expert "), mode)
            self.assertIn("Instructions for an AI assistant", text)
            for path in spec["files"]:
                self.assertIn(f"<!-- ===== FILE: {path} ===== -->", text, f"{mode}: {path}")

    def test_frontmatter_is_stripped(self):
        self.assertNotIn("\nname: ux-expert\n", self.read("full"))

    def test_the_audit_bundle_has_every_area(self):
        text = self.read("audit")
        self.assertEqual(len(AREAS), len([p for p in (SKILL / "criteria").glob("*.yaml") if p.name not in NOT_AREAS]))
        self.assertTrue(all(f"FILE: {area}" in text for area in AREAS))

    def test_design_bundles_carry_the_design_criteria_table(self):
        for mode in ("design", "full"):
            text = self.read(mode)
            self.assertIn("FILE: criteria (design phase)", text)
            table = text.split("FILE: criteria (design phase)", 1)[1]
            self.assertIn("| FORM-01 | Only necessary fields, asked when needed |", table)
            self.assertNotIn("| FORM-06 |", table, "build-only criteria stay out of the design table")

    def test_the_skill_zip_has_the_skill_under_one_folder(self):
        with zipfile.ZipFile(self.out / "ux-expert-skill.zip") as archive:
            names = archive.namelist()
        self.assertIn("ux-expert/SKILL.md", names)
        self.assertIn("ux-expert/criteria/catalogue.json", names)
        expected = {f"ux-expert/{p.relative_to(SKILL).as_posix()}" for p in SKILL.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
        self.assertEqual(set(names), expected)


if __name__ == "__main__":
    unittest.main()
