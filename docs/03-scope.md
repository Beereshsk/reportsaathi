# Scope & Product Boundary: Aushadha Sathi

**Document Reference:** `docs/03-scope.md`  
**Dependencies:** [`docs/01-problem.md`](file:///c:/Users/beere/reportsaathi/docs/01-problem.md) & [`docs/02-research.md`](file:///c:/Users/beere/reportsaathi/docs/02-research.md)  
**Objective:** Define the single core flow that delivers maximum user value, break it into features and sub-features, and categorize them ruthlessly into **MVP**, **Later**, and **Never** with explicit clinical, legal, and operational justifications.

---

## 1. The Single Core Flow

The primary failure of existing health solutions identified in `docs/02-research.md` is that they either push commerce (e-pharmacies), induce panic (symptom checkers), or hallucinate unverified drug names (generic AI chatbots).

*Aushadha Sathi* succeeds by solving one specific friction point: **turning an unreadable prescription into a clear, spoken, and visual schedule in the user's native language without guessing.**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ THE SINGLE CORE FLOW                                                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   [Capture / Upload / Type]                                                     │
│              │                                                                  │
│              ▼                                                                  │
│   [Safety-First Extraction & Ambiguity Flagging]                                │
│   • Extracts clear text                                                         │
│   • Marks unreadable text as "Unclear — Ask Pharmacist" (Amber alert)          │
│              │                                                                  │
│              ▼                                                                  │
│   [Bilingual Visual Schedule Cards]                                             │
│   • Large typography, high contrast (min 56px buttons)                          │
│   • Sun/Moon icons for Morning, Afternoon, Night                                │
│   • Meal relationship (Before / After Food) in Kannada & English               │
│              │                                                                  │
│              ▼                                                                  │
│   [Accessibility & Verification Action]                                         │
│   • One-tap Web Speech API read-aloud (Kannada / English)                       │
│   • One-tap WhatsApp share to family caregiver or local chemist                 │
│              │                                                                  │
│              ▼                                                                  │
│   [Ephemeral Session Termination]                                               │
│   • Data purged from memory; zero persistent storage                            │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Feature & Sub-Feature Decomposition

```
Aushadha Sathi
├── 1. Ingestion & Input Handling
│   ├── 1.1 Mobile camera capture
│   ├── 1.2 Image file upload (JPEG/PNG/WebP)
│   ├── 1.3 Manual text & notes fallback
│   └── 1.4 Client-side image preview & downscaling
├── 2. Extraction & Ambiguity Engine
│   ├── 2.1 Multimodal text extraction
│   ├── 2.2 Indian dosage shorthand parsing (1-0-1, OD, BD, TDS, AC, PC)
│   ├── 2.3 Confidence scoring & ambiguity detection
│   └── 2.4 Ephemeral stateless processing pipeline
├── 3. Vernacular Translation & Simplification
│   ├── 3.1 Kannada & Indian English localization
│   ├── 3.2 Medical jargon simplification
│   └── 3.3 One-tap language toggle
├── 4. Accessible Visual Schedule Interface
│   ├── 4.1 Card-based medicine layout
│   ├── 4.2 Visual time-of-day iconography (Sun / Half-sun / Moon)
│   ├── 4.3 Meal timing indicators (Before / After Food)
│   ├── 4.4 Large font toggle & accessible touch targets (≥56px)
│   └── 4.5 Mandatory non-diagnostic safety banner
├── 5. Voice & Audio Engine (TTS)
│   ├── 5.1 Web Speech API voice synthesis
│   ├── 5.2 Kannada native speech (`kn-IN`)
│   └── 5.3 Indian English speech (`en-IN`)
└── 6. Caregiver & Pharmacist Verification Loop
    ├── 6.1 WhatsApp Share API integration
    ├── 6.2 Pre-formatted family summary text
    └── 6.3 Pre-formatted pharmacist clarification query
```

---

## 3. Scope Categorization: MVP, Later, and Never

### 3.1 MVP (Minimum Viable Product)
*Only features indispensable to completing the core flow safely, clearly, and legally.*

| Feature | Sub-Features | Inclusion Rationale |
|---|---|---|
| **1. Ingestion** | Camera capture, photo upload, manual text fallback | Accommodates physical paper slips, saved photos sent by relatives, or manual typing if a camera is unavailable. |
| **2. Extraction & Ambiguity Flagging** | Multimodal OCR + Indian notation parser (`1-0-1`, `OD`, `BD`, `TDS`, `AC`, `PC`); confidence scoring | Solves the core unreadability problem. **Ambiguity flagging is mandatory for safety:** if a word is blurry or ambiguous, it *must* be highlighted in amber rather than guessed. |
| **3. Vernacular Schedule Cards** | Individual medicine cards; Kannada + English; visual Sun/Moon and Meal icons | Eliminates reliance on English jargon. Visual icons allow illiterate or low-vision seniors to immediately understand *when* to take each tablet. |
| **4. Spoken Audio (TTS)** | Native Web Speech API integration in Kannada (`kn-IN`) and English (`en-IN`) | Essential for elderly patients with deteriorating eyesight or low literacy who cannot read screen text. |
| **5. WhatsApp Verification Share** | Pre-formatted message to WhatsApp with structured schedule & flagged questions | Enables adult children in distant cities to verify the schedule or allows patients to send an instant verification question to their local retail chemist. |
| **6. Ephemeral Privacy by Design** | In-memory processing; zero persistent database storage of images or medical text | Guarantees compliance with Section 8(7) of India's DPDP Act 2023 without expensive security/EHR infrastructure. |
| **7. Mandatory Safety Disclaimer** | Static, prominent warning: *"Please confirm all medicine details with your doctor or pharmacist before taking any medicine."* | Legal prerequisite under CDSCO and Consumer Protection regulations to maintain status as an informational reading aid. |

---

### 3.2 Challenged & Removed from MVP (Moved to "Later" or Dropped)
*In strict accordance with the instruction to "challenge anything in the MVP that the core flow can work without":*

1. **CHALLENGED: "Common Side Effects & Precautions Database" (Originally in `docs/01-problem.md` §3, Feature 3)**
   * *Challenge:* Does an elderly patient need a list of 15 theoretical side effects to know to take their BP tablet after breakfast? No.
   * *Risk:* Research in `docs/02-research.md` proved that listing side effects induces catastrophizing and causes patients to stop taking life-saving chronic medications (Pattern 5: Medical Alarmism). Furthermore, maintaining a verified Indian drug side-effect database creates severe clinical liability.
   * *Decision:* **REMOVED FROM MVP ➔ MOVED TO LATER (Restricted strictly to standard packaging precautions like "Take with plenty of water").**
2. **CHALLENGED: "Medicine Pronunciation Guide" (Originally in `docs/01-problem.md` §3, Feature 3)**
   * *Challenge:* A dedicated phonetic guide widget adds UI complexity. The core TTS engine already speaks the name aloud in the chosen language.
   * *Decision:* **REMOVED FROM MVP ➔ DROPPED.**
3. **CHALLENGED: User Accounts, Authentication & Saved Profiles**
   * *Challenge:* Does a patient need to sign up, create a password, or verify an OTP to understand their prescription? No.
   * *Decision:* **REMOVED FROM MVP ➔ DROPPED.** A no-login, stateless tool eliminates onboarding friction and perfectly satisfies the DPDP Act's data minimization mandates.
4. **CHALLENGED: Multi-Page Document Ingestion**
   * *Challenge:* Single-page prescription slips account for >85% of outpatient visits in India. Handling multi-page PDF stitching adds OCR overhead without proving core value.
   * *Decision:* **REMOVED FROM MVP ➔ MOVED TO LATER.**

---

### 3.3 Later (Post-MVP Roadmap)
*Valuable extensions that enhance utility but are not required for the initial core flow.*

| Feature | Target Phase | Rationale for Deferral |
|---|---|---|
| **WhatsApp Ingestion Bot** | Phase 2 | Allowing users to message a WhatsApp Business bot directly eliminates app installation friction, but requires Twilio/Meta Business API setup and recurring server costs. |
| **Additional Languages (Hindi, Tamil, Telugu, Marathi)** | Phase 2 | Kannada and English cover the initial testing demographic (Karnataka); expanding to more languages requires verified medical terminology dictionaries. |
| **Printed Hospital Discharge Parser** | Phase 2 | Hospital discharge summaries are multi-page documents requiring specialized table-extraction models (e.g., separating admission history from discharge medications). |
| **Offline Progressive Web App (PWA) Caching** | Phase 2 | Allows the visual cards and previously loaded audio to work in rural areas with spotty connectivity. |
| **Caregiver Medication Reminders (WhatsApp/Push Alarms)** | Phase 3 | Automated alarm notifications for elderly caregivers; requires persistent scheduling infrastructure and notification delivery services. |
| **Retail Chemist Sticker Label Print Mode** | Phase 3 | Generates printable 2"x1" vernacular adhesive labels that local pharmacists can stick onto blister packs, replacing faint pencil marks. |
| **ABDM / ABHA Digital Locker Integration** | Phase 4 | Connecting to India’s Ayushman Bharat Digital Mission (M1/M2 milestone) to pull verified e-prescriptions directly from government health records. |

---

### 3.4 Never (Strictly Prohibited & Out of Scope)
*Features that violate Indian medical laws (CDSCO, NMC, Drugs & Cosmetics Act, DPDP Act) or create unacceptable clinical risks.*

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ STRICTLY PROHIBITED (NEVER)                                                     │
├─────────────────────────────────────────────────────────────────────────────────┤
│ 1. Autonomous Clinical Diagnosis or Symptom Inference                           │
│ 2. Drug Substitution, Brand Switching or Generic Recommendations                │
│ 3. Dosage Recalculation, Titration or Discontinuation Advice                    │
│ 4. Clinical Drug-Drug Interaction / Contraindication Analysis (SaMD / CDSS)     │
│ 5. Direct E-Commerce Checkout / Pharmacy Affiliate Push                         │
│ 6. Unsupervised AI Guessing on Illegible Cursive Handwriting                   │
│ 7. Permanent Storage or Sale of Patient Medical Records                         │
└─────────────────────────────────────────────────────────────────────────────────┘
```

| Prohibited Feature | Statutory & Clinical Reason for Permanent Rejection |
|---|---|
| **1. Autonomous Clinical Diagnosis or Symptom Correlation** | **Violates NMC Regulations & CDSCO SaMD Rules.** Under Indian law, only a Registered Medical Practitioner (RMP) can diagnose illness. Software attempting diagnosis is classified as Class C/D SaMD and faces prosecution. |
| **2. Drug Substitution or Generic Brand Switching** | **Violates Drugs and Cosmetics Act, 1940.** Suggesting alternative brands or chemical equivalents without a doctor's explicit endorsement creates severe liability and commercial bias (identified in `docs/02-research.md` as Pattern 3). |
| **3. Dosage Recalculation or Titration Advice** | **Lethal Clinical Hazard.** The application must *never* suggest altering, increasing, or stopping a dose, even if a user reports side effects. |
| **4. Drug-Drug Interaction Checking (CDSS)** | **Triggers Regulated SaMD Class B/C Classification.** Automated contraindication checkers act as Clinical Decision Support Systems, requiring clinical trial data, CDSCO licensing, and certified quality management (ISO 13485). |
| **5. E-Commerce Checkout / Medicine Sales Integration** | **Destroys Healthcare Trust.** Blurring patient education with retail commerce recreates the exact spam and conflict of interest that patients despise in e-pharmacies. |
| **6. Unsupervised Probabilistic AI Guessing on Illegible Text** | **Lethal LASA Drug Risk.** If handwriting cannot be extracted with high optical certainty, the system must *never* guess. It must mark the field as unverified and demand human confirmation. |
| **7. Permanent Storage or Monetization of Patient Health Data** | **Violates DPDP Act 2023.** Storing unencrypted health records or selling user prescription history to insurers/pharmaceutical companies attracts penalties up to ₹250 Crore. |

---

## 4. MVP Traceability Matrix

This matrix verifies that every feature included in the MVP directly traces back to solving a problem identified in `docs/01-problem.md` while bypassing the user complaints analyzed in `docs/02-research.md`.

| MVP Feature | Solves Problem in `01-problem.md` | Bypasses Complaint in `02-research.md` | Success Metric |
|---|---|---|---|
| **Camera & Text Fallback** | Physical paper slip barrier (§3, F1) | App store rejections of paper slips | 100% of user prescriptions can be submitted |
| **Ambiguity Flagging (Amber alert)** | Misreading doctor handwriting (§3, F2) | AI hallucination on cursive text (Pattern 4) | 0% unverified guesses presented as clinical facts |
| **Vernacular Visual Cards** | Medical terms & small text (§3, F3) | English medical jargon exclusion (Pattern 2) | User understands morning/night timings in <30s |
| **Kannada / English Audio (TTS)** | Elderly deteriorating eyesight (§3, F4) | Missing audio accessibility in apps (Pattern 2) | 1-tap playback in under 2 seconds |
| **WhatsApp Verification Share** | Family coordination barrier (§3, F5) | Faded chemist pencil marks on blisters (Pattern 1) | Caregiver receives clean, formatted message in 1 tap |
| **Stateless Privacy by Design** | Patient data protection mandate (§5) | Data leaks & commercial spam (DPDP Act) | 0 bytes of patient data stored on disk |
| **Mandatory Safety Disclaimer** | Non-diagnostic regulatory boundary (§5) | Medical liability & illegal diagnosis claims | 100% compliance with CDSCO informational rules |

---

## 5. Scope Sign-Off Summary

* **What we are building:** A lightweight, bilingual, mobile-first prescription transcription and scheduling assistant that converts prescriptions into visual, spoken Kannada and English cards, highlights unreadable text for pharmacist verification, and purges all data after use.
* **What we are NOT building:** A diagnostic engine, a telemedicine platform, an online pharmacy, or an autonomous AI doctor.
