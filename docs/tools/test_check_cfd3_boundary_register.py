from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("check_cfd3_boundary_register.py")
SPEC = importlib.util.spec_from_file_location("boundary_checker", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class BoundaryRegisterCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / "docs").mkdir()
        (self.root / "docs/source.md").write_text(
            "# Title\n\nquoted statement\n\n## Other\n\nother statement\n",
            encoding="utf-8",
            newline="\n",
        )
        (self.root / "docs/source.json").write_text(
            json.dumps({"scope": {"statement": "quoted statement"}}), encoding="utf-8", newline="\n"
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def register(self, entry: dict | None = None) -> Path:
        entry = entry or {
            "entry_id": "SB-001",
            "kind": "SEARCH_BOUNDARY",
            "statement": "quoted statement",
            "source": {"path": "docs/source.md", "locator": "section: Title"},
        }
        path = self.root / "register.json"
        path.write_text(
            json.dumps({"schema_version": "1.0", "register_id": "test", "policy": "test", "entries": [entry]}),
            encoding="utf-8",
            newline="\n",
        )
        return path

    def result(self, register: Path) -> dict:
        output = self.root / "result.json"
        self.assertEqual(checker.main(["--register", str(register), "--root", str(self.root), "--output", str(output)]), 0)
        return json.loads(output.read_text(encoding="utf-8"))

    def test_pass(self) -> None:
        self.assertEqual(self.result(self.register())["status"], "PASS")

    def test_hashes_only_under_local_evidence(self) -> None:
        import hashlib
        register = self.register()
        report = self.result(register)
        self.assertNotIn("cited_file_sha256", report)
        self.assertNotIn("register_sha256", report)
        evidence = report["local_evidence"]
        self.assertEqual(evidence["register_sha256"], hashlib.sha256(register.read_bytes()).hexdigest())
        cited = {k: v for k, v in evidence.items() if k.startswith("cited_")}
        self.assertTrue(cited)
        for key, digest in evidence.items():
            self.assertTrue(key.endswith("_sha256"))
            self.assertRegex(digest, "^[0-9a-f]{64}$")

    def test_cited_key_is_flat(self) -> None:
        self.assertEqual(checker.cited_key("docs/feasibility/README.md"), "cited_docs_feasibility_readme_md_sha256")

    def test_cited_key_collision_fails(self) -> None:
        text = (self.root / "docs/source.md").read_text(encoding="utf-8")
        for name in ("docs/a-b.md", "docs/a_b.md"):
            (self.root / name).write_text(text, encoding="utf-8", newline="\n")
        self.assertEqual(checker.cited_key("docs/a-b.md"), checker.cited_key("docs/a_b.md"))
        entries = [
            {"entry_id": f"SB-00{i}", "kind": "SEARCH_BOUNDARY", "statement": statement,
             "source": {"path": name, "locator": locator}}
            for i, (name, statement, locator) in enumerate(
                (("docs/a-b.md", "quoted statement", "section: Title"),
                 ("docs/a_b.md", "other statement", "section: Other")), start=1)
        ]
        register = self.root / "register.json"
        register.write_text(
            json.dumps({"schema_version": "1.0", "register_id": "test", "policy": "test", "entries": entries}),
            encoding="utf-8", newline="\n")
        output = self.root / "result.json"
        self.assertEqual(checker.main(["--register", str(register), "--root", str(self.root), "--output", str(output)]), 1)
        report = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(report["failure_counts_by_rule"], {"cited_key_collision": 1})

    def test_paraphrased_quote_fails(self) -> None:
        register = self.register({"entry_id": "SB-001", "kind": "SEARCH_BOUNDARY", "statement": "paraphrased", "source": {"path": "docs/source.md", "locator": "section: Title"}})
        report, failed = checker.failure_report(register, self.root)
        self.assertTrue(failed)
        self.assertIn("verbatim_quote", report["failure_counts_by_rule"])

    def test_wrong_section_fails(self) -> None:
        register = self.register({"entry_id": "SB-001", "kind": "SEARCH_BOUNDARY", "statement": "quoted statement", "source": {"path": "docs/source.md", "locator": "section: Other"}})
        report, failed = checker.failure_report(register, self.root)
        self.assertTrue(failed)
        self.assertIn("verbatim_quote", report["failure_counts_by_rule"])

    def test_bad_json_pointer_fails(self) -> None:
        register = self.register({"entry_id": "SB-001", "kind": "SEARCH_BOUNDARY", "statement": "quoted statement", "source": {"path": "docs/source.json", "locator": "/scope/missing"}})
        report, failed = checker.failure_report(register, self.root)
        self.assertTrue(failed)
        self.assertIn("verbatim_quote", report["failure_counts_by_rule"])

    def test_duplicate_id_fails(self) -> None:
        register = self.register()
        document = json.loads(register.read_text(encoding="utf-8"))
        document["entries"].append(document["entries"][0].copy())
        register.write_text(json.dumps(document), encoding="utf-8", newline="\n")
        report, failed = checker.failure_report(register, self.root)
        self.assertTrue(failed)
        self.assertIn("entry_ids", report["failure_counts_by_rule"])

    def test_bad_kind_fails(self) -> None:
        register = self.register({"entry_id": "SB-001", "kind": "BAD_KIND", "statement": "quoted statement", "source": {"path": "docs/source.md", "locator": "section: Title"}})
        report, failed = checker.failure_report(register, self.root)
        self.assertTrue(failed)
        self.assertIn("kind", report["failure_counts_by_rule"])


if __name__ == "__main__":
    unittest.main()
