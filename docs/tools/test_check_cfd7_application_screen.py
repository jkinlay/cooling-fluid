import copy
import hashlib
import subprocess
import sys
import tempfile
import json
from pathlib import Path
import unittest

from check_cfd7_application_screen import check_rules, evaluate, evidence_policy, profile_ready, screen_candidate, screen_evidence, screen_record

RULES = json.loads((Path(__file__).resolve().parents[1] / "feasibility" / "cfd7_application_screen_rules.json").read_text(encoding="utf-8"))
REGISTER = json.loads((Path(__file__).resolve().parents[1] / "feasibility" / "acceptability_register.json").read_text(encoding="utf-8"))
SOURCE = "SOURCE_REPORTED_NOT_PROJECT_MEASUREMENT"


def constraint(adopted=True):
    return {"hard_rule_adopted": adopted, "candidate_screening_rule": adopted, "status": "ADOPTED" if adopted else "PROPOSED"}


def register(ready=True, state="RESEARCH_FROZEN", adopted=True):
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

    def test_numeric_limit_under_any_name_fails(self):
        for key in ("upper_bound", "temperature_c", "anything"):
            rules = copy.deepcopy(RULES)
            rules["evaluation_order"][3][key] = 100
            self.assertIn("numeric_limit", check_rules(rules))

    def test_nested_and_top_level_numbers_fail(self):
        for mutate in (lambda r: r.update({"window": {"lower": 1}}),
                       lambda r: r.update({"bounds": [1, 2]}),
                       lambda r: r.update({"cap": 1.5})):
            rules = copy.deepcopy(RULES)
            mutate(rules)
            self.assertIn("numeric_limit", check_rules(rules))

    def test_numeric_text_fails(self):
        rules = copy.deepcopy(RULES)
        rules["evaluation_order"][3]["upper_bound"] = "100"
        self.assertIn("numeric_limit", check_rules(rules))

    def test_version_label_exempt_only_at_top_level(self):
        rules = copy.deepcopy(RULES)
        rules["version"] = "2"
        self.assertNotIn("numeric_limit", check_rules(rules))
        rules["evaluation_order"][0]["version"] = "2"
        self.assertIn("numeric_limit", check_rules(rules))

    def test_non_string_version_not_exempt(self):
        rules = copy.deepcopy(RULES)
        rules["version"] = {"revision": 2, "limit": 100}
        problems = check_rules(rules)
        self.assertIn("version", problems)
        self.assertIn("numeric_limit", problems)
        rules["version"] = 2
        self.assertIn("numeric_limit", check_rules(rules))

    def test_nested_evaluation_order_step_not_exempt(self):
        rules = copy.deepcopy(RULES)
        rules["metadata"] = {"evaluation_order": [{"step": 100, "unit": "C"}]}
        self.assertIn("numeric_limit", check_rules(rules))

    def test_step_exemption_only_in_evaluation_order(self):
        rules = copy.deepcopy(RULES)
        rules["extra"] = {"step": 3}
        self.assertIn("numeric_limit", check_rules(rules))

    def test_unknown_outcome_status_fails(self):
        rules = copy.deepcopy(RULES)
        rules["evaluation_order"][6]["on_match"] = "PASS"
        self.assertIn("outcome:all_measured_inside", check_rules(rules))

    def test_swapped_existing_status_fails(self):
        rules = copy.deepcopy(RULES)
        rules["evaluation_order"][3]["on_match"] = "SURVIVES_SCREEN"
        self.assertIn("outcome:measured_hard_fail", check_rules(rules))


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


def screen(ready, identity, *results):
    keys = [f"c{i}" for i in range(len(results))]
    return screen_candidate(ready, identity, keys, dict(zip(keys, results)))


class AdoptedStatusTests(unittest.TestCase):
    def test_flags_without_adopted_status_do_not_screen(self):
        for status in ("PROPOSED", "UNKNOWN"):
            reg = register()
            reg["profiles"][0]["constraints"][0]["status"] = status
            self.assertEqual(profile_ready(reg, reg["profiles"][0]), (False, "adopted_constraints_only"))


class SpecStateTests(unittest.TestCase):
    def test_each_spec_state_past_draft_is_ready(self):
        for state in ("RESEARCH_FROZEN", "CAMPAIGN_READY", "QUALIFICATION_READY"):
            reg = register(state=state)
            self.assertEqual(profile_ready(reg, reg["profiles"][0]), (True, ""))


