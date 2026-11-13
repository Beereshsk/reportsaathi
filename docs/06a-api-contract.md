# API Contract Specification: Aushadha Sathi

**Document Reference:** `docs/06a-api-contract.md`  
**Dependencies:** [`docs/05-prd.md`](file:///c:/Users/beere/reportsaathi/docs/05-prd.md) and [`docs/06-architecture.md`](file:///c:/Users/beere/reportsaathi/docs/06-architecture.md)  
**Standard:** OpenAPI 3.1.0 Compatible Specification  
**Security & Privacy:** TLS 1.3, Anonymous Stateless Processing, Zero Persistent Storage

---

## 1. Global Specifications

* **Base URL:** `https://api.reportsaathi.in/v1` (Production) / `http://localhost:5000/api` (Local)
* **Transport:** HTTPS strictly enforced. All non-HTTPS requests receive `301 Moved Permanently`.
* **Content Negotiation:** `application/json` (standard), `multipart/form-data` (image uploads).
* **Character Encoding:** `UTF-8` (mandatory for Unicode Indic scripts like Kannada `kn`).

---

## 2. Endpoints

### 2.1 `POST /extract`
Parses explicit dosage, schedule, meal, and duration tokens from manually entered text. It preserves unrecognized details and flags missing fields; it does not identify medicine brands or infer missing values. Image OCR returns `501 OCR_UNAVAILABLE` until an OCR adapter is implemented.

#### Request Headers
| Header | Type | Required | Description |
|---|---|---|---|
| `Content-Type` | String | Yes | `multipart/form-data` (for files) OR `application/json` (for text) |
| `Accept` | String | Yes | `application/json` |

#### Request Body: Form-Data (Image Mode)
| Field | Type | Required | Validation / Description |
|---|---|---|---|
| `file` | Binary | Yes | JPEG, PNG, or WebP image. Maximum size: $10\text{ MB}$. Minimum resolution: $300\times 300\text{px}$. |
| `language` | String | No | Target UI language: `"kn"` (Kannada, default) or `"en"` (Indian English). |

#### Request Body: JSON (Text Fallback Mode)
```json
{
  "raw_text": "Paracetamol 650 1-0-1 after food 5 days\nTelma 40 1-0-0 before food",
  "language": "kn"
}
```

#### Success Response (200 OK)
```json
{
  "success": true,
  "request_id": "req-98f2b3a1-7c4e",
  "total_medicines_detected": 2,
  "has_ambiguous_entries": true,
  "language": "kn",
  "medicines": [
    {
      "id": "med-1",
      "raw_name": "Paracetamol 650mg",
      "canonical_name": "Paracetamol",
      "form": "tablet",
      "dosage": "650mg",
      "timing": {
        "morning": 1,
        "afternoon": 0,
        "night": 1
      },
      "meal_relation": "after_food",
      "duration_days": 5,
      "confidence": 0.96,
      "is_ambiguous": false,
      "display_text": {
        "kn": "ಪ್ಯಾರಸಿಟಮಾಲ್ 650mg: ಬೆಳಿಗ್ಗೆ 1, ರಾತ್ರಿ 1 (ಊಟದ ನಂತರ, 5 ದಿನಗಳು)",
        "en": "Paracetamol 650mg: 1 Morning, 1 Night (After Food, 5 Days)"
      }
    },
    {
      "id": "med-2",
      "raw_name": "Telma-40 (?)",
      "canonical_name": "Telmisartan (?)",
      "form": "tablet",
      "dosage": "40mg",
      "timing": {
        "morning": 1,
        "afternoon": 0,
        "night": 0
      },
      "meal_relation": "before_food",
      "duration_days": null,
      "confidence": 0.68,
      "is_ambiguous": true,
      "ambiguity_reason": "Low optical confidence on drug brand name. Cursive strokes resemble Telma or Tolol.",
      "display_text": {
        "kn": "ಟೆಲ್ಮಾ-40 (?): ಬೆಳಿಗ್ಗೆ 1 (ಉಪಹಾರಕ್ಕೆ ಮುನ್ನ) - ಔಷಧಿಕಾರರಲ್ಲಿ ಖಚಿತಪಡಿಸಿ",
        "en": "Telma-40 (?): 1 Morning (Before Food) - Confirm with Pharmacist"
      }
    }
  ],
  "disclaimer": "Please confirm all medicine details with your doctor or pharmacist before taking any medicine.",
  "timestamp": "2026-11-13T14:15:00Z"
}
```

#### Error Responses
* **400 Bad Request (Invalid File Format or Corrupt Body):**
  ```json
  {
    "success": false,
    "error_code": "INVALID_FILE_TYPE",
    "message": "Only JPEG, PNG, and WebP image formats are supported."
  }
  ```
* **413 Payload Too Large (File Size Exceeds 10MB):**
  ```json
  {
    "success": false,
    "error_code": "PAYLOAD_TOO_LARGE",
    "message": "Image size exceeds the 10MB limit. Please compress or crop the photo."
  }
  ```
* **501 Not Implemented (Image OCR Unavailable):** The image-reading adapter is not configured. Users must not be shown guessed medicine details.
* **422 Unprocessable Entity (Blurry or Unreadable Prescription):**
  ```json
  {
    "success": false,
    "error_code": "BLURRY_PRESCRIPTION",
    "message": "The prescription text is too blurry to extract reliably without guessing.",
    "tips": [
      "Ensure sufficient overhead lighting.",
      "Hold the phone parallel to the paper.",
      "Avoid shadows across the handwriting."
    ]
  }
  ```
* **429 Too Many Requests (Rate Limit Exceeded):**
  ```json
  {
    "success": false,
    "error_code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please wait 60 seconds before submitting another image."
  }
  ```

---

### 2.2 `POST /simplify`
Takes clinical abbreviations or complex medical terminology and returns deterministic, plain-language translations in Kannada and English.

#### Request Body (JSON)
```json
{
  "terms": ["TDS", "OD", "HS", "AC", "PC", "SOS", "q8h"],
  "language": "kn"
}
```

#### Success Response (200 OK)
```json
{
  "success": true,
  "simplified_terms": [
    { "term": "TDS", "meaning_en": "Three times daily (Morning, Afternoon, Night)", "meaning_kn": "ದಿನಕ್ಕೆ ಮೂರು ಬಾರಿ (ಬೆಳಿಗ್ಗೆ, ಮಧ್ಯಾಹ್ನ, ರಾತ್ರಿ)" },
    { "term": "OD", "meaning_en": "Once daily", "meaning_kn": "ದಿನಕ್ಕೆ ಒಂದು ಬಾರಿ" },
    { "term": "HS", "meaning_en": "At bedtime / Night", "meaning_kn": "ಮಲಗುವ ಮುನ್ನ / ರಾತ್ರಿ" },
    { "term": "AC", "meaning_en": "Before meals / food", "meaning_kn": "ಊಟ/ಉಪಹಾರಕ್ಕೆ ಮುನ್ನ" },
    { "term": "PC", "meaning_en": "After meals / food", "meaning_kn": "ಊಟದ ನಂತರ" },
    { "term": "SOS", "meaning_en": "Take only when required / pain arises", "meaning_kn": "ಅವಶ್ಯಕತೆ ಇದ್ದಾಗ ಮಾತ್ರ ತೆಗೆದುಕೊಳ್ಳಿ" },
    { "term": "q8h", "meaning_en": "Every 8 hours", "meaning_kn": "ಪ್ರತಿ 8 ಗಂಟೆಗಳಿಗೊಮ್ಮೆ" }
  ]
}
```

### 2.3 `POST /notes`
Accepts manually entered prescription text and returns it verbatim for clients that need a notes-only flow. The main assistant uses `/extract` to return parsed fields. This endpoint does not persist prescription data.

#### Request Body (JSON)
```json
{
  "raw_text": "Medicine name as written\nDirections: unclear",
  "language": "en"
}
```

#### Success Response (200 OK)
```json
{
  "success": true,
  "request_id": "note-a1b2c3d4e5f6",
  "notes_text": "Medicine name as written\nDirections: unclear",
  "language": "en",
  "disclaimer": "Please confirm all medicine details with your doctor or pharmacist before taking any medicine."
}
```

Empty text or unsupported languages return `400 INVALID_REQUEST`. Text longer than 20,000 characters returns `413 PAYLOAD_TOO_LARGE`. Prescription notes are held only while handling the request and are never written to the health database.

---

### 2.4 `GET /health`
Liveness, readiness, and database connectivity check for hosting orchestration.

#### Success Response (200 OK)
```json
{
  "status": "pass",
  "service": "aushadha-sathi-api",
  "version": "1.0.0",
  "timestamp": "2026-11-13T14:15:00Z",
  "database": {
    "status": "connected",
    "value": "Database connection healthy (SQLite)"
  }
}
```
