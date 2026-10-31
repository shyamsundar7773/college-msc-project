# Deployment architecture preparation

Deployment is prepared but has not been performed. No production domain,
credential, cloud database, or service URL is included or assumed.

## Netlify frontend

`netlify.toml` sets the base directory to `frontend`, runs `npm run build`,
and publishes `dist`. In Netlify's site environment settings, set
`VITE_API_BASE_URL` to the actual deployed Render API origin after deployment.
This value is bundled into browser code and must contain no secret. Netlify's
documentation recommends managing environment variables through its UI, CLI,
or API when values should not be stored in the repository.

## Render backend

`render.yaml` describes a Python web service that installs
`backend/requirements.txt`, starts Uvicorn on the platform-provided `$PORT`,
and uses `/health` as the Render process health check. It does not declare or
create a database resource.

Set these values in Render's service environment before deployment:

- `DATABASE_URL`: URL for a separate hosted PostgreSQL database.
- `CORS_ORIGINS` and `FRONTEND_ORIGIN`: the real Netlify site origin(s), with
  no invented or placeholder production URL.
- `GEMINI_API_KEY`: private backend secret, if/when Gemini is enabled.
- `APP_ENV=production`, `GEMINI_MODEL`, and `MAX_UPLOAD_SIZE_MB` as declared
  in `render.yaml`.

When the Render backend and PostgreSQL database share a supported private
network and region, prefer the database's internal connection URL. Never use
the local Windows address `127.0.0.1:3000` in production. Keep the hosted
database separate from local PostgreSQL and do not reuse `customer_churn_db`.

Render's `/health` check reports that the API process is alive. The separate
`/api/v1/health/database` endpoint tests the configured database with `SELECT
1`; it can be used for manual readiness checks without making a missing
database take the API process health check offline.

## Remaining deployment steps

1. Create the hosted PostgreSQL resource manually in Render and choose its
   region/network placement; this project does not create cloud resources.
2. Add the hosted connection URL and production CORS/API settings in Render.
3. Create/configure the Netlify site and set `VITE_API_BASE_URL` to the actual
   Render API URL.
4. Deploy only after the production variables and data connection have been
   reviewed. No deployment has been run as part of Phase 0.