class ScreenTests(unittest.TestCase):
    def test_not_ready_never_survives(self):
        self.assertEqual(screen(False, True, res("MEASURED", "INSIDE"))[0], "SCREEN_NOT_READY")

    def test_identity_gate_before_constraints(self):
        self.assertEqual(screen(True, False, res("MEASURED", "OUTSIDE")), ("UNKNOWN", "identity_gate"))

    def test_measured_fail_beats_everything(self):
        status = screen(True, True, res("PREDICTED", "OUTSIDE"), res("MEASURED", "OUTSIDE"), res("MISSING", None))
        self.assertEqual(status[0], "EXCLUDED_MEASURED_HARD_FAIL")

    def test_predicted_fail_deferred(self):
        self.assertEqual(screen(True, True, res("PREDICTED", "OUTSIDE"), res("MEASURED", "INSIDE"))[0], "DEFERRED_PREDICTED_FAIL")

    def test_predicted_inside_is_not_pass(self):
        self.assertEqual(screen(True, True, res("PREDICTED", "INSIDE")), ("UNKNOWN", "unresolved_constraint"))

    def test_missing_overlap_conflict_unknown(self):
        for r in (res("MISSING", None), res("MEASURED", "OVERLAP"), res("MEASURED", "CONFLICT")):
            self.assertEqual(screen(True, True, r, res("MEASURED", "INSIDE"))[0], "UNKNOWN")

    def test_all_measured_inside_survives(self):
        self.assertEqual(screen(True, True, res("MEASURED", "INSIDE"), res("MEASURED", "INSIDE")), ("SURVIVES_SCREEN", "all_measured_inside"))

    def test_omitted_adopted_constraint_is_missing(self):
        status = screen_candidate(True, True, ["a", "b"], {"a": res("MEASURED", "INSIDE")})
        self.assertEqual(status, ("UNKNOWN", "unresolved_constraint"))

    def test_result_for_unadopted_constraint_rejected(self):
        with self.assertRaises(ValueError):
            screen_candidate(True, True, ["a"], {"a": res("MEASURED", "INSIDE"), "z": res("MEASURED", "INSIDE")})

    def test_readiness_reason_preserved(self):
        reg = register(adopted=False)
        readiness = profile_ready(reg, reg["profiles"][0])
        self.assertEqual(screen_candidate(readiness, True, [], {}), ("SCREEN_NOT_READY", "adopted_constraints_only"))
        reg = register(ready=False)
        readiness = profile_ready(reg, reg["profiles"][0])
        self.assertEqual(screen_candidate(readiness, True, ["a"], {}), ("SCREEN_NOT_READY", "profile_gate"))

    def test_ready_tuple_screens(self):
        reg = register()
        readiness = profile_ready(reg, reg["profiles"][0])
        self.assertEqual(screen_candidate(readiness, True, ["a"], {"a": res("MEASURED", "INSIDE")}), ("SURVIVES_SCREEN", "all_measured_inside"))

    def test_unknown_readiness_reason_rejected(self):
        with self.assertRaises(ValueError):
            screen_candidate((False, "identity_gate"), True, ["a"], {})

    def test_identity_gate_before_label_validation(self):
        self.assertEqual(screen(True, False, res("ESTIMATED", "INSIDE")), ("UNKNOWN", "identity_gate"))

    def test_bad_label_rejected(self):
        with self.assertRaises(ValueError):
            screen(True, True, res("ESTIMATED", "INSIDE"))


def policy_register(**overrides):
    policy = {"source_reported_counts_as": "MEASURED", "applies_to_evidence_types": [SOURCE], "label": "SOURCE_REPORTED"}
    policy.update(overrides)
    reg = register()
    reg["screening_evidence_policy"] = policy
    return reg


class EvidencePolicyTests(unittest.TestCase):
    def test_source_reported_counts_as_measured_with_label(self):
        self.assertEqual(screen_evidence(policy_register(), SOURCE), ("MEASURED", "SOURCE_REPORTED"))

    def test_without_policy_source_reported_is_rejected(self):
        with self.assertRaises(ValueError):
            screen_evidence(register(), SOURCE)

    def test_unlisted_type_rejected(self):
        with self.assertRaises(ValueError):
            screen_evidence(policy_register(), "VENDOR_CLAIM")

    def test_missing_and_predicted_unchanged(self):
        reg = policy_register()
        self.assertEqual(screen_evidence(reg, None), ("MISSING", None))
        self.assertEqual(screen_evidence(reg, SOURCE, predicted=True), ("PREDICTED", None))

    def test_prediction_without_evidence_type_is_predicted_not_missing(self):
        reg = policy_register()
        self.assertEqual(screen_evidence(reg, None, predicted=True), ("PREDICTED", None))
        result = {"a": res(screen_evidence(reg, None, predicted=True)[0], "OUTSIDE")}
        self.assertEqual(screen_candidate(True, True, ["a"], result), ("DEFERRED_PREDICTED_FAIL", "predicted_fail"))

    def test_malformed_policy_fails_report(self):
        for bad in ({"source_reported_counts_as": "PREDICTED"}, {"applies_to_evidence_types": []}, {"label": ""}):
            reg = policy_register(**bad)
            with self.assertRaises(ValueError):
                evidence_policy(reg)
            self.assertIn("evidence_policy", evaluate(RULES, reg)["rules_problems"])

    def test_source_reported_inside_survives_and_outside_is_measured_fail(self):
        reg = policy_register()
        inside = {"a": res(screen_evidence(reg, SOURCE)[0], "INSIDE")}
        outside = {"a": res(screen_evidence(reg, SOURCE)[0], "OUTSIDE")}
        self.assertEqual(screen_candidate(True, True, ["a"], inside), ("SURVIVES_SCREEN", "all_measured_inside"))
        self.assertEqual(screen_candidate(True, True, ["a"], outside), ("EXCLUDED_MEASURED_HARD_FAIL", "measured_hard_fail"))


