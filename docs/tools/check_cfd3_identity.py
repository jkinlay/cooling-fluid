"""Reconcile identifiers in the tracked CFD-3 feasibility dataset.

This checker is deliberately read-only except for the explicit ``--output``
report path.  It validates identifiers and cross-file identity consistency; it
does not assess chemical properties or source content.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any


CAS_PATTERN = re.compile(r"^\d{2,7}-\d{2}-\d$")
EXPECTED_CANDIDATE_IDS = [f"CF{number:03d}" for number in range(1, 33)]


def _check(status: str, findings: list[str]) -> dict[str, Any]:
    return {"findings": findings, "status": status}


def _cas_check_digit_is_valid(cas: str) -> bool:
    """Return whether a format-valid CAS Registry Number has a valid digit."""
    digits = cas.replace("-", "")
    total = sum(int(digit) * multiplier for multiplier, digit in enumerate(reversed(digits[:-1]), 1))
    return total % 10 == int(digits[-1])


def _source_ids_in(value: Any) -> set[str]:
    """Find nested fields named source_id without interpreting their content."""
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "source_id" and isinstance(item, str):
                found.add(item)
            found.update(_source_ids_in(item))
    elif isinstance(value, list):
        for item in value:
            found.update(_source_ids_in(item))
    return found


def _normalise_header(name: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", (name or "").lower())


def _csv_columns(fieldnames: list[str] | None) -> tuple[str | None, str | None]:
    names = fieldnames or []
    normalized = {_normalise_header(name): name for name in names}
    candidate_column = normalized.get("candidateid") or normalized.get("id")
    cas_column = normalized.get("cas") or normalized.get("casnumber")
    return candidate_column, cas_column


def evaluate(dataset: dict[str, Any], csv_path: Path) -> dict[str, Any]:
    """Evaluate all CFD-3 identity checks and return a deterministic report body."""
    candidates = dataset.get("candidates", [])
    observations = dataset.get("observations", [])
    sources = dataset.get("sources", [])
    summary = dataset.get("summary", {})
    checks: dict[str, dict[str, Any]] = {}

    candidate_ids = [item.get("candidate_id") if isinstance(item, dict) else None for item in candidates]
    candidate_findings: list[str] = []
    duplicate_candidate_ids = sorted({item for item in candidate_ids if item is not None and candidate_ids.count(item) > 1})
    if duplicate_candidate_ids:
        candidate_findings.append("duplicate candidate_id values: " + ", ".join(duplicate_candidate_ids))
    if candidate_ids != EXPECTED_CANDIDATE_IDS:
        missing = sorted(set(EXPECTED_CANDIDATE_IDS) - set(candidate_ids))
        unexpected = sorted({str(item) for item in candidate_ids if item not in EXPECTED_CANDIDATE_IDS})
        candidate_findings.append(
            "candidate IDs are not exactly contiguous CF001..CF032"
            + ("; missing: " + ", ".join(missing) if missing else "")
            + ("; unexpected: " + ", ".join(unexpected) if unexpected else "")
        )
    checks["candidate_ids"] = _check("PASS" if not candidate_findings else "FAIL", candidate_findings)

    cas_values = [item.get("cas") if isinstance(item, dict) else None for item in candidates]
    cas_findings: list[str] = []
    invalid_format = [str(value) for value in cas_values if not isinstance(value, str) or not CAS_PATTERN.fullmatch(value)]
    invalid_digit = [value for value in cas_values if isinstance(value, str) and CAS_PATTERN.fullmatch(value) and not _cas_check_digit_is_valid(value)]
    duplicate_cas = sorted({value for value in cas_values if value is not None and cas_values.count(value) > 1})
    if invalid_format:
        cas_findings.append("invalid CAS format: " + ", ".join(invalid_format))
    if invalid_digit:
        cas_findings.append("invalid CAS check digit: " + ", ".join(invalid_digit))
    if duplicate_cas:
        cas_findings.append("duplicate CAS values: " + ", ".join(duplicate_cas))
    checks["cas_format_and_check_digit"] = _check("PASS" if not cas_findings else "FAIL", cas_findings)

    source_ids = [item.get("source_id") if isinstance(item, dict) else None for item in sources]
    candidate_id_set = {item for item in candidate_ids if isinstance(item, str)}
    source_id_set = {item for item in source_ids if isinstance(item, str)}
    observation_ids = [item.get("observation_id") if isinstance(item, dict) else None for item in observations]
    observation_findings: list[str] = []
    duplicate_observations = sorted({item for item in observation_ids if item is not None and observation_ids.count(item) > 1})
    if duplicate_observations:
        observation_findings.append("duplicate observation_id values: " + ", ".join(duplicate_observations))
    for index, observation in enumerate(observations):
        prefix = f"observation[{index}]"
        if not isinstance(observation, dict):
            observation_findings.append(prefix + " is not an object")
            continue
        if not isinstance(observation.get("observation_id"), str) or not observation["observation_id"]:
            observation_findings.append(prefix + " has no observation_id")
        if observation.get("candidate_id") not in candidate_id_set:
            observation_findings.append(prefix + " has dangling candidate_id: " + repr(observation.get("candidate_id")))
        if observation.get("source_id") not in source_id_set:
            observation_findings.append(prefix + " has dangling source_id: " + repr(observation.get("source_id")))
    checks["observation_refs"] = _check("PASS" if not observation_findings else "FAIL", observation_findings)

    source_findings: list[str] = []
    duplicate_sources = sorted({item for item in source_ids if item is not None and source_ids.count(item) > 1})
    if duplicate_sources:
        source_findings.append("duplicate source_id values: " + ", ".join(duplicate_sources))
    if any(not isinstance(item, str) or not item for item in source_ids):
        source_findings.append("one or more sources have no source_id")
    referenced_sources = _source_ids_in(candidates) | {
        item.get("source_id") for item in observations if isinstance(item, dict) and isinstance(item.get("source_id"), str)
    }
    for source_id in sorted(source_id_set - referenced_sources):
        source_findings.append("INFO unreferenced source_id: " + source_id)
    checks["source_ids"] = _check(
        "FAIL" if duplicate_sources or any(not isinstance(item, str) or not item for item in source_ids) else "PASS",
        source_findings,
    )

    summary_findings: list[str] = []
    if not isinstance(summary, dict):
        summary_findings.append("summary is not an object")
    else:
        expected_counts = {
            "records": len(candidates),
            "property_observations": len(observations),
            "source_records": len(sources),
        }
        for key, expected in expected_counts.items():
            if key in summary and summary[key] != expected:
                summary_findings.append(f"summary.{key} is {summary[key]!r}, expected {expected}")
    checks["summary_counts"] = _check("PASS" if not summary_findings else "FAIL", summary_findings)

    csv_findings: list[str] = []
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        candidate_column, cas_column = _csv_columns(reader.fieldnames)
        rows = list(reader)
    if candidate_column is None or cas_column is None:
        csv_findings.append(
            "CSV header must contain candidate ID (candidate_id or ID) and CAS (cas or cas_number) columns"
        )
    else:
        csv_ids = [row.get(candidate_column) for row in rows]
        expected_by_id = {
            item.get("candidate_id"): item.get("cas") for item in candidates if isinstance(item, dict)
        }
        if len(rows) != len(candidates):
            csv_findings.append(f"CSV has {len(rows)} rows, expected {len(candidates)}")
        duplicate_csv_ids = sorted({item for item in csv_ids if item and csv_ids.count(item) > 1})
        if duplicate_csv_ids:
            csv_findings.append("duplicate CSV candidate IDs: " + ", ".join(duplicate_csv_ids))
        missing_csv_ids = sorted(set(expected_by_id) - set(csv_ids))
        unexpected_csv_ids = sorted({item for item in csv_ids if item not in expected_by_id})
        if missing_csv_ids:
            csv_findings.append("missing CSV candidate IDs: " + ", ".join(missing_csv_ids))
        if unexpected_csv_ids:
            csv_findings.append("unexpected CSV candidate IDs: " + ", ".join(str(item) for item in unexpected_csv_ids))
        for row in rows:
            candidate_id = row.get(candidate_column)
            if candidate_id in expected_by_id and row.get(cas_column) != expected_by_id[candidate_id]:
                csv_findings.append(
                    f"CSV CAS mismatch for {candidate_id}: {row.get(cas_column)!r}, expected {expected_by_id[candidate_id]!r}"
                )
    checks["csv_identity_match"] = _check("PASS" if not csv_findings else "FAIL", csv_findings)

    return {
        "all_checks_pass": all(check["status"] == "PASS" for check in checks.values()),
        "checks": checks,
        "counts": {"candidates": len(candidates), "observations": len(observations), "sources": len(sources)},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True, help="JSON dataset path")
    parser.add_argument("--csv", type=Path, required=True, help="CSV dataset path")
    parser.add_argument("--output", type=Path, required=True, help="JSON report path")
    args = parser.parse_args()
    dataset_raw = args.dataset.read_bytes()
    csv_raw = args.csv.read_bytes()
    dataset = json.loads(dataset_raw)
    if not isinstance(dataset, dict):
        raise ValueError("dataset top level must be an object")
    report = evaluate(dataset, args.csv)
    report["input_sha256"] = {
        "csv": hashlib.sha256(csv_raw).hexdigest(),
        "dataset": hashlib.sha256(dataset_raw).hexdigest(),
    }
    report["inputs"] = {"csv": args.csv.as_posix(), "dataset": args.dataset.as_posix()}
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    raise SystemExit(0 if report["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
