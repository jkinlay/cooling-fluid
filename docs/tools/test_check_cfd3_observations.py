"""Synthetic regression tests for the CFD-3 observation checker."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("check_cfd3_observations.py")
SPEC = importlib.util.spec_from_file_location("check_cfd3_observations", MODULE_PATH)
CHECKER = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(CHECKER)


def observation(**changes: object) -> dict:
    row = {
        "observation_id": "synthetic-1",
        "candidate_id": "synthetic-candidate",
        "property": "boiling_marker",
        "reported_value": "400 K",
        "reported_unit": "K",
        "relation": "=",
        "value": 400.0,
        "low": 400.0,
        "high": 400.0,
        "reported_plus_minus": None,
        "temperature_low_c": 126.85,
        "temperature_high_c": 126.85,
        "pressure": None,
        "method": None,
        "note": None,
        "evidence_type": "SOURCE_REPORTED_NOT_PROJECT_MEASUREMENT",
        "source_id": "synthetic-source",
    }
    row.update(changes)
    return row


class ObservationCheckerTests(unittest.TestCase):
    def report(self, *rows: dict) -> dict:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text(json.dumps({"observations": list(rows)}), encoding="utf-8")
            return CHECKER.evaluate(json.loads(path.read_text(encoding="utf-8")), path)

    def test_passing_fixture(self) -> None:
        report = self.report(observation())
        self.assertTrue(all(check["status"] == "PASS" for check in report["checks"].values()))

    def test_unit_conversion_failure(self) -> None:
        report = self.report(observation(temperature_low_c=125.0))
        self.assertEqual(report["checks"]["unit_conversion"]["status"], "FAIL")

    def test_unit_vocabulary_failure(self) -> None:
        report = self.report(observation(reported_unit="rankine"))
        self.assertEqual(report["checks"]["unit_vocabulary"]["status"], "FAIL")

    def test_text_only_temperature_is_info(self) -> None:
        row = observation(reported_unit=None, value=None, low=None, high=None,
                          temperature_low_c=None, temperature_high_c=None)
        report = self.report(row)
        self.assertEqual(report["checks"]["unit_vocabulary"]["status"], "INFO")

    def test_numeric_temperature_without_unit_fails(self) -> None:
        report = self.report(observation(reported_unit=None))
        self.assertEqual(report["checks"]["unit_vocabulary"]["status"], "FAIL")

    def test_relation_preserved_failure(self) -> None:
        report = self.report(observation(relation="<", reported_value="400 K"))
        self.assertEqual(report["checks"]["relation_preserved"]["status"], "FAIL")

    def test_uncertainty_fields_failure(self) -> None:
        report = self.report(
            observation(
                reported_value="400 +/- 4 K",
                reported_plus_minus=4.0,
                low=396.0,
                high=404.0,
                temperature_low_c=123.0,
                temperature_high_c=130.85,
            )
        )
        self.assertEqual(report["checks"]["uncertainty_fields"]["status"], "FAIL")

    def test_missing_states_failure(self) -> None:
        report = self.report(observation(low=None))
        self.assertEqual(report["checks"]["missing_states"]["status"], "FAIL")

    def test_evidence_type_failure(self) -> None:
        report = self.report(observation(evidence_type="SYNTHETIC"))
        self.assertEqual(report["checks"]["evidence_type"]["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
