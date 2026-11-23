import importlib.util
import hashlib
import json
import tempfile
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('eval_skill_routing',ROOT/'skills/control-laboratorio/tools/eval_skill_routing.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TestRoutingEval(unittest.TestCase):
 def test_bank_has_positive_and_negative(self):
  cases=m.load_cases(ROOT/'skills/control-laboratorio/references/eval_cases.jsonl')
  self.assertGreaterEqual(len(cases),24)
  self.assertTrue(any(not x['expected_skills'] for x in cases))
  self.assertTrue(any(len(x['expected_skills'])>1 for x in cases))
 def test_unobserved_not_passed(self):
  x=m.score(m.load_cases(ROOT/'skills/control-laboratorio/references/eval_cases.jsonl'),[])
  self.assertEqual(x['status'],'not_evaluated')
  self.assertEqual(x['observed'],0)
 def test_false_positive_and_false_negative(self):
  cases=[{"id":"x","expected_skills":[]},{"id":"y","expected_skills":["control-laboratorio"]}]
  observed=[{"id":"x","selected_skills":["control-laboratorio"],"evidence":"trace A"},
            {"id":"y","selected_skills":[],"evidence":"trace B"}]
  x=m.score(cases,observed)
  self.assertEqual((x['TP'],x['FP'],x['FN']),(0,1,1))
  self.assertEqual(x['status'],'reported_partial')
 def test_rejects_unverifiable_observation(self):
  with self.assertRaises(ValueError):
   m.score([{"id":"x","expected_skills":[]}],[{"id":"x","selected_skills":[]}])
 def test_report_does_not_count_as_l4(self):
  cases=[{"id":"a","expected_skills":["control-laboratorio"]}]
  report=[{"id":"a","selected_skills":["control-laboratorio"],
           "evidence":"User supplied report","observation_kind":"user_report",
           "plugin_version":"0.4.56"}]
  scored=m.score(cases,report,expected_version="0.4.58")
  self.assertFalse(scored["independent_l4_validated"])
  self.assertEqual(scored["status"],"reported_partial")
  self.assertEqual(scored["version_mismatches"],["a"])
 def test_distinct_verified_tool_traces(self):
  cases=[{"id":"a","expected_skills":[]},{"id":"b","expected_skills":[]}]
  with tempfile.TemporaryDirectory() as d:
   obs=[]
   for c in cases:
    ref="unique-"+c["id"]
    event={"conversation_ref":ref,"plugin_version":"0.4.58","tool_name":"misc"}
    payload=(json.dumps(event)+"\n").encode()
    path=Path(d)/(ref+".jsonl")
    path.write_bytes(payload)
    obs.append({"id":c["id"],"selected_skills":[],"evidence":"verified file",
      "observation_kind":"verified_tool_trace","plugin_version":"0.4.58",
      "conversation_ref":ref,"trace_path":path.name,
      "trace_sha256":hashlib.sha256(payload).hexdigest()})
   self.assertTrue(m.score(cases,obs,expected_version="0.4.58",trace_root=d)["independent_l4_validated"])
   obs[1]["conversation_ref"]=obs[0]["conversation_ref"]
   with self.assertRaises(ValueError):
    m.score(cases,obs,expected_version="0.4.58",trace_root=d)
   obs[1]["conversation_ref"]="unique-b"
   obs[0]["trace_sha256"]="a"*64
   with self.assertRaises(ValueError):
    m.score(cases,obs,expected_version="0.4.58",trace_root=d)
 def test_current_skill_resource_uri(self):
  uri="skill://plugins_6add39166308819193bc271cfa0af302/control-laboratorio/SKILL.md"
  with tempfile.TemporaryDirectory() as d:
   row=self.write_trace(d, {"tool_name":"skills__read","uri":uri}, ["control-laboratorio"])
   self.assertTrue(m.validate_trace(d,row))
 def test_empty_traces_are_not_verified(self):
  with tempfile.TemporaryDirectory() as d:
   row=self.write_trace(d, None, [])
   with self.assertRaisesRegex(ValueError,"empty_trace"):
    m.validate_trace(d,row)
 def test_other_plugin_same_skill_does_not_count(self):
  uri="skill://plugins_other/control-laboratorio/SKILL.md"
  with tempfile.TemporaryDirectory() as d:
   row=self.write_trace(d, {"tool_name":"skills__read","uri":uri}, [])
   self.assertTrue(m.validate_trace(d,row))
 def write_trace(self,d,event,skills):
  row={"conversation_ref":"test-conversation","plugin_version":"0.4.58",
       "trace_path":"trace.jsonl","selected_skills":skills}
  raw=b"\n" if event is None else json.dumps({
      "conversation_ref":row["conversation_ref"],"plugin_version":row["plugin_version"],**event
  }).encode()
  (Path(d)/row["trace_path"]).write_bytes(raw)
  row["trace_sha256"]=hashlib.sha256(raw).hexdigest()
  return row
if __name__=='__main__':unittest.main()
