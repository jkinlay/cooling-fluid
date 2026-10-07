"""Synthetic tests for the aggregate-only CFD-3 discrepancy report."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


sys.path.insert(0, str(Path(__file__).parent))
import check_cfd3_discrepancies as checker


def observation(candidate_id: str, property_name: str, low: object, high: object) -> dict[str, object]:
    return {
        "candidate_id": candidate_id,
        "property": property_name,
        "temperature_low_c": low,
        "temperature_high_c": high,
    }


class DiscrepancyCheckerTests(unittest.TestCase):
    def report_for(self, observations: list[dict[str, object]]) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text(json.dumps({"observations": observations}), encoding="utf-8", newline="\n")
            return checker.evaluate(json.loads(path.read_text(encoding="utf-8")), path)[0]

    def test_classifies_consistent_non_overlapping_buckets_single_and_text(self) -> None:
        observations = [
            observation("CF001", "consistent", 10, 12),
            observation("CF001", "consistent", 11, 13),
            observation("CF002", "one_c", 0, 0), observation("CF002", "one_c", 0.5, 0.5),
            observation("CF003", "five_c", 0, 1), observation("CF003", "five_c", 5, 5),
            observation("CF004", "twenty_c", 0, 1), observation("CF004", "twenty_c", 20, 20),
            observation("CF005", "over_twenty_c", 0, 1), observation("CF005", "over_twenty_c", 21, 21),
            observation("CF006", "single", 7, 8),
            observation("CF007", "text", None, None),
        ]
        report = self.report_for(observations)
        self.assertEqual("INFO", report["status"])
        self.assertEqual(1, report["per_property"]["consistent"]["consistent"])
        self.assertEqual(1, report["per_property"]["single"]["single_or_none"])
        self.assertEqual(1, report["per_property"]["text"]["text_only_rows"])
        self.assertEqual(
            {"<=1C": 1, "1-5C": 1, "5-20C": 1, ">20C": 1},
            report["totals"]["spread_buckets"],
        )

    def test_low_greater_than_high_is_structural_failure(self) -> None:
        report = self.report_for([observation("CF001", "p", 4, 3)])
        self.assertEqual("FAIL", report["status"])
        self.assertEqual(1, report["structural_problem_counts"]["celsius_low_greater_than_high"])

    def test_default_report_contains_no_fixture_ids(self) -> None:
        report = self.report_for([
            observation("CF001", "p", 1, 2),
            observation("CF001", "p", 3, 4),
        ])
        rendered = json.dumps(report, sort_keys=True)
        self.assertNotIn("CF001", rendered)
        self.assertNotIn("observation_id", rendered)


if __name__ == "__main__":
    unittest.main()
