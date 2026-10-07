"""Synthetic fixtures for the public CFD-3 workbook checker."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


CHECKER_PATH = Path(__file__).with_name("check_cfd3_workbook.py")
SPEC = importlib.util.spec_from_file_location("check_cfd3_workbook", CHECKER_PATH)
assert SPEC is not None and SPEC.loader is not None
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
DOC_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL = "http://schemas.openxmlformats.org/package/2006/relationships"


def _cell(column: int, row: int, value: object, shared_index: int | None = None) -> str:
    reference = f"{checker._column_letters(column)}{row}"
    if value is None:
        return f'<c r="{reference}"/>'
    if shared_index is not None:
        return f'<c r="{reference}" t="s"><v>{shared_index}</v></c>'
    if isinstance(value, bool):
        return f'<c r="{reference}" t="b"><v>{int(value)}</v></c>'
    if isinstance(value, (int, float)):
        return f'<c r="{reference}" t="n"><v>{value}</v></c>'
    return f'<c r="{reference}" t="inlineStr"><is><t>{escape(str(value))}</t></is></c>'


def _worksheet(headers: list[str], rows: list[list[object]], table_number: int) -> str:
    body = []
    for row_number, values in enumerate([headers, *rows], 1):
        cells = []
        for column, value in enumerate(values):
            # The candidate Compound cell exercises shared-string rich-text parsing.
            shared = 0 if table_number == 1 and row_number == 2 and column == 1 else None
            cells.append(_cell(column, row_number, value, shared))
        body.append(f'<row r="{row_number}">{"".join(cells)}</row>')
    return (
        f'<worksheet xmlns="{MAIN}" xmlns:r="{DOC_REL}"><sheetData>{"".join(body)}</sheetData>'
        f'<tableParts count="1"><tablePart r:id="table{table_number}"/></tableParts></worksheet>'
    )


def _table(headers: list[str], row_count: int, table_number: int) -> str:
    end = checker._column_letters(len(headers) - 1) + str(row_count + 1)
    columns = "".join(
        f'<tableColumn id="{index}" name="{escape(header)}"/>' for index, header in enumerate(headers, 1)
    )
    return (
        f'<table xmlns="{MAIN}" id="{table_number}" name="Table{table_number}" displayName="Table{table_number}" ref="A1:{end}">'
        f'<tableColumns count="{len(headers)}">{columns}</tableColumns></table>'
    )


def _write_workbook(
    path: Path, candidate_rows: list[list[object]], include_evidence: bool = True, candidate_headers: list[str] | None = None,
) -> None:
    sheets = [("Candidates", candidate_headers or ["ID", "Compound"], candidate_rows)]
    if include_evidence:
        sheets.append(("Evidence", ["Observation", "Candidate"], [["O001", "CF001"]]))
    sheets.append(("Data gaps", ["Property / question"], [["invented gap"]]))
    workbook_sheets = "".join(
        f'<sheet name="{name}" sheetId="{index}" r:id="sheet{index}"/>' for index, (name, _, _) in enumerate(sheets, 1)
    )
    relationships = "".join(
        f'<Relationship xmlns="{PACKAGE_REL}" Id="sheet{index}" Type="{DOC_REL}/worksheet" Target="worksheets/sheet{index}.xml"/>'
        for index in range(1, len(sheets) + 1)
    )
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("xl/workbook.xml", f'<workbook xmlns="{MAIN}" xmlns:r="{DOC_REL}"><sheets>{workbook_sheets}</sheets></workbook>')
        archive.writestr("xl/_rels/workbook.xml.rels", f'<Relationships xmlns="{PACKAGE_REL}">{relationships}</Relationships>')
        archive.writestr("xl/sharedStrings.xml", f'<sst xmlns="{MAIN}"><si><r><t>Alpha</t></r><r><t> Beta</t></r></si></sst>')
        for index, (_, headers, rows) in enumerate(sheets, 1):
            archive.writestr(f"xl/worksheets/sheet{index}.xml", _worksheet(headers, rows, index))
            archive.writestr(
                f"xl/worksheets/_rels/sheet{index}.xml.rels",
                f'<Relationships xmlns="{PACKAGE_REL}"><Relationship Id="table{index}" Type="{DOC_REL}/table" Target="../tables/table{index}.xml"/></Relationships>',
            )
            archive.writestr(f"xl/tables/table{index}.xml", _table(headers, len(rows), index))


def _dataset() -> dict[str, object]:
    return {
        "candidates": [{"candidate_id": "CF001", "name": "Alpha Beta"}],
        "observations": [{"observation_id": "O001", "candidate_id": "CF001"}],
        "sources": [],
    }


class WorkbookCheckerTests(unittest.TestCase):
    def evaluate(
        self, rows: list[list[object]], include_evidence: bool = True, candidate_headers: list[str] | None = None,
    ) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as directory:
            workbook = Path(directory) / "fixture.xlsx"
            _write_workbook(workbook, rows, include_evidence, candidate_headers)
            return checker.evaluate(workbook, _dataset())

    def test_pass_case_and_rich_text_shared_string(self) -> None:
        report = self.evaluate([["CF001", "ignored inline text"]])
        self.assertTrue(report["all_checks_pass"])
        self.assertEqual(report["sheets"]["Candidates"]["columns"]["Compound"]["status"], "PASS")

    def test_numeric_mismatch_is_reported(self) -> None:
        dataset = _dataset()
        dataset["candidates"] = [{"candidate_id": "CF001", "name": "Alpha Beta", "normal_boiling_point": {"evidence_envelope_low_c": 12.5}}]
        with tempfile.TemporaryDirectory() as directory:
            workbook = Path(directory) / "fixture.xlsx"
            _write_workbook(workbook, [["CF001", "ignored", 12.4]], candidate_headers=["ID", "Compound", "NIST low (°C)"])
            report = checker.evaluate(workbook, dataset)
        self.assertFalse(report["all_checks_pass"])
        self.assertEqual(report["sheets"]["Candidates"]["columns"]["NIST low (°C)"]["status"], "FAIL")

    def test_text_mismatch_is_reported(self) -> None:
        dataset = _dataset()
        dataset["candidates"] = [{"candidate_id": "CF001", "name": "Alpha Beta", "cas": "invented-cas"}]
        with tempfile.TemporaryDirectory() as directory:
            workbook = Path(directory) / "fixture.xlsx"
            _write_workbook(workbook, [["CF001", "ignored", "different-cas"]], candidate_headers=["ID", "Compound", "CAS"])
            report = checker.evaluate(workbook, dataset)
        self.assertFalse(report["all_checks_pass"])
        self.assertEqual(report["sheets"]["Candidates"]["columns"]["CAS"]["status"], "FAIL")

    def test_missing_sheet_fails_structure(self) -> None:
        report = self.evaluate([["CF001", "ignored"]], include_evidence=False)
        self.assertFalse(report["all_checks_pass"])
        self.assertEqual(report["sheets"]["Evidence"]["status"], "FAIL")

    def test_extra_row_fails_alignment(self) -> None:
        report = self.evaluate([["CF001", "ignored"], ["CF002", "another"]])
        self.assertEqual(report["sheets"]["Candidates"]["row_alignment"]["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
