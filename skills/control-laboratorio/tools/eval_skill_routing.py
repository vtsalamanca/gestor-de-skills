#!/usr/bin/env python3
"""Evaluador L4 offline. Nunca inventa llamadas reales del modelo.

Formato observaciones (JSONL): {"id":"...", "selected_skills":["..."],
 "evidence":"identificadores o transcripción verificable"}.
Si no se entregan observaciones, solo valida el banco; NO declara aprobado L4.
"""
from __future__ import annotations
import argparse
import json
import hashlib
import re
from pathlib import Path
from collections import Counter

SKILL_RESOURCE = re.compile(
    r"(?:skill://plugins_6add39166308819193bc271cfa0af302/([a-z0-9_-]+)/SKILL\.md"
    r"|skills://plugins/gestor-de-skills/([a-z0-9_-]+)/skill\.md)"
)

def load_cases(path):
    cases=[]
    known=set()
    for lineno,line in enumerate(Path(path).read_text().splitlines(),1):
        if not line.strip():continue
        item=json.loads(line)
        if not isinstance(item,dict) or not isinstance(item.get("id"),str) or not item["id"].strip():
            raise ValueError(f"invalid_id_{lineno}")
        if item["id"] in known:raise ValueError("duplicate_case")
        if not isinstance(item.get("prompt"),str) or not item["prompt"].strip():
            raise ValueError("invalid_prompt")
        if not isinstance(item.get("expected_skills"),list) or not all(isinstance(x,str) for x in item["expected_skills"]):
            raise ValueError("invalid_expectation")
        if len(set(item["expected_skills"]))!=len(item["expected_skills"]):
            raise ValueError("duplicate_expectation")
        known.add(item["id"]);cases.append(item)
    if not cases:raise ValueError("empty_case_bank")
    return cases

def validate_trace(root, row):
    """Check supplied JSONL records and checksum, not merely a claimed hash.

    The caller must independently establish that the file really came from a
    ChatGPT execution; filesystem checksum alone does not attest provenance.
    """
    root=Path(root).resolve()
    rel=row.get("trace_path")
    if not isinstance(rel,str) or not rel.strip() or Path(rel).is_absolute():
        raise ValueError("trace_path_required")
    candidate=(root/rel).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_file() or candidate.is_symlink():
        raise ValueError("unsafe_or_missing_trace")
    raw=candidate.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=row["trace_sha256"]:
        raise ValueError("trace_hash_mismatch")
    if not raw.strip():
        raise ValueError("empty_trace")
    skills=set()
    for line in raw.splitlines():
        if not line.strip():continue
        event=json.loads(line)
        if not isinstance(event, dict):
            raise ValueError("invalid_trace_event")
        if event.get("conversation_ref")!=row.get("conversation_ref"):
            raise ValueError("wrong_conversation_trace")
        if event.get("plugin_version")!=row.get("plugin_version"):
            raise ValueError("wrong_plugin_version_trace")
        if event.get("tool_name") not in ("skills__read","tools.skills__read"):
            continue
        uri=event.get("uri","")
        if not isinstance(uri, str):
            raise ValueError("invalid_skill_resource_uri")
        match=SKILL_RESOURCE.fullmatch(uri)
        if match:
            skills.add(match.group(1) or match.group(2))
    if skills!=set(row["selected_skills"]):
        raise ValueError("selected_skills_mismatch_with_trace")
    return True

def score(cases,observations,expected_version=None,trace_root=None):
    expected={case['id']:set(case['expected_skills']) for case in cases}
    found={}
    seen_conversations=set()
    provenance=Counter()
    versions=Counter()
    version_mismatches=[]
    for row in observations:
        key=row.get("id")
        if key not in expected:raise ValueError("unknown_observation")
        if key in found:raise ValueError("duplicate_observation")
        if not isinstance(row.get("selected_skills"),list) or not all(isinstance(x,str) for x in row["selected_skills"]):
            raise ValueError("invalid_observation")
        if not isinstance(row.get("evidence"),str) or not row['evidence'].strip():
            raise ValueError("observation_requires_evidence")
        kind=row.get("observation_kind","unverified")
        if kind not in ("user_report","verified_tool_trace","unverified"):
            raise ValueError("invalid_evidence_kind")
        version=row.get("plugin_version","unknown")
        if not isinstance(version,str) or not version.strip():
            raise ValueError("invalid_version")
        conversation_ref=row.get("conversation_ref")
        if kind=="verified_tool_trace":
            if not isinstance(conversation_ref,str) or not conversation_ref.strip():
                raise ValueError("verified_trace_requires_conversation")
            if conversation_ref in seen_conversations:
                raise ValueError("not_independent_conversations")
            if not isinstance(row.get("trace_sha256"),str) or len(row["trace_sha256"])!=64 or any(c not in '0123456789abcdef' for c in row["trace_sha256"]):
                raise ValueError("verified_trace_requires_sha256")
            if trace_root is None:
                raise ValueError("verified_trace_requires_local_evidence_root")
            validate_trace(trace_root,row)
            seen_conversations.add(conversation_ref)
        provenance[kind]+=1
        versions[version]+=1
        if expected_version and version!=expected_version:
            version_mismatches.append(key)
        found[key]=set(row["selected_skills"])
    tp=fp=fn=0
    details=[]
    for case in cases:
        key=case['id']
        if key not in found:continue
        selected=found[key];want=expected[key]
        tp+=len(want&selected);fp+=len(selected-want);fn+=len(want-selected)
        details.append({"id":key,"true_positive":sorted(want&selected),
          "false_positive":sorted(selected-want),"false_negative":sorted(want-selected)})
    all_observed=len(found)==len(cases)
    independently_verified=(provenance.get("verified_tool_trace",0)==len(cases)
                           and len(cases)>0 and not version_mismatches)
    status=("not_evaluated" if not found else
            "measured" if independently_verified else
            "reported_partial" if not provenance.get("verified_tool_trace",0) else
            "partial")
    return {"total_cases":len(cases),"observed":len(found),
      "provenance":dict(provenance),"plugin_versions":dict(versions),
      "expected_version":expected_version,
      "version_mismatches":version_mismatches,
      "independent_l4_validated":independently_verified,
      "attestation_note":"The trace source must be independently trusted; a matching SHA256 alone cannot attest ChatGPT provenance.",
      "unobserved":sorted(set(expected)-set(found)),
      "TP":tp,"FP":fp,"FN":fn,
      "precision":round(tp/(tp+fp),3) if tp+fp else None,
      "recall":round(tp/(tp+fn),3) if tp+fn else None,
      "all_cases_observed":all_observed,
      "status":status,
      "case_details":details}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cases",type=Path,default=Path(__file__).resolve().parents[1]/'references/eval_cases.jsonl')
    p.add_argument("--observations",type=Path,help="Trazas verificadas o informes etiquetados.")
    p.add_argument("--version",help="Versión de plugin para validación L4; datos de otra versión no cuentan.")
    p.add_argument("--trace-root",type=Path,help="Carpeta privada de trazas JSONL exportadas y comprobables.")
    args=p.parse_args()
    cases=load_cases(args.cases)
    obs=[json.loads(line) for line in args.observations.read_text().splitlines() if line.strip()] if args.observations else []
    if args.version:
        version=args.version
    else:
        version=json.loads((Path(__file__).resolve().parents[3]/'.codex-plugin/plugin.json').read_text())['version']
    print(json.dumps(score(cases,obs,expected_version=version,trace_root=args.trace_root),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
