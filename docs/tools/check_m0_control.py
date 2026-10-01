"""Check bounded M0 study control against retained acceptance scenarios.

Document-control check only: no chemistry, legal, or AWF execution validation.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from datetime import date
from pathlib import Path

REQUIRED_POSITIVE_NUMBERS = (
    "accepted_research_hours_cap",
    "accepted_owner_hours_total",
    "accepted_owner_hours_per_week",
)
REQUIRED_OUTCOMES = ("STOP_DOMAIN", "INCONCLUSIVE", "CONTINUE")


def _valid_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def evaluate(record: dict, as_of_date: str) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if record.get("record_type") != "ACCEPTED_M0_STUDY_CONTROL" or record.get("status") != "ACCEPTED":
        reasons.append("status_not_accepted")
    if not isinstance(record.get("owner_account"), str) or not record["owner_account"].strip():
        reasons.append("missing_owner")
    if record.get("owner_accepted") is not True:
        reasons.append("owner_not_accepted")

    evidence = record.get("acceptance_evidence")
    if not isinstance(evidence, dict) or not all(evidence.get(k) for k in ("date", "owner", "response", "scope")):
        reasons.append("missing_acceptance_evidence")
    else:
        if not _valid_date(evidence["date"]):
            reasons.append("invalid_acceptance_date")
        if evidence["owner"] != record.get("owner_account"):
            reasons.append("acceptance_owner_mismatch")
        if evidence["response"] != "Accept these M0 limits":
            reasons.append("acceptance_response_mismatch")
        terms = evidence.get("accepted_terms")
        expected_terms = {
            "start_date": record.get("accepted_start_date"),
            "review_deadline": record.get("accepted_review_deadline"),
            "research_hours_cap": record.get("accepted_research_hours_cap"),
            "owner_hours_total": record.get("accepted_owner_hours_total"),
            "owner_hours_per_week": record.get("accepted_owner_hours_per_week"),
            "external_spend_cap_gbp": record.get("accepted_external_spend_cap_gbp"),
            "public_desk_only": True,
        }
        if not isinstance(terms, dict) or any(terms.get(k) != v for k, v in expected_terms.items()):
            reasons.append("acceptance_scope_mismatch")
        if _valid_date(evidence.get("date")) and evidence["date"] != record.get("accepted_start_date"):
            reasons.append("acceptance_start_date_mismatch")

    for field in ("accepted_start_date", "accepted_review_deadline"):
        if not _valid_date(record.get(field)):
            reasons.append(f"missing_or_invalid_{field}")
    for field in REQUIRED_POSITIVE_NUMBERS:
        value = record.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            reasons.append(f"missing_or_invalid_{field}")
    spend = record.get("accepted_external_spend_cap_gbp")
    if isinstance(spend, bool) or not isinstance(spend, (int, float)) or spend < 0:
        reasons.append("missing_or_invalid_spend_cap")
    elif spend != 0 or record.get("paid_action_authorized") is not False:
        reasons.append("external_spend_outside_owner_acceptance")
    consumed = record.get("actual_research_hours")
    if isinstance(consumed, bool) or not isinstance(consumed, (int, float)) or consumed < 0:
        reasons.append("invalid_consumed_hours")
    rules = record.get("outcome_rules")
    if not isinstance(rules, dict) or any(not isinstance(rules.get(k), str) or not rules[k].strip() for k in REQUIRED_OUTCOMES):
        reasons.append("missing_outcome_rules")
    if not isinstance(record.get("stop_rules"), list) or not record["stop_rules"]:
        reasons.append("missing_stop_rules")
    if reasons:
        return "PROPOSED_NOT_STARTED", reasons

    start = date.fromisoformat(record["accepted_start_date"])
    deadline = date.fromisoformat(record["accepted_review_deadline"])
    today = date.fromisoformat(as_of_date)
    if deadline < start:
        return "PROPOSED_NOT_STARTED", ["deadline_before_start"]
    if today < start:
        return "NOT_YET_STARTED", ["before_accepted_start"]
    boundary_reasons: list[str] = []
    if consumed >= record["accepted_research_hours_cap"]:
        boundary_reasons.append("research_hour_cap_reached")
    if today > deadline:
        boundary_reasons.append("accepted_deadline_passed")
    if boundary_reasons:
        if record.get("decisive_evidence_status") == "UNRESOLVED":
            boundary_reasons.append("decisive_evidence_unresolved")
        return "STOP_PENDING_OWNER_DECISION", boundary_reasons
    return "PUBLIC_DESK_ONLY", ["within_accepted_date_and_hour_caps"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--control", type=Path, required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    control_raw = args.control.read_bytes()
    cases_raw = args.cases.read_bytes()
    base = json.loads(control_raw)
    fixtures = json.loads(cases_raw)
    results = []
    for case in fixtures["cases"]:
        record = copy.deepcopy(base)
        for key in case.get("remove", []):
            record.pop(key, None)
        record.update(case.get("set", {}))
        record.get("acceptance_evidence", {}).update(case.get("evidence_set", {}))
        record.get("acceptance_evidence", {}).get("accepted_terms", {}).update(case.get("evidence_terms_set", {}))
        observed, reasons = evaluate(record, case["as_of_date"])
        reasons_match = all(reason in reasons for reason in case.get("expected_reasons", []))
        results.append({
            "id": case["id"],
            "input_scenario": case["input_scenario"],
            "input_record": record,
            "as_of_date": case["as_of_date"],
            "expected": case["expected"],
            "expected_reasons": case.get("expected_reasons", []),
            "observed": observed,
            "reasons": reasons,
            "result": "PASS" if observed == case["expected"] and reasons_match else "FAIL",
            "reviewer": "Codex controller; independent review pending",
            "date": "2026-10-01",
            "evidence_ref": "docs/feasibility/study_control.json and docs/feasibility/study_control_cases.json",
        })
    report = {
        "kind": "FDE-FEAS-001 control-case execution",
        "scope": "document control only; no chemistry or AWF dispatch verification",
        "control_path": args.control.as_posix(),
        "control_sha256": hashlib.sha256(control_raw).hexdigest(),
        "cases_path": args.cases.as_posix(),
        "cases_sha256": hashlib.sha256(cases_raw).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "results": results,
        "all_pass": all(r["result"] == "PASS" for r in results),
    }
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": report["all_pass"], "cases": [(r["id"], r["result"], r["observed"]) for r in results]}))
    if not report["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
