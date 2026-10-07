import copy
import unittest

from check_cfd6_fire_evidence_rules import evaluate


def dataset():
    def cand(value, sign, relation, category, classification, codes):
        return {
            "flash_point": {"selected_value_c": value, "sign_description": sign, "relation": relation},
            "fire_evidence": {
                "supplier_ghs_flammable_liquid_category": category,
                "supplier_classification": classification,
                "supplier_hazard_codes": codes,
                "application_acceptance_status": "UNKNOWN",
            },
        }
    return {"candidates": [
        cand(-1.5, "BELOW_ZERO", "=", 2, "Flam. Liq. 2 - STOT SE 3", ["H225"]),
        cand(None, "UNKNOWN", None, None, None, ["H225"]),
    ]}


REGISTER = {"profiles": [{"constraints": [{"domain": "fire_behavior", "hard_rule_adopted": False}]}]}


class FireRuleTests(unittest.TestCase):
    def test_clean_fixture_passes(self):
        report = evaluate(dataset(), REGISTER)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["context_counts"]["ghs_category_absent_with_hazard_code_not_imputed"], 1)

    def test_missing_flash_with_sign_fails(self):
        data = dataset()
        data["candidates"][1]["flash_point"]["sign_description"] = "BELOW_ZERO"
        self.assertEqual(evaluate(data, REGISTER)["rule_counts"]["missing_flash_stays_unknown"]["FAIL"], 1)

    def test_inferred_category_fails(self):
        data = dataset()
        data["candidates"][1]["fire_evidence"]["supplier_ghs_flammable_liquid_category"] = 2
        self.assertEqual(evaluate(data, REGISTER)["rule_counts"]["no_inferred_ghs_category"]["FAIL"], 1)

    def test_acceptance_without_adopted_requirement_fails(self):
        data = dataset()
        data["candidates"][0]["fire_evidence"]["application_acceptance_status"] = "PASS"
        self.assertEqual(evaluate(data, REGISTER)["status"], "FAIL")

    def test_adopted_requirement_makes_rule_not_applicable(self):
        register = copy.deepcopy(REGISTER)
        register["profiles"][0]["constraints"][0]["hard_rule_adopted"] = True
        counts = evaluate(dataset(), register)["rule_counts"]["fire_acceptance_needs_adopted_requirement"]
        self.assertEqual(counts["NOT_APPLICABLE"], 2)

    def test_output_has_no_values(self):
        text = repr(evaluate(dataset(), REGISTER))
        for token in ("-1.5", "STOT", "H225"):
            self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
