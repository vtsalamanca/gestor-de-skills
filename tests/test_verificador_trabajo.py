"""Pruebas sin dependencias externas del verificador propio de tareas."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "ingenieria-fiable" / "tools" / "verificador_trabajo.py"


class VerificadorTrabajoTests(unittest.TestCase):
    def scan(self, filename, code, *flags):
        with tempfile.TemporaryDirectory() as tmp:
            sample = Path(tmp) / filename
            sample.write_text(code, encoding="utf-8")
            proc = subprocess.run([sys.executable, str(SCRIPT), "--json", *flags, str(sample)],
                                  capture_output=True, text=True, check=False)
            return proc.returncode, json.loads(proc.stdout)

    def test_detects_function_stub_and_critical_exit(self):
        code, result = self.scan("modulo.py", "def incomplete():\n    pass\n")
        self.assertEqual(code, 1)
        self.assertEqual(result["critical"], 1)
        self.assertEqual(result["findings"][0]["rule"], "function-stub")

    def test_allows_valid_function(self):
        code, result = self.scan("modulo.py", "def complete(value):\n    return value + 1\n")
        self.assertEqual(code, 0)
        self.assertEqual(result["findings"], [])

    def test_empty_test_warns_by_default_and_fails_if_requested(self):
        source = "def test_something():\n    value = 2\n"
        code, result = self.scan("test_example.py", source)
        self.assertEqual(code, 0)
        self.assertEqual(result["warning"], 1)
        code, result = self.scan("test_example.py", source, "--fail-on", "warning")
        self.assertEqual(code, 1)

    def test_pytest_raises_is_a_verification(self):
        source = "import pytest\ndef test_failure():\n    with pytest.raises(ValueError):\n        int('a')\n"
        code, result = self.scan("test_example.py", source)
        self.assertEqual(code, 0)
        self.assertEqual(result["findings"], [])

    def test_abstractmethod_is_not_stub(self):
        source = "from abc import abstractmethod\n@abstractmethod\ndef abstract():\n    pass\n"
        code, result = self.scan("modulo.py", source)
        self.assertEqual(code, 0)
        self.assertEqual(result["findings"], [])

    def test_swallowed_exception_and_debugger(self):
        source = "try:\n    1 / 0\nexcept Exception:\n    pass\nbreakpoint()\n"
        code, result = self.scan("modulo.py", source)
        self.assertEqual(code, 0)
        self.assertEqual({f["rule"] for f in result["findings"]}, {"swallowed-exception", "debugger"})

    def test_js_patterns_are_warn_only(self):
        code, result = self.scan("sample.ts", "debugger;\nit.only('x', () => {})\n")
        self.assertEqual(code, 0)
        self.assertEqual({f["rule"] for f in result["findings"]}, {"debugger", "test-only"})

    def test_syntax_error_is_critical(self):
        code, result = self.scan("broken.py", "def bad(:\n")
        self.assertEqual(code, 1)
        self.assertEqual(result["findings"][0]["rule"], "parse-or-read-error")


if __name__ == "__main__":
    unittest.main()
