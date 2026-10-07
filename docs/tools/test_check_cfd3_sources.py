"""Synthetic fixtures for check_cfd3_sources; no project chemical data is used."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("check_cfd3_sources.py")
SPEC = importlib.util.spec_from_file_location("check_cfd3_sources", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


def passing_fixture() -> dict[str, object]:
    return {
        "created_date": "2026-01-02",
        "sources": [
            {
                "source_id": "SRC-A",
                "url": "https://example.org/a",
                "locator": "section A",
                "retrieved_date": "2026-01-01",
                "retrieved_text_sha256": "a" * 64,
            },
            {
                "source_id": "SRC-B",
                "url": "https://example.org/b",
                "locator": "section B",
                "retrieved_date": "2026-01-02",
                "retrieved_text_sha256": "b" * 64,
            },
        ],
        "candidates": [
            {
                "candidate_id": "CAND-A",
                "normal_boiling_point": {
                    "source_id": "SRC-A",
                    "observation_ids": ["OBS-BOIL"],
                    "evidence_envelope_low_c": 49.0,
                    "evidence_envelope_high_c": 51.0,
                },
                "flash_point": {
                    "selected_value_c": -20.0,
                    "relation": "=",
                    "method": "closed cup",
                    "source_id": "SRC-B",
                    "observation_ids": ["OBS-FLASH"],
                },
            }
        ],
        "observations": [
            {
                "observation_id": "OBS-BOIL",
                "candidate_id": "CAND-A",
                "property": "normal_boiling_point",
                "source_id": "SRC-A",
                "temperature_low_c": 49.0,
                "temperature_high_c": 51.0,
            },
            {
                "observation_id": "OBS-FLASH",
                "candidate_id": "CAND-A",
                "property": "flash_point",
                "source_id": "SRC-B",
                "relation": "=",
                "temperature_low_c": -20.0,
            },
        ],
    }


class SourceCheckerTests(unittest.TestCase):
    def report(self, fixture: dict[str, object]) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixture.json"
            path.write_text(json.dumps(fixture), encoding="utf-8", newline="\n")
            return CHECKER.build_report(path)

    def test_passing_fixture(self) -> None:
        report = self.report(passing_fixture())
        self.assertEqual(report["overall_counts"], {"PASS": 6, "FAIL": 0, "INFO": 0})
        self.assertEqual(set(report), {"checks", "input_path", "input_sha256", "overall_counts"})

    def test_retrieved_date_failure(self) -> None:
        fixture = passing_fixture()
        fixture["sources"][0]["retrieved_date"] = "2026-02-30"
        self.assertEqual(self.report(fixture)["checks"]["retrieved_date_iso"]["status"], "FAIL")

    def test_url_well_formed_failure(self) -> None:
        fixture = passing_fixture()
        fixture["sources"][0]["url"] = "ftp://example.org/a"
        self.assertEqual(self.report(fixture)["checks"]["url_well_formed"]["status"], "FAIL")

    def test_text_hash_failure(self) -> None:
        fixture = passing_fixture()
        fixture["sources"][0]["retrieved_text_sha256"] = "A" * 64
        self.assertEqual(self.report(fixture)["checks"]["text_hash_format"]["status"], "FAIL")

    def test_duplicate_url_failure(self) -> None:
        fixture = passing_fixture()
        fixture["sources"][1]["url"] = "https://EXAMPLE.org/a#fragment"
        fixture["sources"][1]["locator"] = "section A"
        self.assertEqual(self.report(fixture)["checks"]["duplicate_urls"]["status"], "FAIL")

    def test_boiling_display_traceability_failure(self) -> None:
        fixture = passing_fixture()
        fixture["candidates"][0]["normal_boiling_point"]["evidence_envelope_high_c"] = 52.0
        self.assertEqual(
            self.report(fixture)["checks"]["boiling_display_traceability"]["status"], "FAIL"
        )

    def test_flash_display_traceability_failure(self) -> None:
        fixture = passing_fixture()
        fixture["candidates"][0]["flash_point"]["selected_value_c"] = -19.0
        self.assertEqual(
            self.report(fixture)["checks"]["flash_display_traceability"]["status"], "FAIL"
        )

    def test_null_flash_requires_null_metadata(self) -> None:
        fixture = passing_fixture()
        flash = fixture["candidates"][0]["flash_point"]
        flash["selected_value_c"] = None
        self.assertEqual(
            self.report(fixture)["checks"]["flash_display_traceability"]["status"], "FAIL"
        )

    def test_http_is_info(self) -> None:
        fixture = passing_fixture()
        fixture["sources"][0]["url"] = "http://example.org/a"
        self.assertEqual(self.report(fixture)["checks"]["url_well_formed"]["status"], "INFO")

    def test_duplicate_url_with_distinct_locator_is_info(self) -> None:
        fixture = passing_fixture()
        fixture["sources"][1]["url"] = "https://example.org/a"
        self.assertEqual(self.report(fixture)["checks"]["duplicate_urls"]["status"], "INFO")


if __name__ == "__main__":
    unittest.main()
