from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = ""
    gemini_api_key: str = ""
    gemini_model: str = ""
    cors_origins: str = ""
    frontend_origin: str = ""
    max_upload_size_mb: int | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("max_upload_size_mb", mode="before")
    @classmethod
    def blank_upload_limit_is_unset(cls, value: object) -> object:
        return None if value == "" else value

    @property
    def allowed_origins(self) -> list[str]:
        origins = [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        if self.frontend_origin.strip():
            origins.append(self.frontend_origin.strip())
        if not origins and self.app_env == "development":
            origins.append("http://localhost:5173")
        return list(dict.fromkeys(origins))


@lru_cache
def get_settings() -> Settings:
    return Settings()
