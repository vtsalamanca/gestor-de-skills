"""Pruebas herméticas: portabilidad, continuidad y política sin llamar a modelos."""
from pathlib import Path
import json
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills/integrar-skills/tools"))
sys.path.insert(0, str(ROOT / "skills/bibliotecario-memoria/tools"))
sys.path.insert(0, str(ROOT / "skills/control-laboratorio/tools"))
from portabilidad_agentes import check, REQUIRED_SKILLS
from traspaso_seguro import create, inspect, validate
from preflight_agentes import inspect as audit_agents
from arranque_seguro_agentes import plan


class PortabilityTests(unittest.TestCase):
    def fixture(self, root):
        (root / ".codex-plugin").mkdir()
        (root / ".agents/plugins").mkdir(parents=True)
        (root / ".codex-plugin/plugin.json").write_text('{"version":"0.4.53"}')
        (root / ".agents/plugins/marketplace.json").write_text('{"plugins":[{"version":"0.4.53"}]}')
        for skill in REQUIRED_SKILLS:
            (root / "skills" / skill).mkdir(parents=True)
        path = root / "skills/ingenieria-fiable/SKILL.md"
        path.write_text("# portable\n")
        return path

    def test_actual_repository_manifests_and_links(self):
        outcome = check(ROOT)
        self.assertEqual(outcome["errors"], 0)
        self.assertGreater(outcome["scanned"], 50)

    def test_fixed_home_path_and_broken_local_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = self.fixture(root)
            p.write_text("See /home/somebody/private\n[ref](references/missing.md)\n")
            result = check(root)
            self.assertEqual({v["rule"] for v in result["findings"]},
                             {"home-hardcoded", "broken-link"})

    def test_different_manifest_versions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.fixture(root)
            (root / ".codex-plugin/plugin.json").write_text('{"version":"0.4.52"}')
            self.assertIn("version-mismatch", {f["rule"] for f in check(root)["findings"]})


class HandoffTests(unittest.TestCase):
    def fixture(self):
        return {"schema_version": 1, "project": "lab",
                "objective": "mejorar herramientas",
                "verified_facts": [{"statement": "3 tests pasaron", "evidence": "commit sha verificable"}],
                "pending": [{"statement": "validar login", "evidence": "no probado"}],
                "authorization_history": [{"action": "revisar", "scope": "fixture",
                                            "source": "conversación precedente"}],
                "source_commit": "a" * 40}

    def test_receipt_is_private_and_not_authority(self):
        with tempfile.TemporaryDirectory() as temp:
            t = Path(temp)
            source, target = t / "input.json", t / "private.json"
            source.write_text(json.dumps(self.fixture()))
            checksum = create(source, target)
            data = json.loads(target.read_text())
            self.assertEqual(data["sha256"], checksum)
            self.assertTrue(data["requires_current_session_permission_check"])
            self.assertEqual(data["authorization_status"], "historical_unverified")
            self.assertEqual(inspect(target)["authorizations"], "historical_only")
            self.assertEqual(target.stat().st_mode & 0o777, 0o600)
            with self.assertRaises(ValueError):
                create(source, target)
            data["authorization_status"] = "active"
            target.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                inspect(target)

    def test_secrets_and_extra_authorization_flags_rejected(self):
        data = self.fixture()
        data["verified_facts"][0]["statement"] = "password: something-secret"
        with self.assertRaises(ValueError):
            validate(data)
        data = self.fixture()
        data["authorization_history"][0]["granted"] = True
        with self.assertRaises(ValueError):
            validate(data)


class SafetyTests(unittest.TestCase):
    def test_detect_unrestricted_codex_and_autonomous_external_goose(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".codex").mkdir()
            (home / ".config/goose").mkdir(parents=True)
            (home / ".codex/config.toml").write_text(
                'sandbox_mode = "danger-full-access"\napproval_policy = "never"\n')
            (home / ".config/goose/config.yaml").write_text(
                "GOOSE_MODE: auto\nactive_provider: groq\nGROQ_API_KEY: should_not_leave\n")
            report = audit_agents(home)
            rules = {r["rule"] for r in report["findings"]}
            self.assertIn("unsandboxed", rules)
            self.assertIn("no-approvals", rules)
            self.assertIn("external-provider-configured", rules)
            self.assertNotIn("should_not_leave", json.dumps(report))

    def test_codex_wrapper_blocks_non_chatgpt_auth(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".codex").mkdir()
            (home / ".codex/config.toml").write_text("")
            (home / ".codex/auth.json").write_text('{"auth_mode":"apikey"}')
            with self.assertRaises(ValueError):
                plan("codex", None, home)
            (home / ".codex/auth.json").write_text('{"auth_mode":"chatgpt"}')
            options = plan("codex", None, home)
            self.assertIn("workspace-write", options["command"])
            self.assertIn("sandbox_workspace_write.network_access=false", options["command"])

    def test_goose_wrapper_forces_local_provider_and_approvals(self):
        spec = plan("goose", "qwen2.5:2b", Path("/tmp"))
        self.assertEqual(spec["env_overrides"]["GOOSE_PROVIDER"], "ollama")
        self.assertEqual(spec["env_overrides"]["GOOSE_MODE"], "approve")
        self.assertEqual(spec["env_overrides"]["OLLAMA_HOST"], "127.0.0.1:11434")
        with self.assertRaises(ValueError):
            plan("goose", "https://evil.example?key=x", Path("/tmp"))


if __name__ == "__main__":
    unittest.main()
