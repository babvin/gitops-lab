from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration, overridable via environment variables.

    e.g. SAMPLE_API_LOG_LEVEL=debug
    """

    model_config = SettingsConfigDict(env_prefix="SAMPLE_API_")

    service_name: str = "sample-api"
    version: str = "0.1.0"
    log_level: str = "info"


@lru_cache
def get_settings() -> Settings:
    return Settings()
