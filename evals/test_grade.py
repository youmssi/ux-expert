import json
import tempfile
import unittest
from pathlib import Path

import yaml

from grade import EVALS_DIR, benchmark, grade, load_catalogue_ids

FIELDS = "- **Severity:** S3 · **Reach:** R3 · **Priority:** P0\n- **Recommendation:** fix it\n- **Verification:** test it\n"


def finding(n: int, body: str, fields: str = FIELDS) -> str:
    return f"### F-{n:03d} · {body}\n{fields}\n"


class AnswerKeyTest(unittest.TestCase):
    def test_answer_keys_point_to_real_files_and_criteria(self):
        ids, _ = load_catalogue_ids()
        for spec in json.loads((EVALS_DIR / "evals.json").read_text())["evals"]:
            if spec["kind"] != "audit":
                continue
            key = yaml.safe_load((EVALS_DIR / spec["answer_key"]).read_text())
            fixture_files = {p.name for p in (EVALS_DIR / "fixtures" / key["fixture"]).rglob("*") if p.is_file()}
            for item in key["defects"] + key["decoys"]:
                self.assertIn(item["file"], fixture_files, f"{spec['id']} {item['id']}")
                self.assertTrue(set(item["criteria"]) <= ids, f"{spec['id']} {item['id']}: {item['criteria']}")

    def test_fixtures_do_not_reveal_the_answers(self):
        for path in (EVALS_DIR / "fixtures").rglob("*"):
            if path.is_file() and path.name != "answers.yaml":
                text = path.read_text()
                self.assertNotRegex(text, r"(?i)decoy|\b(FORM|A11Y|STATE|AI)-\d{2}\b", str(path))


class GradeAuditTest(unittest.TestCase):
    def test_a_perfect_report_finds_every_defect_and_no_decoy(self):
        key = yaml.safe_load((EVALS_DIR / "fixtures/signup-app/answers.yaml").read_text())
        report = "# Report\n" + "".join(finding(i, f"{d['criteria'][0]} in `{d['file']}`") for i, d in enumerate(key["defects"], 1))
        result = grade("audit-signup-app", report)
        self.assertEqual(result["metrics"]["recall"], 1.0)
        self.assertEqual(result["summary"]["pass_rate"], 1.0)

    def test_a_decoy_reported_as_a_defect_fails_its_assertion(self):
        report = finding(1, "FORM-09 validation timing in LoginForm.tsx")
        result = grade("audit-signup-app", report)
        self.assertEqual(result["metrics"]["false_positives"], ["N01"])
        self.assertFalse(result["assertion_results"][1]["passed"])

    def test_a_defect_needs_both_its_file_and_a_criterion_in_one_finding(self):
        report = finding(1, "FORM-02 placeholders everywhere") + finding(2, "Problems in SignupForm.tsx")
        self.assertEqual(grade("audit-signup-app", report)["metrics"]["found"], [])

    def test_unknown_ids_and_incomplete_findings_are_reported(self):
        report = finding(1, "FORM-99 in SignupForm.tsx", fields="- **Severity:** S2\n")
        metrics = grade("audit-signup-app", report)["metrics"]
        self.assertEqual(metrics["unknown_ids"], ["FORM-99"])
        self.assertEqual(metrics["incomplete_findings"], [1])


class GradeDesignTest(unittest.TestCase):
    def story(self, key: str, n: int) -> str:
        lines = "".join(f"- [ ] behaviour {i} [STATE-0{2 + i % 3}, A11Y-02]\n" for i in range(n))
        return f"#### UX requirements: {key}\n{lines}\n"

    def test_a_complete_design_output_passes(self):
        report = "".join(self.story(k, 6) for k in ("CARE-1", "CARE-2", "CARE-3"))
        report += "[INTERACTIVE STEP] No-show fee?\n## UX Definition of Done\n"
        self.assertEqual(grade("design-clinic-brief", report)["summary"]["pass_rate"], 1.0)

    def test_too_few_criteria_and_missing_decisions_fail(self):
        report = self.story("CARE-1", 2) + self.story("CARE-2", 6) + self.story("CARE-3", 6)
        result = grade("design-clinic-brief", report)
        self.assertEqual(result["metrics"]["criteria_per_story"]["CARE-1"], 2)
        self.assertEqual(result["summary"]["passed"], 2)


class BenchmarkTest(unittest.TestCase):
    def test_benchmark_aggregates_pass_rates_and_delta(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for config, rate in (("with_skill", 0.75), ("without_skill", 0.25)):
                path = root / "audit-signup-app" / config
                path.mkdir(parents=True)
                (path / "grading.json").write_text(json.dumps({"summary": {"pass_rate": rate}}))
            result = benchmark(root)["run_summary"]
            self.assertEqual(result["delta"]["pass_rate"], 0.5)


if __name__ == "__main__":
    unittest.main()
