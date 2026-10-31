# Phase 0 Setup Report

**Project:** Customer Intelligence Hub  
**Audit date:** 31 October 2026  
**Scope:** Phase 0 foundation, PostgreSQL integration, and deployment preparation. Dashboard and Phase 1 work have not started.

## 1. Project overview

The repository began with only its `.git` metadata and no project files. Phase 0 adds the requested React + TypeScript frontend, FastAPI backend, configuration boundaries, data placeholders, and setup documentation. The frontend is a small development health page; it is not the product dashboard.

## 2. Final folder structure

```text
college-msc-project/
├── backend/
│   ├── app/
│   │   ├── api/             # Versioned health route
│   │   ├── core/            # Settings and logging
│   │   ├── db/              # Lazy SQLAlchemy engine
│   │   ├── ml/              # Reserved for later model code
│   │   ├── schemas/         # Reserved for API schemas
│   │   ├── services/        # Gemini boundary
│   │   └── main.py
│   ├── .env.example
│   └── requirements.txt
├── data/
│   ├── raw/.gitkeep
│   ├── processed/.gitkeep
│   └── README.md
├── docs/
│   ├── architecture/overview.md
│   └── setup/              # backend, environment, deployment
├── frontend/
│   ├── public/.gitkeep
│   ├── src/                 # Health page and API client
│   ├── .env.example
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig*.json
│   └── vite.config.ts
├── .gitignore
├── netlify.toml
├── render.yaml
├── README.md
└── PHASE_0_SETUP_REPORT.md
```

Local `.env` files and generated dependency/build directories are excluded from Git.

## 3. Technology stack

- Frontend: React, TypeScript, Vite, Tailwind CSS v4, React Router, Lucide, Framer Motion, Plotly.
- Backend: Python 3.12, FastAPI, Uvicorn, Pydantic Settings, Pandas, NumPy, scikit-learn.
- Database: SQLAlchemy 2 engine/session factory and Psycopg 3. Engine creation is lazy, a request-scoped session dependency closes sessions, and the readiness probe executes `SELECT 1`. No tables or migrations were created.
- Gemini: configuration-only service boundary; no SDK or API call is included in Phase 0.

## 4. Files created or modified in the PostgreSQL/deployment pass

- Modified: `backend/app/db/session.py`, `backend/app/api/health.py`, `backend/app/main.py`, `README.md`, `docs/setup/environment.md`, and this report.
- Added: `docs/setup/backend.md`, `docs/setup/deployment.md`, `netlify.toml`, and `render.yaml`.
- `backend/.env` was not changed; its `DATABASE_URL` remains blank and its existing Gemini configuration was preserved. `backend/.env.example` was checked and is safe to track: the database URL and key are blank, with only nonsecret defaults set.
- No existing automated test files were found. No business tables or migrations were added.

## 5. Frontend setup status

**PASS** — `npm install` completed; npm reported zero vulnerabilities.  
**PASS** — `npm run build` completed successfully with TypeScript checking and Vite production bundling.  
**PASS** — Vite development server started at `http://127.0.0.1:5173`; an HTTP request returned 200.  
**PASS** — API client reads `VITE_API_BASE_URL`, with a local API fallback when the variable is blank.

The npm installer initially blocked package install scripts by default. The required `esbuild` script was approved to enable Vite builds; the optional `es5-ext` postinstall script remained blocked and did not prevent installation or build.

## 6. Backend setup status

**PASS** — `pip install -r requirements.txt` completed in the ignored Python 3.12 virtual environment.  
**PASS** — Uvicorn started the FastAPI application on port 8000.  
**PASS** — `GET /health`, `GET /api/v1/health`, and `/docs` responded successfully.  
**PASS** — The database readiness route returns a generic HTTP 503 when `DATABASE_URL` is missing; it does not return configuration details.  
**PASS** — CORS preflight for `http://localhost:5173` succeeded.  
**PASS** — PostgreSQL engine parsing rejects non-PostgreSQL/SQLite URLs. A test URL with percent-encoded reserved password characters parsed correctly.  
**PASS** — SQLAlchemy engine disposal is wired into FastAPI shutdown; request-scoped sessions close after use.

