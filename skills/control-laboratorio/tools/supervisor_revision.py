#!/usr/bin/env python3
"""Revisar operaciones inciertas sin reejecutarlas ni inventar justificantes."""
from __future__ import annotations
import argparse
import datetime as dt
import json
import sqlite3
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

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--db",type=Path,default=Path.home()/".local/state/control-laboratorio/operaciones.sqlite3")
    p.add_argument("--apply-proven",action="store_true",help="Solo reconciliar efectos demostrados; nunca reejecutar trabajos.")
    args=p.parse_args()
    from supervision_diaria import JOBS,inspect
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
