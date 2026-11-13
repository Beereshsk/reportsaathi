"""
Unit and Integration Tests for GET /api/health
Verifies health endpoint and database read functionality.
"""

import unittest

from backend.app.database import init_db, read_health_value
from backend.app.main import app


class TestHealthEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = app.test_client()

    def test_database_read_value(self):
        """Verify the database read function returns connected status and stored value."""
        status, value = read_health_value()
        self.assertEqual(status, "connected")
        self.assertIn("Database connection healthy", value)

    def test_health_get_success(self):
        """Verify GET /api/health returns 200 OK with valid JSON structure."""
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(data.get("status"), "pass")
        self.assertEqual(data.get("service"), "aushadha-sathi-api")
        self.assertEqual(data.get("version"), "1.0.0")
        self.assertIn("timestamp", data)

        # Database verification
        db = data.get("database")
        self.assertIsNotNone(db)
        self.assertEqual(db.get("status"), "connected")
        self.assertTrue(len(db.get("value", "")) > 0)
        self.assertIn("Database connection healthy", db.get("value"))

    def test_health_cors_headers(self):
        """Verify CORS headers are present for cross-origin frontend requests."""
        response = self.client.get("/api/health")
        self.assertEqual(response.headers.get("Access-Control-Allow-Origin"), "*")


if __name__ == "__main__":
    unittest.main()
