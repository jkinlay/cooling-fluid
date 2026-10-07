"""Rerun every committed CFD evidence checker and confirm each committed result reproduces (report-only).

Each job runs one checker from the repository root on the published inputs, writes to a temporary
directory, and compares the fresh output with the committed result as parsed JSON, so line-ending
or whitespace differences between platforms do not count. Committed files are never modified.

The summary is counts-only: job counts, reproduced/differs/error counts, the interpreter version as
integers, and SHA-256 digests of the committed results and inputs under local_evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any

POLICY = "Report-only. Committed inputs and results are not modified; counts and digests only."
REPO_ROOT = Path(__file__).resolve().parents[2]
F = "docs/feasibility"
D = f"{F}/feasibility_table.json"
R = f"{F}/acceptability_register.json"
JOBS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("cfd3_boundary_register_check_results.json", "check_cfd3_boundary_register.py",
     ("--register", f"{F}/search_boundary_register.json", "--root", ".")),
    ("cfd3_csv_json_check_results.json", "check_cfd3_csv_json.py", ("--dataset", D, "--csv", f"{F}/feasibility_table.csv")),
    ("cfd3_discrepancy_log.json", "check_cfd3_discrepancies.py", ("--dataset", D)),
    ("cfd3_identity_check_results.json", "check_cfd3_identity.py", ("--dataset", D, "--csv", f"{F}/feasibility_table.csv")),
    ("cfd3_observation_check_results.json", "check_cfd3_observations.py", ("--dataset", D)),
    ("cfd3_source_check_results.json", "check_cfd3_sources.py", ("--dataset", D)),
    ("cfd3_workbook_check_results.json", "check_cfd3_workbook.py",
     ("--workbook", f"{F}/Cooling_Fluid_Candidate_Table.xlsx", "--dataset", D)),
    ("cfd5_boiling_screen_check_results.json", "check_cfd5_boiling_screen.py", ("--dataset", D)),
    ("cfd6_fire_evidence_rules_check_results.json", "check_cfd6_fire_evidence_rules.py", ("--dataset", D, "--register", R)),
    ("cfd7_application_screen_check_results.json", "check_cfd7_application_screen.py",
     ("--rules", f"{F}/cfd7_application_screen_rules.json", "--register", R)),
    ("cfd7_qualification_status_check_results.json", "check_cfd7_qualification_status.py", ("--dataset", D)),
    ("cfd8_decision_traceability_check_results.json", "check_cfd8_decision_traceability.py", ("--dataset", D)),
    ("study_control_case_results.json", "check_m0_control.py",
     ("--control", f"{F}/study_control.json", "--cases", f"{F}/study_control_cases.json")),
)


def same_json(committed: bytes, fresh: bytes) -> bool:
    """Parsed-JSON equality; line endings and formatting do not matter."""
    try:
        return json.loads(committed.decode("utf-8")) == json.loads(fresh.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return False


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _key(path: str) -> str:
    return Path(path).name.replace(".", "_").replace("-", "_") + "_sha256"


def run_jobs(root: Path, jobs=JOBS) -> dict[str, Any]:
    counts = {"reproduced": 0, "differs": 0, "error": 0}
    evidence: dict[str, str] = {}
    inputs: set[str] = set()
    with tempfile.TemporaryDirectory() as tmp:
        for result_name, script, args in jobs:
            committed_path = root / F / result_name
            fresh_path = Path(tmp) / result_name
            for i, arg in enumerate(args):
                if i and args[i - 1] in {"--dataset", "--csv", "--register", "--workbook", "--rules", "--control", "--cases"}:
                    inputs.add(arg)
            proc = subprocess.run([sys.executable, "-B", str(root / "docs" / "tools" / script), *args,
                                   "--output", str(fresh_path)], cwd=root, capture_output=True)
            if not committed_path.is_file() or not fresh_path.is_file():
                counts["error"] += 1
                continue
            committed = committed_path.read_bytes()
            evidence[_key(result_name)] = _sha(committed)
            counts["reproduced" if same_json(committed, fresh_path.read_bytes()) else "differs"] += 1
            _ = proc.returncode  # a checker may exit non-zero on a FAIL report; reproduction is what counts
    for path in sorted(inputs):
        evidence[_key(path)] = _sha((root / path).read_bytes())
    return {"counts": counts, "local_evidence": dict(sorted(evidence.items()))}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run = run_jobs(REPO_ROOT)
    v = sys.version_info
    report = {
        "jobs": len(JOBS),
        "local_evidence": run["local_evidence"],
        "policy": POLICY,
        "python_version": {"major": v.major, "minor": v.minor, "micro": v.micro},
        "result_counts": run["counts"],
        "status": "PASS" if run["counts"]["reproduced"] == len(JOBS) else "FAIL",
    }
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
