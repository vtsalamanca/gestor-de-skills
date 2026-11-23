"""Estado explícito de pendientes, separado de checkpoints históricos inmutables.

Sin IA ni inferencia: cerrar/sustituir/bloquear requiere un hito probatorio
existente del mismo expediente y una operación idempotente. Solo la transición
autorizada crea tablas nuevas; consultar funciona sobre la DB antigua.
"""
from __future__ import annotations
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from contextlib import closing
from pathlib import Path

STATES = {"open", "resolved", "blocked", "superseded"}
EVIDENCE_KINDS = {
    "resolved": {"verified_result"},
    "blocked": {"failure", "verified_result"},
    "superseded": {"next_action"},
    "open": {"decision", "verified_result"},
}
SCHEMA = """
CREATE TABLE IF NOT EXISTS knowledge_action_status (
 job_id TEXT NOT NULL REFERENCES jobs(id), source_revision INTEGER NOT NULL,
 source_ordinal INTEGER NOT NULL, content_sha TEXT NOT NULL,
 status TEXT NOT NULL CHECK(status IN ('open','resolved','blocked','superseded')),
 evidence_revision INTEGER, evidence_ordinal INTEGER, updated_at TEXT NOT NULL,
 PRIMARY KEY(job_id,source_revision,source_ordinal));
CREATE TABLE IF NOT EXISTS knowledge_action_events (
 operation_id TEXT PRIMARY KEY, job_id TEXT NOT NULL,
 source_revision INTEGER NOT NULL, source_ordinal INTEGER NOT NULL,
 content_sha TEXT NOT NULL, status TEXT NOT NULL,
 evidence_revision INTEGER, evidence_ordinal INTEGER,
 request_sha TEXT NOT NULL, at TEXT NOT NULL);
"""

def _connect(path, readonly=False):
    path = Path(path).resolve()
    uri=path.as_uri()+("?mode=ro" if readonly else "")
    conn=sqlite3.connect(uri,uri=True,timeout=10)
    conn.execute("PRAGMA foreign_keys=ON")
    if readonly:
        conn.execute("PRAGMA query_only=ON")
    return conn

def _entries(conn, work, revision):
    row=conn.execute("SELECT content FROM checkpoints WHERE job_id=? AND revision=?",
                     (work,revision)).fetchone()
    if not row:
        raise ValueError("checkpoint_not_found")
    try:
        value=json.loads(row[0])
    except (TypeError,ValueError) as exc:
        raise ValueError("invalid_checkpoint") from exc
    if not isinstance(value,list):
        raise ValueError("invalid_checkpoint")
    return value

def _at(conn, work, revision, ordinal, allowed):
    if not isinstance(revision,int) or revision<1 or not isinstance(ordinal,int) or ordinal<0:
        raise ValueError("invalid_source_position")
    items=_entries(conn,work,revision)
    if ordinal>=len(items):
        raise ValueError("ordinal_not_found")
    item=items[ordinal]
    if not isinstance(item,dict) or item.get("kind") not in allowed or not isinstance(item.get("text"),str):
        raise ValueError("wrong_evidence_type")
    return item

