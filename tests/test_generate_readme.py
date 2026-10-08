import copy
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import generate_readme as generator


def sample_data():
    return {
        "meta": {
            "title": "World Models",
            "subtitle": "中文介绍",
            "subtitle_en": "English introduction",
            "description": "中文说明。",
            "description_en": "English description.",
            "updated": "2026-10-08",
        },
        "categories": [{"id": "driving", "name": "自动驾驶", "name_en": "Autonomous Driving"}],
        "papers": [{
            "title": "Demo: An Interactive Model",
            "short": "Demo",
            "category": "driving",
            "year": 2025,
            "venue": "ICLR 2026 (Oral)",
            "org": "中文机构",
            "org_en": "Example Institute",
            "features": {"action": True, "closedloop": True},
            "links": {"arxiv": "2501.00001", "code": "https://example.org/code"},
            "note": "预测 | 控制，得分 80.2。",
            "note_en": "Prediction | control, scoring 80.2.",
        }],
    }


class BilingualReadmeTests(unittest.TestCase):
    def test_localized_rendering_keeps_research_metadata(self):
        data = sample_data()
        zh = generator.render_readme(data, "zh")
        en = generator.render_readme(data, "en")
        self.assertIn("**简体中文** | [English](README.en.md)", zh)
        self.assertIn("[简体中文](README.md) | **English**", en)
        self.assertIn("中文机构", zh)
        self.assertIn("Example Institute", en)
        self.assertIn(r"Prediction \| control, scoring 80.2.", en)
        self.assertIn("CONTRIBUTING.en.md", en)
        self.assertIn("(#autonomous-driving)", en)
        for content in (zh, en):
            self.assertIn("**Demo**: An Interactive Model", content)
            self.assertIn("ICLR (2025, Oral)", content)
            self.assertIn("🎮 🔁", content)
            self.assertIn("https://arxiv.org/abs/2501.00001", content)
            self.assertIn("2026-10-08", content)
        self.assertEqual(data, sample_data())

    def test_generation_preserves_both_files_if_a_translation_is_missing(self):
        data = sample_data()
        del data["papers"][0]["note_en"]
        with tempfile.TemporaryDirectory() as directory:
            paths = {language: Path(directory) / name for language, name in (("zh", "README.md"), ("en", "README.en.md"))}
            for path in paths.values():
                path.write_text("Existing document", encoding="utf-8")
            with patch.object(generator, "load_data", return_value=data), patch.object(generator, "README_FILES", paths):
                with self.assertRaisesRegex(SystemExit, "note_en.*Demo"):
                    generator.main()
            for path in paths.values():
                self.assertEqual(path.read_text(encoding="utf-8"), "Existing document")

    def test_english_organization_fallback_and_translation_requirements(self):
        data = sample_data()
        del data["papers"][0]["org_en"]
        with self.assertRaisesRegex(ValueError, "org_en.*Demo"):
            generator.render_readme(data, "en")
        data["papers"][0]["org_en"] = "   "
        with self.assertRaisesRegex(ValueError, "org_en.*Demo"):
            generator.render_readme(data, "en")
        del data["papers"][0]["org_en"]
        data["papers"][0]["org"] = "Example Institute"
        self.assertIn("Example Institute", generator.render_readme(data, "en"))
        for field in ("subtitle_en", "description_en"):
            missing = copy.deepcopy(data)
            missing["meta"][field] = ""
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, field):
                generator.render_readme(missing, "en")
        data["papers"][0]["category"] = "unknown"
        with self.assertRaisesRegex(ValueError, "Unknown category"):
            generator.render_readme(data, "zh")

    def test_repository_versions_cover_the_same_papers_links_and_capabilities(self):
        data = generator.load_data()
        zh = generator.render_readme(data, "zh")
        en = generator.render_readme(data, "en")
        rows_zh = [line for line in zh.splitlines() if line.startswith("| **")]
        rows_en = [line for line in en.splitlines() if line.startswith("| **")]
        self.assertEqual(len(rows_zh), len(data["papers"]))
        self.assertEqual(len(rows_zh), len(rows_en))
        for row_zh, row_en in zip(rows_zh, rows_en):
            self.assertEqual(re.findall(r"\]\((https?://[^)]+)\)", row_zh), re.findall(r"\]\((https?://[^)]+)\)", row_en))
            self.assertEqual(re.findall(r"[🎮⚡🔁⏳]", row_zh), re.findall(r"[🎮⚡🔁⏳]", row_en))
            self.assertEqual(row_zh.split(" | ", 2)[:2], row_en.split(" | ", 2)[:2])
        for line in en.splitlines():
            if line != "[简体中文](README.md) | **English**":
                self.assertIsNone(generator.CJK.search(line), line)

    def test_repository_local_links_and_images_exist_and_anchors_resolve(self):
        data = generator.load_data()
        documents = [generator.render_readme(data, language) for language in ("zh", "en")]
        documents += [(generator.ROOT / name).read_text(encoding="utf-8") for name in ("CONTRIBUTING.md", "CONTRIBUTING.en.md")]
        for content in documents:
            anchors = {generator.github_anchor(line[3:]) for line in content.splitlines() if line.startswith("## ")}
            for target in re.findall(r"\]\(([^)]+)\)|src=\"([^\"]+)\"", content):
                link = target[0] or target[1]
                if link.startswith("#"):
                    self.assertIn(link[1:], anchors)
                elif not link.startswith(("https://", "http://")):
                    self.assertTrue((generator.ROOT / link).exists(), link)


if __name__ == "__main__":
    unittest.main()
