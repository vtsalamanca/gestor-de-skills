import importlib.util
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
  self.assertEqual(x['status'],'measured')
 def test_rejects_unverifiable_observation(self):
  with self.assertRaises(ValueError):
   m.score([{"id":"x","expected_skills":[]}],[{"id":"x","selected_skills":[]}])
if __name__=='__main__':unittest.main()
