import json
import unittest
from pathlib import Path

QUERIES = json.loads((Path(__file__).resolve().parent / "trigger_queries.json").read_text(encoding="utf-8"))


class TriggerQueriesTest(unittest.TestCase):
    def test_the_set_is_balanced_and_unique(self):
        positives = [q for q in QUERIES if q["should_trigger"]]
        self.assertEqual(len(QUERIES), 20)
        self.assertEqual(len(positives), 10)
        self.assertEqual(len({q["query"] for q in QUERIES}), 20)

    def test_most_positive_queries_do_not_name_the_domain(self):
        # The guide's most useful positives describe the need without saying "UX".
        implicit = [q for q in QUERIES if q["should_trigger"] and "ux" not in q["query"].lower()]
        self.assertGreaterEqual(len(implicit), 7)


if __name__ == "__main__":
    unittest.main()
