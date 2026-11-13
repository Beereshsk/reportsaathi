import unittest

from backend.app.main import app


class TestPrescriptionNotesEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_notes_are_processed_and_returned_without_inference(self):
        raw_text = "Medicine: ABC as written\nDirections: unclear"
        response = self.client.post("/api/notes", json={"raw_text": raw_text, "language": "en"})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["notes_text"], raw_text)
        self.assertEqual(data["language"], "en")
        self.assertIn("doctor or pharmacist", data["disclaimer"])

    def test_notes_endpoint_rejects_empty_text(self):
        response = self.client.post("/api/notes", json={"raw_text": "  "})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error_code"], "INVALID_REQUEST")


if __name__ == "__main__":
    unittest.main()
