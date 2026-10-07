"""Report aggregate-only CFD-3 observation interval discrepancies.

This checker never changes the source dataset.  Its committed output deliberately
contains no candidate, observation, source, name, CAS, or measurement values.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
import math
from pathlib import Path
from typing import Any


POLICY = "Report-only. Raw observations are not modified, averaged or discarded."
TOLERANCE_C = 0.01
BUCKETS = ("<=1C", "1-5C", "5-20C", ">20C")
SUPPLIER_GOVERNMENT_PROPERTIES = {"supplier_boiling_point", "government_boiling_point"}


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _empty_counts() -> dict[str, int]:
    return {
        "groups_total": 0,
        "consistent": 0,
        "non_overlapping": 0,
        "single_or_none": 0,
        "text_only_rows": 0,
        "spread_buckets": {bucket: 0 for bucket in BUCKETS},
    }


def _spread_bucket(spread: float) -> str:
    if spread <= 1:
        return "<=1C"
    if spread <= 5:
        return "1-5C"
    if spread <= 20:
        return "5-20C"
    return ">20C"


def _numeric_interval(observation: dict[str, Any], findings: list[str]) -> tuple[float, float] | None:
    low = observation.get("temperature_low_c")
    high = observation.get("temperature_high_c")
    if low is None and high is None:
        return None
    if not _is_number(low) or not _is_number(high):
        findings.append("non_numeric_celsius_field")
        return None
    low_float, high_float = float(low), float(high)
    if low_float > high_float:
        findings.append("celsius_low_greater_than_high")
        return None
    return low_float, high_float


def _boiling_family_count(
    intervals_by_group: dict[tuple[str, str], list[tuple[float, float]]],
) -> dict[str, Any]:
    candidate_ids = {candidate_id for candidate_id, _ in intervals_by_group}
    outside_candidates = 0
    numeric_supplier_government_rows = 0
    for candidate_id in candidate_ids:
        normal = intervals_by_group.get((candidate_id, "normal_boiling_point"), [])
        compared = [
            interval
            for property_name in SUPPLIER_GOVERNMENT_PROPERTIES
            for interval in intervals_by_group.get((candidate_id, property_name), [])
        ]
        numeric_supplier_government_rows += len(compared)
        if not normal or not compared:
            continue
        envelope_low = min(low for low, _ in normal)
        envelope_high = max(high for _, high in normal)
        if any(high < envelope_low or low > envelope_high for low, high in compared):
            outside_candidates += 1
    return {
        "candidates_with_supplier_government_outside_normal_envelope": outside_candidates,
        "note_key": (
            "supplier_government_numeric_values_absent"
            if numeric_supplier_government_rows == 0
            else "supplier_government_numeric_values_compared"
        ),
    }


def evaluate(dataset: dict[str, Any], dataset_path: Path) -> tuple[dict[str, Any], list[str]]:
    """Return the aggregate report and optional local-only group detail lines."""
    observations = dataset.get("observations") if isinstance(dataset, dict) else None
    if not isinstance(observations, list) or not all(isinstance(item, dict) for item in observations):
        raise ValueError("dataset observations must be a list of objects")

    findings: list[str] = []
    groups: dict[tuple[str, str], list[tuple[float, float]]] = defaultdict(list)
    text_rows_by_property: dict[str, int] = defaultdict(int)
    properties: set[str] = set()
    for observation in observations:
        candidate_id = observation.get("candidate_id")
        property_name = observation.get("property")
        if not isinstance(candidate_id, str) or not isinstance(property_name, str):
            raise ValueError("each observation must have string candidate_id and property")
        properties.add(property_name)
        interval = _numeric_interval(observation, findings)
        if interval is None:
            if observation.get("temperature_low_c") is None and observation.get("temperature_high_c") is None:
                text_rows_by_property[property_name] += 1
            groups[(candidate_id, property_name)]
        else:
            groups[(candidate_id, property_name)].append(interval)

    by_property: dict[str, dict[str, Any]] = {property_name: _empty_counts() for property_name in sorted(properties)}
    detail_lines: list[str] = []
    for (candidate_id, property_name), intervals in sorted(groups.items()):
        counts = by_property[property_name]
        counts["groups_total"] += 1
        if len(intervals) < 2:
            counts["single_or_none"] += 1
            classification = "SINGLE_OR_NONE"
        else:
            maximum_low = max(low for low, _ in intervals)
            minimum_high = min(high for _, high in intervals)
            if maximum_low <= minimum_high + TOLERANCE_C:
                counts["consistent"] += 1
                classification = "CONSISTENT"
            else:
                counts["non_overlapping"] += 1
                spread = max(high for _, high in intervals) - min(low for low, _ in intervals)
                counts["spread_buckets"][_spread_bucket(spread)] += 1
                classification = "NON_OVERLAPPING"
        detail_lines.append(f"{candidate_id}\t{property_name}\t{classification}")
    for property_name, count in text_rows_by_property.items():
        by_property[property_name]["text_only_rows"] = count

    totals = _empty_counts()
    for counts in by_property.values():
        for key in ("groups_total", "consistent", "non_overlapping", "single_or_none", "text_only_rows"):
            totals[key] += counts[key]
        for bucket in BUCKETS:
            totals["spread_buckets"][bucket] += counts["spread_buckets"][bucket]

    raw = dataset_path.read_bytes()
    status = "FAIL" if findings else ("INFO" if totals["non_overlapping"] else "PASS")
    report = {
        "boiling_point_family": _boiling_family_count(groups),
        "input_path": dataset_path.as_posix(),
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "per_property": by_property,
        "policy": POLICY,
        "status": status,
        "structural_problem_counts": dict(sorted({item: findings.count(item) for item in set(findings)}.items())),
        "totals": totals,
    }
    return report, detail_lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--detail", type=Path, help="optional local-only group-key detail output")
    args = parser.parse_args()
    raw = args.dataset.read_bytes()
    dataset = json.loads(raw.decode("utf-8"))
    report, detail_lines = evaluate(dataset, args.dataset)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    if args.detail is not None:
        args.detail.write_text("\n".join(detail_lines) + ("\n" if detail_lines else ""), encoding="utf-8", newline="\n")
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
