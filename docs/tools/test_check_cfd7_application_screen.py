import copy
import json
from pathlib import Path
import unittest

from check_cfd7_application_screen import check_rules, evaluate, profile_ready, screen_candidate

RULES = json.loads((Path(__file__).resolve().parents[1] / "feasibility" / "cfd7_application_screen_rules.json").read_text(encoding="utf-8"))


def constraint(adopted=True):
    return {"hard_rule_adopted": adopted, "candidate_screening_rule": adopted}


def register(ready=True, state="APPROVED_FOR_CANDIDATE_JUDGEMENT", adopted=True):
    return {"candidate_judgement_ready": ready,
            "profiles": [{"profile_state": state, "constraints": [constraint(adopted)]}]}


def res(evidence, outcome):
    return {"evidence": evidence, "outcome": outcome}


class RulesFileTests(unittest.TestCase):
    def test_committed_rules_well_formed(self):
        self.assertEqual(check_rules(RULES), [])

    def test_reordered_steps_fail(self):
        rules = copy.deepcopy(RULES)
        rules["evaluation_order"][3], rules["evaluation_order"][4] = rules["evaluation_order"][4], rules["evaluation_order"][3]
        self.assertIn("order", check_rules(rules))

    def test_numeric_limit_fails(self):
        rules = copy.deepcopy(RULES)
        rules["evaluation_order"][3]["max"] = 1
        self.assertIn("numeric_limit", check_rules(rules))

    def test_unknown_outcome_status_fails(self):
        rules = copy.deepcopy(RULES)
        rules["evaluation_order"][6]["on_match"] = "PASS"
        self.assertIn("outcome:all_measured_inside", check_rules(rules))


class ReadinessTests(unittest.TestCase):
    def test_register_not_ready(self):
        reg = register(ready=False)
        self.assertEqual(profile_ready(reg, reg["profiles"][0]), (False, "profile_gate"))

    def test_draft_profile_not_ready(self):
        reg = register(state="RESEARCH_DRAFT")
        self.assertEqual(profile_ready(reg, reg["profiles"][0]), (False, "profile_gate"))

    def test_proposed_constraints_only_not_ready(self):
        reg = register(adopted=False)
        self.assertEqual(profile_ready(reg, reg["profiles"][0]), (False, "adopted_constraints_only"))
        self.assertEqual(evaluate(RULES, reg)["profile_readiness_counts"], {"SCREEN_NOT_READY_adopted_constraints_only": 1})


class ScreenTests(unittest.TestCase):
    def test_not_ready_never_survives(self):
        self.assertEqual(screen_candidate(False, True, [res("MEASURED", "INSIDE")])[0], "SCREEN_NOT_READY")

    def test_identity_gate_before_constraints(self):
        self.assertEqual(screen_candidate(True, False, [res("MEASURED", "OUTSIDE")]), ("UNKNOWN", "identity_gate"))

    def test_measured_fail_beats_everything(self):
        status = screen_candidate(True, True, [res("PREDICTED", "OUTSIDE"), res("MEASURED", "OUTSIDE"), res("MISSING", None)])
        self.assertEqual(status[0], "EXCLUDED_MEASURED_HARD_FAIL")

    def test_predicted_fail_deferred(self):
        self.assertEqual(screen_candidate(True, True, [res("PREDICTED", "OUTSIDE"), res("MEASURED", "INSIDE")])[0], "DEFERRED_PREDICTED_FAIL")

    def test_predicted_inside_is_not_pass(self):
        self.assertEqual(screen_candidate(True, True, [res("PREDICTED", "INSIDE")]), ("UNKNOWN", "unresolved_constraint"))

    def test_missing_overlap_conflict_unknown(self):
        for r in (res("MISSING", None), res("MEASURED", "OVERLAP"), res("MEASURED", "CONFLICT")):
            self.assertEqual(screen_candidate(True, True, [r, res("MEASURED", "INSIDE")])[0], "UNKNOWN")

    def test_all_measured_inside_survives(self):
        self.assertEqual(screen_candidate(True, True, [res("MEASURED", "INSIDE")] * 2), ("SURVIVES_SCREEN", "all_measured_inside"))

    def test_bad_label_rejected(self):
        with self.assertRaises(ValueError):
            screen_candidate(True, True, [res("ESTIMATED", "INSIDE")])


if __name__ == "__main__":
    unittest.main()
