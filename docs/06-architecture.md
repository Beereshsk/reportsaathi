# Technical Architecture & System Design: Aushadha Sathi

**Document Reference:** `docs/06-architecture.md`  
**Dependencies:** [`docs/01-problem.md`](file:///c:/Users/beere/reportsaathi/docs/01-problem.md) through [`docs/05-prd.md`](file:///c:/Users/beere/reportsaathi/docs/05-prd.md)  
**Constraint Mandate:** 100% Free or Open-Source tools, ephemeral in-memory processing, budget Android performance, and zero persistent storage.

---

## 1. System Architecture Overview

The system is designed with an **ephemeral, stateless architecture**. User prescription data is processed strictly in-flight in RAM; no files are saved to disk, no databases exist, and all session state resides in the client browser.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ SYSTEM TOPOLOGY (STATELESS PIPELINE)                                                   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   CLIENT TIER (Budget Android Browser / PWA)                                           │
│   ┌──────────────────────────────────────────────────────────────────────────────┐     │
│   │ • HTML5 / Vanilla JS / React SPA (<180KB bundle)                             │     │
│   │ • Client-side Image Downscaler (Canvas API: max 1920px)                      │     │
│   │ • Web Speech API (Local Kannada 'kn-IN' & English 'en-IN' TTS)               │     │
│   │ • Web Share API / WhatsApp URL Protocol (wa.me/?text=...)                    │     │
│   └──────────────────────┬───────────────────────────────────────────────────────┘     │
│                          │ HTTPS POST (TLS 1.3 / Multipart Form)                       │
│                          ▼                                                             │
│   BACKEND TIER (Python Flask / FastAPI Stateless Engine)                               │
│   ┌──────────────────────────────────────────────────────────────────────────────┐     │
│   │ 1. Rate Limiting (In-memory IP token bucket)                                 │     │
│   │ 2. Stream Ingestion (BytesIO buffer — NO DISK WRITE)                         │     │
│   │ 3. Multimodal Extraction Layer (Free-tier Gemini Flash / Vision)             │     │
│   │ 4. Deterministic Shorthand Parser (1-0-1, OD, BD, TDS, AC, PC Regex Engine)  │     │
│   │ 5. Ambiguity Confidence Evaluator (Scores <0.85 -> is_ambiguous: true)       │     │
│   │ 6. Deterministic Bilingual Dictionary (Kannada / English Mapping)            │     │
│   └──────────────────────┬───────────────────────────────────────────────────────┘     │
│                          │                                                             │
│                          ▼ JSON Response (No DB, In-Memory Stream Purged)              │
│   CLIENT TILES RENDERED IN BROWSER MEMORY                                              │
│                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Comparison of Two Stack Options & Recommendation

| Architectural Dimension | Option A: Unified Python Flask / FastAPI + Modern Vanilla/React PWA (Recommended) | Option B: Next.js (TypeScript) Serverless on Vercel |
|---|---|---|
| **Architecture** | Lightweight Python API serving optimized static assets or decoupled SPA. | Fullstack TypeScript Next.js with Serverless Edge Functions. |
| **Image Processing (OCR)** | **Superior:** Python's ecosystem (`Pillow`, `PyMuPDF`, `PaddleOCR`, `Tesseract`, official Google GenAI SDK) provides native byte-stream manipulation in RAM. | **Constrained:** Node.js serverless functions have strict 4.5MB payload limits on Vercel free tier; Sharp compilation can cause cold-start issues. |
| **Determinism & Regex** | High-performance Python regex engine handling Indian medical abbreviation dictionaries (*OD, BD, TDS, SOS, AC, PC*). | Standard JavaScript RegExp engine. |
| **Cold Start Latency** | Low and predictable on free containers (Render / Hugging Face Spaces). | Edge/Serverless cold starts can add $2–$4\text{s}$ delay during image uploads on free tiers. |
| **Free-Tier Viability** | **100% Free:** Deployable as a single unified service on Render Free Tier or Hugging Face Spaces. | Free on Vercel, but external OCR/LLM API calls require separate secrets orchestration. |
| **Bundle Footprint** | Extremely low ($<80\text{KB}$ with Vanilla ES6/Preact). Critical for budget Android devices. | Next.js runtime baseline bundle is typically $180\text{KB}–$300\text{KB}$. |

### Architectural Recommendation: **Option A (Python FastAPI/Flask + Lightweight Client)**
* **Why:** Python allows zero-disk image buffer operations (`io.BytesIO`), direct integration with free multimodal AI libraries, and unified single-port hosting on Render or Hugging Face Spaces with zero deployment friction.

---

## 3. Data Model (Stateless Ephemeral Schemas)

*There are **no database tables** in this product.* The data model exists strictly as validated in-memory Pydantic / TypeScript transfer schemas:

```typescript
// 1. Ingestion Request Schema
interface PrescriptionRequest {
  image_base64?: string;       // Base64 encoded JPEG/PNG (if image mode)
  raw_text?: string;           // Manual user typed instructions (if text mode)
  target_language: "kn" | "en"; // Preferred translation language
}

// 2. Individual Medicine Item Schema
interface MedicineItem {
  id: string;                  // Client ephemeral UUID (e.g. "med-1")
  raw_name: string;            // Name as extracted from prescription (e.g. "Paracetamol 650mg")
  form: "tablet" | "capsule" | "syrup" | "injection" | "ointment" | "other";
  dosage: string;              // Extracted strength (e.g. "650mg")
  timing: {
    morning: number;           // Quantity to take in morning (e.g. 1)
    afternoon: number;         // Quantity to take in afternoon (e.g. 0)
    night: number;             // Quantity to take at night (e.g. 1)
  };
  meal_relation: "before_food" | "after_food" | "with_food" | "unspecified";
  duration_days: number | null;// Number of prescribed days (null if ongoing/unspecified)
  confidence: number;          // Optical confidence score (0.0 to 1.0)
  is_ambiguous: boolean;       // TRUE if confidence < 0.85 or text contains illegible cursive
  ambiguity_reason?: string;   // Explanation (e.g. "Cursive handwriting partially unreadable")
}

// 3. Extraction Response Payload
interface ExtractionResponse {
  success: boolean;
  medicines: MedicineItem[];
  total_medicines_detected: number;
  has_ambiguous_entries: boolean;
  disclaimer: string;          // Mandatory statutory disclaimer
  language: "kn" | "en";
  timestamp: string;           // ISO UTC timestamp (ephemeral)
}
```

---

## 4. API Endpoints & Contract Specification

### 4.1 `POST /api/extract`
Processes a prescription image or raw text and outputs the structured schedule.

* **Headers:** `Content-Type: multipart/form-data` or `application/json`
* **Request Body (Multipart):**
  * `file`: Binary image stream (JPEG, PNG, WebP)
  * `language`: `"kn"` or `"en"`
* **Response (200 OK):**
  ```json
  {
    "success": true,
    "total_medicines_detected": 2,
    "has_ambiguous_entries": true,
    "medicines": [
      {
        "id": "med-1",
        "raw_name": "Paracetamol 650mg",
        "form": "tablet",
        "dosage": "650mg",
        "timing": { "morning": 1, "afternoon": 0, "night": 1 },
        "meal_relation": "after_food",
        "duration_days": 5,
        "confidence": 0.96,
        "is_ambiguous": false
      },
      {
        "id": "med-2",
        "raw_name": "Telma-40 (?)",
        "form": "tablet",
        "dosage": "40mg",
        "timing": { "morning": 1, "afternoon": 0, "night": 0 },
        "meal_relation": "before_food",
        "duration_days": null,
        "confidence": 0.68,
        "is_ambiguous": true,
        "ambiguity_reason": "Low optical confidence on drug brand name. Cursive strokes resemble Telma or Tolol."
      }
    ],
    "disclaimer": "Please confirm all medicine details with your doctor or pharmacist before taking any medicine.",
    "language": "kn",
    "timestamp": "2026-11-13T14:15:00Z"
  }
  ```
* **Error Responses:**
  * `400 Bad Request`: `{ "error": "INVALID_IMAGE", "message": "File format not supported. Please upload a JPG or PNG." }`
  * `422 Unprocessable`: `{ "error": "BLURRY_IMAGE", "message": "The prescription is too blurry to extract reliably. Please retake under better lighting." }`
  * `429 Too Many Requests`: `{ "error": "RATE_LIMIT_EXCEEDED", "message": "Please wait a moment before trying again." }`

### 4.2 `GET /api/health`
Lightweight health probe for cloud hosting uptime monitors.
* **Response (200 OK):** `{ "status": "healthy", "service": "aushadha-sathi-api" }`

---

## 5. Authentication & Security Architecture

* **Zero Authentication (Anonymous by Design):**  
  In compliance with DPDP Act 2023 §8(7) (Data Minimization), users are not required to provide telephone numbers, emails, passwords, or KYC.
* **Abuse Prevention & Rate Limiting:**
  * In-memory token bucket rate limiter (e.g., `slowapi` or `Flask-Limiter` using in-memory storage): Max **10 requests per minute per IP**.
  * Request payload hard cap: **10 MB maximum** to prevent memory buffer exhaustion attacks.
* **Transport Encryption:** Enforced HTTPS / TLS 1.3 across all client-server communications.

---

## 6. Third-Party Services & Integration Stack (100% Free / Open Source)

```
┌────────────────────────────────────────────────────────────────────────┐
│ THIRD-PARTY INTEGRATION CHOICES (FREE & OPEN SOURCE)                   │
├────────────────────────────────────────────────────────────────────────┤
│ • Vision & OCR Extraction: Google Gemini API Free Tier (Flash)         │
│ • Offline Fallback OCR: Tesseract.js / Python Tesseract (Open Source)  │
│ • Text-to-Speech (TTS): Browser-native Web Speech API (Free & Offline) │
│ • Caregiver Messaging: WhatsApp URL Protocol (wa.me) (Zero Cost)       │
│ • Maps & Geolocation: EXCLUDED / Out of Scope                          │
│ • Cloud Hosting: Render Free Web Service / Cloudflare Pages (Free)     │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Multimodal Vision & OCR Engine:**
   * **Primary:** Google Gemini 1.5 / 2.0 Flash API (Free Tier: 15 Requests Per Minute, 1 million tokens/minute, zero credit card requirement for developer tier).
   * **Open-Source Local Fallback:** Tesseract OCR (`pytesseract`) configured with the Indian English medical wordlist for offline or low-connectivity environments.
2. **Text-to-Speech (TTS):**
   * **Implementation:** Client-side Web Speech API (`window.speechSynthesis`).
   * **Cost:** **$0.00** (runs directly on device hardware).
   * **Language Support:** `kn-IN` (Kannada India) and `en-IN` (Indian English).
3. **Caregiver / Pharmacist Messaging:**
   * **Implementation:** Standard WhatsApp Web / Mobile URL protocol (`https://wa.me/?text=<encoded_payload>`) and Web Share API (`navigator.share`).
   * **Cost:** **$0.00** (bypasses expensive Twilio/Meta WhatsApp Business API message fees; opens directly in the user's personal WhatsApp app).
4. **Maps / Geolocation:**
   * **Status:** **Explicitly Excluded.** Locating pharmacies is out of scope and introduces unwanted location tracking under DPDP Act.

---

## 7. Deterministic Code vs. AI Model Boundary

To guarantee medical safety and prevent hallucinations, system responsibilities are rigorously segregated:

| Pipeline Stage | Implementation Mechanism | Component Classification |
|---|---|---|
| **Image Preprocessing** | Contrast enhancement, grayscale conversion, and downscaling via Python `Pillow` | **100% Deterministic Code** |
| **Raw Character & Stroke Recognition** | Gemini Vision / Multimodal OCR Layer | **AI Model** |
| **Confidence Scoring & Ambiguity Gate** | Threshold evaluation (`confidence < 0.85` triggers Amber Alert) | **100% Deterministic Code** |
| **Indian Shorthand Parser** | Regex tokenization (`1-0-1`, `OD`, `BD`, `TDS`, `AC`, `PC`, `SOS`) | **100% Deterministic Code** |
| **Schedule Slot Assignment** | Mathematical assignment to Morning, Afternoon, Night bins | **100% Deterministic Code** |
| **Linguistic Simplification** | Static bilingual medical dictionary mapping (e.g. `PC` $\rightarrow$ *"ಊಟದ ನಂತರ"*) | **100% Deterministic Code** |
| **Statutory Safety Warnings** | Immutable hardcoded legal disclaimers and amber UI cards | **100% Deterministic Code** |
| **WhatsApp Message Formatting** | String concatenation and URL encoding template | **100% Deterministic Code** |
| **Audio Voice Synthesis** | Browser hardware speech synthesizer | **Native System Code** |

> **Crucial Rule:** An AI model is used *only* for optical feature transcription. **All timing calculations, slot assignments, ambiguity alerts, and legal safety disclaimers are governed by 100% deterministic code.**

---

## 8. Hosting & Environment Configuration

### 8.1 Hosting Setup
* **Backend API:** Render Free Web Service (Docker / Python runtime) or Hugging Face Spaces.
* **Frontend:** Embedded within the Flask static distribution or deployed to Cloudflare Pages / Vercel Free Tier.

### 8.2 Environment Variables (`.env.example`)

```ini
# ==============================================================================
# Aushadha Sathi - Environment Configuration
# ==============================================================================

# Server Configuration
PORT=5000
ENVIRONMENT=production
DEBUG=False

# AI Vision & OCR Provider (Google Gemini Free Tier)
# Get a free key at https://aistudio.google.com/
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash

# Safety & Optical Confidence Thresholds
# Any extraction confidence below this triggers is_ambiguous=True
CONFIDENCE_THRESHOLD=0.85

# Rate Limiting (In-Memory IP Limiter)
RATE_LIMIT_PER_MINUTE=10

# Security & CORS
ALLOWED_ORIGINS=https://reportsaathi.onrender.com,http://localhost:5000
MAX_CONTENT_LENGTH_MB=10
```

---

## 9. Open Questions (Unresolved Technical & Operational Items)

*In compliance with prompt instructions ("List any open questions instead of guessing the answers"):*

1. **Web Speech API Kannada Voice Availability Across Android ROMs:**
   * *The Issue:* While Google Pixel, Motorola, and Samsung devices typically ship with the Google TTS engine (which supports `kn-IN`), certain heavily stripped budget devices (e.g., ultra-low-cost Transsion/Itel devices) omit Indic voice packs by default.
   * *Investigation Needed:* We must empirically test whether `window.speechSynthesis` triggers an automatic voice download prompt or silently fails on low-end MediaTek budget devices, and define an accessible fallback audio approach.
2. **Gemini Free Tier Concurrency & Rate Limit Behavior:**
   * *The Issue:* The free tier of Gemini Flash allows 15 Requests Per Minute (RPM). If multiple clinic patients test the app simultaneously, will the backend queue requests gracefully, or should an in-memory queue delay requests to prevent 429 errors?
3. **Medical Abbreviations in Ayush / Traditional Prescriptions:**
   * *The Issue:* In Karnataka, outpatient prescriptions often combine Allopathic medicines with Ayurvedic or Homeopathic tonics (e.g., *Kashayam*, *Asava*).
   * *Investigation Needed:* Are these dosage formats (e.g., *"15ml with warm water twice daily"*) parsed accurately by standard allopathic regex rules, or do they require specialized botanical dosage tokens?
