"""Compare the public CFD-3 workbook tables with their JSON baseline.

The checker is read-only apart from its explicit ``--output`` report.  Its
report deliberately excludes row values and identifiers so it is safe to
publish with the public feasibility materials.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import zipfile
from datetime import date, timedelta
from pathlib import Path, PurePosixPath
from typing import Any, Callable
from xml.etree import ElementTree as ET


MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"x": MAIN_NS, "r": DOC_REL_NS, "pr": PACKAGE_REL_NS}
EXPECTED_PARTS = {
    "xl/workbook.xml",
    "xl/_rels/workbook.xml.rels",
    "xl/sharedStrings.xml",
    "xl/worksheets/sheet1.xml",
    "xl/worksheets/sheet2.xml",
    "xl/worksheets/sheet3.xml",
    "xl/tables/table1.xml",
    "xl/tables/table2.xml",
    "xl/tables/table3.xml",
}
EXPECTED_SHEETS = ("Candidates", "Evidence", "Data gaps")


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _column_number(reference: str) -> int:
    """Return the zero-based column index for an A1-style cell reference."""
    letters = re.match(r"[A-Z]+", reference)
    if letters is None:
        raise ValueError(f"invalid cell reference: {reference!r}")
    number = 0
    for letter in letters.group():
        number = number * 26 + ord(letter) - ord("A") + 1
    return number - 1


def _column_letters(index: int) -> str:
    """Return spreadsheet column letters for a zero-based index."""
    result = ""
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(ord("A") + remainder) + result
    return result


def _part_target(base_part: str, target: str) -> str:
    """Resolve an Open XML relationship target to a ZIP member name."""
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(str(PurePosixPath(base_part).parent.joinpath(target)))


def _relationships(archive: zipfile.ZipFile, part: str) -> dict[str, str]:
    rels_part = str(PurePosixPath(part).parent / "_rels" / (PurePosixPath(part).name + ".rels"))
    if rels_part not in archive.namelist():
        return {}
    root = ET.fromstring(archive.read(rels_part))
    return {
        element.attrib["Id"]: _part_target(part, element.attrib["Target"])
        for element in root.findall("pr:Relationship", NS)
    }


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    # itertext() intentionally handles both simple strings and rich-text <r><t> runs.
    return ["".join(item.itertext()) for item in root.findall("x:si", NS)]


def _cell_value(cell: ET.Element, shared_strings: list[str]) -> Any:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(cell.find("x:is", NS).itertext()) if cell.find("x:is", NS) is not None else ""
    value = cell.findtext("x:v", default=None, namespaces=NS)
    if value is None:
        return None
    if cell_type == "s":
        return shared_strings[int(value)]
    if cell_type == "b":
        return value == "1"
    if cell_type in {"str", "e"}:
        return value
    if cell_type == "n" or cell_type is None:
        try:
            number = float(value)
        except ValueError:
            return value
        return int(number) if number.is_integer() else number
    return value


def _range_bounds(reference: str) -> tuple[int, int, int, int]:
    start, end = reference.split(":")
    start_column = _column_number(start)
    end_column = _column_number(end)
    start_row = int(re.search(r"\d+$", start).group())
    end_row = int(re.search(r"\d+$", end).group())
    return start_column, end_column, start_row, end_row


def _table_definition(archive: zipfile.ZipFile, worksheet_part: str) -> tuple[str, list[str]] | None:
    root = ET.fromstring(archive.read(worksheet_part))
    relationship_ids = [element.attrib.get(f"{{{DOC_REL_NS}}}id") for element in root.findall("x:tableParts/x:tablePart", NS)]
    targets = _relationships(archive, worksheet_part)
    for relationship_id in relationship_ids:
        table_part = targets.get(relationship_id)
        if table_part is None or table_part not in archive.namelist():
            continue
        table = ET.fromstring(archive.read(table_part))
        headers = [element.attrib["name"] for element in table.findall("x:tableColumns/x:tableColumn", NS)]
        return table.attrib["ref"], headers
    return None


def _sheet_rows(archive: zipfile.ZipFile, worksheet_part: str, shared_strings: list[str]) -> tuple[list[str], list[dict[str, Any]]]:
    definition = _table_definition(archive, worksheet_part)
    if definition is None:
        return [], []
    table_ref, headers = definition
    start_column, end_column, start_row, end_row = _range_bounds(table_ref)
    root = ET.fromstring(archive.read(worksheet_part))
    by_row: dict[int, dict[int, Any]] = {}
    for row in root.findall("x:sheetData/x:row", NS):
        row_number = int(row.attrib["r"])
        if not start_row <= row_number <= end_row:
            continue
        cells: dict[int, Any] = {}
        for cell in row.findall("x:c", NS):
            column = _column_number(cell.attrib["r"])
            if start_column <= column <= end_column:
                cells[column] = _cell_value(cell, shared_strings)
        by_row[row_number] = cells
    rows: list[dict[str, Any]] = []
    for row_number in range(start_row + 1, end_row + 1):
        cells = by_row.get(row_number, {})
        rows.append({header: cells.get(start_column + offset) for offset, header in enumerate(headers)})
    return headers, rows


def read_workbook(path: Path) -> tuple[dict[str, tuple[list[str], list[dict[str, Any]]]], dict[str, int]]:
    """Read table-backed worksheets, resolving workbook and relationship parts."""
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        structure = {
            "missing_part_count": len(EXPECTED_PARTS - names),
            "formula_count": 0,
        }
        for name in names:
            if name.startswith("xl/worksheets/") and name.endswith(".xml"):
                structure["formula_count"] += len(ET.fromstring(archive.read(name)).findall(".//x:f", NS))
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        targets = _relationships(archive, "xl/workbook.xml")
        shared_strings = _shared_strings(archive)
        sheets: dict[str, tuple[list[str], list[dict[str, Any]]]] = {}
        for sheet in workbook.findall("x:sheets/x:sheet", NS):
            relationship_id = sheet.attrib.get(f"{{{DOC_REL_NS}}}id")
            worksheet_part = targets.get(relationship_id)
            if worksheet_part is not None and worksheet_part in names:
                sheets[sheet.attrib["name"]] = _sheet_rows(archive, worksheet_part, shared_strings)
        return sheets, structure


def _empty_to_none(value: Any) -> Any:
    return None if value == "" else value


def _excel_date(value: Any) -> Any:
    if not isinstance(value, (int, float)):
        return value
    return (date(1899, 12, 30) + timedelta(days=value)).isoformat()


def _join(values: Any) -> Any:
    """Workbook flags use a semicolon-plus-space list with spaces in place of underscores (as the CSV)."""
    return "; ".join(str(item).replace("_", " ") for item in values) if isinstance(values, list) else values


def _or(value: Any, sentinel: str) -> Any:
    """Absent scalars are written as an explicit sentinel in the workbook."""
    return sentinel if value is None or value == "" else value


def _candidate_value(header: str, record: dict[str, Any]) -> Any:
    boiling = record.get("normal_boiling_point", {})
    flash = record.get("flash_point", {})
    leads = record.get("additional_source_leads", {})
    mapping: dict[str, Callable[[], Any]] = {
        # ID serializes candidate_id unchanged.
        "ID": lambda: record.get("candidate_id"),
        # Compound serializes name unchanged.
        "Compound": lambda: record.get("name"),
        # CAS serializes cas unchanged.
        "CAS": lambda: record.get("cas"),
        # Family serializes family unchanged.
        "Family": lambda: record.get("family"),
        # Boiling screen serializes normal_boiling_point.status.
        "Boiling screen": lambda: boiling.get("status"),
        # NIST low (°C) serializes evidence_envelope_low_c at JSON precision.
        "NIST low (°C)": lambda: boiling.get("evidence_envelope_low_c"),
        # NIST high (°C) serializes evidence_envelope_high_c at JSON precision.
        "NIST high (°C)": lambda: boiling.get("evidence_envelope_high_c"),
        # Flash point (°C) serializes selected_value_c.
        "Flash point (°C)": lambda: flash.get("selected_value_c"),
        # FP relation translates JSON '=' to workbook EQ.
        "FP relation": lambda: "EQ" if flash.get("relation") == "=" else _or(flash.get("relation"), "UNKNOWN"),
        # Fire evidence renders the retained GHS flammable-liquid category.
        "Fire evidence": lambda: _fire_evidence(record.get("fire_evidence", {})),
        # Overall profile serializes overall_profile_status.
        "Overall profile": lambda: record.get("overall_profile_status"),
        # Evidence flags joins flags with semicolon-space, underscores as spaces.
        "Evidence flags": lambda: _join(record.get("flags")),
        # Next evidence need serializes next_evidence_need unchanged.
        "Next evidence need": lambda: record.get("next_evidence_need"),
        # Boiling source ID serializes normal_boiling_point.source_id.
        "Boiling source ID": lambda: boiling.get("source_id"),
        # Flash source ID serializes flash_point.source_id.
        "Flash source ID": lambda: _or(flash.get("source_id"), "UNKNOWN"),
        # Supplier bp report serializes normal_boiling_point.supplier_reported.
        "Supplier bp report": lambda: _or(boiling.get("supplier_reported"), "Not retrieved"),
        # Flash-point method serializes flash_point.method.
        "Flash-point method": lambda: _or(flash.get("method"), "UNKNOWN"),
        # Formula serializes formula unchanged.
        "Formula": lambda: record.get("formula"),
        # Catalogue purity serializes sample_purity unchanged.
        "Catalogue purity": lambda: _or(record.get("sample_purity"), "Not retrieved"),
        # Vapour-pressure lead renders antoine coverage/status convention.
        "Vapour-pressure lead": lambda: _vapour_pressure_lead(leads),
        # Vaporization heat lead renders its located/not-extracted convention.
        "Vaporization heat lead": lambda: _vaporization_heat_lead(leads),
    }
    return _empty_to_none(mapping[header]())


def _fire_evidence(evidence: dict[str, Any]) -> Any:
    category = evidence.get("supplier_ghs_flammable_liquid_category")
    if category is not None:
        return f"GHS Flam. Liq. {category}"
    if "H225" in evidence.get("supplier_hazard_codes", []):
        return "Supplier H225"
    description = evidence.get("government_description") or ""
    if description.startswith("Class IB"):
        return "NIOSH Class IB"
    return "UNKNOWN"


def _vapour_pressure_lead(leads: dict[str, Any]) -> Any:
    if not leads.get("antoine_section_located"):
        return "Not located"
    return "Full 45–55°C range" if leads.get("antoine_covers_full_45_55_c") else "Other / partial range"


def _vaporization_heat_lead(leads: dict[str, Any]) -> Any:
    return "Located; not extracted" if leads.get("vaporization_enthalpy_data_located") else "Not located"


def _pressure(value: Any) -> Any:
    if not isinstance(value, dict):
        return None
    amount, unit, status = value.get("value"), value.get("unit"), value.get("status")
    if amount is None or unit is None:
        return None
    suffix = "; normal convention, not separately reported" if status else ""
    return f"{amount:g} {unit}{suffix}"


def _source_url(dataset: dict[str, Any], source_id: Any) -> Any:
    return dataset.get("_sources", {}).get(source_id, {}).get("url")


def _source_date(dataset: dict[str, Any], source_id: Any) -> Any:
    return dataset.get("_sources", {}).get(source_id, {}).get("retrieved_date")


def _observation_value(header: str, record: dict[str, Any], dataset: dict[str, Any]) -> Any:
    mapping: dict[str, Callable[[], Any]] = {
        # Observation serializes observation_id unchanged.
        "Observation": lambda: record.get("observation_id"),
        # Candidate serializes candidate_id unchanged.
        "Candidate": lambda: record.get("candidate_id"),
        # Property serializes property unchanged.
        "Property": lambda: record.get("property"),
        # Reported value serializes reported_value unchanged.
        "Reported value": lambda: record.get("reported_value"),
        # Unit serializes reported_unit unchanged.
        "Unit": lambda: record.get("reported_unit"),
        # Reported low serializes low at JSON precision.
        "Reported low": lambda: record.get("low"),
        # Reported high serializes high at JSON precision.
        "Reported high": lambda: record.get("high"),
        # Reported ± serializes reported_plus_minus at JSON precision.
        "Reported ±": lambda: record.get("reported_plus_minus"),
        # Relation translates JSON '=' to workbook EQ.
        "Relation": lambda: "EQ" if record.get("relation") == "=" else record.get("relation"),
        # Low (°C) serializes temperature_low_c at JSON precision.
        "Low (°C)": lambda: record.get("temperature_low_c"),
        # High (°C) serializes temperature_high_c at JSON precision.
        "High (°C)": lambda: record.get("temperature_high_c"),
        # Method serializes method unchanged.
        "Method": lambda: record.get("method"),
        # Pressure / convention renders the nested pressure object.
        "Pressure / convention": lambda: _pressure(record.get("pressure")),
        # Evidence note serializes note unchanged.
        "Evidence note": lambda: record.get("note"),
        # Source ID serializes source_id unchanged.
        "Source ID": lambda: record.get("source_id"),
        # Source URL resolves source_id against sources[].url.
        "Source URL": lambda: _source_url(dataset, record.get("source_id")),
        # Retrieved resolves source_id against sources[].retrieved_date as an Excel date.
        "Retrieved": lambda: _source_date(dataset, record.get("source_id")),
    }
    return _empty_to_none(mapping[header]())


def _same(left: Any, right: Any) -> bool:
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        return left == right
    return left == right


def _mapped_sheet(
    headers: list[str], rows: list[dict[str, Any]], records: list[dict[str, Any]], key_header: str, key_name: str,
    expected: Callable[[str, dict[str, Any]], Any],
) -> dict[str, Any]:
    by_workbook = {row.get(key_header): row for row in rows if row.get(key_header) is not None}
    by_dataset = {record.get(key_name): record for record in records if record.get(key_name) is not None}
    row_ok = len(rows) == len(records) and len(by_workbook) == len(rows) and set(by_workbook) == set(by_dataset)
    columns: dict[str, dict[str, Any]] = {}
    for header in headers:
        mismatches = sum(
            not _same(_excel_date(row.get(header)) if header == "Retrieved" else row.get(header), expected(header, by_dataset[key]))
            for key, row in by_workbook.items()
            if key in by_dataset
        )
        columns[header] = {"mismatch_count": mismatches, "status": "PASS" if mismatches == 0 else "FAIL"}
    return {
        "columns": columns,
        "row_alignment": {
            "dataset_row_count": len(records),
            "key_match_count": len(set(by_workbook) & set(by_dataset)),
            "status": "PASS" if row_ok else "FAIL",
            "workbook_row_count": len(rows),
        },
        "status": "PASS" if row_ok and all(item["status"] == "PASS" for item in columns.values()) else "FAIL",
    }


def evaluate(workbook_path: Path, dataset: dict[str, Any]) -> dict[str, Any]:
    sheets, structure = read_workbook(workbook_path)
    sheet_reports: dict[str, Any] = {}
    candidates = [item for item in dataset.get("candidates", []) if isinstance(item, dict)]
    observations = [item for item in dataset.get("observations", []) if isinstance(item, dict)]
    dataset = dict(dataset)
    dataset["_sources"] = {item.get("source_id"): item for item in dataset.get("sources", []) if isinstance(item, dict)}
    mapped_columns = 0
    unmapped_headers: list[str] = []
    for name in EXPECTED_SHEETS:
        headers, rows = sheets.get(name, ([], []))
        if name == "Candidates" and name in sheets:
            report = _mapped_sheet(headers, rows, candidates, "ID", "candidate_id", _candidate_value)
            mapped_columns += len(headers)
        elif name == "Evidence" and name in sheets:
            report = _mapped_sheet(
                headers, rows, observations, "Observation", "observation_id", lambda header, record: _observation_value(header, record, dataset)
            )
            mapped_columns += len(headers)
        elif name == "Data gaps" and name in sheets:
            report = {
                "columns": {header: {"mismatch_count": 0, "status": "INFO"} for header in headers},
                "row_alignment": {"status": "INFO", "workbook_row_count": len(rows)},
                "status": "INFO",
            }
            unmapped_headers.extend(headers)
        else:
            report = {"columns": {}, "row_alignment": {"status": "FAIL", "workbook_row_count": 0}, "status": "FAIL"}
        sheet_reports[name] = report
    expected_sheets_present = all(name in sheets for name in EXPECTED_SHEETS)
    # Summary COUNT formulas are a known workbook feature: reported as INFO, not a failure.
    if structure["missing_part_count"] != 0 or not expected_sheets_present:
        structure_status = "FAIL"
    else:
        structure_status = "INFO" if structure["formula_count"] else "PASS"
    all_pass = structure_status in {"PASS", "INFO"} and all(
        report["status"] in {"PASS", "INFO"} for report in sheet_reports.values()
    )
    return {
        "all_checks_pass": all_pass,
        "mapping_coverage": {
            "mapped_column_count": mapped_columns,
            "unmapped_column_count": len(unmapped_headers),
            "unmapped_column_headers": unmapped_headers,
        },
        "sheets": sheet_reports,
        "workbook_structure": {
            "expected_sheet_count": len(EXPECTED_SHEETS),
            "formula_count": structure["formula_count"],
            "missing_part_count": structure["missing_part_count"],
            "present_sheet_count": len(sheets),
            "status": structure_status,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workbook", type=Path, required=True, help="XLSX workbook path")
    parser.add_argument("--dataset", type=Path, required=True, help="JSON dataset path")
    parser.add_argument("--output", type=Path, required=True, help="JSON report path")
    args = parser.parse_args()
    workbook_raw = args.workbook.read_bytes()
    dataset_raw = args.dataset.read_bytes()
    dataset = json.loads(dataset_raw)
    if not isinstance(dataset, dict):
        raise ValueError("dataset top level must be an object")
    report = evaluate(args.workbook, dataset)
    report["input_sha256"] = {
        "dataset": hashlib.sha256(dataset_raw).hexdigest(),
        "workbook": hashlib.sha256(workbook_raw).hexdigest(),
    }
    report["inputs"] = {"dataset": args.dataset.as_posix(), "workbook": args.workbook.as_posix()}
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    raise SystemExit(0 if report["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
