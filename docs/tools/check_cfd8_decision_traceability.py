"""Check that CFD-8 candidate results trace to their raw observations (report-only).

Rules (per candidate result: normal_boiling_point and flash_point):
  result_traces_to_observation - every cited observation_id exists, and a result that carries a
                                 value cites at least one observation.
  no_isomer_swap               - every cited observation belongs to the same candidate_id.
  property_matches_field       - every cited observation has the property of the result field.
  celsius_consistent           - a boiling envelope equals the min/max Celsius bounds of its cited
                                 observations; a selected flash point equals the Celsius value of
                                 one cited observation.
  missing_not_value            - a result that cites no observation carries no value (missing stays
                                 UNKNOWN, never a number).
  missing_not_zero             - no observation numeric field (including reported_plus_minus) is
                                 zero unless its reported text contains a zero.
Context (not a failure): results citing more than one observation from the same source, which must
not be read as independent corroboration; independent sources are counted per distinct source_id.
Output is aggregate-only: no candidate, source, name, CAS or measurement values.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any

POLICY = "Report-only. The dataset is not modified; counts only."
RULES = ("result_traces_to_observation", "no_isomer_swap", "property_matches_field",
         "celsius_consistent", "missing_not_value", "missing_not_zero")
FIELDS = ("normal_boiling_point", "flash_point")
NUMERIC_FIELDS = ("value", "low", "high", "reported_plus_minus", "temperature_low_c", "temperature_high_c")
TOLERANCE_C = 0.01
NUMBER_TEXT = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)")
CELSIUS_FIELDS = {"temperature_low_c", "temperature_high_c"}
REPO_ROOT = Path(__file__).resolve().parents[2]


def _num(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _close(a: Any, b: Any) -> bool:
    return _num(a) and _num(b) and abs(a - b) <= TOLERANCE_C


def result_value(field: str, result: dict[str, Any]) -> list[Any]:
    if field == "normal_boiling_point":
        return [result.get("evidence_envelope_low_c"), result.get("evidence_envelope_high_c")]
    return [result.get("selected_value_c")]


def independent_source_count(cited: list[dict[str, Any]]) -> int:
    return len({o.get("source_id") for o in cited if o.get("source_id")})


def check_result(candidate_id: Any, field: str, result: Any, observations: dict[str, dict[str, Any]]) -> dict[str, str]:
    """Return {rule: PASS|FAIL} for one candidate result (missing_not_zero is dataset-level)."""
    out = {}
    if not isinstance(result, dict):
        return {rule: "FAIL" for rule in RULES[:-1]}
    ids = result.get("observation_ids") or []
    values = result_value(field, result)
    has_value = any(v is not None for v in values)
    cited = [observations.get(i) for i in ids]
    found = [o for o in cited if o is not None]
    out["result_traces_to_observation"] = "PASS" if len(found) == len(cited) and (ids or not has_value) else "FAIL"
    out["no_isomer_swap"] = "PASS" if all(o.get("candidate_id") == candidate_id for o in found) else "FAIL"
    out["property_matches_field"] = "PASS" if all(o.get("property") == field for o in found) else "FAIL"
    out["missing_not_value"] = "PASS" if ids or not has_value else "FAIL"
    if not has_value:
        out["celsius_consistent"] = "PASS"
    elif field == "normal_boiling_point":
        lows = [o.get("temperature_low_c") for o in found if _num(o.get("temperature_low_c"))]
        highs = [o.get("temperature_high_c") for o in found if _num(o.get("temperature_high_c"))]
        ok = bool(lows and highs) and _close(values[0], min(lows)) and _close(values[1], max(highs))
        out["celsius_consistent"] = "PASS" if ok else "FAIL"
    else:
        ok = any(_close(values[0], o.get("temperature_low_c")) for o in found)
        out["celsius_consistent"] = "PASS" if ok else "FAIL"
    return out


def _reported_numbers(text: Any) -> list[float]:
    return [float(m) for m in NUMBER_TEXT.findall(text)] if isinstance(text, str) else []


def _to_celsius(value: float, unit: Any) -> float:
    if unit == "K":
        return value - 273.15
    if unit == "degF":
        return (value - 32) * 5 / 9
    return value


def zero_without_text(observation: dict[str, Any]) -> bool:
    """True if a numeric field is zero although the reported text supports no zero.

    A zero is supported when the reported text contains a zero, or (for Celsius fields) a reported
    number that converts to zero Celsius in the reported unit, e.g. a Kelvin value at the ice point.
    """
    numbers = _reported_numbers(observation.get("reported_value"))
    raw_zero = any(abs(n) <= TOLERANCE_C for n in numbers)
    unit = observation.get("reported_unit")
    celsius_zero = raw_zero or any(abs(_to_celsius(n, unit)) <= TOLERANCE_C for n in numbers)
    for key in NUMERIC_FIELDS:
        val = observation.get(key)
        if not (_num(val) and val == 0):
            continue
        supported = celsius_zero if key in CELSIUS_FIELDS else raw_zero
        if not supported:
            return True
    return False


def evaluate(dataset: dict[str, Any]) -> dict[str, Any]:
    candidates = dataset.get("candidates")
    obs_list = dataset.get("observations")
    if not isinstance(candidates, list) or not isinstance(obs_list, list):
        raise ValueError("dataset must contain candidates and observations lists")
    observations = {o.get("observation_id"): o for o in obs_list if isinstance(o, dict)}
    counts: dict[str, Counter[str]] = {rule: Counter() for rule in RULES}
    context: Counter[str] = Counter()
    for candidate in candidates:
        for field in FIELDS:
            result = candidate.get(field)
            for rule, status in check_result(candidate.get("candidate_id"), field, result, observations).items():
                counts[rule][status] += 1
            if isinstance(result, dict):
                found = [observations[i] for i in result.get("observation_ids") or [] if i in observations]
                if not found:
                    context[f"{field}_results_citing_no_observation"] += 1
                elif independent_source_count(found) < len(found):
                    context[f"{field}_results_with_repeated_source"] += 1
    for observation in obs_list:
        counts["missing_not_zero"]["FAIL" if isinstance(observation, dict) and zero_without_text(observation) else "PASS"] += 1
    rule_counts = {rule: {k: counts[rule][k] for k in ("PASS", "FAIL")} for rule in RULES}
    return {
        "candidates": len(candidates),
        "context_counts": dict(sorted(context.items())),
        "observations": len(obs_list),
        "policy": POLICY,
        "rule_counts": rule_counts,
        "status": "FAIL" if any(c["FAIL"] for c in rule_counts.values()) else "PASS",
    }


def public_path(path: Path) -> str:
    """Repository-relative path, so reruns never publish machine-specific absolute paths."""
    resolved = path.resolve()
    try:
        return resolved.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return resolved.name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.dataset.read_bytes()
    report = evaluate(json.loads(raw.decode("utf-8")))
    report["dataset_path"] = public_path(args.dataset)
    report["dataset_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
