from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://curso:curso@localhost:5432/cursofastapi"
    DBBaseModel: ClassVar = declarative_base()

    JWT_SECRET: str = "0dpdlL2l9oZCADJAKsS94Veq2748mgr_xHUHwTekqsk"
    """
    import secrets

    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = "HS256"

    # 60 Minutos * 24 Horas * 7 Dias = 1 Semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True

settings: Settings = Settings()
