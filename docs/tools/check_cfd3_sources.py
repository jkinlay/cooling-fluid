#!/usr/bin/env python3
"""Check public source-register and displayed-value traceability for CFD-3.

The JSON report deliberately contains aggregate counts only: it is safe to
publish alongside the public feasibility dataset without repeating source or
candidate details.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}\Z")
TOLERANCE = 0.01


def add(counter: Counter[str], rule: str) -> None:
    counter[rule] += 1


def result(failures: Counter[str], infos: Counter[str] | None = None) -> dict[str, object]:
    """Return a public aggregate result, preferring FAIL over INFO."""
    infos = infos or Counter()
    counts = Counter(failures)
    counts.update(infos)
    if failures:
        status = "FAIL"
    elif infos:
        status = "INFO"
    else:
        status = "PASS"
    return {
        "finding_count": sum(counts.values()),
        "rule_counts": dict(sorted(counts.items())),
        "status": status,
    }


def normalized_url(value: object) -> str | None:
    if not isinstance(value, str) or any(char.isspace() for char in value):
        return None
    parts = urlsplit(value)
    if not parts.scheme or not parts.netloc:
        return None
    scheme = parts.scheme.lower()
    host = parts.hostname.lower() if parts.hostname else ""
    if not host:
        return None
    try:
        port = parts.port
    except ValueError:
        return None
    netloc = host
    if parts.username is not None:
        netloc = parts.username
        if parts.password is not None:
            netloc += ":" + parts.password
        netloc += "@" + host
    if port is not None and not ((scheme == "https" and port == 443) or (scheme == "http" and port == 80)):
        netloc += ":" + str(port)
    return urlunsplit((scheme, netloc, parts.path, parts.query, ""))


def check_retrieved_dates(sources: list[dict[str, object]], created_date: object) -> dict[str, object]:
    failures: Counter[str] = Counter()
    try:
        created = (
            dt.date.fromisoformat(created_date)
            if isinstance(created_date, str) and DATE_RE.fullmatch(created_date)
            else None
        )
    except ValueError:
        created = None
    if created is None:
        add(failures, "dataset_created_date_invalid")
        return result(failures)
    for source in sources:
        value = source.get("retrieved_date")
        try:
            retrieved = (
                dt.date.fromisoformat(value)
                if isinstance(value, str) and DATE_RE.fullmatch(value)
                else None
            )
        except ValueError:
            retrieved = None
        if retrieved is None:
            add(failures, "invalid_retrieved_date")
        elif retrieved > created:
            add(failures, "retrieved_date_after_dataset_created_date")
    return result(failures)


def check_urls(sources: list[dict[str, object]]) -> dict[str, object]:
    failures: Counter[str] = Counter()
    infos: Counter[str] = Counter()
    for source in sources:
        value = source.get("url")
        normalized = normalized_url(value)
        if normalized is None:
            add(failures, "url_missing_scheme_netloc_or_contains_whitespace")
        elif urlsplit(normalized).scheme == "http":
            add(infos, "http_url")
        elif urlsplit(normalized).scheme != "https":
            add(failures, "url_scheme_not_https")
    return result(failures, infos)


def check_text_hashes(sources: list[dict[str, object]]) -> dict[str, object]:
    failures: Counter[str] = Counter()
    for source in sources:
        value = source.get("retrieved_text_sha256")
        if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
            add(failures, "retrieved_text_sha256_not_lowercase_sha256")
    return result(failures)


def check_duplicate_urls(sources: list[dict[str, object]]) -> dict[str, object]:
    failures: Counter[str] = Counter()
    infos: Counter[str] = Counter()
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for source in sources:
        normalized = normalized_url(source.get("url"))
        if normalized is not None:
            groups[normalized].append(source)
    for grouped_sources in groups.values():
        source_ids = {source.get("source_id") for source in grouped_sources}
        if len(source_ids) < 2:
            continue
        locators = [source.get("locator") for source in grouped_sources]
        if len(set(locators)) < len(locators):
            add(failures, "duplicate_url_and_locator")
        else:
            add(infos, "duplicate_url_with_distinct_locators")
    return result(failures, infos)


def observations_by_id(observations: list[dict[str, object]]) -> dict[object, list[dict[str, object]]]:
    grouped: dict[object, list[dict[str, object]]] = defaultdict(list)
    for observation in observations:
        grouped[observation.get("observation_id")].append(observation)
    return grouped


def as_number(value: object) -> float | None:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def check_boiling_traceability(candidates: list[dict[str, object]], observations: list[dict[str, object]]) -> dict[str, object]:
    failures: Counter[str] = Counter()
    infos: Counter[str] = Counter()
    by_id = observations_by_id(observations)
    for candidate in candidates:
        candidate_id = candidate.get("candidate_id")
        boiling = candidate.get("normal_boiling_point")
        if not isinstance(boiling, dict):
            add(failures, "normal_boiling_point_missing")
            continue
        ids = boiling.get("observation_ids")
        cited: list[dict[str, object]] = []
        if not isinstance(ids, list):
            add(failures, "observation_ids_not_list")
            ids = []
        for observation_id in ids:
            rows = by_id.get(observation_id, [])
            if len(rows) != 1:
                add(failures, "observation_reference_missing_or_ambiguous")
                continue
            observation = rows[0]
            cited.append(observation)
            if observation.get("candidate_id") != candidate_id:
                add(failures, "observation_candidate_mismatch")
            if observation.get("property") != "normal_boiling_point":
                add(failures, "observation_property_mismatch")
        if boiling.get("source_id") not in {row.get("source_id") for row in cited}:
            add(failures, "source_not_cited_by_observations")
        lows = [as_number(row.get("temperature_low_c")) for row in cited]
        highs = [as_number(row.get("temperature_high_c")) for row in cited]
        displayed_low = as_number(boiling.get("evidence_envelope_low_c"))
        displayed_high = as_number(boiling.get("evidence_envelope_high_c"))
        if not cited or None in lows or None in highs or displayed_low is None or displayed_high is None:
            add(infos, "envelope_not_computable_from_cited_observations")
        elif abs(displayed_low - min(lows)) > TOLERANCE or abs(displayed_high - max(highs)) > TOLERANCE:
            add(failures, "displayed_envelope_does_not_match_cited_observations")
    return result(failures, infos)


def check_flash_traceability(candidates: list[dict[str, object]], observations: list[dict[str, object]]) -> dict[str, object]:
    failures: Counter[str] = Counter()
    infos: Counter[str] = Counter()
    by_id = observations_by_id(observations)
    for candidate in candidates:
        candidate_id = candidate.get("candidate_id")
        flash = candidate.get("flash_point")
        if not isinstance(flash, dict):
            add(failures, "flash_point_missing")
            continue
        ids = flash.get("observation_ids")
        cited: list[dict[str, object]] = []
        if not isinstance(ids, list):
            add(failures, "observation_ids_not_list")
            ids = []
        for observation_id in ids:
            rows = by_id.get(observation_id, [])
            if len(rows) != 1:
                add(failures, "observation_reference_missing_or_ambiguous")
                continue
            observation = rows[0]
            cited.append(observation)
            if observation.get("candidate_id") != candidate_id:
                add(failures, "observation_candidate_mismatch")
            if observation.get("property") != "flash_point":
                add(failures, "observation_property_mismatch")
        selected = flash.get("selected_value_c")
        if selected is None:
            if any(flash.get(key) is not None for key in ("source_id", "relation", "method")):
                add(failures, "null_selection_has_display_metadata")
            continue
        selected_number = as_number(selected)
        if selected_number is None:
            add(failures, "selected_value_not_numeric")
            continue
        matches = []
        unsupported_value = False
        for observation in cited:
            value = as_number(observation.get("temperature_low_c"))
            if value is None:
                unsupported_value = True
                continue
            if (abs(value - selected_number) <= TOLERANCE
                    and observation.get("relation") == flash.get("relation")
                    and observation.get("source_id") == flash.get("source_id")):
                matches.append(observation)
        if not matches:
            if unsupported_value:
                add(infos, "selected_value_not_computable_for_all_cited_observations")
            else:
                add(failures, "selected_value_relation_or_source_not_cited")
    return result(failures, infos)


def build_report(dataset_path: Path) -> dict[str, object]:
    raw = dataset_path.read_bytes()
    dataset = json.loads(raw.decode("utf-8"))
    sources = dataset.get("sources", [])
    candidates = dataset.get("candidates", [])
    observations = dataset.get("observations", [])
    checks = {
        "boiling_display_traceability": check_boiling_traceability(candidates, observations),
        "duplicate_urls": check_duplicate_urls(sources),
        "flash_display_traceability": check_flash_traceability(candidates, observations),
        "retrieved_date_iso": check_retrieved_dates(sources, dataset.get("created_date")),
        "text_hash_format": check_text_hashes(sources),
        "url_well_formed": check_urls(sources),
    }
    statuses = Counter(check["status"] for check in checks.values())
    return {
        "checks": checks,
        "input_path": dataset_path.as_posix(),
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "overall_counts": {status: statuses.get(status, 0) for status in ("PASS", "FAIL", "INFO")},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    report = build_report(args.dataset)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 1 if report["overall_counts"]["FAIL"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
