"""Pruebas herméticas del recibo de corrección; sin red ni proveedores externos."""
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "skills" / "ingenieria-fiable" / "tools" / "prueba_correccion.py"


class ProofOfFixTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "parser.py"
        self.test = self.root / "test_parser.py"
        self.receipt = self.root / "private-proof.json"
        self.source.write_text("def parse(x):\n    return x.strip()\n", encoding="utf-8")
        self.test.write_text("from parser import parse\nassert parse(' x ') == 'x'\n", encoding="utf-8")

    def cli(self, *args):
        return subprocess.run([sys.executable, str(TOOL), *map(str, args)],
                              text=True, capture_output=True, cwd=self.root)

    def phase(self, value, command=None, paths=None):
        command = command or [sys.executable, "test_parser.py"]
        flags = ["record", "--root", self.root, "--evidence", self.receipt,
                 "--phase", value, "--requirement", "R1", "--watch", "parser.py",
                 "--watch", "test_parser.py"]
        if paths is not None:
            flags = ["record", "--root", self.root, "--evidence", self.receipt,
                     "--phase", value, "--requirement", "R1"] + [
                         x for path in paths for x in ("--watch", path)]
        return self.cli(*flags, "--", *command)

    def test_before_after_with_drift_and_recovery(self):
        self.source.write_text("def parse(x):\n    return x\n")
        first = self.phase("before")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(json.loads(first.stdout)["test_exit_code"], 1)
        self.source.write_text("def parse(x):\n    return x.strip()\n")
        second = self.phase("after")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(json.loads(second.stdout)["verdict"], "consistent_record")
        self.assertEqual(self.cli("check", "--root", self.root, "--evidence", self.receipt).returncode, 0)
        self.assertEqual(stat.S_IMODE(self.receipt.stat().st_mode), 0o600)
        self.source.write_text("def parse(x):\n    return x.strip()  # drift\n")
        stale = self.cli("check", "--root", self.root, "--evidence", self.receipt)
        self.assertEqual(stale.returncode, 1)
        self.assertIn("obsoleta", stale.stdout)
        self.source.write_text("def parse(x):\n    return x.strip()\n")
        self.assertEqual(self.cli("check", "--root", self.root, "--evidence", self.receipt).returncode, 0)

    def test_before_already_passes_is_not_proof(self):
        self.assertEqual(self.phase("before").returncode, 0)
        after = self.phase("after")
        self.assertEqual(after.returncode, 0)
        self.assertIn("no quedó reproducido", after.stdout)
        self.assertEqual(self.cli("check", "--root", self.root, "--evidence", self.receipt).returncode, 1)

    def test_after_test_failure_is_not_proof(self):
        self.source.write_text("def parse(x):\n    return x\n")
        self.assertEqual(self.phase("before").returncode, 0)
        fail = self.phase("after")
        self.assertEqual(fail.returncode, 1)
        self.assertIn("no terminó", fail.stdout)

    def test_command_mismatch_rejected(self):
        self.source.write_text("def parse(x):\n    return x\n")
        self.phase("before")
        r = self.phase("after", command=[sys.executable, "-c", "print('skip')"])
        self.assertEqual(r.returncode, 2)
        self.assertIn("iguales", r.stderr)

    def test_prevents_overwrite_before(self):
        self.phase("before")
        second = self.phase("before")
        self.assertEqual(second.returncode, 2)
        self.assertIn("ya existe", second.stderr)

    def test_watched_test_mutates_code_is_detected(self):
        self.source.write_text("def parse(x):\n    return x\n")
        self.test.write_text("from pathlib import Path\nPath('parser.py').write_text('changed')\nraise ValueError()\n")
        self.phase("before")
        self.test.write_text("from parser import parse\nassert parse(' x ') == 'x'\n")
        self.source.write_text("def parse(x):\n    return x.strip()\n")
        r = self.phase("after")
        self.assertIn("modificó", r.stdout)

    def test_symlink_outside_is_rejected(self):
        outside = self.root.parent / "not-me.txt"
        (self.root / "alias.py").symlink_to(outside)
        r = self.phase("before", paths=["alias.py"])
        self.assertEqual(r.returncode, 2)

    def test_other_project_cannot_claim_same_receipt(self):
        self.source.write_text("def parse(x):\n    return x\n")
        self.phase("before")
        self.source.write_text("def parse(x):\n    return x.strip()\n")
        self.phase("after")
        other = self.root / "other-project"
        other.mkdir()
        (other / "parser.py").write_text(self.source.read_text())
        (other / "test_parser.py").write_text(self.test.read_text())
        changed = self.cli("check", "--root", other, "--evidence", self.receipt)
        self.assertEqual(changed.returncode, 1)
        self.assertIn("otro directorio", changed.stdout)

    def test_timeout_is_not_success(self):
        result = self.cli("record", "--root", self.root, "--evidence", self.receipt,
                          "--phase", "before", "--requirement", "R1", "--watch", "parser.py",
                          "--timeout", "1", "--", sys.executable, "-c",
                          "import time; time.sleep(4)")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["test_exit_code"], "timeout")
        self.assertEqual(self.cli("check", "--root", self.root, "--evidence", self.receipt).returncode, 1)

    def test_reject_missing_evidence(self):
        r = self.cli("check", "--root", self.root, "--evidence", self.receipt)
        self.assertEqual(r.returncode, 2)

    def test_receipt_does_not_include_test_output(self):
        self.test.write_text("import sys\nprint('FAKE_PRIVATE_VALUE', file=sys.stderr)\nraise ValueError('fail')\n")
        self.phase("before")
        self.assertNotIn("FAKE_PRIVATE_VALUE", self.receipt.read_text())
        self.assertIn("output_sha256", self.receipt.read_text())


if __name__ == "__main__":
    unittest.main()
