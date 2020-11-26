from datetime import timedelta
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    APP_ENV: str = "development"
    API_V1_STR: str = "/api/v1"
    AUTHJWT_SECRET_KEY: str
    AUTHJWT_ACCESS_TOKEN_EXPIRE: timedelta = timedelta(minutes=10)
    AUTHJWT_HEADER_NAME: str = "X-Access-Token"
    AUTHJWT_HEADER_TYPE: str = None
    AUTHJWT_DENYLIST_ENABLED: bool = True
    AUTHJWT_DENYLIST_TOKEN_CHECKS: set = {"access", "refresh"}

    GRAVATAR_DEFAULT_URL: str = (
        "https://www.gravatar.com/avatar/00000000000000000000000000000000"
    )

    SERVER_HOST: AnyHttpUrl

    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        case_sensitive = False


settings = Settings()
