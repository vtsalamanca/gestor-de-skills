"""Dos jornadas con datos sintéticos: nunca abren Educamos ni InfoJobs."""
from __future__ import annotations
import datetime as dt
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock
from zoneinfo import ZoneInfo

ROOT=Path(__file__).resolve().parents[1]
TOOLS=ROOT/"skills/control-laboratorio/tools"
sys.path.insert(0,str(TOOLS))
spec=importlib.util.spec_from_file_location("supervision_diaria",TOOLS/"supervision_diaria.py")
s=importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)
from supervisor_operaciones import Ledger

TZ=ZoneInfo("Europe/Madrid")
DAY=dt.datetime.now(TZ).date()

class DailyTests(unittest.TestCase):
    def setUp(self):
        t=tempfile.TemporaryDirectory()
        self.addCleanup(t.cleanup)
        self.root=Path(t.name)
        self.state=self.root/"state"
        self.script=self.root/"worker.py"
        self.script.write_text("print('fixture')\n")
        self.report=self.root/"result.json"
        self.calls=0
        self.cfg={"script":self.script,"report":self.report,"timeout":1,
                  "allowed":("completo",),"timestamp":"fecha"}
        self.now_ns=time.time_ns()

    def report_ok(self):
        data={"estado":"completo","fecha":dt.datetime.now(TZ).isoformat()}
        self.report.write_text(json.dumps(data))
        os.chmod(self.report,0o600)

    def runner_ok(self,*args,**kwargs):
        self.calls+=1
        self.report_ok()
        return subprocess.CompletedProcess([],0)

    def execute_fixture(self,runner=None):
        return s.execute("educamos",day=DAY,state_dir=self.state,config=self.cfg,
                         now_ns=self.now_ns,runner=runner or self.runner_ok)

    def test_one_execution_and_second_skipped(self):
        self.assertEqual(self.execute_fixture()["state"],"verified")
        self.assertEqual(self.execute_fixture()["state"],"already_succeeded")
        self.assertEqual(self.calls,1)
        self.assertEqual(Ledger(self.state/"operaciones.sqlite3").status()[0]["state"],"succeeded")

    def test_missing_report_keeps_unknown_without_retry(self):
        def missing(*args,**kwargs):
            self.calls+=1
            return subprocess.CompletedProcess([],0)
        self.assertEqual(self.execute_fixture(missing)["state"],"report_not_verified")
        self.assertEqual(self.execute_fixture()["state"],"needs_reconciliation")
        self.assertEqual(self.calls,1)

    def test_nonzero_exit_and_timeout_block_retry(self):
        def err(*args,**kwargs):
            self.calls+=1
            return subprocess.CompletedProcess([],2)
        self.assertEqual(self.execute_fixture(err)["state"],"job_returned_error")
        self.assertEqual(self.execute_fixture()["state"],"needs_reconciliation")
        self.assertEqual(self.calls,1)
        self.assertEqual(s.execute("educamos",day=DAY,state_dir=self.root/"second",
                                 config=self.cfg,now_ns=self.now_ns,
                                 runner=lambda *a,**k: (_ for _ in ()).throw(
                                     subprocess.TimeoutExpired("fixture",1)))["state"],"execution_uncertain")

    def test_crash_after_side_effect_reconciles_without_rerun(self):
        self.state.mkdir(mode=0o700)
        key=f"daily:educamos:{DAY.isoformat()}"
        request=s.digest(("educamos|"+str(self.script.resolve())+"|"+s.digest(self.script.read_bytes())).encode())
        ledger=Ledger(self.state/"operaciones.sqlite3")
        self.assertEqual(ledger.begin(key,"write",request),"started")
        self.report_ok()
        self.assertEqual(self.execute_fixture()["state"],"recovered_succeeded")
        self.assertEqual(self.calls,0)

    def test_old_report_and_symlink_not_accepted(self):
        self.report_ok()
        past=self.now_ns/1e9-120
        os.utime(self.report,(past,past))
        self.assertEqual(self.execute_fixture(lambda *a,**k: subprocess.CompletedProcess([],0))["state"],"report_not_verified")
        another=self.root/"third"
        other=self.root/"link.json"
        other.symlink_to(self.report)
        cfg={**self.cfg,"report":other}
        r=s.execute("educamos",day=DAY,state_dir=another,config=cfg,now_ns=self.now_ns,
                    runner=lambda *a,**k: subprocess.CompletedProcess([],0))
        self.assertEqual(r["state"],"report_not_verified")

    def test_changed_script_fingerprint_conflict(self):
        self.assertEqual(self.execute_fixture()["state"],"verified")
        self.script.write_text("print('changed fixture')\n")
        self.assertEqual(self.execute_fixture()["state"],"fingerprint_conflict")
        self.assertEqual(self.calls,1)

    def test_different_dates_not_dependent(self):
        self.assertEqual(self.execute_fixture()["state"],"verified")
        another=s.execute("educamos",day=DAY+dt.timedelta(days=1),state_dir=self.state,
                          config=self.cfg,now_ns=self.now_ns,
                          runner=lambda *a,**k: subprocess.CompletedProcess([],0))
        self.assertEqual(another["state"],"report_not_verified")

    def test_preflight_runs_inside_claim_and_only_once(self):
        preparer=self.root/"preparer.py"
        preparer.write_text("print('fixture')\n")
        self.cfg["preflight"]=preparer
        self.cfg["preflight_timeout"]=1
        seen=[]
        def mock_run(cmd,**kwargs):
            seen.append(Path(cmd[1]).name)
            if Path(cmd[1])==self.script:
                self.report_ok()
                return subprocess.CompletedProcess([],0)
            return subprocess.CompletedProcess([],1)
        self.assertEqual(self.execute_fixture(mock_run)["state"],"verified")
        self.assertEqual(self.execute_fixture(mock_run)["state"],"already_succeeded")
        self.assertEqual(seen,["preparer.py","worker.py"])

    def test_employment_partial_report_and_preflight(self):
        self.cfg["allowed"]=("completo","parcial")
        self.cfg["timestamp"]="fecha_utc"
        preparer=self.root/"preparer.py"
        preparer.write_text("print('test')\n")
        self.cfg["preflight"]=preparer
        paths=[]
        def fake(cmd,**kwargs):
            paths.append(Path(cmd[1]).name)
            if Path(cmd[1])==self.script:
                self.report.write_text(json.dumps({
                    "estado":"parcial",
                    "fecha_utc":dt.datetime.now(TZ).isoformat()
                }))
                os.chmod(self.report,0o600)
            return subprocess.CompletedProcess([],0)
        outcome=s.execute("buscar-curro",day=DAY,state_dir=self.state,
                          config=self.cfg,now_ns=self.now_ns,runner=fake)
        self.assertEqual(outcome["state"],"verified")
        self.assertEqual(paths,["preparer.py","worker.py"])
        self.assertEqual(s.execute("buscar-curro",day=DAY,state_dir=self.state,
                                   config=self.cfg,now_ns=self.now_ns,runner=fake)["state"],"already_succeeded")
        self.assertEqual(len(paths),2)

    def test_invalid_job_never_runs(self):
        with self.assertRaises(ValueError):
            s.execute("other",state_dir=self.state,config=self.cfg)

if __name__=="__main__":
    unittest.main()
