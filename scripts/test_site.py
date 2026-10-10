import json
import re
import tempfile
import unittest
from pathlib import Path

from build_site import ROOT, blank_line_before_lists, build

CATALOGUE = json.loads((ROOT / "skills" / "ux-expert" / "criteria" / "catalogue.json").read_text(encoding="utf-8"))


class SiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls._tmp.name) / "site"
        cls.pages = build(cls.out)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def read(self, page):
        return (self.out / page).read_text(encoding="utf-8")

    def test_one_page_per_area_plus_the_fixed_pages(self):
        self.assertEqual(sum(p.startswith("areas/") for p in self.pages), len(CATALOGUE["areas"]))
        self.assertEqual(sum(p.startswith("stacks/") for p in self.pages), len(CATALOGUE["stacks"]))
        for page in ("index.html", "criteria.html", "sources.html", "stability.html", "changelog.html", "areas.html", "stacks.html"):
            self.assertIn(page, self.pages)

    def test_every_criterion_is_listed_with_its_id_as_anchor(self):
        text = self.read("criteria.html")
        self.assertEqual(len(re.findall(r'<tr id="[A-Z0-9]+-\d+"', text)), len(CATALOGUE["criteria"]))

    def test_links_to_rendered_files_stay_on_the_site_and_others_go_to_github(self):
        index = self.read("index.html")
        self.assertIn('href="install.html"', index)
        self.assertIn('href="https://github.com/youmssi/ux-expert/blob/main/skills/ux-expert/SKILL.md"', index)
        for page in self.pages:
            self.assertNotRegex(self.read(page), r'href="(?!https?:)[^"]+\.md[#"]', page)

    def test_source_citations_link_to_their_row(self):
        area = self.read("areas/commerce.html")
        self.assertIn('href="../sources.html#src-eu-price-indication"', area)
        self.assertIn('id="src-eu-price-indication"', self.read("sources.html"))

    def test_internal_links_resolve(self):
        for page in self.pages:
            for target in re.findall(r'href="(?!https?:|#)([^"#]+)', self.read(page)):
                self.assertTrue((self.out / page).parent.joinpath(target).resolve().exists(), f"{page} → {target}")

    def test_lists_after_a_paragraph_line_get_a_blank_line_outside_code(self):
        self.assertEqual(blank_line_before_lists("Principles:\n1. One\n2. Two\n"), "Principles:\n\n1. One\n2. Two\n")
        fenced = "```\nnote:\n- not a list\n```\n"
        self.assertEqual(blank_line_before_lists(fenced), fenced)


if __name__ == "__main__":
    unittest.main()
