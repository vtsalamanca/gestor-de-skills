from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import unittest
import uuid
import zipfile

from scripts.package_plugin import EXPECTED_SKILLS, PackageError, build_archive, export_commit, remove_tree, validate_snapshot


class PackagePluginTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = Path.cwd() / f".package-tests-{uuid.uuid4().hex}"
        self.root = self.temporary / "source"
        self.root.mkdir(parents=True)
        (self.root / ".codex-plugin").mkdir()
        (self.root / ".agents" / "plugins").mkdir(parents=True)
        (self.root / "skills").mkdir()
        (self.root / "README.md").write_bytes(b"# fixture\r\n")
        plugin = {"name": "gestor-de-skills", "version": "0.4.6", "skills": "./skills/"}
        marketplace = {"plugins": [{"name": "gestor-de-skills", "version": "0.4.6"}]}
        (self.root / ".codex-plugin" / "plugin.json").write_text(json.dumps(plugin), encoding="utf-8")
        (self.root / ".agents" / "plugins" / "marketplace.json").write_text(json.dumps(marketplace), encoding="utf-8")
        for skill in EXPECTED_SKILLS:
            directory = self.root / "skills" / skill
            (directory / "references").mkdir(parents=True)
            (directory / "SKILL.md").write_text(f"---\nname: {skill}\ndescription: test\n---\n", encoding="utf-8")
            (directory / "references" / "data.txt").write_bytes(f"{skill}\r\n".encode())

    def tearDown(self) -> None:
        remove_tree(self.temporary)

    def test_archive_is_deterministic_and_preserves_source_bytes(self) -> None:
        before = self._tree_hashes()
        first = self.temporary / "first.zip"
        second = self.temporary / "second.zip"
        report_one = build_archive(self.root, first, "a" * 40)
        report_two = build_archive(self.root, second, "a" * 40)

        self.assertEqual(first.read_bytes(), second.read_bytes())
        self.assertEqual(report_one["archive"]["sha256"], report_two["archive"]["sha256"])
        self.assertEqual(before, self._tree_hashes())
        with zipfile.ZipFile(first) as archive:
            self.assertNotIn(".agents/plugins/marketplace.json", archive.namelist())
            self.assertEqual(archive.read("README.md"), b"# fixture\r\n")
            packaged_skills = {
                Path(name).parent.name
                for name in archive.namelist()
                if name.endswith("/SKILL.md")
            }
            self.assertEqual(packaged_skills, EXPECTED_SKILLS)
            self.assertEqual(len(packaged_skills), 8)
            self.assertIn("acceso_webs", packaged_skills)
            for name, digest in report_one["files"].items():
                self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(), digest)

    def test_missing_skill_is_reported(self) -> None:
        missing = self.root / "skills" / "auditar-skills"
        for path in sorted(missing.rglob("*"), reverse=True):
            if path.is_file():
                path.unlink()
            else:
                path.rmdir()
        missing.rmdir()
        with self.assertRaisesRegex(PackageError, "Faltan=.*auditar-skills"):
            validate_snapshot(self.root)

    def test_version_mismatch_is_reported(self) -> None:
        marketplace = {"plugins": [{"name": "gestor-de-skills", "version": "9.9.9"}]}
        (self.root / ".agents" / "plugins" / "marketplace.json").write_text(json.dumps(marketplace), encoding="utf-8")
        with self.assertRaisesRegex(PackageError, "no coinciden"):
            validate_snapshot(self.root)

    def test_exact_commit_is_exported_without_modifying_repository(self) -> None:
        subprocess.run(["git", "init", "--quiet"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "--quiet", "-m", "fixture"], cwd=self.root, check=True)
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.root, check=True, capture_output=True, text=True).stdout.strip()
        original_status = subprocess.run(["git", "status", "--porcelain"], cwd=self.root, check=True, capture_output=True, text=True).stdout
        destination = self.temporary / "exported"
        self.assertEqual(export_commit(str(self.root), commit, destination), commit)
        self.assertEqual((destination / "README.md").read_bytes(), b"# fixture\r\n")
        final_status = subprocess.run(["git", "status", "--porcelain"], cwd=self.root, check=True, capture_output=True, text=True).stdout
        self.assertEqual(original_status, final_status)

    def _tree_hashes(self) -> dict[str, str]:
        return {
            path.relative_to(self.root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in self.root.rglob("*")
            if path.is_file() and ".git" not in path.parts
        }


class RepositoryReleaseTests(unittest.TestCase):
    def test_release_metadata_and_codex_update_recovery_are_synchronized(self) -> None:
        root = Path(__file__).resolve().parents[1]
        plugin = json.loads((root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((root / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8"))
        procedure = (root / "skills" / "organizaciondeltrabajo" / "SKILL.md").read_text(encoding="utf-8")

        self.assertEqual(plugin["version"], "0.4.9")
        self.assertEqual(marketplace["plugins"][0]["version"], plugin["version"])
        self.assertIn("version: 0.2.7", procedure)
        self.assertIn("http.sslBackend", procedure)
        self.assertIn("codex plugin marketplace upgrade", procedure)
        self.assertIn("no ejecutar `plugin add`", procedure)


if __name__ == "__main__":
    unittest.main()


