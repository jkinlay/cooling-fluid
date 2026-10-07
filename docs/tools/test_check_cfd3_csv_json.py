"""Synthetic tests for the CFD-3 CSV/JSON consistency checker."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("check_cfd3_csv_json.py")
SPEC = importlib.util.spec_from_file_location("check_cfd3_csv_json", MODULE_PATH)
assert SPEC and SPEC.loader
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


def candidate() -> dict[str, object]:
    return {
        "candidate_id": "CF001", "name": "Synthetic compound", "cas": "1-11-1", "family": "Synthetic",
        "formula": "C1", "sample_purity": "99%", "overall_profile_status": "UNKNOWN",
        "flags": ["ONE_FLAG"], "next_evidence_need": "Need evidence.",
        "normal_boiling_point": {"status": "PASS", "evidence_envelope_low_c": 49.1251,
            "evidence_envelope_high_c": 50.1251, "source_id": "bp-source", "supplier_reported": "49–50°C"},
        "flash_point": {"selected_value_c": -20.1251, "relation": "=", "method": "closed cup", "source_id": "fp-source"},
        "fire_evidence": {"supplier_ghs_flammable_liquid_category": 2, "supplier_hazard_codes": ["H225"]},
        "additional_source_leads": {"antoine_section_located": True, "antoine_covers_full_45_55_c": True,
            "vaporization_enthalpy_data_located": True},
    }


def rows_for(item: dict[str, object]) -> list[dict[str, str]]:
    return [{column: str(deriver(item)) for column, deriver in CHECKER.COLUMN_MAPPINGS.items()}]


class CsvJsonCheckerTests(unittest.TestCase):
    def report(self, rows: list[dict[str, str]], headers: list[str] | None = None) -> dict[str, object]:
        return CHECKER.evaluate({"candidates": [candidate()]}, rows, headers or list(CHECKER.COLUMN_MAPPINGS))

    def test_full_pass(self) -> None:
        report = self.report(rows_for(candidate()))
        self.assertTrue(report["all_checks_pass"])

    def test_numeric_mismatch(self) -> None:
        rows = rows_for(candidate())
        rows[0]["NIST low (°C)"] = "49.14"
        report = self.report(rows)
        column = next(item for item in report["columns"] if item["column"] == "NIST low (°C)")
        self.assertEqual((column["status"], column["mismatch_count"]), ("FAIL", 1))

    def test_text_mismatch(self) -> None:
        rows = rows_for(candidate())
        rows[0]["Compound"] = "Different synthetic compound"
        report = self.report(rows)
        column = next(item for item in report["columns"] if item["column"] == "Compound")
        self.assertEqual((column["status"], column["mismatch_count"]), ("FAIL", 1))

    def test_relation_convention(self) -> None:
        rows = rows_for(candidate())
        self.assertEqual(rows[0]["FP relation"], "EQ")
        self.assertTrue(self.report(rows)["all_checks_pass"])
        rows[0]["FP relation"] = "="
        report = self.report(rows)
        column = next(item for item in report["columns"] if item["column"] == "FP relation")
        self.assertEqual(column["status"], "FAIL")

    def test_not_retrieved_convention(self) -> None:
        item = candidate()
        item["sample_purity"] = None
        rows = rows_for(item)
        self.assertEqual(rows[0]["Catalogue purity"], "Not retrieved")
        headers = list(CHECKER.COLUMN_MAPPINGS)
        self.assertTrue(CHECKER.evaluate({"candidates": [item]}, rows, headers)["all_checks_pass"])
        rows[0]["Catalogue purity"] = "UNKNOWN"
        report = CHECKER.evaluate({"candidates": [item]}, rows, headers)
        column = next(c for c in report["columns"] if c["column"] == "Catalogue purity")
        self.assertEqual(column["status"], "FAIL")

    def test_missing_column(self) -> None:
        rows = rows_for(candidate())
        headers = list(CHECKER.COLUMN_MAPPINGS)
        headers.remove("Formula")
        for row in rows:
            row.pop("Formula")
        report = self.report(rows, headers)
        self.assertEqual(report["checks"]["header_complete"]["status"], "FAIL")

    def test_extra_row(self) -> None:
        rows = rows_for(candidate())
        extra = dict(rows[0])
        extra["ID"] = "CF999"
        rows.append(extra)
        report = self.report(rows)
        self.assertEqual(report["checks"]["row_alignment"]["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
