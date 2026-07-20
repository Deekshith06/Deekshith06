from __future__ import annotations

import datetime as dt
import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


fetch = load_module("fetch_contributions", "fetch_contributions.py")
render = load_module("render_heatmap_svg", "render_heatmap_svg.py")
info = load_module("make_info_card", "make_info_card.py")


class ContributionTests(unittest.TestCase):
    def setUp(self):
        self.days = [
            {"date": "2026-01-01", "count": 1},
            {"date": "2026-01-02", "count": 2},
            {"date": "2026-01-03", "count": 0},
            {"date": "2026-01-04", "count": 3},
            {"date": "2026-01-05", "count": 4},
            {"date": "2026-01-06", "count": 5},
        ]

    def test_build_data_uses_configured_username(self):
        data = fetch.build_data(self.days)
        self.assertEqual(data["username"], "Deekshith06")
        self.assertEqual(data["total_contributions"], 15)
        self.assertEqual(data["active_days"], 5)
        self.assertEqual(data["longest_streak"]["length"], 3)
        self.assertEqual(data["best_day"], {"date": "2026-01-06", "count": 5})

    def test_stale_snapshot_has_no_current_streak(self):
        length, start, end = fetch.compute_current_streak(self.days)
        self.assertEqual((length, start, end), (0, None, None))

    def test_grid_places_sunday_in_row_zero(self):
        normalized = render.validate_data({"days": self.days})
        grid, start_sunday = render.build_grid(normalized)
        self.assertEqual(start_sunday.weekday(), 6)
        sunday = dt.date(2026, 1, 4)
        offset = (sunday - start_sunday).days
        column, row = divmod(offset, 7)
        self.assertEqual(row, 0)
        self.assertEqual(grid[column][row]["date"], sunday)

    def test_svg_contains_accessibility_and_verified_identity(self):
        data = fetch.build_data(self.days)
        svg = render.render(data)
        self.assertIn('role="img"', svg)
        self.assertIn("Deekshith06", svg)
        self.assertIn("15 public contributions", svg)
        self.assertNotIn("9365", svg)


class ProfileCardTests(unittest.TestCase):
    def test_education_is_correct_and_fake_history_removed(self):
        svg = info.build_svg()
        self.assertIn("Lovely Professional University", svg)
        self.assertIn("Expected 2027", svg)
        self.assertIn("AI/ML Engineer · Full-Stack Developer", svg)
        self.assertIn("AI/ML Engineer and Full-Stack Developer", svg)
        self.assertIn("fully working websites", svg)
        self.assertIn('width="760" height="720"', svg)
        self.assertNotIn("IIIT Delhi", svg)
        self.assertNotIn("Dock.us", svg)
        self.assertNotIn("Turgon AI", svg)
        self.assertNotIn("AccioJob", svg)


class PortraitAssetTests(unittest.TestCase):
    def test_readme_uses_equal_non_gif_one_time_portrait(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        static_portrait = ROOT / "deekshith-ascii-clear.png"
        animated_portrait = ROOT / "deekshith-ascii-once.svg"
        self.assertTrue(static_portrait.exists())
        self.assertTrue(animated_portrait.exists())
        self.assertGreater(static_portrait.stat().st_size, 100_000)
        self.assertGreater(animated_portrait.stat().st_size, 500_000)
        self.assertIn("./deekshith-ascii-once.svg", readme)
        self.assertIn('width="470"', readme)
        self.assertNotIn(".gif", readme)
        svg = animated_portrait.read_text(encoding="utf-8")
        self.assertIn('repeatCount="1"', svg)
        self.assertNotIn('repeatCount="indefinite"', svg.split('portrait loaded successfully')[0])


if __name__ == "__main__":
    unittest.main()
