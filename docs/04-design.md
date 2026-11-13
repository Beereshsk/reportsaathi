# Design Specification: Aushadha Sathi

**Document Reference:** `docs/04-design.md`  
**Dependencies:** [`docs/01-problem.md`](file:///c:/Users/beere/reportsaathi/docs/01-problem.md), [`docs/02-research.md`](file:///c:/Users/beere/reportsaathi/docs/02-research.md), and [`docs/03-scope.md`](file:///c:/Users/beere/reportsaathi/docs/03-scope.md)  
**Target Hardware:** Low-cost Android smartphones (e.g., Redmi 9A/A1, Samsung Galaxy M04/A04; 720×1600 physical resolution, 360×800 CSS viewport, 2GB–3GB RAM, outdoor sunlight usage).  
**Target Demographics & Language:** Elderly patients, family caregivers, Kannada (`ಕನ್ನಡ`) and Indian English speakers.

---

## 1. Core Flow Screen Inventory & State Matrix

In alignment with [`docs/03-scope.md`](file:///c:/Users/beere/reportsaathi/docs/03-scope.md), the core user flow is strictly linear: **Home/Input ➔ Processing ➔ Visual Schedule ➔ Caregiver Verification**.

```
┌────────────────────────────────────────────────────────────────────────┐
│ CORE FLOW SCREENS & MODALS                                             │
├────────────────────────────────────────────────────────────────────────┤
│ Screen 1: Home / Ingestion Screen                                      │
│ Screen 2: Prescription Input & Manual Fallback Screen                  │
│ Screen 3: Processing & Safety Extraction Screen                        │
│ Screen 4: Visual Medication Schedule Screen (Kannada / English)        │
│ Screen 5: Caregiver & Pharmacist Verification Drawer (WhatsApp Share)  │
└────────────────────────────────────────────────────────────────────────┘
```

---

### Screen 1: Home / Ingestion Screen
The primary landing point where users select their preferred language and input method.

* **Default State:**
  * Top bar shows brand logo (`✳ ಔಷಧ ಸಾಥಿ`) with a high-contrast language toggle button (`ಕನ್ನಡ / EN`).
  * Headline: *"ಔಷಧದ ಚೀಟಿ ಸುಲಭವಾಗಿ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಿ"* (*"Understand medicine instructions simply"*).
  * Three large, vertical action cards with icons:
    1. **Take a Photo** (`📷 ಫೋಟೋ ತೆಗೆಯಿರಿ`)
    2. **Upload from Gallery** (`📁 ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ`)
    3. **Type It In** (`✍️ ಟೈಪ್ ಮಾಡಿ`)
  * Bottom safety badge: *"Private by design. Your prescription is never stored."*
  * Mandatory disclaimer: *"Notice: Not a diagnosis. Always confirm details with your doctor or pharmacist."*
* **Empty State:**
  * Clean, distraction-free view ready for immediate single-tap input; no historical list or login prompts.
* **Loading State:**
  * When opening the native camera feed: Action button shows a gentle pulse ring; touch interaction is temporarily debounced to prevent duplicate taps on low-RAM devices.
* **Error State:**
  * **Camera Permission Denied:** A polite alert card explains: *"Camera access is needed to photograph your prescription. You can enable it in phone settings or use 'Upload Image' instead."*

---

### Screen 2: Prescription Input & Manual Fallback Screen
Activated when the user selects manual text entry or uploads an image file for pre-extraction verification.

* **Default State:**
  * If Image Mode: Displays a clear image preview container with filename, file size, a *"Change image"* link, and a large primary button: *"Read My Prescription →"*.
  * If Text Mode: Clean, high-contrast `<textarea>` pre-populated with gentle placeholder instructions (*"For example: Paracetamol 650, 1 tablet morning and night after food for 5 days"*).
* **Empty State:**
  * Text area is blank with prominent focus ring ($3\text{px}$ forest green) upon tap; primary submission button is disabled with high contrast styling (`opacity: 0.5`).
* **Loading State:**
  * Image compression & client-side preview generation shows an inline spinner with label: *"Preparing image..."*.
* **Error State:**
  * **Unsupported File Format:** Red alert badge: *"Please select a photo in JPG or PNG format."*
  * **Blank Submission:** Toast banner: *"Please enter at least one medicine name or instruction before proceeding."*

---

### Screen 3: Processing & Safety Extraction Screen
The intermediary state while optical character recognition and clinical notation extraction execute.

* **Default State (Active Processing):**
  * Centered visual spinner with clinical calming pulse ring.
  * Primary status heading: *"ಚೀಟಿಯನ್ನು ಓದಲಾಗುತ್ತಿದೆ..."* (*"Reading prescription..."*).
  * Subtext: *"ವೈದ್ಯರ ಕೈಬರಹವನ್ನು ಎಚ್ಚರಿಕೆಯಿಂದ ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ. ಊಹೆ ಮಾಡದೆ ಕೇವಲ ಸ್ಪಷ್ಟವಿರುವ ವಿವರಗಳನ್ನು ಮಾತ್ರ ಪಟ್ಟಿ ಮಾಡಲಾಗುತ್ತಿದೆ."* (*"Examining doctor's handwriting carefully. Highlighting clear instructions without guessing."*).
  * Progressive step list with animated checkmarks:
    - [✓] Image clarity checked
    - [✓] Identifying medicine names
    - [⏳] Organizing morning and night timings...
* **Empty State:**
  * Not applicable (pure transitional state; auto-redirects on completion or failure).
* **Loading State:**
  * If processing exceeds 5 seconds (slow 3G / 4G connections): Updates subtext with reassuring notice: *"Handwriting is complex, taking a few extra seconds. Please keep this screen open."*
* **Error State:**
  * **Low Optical Quality / Blurry Photo:** Transitions to dedicated error screen (see `docs/references/04-error-screen.png`):
    - Red alert circle: `!`
    - Headline: *"ಫೋಟೋ ಸ್ಪಷ್ಟವಾಗಿಲ್ಲ (Photo is blurry)"*
    - Educational guidance box: *"Tips for a clear photo: 1. Place prescription under bright light. 2. Hold camera steady. 3. Avoid shadows."*
    - Single large action button: *"ಮತ್ತೆ ಫೋಟೋ ತೆಗೆಯಿರಿ (Retake Photo)"*.
  * **Network Timeout:** Reversible offline banner with a *"Try Again"* button; zero data lost from the input buffer.

---

### Screen 4: Visual Medication Schedule Screen
The primary outcome screen delivering the core value of the product.

* **Default State (Successful Extraction):**
  * Top bar shows badge count: *"2 medicines found"* + *"Aa Large Text"* toggle.
  * **Sticky / Prominent Audio Player Bar:** Deep green card (`#285F4C`) with speaker icon: *"🔊 ಸೂಚನೆಗಳನ್ನು ಕೇಳಿ (Listen to Instructions)"* with play/pause button.
  * **Individual Medicine Cards:**
    - Medicine Name in bold typography ($\ge 20\text{px}$).
    - Medicine form pill badge (e.g., *"ಮಾತ್ರೆ (Tablet)"*, *"ಸಿರಪ್ (Syrup)"*).
    - **Visual Timing Grid (3 Slots):**
      * ☀️ Morning slot (e.g., *"1 ಬೆಳಿಗ್ಗೆ"* - highlighted in green if active)
      * 🌤️ Afternoon slot (e.g., *"0 ಮಧ್ಯಾಹ್ನ"*)
      * 🌙 Night slot (e.g., *"1 ರಾತ್ರಿ"* - highlighted in green if active)
    - **Food Relationship Badge:** Plate & cutlery icon (`🍽️ ಊಟದ ನಂತರ (After Food) • 5 ದಿನಗಳು`).
  * **Ambiguity Warning State (Amber Alert):**
    - If handwriting confidence for a drug name or dose is $<85\%$, the card renders with an amber border (`#F59E0B`) and amber banner:
      * *"⚠️ ಅಸ್ಪಷ್ಟ ಕೈಬರಹ (Unclear Handwriting) - ಈ ಔಷಧದ ಹೆಸರು ಸಂಪೂರ್ಣ ಸ್ಪಷ್ಟವಾಗಿಲ್ಲ. ಔಷಧಿಕಾರರಲ್ಲಿ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ."* (*"Handwriting is not completely clear. Confirm with your pharmacist before taking."*)
  * Bottom sticky action bar:
    - Primary Button: *"💬 ವಾಟ್ಸಾಪ್‌ನಲ್ಲಿ ಹಂಚಿಕೊಳ್ಳಿ (Share to WhatsApp)"*
    - Secondary Button: *"ಮತ್ತೊಮ್ಮೆ ↗ (Start Over)"*
* **Empty State:**
  * If no medicines could be detected from the image: Friendly prompt: *"We couldn't detect medicine instructions on this paper. Would you like to type them in or retake the photo?"*
* **Loading State (Audio Synthesis):**
  * Audio bar shows a pulsing wave animation with label: *"ಧ್ವನಿ ಸಿದ್ಧವಾಗುತ್ತಿದೆ... (Preparing audio...)"*.
* **Error State:**
  * **Web Speech API Unavailable:** Audio bar gracefully hides or disables with helper text: *"Audio playback is not supported on this browser version."*

---

### Screen 5: Caregiver & Pharmacist Verification Drawer (WhatsApp Share)
Triggered when the user taps *"Share to WhatsApp"*.

* **Default State:**
  * Bottom sheet displaying a pre-formatted message preview:
    ```text
    ✳ Aushadha Sathi - Medicine Schedule Notes:
    1. Paracetamol 650mg: 1 Morning, 0 Afternoon, 1 Night (After Food, 5 Days)
    2. [ATTENTION NEEDED] Line 2: Telma-40 (?) - Unclear handwriting.

    Chemist anna / Doctor: Please verify Line 2 before dispensing.
    (Note: Please confirm all details with a licensed professional.)
    ```
  * Two one-tap target buttons:
    - *"Share with Family Caregiver"*
    - *"Ask Local Pharmacist for Verification"*
* **Empty State:**
  * If no medicines exist, share button remains disabled.
* **Loading State:**
  * System share sheet launch indicator.
* **Error State:**
  * **WhatsApp App Not Installed:** Fallback triggers standard Web Share API or copies formatted text to clipboard with toast: *"Copied to clipboard. Paste into your messaging app."*

---

## 2. Review of Attached References & Design Borrowings

| Reference Source | Key Characteristics | What to Borrow | What to Avoid |
|---|---|---|---|
| **Reference 1: Existing Aushadha Sathi Prototype** (`index.html` / `styles.css`) | Clean, calming paper-and-botanical aesthetic (`#f6f7f1`, `#285f4c`), step labels, bilingual toggle. | • Calm, glare-free background tone.<br>• Native Kannada/English language switcher.<br>• Large touch cards for camera/upload.<br>• Prominent safety disclaimers. | • Desktop-heavy hero illustration that pushes buttons below fold on 360px phones.<br>• Outputting unformatted raw text inside a generic `<textarea>` instead of structured dosage cards.<br>• Absence of amber visual alerts for ambiguous text. |
| **Reference 2: Indian E-Pharmacies** (*Tata 1mg, PharmEasy*) | Commercial mobile web interfaces with camera prescription upload buttons. | • Familiar bottom-sheet camera/gallery trigger.<br>• Common packaging nomenclature recognized by Indian patients (*strip, blister, tablet*). | • Cluttered screens packed with discount banners, countdown timers, and "Care Plan" upsells.<br>• Aggressive tele-doctor consultation popups.<br>• Cart checkout pressure that distracts elderly users. |
| **Reference 3: Clinical Triage Apps** (*Ada Health*) | Conversational, structured assessment with strong typography and white space. | • Progressive disclosure (revealing one piece of information at a time).<br>• Dignified, respectful medical tone. | • Multi-question conversational questionnaires that exhaust elderly patients.<br>• Alarmist triage defaults ("Seek emergency care immediately").<br>• Dense English text blocks with zero audio support. |
| **Reference 4: Multimodal AI Chatbots** (*Google Gemini, ChatGPT*) | Large language model conversational interfaces. | • Natural, empathetic regional language translation.<br>• Ability to interpret colloquial Indian abbreviations (*OD, BD, TDS*). | • Monolithic walls of markdown text.<br>• Conversational bubbles (seniors struggle to parse daily medicine schedules from chat logs).<br>• Probabilistic guessing on ambiguous handwriting without confidence warnings. |
| **Reference 5: Offline Chemist Blister Strips & WhatsApp** | Physical foil strips with pencil markings (*1-0-1*); WhatsApp family chats. | • Universal visual shorthand (*1-0-1*, Morning Sun, Night Moon).<br>• One-tap WhatsApp sharing that multi-generational Indian families already use. | • Faint pencil marks that smudge or tear off.<br>• Unformatted text forwards that get lost among viral home-remedy forwards. |

---

## 3. Design Direction for Older Users on Low-Cost Android Devices

Designing for low-cost Android phones in regional Indian languages requires strict constraints around layout geometry, typography, color contrast, and linguistic morphology.

```
┌────────────────────────────────────────────────────────────────────────┐
│ DESIGN SYSTEM CONSTRAINTS FOR BHARAT HARDWARE & ELDERLY USERS          │
├────────────────────────────────────────────────────────────────────────┤
│ • Viewport: 360px CSS width (Redmi 9A, Samsung Galaxy M04)             │
│ • Scripts: Kannada (Unicode complex script) + Latin Indian English      │
│ • Minimum Touch Target: 56px height, 12px separation                   │
│ • Contrast: WCAG AAA compliance (>7:1 on text)                         │
│ • Zero Truncation: No CSS ellipsis on medicine names or instructions   │
└────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Layout & Ergonomics (The Elderly Thumb Zone)
* **Single Column Architecture:** 100% vertical stack layout. Zero horizontal scrolling, zero multi-column table grids that get cut off on 360px displays.
* **Thumb Zone Optimization:** All primary action buttons (Camera, Audio Playback, WhatsApp Share) are anchored within the lower 60% of the screen height, accommodating restricted joint mobility in older hands.
* **Touch Targets $\ge 56\text{px}$:** All interactive touch targets have a minimum dimension of $56 \times 56\text{px}$, with at least $12\text{px}$ spacing between adjacent tappable elements to prevent accidental mis-taps caused by hand tremors.

### 3.2 Typography & Indic Script Considerations
* **Complex Script Geometry (Kannada `ಕನ್ನಡ`):**
  * Kannada script features tall vowel matras (ascenders like `ೀ`, `ೇ`) and subscript consonant conjuncts (ottakshara like `್ಕ`, `್ತ್ರ`).
  * Standard Latin line-heights ($1.2–1.4$) will clip Kannada conjuncts. **Mandatory line-height: $1.65–1.8$ for all regional text.**
* **Long Compound Words:** Agglutinative regional languages produce long terms (e.g., *"ಉಪಹಾರಕ್ಕೆ ಮುನ್ನ"*, *"ಔಷಧೋಪಚಾರ"*).
  * **Rule: Zero Text Ellipsis.** Never use `overflow: hidden; text-overflow: ellipsis; white-space: nowrap;` on medicine cards. A truncated medicine name (*"Metoprol..."* vs *"Metformin..."*) can cause fatal clinical errors. Text must wrap cleanly onto the next line.
* **Font Stacks:**
  ```css
  font-family: 'Noto Sans Kannada', 'Baloo Tamma 2', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  ```
* **Font Sizing:**
  * Default body text: **$16\text{px}–18\text{px}$**
  * Medicine Names: **$20\text{px}–22\text{px}$ (Bold 800)**
  * Time-of-Day slot numbers: **$18\text{px}$ (Bold 700)**
  * Large Text Mode (Toggleable): Increases base body to **$20\text{px}$** and titles to **$24\text{px}$**.

### 3.3 Colour Palette & Contrast
To combat poor TN/budget LCD panels and harsh outdoor sunlight glare, colors are chosen for maximum optical clarity:

* **Background:** `#F8FAF6` (Soft warm paper; eliminates harsh blue-light glare and reduces eye strain).
* **Primary Brand / Action Ink:** `#285F4C` (Deep Ayurvedic forest green; creates an approachable clinical feel while delivering $>7.5:1$ contrast against white/paper).
* **Text / Surface Ink:** `#192A24` (Deep obsidian green/black; delivers $14:1$ contrast against `#FFFFFF` cards, surpassing WCAG AAA).
* **Safety / Amber Alert (Unreadable Cursive):**
  * Background: `#FEF3C7` (Warm cream)
  * Border: `#F59E0B` ($2\text{px}$ solid amber)
  * Text: `#92400E` (Deep amber-brown, $>6:1$ contrast)
* **Time-of-Day Iconography:**
  * ☀️ Morning: Warm Gold (`#D97706`)
  * 🌤️ Afternoon: Soft Sky (`#0284C7`)
  * 🌙 Night: Calm Indigo (`#4338CA`)

### 3.4 Spacing & Visual Hierarchy
* **Container Padding:** $16\text{px}$ horizontal gutter (leaves $328\text{px}$ usable width on $360\text{px}$ screens).
* **Card Separation:** $14\text{px}$ vertical gap between cards.
* **Visual Icon Reinforcement:** Every temporal instruction is paired with both a text label and a recognized symbol (☀️ Sun for morning, 🍽️ Plate for meals) so low-literacy users can parse the card without reading every character.

### 3.5 Tone of Voice
* **Reassuring & Respectful:** Addresses the user with dignity. Uses polite Kannada honorifics (*"ದಯವಿಟ್ಟು ಗಮನಿಸಿ"*, *"ನಿಮ್ಮ ವೈದ್ಯರಲ್ಲಿ ಖಚಿತಪಡಿಸಿ"*).
* **Anti-Alarmist & Non-Diagnostic:** Uses clear, neutral language: *"ವೈದ್ಯರು ಬರೆದ ವಿವರ"* (*"Instructions written by your doctor"*). Never uses panic-inducing words like *"ರೋಗ ಲಕ್ಷಣ"* (*"Disease symptom"*) or *"ಅಪಾಯಕಾರಿ"* (*"Dangerous"*).
* **Transparent Humility:** When handwriting is ambiguous, the app honestly states: *"ನಾವು ಊಹೆ ಮಾಡುವುದಿಲ್ಲ"* (*"We do not guess"*), empowering the patient to consult their local chemist.

---

## 4. Visual References & Generated Screenshots

The following reference screens were rendered headlessly at a realistic mobile viewport ($360 \times 800\text{px}$) and are preserved in [`docs/references/`](file:///c:/Users/beere/reportsaathi/docs/references):

| Reference Screenshot | File Link | State Represented & Visual Details |
|---|---|---|
| **01: Home Screen** | [`01-home-screen.png`](file:///c:/Users/beere/reportsaathi/docs/references/01-home-screen.png) | **Default Landing State:** Large vertical input cards (Camera, Upload, Type), Kannada/English language switcher, privacy trust badge, and prominent safety disclaimer banner. |
| **02: Loading Screen** | [`02-loading-screen.png`](file:///c:/Users/beere/reportsaathi/docs/references/02-loading-screen.png) | **Processing State:** Pulse spinner, step-by-step progress checklist, and transparent subtext explaining that handwriting is being verified without guessing. |
| **03: Schedule Screen** | [`03-results-schedule-kannada.png`](file:///c:/Users/beere/reportsaathi/docs/references/03-results-schedule-kannada.png) | **Populated Schedule State (Kannada):** Sticky audio read-aloud bar (`🔊 ಸೂಚನೆಗಳನ್ನು ಕೇಳಿ`), visual ☀️/🌤️/🌙 timing grid, 🍽️ meal relationship tags, **Amber Alert badge for ambiguous text**, and WhatsApp share button. |
| **04: Error Screen** | [`04-error-screen.png`](file:///c:/Users/beere/reportsaathi/docs/references/04-error-screen.png) | **Unreadable Image State:** Clear red warning icon, constructive photo-taking guidelines (lighting, steady camera), and full-width *"Retake Photo"* action button. |
