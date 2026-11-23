"""Regresión de documentación del flujo autónomo de Plugin Creator."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "skills/ingenieria-fiable/references/publicacion-autonoma-complemento.md"


class PublicacionAutonomaTest(unittest.TestCase):
    def test_protocolo_persistente_y_enrutamiento(self):
        self.assertTrue(RUNBOOK.is_file())
        txt = RUNBOOK.read_text(encoding="utf-8")
        for key in ("No pedirle", "Plugin_Creator.update_plugin", "expected_release_id", "get_plugin_files"):
            self.assertIn(key.lower(), txt.lower())
        for rel in (
            "skills/ingenieria-fiable/SKILL.md",
            "skills/ingenieria-fiable/references/actualizar-skills.md",
            "skills/control-laboratorio/references/08-git-y-skills.md",
            "skills/integrar-skills/SKILL.md",
        ):
            self.assertIn("publicacion-autonoma-complemento.md", (ROOT / rel).read_text(encoding="utf-8"))

    def test_manifiestos_con_version_coherente(self):
        v1 = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))["version"]
        v2 = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))["plugins"][0]["version"]
        self.assertEqual(v1, v2)


if __name__ == "__main__":
    unittest.main()
