import json
from pathlib import Path
import unittest

from rerun_evidence_matrix import F, JOBS, REPO_ROOT, run_jobs, same_json


class CompareTests(unittest.TestCase):
    def test_line_endings_and_formatting_ignored(self):
        self.assertTrue(same_json(b'{\r\n  "a": 1\r\n}\r\n', b'{"a":1}\n'))

    def test_value_change_detected(self):
        self.assertFalse(same_json(b'{"a": 1}', b'{"a": 2}'))

    def test_type_changes_detected(self):
        self.assertFalse(same_json(b'{"ok": true}', b'{"ok": 1}'))
        self.assertFalse(same_json(b'{"n": 1}', b'{"n": 1.0}'))
        self.assertFalse(same_json(b'[false]', b'[0]'))
        self.assertTrue(same_json(b'{"a": [1, {"b": null}]}', b'{"a":[1,{"b":null}]}'))

    def test_invalid_json_is_not_same(self):
        self.assertFalse(same_json(b'{"a": 1}', b'not json'))


class JobTests(unittest.TestCase):
    def test_every_job_targets_a_committed_result_and_checker(self):
        for result, script, _ in JOBS:
            self.assertTrue((REPO_ROOT / F / result).is_file(), result)
            self.assertTrue((REPO_ROOT / "docs" / "tools" / script).is_file(), script)

    def test_missing_checker_counts_as_error(self):
        run = run_jobs(REPO_ROOT, (("cfd8_decision_traceability_check_results.json", "no_such_checker.py", ()),))
        self.assertEqual(run["counts"], {"reproduced": 0, "differs": 0, "error": 1})

    def test_single_job_reproduces(self):
        job = [j for j in JOBS if j[0] == "cfd8_decision_traceability_check_results.json"]
        run = run_jobs(REPO_ROOT, tuple(job))
        self.assertEqual(run["counts"]["reproduced"], 1)
        self.assertIn("feasibility_table_json_sha256", run["local_evidence"])


if __name__ == "__main__":
    unittest.main()
