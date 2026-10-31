# Architecture overview

Customer Intelligence Hub is a single application with a React/TypeScript
frontend and a Python/FastAPI backend. The frontend calls versioned endpoints
under `/api/v1`; its base URL comes from `VITE_API_BASE_URL`. PostgreSQL access
is prepared behind a lazy SQLAlchemy engine in `backend/app/db/session.py`.
No tables, migrations, or database connection checks are part of Phase 0.

Backend modules separate HTTP routes, configuration, database access, schemas,
services, and future ML code. Gemini belongs behind a backend service boundary
and may explain verified model outputs. Trained models produce churn
probabilities; SHAP and LIME produce their own explanations. Gemini must not
invent predictions or explanation values.

The frontend setup includes React Router, Tailwind CSS v4's Vite plugin,
Lucide icons, Framer Motion, and Plotly for later phases. Only the setup health
page is implemented now. Counterfactual tooling will be selected after a
compatibility evaluation with the eventual model and data pipeline.
