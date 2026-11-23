"""Regresión sin acceder a proyectos o bases personales."""
import importlib.util
import json
from pathlib import Path
import sqlite3
from contextlib import closing
import tempfile
import unittest

MODULE=Path(__file__).resolve().parents[1]/'skills/bibliotecario-memoria/tools/knowledge_status.py'
spec=importlib.util.spec_from_file_location('knowledge_test',MODULE)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class TestKnowledgeStatus(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  self.db=Path(self.tmp.name)/'data.db'
  with closing(sqlite3.connect(self.db)) as c:
   c.executescript("""CREATE TABLE jobs(id TEXT PRIMARY KEY, revision INT);
   CREATE TABLE checkpoints(job_id TEXT, revision INT,content TEXT);""")
   c.execute("INSERT INTO jobs VALUES ('w',4)")
   c.executemany("INSERT INTO checkpoints VALUES ('w',?,?)",[
    (2,json.dumps([{"kind":"next_action","text":"Probar FTS5"}])),
    (3,json.dumps([{"kind":"verified_result","text":"FTS5 ejecutado"}])),
    (4,json.dumps([{"kind":"next_action","text":"Homologar Firefox"},{"kind":"failure","text":"Todavía bloqueado"}]))])
   c.commit()
 def tearDown(self):self.tmp.cleanup()
 def test_legacy_read_no_schema_mutation(self):
  self.assertEqual(m.pending(self.db,'w')['open_count'],1)
  self.assertEqual(m.pending(self.db,'w')['historical_unreviewed_count'],1)
  with closing(sqlite3.connect(self.db)) as c:self.assertFalse(c.execute("select name from sqlite_master where name='knowledge_action_status'").fetchone())
 def test_proven_close_idempotent(self):
  op='cerrar-fts5-fixture'
  self.assertEqual(m.transition(self.db,'w',2,0,'resolved',3,0,op)['status'],'saved')
  self.assertEqual(m.transition(self.db,'w',2,0,'resolved',3,0,op)['status'],'duplicate')
  p=m.pending(self.db,'w')
  self.assertEqual(p['open_count'],1)
  self.assertIn('Homologar',p['pending_actions'][0]['text'])
 def test_no_proof_wrong_kind_or_early(self):
  with self.assertRaises(ValueError):m.transition(self.db,'w',2,0,'resolved',2,0,'bad-wrong-kind')
  with self.assertRaises(ValueError):m.transition(self.db,'w',2,0,'resolved',1,0,'bad-early')
  self.assertEqual(m.pending(self.db,'w')['open_count'],1)
  self.assertEqual(m.pending(self.db,'w')['historical_unreviewed_count'],1)
 def test_conflicting_operation_and_terminal(self):
  op='cerrar-probado'
  m.transition(self.db,'w',2,0,'resolved',3,0,op)
  with self.assertRaises(ValueError):m.transition(self.db,'w',2,0,'blocked',4,1,op)
  with self.assertRaises(ValueError):m.transition(self.db,'w',2,0,'blocked',4,1,'otro-op')
 def test_supersedes_with_new_action_only(self):
  with self.assertRaises(ValueError):
   m.transition(self.db,'w',2,0,'superseded',3,0,'bad-supersedes')
  result=m.transition(self.db,'w',2,0,'superseded',4,0,'reemplazo-justificado')
  self.assertEqual(result['status'],'saved')
  self.assertEqual(m.pending(self.db,'w')['historical_unreviewed_count'],0)
 def test_blocked_is_not_resolved(self):
  m.transition(self.db,'w',4,0,'blocked',4,1,'incidencia-firefox')
  p=m.pending(self.db,'w')
  self.assertEqual(p['blocked_count'],1)
  self.assertEqual(p['open_count'],0)
if __name__=='__main__':unittest.main()
