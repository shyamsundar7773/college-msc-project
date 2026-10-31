# Environment and deployment settings

Copy the example files when setting up a new machine. The local `.env` files
are ignored by Git. Keep backend secrets in `backend/.env` only.

| Variable | Location | Purpose |
| --- | --- | --- |
| `VITE_API_BASE_URL` | `frontend/.env`; Netlify | Public API origin used by browser requests. Browser-visible; never put secrets here. Blank uses the frontend's local `http://localhost:8000` fallback. |
| `APP_ENV` | backend; Render | Environment label, default `development`. |
| `DATABASE_URL` | backend; Render | PostgreSQL SQLAlchemy connection URL. |
| `GEMINI_API_KEY` | backend; Render | Private Gemini API key. It belongs only in the backend environment, never in frontend variables or source code. |
| `GEMINI_MODEL` | backend; Render | Gemini model ID: `gemini-3.5-flash-lite`. |
| `CORS_ORIGINS` | backend; Render | Comma-separated browser origins allowed by the API. Local value: `http://localhost:5173`. |
| `FRONTEND_ORIGIN` | backend; Render | Frontend origin added to allowed CORS origins. Local value: `http://localhost:5173`. |
| `MAX_UPLOAD_SIZE_MB` | backend; Render | Maximum upload size setting: `1024` MB. |

Render should receive the seven backend variables above as service environment
settings. Do not hardcode a `PORT`; launch Uvicorn with the platform-provided
`$PORT` (or `PORT` on Windows). Netlify needs `VITE_API_BASE_URL` at build
time. Vite variables are bundled into public browser code.

To add Gemini later, create a key in Google's developer console and paste it
manually into the local `backend/.env` as `GEMINI_API_KEY=...`. Do not share it
in chat, commit it, or place it in any `VITE_` variable. Phase 0 does not make
Gemini API calls.

## Local service URLs

- Frontend: <http://localhost:5173>
- Backend: <http://localhost:8000>
- API health: <http://localhost:8000/health>
- FastAPI docs: <http://localhost:8000/docs>

The local PostgreSQL database name is `customer_intelligence_hub`. Set
`DATABASE_URL` in `backend/.env` after creating that database, using the
SQLAlchemy Psycopg driver format:

```text
postgresql+psycopg://cih_app:URL_ENCODED_PASSWORD@127.0.0.1:3000/customer_intelligence_hub
```

Percent-encode reserved characters in the password first; Python's
`urllib.parse.quote(password, safe="")` does this. Keep the URL in the backend
environment only.

The database readiness probe at `/api/v1/health/database` executes `SELECT 1`.
It returns HTTP 503 when the URL is not configured or the connection fails.
This local connection must be verified separately from Render's hosted database.
