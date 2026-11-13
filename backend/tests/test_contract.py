"""
Contract Tests & Fixture Validation Suite
Reference: docs/08-tasks.md (Task 01 DoD) & docs/06a-api-contract.md
"""

import glob
import json
import os
import unittest

from backend.app.main import app

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FIXTURES_DIR = os.path.join(PROJECT_ROOT, "tests", "fixtures")
OPENAPI_PATH = os.path.join(PROJECT_ROOT, "shared", "openapi.json")


class TestApiContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_openapi_schema_syntax_and_paths(self):
        """DoD 1: OpenAPI 3.1 schema validates with zero syntax errors and required endpoints."""
        self.assertTrue(os.path.exists(OPENAPI_PATH), f"OpenAPI file not found at {OPENAPI_PATH}")
        with open(OPENAPI_PATH, "r", encoding="utf-8") as f:
            schema = json.load(f)

        self.assertEqual(schema.get("openapi"), "3.1.0")
        self.assertIn("info", schema)
        self.assertIn("paths", schema)

        paths = schema.get("paths", {})
        self.assertIn("/health", paths)
        self.assertIn("/extract", paths)
        self.assertIn("/notes", paths)
        self.assertIn("/simplify", paths)

        # Components and schemas verification
        schemas = schema.get("components", {}).get("schemas", {})
        for required_schema in [
            "HealthResponse",
            "DatabaseHealth",
            "MedicineItem",
            "TimingSlot",
            "ExtractionResponse",
            "PrescriptionNotesRequest",
            "PrescriptionNotesResponse",
            "SimplifyRequest",
            "SimplifyResponse",
            "ErrorResponse",
        ]:
            self.assertIn(required_schema, schemas, f"Missing component schema: {required_schema}")

    def test_mock_extract_matches_rx01(self):
        """DoD 2: Mock server returns deterministic responses matching rx-01-clean-standard.json."""
        rx01_path = os.path.join(FIXTURES_DIR, "rx-01-clean-standard.json")
        self.assertTrue(os.path.exists(rx01_path), f"Fixture not found: {rx01_path}")

        with open(rx01_path, "r", encoding="utf-8") as f:
            fixture = json.load(f)

        input_payload = fixture.get("input", {})
        expected_output = fixture.get("expected_output", {})

        response = self.client.post("/api/extract", json=input_payload)
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data.get("total_medicines_detected"), expected_output.get("total_medicines"))
        self.assertEqual(data.get("has_ambiguous_entries"), expected_output.get("has_ambiguous_entries"))

        meds = data.get("medicines", [])
        expected_meds = expected_output.get("medicines", [])
        self.assertEqual(len(meds), len(expected_meds))

        for idx, expected_med in enumerate(expected_meds):
            actual_med = meds[idx]
            self.assertEqual(actual_med.get("raw_name"), expected_med.get("raw_name"))
            self.assertEqual(actual_med.get("dosage"), expected_med.get("dosage"))
            self.assertEqual(actual_med.get("timing"), expected_med.get("timing"))
            self.assertEqual(actual_med.get("meal_relation"), expected_med.get("meal_relation"))
            self.assertEqual(actual_med.get("duration_days"), expected_med.get("duration_days"))
            self.assertEqual(actual_med.get("is_ambiguous"), expected_med.get("is_ambiguous"))

    def test_all_ten_fixtures_exist_and_validate(self):
        """Validates that all 10 fixtures in tests/fixtures parse as valid JSON and have required keys."""
        fixture_files = sorted(glob.glob(os.path.join(FIXTURES_DIR, "*.json")))
        self.assertEqual(len(fixture_files), 10, f"Expected 10 fixtures, found {len(fixture_files)}")

        expected_ids = [
            "rx-01-clean-standard",
            "rx-02-chronic-hypertension",
            "rx-03-diabetes-metformin",
            "rx-04-lasa-lookalike-pair",
            "rx-05-blurry-illegible",
            "rx-06-kannada-vernacular-notes",
            "rx-07-overdose-safety-breach",
            "rx-08-adversarial-diagnosis-prompt",
            "rx-09-adversarial-dose-alteration",
            "rx-10-printed-discharge-summary",
        ]

        found_ids = []
        for file_path in fixture_files:
            with open(file_path, "r", encoding="utf-8") as f:
                content = json.load(f)
            found_ids.append(content.get("id"))
            self.assertIn("category", content)
            self.assertIn("input", content)
            self.assertIn("expected_output", content)
            self.assertIn("safety_assertions", content)

        self.assertEqual(sorted(found_ids), sorted(expected_ids))

    def test_simplify_endpoint(self):
        """Verifies POST /api/simplify returns structured meanings for clinical abbreviations."""
        payload = {"terms": ["TDS", "AC", "PC"], "language": "kn"}
        response = self.client.post("/api/simplify", json=payload)
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertTrue(data.get("success"))
        terms = data.get("simplified_terms", [])
        self.assertEqual(len(terms), 3)
        term_map = {t["term"]: t for t in terms}
        self.assertIn("TDS", term_map)
        self.assertIn("Three times daily", term_map["TDS"]["meaning_en"])


if __name__ == "__main__":
    unittest.main()
