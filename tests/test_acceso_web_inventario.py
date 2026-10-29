"""Regresión documental: contenidos obligatorios y estados honestos."""
from pathlib import Path
import json
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
ACCESS=ROOT/"skills/acceso_webs"
INVENT=ROOT/"skills/inventariar-skills"
TECH=ACCESS/"references/sesiones-navegador-llavero-oauth.md"
TABLE=INVENT/"references/inventario-acceso-web-2026-10-27.md"


class KnowledgeInventoryTests(unittest.TestCase):
    def test_consistent_release_version(self):
        plugin=json.loads((ROOT/".codex-plugin/plugin.json").read_text())
        marketplace=json.loads((ROOT/".agents/plugins/marketplace.json").read_text())
        self.assertEqual(plugin["version"],marketplace["plugins"][0]["version"])
        self.assertEqual(len(plugin["version"].split(".")),3)
        self.assertTrue(all(piece.isdigit() for piece in plugin["version"].split(".")))
        self.assertIn(plugin["version"],(ROOT/"README.md").read_text(encoding="utf-8").splitlines()[0])

    def test_access_skills_refers_to_real_reference(self):
        src=(ACCESS/"SKILL.md").read_text()
        self.assertIn("version: 0.4.3",src)
        self.assertIn("references/sesiones-navegador-llavero-oauth.md",src)
        self.assertTrue(TECH.is_file())
        self.assertGreater(len(TECH.read_text().splitlines()),40)

    def test_inventory_is_registered(self):
        src=(INVENT/"SKILL.md").read_text()
        self.assertIn("references/inventario-acceso-web-2026-10-27.md",src)
        data=TABLE.read_text()
        for expected in ("WebDriver BiDi","GNOME Keyring","Wallapop","InfoJobs Developers","Plugin Creator"):
            self.assertIn(expected,data)

    def test_control_debian_inventory_is_registered_and_versioned(self):
        inv=INVENT/"references/inventario-control-debian-2026-10-29.md"
        self.assertTrue(inv.is_file())
        skills=(INVENT/"SKILL.md").read_text()
        self.assertIn("references/inventario-control-debian-2026-10-29.md",skills)
        text=inv.read_text(encoding="utf-8")
        for term in ("Open Computer Use","Firefox DevTools MCP","Codex CLI",
                     "GitHub Actions", "PENDIENTE", "cuota", "CDC"):
            self.assertIn(term.lower(),text.lower())
        org=(ROOT/"skills/organizaciondeltrabajo/SKILL.md").read_text()
        self.assertIn("Puerta de detección y autorización previa",org)

    def test_prior_consent_for_catalog_and_backup(self):
        protocol=(INVENT/"references/autorizacion_catalogacion_y_resguardo.md")
        self.assertTrue(protocol.is_file())
        text=protocol.read_text(encoding="utf-8")
        for phrase in ("autorización", "resguardo", "CATALOGACION_PENDIENTE_AUTORIZACION",
                       "RESGUARDO_PENDIENTE_AUTORIZACION", "misma", "no crear"):
            self.assertIn(phrase.lower(), text.lower())
        for folder in ("inventariar-skills", "organizaciondeltrabajo",
                       "ingenieria-fiable", "bibliotecario-memoria"):
            skill=(ROOT/"skills"/folder/"SKILL.md").read_text(encoding="utf-8")
            self.assertIn("autorización", skill.lower())
            self.assertIn("autorizacion_catalogacion_y_resguardo.md", skill)
        runbook=(ROOT/"skills/ingenieria-fiable/references/actualizar-skills.md").read_text()
        self.assertIn("Regla vigente de autorización",runbook)
        self.assertIn("prioridad sobre las instrucciones históricas",runbook)

    def test_clearly_separates_evidence(self):
        text=TECH.read_text()+"\n"+TABLE.read_text()
        for required in ("NO se demostró","no se ha demostrado","BLOQUEADO","VERIFICADO","NO_PROBADO"):
            self.assertIn(required.lower(),text.lower())
        self.assertIn("no hay Client ID",text)

    def test_no_private_material_embedded(self):
        text=TECH.read_text()+"\n"+TABLE.read_text()
        # No pasted user email, tokens, personal identifiers or password dumps.
        self.assertNotRegex(text,r"[\w.+-]+@gmail\.com")
        self.assertNotRegex(text,r"(?i)-----BEGIN (RSA |OPENSSH )?PRIVATE KEY-----")
        self.assertNotRegex(text,r"(?i)(?:refresh_token|access_token)\s*[:=]\s*['\"][A-Za-z0-9_-]{20,}")


if __name__=="__main__":
    unittest.main()
