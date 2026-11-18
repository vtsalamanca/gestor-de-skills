import io,json,tempfile,unittest,zipfile
from pathlib import Path
from scripts.preflight_plugin_upload import validate
from scripts.package_plugin import EXPECTED_SKILLS
class PreflightUpload(unittest.TestCase):
 def archive(self,marketplace=False):
  t=tempfile.TemporaryDirectory();p=Path(t.name)/'plugin.zip'
  with zipfile.ZipFile(p,'w') as z:
   z.writestr('.codex-plugin/plugin.json',json.dumps({'name':'gestor-de-skills','version':'0.4.29'}))
   for name in sorted(EXPECTED_SKILLS):
    z.writestr('skills/'+name+'/SKILL.md','---\nname: '+name+'\n---')
   if marketplace:z.writestr('.agents/plugins/marketplace.json','{}')
  return t,p
 def test_good(self):
  t,p=self.archive();self.addCleanup(t.cleanup);self.assertTrue(validate(p)['valid'])
 def test_marketplace_fails_closed(self):
  t,p=self.archive(True);self.addCleanup(t.cleanup)
  with self.assertRaisesRegex(ValueError,'MARKETPLACE_IN_UPLOAD_PROHIBITED'):validate(p)
 def test_digest_guard(self):
  t,p=self.archive();self.addCleanup(t.cleanup)
  with self.assertRaisesRegex(ValueError,'ZIP_SHA256_MISMATCH'):validate(p,'0'*64)
if __name__=='__main__':unittest.main()
