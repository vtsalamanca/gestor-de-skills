import importlib.util
from pathlib import Path
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'skills/bibliotecario-memoria/tools'
spec=importlib.util.spec_from_file_location('deploy_local',src/'deploy_local_bibliotecario.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestDeploy(unittest.TestCase):
 def test_existing_unchanged(self):
  with tempfile.TemporaryDirectory() as d:
   dst=Path(d)
   (dst/'interfaz_chat.py').write_text('import sys,json,uuid\n if action=="resume":')
   (dst/'resumen_trabajo.py').write_text('import recuperar_contexto\n"latest_revision":info["job"]["revision"]}')
   first=m.plan(src,dst)
   self.assertEqual(len(first),5)
   applied=m.apply(src,dst,dst/'backups')
   self.assertEqual(applied['status'],'applied')
   self.assertEqual(m.plan(src,dst),{})
 def test_unknown_version_rejected(self):
  with self.assertRaises(ValueError):m.patch_brief('no expected format')
  with self.assertRaises(ValueError):m.patch_interface('missing')
if __name__=='__main__':unittest.main()
