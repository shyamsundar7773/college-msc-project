# Customer Intelligence Hub

**An Explainable Customer Intelligence Framework for Churn Prediction and Cost-Aware Retention Prioritisation.**

An M.Sc. Data Science and AI project foundation. The planned application will
combine a React + TypeScript frontend with a FastAPI backend, PostgreSQL, and
explainable machine-learning workflows. Phase 0 provides a local health page,
API health endpoints, configuration boundaries, and setup documentation. It
does not yet implement the analytics dashboard, dataset pipeline, database
tables, model training, or Gemini calls.

## Requirements

- Node.js 20.19+ or 22.12+ and npm
- Python 3.10+
- PostgreSQL for later database-backed phases

## Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open <http://localhost:5173>. Set `VITE_API_BASE_URL` in `frontend/.env` when
the backend is hosted elsewhere. A blank value uses `http://localhost:8000`.

## Backend

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open <http://localhost:8000/health>, <http://localhost:8000/api/v1/health>,
or <http://localhost:8000/docs>. For Render or another platform, bind Uvicorn
to the supplied `PORT` environment variable rather than a hardcoded port.

## PostgreSQL

PostgreSQL 18 is expected locally on `127.0.0.1:3000`. Create the
`customer_intelligence_hub` database and use the `cih_app` role. Enter the
connection URL manually in `backend/.env` as `DATABASE_URL` (the password is
not stored in the example):

```text
postgresql+psycopg://cih_app:URL_ENCODED_PASSWORD@127.0.0.1:3000/customer_intelligence_hub
```

Replace the placeholder locally; never commit the URL. Percent-encode reserved
characters in the password (for example, use Python's
`urllib.parse.quote(password, safe="")`) before placing it in the URL. The
backend parses the URL with SQLAlchemy's URL parser and passes a URL object to
the engine. Phase 0 creates no business tables and applies no migrations.
The `customer_churn_db` database is unrelated and must not be used.

## Gemini and upload configuration

The configured Gemini model ID is `gemini-3.5-flash-lite`. Keep
`GEMINI_API_KEY` only in `backend/.env` or the backend hosting environment;
never put it in frontend variables or source code. Phase 0 does not make
Gemini API calls. `MAX_UPLOAD_SIZE_MB` is configured to `1024` MB.

## Local URLs

- Frontend: <http://localhost:5173>
- Backend: <http://localhost:8000>
- Backend health: <http://localhost:8000/health>
- FastAPI docs: <http://localhost:8000/docs>

The database connectivity probe is available at
<http://localhost:8000/api/v1/health/database>; it runs `SELECT 1` and returns
HTTP 503 when `DATABASE_URL` is missing or the database is unavailable.

## Deployment preparation

The repository includes `netlify.toml` and `render.yaml` as deployment
configuration templates. No production URLs or credentials are included.
Configure `VITE_API_BASE_URL` in Netlify's site environment for the deployed
API. Configure `DATABASE_URL`, `CORS_ORIGINS`, `FRONTEND_ORIGIN`, and
`GEMINI_API_KEY` in Render's service environment. Use a separate hosted
PostgreSQL database for production and prefer its internal connection URL when
the Render services share a supported private network. See
[`docs/setup/deployment.md`](docs/setup/deployment.md).

## Data

When dataset work begins, place the IBM Telco Customer Churn CSV in
`data/raw/`. Raw and processed data are Git-ignored. See [data/README.md](data/README.md).

## Configuration and deployment

See [docs/setup/environment.md](docs/setup/environment.md) and the
`frontend/.env.example` and `backend/.env.example` templates. Backend secrets
stay on the backend. Netlify uses `VITE_API_BASE_URL`; Render uses
`APP_ENV`, `DATABASE_URL`, `GEMINI_API_KEY`, `GEMINI_MODEL`, `CORS_ORIGINS`,
`FRONTEND_ORIGIN`, and `MAX_UPLOAD_SIZE_MB` as service settings.

## Project layout

- `frontend/` — Vite React application and API client
- `backend/app/` — FastAPI routes, configuration, database, services, schemas, and ML boundaries
- `data/` — ignored local raw and processed datasets
- `docs/` — architecture and setup notes
- `PHASE_0_SETUP_REPORT.md` — initial audit and verification results
