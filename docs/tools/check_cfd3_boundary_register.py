#!/usr/bin/env python3
"""Validate a CFD-3 public-document search-boundary register."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ALLOWED_KINDS = {"INCLUSION_RULE", "EXCLUSION", "SEARCH_BOUNDARY", "NON_CLAIM"}
REQUIRED_TOP_LEVEL = {"schema_version", "register_id", "policy", "entries"}
REQUIRED_ENTRY = {"entry_id", "kind", "statement", "source"}
REQUIRED_SOURCE = {"path", "locator"}
HEADING = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$")


def normalized_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")


def cited_key(name: str) -> str:
    """Flat local_evidence key for a cited repo path, e.g. docs/a-b.md -> cited_docs_a_b_md_sha256.
    Every non-alphanumeric run maps to one underscore, so keys stay *_sha256 as the leak scan allows."""
    return "cited_" + re.sub(r"[^0-9A-Za-z]+", "_", name).strip("_").lower() + "_sha256"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pointer_tokens(pointer: str) -> list[str]:
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("pointer must begin with '/'")
    tokens = []
    for token in pointer[1:].split("/"):
        index = 0
        decoded = []
        while index < len(token):
            if token[index] != "~":
                decoded.append(token[index])
                index += 1
                continue
            if index + 1 == len(token) or token[index + 1] not in "01":
                raise ValueError("invalid RFC 6901 escape")
            decoded.append("/" if token[index + 1] == "1" else "~")
            index += 2
        tokens.append("".join(decoded))
    return tokens


def resolve_pointer(document: Any, pointer: str) -> Any:
    value = document
    for token in pointer_tokens(pointer):
        if isinstance(value, dict) and token in value:
            value = value[token]
        elif isinstance(value, list) and token.isdigit() and int(token) < len(value):
            value = value[int(token)]
        else:
            raise ValueError("pointer does not resolve")
    return value


def strings_under(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for child in value for item in strings_under(child)]
    if isinstance(value, dict):
        return [item for child in value.values() for item in strings_under(child)]
    return []


def markdown_section(text: str, locator: str) -> str:
    if not locator.startswith("section: "):
        raise ValueError("Markdown locator must begin with 'section: '")
    requested = locator[len("section: "):]
    lines = text.splitlines(keepends=True)
    start = None
    level = None
    for number, line in enumerate(lines):
        match = HEADING.match(line.rstrip("\n"))
        if match and match.group(2) == requested:
            start = number + 1
            level = len(match.group(1))
            break
    if start is None or level is None:
        raise ValueError("section heading does not exist")
    end = len(lines)
    for number in range(start, len(lines)):
        match = HEADING.match(lines[number].rstrip("\n"))
        if match and len(match.group(1)) <= level:
            end = number
            break
    return "".join(lines[start:end])


def failure_report(register: Path, root: Path) -> tuple[dict[str, Any], bool]:
    failures: Counter[str] = Counter()
    counts: Counter[str] = Counter()
    cited: dict[str, Path] = {}
    try:
        document = json.loads(normalized_text(register))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        document = None
        failures["schema"] += 1

    entries: list[Any] = []
    if not isinstance(document, dict):
        failures["schema"] += 1
    else:
        valid_top_level = (
            REQUIRED_TOP_LEVEL.issubset(document)
            and isinstance(document.get("schema_version"), str)
            and isinstance(document.get("register_id"), str)
            and isinstance(document.get("policy"), str)
            and isinstance(document.get("entries"), list)
        )
        if not valid_top_level:
            failures["schema"] += 1
        else:
            entries = document["entries"]

    statements: list[str] = []
    observed_ids: list[str] = []
    for position, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict) or not REQUIRED_ENTRY.issubset(entry):
            failures["schema"] += 1
            continue
        entry_id = entry["entry_id"]
        if not isinstance(entry_id, str):
            failures["schema"] += 1
        else:
            observed_ids.append(entry_id)
        kind = entry["kind"]
        if not isinstance(kind, str) or kind not in ALLOWED_KINDS:
            failures["kind"] += 1
        else:
            counts[kind] += 1
        statement = entry["statement"]
        if not isinstance(statement, str) or not statement:
            failures["schema"] += 1
            continue
        statements.append(statement)
        source = entry["source"]
        if not isinstance(source, dict) or not REQUIRED_SOURCE.issubset(source):
            failures["schema"] += 1
            continue
        source_path = source["path"]
        locator = source["locator"]
        if (
            not isinstance(source_path, str)
            or not source_path
            or not isinstance(locator, str)
            or not locator
            or "\\" in source_path
        ):
            failures["schema"] += 1
            continue
        candidate = (root / Path(source_path)).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            failures["source_tracked"] += 1
            continue
        if not candidate.is_file():
            failures["source_tracked"] += 1
            continue
        cited[candidate.relative_to(root).as_posix()] = candidate
        try:
            if candidate.suffix.lower() == ".md":
                matched = statement in markdown_section(normalized_text(candidate), locator)
            elif candidate.suffix.lower() == ".json":
                value = resolve_pointer(json.loads(normalized_text(candidate)), locator)
                matched = any(statement in text for text in strings_under(value))
            else:
                raise ValueError("unsupported source type")
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError):
            matched = False
        if not matched:
            failures["verbatim_quote"] += 1

    expected_ids = [f"SB-{number:03d}" for number in range(1, len(entries) + 1)]
    if observed_ids != expected_ids:
        failures["entry_ids"] += 1
    if len(statements) != len(set(statements)):
        failures["no_duplicates"] += 1

    # Distinct cited paths must keep distinct evidence keys; otherwise one digest would be lost.
    if len({cited_key(name) for name in cited}) != len(cited):
        failures["cited_key_collision"] += 1

    # Digests of the public register and cited files sit under local_evidence (CFD-13 precedent).
    report = {
        "entry_counts_by_kind": dict(sorted(counts.items())),
        "failure_counts_by_rule": dict(sorted(failures.items())),
        "local_evidence": {
            **{cited_key(name): sha256_file(path) for name, path in sorted(cited.items())},
            "register_sha256": sha256_file(register),
        },
        "status": "FAIL" if failures else "PASS",
    }
    return report, bool(failures)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", required=True, type=Path)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    register = args.register.resolve()
    report, failed = failure_report(register, root)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