def _sha(item):
    return hashlib.sha256(json.dumps(item,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def pending(db_path, work, limit=10):
    if not isinstance(limit,int) or not 1<=limit<=100:
        raise ValueError("invalid_limit")
    with closing(_connect(db_path,True)) as c:
        jobs=c.execute("SELECT revision FROM jobs WHERE id=?",(work,)).fetchone()
        if jobs is None:
            return {"status":"not_found"}
        has_table=c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='knowledge_action_status'").fetchone()
        statuses={}
        if has_table:
            statuses={(rev,ordinal):(status,sha,e_rev,e_ord) for rev,ordinal,status,sha,e_rev,e_ord in
                c.execute("SELECT source_revision,source_ordinal,status,content_sha,evidence_revision,evidence_ordinal FROM knowledge_action_status WHERE job_id=?",(work,))}
        rows=c.execute("SELECT revision,content FROM checkpoints WHERE job_id=? ORDER BY revision DESC",(work,)).fetchall()
        result=[]
        unreviewed=0
        for rev,body in rows:
            try: entries=json.loads(body)
            except (TypeError,ValueError): continue
            if not isinstance(entries,list): continue
            for ordinal,item in enumerate(entries):
                if not isinstance(item,dict) or item.get("kind")!="next_action" or not isinstance(item.get("text"),str):
                    continue
                key=(rev,ordinal); mark=statuses.get(key); digest=_sha(item)
                if mark and mark[1]!=digest:
                    raise ValueError("checkpoint_content_changed")
                # Never present historical unclassified checkpoint as a current task.
                # Only the latest checkpoint's unclassified actions are provisional.
                state=mark[0] if mark else ("open" if rev==jobs[0] else "historical_unreviewed")
                if state=="historical_unreviewed":
                    unreviewed+=1
                if state in ("open","blocked"):
                    result.append({"revision":rev,"ordinal":ordinal,"text":item["text"],"status":state,
                                   "evidence_revision":mark[2] if mark else None})
        result.sort(key=lambda x:(-x["revision"],x["ordinal"]))
        return {"work":work,"latest_revision":jobs[0],"open_count":sum(x["status"]=="open" for x in result),
                "blocked_count":sum(x["status"]=="blocked" for x in result),
                "historical_unreviewed_count":unreviewed,"pending_actions":result[:limit],
                "truncated":len(result)>limit}

def transition(db_path,work,source_revision,source_ordinal,status,evidence_revision,evidence_ordinal,operation_id):
    if status not in STATES:
        raise ValueError("invalid_status")
    if not isinstance(operation_id,str) or not 8<=len(operation_id)<=120 or not all(x.isalnum() or x in "-_:." for x in operation_id):
        raise ValueError("invalid_operation_id")
    if not isinstance(evidence_revision,int) or evidence_revision<source_revision:
        raise ValueError("evidence_must_follow_source")
    with closing(_connect(db_path)) as c:
        # Additive migration, committed before the guarded state transition.
        for sql in SCHEMA.strip().split(";"):
            if sql.strip(): c.execute(sql)
        c.commit()
        c.execute("BEGIN IMMEDIATE")
        source=_at(c,work,source_revision,source_ordinal,{"next_action"})
        _at(c,work,evidence_revision,evidence_ordinal,EVIDENCE_KINDS[status])
        content_sha=_sha(source)
        request=[work,source_revision,source_ordinal,content_sha,status,evidence_revision,evidence_ordinal]
        fingerprint=hashlib.sha256(json.dumps(request).encode()).hexdigest()
        prior=c.execute("SELECT request_sha FROM knowledge_action_events WHERE operation_id=?",(operation_id,)).fetchone()
        if prior:
            if prior[0]!=fingerprint:raise ValueError("operation_id_conflict")
            c.commit()
            return {"status":"duplicate","action_state":status,"source_revision":source_revision}
        current=c.execute("SELECT content_sha,status FROM knowledge_action_status WHERE job_id=? AND source_revision=? AND source_ordinal=?",
                          (work,source_revision,source_ordinal)).fetchone()
        if current and current[0]!=content_sha:
            raise ValueError("checkpoint_content_changed")
        if current and current[1] in ("resolved","superseded") and status!=current[1]:
            raise ValueError("terminal_action_cannot_change")
        at=datetime.now(timezone.utc).isoformat()
        c.execute("""INSERT INTO knowledge_action_status VALUES (?,?,?,?,?,?,?,?)
          ON CONFLICT(job_id,source_revision,source_ordinal)
          DO UPDATE SET status=excluded.status,evidence_revision=excluded.evidence_revision,
             evidence_ordinal=excluded.evidence_ordinal,updated_at=excluded.updated_at""",
          (work,source_revision,source_ordinal,content_sha,status,evidence_revision,evidence_ordinal,at))
        c.execute("INSERT INTO knowledge_action_events VALUES (?,?,?,?,?,?,?,?,?,?)",
                  (operation_id,work,source_revision,source_ordinal,content_sha,status,
                   evidence_revision,evidence_ordinal,fingerprint,at))
        c.commit()
        return {"status":"saved","action_state":status,"source_revision":source_revision,
                "evidence_revision":evidence_revision}
