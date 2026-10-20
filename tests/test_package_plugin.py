from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import unittest
import uuid
import zipfile

from scripts.package_plugin import EXPECTED_SKILLS, PackageError, build_archive, export_commit, remove_tree, validate_snapshot, validate_archive_member


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

    def test_sensitive_files_are_rejected(self) -> None:
        skill_dir = self.root / "skills" / "auditar-skills"
        for name in (".env", "private.pem", "credentials.json"):
            with self.subTest(name=name):
                target = skill_dir / name
                target.write_text("fixture only", encoding="utf-8")
                try:
                    with self.assertRaisesRegex(PackageError, "potencialmente sensible"):
                        validate_snapshot(self.root)
                finally:
                    target.unlink()

    def test_unexpected_root_files_are_not_packaged(self) -> None:
        (self.root / "unexpected.txt").write_text("EXCLUDED", encoding="utf-8")
        archive_path = self.temporary / "safe.zip"
        build_archive(self.root, archive_path, "a" * 40)
        with zipfile.ZipFile(archive_path) as archive:
            self.assertNotIn("unexpected.txt", archive.namelist())

    def test_skill_declared_name_must_match_folder(self) -> None:
        skill_file = self.root / "skills" / "auditar-skills" / "SKILL.md"
        skill_file.write_text("---\\nname: incorrecto\\ndescription: test\\n---\\n", encoding="utf-8")
        with self.assertRaisesRegex(PackageError, "no coincide"):
            validate_snapshot(self.root)

    def test_archive_paths_reject_traversal_and_windows_forms(self) -> None:
        for name in ("../escape", "skills/../../escape", "/absolute", "C:/Windows/escape", "skills\\..\\escape"):
            with self.subTest(name=name), self.assertRaisesRegex(PackageError, "Ruta insegura"):
                validate_archive_member(name)
        validate_archive_member("skills/auditar-skills/SKILL.md")

    def test_large_file_is_rejected(self) -> None:
        large = self.root / "skills" / "auditar-skills" / "references" / "large.txt"
        with large.open("wb") as file:
            file.truncate(5 * 1024 * 1024 + 1)
        with self.assertRaisesRegex(PackageError, "demasiado grande"):
            validate_snapshot(self.root)

    def test_root_symlink_is_rejected_when_supported(self) -> None:
        path = self.root / "README.md"
        path.unlink()
        target = self.temporary / "elsewhere.txt"
        target.write_text("OUTSIDE", encoding="utf-8")
        try:
            path.symlink_to(target)
        except (OSError, NotImplementedError):
            self.skipTest("Windows no permite enlaces simbolicos en esta cuenta")
        with self.assertRaisesRegex(PackageError, "Ruta insegura"):
            validate_snapshot(self.root)

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

        self.assertEqual(plugin["version"], "0.4.11")
        self.assertEqual(marketplace["plugins"][0]["version"], plugin["version"])
        self.assertIn("version: 0.2.8", procedure)
        self.assertIn("http.sslBackend", procedure)
        self.assertIn("codex plugin marketplace upgrade", procedure)
        self.assertIn("no ejecutar `plugin add`", procedure)


if __name__ == "__main__":
    unittest.main()


