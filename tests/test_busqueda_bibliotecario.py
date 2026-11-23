"""Pruebas sintéticas contra la copia canónica de búsqueda; no abre memoria personal."""
from pathlib import Path
import importlib.util
import sqlite3
import sys
import tempfile
import types
import unittest

MODULE=Path(__file__).resolve().parents[1]/'skills/bibliotecario-memoria/tools/busqueda_fts5.py'

class TestFTS(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.db=Path(self.tmp.name)/'fixture.sqlite3'
        c=sqlite3.connect(self.db)
        c.executescript("""CREATE TABLE jobs(id TEXT,title TEXT,status TEXT,revision INT,updated TEXT);
                           CREATE TABLE events(job_id TEXT, detail TEXT);""")
        c.executemany('INSERT INTO jobs VALUES (?,?,?,?,?)',[
            ('a','Gestor de Skills — registro','active',2,'2026-11-20'),
            ('b','Nota incidental','active',3,'2026-11-23'),
            ('c','Buscar-Curro — empleo','active',5,'2026-11-21'),
            ('d','Goose — interfaz','active',4,'2026-11-23')])
        c.executemany('INSERT INTO events VALUES (?,?)',[
            ('b','Gestor de Skills mencionado de paso'),
            ('c','InfoJobs candidatura'),
            ('d','InfoJobs comparación')])
        c.commit();c.close()
        self.old=sys.modules.get('bibliotecario')
        sys.modules['bibliotecario']=types.SimpleNamespace(DB=self.db)
        spec=importlib.util.spec_from_file_location('busqueda_fts_fixture',MODULE)
        self.module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
    def tearDown(self):
        if self.old is None:sys.modules.pop('bibliotecario',None)
        else:sys.modules['bibliotecario']=self.old
        self.tmp.cleanup()
    def test_title_over_event(self):
        self.assertEqual(self.module.find('gestor de skills')[0]['id'],'a')
    def test_scoped_project(self):
        self.assertEqual([j['id'] for j in self.module.find('InfoJobs',scope='Buscar-Curro')],['c'])
    def test_no_scope_guessing(self):
        self.assertEqual(self.module.find('InfoJobs',scope='Unknown'),[])
    def test_literal_fts_injection_resistance(self):
        self.assertEqual(self.module.find('" OR *'),[])
    def test_read_only_db(self):
        connection=sqlite3.connect(self.db)
        before=connection.execute('select name from sqlite_master order by name').fetchall()
        self.module.find('Skills')
        after=connection.execute('select name from sqlite_master order by name').fetchall()
        connection.close()
        self.assertEqual(before,after)
if __name__=='__main__':unittest.main()
