"""Tests aislados del catálogo de herramientas de Control Debian, sin red."""
import contextlib
import io
import json
from pathlib import Path
import runpy
import stat
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FUNCTIONS = runpy.run_path(str(ROOT / "skills/control-laboratorio/tools/inventario_herramientas.py"))
parse = FUNCTIONS["read_snapshot_tsv"]
build = FUNCTIONS["build_snapshot"]
read_evidence = FUNCTIONS["read_evidence"]
diff = FUNCTIONS["differences"]
markdown = FUNCTIONS["markdown"]
run = FUNCTIONS["run"]

SAMPLE = "read_file\tRead a file safely.\ndebian_gui_fixture_status\tFixture status.\n"
DATE = "2026-11-19T06:00:00+01:00"


class InventoryTests(unittest.TestCase):
    def test_parse_all_rows_and_groups(self):
        parsed = parse(SAMPLE)
        self.assertEqual(len(parsed), 2)
        snap = build(SAMPLE, DATE)
        self.assertEqual(snap["total"], 2)
        self.assertEqual(snap["tools"][0]["group"], "archivos_y_configuracion")
        self.assertEqual(snap["tools"][1]["group"], "interfaz_grafica")
        self.assertEqual(snap["tools"][0]["verification"]["result"], "sin_prueba")

    def test_parse_rejects_empty(self):
        with self.assertRaisesRegex(ValueError, "vacía"):
            parse("  \n")

    def test_parse_rejects_duplicates(self):
        with self.assertRaisesRegex(ValueError, "duplicada"):
            parse(SAMPLE + "read_file\tRepeated.\n")

    def test_parse_rejects_bad_name(self):
        for name in ("../../env", "ABC", "some-name", "foo bar"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                parse(name + "\tSomething.\n")

    def test_parse_rejects_invalid_columns(self):
        for raw in ("bad_column\n", "name\tone\textra\n", "good_tool\t\n"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse(raw)

    def test_evidence_has_explicit_scope_and_time(self):
        with tempfile.TemporaryDirectory() as dirname:
            p = Path(dirname) / "checks.json"
            p.write_text(json.dumps({"schema_version": 1, "checks": {
                "read_file": {"result": "verificada", "checked_at": DATE, "scope": "Un fixture sintético"}
            }}))
            checked = read_evidence(p, {"read_file"})
            snap = build(SAMPLE, DATE, checked)
            self.assertEqual(snap["tools"][0]["verification"]["result"], "verificada")
            self.assertEqual(snap["tools"][1]["verification"]["result"], "sin_prueba")

    def test_unknown_or_forged_evidence_rejected(self):
        with tempfile.TemporaryDirectory() as dirname:
            p = Path(dirname) / "checks.json"
            p.write_text(json.dumps({"schema_version": 1, "checks": {
                "unknown": {"result": "verificada", "checked_at": DATE, "scope": "No existe"}
            }}))
            with self.assertRaises(ValueError):
                read_evidence(p, {"read_file"})
            p.write_text(json.dumps({"schema_version": 1, "checks": {
                "read_file": {"result": "all_good", "checked_at": DATE, "scope": "Inventada"}
            }}))
            with self.assertRaises(ValueError):
                read_evidence(p, {"read_file"})

    def test_timezone_is_mandatory(self):
        with self.assertRaisesRegex(ValueError, "zona horaria"):
            build(SAMPLE, "2026-11-19T06:00:00")

    def test_diffs_added_removed_and_changed(self):
        before = build(SAMPLE, DATE)
        after = build("read_file\tRead files.\nnew_tool\tNew function.\n", DATE)
        changes = diff(before, after)
        self.assertEqual(changes["added"], ["new_tool"])
        self.assertEqual(changes["removed"], ["debian_gui_fixture_status"])
        self.assertEqual(changes["description_changed"], ["read_file"])

    def test_previous_variant_is_supported(self):
        legacy = {"tools": [{"name": "read_file", "declared_description": "Read a file safely."}]}
        self.assertEqual(diff(legacy, build("read_file\tRead a file safely.\n", DATE))["description_changed"], [])

    def test_report_lists_tools_and_verification_scope(self):
        checked = {"read_file": {"result": "verificada", "checked_at": DATE, "scope": "Solo un fixture"}}
        report = markdown(build(SAMPLE, DATE, checked), {"added": [], "removed": [], "description_changed": []})
        self.assertIn("read_file", report)
        self.assertIn("debian_gui_fixture_status", report)
        self.assertIn("Solo un fixture", report)
        self.assertIn("No probada", report)

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as dirname:
            src, dst = Path(dirname) / "sample.tsv", Path(dirname) / "out"
            src.write_text(SAMPLE)
            with contextlib.redirect_stdout(io.StringIO()) as captured:
                run(["--input", str(src), "--output-dir", str(dst), "--captured-at", DATE, "--expected-count", "2"])
            self.assertEqual(json.loads(captured.getvalue())["status"], "dry-run")
            self.assertFalse(dst.exists())

    def test_explicit_write_and_readback(self):
        with tempfile.TemporaryDirectory() as dirname:
            src, dst = Path(dirname) / "sample.tsv", Path(dirname) / "out"
            src.write_text(SAMPLE)
            with contextlib.redirect_stdout(io.StringIO()):
                run(["--input", str(src), "--output-dir", str(dst), "--captured-at", DATE, "--expected-count", "2", "--write"])
            snap = json.loads((dst / "inventario-mcp.json").read_text())
            md = (dst / "inventario-mcp.md").read_text()
            self.assertEqual(snap["total"], 2)
            self.assertIn("read_file", md)
            self.assertEqual(stat.S_IMODE((dst / "inventario-mcp.json").stat().st_mode), 0o600)

    def test_fail_closed_on_missing_tools(self):
        with tempfile.TemporaryDirectory() as dirname:
            src, dst = Path(dirname) / "sample.tsv", Path(dirname) / "out"
            src.write_text(SAMPLE)
            with contextlib.redirect_stdout(io.StringIO()):
                run(["--input", str(src), "--output-dir", str(dst), "--captured-at", DATE, "--expected-count", "2", "--write"])
            src.write_text("read_file\tRead a file safely.\n")
            with self.assertRaisesRegex(ValueError, "bajas"):
                run(["--input", str(src), "--output-dir", str(dst), "--captured-at", DATE, "--write"])
            self.assertEqual(json.loads((dst / "inventario-mcp.json").read_text())["total"], 2)

    def test_fail_closed_on_incomplete_capture(self):
        with tempfile.TemporaryDirectory() as dirname:
            src = Path(dirname) / "sample.tsv"
            src.write_text(SAMPLE)
            with self.assertRaisesRegex(ValueError, "incompleta"):
                run(["--input", str(src), "--output-dir", str(Path(dirname) / "out"),
                     "--captured-at", DATE, "--expected-count", "3", "--write"])


if __name__ == "__main__":
    unittest.main()
