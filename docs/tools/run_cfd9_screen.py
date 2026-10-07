"""Run the CFD-9 application screen: every candidate against every register profile (report-only).

Uses the CFD-7 rules and checker (profile_ready, screen_evidence, screen_record) on the published
dataset and the acceptability register. For each adopted screening constraint the candidate's cited
observations of that property give an evidence envelope: wholly inside the inclusive window is INSIDE,
wholly outside is OUTSIDE, crossing a bound is OVERLAP, and no cited observation is MISSING. Evidence
labels follow the register screening_evidence_policy, so source-reported values screen as MEASURED and
stay labelled.

Per-candidate records go only to --local-output, which must be outside the repository. The committed
--summary is counts-only (status per profile and deciding rule) plus input and local-output hashes.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import subprocess
from typing import Any

from check_cfd7_application_screen import (STATUSES, adopted_constraints, check_rules, profile_ready,
                                           screen_evidence, screen_record)

POLICY = ("Report-only CFD-9 screen. Dataset, register and rules are not modified. Counts only; "
          "per-candidate records are kept outside the repository.")
SUPPORTED_DOMAINS = {"normal_boiling_point"}


def _num(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
        return float(value)
    return None


def window_outcome(low: float | None, high: float | None, constraint: dict[str, Any]) -> str | None:
    """INSIDE/OUTSIDE/OVERLAP for an envelope against an inclusive min/max window; None if no envelope."""
    if low is None or high is None:
        return None
    if low > high:
        raise ValueError("envelope low exceeds high")
    bounds = constraint.get("value") or {}
    lo, hi = _num(bounds.get("min")), _num(bounds.get("max"))
    inclusive = constraint.get("inclusive_boundary") or {}
    if lo is None or hi is None or inclusive.get("lower") is not True or inclusive.get("upper") is not True:
        raise ValueError("adopted constraint must be an inclusive numeric min/max window")
    if low >= lo and high <= hi:
        return "INSIDE"
    if high < lo or low > hi:
        return "OUTSIDE"
    return "OVERLAP"


def constraint_result(register: dict[str, Any], candidate: dict[str, Any], constraint: dict[str, Any],
                      by_id: dict[Any, list[dict[str, Any]]]) -> dict[str, Any]:
    domain = constraint.get("domain")
    if domain not in SUPPORTED_DOMAINS:
        raise ValueError("adopted constraint domain is not supported by the CFD-9 screen")
    field = candidate.get(domain) or {}
    cited = []
    for oid in field.get("observation_ids") or []:
        rows = by_id.get(oid, [])
        if len(rows) != 1 or rows[0].get("property") != domain or rows[0].get("candidate_id") != candidate.get("candidate_id"):
            raise ValueError("cited observation missing, ambiguous, wrong property or wrong candidate")
        cited.append(rows[0])
    if not cited:
        return {"evidence": "MISSING", "outcome": None}
    lows = [_num(r.get("temperature_low_c")) for r in cited]
    highs = [_num(r.get("temperature_high_c")) for r in cited]
    if None in lows or None in highs:
        return {"evidence": "MISSING", "outcome": None}
    if any(lo > hi for lo, hi in zip(lows, highs)):
        raise ValueError("cited observation has inverted bounds")
    types = {r.get("evidence_type") for r in cited}
    if len(types) != 1:
        raise ValueError("cited observations mix evidence types")
    evidence, label = screen_evidence(register, types.pop())
    result = {"evidence": evidence, "outcome": window_outcome(min(lows), max(highs), constraint)}
    if label:
        result["label"] = label
    return result


def identity_resolved(candidate: dict[str, Any]) -> bool:
    return (candidate.get("lane") == "PURE_CHEMICAL_IDENTITY"
            and all(isinstance(candidate.get(k), str) and candidate[k].strip() for k in ("candidate_id", "cas", "formula")))


def run(rules: dict[str, Any], register: dict[str, Any], dataset: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    problems = check_rules(rules)
    if problems:
        raise ValueError("rules file is not well formed")
    candidates, observations = dataset.get("candidates"), dataset.get("observations")
    profiles = register.get("profiles")
    if not isinstance(candidates, list) or not candidates or not isinstance(observations, list):
        raise ValueError("dataset must contain candidates and observations")
    if not isinstance(profiles, list) or not profiles:
        raise ValueError("register must contain profiles")
    by_id: dict[Any, list[dict[str, Any]]] = {}
    for row in observations:
        by_id.setdefault(row.get("observation_id"), []).append(row)
    records = []
    per_profile: dict[str, Counter[str]] = {}
    per_rule: dict[str, Counter[str]] = {}
    labels: Counter[str] = Counter()
    for profile in profiles:
        pid = profile.get("profile_id")
        readiness = profile_ready(register, profile)
        adopted = adopted_constraints(profile) if readiness[0] else []
        keys = [c["id"] for c in adopted]
        counts = per_profile.setdefault(pid, Counter())
        rules_used = per_rule.setdefault(pid, Counter())
        for candidate in candidates:
            results = {c["id"]: constraint_result(register, candidate, c, by_id) for c in adopted}
            record = screen_record(readiness, identity_resolved(candidate), keys, results)
            counts[record["status"]] += 1
            rules_used[record["rule"]] += 1
            labels.update(record["evidence_labels"])
            records.append({"candidate_id": candidate.get("candidate_id"), "profile_id": pid,
                            "rules_version": rules.get("version"), **record, "constraint_results": results})
    summary = {
        "candidates": len(candidates),
        "evidence_label_counts": dict(sorted(labels.items())),
        "pairs": len(records),
        "policy": POLICY,
        "profiles": len(profiles),
        "rules_version": rules.get("version"),
        "status": "PASS",
        "status_counts_by_profile": {pid: {s: c[s] for s in STATUSES} for pid, c in sorted(per_profile.items())},
        "deciding_rule_counts_by_profile": {pid: dict(sorted(c.items())) for pid, c in sorted(per_rule.items())},
        "adopted_screening_constraints_by_profile": {p.get("profile_id"): len(adopted_constraints(p)) for p in profiles},
    }
    return summary, records


def _inside_repo(path: Path, repo: Path) -> bool:
    try:
        path.resolve().relative_to(repo.resolve())
        return True
    except ValueError:
        return False


def safe_path(path: Path, repo: Path) -> str:
    """Repository-relative POSIX path for an in-repo input, else only the file name."""
    try:
        return path.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError:
        return path.name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rules", type=Path, required=True)
    parser.add_argument("--register", type=Path, required=True)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--local-output", type=Path, required=True)
    args = parser.parse_args()
    repo = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    if _inside_repo(args.local_output, repo):
        raise SystemExit("--local-output must be outside the repository")
    raw_rules, raw_register, raw_dataset = (p.read_bytes() for p in (args.rules, args.register, args.dataset))
    summary, records = run(*(json.loads(b.decode("utf-8")) for b in (raw_rules, raw_register, raw_dataset)))
    local = (json.dumps(records, indent=2, sort_keys=True) + "\n").encode("utf-8")
    args.local_output.parent.mkdir(parents=True, exist_ok=True)
    args.local_output.write_bytes(local)
    summary["dataset_path"] = safe_path(args.dataset, repo)
    summary["dataset_sha256"] = hashlib.sha256(raw_dataset).hexdigest()
    summary["local_evidence"] = {
        "per_candidate_records_sha256": hashlib.sha256(local).hexdigest(),
        "register_sha256": hashlib.sha256(raw_register).hexdigest(),
        "rules_sha256": hashlib.sha256(raw_rules).hexdigest(),
    }
    summary["register_path"] = safe_path(args.register, repo)
    summary["rules_path"] = safe_path(args.rules, repo)
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
