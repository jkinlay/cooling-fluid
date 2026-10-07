"""Check the public CFD-3 CSV projection against its JSON candidate records."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Callable


UNKNOWN = "UNKNOWN"
NUMERIC_COLUMNS = {"NIST low (°C)", "NIST high (°C)", "Flash point (°C)"}
NUMERIC_TOLERANCE = 0.005


def _unknown(value: Any) -> str:
    """Use the dataset's CSV sentinel for absent scalar fields."""
    return UNKNOWN if value is None or value == "" else str(value)


def _not_retrieved(value: Any) -> str:
    """Supplier-record columns spell an absent value as "Not retrieved" in the tracked CSV."""
    return "Not retrieved" if value is None or value == "" else str(value)


def _number(value: Any) -> float | str:
    """Match the six-decimal precision displayed by the tracked CSV."""
    return UNKNOWN if value is None else round(float(value), 6)


def _relation(value: Any) -> str:
    """The CSV spells an equality relation as EQ; inequalities remain symbols."""
    if value is None:
        return UNKNOWN
    return "EQ" if value == "=" else str(value)


def _fire_evidence(candidate: dict[str, Any]) -> str:
    fire = candidate.get("fire_evidence") or {}
    category = fire.get("supplier_ghs_flammable_liquid_category")
    if category is not None:
        return f"GHS Flam. Liq. {category}"
    codes = fire.get("supplier_hazard_codes") or []
    if "H225" in codes:
        return "Supplier H225"
    description = fire.get("government_description")
    source_id = (candidate.get("flash_point") or {}).get("source_id")
    if isinstance(description, str) and source_id and str(source_id).endswith("_niosh"):
        if description.startswith("Class "):
            return "NIOSH " + description.split(" Flammable", 1)[0]
    return UNKNOWN


def _flags(value: Any) -> str:
    """CSV uses a semicolon-plus-space list and spaces in place of flag underscores."""
    if not value:
        return ""
    return "; ".join(str(item).replace("_", " ") for item in value)


def _vapour_pressure_lead(candidate: dict[str, Any]) -> str:
    leads = candidate.get("additional_source_leads") or {}
    if not leads.get("antoine_section_located"):
        return "Not located"
    if leads.get("antoine_covers_full_45_55_c"):
        return "Full 45–55°C range"
    return "Other / partial range"


def _vaporization_heat_lead(candidate: dict[str, Any]) -> str:
    leads = candidate.get("additional_source_leads") or {}
    return "Located; not extracted" if leads.get("vaporization_enthalpy_data_located") else "Not located"


ColumnDeriver = Callable[[dict[str, Any]], Any]

# This is deliberately an explicit, reviewed CSV-to-JSON projection table.
COLUMN_MAPPINGS: dict[str, ColumnDeriver] = {
    "ID": lambda c: _unknown(c.get("candidate_id")),  # candidate_id
    "Compound": lambda c: _unknown(c.get("name")),  # name
    "CAS": lambda c: _unknown(c.get("cas")),  # cas
    "Family": lambda c: _unknown(c.get("family")),  # family
    "Boiling screen": lambda c: _unknown((c.get("normal_boiling_point") or {}).get("status")),  # normal_boiling_point.status
    "NIST low (°C)": lambda c: _number((c.get("normal_boiling_point") or {}).get("evidence_envelope_low_c")),  # normal_boiling_point.evidence_envelope_low_c
    "NIST high (°C)": lambda c: _number((c.get("normal_boiling_point") or {}).get("evidence_envelope_high_c")),  # normal_boiling_point.evidence_envelope_high_c
    "Flash point (°C)": lambda c: _number((c.get("flash_point") or {}).get("selected_value_c")),  # flash_point.selected_value_c
    "FP relation": lambda c: _relation((c.get("flash_point") or {}).get("relation")),  # flash_point.relation
    "Fire evidence": _fire_evidence,  # fire_evidence plus flash_point.source_id
    "Overall profile": lambda c: _unknown(c.get("overall_profile_status")),  # overall_profile_status
    "Evidence flags": lambda c: _flags(c.get("flags")),  # flags
    "Next evidence need": lambda c: _unknown(c.get("next_evidence_need")),  # next_evidence_need
    "Boiling source ID": lambda c: _unknown((c.get("normal_boiling_point") or {}).get("source_id")),  # normal_boiling_point.source_id
    "Flash source ID": lambda c: _unknown((c.get("flash_point") or {}).get("source_id")),  # flash_point.source_id
    "Supplier bp report": lambda c: _not_retrieved((c.get("normal_boiling_point") or {}).get("supplier_reported")),  # normal_boiling_point.supplier_reported; null -> "Not retrieved"
    "Flash-point method": lambda c: _unknown((c.get("flash_point") or {}).get("method")),  # flash_point.method
    "Formula": lambda c: _unknown(c.get("formula")),  # formula
    "Catalogue purity": lambda c: _not_retrieved(c.get("sample_purity")),  # sample_purity; null -> "Not retrieved"
    "Vapour-pressure lead": _vapour_pressure_lead,  # additional_source_leads Antoine fields
    "Vaporization heat lead": _vaporization_heat_lead,  # additional_source_leads.vaporization_enthalpy_data_located
}


