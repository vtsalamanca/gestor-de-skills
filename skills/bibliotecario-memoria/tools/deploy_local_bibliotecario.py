#!/usr/bin/env python3
"""Despliegue idempotente y conservador de extensiones del Bibliotecario.

Por defecto solo previsualiza, --apply requiere aprobación del lote. Crea
copias privadas antes de tocar módulos locales, sin reiniciar servicios.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil

MAPPING={
 "busqueda_fts5.py":"busqueda.py",
 "knowledge_status.py":"knowledge_status.py",
 "vinculos_contexto.py":"vinculos_contexto.py",
}

def patch_interface(text):
    if 'if action=="knowledge_transition":' in text:return text
    needle=' if action=="resume":'
    if text.count(needle)!=1:raise ValueError("interface_unknown_version")
    text=text.replace('import sys,json,uuid','import sys,json,uuid\nimport knowledge_status',1)
    return text.replace(needle,''' if action=="knowledge_pending":
  return knowledge_status.pending(b.DB,req["work"],limit=req.get("limit",10))
 if action=="knowledge_transition":
  return knowledge_status.transition(b.DB,req["work"],req["source_revision"],req["source_ordinal"],
                                    req["status"],req["evidence_revision"],req["evidence_ordinal"],
                                    req["operation_id"])
'''+needle,1)

def patch_brief(text):
    if '"pending_knowledge":' in text:return text
    if text.count('"latest_revision":info["job"]["revision"]}')!=1:raise ValueError("brief_unknown_version")
    text=text.replace('import recuperar_contexto','import recuperar_contexto\nimport knowledge_status\nimport bibliotecario as b',1)
    return text.replace('"latest_revision":info["job"]["revision"]}',
     '"latest_revision":info["job"]["revision"],\n         "pending_knowledge":knowledge_status.pending(b.DB,work,limit=10)}',1)

def plan(source_dir,target_dir):
    source_dir=Path(source_dir);target_dir=Path(target_dir)
    if not target_dir.is_dir() or target_dir.is_symlink():
        raise ValueError("invalid_target")
    changes={}
    for source,target in MAPPING.items():
        raw=(source_dir/source).read_bytes()
        path=target_dir/target
        if path.is_symlink():raise ValueError("symlink_destination")
        if not path.exists() or path.read_bytes()!=raw:changes[target]=raw
    for name,transform in [('interfaz_chat.py',patch_interface),('resumen_trabajo.py',patch_brief)]:
        path=target_dir/name
        if not path.is_file() or path.is_symlink():raise ValueError("unsafe_existing_module")
        old=path.read_text()
        new=transform(old)
        if new!=old:changes[name]=new.encode()
    return changes

def apply(source_dir,target_dir,backup_root):
    target_dir=Path(target_dir)
    changes=plan(source_dir,target_dir)
    if not changes:return {"status":"already_current","files":0}
    backup_root=Path(backup_root)
    if backup_root.is_symlink():raise ValueError("unsafe_backup")
    backup_root.mkdir(mode=0o700,parents=True,exist_ok=True)
    os.chmod(backup_root,0o700)
    bundle=backup_root/("bibliotecario-"+datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    if bundle.exists():raise FileExistsError("backup_collision")
    bundle.mkdir(mode=0o700)
    for name in changes:
        existing=target_dir/name
        if existing.exists():
            shutil.copyfile(existing,bundle/name)
            (bundle/name).chmod(0o600)
    for name,raw in changes.items():
        target=target_dir/name
        tmp=target.with_name(target.name+".new-ext")
        flags=os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0)
        with os.fdopen(os.open(tmp,flags,0o600),'wb') as f:
            f.write(raw);f.flush();os.fsync(f.fileno())
        os.replace(tmp,target)
    return {"status":"applied","files":len(changes),"backup_dir":str(bundle)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--target',type=Path,default=Path.home()/'bibliotecario-piloto')
    p.add_argument('--backup-root',type=Path,default=Path.home()/'.local/state/control-laboratorio/backup-bibliotecario')
    p.add_argument('--apply',action='store_true')
    args=p.parse_args()
    source=Path(__file__).resolve().parent
    if args.apply:
        outcome=apply(source,args.target,args.backup_root)
    else:
        outcome={"status":"dry_run","would_change":sorted(plan(source,args.target))}
    print(json.dumps(outcome,ensure_ascii=False))
if __name__=='__main__':main()
