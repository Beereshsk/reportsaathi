# Aushadha Sathi

Aushadha Sathi is a mobile-friendly prescription notes assistant. It supports camera capture, image preview, manual entry, read-aloud, larger text, language switching, and sharing notes with family. It keeps entered notes in the current browser session and does not send prescription images to the API.

**OCR and AI medicine recognition are not enabled.** The app does not identify medicines, infer doses, or verify prescription details. Enter only what you can read, and confirm all details with a doctor or pharmacist.

## Run locally

Start the API in one terminal:

```powershell
cd backend
python -m pip install -r requirements.txt
python -m app.main
```

Start the frontend in a second terminal:

```powershell
cd frontend
npm start
```

Open <http://localhost:3000>. Typed instructions are sent to `POST http://localhost:5000/api/extract`; the backend parses explicit fields in memory, flags missing details, and does not save prescription data. Image OCR is not enabled; images stay in the browser.

## Checks

```powershell
cd frontend
npm test
npm run lint
npm run type-check

cd ..\backend
python run_tests.py
python lint.py
python typecheck.py
```