def _numeric_match(csv_value: str, derived_value: Any) -> bool:
    csv_text = _unknown(csv_value)
    derived_text = _unknown(derived_value)
    if csv_text == UNKNOWN or derived_text == UNKNOWN:
        return csv_text == derived_text
    try:
        return abs(float(csv_text) - float(derived_value)) <= NUMERIC_TOLERANCE
    except (TypeError, ValueError):
        return False


def _value_matches(column: str, csv_value: str, derived_value: Any) -> bool:
    if column in NUMERIC_COLUMNS:
        return _numeric_match(csv_value, derived_value)
    return csv_value == str(derived_value)


def evaluate(dataset: dict[str, Any], rows: list[dict[str, str]], fieldnames: list[str] | None) -> dict[str, Any]:
    """Return a public-safe, deterministic comparison report body."""
    expected_columns = list(COLUMN_MAPPINGS)
    actual_columns = fieldnames or []
    missing_columns = [column for column in expected_columns if column not in actual_columns]
    extra_columns = [column for column in actual_columns if column not in COLUMN_MAPPINGS]
    header_status = "FAIL" if missing_columns else "PASS"
    if extra_columns and header_status == "PASS":
        header_status = "INFO"

    candidates_raw = dataset.get("candidates", [])
    candidates = [item for item in candidates_raw if isinstance(item, dict)] if isinstance(candidates_raw, list) else []
    candidate_ids = [candidate.get("candidate_id") for candidate in candidates]
    candidate_id_counts = Counter(candidate_ids)
    candidates_by_id = {candidate_id: candidate for candidate_id, candidate in ((c.get("candidate_id"), c) for c in candidates) if candidate_id_counts[candidate_id] == 1}
    csv_ids = [row.get("ID") for row in rows]
    csv_id_counts = Counter(csv_ids)
    matched_rows = sum(1 for candidate_id in csv_ids if candidate_id_counts[candidate_id] == 1 and csv_id_counts[candidate_id] == 1)
    row_status = "PASS" if len(rows) == len(candidates) and matched_rows == len(rows) else "FAIL"

    columns: list[dict[str, Any]] = []
    for column, derive in COLUMN_MAPPINGS.items():
        if column not in actual_columns:
            columns.append({"column": column, "mismatch_count": 0, "status": "FAIL"})
            continue
        mismatches = 0
        for row in rows:
            candidate_id = row.get("ID")
            candidate = candidates_by_id.get(candidate_id)
            if candidate is None or csv_id_counts[candidate_id] != 1:
                mismatches += 1
            elif not _value_matches(column, row.get(column, ""), derive(candidate)):
                mismatches += 1
        columns.append({"column": column, "mismatch_count": mismatches, "status": "PASS" if mismatches == 0 else "FAIL"})

    mapped_columns = len(COLUMN_MAPPINGS)
    report = {
        "all_checks_pass": header_status != "FAIL" and row_status == "PASS" and all(item["status"] == "PASS" for item in columns),
        "checks": {
            "header_complete": {
                "extra_column_count": len(extra_columns),
                "missing_column_count": len(missing_columns),
                "status": header_status,
            },
            "row_alignment": {
                "csv_row_count": len(rows),
                "dataset_candidate_count": len(candidates),
                "matched_row_count": matched_rows,
                "status": row_status,
            },
        },
        "columns": columns,
        "mapping_coverage": {
            "mapped_column_count": mapped_columns,
            "unmapped_column_count": 0,
            "unmapped_columns": [],
        },
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--csv", dest="csv_path", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    dataset_raw = args.dataset.read_bytes()
    csv_raw = args.csv_path.read_bytes()
    dataset = json.loads(dataset_raw)
    if not isinstance(dataset, dict):
        raise ValueError("dataset top level must be an object")
    with args.csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames
    report = evaluate(dataset, rows, fieldnames)
    report["input_sha256"] = {
        "csv": hashlib.sha256(csv_raw).hexdigest(),
        "dataset": hashlib.sha256(dataset_raw).hexdigest(),
    }
    report["inputs"] = {"csv": args.csv_path.as_posix(), "dataset": args.dataset.as_posix()}
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    raise SystemExit(0 if report["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
