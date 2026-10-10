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
PROBES = len(CATALOGUE["probes"])
CRITERIA_COUNT = re.compile(r"\b(\d{3}) (?:sourced )?criteria\b")
PROBE_COUNT = re.compile(r"\b(\d{2}) (?:native |code search )?probes\b")
AREA_COUNT = re.compile(r"\b(\d{2}) (?:UX )?areas\b")


class CountsTest(unittest.TestCase):
    def test_counts_in_published_text_match_the_catalogue(self):
        for name in FILES:
            text = (ROOT / name).read_text(encoding="utf-8")
            for found in CRITERIA_COUNT.findall(text):
                self.assertEqual(int(found), CRITERIA, f"{name} says {found} criteria")
            for found in AREA_COUNT.findall(text):
                self.assertEqual(int(found), AREAS, f"{name} says {found} areas")

    def test_native_probe_counts_match_the_catalogue(self):
        for name in ["README.md", "CHANGELOG.md", "docs/backlog/UXE-14-native-probes.md"]:
            for found in PROBE_COUNT.findall((ROOT / name).read_text(encoding="utf-8")):
                self.assertEqual(int(found), PROBES, f"{name} says {found} probes")


if __name__ == "__main__":
    unittest.main()