class LabelledRecordTests(unittest.TestCase):
    def labelled(self, reg, outcome):
        evidence, label = screen_evidence(reg, SOURCE)
        return {"evidence": evidence, "outcome": outcome, "label": label}

    def test_source_reported_label_kept_on_survivor_and_fail(self):
        reg = policy_register()
        for outcome, status in (("INSIDE", "SURVIVES_SCREEN"), ("OUTSIDE", "EXCLUDED_MEASURED_HARD_FAIL")):
            record = screen_record(True, True, ["a"], {"a": self.labelled(reg, outcome)})
            self.assertEqual((record["status"], record["evidence_labels"]), (status, ["SOURCE_REPORTED"]))

    def test_unlabelled_measurement_has_no_label(self):
        self.assertEqual(screen_record(True, True, ["a"], {"a": res("MEASURED", "INSIDE")})["evidence_labels"], [])

    def test_label_on_non_measured_rejected(self):
        for bad in ({"evidence": "PREDICTED", "outcome": "OUTSIDE", "label": "SOURCE_REPORTED"},
                    {"evidence": "MEASURED", "outcome": "INSIDE", "label": ""}):
            with self.assertRaises(ValueError):
                screen_record(True, True, ["a"], {"a": bad})


class CommittedRegisterTests(unittest.TestCase):
    """CFD-9 owner decision (Jonathan Kinlay via DevHead, 7 Oct 2026)."""

    def profile(self, pid):
        return next(p for p in REGISTER["profiles"] if p["profile_id"] == pid)

    def test_only_two_phase_immersion_is_ready(self):
        self.assertTrue(REGISTER["candidate_judgement_ready"])
        self.assertEqual(profile_ready(REGISTER, self.profile("TP_IMMERSION_F0")), (True, ""))
        for pid in ("SP_IMMERSION", "TP_DIRECT_CHIP"):
            self.assertEqual(profile_ready(REGISTER, self.profile(pid)), (False, "profile_gate"))
        report = evaluate(RULES, REGISTER)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["adopted_screening_constraints"], 1)
        self.assertEqual(report["profile_readiness_counts"], {"READY": 1, "SCREEN_NOT_READY_profile_gate": 2})

    def test_adopted_boiling_window(self):
        from check_cfd7_application_screen import adopted_constraints
        adopted = adopted_constraints(self.profile("TP_IMMERSION_F0"))
        self.assertEqual([c["id"] for c in adopted], ["TPI-BOIL-EXPLORATORY"])
        c = adopted[0]
        self.assertEqual((c["domain"], c["value"], c["inclusive_boundary"]),
                         ("normal_boiling_point", {"min": 45, "max": 60}, {"lower": True, "upper": True}))
        self.assertEqual(c["decision_provenance"]["decided_by"], "Jonathan Kinlay via DevHead")

    def test_committed_policy_labels_source_reported(self):
        self.assertEqual(screen_evidence(REGISTER, SOURCE), ("MEASURED", "SOURCE_REPORTED"))


class ReportBindingTests(unittest.TestCase):
    def test_report_records_rules_digest(self):
        tools = Path(__file__).resolve().parent
        rules_path = tools.parents[0] / "feasibility" / "cfd7_application_screen_rules.json"
        with tempfile.TemporaryDirectory() as tmp:
            reg = Path(tmp) / "register.json"
            reg.write_text(json.dumps(register()), encoding="utf-8")
            out = Path(tmp) / "out.json"
            subprocess.run([sys.executable, str(tools / "check_cfd7_application_screen.py"), "--rules", str(rules_path),
                            "--register", str(reg), "--output", str(out)], check=True)
            report = json.loads(out.read_text(encoding="utf-8"))
        self.assertEqual(report["local_evidence"]["rules_sha256"], hashlib.sha256(rules_path.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
