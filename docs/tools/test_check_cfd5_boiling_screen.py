import copy
import unittest

from check_cfd5_boiling_screen import evaluate, screen


def fixture():
    def cand(cid, status, lo, hi, oid):
        return {"candidate_id": cid, "normal_boiling_point": {"status": status, "evidence_envelope_low_c": lo, "evidence_envelope_high_c": hi, "observation_ids": [oid]}}
    return {
        "candidates": [cand("A", "PASS", 49.0, 51.0, "o1"), cand("B", "FAIL", 60.0, 61.0, "o2"), cand("C", "UNKNOWN", 54.0, 56.0, "o3")],
        "observations": [
            {"observation_id": "o1", "temperature_low_c": 49.0, "temperature_high_c": 51.0},
            {"observation_id": "o2", "temperature_low_c": 60.0, "temperature_high_c": 61.0},
            {"observation_id": "o3", "temperature_low_c": 54.0, "temperature_high_c": 56.0},
        ],
        "summary": {"boiling_pass": 1, "boiling_fail": 1, "boiling_unknown": 1},
    }


class ScreenTests(unittest.TestCase):
    def test_inclusive_bounds(self):
        self.assertEqual(screen(45.0, 55.0), "PASS")
        self.assertEqual(screen(44.9, 45.5), "UNKNOWN")
        self.assertEqual(screen(40.0, 44.99), "FAIL")
        self.assertEqual(screen(None, 50.0), "UNKNOWN")

    def test_clean_fixture_passes(self):
        report = evaluate(fixture())
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["envelopes_touching_or_crossing_a_bound"], 1)

    def test_wrong_published_status_fails(self):
        data = fixture()
        data["candidates"][2]["normal_boiling_point"]["status"] = "PASS"
        data["summary"]["boiling_pass"] = 2
        data["summary"]["boiling_unknown"] = 0
        report = evaluate(data)
        self.assertEqual(report["problem_counts"].get("status_not_reproduced"), 1)
        self.assertEqual(report["status"], "FAIL")

    def test_envelope_drift_fails(self):
        data = fixture()
        data["observations"][0]["temperature_high_c"] = 52.0
        self.assertEqual(evaluate(data)["problem_counts"].get("envelope_not_reproduced_from_cited_observations"), 1)

    def test_output_has_no_identifiers(self):
        text = repr(evaluate(fixture()))
        for token in ("o1", "'A'", "49.0"):
            self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
