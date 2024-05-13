from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    DB_URL: str = "postgresql+asyncpg://curso:curso@localhost:5432/cursofastapi"

    class Config:
        case_sensitive = True

settings: Settings = Settings()
