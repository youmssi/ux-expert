"""Published area and criteria counts match the catalogue."""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOGUE = json.loads((ROOT / "skills" / "ux-expert" / "criteria" / "catalogue.json").read_text(encoding="utf-8"))
CRITERIA = len(CATALOGUE["criteria"])
AREAS = len(CATALOGUE["areas"])
FILES = ["README.md", "skills/ux-expert/SKILL.md", "mcp/README.md", "mcp/package.json", "mcp/src/server.ts", ".claude-plugin/marketplace.json"]
CRITERIA_COUNT = re.compile(r"\b(\d{3}) (?:sourced )?criteria\b")
AREA_COUNT = re.compile(r"\b(\d{2}) (?:UX )?areas\b")


class CountsTest(unittest.TestCase):
    def test_counts_in_published_text_match_the_catalogue(self):
        for name in FILES:
            text = (ROOT / name).read_text(encoding="utf-8")
            for found in CRITERIA_COUNT.findall(text):
                self.assertEqual(int(found), CRITERIA, f"{name} says {found} criteria")
            for found in AREA_COUNT.findall(text):
                self.assertEqual(int(found), AREAS, f"{name} says {found} areas")


if __name__ == "__main__":
    unittest.main()
