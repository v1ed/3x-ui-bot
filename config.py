import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    # SERVER_LOGIN: str
    # SERVER_PASSWORD: str
    # SERVER_HOSTNAME: str
    # SERVER_PORT: str
    # SERVER_WEBPATH: str
    BOT_TOKEN: str
    model_config = model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    )

settings = Settings()

def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")