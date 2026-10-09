import contextlib
import io
import json
import sys
import unittest
from pathlib import Path

SKILL_SCRIPTS = Path(__file__).resolve().parent.parent / "skills" / "ux-expert" / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from select_criteria import CATALOGUE, main, select  # noqa: E402

CATALOGUE_DATA = json.loads(CATALOGUE.read_text(encoding="utf-8"))


def run_cli(*args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        main(list(args))
    return out.getvalue()


class SelectCriteriaTest(unittest.TestCase):
    def test_design_selection_only_contains_design_criteria_for_the_product(self):
        selected = select(CATALOGUE_DATA, "web-app", "design", [])
        self.assertTrue(selected)
        self.assertTrue(all("design" in c["phases"] and "web-app" in c["applies_to"] for c in selected))

    def test_build_only_criteria_are_left_out_of_design(self):
        ids = {c["id"] for c in select(CATALOGUE_DATA, "web-app", "design", [])}
        self.assertNotIn("FORM-06", ids)  # autocomplete tokens: build only
        self.assertIn("FORM-01", ids)  # only necessary fields: design

    def test_criteria_narrowed_to_other_products_are_left_out(self):
        ids = {c["id"] for c in select(CATALOGUE_DATA, "web-app", None, [])}
        self.assertNotIn("RESP-12", ids)  # iOS conventions: mobile only
        self.assertIn("RESP-12", {c["id"] for c in select(CATALOGUE_DATA, "mobile", None, [])})

    def test_areas_not_applicable_to_a_product_are_left_out(self):
        areas = {c["area"] for c in select(CATALOGUE_DATA, "sdk-api", None, [])}
        self.assertNotIn("typography", areas)
        self.assertIn("developer-experience", areas)

    def test_area_filter_limits_the_selection(self):
        selected = select(CATALOGUE_DATA, "mobile", "build", ["forms-input"])
        self.assertTrue(selected)
        self.assertEqual({c["area"] for c in selected}, {"forms-input"})

    def test_an_unknown_area_is_rejected_with_the_known_ones(self):
        with self.assertRaisesRegex(ValueError, "unknown area\\(s\\): forms; known: accessibility"):
            select(CATALOGUE_DATA, "web-app", None, ["forms"])

    def test_markdown_output_groups_by_area_and_counts(self):
        output = run_cli("--product", "web-app", "--phase", "design", "--area", "forms-input")
        self.assertTrue(output.startswith("## forms-input (FORM): run for web-app\n- **FORM-01**"))
        self.assertRegex(output, r"\n\d+ criteria\.\n$")

    def test_conditional_areas_show_when_they_apply(self):
        output = run_cli("--product", "web-app", "--area", "ai-interfaces")
        self.assertIn("conditional for web-app; run when the product contains an AI", output)

    def test_json_output_is_a_list_of_criteria(self):
        data = json.loads(run_cli("--product", "cli", "--area", "developer-experience", "--format", "json"))
        self.assertIn("DX-14", {c["id"] for c in data})


if __name__ == "__main__":
    unittest.main()
