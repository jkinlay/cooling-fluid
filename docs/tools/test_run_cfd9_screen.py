import copy
import json
from pathlib import Path
import unittest

from run_cfd9_screen import constraint_result, identity_resolved, run, safe_path, window_outcome

FEAS = Path(__file__).resolve().parents[1] / "feasibility"
RULES = json.loads((FEAS / "cfd7_application_screen_rules.json").read_text(encoding="utf-8"))
SOURCE = "SOURCE_REPORTED_NOT_PROJECT_MEASUREMENT"
WINDOW = {"id": "W", "domain": "normal_boiling_point", "status": "ADOPTED", "hard_rule_adopted": True,
          "candidate_screening_rule": True, "value": {"min": 10, "max": 20},
          "inclusive_boundary": {"lower": True, "upper": True}}


def register(state="RESEARCH_FROZEN", policy=True):
    reg = {"candidate_judgement_ready": True,
           "profiles": [{"profile_id": "P", "profile_state": state, "constraints": [copy.deepcopy(WINDOW)]},
                        {"profile_id": "Q", "profile_state": "RESEARCH_DRAFT", "constraints": []}]}
    if policy:
        reg["screening_evidence_policy"] = {"source_reported_counts_as": "MEASURED",
                                            "applies_to_evidence_types": [SOURCE], "label": "SOURCE_REPORTED"}
    return reg


def dataset(*envelopes):
    cands, obs = [], []
    for i, env in enumerate(envelopes):
        cid = f"X{i}"
        ids = []
        for j, (lo, hi) in enumerate(env):
            oid = f"{cid}-{j}"
            ids.append(oid)
            obs.append({"observation_id": oid, "candidate_id": cid, "property": "normal_boiling_point",
                        "temperature_low_c": lo, "temperature_high_c": hi, "evidence_type": SOURCE})
        cands.append({"candidate_id": cid, "cas": "c", "formula": "f", "lane": "PURE_CHEMICAL_IDENTITY",
                      "normal_boiling_point": {"observation_ids": ids}})
    return {"candidates": cands, "observations": obs}


class WindowTests(unittest.TestCase):
    def test_inclusive_bounds(self):
        self.assertEqual(window_outcome(10, 20, WINDOW), "INSIDE")
        self.assertEqual(window_outcome(5, 9.99, WINDOW), "OUTSIDE")
        self.assertEqual(window_outcome(20.01, 25, WINDOW), "OUTSIDE")
        self.assertEqual(window_outcome(9, 11, WINDOW), "OVERLAP")
        self.assertIsNone(window_outcome(None, 11, WINDOW))

    def test_non_inclusive_window_rejected(self):
        bad = dict(WINDOW, inclusive_boundary={"lower": True, "upper": False})
        with self.assertRaises(ValueError):
            window_outcome(12, 13, bad)


class RunTests(unittest.TestCase):
    def test_statuses_and_labels(self):
        data = dataset([(12, 13)], [(30, 31)], [(19, 21)], [], [(12, 13), (14, 15)])
        summary, records = run(RULES, register(), data)
        self.assertEqual(summary["status_counts_by_profile"]["P"],
                         {"SCREEN_NOT_READY": 0, "UNKNOWN": 2, "DEFERRED_PREDICTED_FAIL": 0,
                          "EXCLUDED_MEASURED_HARD_FAIL": 1, "SURVIVES_SCREEN": 2})
        self.assertEqual(summary["status_counts_by_profile"]["Q"]["SCREEN_NOT_READY"], 5)
        self.assertEqual(summary["pairs"], 10)
        self.assertEqual(summary["evidence_label_counts"], {"SOURCE_REPORTED": 4})
        survivor = next(r for r in records if r["profile_id"] == "P" and r["status"] == "SURVIVES_SCREEN")
        self.assertEqual((survivor["evidence_labels"], survivor["rules_version"]), (["SOURCE_REPORTED"], RULES["version"]))

    def test_draft_profile_never_screens(self):
        summary, _ = run(RULES, register(state="RESEARCH_DRAFT"), dataset([(12, 13)]))
        self.assertEqual(summary["status_counts_by_profile"]["P"]["SCREEN_NOT_READY"], 1)

    def test_without_policy_source_reported_cannot_screen(self):
        with self.assertRaises(ValueError):
            run(RULES, register(policy=False), dataset([(12, 13)]))

    def test_unresolved_identity_is_unknown(self):
        data = dataset([(12, 13)])
        data["candidates"][0]["cas"] = ""
        self.assertFalse(identity_resolved(data["candidates"][0]))
        summary, _ = run(RULES, register(), data)
        self.assertEqual(summary["deciding_rule_counts_by_profile"]["P"], {"identity_gate": 1})

    def test_identity_gate_before_evidence_validation(self):
        data = dataset([(12, 13)])
        data["candidates"][0]["cas"] = ""
        data["observations"][0]["evidence_type"] = "UNSUPPORTED"
        summary, _ = run(RULES, register(), data)
        self.assertEqual(summary["deciding_rule_counts_by_profile"]["P"], {"identity_gate": 1})

    def test_guard_uses_script_checkout_not_cwd(self):
        import subprocess, sys, tempfile
        tools = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["git", "init", "-q", tmp], check=True)
            out = tools.parent / "feasibility" / "_should_not_exist.json"
            proc = subprocess.run([sys.executable, str(tools / "run_cfd9_screen.py"),
                                   "--rules", str(FEAS / "cfd7_application_screen_rules.json"),
                                   "--register", str(FEAS / "acceptability_register.json"),
                                   "--dataset", str(FEAS / "feasibility_table.json"),
                                   "--summary", str(Path(tmp) / "s.json"), "--local-output", str(out)],
                                  cwd=tmp, capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse(out.exists())

    def test_cited_observation_of_other_candidate_rejected(self):
        data = dataset([(12, 13)], [(14, 15)])
        data["candidates"][0]["normal_boiling_point"]["observation_ids"] = ["X1-0"]
        with self.assertRaises(ValueError):
            run(RULES, register(), data)

    def test_inverted_cited_bounds_rejected_even_when_hidden(self):
        data = dataset([(19, 11), (14, 15)])
        with self.assertRaises(ValueError):
            run(RULES, register(), data)

    def test_summary_paths_are_repo_relative_or_basename(self):
        repo = Path(__file__).resolve().parents[2]
        self.assertEqual(safe_path(FEAS / "feasibility_table.json", repo), "docs/feasibility/feasibility_table.json")
        outside = repo.parent / "elsewhere" / "input.json"
        self.assertEqual(safe_path(outside, repo), "input.json")

    def test_unsupported_domain_rejected(self):
        reg = register()
        reg["profiles"][0]["constraints"][0]["domain"] = "viscosity"
        with self.assertRaises(ValueError):
            constraint_result(reg, dataset([(12, 13)])["candidates"][0], reg["profiles"][0]["constraints"][0], {})


if __name__ == "__main__":
    unittest.main()
