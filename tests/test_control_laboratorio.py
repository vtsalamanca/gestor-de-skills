"""Pruebas estáticas de la habilidad principal: sin red, llaveros ni procesos reales."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from scripts.package_plugin import EXPECTED_SKILLS

ROOT = Path(__file__).resolve().parents[1]
HUB = ROOT / "skills" / "control-laboratorio"
MAIN = HUB / "SKILL.md"
REF = HUB / "references"


class ControlLaboratorioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = MAIN.read_text(encoding="utf-8")
        cls.refs = {p.name: p.read_text(encoding="utf-8") for p in REF.glob("*.md")}

    def test_valid_frontmatter_and_activation(self):
        self.assertTrue(self.text.startswith("---\n"))
        hdr = self.text.split("---", 2)[1]
        self.assertIn("\nname: control-laboratorio\n", hdr)
        self.assertRegex(hdr, r"(?m)^version: 0\.2\.2$")
        for term in ("Control Debian", "Bibliotecario", "LAB-AUTH", "Goose", "GitHub"):
            self.assertIn(term, hdr)

    def test_complete_references_no_broken_links(self):
        self.assertEqual(len(self.refs), 18)
        links = re.findall(r"\]\(references/([a-z0-9-]+\.md)\)", self.text)
        self.assertEqual(set(links), set(self.refs), "Todas las referencias deben enlazarse")
        for name, content in self.refs.items():
            with self.subTest(reference=name):
                self.assertTrue(content.startswith("# "), name)
                self.assertGreater(len(content), 600)
                self.assertLess(len(content), 14000)

    def test_short_router_with_ten_specialists(self):
        self.assertLess(len(self.text), 14000, "No crear una skill monolitica")
        specialists = {
            "organizaciondeltrabajo", "ingenieria-fiable", "acceso_webs",
            "buscar-comparar-productos", "bibliotecario-memoria",
            "descubrir-skills", "auditar-skills", "crear-skills",
            "integrar-skills", "inventariar-skills",
        }
        for name in specialists:
            self.assertIn(name, self.text)
        self.assertEqual(EXPECTED_SKILLS, specialists | {"control-laboratorio"})
        self.assertEqual({p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}, EXPECTED_SKILLS)

    def test_manifests_consistent(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        market = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        entry = next(p for p in market["plugins"] if p["name"] == manifest["name"])
        self.assertEqual(manifest["version"], "0.4.51")
        self.assertEqual(entry["version"], manifest["version"])
        self.assertEqual(manifest["interface"]["capabilities"], ["Read"])
        self.assertIn("once habilidades", manifest["interface"]["longDescription"])
        self.assertIn("control-laboratorio", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_no_secrets_or_private_identifiers(self):
        all_text = "\n".join([self.text] + list(self.refs.values()))
        for bad in ("/home/labgestor/", "vtsalamanca@gmail.com", "-----BEGIN PRIVATE KEY",
                    "sk-proj-", "ghp_", "xoxb-", "AKIA", "Bearer eyJ",
                    "192.168."):
            with self.subTest(forbidden=bad):
                self.assertNotIn(bad, all_text)
        self.assertFalse(re.search(r"(?i)(password|token|secret)[ \t]*[:=][ \t]*['\"][^'\"]{8,}", all_text))

    def test_non_executable_knowledge_only(self):
        self.assertEqual({str(p.relative_to(HUB)) for p in HUB.rglob("*") if p.is_file() and p.suffix != ".md" and "__pycache__" not in p.parts}, {"tools/inventario_herramientas.py", "tools/eficiencia_mcp.py", "tools/supervisor_operaciones.py", "tools/laboratorio_doctor.py", "tools/supervision_diaria.py"})
        generator = (HUB / "tools/inventario_herramientas.py").read_text(encoding="utf-8")
        for forbidden in ("import subprocess", "import requests", "import socket", "import keyring", "os.system(", "os.popen(", "eval(", "exec("):
            self.assertNotIn(forbidden, generator)
        for word in ("autorización", "verificar", "Bibliotecario", "0 €"):
            self.assertIn(word, self.text)
        self.assertIn("no crea herramientas", self.text.lower())

    def test_source_of_truth_and_delivery_distinction(self):
        arch = self.refs["01-arquitectura.md"]
        self.assertIn("Estado vivo", arch)
        tasks = self.refs["05-automatizaciones.md"]
        for word in ("systemd", "Automations", "entrega", "adjuntos", "InfoJobs"):
            self.assertIn(word, tasks)
        self.assertIn("ticket", self.refs["02-control-debian.md"])
        self.assertIn("readback", self.refs["03-bibliotecario.md"])

    def test_inventory_reference_and_generator(self):
        guide = self.refs["17-inventario-operativo.md"]
        self.assertIn("inventario-mcp.json", guide)
        self.assertIn("--expected-count", guide)
        self.assertIn("no equivale", guide.lower())
        self.assertTrue((HUB / "tools/inventario_herramientas.py").is_file())
        self.assertIn("17-inventario-operativo.md", self.text)

    def test_auth_privacy_and_recovery(self):
        auth = self.refs["04-lab-auth.md"]
        for term in ("GNOME Keyring", "Thunderbird", "CAPTCHA", "candidaturas", "OTP"):
            self.assertIn(term, auth)
        recovery = self.refs["12-recuperacion.md"]
        for term in ("SQLite", "GitHub", "VirtualBox", "reversión", "perfil"):
            self.assertIn(term, recovery)

    def test_20_historical_lessons_and_20_scenarios(self):
        cases = self.refs["13-lecciones-reutilizables.md"]
        matrix = self.refs["11-pruebas-y-aceptacion.md"]
        for i in range(1, 21):
            with self.subTest(i=i):
                self.assertRegex(cases, rf"(?m)^{i}\. ")
                self.assertRegex(matrix, rf"(?m)^{i}\. ")

    def test_guide_routes_real_work(self):
        guide = self.refs["14-guia-rapida.md"]
        for term in ("Control Debian", "InfoJobs", "Educamos", "GitHub", "backups", "Igor"):
            self.assertIn(term, guide)
        org = (ROOT / "skills/organizaciondeltrabajo/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("control-laboratorio", org)
        self.assertIn("version: 0.2.25", org)


if __name__ == "__main__":
    unittest.main()
