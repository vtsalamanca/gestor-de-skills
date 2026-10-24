import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from scripts.postflight_plugin_release import check


class PostflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.archive = Path(self.tmp.name) / 'canonical.zip'
        self.contents = {'.codex-plugin/plugin.json': json.dumps({'name': 'gestor-de-skills', 'version': '0.4.32'}), 'skills/bibliotecario-memoria/SKILL.md': 'real verified content'}
        with zipfile.ZipFile(self.archive, 'w') as archive:
            for name, body in self.contents.items():
                archive.writestr(name, body)
        self.observation = {'plugin': {'plugin_id':'plugins_example', 'current_release_id':'pluginrel_example','scope':'USER','discoverability':'PRIVATE','version':'0.4.32'}, 'files':[{'path':name} for name in self.contents], 'contents':dict(self.contents), 'next_offset':None, 'missing_paths':[], 'size_limited_paths':[]}

    def test_identical_release(self):
        self.assertEqual(check(self.archive, self.observation)['files'], 2)

    def test_omitted_marketplace_detected(self):
        self.observation['files'].append({'path':'.agents/plugins/marketplace.json'})
        with self.assertRaisesRegex(ValueError, 'FILE_INVENTORY_MISMATCH'):
            check(self.archive, self.observation)

    def test_content_changes_detected(self):
        self.observation['contents']['skills/bibliotecario-memoria/SKILL.md'] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'CONTENT_MISMATCH'):
            check(self.archive, self.observation)

    def test_incomplete_read_detected(self):
        del self.observation['contents']['skills/bibliotecario-memoria/SKILL.md']
        with self.assertRaisesRegex(ValueError, 'INCOMPLETE_REMOTE_CONTENTS'):
            check(self.archive, self.observation)

    def test_privacy_changed_detected(self):
        self.observation['plugin']['discoverability'] = 'LISTED'
        with self.assertRaisesRegex(ValueError, 'PLUGIN_IDENTITY_OR_PRIVACY_MISMATCH'):
            check(self.archive, self.observation)


if __name__ == '__main__':
    unittest.main()
