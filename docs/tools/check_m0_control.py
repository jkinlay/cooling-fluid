"""Check bounded M0 study control against retained acceptance scenarios.

Document-control check only: no chemistry, legal, AWF execution, or source
authentication validation.  The retained conversation text can be compared
exactly, but this local checker cannot authenticate its original author.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from datetime import date
from pathlib import Path

REQUIRED_POSITIVE_NUMBERS = (
    "accepted_research_hours_cap",
    "accepted_owner_hours_total",
    "accepted_owner_hours_per_week",
)
REQUIRED_OUTCOMES = ("STOP_DOMAIN", "INCONCLUSIVE", "CONTINUE")
RETAINED_OWNER_ACCOUNT = "jkinlay"
RETAINED_PUBLICATION_POLICY_STATUS = "UNDECIDED_CANDIDATE_LEVEL_PUBLICATION_BLOCKED"
RETAINED_ACCEPTANCE_TERMS = {
    "start_date": "2026-10-01",
    "review_deadline": "2026-10-14",
    "research_hours_cap": 40,
    "owner_hours_total": 8,
    "owner_hours_per_week": 4,
    "external_spend_cap_gbp": 0,
    "public_desk_only": True,
}
RETAINED_ACCEPTANCE_SCOPE = (
    "1–14 October 2026; ten working days; 40 shared research hours; eight owner-review hours "
    "total, at most four per week; zero external spend; stated checkpoint and stop rules; public "
    "desk research only"
)
RETAINED_ACCEPTANCE_EVIDENCE = {
    "date": "2026-10-01",
    "channel": "Codex conversation",
    "owner": RETAINED_OWNER_ACCOUNT,
    "response": "Accept these M0 limits",
    "scope": RETAINED_ACCEPTANCE_SCOPE,
    "accepted_terms": RETAINED_ACCEPTANCE_TERMS,
}
FIRST_CAP_ONLY_SCOPE = (
    "Research-hour ceiling only; the accepted 14 October deadline, owner-review limits, "
    "zero external spend and public desk-study restrictions remain unchanged."
)
SECOND_CAP_ONLY_SCOPE = (
    "Shared research-hour ceiling only. Continue unblocked streams; the previously accepted "
    "14 October deadline, eight owner-review hours (at most four per week), zero external "
    "spend and public desk-study/publication restrictions remain in force."
)
RETAINED_CAP_AMENDMENTS = (
    {
        "date": "2026-10-01",
        "channel": "Codex conversation",
        "response": "I am authorizing an increase in the number of research hours to 120",
        "previous_shared_research_hours_cap": 40,
        "accepted_shared_research_hours_cap": 120,
        "scope": FIRST_CAP_ONLY_SCOPE,
    },
    {
        "date": "2026-10-02",
        "channel": "Codex conversation",
        "response": "Increase the permitted research time to 1000 hours. Continue the project in all 3 streams and do not stop unless you are blocked or instructed to. Even if one of the streams is blocked, research should continue in the remaining streams",
        "previous_shared_research_hours_cap": 120,
        "accepted_shared_research_hours_cap": 1000,
        "scope": SECOND_CAP_ONLY_SCOPE,
    },
)
RETAINED_IMMUTABLE_CONTROL = {
    "record_type": "ACCEPTED_M0_STUDY_CONTROL",
    "version": "1.3",
    "status": "ACCEPTED",
    "epic": "CFD-1",
    "owner_account": RETAINED_OWNER_ACCOUNT,
    "owner_accepted": True,
    "proposed_start_date": "2026-10-01",
    "proposed_review_deadline": "2026-10-14",
    "actual_start_date": "2026-10-01",
    "accepted_review_deadline": "2026-10-14",
    "proposed_working_days": 10,
    "proposed_research_hours_cap": 40,
    "proposed_owner_hours_total": 8,
    "proposed_owner_hours_per_week": 4,
    "accepted_research_hours_cap": 1000,
    "accepted_owner_hours_total": 8,
    "accepted_owner_hours_per_week": 4,
    "authorized_external_spend_gbp": 0,
    "paid_action_authorized": False,
    "checkpoint": "Five working days or 20 shared research hours, whichever comes first; final decision at the accepted deadline or cap exhaustion.",
    "named_chemistry_reviewer": None,
    "named_thermal_reviewer": None,
    "laboratory_partner": None,
    "publication_policy_status": RETAINED_PUBLICATION_POLICY_STATUS,
    "stop_rules": [
        "All candidates in the bounded universe have measured hard failures => STOP_DOMAIN for that domain/profile",
        "Missing decisive data => INCONCLUSIVE or separately capped evidence request",
        "Cap/deadline reached => no automatic continuation",
        "Sunk engineering cost cannot override a hard constraint",
    ],
    "acceptance_evidence": RETAINED_ACCEPTANCE_EVIDENCE,
    "research_cap_amendments": [
        {"date": "2026-10-01", "channel": "Codex conversation", "owner": RETAINED_OWNER_ACCOUNT, "response": "I am authorizing an increase in the number of research hours to 120", "previous_shared_research_hours_cap": 40, "accepted_shared_research_hours_cap": 120, "scope": FIRST_CAP_ONLY_SCOPE},
        {"date": "2026-10-02", "channel": "Codex conversation", "owner": RETAINED_OWNER_ACCOUNT, "response": "Increase the permitted research time to 1000 hours. Continue the project in all 3 streams and do not stop unless you are blocked or instructed to. Even if one of the streams is blocked, research should continue in the remaining streams", "previous_shared_research_hours_cap": 120, "accepted_shared_research_hours_cap": 1000, "scope": SECOND_CAP_ONLY_SCOPE},
    ],
    "runtime_spike_hours_cap": None,
    "runtime_spike_spend_cap": None,
    "note": "The owner raised the shared research-hour cap to 120 on 1 October 2026 and to 1000 on 2 October 2026. Continue all unblocked streams. Public desk research remains bounded by the accepted 14 October deadline and other limits. This does not authorize outreach, paid computation, purchases, experiments, candidate-level publication, or work beyond the cap/deadline. AWF dispatch and Jira lifecycle writes remain subject to their separate gates.",
    "accepted_start_date": "2026-10-01",
    "accepted_external_spend_cap_gbp": 0,
    "schedule_basis": "The 29 Sep–12 Oct template proposal was superseded by owner acceptance on 1 Oct 2026; ten working days counted inclusively gives 14 Oct 2026.",
    "outcome_rules": {
        "STOP_DOMAIN": "All candidates in the named bounded universe/profile have measured hard failures against accepted constraints; owner decides to stop that domain.",
        "INCONCLUSIVE": "Decisive evidence missing or conflicting; mark UNKNOWN and request separately capped evidence or conclude INCONCLUSIVE.",
        "CONTINUE": "Only a specifically scoped public desk question inside the accepted M0 date/hour/spend limits after an owner-recorded decision; no automatic next stage.",
    },
}
MUTABLE_PROGRESS_FIELDS = {"actual_research_hours"}
OPTIONAL_MUTABLE_PROGRESS_FIELDS = {"decisive_evidence_status"}
ALLOWED_DECISIVE_EVIDENCE_STATUSES = {"UNRESOLVED"}


def _valid_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _reject_nonfinite(value: str) -> None:
    raise ValueError(f"non-finite JSON constant: {value}")


def _load_json(raw: bytes, label: str) -> object:
    try:
        return json.loads(raw, object_pairs_hook=_reject_duplicate_keys, parse_constant=_reject_nonfinite)
    except (json.JSONDecodeError, ValueError) as exc:
        raise ValueError(f"{label}: {exc}") from exc


def _same_json_value(actual: object, expected: object) -> bool:
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return set(actual) == set(expected) and all(
            _same_json_value(actual[key], value) for key, value in expected.items()
        )
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            _same_json_value(item, expected_item) for item, expected_item in zip(actual, expected)
        )
    return actual == expected


def _finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _immutable_control_is_retained(record: dict) -> bool:
    allowed_keys = set(RETAINED_IMMUTABLE_CONTROL) | MUTABLE_PROGRESS_FIELDS | OPTIONAL_MUTABLE_PROGRESS_FIELDS
    if set(record) - allowed_keys or not MUTABLE_PROGRESS_FIELDS <= set(record):
        return False
    if not _same_json_value(
        {key: value for key, value in record.items() if key in RETAINED_IMMUTABLE_CONTROL},
        RETAINED_IMMUTABLE_CONTROL,
    ):
        return False
    status = record.get("decisive_evidence_status")
    return status is None or status in ALLOWED_DECISIVE_EVIDENCE_STATUSES


def evaluate(record: dict, as_of_date: str) -> tuple[str, list[str]]:
    reasons: list[str] = []
    if not _immutable_control_is_retained(record):
        reasons.append("immutable_control_mismatch")
    if record.get("record_type") != "ACCEPTED_M0_STUDY_CONTROL" or record.get("status") != "ACCEPTED":
        reasons.append("status_not_accepted")
    if not isinstance(record.get("owner_account"), str) or not record["owner_account"].strip():
        reasons.append("missing_owner")
    elif record["owner_account"] != RETAINED_OWNER_ACCOUNT:
        reasons.append("acceptance_owner_mismatch")
    if record.get("owner_accepted") is not True:
        reasons.append("owner_not_accepted")

    evidence = record.get("acceptance_evidence")
    if not isinstance(evidence, dict) or not all(evidence.get(k) for k in ("date", "owner", "response", "scope")):
        reasons.append("missing_acceptance_evidence")
    else:
        if not _valid_date(evidence["date"]):
            reasons.append("invalid_acceptance_date")
        if evidence.get("owner") != RETAINED_OWNER_ACCOUNT:
            reasons.append("acceptance_owner_mismatch")
        if evidence.get("response") != RETAINED_ACCEPTANCE_EVIDENCE["response"]:
            reasons.append("acceptance_response_mismatch")
        terms = evidence.get("accepted_terms")
        if (
            set(evidence) != set(RETAINED_ACCEPTANCE_EVIDENCE)
            or evidence.get("date") != RETAINED_ACCEPTANCE_EVIDENCE["date"]
            or evidence.get("channel") != RETAINED_ACCEPTANCE_EVIDENCE["channel"]
            or evidence.get("owner") != RETAINED_ACCEPTANCE_EVIDENCE["owner"]
            or evidence.get("response") != RETAINED_ACCEPTANCE_EVIDENCE["response"]
            or evidence.get("scope") != RETAINED_ACCEPTANCE_EVIDENCE["scope"]
            or not _same_json_value(terms, RETAINED_ACCEPTANCE_TERMS)
        ):
            reasons.append("acceptance_scope_mismatch")
        retained_record_terms = {
            "accepted_start_date": RETAINED_ACCEPTANCE_TERMS["start_date"],
            "accepted_review_deadline": RETAINED_ACCEPTANCE_TERMS["review_deadline"],
            "accepted_owner_hours_total": RETAINED_ACCEPTANCE_TERMS["owner_hours_total"],
            "accepted_owner_hours_per_week": RETAINED_ACCEPTANCE_TERMS["owner_hours_per_week"],
            "accepted_external_spend_cap_gbp": RETAINED_ACCEPTANCE_TERMS["external_spend_cap_gbp"],
        }
        if any(not _same_json_value(record.get(key), value) for key, value in retained_record_terms.items()):
            reasons.append("acceptance_scope_mismatch")
        initial_cap = RETAINED_ACCEPTANCE_TERMS["research_hours_cap"]
        latest_cap = initial_cap
        effective_cap = initial_cap
        amendments = record.get("research_cap_amendments", [])
        if not _finite_number(initial_cap) or initial_cap <= 0:
            reasons.append("acceptance_scope_mismatch")
        if not isinstance(amendments, list):
            reasons.append("acceptance_scope_mismatch")
        else:
            if len(amendments) != len(RETAINED_CAP_AMENDMENTS):
                reasons.append("acceptance_scope_mismatch")
            for index, amendment in enumerate(amendments):
                expected_amendment = RETAINED_CAP_AMENDMENTS[index] if index < len(RETAINED_CAP_AMENDMENTS) else None
                valid = (
                    isinstance(amendment, dict)
                    and expected_amendment is not None
                    and amendment.get("owner") == RETAINED_OWNER_ACCOUNT
                    and set(amendment) == {"owner", *expected_amendment}
                    and all(amendment.get(key) == value for key, value in expected_amendment.items())
                    and amendment.get("date") >= RETAINED_ACCEPTANCE_EVIDENCE["date"]
                    and amendment.get("previous_shared_research_hours_cap") == latest_cap
                )
                if not valid:
                    reasons.append("acceptance_scope_mismatch")
                    break
                latest_cap = amendment["accepted_shared_research_hours_cap"]
                if amendment["date"] <= as_of_date:
                    effective_cap = latest_cap
        if latest_cap != record.get("accepted_research_hours_cap"):
            reasons.append("acceptance_scope_mismatch")
        if _valid_date(evidence.get("date")) and evidence["date"] != RETAINED_ACCEPTANCE_TERMS["start_date"]:
            reasons.append("acceptance_start_date_mismatch")

    for field in ("accepted_start_date", "accepted_review_deadline"):
        if not _valid_date(record.get(field)):
            reasons.append(f"missing_or_invalid_{field}")
    for field in REQUIRED_POSITIVE_NUMBERS:
        value = record.get(field)
        if not _finite_number(value) or value <= 0:
            reasons.append(f"missing_or_invalid_{field}")
    spend = record.get("accepted_external_spend_cap_gbp")
    if not _finite_number(spend) or spend < 0:
        reasons.append("missing_or_invalid_spend_cap")
    elif spend != 0 or record.get("paid_action_authorized") is not False:
        reasons.append("external_spend_outside_owner_acceptance")
    consumed = record.get("actual_research_hours")
    if not _finite_number(consumed) or consumed < 0:
        reasons.append("invalid_consumed_hours")
    if record.get("publication_policy_status") != RETAINED_PUBLICATION_POLICY_STATUS:
        reasons.append("publication_policy_outside_owner_acceptance")
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
    if consumed >= effective_cap:
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
    base = _load_json(control_raw, "control")
    fixtures = _load_json(cases_raw, "cases")
    if not isinstance(base, dict) or not isinstance(fixtures, dict) or not isinstance(fixtures.get("cases"), list):
        raise ValueError("control/cases top-level structure is invalid")
    results = []
    for case in fixtures["cases"]:
        record = copy.deepcopy(base)
        for key in case.get("remove", []):
            record.pop(key, None)
        record.update(case.get("set", {}))
        for dotted_path, value in case.get("set_path", {}).items():
            target = record
            *parents, field = dotted_path.split(".")
            for parent in parents:
                target = target[parent]
            target[field] = value
        for field, token in case.get("nonfinite_set", {}).items():
            if token != "NaN":
                raise ValueError(f"unsupported nonfinite test token: {token}")
            record[field] = float("nan")
        record.get("acceptance_evidence", {}).update(case.get("evidence_set", {}))
        record.get("acceptance_evidence", {}).get("accepted_terms", {}).update(case.get("evidence_terms_set", {}))
        amendment_records = record.get("research_cap_amendments")
        amendment_index = case.get("amendment_index", 0)
        if (
            isinstance(amendment_records, list)
            and isinstance(amendment_index, int)
            and 0 <= amendment_index < len(amendment_records)
            and isinstance(amendment_records[amendment_index], dict)
        ):
            for key in case.get("amendment_remove", []):
                amendment_records[amendment_index].pop(key, None)
            amendment_records[amendment_index].update(case.get("amendment_set", {}))
        observed, reasons = evaluate(record, case["as_of_date"])
        reasons_match = all(reason in reasons for reason in case.get("expected_reasons", []))
        results.append({
            "id": case["id"],
            "input_scenario": case["input_scenario"],
            "input_record": {
                **record,
                **{field: token for field, token in case.get("nonfinite_set", {}).items()},
            },
            "as_of_date": case["as_of_date"],
            "expected": case["expected"],
            "expected_reasons": case.get("expected_reasons", []),
            "observed": observed,
            "reasons": reasons,
            "result": "PASS" if observed == case["expected"] and reasons_match else "FAIL",
            "reviewer": "Codex controller; independent review pending",
            "date": case["as_of_date"],
            "evidence_ref": "docs/feasibility/study_control.json and docs/feasibility/study_control_cases.json",
        })
    for regression in fixtures.get("parser_regressions", []):
        try:
            _load_json(regression["raw"].encode("utf-8"), regression["id"])
            observed, reasons = "ACCEPTED", []
        except ValueError as exc:
            observed, reasons = "REJECTED", [str(exc)]
        expected_error = regression["expected_error"]
        results.append({
            "id": regression["id"],
            "input_scenario": regression["input_scenario"],
            "raw_input": regression["raw"],
            "expected": "REJECTED",
            "expected_reasons": [expected_error],
            "observed": observed,
            "reasons": reasons,
            "result": "PASS" if observed == "REJECTED" and any(expected_error in reason for reason in reasons) else "FAIL",
            "reviewer": "Codex controller; independent review pending",
            "evidence_ref": "docs/feasibility/study_control_cases.json",
        })
    report = {
        "kind": "FDE-FEAS-001 control-case execution",
        "scope": "document control only; no chemistry or AWF dispatch verification",
        "source_authentication_limitation": (
            "Exact retained conversation text is compared locally; this checker cannot authenticate "
            "the original owner or conversation source."
        ),
        "control_path": args.control.as_posix(),
        "control_sha256": hashlib.sha256(control_raw).hexdigest(),
        "cases_path": args.cases.as_posix(),
        "cases_sha256": hashlib.sha256(cases_raw).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "results": results,
        "all_pass": all(r["result"] == "PASS" for r in results),
    }
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": report["all_pass"], "cases": [(r["id"], r["result"], r["observed"]) for r in results]}))
    if not report["all_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
