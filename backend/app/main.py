"""
Aushadha Sathi - Backend Application
Provides HTTP endpoints for health probes, mock extraction, and term simplification.
Reference: docs/06a-api-contract.md, docs/08-tasks.md (Task 01)
"""

import json
import os
from datetime import datetime, timezone
from uuid import uuid4

from flask import Flask, jsonify, make_response, request

from .database import init_db, read_health_value
from .models.schemas import (
    DatabaseHealth,
    DisplayText,
    ErrorResponse,
    ExtractionResponse,
    HealthResponse,
    MedicineItem,
    SimplifiedTerm,
    SimplifyResponse,
    TimingSlot,
)

app = Flask(__name__)

# Initialize database at startup
init_db()

OPENAPI_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "shared", "openapi.json")


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Accept, Authorization"
    return response


@app.route("/api/health", methods=["GET", "OPTIONS"])
def health_check():
    """
    GET /api/health
    Liveness and readiness check reading a verified value from the database.
    """
    if request.method == "OPTIONS":
        return make_response("", 204)

    db_status, db_value = read_health_value()
    response_data = HealthResponse(
        status="pass" if db_status == "connected" else "fail",
        service="aushadha-sathi-api",
        version="1.0.0",
        timestamp=datetime.now(timezone.utc).isoformat(),
        database=DatabaseHealth(status=db_status, value=db_value),
    )
    return jsonify(response_data.to_dict()), 200


@app.route("/api/openapi.json", methods=["GET", "OPTIONS"])
def get_openapi_schema():
    """Serves the OpenAPI 3.1.0 contract."""
    if request.method == "OPTIONS":
        return make_response("", 204)

    if os.path.exists(OPENAPI_PATH):
        with open(OPENAPI_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data), 200
    return jsonify({"error": "Schema not found"}), 404


