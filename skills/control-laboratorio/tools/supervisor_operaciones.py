#!/usr/bin/env python3
"""Registro duradero de operaciones: sin ejecución automática ni reintentos ambiguos.

Guarda únicamente identificadores y SHA256, nunca argumentos, secretos ni salidas.
Una operación puede haberse realizado aunque su respuesta se pierda.
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sqlite3

KEY = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9._:-]{0,95}\Z")
SHA = re.compile(r"[a-f0-9]{64}\Z")
KINDS = {"read", "write", "external"}
SCHEMA = """CREATE TABLE IF NOT EXISTS operations (
    key TEXT PRIMARY KEY, kind TEXT NOT NULL, request_sha TEXT NOT NULL,
    state TEXT NOT NULL, proof_sha TEXT, created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL, attempts INTEGER NOT NULL DEFAULT 1
)"""

def stamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def valid(value, expression, field):
    if not isinstance(value, str) or not expression.fullmatch(value):
        raise ValueError("invalid " + field)
    return value

class Ledger:
    def __init__(self, db: Path):
        self.db = Path(db).expanduser().absolute()
        parent = self.db.parent
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            raise ValueError("unsafe parent directory")
        parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        if parent.stat().st_mode & 0o077:
            raise PermissionError("ledger directory is not private")
        if self.db.is_symlink():
            raise ValueError("database symlink rejected")
        old_umask = os.umask(0o077)
        try:
            with self.connection() as c:
                c.execute(SCHEMA)
        finally:
            os.umask(old_umask)
        if self.db.stat().st_mode & 0o077:
            raise PermissionError("ledger is not private")

    @contextmanager
    def connection(self):
        c = sqlite3.connect(str(self.db), timeout=5, isolation_level=None)
        try:
            c.execute("PRAGMA busy_timeout=5000")
            c.execute("PRAGMA synchronous=FULL")
            c.execute("PRAGMA journal_mode=WAL")
            yield c
        finally:
            c.close()

    def begin(self, key, kind, request_sha, allow_reconciled_retry=False):
        valid(key, KEY, "key")
        valid(request_sha, SHA, "request_sha")
        if kind not in KINDS:
            raise ValueError("invalid kind")
        with self.connection() as c:
            c.execute("BEGIN IMMEDIATE")
            row = c.execute("SELECT kind,request_sha,state,attempts FROM operations WHERE key=?", (key,)).fetchone()
            if row is None:
                c.execute("INSERT INTO operations(key,kind,request_sha,state,created_at,updated_at) VALUES(?,?,?,?,?,?)",
                          (key,kind,request_sha,"running",stamp(),stamp()))
                outcome="started"
            elif row[:2] != (kind,request_sha):
                outcome="fingerprint_conflict"
            elif row[2] == "succeeded":
                outcome="already_succeeded"
            elif row[2] == "not_applied" and allow_reconciled_retry:
                c.execute("UPDATE operations SET state='running',attempts=attempts+1,updated_at=? WHERE key=?", (stamp(),key))
                outcome="started_after_reconciliation"
            else:
                outcome="requires_reconciliation"
            c.execute("COMMIT")
        return outcome

    def complete(self, key, proof_sha):
        valid(key, KEY, "key")
        valid(proof_sha, SHA, "proof_sha")
        with self.connection() as c:
            c.execute("BEGIN IMMEDIATE")
            row=c.execute("SELECT state,proof_sha FROM operations WHERE key=?", (key,)).fetchone()
            if row is None:
                raise KeyError("unknown key")
            if row[0] == "succeeded" and row[1] == proof_sha:
                outcome="already_succeeded"
            elif row[0] != "running":
                outcome="requires_reconciliation"
            else:
                c.execute("UPDATE operations SET state='succeeded',proof_sha=?,updated_at=? WHERE key=?",
                          (proof_sha,stamp(),key))
                outcome="succeeded"
            c.execute("COMMIT")
        return outcome

    def unknown(self, key):
        valid(key, KEY, "key")
        with self.connection() as c:
            c.execute("BEGIN IMMEDIATE")
            row=c.execute("SELECT state FROM operations WHERE key=?", (key,)).fetchone()
            if row is None:
                raise KeyError("unknown key")
            if row[0] == "running":
                c.execute("UPDATE operations SET state='unknown',updated_at=? WHERE key=?", (stamp(),key))
                outcome="unknown"
            else:
                outcome=row[0]
            c.execute("COMMIT")
        return outcome

    def reconcile(self, key, outcome, proof_sha):
        valid(key, KEY, "key")
        valid(proof_sha, SHA, "proof_sha")
        if outcome not in ("applied", "not_applied"):
            raise ValueError("invalid reconciliation")
        with self.connection() as c:
            c.execute("BEGIN IMMEDIATE")
            row=c.execute("SELECT state,proof_sha FROM operations WHERE key=?", (key,)).fetchone()
            if row is None:
                raise KeyError("unknown key")
            target="succeeded" if outcome=="applied" else "not_applied"
            if row[0] == "succeeded" or (row[0]=="not_applied" and target!="not_applied"):
                raise ValueError("completed records cannot change")
            c.execute("UPDATE operations SET state=?,proof_sha=?,updated_at=? WHERE key=?",
                      (target,proof_sha,stamp(),key))
            c.execute("COMMIT")
        return target

    def status(self, key=None):
        if key is not None:
            valid(key, KEY, "key")
        with self.connection() as c:
            c.row_factory=sqlite3.Row
            if key:
                rows=c.execute("SELECT * FROM operations WHERE key=?", (key,)).fetchall()
            else:
                rows=c.execute("SELECT * FROM operations ORDER BY updated_at DESC LIMIT 40").fetchall()
            return [dict(x) for x in rows]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--db",type=Path,default=Path.home()/".local/state/control-laboratorio/operaciones.sqlite3")
    sub=p.add_subparsers(dest="action",required=True)
    for verb in ("begin","complete","unknown","reconcile","status"):
        a=sub.add_parser(verb)
        a.add_argument("--key",required=verb!="status")
        if verb=="begin":
            a.add_argument("--kind",choices=sorted(KINDS),required=True)
            a.add_argument("--request-sha",required=True)
            a.add_argument("--allow-reconciled-retry",action="store_true")
        if verb in ("complete","reconcile"):
            a.add_argument("--proof-sha",required=True)
        if verb=="reconcile":
            a.add_argument("--outcome",choices=("applied","not_applied"),required=True)
    a=p.parse_args()
    l=Ledger(a.db)
    if a.action=="begin":
        result=l.begin(a.key,a.kind,a.request_sha,a.allow_reconciled_retry)
    elif a.action=="complete":
        result=l.complete(a.key,a.proof_sha)
    elif a.action=="unknown":
        result=l.unknown(a.key)
    elif a.action=="reconcile":
        result=l.reconcile(a.key,a.outcome,a.proof_sha)
    else:
        result=l.status(a.key)
    print(json.dumps({"action":a.action,"result":result},ensure_ascii=False))
    if result in ("fingerprint_conflict","requires_reconciliation"):
        raise SystemExit(3)

if __name__=="__main__":
    main()
