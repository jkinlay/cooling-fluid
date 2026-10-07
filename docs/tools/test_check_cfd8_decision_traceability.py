import copy
import unittest

from pathlib import Path

from check_cfd8_decision_traceability import REPO_ROOT, evaluate, independent_source_count, public_path


def obs(oid, cand, prop, low, high, src="s1", text="12 K"):
    return {"observation_id": oid, "candidate_id": cand, "property": prop, "source_id": src,
            "value": low, "low": low, "high": high, "temperature_low_c": low, "temperature_high_c": high,
            "reported_value": text}


def dataset():
    return {
        "candidates": [
            {"candidate_id": "A",
             "normal_boiling_point": {"observation_ids": ["o1", "o2"], "evidence_envelope_low_c": 10, "evidence_envelope_high_c": 14},
             "flash_point": {"observation_ids": ["o3"], "selected_value_c": 5}},
            {"candidate_id": "B",
             "normal_boiling_point": {"observation_ids": ["o4"], "evidence_envelope_low_c": 20, "evidence_envelope_high_c": 21},
             "flash_point": {"observation_ids": [], "selected_value_c": None}},
        ],
        "observations": [
            obs("o1", "A", "normal_boiling_point", 10, 12),
            obs("o2", "A", "normal_boiling_point", 11, 14, src="s2"),
            obs("o3", "A", "flash_point", 5, 5),
            obs("o4", "B", "normal_boiling_point", 20, 21),
        ],
    }


def fails(data, rule):
    return evaluate(data)["rule_counts"][rule]["FAIL"]


class TraceabilityTests(unittest.TestCase):
    def test_clean_fixture_passes(self):
        report = evaluate(dataset())
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["context_counts"], {"flash_point_results_citing_no_observation": 1})

    def test_dangling_observation_id_fails(self):
        data = dataset()
        data["candidates"][0]["flash_point"]["observation_ids"] = ["missing"]
        self.assertEqual(fails(data, "result_traces_to_observation"), 1)

    def test_isomer_swap_fails(self):
        data = dataset()
        data["observations"][3]["candidate_id"] = "A"
        self.assertEqual(fails(data, "no_isomer_swap"), 1)

    def test_property_mismatch_fails(self):
        data = dataset()
        data["candidates"][0]["flash_point"]["observation_ids"] = ["o1"]
        self.assertEqual(fails(data, "property_matches_field"), 1)

    def test_kelvin_left_unconverted_fails(self):
        data = dataset()
        data["candidates"][0]["normal_boiling_point"]["evidence_envelope_high_c"] = 14 + 273.15
        self.assertEqual(fails(data, "celsius_consistent"), 1)

    def test_flash_selection_not_traced_fails(self):
        data = dataset()
        data["candidates"][0]["flash_point"]["selected_value_c"] = 6
        self.assertEqual(fails(data, "celsius_consistent"), 1)

    def test_missing_with_value_fails(self):
        data = dataset()
        data["candidates"][1]["flash_point"]["selected_value_c"] = 0
        self.assertEqual(fails(data, "missing_not_value"), 1)
        self.assertEqual(fails(data, "result_traces_to_observation"), 1)

    def test_missing_as_zero_fails(self):
        data = dataset()
        data["observations"][2].update({"value": 0, "low": 0, "temperature_low_c": 0, "reported_value": "not stated"})
        self.assertEqual(fails(data, "missing_not_zero"), 1)

    def test_zero_uncertainty_without_text_fails(self):
        data = dataset()
        data["observations"][0]["reported_plus_minus"] = 0
        self.assertEqual(fails(data, "missing_not_zero"), 1)

    def test_converted_zero_celsius_is_allowed(self):
        data = dataset()
        data["observations"][2].update({"value": 273.15, "low": 273.15, "high": 273.15, "temperature_low_c": 0.0,
                                        "temperature_high_c": 0.0, "reported_value": "273.15 K", "reported_unit": "K"})
        self.assertEqual(fails(data, "missing_not_zero"), 0)

    def test_zero_raw_value_from_nonzero_kelvin_text_fails(self):
        data = dataset()
        data["observations"][2].update({"value": 0, "reported_value": "273.15 K", "reported_unit": "K"})
        self.assertEqual(fails(data, "missing_not_zero"), 1)

    def test_reported_zero_is_allowed(self):
        data = dataset()
        data["observations"][2].update({"value": 0, "low": 0, "high": 0, "temperature_low_c": 0,
                                        "temperature_high_c": 0, "reported_value": "0 degC"})
        data["candidates"][0]["flash_point"]["selected_value_c"] = 0
        self.assertEqual(evaluate(data)["status"], "PASS")

    def test_repeated_source_is_not_independent(self):
        data = dataset()
        data["observations"][1]["source_id"] = "s1"
        report = evaluate(data)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["context_counts"]["normal_boiling_point_results_with_repeated_source"], 1)
        self.assertEqual(independent_source_count(data["observations"][:2]), 1)

    def test_non_dict_result_fails(self):
        data = dataset()
        data["candidates"][0]["flash_point"] = None
        self.assertEqual(evaluate(data)["status"], "FAIL")


class PathTests(unittest.TestCase):
    def test_absolute_path_published_repo_relative(self):
        target = REPO_ROOT / "docs" / "feasibility" / "feasibility_table.json"
        self.assertEqual(public_path(target), "docs/feasibility/feasibility_table.json")

    def test_path_outside_repo_keeps_only_name(self):
        self.assertEqual(public_path(Path(REPO_ROOT.anchor) / "elsewhere" / "data.json"), "data.json")


if __name__ == "__main__":
    unittest.main()
