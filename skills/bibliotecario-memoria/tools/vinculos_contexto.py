"""Alias de ámbito por expediente; no modifica archivos ni crea asociaciones implícitas."""
from __future__ import annotations
import sqlite3
from contextlib import closing
import unicodedata
from pathlib import Path

SCHEMA="""CREATE TABLE IF NOT EXISTS work_aliases (
    alias TEXT NOT NULL, work_id TEXT NOT NULL,
    confirmed INTEGER NOT NULL CHECK(confirmed IN (0,1)),
    source TEXT NOT NULL CHECK(source IN ('explicit','project_rule')),
    PRIMARY KEY(alias,work_id))"""

def normal(text):
    return "".join(c for c in unicodedata.normalize("NFKD",str(text).strip().casefold()) if not unicodedata.combining(c))

def lookup(index_path,scope):
    path=Path(index_path)
    if not path.is_file():return set()
    with closing(sqlite3.connect(path.resolve().as_uri()+"?mode=ro",uri=True)) as db:
        if db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='work_aliases'").fetchone() is None:
            return set()
        return {work for alias,work in db.execute("SELECT alias,work_id FROM work_aliases WHERE confirmed=1")
                if normal(alias)==normal(scope)}

def confirmed(index_path):
    path=Path(index_path)
    if not path.is_file():return []
    with closing(sqlite3.connect(path.resolve().as_uri()+"?mode=ro",uri=True)) as db:
        if db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='work_aliases'").fetchone() is None:
            return []
        return [(alias,work) for alias,work in db.execute(
            "SELECT alias,work_id FROM work_aliases WHERE confirmed=1")]

def bind(index_path,alias,work_id,confirmed=True):
    if not isinstance(alias,str) or not 2<=len(alias)<=120 or "\x00" in alias:
        raise ValueError("invalid_alias")
    if not isinstance(work_id,str) or len(work_id)<6:
        raise ValueError("invalid_work")
    with closing(sqlite3.connect(index_path,timeout=10)) as db:
        db.execute(SCHEMA)
        db.execute("""INSERT INTO work_aliases(alias,work_id,confirmed,source)
                    VALUES (?,?,?,'explicit')
                    ON CONFLICT(alias,work_id) DO UPDATE SET confirmed=excluded.confirmed""",
                   (normal(alias),work_id,int(confirmed)))
        db.commit()
