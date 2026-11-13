# Architecture Decision Records (ADR): Aushadha Sathi

**Document Reference:** `docs/decisions.md`  
**Governing Rule:** `docs/AGENT.md` (Rule: "After each task, update docs/08-tasks.md and record decisions in docs/decisions.md")

---

## ADR-001: Monorepo Directory Partitioning (`frontend/`, `backend/`, `shared/`)
* **Date:** 2026-11-13
* **Status:** Accepted (Milestone 1, Task 1)
* **Context:** The project requires decoupled development streams for frontend (budget mobile web / PWA) and backend (ephemeral vision OCR & Indian clinical shorthand regex parsing), while keeping API contracts strictly synchronized without code duplication.
* **Decision:**
  - Structure repository into three isolated directories:
    1. `frontend/`: Lightweight SPA client, zero product features in walking skeleton, native fetch to backend.
    2. `backend/`: Python WSGI/ASGI service hosting `/api/health`, `/api/extract`, `/api/simplify`.
    3. `shared/`: Single source of truth for contract types (`types.ts`, `openapi.json`), imported by both tiers.
* **Consequences:** Changes to endpoints or schemas require simultaneous updates to `shared/` and `docs/06a-api-contract.md`.

---

## ADR-002: Ephemeral Database Isolation for Health Monitoring
* **Date:** 2026-11-13
* **Status:** Accepted (Milestone 1, Task 1)
* **Context:** Task 1 requires `GET /api/health` to demonstrate reading a value from a database, while strict regulatory rules (`DPDP Act 2023 §8(7)` and `docs/06-architecture.md`) mandate zero persistent storage of medical prescription images or patient data.
* **Decision:**
  - Introduce an isolated SQLite database (`backend/health.db`) with support for `DATABASE_URL` environment variable overrides.
  - Dedicate the database exclusively to infrastructure/operational health checks (`system_health` table).
  - Explicitly prohibit storing patient data, prescription images, or clinical transcription logs in any database.
* **Consequences:** Upholds DPDP zero-persistence mandate while providing real database verification on the walking skeleton frontend.

---

## ADR-003: Contract-First Validation with OpenAPI 3.1 & 10 Core Fixtures
* **Date:** 2026-11-13
* **Status:** Accepted (Milestone 1, Task 1)
* **Context:** Task 01 (PR-01) Definition of Done mandates zero OpenAPI syntax errors, deterministic response matching `rx-01-clean-standard.json`, and validation against the 10 fixtures in `tests/fixtures/`.
* **Decision:**
  - Specify OpenAPI 3.1.0 schema in `shared/openapi.json`.
  - Provide Pydantic models in `backend/app/models/schemas.py` and TypeScript interfaces in `shared/types.ts`.
  - Implement contract test suite in `backend/tests/test_contract.py` validating all 10 fixtures.
* **Consequences:** All future endpoints and pull requests must validate against this contract.

---

## ADR-004: Dual-Layer Testing Strategy (Zero-Network Sandboxed + CI Pipeline)
* **Date:** 2026-11-13
* **Status:** Accepted (Milestone 1, Task 1)
* **Context:** Local sandbox development operates in strict zero-network mode, while CI runners (GitHub Actions) run full dependency installation.
* **Decision:**
  - Provide lightweight test and lint runners (`run_tests.py`, `typecheck.py`, `lint.py` in backend; `run_tests.js`, `typecheck.js`, `lint.js` in frontend) using Python `unittest` and Node `node:test` that run instantaneously with zero external network downloads.
  - In CI (`.github/workflows/ci.yml`), run full `pip install -r requirements.txt` and `node:test` plus automated smoke test.
* **Consequences:** Fast local development loops with 100% test pass rate in sandboxed environments, backed by comprehensive CI validation on GitHub.

---

## ADR-005: Staging Deployment Strategy (Render + Vercel)
* **Date:** 2026-11-13
* **Status:** Accepted (Milestone 1, Task 1)
* **Context:** Continuous staging deployment required for both frontend and backend.
* **Decision:**
  - Backend: Containerized Python web service configured via `backend/render.yaml` and `backend/Dockerfile` deployable to Render Free Tier or Hugging Face Spaces.
  - Frontend: Static web app with API proxy rewrite configured via `frontend/vercel.json`.
  - GitHub Actions: `.github/workflows/staging.yml` triggers automated deployment and post-deploy health check.
* **Consequences:** Low maintenance, zero hosting cost, fast staging feedback.

---

## ADR-006: Local Development Runs Frontend and API Separately
* **Date:** 2026-11-13
* **Status:** Accepted
* **Context:** The frontend needs to send user-entered prescription notes to the backend while preserving the product's no-retention rule.
* **Decision:** Run the frontend from `frontend/` with `npm start`; run the API from `backend/` with `python -m app.main`. `POST /api/notes` validates and returns the entered text in the response only; it never writes notes to the database. The frontend must not display mock extraction results as readings from a user's prescription.
* **Consequences:** Manual notes require the API and are processed in request memory only. Image recognition requires a real approved implementation before it can be enabled.

---

## ADR-007: Run CI Smoke Tests as a Python Module
* **Date:** 2026-11-13
* **Status:** Accepted
* **Context:** Executing `backend/tests/test_smoke.py` by file path makes Python use the tests directory as its import root, so the `backend` package cannot be resolved in CI.
* **Decision:** Invoke the smoke suite from the repository root with `python -m unittest backend.tests.test_smoke`.
* **Consequences:** The test runner uses the same package imports as the regular backend test suite and passes in CI's repository-root working directory.
