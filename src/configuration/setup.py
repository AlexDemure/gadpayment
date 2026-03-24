from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Postgres(BaseSettings):
    POSTGRES_HOST: str

    @property
    def psycopg(self) -> str:
        return self.POSTGRES_HOST.replace("asyncpg", "psycopg2")

    @property
    def asyncpg(self) -> str:
        return self.POSTGRES_HOST


class Rabbit(BaseSettings):
    RABBIT_HOST: str


class Security(BaseSettings):
    API_KEY: str


class Integration(BaseSettings):
    WEBHOOK: bool


configs = [
    Postgres,
    Rabbit,
    Security,
    Integration,
]


class Settings(*configs):  # type: ignore[misc]
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


settings = Settings()
