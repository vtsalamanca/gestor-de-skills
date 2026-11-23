#!/usr/bin/env python3
"""Ensayo aislado de restauración SQLite: no restaura ni reinicia la VM real."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
from contextlib import closing
import sqlite3
import tempfile

def clone_and_verify(source):
    source=Path(source)
    if not source.is_file() or source.is_symlink():
        raise ValueError("invalid_source")
    with tempfile.TemporaryDirectory(prefix="ensayo-restore-") as tmp:
        target=Path(tmp)/"restore.db"
        with closing(sqlite3.connect(source.resolve().as_uri()+"?mode=ro",uri=True,timeout=10)) as origin:
            with closing(sqlite3.connect(target)) as dest:
                origin.backup(dest)
        with closing(sqlite3.connect(target.resolve().as_uri()+"?mode=ro",uri=True)) as restored:
            check=restored.execute("PRAGMA integrity_check").fetchone()[0]
            tables=restored.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0]
        if check!="ok":raise ValueError("restoration_integrity_failed")
        return {"db":source.name,"status":"verified_sqlite_copy","tables":tables,
                "restored_sha256":hashlib.sha256(target.read_bytes()).hexdigest()}

def run(sources):
    return {"checks":[clone_and_verify(x) for x in sources],
            "full_vm_restore":"not_certified",
            "note":"Sin VirtualBox host, perfiles ni llaveros. El ensayo NO certifica recuperación total del sistema."}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("sources",nargs="+",type=Path,help="Bases SQLite explícitamente autorizadas.")
    print(json.dumps(run(p.parse_args().sources),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
