"""Severity calibration rules from references/severity-and-scoring.md, checked on the real catalogue.

Default severities describe typical impact; these rules make sure every
criterion can reach the level the escalation rules require.
"""

import json
import re
import unittest
from pathlib import Path

CATALOGUE = Path(__file__).resolve().parent.parent / "skills" / "ux-expert" / "criteria" / "catalogue.json"
CRITERIA = json.loads(CATALOGUE.read_text(encoding="utf-8"))["criteria"]
LOST_WORK = re.compile(r"(?i)\b(work|form|progress|data|draft)s? (is )?lost\b")
LEGAL = re.compile(r"(?i)\b(missing legal|legal entity|pre-checked consent|tracking before consent|consent)\b")


def highest_reachable(criterion: dict) -> int:
    """The highest severity the default range or its escalation note allows."""
    levels = [int(s) for s in re.findall(r"S([0-4])", criterion["severity"] + " " + criterion.get("severity_note", ""))]
    return max(levels)


class CalibrationTest(unittest.TestCase):
    def test_wcag_criteria_can_reach_s3_where_accessibility_law_applies(self):
        low = [c["id"] for c in CRITERIA if "wcag22" in c.get("sources", []) and highest_reachable(c) < 3]
        self.assertEqual(low, [], "escalation rule: legal accessibility failures are at least S3")

    def test_lost_user_work_can_reach_s4(self):
        low = [c["id"] for c in CRITERIA if LOST_WORK.search(c["fail_signal"]) and highest_reachable(c) < 4]
        self.assertEqual(low, [], "escalation rule: data loss is always S4")

    def test_legal_and_consent_failures_can_reach_s3(self):
        low = [c["id"] for c in CRITERIA if LEGAL.search(c["fail_signal"]) and highest_reachable(c) < 3]
        self.assertEqual(low, [], "escalation rule: legal or regulatory violations are at least S3")

    def test_s4_stays_rare_by_default(self):
        s4_defaults = [c["id"] for c in CRITERIA if c["severity"] == "S4"]
        self.assertLessEqual(len(s4_defaults) / len(CRITERIA), 0.05, "S4 as a default means every instance blocks; keep it rare")


if __name__ == "__main__":
    unittest.main()
