import importlib.util
import sqlite3
from contextlib import closing
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]/'skills/control-laboratorio/tools'
def load(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/(name+'.py'))
 obj=importlib.util.module_from_spec(spec)
 spec.loader.exec_module(obj)
 return obj

class TestRecuperacion(unittest.TestCase):
 def test_mcp_classifies_without_automatic_restart(self):
  m=load('mcp_sesion_diagnostico')
  self.assertEqual(m.classify(True,'session-terminated'),'client_or_transport_suspected')
  self.assertEqual(m.classify(False,'none'),'server_unavailable')
  calls=[]
  def runner(args,timeout=8):
   calls.append(args)
   return 0,'ActiveState=active\nSubState=running\nNRestarts=0' if args[0]=='systemctl' else 'session terminated'
  x=m.diagnose('session-terminated',runner=runner)
  self.assertEqual(x['diagnosis'],'client_or_transport_suspected')
  self.assertEqual(x['journal_pattern_counts']['session'],1)
  self.assertFalse(any('restart' in x[:3] for x in calls))
 def test_sqlite_restore_isolated(self):
  m=load('ensayo_restauracion')
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'source.sqlite'
   with closing(sqlite3.connect(path)) as db:
    db.execute('create table testdata (value int)')
    db.execute('insert into testdata values (1)'); db.commit()
   first=path.read_bytes()
   info=m.run([path])
   self.assertEqual(info['checks'][0]['status'],'verified_sqlite_copy')
   self.assertEqual(info['full_vm_restore'],'not_certified')
   self.assertEqual(path.read_bytes(),first)
 def test_unknown_never_guessed(self):
  m=load('supervisor_revision')
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'ledger.db'
   with closing(sqlite3.connect(p)) as c:
    c.execute('create table operations(key text,state text,created_at text)')
    c.execute("insert into operations values('daily:educamos:2026-11-21','unknown','2026-11-21T12:45:09+00:00')");c.commit()
   x=m.review(p,{'educamos':{'report':'/no/such/report'}},lambda *args:None)
   self.assertEqual(x[0]['evidence'],'missing_or_stale')
   self.assertIsNone(x[0]['proof_sha'])
 def test_proof_failed_requires_independent_correlated_log(self):
  m=load('supervisor_revision')
  key='daily:educamos:2026-11-20'
  created='2026-11-20T12:45:09+00:00'
  fixture="""{"job": "educamos", "state": "job_returned_error", "exit": 3}
educamos-diario-laboratorio.service: Main process exited, code=exited, status=3/NOTIMPLEMENTED
educamos-diario-laboratorio.service: Failed with result 'exit-code'."""
  assert len(m.proof_failed_run(key,created,lambda _:fixture))==64
  self.assertIsNone(m.proof_failed_run(key,created,lambda _:fixture.replace('job_returned_error','verified')))
  self.assertIsNone(m.proof_failed_run(key,created,lambda _:fixture.replace('Failed with result','Succeeded with result')))
  self.assertIsNone(m.proof_failed_run('daily:buscar-curro:2026-11-20',created,lambda _:fixture))
  self.assertIsNone(m.proof_failed_run(key,'2026-11-19T12:45:09+00:00',lambda _:fixture))

if __name__=='__main__':unittest.main()
