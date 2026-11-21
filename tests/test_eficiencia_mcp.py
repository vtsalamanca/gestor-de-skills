"""Tests offline del análisis MCP: nunca invocan servidores MCP."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "control-laboratorio" / "tools" / "eficiencia_mcp.py"
sys.path.insert(0, str(SCRIPT.parent))
from eficiencia_mcp import analyze, render_markdown


def fixture():
    return {
        "schema_version": 1, "connector": "Control Debian",
        "captured_at": "2026-11-21T06:00:00+01:00", "input_sha256": "synthetic",
        "total": 2,
        "tools": [
            {"name": "read_file", "description": "Read an allowed fixture", "group": "archivos"},
            {"name": "debian_host_status", "description": "Check host status", "group": "equipo"}
        ]
    }


class EficienciaMCPTests(unittest.TestCase):
    def test_analysis_without_usage_is_unknown(self):
        result = analyze(fixture())
        self.assertEqual(result["summary"]["tools"], 2)
        self.assertIsNone(result["summary"]["tool_schema_tokens"])
        self.assertTrue(all(t["observed_calls"] is None for t in result["tools"]))
        self.assertTrue(all(t["observation"] == "unknown" for t in result["tools"]))

    def test_partial_counts_do_not_imply_unused(self):
        result = analyze(fixture(), {"schema_version": 1, "scope": "sesion 1", "complete": False, "counts": {"read_file": 3}})
        entries = {x["name"]: x for x in result["tools"]}
        self.assertEqual(entries["read_file"]["observed_calls"], 3)
        self.assertIsNone(entries["debian_host_status"]["observed_calls"])

    def test_complete_observed_scope_marks_zero_without_recommend_disconnection(self):
        report = analyze(fixture(), {"schema_version": 1, "scope": "sesion completa", "complete": True, "counts": {"read_file": 2}})
        entries = {x["name"]: x for x in report["tools"]}
        self.assertEqual(entries["debian_host_status"]["observation"], "not_observed_in_scope")
        self.assertIn("No desconectar", " ".join(report["warnings"]))

    def test_reject_duplicate_and_wrong_total(self):
        data = fixture()
        data["tools"].append(dict(data["tools"][0]))
        data["total"] = 3
        with self.assertRaisesRegex(ValueError, "duplicada"):
            analyze(data)
        data["tools"].pop()
        with self.assertRaisesRegex(ValueError, "incongruente"):
            analyze(data)

    def test_reject_fake_usage(self):
        base = {"schema_version": 1, "scope": "sesion 1", "complete": True, "counts": {"unlisted": 1}}
        with self.assertRaises(ValueError):
            analyze(fixture(), base)
        base["counts"] = {"read_file": True}
        with self.assertRaises(ValueError):
            analyze(fixture(), base)

    def test_markdown_uses_explicit_proxy_language(self):
        text = render_markdown(analyze(fixture()), limit=2)
        self.assertIn("NO tokens reales", text)
        self.assertIn("read_file", text)
        self.assertIn("Sin observación", text)
        self.assertIn("sin datos", text)

    def test_cli_json_does_not_write_input(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "inventory.json"
            raw = json.dumps(fixture())
            path.write_text(raw)
            proc = subprocess.run([sys.executable, str(SCRIPT), "--inventory", str(path),
                                   "--format", "json"], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)["summary"]["tools"], 2)
            self.assertEqual(path.read_text(), raw)

    def test_reject_invalid_json(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "broken.json"
            path.write_text("{")
            proc = subprocess.run([sys.executable, str(SCRIPT), "--inventory", str(path)],
                                  capture_output=True, text=True)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("ERROR:", proc.stderr)


if __name__ == "__main__":
    unittest.main()