The deployment command should bind to the platform-provided `PORT` variable. No `PORT` value is hardcoded in application configuration.

## 7. PostgreSQL status

**PASS** — Windows service `postgresql-x64-18` is running and `pg_isready` reports that `127.0.0.1:3000` accepts connections.  
**NOT TESTED** — `backend/.env` has a blank `DATABASE_URL`. A noninteractive `psql` attempt using `cih_app` and the requested database failed because no password was supplied; no SQL statement reached the server. The API readiness route correctly returns HTTP 503 while the URL is unset.  
**NOT TESTED** — No SQLAlchemy connection or real SQL query has succeeded yet. No business tables or migrations were created. The existing `customer_churn_db` was not used or modified.

Manual action: enter the connection URL in `backend/.env` at `DATABASE_URL=`. Use `postgresql+psycopg://cih_app:URL_ENCODED_PASSWORD@127.0.0.1:3000/customer_intelligence_hub`; percent-encode reserved characters in the password. Do not paste the password into chat or commit the file. After setting it, rerun the SQLAlchemy readiness check and query.

## 8. Gemini AI preparation status

**PASS** — Backend configuration sets model ID `gemini-3.5-flash-lite`; `GEMINI_API_KEY` remains backend-only. A service boundary documents that Gemini may explain verified analytical outputs and must not invent predictions or SHAP/LIME results.  
**NOT TESTED** — No Gemini request or API credit was used. A value is present in local environment configuration; its contents are intentionally omitted from this report and were not sent to the API.

During the initial local configuration audit, the key value was inadvertently included in a diagnostic command output. Rotate that key in the provider console before using it. The value is not repeated in this report.

Edit Gemini settings locally in `backend/.env`. Keep the key out of source code, frontend variables, chat, and Git.

## 9. Environment variables

| Variable | Purpose |
| --- | --- |
| `VITE_API_BASE_URL` | Browser-visible backend base URL; blank uses `http://localhost:8000`. Never put a private key here. |
| `APP_ENV` | Backend environment label. |
| `DATABASE_URL` | PostgreSQL connection URL. |
| `GEMINI_API_KEY` | Private backend Gemini key. |
| `GEMINI_MODEL` | `gemini-3.5-flash-lite`. |
| `CORS_ORIGINS` | Comma-separated allowed origins; configured locally as `http://localhost:5173`. |
| `FRONTEND_ORIGIN` | Configured locally as `http://localhost:5173`. |
| `MAX_UPLOAD_SIZE_MB` | Configured to `1024` MB; Settings parses this as an integer. |

Render should receive the seven backend variables as service settings. Netlify should receive `VITE_API_BASE_URL` at build time; Vite variables are public to browser users.

## 10. Git and GitHub inspection

- Current branch: `master`.
- Commits: none; repository has no commit history yet.
- Initial working tree: clean; after setup, new project files are untracked.
- Remote: `origin` is configured as `https://github.com/shyamsundar7773/college-msc-project.git`; it was added during the environment correction because no remote existed.
- Git identity is available from global configuration.
- No branch change, commit, push, or history rewrite was performed.

## 11. Local commands and URLs

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Backend:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Frontend: <http://localhost:5173>
- Backend: <http://localhost:8000>
- Health: <http://localhost:8000/health>
- API health: <http://localhost:8000/api/v1/health>
- API docs: <http://localhost:8000/docs>
- Database readiness (executes `SELECT 1`): <http://localhost:8000/api/v1/health/database>

See the root README and `docs/setup/environment.md` for PostgreSQL and deployment configuration.

## 12. Test summary

