"""SQLAlchemy engine, session lifecycle, and connection verification."""

from collections.abc import Iterator
from functools import lru_cache

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.exc import ArgumentError
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


@lru_cache
def get_engine() -> Engine:
    database_url = get_settings().database_url.strip()
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")
    try:
        url = make_url(database_url)
    except ArgumentError as exc:
        raise RuntimeError("DATABASE_URL is invalid") from exc
    if url.get_backend_name() != "postgresql" or url.get_driver_name() != "psycopg":
        raise RuntimeError("DATABASE_URL must use PostgreSQL with the Psycopg 3 driver")
    return create_engine(url, pool_pre_ping=True, connect_args={"connect_timeout": 5})


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    """FastAPI dependency that closes each SQLAlchemy session after use."""
    session = get_session_factory()()
    try:
        yield session
    finally:
        session.close()


def verify_database_connection() -> None:
    """Run a minimal query to verify connectivity without creating tables."""
    with get_engine().connect() as connection:
        connection.execute(text("SELECT 1"))


def dispose_engine() -> None:
    """Close pooled connections during application shutdown if initialized."""
    if get_engine.cache_info().currsize:
        get_engine().dispose()