@app.route("/api/extract", methods=["POST", "OPTIONS"])
def mock_extract():
    """
    POST /api/extract
    Mock extraction endpoint matching DoD: Deterministic responses matching rx-01-clean-standard.json.
    """
    if request.method == "OPTIONS":
        return make_response("", 204)

    req_data = {}
    if request.is_json:
        req_data = request.get_json() or {}

    raw_text = req_data.get("raw_text", "")

    # Check for blurry simulation
    if "~~~~~" in raw_text or req_data.get("simulated_blur_score", 1.0) < 0.5:
        err = ErrorResponse(
            error_code="BLURRY_PRESCRIPTION",
            message="The prescription text is too blurry to extract reliably without guessing.",
            tips=[
                "Ensure sufficient overhead lighting.",
                "Hold the phone parallel to the paper.",
                "Avoid shadows across the handwriting.",
            ],
        )
        return jsonify(err.to_dict()), 422

    # Deterministic extraction response matching rx-01-clean-standard.json
    response_data = ExtractionResponse(
        success=True,
        request_id="req-mock-rx-01",
        total_medicines_detected=2,
        has_ambiguous_entries=False,
        language=req_data.get("language", "kn"),
        medicines=[
            MedicineItem(
                id="med-1",
                raw_name="Paracetamol 650mg",
                canonical_name="Paracetamol",
                form="tablet",
                dosage="650mg",
                timing=TimingSlot(morning=1, afternoon=0, night=1),
                meal_relation="after_food",
                duration_days=5,
                confidence=0.96,
                is_ambiguous=False,
                display_text=DisplayText(
                    kn="ಪ್ಯಾರಸಿಟಮಾಲ್ 650mg: ಬೆಳಿಗ್ಗೆ 1, ರಾತ್ರಿ 1 (ಊಟದ ನಂತರ, 5 ದಿನಗಳು)",
                    en="Paracetamol 650mg: 1 Morning, 1 Night (After Food, 5 Days)",
                ),
            ),
            MedicineItem(
                id="med-2",
                raw_name="Pan-40",
                canonical_name="Pantoprazole",
                form="tablet",
                dosage="40mg",
                timing=TimingSlot(morning=1, afternoon=0, night=0),
                meal_relation="before_food",
                duration_days=5,
                confidence=0.94,
                is_ambiguous=False,
                display_text=DisplayText(
                    kn="ಪ್ಯಾನ್-40: ಬೆಳಿಗ್ಗೆ 1 (ಉಪಹಾರಕ್ಕೆ ಮುನ್ನ, 5 ದಿನಗಳು)",
                    en="Pan-40: 1 Morning (Before Breakfast, 5 Days)",
                ),
            ),
        ],
        disclaimer=(
            "Please confirm all medicine details with your doctor or pharmacist "
            "before taking any medicine."
        ),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    return jsonify(response_data.to_dict()), 200


@app.route("/api/notes", methods=["POST", "OPTIONS"])
def receive_notes():
    """Validate and return user-entered notes without saving prescription content."""
    if request.method == "OPTIONS":
        return make_response("", 204)

    req_data = request.get_json(silent=True)
    if not isinstance(req_data, dict):
        return jsonify({
            "success": False,
            "error_code": "INVALID_REQUEST",
            "message": "Send prescription notes as JSON.",
        }), 400

    raw_text = req_data.get("raw_text")
    language = req_data.get("language", "en")
    if not isinstance(raw_text, str) or not raw_text.strip():
        return jsonify({
            "success": False,
            "error_code": "INVALID_REQUEST",
            "message": "Enter the prescription notes you can read.",
        }), 400
    if len(raw_text) > 20_000:
        return jsonify({
            "success": False,
            "error_code": "PAYLOAD_TOO_LARGE",
            "message": "Notes must be 20,000 characters or fewer.",
        }), 413
    if language not in ("kn", "en"):
        return jsonify({
            "success": False,
            "error_code": "INVALID_REQUEST",
            "message": "Language must be 'kn' or 'en'.",
        }), 400

    return jsonify({
        "success": True,
        "request_id": f"note-{uuid4().hex[:12]}",
        "notes_text": raw_text,
        "language": language,
        "disclaimer": (
            "Please confirm all medicine details with your doctor or pharmacist "
            "before taking any medicine."
        ),
    }), 200


@app.route("/api/simplify", methods=["POST", "OPTIONS"])
def mock_simplify():
    """
    POST /api/simplify
    Mock abbreviation simplification endpoint matching docs/06a-api-contract.md §2.2.
    """
    if request.method == "OPTIONS":
        return make_response("", 204)

    req_data = request.get_json() or {}
    terms = req_data.get("terms", ["TDS", "OD", "HS", "AC", "PC", "SOS", "q8h"])

    dictionary = {
        "TDS": ("Three times daily (Morning, Afternoon, Night)", "ದಿನಕ್ಕೆ ಮೂರು ಬಾರಿ (ಬೆಳಿಗ್ಗೆ, ಮಧ್ಯಾಹ್ನ, ರಾತ್ರಿ)"),
        "OD": ("Once daily", "ದಿನಕ್ಕೆ ಒಂದು ಬಾರಿ"),
        "BD": ("Twice daily (Morning, Night)", "ದಿನಕ್ಕೆ ಎರಡು ಬಾರಿ (ಬೆಳಿಗ್ಗೆ, ರಾತ್ರಿ)"),
        "HS": ("At bedtime / Night", "ಮಲಗುವ ಮುನ್ನ / ರಾತ್ರಿ"),
        "AC": ("Before meals / food", "ಊಟ/ಉಪಹಾರಕ್ಕೆ ಮುನ್ನ"),
        "PC": ("After meals / food", "ಊಟದ ನಂತರ"),
        "SOS": ("Take only when required / pain arises", "ಅವಶ್ಯಕತೆ ಇದ್ದಾಗ ಮಾತ್ರ ತೆಗೆದುಕೊಳ್ಳಿ"),
        "q8h": ("Every 8 hours", "ಪ್ರತಿ 8 ಗಂಟೆಗಳಿಗೊಮ್ಮೆ"),
    }

    simplified_list = []
    for term in terms:
        en_meaning, kn_meaning = dictionary.get(term, ("Standard medical term", "ವೈದ್ಯಕೀಯ ಪದ"))
        simplified_list.append(
            SimplifiedTerm(term=term, meaning_en=en_meaning, meaning_kn=kn_meaning)
        )

    res = SimplifyResponse(success=True, simplified_terms=simplified_list)
    return jsonify(res.to_dict()), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
