"""Rerun the inclusive 45-55 C normal-boiling screen from published evidence envelopes (CFD-5).

Report-only and aggregate-only: the committed output contains no candidate, observation,
source, name, CAS or measurement values.  The dataset is never modified.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
from typing import Any

LOWER_C = 45.0
UPPER_C = 55.0
TOLERANCE_C = 0.01
STATUSES = ("PASS", "FAIL", "UNKNOWN")
POLICY = (
    "Inclusive 45-55 C screen recomputed from the published evidence envelope: wholly inside is PASS, "
    "wholly outside is FAIL, crossing a bound or missing is UNKNOWN. Report-only; the dataset is not modified."
)


def _num(value: object) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
        return float(value)
    return None


def screen(low: float | None, high: float | None) -> str:
    """Inclusive screen: wholly inside is PASS, wholly outside is FAIL, anything else UNKNOWN."""
    if low is None or high is None or low > high:
        return "UNKNOWN"
    if low >= LOWER_C and high <= UPPER_C:
        return "PASS"
    if high < LOWER_C or low > UPPER_C:
        return "FAIL"
    return "UNKNOWN"


def evaluate(dataset: dict[str, Any]) -> dict[str, Any]:
    candidates = dataset.get("candidates")
    observations = dataset.get("observations")
    if not isinstance(candidates, list) or not isinstance(observations, list):
        raise ValueError("dataset must contain candidates and observations lists")
    by_id: dict[object, list[dict[str, Any]]] = {}
    for row in observations:
        by_id.setdefault(row.get("observation_id"), []).append(row)

    published: Counter[str] = Counter()
    recomputed: Counter[str] = Counter()
    transitions: Counter[str] = Counter()
    problems: Counter[str] = Counter()
    boundary_touching = 0
    for candidate in candidates:
        boiling = candidate.get("normal_boiling_point") or {}
        status = boiling.get("status")
        if status not in STATUSES:
            problems["published_status_not_recognised"] += 1
        published[str(status)] += 1
        low = _num(boiling.get("evidence_envelope_low_c"))
        high = _num(boiling.get("evidence_envelope_high_c"))
        cited = []
        for oid in boiling.get("observation_ids") or []:
            rows = by_id.get(oid, [])
            if len(rows) == 1:
                cited.append(rows[0])
            else:
                problems["observation_reference_missing_or_ambiguous"] += 1
        lows = [_num(r.get("temperature_low_c")) for r in cited]
        highs = [_num(r.get("temperature_high_c")) for r in cited]
        if cited and None not in lows and None not in highs and low is not None and high is not None:
            if abs(min(lows) - low) > TOLERANCE_C or abs(max(highs) - high) > TOLERANCE_C:
                problems["envelope_not_reproduced_from_cited_observations"] += 1
        else:
            problems["envelope_not_computable"] += 1
        result = screen(low, high)
        recomputed[result] += 1
        transitions[f"{status}->{result}"] += 1
        if result != status:
            problems["status_not_reproduced"] += 1
        if low is not None and high is not None and any(
            low - TOLERANCE_C <= bound <= high + TOLERANCE_C for bound in (LOWER_C, UPPER_C)
        ):
            boundary_touching += 1

    summary = dataset.get("summary") or {}
    for status, key in (("PASS", "boiling_pass"), ("FAIL", "boiling_fail"), ("UNKNOWN", "boiling_unknown")):
        if summary.get(key) != recomputed[status]:
            problems["summary_count_mismatch"] += 1
    return {
        "candidates": len(candidates),
        "envelopes_touching_or_crossing_a_bound": boundary_touching,
        "policy": POLICY,
        "problem_counts": dict(sorted(problems.items())),
        "published_status_counts": {s: published[s] for s in STATUSES},
        "recomputed_status_counts": {s: recomputed[s] for s in STATUSES},
        "screen_bounds_c": {"lower_inclusive": LOWER_C, "upper_inclusive": UPPER_C},
        "status": "FAIL" if problems else "PASS",
        "status_transitions": dict(sorted(transitions.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.dataset.read_bytes()
    report = evaluate(json.loads(raw.decode("utf-8")))
    report["input_path"] = args.dataset.as_posix()
    report["input_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
