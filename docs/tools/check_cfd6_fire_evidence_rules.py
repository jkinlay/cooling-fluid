"""Check CFD-6 fire-evidence acceptance rules against the published dataset (report-only).

Rules:
  missing_flash_stays_unknown  - a null selected flash value carries sign UNKNOWN and no relation,
                                 and sign UNKNOWN only occurs with a null value.
  no_inferred_ghs_category     - a supplier GHS flammable-liquid category is present only when the
                                 supplier classification text states that same category.
  fire_acceptance_needs_adopted_requirement
                               - application fire acceptance is UNKNOWN unless the acceptability
                                 register holds an adopted fire_behavior hard rule.
Output is aggregate-only: no candidate, source, name, CAS or measurement values.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import re
from pathlib import Path
from typing import Any

POLICY = "Report-only. The dataset and register are not modified; counts only."
RULES = ("missing_flash_stays_unknown", "no_inferred_ghs_category", "fire_acceptance_needs_adopted_requirement")
_CATEGORY = re.compile(r"Flam\. Liq\. (\d)")


def adopted_fire_requirement(register: dict[str, Any]) -> bool:
    for profile in register.get("profiles") or []:
        for constraint in profile.get("constraints") or []:
            if constraint.get("domain") == "fire_behavior" and constraint.get("hard_rule_adopted") is True:
                return True
    return False


def evaluate(dataset: dict[str, Any], register: dict[str, Any]) -> dict[str, Any]:
    candidates = dataset.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError("dataset must contain a candidates list")
    adopted = adopted_fire_requirement(register)
    results: dict[str, Counter[str]] = {rule: Counter() for rule in RULES}
    context: Counter[str] = Counter()
    for candidate in candidates:
        flash = candidate.get("flash_point") or {}
        fire = candidate.get("fire_evidence") or {}

        value_missing = flash.get("selected_value_c") is None
        sign_unknown = flash.get("sign_description") == "UNKNOWN"
        if value_missing:
            context["flash_value_missing"] += 1
            ok = sign_unknown and flash.get("relation") is None
            results["missing_flash_stays_unknown"]["PASS" if ok else "FAIL"] += 1
        elif sign_unknown:
            results["missing_flash_stays_unknown"]["FAIL"] += 1
        else:
            results["missing_flash_stays_unknown"]["NOT_APPLICABLE"] += 1

        category = fire.get("supplier_ghs_flammable_liquid_category")
        stated = _CATEGORY.findall(fire.get("supplier_classification") or "")
        if category is None:
            context["ghs_category_absent"] += 1
            if "H225" in (fire.get("supplier_hazard_codes") or []):
                context["ghs_category_absent_with_hazard_code_not_imputed"] += 1
            results["no_inferred_ghs_category"]["NOT_APPLICABLE"] += 1
        else:
            context["ghs_category_present"] += 1
            ok = stated == [str(category)]
            results["no_inferred_ghs_category"]["PASS" if ok else "FAIL"] += 1

        status = fire.get("application_acceptance_status")
        if adopted:
            results["fire_acceptance_needs_adopted_requirement"]["NOT_APPLICABLE"] += 1
        else:
            results["fire_acceptance_needs_adopted_requirement"]["PASS" if status == "UNKNOWN" else "FAIL"] += 1

    rule_counts = {
        rule: {key: results[rule][key] for key in ("PASS", "FAIL", "NOT_APPLICABLE")} for rule in RULES
    }
    failed = any(counts["FAIL"] for counts in rule_counts.values())
    return {
        "adopted_fire_requirement_present": adopted,
        "candidates": len(candidates),
        "context_counts": dict(sorted(context.items())),
        "policy": POLICY,
        "rule_counts": rule_counts,
        "status": "FAIL" if failed else "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--register", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw_dataset = args.dataset.read_bytes()
    raw_register = args.register.read_bytes()
    report = evaluate(json.loads(raw_dataset.decode("utf-8")), json.loads(raw_register.decode("utf-8")))
    report["dataset_path"] = args.dataset.as_posix()
    report["dataset_sha256"] = hashlib.sha256(raw_dataset).hexdigest()
    report["register_path"] = args.register.as_posix()
    # The register digest sits under local_evidence as a flat *_sha256 key (CFD-16 pattern).
    report["local_evidence"] = {"register_sha256": hashlib.sha256(raw_register).hexdigest()}
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
