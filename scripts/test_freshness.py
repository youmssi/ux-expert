import tempfile
import unittest
from datetime import date
from pathlib import Path

import yaml

from check_freshness import STACKS, stale_packs


class FreshnessTest(unittest.TestCase):
    def test_packs_older_than_the_limit_are_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            stacks = Path(tmp) / "skills" / "ux-expert" / "criteria" / "stacks"
            stacks.mkdir(parents=True)
            verified = {"version": "1.x", "repository": "https://github.com/o/r", "commit": "c" * 40, "verified_on": "2026-01-01"}
            (stacks / "old.yaml").write_text(yaml.safe_dump({"verified": verified}))
            self.assertEqual(stale_packs(stacks, date(2026, 6, 1), 183), [])
            problems = stale_packs(stacks, date(2026, 10, 1), 183)
            self.assertEqual(len(problems), 1)
            self.assertIn("verified 273 days ago against https://github.com/o/r@ccccccc", problems[0])

    def test_the_shipped_packs_are_fresh_today(self):
        self.assertEqual(stale_packs(STACKS, date(2026, 10, 10), 183), [])


if __name__ == "__main__":
    unittest.main()
