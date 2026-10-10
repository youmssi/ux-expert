import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "skills" / "ux-expert" / "scripts"))

from probe import run  # noqa: E402

FILES = {
    "ios/App/SettingsView.swift": 'Text("Settings").font(.system(size: 13))\nImage("hero").onTapGesture { open() }\n',
    "android/app/src/main/java/Settings.kt": 'Text("Save changes", fontSize = with(d) { 14.dp.toSp() })\nModifier.clickable { open() }\n',
    "android/app/src/main/AndroidManifest.xml": "<manifest />\n",
    "lib/settings.dart": "MediaQuery(data: q.copyWith(textScaler: TextScaler.noScaling), child: app)\nIconButton(onPressed: open, icon: x)\n",
    "pubspec.yaml": "name: demo\n",
    "src/Settings.tsx": "<Text allowFontScaling={false}>Save changes</Text>\n<Pressable onPress={close}>\n",
    "package.json": json.dumps({"dependencies": {"react-native": "0.82.0"}}),
    "node_modules/lib/index.js": "<Text allowFontScaling={false}>Vendored</Text>\n",
}


class ProbeTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        for name, text in FILES.items():
            (self.root / name).parent.mkdir(parents=True, exist_ok=True)
            (self.root / name).write_text(text)

    def tearDown(self):
        self._tmp.cleanup()

    def result(self, report, probe_id):
        return next(r for r in report["results"] if r["probe"] == probe_id)

    def test_detects_every_platform_present(self):
        self.assertEqual(run(self.root, None, 20)["platforms"], ["ios", "android", "flutter", "react-native"])

    def test_finds_the_seeded_smells_with_file_and_line(self):
        report = run(self.root, None, 20)
        for probe_id, file, line in [("ios-fixed-font-size", "ios/App/SettingsView.swift", 1),
                                     ("ios-tap-gesture", "ios/App/SettingsView.swift", 2),
                                     ("android-text-size-dp", "android/app/src/main/java/Settings.kt", 1),
                                     ("android-clickable", "android/app/src/main/java/Settings.kt", 2),
                                     ("flutter-text-scaling-off", "lib/settings.dart", 1),
                                     ("rn-font-scaling-off", "src/Settings.tsx", 1)]:
            hits = self.result(report, probe_id)["hits"]
            self.assertEqual([(h["file"], h["line"]) for h in hits], [(file, line)], probe_id)

    def test_skips_dependency_folders(self):
        hits = self.result(run(self.root, ["react-native"], 20), "rn-font-scaling-off")["hits"]
        self.assertFalse(any("node_modules" in h["file"] for h in hits))

    def test_platform_flag_limits_the_run_and_unknown_platforms_fail(self):
        report = run(self.root, ["flutter"], 20)
        self.assertEqual({r["platform"] for r in report["results"]}, {"flutter"})
        with self.assertRaisesRegex(ValueError, "unknown platform"):
            run(self.root, ["symbian"], 20)

    def test_skips_comment_lines(self):
        (self.root / "lib" / "docs.dart").write_text('/// Text("Example")\n// Text("Old")\n * Text("Doc")\n')
        hits = self.result(run(self.root, ["flutter"], 20), "flutter-hardcoded-string")["hits"]
        self.assertEqual(hits, [])

    def test_counts_every_hit_but_lists_at_most_max_hits(self):
        (self.root / "ios" / "More.swift").write_text(".font(.system(size: 12))\n" * 5)
        result = self.result(run(self.root, ["ios"], 2), "ios-fixed-font-size")
        self.assertEqual((result["count"], len(result["hits"])), (6, 2))

    def test_detects_stack_packs_from_dependencies_and_root_files(self):
        (self.root / "package.json").write_text(json.dumps({"dependencies": {"next": "16.0.0", "react": "19.2.0"}}))
        (self.root / "components.json").write_text("{}")
        report = run(self.root, None, 20)
        self.assertEqual([s["id"] for s in report["stacks"]], ["nextjs", "shadcn-ui"])
        self.assertEqual(report["stacks"][0]["read"], "references/stacks/nextjs.md")

    def test_runs_stack_probes_and_the_stack_flag_limits_the_run(self):
        (self.root / "app").mkdir()
        (self.root / "app" / "error.tsx").write_text("<button onClick={() => reset()}>Try again</button>\n")
        (self.root / "app" / "layout.tsx").write_text("export const viewport = {\n  maximumScale: 1,\n}\n")
        report = run(self.root, None, 20, ["nextjs"])
        self.assertEqual(report["platforms"], [])
        self.assertEqual({r["stack"] for r in report["results"]}, {"nextjs"})
        self.assertEqual(self.result(report, "nextjs-error-boundary-reset-only")["hits"][0]["file"], "app/error.tsx")
        self.assertEqual(self.result(report, "nextjs-viewport-zoom-blocked")["hits"][0]["line"], 2)
        with self.assertRaisesRegex(ValueError, "unknown stack"):
            run(self.root, None, 20, ["angular-material"])

    def test_a_web_project_has_no_native_platform(self):
        (self.root / "package.json").write_text(json.dumps({"dependencies": {"react": "19.2.0"}}))
        for name in ("ios", "android", "lib"):
            shutil.rmtree(self.root / name)
        (self.root / "pubspec.yaml").unlink()
        self.assertEqual(run(self.root, None, 20)["platforms"], [])


if __name__ == "__main__":
    unittest.main()
