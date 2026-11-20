#!/usr/bin/env python3
"""Supervisión de una jornada: idempotencia, postcondición y no reintento ciego.

La CLI de producción solo permite dos coordinadores ya autorizados. No ejecuta
acciones durante las pruebas, que inyectan scripts y runners sintéticos.
"""
from __future__ import annotations
import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from zoneinfo import ZoneInfo

from supervisor_operaciones import Ledger

TZ=ZoneInfo("Europe/Madrid")
HOME=Path.home()
JOBS={
    "educamos":{
        "script":HOME/"proyectos/educamos-puente/educamos_diario.py",
        "report":HOME/"proyectos/educamos-puente/resultado/educamos_diario_ultimo.json",
        "timeout":410,"allowed":("completo",),"timestamp":"fecha"},
    "buscar-curro":{
        "script":HOME/"proyectos/_gestion/buscar-curro/buscar_curro_jornada.py",
        "report":HOME/".local/state/buscar-curro/ultimo_resumen_jornada.json",
        "timeout":520,"allowed":("completo","parcial"),"timestamp":"fecha_utc",
        "preflight":HOME/"proyectos/_gestion/credenciales-laboratorio/preparar_correo_infojobs.py",
        "preflight_timeout":70}
}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def inspect(report, job, day, after_ns):
    if report.is_symlink() or not report.is_file():
        return None
    stat=report.stat()
    if stat.st_uid!=os.getuid() or stat.st_mode&0o077 or not 16<=stat.st_size<=2_000_000:
        return None
    if stat.st_mtime_ns+1_000_000_000<after_ns:
        return None
    try:
        data=report.read_bytes()
        doc=json.loads(data)
        if not isinstance(doc,dict) or doc.get("estado") not in job["allowed"]:
            return None
        timestamp=dt.datetime.fromisoformat(doc[job["timestamp"]])
        if timestamp.tzinfo is None or timestamp.astimezone(TZ).date()!=day:
            return None
        if int(timestamp.timestamp()*1_000_000_000)+2_000_000_000<after_ns:
            return None
        return digest(data)
    except (OSError,ValueError,KeyError,TypeError,UnicodeError):
        return None

def execute(job_name, *, day=None, state_dir=None, config=None, runner=None, now_ns=None):
    if job_name not in JOBS:
        raise ValueError("job not approved")
    cfg=config if config is not None else JOBS[job_name]
    script=Path(cfg["script"])
    report=Path(cfg["report"])
    if not script.is_file() or script.is_symlink() or script.stat().st_uid!=os.getuid():
        raise PermissionError("script not approved")
    base=Path(state_dir) if state_dir is not None else HOME/".local/state/control-laboratorio"
    if base.is_symlink():
        raise PermissionError("unsafe state dir")
    base.mkdir(mode=0o700,parents=True,exist_ok=True)
    if base.stat().st_mode&0o077:
        raise PermissionError("state dir not private")
    day=day or dt.datetime.now(TZ).date()
    key=f"daily:{job_name}:{day.isoformat()}"
    request=digest((job_name+"|"+str(script.resolve())+"|"+digest(script.read_bytes())).encode())
    ledger=Ledger(base/"operaciones.sqlite3")
    lock=base/("guard-"+job_name+".lock")
    fd=os.open(lock,os.O_RDWR|os.O_CREAT|getattr(os,"O_NOFOLLOW",0),0o600)
    try:
        with os.fdopen(fd,"rb") as guard:
            try: fcntl.flock(guard,fcntl.LOCK_EX|fcntl.LOCK_NB)
            except BlockingIOError:
                return {"job":job_name,"state":"in_progress","exit":3}
            rows=ledger.status(key)
            existing=rows[0] if rows else None
            if existing:
                if existing["request_sha"]!=request:
                    return {"job":job_name,"state":"fingerprint_conflict","exit":3}
                start=dt.datetime.fromisoformat(existing["created_at"]).timestamp()
                proof=inspect(report,cfg,day,int(start*1_000_000_000))
                if existing["state"]=="succeeded":
                    if proof and proof==existing["proof_sha"]:
                        return {"job":job_name,"state":"already_succeeded","exit":0}
                    return {"job":job_name,"state":"needs_reconciliation","exit":3}
                if proof and existing["state"] in ("unknown","running"):
                    status=ledger.reconcile(key,"applied",proof)
                    return {"job":job_name,"state":"recovered_"+status,"exit":0}
                ledger.unknown(key)
                return {"job":job_name,"state":"needs_reconciliation","exit":3}
            claimed=ledger.begin(key,"write",request)
            if claimed!="started":
                return {"job":job_name,"state":claimed,"exit":3}
            started=now_ns if now_ns is not None else __import__("time").time_ns()
            call=runner if runner is not None else subprocess.run
            try:
                preflight=cfg.get("preflight")
                if preflight:
                    preflight=Path(preflight)
                    if preflight.is_symlink() or not preflight.is_file() or preflight.stat().st_uid!=os.getuid():
                        ledger.unknown(key)
                        return {"job":job_name,"state":"preflight_unavailable","exit":3}
                    # Keep the previous systemd ExecStartPre=- semantics: nonzero is advisory.
                    call([sys.executable,str(preflight)],cwd=str(preflight.parent),
                         stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                         timeout=cfg.get("preflight_timeout",70),check=False)
                completed=call([sys.executable,str(script)],cwd=str(script.parent),
                               stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
                               timeout=cfg["timeout"],check=False)
                if completed.returncode!=0:
                    ledger.unknown(key)
                    return {"job":job_name,"state":"job_returned_error","exit":3}
                proof=inspect(report,cfg,day,started)
                if not proof:
                    ledger.unknown(key)
                    return {"job":job_name,"state":"report_not_verified","exit":3}
                if ledger.complete(key,proof)!="succeeded":
                    return {"job":job_name,"state":"needs_reconciliation","exit":3}
                return {"job":job_name,"state":"verified","exit":0}
            except (OSError,subprocess.TimeoutExpired):
                ledger.unknown(key)
                return {"job":job_name,"state":"execution_uncertain","exit":3}
    finally:
        # The fixed lock file is reused; deleting it can break flock mutual exclusion.
        pass

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job",required=True,choices=sorted(JOBS))
    args=parser.parse_args()
    data=execute(args.job)
    print(json.dumps(data,ensure_ascii=False))
    return data["exit"]

if __name__=="__main__":
    raise SystemExit(main())
