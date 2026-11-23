"""Recuperación léxica de trabajos, FTS5 en RAM (sin mutar la SQLite original).

Priorizar títulos exactos y del ámbito explícito; no inferir proyecto a partir
de menciones incidentales. Bibliotecario conserva el contrato find(term,limit).
"""
import argparse
import json
import re
import sqlite3
import unicodedata
import bibliotecario as b
try:
    from vinculos_contexto import lookup as lookup_scope, confirmed as confirmed_aliases
except ImportError:
    lookup_scope = None
    confirmed_aliases = None

def normalize(text):
    return "".join(c for c in unicodedata.normalize("NFKD", str(text).casefold())
                   if not unicodedata.combining(c))

def _tokens(text):
    return re.findall(r"\w+", normalize(text), flags=re.UNICODE)

def _rank(job, tokens):
    t = normalize(job["title"])
    phrase = " ".join(tokens)
    return (0 if t == phrase else
            1 if t.startswith(phrase) else
            2 if phrase in t else
            3 if all(x in t for x in tokens) else 4)

def _fallback(jobs, events, term, scope, limit, tokens):
    """Read-only literal match if FTS5 is not compiled into local SQLite."""
    norm = normalize(term)
    matched = set()
    for job in jobs:
        if norm in normalize(job["title"]):
            matched.add(job["id"])
    for jid, detail in events:
        if norm in normalize(detail):
            matched.add(jid)
    return _sorted(jobs, matched, scope, limit, tokens)

def _sorted(jobs, ids, scope, limit, tokens, bm_scores=None):
    by_id = {j["id"]: j for j in jobs}
    scope_norm = normalize(scope).strip() if scope else ""
    matched_scope_ids=set()
    if scope_norm and lookup_scope is not None:
        home=getattr(b,"BASE",b.DB.parent)
        try:matched_scope_ids=lookup_scope(home/"proyectos_indice.sqlite3",scope)
        except (OSError,sqlite3.Error):matched_scope_ids=set()
    filtered = [by_id[i] for i in ids if i in by_id and
                (not scope_norm or scope_norm in normalize(by_id[i]["title"]) or i in matched_scope_ids)]
    # Exact/prefix/title matches first; event-only matches by BM25 and recency.
    # ISO timestamps sort descending within equal lexical ranking and score.
    filtered.sort(key=lambda j: j["updated"], reverse=True)
    filtered.sort(key=lambda j: ( _rank(j,tokens),
                  (bm_scores or {}).get(j["id"],0.0)))
    return filtered[:limit]

def find(term, limit=20, scope=None):
    if not isinstance(term,str) or len(term.strip())<2:
        raise ValueError("query_too_short")
    if not isinstance(limit,int) or not 1<=limit<=100:
        raise ValueError("invalid_limit")
    if scope is not None and not isinstance(scope,str):
        raise ValueError("invalid_scope")
    if scope is not None and len(scope)>200:
        raise ValueError("invalid_scope")
    tokens = _tokens(term)
    if not tokens:
        return []
    source = sqlite3.connect(b.DB.resolve().as_uri()+"?mode=ro",uri=True,timeout=10)
    try:
        source.row_factory=sqlite3.Row
        jobs = [dict(x) for x in source.execute(
          "SELECT id,title,status,revision,updated FROM jobs")]
        events = list(source.execute("SELECT job_id,detail FROM events").fetchall())
        if confirmed_aliases is not None:
            home=getattr(b,"BASE",b.DB.parent)
            try:
                allow={j["id"] for j in jobs}
                events.extend((work,alias) for alias,work in confirmed_aliases(home/"proyectos_indice.sqlite3")
                              if work in allow)
            except (OSError,sqlite3.Error):
                pass
        try:
            idx = sqlite3.connect(":memory:")
            try:
                idx.execute("""CREATE VIRTUAL TABLE finder USING fts5(
                  job_id UNINDEXED, title, detail,
                  tokenize='unicode61 remove_diacritics 2')""")
                idx.executemany("INSERT INTO finder(job_id,title,detail) VALUES (?,?,?)",
                   ((j["id"],j["title"],"") for j in jobs))
                idx.executemany("INSERT INTO finder(job_id,title,detail) VALUES (?,?,?)",
                   ((jid,"",detail) for jid,detail in events))
                match = " AND ".join('"'+t.replace('"','""')+'"' for t in tokens)
                # BM25 is a tie-breaker for event matches; title priority above it.
                matches=idx.execute("""SELECT job_id, bm25(finder,12.0,1.0)
                   FROM finder WHERE finder MATCH ? ORDER BY bm25(finder,12.0,1.0)""",
                   (match,)).fetchall()
                scores={}
                for jid,score in matches:
                    scores[jid]=min(score,scores.get(jid,score))
                return _sorted(jobs,scores,scope,limit,tokens,scores)
            finally:
                idx.close()
        except sqlite3.OperationalError as exc:
            if "no such module: fts5" not in str(exc).lower():
                raise
            return _fallback(jobs,events,term,scope,limit,tokens)
    finally:
        source.close()

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("term")
    parser.add_argument("--limit",type=int,default=20)
    parser.add_argument("--scope")
    args=parser.parse_args()
    print(json.dumps(find(args.term,args.limit,args.scope),ensure_ascii=False,indent=2))
