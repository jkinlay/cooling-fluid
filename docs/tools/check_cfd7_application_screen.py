"""Check the CFD-7 application-screen rules file and report screen readiness (report-only).

Rules:
  rules_well_formed  - the rules file declares exactly the allowed statuses, a contiguous evaluation
                       order whose outcomes are allowed statuses, and adopts no numerical limit.
  profile_readiness  - each register profile is SCREEN_NOT_READY unless the register is ready for
                       candidate judgement, the profile is approved and it has an adopted screening
                       constraint.
screen_candidate() applies the evaluation order to one candidate's results for every adopted constraint.
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

POLICY = "Report-only. The register and dataset are not modified; counts only."
STATUSES = ("SCREEN_NOT_READY", "UNKNOWN", "DEFERRED_PREDICTED_FAIL", "EXCLUDED_MEASURED_HARD_FAIL", "SURVIVES_SCREEN")
EXPECTED = (
    ("profile_gate", "on_fail", "SCREEN_NOT_READY"),
    ("adopted_constraints_only", "on_fail", "SCREEN_NOT_READY"),
    ("identity_gate", "on_fail", "UNKNOWN"),
    ("measured_hard_fail", "on_match", "EXCLUDED_MEASURED_HARD_FAIL"),
    ("predicted_fail", "on_match", "DEFERRED_PREDICTED_FAIL"),
    ("unresolved_constraint", "on_match", "UNKNOWN"),
    ("all_measured_inside", "on_match", "SURVIVES_SCREEN"),
)
ORDER = tuple(rule for rule, _, _ in EXPECTED)
EVIDENCE = {"MEASURED", "PREDICTED", "MISSING"}
OUTCOMES = {"INSIDE", "OUTSIDE", "OVERLAP", "CONFLICT"}
# Project specification profile states; RESEARCH_DRAFT is never screened.
SCREENABLE_STATES = {"RESEARCH_FROZEN", "CAMPAIGN_READY", "QUALIFICATION_READY"}


_NUMBER_TEXT = re.compile(r"\s*[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?\s*")


def _is_number(val: Any) -> bool:
    if isinstance(val, bool):
        return False
    if isinstance(val, (int, float)):
        return True
    return isinstance(val, str) and _NUMBER_TEXT.fullmatch(val) is not None


def _has_numeric_limit(node: Any, step_entry: bool = False) -> bool:
    """True if any value is a number (or numeric text) under any field name.

    The only exemptions are the integer step number of an evaluation_order entry and the
    top-level rules version label.
    """
    if isinstance(node, dict):
        for key, val in node.items():
            if step_entry and key == "step" and isinstance(val, int) and not isinstance(val, bool):
                continue
            if _is_number(val) or _has_numeric_limit(val, step_entry=(key == "evaluation_order")):
                return True
        return False
    if isinstance(node, list):
        return any(_is_number(item) or _has_numeric_limit(item, step_entry=step_entry) for item in node)
    return False


def check_rules(rules: dict[str, Any]) -> list[str]:
    problems = []
    if set(rules.get("allowed_screen_statuses") or {}) != set(STATUSES):
        problems.append("statuses")
    if set(rules.get("allowed_constraint_evidence") or []) != EVIDENCE:
        problems.append("evidence")
    if set(rules.get("allowed_constraint_outcomes") or []) != OUTCOMES:
        problems.append("outcomes")
    steps = rules.get("evaluation_order")
    if not isinstance(steps, list) or [s.get("rule") for s in steps] != list(ORDER):
        problems.append("order")
    else:
        if [s.get("step") for s in steps] != list(range(1, len(ORDER) + 1)):
            problems.append("step_numbers")
        for s, (rule, key, status) in zip(steps, EXPECTED):
            if s.get(key) != status or ("on_fail" in s) == ("on_match" in s):
                problems.append(f"outcome:{rule}")
    if _has_numeric_limit({key: val for key, val in rules.items() if key != "version"}):
        problems.append("numeric_limit")
    return problems


def adopted_constraints(profile: dict[str, Any]) -> list[dict[str, Any]]:
    return [c for c in profile.get("constraints") or []
            if c.get("hard_rule_adopted") is True and c.get("candidate_screening_rule") is True
            and c.get("status") == "ADOPTED"]


def profile_ready(register: dict[str, Any], profile: dict[str, Any]) -> tuple[bool, str]:
    if register.get("candidate_judgement_ready") is not True or profile.get("profile_state") not in SCREENABLE_STATES:
        return False, "profile_gate"
    if not adopted_constraints(profile):
        return False, "adopted_constraints_only"
    return True, ""


def screen_candidate(ready: bool, identity_resolved: bool, adopted_keys: list[str],
                     results: dict[str, dict[str, str]]) -> tuple[str, str]:
    """Return (status, deciding rule) for one candidate under one profile.

    adopted_keys lists every adopted screening constraint of the profile; results maps those keys to
    evidence/outcome labels. An adopted constraint with no result counts as MISSING evidence, and a
    result for a constraint that is not adopted is rejected.
    """
    if not ready:
        return "SCREEN_NOT_READY", "profile_gate"
    if not adopted_keys:
        return "SCREEN_NOT_READY", "adopted_constraints_only"
    if len(set(adopted_keys)) != len(adopted_keys):
        raise ValueError("adopted constraint keys must be unique")
    extra = set(results) - set(adopted_keys)
    if extra:
        raise ValueError("result supplied for a constraint that is not adopted")
    covered = [results.get(key, {"evidence": "MISSING", "outcome": None}) for key in adopted_keys]
    if not identity_resolved:
        return "UNKNOWN", "identity_gate"
    for r in covered:
        if r.get("evidence") not in EVIDENCE or r.get("outcome") not in OUTCOMES | {None}:
            raise ValueError("constraint result has an unknown evidence or outcome label")
    if any(r["evidence"] == "MEASURED" and r.get("outcome") == "OUTSIDE" for r in covered):
        return "EXCLUDED_MEASURED_HARD_FAIL", "measured_hard_fail"
    if any(r["evidence"] == "PREDICTED" and r.get("outcome") == "OUTSIDE" for r in covered):
        return "DEFERRED_PREDICTED_FAIL", "predicted_fail"
    if any(r["evidence"] != "MEASURED" or r.get("outcome") != "INSIDE" for r in covered):
        return "UNKNOWN", "unresolved_constraint"
    return "SURVIVES_SCREEN", "all_measured_inside"


def evaluate(rules: dict[str, Any], register: dict[str, Any]) -> dict[str, Any]:
    profiles = register.get("profiles")
    if not isinstance(profiles, list) or not profiles:
        raise ValueError("register must contain a non-empty profiles list")
    problems = check_rules(rules)
    readiness: Counter[str] = Counter()
    adopted = 0
    for profile in profiles:
        ok, rule = profile_ready(register, profile)
        adopted += len(adopted_constraints(profile))
        readiness["READY" if ok else f"SCREEN_NOT_READY_{rule}"] += 1
    return {
        "adopted_screening_constraints": adopted,
        "policy": POLICY,
        "profile_readiness_counts": dict(sorted(readiness.items())),
        "profiles": len(profiles),
        "rule_counts": {
            "rules_well_formed": {"FAIL": len(problems), "PASS": 0 if problems else 1},
        },
        "rules_problems": problems,
        "rules_version": rules.get("version"),
        "status": "FAIL" if problems else "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rules", type=Path, required=True)
    parser.add_argument("--register", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw_rules = args.rules.read_bytes()
    raw = args.register.read_bytes()
    report = evaluate(json.loads(raw_rules.decode("utf-8")), json.loads(raw.decode("utf-8")))
    report["rules_path"] = args.rules.as_posix()
    report["dataset_path"] = args.register.as_posix()
    report["dataset_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 1 if report["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
