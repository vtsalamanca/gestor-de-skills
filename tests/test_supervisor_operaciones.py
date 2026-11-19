"""Pruebas SQLite de idempotencia y recuperación; sin efectos externos."""
import importlib.util
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"skills/control-laboratorio/tools/supervisor_operaciones.py"
SPEC=importlib.util.spec_from_file_location("supervisor_operaciones",SOURCE)
mod=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)
A="a"*64
B="b"*64

class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.db=Path(self.tmp.name)/"private/operations.sqlite3"
        self.ledger=mod.Ledger(self.db)

    def test_started_success_idempotent_and_conflicts(self):
        l=self.ledger
        self.assertEqual(l.begin("task-1","write",A),"started")
        self.assertEqual(l.begin("task-1","write",A),"requires_reconciliation")
        self.assertEqual(l.begin("task-1","write",B),"fingerprint_conflict")
        self.assertEqual(l.complete("task-1",B),"succeeded")
        self.assertEqual(l.begin("task-1","write",A),"already_succeeded")
        self.assertEqual(l.complete("task-1",B),"already_succeeded")
        self.assertEqual(l.complete("task-1",A),"requires_reconciliation")
        self.assertEqual(l.status("task-1")[0]["attempts"],1)

    def test_lost_reply_does_not_duplicate(self):
        l=self.ledger
        self.assertEqual(l.begin("task-2","external",A),"started")
        self.assertEqual(mod.Ledger(self.db).begin("task-2","external",A),"requires_reconciliation")
        self.assertEqual(l.unknown("task-2"),"unknown")
        self.assertEqual(l.begin("task-2","external",A),"requires_reconciliation")
        self.assertEqual(l.reconcile("task-2","applied",B),"succeeded")
        self.assertEqual(l.begin("task-2","external",A),"already_succeeded")

    def test_proof_needed_before_reconciled_retry(self):
        l=self.ledger
        l.begin("task-3","write",A)
        l.unknown("task-3")
        self.assertEqual(l.reconcile("task-3","not_applied",B),"not_applied")
        self.assertEqual(l.begin("task-3","write",A),"requires_reconciliation")
        self.assertEqual(l.begin("task-3","write",A,allow_reconciled_retry=True),"started_after_reconciliation")
        self.assertEqual(l.status("task-3")[0]["attempts"],2)
        self.assertEqual(l.complete("task-3",B),"succeeded")

    def test_bad_keys_and_missing_operations(self):
        l=self.ledger
        for key in ("../evil","", "x y","x"*100,"a/b"):
            with self.subTest(key=key),self.assertRaises(ValueError):
                l.begin(key,"write",A)
        with self.assertRaises(ValueError):
            l.begin("t","write","wrong")
        with self.assertRaises(ValueError):
            l.begin("t","root",A)
        with self.assertRaises(KeyError):
            l.complete("unknown",B)

    def test_permissions_and_restore_drill(self):
        l=self.ledger
        l.begin("task-restore","read",A)
        l.complete("task-restore",B)
        self.assertEqual(self.db.stat().st_mode&0o777,0o600)
        self.assertEqual(self.db.parent.stat().st_mode&0o777,0o700)
        restored=Path(self.tmp.name)/"restored.sqlite3"
        with sqlite3.connect(self.db) as source, sqlite3.connect(restored) as dest:
            source.backup(dest)
        self.assertEqual(sqlite3.connect(restored).execute("PRAGMA integrity_check").fetchone()[0],"ok")
        self.assertEqual(sqlite3.connect(restored).execute(
            "SELECT state FROM operations WHERE key='task-restore'").fetchone()[0],"succeeded")

    def test_symlink_rejected(self):
        if not hasattr(Path,"symlink_to"):
            self.skipTest("no symlink")
        link=Path(self.tmp.name)/"linked.sqlite3"
        link.symlink_to(self.db)
        with self.assertRaises(ValueError):
            mod.Ledger(link)

    def test_concurrent_claim_only_one_starts(self):
        from concurrent.futures import ThreadPoolExecutor
        def claim(_):
            return mod.Ledger(self.db).begin("shared-job","external",A)
        with ThreadPoolExecutor(max_workers=8) as pool:
            outcomes=list(pool.map(claim,range(8)))
        self.assertEqual(outcomes.count("started"),1)
        self.assertEqual(outcomes.count("requires_reconciliation"),7)
        self.assertEqual(self.ledger.status("shared-job")[0]["attempts"],1)

    def test_cli_exit_code_on_uncertainty(self):
        cmd=[sys.executable,str(SOURCE),"--db",str(self.db),
             "begin","--key","testcli","--kind","write","--request-sha",A]
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=4)
        self.assertEqual(p.returncode,0,p.stderr)
        repeated=subprocess.run(cmd,capture_output=True,text=True,timeout=4)
        self.assertEqual(repeated.returncode,3,repeated.stderr)
        self.assertIn("requires_reconciliation",repeated.stdout)

if __name__=="__main__":
    unittest.main()
