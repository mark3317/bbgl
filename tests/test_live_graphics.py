"""Startup patch selection for the opt-in live graphics experiment."""
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import patches

class LiveGraphicsTests(unittest.TestCase):
    def test_normal_startup_is_unchanged(self):
        with patch.dict(os.environ, {"BB_LIVE_GRAPHICS": "0"}):
            names = patches.effect_patches({"effect_ssao": "0", "model_lod": "2"})
        self.assertIn("Disable SSAO", names)
        self.assertIn("Model LOD 2 (Lowest)", names)

    def test_live_start_prepares_all_effects_even_when_disabled(self):
        settings = {k: "0" for k in patches.EFFECTS if k.startswith("effect_")}
        settings.update(model_lod="2", skip_intro="1")
        with patch.dict(os.environ, {"BB_LIVE_GRAPHICS": "1"}):
            names = patches.effect_patches(settings)
        self.assertEqual(names, ["Skip Intro"])

    def test_ssr_remains_a_startup_setting(self):
        with patch.dict(os.environ, {"BB_LIVE_GRAPHICS": "1"}):
            self.assertEqual(patches.effect_patches({}), [])
            self.assertEqual(patches.effect_patches({"effect_ssr": "1"}), ["Enable Screen Space Reflections (READ NOTE)"])

if __name__ == "__main__": unittest.main()
