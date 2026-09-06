from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CloudTask AI Development API"
    app_version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True

    database_url: str

    secret_key: str

    algorithm: str = "HS256"

    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
