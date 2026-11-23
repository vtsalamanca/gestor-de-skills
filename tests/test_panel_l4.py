import hashlib
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("panel_l4", ROOT / "scripts/panel_l4.py")
panel = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(panel)

REF = "https://chatgpt.com/c/00000000-0000-0000-0000-000000000001"
CASES = [{"id": "x", "prompt": "<script>example</script>", "expected_skills": []}]


class TestPanelL4(unittest.TestCase):
    def test_pilot_does_not_set_metrics_and_prompt_is_escaped(self):
        html = panel.render(CASES, [{"caso": "x", "ref": REF}], [], "0.4.59", None)
        self.assertIn("Ejecutados</dt><dd>1 / 1", html)
        self.assertIn("Verificados en la versión</dt><dd>0 / 1", html)
        self.assertIn("&lt;script&gt;example&lt;/script&gt;", html)
        self.assertIn("Sin datos", html)

    def test_rejects_unreviewed_observations_and_unsafe_links(self):
        with self.assertRaisesRegex(ValueError, "requiere trazas"):
            panel.render(CASES, [], [{"id": "x", "observation_kind": "user_report"}], "0.4.59", None)
        with self.assertRaisesRegex(ValueError, "enlace privado"):
            panel.render(CASES, [{"caso": "x", "ref": REF + "?token=example"}], [], "0.4.59", None)

    def test_reviewed_trace_from_other_version_has_no_effect_on_score(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            trace = json.dumps({"conversation_ref": REF, "plugin_version": "0.4.59", "tool_name": "turn"}).encode()
            (root / "turn.jsonl").write_bytes(trace)
            row = {"id": "x", "observation_kind": "verified_tool_trace", "selected_skills": [],
                   "conversation_ref": REF, "plugin_version": "0.4.59", "trace_path": "turn.jsonl",
                   "trace_sha256": hashlib.sha256(trace).hexdigest(), "evidence": "test fixture"}
            html = panel.render(CASES, [], [row], "0.4.58", root)
            self.assertIn("Verificados en la versión</dt><dd>0 / 1", html)
            self.assertIn('<tr data-state="other">', html)
            html = panel.render(CASES, [], [row], "0.4.59", root)
            self.assertIn("Verificados en la versión</dt><dd>1 / 1", html)
            self.assertIn("Medición completa", html)
