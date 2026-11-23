#!/usr/bin/env python3
"""Revisar operaciones inciertas sin reejecutarlas ni inventar justificantes."""
from __future__ import annotations
import argparse
import datetime as dt
import json
import sqlite3
import subprocess
import hashlib
from contextlib import closing
from contextlib import closing
from pathlib import Path
from zoneinfo import ZoneInfo

def review(db_path, jobs, inspector):
    db_path=Path(db_path)
    with closing(sqlite3.connect(db_path.resolve().as_uri()+"?mode=ro",uri=True)) as c:
        rows=c.execute("""SELECT key,state,created_at FROM operations
                          WHERE state IN ('unknown','running') ORDER BY created_at""").fetchall()
    output=[]
    for key,state,created in rows:
        parts=key.split(":")
        found=None
        if len(parts)==3 and parts[0]=="daily" and parts[1] in jobs:
            try:
                day=dt.date.fromisoformat(parts[2])
                created_ns=int(dt.datetime.fromisoformat(created).timestamp()*1e9)
                found=inspector(jobs[parts[1]]["report"],jobs[parts[1]],day,created_ns)
            except (TypeError,ValueError,OSError):found=None
        output.append({"key":key,"state":state,"created_at":created,
                       "evidence":"valid" if found else "missing_or_stale",
                       "proof_sha":found})
    return output

def proof_failed_run(key, created_at, journal_reader=None):
    """Hash independent evidence of a failed systemd job, never infer no effects.

    Only Educamos' two historical supervised daily runs, with systemd journal
    in a 20-minute window around its creation. Caller must separately verify
    absence of a valid completed daily report using review().
    """
    parts=key.split(":")
    if len(parts)!=3 or parts[:2]!=["daily","educamos"]:
        return None
    try:
        day=dt.date.fromisoformat(parts[2])
        created=dt.datetime.fromisoformat(created_at).astimezone(ZoneInfo("Europe/Madrid"))
    except (ValueError,TypeError):
        return None
    if created.date()!=day or not 13<=created.hour<=14:
        return None
    a=(created-dt.timedelta(minutes=3)).strftime("%Y-%m-%d %H:%M:%S")
    b=(created+dt.timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
    cmd=["journalctl","--user","-u","educamos-diario-laboratorio.service",
         "--since",a,"--until",b,"--no-pager","-o","cat"]
    if journal_reader is None:
        try:
            done=subprocess.run(cmd,capture_output=True,text=True,timeout=8,check=False)
            if done.returncode!=0:return None
            journal=done.stdout
        except (OSError,subprocess.TimeoutExpired):
            return None
    else:
        journal=journal_reader(cmd)
    lines=journal.splitlines()
    # The wrapper explicitly reported job_returned_error. systemd confirmed
    # nonzero exit. Neither implies any partial web effect was/not applied.
    error=[x.strip() for x in lines if '"job": "educamos"' in x and '"state": "job_returned_error"' in x]
    systemd_failed=[x.strip() for x in lines if "Failed with result 'exit-code'" in x]
    exit3=[x.strip() for x in lines if "status=3/NOTIMPLEMENTED" in x]
    if len(error)!=1 or len(systemd_failed)!=1 or len(exit3)!=1:
        return None
    selected="\n".join(error+exit3+systemd_failed)
    return hashlib.sha256(("failure_observed_effects_unknown:"+key+"\n"+selected).encode()).hexdigest()

def close_proven_failures(db_path, jobs, inspector, journal_reader=None, ledger_cls=None):
    """No replays; no closure unless independent failure proof exists."""
    targets=review(db_path,jobs,inspector)
    if ledger_cls is None:
        from supervisor_operaciones import Ledger
        ledger_cls=Ledger
    ledger=ledger_cls(db_path)
    result=[]
    for item in targets:
        closed=False
        proof=proof_failed_run(item["key"],item["created_at"],journal_reader=journal_reader)
        if proof and item["state"]=="unknown" and item["evidence"]!="valid":
            outcome=ledger.close_failed_effects_unknown(item["key"],proof)
            closed=outcome in ("failed_effects_unknown","already_closed")
        result.append({
            "day":item["key"].split(":")[-1],
            "previous_state":item["state"],"complete_report_proven":item["evidence"]=="valid",
            "independent_failure_evidence":bool(proof),
            "closed_failed_effects_unknown":closed,
        })
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--db",type=Path,default=Path.home()/".local/state/control-laboratorio/operaciones.sqlite3")
    p.add_argument("--apply-proven",action="store_true",help="Solo reconciliar efectos demostrados; nunca reejecutar trabajos.")
    p.add_argument("--close-proven-failures",action="store_true",
      help="Cierre terminal de ejecuciones fallidas según journal; los efectos parciales permanecen desconocidos.")
    args=p.parse_args()
    from supervision_diaria import JOBS,inspect
    if args.apply_proven and args.close_proven_failures:
        p.error("Choose one reconciliation mode")
    if args.close_proven_failures:
        outcome=close_proven_failures(args.db,JOBS,inspect)
        print(json.dumps({"failed_service_closure":outcome,
             "no_effect_replayed":True,
             "partial_effects_known":False},ensure_ascii=False))
        return
    result=review(args.db,JOBS,inspect)
    applied=[]
    if args.apply_proven:
        from supervisor_operaciones import Ledger
        ledger=Ledger(args.db)
        for x in result:
            if x["evidence"]=="valid" and x["state"]=="unknown":
                x["result"]=ledger.reconcile(x["key"],"applied",x["proof_sha"])
                applied.append(x["key"])
    # Keys are opaque but not printed; dates and evidence status suffice.
    print(json.dumps({"unsettled":len(result),
      "by_day":[{"date":x["key"].split(":")[-1],"family":x["key"].split(":")[1] if ":" in x["key"] else "unknown",
                 "state":x["state"],"evidence":x["evidence"],
                 "reconciled":x["key"] in applied} for x in result],
      "reconciled_count":len(applied),
      "no_effect_replayed":True},ensure_ascii=False))
if __name__=="__main__":main()
