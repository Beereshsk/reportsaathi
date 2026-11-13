# Product Requirements Document (PRD): Aushadha Sathi

**Document Reference:** `docs/05-prd.md`  
**Dependencies:** [`docs/01-problem.md`](file:///c:/Users/beere/reportsaathi/docs/01-problem.md), [`docs/02-research.md`](file:///c:/Users/beere/reportsaathi/docs/02-research.md), [`docs/03-scope.md`](file:///c:/Users/beere/reportsaathi/docs/03-scope.md), and [`docs/04-design.md`](file:///c:/Users/beere/reportsaathi/docs/04-design.md)  
**Product Version:** MVP (Phase 1.0)  
**Target Market:** India (Karnataka pilot with Kannada & Indian English)

---

## 1. Product Overview & Strategic Goals

*Aushadha Sathi* is an accessible, bilingual, mobile-web prescription comprehension assistant designed to help elderly patients, low-literacy individuals, and family caregivers decode handwritten and printed medical prescriptions into clear, visual, and spoken daily schedules without guessing.

### 1.1 Product Goals
* **G-1 (Comprehension Speed):** Enable an elderly patient or non-medical caregiver to understand *which medicine to take, at what time (Morning/Afternoon/Night), and relative to meals (Before/After Food)* in **less than 30 seconds**.
* **G-2 (Zero Hallucination Policy):** Never guess unreadable cursive handwriting. If visual confidence is below standard thresholds, immediately flag the text for human pharmacist verification.
* **G-3 (Vernacular Accessibility):** Provide full native-language parity in Kannada (`ಕನ್ನಡ`) and Indian English, supported by browser-native spoken audio (Text-to-Speech).
* **G-4 (Zero Caregiver Barrier):** Enable 1-tap sharing of the visual schedule and pharmacist verification queries over WhatsApp without requiring account logins or app installation.
* **G-5 (Privacy by Design):** Adhere strictly to India's Digital Personal Data Protection Act (DPDP Act, 2023) by enforcing **100% ephemeral in-memory processing** with zero persistent storage of medical images or patient records.

### 1.2 Non-Goals (Explicit Product Boundaries)
* **NG-1 (No Autonomous Diagnosis):** The product will *never* diagnose illnesses, correlate symptoms, or predict medical conditions.
* **NG-2 (No Prescription Alteration):** The product will *never* recalculate doses, alter frequencies, titrate medications, or recommend stopping a drug.
* **NG-3 (No Drug Substitution or Commercial Commerce):** The product will *never* recommend generic alternatives, suggest substitute brands, sell medicines, or integrate with e-pharmacy shopping carts.
* **NG-4 (No Clinical Decision Support System / CDSS):** The product will *never* act as a diagnostic clinical interaction checker (avoiding Class B/C CDSCO SaMD classification).
* **NG-5 (No User Accounts or Persistent Health Locker):** The product will *not* provide user registration, passwords, health history tracking, or EHR storage in MVP.

---

## 2. User Personas & User Stories

### 2.1 Personas
1. **Basavaraj (68, Retired Teacher, Hubballi, Karnataka):** Suffers from hypertension and early cataracts. Speaks and reads Kannada; struggles with small cursive English letters on doctor slips; relies on neighbor chemist's fading pencil marks.
2. **Kavitha (34, Software Engineer, Bengaluru):** Basavaraj’s daughter living 400 km away. Manages her father's health remotely over phone calls. Needs a clear, verified WhatsApp summary of what the clinic doctor prescribed.
3. **Manjula (55, Homemaker, Mysuru):** Low formal medical literacy. Prefers listening to spoken voice instructions in Kannada rather than reading dense text on a budget Android phone.

### 2.2 User Stories
* **US-01 (Photo Input):** *As an elderly patient with trembling hands, I want to capture a photo of my prescription slip with one large button so that I don't have to struggle typing medical names.*
* **US-02 (Manual Text Fallback):** *As a caregiver who already deciphered the doctor's handwriting on the phone, I want to type or paste the text notes directly so that I can generate a clean visual schedule for my mother.*
* **US-03 (Visual Timing Schedule):** *As a patient with poor eyesight, I want to see clear Sun (☀️) and Moon (🌙) symbols showing whether a pill is for morning, afternoon, or night so that I never take a sedative in the morning.*
* **US-04 (Meal Relation Clarity):** *As a chronic diabetes patient, I want to see prominent "Before Food" or "After Food" badges in Kannada so that I don't suffer gastric irritation or hypoglycemia.*
* **US-05 (Audio Read-Aloud):** *As a low-vision senior, I want to tap one large speaker button to hear my medicine schedule read aloud in spoken Kannada so that I can take my medicines independently.*
* **US-06 (Ambiguity / Safety Flag):** *As a cautious caregiver, I want the app to highlight blurry or unreadable medicine names in amber and advise pharmacist verification so that my father never consumes a misread drug.*
* **US-07 (Caregiver WhatsApp Share):** *As an adult child, I want to share the formatted medicine schedule directly to our family WhatsApp group in one tap so that everyone coordinates my parents' care.*
* **US-08 (No-Login Privacy):** *As a privacy-conscious patient, I want to use this service without entering my phone number, Aadhaar, or email so that my medical data is never sold or leaked.*

---

## 3. Numbered Functional Requirements

```
┌────────────────────────────────────────────────────────────────────────┐
│ FUNCTIONAL REQUIREMENT MODULES                                         │
├────────────────────────────────────────────────────────────────────────┤
│ Module 1: Ingestion & Input Handling             (FR-01 to FR-04)     │
│ Module 2: Extraction & Indian Shorthand Engine   (FR-05 to FR-08)     │
│ Module 3: Ambiguity Flagging & Safety Checks     (FR-09 to FR-11)     │
│ Module 4: Bilingual Schedule Cards & UI          (FR-12 to FR-15)     │
│ Module 5: Spoken Audio Accessibility (TTS)       (FR-16 to FR-18)     │
│ Module 6: WhatsApp Caregiver & Chemist Loop      (FR-19 to FR-21)     │
│ Module 7: Ephemeral Privacy & Session Management (FR-22 to FR-24)     │
└────────────────────────────────────────────────────────────────────────┘
```

### Module 1: Ingestion & Input Handling
* **FR-01 (Camera Capture):** The system shall invoke the native device camera using `<input type="file" accept="image/*" capture="environment">` with a minimum touch target button of $56 \times 56\text{px}$.
* **FR-02 (Gallery Upload):** The system shall allow uploading image files (JPEG, PNG, WebP) up to $10\text{MB}$.
* **FR-03 (Manual Text Fallback):** The system shall provide an accessible multi-line text input field pre-filled with helpful placeholder examples (*"e.g., Paracetamol 650, 1 tablet morning and night after food for 5 days"*).
* **FR-04 (Client-Side Compression):** The system shall downscale client images exceeding $1920\text{px}$ on the longest edge to optimize upload performance on slow 2G/3G networks prior to transmission.

### Module 2: Extraction & Indian Shorthand Engine
* **FR-05 (Multimodal OCR & Vision Parsing):** The system shall process prescription images or text to extract: (a) Medicine Name, (b) Dosage/Strength, (c) Frequency, (d) Meal relationship, and (e) Course duration.
* **FR-06 (Indian Clinical Shorthand Mapping):** The deterministic parsing engine shall map standard Indian medical shorthand into structured slots:
  * `1-0-1` or `BD` $\rightarrow$ Morning: 1, Afternoon: 0, Night: 1
  * `1-1-1` or `TDS` $\rightarrow$ Morning: 1, Afternoon: 1, Night: 1
  * `1-0-0` or `OD` (Morning) $\rightarrow$ Morning: 1, Afternoon: 0, Night: 0
  * `0-0-1` or `HS` $\rightarrow$ Morning: 0, Afternoon: 0, Night: 1
  * `SOS` $\rightarrow$ Take only when needed / as required
* **FR-07 (Meal Timing Mapping):** The engine shall map:
  * `AC` / `BBF` / "Before Food" $\rightarrow$ *ಉಪಹಾರ/ಊಟಕ್ಕೆ ಮುನ್ನ (Before Food)*
  * `PC` / `AF` / "After Food" $\rightarrow$ *ಊಟದ ನಂತರ (After Food)*
* **FR-08 (Duration Extraction):** The engine shall extract duration strings (e.g., *"for 5 days"*, *"for 1 month"*) and standardize them into human-readable text.

### Module 3: Ambiguity Flagging & Safety Checks
* **FR-09 (Optical Confidence Threshold):** The extraction engine shall assign a confidence score ($0.0–1.0$) to each extracted medicine line. Any line with confidence $<0.85$ or containing unresolved handwriting scribbles shall be marked `is_ambiguous: true`.
* **FR-10 (Zero Guessing Rule):** The system shall *never* generate a probabilistic drug guess if a handwriting character stream is unreadable; it must preserve the raw legible characters and append an unverified indicator (e.g., *"Telma-40 (?)"*).
* **FR-11 (Amber Alert Presentation):** Any medicine card marked `is_ambiguous: true` must render with a prominent amber border (`#F59E0B`), an amber warning badge (`⚠️ ಅಸ್ಪಷ್ಟ ಕೈಬರಹ - ಔಷಧಿಕಾರರಲ್ಲಿ ಖಚಿತಪಡಿಸಿ`), and an explanation that the text requires physical pharmacist verification.

### Module 4: Bilingual Schedule Cards & UI
* **FR-12 (Card UI Representation):** Every identified medicine must be displayed in an independent card featuring: (a) Drug name and strength, (b) Medicine form (Tablet, Capsule, Syrup), (c) Visual ☀️ Morning / 🌤️ Afternoon / 🌙 Night grid, (d) Meal timing badge, and (e) Duration.
* **FR-13 (Bilingual Parity):** The UI must support seamless, 1-tap toggling between Kannada (`ಕನ್ನಡ`) and Indian English (`EN`), translating all instructional labels, food timings, and slot markers.
* **FR-14 (Large Text Toggle):** The UI shall feature an accessible *"Aa Large Text"* toggle that scales base typography from $16\text{px}$ to $20\text{px}$ and card headers to $24\text{px}$.
* **FR-15 (Mandatory Safety Warning):** The schedule view must render an un-dismissible safety banner: *"Please confirm all medicine details with your doctor or pharmacist before taking any medicine."*

### Module 5: Spoken Audio Accessibility (TTS)
* **FR-16 (Web Speech API Synthesis):** The application shall integrate the native browser SpeechSynthesis interface to synthesize spoken audio directly on the client device.
* **FR-17 (Kannada Voice Localization):** When language is Kannada, TTS must output speech using `lang="kn-IN"`; when English, it must use `lang="en-IN"`.
* **FR-18 (Audio Controls):** The audio player must provide simple 1-tap Play, Pause, and Restart controls with high-contrast visual indicators.

### Module 6: WhatsApp Caregiver & Chemist Loop
* **FR-19 (WhatsApp Share Payload):** The system shall format extracted medicine schedules into a structured plain-text message encoded for the WhatsApp Web/App Share API (`https://wa.me/?text=...`).
* **FR-20 (Flagged Chemist Query Formatting):** If any medicine was flagged as ambiguous, the WhatsApp message must prepend a dedicated verification block:
  * *"Chemist Anna / Doctor: Please verify Line [X] on this prescription slip. Our reader marked it as unclear."*
* **FR-21 (Clipboard Fallback):** If WhatsApp fails to launch, the system shall copy the formatted text to the user's clipboard and display a confirmation toast.

### Module 7: Ephemeral Privacy & Session Management
* **FR-22 (Zero Disk Persistence):** The backend shall process images entirely in RAM (memory streams) and never write prescription images or patient text to a persistent database or file system.
* **FR-23 (Session Purge on Navigation):** When the user taps *"Start Over"* or navigates away from the page, all active image buffers, object URLs, and speech utterances must be immediately revoked and deallocated.
* **FR-24 (No Tracking or PII Intake):** The system shall not capture, request, or store names, phone numbers, email addresses, IP logs, or GPS coordinates.

---

## 4. Non-Functional Requirements (NFRs)

* **NFR-01 (Performance & Latency):**
  * Client page load under $1.5\text{s}$ on standard 4G; under $3\text{s}$ on 3G mobile connections.
  * Total end-to-end extraction latency (from photo submission to card rendering) must not exceed $4.5\text{s}$.
  * Audio synthesis initiation within $<500\text{ms}$ upon tapping the Play button.
* **NFR-02 (Bundle Size & Budget Hardware Optimization):**
  * Total initial JavaScript bundle size must not exceed $180\text{KB}$ (gzipped) to ensure fast initialization on budget Android phones with 2GB RAM.
  * DOM tree depth must remain under 12 levels to avoid UI stutter on budget GPU chipsets.
* **NFR-03 (Accessibility & Contrast):**
  * Full compliance with WCAG 2.1 Level AAA for text contrast ($\ge 7:1$ contrast ratio for all essential informational text).
  * Minimum touch target size of $56 \times 56\text{px}$ with $\ge 12\text{px}$ separation between adjacent buttons.
  * Zero CSS text truncation (`text-overflow: ellipsis` is strictly barred on medicine names and dosages).
* **NFR-04 (Linguistic Typographic Integrity):**
  * All Indic (Kannada) typography must enforce line-heights between $1.65$ and $1.8$ to prevent clipping of vowel matras and subscript consonant conjuncts (*ottakshara*).
* **NFR-05 (Security & DPDP Compliance):**
  * End-to-end transport encryption over TLS 1.3 (HTTPS only).
  * Strict Content Security Policy (CSP) preventing third-party script injection or unauthorized data exfiltration.

---

## 5. Safety & Regulatory Requirements

* **SR-01 (CDSCO SaMD Exemption Compliance):** The product must maintain its legal status as an **informational transcription reading aid** under CDSCO Medical Device Software Guidelines 2026 by strictly abstaining from any diagnostic, prognostic, or therapeutic recommendations.
* **SR-02 (NMC Compliance):** The product shall prominently display that only a Registered Medical Practitioner (RMP) can prescribe or alter treatments.
* **SR-03 (Drugs & Cosmetics Act Compliance):** The product shall not recommend or facilitate the dispensing of Schedule H, H1, or X drugs without a physical prescription.
* **SR-04 (Look-Alike Sound-Alike Protection):** If an extracted text token has multiple valid drug interpretations with differing therapeutic classes, it must be flagged for pharmacist review.

---

## 6. Success Metrics & Quantifiable KPIs

| Metric Category | KPI | Target Metric | Measurement Method |
|---|---|---|---|
| **Usability** | Time to Schedule Comprehension | $\le 30$ seconds | Task completion in elderly user testing sessions |
| **Accessibility** | Audio Playback Rate | $\ge 55\%$ of sessions | Anonymous client-side interaction events |
| **Safety** | False-Certainty Hallucination Rate | **$0.0\%$** on ambiguous text | Clinical audit of 500 test prescription scans |
| **Verification Loop** | WhatsApp Share Action Rate | $\ge 35\%$ of sessions | Tap events on the WhatsApp verification button |
| **Performance** | Core Flow Completion Rate | $\ge 85\%$ | Ratio of submitted prescriptions reaching Schedule view |
| **Privacy Compliance** | Data Leakage / Retention Audits | **0 bytes** stored on disk | Automated CI/CD backend memory & disk audits |
