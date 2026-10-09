import json
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

from generate import ROOT, run

SCHEMA = ROOT / "skills" / "ux-expert" / "criteria" / "schema.json"
SOURCES_SCHEMA = ROOT / "skills" / "ux-expert" / "criteria" / "sources.schema.json"
CRITERIA = ROOT / "skills" / "ux-expert" / "criteria"
SCORING_MD = "<!-- BEGIN GENERATED priority-matrix -->\n<!-- END GENERATED priority-matrix -->\n<!-- BEGIN GENERATED launch-gate -->\n<!-- END GENERATED launch-gate -->\n"
SOURCE = {"id": "spec", "title": "A spec", "status": "primary", "verified_on": "2026-10-09", "verified_against": "repo@abc", "supports": "The 24 px rule."}
AREA_MD = "# Demo\n\n## Criteria\n\n<!-- BEGIN GENERATED criteria (demo) -->\n<!-- END GENERATED criteria -->\n\n## Output\n"
SKILL_MD = "# Skill\n\n<!-- BEGIN GENERATED applicability -->\n<!-- END GENERATED applicability -->\n"
TYPES = ["web-app", "marketing-site", "mobile", "desktop", "cli", "sdk-api", "ai-feature"]


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
        shutil.copy(SOURCES_SCHEMA, self.skill / "criteria" / "sources.schema.json")
        for name in ("scoring.yaml", "scoring.schema.json"):
            shutil.copy(CRITERIA / name, self.skill / "criteria" / name)
        (self.skill / "references" / "severity-and-scoring.md").write_text(SCORING_MD)
        self.write_sources([SOURCE])
        self.area_md = self.skill / "references" / "areas" / "demo.md"
        self.area_md.write_text(AREA_MD)
        (self.skill / "SKILL.md").write_text(SKILL_MD)
        self.write([criterion()])

    def tearDown(self):
        self._tmp.cleanup()

    def write_sources(self, sources):
        (self.skill / "criteria" / "sources.yaml").write_text(yaml.safe_dump({"sources": sources}, allow_unicode=True))

    def write(self, criteria, area="demo", prefix="DEMO", **fields):
        document = {"area": area, "prefix": prefix, "applicability": {t: "run" for t in TYPES} | {"sdk-api": "n/a"},
                    "phases": ["design"], "criteria": criteria} | fields
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
        self.assertIn("demo.md: out of date with criteria/*.yaml", problems[0])

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

    def test_the_skill_matrix_is_rendered_from_applicability(self):
        self.write([criterion()], applicability={t: "run" for t in TYPES} | {"cli": "conditional"}, applicability_note="only for data tools")
        self.assertEqual(run(self.skill, check=False), [])
        text = (self.skill / "SKILL.md").read_text()
        self.assertIn("| `demo.md` (DEMO) | Run | Run | Run | Run | Conditional | Run | Run |", text)
        self.assertIn("- **DEMO**: only for data tools.", text)

    def test_a_conditional_area_without_a_note_is_rejected(self):
        self.write([criterion()], applicability={t: "run" for t in TYPES} | {"cli": "conditional"})
        self.assertIn("needs an applicability_note", run(self.skill, check=True)[0])

    def test_the_catalogue_has_effective_phases_and_product_types(self):
        self.write([criterion(), criterion(id="DEMO-02", phases=["build"], applies_to=["mobile"])])
        run(self.skill, check=False)
        catalogue = json.loads((self.skill / "criteria" / "catalogue.json").read_text())
        first, second = catalogue["criteria"]
        self.assertEqual(first["phases"], ["design"])
        self.assertNotIn("sdk-api", first["applies_to"])
        self.assertEqual((second["phases"], second["applies_to"]), (["build"], ["mobile"]))

    def test_applies_to_a_product_where_the_area_is_not_applicable_is_rejected(self):
        self.write([criterion(applies_to=["sdk-api"])])
        self.assertIn("applies_to ['sdk-api'], where the area is n/a", run(self.skill, check=True)[0])

    def test_a_missing_catalogue_fails_the_check(self):
        run(self.skill, check=False)
        (self.skill / "criteria" / "catalogue.json").unlink()
        self.assertIn("catalogue.json: out of date", run(self.skill, check=True)[0])

    def test_citing_an_unknown_or_retired_criterion_is_reported(self):
        self.write([criterion(), criterion(id="DEMO-02", status="retired")])
        (self.skill / "references" / "guide.md").write_text("Check DEMO-01, DEMO-02 and DEMO-09. UXE-10 is not a criterion.\n")
        problems = run(self.skill, check=False)
        self.assertEqual([p.split(": ", 1)[1] for p in problems],
                         ["cites DEMO-02, which is not an active criterion", "cites DEMO-09, which is not an active criterion"])

    def test_sources_are_rendered_and_attached_to_criteria(self):
        self.write([criterion(sources=["spec"])])
        self.assertEqual(run(self.skill, check=False), [])
        bibliography = (self.skill / "references" / "sources.md").read_text()
        self.assertIn("| `spec` | A spec | primary | 2026-10-09 (repo@abc) | The 24 px rule. |", bibliography)
        catalogue = json.loads((self.skill / "criteria" / "catalogue.json").read_text())
        self.assertEqual(catalogue["criteria"][0]["sources"], ["spec"])
        self.assertEqual(catalogue["sources"][0]["id"], "spec")

    def test_a_criterion_citing_an_unknown_source_is_rejected(self):
        self.write([criterion(sources=["nope"])])
        self.assertIn("DEMO-01 cites unknown source 'nope'", run(self.skill, check=True)[0])

    def test_a_verified_source_without_its_verification_is_rejected(self):
        source = dict(SOURCE)
        del source["verified_against"]
        self.write_sources([source])
        self.assertIn("'verified_against' is a required property", run(self.skill, check=True)[0])

    def test_an_unknown_source_citation_in_text_is_reported(self):
        (self.skill / "references" / "guide.md").write_text("Per [src:spec] and [src:missing]; `[disabled]` is CSS.\n")
        problems = run(self.skill, check=False)
        self.assertEqual([p.split(": ", 1)[1] for p in problems], ["cites [src:missing], which is not in criteria/sources.yaml"])

    def test_scoring_tables_are_rendered_and_in_the_catalogue(self):
        self.assertEqual(run(self.skill, check=False), [])
        text = (self.skill / "references" / "severity-and-scoring.md").read_text()
        self.assertIn("| **S3** | P0 | P1 | P2 |", text)
        self.assertIn("| **No-Go** | Any P0 open", text)
        catalogue = json.loads((self.skill / "criteria" / "catalogue.json").read_text())
        self.assertEqual(catalogue["scoring"]["priority_matrix"]["S2"]["R3"], "P1")

    def test_a_launch_gate_without_a_final_default_is_rejected(self):
        path = self.skill / "criteria" / "scoring.yaml"
        scoring = yaml.safe_load(path.read_text())
        scoring["launch_gate"] = scoring["launch_gate"][:-1]
        path.write_text(yaml.safe_dump(scoring))
        self.assertIn("launch_gate needs exactly one default rule", run(self.skill, check=True)[0])

    def test_an_area_file_without_criteria_is_reported(self):
        run(self.skill, check=False)
        (self.skill / "references" / "areas" / "orphan.md").write_text("# Orphan\n")
        self.assertEqual(run(self.skill, check=True), [f"{self.skill}/references/areas/orphan.md: no criteria/orphan.yaml for this area"])


if __name__ == "__main__":
    unittest.main()
