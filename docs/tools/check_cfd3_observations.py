"""Check public CFD-3 observation records without altering their source data."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
import re
from pathlib import Path


ALLOWED_UNITS = {"K", "degC", "degF", None}
ALLOWED_RELATIONS = {"=", "<", ">", "<=", ">="}
NON_TEMPERATURE_PROPERTIES = {
    "hazard_codes",
    "hazard_classification",
    "fire_description",
}
NUMERIC_FIELDS = (
    "value",
    "low",
    "high",
    "reported_plus_minus",
    "temperature_low_c",
    "temperature_high_c",
)
TOLERANCE_C = 0.01
INEQUALITY_RE = re.compile(r"(?:<=|>=|<|>)")
NUMBER_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)")


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _finding(observation: dict, rule: str) -> dict:
    return {"observation_id": observation.get("observation_id"), "rule": rule}


def _parse_first_number(text: object) -> float | None:
    if not isinstance(text, str):
        return None
    match = NUMBER_RE.search(text.replace("−", "-"))
    return float(match.group()) if match else None


def _to_celsius(value: float, unit: str) -> float:
    if unit == "K":
        return value - 273.15
    if unit == "degF":
        return (value - 32) * 5 / 9
    return value


def _uncertainty_in_celsius(value: float, unit: str) -> float:
    return value * 5 / 9 if unit == "degF" else value


def _check_unit_conversion(observations: list[dict]) -> list[dict]:
    findings = []
    for observation in observations:
        unit = observation.get("reported_unit")
        if unit not in {"K", "degC", "degF"}:
            continue
        parsed = _parse_first_number(observation.get("reported_value"))
        if parsed is None:
            findings.append(_finding(observation, "unparseable_reported_number"))
            continue
        value = observation.get("value")
        if value is not None and (not _is_number(value) or abs(value - parsed) > TOLERANCE_C):
            findings.append(_finding(observation, "parsed_value_mismatch"))
        low, high = observation.get("low"), observation.get("high")
        low_c, high_c = observation.get("temperature_low_c"), observation.get("temperature_high_c")
        if not all(_is_number(item) for item in (low, high, low_c, high_c)):
            findings.append(_finding(observation, "missing_convertible_bounds"))
            continue
        if abs(_to_celsius(low, unit) - low_c) > TOLERANCE_C:
            findings.append(_finding(observation, "low_celsius_mismatch"))
        if abs(_to_celsius(high, unit) - high_c) > TOLERANCE_C:
            findings.append(_finding(observation, "high_celsius_mismatch"))
    return findings


def _check_unit_vocabulary(observations: list[dict]) -> list[dict]:
    findings = []
    for observation in observations:
        unit = observation.get("reported_unit")
        if unit not in ALLOWED_UNITS:
            findings.append(_finding(observation, "unknown_reported_unit"))
        if observation.get("property") in NON_TEMPERATURE_PROPERTIES:
            if unit is not None:
                findings.append(_finding(observation, "non_temperature_has_unit"))
            if any(observation.get(field) is not None for field in NUMERIC_FIELDS):
                findings.append(_finding(observation, "non_temperature_has_numeric_field"))
        elif unit is None:
            if any(observation.get(field) is not None for field in NUMERIC_FIELDS):
                findings.append(_finding(observation, "temperature_missing_unit"))
            else:
                # Source text retained without numeric parsing (e.g. unqualified supplier values); informational.
                findings.append(_finding(observation, "temperature_text_only"))
    return findings


def _check_relation_preserved(observations: list[dict]) -> list[dict]:
    findings = []
    for observation in observations:
        relation = observation.get("relation")
        reported = observation.get("reported_value")
        if relation not in ALLOWED_RELATIONS:
            findings.append(_finding(observation, "unknown_relation"))
            continue
        has_inequality = isinstance(reported, str) and INEQUALITY_RE.search(reported) is not None
        if relation == "=" and has_inequality:
            findings.append(_finding(observation, "equality_contains_inequality"))
        elif relation != "=" and not has_inequality:
            findings.append(_finding(observation, "inequality_not_preserved"))
    return findings


def _check_uncertainty_fields(observations: list[dict]) -> list[dict]:
    findings = []
    for observation in observations:
        uncertainty = observation.get("reported_plus_minus")
        if uncertainty is not None and (not _is_number(uncertainty) or uncertainty < 0):
            findings.append(_finding(observation, "invalid_reported_plus_minus"))
            continue
        values = (observation.get("low"), observation.get("value"), observation.get("high"))
        if all(_is_number(item) for item in values) and not values[0] <= values[1] <= values[2]:
            findings.append(_finding(observation, "value_outside_bounds"))
        if uncertainty is None:
            continue
        unit = observation.get("reported_unit")
        value = observation.get("value")
        low_c, high_c = observation.get("temperature_low_c"), observation.get("temperature_high_c")
        if unit not in {"K", "degC", "degF"} or not all(_is_number(item) for item in (value, low_c, high_c)):
            findings.append(_finding(observation, "uncertainty_missing_convertible_bounds"))
            continue
        center_c = _to_celsius(value, unit)
        delta_c = _uncertainty_in_celsius(uncertainty, unit)
        if abs(low_c - (center_c - delta_c)) > TOLERANCE_C:
            findings.append(_finding(observation, "uncertainty_low_span_mismatch"))
        if abs(high_c - (center_c + delta_c)) > TOLERANCE_C:
            findings.append(_finding(observation, "uncertainty_high_span_mismatch"))
    return findings


def _check_missing_states(observations: list[dict]) -> list[dict]:
    findings = []
    for observation in observations:
        reported = observation.get("reported_value")
        if not isinstance(reported, str) or not reported.strip():
            findings.append(_finding(observation, "empty_reported_value"))
        invalid_numeric = False
        for field in NUMERIC_FIELDS:
            value = observation.get(field)
            if value is not None and not _is_number(value):
                findings.append(_finding(observation, "invalid_numeric_field"))
                invalid_numeric = True
                break
        if invalid_numeric:
            continue
        value, low, high = (observation.get(field) for field in ("value", "low", "high"))
        low_c, high_c = (observation.get(field) for field in ("temperature_low_c", "temperature_high_c"))
        numeric_state = (value, low, high, low_c, high_c)
        if all(item is None for item in numeric_state):
            continue
        # The retained method supports intervals without a declared central value.
        if low is None or high is None or low_c is None or high_c is None:
            findings.append(_finding(observation, "incoherent_numeric_state"))
    return findings


def _check_evidence_type(observations: list[dict]) -> list[dict]:
    return [
        _finding(observation, "unexpected_evidence_type")
        for observation in observations
        if observation.get("evidence_type") != "SOURCE_REPORTED_NOT_PROJECT_MEASUREMENT"
    ]


CHECKS = {
    "unit_conversion": _check_unit_conversion,
    "unit_vocabulary": _check_unit_vocabulary,
    "relation_preserved": _check_relation_preserved,
    "uncertainty_fields": _check_uncertainty_fields,
    "missing_states": _check_missing_states,
    "evidence_type": _check_evidence_type,
}


INFO_RULES = frozenset({"temperature_text_only"})


def evaluate(dataset: dict, dataset_path: Path) -> dict:
    observations = dataset.get("observations") if isinstance(dataset, dict) else None
    if not isinstance(observations, list):
        raise ValueError("dataset observations must be a list")
    if not all(isinstance(observation, dict) for observation in observations):
        raise ValueError("each observation must be an object")
    checks = {}
    for name, checker in CHECKS.items():
        findings = checker(observations)
        checks[name] = {
            "status": ("FAIL" if any(f["rule"] not in INFO_RULES for f in findings)
                       else "INFO" if findings else "PASS"),
            "finding_count": len(findings),
            "rule_counts": dict(sorted(Counter(f["rule"] for f in findings).items())),
        }
    raw = dataset_path.read_bytes()
    return {
        "dataset_path": dataset_path.as_posix(),
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "counts": {
            "observations": len(observations),
            "by_check": {name: check["finding_count"] for name, check in checks.items()},
        },
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.dataset.read_bytes()
    dataset = json.loads(raw.decode("utf-8"))
    report = evaluate(dataset, args.dataset)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 1 if any(check["status"] == "FAIL" for check in report["checks"].values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
