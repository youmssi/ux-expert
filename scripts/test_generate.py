import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from generate import ROOT, run

SCHEMA = ROOT / "skills" / "ux-expert" / "criteria" / "schema.json"
AREA_MD = "# Demo\n\n## Criteria\n\n<!-- BEGIN GENERATED criteria (demo) -->\n<!-- END GENERATED criteria -->\n\n## Output\n"


def criterion(**overrides):
    item = {"id": "DEMO-01", "name": "Clear labels", "fail_signal": "Unlabeled inputs", "severity": "S2"}
    item.update(overrides)
    return item


class GenerateTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.skill = Path(self._tmp.name)
        (self.skill / "criteria").mkdir()
        (self.skill / "references" / "areas").mkdir(parents=True)
        shutil.copy(SCHEMA, self.skill / "criteria" / "schema.json")
        self.area_md = self.skill / "references" / "areas" / "demo.md"
        self.area_md.write_text(AREA_MD)
        self.write([criterion()])

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, criteria, area="demo", prefix="DEMO"):
        document = {"area": area, "prefix": prefix, "criteria": criteria}
        (self.skill / "criteria" / f"{area}.yaml").write_text(yaml.safe_dump(document, allow_unicode=True))

    def test_tables_are_rendered_between_the_markers_and_then_up_to_date(self):
        self.assertEqual(run(self.skill, check=False), [])
        text = self.area_md.read_text()
        self.assertIn("| DEMO-01 | Clear labels | Unlabeled inputs | S2 |", text)
        self.assertTrue(text.endswith("<!-- END GENERATED criteria -->\n\n## Output\n"))
        self.assertEqual(run(self.skill, check=True), [])

    def test_a_check_column_appears_only_when_a_criterion_has_one(self):
        self.write([criterion(check="Read the form"), criterion(id="DEMO-02")])
        run(self.skill, check=False)
        text = self.area_md.read_text()
        self.assertIn("| ID | Criterion | Check | Fail signal | Default severity |", text)
        self.assertIn("| DEMO-02 | Clear labels | — | Unlabeled inputs | S2 |", text)

    def test_severity_note_and_related_are_rendered_in_the_severity_cell(self):
        self.write([criterion(severity="S2–S3", severity_note="S3 on payment forms", related=["DEMO-02"]), criterion(id="DEMO-02")])
        run(self.skill, check=False)
        self.assertIn("| S2–S3 (S3 on payment forms; → DEMO-02) |", self.area_md.read_text())

    def test_retired_criteria_are_left_out_of_the_table_but_keep_their_id(self):
        self.write([criterion(status="retired"), criterion(id="DEMO-02")])
        run(self.skill, check=False)
        self.assertNotIn("DEMO-01", self.area_md.read_text())
        self.write([criterion(status="retired"), criterion(id="DEMO-01")])
        self.assertIn("duplicate criterion ID DEMO-01", run(self.skill, check=False)[0])

    def test_a_hand_edited_table_fails_the_check_and_names_the_file(self):
        run(self.skill, check=False)
        self.area_md.write_text(self.area_md.read_text().replace("Clear labels", "Edited by hand"))
        problems = run(self.skill, check=True)
        self.assertEqual(len(problems), 1)
        self.assertIn("demo.md: criteria table is out of date", problems[0])

    def test_a_missing_field_is_rejected(self):
        item = criterion()
        del item["fail_signal"]
        self.write([item])
        self.assertIn("'fail_signal' is a required property", run(self.skill, check=True)[0])

    def test_an_unknown_severity_is_rejected(self):
        self.write([criterion(severity="S5")])
        self.assertIn("criteria/0/severity", run(self.skill, check=True)[0])

    def test_a_malformed_id_is_rejected(self):
        self.write([criterion(id="DEMO-1")])
        self.assertIn("criteria/0/id", run(self.skill, check=True)[0])

    def test_a_duplicate_id_across_areas_is_rejected(self):
        (self.skill / "references" / "areas" / "other.md").write_text(AREA_MD.replace("(demo)", "(other)"))
        self.write([criterion(id="DEMO-01")], area="other", prefix="DEMO")
        self.assertIn("duplicate criterion ID DEMO-01, first defined in demo.yaml", " ".join(run(self.skill, check=True)))

    def test_an_id_with_another_area_prefix_is_rejected(self):
        self.write([criterion(id="FORM-01")])
        self.assertIn("does not use the area prefix DEMO", run(self.skill, check=True)[0])

    def test_a_reversed_severity_range_is_rejected(self):
        self.write([criterion(severity="S3–S2")])
        self.assertIn("severity range S3–S2 is reversed", run(self.skill, check=True)[0])

    def test_a_related_target_that_does_not_exist_is_rejected(self):
        self.write([criterion(related=["NOPE"])])
        self.assertIn("relates to unknown 'NOPE'", run(self.skill, check=True)[0])

    def test_an_area_file_without_criteria_is_reported(self):
        run(self.skill, check=False)
        (self.skill / "references" / "areas" / "orphan.md").write_text("# Orphan\n")
        self.assertEqual(run(self.skill, check=True), [f"{self.skill}/references/areas/orphan.md: no criteria/orphan.yaml for this area"])


if __name__ == "__main__":
    unittest.main()
