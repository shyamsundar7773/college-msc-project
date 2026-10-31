import logging

from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import verify_database_connection

router = APIRouter(prefix="/api/v1", tags=["health"])
logger = logging.getLogger(__name__)


@router.get("/health")
def api_health() -> dict[str, str]:
    return {"status": "ok", "service": "customer-intelligence-hub-api", "api_version": "v1"}


@router.get("/health/database")
def database_health() -> dict[str, str]:
    try:
        verify_database_connection()
    except (RuntimeError, SQLAlchemyError):
        logger.warning("Database readiness check failed")
        raise HTTPException(status_code=503, detail="Database is unavailable or not configured") from None
    return {"status": "ok", "database": "connected"}
