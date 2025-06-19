from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: str
    redis_host: str
    redis_port: str
    celery_timezone: str

    @property
    def driver_database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def celery_broker_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    @property
    def celery_result_backend(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
