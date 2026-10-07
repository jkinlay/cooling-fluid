"""Check CFD-7 qualification-status acceptance rules against the published dataset (report-only).

Rules:
  unassessed_not_pass            - no other_qualification field is PASS while the dataset carries no
                                   assessment evidence for it (every field must be NOT_ASSESSED,
                                   UNKNOWN or FAIL).
  electrical_properties_distinct - resistivity and dielectric breakdown are separate fields, and no
                                   single field merges resistivity, permittivity or breakdown.
  no_qualified_candidate         - no candidate profile is PASS while any qualification field is
                                   unassessed, and the dataset summary reports zero qualified coolants.
Output is aggregate-only: no candidate, source, name, CAS or measurement values.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from typing import Any

POLICY = "Report-only. The dataset is not modified; counts only."
RULES = ("unassessed_not_pass", "electrical_properties_distinct", "no_qualified_candidate")
ALLOWED_UNASSESSED = {"NOT_ASSESSED", "UNKNOWN", "FAIL"}
ELECTRICAL_TERMS = ("resistivity", "permittivity", "dielectric_constant", "breakdown")


def _electrical_terms(key: str) -> set[str]:
    lowered = key.lower()
    return {term for term in ELECTRICAL_TERMS if term in lowered}


def evaluate(dataset: dict[str, Any]) -> dict[str, Any]:
    candidates = dataset.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError("dataset must contain a candidates list")
    results: dict[str, Counter[str]] = {rule: Counter() for rule in RULES}
    field_status: Counter[str] = Counter()
    context: Counter[str] = Counter()
    for candidate in candidates:
        qualification = candidate.get("other_qualification")
        if not isinstance(qualification, dict) or not qualification:
            for rule in RULES:
                results[rule]["FAIL"] += 1
            continue
        for value in qualification.values():
            field_status[str(value)] += 1
        unassessed = any(value != "PASS" for value in qualification.values())
        ok = all(value in ALLOWED_UNASSESSED for value in qualification.values())
        results["unassessed_not_pass"]["PASS" if ok else "FAIL"] += 1

        terms_per_key = [_electrical_terms(key) for key in qualification]
        merged = any(len(terms) > 1 for terms in terms_per_key)
        has_resistivity = any("resistivity" in terms for terms in terms_per_key)
        has_breakdown = any("breakdown" in terms for terms in terms_per_key)
        has_permittivity = any(terms & {"permittivity", "dielectric_constant"} for terms in terms_per_key)
        if not has_permittivity:
            context["permittivity_field_absent"] += 1
        distinct = has_resistivity and has_breakdown and not merged
        results["electrical_properties_distinct"]["PASS" if distinct else "FAIL"] += 1

        profile = candidate.get("overall_profile_status")
        context[f"overall_profile_status_{profile}"] += 1
        bad = profile == "PASS" and unassessed
        results["no_qualified_candidate"]["FAIL" if bad else "PASS"] += 1

    summary = dataset.get("summary") or {}
    summary_ok = summary.get("qualified_coolants") == 0
    rule_counts = {rule: {key: results[rule][key] for key in ("PASS", "FAIL")} for rule in RULES}
    failed = any(counts["FAIL"] for counts in rule_counts.values()) or not summary_ok
    return {
        "candidates": len(candidates),
        "context_counts": dict(sorted(context.items())),
        "qualification_field_status_counts": dict(sorted(field_status.items())),
        "policy": POLICY,
        "rule_counts": rule_counts,
        "status": "FAIL" if failed else "PASS",
        "summary_reports_zero_qualified": summary_ok,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.dataset.read_bytes()
    report = evaluate(json.loads(raw.decode("utf-8")))
    report["dataset_path"] = args.dataset.as_posix()
    report["dataset_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
