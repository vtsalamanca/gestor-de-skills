#!/usr/bin/env python3
"""Evaluador L4 offline. Nunca inventa llamadas reales del modelo.

Formato observaciones (JSONL): {"id":"...", "selected_skills":["..."],
 "evidence":"identificadores o transcripción verificable"}.
Si no se entregan observaciones, solo valida el banco; NO declara aprobado L4.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

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

def score(cases,observations):
    expected={case['id']:set(case['expected_skills']) for case in cases}
    found={}
    for row in observations:
        key=row.get("id")
        if key not in expected:raise ValueError("unknown_observation")
        if key in found:raise ValueError("duplicate_observation")
        if not isinstance(row.get("selected_skills"),list) or not all(isinstance(x,str) for x in row["selected_skills"]):
            raise ValueError("invalid_observation")
        if not isinstance(row.get("evidence"),str) or not row['evidence'].strip():
            raise ValueError("observation_requires_evidence")
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
    return {"total_cases":len(cases),"observed":len(found),
      "unobserved":sorted(set(expected)-set(found)),
      "TP":tp,"FP":fp,"FN":fn,
      "precision":round(tp/(tp+fp),3) if tp+fp else None,
      "recall":round(tp/(tp+fn),3) if tp+fn else None,
      "all_cases_observed":len(found)==len(cases),
      "status":"not_evaluated" if not found else "partial" if len(found)<len(cases) else "measured",
      "case_details":details}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cases",type=Path,default=Path(__file__).resolve().parents[1]/'references/eval_cases.jsonl')
    p.add_argument("--observations",type=Path,help="Trazas reales verificadas, no simulaciones.")
    args=p.parse_args()
    cases=load_cases(args.cases)
    obs=[json.loads(line) for line in args.observations.read_text().splitlines() if line.strip()] if args.observations else []
    print(json.dumps(score(cases,obs),ensure_ascii=False,indent=2))
if __name__=="__main__":main()
