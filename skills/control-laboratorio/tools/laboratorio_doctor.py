#!/usr/bin/env python3
"""Diagnóstico privado, de solo lectura, sin red ni reparaciones automáticas."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone, timedelta
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sqlite3
from zoneinfo import ZoneInfo

SERVICES=("control-debian-sustituto.service","control-debian-audit-retention.service")
TIMERS=("buscar-curro-laboratorio.timer","educamos-diario-laboratorio.timer")
JOBS=("buscar-curro-laboratorio.service","educamos-diario-laboratorio.service")
UID=os.getuid()

def result(status, detail):
    return {"status":status,"detail":detail}

def command(args, timeout=4):
    try:
        r=subprocess.run(args,capture_output=True,text=True,timeout=timeout,check=False)
        return r.returncode,r.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return 127,""

def check_audit(home):
    base=home/"utilidades/control-laboratorio"
    try:
        report=json.loads((base/"auditoria-homologacion.json").read_text())
        data=(base/"evidencias.json").read_bytes()
        evidence=json.loads(data)
        if report["total"]!=len(report["tools"]) or len({x["name"] for x in report["tools"]})!=report["total"]:
            return result("error","audit inventory inconsistent")
        if report["sources"]["evidence_sha256"]!=hashlib.sha256(data).hexdigest():
            return result("error","audit evidence hash mismatch")
        if not isinstance(evidence.get("checks"),dict):
            return result("error","audit evidence schema invalid")
        complete=report["counts"].get("homologada_en_alcance",0)
        other=sum(v for k,v in report["counts"].items() if k!="homologada_en_alcance")
        if complete+other!=report["total"]:
            return result("error","audit count mismatch")
        return result("ok" if other==0 else "warning",
                      f"audit checked {complete}/{report['total']} in documented scopes; checks={len(evidence['checks'])}")
    except (OSError,KeyError,TypeError,ValueError,UnicodeError):
        return result("error","audit unavailable or unreadable")

def check_services():
    out={}
    for name in SERVICES:
        rc,body=command(["systemctl","--user","is-active",name])
        out[name]=result("ok" if (rc==0 and body=="active") else "error",
                         "active" if rc==0 and body=="active" else "inactive or inaccessible")
    for name in TIMERS:
        rc,body=command(["systemctl","--user","is-active",name])
        out[name]=result("ok" if (rc==0 and body=="active") else "warning",
                         "active" if rc==0 and body=="active" else "timer inactive or inaccessible")
    return out

def check_last_trigger(timer,now=None):
    rc,body=command(["systemctl","--user","show",timer,"-p","LastTriggerUSec","--no-pager"])
    if rc:
        return result("warning","last trigger unavailable")
    raw=body.partition("=")[-1].split()
    if len(raw)<4 or raw[1]=="n/a":
        return result("warning","no recorded last trigger")
    try:
        when=datetime.fromisoformat(raw[1]+"T"+raw[2]).replace(tzinfo=ZoneInfo("Europe/Madrid"))
        age=((now or datetime.now(timezone.utc))-when).total_seconds()
        if age< -120:
            return result("warning","last trigger in the future")
        return result("ok" if age<=48*3600 else "warning",
                      f"last trigger age_hours={max(0,age)/3600:.1f}")
    except (ValueError,IndexError):
        return result("warning","last trigger date not understood")

def check_job_supervision(job):
    rc,body=command(["systemctl","--user","show",job,
                     "-p","ExecStart","-p","DropInPaths","--no-pager"])
    if rc:
        return result("warning","supervision binding unavailable")
    if "supervision_diaria.py" not in body or "10-supervisor.conf" not in body:
        return result("warning","supervised daily job not configured")
    return result("ok","supervisor adapter loaded; no execution implied")

def check_job_completion(job,now=None):
    rc,body=command(["systemctl","--user","show",job,"-p","Result","-p","ExecMainStatus","-p","ExecMainExitTimestamp","--no-pager"])
    if rc:
        return result("warning","job completion unavailable")
    fields=dict(line.split("=",1) for line in body.splitlines() if "=" in line)
    if fields.get("Result")!="success" or fields.get("ExecMainStatus")!="0":
        return result("warning","job last process result not successful")
    raw=fields.get("ExecMainExitTimestamp","").split()
    if len(raw)<4:
        return result("warning","no job completion timestamp")
    try:
        when=datetime.fromisoformat(raw[1]+"T"+raw[2]).replace(tzinfo=ZoneInfo("Europe/Madrid"))
        age=((now or datetime.now(timezone.utc))-when).total_seconds()
    except (ValueError,IndexError):
        return result("warning","job completion timestamp invalid")
    if age< -120 or age>48*3600:
        return result("warning","job last success missing or stale")
    return result("ok",f"process success age_hours={max(0,age)/3600:.1f}; downstream delivery unverified")

def check_node_process():
    """Linux thread names can say MainThread; inspect cmdline, never print it."""
    root=Path("/proc")
    try:
        for path in root.iterdir():
            if not path.name.isdecimal():
                continue
            try:
                if path.stat().st_uid!=UID:
                    continue
                cmdline=(path/"cmdline").read_bytes()
                if b"sustituto-dc-independiente/node_modules/@wonderwhy-er/desktop-commander/dist/index.js" in cmdline:
                    return result("ok","generic MCP Node.js child present")
            except (OSError,PermissionError,ProcessLookupError):
                continue
    except OSError:
        return result("warning","process table inaccessible")
    return result("error","generic MCP Node.js child absent")

def check_docs(home):
    p=home/"proyectos/gestor-de-skills/skills/bibliotecario-memoria/SKILL.md"
    try:
        text=p.read_text(encoding="utf-8")
    except OSError:
        return result("warning","bibliotecario skill unavailable")
    if "43 herramientas" in text:
        return result("warning","bibliotecario instructions refer to historical 43-tool catalog")
    return result("ok","no detected historical 43-tool reference")

def check_supervisor(home):
    db=home/".local/state/control-laboratorio/operaciones.sqlite3"
    if not db.is_file():
        return result("unknown","daily operations not yet supervised")
    if db.is_symlink() or db.stat().st_mode & 0o077:
        return result("error","supervisor ledger permissions unsafe")
    try:
        with sqlite3.connect(f"file:{db}?mode=ro",uri=True,timeout=3) as connection:
            rows=connection.execute("SELECT state,COUNT(*) FROM operations GROUP BY state").fetchall()
        counts=dict(rows)
    except (sqlite3.Error,OSError):
        return result("error","supervisor ledger unreadable")
    unsettled=sum(counts.get(s,0) for s in ("unknown","running"))
    status="warning" if unsettled else "ok"
    detail=f"operations={sum(counts.values())}, unsettled={unsettled}; no replay performed"
    return result(status,detail)

def check_git(home):
    repo=home/"proyectos/gestor-de-skills"
    rc,out=command(["git","-C",str(repo),"status","--porcelain=v1"],timeout=5)
    if rc:
        return result("warning","skills Git status unavailable")
    if out:
        return result("warning",f"skills repository has {len(out.splitlines())} uncommitted paths")
    return result("ok","skills repository clean")

def doctor(home,with_systemd=True):
    now=datetime.now(timezone.utc)
    checks={"audit":check_audit(home),"skills_docs":check_docs(home),"skills_git":check_git(home),"supervisor":check_supervisor(home)}
    if with_systemd:
        checks.update(check_services())
        checks["node_child"]=check_node_process()
        for timer in TIMERS:
            checks["last_"+timer]=check_last_trigger(timer,now)
        for job in JOBS:
            checks["last_success_"+job]=check_job_completion(job,now)
            checks["supervision_"+job]=check_job_supervision(job)
    else:
        checks["live_services"]=result("unknown","not queried in fixture mode")
    checks["full_vm_restore"]=result("unknown","not certified: synthetic SQLite restore is not a full VM restore")
    status=("error" if any(x["status"]=="error" for x in checks.values()) else
            "warning" if any(x["status"]=="warning" for x in checks.values()) else "ok")
    return {"schema_version":1,"checked_at":now.isoformat(timespec="seconds"),
            "status":status,"checks":checks,"automatic_repairs":False}

def save_report(path,body):
    path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
    if path.is_symlink() or (path.parent.stat().st_mode&0o077):
        raise PermissionError("unsafe doctor report destination")
    tmp=path.with_name(".doctor-ultimo.tmp")
    data=(json.dumps(body,ensure_ascii=False,indent=2)+"\n").encode()
    flags=os.O_CREAT|os.O_WRONLY|os.O_EXCL|getattr(os,"O_NOFOLLOW",0)
    fd=os.open(tmp,flags,0o600)
    try:
        with os.fdopen(fd,"wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if tmp.exists():tmp.unlink()

def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--home",type=Path,default=Path.home())
    a.add_argument("--no-systemd",action="store_true")
    a.add_argument("--save",action="store_true")
    args=a.parse_args()
    report=doctor(args.home,not args.no_systemd)
    if args.save:
        save_report(args.home/".local/state/control-laboratorio/doctor-ultimo.json",report)
    print(json.dumps(report,ensure_ascii=False))
    if report["status"]=="error":
        raise SystemExit(2)
    if report["status"]=="warning":
        raise SystemExit(1)

if __name__=="__main__":
    main()
