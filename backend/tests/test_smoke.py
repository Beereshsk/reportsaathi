"""
Automated Smoke Test Suite
Verifies end-to-end liveness, database reading, and contract health probe.
Reference: User Request & docs/08-tasks.md (Task 02 DoD)
"""

import time
import unittest

from backend.app.database import read_health_value
from backend.app.main import app


class TestAutomatedSmoke(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()

    def test_smoke_health_and_database_probe(self):
        """
        Automated Smoke Test:
        Probes the live /api/health endpoint, checks latency < 500ms,
        verifies 200 OK, service name, and confirms live database value extraction.
        """
        start_time = time.time()
        response = self.client.get("/api/health")
        duration = time.time() - start_time

        self.assertEqual(response.status_code, 200, f"Health check failed with status {response.status_code}")
        self.assertLess(duration, 0.500, f"Health probe exceeded 500ms: {duration:.3f}s")

        data = response.get_json()
        self.assertIsNotNone(data, "Health endpoint returned empty response")
        self.assertEqual(data.get("status"), "pass", f"Status expected 'pass', got {data.get('status')}")
        self.assertEqual(data.get("service"), "aushadha-sathi-api")
        self.assertEqual(data.get("version"), "1.0.0")

        # Database verification
        db = data.get("database", {})
        self.assertEqual(db.get("status"), "connected", "Database status must be 'connected'")
        db_val = db.get("value", "")
        self.assertTrue(len(db_val) > 0, "Database returned empty health value")
        self.assertIn("Database connection healthy", db_val)

    def test_smoke_direct_database_query(self):
        """Smoke test directly querying database read function."""
        status, value = read_health_value()
        self.assertEqual(status, "connected")
        self.assertTrue(len(value) > 0)

    def test_smoke_openapi_availability(self):
        """Smoke test verifying OpenAPI specification endpoint."""
        response = self.client.get("/api/openapi.json")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get("openapi"), "3.1.0")


if __name__ == "__main__":
    unittest.main()
