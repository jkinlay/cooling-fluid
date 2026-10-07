import unittest

from check_cfd7_qualification_status import evaluate


def dataset():
    qualification = {"electrical_resistivity": "NOT_ASSESSED", "dielectric_breakdown": "NOT_ASSESSED", "materials_compatibility": "NOT_ASSESSED"}
    return {
        "candidates": [
            {"overall_profile_status": "UNKNOWN", "other_qualification": dict(qualification)},
            {"overall_profile_status": "FAIL", "other_qualification": dict(qualification)},
        ],
        "summary": {"qualified_coolants": 0},
    }


class QualificationTests(unittest.TestCase):
    def test_clean_fixture_passes(self):
        report = evaluate(dataset())
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["context_counts"]["permittivity_field_absent"], 2)

    def test_unassessed_marked_pass_fails(self):
        data = dataset()
        data["candidates"][0]["other_qualification"]["materials_compatibility"] = "PASS"
        self.assertEqual(evaluate(data)["rule_counts"]["unassessed_not_pass"]["FAIL"], 1)

    def test_merged_electrical_field_fails(self):
        data = dataset()
        data["candidates"][0]["other_qualification"]["resistivity_and_breakdown"] = "NOT_ASSESSED"
        self.assertEqual(evaluate(data)["rule_counts"]["electrical_properties_distinct"]["FAIL"], 1)

    def test_qualified_profile_with_unassessed_fields_fails(self):
        data = dataset()
        data["candidates"][0]["overall_profile_status"] = "PASS"
        self.assertEqual(evaluate(data)["rule_counts"]["no_qualified_candidate"]["FAIL"], 1)

    def test_nonzero_qualified_summary_fails(self):
        data = dataset()
        data["summary"]["qualified_coolants"] = 1
        self.assertEqual(evaluate(data)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
