import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "ux-expert" / "scripts"))

from contrast import contrast  # noqa: E402


class ContrastTest(unittest.TestCase):
    # Same reference values as the MCP server's tests (mcp/test/logic.test.ts), so both implementations agree.
    def test_known_ratios(self):
        self.assertEqual(contrast("#000", "#fff")["ratio"], 21)
        self.assertEqual(contrast("#6B7280", "#FFFFFF")["ratio"], 4.83)
        self.assertEqual(contrast("#9CA3AF", "#FFFFFF")["ratio"], 2.54)

    def test_large_text_threshold(self):
        self.assertFalse(contrast("#959595", "#fff", 16)["passes"]["text_aa"])
        self.assertTrue(contrast("#959595", "#fff", 24)["passes"]["text_aa"])
        self.assertTrue(contrast("#959595", "#fff", 19, bold=True)["passes"]["text_aa"])

    def test_alpha_colors_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "composite alpha colors"):
            contrast("rgba(0,0,0,.5)", "#fff")


if __name__ == "__main__":
    unittest.main()
