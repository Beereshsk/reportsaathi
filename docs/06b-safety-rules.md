# Medical Safety Rules & Clinical Guardrails: Aushadha Sathi

**Document Reference:** `docs/06b-safety-rules.md`  
**Dependencies:** [`docs/01-problem.md`](file:///c:/Users/beere/reportsaathi/docs/01-problem.md) through [`docs/06-architecture.md`](file:///c:/Users/beere/reportsaathi/docs/06-architecture.md)  
**Regulatory Alignment:** CDSCO Medical Device Software Guidelines 2026, NMC Telemedicine Guidelines 2020, Drugs and Cosmetics Act 1940, DPDP Act 2023.

---

## 1. Core Safety Philosophy & Absolute Non-Negotiables

*Aushadha Sathi* operates under a single governing clinical maxim:

> **"A false reading in healthcare is an adverse drug event. Optical certainty must always take precedence over AI helpfulness. When a human doctor's handwriting is unreadable, the safest output is an honest admission of unreadability."**

```
┌────────────────────────────────────────────────────────────────────────┐
│ THE THREE NON-NEGOTIABLE SAFETY LAWS                                   │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Zero Probabilistic Guessing on Illegible Cursive.                  │
│ 2. Zero Autonomous Clinical Diagnosis or Therapeutic Alteration.       │
│ 3. Instant Flagging of Ambiguity for Human Pharmacist Verification.   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Ambiguity & Optical Confidence Rules

### Rule 2.1: Numerical Confidence Threshold
* The extraction pipeline must evaluate an optical confidence score ($0.00$ to $1.00$) for every extracted line item.
* **The Threshold:** If the confidence score for a medicine name, dosage, or frequency is **less than $0.85$ ($85\%$)**, the engine must automatically flag the entry as `is_ambiguous = true`.

### Rule 2.2: The "Two-Stroke" Illegibility Boundary
* If two or more consecutive letters in a brand name cannot be confirmed by clear optical stroke features, the system is strictly prohibited from autocorrecting or completing the word.
* The extracted text must be rendered with an inline unverified question mark (e.g., *"Telma-40 (?)"*) and assigned an Amber Alert status.

### Rule 2.3: Visual Presentation of Ambiguity (Amber Alert)
* Whenever `is_ambiguous == true`:
  1. The medicine card must render with a high-visibility amber border (`#F59E0B`, $2\text{px}$ solid).
  2. The card must display an explicit amber badge in Kannada and English:
     * *Kannada:* `⚠️ ಅಸ್ಪಷ್ಟ ಕೈಬರಹ - ಔಷಧಿಕಾರರಲ್ಲಿ ಖಚಿತಪಡಿಸಿ`
     * *English:* `⚠️ Unclear Handwriting - Confirm with Pharmacist`
  3. The TTS audio synthesis must preface the reading with: *"ದಯವಿಟ್ಟು ಗಮನಿಸಿ, ಈ ಔಷಧದ ಹೆಸರು ಸಂಪೂರ್ಣ ಸ್ಪಷ್ಟವಾಗಿಲ್ಲ. ನಿಮ್ಮ ಔಷಧಿಕಾರರಲ್ಲಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ."* (*"Please note, this medicine name is not completely clear. Confirm with your pharmacist."*).

---

## 3. Look-Alike Sound-Alike (LASA) Drug Safeguards

Look-Alike Sound-Alike (LASA) errors represent the most frequent cause of catastrophic medication mistakes in retail pharmacy dispensing.

```
┌────────────────────────────────────────────────────────────────────────┐
│ FREQUENT INDIAN CLINICAL LASA PAIRS & HAZARDS                          │
├────────────────────────────────────────────────────────────────────────┤
│ • Telmisartan (BP)           vs.   Tolol / Metoprolol (Heart Rate)     │
│ • Metformin (Diabetes)       vs.   Metoprolol (Beta-Blocker)           │
│ • Lasix (Diuretic)           vs.   Losec (Proton Pump Inhibitor)       │
│ • Amoxil (Antibiotic)        vs.   Amiodarone (Anti-arrhythmic)        │
│ • Plavix (Blood Thinner)     vs.   Paxil (Antidepressant)              │
└────────────────────────────────────────────────────────────────────────┘
```

### Rule 3.1: Levenshtein Distance Collision Check
* The extraction engine must maintain an internal dictionary of verified Indian allopathic drug brands.
* If extracted OCR text matches two distinct therapeutic drug classes within a Levenshtein edit distance of $\le 2$ (e.g., *Losec* vs *Lasix*), **the system must never autonomously pick the higher-probability candidate**.
* **Action Required:** Both possible interpretations must be highlighted, and the card must be locked with a pharmacist verification requirement.

---

## 4. Clinical Dosage Bound Sanity Rules

The system includes deterministic clinical boundary filters to catch extreme prescription errors or transcription anomalies:

| Parameter | Normal Range Limit | Safety Action if Exceeded |
|---|---|---|
| **Daily Tablet Frequency** | 1 to 4 doses per day (`1-0-1`, `1-1-1-1`) | If extracted frequency $>4$ times daily, flag as `POSSIBLE_OVERDOSE_RISK` and mark for urgent verification. |
| **Single Dose Quantity** | 0.5 to 2 tablets/capsules | If single dose $>2$ units (e.g. "Take 5 tablets"), flag as `UNUSUAL_DOSE_VOLUME`. |
| **Paracetamol Single Dose** | Max 1000 mg per dose | If Paracetamol dosage exceeds 1000 mg, trigger an immediate warning flag. |
| **Course Duration** | 1 to 90 days | If duration $>90$ days on acute antibiotics/NSAIDs, highlight for duration confirmation. |

---

## 5. Non-Diagnostic Regulatory Guardrails (CDSCO & NMC Compliance)

To guarantee that *Aushadha Sathi* remains exempt from medical device licensing under CDSCO Guidelines (CDSCO/MD/GD/MDSW/01/2026) and complies with the National Medical Commission (NMC):

### Rule 5.1: Prohibition of Diagnostic Inferences
* The application must **never** extrapolate, display, or speculate on the underlying medical disease, condition, or prognosis from a prescription.
  * *Permitted:* Displaying *"Paracetamol 650mg: 1 tablet after food"*
  * *Strictly Barred:* Adding *"Prescribed for suspected Dengue Fever or Viral Infection"*

### Rule 5.2: Prohibition of Drug Substitution & Generic Switching
* The system shall never propose generic equivalents, cheaper alternatives, or brand substitutes, regardless of price variance. This prevents commercial conflicts of interest and complies with the Drugs & Cosmetics Act 1940.

### Rule 5.3: Mandatory Statutory Disclaimer Presentation
* The statutory safety disclaimer must appear:
  1. On the landing screen below the action cards.
  2. Permanently pinned at the top of the Schedule Results view.
  3. Inside the pre-formatted WhatsApp share message.
* **Exact Phrasing (Bilingual):**
  * *English:* **"Please confirm all medicine details with your doctor or pharmacist before taking any medicine. This tool helps you read instructions—it does not provide medical advice or diagnosis."**
  * *Kannada:* **"ಯಾವುದೇ ಔಷಧ ಸೇವಿಸುವ ಮುನ್ನ ವಿವರಗಳನ್ನು ನಿಮ್ಮ ವೈದ್ಯರು ಅಥವಾ ಔಷಧಿಕಾರರೊಂದಿಗೆ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ. ಇದು ಓದಲು ಮಾತ್ರ ಸಹಾಯ ಮಾಡುತ್ತದೆ—ವೈದ್ಯಕೀಯ ಸಲಹೆಯಲ್ಲ."**

---

## 6. Acute Emergency Symptoms Escalation Protocol

If an uploaded prescription, emergency triage slip, or manual text entry contains explicit acute red-flag terminology:

```
┌────────────────────────────────────────────────────────────────────────┐
│ ACUTE EMERGENCY RED FLAGS (IMMEDIATE ESCALATION)                       │
├────────────────────────────────────────────────────────────────────────┤
│ • Crushing chest pain / suspected Myocardial Infarction                │
│ • Unilateral facial droop, slurred speech, sudden weakness (Stroke)    │
│ • Profuse uncontained bleeding or severe head trauma                   │
│ • Anaphylaxis / severe airway swelling / acute stridor                 │
└────────────────────────────────────────────────────────────────────────┘
```

* **Immediate Protocol Action:**
  1. Display a full-screen red emergency modal.
  2. Display national emergency contact links: **"Call 108 (National Ambulance Helpline)"**.
  3. Advice message: *"This appears to be an acute emergency situation. Do not wait to read instructions online—proceed immediately to the nearest hospital casualty / emergency department."*

---

## 7. Ephemeral Data Purge & DPDP Act Compliance Rules

Under Section 8(7) of India’s Digital Personal Data Protection Act, 2023, data fiduciaries must erase personal data once the specified purpose is fulfilled.

* **Rule 7.1 (RAM-Only Stream Ingestion):** Uploaded images must be processed exclusively in volatile memory buffers (`io.BytesIO`). No temporary image files may be written to disk (`/tmp` or local directories).
* **Rule 7.2 (Zero-Log PII Policy):** Server access logs (Nginx/Gunicorn) must be configured to exclude request bodies, filenames, and extracted medicine text.
* **Rule 7.3 (Client Object URL Revocation):** When a user taps *"Start Over"* or navigates away, `URL.revokeObjectURL()` must be called immediately to wipe the preview image from browser cache.
* **Rule 7.4 (Zero Model Training):** Third-party AI vision APIs (Gemini Flash Developer Tier) must have zero-data-retention or non-training flags enabled where available, ensuring user prescriptions are never used for AI model re-training.
