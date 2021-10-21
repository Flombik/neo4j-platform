import secrets
from typing import Union

from pydantic import BaseSettings, AnyHttpUrl, IPvAnyAddress


class Settings(BaseSettings):
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_HOST: Union[AnyHttpUrl, IPvAnyAddress]
    SERVER_PORT: int
    SQLALCHEMY_DATABASE_URL: str

    class Config:
        case_sensitive = True


settings = Settings()