| Check | Result | Evidence |
| --- | --- | --- |
| Frontend dependency installation | PASS | `npm ci` completed; 0 vulnerabilities reported. |
| Frontend production build | PASS | `npm run build` completed. |
| Frontend local startup | PASS | Vite served an HTTP 200 response. |
| Backend dependency installation | PASS | `pip install -r requirements.txt` completed under Python 3.12. |
| FastAPI startup | PASS | Uvicorn startup completed on port 8000. |
| `GET /health` | PASS | Exact expected status and service returned. |
| `GET /api/v1/health` | PASS | API-specific health response returned. |
| Database readiness error handling | PASS | Missing `DATABASE_URL` returns generic HTTP 503. |
| CORS configuration | PASS | Allowed-origin preflight returned HTTP 200 with the configured origin. |
| Environment settings load | PASS | Backend settings load; `DATABASE_URL` is blank and no credential value is emitted. |
| `.env` ignore rules | PASS | Root and nested `.env`, backend `.venv`, frontend `node_modules` and `dist`, and local dataset paths matched ignore rules. |
| `.env.example` templates | PASS | Frontend and backend templates are present and Git-visible. |
| Secret values in source files | PASS | No API keys or database credentials were added to application source. Local environment values are excluded from Git and redacted here. |
| Frontend API configuration | PASS | Variable-based API base URL and local fallback are implemented. |
| PostgreSQL service readiness | PASS | PostgreSQL service is running and accepts connections on `127.0.0.1:3000`. |
| PostgreSQL authentication as `cih_app` | NOT TESTED | App `DATABASE_URL` is blank; `psql -w` confirms no password was supplied. |
| SQLAlchemy connection | NOT TESTED | Requires the local `DATABASE_URL` to be populated manually first. |
| Real SQL query on `customer_intelligence_hub` | NOT TESTED | No credentials were available to this project process, so no SQL statement was executed against the target database. |
| SQLite fallback rejection | PASS | Explicit SQLite URL was rejected before engine creation; no SQLite file was created. |
| Special-character URL parsing | PASS | SQLAlchemy parsed a test URL with percent-encoded reserved password characters. |
| Gemini integration | NOT TESTED | No request made; configuration boundary only. |
| Netlify/Render configuration files | PASS | TOML and YAML parsed; build, start, `$PORT`, and health-check settings were checked. No deployment was performed. |
| Folder structure and documentation | PASS | Backend, environment, PostgreSQL, and deployment docs are present. |

## 13. Errors and unresolved issues

- PostgreSQL is listening, but the backend cannot authenticate until `DATABASE_URL` is set in `backend/.env`.
- The local DB query remains unverified. Hosted Render/Netlify deployment settings have not been exercised.
- No automated test suite exists yet; verification in this report used install/build, HTTP, configuration, and live-service checks.

## 14. Manual setup steps

1. Add the local `postgresql+psycopg://cih_app:URL_ENCODED_PASSWORD@127.0.0.1:3000/customer_intelligence_hub` URL to `DATABASE_URL=` in `backend/.env`. Encode reserved password characters; do not send the password through chat.
2. Restart the backend and verify `/api/v1/health/database`, then run a real `SELECT current_database(), current_user, inet_server_port()` query as `cih_app`.
3. Rotate and replace the Gemini key manually; keep it backend-only. The configured model ID is `gemini-3.5-flash-lite`.
4. Before deployment, set real `CORS_ORIGINS` / `FRONTEND_ORIGIN` in Render and `VITE_API_BASE_URL` in Netlify.
5. Place the IBM Telco CSV in `data/raw/` only when the dataset phase begins. It will remain ignored by Git.

## 15. Completion and recommendation

No commit, push, deployment, cloud resource creation, database migration, or Phase 1 implementation was performed. Frontend/backend local foundation checks pass, PostgreSQL deployment configuration is prepared, and the database service is listening. **Phase 0 PostgreSQL integration is not complete yet:** the project `DATABASE_URL` is blank, so authentication and a real SQL query remain untested. Once that URL is entered locally and the real query passes, the final database integration verification can be completed.
