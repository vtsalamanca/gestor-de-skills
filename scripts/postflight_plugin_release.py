"""Validate a live Plugin Creator get_plugin_files export against a canonical ZIP.

Input JSON must be the structured get_plugin_files result with full read_paths contents.
This tool does not contact the plugin service and never modifies remote releases.
"""
import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path


def check(archive_path, observation):
    if 'result' in observation and isinstance(observation['result'], dict):
        observation = observation['result']
    plugin = observation.get('plugin') or {}
    if plugin.get('scope') != 'USER' or plugin.get('discoverability') != 'PRIVATE':
        raise ValueError('PLUGIN_IDENTITY_OR_PRIVACY_MISMATCH')
    if not plugin.get('plugin_id') or not plugin.get('current_release_id'):
        raise ValueError('PLUGIN_OR_RELEASE_ID_MISSING')
    files = observation.get('files') or []
    names = [item['path'] for item in files]
    if len(names) != len(set(names)):
        raise ValueError('DUPLICATE_REMOTE_PATHS')
    if observation.get('next_offset') is not None:
        raise ValueError('INCOMPLETE_FILE_LIST')
    if observation.get('missing_paths') or observation.get('size_limited_paths'):
        raise ValueError('UNREADABLE_REMOTE_FILES')
    with zipfile.ZipFile(archive_path) as z:
        expected = set(z.namelist())
        if set(names) != expected:
            raise ValueError('FILE_INVENTORY_MISMATCH')
        contents = observation.get('contents') or {}
        if set(contents) != expected:
            raise ValueError('INCOMPLETE_REMOTE_CONTENTS')
        for name in expected:
            item = contents[name]
            if isinstance(item, dict):
                item = item.get('content')
            if not isinstance(item, str):
                raise ValueError('NON_TEXT_REMOTE_CONTENT: ' + name)
            if hashlib.sha256(item.encode('utf-8')).digest() != hashlib.sha256(z.read(name)).digest():
                raise ValueError('CONTENT_MISMATCH: ' + name)
        manifest = json.loads(z.read('.codex-plugin/plugin.json'))
        # The service may bump a previously unchanged version; compare names and contents
        # strictly unless an explicitly generated new canonical archive is supplied.
        if plugin.get('version') != manifest.get('version'):
            raise ValueError('VERSION_MISMATCH')
    return {'valid': True, 'plugin_id': plugin['plugin_id'], 'release_id': plugin['current_release_id'], 'version': plugin['version'], 'files': len(expected), 'skills': sum(x.endswith('/SKILL.md') for x in expected)}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('archive')
    p.add_argument('observation_json')
    a = p.parse_args()
    try:
        print(json.dumps(check(a.archive, json.loads(Path(a.observation_json).read_text(encoding='utf-8')))))
    except (ValueError, OSError, zipfile.BadZipFile, KeyError, TypeError, json.JSONDecodeError) as e:
        print('BLOCK_RELEASE: ' + str(e), file=sys.stderr)
        sys.exit(2)
