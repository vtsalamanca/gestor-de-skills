"""Regresión del catálogo BrowserLearn: solo instrucciones, sin navegador ni cuentas reales."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
ACCESS = ROOT / "skills" / "acceso_webs"
CONTROL = ROOT / "skills" / "control-laboratorio"
INDEX = ACCESS / "references" / "modalidades.json"
MANUAL = ACCESS / "references" / "browserlearn-laboratorio.md"


class BrowserLearnCatalogTests(unittest.TestCase):
    def test_registered_in_skills_without_new_duplicate_skill(self):
        access = (ACCESS / "SKILL.md").read_text(encoding="utf-8")
        control = (CONTROL / "SKILL.md").read_text(encoding="utf-8")
        inventory = (ROOT / "skills" / "inventariar-skills" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("references/browserlearn-laboratorio.md", access)
        self.assertIn("BrowserLearn", control)
        self.assertIn("BrowserLearn", inventory)
        self.assertTrue(MANUAL.is_file())
        self.assertEqual(len([p for p in (ROOT / "skills").iterdir() if p.is_dir()]), 11)
        self.assertFalse((ROOT / "skills" / "browserlearn").exists())

    def test_manual_describes_local_only_limits_and_recovery(self):
        manual = MANUAL.read_text(encoding="utf-8")
        for expected in ("browserlearn-lab start", "browserlearn-lab-browser",
                         "127.0.0.1:7420", "BROWSERLEARN_STRICT_REDACTION",
                         "http://*/*", "https://*/*", "LAB-AUTH",
                         "No configurada como servicio", "datos", "0 €"):
            self.assertIn(expected, manual)
        self.assertNotIn("/home/labgestor/", manual)
        self.assertNotIn("-----BEGIN PRIVATE KEY", manual)

    def test_declarative_modality_opt_in(self):
        data = json.loads(INDEX.read_text(encoding="utf-8"))
        methods = data["modalidades"]
        self.assertEqual([m["orden"] for m in methods], sorted(m["orden"] for m in methods))
        matches = [m for m in methods if m["id"] == "M45_GRABAR_PROCEDIMIENTO_WEB"]
        self.assertEqual(len(matches), 1)
        entry = matches[0]
        self.assertEqual(entry["capacidad_requerida"], "browserlearn_local")
        self.assertIn("PROCEDIMIENTO_WEB_REPETIBLE", entry["senales"])
        self.assertNotIn("*", entry["senales"])
        self.assertIn("consentimiento explícito para grabar", entry["requisitos"])

    def test_selector_requires_real_local_capability(self):
        sys.path.insert(0, str(ACCESS / "tools"))
        from selector_metodos import recomendar
        signal = "PROCEDIMIENTO_WEB_REPETIBLE"
        found = recomendar(signal, {"browserlearn_local": True})
        self.assertEqual(found["metodo"], "M45_GRABAR_PROCEDIMIENTO_WEB")
        missing = recomendar(signal, {"browserlearn_local": False})
        self.assertNotEqual(missing["metodo"], "M45_GRABAR_PROCEDIMIENTO_WEB")
        self.assertEqual(recomendar("CAPTCHA_PENDIENTE", {"browserlearn_local": True})["estado"], "DETENER")

    def test_cli_flag_is_effective(self):
        script = ACCESS / "tools" / "selector_metodos.py"
        p = subprocess.run([sys.executable, str(script), "PROCEDIMIENTO_WEB_REPETIBLE",
                            "--browserlearn-local"], capture_output=True, text=True, check=False)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["metodo"], "M45_GRABAR_PROCEDIMIENTO_WEB")

    def test_proof_of_fix_is_integrated(self):
        skill = (ROOT / "skills" / "ingenieria-fiable" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("prueba_correccion.py", skill)
        self.assertTrue((ROOT / "skills" / "ingenieria-fiable" / "tools" / "prueba_correccion.py").is_file())
        self.assertTrue((ROOT / "skills" / "ingenieria-fiable" / "references" / "prueba-correccion.md").is_file())


if __name__ == "__main__":
    unittest.main()
