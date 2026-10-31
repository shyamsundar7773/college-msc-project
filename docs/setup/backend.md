# Backend setup and PostgreSQL

## Local backend

From PowerShell:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is at <http://localhost:8000>, its process health check is
<http://localhost:8000/health>, and OpenAPI docs are at
<http://localhost:8000/docs>. The database readiness probe is
`GET /api/v1/health/database`; it executes `SELECT 1` and returns HTTP 503 if
the database URL is missing or PostgreSQL cannot be reached.

## Local PostgreSQL

The project's local PostgreSQL 18 service is expected at `127.0.0.1:3000`.
Use the `customer_intelligence_hub` database and `cih_app` role. Do not use
the unrelated `customer_churn_db` database.

After creating the database and role, add the URL to `backend/.env` manually:

```dotenv
DATABASE_URL=postgresql+psycopg://cih_app:URL_ENCODED_PASSWORD@127.0.0.1:3000/customer_intelligence_hub
```

No database password is included in this repository. If the password contains
reserved URL characters, percent-encode it first; for example, locally use
Python's `urllib.parse.quote(password, safe="")`. SQLAlchemy's `make_url`
parses the URL and the engine receives a SQLAlchemy `URL` object. Never print
the URL or place it in frontend configuration.

With `DATABASE_URL` configured, verify the role and database interactively:

```powershell
psql -h 127.0.0.1 -p 3000 -U cih_app -d customer_intelligence_hub -c "SELECT current_database(), current_user, inet_server_port();"
```

`psql` prompts for the password. The application verification is
`GET /api/v1/health/database`, which executes `SELECT 1`. No business tables
or migrations are part of Phase 0.

## Connection lifecycle

The backend creates one lazily initialized SQLAlchemy engine with
`pool_pre_ping`; it validates that the configured dialect is PostgreSQL via
Psycopg 3, so no SQLite fallback is used. `get_db` yields a SQLAlchemy session
and closes it after the request. The application disposes the engine pool on
shutdown. Database errors at the readiness route produce a generic 503 without
returning connection details or credentials.
