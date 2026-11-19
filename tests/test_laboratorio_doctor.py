"""Pruebas puras del diagnóstico; no manipulan el Debian real."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"skills/control-laboratorio/tools/laboratorio_doctor.py"
spec=importlib.util.spec_from_file_location("laboratorio_doctor",SRC)
doctor=importlib.util.module_from_spec(spec)
spec.loader.exec_module(doctor)

class DoctorTests(unittest.TestCase):
    def setUp(self):
        d=tempfile.TemporaryDirectory()
        self.addCleanup(d.cleanup)
        self.home=Path(d.name)
        self.audit=self.home/"utilidades/control-laboratorio"
        self.audit.mkdir(parents=True)
        self.skills=self.home/"proyectos/gestor-de-skills/skills/bibliotecario-memoria"
        self.skills.mkdir(parents=True)
        (self.skills/"SKILL.md").write_text("# Bibliotecario actualizado\n")
        self.evidence=b'{"checks":{"read":{"result":"verificada"}}}'
        self.report={"total":2,"tools":[{"name":"a"},{"name":"b"}],
                     "counts":{"homologada_en_alcance":2},
                     "sources":{"evidence_sha256":hashlib.sha256(self.evidence).hexdigest()}}
        self.write_fixture()

    def write_fixture(self):
        (self.audit/"evidencias.json").write_bytes(self.evidence)
        (self.audit/"auditoria-homologacion.json").write_text(json.dumps(self.report))

    def test_audit_hash_count_and_unique(self):
        self.assertEqual(doctor.check_audit(self.home)["status"],"ok")
        self.report["tools"].append({"name":"a"})
        self.write_fixture()
        self.assertEqual(doctor.check_audit(self.home)["status"],"error")
        self.report["tools"].pop()
        self.report["sources"]["evidence_sha256"]="0"*64
        self.write_fixture()
        self.assertEqual(doctor.check_audit(self.home)["status"],"error")

    def test_reduced_coverage_warns(self):
        self.report["counts"]={"homologada_en_alcance":1,"limitada_o_bloqueada":1}
        self.write_fixture()
        self.assertEqual(doctor.check_audit(self.home)["status"],"warning")

    def test_historical_docs_detected(self):
        (self.skills/"SKILL.md").write_text("El catálogo de 43 herramientas es antiguo")
        self.assertEqual(doctor.check_docs(self.home)["status"],"warning")
        (self.skills/"SKILL.md").write_text("Comprobar catálogo actual")
        self.assertEqual(doctor.check_docs(self.home)["status"],"ok")

    def test_last_trigger_future_and_old(self):
        with mock.patch.object(doctor,"command",return_value=(0,"LastTriggerUSec=Thu 2026-11-19 13:45:09 CET")):
            now=doctor.datetime(2026,11,20,0,0,tzinfo=doctor.timezone.utc)
            self.assertEqual(doctor.check_last_trigger("job.timer",now)["status"],"ok")
            past=doctor.datetime(2026,11,23,0,0,tzinfo=doctor.timezone.utc)
            self.assertEqual(doctor.check_last_trigger("job.timer",past)["status"],"warning")

    def test_last_success_requires_timestamp_and_exit_zero(self):
        response=("Result=success\nExecMainStatus=0\n"
                  "ExecMainExitTimestamp=Thu 2026-11-19 13:45:28 CET")
        now=doctor.datetime(2026,11,20,0,0,tzinfo=doctor.timezone.utc)
        with mock.patch.object(doctor,"command",return_value=(0,response)):
            d=doctor.check_job_completion("educamos-diario-laboratorio.service",now)
            self.assertEqual(d["status"],"ok")
            self.assertIn("downstream delivery unverified",d["detail"])
        with mock.patch.object(doctor,"command",return_value=(0,response.replace("Status=0","Status=1"))):
            self.assertEqual(doctor.check_job_completion("job.service",now)["status"],"warning")

    def test_report_private_and_no_execution(self):
        with mock.patch.object(doctor,"check_git",return_value=doctor.result("ok","git clean")):
            report=doctor.doctor(self.home,with_systemd=False)
        self.assertEqual(report["status"],"ok")
        self.assertFalse(report["automatic_repairs"])
        output=self.home/".local/state/control-laboratorio/doctor-ultimo.json"
        doctor.save_report(output,report)
        self.assertEqual(output.stat().st_mode&0o777,0o600)
        self.assertEqual(output.parent.stat().st_mode&0o777,0o700)
        self.assertEqual(json.loads(output.read_text())["status"],"ok")
        doctor.save_report(output,report)
        self.assertEqual(json.loads(output.read_text())["schema_version"],1)

    def test_symlink_report_rejected(self):
        destination=self.home/"doctor.json"
        destination.symlink_to(self.audit/"evidencias.json")
        with self.assertRaises(PermissionError):
            doctor.save_report(destination,{"safe":True})

if __name__=="__main__":
    unittest.main()
