"""Regresión documental: acceso web y entrega de tareas programadas."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GUIDE = "automatizacion-lab-auth.md"


class AccesoWebProgramadoTests(unittest.TestCase):
    def test_referencia_existente(self):
        protocol = ROOT / "skills/acceso_webs/references" / GUIDE
        text = protocol.read_text(encoding="utf-8")
        for token in ("start_process", "debian_lab_command_approve_on_desktop",
                      "Thunderbird", "Firefox", "ENTREGA_PENDIENTE",
                      "solo lectura", "temporizador", "MFA"):
            self.assertIn(token.lower(), text.lower())

    def test_enlaces_y_version(self):
        skill = (ROOT / "skills/acceso_webs/SKILL.md").read_text()
        auth = (ROOT / "skills/acceso_webs/references/lab-auth.md").read_text()
        self.assertIn("version: 0.5.3", skill)
        self.assertIn(GUIDE, skill)
        self.assertIn(GUIDE, auth)


if __name__ == "__main__":
    unittest.main()

