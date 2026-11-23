#!/usr/bin/env python3
"""Diagnóstico por capas MCP, solo lectura, sin reinicios ni credenciales."""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from datetime import datetime, timezone

SERVICE="control-debian-sustituto.service"
PATTERNS={
 "session":r"session terminat|session expired|session close",
 "transport":r"connection reset|connection closed|transport error|broken pipe",
 "service_error":r"traceback|exception|error|failed",
 "reconnect":r"reconnect|tunnel.*connect",
}
def run(args,timeout=8):
    try:
        p=subprocess.run(args,capture_output=True,text=True,timeout=timeout,check=False)
        return p.returncode,p.stdout
    except (OSError,subprocess.TimeoutExpired):
        return 124,""

def classify(active,observed_error):
    if active is False:return "server_unavailable"
    if active is None:return "insufficient_evidence"
    if observed_error in ("session-terminated","timeout"):
        return "client_or_transport_suspected"
    return "service_running_no_end_to_end_proof"

def diagnose(observed_error="none",runner=run):
    _,txt=runner(["systemctl","--user","show",SERVICE,
        "-p","ActiveState","-p","SubState","-p","NRestarts","-p","MainPID"])
    info=dict(x.split("=",1) for x in txt.splitlines() if "=" in x and x.split("=",1)[0] in
              {"ActiveState","SubState","NRestarts","MainPID"})
    active={"active":True,"inactive":False,"failed":False}.get(info.get("ActiveState"))
    rc,journal=runner(["journalctl","--user","-u",SERVICE,"--since","-24h","--no-pager","-o","cat"])
    counts={k:len(re.findall(pattern,journal,re.I)) for k,pattern in PATTERNS.items()} if rc==0 else None
    return {"checked_at":datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "service":SERVICE,"active":active,"service_substate":info.get("SubState","unknown"),
            "restart_count":info.get("NRestarts","unknown"),
            "observed_client_error":observed_error,
            "diagnosis":classify(active,observed_error),
            "journal_pattern_counts":counts,
            "note":"Sin credenciales, líneas del journal ni reinicios. Estado servidor no certifica sesión MCP."}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--observed-error",choices=("none","session-terminated","timeout"),default="none")
    args=p.parse_args()
    print(json.dumps(diagnose(args.observed_error),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
