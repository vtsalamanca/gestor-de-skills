"""Strict fail-closed verification of a Plugin Creator ZIP before upload."""
import argparse, hashlib, json, re, sys, zipfile
from pathlib import PurePosixPath, Path

def validate(path, expected_sha=None):
    data=Path(path).read_bytes()
    digest=hashlib.sha256(data).hexdigest()
    if expected_sha and digest.lower()!=expected_sha.lower():raise ValueError('ZIP_SHA256_MISMATCH')
    with zipfile.ZipFile(path) as archive:
        names=archive.namelist()
        if len(names)!=len(set(names)):raise ValueError('DUPLICATE_ARCHIVE_MEMBERS')
        if any(n.endswith('/') or n.startswith('/') or '..' in PurePosixPath(n).parts or '\\' in n for n in names):raise ValueError('UNSAFE_ARCHIVE_PATH')
        if '.agents/plugins/marketplace.json' in names or any('marketplace.json' in n for n in names):raise ValueError('MARKETPLACE_IN_UPLOAD_PROHIBITED')
        if '.codex-plugin/plugin.json' not in names:raise ValueError('PLUGIN_MANIFEST_MISSING')
        manifest=json.loads(archive.read('.codex-plugin/plugin.json'))
        if manifest.get('name')!='gestor-de-skills' or not re.fullmatch(r'\\d+\\.\\d+\\.\\d+',manifest.get('version','')):raise ValueError('INVALID_PLUGIN_IDENTITY_OR_VERSION')
        skills={n.split('/')[1] for n in names if n.startswith('skills/') and n.endswith('/SKILL.md') and len(n.split('/'))==3}
        if len(skills)!=9 or 'bibliotecario-memoria' not in skills:raise ValueError('INCOMPLETE_SKILL_ARCHIVE')
        if not all(n=='README.md' or n=='.codex-plugin/plugin.json' or n.startswith('skills/') for n in names):raise ValueError('UNEXPECTED_ROOT_MEMBER')
    return {'sha256':digest,'version':manifest['version'],'skills':len(skills),'files':len(names),'valid':True}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('archive');parser.add_argument('--sha256');args=parser.parse_args()
    try:print(json.dumps(validate(args.archive,args.sha256)))
    except (ValueError,OSError,zipfile.BadZipFile,json.JSONDecodeError) as e:
        print('BLOCK_PUBLICATION: '+str(e),file=sys.stderr);sys.exit(2)
