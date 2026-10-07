"""Synthetic-fixture tests for the CFD-3 identity reconciliation checker."""
from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from check_cfd3_identity import EXPECTED_CANDIDATE_IDS, evaluate


def valid_cas(number: int) -> str:
    body = f"100{number:03d}00"
    digit = sum(int(value) * multiplier for multiplier, value in enumerate(reversed(body), 1)) % 10
    return f"{body[:-2]}-{body[-2:]}-{digit}"


def passing_fixture() -> dict:
    candidates = [{"candidate_id": candidate_id, "cas": valid_cas(index), "source_id": "S000"}
                  for index, candidate_id in enumerate(EXPECTED_CANDIDATE_IDS, 1)]
    observations = [{"observation_id": f"O{index:03d}", "candidate_id": candidate_id, "source_id": "S000"}
                    for index, candidate_id in enumerate(EXPECTED_CANDIDATE_IDS, 1)]
    return {
        "candidates": candidates,
        "observations": observations,
        "sources": [{"source_id": "S000"}, {"source_id": "S001"}],
        "summary": {"records": 32, "property_observations": 32, "source_records": 2},
    }


class IdentityCheckTests(unittest.TestCase):
    def write_fixture(self, dataset: dict, mutate_csv=None) -> tuple[tempfile.TemporaryDirectory, Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        csv_path = root / "fixture.csv"
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["ID", "CAS"])
            writer.writeheader()
            for candidate in dataset["candidates"]:
                row = {"ID": candidate["candidate_id"], "CAS": candidate["cas"]}
                if mutate_csv:
                    row = mutate_csv(row)
                writer.writerow(row)
        return temporary, csv_path

    def evaluate_fixture(self, dataset: dict, mutate_csv=None) -> dict:
        temporary, csv_path = self.write_fixture(dataset, mutate_csv)
        self.addCleanup(temporary.cleanup)
        return evaluate(dataset, csv_path)

    def test_passing_fixture(self) -> None:
        report = self.evaluate_fixture(passing_fixture())
        self.assertTrue(report["all_checks_pass"])
        for name, check in report["checks"].items():
            self.assertEqual("PASS", check["status"], name)
        self.assertIn("INFO unreferenced source_id: S001", report["checks"]["source_ids"]["findings"])

    def test_candidate_ids_failing_fixture(self) -> None:
        dataset = passing_fixture()
        dataset["candidates"][-1]["candidate_id"] = "CF031"
        self.assertEqual("FAIL", self.evaluate_fixture(dataset)["checks"]["candidate_ids"]["status"])

    def test_cas_check_digit_failing_fixture(self) -> None:
        dataset = passing_fixture()
        dataset["candidates"][0]["cas"] = "1001-00-0"
        self.assertEqual("FAIL", self.evaluate_fixture(dataset)["checks"]["cas_format_and_check_digit"]["status"])

    def test_observation_references_failing_fixture(self) -> None:
        dataset = passing_fixture()
        dataset["observations"][0]["source_id"] = "MISSING"
        self.assertEqual("FAIL", self.evaluate_fixture(dataset)["checks"]["observation_refs"]["status"])

    def test_source_ids_failing_fixture(self) -> None:
        dataset = passing_fixture()
        dataset["sources"][1]["source_id"] = "S000"
        self.assertEqual("FAIL", self.evaluate_fixture(dataset)["checks"]["source_ids"]["status"])

    def test_summary_counts_failing_fixture(self) -> None:
        dataset = passing_fixture()
        dataset["summary"]["records"] = 31
        self.assertEqual("FAIL", self.evaluate_fixture(dataset)["checks"]["summary_counts"]["status"])

    def test_csv_identity_failing_fixture(self) -> None:
        dataset = passing_fixture()
        report = self.evaluate_fixture(dataset, lambda row: {**row, "CAS": "11-11-1"} if row["ID"] == "CF001" else row)
        self.assertEqual("FAIL", report["checks"]["csv_identity_match"]["status"])


if __name__ == "__main__":
    unittest.main()
