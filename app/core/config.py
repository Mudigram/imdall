from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Environment
    ENV: str = "local"

    # Database
    DATABASE_URL: str

    # Scheduler
    METRICS_INTERVAL_MINUTES: int = 5
    ALERT_FAILURE_THRESHOLD: int = 5

    # App
    APP_NAME: str = "Imdall"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()
